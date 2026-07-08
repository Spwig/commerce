# Email Templates for Translation

This directory contains all email templates extracted from the Spwig platform's Django migrations. Each template is stored as an individual markdown file for easy translation and management.

## Extraction Summary

**Total Templates:** 52
**Migration Files Processed:** 10
**Extraction Date:** 2026-02-15

## Template Categories

### Core E-commerce (5 templates)
- `order_confirmation.md` - Order confirmation email
- `payment_confirmation.md` - Payment received confirmation
- `shipping_confirmation.md` - Shipping notification
- `delivery_confirmation.md` - Delivery confirmation
- `refund_notification.md` - Refund processed notification

### Authentication (2 templates)
- `password_reset.md` - Password reset request
- `email_verification.md` - Email address verification

### Enhanced E-commerce (3 templates)
- `account_welcome.md` - New account welcome email
- `order_delay.md` - Order delay notification
- `review_request.md` - Product review request

### Admin Notifications (2 templates)
- `admin_new_order.md` - New order notification for admin
- `admin_payment_failed.md` - Payment failure notification for admin

### Loyalty Program (5 templates)
- `loyalty_welcome.md` - Welcome to loyalty program
- `loyalty_points_earned.md` - Points earned notification
- `loyalty_tier_upgrade.md` - Tier upgrade notification
- `loyalty_points_expiring.md` - Points expiration warning
- `loyalty_reward_available.md` - New reward unlocked

### Referral Program (5 templates)
- `referral_reward_issued_referrer.md` - Reward issued to referrer
- `referral_reward_issued_referee.md` - Welcome reward for referee
- `referral_successful.md` - Successful referral notification
- `referral_reward_expiring.md` - Reward expiration warning
- `referral_invitation.md` - Referral invitation email

### Digital Products (4 templates)
- `digital_product_delivery.md` - Digital product download ready
- `digital_product_license_key.md` - Software license key delivery
- `digital_product_download_expired.md` - Download link expired
- `digital_product_license_expired.md` - License expiration warning

### Gift Cards (1 template)
- `gift_card_delivery.md` - Gift card delivery email

### Subscriptions (10 templates)
- `subscription_created.md` - Subscription activated
- `subscription_trial_ending.md` - Trial ending soon
- `subscription_renewal_reminder.md` - Renewal reminder
- `subscription_payment_success.md` - Payment successful
- `subscription_payment_failed.md` - Payment failed
- `subscription_paused.md` - Subscription paused
- `subscription_resumed.md` - Subscription resumed
- `subscription_canceled.md` - Subscription canceled
- `subscription_expired.md` - Subscription expired
- `subscription_payment_method_expiring.md` - Payment method expiring

### Inventory (1 template)
- `back_in_stock.md` - Back in stock notification

### POS (1 template)
- `pos_receipt.md` - Point of sale receipt email

### Developer Portal (13 templates)
- `dev_registration_ack.md` - Registration received
- `dev_account_approved.md` - Account approved
- `dev_account_rejected.md` - Account rejected
- `dev_account_suspended.md` - Account suspended
- `dev_submission_received.md` - Component submission received
- `dev_submission_approved.md` - Component approved
- `dev_submission_rejected.md` - Component rejected
- `dev_revision_requested.md` - Revision requested
- `dev_component_published.md` - Component published
- `dev_new_review.md` - New review notification
- `dev_review_digest.md` - Review digest summary
- `dev_license_approved.md` - License approved
- `dev_license_rejected.md` - License rejected

## File Format

Each markdown file follows this structure:

```markdown
---
template_type: template_name
category: Category Name
---

# Email Template: template_name

## Subject
Subject line with {{ variables }}

## HTML Content
MJML/HTML template with Django template tags

## Text Content
Plain text version with {{ variables }}
```

## Django Template Variables

All templates preserve Django template variables and tags:
- Variables: `{{ variable_name }}`
- Template tags: `{% tag_name %}`
- Filters: `{{ variable|filter }}`
- Translations: `{% trans "text" %}` and `{% load i18n %}`

## MJML Structure

HTML templates use MJML (Mailjet Markup Language) for responsive email design:
- All MJML tags are preserved exactly as-is
- Common components: `<mj-section>`, `<mj-column>`, `<mj-text>`, `<mj-button>`
- Responsive and mobile-friendly by default

## Source Migrations

Templates were extracted from these Django migration files:

1. `email_system/migrations/0002_default_email_templates.py` - Core e-commerce templates
2. `email_system/migrations/0010_enhanced_email_templates.py` - Enhanced templates with MJML
3. `email_system/migrations/0018_add_loyalty_campaign_templates.py` - Loyalty program
4. `email_system/migrations/0019_add_referral_email_templates.py` - Referral program
5. `email_system/migrations/0023_add_digital_product_email_templates.py` - Digital products
6. `email_system/migrations/0026_add_gift_card_email_template.py` - Gift cards
7. `email_system/migrations/0027_add_subscription_email_templates.py` - Subscriptions
8. `email_system/migrations/0031_add_back_in_stock_email_template.py` - Inventory notifications
9. `email_system/migrations/0041_create_pos_receipt_template.py` - POS system
10. `email_system/migrations/0042_developer_portal_email_templates.py` - Developer portal

## Translation Notes

When translating these templates:

1. **Preserve all Django template syntax** - Do not translate `{{ }}` or `{% %}` tags
2. **Preserve MJML tags** - Keep all `<mj-*>` tags intact
3. **Translate user-facing text only** - Subject lines and content text
4. **Maintain variable placeholders** - Keep `{{ variable }}` in their original position
5. **Test rendering** - Ensure MJML compiles correctly after translation
6. **Keep HTML attributes** - Colors, sizes, and styles should remain unchanged

## Validation

All templates have been validated for:
- ✓ English (en) language version only
- ✓ Complete subject, HTML, and text content
- ✓ Preserved Django template variables
- ✓ Preserved MJML structure
- ✓ Proper category assignment

## Usage

These templates can be used for:
- Translation into multiple languages
- Email template customization
- Documentation and reference
- Quality assurance and testing
- Template comparison across versions

---

**Generated:** 2026-02-15
**Source:** Spwig E-commerce Platform
**Format Version:** 1.0
