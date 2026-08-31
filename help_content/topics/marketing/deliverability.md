---
slug: deliverability
title_i18n_key: Email Deliverability Runbook
category: marketing-seo
component: email_marketing
keywords:
  - email deliverability
  - inbox placement
  - spam folder
  - SPF
  - DKIM
  - DMARC
  - sender reputation
  - bulk sender requirements
  - Gmail deliverability
  - Yahoo deliverability
  - domain authentication
  - email warm-up
  - spam complaints
  - bounce rate
  - mail gateway
url_patterns:
  - /admin/email_system/emailaccount/
  - /admin/email_system/emailaccount/add/
  - /admin/campaigns/dashboard/
  - /admin/email_marketing/suppressionentry/
related:
  - email-configuration
  - list-hygiene
  - campaign-reports
  - communication-preferences
  - audiences
published: true
---

<!-- screenshots-needed:
- url: /admin/email_system/emailaccount/add/
  filename: wizard-dns-step.webp
  description: Step 4 (DNS Configuration) of the email account setup wizard for the built-in SMTP provider, showing the SPF/DKIM/DMARC validation one-liners and the DNS provider tabs (Cloudflare/GoDaddy/Namecheap/Route 53/Other) with at least one record's "Details" panel expanded so a copyable TXT record is visible.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/email_system/emailaccount/{account_id}/change/
  filename: dkim-dns-record.webp
  description: An existing built-in SMTP EmailAccount's change form scrolled to the "DKIM keys configured" panel, showing the DNS TXT record Name/Value and the Copy DNS Record button.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: suppressed-addresses-card.webp
  description: The Campaign Studio dashboard's Suppressed addresses stat card, for the "monitor" section of this runbook.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
-->

Getting an email *sent* is easy. Getting it into the inbox instead of the spam folder is the actual job — and mailbox providers like Gmail and Yahoo now enforce hard technical requirements before they'll even consider it. This runbook walks through what to configure, in what order, so your order confirmations and campaigns land where customers can see them.

Nothing here is a one-time task. Deliverability is a standing you build up over time and can lose quickly — the checklist at the end is worth revisiting whenever something looks off.

## Why it matters

Every major inbox provider scores incoming mail on sender reputation before it decides whether to deliver, fold into a spam folder, or reject it outright. Since 2024, Gmail and Yahoo formalised this into explicit **bulk sender requirements** for anyone sending meaningful volume:

- **Authenticate your domain** — valid SPF, DKIM, and DMARC records.
- **Make it easy to unsubscribe** — a working, low-friction opt-out in every marketing email.
- **Keep spam complaints low** — bulk senders that cross roughly 0.3% complaints risk having mail rejected or bulk-foldered outright; the safest target is well under 0.1%.

Fail these and it isn't just marketing campaigns that suffer — a damaged domain reputation can drag transactional mail (order confirmations, password resets) into spam too, since Gmail and Yahoo increasingly judge reputation at the sending-domain level, not just per message type. The steps below are how you meet all three.

## Step 1: Authenticate your sending domain

SPF, DKIM, and DMARC are DNS TXT records that prove to receiving mail servers that mail claiming to be from your domain really was sent by you. How you set them up depends on which sending mode your store uses — all three are configured under **Email Configuration** in the admin sidebar (this opens the Email Accounts list; see [Email Configuration](email-configuration) for the full account setup walkthrough).

| Sending mode | How authentication works |
|---|---|
| **Built-in SMTP** (Spwig's own email server) | Spwig generates a DKIM key pair for your domain automatically. Add an email account, and **Step 4** of the setup wizard shows your SPF, DKIM, and DMARC status plus the exact record to add, with copy-to-clipboard and provider-specific instructions for Cloudflare, GoDaddy, Namecheap, and AWS Route 53. The same DKIM DNS record is also shown on the account's own admin page later, under **DKIM keys configured**, if you need to find it again. |
| **Generic SMTP** (a bring-your-own provider like SendGrid, Mailgun, Amazon SES, or Google Workspace, connected via SMTP credentials) | Authentication happens partly in that provider's own dashboard. The setup wizard's DNS step includes tabbed instructions for Gmail, Outlook, SendGrid, Mailgun, and Amazon SES specifically — each explains what to configure in the provider's console (e.g. verifying a sending domain in SendGrid) and which resulting DNS records to add at your DNS host. |
| **Spwig-hosted mail gateway** | Available on Spwig-hosted plans as a managed sending option. It signs outgoing mail with DKIM automatically and defaults to sending from an address on Spwig's own verified domain, so it works with zero setup. If you want to send from your own domain through the gateway, talk to your hosting provider about verifying it — this is a managed service, not a self-serve DNS flow. |

Whichever mode you use, **adding the DNS record itself is always an external step** — you do it at your domain registrar or DNS host (Cloudflare, GoDaddy, Namecheap, Route 53, or wherever your domain's nameservers point), not inside Spwig. Spwig can tell you exactly what to add and validate that it's live, but it can't reach into your registrar and add it for you.

A few things worth knowing before you start:

- **DNS changes are not instant.** Propagation can take anywhere from a few minutes to 48 hours. The wizard's validation step will show a record as failing or missing until it has actually propagated — that's expected, not a sign something's wrong.
- **Only one SPF record is allowed per domain.** If you already have one (from Google Workspace, another mailer, etc.), add your new sender to the existing record with `include:` rather than creating a second SPF TXT record — two SPF records will break authentication for everyone.
- **DMARC needs SPF or DKIM to already pass.** Set it up last, once SPF and DKIM are both verified.

## Step 2: Use a real sending identity

Once your domain is authenticated, make sure what recipients actually see backs it up:

- **From address** — use an address on your own authenticated domain (`orders@yourstore.com`), never a free provider address (`yourstore@gmail.com`). A free-provider From address can't be authenticated by your SPF/DKIM/DMARC records at all, and inbox providers treat it as a strong spam signal from a store.
- **From name** — use your store's recognizable name, not a generic label like "Notifications" or "No Reply."
- **Reply-to** — set a monitored address. An unmonitored `noreply@` address that bounces or silently discards replies is itself a mild reputation signal, and it blocks the one channel customers have to tell you something went wrong.

Set all three under **Email Configuration > (your account) > Sender Configuration** — see [Email Configuration](email-configuration) for the full field walkthrough.

## Step 3: Warm up before you scale

A domain or IP with no sending history has no reputation yet — good or bad — and inbox providers are cautious with the unknown. Sending a huge first blast from a brand-new domain looks statistically identical to a spammer starting a new campaign, and it can get bulk-foldered even though every technical box is checked.

- Start smaller. Send your first few campaigns to your most engaged, most likely-to-open audience rather than your entire list at once — see [Audiences](audiences) for building a targeted starter segment.
- Increase volume gradually over the first few weeks rather than jumping straight to full-list sends.
- If you're migrating an existing list from another platform, treat it as day one for reputation purposes too — your old platform's sending history doesn't transfer with the domain.

## Step 4: Keep your list clean

Every complaint or bounce costs you reputation, and both are largely a function of who's on your list and how they got there:

- **Only mail people who consented.** Imported contacts, purchased lists, and scraped addresses are the fastest way to spike spam complaints and hard bounces.
- **Use double opt-in.** Spwig's marketing-consent flow verifies a subscriber's email address before sending them marketing mail — see [Communication Preferences](communication-preferences) for how this is configured.
- **Let Spwig's automatic suppression do its job.** Spwig watches for hard bounces, spam complaints, and repeated soft bounces and stops mailing those addresses automatically, with no setup required — see [List Hygiene and Suppressions](list-hygiene) for exactly how this works and when (rarely) to override it.
- **Prune inactive subscribers periodically** rather than mailing the same unengaged addresses indefinitely — a shrinking list that opens and clicks is worth more to your reputation than a large one that doesn't.

## Step 5: Monitor

Deliverability problems show up in the numbers before a customer ever tells you an email didn't arrive.

Open a campaign's [Report](campaign-reports) after each send and watch:

| Metric | What to watch for |
|---|---|
| **Bounce rate** | Mostly soft bounces is normal; a rising **hard bounce** share means your list has stale or invalid addresses accumulating. |
| **Spam complaints** | Should sit near zero on every send. Keep it well under the roughly 0.3% threshold that triggers bulk-sender enforcement at Gmail and Yahoo — treat even a small spike as worth investigating immediately. |
| **Open rate / click-to-open rate** | A sudden, unexplained drop across sends to the same list (not just one campaign) can be an early sign that mail is landing in spam rather than the inbox, even before bounce or complaint numbers move. |

Also check the Campaign Studio dashboard's **Suppressed addresses** card periodically — a steady trickle is normal list decay, but a sudden spike is worth investigating before your next send (see [List Hygiene](list-hygiene)).

If something spikes: pause and check your DNS records are still valid first (a lapsed domain renewal or an accidental DNS change can silently break SPF/DKIM), then look at what changed about the content or audience of the send that triggered it.

## Step 6: Content hygiene

Authentication and list quality get you in the door; content still affects how you're treated once you're there.

- **Avoid spam-trigger patterns** in subject lines — ALL CAPS, excessive punctuation ("!!!"), and phrases like "act now" or "free money" still weigh against you with spam filters, even from an authenticated domain.
- **Don't send image-only emails.** An email that's a single image with no real text is a classic spam pattern; keep a meaningful amount of actual text content alongside any images.
- **Preview before sending.** Check how the email actually renders — including on mobile — before it goes to your full list.
- **The unsubscribe link is already handled.** Spwig automatically adds a working, no-login-required unsubscribe link to the footer of every marketing email — you don't need to add your own (see [Communication Preferences](communication-preferences) for exactly how that flow works). Don't strip or hide it; a missing or broken unsubscribe link is itself a policy violation with Gmail and Yahoo's bulk sender rules, regardless of your other numbers.

## "My emails are going to spam" — troubleshooting checklist

Work through these in order:

1. **Re-check your DNS records.** Open the account's setup wizard DNS step (or the DKIM panel on the account's admin page for built-in SMTP) and confirm SPF, DKIM, and DMARC all still show as passing. A domain renewal, a DNS provider migration, or an unrelated change to your zone file can silently break one of these.
2. **Check the campaign report's bounce and complaint numbers** for the affected send(s) — see [Campaign Reports](campaign-reports). A spike in either points to a list-quality or content problem rather than an authentication one.
3. **Check the Suppressions list** ([List Hygiene](list-hygiene)) for a sudden jump — if a large chunk of your list has been failing for a while, deliverability to the rest degrades too.
4. **Confirm your From address is on your authenticated domain**, not a free-provider address or a domain that doesn't match what SPF/DKIM/DMARC were set up for.
5. **Send a test email to a Gmail and a Yahoo/Outlook address you control** and check the actual folder it lands in, not just whether it arrived.
6. **If you recently changed sending volume or audience sharply,** treat it as a fresh warm-up — dial volume back down and ramp more gradually.
7. **If everything above checks out and the problem persists,** it may be provider-specific throttling rather than a fault in your setup — this can take some time to resolve on its own once the underlying cause (usually complaints or bounces) has been fixed.

## Tips

- Fix DNS authentication before you fix anything else — every other deliverability lever (content, list hygiene, warm-up) matters less if SPF/DKIM/DMARC aren't passing.
- Treat the setup wizard's DNS validation as a point-in-time check, not a one-off — re-run it any time you migrate DNS providers or renew a domain through a different registrar.
- A clean list that opens and clicks will always out-perform a bigger list that doesn't — resist the urge to import an old, unverified list "just in case."
- Watch your numbers relative to your own past sends, not a generic industry benchmark — your own history is the most reliable signal of a real problem.
- If you're on a Spwig-hosted plan, the hosted mail gateway's DKIM signing and reputation management are handled for you — your remaining responsibility is list quality and content, not DNS.
