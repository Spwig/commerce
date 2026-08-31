---
slug: recurring-campaigns
title_i18n_key: Recurring Campaigns
category: marketing-seo
component: email_marketing
keywords:
  - recurring campaign
  - campaign studio
  - email newsletter
  - automated email
  - newsletter schedule
  - weekly digest
  - monthly digest
  - blog digest email
  - new since last send
  - no new content policy
  - occurrence history
  - email automation
url_patterns:
  - /admin/email_marketing/campaign/
related:
  - blog-management
  - ab-testing
  - audiences
  - campaign-reports
published: true
---

Campaign Studio's **Recurring Campaigns** let you set up a newsletter once — a weekly product roundup, a monthly blog digest — and have Spwig send it automatically on a repeating schedule, instead of you creating and sending a new campaign by hand every time.

## Broadcast vs. recurring

Every campaign in Campaign Studio has a **Campaign type**:

| Type | Behaviour |
|------|-----------|
| **Broadcast** | Sent once — immediately or at a single scheduled date and time. Use this for a one-off announcement, sale, or product launch email. |
| **Recurring** | Acts as a template that sends on a repeating schedule. Each send is a fresh, dated copy called an **occurrence** — the template itself never "sends" directly. |

To turn a campaign into a recurring one, open it in **Campaign Studio > Campaigns** and set **Campaign type** to **Recurring**, then save. A **Schedule** section appears on the campaign once you reopen it — it only shows up for recurring campaigns.

![Campaign type set to Recurring](/static/core/admin/img/help/recurring-campaigns/campaign-type-selector.webp)

## Setting a schedule

Once a campaign is recurring, its **Schedule** section controls when it fires:

| Field | Description |
|-------|-------------|
| **Active** | Turns the recurrence on or off without deleting the schedule. |
| **Cadence** | **Daily**, **Weekly**, or **Monthly**. |
| **Interval** | Send every N cadence units — e.g. interval `2` with **Weekly** cadence means every 2 weeks. |
| **Weekday** | Which day to send on for a weekly cadence (`0` = Monday … `6` = Sunday). |
| **Day of month** | Which day to send on for a monthly cadence (`1`–`28`, so every month has that day). |
| **Send time** | The time of day the campaign goes out. |
| **Timezone** | An IANA timezone name, e.g. `Europe/London` or `America/New_York` — the send time is interpreted in this zone, not the server's. |

![Weekly schedule section on a recurring campaign](/static/core/admin/img/help/recurring-campaigns/schedule-section.webp)

As soon as you save an active schedule, it **arms itself** — Spwig calculates the next fire time and shows it in **Next run at**. You don't need to trigger anything manually; a background task checks for due schedules and sends the occurrence when the time comes. **Last run at** and **Occurrences sent** update automatically after every send so you can see the schedule is alive.

## The no-new-content policy

Recurring newsletters often feature dynamic content — most commonly a **Blog Posts** block (or a **Product Grid**) set to **New since last send** in the visual builder, which only pulls in posts published — or products added — since the campaign's previous send. That raises an obvious question: what happens if a scheduled run arrives and there's nothing new to feature?

Spwig answers this with the schedule's **No-new-content policy**:

| Policy | What happens | Best for |
|--------|---------------|----------|
| **Skip this send** *(default)* | The occurrence is skipped entirely — nothing sends. The schedule moves straight on to its next scheduled run. | A blog or product digest, so subscribers are never sent an email that just repeats what they already saw. |
| **Send anyway (omit empty blocks)** | The email sends on schedule regardless. Any block that has nothing new — like an empty "New since last send" Blog Posts block — simply renders nothing in that spot. | Newsletters that always have other content worth sending (a welcome message, evergreen sections, or several dynamic blocks) even if one block comes up empty. |
| **Hold and send late** | The send is postponed. Spwig checks again once a day for fresh content, up to the **Hold window (days)**. If new content appears within that window, the occurrence sends late; if the window elapses with nothing new, that occurrence is given up and the schedule moves on to its next slot. | A cadence you want to protect (e.g. always send *something* eventually) without firing an empty issue the moment nothing new happened to publish that week. |

Only campaigns using delta-aware content — a Blog Posts block or a Product Grid set to **New since last send** — trigger this check. A recurring campaign with no such blocks is always considered to have fresh content and sends normally on schedule.

**Hold window (days)** only applies to the **Hold and send late** policy — it sets how many days Spwig will keep retrying before giving up on that occurrence.

## A/B testing each occurrence

A recurring newsletter is a natural place to A/B test your **subject lines** — you send on a regular cadence to the same audience, so you can keep learning what wording earns more opens. Spwig can run a fresh subject-line A/B on **every occurrence** automatically.

Set it up in the **Schedule** section:

1. In **A/B subject lines**, enter **two to four** subject lines, one per line. Leave it blank to send occurrences normally with the template's own subject.
2. Set the **A/B test sample %** — the share of each occurrence's audience used to test, split evenly across the subjects. The rest is the holdout that receives the winner.
3. Choose the **A/B winner metric** (open or click rate), the **A/B test window (hours)** to gather results before deciding, and whether to **auto-send the winner** to the holdout.

From then on, each time the schedule fires, that occurrence splits its audience, sends each subject line to a slice, waits out the test window, then picks the winning subject and sends it to everyone else — with no further action from you. Each occurrence is its own self-contained test, so you get a fresh read every send and can watch which subjects win over the weeks. Each occurrence's result shows up under **Occurrence history** below, linking straight to its results page with the per-variant rates, the winner, and how confident Spwig is (see [A/B Testing](ab-testing) for how to read those results).

Two things worth knowing:

- **A/B testing here is subject-line only.** To compare entirely different designs, use a one-off broadcast A/B test — the full wizard, which supports content variants, is for broadcast campaigns.
- If an occurrence's audience is ever **too small to split** across the variants, Spwig quietly sends that occurrence as a normal newsletter instead — a lean week never means a missed send.

## Occurrence history

Every time a recurring campaign actually sends, Spwig creates a dated **occurrence** — a real, independent campaign record with its own subject, recipients, and send statistics (sent, failed, skipped, opens, clicks). The occurrence is named after the template with the send date appended, e.g. "Weekly Blog Digest — 2026-08-19".

The recurring campaign's edit page lists its **Occurrence history** — the most recent occurrences, each linking through to that occurrence's own campaign record so you can review exactly what was sent and how it performed.

![Occurrence history list on a recurring campaign](/static/core/admin/img/help/recurring-campaigns/occurrence-history.webp)

## Tips

- Pair a recurring campaign with a **Blog Posts** block set to **New since last send** for a self-maintaining "new posts this week" digest — you write posts, Spwig handles the emailing.
- Start with **Skip this send** for content digests. It's the safest default: subscribers never receive a repeat of last time's content.
- Only switch to **Send anyway** if your template has other content that's worth sending on its own, even when the dynamic block is empty.
- Use **Hold and send late** when missing a cadence beat occasionally is fine, but missing it for weeks in a row isn't — set the hold window to match how long a gap you're comfortable with.
- Check **Next run at** after saving a schedule to confirm it landed on the day and time you expected, especially when working across timezones.
- Review the **Occurrence history** regularly — a template that keeps skipping is a sign your dynamic content source (e.g. the blog) has gone quiet.
