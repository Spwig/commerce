"""
DKIM Signing Integration Tests

Tests for the DKIMHandler class and DKIM signing functionality
in the built-in SMTP server provider.
"""
import unittest
from pathlib import Path
import tempfile
import os

try:
    import dkim  # dkimpy package
    DKIM_AVAILABLE = True
except ImportError:
    DKIM_AVAILABLE = False

from django.test import TestCase
from django.conf import settings

from email_system.smtp_server.dkim_handler import DKIMHandler


@unittest.skipUnless(DKIM_AVAILABLE, "dkimpy package not installed")
class DKIMHandlerTestCase(TestCase):
    """Test DKIM signing functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.domain = 'example.com'
        self.selector = 'test'
        self.handler = DKIMHandler(domain=self.domain, selector=self.selector)

    def test_key_generation(self):
        """Test RSA key pair generation"""
        handler = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler.generate_key_pair()

        # Verify keys are not empty
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)
        self.assertGreater(len(private_key), 0)
        self.assertGreater(len(public_key), 0)

        # Verify private key format
        self.assertTrue(private_key.startswith(b'-----BEGIN RSA PRIVATE KEY-----'))
        self.assertTrue(private_key.endswith(b'-----END RSA PRIVATE KEY-----\n'))

        # Verify public key format (base64 encoded for DNS)
        self.assertIsInstance(public_key, str)
        self.assertGreater(len(public_key), 100)  # 2048-bit key should be substantial

    def test_sign_message(self):
        """Test DKIM signature creation"""
        # Generate test keys
        handler = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler.generate_key_pair()

        # Create test message
        message = b"""From: sender@example.com
To: recipient@example.com
Subject: Test Message
Date: Mon, 28 Oct 2024 00:00:00 +0000
Message-ID: <test@example.com>

This is a test message body.
"""

        # Sign the message
        signed_message = handler.sign_message(message, private_key)

        # Verify signature was added
        self.assertIsNotNone(signed_message)
        self.assertIn(b'DKIM-Signature:', signed_message)
        self.assertIn(b'd=example.com', signed_message)
        self.assertIn(b's=test', signed_message)

    def test_signature_validation(self):
        """Test that generated DKIM signatures are valid"""
        # Generate test keys
        handler_temp = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler_temp.generate_key_pair()

        # Create test message
        message = b"""From: sender@example.com
To: recipient@example.com
Subject: Test Message
Date: Mon, 28 Oct 2024 00:00:00 +0000
Message-ID: <test@example.com>

This is a test message body.
"""

        # Sign the message
        handler = DKIMHandler(domain=self.domain, selector=self.selector)
        signed_message = handler.sign_message(message, private_key)

        # Verify the signature using dkimpy
        # Note: In real world, DNS would be queried for the public key
        # For testing, we'll mock the DNS lookup
        def mock_dns_query(name):
            """Mock DNS query to return our test public key"""
            if name == f"{self.selector}._domainkey.{self.domain}":
                # Return DKIM DNS record format
                return [f"v=DKIM1; k=rsa; p={public_key}"]
            return []

        # Verify signature (this will raise exception if invalid)
        try:
            result = dkim.verify(signed_message, dnsfunc=lambda name: mock_dns_query(name.decode()))
            self.assertTrue(result, "DKIM signature verification failed")
        except Exception as e:
            self.fail(f"DKIM verification raised exception: {e}")

    def test_get_dns_record(self):
        """Test DNS record generation for public key"""
        # Generate test keys
        handler_temp = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler_temp.generate_key_pair()

        # Get DNS record
        handler = DKIMHandler(domain=self.domain, selector=self.selector)
        dns_record = handler.get_dns_record(public_key)

        # Verify DNS record format
        self.assertIsNotNone(dns_record)
        self.assertIn('v=DKIM1', dns_record)
        self.assertIn('k=rsa', dns_record)
        self.assertIn(f'p={public_key}', dns_record)

    def test_multiple_selectors(self):
        """Test DKIM signing with different selectors"""
        # Generate keys
        handler_temp = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler_temp.generate_key_pair()

        # Test different selectors
        selectors = ['mail', 'default', 'key1', '2024-10']

        for selector in selectors:
            handler = DKIMHandler(domain=self.domain, selector=selector)

            message = b"""From: sender@example.com
To: recipient@example.com
Subject: Test Message

Test body
"""

            signed_message = handler.sign_message(message, private_key)

            # Verify correct selector in signature
            self.assertIn(f's={selector}'.encode(), signed_message)

    def test_sign_unicode_message(self):
        """Test DKIM signing with unicode content"""
        handler_temp = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler_temp.generate_key_pair()

        # Message with unicode characters
        message = """From: sender@example.com
To: recipient@example.com
Subject: Test Message with émojis 🎉
Content-Type: text/plain; charset=utf-8

This is a message with unicode: Héllo Wörld! 你好世界
""".encode('utf-8')

        handler = DKIMHandler(domain=self.domain, selector=self.selector)
        signed_message = handler.sign_message(message, private_key)

        # Verify signature was added
        self.assertIsNotNone(signed_message)
        self.assertIn(b'DKIM-Signature:', signed_message)

    def test_sign_multipart_message(self):
        """Test DKIM signing with multipart MIME messages"""
        handler_temp = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler_temp.generate_key_pair()

        # Multipart message
        message = b"""From: sender@example.com
To: recipient@example.com
Subject: Multipart Message
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="boundary123"

--boundary123
Content-Type: text/plain; charset=utf-8

Plain text version

--boundary123
Content-Type: text/html; charset=utf-8

<html><body><p>HTML version</p></body></html>

--boundary123--
"""

        handler = DKIMHandler(domain=self.domain, selector=self.selector)
        signed_message = handler.sign_message(message, private_key)

        # Verify signature was added
        self.assertIsNotNone(signed_message)
        self.assertIn(b'DKIM-Signature:', signed_message)
        # Signature should be at the beginning
        self.assertTrue(signed_message.startswith(b'DKIM-Signature:'))

    def test_empty_message_handling(self):
        """Test handling of empty messages"""
        handler_temp = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler_temp.generate_key_pair()

        handler = DKIMHandler(domain=self.domain, selector=self.selector)

        # Empty message should raise or return None
        with self.assertRaises(Exception):
            handler.sign_message(b'', private_key)

    def test_invalid_private_key(self):
        """Test handling of invalid private key"""
        handler = DKIMHandler(domain=self.domain, selector=self.selector)

        message = b"""From: sender@example.com
To: recipient@example.com
Subject: Test

Body
"""

        # Invalid private key should raise exception
        with self.assertRaises(Exception):
            handler.sign_message(message, b'invalid-key')


class DKIMIntegrationTestCase(TestCase):
    """Integration tests for DKIM with email system"""

    def setUp(self):
        """Set up test fixtures"""
        self.domain = 'test.example.com'
        self.selector = 'integration_test'

    @unittest.skipUnless(DKIM_AVAILABLE, "dkimpy not available")
    def test_end_to_end_signing_verification(self):
        """Test complete DKIM signing and verification workflow"""
        # Step 1: Generate keys
        handler_temp = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler_temp.generate_key_pair()

        # Step 2: Create handler
        handler = DKIMHandler(domain=self.domain, selector=self.selector)

        # Step 3: Create realistic email message
        message = b"""From: noreply@test.example.com
To: customer@example.org
Reply-To: support@test.example.com
Subject: Order Confirmation #12345
Date: Mon, 28 Oct 2024 12:34:56 +0000
Message-ID: <order-12345@test.example.com>
MIME-Version: 1.0
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
<head><title>Order Confirmation</title></head>
<body>
<h1>Thank you for your order!</h1>
<p>Your order #12345 has been confirmed.</p>
</body>
</html>
"""

        # Step 4: Sign the message
        signed_message = handler.sign_message(message, private_key)

        # Step 5: Verify signature present
        self.assertIn(b'DKIM-Signature:', signed_message)

        # Step 6: Verify signature is valid (mock DNS)
        def mock_dns(name):
            """Mock DNS TXT record lookup"""
            if name.decode() == f"{self.selector}._domainkey.{self.domain}":
                return [f"v=DKIM1; k=rsa; p={public_key}"]
            return []

        try:
            result = dkim.verify(signed_message, dnsfunc=mock_dns)
            self.assertTrue(result, "End-to-end DKIM verification failed")
        except Exception as e:
            self.fail(f"End-to-end verification raised exception: {e}")

    def test_dns_record_format_for_dns_assistant(self):
        """Test that DNS record format is compatible with DNS assistant"""
        handler_temp = DKIMHandler(domain=self.domain, selector=self.selector)
        private_key, public_key = handler_temp.generate_key_pair()
        handler = DKIMHandler(domain=self.domain, selector=self.selector)

        dns_record = handler.get_dns_record(public_key)

        # Verify format matches what DNS assistant expects
        self.assertTrue(dns_record.startswith('v=DKIM1'))
        self.assertIn('k=rsa', dns_record)
        self.assertIn('p=', dns_record)

        # Verify no newlines or spaces that could break DNS TXT records
        self.assertNotIn('\n', dns_record)
        # Spaces after semicolons are OK
        parts = dns_record.split('; ')
        for part in parts:
            self.assertFalse(part.strip() != part, f"Extra whitespace in: {part}")
