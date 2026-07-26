"""
R1 coverage: manual gift card issuance in the admin, and the delivery email.

Two R1 fixes:

1. **A merchant could not create a funded card by hand.** ``GiftCardAdmin``
   marked ``code`` / ``initial_value`` / ``current_balance`` read-only with no
   add-form override, and the fieldsets exposed ``product_link`` (a display
   method) rather than the ``product`` FK — which is a non-nullable PROTECT
   column. The Add button rendered a form that could never save. R1 adds
   ``add_fieldsets`` / ``get_fieldsets`` / ``get_readonly_fields`` /
   ``save_model``. Editing must stay locked down: money moves through the
   ``GiftCardTransaction`` ledger, not by typing a new balance into a field.

2. **The delivery email rendered blank.** ``GiftCard.issue()`` passed
   *stringified* fields, but the template dereferences
   ``gift_card.current_balance.amount`` / ``.currency`` and applies the ``date``
   filter to ``gift_card.expires_at``. Against a string those resolve to the
   empty string, so recipients got a gift card email showing no value and no
   expiry. ``issue()`` now passes the model instance. The admin preview sample
   had the same shape bug and must not diverge again.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R1)
"""

from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

import pytest
from django.template import Context, Template
from django.urls import reverse
from django.utils import timezone
from djmoney.money import Money

from tests.factories import ProductFactory, UserFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.r1,
]


# ============================================================
# Helpers
# ============================================================


@pytest.fixture
def superuser(db):
    return UserFactory(is_staff=True, is_superuser=True)


@pytest.fixture
def admin_client_su(client, superuser):
    client.force_login(superuser)
    return client


@pytest.fixture
def gift_card_product(db):
    """``GiftCard.product`` is ``limit_choices_to={"product_type": "gift_card"}``."""
    return ProductFactory(product_type="gift_card")


def _gift_card(product, initial_value="50.00", **kwargs):
    from catalog.models import GiftCard

    defaults = {
        "code": kwargs.pop("code", None) or GiftCard.generate_code(),
        "product": product,
        "initial_value": Money(Decimal(initial_value), "USD"),
        "recipient_email": "recipient@example.com",
        "recipient_name": "Sarah Johnson",
        "sender_name": "John Smith",
        "is_active": True,
    }
    defaults.update(kwargs)
    return GiftCard.objects.create(**defaults)


def _load_delivery_template():
    """
    Parse the real ``gift_card_delivery`` markdown template off disk.

    The rendered email in production comes from an ``EmailTemplate`` row seeded
    from this file, so this is the same content — and it is the content that
    contains the ``gift_card.current_balance.amount`` expressions the bug hit.
    """
    from pathlib import Path

    from django.conf import settings as django_settings

    from email_system.management.commands.seed_email_templates import (
        parse_markdown_template,
    )

    path = (
        Path(django_settings.BASE_DIR) / "email_templates_for_translation" / "gift_card_delivery.md"
    )
    parsed = parse_markdown_template(str(path))
    assert "error" not in parsed, parsed
    return parsed


# ============================================================
# 8. GiftCardAdmin add form
# ============================================================


class TestGiftCardAdminAddForm:
    def test_superuser_can_load_the_add_form(self, admin_client_su, site_settings):
        response = admin_client_su.get(reverse("admin:catalog_giftcard_add"))

        assert response.status_code == 200

    def test_the_add_form_exposes_the_writable_fields(self, admin_client_su, site_settings):
        """
        Specifically ``product`` (the FK, not the ``product_link`` display
        method) and ``initial_value`` — without both, no add can ever save.
        """
        response = admin_client_su.get(reverse("admin:catalog_giftcard_add"))
        form = response.context["adminform"].form

        assert "product" in form.fields
        assert "initial_value" in form.fields
        assert "recipient_email" in form.fields

    def test_the_add_form_has_no_readonly_fields(self, admin_client_su, site_settings):
        from django.contrib.admin.sites import site as admin_site

        from catalog.admin import GiftCardAdmin
        from catalog.models import GiftCard

        model_admin = GiftCardAdmin(GiftCard, admin_site)
        request = admin_client_su.get(reverse("admin:catalog_giftcard_add")).wsgi_request

        assert model_admin.get_readonly_fields(request, obj=None) == []

    def test_the_add_form_shows_no_inlines(self, admin_client_su, site_settings):
        """A transactions inline needs a saved card to hang off."""
        from django.contrib.admin.sites import site as admin_site

        from catalog.admin import GiftCardAdmin
        from catalog.models import GiftCard

        model_admin = GiftCardAdmin(GiftCard, admin_site)
        request = admin_client_su.get(reverse("admin:catalog_giftcard_add")).wsgi_request

        assert model_admin.get_inlines(request, obj=None) == []

    def test_posting_the_add_form_creates_a_funded_card(
        self, admin_client_su, site_settings, gift_card_product, superuser
    ):
        from catalog.models import GiftCard

        response = admin_client_su.post(
            reverse("admin:catalog_giftcard_add"),
            {
                "product": str(gift_card_product.id),
                "initial_value_0": "50.00",
                "initial_value_1": "USD",
                "recipient_email": "recipient@example.com",
                "recipient_name": "Sarah Johnson",
                "sender_name": "John Smith",
                "message": "Happy birthday!",
                "expires_at_0": "",
                "expires_at_1": "",
                "scheduled_send_at_0": "",
                "scheduled_send_at_1": "",
                "is_active": "on",
            },
            follow=True,
        )

        assert response.status_code == 200
        card = GiftCard.objects.filter(recipient_email="recipient@example.com").first()
        assert card is not None, (
            "The add form did not save. Before R1 the Add button rendered a "
            "form that was unsatisfiable."
        )

    def test_the_created_card_has_a_generated_code(
        self, admin_client_su, site_settings, gift_card_product
    ):
        import re

        from catalog.models import GiftCard

        self._post_add(admin_client_su, gift_card_product)

        card = GiftCard.objects.get(recipient_email="recipient@example.com")
        assert re.fullmatch(r"GC-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}", card.code), (
            f"save_model did not mint a code in the documented shape: {card.code!r}"
        )

    def test_the_balance_opens_at_the_initial_value(
        self, admin_client_su, site_settings, gift_card_product
    ):
        from catalog.models import GiftCard

        self._post_add(admin_client_su, gift_card_product)

        card = GiftCard.objects.get(recipient_email="recipient@example.com")
        assert card.current_balance == card.initial_value
        assert card.current_balance == Money(Decimal("50.00"), "USD"), (
            "A hand-issued card must be funded, not opened at zero."
        )

    def test_created_by_records_the_issuing_merchant(
        self, admin_client_su, site_settings, gift_card_product, superuser
    ):
        from catalog.models import GiftCard

        self._post_add(admin_client_su, gift_card_product)

        card = GiftCard.objects.get(recipient_email="recipient@example.com")
        assert card.created_by_id == superuser.id, (
            "Manual issuance of stored value must record who did it."
        )

    def test_two_added_cards_get_distinct_codes(
        self, admin_client_su, site_settings, gift_card_product
    ):
        from catalog.models import GiftCard

        self._post_add(admin_client_su, gift_card_product, email="one@example.com")
        self._post_add(admin_client_su, gift_card_product, email="two@example.com")

        codes = set(GiftCard.objects.values_list("code", flat=True))
        assert len(codes) == GiftCard.objects.count() == 2

    @staticmethod
    def _post_add(client, product, email="recipient@example.com"):
        return client.post(
            reverse("admin:catalog_giftcard_add"),
            {
                "product": str(product.id),
                "initial_value_0": "50.00",
                "initial_value_1": "USD",
                "recipient_email": email,
                "recipient_name": "Sarah Johnson",
                "sender_name": "John Smith",
                "message": "",
                "expires_at_0": "",
                "expires_at_1": "",
                "scheduled_send_at_0": "",
                "scheduled_send_at_1": "",
                "is_active": "on",
            },
            follow=True,
        )


class TestGiftCardAdminChangeFormStaysLockedDown:
    """
    Editing must not become a back door around the ledger. Money moves through
    ``redeem()`` / ``refund()`` / ``adjust_balance()`` so every change lands in
    ``GiftCardTransaction``.
    """

    @pytest.mark.parametrize("field", ["code", "initial_value", "current_balance"])
    def test_field_is_readonly_on_an_existing_card(
        self, admin_client_su, site_settings, gift_card_product, field
    ):
        from django.contrib.admin.sites import site as admin_site

        from catalog.admin import GiftCardAdmin
        from catalog.models import GiftCard

        card = _gift_card(gift_card_product)
        model_admin = GiftCardAdmin(GiftCard, admin_site)
        request = admin_client_su.get(
            reverse("admin:catalog_giftcard_change", args=[card.pk])
        ).wsgi_request

        assert field in model_admin.get_readonly_fields(request, obj=card), (
            f"{field} became editable on the change form — a merchant could "
            f"move stored value without a ledger entry."
        )

    def test_the_change_form_loads(self, admin_client_su, site_settings, gift_card_product):
        card = _gift_card(gift_card_product)

        response = admin_client_su.get(reverse("admin:catalog_giftcard_change", args=[card.pk]))

        assert response.status_code == 200

    def test_the_change_form_does_not_render_readonly_fields_as_inputs(
        self, admin_client_su, site_settings, gift_card_product
    ):
        card = _gift_card(gift_card_product)

        response = admin_client_su.get(reverse("admin:catalog_giftcard_change", args=[card.pk]))
        form = response.context["adminform"].form

        for field in ("code", "initial_value", "current_balance"):
            assert field not in form.fields, f"{field} is a live form input on the change form."

    def test_editing_does_not_reset_the_balance(
        self, admin_client_su, site_settings, gift_card_product
    ):
        """``save_model`` must only derive on create, never on edit."""
        from django.contrib.admin.sites import site as admin_site

        from catalog.admin import GiftCardAdmin
        from catalog.models import GiftCard

        card = _gift_card(gift_card_product, initial_value="50.00")
        card.current_balance = Money(Decimal("12.34"), "USD")
        card.save(update_fields=["current_balance"])

        model_admin = GiftCardAdmin(GiftCard, admin_site)
        request = admin_client_su.get(
            reverse("admin:catalog_giftcard_change", args=[card.pk])
        ).wsgi_request
        card.recipient_name = "Renamed Recipient"
        model_admin.save_model(request, card, form=None, change=True)

        card.refresh_from_db()
        assert card.current_balance == Money(Decimal("12.34"), "USD"), (
            "Editing a card reset its balance to the initial value — that is "
            "stored value appearing out of nowhere."
        )
        assert card.recipient_name == "Renamed Recipient"

    def test_a_non_staff_user_cannot_reach_the_add_form(self, site_settings, client):
        client.force_login(UserFactory(is_staff=False))

        response = client.get(reverse("admin:catalog_giftcard_add"))

        assert response.status_code in (302, 403)

    def test_an_anonymous_user_cannot_reach_the_add_form(self, site_settings, client):
        response = client.get(reverse("admin:catalog_giftcard_add"))

        assert response.status_code in (302, 403)


# ============================================================
# 10. Gift card delivery email context
# ============================================================


class TestIssueSendsATemplateFriendlyContext:
    """
    The bug: ``issue()`` passed ``str(...)`` values, so
    ``{{ gift_card.current_balance.amount }}`` and
    ``{{ gift_card.expires_at|date:"F d, Y" }}`` rendered EMPTY.
    """

    def _capture_context(self, card):
        with patch("email_system.services.email_sender.EmailSendingService") as mock_service:
            card.issue(send_email=True)

        assert mock_service.send_template_email.called, (
            "issue() did not send the delivery email. Note issue() wraps the "
            "send in `except Exception`, so a failure here is silent in prod."
        )
        kwargs = mock_service.send_template_email.call_args.kwargs
        assert kwargs["template_type"] == "gift_card_delivery"
        return kwargs["context"]

    def test_the_context_carries_the_model_instance(self, site_settings, gift_card_product):
        from catalog.models import GiftCard

        card = _gift_card(gift_card_product, expires_at=timezone.now() + timedelta(days=365))

        context = self._capture_context(card)

        assert isinstance(context["gift_card"], GiftCard), (
            "issue() passed a stringified/dict gift_card again — the template "
            "dereferences attributes on it and will render empty."
        )

    def test_the_balance_is_a_money_object_not_a_string(self, site_settings, gift_card_product):
        card = _gift_card(gift_card_product, initial_value="50.00")

        context = self._capture_context(card)

        balance = context["gift_card"].current_balance
        assert isinstance(balance, Money)
        assert balance.amount == Decimal("50.00")
        assert str(balance.currency) == "USD"

    def test_expires_at_is_a_datetime_not_a_formatted_string(
        self, site_settings, gift_card_product
    ):
        from datetime import datetime

        expiry = timezone.now() + timedelta(days=365)
        card = _gift_card(gift_card_product, expires_at=expiry)

        context = self._capture_context(card)

        assert isinstance(context["gift_card"].expires_at, datetime), (
            "A pre-formatted expiry string makes the template's `date` filter render nothing."
        )


class TestDeliveryTemplateRendersNonEmptyValues:
    """
    Render the real template against the real ``issue()`` context. This is the
    assertion that would have caught the original bug: the template rendered
    fine, it just rendered *blank* where the value should be.
    """

    def _render(self, card):
        with patch("email_system.services.email_sender.EmailSendingService") as mock_service:
            card.issue(send_email=True)
        context = mock_service.send_template_email.call_args.kwargs["context"]

        parsed = _load_delivery_template()
        html = Template(parsed["html_content"]).render(Context(context))
        text = Template(parsed["text_content"]).render(Context(context))
        return html, text

    def test_the_balance_amount_is_rendered(self, site_settings, gift_card_product):
        card = _gift_card(
            gift_card_product,
            initial_value="50.00",
            expires_at=timezone.now() + timedelta(days=365),
        )

        html, text = self._render(card)

        assert "50.00" in html, (
            "The balance amount rendered empty — `current_balance.amount` "
            "resolved to nothing, which is exactly the original bug."
        )
        assert "50.00" in text

    def test_the_currency_is_rendered(self, site_settings, gift_card_product):
        card = _gift_card(
            gift_card_product,
            initial_value="50.00",
            expires_at=timezone.now() + timedelta(days=365),
        )

        html, text = self._render(card)

        assert "USD" in html
        assert "USD" in text

    def test_the_expiry_is_rendered_and_formatted(self, site_settings, gift_card_product):
        expiry = timezone.now() + timedelta(days=365)
        card = _gift_card(gift_card_product, expires_at=expiry)

        html, text = self._render(card)

        # The template applies |date:"F d, Y" — e.g. "July 18, 2027".
        expected = expiry.strftime("%B %d, %Y")
        assert expected in html, (
            f"Expected the formatted expiry {expected!r} in the email; the "
            f"`date` filter rendered nothing."
        )
        assert expected in text

    def test_the_code_is_rendered(self, site_settings, gift_card_product):
        card = _gift_card(gift_card_product, expires_at=timezone.now() + timedelta(days=30))

        html, text = self._render(card)

        assert card.code in html
        assert card.code in text

    def test_no_expiry_renders_the_never_expires_copy(self, site_settings, gift_card_product):
        card = _gift_card(gift_card_product, expires_at=None)

        html, _text = self._render(card)

        assert "never expires" in html.lower()


class TestSampleDataMatchesTheRealEmail:
    """
    The admin preview must not diverge from the real email again. The sample
    previously used pre-formatted strings ("$50.00", "December 31, 2026"), which
    render as empty against the template's expressions — so the preview looked
    plausible while the real email showed nothing.
    """

    def _sample_context(self):
        from email_system.services.sample_data import SampleDataProvider

        return SampleDataProvider.get_sample_data("gift_card_delivery")

    def test_the_sample_balance_is_a_money_object(self, site_settings):
        sample = self._sample_context()

        balance = sample["gift_card"]["current_balance"]
        assert isinstance(balance, Money), (
            f"Sample current_balance is {type(balance).__name__}; the template "
            f"reads `.amount` and `.currency` off it and would render empty."
        )

    def test_the_sample_expiry_is_a_datetime(self, site_settings):
        from datetime import datetime

        sample = self._sample_context()

        assert isinstance(sample["gift_card"]["expires_at"], datetime)

    def test_the_sample_renders_a_non_empty_balance(self, site_settings):
        sample = self._sample_context()
        parsed = _load_delivery_template()

        html = Template(parsed["html_content"]).render(Context(sample))

        assert "50.00" in html
        assert "USD" in html

    def test_the_sample_renders_a_non_empty_expiry(self, site_settings):
        sample = self._sample_context()
        parsed = _load_delivery_template()

        html = Template(parsed["html_content"]).render(Context(sample))
        expected = sample["gift_card"]["expires_at"].strftime("%B %d, %Y")

        assert expected in html

    def test_the_sample_renders_the_code(self, site_settings):
        sample = self._sample_context()
        parsed = _load_delivery_template()

        html = Template(parsed["html_content"]).render(Context(sample))

        assert sample["gift_card"]["code"] in html

    def test_sample_and_real_context_expose_the_same_keys(self, site_settings, gift_card_product):
        """
        The preview and the real send must read the same variables, or the
        preview stops being evidence about the email.
        """
        card = _gift_card(gift_card_product, expires_at=timezone.now() + timedelta(days=30))
        with patch("email_system.services.email_sender.EmailSendingService") as mock_service:
            card.issue(send_email=True)
        real_context = mock_service.send_template_email.call_args.kwargs["context"]

        sample = self._sample_context()

        assert set(real_context) <= set(sample), (
            f"issue() sends keys the admin preview never supplies: "
            f"{set(real_context) - set(sample)}"
        )
        for key in ("code", "current_balance", "expires_at"):
            assert key in sample["gift_card"]
            assert hasattr(real_context["gift_card"], key)
