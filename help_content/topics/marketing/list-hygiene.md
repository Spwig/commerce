---
slug: list-hygiene
title_i18n_key: List Hygiene and Suppressions
category: marketing-seo
component: email_marketing
keywords:
  - list hygiene
  - suppression list
  - do not mail
  - do-not-mail list
  - email deliverability
  - hard bounce
  - soft bounce
  - spam complaint
  - sender reputation
  - suppressed address
  - release address
  - unsuppress
  - bounce handling
  - blocklist email
  - email bounce management
url_patterns:
  - /admin/campaigns/dashboard/
  - /admin/email_marketing/suppressionentry/
related:
  - email-outbox
  - ab-testing
  - audiences
  - recurring-campaigns
  - campaign-reports
  - deliverability
published: true
---

Every email address that hard-bounces, marks your mail as spam, or repeatedly fails to receive your messages puts the rest of your list at risk — mailbox providers judge your sender reputation by how clean your sending is, and a dirty list means more of *every* campaign lands in spam. Campaign Studio protects you from this automatically with **list hygiene**: it watches for undeliverable and complaining addresses and stops sending marketing email to them, without any setup on your part.

This is separate from unsubscribes. An unsubscribed address has withdrawn consent; a **suppressed** address is one Spwig has learned is unsafe or impossible to keep mailing to, regardless of consent.

## How addresses get suppressed

Spwig adds an address to the **Suppression list** automatically when:

| Trigger | What it means |
|---------|---------------|
| **Hard bounce** | The address doesn't exist, or the domain refused to accept mail for it — permanently undeliverable. |
| **Spam complaint** | A recipient marked your email as spam or junk. |
| **Repeated soft bounces** | The address soft-bounced (mailbox full, server temporarily unavailable) 5 times within a rolling 30-day window. A single soft bounce is treated as a temporary hiccup and ignored — only a pattern of repeated failures triggers suppression. |
| **Manually blocked** | You added the address yourself. |

Once an address is suppressed, Spwig stops sending it any further **campaigns** or **journey** emails immediately — no other action is required from you.

## Where the signal comes from

Spwig can learn about a bounce or complaint from a few different places, shown as the **Source** on each suppressed address:

- **Rejected at send** — your mail server refused the address immediately when Spwig tried to send to it.
- **Provider webhook** — if you've connected an email provider (such as SendGrid, Amazon SES, Mailgun, or Postmark), that provider reports bounces and complaints back to Spwig as they happen.
- **Mail gateway** — if your store sends through the Spwig-hosted mail gateway, Spwig pulls bounce reports from the gateway on your behalf.
- **Added manually** — you entered the address yourself from the admin.

You don't need to configure anything to benefit from this — whichever way you send mail, Spwig is watching for failures and keeping your list clean.

## The Campaign Studio dashboard

Open **Campaign Studio** and look for the **Suppressed addresses** card. It shows the total number of addresses currently suppressed, plus how many are new in the last 30 days. Click the card to open the full Suppressions list.

![The Campaign Studio dashboard's Suppressed addresses stat card, showing a total and a "new in the last 30 days" count](/static/core/admin/img/help/list-hygiene/dashboard-suppressed-card.webp)

A steadily climbing count is normal — every list accumulates some bad addresses over time as people change jobs, close accounts, or abandon inboxes. A sudden spike is worth investigating; see [Email Outbox](email-outbox) to check whether a particular send hit an unusual number of failures.

## The Suppressions list

Click through to **Suppressions** to see every suppressed address, why it was suppressed, and where the signal came from.

![The Suppressions list showing suppressed addresses with their Reason and Source columns](/static/core/admin/img/help/list-hygiene/suppressions-list.webp)

Use the filters on the right to narrow the list by **Reason** or **Source** — for example, to review every manually blocked address, or everything that came in through a provider webhook.

## Adding an address manually

To block an address yourself — a known abuse address, a competitor scraping your newsletter, or anything else you want to keep off your list — click **+ Add suppressed address** and fill in:

- **Email** — the address to block
- **Reason** — choose **Manually blocked** for a self-added entry
- **Source** — choose **Added manually**
- **Detail** — an optional note explaining why (useful for your own records, and for any staff who review the list later)

Save the entry and Spwig stops sending that address any campaign or journey email immediately.

## When would I release an address?

Releasing (un-suppressing) an address should be rare and deliberate. Only do it when you're confident the underlying problem is actually fixed — for example:

- A customer tells you their mailbox was full and it's been cleared out.
- An address was suppressed by a soft-bounce streak that you know was caused by a temporary outage at their mail provider, not a dead mailbox.
- You blocked an address manually and later decide the block was a mistake.

To release an address, open it in the Suppressions list and delete the entry — this lifts the block so the address can receive mail again. Don't release a hard-bounced address just because it's inconvenient to lose a subscriber; the address doesn't exist, and sending to it again will just bounce and cost you reputation a second time. Likewise, releasing a spam-complaint address rarely helps — that recipient told their mailbox provider they don't want your mail, and sending to them again risks another complaint.

## What isn't affected

Suppression only applies to **marketing campaigns and journeys** sent through Campaign Studio. It does not affect **transactional email** — order confirmations, shipping updates, password resets, and other emails your store sends as part of an order or account action always go through, even to a suppressed address. Suppression exists to protect your marketing sender reputation; it isn't a general email blocklist for your store.

## Tips

- Don't fight the system by manually releasing every hard bounce you see — a hard bounce means the address is gone, and re-adding it to your sends will only bounce again.
- Check the Suppressions list after a big send if your open rate looks unusually low — a wave of soft bounces on a shared domain (e.g. a corporate mail server having issues) can be a sign of a temporary delivery problem worth investigating with your provider.
- If you're moving to Spwig from another platform, don't manually import your entire old blocklist as suppressions — let Spwig learn from real bounces and complaints on this list instead, so you don't accidentally block addresses that would have delivered fine.
- Review the **Source** column occasionally — a lot of **Provider webhook** entries confirms your email provider's bounce reporting is connected and working.
- Keep the **Detail** field meaningful when adding a manual block; it's the only record of why that decision was made once time has passed.
