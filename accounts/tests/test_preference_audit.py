"""
Tests for Preference Change Audit Log functionality.

Tests the PreferenceChangeLog model, PreferenceAuditService, and integration
with PreferenceService for GDPR Article 7 compliance.
"""
import pytest
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from accounts.models import CommunicationPreference, PreferenceChangeLog
from accounts.services.preference_service import PreferenceService
from accounts.services.preference_audit_service import PreferenceAuditService
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.unit, pytest.mark.preferences]


class TestPreferenceChangeLogModel:
    """Test PreferenceChangeLog model functionality."""

    def test_create_log_entry(self, db):
        """Test creating a preference change log entry."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        log = PreferenceChangeLog.objects.create(
            user=user,
            preference=prefs,
            action='email_marketing.enable',
            old_value={'email_marketing': False},
            new_value={'email_marketing': True},
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0',
            source='user',
            notes='Customer opted into marketing emails',
        )

        assert log.user == user
        assert log.preference == prefs
        assert log.action == 'email_marketing.enable'
        assert log.old_value == {'email_marketing': False}
        assert log.new_value == {'email_marketing': True}
        assert log.ip_address == '192.168.1.1'
        assert log.source == 'user'
        assert log.timestamp is not None

    def test_log_string_representation(self, db):
        """Test __str__ method."""
        user = UserFactory(email='test@example.com')
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        log = PreferenceChangeLog.objects.create(
            user=user,
            preference=prefs,
            action='sms_marketing.disable',
            old_value={},
            new_value={},
            source='api',
        )

        assert 'test@example.com' in str(log)
        assert 'sms_marketing.disable' in str(log)

    def test_cleanup_old_logs(self, db):
        """Test cleanup_old_logs() class method."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Create old log (91 days ago)
        old_timestamp = timezone.now() - timedelta(days=91)
        old_log = PreferenceChangeLog.objects.create(
            user=user,
            preference=prefs,
            action='test.old',
            old_value={},
            new_value={},
            source='system',
        )
        PreferenceChangeLog.objects.filter(id=old_log.id).update(timestamp=old_timestamp)

        # Create recent log (30 days ago)
        recent_timestamp = timezone.now() - timedelta(days=30)
        recent_log = PreferenceChangeLog.objects.create(
            user=user,
            preference=prefs,
            action='test.recent',
            old_value={},
            new_value={},
            source='system',
        )
        PreferenceChangeLog.objects.filter(id=recent_log.id).update(timestamp=recent_timestamp)

        # Cleanup logs older than 90 days
        deleted_count = PreferenceChangeLog.cleanup_old_logs(days=90)

        assert deleted_count == 1
        assert not PreferenceChangeLog.objects.filter(id=old_log.id).exists()
        assert PreferenceChangeLog.objects.filter(id=recent_log.id).exists()

    def test_cascade_delete_with_user(self, db):
        """Test that logs are deleted when user is deleted."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        log = PreferenceChangeLog.objects.create(
            user=user,
            preference=prefs,
            action='test.action',
            old_value={},
            new_value={},
            source='user',
        )

        log_id = log.id
        user.delete()

        assert not PreferenceChangeLog.objects.filter(id=log_id).exists()

    def test_cascade_delete_with_preference(self, db):
        """Test that logs are deleted when preference is deleted."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        log = PreferenceChangeLog.objects.create(
            user=user,
            preference=prefs,
            action='test.action',
            old_value={},
            new_value={},
            source='user',
        )

        log_id = log.id
        prefs.delete()

        assert not PreferenceChangeLog.objects.filter(id=log_id).exists()


class TestPreferenceAuditService:
    """Test PreferenceAuditService functionality."""

    def test_log_change_basic(self, db):
        """Test basic log_change functionality."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        log = PreferenceAuditService.log_change(
            preference=prefs,
            action='email_marketing.enable',
            old_value={'email_marketing': False},
            new_value={'email_marketing': True},
            source='user',
            ip_address='10.0.0.1',
            user_agent='TestAgent/1.0',
        )

        assert log is not None
        assert log.user == user
        assert log.preference == prefs
        assert log.action == 'email_marketing.enable'
        assert log.ip_address == '10.0.0.1'
        assert log.source == 'user'

    def test_log_change_with_request(self, db):
        """Test log_change with HttpRequest object."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        factory = RequestFactory()
        request = factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.100'
        request.META['HTTP_USER_AGENT'] = 'Mozilla/5.0'

        log = PreferenceAuditService.log_change(
            preference=prefs,
            action='test.action',
            old_value={},
            new_value={},
            request=request,
            source='api',
        )

        assert log.ip_address == '192.168.1.100'
        assert log.user_agent == 'Mozilla/5.0'

    def test_log_change_with_x_forwarded_for(self, db):
        """Test IP extraction from X-Forwarded-For header."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        factory = RequestFactory()
        request = factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '203.0.113.1, 198.51.100.1'
        request.META['REMOTE_ADDR'] = '192.168.1.1'

        log = PreferenceAuditService.log_change(
            preference=prefs,
            action='test.action',
            old_value={},
            new_value={},
            request=request,
            source='user',
        )

        # Should use first IP from X-Forwarded-For
        assert log.ip_address == '203.0.113.1'

    def test_log_change_error_handling(self, db):
        """Test that logging errors don't break the main operation."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Pass invalid data - should not raise exception
        log = PreferenceAuditService.log_change(
            preference=None,  # Invalid - will cause error
            action='test.action',
            old_value={},
            new_value={},
            source='user',
        )

        # Should return None on error, not raise exception
        assert log is None

    def test_log_verification(self, db):
        """Test log_verification method."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        log = PreferenceAuditService.log_verification(
            preference=prefs,
            channel='email',
        )

        assert log is not None
        assert log.action == 'email_verified'
        assert log.source == 'verification'
        assert log.old_value == {'email_verified': False}
        assert log.new_value == {'email_verified': True}

    def test_log_bulk_update(self, db):
        """Test log_bulk_update method."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        changes = {
            'email_marketing': {'old': False, 'new': True},
            'sms_marketing': {'old': False, 'new': True},
        }

        log = PreferenceAuditService.log_bulk_update(
            preference=prefs,
            changes=changes,
            source='admin',
        )

        assert log is not None
        assert log.action == 'bulk_update.2_fields'
        assert log.old_value == {'email_marketing': False, 'sms_marketing': False}
        assert log.new_value == {'email_marketing': True, 'sms_marketing': True}

    def test_log_unsubscribe_all(self, db):
        """Test log_unsubscribe_all method."""
        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]
        prefs.email_marketing = True
        prefs.app_preferences = {'blog': {'enabled': True}}
        prefs.save()

        log = PreferenceAuditService.log_unsubscribe_all(
            preference=prefs,
            reason='Too many emails',
        )

        assert log is not None
        assert log.action == 'unsubscribe_all'
        assert log.source == 'unsubscribe'
        assert 'Too many emails' in log.notes


class TestPreferenceServiceAuditIntegration:
    """Test audit logging integration with PreferenceService."""

    def test_update_preference_creates_audit_log(self, db):
        """Test that update_preference creates an audit log."""
        user = UserFactory()

        # Update preference
        PreferenceService.update_preference(
            user=user,
            channel='email',
            message_type='newsletter',
            enabled=True,
            ip_address='192.168.1.1',
            user_agent='TestBrowser/1.0',
        )

        # Check audit log was created
        logs = PreferenceChangeLog.objects.filter(user=user)
        assert logs.count() == 1

        log = logs.first()
        assert 'email_marketing' in log.action
        assert log.source == 'user'
        assert log.ip_address == '192.168.1.1'

    def test_verify_email_creates_audit_log(self, db):
        """Test that verify_email creates an audit log."""
        from django.core.cache import cache
        from django.utils import timezone
        import secrets

        user = UserFactory()
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Manually create verification token in cache (skip email sending)
        token = secrets.token_urlsafe(32)
        cache_key = f'email_verify:{token}'
        cache.set(cache_key, {
            'user_id': user.id,
            'timestamp': timezone.now().isoformat(),
        }, timeout=86400)

        # Verify email
        PreferenceService.verify_email(
            token=token,
            ip_address='10.0.0.1',
            user_agent='VerifyAgent/1.0',
        )

        # Check audit log was created
        logs = PreferenceChangeLog.objects.filter(user=user, action='email_verified')
        assert logs.count() == 1

        log = logs.first()
        assert log.source == 'verification'

    def test_unsubscribe_all_creates_audit_log(self, db):
        """Test that unsubscribe_all creates an audit log."""
        user = UserFactory()

        # Unsubscribe from all
        PreferenceService.unsubscribe_all(
            user=user,
            reason='Not interested',
        )

        # Check audit log was created
        logs = PreferenceChangeLog.objects.filter(user=user, action='unsubscribe_all')
        assert logs.count() == 1

        log = logs.first()
        assert log.source == 'unsubscribe'
        assert 'Not interested' in log.notes

    def test_audit_log_with_request_object(self, db):
        """Test audit logging with HttpRequest object."""
        user = UserFactory()

        factory = RequestFactory()
        request = factory.post('/')
        request.META['REMOTE_ADDR'] = '203.0.113.50'
        request.META['HTTP_USER_AGENT'] = 'CustomBrowser/2.0'

        # Update with request
        PreferenceService.update_preference(
            user=user,
            channel='email',
            message_type='newsletter',
            enabled=True,
            request=request,
        )

        log = PreferenceChangeLog.objects.filter(user=user).first()
        assert log.ip_address == '203.0.113.50'
        assert log.user_agent == 'CustomBrowser/2.0'
