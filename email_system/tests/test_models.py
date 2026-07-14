"""
Tests for email_system models.
Tests cover EmailAccount, EmailTemplate, EmailOutbox, and EmailEvent models.
"""

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase
from django.utils import timezone

from component_updates.models import ComponentRegistry
from email_system.models import EmailAccount, EmailEvent, EmailOutbox, EmailTemplate
from email_system.utils.encryption import encrypt_credentials

User = get_user_model()


class EmailAccountModelTest(TestCase):
    """Tests for EmailAccount model"""

    def setUp(self):
        """Set up test data"""
        self.site = Site.objects.get_current()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create a test email provider component
        self.component = ComponentRegistry.objects.create(
            component_type="email_provider",
            slug="test-gmail",
            name="Test Gmail Provider",
            current_version="1.0.0",
        )

    def test_create_email_account(self):
        """Test creating an EmailAccount"""
        credentials = {"api_key": "test_key_123", "secret": "test_secret"}

        account = EmailAccount.objects.create(
            site=self.site,
            component=self.component,
            name="Test Account",
            from_email="test@example.com",
            from_name="Test Sender",
            credentials=encrypt_credentials(credentials),
            created_by=self.user,
        )

        self.assertIsNotNone(account.id)
        self.assertEqual(account.name, "Test Account")
        self.assertEqual(account.from_email, "test@example.com")
        self.assertEqual(account.from_name, "Test Sender")
        self.assertTrue(account.is_active)
        self.assertFalse(account.is_default)
        self.assertEqual(account.connection_status, "unknown")

    def test_credentials_encryption_decryption(self):
        """Test that credentials are properly encrypted and can be decrypted"""
        credentials = {
            "client_id": "test_client_id",
            "client_secret": "super_secret_value",
            "access_token": "test_access_token",
        }

        account = EmailAccount.objects.create(
            site=self.site,
            component=self.component,
            name="Test Account",
            from_email="test@example.com",
            credentials=encrypt_credentials(credentials),
            created_by=self.user,
        )

        # Retrieve and decrypt
        retrieved_account = EmailAccount.objects.get(pk=account.pk)
        decrypted = retrieved_account.get_credentials()

        self.assertEqual(decrypted["client_id"], "test_client_id")
        self.assertEqual(decrypted["client_secret"], "super_secret_value")
        self.assertEqual(decrypted["access_token"], "test_access_token")

    def test_set_credentials_method(self):
        """Test set_credentials() method"""
        account = EmailAccount.objects.create(
            site=self.site,
            component=self.component,
            name="Test Account",
            from_email="test@example.com",
            credentials=encrypt_credentials({}),
            created_by=self.user,
        )

        new_credentials = {"api_key": "new_key", "secret": "new_secret"}
        account.set_credentials(new_credentials)
        account.save()

        # Reload and verify
        account.refresh_from_db()
        decrypted = account.get_credentials()

        self.assertEqual(decrypted["api_key"], "new_key")
        self.assertEqual(decrypted["secret"], "new_secret")

    def test_get_credentials_empty(self):
        """Test get_credentials() with no credentials"""
        account = EmailAccount(
            site=self.site,
            component=self.component,
            name="Test Account",
            from_email="test@example.com",
            created_by=self.user,
        )
        # Don't set credentials, so it will be empty

        # For the model to work, we need to provide some credentials
        account.credentials = encrypt_credentials({})
        account.save()

        decrypted = account.get_credentials()
        self.assertEqual(decrypted, {})

    def test_is_default_single_account(self):
        """Test that only one account can be default per site"""
        # Create first default account
        account1 = EmailAccount.objects.create(
            site=self.site,
            component=self.component,
            name="Account 1",
            from_email="account1@example.com",
            is_default=True,
            credentials=encrypt_credentials({}),
            created_by=self.user,
        )

        self.assertTrue(account1.is_default)

        # Create second account as default
        component2 = ComponentRegistry.objects.create(
            component_type="email_provider",
            slug="test-smtp",
            name="Test SMTP Provider",
            current_version="1.0.0",
        )

        account2 = EmailAccount.objects.create(
            site=self.site,
            component=component2,
            name="Account 2",
            from_email="account2@example.com",
            is_default=True,
            credentials=encrypt_credentials({}),
            created_by=self.user,
        )

        # Refresh account1 from database
        account1.refresh_from_db()

        # Account1 should no longer be default
        self.assertFalse(account1.is_default)
        self.assertTrue(account2.is_default)

    def test_is_default_multiple_sites(self):
        """Test that each site can have its own default account"""
        site2 = Site.objects.create(domain="site2.example.com", name="Site 2")

        # Create default account for site 1
        account1 = EmailAccount.objects.create(
            site=self.site,
            component=self.component,
            name="Account Site 1",
            from_email="account1@example.com",
            is_default=True,
            credentials=encrypt_credentials({}),
            created_by=self.user,
        )

        # Create default account for site 2
        component2 = ComponentRegistry.objects.create(
            component_type="email_provider",
            slug="test-smtp-2",
            name="Test SMTP 2",
            current_version="1.0.0",
        )

        account2 = EmailAccount.objects.create(
            site=site2,
            component=component2,
            name="Account Site 2",
            from_email="account2@example.com",
            is_default=True,
            credentials=encrypt_credentials({}),
            created_by=self.user,
        )

        # Both should remain as defaults for their respective sites
        account1.refresh_from_db()
        account2.refresh_from_db()

        self.assertTrue(account1.is_default)
        self.assertTrue(account2.is_default)

    def test_str_method(self):
        """Test __str__ method"""
        account = EmailAccount.objects.create(
            site=self.site,
            component=self.component,
            name="My Email Account",
            from_email="sender@example.com",
            credentials=encrypt_credentials({}),
            created_by=self.user,
        )

        self.assertEqual(str(account), "My Email Account (sender@example.com)")

    def test_connection_status_tracking(self):
        """Test connection status and error tracking"""
        account = EmailAccount.objects.create(
            site=self.site,
            component=self.component,
            name="Test Account",
            from_email="test@example.com",
            credentials=encrypt_credentials({}),
            created_by=self.user,
        )

        # Update connection status
        account.connection_status = "error"
        account.connection_error = "Failed to authenticate"
        account.last_tested_at = timezone.now()
        account.save()

        account.refresh_from_db()

        self.assertEqual(account.connection_status, "error")
        self.assertEqual(account.connection_error, "Failed to authenticate")
        self.assertIsNotNone(account.last_tested_at)


class EmailTemplateModelTest(TestCase):
    """Tests for EmailTemplate model"""

    def setUp(self):
        """Set up test data"""
        self.site = Site.objects.get_current()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_create_email_template(self):
        """Test creating an EmailTemplate"""
        template = EmailTemplate.objects.create(
            site=self.site,
            template_type="order_confirmation",
            language_code="en",
            subject="Order Confirmed #{{ order_number }}",
            html_content="<h1>Thank you for your order!</h1>",
            text_content="Thank you for your order!",
            created_by=self.user,
        )

        self.assertIsNotNone(template.id)
        self.assertEqual(template.template_type, "order_confirmation")
        self.assertEqual(template.language_code, "en")
        self.assertTrue(template.is_active)
        self.assertFalse(template.is_system)

    def test_multiple_templates_per_type_language_site_allowed(self):
        """EmailTemplate.Meta has NO unique constraint on (site, template_type,
        language_code) — the model documents this intentionally so a merchant
        can keep the system template AND their cloned/customised copy
        side-by-side (see comment in EmailTemplate.Meta). This test locks
        that behaviour in."""
        system = EmailTemplate.objects.create(
            site=self.site,
            template_type="order_confirmation",
            language_code="en",
            subject="Order Confirmed",
            html_content="<h1>Thank you!</h1>",
            is_system=True,
            created_by=self.user,
        )

        # Custom clone with the same (site, type, language) tuple must be
        # allowed — no IntegrityError.
        clone = EmailTemplate.objects.create(
            site=self.site,
            template_type="order_confirmation",
            language_code="en",
            subject="Different Subject",
            html_content="<h1>Different Content</h1>",
            is_system=False,
            created_by=self.user,
        )

        self.assertNotEqual(system.pk, clone.pk)
        matching = EmailTemplate.objects.filter(
            site=self.site,
            template_type="order_confirmation",
            language_code="en",
        )
        self.assertEqual(matching.count(), 2)

    def test_multiple_languages_same_template_type(self):
        """Test creating templates for same type in different languages"""
        template_en = EmailTemplate.objects.create(
            site=self.site,
            template_type="order_confirmation",
            language_code="en",
            subject="Order Confirmed",
            html_content="<h1>Thank you!</h1>",
            created_by=self.user,
        )

        template_es = EmailTemplate.objects.create(
            site=self.site,
            template_type="order_confirmation",
            language_code="es",
            subject="Pedido Confirmado",
            html_content="<h1>¡Gracias!</h1>",
            created_by=self.user,
        )

        self.assertNotEqual(template_en.id, template_es.id)
        self.assertEqual(template_en.template_type, template_es.template_type)
        self.assertNotEqual(template_en.language_code, template_es.language_code)

    def test_str_method(self):
        """Test __str__ method"""
        template = EmailTemplate.objects.create(
            site=self.site,
            template_type="password_reset",
            language_code="en",
            subject="Reset Your Password",
            html_content="<h1>Password Reset</h1>",
            created_by=self.user,
        )

        self.assertEqual(str(template), "Password Reset (en)")

    def test_system_template_flag(self):
        """Test is_system flag for pre-installed templates"""
        template = EmailTemplate.objects.create(
            site=self.site,
            template_type="order_confirmation",
            language_code="en",
            subject="Order Confirmed",
            html_content="<h1>Thank you!</h1>",
            is_system=True,
            created_by=self.user,
        )

        self.assertTrue(template.is_system)


class EmailOutboxModelTest(TestCase):
    """Tests for EmailOutbox model"""

    def setUp(self):
        """Set up test data"""
        self.site = Site.objects.get_current()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.component = ComponentRegistry.objects.create(
            component_type="email_provider",
            slug="test-gmail",
            name="Test Gmail",
            current_version="1.0.0",
        )

        self.account = EmailAccount.objects.create(
            site=self.site,
            component=self.component,
            name="Test Account",
            from_email="sender@example.com",
            credentials=encrypt_credentials({}),
            created_by=self.user,
        )

    def test_create_email_outbox(self):
        """Test creating an EmailOutbox entry"""
        email = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            to_email="recipient@example.com",
            from_email="sender@example.com",
            from_name="Test Sender",
            subject="Test Email",
            html_body="<p>Hello World</p>",
            text_body="Hello World",
        )

        self.assertIsNotNone(email.id)
        self.assertEqual(email.to_email, "recipient@example.com")
        self.assertEqual(email.subject, "Test Email")
        self.assertEqual(email.status, "queued")
        self.assertEqual(email.retry_count, 0)
        self.assertEqual(email.max_retries, 3)

    def test_status_transitions(self):
        """Test email status transitions"""
        email = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            to_email="recipient@example.com",
            from_email="sender@example.com",
            subject="Test Email",
            html_body="<p>Test</p>",
        )

        # Queued → Sending
        email.status = "sending"
        email.save()
        self.assertEqual(email.status, "sending")

        # Sending → Sent
        email.status = "sent"
        email.sent_at = timezone.now()
        email.provider_message_id = "msg_12345"
        email.save()

        email.refresh_from_db()
        self.assertEqual(email.status, "sent")
        self.assertIsNotNone(email.sent_at)
        self.assertEqual(email.provider_message_id, "msg_12345")

    def test_failed_status_with_error(self):
        """Test failed email with error message"""
        email = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            to_email="recipient@example.com",
            from_email="sender@example.com",
            subject="Test Email",
            html_body="<p>Test</p>",
        )

        email.status = "failed"
        email.error_message = "Authentication failed"
        email.failed_at = timezone.now()
        email.retry_count = 1
        email.save()

        email.refresh_from_db()
        self.assertEqual(email.status, "failed")
        self.assertEqual(email.error_message, "Authentication failed")
        self.assertEqual(email.retry_count, 1)
        self.assertIsNotNone(email.failed_at)

    def test_cc_bcc_recipients(self):
        """Test CC and BCC recipients as JSON"""
        email = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            to_email="recipient@example.com",
            from_email="sender@example.com",
            subject="Test Email",
            html_body="<p>Test</p>",
            cc=["cc1@example.com", "cc2@example.com"],
            bcc=["bcc@example.com"],
        )

        self.assertEqual(email.cc, ["cc1@example.com", "cc2@example.com"])
        self.assertEqual(email.bcc, ["bcc@example.com"])

    def test_str_method(self):
        """Test __str__ method"""
        email = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            to_email="recipient@example.com",
            from_email="sender@example.com",
            subject="Order Confirmation",
            html_body="<p>Test</p>",
            status="sent",
        )

        self.assertEqual(str(email), "Order Confirmation → recipient@example.com (Sent)")


class EmailEventModelTest(TestCase):
    """Tests for EmailEvent model"""

    def setUp(self):
        """Set up test data"""
        self.site = Site.objects.get_current()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.component = ComponentRegistry.objects.create(
            component_type="email_provider",
            slug="test-gmail",
            name="Test Gmail",
            current_version="1.0.0",
        )

        self.account = EmailAccount.objects.create(
            site=self.site,
            component=self.component,
            name="Test Account",
            from_email="sender@example.com",
            credentials=encrypt_credentials({}),
            created_by=self.user,
        )

        self.email = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            to_email="recipient@example.com",
            from_email="sender@example.com",
            subject="Test Email",
            html_body="<p>Test</p>",
        )

    def test_create_email_event(self):
        """Test creating an EmailEvent"""
        event = EmailEvent.objects.create(
            email=self.email,
            event_type="delivered",
            event_data={"provider": "gmail", "timestamp": "2025-10-25T10:00:00Z"},
        )

        self.assertIsNotNone(event.id)
        self.assertEqual(event.event_type, "delivered")
        self.assertEqual(event.email, self.email)

    def test_bounce_event(self):
        """Test bounce event with details"""
        event = EmailEvent.objects.create(
            email=self.email,
            event_type="bounced",
            bounce_type="hard",
            bounce_reason="Mailbox does not exist",
            event_data={"smtp_code": 550},
        )

        self.assertEqual(event.event_type, "bounced")
        self.assertEqual(event.bounce_type, "hard")
        self.assertEqual(event.bounce_reason, "Mailbox does not exist")

    def test_open_event_with_tracking(self):
        """Test open event with user agent and IP"""
        event = EmailEvent.objects.create(
            email=self.email,
            event_type="opened",
            user_agent="Mozilla/5.0...",
            ip_address="192.168.1.1",
        )

        self.assertEqual(event.event_type, "opened")
        self.assertEqual(event.user_agent, "Mozilla/5.0...")
        self.assertEqual(event.ip_address, "192.168.1.1")

    def test_str_method(self):
        """Test __str__ method"""
        event = EmailEvent.objects.create(
            email=self.email,
            event_type="clicked",
        )

        self.assertEqual(str(event), "Clicked - Test Email")
