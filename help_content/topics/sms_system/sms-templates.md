---
slug: sms-templates
title_i18n_key: SMS Templates
category: store-config
component: sms_system
keywords:
  - SMS templates
  - SMS message template
  - order confirmation SMS
  - shipping SMS
  - delivery notification SMS
  - SMS variables
  - message placeholders
  - customize SMS
  - SMS character limit
  - SMS notification text
  - password reset SMS
  - verification code SMS
url_patterns:
  - /admin/sms_system/smstemplate/
related:
  - sms-setup
  - sms-outbox
published: true
---

SMS templates control the text of every notification your store sends to customers via text message. Each template corresponds to a specific event — such as an order confirmation or a shipping update — and uses placeholder variables that Spwig replaces with the actual order details when the message is sent.

Navigate to **SMS System > SMS Templates** to view and edit your templates.

![SMS templates list](/static/core/admin/img/help/sms-templates/templates-list.webp)

## Available template types

Spwig includes the following built-in template types:

| Template Type | When it is sent |
|---------------|-----------------|
| Order Confirmation | When a customer places an order |
| Shipping Update | When an order's tracking status changes |
| Delivery Notification | When an order is marked as delivered |
| Password Reset | When a customer requests a password reset |
| Verification Code | When a one-time code is needed for account verification |
| POS Receipt | When a sale is processed at a point-of-sale terminal |
| Marketing | For promotional campaigns (requires separate opt-in) |
| Custom | For any other notification you create |

## Editing a template

1. Navigate to **SMS System > SMS Templates**
2. Click on the template you want to edit
3. Update the **Message** field with your desired text
4. Use `{variable}` placeholders to include order-specific information (see variables below)
5. Check **Active** to enable the template — inactive templates are not sent
6. Click **Save**

![Editing an SMS template](/static/core/admin/img/help/sms-templates/template-edit.webp)

## Using variables

Variables are placeholders written in curly braces — for example, `{name}` or `{order_number}`. When Spwig sends the message, it replaces each placeholder with the real value for that customer or order.

### Common variables

| Variable | Replaced with |
|----------|---------------|
| `{name}` | The customer's first name |
| `{order_number}` | The order reference number |
| `{total}` | The order total amount |
| `{tracking_number}` | The shipment tracking number |
| `{store_name}` | Your store's name |
| `{code}` | A verification or reset code |

**Example message:**

```
Hi {name}, your order #{order_number} has been confirmed. Total: {total}. We'll update you when it ships. - {store_name}
```

When sent, this becomes:

```
Hi Sarah, your order #10045 has been confirmed. Total: $89.00. We'll update you when it ships. - The Garden Shop
```

> Only include variables that are available for a given template type. For example, `{tracking_number}` is available in a Shipping Update template but not in a Password Reset template. If you use an unavailable variable, it will appear as-is (unreplaced) in the message.

## Character limits and message length

Standard SMS messages are limited to **160 characters** for a single segment. Longer messages are split into multiple segments and sent as one (concatenated SMS), but carriers count each segment separately for billing purposes.

**Tips for staying within the limit:**
- Keep messages concise — one purpose per message
- Abbreviate common phrases where natural (e.g., "Ord" instead of "Order")
- Avoid unnecessary filler words

Spwig does not enforce a hard character limit in the editor, so count your characters (including variable values) before saving.

## Activating and deactivating templates

The **Active** toggle on each template controls whether that notification type is sent. If a template is inactive, Spwig skips sending that notification entirely — the message will appear as **Skipped** in the SMS Outbox with the reason `template_inactive`.

To activate a template:
1. Open the template
2. Check the **Active** checkbox
3. Save

To deactivate (stop sending a notification type without deleting the template):
1. Open the template
2. Uncheck **Active**
3. Save

## Tips

- Write messages in the same voice as your brand — SMS is a direct, personal channel, so a friendly tone works well
- Always include your store name in the message so customers know who is texting them
- Keep order confirmation messages brief: order number, total, and a note about next steps is enough
- Test messages by placing a test order on your own store (using a phone number you control) to see exactly what customers receive
- If a notification is generating confusion or complaints, deactivate the template and revise it rather than deleting it — that way you can re-enable it once updated
- Marketing templates must only be sent to customers who have explicitly opted in to SMS marketing, as required by telecommunications regulations in most countries
