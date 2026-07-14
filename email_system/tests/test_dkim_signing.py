"""DKIM signing integration tests.

Tests for the ``DKIMHandler`` class and DKIM signing functionality used
by the built-in SMTP server provider.

Key points about the real handler (see
``email_system/smtp_server/dkim_handler.py``):

- ``generate_key_pair()`` returns a ``(private_pem, public_pem)`` tuple
  where both halves are ``bytes`` (PKCS8 / SubjectPublicKeyInfo — so the
  private key header is ``-----BEGIN PRIVATE KEY-----``, not the older
  ``BEGIN RSA PRIVATE KEY``).
- ``sign_message(message, account=None)`` looks the private key up from
  the encrypted credentials JSON on the ``EmailAccount``. Callers do NOT
  pass raw key bytes.
- ``get_dns_record(account=None)`` derives the DNS TXT value from the
  stored public key. Same account-based lookup.
- Keys are persisted via ``store_keys(private, public, account)`` which
  encrypts them into ``account.credentials``.
"""

import unittest

try:
    import dkim  # dkimpy package

    DKIM_AVAILABLE = True
except ImportError:  # pragma: no cover — dkimpy is a hard dep in the venv
    DKIM_AVAILABLE = False

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.test import TestCase

from component_updates.models import ComponentRegistry
from email_system.models import EmailAccount
from email_system.smtp_server.dkim_handler import DKIMHandler
from email_system.utils.encryption import encrypt_credentials

User = get_user_model()


def _make_account(domain: str, name: str = "DKIM Test") -> EmailAccount:
    """Create a minimal EmailAccount tied to Site(id=1) for DKIM tests."""
    site = Site.objects.get(pk=1)
    component, _ = ComponentRegistry.objects.get_or_create(
        slug=f"dkim-test-{domain.replace('.', '-')}",
        defaults={
            "component_type": "email_provider",
            "name": f"DKIM Test Provider ({domain})",
            "current_version": "1.0.0",
        },
    )
    user, _ = User.objects.get_or_create(
        username=f"dkim_test_{domain.replace('.', '_')}",
        defaults={"email": f"admin@{domain}"},
    )
    return EmailAccount.objects.create(
        site=site,
        component=component,
        name=name,
        from_email=f"noreply@{domain}",
        credentials=encrypt_credentials({}),
        created_by=user,
    )


@unittest.skipUnless(DKIM_AVAILABLE, "dkimpy package not installed")
class DKIMHandlerTestCase(TestCase):
    """Test DKIM signing functionality."""

    def setUp(self):
        self.domain = "example.com"
        self.selector = "test"
        self.handler = DKIMHandler(domain=self.domain, selector=self.selector)
        self.account = _make_account(self.domain)
        # Ensure per-test cache isolation — DKIMHandler caches decrypted
        # keys and stale entries would poison unrelated tests.
        cache.clear()

    def test_key_generation(self):
        """Test RSA key pair generation."""
        private_key, public_key = self.handler.generate_key_pair()

        # Both halves must be non-empty bytes.
        self.assertIsInstance(private_key, bytes)
        self.assertIsInstance(public_key, bytes)
        self.assertGreater(len(private_key), 0)
        self.assertGreater(len(public_key), 0)

        # DKIMHandler serialises with PKCS8, so headers are
        # "BEGIN PRIVATE KEY" — NOT the older PKCS1 form.
        self.assertTrue(
            private_key.startswith(b"-----BEGIN PRIVATE KEY-----"),
            f"Unexpected private key header: {private_key[:60]!r}",
        )
        self.assertIn(b"-----END PRIVATE KEY-----", private_key)

        # Public key is a PEM-encoded SubjectPublicKeyInfo block.
        self.assertTrue(
            public_key.startswith(b"-----BEGIN PUBLIC KEY-----"),
            f"Unexpected public key header: {public_key[:60]!r}",
        )
        # 2048-bit RSA public key PEM is comfortably over 300 bytes.
        self.assertGreater(len(public_key), 300)

    def test_sign_message(self):
        """Test DKIM signature creation once keys are stored on an account."""
        private_key, public_key = self.handler.generate_key_pair()
        self.handler.store_keys(private_key, public_key, account=self.account)

        message = (
            b"From: sender@example.com\r\n"
            b"To: recipient@example.com\r\n"
            b"Subject: Test Message\r\n"
            b"Date: Mon, 28 Oct 2024 00:00:00 +0000\r\n"
            b"Message-ID: <test@example.com>\r\n"
            b"\r\n"
            b"This is a test message body.\r\n"
        )

        signed_message = self.handler.sign_message(message, account=self.account)

        self.assertIsNotNone(signed_message)
        self.assertIn(b"DKIM-Signature:", signed_message)
        self.assertIn(b"d=example.com", signed_message)
        self.assertIn(b"s=test", signed_message)

    def test_signature_validation(self):
        """Generated signatures verify against a mocked DNS lookup."""
        private_key, public_key = self.handler.generate_key_pair()
        self.handler.store_keys(private_key, public_key, account=self.account)

        message = (
            b"From: sender@example.com\r\n"
            b"To: recipient@example.com\r\n"
            b"Subject: Test Message\r\n"
            b"Date: Mon, 28 Oct 2024 00:00:00 +0000\r\n"
            b"Message-ID: <test@example.com>\r\n"
            b"\r\n"
            b"This is a test message body.\r\n"
        )

        signed_message = self.handler.sign_message(message, account=self.account)
        self.assertIn(b"DKIM-Signature:", signed_message)

        dns_txt = self.handler.get_dns_record(account=self.account)
        self.assertIsNotNone(dns_txt)

        # Mock DNS to hand dkimpy back our TXT record. dkimpy calls
        # dnsfunc(name) with `bytes`; response must also be `bytes`.
        expected_name = f"{self.selector}._domainkey.{self.domain}"

        def mock_dns(name, timeout=5):
            requested = name.decode() if isinstance(name, bytes) else name
            if requested.rstrip(".") == expected_name:
                return dns_txt.encode() if isinstance(dns_txt, str) else dns_txt
            return b""

        try:
            result = dkim.verify(signed_message, dnsfunc=mock_dns)
        except Exception as exc:  # pragma: no cover
            self.fail(f"DKIM verification raised exception: {exc}")
        self.assertTrue(result, "DKIM signature verification failed")

    def test_get_dns_record(self):
        """Test DNS record generation from a stored public key."""
        private_key, public_key = self.handler.generate_key_pair()
        self.handler.store_keys(private_key, public_key, account=self.account)

        dns_record = self.handler.get_dns_record(account=self.account)

        self.assertIsNotNone(dns_record)
        self.assertIn("v=DKIM1", dns_record)
        self.assertIn("k=rsa", dns_record)
        self.assertIn("p=", dns_record)
        # Sanity check — the base64 portion should be present and long.
        self.assertGreater(len(dns_record.split("p=", 1)[1]), 100)

    def test_get_dns_record_without_keys_returns_none(self):
        """No public key on the account → no DNS record."""
        self.assertIsNone(self.handler.get_dns_record(account=self.account))

    def test_multiple_selectors(self):
        """Different selectors produce signatures under the correct s= tag."""
        for selector in ["mail", "default", "key1", "2024-10"]:
            handler = DKIMHandler(domain=self.domain, selector=selector)
            account = _make_account(self.domain, name=f"DKIM Test {selector}")
            private_key, public_key = handler.generate_key_pair()
            handler.store_keys(private_key, public_key, account=account)

            message = (
                b"From: sender@example.com\r\n"
                b"To: recipient@example.com\r\n"
                b"Subject: Test Message\r\n"
                b"\r\n"
                b"Test body\r\n"
            )

            signed_message = handler.sign_message(message, account=account)
            self.assertIn(f"s={selector}".encode(), signed_message)

    def test_sign_unicode_message(self):
        """DKIM signing works for messages with unicode content."""
        private_key, public_key = self.handler.generate_key_pair()
        self.handler.store_keys(private_key, public_key, account=self.account)

        message = (
            "From: sender@example.com\r\n"
            "To: recipient@example.com\r\n"
            "Subject: Test Message with émojis \U0001f389\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            "\r\n"
            "This is a message with unicode: Héllo Wörld! "
            "你好世界\r\n"
        ).encode()

        signed_message = self.handler.sign_message(message, account=self.account)

        self.assertIsNotNone(signed_message)
        self.assertIn(b"DKIM-Signature:", signed_message)

    def test_sign_multipart_message(self):
        """DKIM signing prepends the header on a multipart MIME message."""
        private_key, public_key = self.handler.generate_key_pair()
        self.handler.store_keys(private_key, public_key, account=self.account)

        message = (
            b"From: sender@example.com\r\n"
            b"To: recipient@example.com\r\n"
            b"Subject: Multipart Message\r\n"
            b"MIME-Version: 1.0\r\n"
            b'Content-Type: multipart/alternative; boundary="boundary123"\r\n'
            b"\r\n"
            b"--boundary123\r\n"
            b"Content-Type: text/plain; charset=utf-8\r\n"
            b"\r\n"
            b"Plain text version\r\n"
            b"\r\n"
            b"--boundary123\r\n"
            b"Content-Type: text/html; charset=utf-8\r\n"
            b"\r\n"
            b"<html><body><p>HTML version</p></body></html>\r\n"
            b"\r\n"
            b"--boundary123--\r\n"
        )

        signed_message = self.handler.sign_message(message, account=self.account)

        self.assertIsNotNone(signed_message)
        self.assertIn(b"DKIM-Signature:", signed_message)
        # The signature must be prepended so it becomes the first header.
        self.assertTrue(signed_message.startswith(b"DKIM-Signature:"))

    def test_sign_message_without_keys_returns_original(self):
        """No stored key → sign_message logs a warning and returns the
        original message unchanged (handler explicitly documents this
        fallback so mail still flows unsigned)."""
        message = (
            b"From: sender@example.com\r\n"
            b"To: recipient@example.com\r\n"
            b"Subject: Test\r\n"
            b"\r\n"
            b"Body\r\n"
        )

        result = self.handler.sign_message(message, account=self.account)

        self.assertEqual(result, message)
        self.assertNotIn(b"DKIM-Signature:", result)

    def test_sign_message_with_invalid_stored_key(self):
        """If the stored private key is unparseable, sign_message swallows
        the dkimpy error and returns the original message (again, so
        mail still flows). The handler must NOT raise."""
        # Poison the credentials with a bogus PEM.
        bad_credentials = {
            "dkim_private_key": "invalid-key",
            "dkim_public_key": "invalid-pub",
            "dkim_selector": self.selector,
        }
        self.account.credentials = encrypt_credentials(bad_credentials)
        self.account.save()
        cache.clear()

        message = (
            b"From: sender@example.com\r\n"
            b"To: recipient@example.com\r\n"
            b"Subject: Test\r\n"
            b"\r\n"
            b"Body\r\n"
        )

        result = self.handler.sign_message(message, account=self.account)
        self.assertEqual(result, message)
        self.assertNotIn(b"DKIM-Signature:", result)


class DKIMIntegrationTestCase(TestCase):
    """Integration tests for DKIM with the wider email system."""

    def setUp(self):
        self.domain = "test.example.com"
        self.selector = "integration_test"
        self.account = _make_account(self.domain, name="DKIM Integration")
        cache.clear()

    @unittest.skipUnless(DKIM_AVAILABLE, "dkimpy not available")
    def test_end_to_end_signing_verification(self):
        """Complete DKIM signing → verification workflow."""
        handler = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler.generate_key_pair()
        handler.store_keys(private_key, public_key, account=self.account)

        message = (
            b"From: noreply@test.example.com\r\n"
            b"To: customer@example.org\r\n"
            b"Reply-To: support@test.example.com\r\n"
            b"Subject: Order Confirmation #12345\r\n"
            b"Date: Mon, 28 Oct 2024 12:34:56 +0000\r\n"
            b"Message-ID: <order-12345@test.example.com>\r\n"
            b"MIME-Version: 1.0\r\n"
            b"Content-Type: text/html; charset=utf-8\r\n"
            b"\r\n"
            b"<!DOCTYPE html>\r\n"
            b"<html>\r\n"
            b"<head><title>Order Confirmation</title></head>\r\n"
            b"<body>\r\n"
            b"<h1>Thank you for your order!</h1>\r\n"
            b"<p>Your order #12345 has been confirmed.</p>\r\n"
            b"</body>\r\n"
            b"</html>\r\n"
        )

        signed_message = handler.sign_message(message, account=self.account)
        self.assertIn(b"DKIM-Signature:", signed_message)

        dns_txt = handler.get_dns_record(account=self.account)
        self.assertIsNotNone(dns_txt)

        expected_name = f"{self.selector}._domainkey.{self.domain}"

        def mock_dns(name, timeout=5):
            requested = name.decode() if isinstance(name, bytes) else name
            if requested.rstrip(".") == expected_name:
                return dns_txt.encode() if isinstance(dns_txt, str) else dns_txt
            return b""

        try:
            result = dkim.verify(signed_message, dnsfunc=mock_dns)
        except Exception as exc:  # pragma: no cover
            self.fail(f"End-to-end verification raised exception: {exc}")
        self.assertTrue(result, "End-to-end DKIM verification failed")

    def test_dns_record_format_for_dns_assistant(self):
        """DNS TXT record shape is compatible with our DNS assistant."""
        handler = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler.generate_key_pair()
        handler.store_keys(private_key, public_key, account=self.account)

        dns_record = handler.get_dns_record(account=self.account)
        self.assertIsNotNone(dns_record)

        self.assertTrue(dns_record.startswith("v=DKIM1"))
        self.assertIn("k=rsa", dns_record)
        self.assertIn("p=", dns_record)

        # Must be single-line — TXT records can be split at 255 chars by
        # DNS servers, but our stored representation should not embed
        # raw newlines.
        self.assertNotIn("\n", dns_record)

        # Semicolon-separated tags should have no extra whitespace after
        # trimming — the assistant relies on the "; " separator to split
        # tags cleanly.
        for part in dns_record.split("; "):
            self.assertEqual(part.strip(), part, f"Extra whitespace in: {part!r}")
