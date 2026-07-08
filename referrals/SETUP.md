# Referral Program Setup

This document explains how to configure the referral program middleware in your Django settings.

## Middleware Configuration

The referral program requires two middleware components to be added to your `settings.py`:

### 1. ReferralTrackingMiddleware

This middleware automatically tracks referral link clicks and sets tracking cookies.

**What it does:**
- Detects `ref` query parameter in URLs (e.g., `https://yoursite.com/?ref=abc123`)
- Tracks the click event in the database
- Sets a referral tracking cookie on the visitor's browser
- Non-intrusive: Does not interfere with normal request flow

### 2. RequestContextMiddleware

This middleware provides request context to Django signal handlers.

**What it does:**
- Stores the HTTP request in thread-local storage
- Allows signal handlers to access request data (cookies, IP address, etc.)
- Automatically cleans up after request completion
- Required for automatic referral attribution

## Installation Steps

Add the following middleware to your `MIDDLEWARE` setting in `core/settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # ... your other middleware ...

    # Referral tracking middleware (add near the end)
    'referrals.middleware.RequestContextMiddleware',  # Must be AFTER authentication
    'referrals.middleware.ReferralTrackingMiddleware',
]
```

### Important Notes:

1. **RequestContextMiddleware** must be placed **AFTER** `AuthenticationMiddleware`
   - This ensures user authentication is complete before referral tracking

2. **ReferralTrackingMiddleware** should be placed **AFTER** `RequestContextMiddleware`
   - This ensures request context is available for tracking

3. Both middleware should be near the **end** of the middleware list
   - This allows all Django core middleware to run first
   - Prevents conflicts with security, session, and authentication middleware

## How It Works

### Referral Link Click Flow

1. User clicks referral link: `https://yoursite.com/?ref=abc123`
2. `ReferralTrackingMiddleware` intercepts the request
3. Validates the referral token against the database
4. Logs the click event with tracking data (IP, user agent, etc.)
5. Sets `ref_token` cookie on the response (default 30-day expiration)
6. User continues browsing normally

### User Signup Flow

1. New user creates an account
2. `RequestContextMiddleware` provides request context to signal handler
3. Signal handler checks for `ref_token` cookie
4. If found, logs signup event and links to referrer

### Order Completion Flow

1. User completes their first order
2. Order status changes to 'delivered'
3. Signal handler checks for `ref_token` cookie and creates attribution
4. Runs validation and fraud checks
5. If approved, creates and issues rewards to both referrer and referee
6. Sends email notifications

## Testing

### Test Referral Link Click

```bash
# Visit your site with a referral parameter
curl -I "http://localhost:8000/?ref=YOUR_REFERRAL_TOKEN"

# Check that cookie is set in response headers
# Look for: Set-Cookie: ref_token=YOUR_REFERRAL_TOKEN
```

### Test in Browser

1. Get a referral link from dashboard: `/admin/referrals/dashboard/`
2. Open in private/incognito window
3. Check browser dev tools → Application → Cookies
4. Verify `ref_token` cookie is present

### Check Logs

```python
# In Django shell
from referrals.models import ReferralEvent

# Check recent click events
ReferralEvent.objects.filter(event_type='click').order_by('-created_at')[:10]

# Check signup events
ReferralEvent.objects.filter(event_type='signup').order_by('-created_at')[:10]
```

## Troubleshooting

### Cookies Not Being Set

**Problem:** Referral cookie is not set after clicking referral link

**Solutions:**
1. Check that middleware is installed in `settings.MIDDLEWARE`
2. Verify referral token is valid in database
3. Check that referral program is active (status='active')
4. Review logs for errors: `grep "referral" logs/django.log`

### Signals Not Triggering

**Problem:** Attributions not created when orders complete

**Solutions:**
1. Verify `RequestContextMiddleware` is installed and AFTER `AuthenticationMiddleware`
2. Check that `referrals.signals` is imported in `referrals/apps.py`
3. Verify signal handler is registered: `python manage.py shell` → `from referrals import signals`
4. Check for errors in signal handlers: review application logs

### Attribution Not Created

**Problem:** Order completed but no attribution created

**Possible causes:**
1. This is not the user's first order (only first order creates attribution)
2. No referral cookie present (expired or user cleared cookies)
3. Self-referral detected (user clicked their own referral link)
4. Order status is not 'delivered' (attributions created on delivery)
5. Referral program is inactive

**Debug:**
```python
# In Django shell
from django.contrib.auth import get_user_model
from referrals.models import ReferralAttribution

User = get_user_model()
user = User.objects.get(email='customer@example.com')

# Check if attribution exists
ReferralAttribution.objects.filter(referee_customer=user)

# Check order count (should be first order)
user.orders.count()
```

## Cookie Settings

### Customize Cookie TTL

The default cookie expiration is 30 days, but this can be customized in the ReferralProgram settings:

```python
# In Django admin or shell
from referrals.models import ReferralProgram

program = ReferralProgram.get_program()
program.settings['cookie_ttl_days'] = 60  # 60 days
program.save()
```

### Production Security

In production with HTTPS, the cookie `secure` flag should be enabled. Update the middleware:

```python
# referrals/services/tracking.py - set_ref_cookie() function
response.set_cookie(
    key='ref_token',
    value=token,
    max_age=max_age,
    expires=expires,
    httponly=True,
    samesite='Lax',
    secure=True,  # Enable in production with HTTPS
)
```

## Next Steps

After configuring the middleware:

1. ✅ Create a referral program in Django admin
2. ✅ Configure reward settings (double-sided, amounts, etc.)
3. ✅ Set up email templates (already created in migration)
4. ✅ Test the full flow: click → signup → order → attribution → reward
5. ✅ Monitor dashboard for referral activity

## Support

For issues or questions:
- Check application logs: `tail -f logs/django.log`
- Review signal handler logs (search for "referral")
- Test with DEBUG=True to see detailed error messages
- Check middleware is in correct order in settings
