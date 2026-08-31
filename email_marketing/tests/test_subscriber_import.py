"""CSV/XLSX subscriber import — the service pipeline and the admin flow."""

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from email_marketing.models import Subscriber, SubscriberTag
from email_marketing.services import subscriber_importer as imp

from .base import MarketingTestCase

User = get_user_model()


def _csv(text: str) -> SimpleUploadedFile:
    return SimpleUploadedFile("contacts.csv", text.encode("utf-8"), content_type="text/csv")


class ParseAndMapTests(MarketingTestCase):
    def test_parse_reads_headers_and_rows(self):
        parsed = imp.parse_file(_csv("Email,First Name\na@x.com,Alex\nb@x.com,Bo\n"))
        self.assertEqual(parsed.headers, ["Email", "First Name"])
        self.assertEqual(parsed.row_count, 2)

    def test_auto_detect_maps_common_headers(self):
        mapping = imp.auto_detect_mapping(["Email Address", "First Name", "Surname", "Locale"])
        self.assertEqual(mapping["email"], "Email Address")
        self.assertEqual(mapping["first_name"], "First Name")
        self.assertEqual(mapping["last_name"], "Surname")
        self.assertEqual(mapping["language"], "Locale")

    def test_validate_mapping_requires_email(self):
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            imp.validate_mapping({"first_name": "First Name"}, ["First Name"])


class PartitionTests(MarketingTestCase):
    def _partition(self, text):
        parsed = imp.parse_file(_csv(text))
        mapping = imp.validate_mapping(imp.auto_detect_mapping(parsed.headers), parsed.headers)
        return imp.partition_rows(parsed.rows, mapping)

    def test_invalid_and_empty_emails_are_rejected(self):
        valid, invalid = self._partition("email\ngood@x.com\nnot-an-email\n\n")
        self.assertEqual([r["email"] for r in valid], ["good@x.com"])
        self.assertEqual(len(invalid), 1)  # blank rows are dropped in parsing, not flagged

    def test_in_file_duplicates_are_rejected_once(self):
        valid, invalid = self._partition("email\nDup@x.com\ndup@x.com\n")
        self.assertEqual([r["email"] for r in valid], ["dup@x.com"])  # normalised + deduped
        self.assertEqual(len(invalid), 1)

    def test_email_is_normalised_lowercase(self):
        valid, _ = self._partition("email\nMixed@Case.COM\n")
        self.assertEqual(valid[0]["email"], "mixed@case.com")


class FindExistingTests(MarketingTestCase):
    def test_dedup_against_existing_rows(self):
        Subscriber.objects.create(site=self.site, email="here@x.com")
        existing = imp.find_existing(self.site, ["here@x.com", "new@x.com"])
        self.assertEqual(existing, {"here@x.com"})


class ImportBatchTests(MarketingTestCase):
    def _rows(self, *emails, **extra):
        return [{"email": e, **extra} for e in emails]

    def test_creates_active_consented_import_rows(self):
        tag = SubscriberTag.objects.create(site=self.site, name="Imported", slug="imported")
        result = imp.import_batch(
            self.site,
            [{"email": "a@x.com", "first_name": "Alex", "last_name": "Rivera", "language": "es"}],
            tag=tag,
        )
        self.assertEqual(result.created, 1)
        sub = Subscriber.objects.get(email="a@x.com")
        self.assertEqual(sub.source, "import")
        self.assertEqual(sub.status, Subscriber.STATUS_ACTIVE)
        self.assertTrue(sub.marketing_opt_in and sub.marketing_verified)
        self.assertEqual(sub.consent_source, "csv_import")
        self.assertIsNotNone(sub.consent_timestamp)
        self.assertEqual(
            (sub.first_name, sub.last_name, sub.language_code), ("Alex", "Rivera", "es")
        )
        self.assertIn(tag, sub.tags.all())

    def test_skip_strategy_leaves_duplicates_untouched(self):
        Subscriber.objects.create(site=self.site, email="dup@x.com", first_name="Old")
        result = imp.import_batch(
            self.site, self._rows("dup@x.com", first_name="New"), duplicate_strategy="skip"
        )
        self.assertEqual((result.created, result.skipped), (0, 1))
        self.assertEqual(Subscriber.objects.get(email="dup@x.com").first_name, "Old")

    def test_tag_applies_to_existing_contacts_even_when_skipping(self):
        tag = SubscriberTag.objects.create(site=self.site, name="VIP", slug="vip")
        existing = Subscriber.objects.create(site=self.site, email="dup@x.com", first_name="Old")
        imp.import_batch(
            self.site, self._rows("dup@x.com", first_name="New"), duplicate_strategy="skip", tag=tag
        )
        existing.refresh_from_db()
        self.assertEqual(existing.first_name, "Old")  # name untouched under skip
        self.assertIn(tag, existing.tags.all())  # but the import tag is applied

    def test_update_strategy_refreshes_name(self):
        Subscriber.objects.create(site=self.site, email="dup@x.com", first_name="Old")
        result = imp.import_batch(
            self.site, self._rows("dup@x.com", first_name="New"), duplicate_strategy="update"
        )
        self.assertEqual((result.created, result.updated), (0, 1))
        self.assertEqual(Subscriber.objects.get(email="dup@x.com").first_name, "New")

    def test_anonymous_import_powers_first_name_merge_field(self):
        from email_marketing.merge_fields import resolve_merge_fields

        imp.import_batch(self.site, [{"email": "m@x.com", "first_name": "Sam"}])
        sub = Subscriber.objects.get(email="m@x.com")
        self.assertEqual(resolve_merge_fields("Hi [[first_name]]", sub, html=False), "Hi Sam")


class SecurityHardeningTests(MarketingTestCase):
    def test_row_cap_short_circuits_before_full_materialisation(self):
        from unittest import mock

        from django.core.exceptions import ValidationError

        text = "email\n" + "".join(f"u{i}@x.com\n" for i in range(6))
        with mock.patch.object(imp, "MAX_ROWS", 3), self.assertRaises(ValidationError):
            imp.parse_file(_csv(text))

    def test_malformed_xlsx_is_a_validation_error_not_500(self):
        from django.core.exceptions import ValidationError

        bad = SimpleUploadedFile(
            "contacts.xlsx", b"this is not a workbook", content_type="application/vnd.ms-excel"
        )
        with self.assertRaises(ValidationError):
            imp.parse_file(bad)

    def test_long_values_are_capped_at_parse_time(self):
        parsed = imp.parse_file(_csv("email,first name\na@x.com," + "N" * 500 + "\n"))
        mapping = imp.validate_mapping(imp.auto_detect_mapping(parsed.headers), parsed.headers)
        valid, _ = imp.partition_rows(parsed.rows, mapping)
        self.assertEqual(len(valid[0]["first_name"]), 100)  # capped to the field max

    def test_soft_deleted_email_is_skipped_not_a_500(self):
        # A since-deleted contact still occupies the (site,email) unique slot;
        # importing it must skip cleanly, not raise IntegrityError.
        sub = Subscriber.objects.create(site=self.site, email="gone@x.com")
        sub.delete()  # soft delete
        result = imp.import_batch(self.site, [{"email": "gone@x.com", "first_name": "Zed"}])
        self.assertEqual((result.created, result.skipped), (0, 1))
        self.assertFalse(Subscriber.objects.filter(email="gone@x.com").exists())  # still deleted


class ImportAdminFlowTests(MarketingTestCase):
    def setUp(self):
        super().setUp()
        self.admin = User.objects.create_superuser(
            username="root", email="root@test.spwig.com", password="pw"
        )
        self.client.force_login(self.admin)

    def _url(self):
        return reverse("admin:email_marketing_subscriber_import")

    def test_get_renders_upload_form(self):
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "multipart/form-data")

    def test_consent_is_required(self):
        resp = self.client.post(
            self._url(), {"file": _csv("email\na@x.com\n"), "duplicate_strategy": "skip"}
        )
        self.assertEqual(resp.status_code, 200)  # re-rendered with an error
        self.assertFalse(Subscriber.objects.filter(email="a@x.com").exists())

    def test_upload_then_confirm_imports(self):
        # Step 1: upload → preview (stashes rows on the session).
        resp = self.client.post(
            self._url(),
            {
                "file": _csv("email,first name\nnew@x.com,Nadia\n"),
                "duplicate_strategy": "skip",
                "consent_confirmed": "on",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Import now")
        # Step 2: confirm.
        resp2 = self.client.post(self._url(), {"confirm": "1"})
        self.assertEqual(resp2.status_code, 302)
        sub = Subscriber.objects.get(email="new@x.com")
        self.assertEqual((sub.source, sub.first_name), ("import", "Nadia"))
