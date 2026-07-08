---
title: Configuração de E-mail
---

A configuração de e-mail controla como sua loja envia e-mails transacionais — confirmações de pedido, notificações de envio, redefinições de senha e muito mais. O Spwig inclui um servidor SMTP embutido e oferece suporte a provedores de e-mail externos para maior entregabilidade.

![Email accounts](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Available Providers

| Provider | Description |
|----------|-------------|
| **Built-in SMTP** | Free, self-hosted email server included with Spwig. Automatic DKIM signing. |
| **Gmail API** | Send via your Gmail or Google Workspace account using OAuth authentication. |
| **Generic SMTP** | Connect any SMTP server (SendGrid, Mailgun, Amazon SES, or your own mail server). |

## Setting Up Email

Navigate to **Settings > Email Accounts** and click **Add Email Account** to launch the setup wizard.

### Step 1: Select Provider

Choose your email provider. The built-in SMTP server is the simplest option to get started — it requires no external accounts.

### Step 2: Configure Credentials

Enter the credentials for your chosen provider:

- **Built-in SMTP** — No credentials needed. The server runs on your Spwig installation.
- **Gmail API** — Authenticate via Google OAuth. You'll be redirected to sign in with your Google account.
- **Generic SMTP** — Enter the SMTP server address, port, username, and password.

### Step 3: Sender Configuration

Set the sender identity for outgoing emails:

- **From Email** — The email address that appears in the "From" field (e.g., orders@yourstore.com)
- **From Name** — The display name next to the email address (e.g., "Your Store Name")
- **Reply-To Email** — Where customer replies are directed (can differ from the From address)

### Step 4: DNS Validation

Verify your domain's email authentication records. The wizard checks three DNS records:

| Record | Purpose |
|--------|---------|
| **SPF** | Authorizes your server to send email on behalf of your domain |
| **DKIM** | Digitally signs emails to prove they haven't been tampered with |
| **DMARC** | Tells receiving servers what to do with emails that fail SPF/DKIM checks |

For each record, the wizard shows:
- **Current status** — Whether the record is correctly configured
- **Required value** — The exact DNS record to add at your domain registrar
- **Propagation status** — Whether recent changes have taken effect (DNS changes can take up to 48 hours)

The built-in SMTP server automatically generates DKIM keys for your domain.

### Step 5: Send Test Email

Send a test email to verify everything works:
1. Enter a recipient email address
2. Click **Send Test**
3. Check your inbox for the test message
4. Verify the email arrives without spam warnings

### Step 6: Save and Activate

Save the configuration and set the account as active. Mark it as **Default** if it should be the primary email account.

## Email Templates

Spwig includes 30+ email templates for every transactional event. Navigate to **Settings > Email Templates** to manage them.

### Template Types

Templates cover all store events including:
- **Order Lifecycle** — Confirmation, processing, shipped, delivered, cancelled
- **Payment** — Receipt, refund confirmation, failed payment
- **Customer Account** — Welcome, password reset, email verification
- **Gift Cards** — Delivery, balance notification
- **Shipping** — Tracking updates, delivery confirmation
- **Digital Products** — Download links, license keys
- **Marketing** — Abandoned cart recovery, review requests

### Customizing Templates

1. Navigate to the template list
2. Click a template to edit
3. Modify the subject line, header, body content, and footer
4. Use template variables (e.g., `{{ order.number }}`, `{{ customer.name }}`) for dynamic content
5. Preview the email before saving

### Multi-Language Support

Email templates support multiple languages:
- Each template can have translations for all your store's active languages
- The system sends emails in the customer's preferred language
- **Language fallback chain** — If a translation isn't available, the system falls back to the store's default language
- Use the **AI Translation** feature to automatically translate templates into other languages

### Cloning Templates

To create a customized version of a system template:
1. Open the template you want to modify
2. Click **Clone Template**
3. Edit the cloned version
4. The clone takes priority over the original system template

## Email Queue

Monitor outgoing emails at **Settings > Email Queue**:

- **Queued** — Emails waiting to be sent
- **Sending** — Currently being transmitted
- **Sent** — Successfully delivered
- **Failed** — Could not be delivered (with error details)
- **Bounced** — Rejected by the recipient's mail server

Click any email to view its full details including recipient, subject, send time, and delivery status.

## Delivery Tracking

Track email engagement:
- **Opens** — How many recipients opened the email
- **Clicks** — Link clicks within the email
- **Bounces** — Hard and soft bounce tracking
- **Complaints** — Spam reports from recipients

## Multiple Accounts

You can configure multiple email accounts:
- **Default Account** — Used for all outgoing emails unless overridden
- **Fallback** — If the default account fails, emails queue for retry
- Use different accounts for different purposes (e.g., one for transactional emails, another for marketing)

## Tips

- Start with the **Built-in SMTP** server for quick setup, then switch to an external provider if you need higher sending volumes or better deliverability.
- Always configure **SPF, DKIM, and DMARC** records — without them, emails are much more likely to land in spam folders.
- Send a **test email** after any configuration change to verify delivery works.
- Monitor the email queue regularly for **failed** or **bounced** emails — these indicate deliverability issues.
- Use a **professional sender address** (e.g., orders@yourstore.com) rather than a free email address for better trust and deliverability.
- Keep your templates concise — transactional emails should deliver information quickly, not be marketing newsletters.

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.