# Email Templates Index

Quick reference guide to all extracted email templates organized by category.

---

## Core E-commerce (5)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Order Confirmation | `order_confirmation.md` | Order Confirmation #{{ order_number }} - Thank You! |
| Payment Confirmation | `payment_confirmation.md` | Payment Confirmed - Order #{{ order_number }} |
| Shipping Confirmation | `shipping_confirmation.md` | Your Order Has Shipped - Order #{{ order_number }} |
| Delivery Confirmation | `delivery_confirmation.md` | Order Delivered - Order #{{ order_number }} |
| Refund Notification | `refund_notification.md` | Refund Processed - Order #{{ order_number }} |

---

## Authentication (2)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Password Reset | `password_reset.md` | Password Reset Request |
| Email Verification | `email_verification.md` | Verify Your Email Address |

---

## Enhanced E-commerce (3)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Account Welcome | `account_welcome.md` | Welcome to {{ shop_name }}! |
| Order Delay | `order_delay.md` | Update: Delay for Order #{{ order_number }} |
| Review Request | `review_request.md` | How Was Your Purchase? Leave a Review |

---

## Admin Notifications (2)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| New Order | `admin_new_order.md` | New Order Received - Order #{{ order_number }} |
| Payment Failed | `admin_payment_failed.md` | Payment Failed - Order #{{ order_number }} |

---

## Loyalty Program (5)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Welcome | `loyalty_welcome.md` | Welcome to {{ shop_name }} Rewards! |
| Points Earned | `loyalty_points_earned.md` | You earned {{ points }} points! |
| Tier Upgrade | `loyalty_tier_upgrade.md` | Congratulations! You've been upgraded to {{ new_tier }} |
| Points Expiring | `loyalty_points_expiring.md` | Reminder: {{ expiring_points }} points expiring soon |
| Reward Available | `loyalty_reward_available.md` | New reward unlocked: {{ reward_name }}! |

---

## Referral Program (5)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Reward Issued (Referrer) | `referral_reward_issued_referrer.md` | You earned a {{ reward_amount }} reward! |
| Reward Issued (Referee) | `referral_reward_issued_referee.md` | Welcome! Here's your {{ reward_amount }} reward |
| Successful Referral | `referral_successful.md` | 🎉 Your friend {{ referee_name }} just signed up! |
| Reward Expiring | `referral_reward_expiring.md` | Reminder: Your {{ reward_amount }} reward expires soon |
| Invitation | `referral_invitation.md` | {{ referrer_name }} sent you a gift! |

---

## Digital Products (4)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Delivery | `digital_product_delivery.md` | Your Digital Product is Ready - Order #{{ order_number }} |
| License Key | `digital_product_license_key.md` | Your Software License Key - Order #{{ order_number }} |
| Download Expired | `digital_product_download_expired.md` | Download Link Expired - Order #{{ order_number }} |
| License Expired | `digital_product_license_expired.md` | License Key Expiring Soon - {{ product_name }} |

---

## Gift Cards (1)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Delivery | `gift_card_delivery.md` | 🎁 Gift Card from {{ sender_name }} - {{ shop_name }} |

---

## Subscriptions (10)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Created | `subscription_created.md` | ✅ Your {{ plan_name }} Subscription is Active - {{ shop_name }} |
| Trial Ending | `subscription_trial_ending.md` | ⏰ Your {{ plan_name }} Trial Ends in {{ days_remaining }} Days |
| Renewal Reminder | `subscription_renewal_reminder.md` | 🔔 Your {{ plan_name }} Renews in {{ days_until_renewal }} Days |
| Payment Success | `subscription_payment_success.md` | ✅ Payment Received for {{ plan_name }} - {{ shop_name }} |
| Payment Failed | `subscription_payment_failed.md` | ⚠️ Payment Failed for {{ plan_name }} - Action Required |
| Paused | `subscription_paused.md` | ⏸️ Your {{ plan_name }} Subscription is Paused |
| Resumed | `subscription_resumed.md` | ▶️ Your {{ plan_name }} Subscription is Active Again |
| Canceled | `subscription_canceled.md` | ❌ Your {{ plan_name }} Subscription is Canceled |
| Expired | `subscription_expired.md` | ⏱️ Your {{ plan_name }} Subscription Has Expired |
| Payment Method Expiring | `subscription_payment_method_expiring.md` | 💳 Update Required: Payment Method Expiring Soon |

---

## Inventory (1)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Back In Stock | `back_in_stock.md` | {{ product_name }} is back in stock! - {{ shop_name }} |

---

## POS (1)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Receipt | `pos_receipt.md` | Your receipt from {{ store_name }} - Order #{{ order_number }} |

---

## Developer Portal (13)

| Template | File | Subject Pattern |
|----------|------|-----------------|
| Registration Ack | `dev_registration_ack.md` | We received your developer application, {{ developer_name }} |
| Account Approved | `dev_account_approved.md` | Welcome to the Spwig Developer Program, {{ developer_name }}! |
| Account Rejected | `dev_account_rejected.md` | Update on your Spwig developer application |
| Account Suspended | `dev_account_suspended.md` | Your Spwig developer account has been suspended |
| Submission Received | `dev_submission_received.md` | Component submission received: {{ component_name }} v{{ version }} |
| Submission Approved | `dev_submission_approved.md` | Component approved: {{ component_name }} v{{ version }} |
| Submission Rejected | `dev_submission_rejected.md` | Component review update: {{ component_name }} v{{ version }} |
| Revision Requested | `dev_revision_requested.md` | Revision requested: {{ component_name }} v{{ version }} |
| Component Published | `dev_component_published.md` | {{ component_name }} v{{ version }} is now live on the Spwig Marketplace! |
| New Review | `dev_new_review.md` | New {{ rating }}-star review on {{ component_name }} |
| Review Digest | `dev_review_digest.md` | {{ review_count }} new review{{ review_count\|pluralize }} on your components |
| License Approved | `dev_license_approved.md` | Your Spwig developer license is ready! |
| License Rejected | `dev_license_rejected.md` | Update on your Spwig developer license request |

---

## Quick Stats

- **Total Templates**: 52
- **Most Templates**: Developer Portal (13)
- **Template Types**: Transactional, Marketing, Admin
- **Languages**: English only (ready for translation)
- **Format**: MJML HTML + Plain Text

---

## Navigation Tips

1. Use Ctrl+F / Cmd+F to search for specific template names
2. Each template file follows the same structure for consistency
3. Category folders can be created if needed for better organization
4. See `README.md` for detailed documentation

---

**Last Updated**: 2026-02-15
