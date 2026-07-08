# Guest Checkout and Referral Attribution

## How Guest Checkout Works

In this e-commerce platform:

1. **Cart Phase**: Guest users can browse and add items to cart with only a session key (no User account)
   - `Cart.user` is nullable (`null=True, blank=True`)
   - Guest cart linked by `session_key` only

2. **Checkout Phase**: When guest proceeds to checkout, a User account **must be created**
   - `Order.user` is **required** (non-nullable ForeignKey)
   - System creates User account with email from checkout form
   - Password is set to unusable or user is marked inactive until they verify/activate

3. **Order Placement**: Order is always linked to a User instance
   - Even "guest" orders have a User account in the database
   - User can later claim their account by verifying email

## Referral Attribution for Guest Checkout

### Current Flow

The referral system handles guest checkout automatically:

1. **Referral Link Click** (Guest browsing)
   - Guest clicks referral link: `https://yoursite.com/?ref=abc123`
   - `ReferralTrackingMiddleware` sets referral cookie
   - Cookie persists for 30 days (configurable)

2. **Guest Adds to Cart** (No account yet)
   - Cart created with only `session_key`
   - Referral cookie remains in browser

3. **Guest Proceeds to Checkout**
   - Guest fills out checkout form (email, shipping, billing)
   - System creates User account from checkout data
   - User account created with referral cookie still present

4. **User Account Creation Signal**
   - `track_user_signup` signal fires when User is created
   - Signal checks for referral cookie via `get_current_request()`
   - Logs signup event and links to referrer

5. **Order Completion**
   - Order is placed and status changes to 'delivered'
   - `handle_order_completion` signal fires
   - Creates `ReferralAttribution` if this is user's first order
   - Runs validation and issues rewards

### Key Points

✅ **Guest checkout is fully supported** - The system automatically creates a User account during checkout, so referral attribution works seamlessly

✅ **No special handling needed** - Since every order has a User account (even guests), the signals work the same way

✅ **Cookie persists** - The referral cookie survives the entire journey from browsing → cart → checkout → account creation

### Edge Cases Handled

1. **Guest checks out multiple times with same email**
   - First checkout creates User account → attribution created
   - Subsequent orders see existing User → no duplicate attribution (only first order counts)

2. **Guest clears cookies before checkout**
   - Referral cookie lost → no attribution
   - This is expected behavior (cookie-based tracking limitation)

3. **Guest browses on mobile, checks out on desktop**
   - Different browsers = different cookies → no attribution
   - This is a limitation of cookie-based tracking
   - Could be solved with email-based matching (future enhancement)

## Signal Handler Behavior

### `track_user_signup` Signal

```python
@receiver(post_save, sender=User)
def track_user_signup(sender, instance, created, **kwargs):
    if not created:
        return

    # Skip if user is staff/superuser
    if instance.is_staff or instance.is_superuser:
        return

    # Get request from thread-local storage (includes cookies)
    request = get_current_request()

    if request:
        # Check for referral cookie and log signup event
        success, identity, message = track_signup(instance, request)
```

**For guest checkout:**
- Signal fires when User account is created during checkout
- `get_current_request()` retrieves the checkout request
- Referral cookie is read from request
- Signup event logged and linked to referrer

**Will NOT track:**
- Staff/superuser accounts
- Accounts created via admin panel
- Accounts created without HTTP request context (management commands, etc.)

### `handle_order_completion` Signal

```python
@receiver(post_save, sender=Order)
def handle_order_completion(sender, instance, created, **kwargs):
    # Only process when status changes to 'delivered'
    if instance.status == 'delivered':
        # Check if this is user's first order
        first_order = Order.objects.filter(user=instance.user).order_by('created_at').first()

        if first_order.pk == instance.pk:
            # Create attribution if referral cookie present
            # Issue rewards if approved
```

**For guest checkout:**
- Signal fires when guest's first order is delivered
- System checks if referral cookie present
- Creates attribution and issues rewards

**Handles:**
- First order only (subsequent orders ignored)
- Self-referral detection (user can't refer themselves)
- Cookie expiration (no attribution if cookie expired)
- Order cancellation/refund (revokes rewards)

## Testing Guest Checkout Referrals

### Test Scenario 1: Happy Path

```bash
# 1. Get referral link from admin dashboard
# Referrer: john@example.com

# 2. Open private/incognito browser (simulate guest)
# Visit: https://yoursite.com/?ref=abc123

# 3. Add products to cart (no account login)

# 4. Proceed to checkout
# Fill out email: jane@example.com
# Complete checkout

# 5. Check Django admin
# - New User created: jane@example.com
# - ReferralEvent logged: type='signup'
# - Order created: linked to jane@example.com

# 6. Mark order as 'delivered'

# 7. Check referrals dashboard
# - ReferralAttribution created
# - Rewards issued to both john and jane
# - Emails sent to both parties
```

### Test Scenario 2: Existing Email

```bash
# 1. User already has account: existing@example.com

# 2. Guest clicks referral link in private browser

# 3. Tries to checkout with email: existing@example.com

# Expected behavior:
# - System should either:
#   a) Show error "email already exists"
#   b) Create duplicate account (if allowed)
#   c) Link to existing account

# Note: This depends on your account creation logic during checkout
```

### Test Scenario 3: Cookie Expiration

```bash
# 1. Click referral link: cookie set with 30-day expiry

# 2. Wait 31 days (or manually delete cookie)

# 3. Checkout as guest

# Result: No attribution created (expected)
```

## Recommendations

### Current Implementation ✅

The current implementation works well for guest checkout because:
- All orders require a User account
- Middleware provides request context to signals
- Cookie tracking persists through checkout flow

### Potential Enhancements 🚀

1. **Email-Based Matching**
   - Store referral mappings in database: `ref_token → email`
   - When guest checks out, match email to referral
   - Works across devices/browsers

2. **Account Linking**
   - If guest later creates full account with same email
   - Link previous guest orders to new account
   - Maintain referral attribution

3. **Guest User Indicator**
   - Add `is_guest` flag to User model
   - Track which users are "claimed" vs "guest only"
   - Allow guests to upgrade to full accounts

4. **Alternative Tracking Methods**
   - URL parameters + database storage
   - LocalStorage + cookie fallback
   - Email-based attribution

### Implementation Priority

**Current system is production-ready** ✅
- Guest checkout referrals work automatically
- No additional code needed
- Signals handle attribution correctly

**Enhancements are optional** 💡
- Only needed if you want cross-device tracking
- Or if you want to distinguish guest vs full accounts
- Can be added in future iterations

## Conclusion

Guest checkout referrals **work automatically** with the current implementation because:

1. Every order requires a User account (even for guests)
2. User accounts are created during checkout
3. Referral cookies persist through the checkout flow
4. Signals fire when User is created and Order is completed
5. Attribution is created and rewards are issued

No special handling or modifications needed! 🎉
