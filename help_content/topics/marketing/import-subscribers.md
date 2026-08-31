---
slug: import-subscribers
title_i18n_key: Importing Subscribers from a CSV
category: marketing-seo
component: email_marketing
keywords:
  - import subscribers
  - CSV import
  - bulk import contacts
  - upload subscriber list
  - xlsx import
  - excel import
  - email marketing import
  - consent checkbox
  - opt-in contacts
  - duplicate contacts
  - import preview
  - campaign studio
  - personalise emails
  - merge fields
url_patterns:
  - /admin/email_marketing/subscriber/import/
  - /admin/email_marketing/subscriber/
related:
  - subscriber-tags
  - triggered-journeys
  - recurring-campaigns
published: true
---

If you already have a mailing list somewhere else — an old email tool, a spreadsheet of newsletter sign-ups, a stack of trade-show badge scans — you don't need to add those contacts to Spwig one at a time. Campaign Studio's subscriber import reads a CSV or Excel file and adds every valid contact to your audience in one go, ready to tag, segment, and email.

## Before you import: consent

Every import requires you to tick a box confirming: **"These contacts have agreed to receive marketing email from me."** This isn't a formality — only import contacts who have genuinely opted in to marketing email from you. It matters for two reasons:

- **It's a legal requirement in most places.** Sending marketing email to people who never agreed to receive it breaks consent laws in many jurisdictions.
- **It protects your deliverability.** Emailing people who never opted in generates spam complaints and bounces, which mailbox providers use to decide whether *any* of your email — including to people who did opt in — reaches the inbox.

If a list doesn't clearly come from opted-in sign-ups, don't import it.

## Preparing your file

The importer accepts a `.csv` or `.xlsx` file with a header row. Only one column is required:

| Column | Required? | Notes |
|--------|-----------|-------|
| **Email** | Yes | Must be a valid email address. |
| **First name** | No | Used to personalise emails. |
| **Last name** | No | Used to personalise emails. |
| **Language** | No | The subscriber's preferred language code (e.g. `en`, `es`). |

Columns are matched to these fields automatically by header name, so you don't need to rename anything first — common variations like `E-mail`, `Email Address`, `First Name`, `Given Name`, `Surname`, or `Locale` are all recognised.

Each import is capped at **5 MB** and **5,000 rows**. If your list is bigger than that, split it into smaller files and import them one after another.

## Importing your contacts

1. Open **Campaign Studio > Subscribers** and click **Import CSV**.
2. Choose your `.csv` or `.xlsx` file.
3. Choose what happens **for contacts already on your list** — see [Handling duplicates](#handling-duplicates) below.
4. Optionally choose a tag under **Tag imported contacts as** to label everyone in this import (e.g. `Event 2026`) — see [Subscriber Tags](/help/subscriber-tags) for more on tags.
5. Tick **These contacts have agreed to receive marketing email from me**.
6. Click **Continue**.

![The import upload form with a file chosen, a tag selected, and consent confirmed](/static/core/admin/img/help/import-subscribers/import-upload-form.webp)

Spwig then shows you a preview before anything is actually imported:

![The import preview showing new, existing, and skipped-invalid counts with reasons](/static/core/admin/img/help/import-subscribers/import-preview.webp)

- **New contacts** — rows that will create a brand-new subscriber.
- **Already on your list** — rows whose email address matches an existing subscriber.
- **Skipped (invalid)** — rows that couldn't be read, each listed with its row number and the reason (an invalid email format, an empty email cell, or a duplicate of an earlier row in the same file).

Check these numbers, then click **Import now** to commit the import, or **Cancel** to back out without changing anything.

## Handling duplicates

A row counts as a duplicate when its email address matches a subscriber you already have. You choose how Spwig treats those rows on the upload form:

| Option | What happens |
|--------|--------------|
| **Leave them unchanged** *(default)* | The existing subscriber's name and language are kept as-is. |
| **Update their name / language** | The existing subscriber's first name, last name, and language are updated from the file (only for the fields the file actually provides). |

The tag you choose for the import is applied to **everyone in the file** — new and existing contacts alike — whichever duplicate option you pick. So importing your "VIP list" with the **VIP** tag tags the people you already have, too. The duplicate option only controls whether an existing contact's *name and language* are overwritten.

## After the import

Every contact created by an import is recorded with source **Import**, and marked as consented at the moment you ran the import (not any earlier date they may have opted in elsewhere). Their first and last name — if the file provided them — are stored on their subscriber record, which means the `[[first_name]]` and `[[last_name]]` merge fields in your campaigns now personalise correctly for them too, even though they've never created a Spwig account.

## Tips

- Export your source list to a single-sheet CSV or `.xlsx` with a clean header row before uploading — extra sheets, merged cells, or summary rows can confuse the column matching.
- Use **Tag imported contacts as** to immediately create the exact audience you'll want to target afterward — see [Subscriber Tags](/help/subscriber-tags) for building a segment from it.
- Always read the **Skipped (invalid)** reasons before assuming an import went wrong — a handful of skipped rows with clear reasons is normal for most real-world lists.
- Re-running the same file is safe: contacts you already imported are treated as duplicates the second time, not re-created.
- If you're consolidating several small lists, tag each import differently (e.g. `Import: Jan Event`, `Import: Trade Show`) so you can tell them apart later even after they're all mixed into your main audience.
- For lists over 5,000 rows, split by an obvious boundary (alphabetical, by source, or by date collected) rather than an arbitrary cut, so each batch stays easy to identify afterward.
