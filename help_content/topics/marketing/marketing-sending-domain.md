---
slug: marketing-sending-domain
title_i18n_key: Marketing Sending Domain
category: marketing-seo
component: email_system
keywords:
  - marketing sending domain
  - dedicated marketing domain
  - subdomain
  - news subdomain
  - separate sending identity
  - sender reputation
  - transactional vs marketing email
  - protect transactional deliverability
  - DKIM
  - SPF
  - DMARC
  - campaign deliverability
  - order confirmation deliverability
url_patterns:
  - /admin/email_system/emailaccount/
  - /admin/email_system/emailaccount/add/
  - /admin/campaigns/dashboard/
related:
  - deliverability
  - email-configuration
  - list-hygiene
  - campaign-reports
published: true
---

# Marketing sending domain

Your store sends two very different kinds of email:

- **Transactional** — order confirmations, shipping updates, password resets. These
  must always reach the inbox.
- **Marketing** — newsletters, promotions, cart-recovery, back-in-stock alerts.

By default both go out under the same sending identity, which means they **share one
sender reputation**. If a marketing campaign draws spam complaints or hits stale
addresses, that reputation drops — and your order confirmations and password resets can
start landing in spam too.

A **marketing sending domain** fixes this. You set up a second sending identity — on its
own subdomain such as `news.yourstore.com` — and mark it for marketing. Spwig then sends
every campaign from that identity and keeps transactional email on your main one. A rough
campaign can no longer drag down the mail your customers *need* to receive.

> This applies to self-hosted stores. On Spwig-hosted plans, sending reputation is
> managed for you.

## How Spwig decides which identity to use

Once a marketing sending account exists, routing is automatic — you don't tag anything:

- **Marketing mail** (campaigns, journeys, newsletters, cart-recovery, back-in-stock) →
  the marketing sending domain.
- **Transactional mail** (orders, shipping, password resets, verification) → your main
  domain.

If you never set up a marketing domain, nothing changes: everything continues to send
from your default account exactly as before.

## Set it up

You can start from either entry point:

- The **"Set up marketing domain"** button on the Campaign Studio dashboard banner, or
- **Email Accounts → "Marketing sending domain"**.

![The Campaign Studio dashboard with the "Protect your transactional email" banner and its Set up marketing domain button](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-nudge.webp)

![The Marketing sending domain button on the Email Accounts list, next to Browse Providers](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-button.webp)

Both open the email setup wizard pre-flagged for a marketing account. Then:

1. **Choose a subdomain.** Use something like `news.yourstore.com` or
   `mail.yourstore.com`. This is the most important step: the marketing identity must be a
   **different (sub)domain** from the one your transactional email uses — that separation
   is exactly what protects your transactional reputation. Sending marketing from your
   main domain gives you no isolation.
2. **Enter the sender address** on that subdomain, e.g. `news@news.yourstore.com`.
3. **Add the DNS records.** The wizard generates SPF, DKIM, and DMARC records for the
   subdomain — including a DKIM key that is unique to this marketing identity. Add them at
   your DNS provider (the wizard has copy buttons and per-provider tabs), then run the
   check until all records pass.
4. **Finish.** The account is created and marked **Marketing only**. From now on your
   campaigns send from it.

You can confirm it worked on the **Email Accounts** list: you'll see a second account with
a **Marketing only** purpose, and the Campaign Studio banner disappears.

## Good to know

- **You can't accidentally break transactional email.** Spwig won't let you set your only
  account to "Marketing only", or disable/delete your last transactional account — there
  is always somewhere for order confirmations and password resets to go.
- **Warm up gradually.** A brand-new sending domain has no reputation yet. Ramp your
  volume up over a couple of weeks rather than blasting your whole list on day one.
- **Keep the subdomain's DNS healthy.** SPF, DKIM, and DMARC on the marketing subdomain
  need to stay valid, just like your main domain. See the
  [Email Deliverability Runbook](deliverability) for the full picture.
- **Consent still applies.** Marketing mail only goes to subscribers who have opted in,
  and every campaign carries an unsubscribe link — separating the domain doesn't change
  any of that.
