# Communication Preferences Test Suite

This directory contains comprehensive integration tests for the Customer Communication Preferences System implemented in Weeks 1-6.

**Total: 180+ tests across 9 test files**

## Test Coverage

### 1. Model Tests (`test_communication_preferences_model.py`)
**20+ tests covering:**
- ✅ Model creation & default values (GDPR opt-out, TCPA opt-in compliance)
- ✅ Automatic unsubscribe token generation (unique 64-char tokens)
- ✅ `should_send_email()` method behavior:
  - Transactional emails always allowed
  - Marketing emails require `email_marketing=True` AND `email_verified=True`
  - App-specific email types check nested `app_preferences`
  - Master `email_enabled` toggle blocks all non-critical emails
- ✅ `should_send_sms()` method behavior:
  - All SMS requires explicit opt-in (TCPA compliance)
  - Separate transactional vs marketing opt-in
  - Master `sms_enabled` toggle blocks all SMS
- ✅ `get_app_preference()` / `update_app_preference()` methods
- ✅ Edge cases (unique constraints, preference persistence)

### 2. Service Layer Tests (`test_preference_service.py`)
**18+ tests covering:**
- ✅ `PreferenceService.get_or_create_for_user()` (create vs return existing)
- ✅ `PreferenceService.check_email_permission()`:
  - Transactional always allowed
  - Marketing requires verification
  - App-specific preference checks (blog, loyalty, referrals, affiliate)
  - Unknown types default to marketing check
- ✅ `PreferenceService.check_sms_permission()`:
  - TCPA opt-in requirements
  - Transactional vs marketing separation
  - Master toggle behavior
- ✅ Caching behavior:
  - 5-minute TTL on permission checks
  - Cache invalidation on updates
  - Performance optimization (reduce DB queries)
- ✅ `PreferenceService.update_preference()` (field updates, cache invalidation)
- ✅ Edge cases (None user for guests, auto-create missing preference)

### 3. Email Integration Tests (`test_email_preference_integration.py`)
**25+ tests covering:**
- ✅ `EmailSendingService.queue_email()` with preference checking:
  - Transactional emails always sent
  - Marketing emails skipped when disabled/unverified
  - Guest emails sent normally
- ✅ `EmailSendingService.send_template_email()` with preferences
- ✅ Unsubscribe footer injection:
  - Added to HTML marketing emails (before `</body>`)
  - Added to plain text marketing emails (at end)
  - NOT added to transactional emails
  - Not duplicated if already present
- ✅ `EmailOutbox` status tracking:
  - Status='skipped' when preference disabled
  - `skip_reason='user_preference_disabled'`
  - Audit trail for compliance
- ✅ App-specific email preferences:
  - Blog post notifications
  - Loyalty points/tier/rewards
  - Referral rewards
  - Affiliate commissions
- ✅ Master email toggle behavior
- ✅ Guest user handling (no preference check)

### 4. SMS Integration Tests (`test_sms_preference_integration.py`)
**15+ tests covering:**
- ✅ `SMSSendingService.send_sms()` with preference checking:
  - Transactional SMS sent when opted in
  - SMS skipped when opted out
  - Marketing SMS requires separate opt-in (TCPA)
  - Guest SMS sent normally (no phone number match in CustomerProfile)
- ✅ `SMSSendingService.send_template_sms()` passes template_type for checking
- ✅ `SMSOutbox` status tracking:
  - Status='skipped' when preference disabled
  - `skip_reason='user_preference_disabled'`
  - SMS without message_type bypasses check (legacy support)
- ✅ Master SMS toggle behavior
- ✅ Phone number lookup via `CustomerProfile.phone`
- ✅ Provider error handling (still creates outbox entry with status='failed')

### 5. API Tests (`test_communication_preferences_api.py`)
**20+ tests covering:**
- ✅ `GET /api/accounts/communication-preferences/`:
  - Requires authentication
  - Returns full preference structure
  - Includes `email_categories` grouping for UI
  - Returns custom values correctly
- ✅ `POST /api/accounts/communication-preferences/update/`:
  - Updates email_marketing, sms_transactional, etc.
  - Updates app-specific preferences (blog, loyalty, etc.)
  - Supports frequency parameter
  - Validates channel/message_type
  - Invalidates cache after update
- ✅ `POST /api/accounts/communication-preferences/bulk-update/`:
  - Updates multiple preferences atomically
  - Rolls back on validation error
  - Handles empty update list
- ✅ `POST /api/accounts/communication-preferences/unsubscribe-all/`:
  - Disables all marketing (email, SMS, all apps)
  - Keeps transactional emails enabled
  - Invalidates cache
- ✅ Edge cases (auto-create preference, corrupted JSON)

### 6. View Tests (`test_communication_preferences_views.py`)
**18+ tests covering:**
- ✅ Preference center (`/accounts/preferences/`) GET:
  - Requires authentication (redirects to login)
  - Displays current preferences
  - Shows verification badge
  - Auto-creates preference if missing
- ✅ Preference center POST:
  - Updates email_marketing, blog_enabled, etc.
  - Handles unchecked checkboxes (sets to False)
  - Updates app_preferences JSON
  - Shows success message
  - Invalidates cache
- ✅ Unsubscribe page (`/accounts/unsubscribe/<token>/`) GET:
  - Accessible with valid token (no login required)
  - Shows user email
  - Returns 404 for invalid token
- ✅ Unsubscribe page POST:
  - Disables marketing communications
  - Disables all app marketing
  - Keeps transactional enabled
  - Accepts optional reason
  - Shows success message
- ✅ Edge cases (corrupted JSON, URL-safe tokens, no-op updates)

### 7. Blog Integration Tests (`test_blog_preference_integration.py`)
**15+ tests covering:**
- ✅ Dual system support:
  - Sends to legacy `BlogSubscriber` users
  - Sends to new `CommunicationPreference` users
  - No duplicate emails when email in both systems
- ✅ New system preference checks:
  - Respects `app_preferences['blog']['enabled']`
  - Respects frequency (immediate vs weekly vs monthly)
  - Requires `email_verified=True`
  - Checks category subscriptions
- ✅ Legacy `BlogSubscriber` compatibility:
  - Immediate frequency sends immediately
  - Weekly/monthly digest doesn't send immediately
  - Unverified subscribers skipped
- ✅ Correct message_type (`blog_post_published`) for preference checks
- ✅ Edge cases (no subscribers, both systems active)

### 8. Referrals Integration Tests (`test_referrals_preference_integration.py`)
**15+ tests covering:**
- ✅ Referral reward emails:
  - Respects `app_preferences['referrals']['enabled']`
  - Requires `email_verified=True`
  - Skipped status when preference disabled
  - Separate templates for referrer vs referee
  - Attribution and referrer identity context
- ✅ Referral successful emails:
  - Sent when referral signs up
  - Respects referrer's preferences
  - Includes referral stats and dashboard link
- ✅ Reward expiring emails:
  - Sent when reward about to expire
  - Respects user preferences
  - Includes expiration date context
- ✅ Referral invitation emails:
  - Sent to non-registered users (guests)
  - Respects registered user preferences
  - Guest users bypass preference checks
  - Personal message support
- ✅ Correct message_type usage (`referral_reward_issued_referrer`, `referral_reward_issued_referee`, `referral_successful`, `referral_reward_expiring`, `referral_invitation`)
- ✅ Edge cases (missing language preference, email verification requirements)

### 9. Admin Interface Tests (`test_communication_preferences_admin.py`)
**35+ tests covering:**
- ✅ Admin registration and configuration:
  - Model registered in admin site
  - List display fields (user_email, status icons, verification badges)
  - List filters (all preference toggles, consent_source, language)
  - Search fields (user email/name, unsubscribe_token)
  - Readonly fields (consent metadata, timestamps)
- ✅ Display methods:
  - `user_email()` - link to user admin
  - `email_status()` / `sms_status()` - green check / gray circle
  - `marketing_status()` - opted in/out badge
  - `verification_status()` - email/SMS verification icons
  - `consent_source_display()` - icon + label
- ✅ Admin actions:
  - `bulk_verify_email` - marks selected users verified, invalidates cache
  - `bulk_unsubscribe_marketing` - disables all marketing, keeps transactional
  - `export_preferences_csv` - generates CSV with all preferences and app settings
- ✅ SiteSettings integration:
  - Has communication preference fields
  - Correct GDPR-compliant defaults (double opt-in, opt-out)
  - Fields are editable
- ✅ Performance optimization:
  - Queryset uses `select_related('user')`
- ✅ Edge cases (corrupted JSON, missing app_preference keys)

## Test Factories

Added to `tests/factories.py`:

```python
class CommunicationPreferenceFactory(factory.django.DjangoModelFactory):
    class Params:
        verified = factory.Trait(...)  # Email verified
        marketing_opted_in = factory.Trait(...)  # Email marketing + verified
        sms_opted_in = factory.Trait(...)  # SMS enabled + verified

class BlogSubscriberFactory(factory.django.DjangoModelFactory):
    class Params:
        weekly = factory.Trait(...)  # Weekly digest
        monthly = factory.Trait(...)  # Monthly digest
        unverified = factory.Trait(...)  # Pending verification
```

## Running Tests

```bash
# Run all communication preference tests
pytest tests/integration/test_communication_preferences*.py tests/integration/test_*_preference_integration.py -v

# Run specific test file
pytest tests/integration/test_preference_service.py -v
pytest tests/integration/test_referrals_preference_integration.py -v

# Run specific test
pytest tests/integration/test_communication_preferences_model.py::test_should_send_email_transactional_always_true -v

# Run with coverage
pytest tests/integration/test_communication_preferences*.py tests/integration/test_*_preference_integration.py --cov=accounts --cov=email_system --cov=sms_system --cov=referrals --cov-report=html
```

## Pytest Markers

All tests use these markers:
- `@pytest.mark.django_db` - Enables database access
- `@pytest.mark.integration` - Marks as integration test
- `@pytest.mark.communication_preferences` (or specific: `preference_service`, `email_preferences`, `referrals_preferences`, etc.)

Filter by marker:
```bash
pytest -m preference_service
pytest -m email_preferences
pytest -m referrals_preferences
pytest -m blog_preferences
```

## Test Database Fixtures

All tests use the following shared fixtures from `tests/conftest.py`:
- `site_settings` - SiteSettings instance (single-tenant)
- `django_site` - Django Site with ID=1
- `admin_user` - Staff superuser
- `customer_user` - Regular customer

## Regulatory Compliance Coverage

These tests verify:
- ✅ **GDPR Article 7**: Proof of consent (timestamps, source, IP, user agent)
- ✅ **GDPR Right to Withdraw**: One-click unsubscribe, preference center
- ✅ **GDPR Separate Consent**: Transactional vs marketing split
- ✅ **TCPA Compliance**: All SMS requires explicit opt-in
- ✅ **CAN-SPAM**: Unsubscribe link in marketing emails
- ✅ **Audit Trail**: EmailOutbox/SMSOutbox track all skipped messages

## Future Test Additions

When implementing remaining features, add tests for:
- [ ] Admin interface (Week 6)
- [ ] PreferenceChangeLog audit model
- [ ] Email verification flow (send verification email, verify token)
- [ ] SMS verification flow (send code, verify code)
- [ ] BlogSubscriber migration script
- [ ] Performance tests (cache efficiency, bulk email sends)
- [ ] GDPR export functionality
