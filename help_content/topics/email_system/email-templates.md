---
slug: email-templates
title_i18n_key: Email Templates
category: store-config
component: email_system
keywords:
  - email templates
  - order confirmation email
  - shipping notification email
  - transactional email
  - email customization
  - email subject line
  - email variables
  - template preview
  - clone template
  - activate template
  - email branding
  - HTML email
  - password reset email
  - customer email
url_patterns:
  - /admin/email_system/emailtemplate/
related:
  - email-outbox
  - sms-templates
published: true
---

Email templates control the design and content of every automated email your store sends to customers and to you — order confirmations, shipping updates, password resets, refund notices, and many more. Editing a template changes every future email of that type; previous emails already in the outbox are not affected.

Navigate to **Email System > Email Templates** to view and manage your templates.

![Email templates list](/static/core/admin/img/help/email-templates/templates-list.webp)

## Template types

Your store includes templates for a wide range of events. They are grouped by category:

### Customer-facing order emails
| Template | Sent when |
|----------|-----------|
| Order Confirmation | A customer completes a purchase |
| Payment Confirmation | A payment is successfully processed |
| Order Shipped | An order is marked as shipped |
| Shipping Confirmation | A shipment tracking number is added |
| Delivery Confirmation | An order is marked as delivered |
| Order Cancelled | An order is cancelled |
| Order Delay Notification | A delay is recorded on an order |
| Refund Notification | A refund is issued |

### Account emails
| Template | Sent when |
|----------|-----------|
| Account Welcome | A customer creates an account |
| Account Invitation | You invite a customer to create an account |
| Email Verification | A customer verifies their email address |
| Password Reset | A customer requests a password reset |

### Returns
| Template | Sent when |
|----------|-----------|
| Returns: Request Received | A customer submits a return request |
| Returns: Approved | A return request is approved |
| Returns: Rejected | A return request is declined |
| Returns: Package Received | The returned item arrives at your location |
| Returns: Refund Processed | The refund for a return is issued |

### Admin notifications (sent to you)
| Template | Sent when |
|----------|-----------|
| Admin: New Order | A new order is placed |
| Admin: Payment Failed | A payment attempt fails |
| Admin: Daily Sales Report | The daily sales summary is generated |
| Admin: Low Stock Alert | A product drops below its stock threshold |
| Admin: Weekly Digest | The weekly store summary is generated |

Additional templates cover shipping tracking milestones, affiliate programme activity, booking confirmations (if the bookings feature is enabled), and loyalty programme events.

## Editing a template

1. Navigate to **Email System > Email Templates**
2. Find the template you want to edit. You can filter by **Template Type**, **Language**, or **Status** using the filters on the right
3. Click the template to open it
4. Edit the **Subject** line (the email subject shown in the customer's inbox)
5. Edit the **HTML Content** for the full-design version of the email
6. Optionally edit the **Text Content** — a plain-text fallback for email clients that do not support HTML
7. Click **Save**

> **HTML emails:** The HTML content field accepts standard HTML including inline CSS. Spwig renders this into a properly formatted email. If you use MJML markup, it is compiled automatically on save.

## Previewing a template

Before saving, you can preview how the template will look in an email client:

1. Open the template you want to preview
2. Click the **Preview** button (visible in the templates list or on the template detail page)
3. A preview opens in a new browser tab showing the rendered email

This lets you check layout, formatting, and placeholder variable appearance before the template goes live.

## Template variables

Variables are placeholders in your template that Spwig replaces with real data when sending the email. They are written as `{{ variable_name }}`.

Common variables available in most templates:

| Variable | Replaced with |
|----------|---------------|
| `{{ customer_name }}` | The customer's full name |
| `{{ order_number }}` | The order reference number |
| `{{ order_total }}` | The order total amount |
| `{{ store_name }}` | Your store's name |
| `{{ store_url }}` | Your store's web address |
| `{{ tracking_number }}` | The shipment tracking number |
| `{{ tracking_url }}` | A clickable link to track the shipment |

The exact variables available depend on the template type. Variables that are relevant for an order-related template (like `{{ order_number }}`) are not available in an account template (like Password Reset). If you include a variable that does not apply, it will appear blank or unreplaced.

## Language support

Each template type can have a version for each language your store supports. The **Language** field on each template controls which language version is active.

Spwig automatically selects the correct language version based on the customer's language preference when sending. If no template exists for a customer's language, Spwig falls back to the English version.

To add a template for a new language:
1. Open an existing template
2. Click **Clone Template** from the **Actions** menu
3. Set the **Language Code** on the clone to the new language
4. Translate the content
5. Activate the cloned template

## Cloning, activating, and deactivating templates

### Cloning a template

Cloning creates an exact copy of a template — useful for creating language variants or testing different versions without affecting the live template.

1. Select one or more templates in the list
2. Choose **Clone selected templates** from the **Actions** dropdown
3. The clone is created as inactive — edit it and activate it when ready

### Activating and deactivating templates

A template must be **Active** to be used for sending. Only one active template per type and language combination is used at a time.

To activate or deactivate in bulk:
1. Select the templates
2. Choose **Activate selected templates** or **Deactivate selected templates** from the **Actions** dropdown

Or open an individual template and toggle the **Active** checkbox.

## System templates

Templates marked with a **System** badge are the default templates seeded by Spwig. They cannot be deleted. You can edit them directly or clone them to create a custom version.

## Tips

- Always preview a template after editing to catch formatting issues before customers see them
- Keep subject lines short and specific — `Your order #10045 has shipped` performs better than generic subjects like `Update from our store`
- Edit the plain-text content too — some email clients only show the plain-text version, and some customers prefer it
- Clone the English version of a template as a starting point before creating a translated version
- If you want to test a change without affecting live emails, clone the template, edit the clone, and leave both active briefly while you verify the preview — then deactivate the original
- Admin notification templates (like **Admin: New Order**) are sent to your store's admin email address — make sure that email address is correct in your store settings
