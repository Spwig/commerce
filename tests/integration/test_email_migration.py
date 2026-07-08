"""
Integration tests for the email template migration.

Tests verify that 5 legacy send_mail() / EmailMultiAlternatives calls have been
fully replaced with EmailSendingService.send_template_email(), plus the staff
password reset fallback removal.

Coverage:
- Customer password reset (accounts/api_views.py)
- Return request confirmation (orders/emails.py)
- Form builder email notification (form_builder/actions/email.py)
- Form builder auto-reply (form_builder/actions/email.py)
- POS license expiration warning (pos_app/tasks.py)
- Staff password reset fallback removal (admin_api/views/auth.py)
- Zero remaining legacy calls (no send_mail / EmailMultiAlternatives imports)
"""
import ast
import os
from datetime import timedelta
from unittest.mock import patch, MagicMock

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from tests.factories import UserFactory

User = get_user_model()

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.email_migration,
]

@pytest.fixture(autouse=True)
def _clear_throttle_cache():
    """Clear DRF throttle cache between tests to prevent rate limit 429s."""
    from django.core.cache import cache
    cache.clear()


# All migrated source files — used for zero-legacy-call checks
MIGRATED_FILES = [
    'accounts/api_views.py',
    'orders/emails.py',
    'form_builder/actions/email.py',
    'pos_app/tasks.py',
    'admin_api/views/auth.py',
]

# ============================================================
# Helpers
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _parse_imports(filepath):
    """Parse a Python file and return all imported names."""
    full_path = os.path.join(PROJECT_ROOT, filepath)
    with open(full_path, 'r') as f:
        source = f.read()
    tree = ast.parse(source)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.add(f'{module}.{alias.name}')
    return imports


def _file_contains_string(filepath, needle):
    """Check if a file contains a raw string (covers lazy imports too)."""
    full_path = os.path.join(PROJECT_ROOT, filepath)
    with open(full_path, 'r') as f:
        return needle in f.read()


def _mock_return_request(**overrides):
    """Create a mock ReturnRequest with sensible defaults."""
    user = MagicMock()
    user.email = 'customer@test.spwig.com'
    user.get_full_name.return_value = 'Jane Customer'
    user.username = 'jane_customer'

    order = MagicMock()
    order.order_number = 'ORD-20260322-001'

    rr = MagicMock()
    rr.id = 42
    rr.order = order
    rr.user = user
    rr.get_reason_display.return_value = 'Defective Product'
    rr.get_status_display.return_value = 'Pending Approval'
    rr.items_json = [
        {'order_item_id': 1, 'quantity': 2, 'reason': 'defective'},
        {'order_item_id': 2, 'quantity': 1, 'reason': 'wrong_item'},
    ]

    for key, value in overrides.items():
        setattr(rr, key, value)

    return rr


def _mock_form_action_and_response(
    to_emails=None,
    include_data=True,
    form_data=None,
    user=None,
    action_config_overrides=None,
):
    """Create mock action + form_response for EmailNotificationAction tests."""
    form = MagicMock()
    form.name = 'Contact Form'
    form.translated_title = 'Contact Us'

    # Create mock fields
    field_name = MagicMock()
    field_name.field_name = 'name'
    field_name.field_type = 'text'
    field_name.translated_label = 'Full Name'
    field_name.order = 0

    field_email = MagicMock()
    field_email.field_name = 'email'
    field_email.field_type = 'email'
    field_email.translated_label = 'Email Address'
    field_email.order = 1

    field_message = MagicMock()
    field_message.field_name = 'message'
    field_message.field_type = 'textarea'
    field_message.translated_label = 'Your Message'
    field_message.order = 2

    # Mock the queryset chain: form.fields.all().order_by(...)
    fields_qs = MagicMock()
    fields_qs.order_by.return_value = [field_name, field_email, field_message]
    fields_all = MagicMock(return_value=fields_qs)

    # Also make fields.all() iterable (for get_form_data_context)
    form.fields.all = fields_all
    form.fields.all.return_value = fields_qs
    # Make the qs iterable for get_form_data_context which iterates directly
    fields_qs.__iter__ = lambda self: iter([field_name, field_email, field_message])

    if form_data is None:
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hello, I need help with my order.',
        }

    form_response = MagicMock()
    form_response.pk = 99
    form_response.form = form
    form_response.data = form_data
    form_response.user = user
    form_response.submitted_at = '2026-03-22 10:30:00'

    config = {
        'to_emails': to_emails if to_emails is not None else ['admin@store.com'],
        'include_data': include_data,
    }
    if action_config_overrides:
        config.update(action_config_overrides)

    action = MagicMock()
    action.pk = 10
    action.config = config

    return action, form_response


def _mock_auto_reply_action_and_response(
    email_field='email',
    subject='Thank you!',
    body_template='Dear {{submitter_name}}, we got your message.',
    form_data=None,
    user=None,
):
    """Create mock action + form_response for AutoReplyAction tests."""
    form = MagicMock()
    form.name = 'Feedback Form'
    form.translated_title = 'Send Feedback'

    field_name = MagicMock()
    field_name.field_name = 'name'
    field_name.field_type = 'text'
    field_name.translated_label = 'Name'

    field_email = MagicMock()
    field_email.field_name = 'email'
    field_email.field_type = 'email'
    field_email.translated_label = 'Email'

    fields_qs = MagicMock()
    fields_qs.__iter__ = lambda self: iter([field_name, field_email])
    form.fields.all = MagicMock(return_value=fields_qs)

    if form_data is None:
        form_data = {
            'name': 'Alice Smith',
            'email': 'alice@example.com',
        }

    form_response = MagicMock()
    form_response.pk = 55
    form_response.form = form
    form_response.data = form_data
    form_response.user = user
    form_response.submitted_at = '2026-03-22 12:00:00'

    config = {
        'email_field': email_field,
        'subject': subject,
        'body_template': body_template,
    }

    action = MagicMock()
    action.pk = 20
    action.config = config

    return action, form_response


# ============================================================
# 1. Customer Password Reset
# ============================================================

class TestCustomerPasswordReset:
    """Verify accounts/api_views.py password_reset_request uses EmailSendingService."""

    @pytest.fixture(autouse=True)
    def _set_frontend_url(self, settings):
        settings.FRONTEND_URL = 'http://localhost:3000'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_calls_send_template_email_with_correct_template_type(self, mock_send, site_settings, django_site):
        """Password reset sends 'password_reset' template."""
        user = UserFactory(email='reset@test.spwig.com')
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post('/api/accounts/password-reset/', {'email': 'reset@test.spwig.com'})
        assert response.status_code == 200
        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args[1]
        assert call_kwargs['template_type'] == 'password_reset'
        assert call_kwargs['to_email'] == 'reset@test.spwig.com'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_context_contains_required_variables(self, mock_send, site_settings, django_site):
        """Context must include user_name, reset_url, expiry_hours."""
        user = UserFactory(email='ctx@test.spwig.com', first_name='Bob', last_name='Tester')
        from rest_framework.test import APIClient
        client = APIClient()
        client.post('/api/accounts/password-reset/', {'email': 'ctx@test.spwig.com'})
        context = mock_send.call_args[1]['context']
        assert 'user_name' in context
        assert 'reset_url' in context
        assert 'expiry_hours' in context
        assert context['user_name'] == 'Bob Tester'
        assert isinstance(context['expiry_hours'], int)
        assert context['expiry_hours'] > 0

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_reset_url_contains_uid_and_token(self, mock_send, site_settings, django_site):
        """Reset URL must contain uid and token segments."""
        user = UserFactory(email='url@test.spwig.com')
        from rest_framework.test import APIClient
        client = APIClient()
        client.post('/api/accounts/password-reset/', {'email': 'url@test.spwig.com'})
        reset_url = mock_send.call_args[1]['context']['reset_url']
        assert '/reset-password/' in reset_url
        # URL format: .../reset-password/<uid>/<token>/
        parts = reset_url.split('/reset-password/')[1].rstrip('/').split('/')
        assert len(parts) == 2, f"Expected uid/token segments, got: {parts}"

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_user_without_name_uses_email(self, mock_send, site_settings, django_site):
        """When user has no first/last name, user_name falls back to email."""
        user = UserFactory(
            email='noname@test.spwig.com',
            first_name='',
            last_name='',
        )
        from rest_framework.test import APIClient
        client = APIClient()
        client.post('/api/accounts/password-reset/', {'email': 'noname@test.spwig.com'})
        context = mock_send.call_args[1]['context']
        assert context['user_name'] == 'noname@test.spwig.com'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_nonexistent_email_returns_success_no_send(self, mock_send, site_settings, django_site):
        """Non-existent email returns 200 (anti-enumeration) but no email sent."""
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post('/api/accounts/password-reset/', {'email': 'nobody@test.spwig.com'})
        assert response.status_code == 200
        mock_send.assert_not_called()

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_invalid_email_returns_400(self, mock_send, site_settings, django_site):
        """Invalid email format returns 400."""
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post('/api/accounts/password-reset/', {'email': 'not-an-email'})
        assert response.status_code == 400
        mock_send.assert_not_called()

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_email_send_failure_does_not_crash(self, mock_send, site_settings, django_site):
        """If EmailSendingService raises, view still returns 200."""
        UserFactory(email='fail@test.spwig.com')
        mock_send.side_effect = Exception("SMTP error")
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post('/api/accounts/password-reset/', {'email': 'fail@test.spwig.com'})
        assert response.status_code == 200

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_inactive_user_not_sent(self, mock_send, site_settings, django_site):
        """Inactive user does not receive reset email."""
        UserFactory(email='inactive@test.spwig.com', is_active=False)
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post('/api/accounts/password-reset/', {'email': 'inactive@test.spwig.com'})
        assert response.status_code == 200
        mock_send.assert_not_called()


# ============================================================
# 2. Return Request Confirmation
# ============================================================

class TestReturnRequestConfirmation:
    """Verify orders/emails.py send_return_request_confirmation uses EmailSendingService."""

    @patch('email_system.utils.language.get_order_email_language', return_value='en')
    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_calls_send_template_email_with_correct_type(self, mock_send, mock_lang):
        """Uses 'return_request_confirmation' template type."""
        from orders.emails import send_return_request_confirmation
        rr = _mock_return_request()
        result = send_return_request_confirmation(rr)
        assert result is True
        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args[1]
        assert call_kwargs['template_type'] == 'return_request_confirmation'

    @patch('email_system.utils.language.get_order_email_language', return_value='en')
    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_context_contains_all_required_fields(self, mock_send, mock_lang):
        """Context includes customer_name, order_number, return_reason, items_count, return_status."""
        from orders.emails import send_return_request_confirmation
        rr = _mock_return_request()
        send_return_request_confirmation(rr)
        context = mock_send.call_args[1]['context']
        assert context['customer_name'] == 'Jane Customer'
        assert context['order_number'] == 'ORD-20260322-001'
        assert context['return_reason'] == 'Defective Product'
        assert context['items_count'] == 2  # len(items_json)
        assert context['return_status'] == 'Pending Approval'

    @patch('email_system.utils.language.get_order_email_language', return_value='en')
    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_sends_to_correct_email(self, mock_send, mock_lang):
        """Email is sent to the return request user's email."""
        from orders.emails import send_return_request_confirmation
        rr = _mock_return_request()
        send_return_request_confirmation(rr)
        assert mock_send.call_args[1]['to_email'] == 'customer@test.spwig.com'

    @patch('email_system.utils.language.get_order_email_language', return_value='de')
    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_uses_order_email_language(self, mock_send, mock_lang):
        """Language is derived from the order via get_order_email_language."""
        from orders.emails import send_return_request_confirmation
        rr = _mock_return_request()
        send_return_request_confirmation(rr)
        assert mock_send.call_args[1]['language'] == 'de'

    @patch('email_system.utils.language.get_order_email_language', return_value='en')
    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_tracking_enabled(self, mock_send, mock_lang):
        """Tracking is enabled for return confirmation emails."""
        from orders.emails import send_return_request_confirmation
        rr = _mock_return_request()
        send_return_request_confirmation(rr)
        assert mock_send.call_args[1]['enable_tracking'] is True

    @patch('email_system.utils.language.get_order_email_language', return_value='en')
    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_send_failure_returns_false(self, mock_send, mock_lang):
        """If send_template_email raises, function returns False."""
        from orders.emails import send_return_request_confirmation
        mock_send.side_effect = Exception("Template not found")
        rr = _mock_return_request()
        result = send_return_request_confirmation(rr)
        assert result is False

    @patch('email_system.utils.language.get_order_email_language', return_value='en')
    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_user_without_full_name_uses_username(self, mock_send, mock_lang):
        """When user has no full name, falls back to username."""
        from orders.emails import send_return_request_confirmation
        rr = _mock_return_request()
        rr.user.get_full_name.return_value = ''
        send_return_request_confirmation(rr)
        context = mock_send.call_args[1]['context']
        assert context['customer_name'] == 'jane_customer'

    @patch('email_system.utils.language.get_order_email_language', return_value='en')
    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_empty_items_json(self, mock_send, mock_lang):
        """Empty items_json results in items_count of 0."""
        from orders.emails import send_return_request_confirmation
        rr = _mock_return_request(items_json=[])
        send_return_request_confirmation(rr)
        context = mock_send.call_args[1]['context']
        assert context['items_count'] == 0


# ============================================================
# 3. Form Builder Email Notification
# ============================================================

class TestFormBuilderEmailNotification:
    """Verify form_builder/actions/email.py EmailNotificationAction uses EmailSendingService."""

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_calls_send_template_email_with_correct_type(self, mock_send, django_site):
        """Uses 'form_submission_admin_notification' template type."""
        from form_builder.actions.email import EmailNotificationAction
        action, form_response = _mock_form_action_and_response(
            to_emails=['admin@store.com']
        )
        executor = EmailNotificationAction(action, form_response)
        result = executor.execute()
        assert result['status'] == 'sent'
        mock_send.assert_called_once()
        assert mock_send.call_args[1]['template_type'] == 'form_submission_admin_notification'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_context_contains_required_variables(self, mock_send, django_site):
        """Context includes form_name, submitter_name, submitter_email, submission_date,
        submission_id, submission_data, admin_submission_url, reply_to_email."""
        from form_builder.actions.email import EmailNotificationAction
        action, form_response = _mock_form_action_and_response()
        executor = EmailNotificationAction(action, form_response)
        executor.execute()
        context = mock_send.call_args[1]['context']
        assert 'form_name' in context
        assert 'submitter_name' in context
        assert 'submitter_email' in context
        assert 'submission_date' in context
        assert 'submission_id' in context
        assert 'submission_data' in context
        assert 'admin_submission_url' in context
        assert 'reply_to_email' in context

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_submission_data_built_from_fields(self, mock_send, django_site):
        """submission_data list is built from form fields, excluding layout types."""
        from form_builder.actions.email import EmailNotificationAction
        action, form_response = _mock_form_action_and_response()
        executor = EmailNotificationAction(action, form_response)
        executor.execute()
        context = mock_send.call_args[1]['context']
        submission_data = context['submission_data']
        # All 3 fields have data, none are layout types
        assert len(submission_data) == 3
        labels = [item['label'] for item in submission_data]
        assert 'Full Name' in labels
        assert 'Email Address' in labels
        assert 'Your Message' in labels

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_include_data_false_skips_submission_data(self, mock_send, django_site):
        """When include_data is False, submission_data is empty."""
        from form_builder.actions.email import EmailNotificationAction
        action, form_response = _mock_form_action_and_response(include_data=False)
        executor = EmailNotificationAction(action, form_response)
        executor.execute()
        context = mock_send.call_args[1]['context']
        assert context['submission_data'] == []

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_sends_to_multiple_recipients(self, mock_send, django_site):
        """Each recipient gets a separate send_template_email call."""
        from form_builder.actions.email import EmailNotificationAction
        to_emails = ['admin@store.com', 'support@store.com', 'ceo@store.com']
        action, form_response = _mock_form_action_and_response(to_emails=to_emails)
        executor = EmailNotificationAction(action, form_response)
        result = executor.execute()
        assert result['status'] == 'sent'
        assert mock_send.call_count == 3
        sent_emails = [c[1]['to_email'] for c in mock_send.call_args_list]
        assert set(sent_emails) == set(to_emails)

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_no_recipients_returns_skipped(self, mock_send, django_site):
        """No configured recipients returns 'skipped' status."""
        from form_builder.actions.email import EmailNotificationAction
        action, form_response = _mock_form_action_and_response(to_emails=[])
        executor = EmailNotificationAction(action, form_response)
        result = executor.execute()
        assert result['status'] == 'skipped'
        mock_send.assert_not_called()

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_tracking_disabled(self, mock_send, django_site):
        """Admin notification emails have tracking disabled."""
        from form_builder.actions.email import EmailNotificationAction
        action, form_response = _mock_form_action_and_response()
        executor = EmailNotificationAction(action, form_response)
        executor.execute()
        assert mock_send.call_args[1]['enable_tracking'] is False

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_submission_id_format(self, mock_send, django_site):
        """submission_id follows FORM-{pk} format."""
        from form_builder.actions.email import EmailNotificationAction
        action, form_response = _mock_form_action_and_response()
        executor = EmailNotificationAction(action, form_response)
        executor.execute()
        context = mock_send.call_args[1]['context']
        assert context['submission_id'] == 'FORM-99'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_admin_url_includes_response_pk(self, mock_send, django_site):
        """admin_submission_url points to the correct FormResponse admin page."""
        from form_builder.actions.email import EmailNotificationAction
        action, form_response = _mock_form_action_and_response()
        executor = EmailNotificationAction(action, form_response)
        executor.execute()
        context = mock_send.call_args[1]['context']
        assert '/en/admin/form_builder/formresponse/99/change/' in context['admin_submission_url']

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_partial_send_failure(self, mock_send, django_site):
        """If one recipient fails, others still get sent."""
        from form_builder.actions.email import EmailNotificationAction

        def side_effect(**kwargs):
            if kwargs['to_email'] == 'bad@store.com':
                raise Exception("SMTP failure")
            return None

        mock_send.side_effect = side_effect
        action, form_response = _mock_form_action_and_response(
            to_emails=['good@store.com', 'bad@store.com', 'ok@store.com']
        )
        executor = EmailNotificationAction(action, form_response)
        result = executor.execute()
        assert result['status'] == 'sent'
        assert 'good@store.com' in result['recipients']
        assert 'ok@store.com' in result['recipients']
        assert 'bad@store.com' not in result['recipients']

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_all_recipients_fail(self, mock_send, django_site):
        """If all recipients fail, status is 'error'."""
        from form_builder.actions.email import EmailNotificationAction
        mock_send.side_effect = Exception("Total failure")
        action, form_response = _mock_form_action_and_response(
            to_emails=['a@store.com']
        )
        executor = EmailNotificationAction(action, form_response)
        result = executor.execute()
        assert result['status'] == 'error'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_empty_field_values_excluded_from_submission_data(self, mock_send, django_site):
        """Fields with empty values are not included in submission_data."""
        from form_builder.actions.email import EmailNotificationAction
        action, form_response = _mock_form_action_and_response(
            form_data={'name': 'John', 'email': '', 'message': 'Hello'}
        )
        executor = EmailNotificationAction(action, form_response)
        executor.execute()
        context = mock_send.call_args[1]['context']
        # email field has empty value, should be excluded
        labels = [item['label'] for item in context['submission_data']]
        assert 'Email Address' not in labels
        assert 'Full Name' in labels
        assert 'Your Message' in labels


# ============================================================
# 4. Form Builder Auto-Reply
# ============================================================

class TestFormBuilderAutoReply:
    """Verify form_builder/actions/email.py AutoReplyAction uses EmailSendingService."""

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_calls_send_template_email_with_correct_type(self, mock_send):
        """Uses 'form_submission_auto_response' template type."""
        from form_builder.actions.email import AutoReplyAction
        action, form_response = _mock_auto_reply_action_and_response()
        executor = AutoReplyAction(action, form_response)
        result = executor.execute()
        assert result['status'] == 'sent'
        mock_send.assert_called_once()
        assert mock_send.call_args[1]['template_type'] == 'form_submission_auto_response'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_context_contains_required_variables(self, mock_send):
        """Context includes submitter_name, auto_response_subject, auto_response_heading,
        auto_response_message, submission_id."""
        from form_builder.actions.email import AutoReplyAction
        action, form_response = _mock_auto_reply_action_and_response()
        executor = AutoReplyAction(action, form_response)
        executor.execute()
        context = mock_send.call_args[1]['context']
        assert 'submitter_name' in context
        assert 'auto_response_subject' in context
        assert 'auto_response_heading' in context
        assert 'auto_response_message' in context
        assert 'submission_id' in context

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_subject_and_heading_from_config(self, mock_send):
        """auto_response_subject and heading come from the action config."""
        from form_builder.actions.email import AutoReplyAction
        action, form_response = _mock_auto_reply_action_and_response(
            subject='We received your inquiry'
        )
        executor = AutoReplyAction(action, form_response)
        executor.execute()
        context = mock_send.call_args[1]['context']
        assert context['auto_response_subject'] == 'We received your inquiry'
        assert context['auto_response_heading'] == 'We received your inquiry'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_body_template_rendered_with_context(self, mock_send):
        """body_template is rendered with form context variables (e.g. {{submitter_name}})."""
        from form_builder.actions.email import AutoReplyAction
        action, form_response = _mock_auto_reply_action_and_response(
            body_template='Dear {{submitter_name}}, thanks for reaching out.'
        )
        executor = AutoReplyAction(action, form_response)
        executor.execute()
        context = mock_send.call_args[1]['context']
        assert 'Alice Smith' in context['auto_response_message']

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_sends_to_submitter_email_from_form_data(self, mock_send):
        """Sends to the email from the configured email_field in form data."""
        from form_builder.actions.email import AutoReplyAction
        action, form_response = _mock_auto_reply_action_and_response()
        executor = AutoReplyAction(action, form_response)
        executor.execute()
        assert mock_send.call_args[1]['to_email'] == 'alice@example.com'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_fallback_to_user_email(self, mock_send):
        """When email_field is empty, falls back to authenticated user's email."""
        from form_builder.actions.email import AutoReplyAction
        user = MagicMock()
        user.email = 'authuser@example.com'
        action, form_response = _mock_auto_reply_action_and_response(
            form_data={'name': 'Bob', 'email': ''},
            user=user,
        )
        executor = AutoReplyAction(action, form_response)
        executor.execute()
        assert mock_send.call_args[1]['to_email'] == 'authuser@example.com'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_no_email_skips(self, mock_send):
        """No submitter email and no user returns 'skipped'."""
        from form_builder.actions.email import AutoReplyAction
        action, form_response = _mock_auto_reply_action_and_response(
            form_data={'name': 'Anon', 'email': ''},
            user=None,
        )
        executor = AutoReplyAction(action, form_response)
        result = executor.execute()
        assert result['status'] == 'skipped'
        mock_send.assert_not_called()

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_tracking_disabled(self, mock_send):
        """Auto-reply emails have tracking disabled."""
        from form_builder.actions.email import AutoReplyAction
        action, form_response = _mock_auto_reply_action_and_response()
        executor = AutoReplyAction(action, form_response)
        executor.execute()
        assert mock_send.call_args[1]['enable_tracking'] is False

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_submission_id_format(self, mock_send):
        """submission_id uses FORM-{pk} format."""
        from form_builder.actions.email import AutoReplyAction
        action, form_response = _mock_auto_reply_action_and_response()
        executor = AutoReplyAction(action, form_response)
        executor.execute()
        context = mock_send.call_args[1]['context']
        assert context['submission_id'] == 'FORM-55'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_send_failure_returns_error(self, mock_send):
        """If send_template_email raises, result status is 'error'."""
        from form_builder.actions.email import AutoReplyAction
        mock_send.side_effect = Exception("Queue full")
        action, form_response = _mock_auto_reply_action_and_response()
        executor = AutoReplyAction(action, form_response)
        result = executor.execute()
        assert result['status'] == 'error'
        assert 'Queue full' in result['error']

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_custom_email_field(self, mock_send):
        """Can configure a custom field name for the submitter's email."""
        from form_builder.actions.email import AutoReplyAction
        action, form_response = _mock_auto_reply_action_and_response(
            email_field='contact_email',
            form_data={'name': 'Custom', 'email': '', 'contact_email': 'custom@test.com'},
        )
        executor = AutoReplyAction(action, form_response)
        executor.execute()
        assert mock_send.call_args[1]['to_email'] == 'custom@test.com'


# ============================================================
# 5. POS License Expiration Warning
# ============================================================

class TestPOSLicenseExpirationWarning:
    """Verify pos_app/tasks.py _send_pos_expiration_warning uses EmailSendingService."""

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_calls_send_template_email_with_correct_type(self, mock_ss_objects, mock_send):
        """Uses 'pos_license_expiration_warning' template type."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = 'admin@store.com'
        mock_ss_objects.first.return_value = ss

        config = MagicMock()
        config.pos_license_key = 'ABCD1234EFGH5678IJKL'
        config.pos_license_expires_at = timezone.now() + timedelta(days=30)

        _send_pos_expiration_warning(config, 30)
        mock_send.assert_called_once()
        assert mock_send.call_args[1]['template_type'] == 'pos_license_expiration_warning'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_context_contains_required_variables(self, mock_ss_objects, mock_send):
        """Context includes days_remaining, license_key_masked, expires_at,
        is_grace_period, renewal_url."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = 'admin@store.com'
        mock_ss_objects.first.return_value = ss

        expires = timezone.now() + timedelta(days=7)
        config = MagicMock()
        config.pos_license_key = 'ABCDEFGH12345678WXYZ'
        config.pos_license_expires_at = expires

        _send_pos_expiration_warning(config, 7)
        context = mock_send.call_args[1]['context']
        assert context['days_remaining'] == 7
        assert 'license_key_masked' in context
        assert context['expires_at'] == str(expires)
        assert context['is_grace_period'] is False
        assert context['renewal_url'] == 'https://spwig.com/pos'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_license_key_masking_long_key(self, mock_ss_objects, mock_send):
        """License key > 12 chars is masked: first 8 + **** + last 4."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = 'admin@store.com'
        mock_ss_objects.first.return_value = ss

        config = MagicMock()
        config.pos_license_key = 'ABCDEFGH12345678WXYZ'  # 20 chars
        config.pos_license_expires_at = timezone.now() + timedelta(days=30)

        _send_pos_expiration_warning(config, 30)
        context = mock_send.call_args[1]['context']
        assert context['license_key_masked'] == 'ABCDEFGH****WXYZ'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_license_key_masking_short_key(self, mock_ss_objects, mock_send):
        """License key <= 12 chars is NOT masked (shown as-is)."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = 'admin@store.com'
        mock_ss_objects.first.return_value = ss

        config = MagicMock()
        config.pos_license_key = 'SHORT123'  # 8 chars, <= 12
        config.pos_license_expires_at = timezone.now() + timedelta(days=1)

        _send_pos_expiration_warning(config, 1)
        context = mock_send.call_args[1]['context']
        assert context['license_key_masked'] == 'SHORT123'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_grace_period_flag(self, mock_ss_objects, mock_send):
        """When grace=True, context['is_grace_period'] is True."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = 'admin@store.com'
        mock_ss_objects.first.return_value = ss

        config = MagicMock()
        config.pos_license_key = 'ABCDEFGHIJKLMNOP'
        config.pos_license_expires_at = timezone.now() - timedelta(days=5)

        _send_pos_expiration_warning(config, 9, grace=True)
        context = mock_send.call_args[1]['context']
        assert context['is_grace_period'] is True
        assert context['days_remaining'] == 9

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_sends_to_admin_email(self, mock_ss_objects, mock_send):
        """Sends to SiteSettings.admin_email."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = 'boss@mystore.com'
        mock_ss_objects.first.return_value = ss

        config = MagicMock()
        config.pos_license_key = 'ABCDEFGHIJKLMNOP'
        config.pos_license_expires_at = timezone.now() + timedelta(days=30)

        _send_pos_expiration_warning(config, 30)
        assert mock_send.call_args[1]['to_email'] == 'boss@mystore.com'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_no_site_settings_skips(self, mock_ss_objects, mock_send):
        """No SiteSettings record skips sending."""
        from pos_app.tasks import _send_pos_expiration_warning
        mock_ss_objects.first.return_value = None

        config = MagicMock()
        config.pos_license_key = 'ABCDEFGHIJKLMNOP'
        config.pos_license_expires_at = timezone.now() + timedelta(days=30)

        _send_pos_expiration_warning(config, 30)
        mock_send.assert_not_called()

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_no_admin_email_skips(self, mock_ss_objects, mock_send):
        """Empty admin_email skips sending."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = ''
        mock_ss_objects.first.return_value = ss

        config = MagicMock()
        config.pos_license_key = 'ABCDEFGHIJKLMNOP'
        config.pos_license_expires_at = timezone.now() + timedelta(days=30)

        _send_pos_expiration_warning(config, 30)
        mock_send.assert_not_called()

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_tracking_disabled(self, mock_ss_objects, mock_send):
        """POS warning emails have tracking disabled."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = 'admin@store.com'
        mock_ss_objects.first.return_value = ss

        config = MagicMock()
        config.pos_license_key = 'ABCDEFGHIJKLMNOP'
        config.pos_license_expires_at = timezone.now() + timedelta(days=30)

        _send_pos_expiration_warning(config, 30)
        assert mock_send.call_args[1]['enable_tracking'] is False

    @patch('core.models.SiteSettings.objects')
    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    def test_language_is_english(self, mock_send, mock_ss_objects):
        """POS warning emails are always sent in English."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = 'admin@store.com'
        mock_ss_objects.first.return_value = ss

        config = MagicMock()
        config.pos_license_key = 'ABCDEFGHIJKLMNOP'
        config.pos_license_expires_at = timezone.now() + timedelta(days=30)

        _send_pos_expiration_warning(config, 30)
        assert mock_send.call_args[1]['language'] == 'en'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_send_failure_does_not_raise(self, mock_ss_objects, mock_send):
        """If EmailSendingService raises, function handles it gracefully."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = 'admin@store.com'
        mock_ss_objects.first.return_value = ss
        mock_send.side_effect = Exception("SMTP down")

        config = MagicMock()
        config.pos_license_key = 'ABCDEFGHIJKLMNOP'
        config.pos_license_expires_at = timezone.now() + timedelta(days=30)

        # Should not raise
        _send_pos_expiration_warning(config, 30)

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('core.models.SiteSettings.objects')
    def test_none_license_key(self, mock_ss_objects, mock_send):
        """None license key is handled gracefully (empty string fallback)."""
        from pos_app.tasks import _send_pos_expiration_warning

        ss = MagicMock()
        ss.admin_email = 'admin@store.com'
        mock_ss_objects.first.return_value = ss

        config = MagicMock()
        config.pos_license_key = None
        config.pos_license_expires_at = None

        _send_pos_expiration_warning(config, 5)
        context = mock_send.call_args[1]['context']
        assert context['license_key_masked'] == ''
        assert context['expires_at'] == ''


# ============================================================
# 6. Staff Password Reset — Fallback Removed
# ============================================================

class TestStaffPasswordResetFallbackRemoval:
    """Verify admin_api/views/auth.py staff_password_reset_request has NO send_mail fallback."""

    def test_no_send_mail_import(self):
        """django.core.mail.send_mail is not imported in admin_api/views/auth.py."""
        assert not _file_contains_string('admin_api/views/auth.py', 'send_mail')

    def test_no_email_multi_alternatives_import(self):
        """EmailMultiAlternatives is not referenced in admin_api/views/auth.py."""
        assert not _file_contains_string('admin_api/views/auth.py', 'EmailMultiAlternatives')

    def test_no_django_core_mail_import(self):
        """django.core.mail module is not imported at all."""
        assert not _file_contains_string('admin_api/views/auth.py', 'django.core.mail')

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('admin_api.services.audit_service.AuditService.log')
    def test_staff_reset_uses_email_sending_service(self, mock_audit, mock_send, site_settings, django_site):
        """Staff password reset uses EmailSendingService, not send_mail."""
        user = UserFactory(
            email='staff@test.spwig.com',
            is_staff=True,
            is_active=True,
        )
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post(
            '/api/admin/auth/password-reset/',
            {'email': 'staff@test.spwig.com'},
        )
        assert response.status_code == 200
        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args[1]
        assert call_kwargs['template_type'] == 'password_reset'
        assert call_kwargs['to_email'] == 'staff@test.spwig.com'

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('admin_api.services.audit_service.AuditService.log')
    def test_staff_reset_context(self, mock_audit, mock_send, site_settings, django_site):
        """Staff reset includes user_name, reset_url, expiry_hours."""
        user = UserFactory(
            email='staffctx@test.spwig.com',
            first_name='Admin',
            last_name='User',
            is_staff=True,
        )
        from rest_framework.test import APIClient
        client = APIClient()
        client.post('/api/admin/auth/password-reset/', {'email': 'staffctx@test.spwig.com'})
        context = mock_send.call_args[1]['context']
        assert context['user_name'] == 'Admin User'
        assert '/reset-password/' in context['reset_url']
        assert isinstance(context['expiry_hours'], int)

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('admin_api.services.audit_service.AuditService.log')
    def test_staff_reset_non_staff_user_not_sent(self, mock_audit, mock_send, site_settings, django_site):
        """Non-staff user email triggers no send (view only queries is_staff=True)."""
        UserFactory(email='regular@test.spwig.com', is_staff=False)
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post('/api/admin/auth/password-reset/', {'email': 'regular@test.spwig.com'})
        assert response.status_code == 200
        mock_send.assert_not_called()

    @patch('email_system.services.email_sender.EmailSendingService.send_template_email')
    @patch('admin_api.services.audit_service.AuditService.log')
    def test_staff_reset_error_does_not_crash(self, mock_audit, mock_send, site_settings, django_site):
        """EmailSendingService failure doesn't crash the view."""
        UserFactory(email='stafferr@test.spwig.com', is_staff=True)
        mock_send.side_effect = Exception("Template missing")
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post('/api/admin/auth/password-reset/', {'email': 'stafferr@test.spwig.com'})
        assert response.status_code == 200


# ============================================================
# 7. Zero Remaining Legacy Calls
# ============================================================

class TestZeroLegacyCalls:
    """Verify no migrated file still imports send_mail or EmailMultiAlternatives."""

    @pytest.mark.parametrize('filepath', MIGRATED_FILES)
    def test_no_send_mail_import(self, filepath):
        """No file imports or references send_mail."""
        assert not _file_contains_string(filepath, 'send_mail'), \
            f"{filepath} still references 'send_mail'"

    @pytest.mark.parametrize('filepath', MIGRATED_FILES)
    def test_no_email_multi_alternatives(self, filepath):
        """No file imports or references EmailMultiAlternatives."""
        assert not _file_contains_string(filepath, 'EmailMultiAlternatives'), \
            f"{filepath} still references 'EmailMultiAlternatives'"

    @pytest.mark.parametrize('filepath', MIGRATED_FILES)
    def test_no_django_core_mail_import(self, filepath):
        """No file imports from django.core.mail."""
        assert not _file_contains_string(filepath, 'from django.core.mail'), \
            f"{filepath} still imports from django.core.mail"

    @pytest.mark.parametrize('filepath', MIGRATED_FILES)
    def test_uses_email_sending_service(self, filepath):
        """Every migrated file references EmailSendingService."""
        assert _file_contains_string(filepath, 'EmailSendingService'), \
            f"{filepath} does not use EmailSendingService"

    @pytest.mark.parametrize('filepath', MIGRATED_FILES)
    def test_uses_send_template_email(self, filepath):
        """Every migrated file calls send_template_email."""
        assert _file_contains_string(filepath, 'send_template_email'), \
            f"{filepath} does not call send_template_email"
