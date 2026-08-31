---
slug: subscriber-tags
title_i18n_key: Subscriber Tags
category: marketing-seo
component: email_marketing
keywords:
  - subscriber tags
  - tag subscribers
  - audience tags
  - VIP customers
  - wholesale customers
  - bulk tag subscribers
  - add tag to selected
  - remove tag from selected
  - tag filter
  - has tag segment rule
  - segment rule builder
  - campaign studio
  - organise subscribers
  - subscriber labels
url_patterns:
  - /admin/email_marketing/subscribertag/
  - /admin/email_marketing/subscriber/
  - /admin/email_marketing/segment/
related:
  - audiences
  - import-subscribers
  - triggered-journeys
  - recurring-campaigns
published: true
---

Tags are your own labels for organising your Campaign Studio audience — short markers like `VIP`, `wholesale`, or `event-2026` that you define and apply to whichever subscribers they fit. Once a tag exists, you can filter your Subscribers list by it, apply or remove it from any number of people at once, and — most usefully — use it as a condition when building a Segment, so your campaigns and journeys can target exactly the people you've tagged.

## What tags are

A tag is nothing more than a name you choose. Spwig doesn't come with any built-in tags, and it never applies one automatically — you decide what they're called and who gets one. That makes them a good fit for anything specific to your own business that doesn't map to a status Spwig already tracks: a loyalty tier, a wholesale account, everyone who signed up at a trade show, or a one-off event list like `event-2026`.

Each tag also gets a **Slug** — a simplified, URL-safe version of its name — generated automatically when you create it. Segments and filters use the slug internally; as a merchant you'll almost never need to look at it.

## Creating a tag

Tags have their own admin section. Open **Campaign Studio > Subscribers**, then click **Campaign Studio** at the top of the page to see the full list of Campaign Studio sections, and choose **Subscriber tags**.

1. Click **Add subscriber tag**.
2. Enter a **Name** — short and specific reads best, e.g. `VIP`, `Wholesale`, or `Event 2026`.
3. Spwig fills in a matching **Slug** as you type. You can leave it as generated.
4. An optional **Colour** field is also available if you'd like to record a hex colour (e.g. `#2563eb`) against the tag for your own reference.
5. Click **Save**.

You don't have to leave what you're doing to create one, either — a green **+** next to the **Tags** field on any subscriber's own edit page opens the same "add a tag" form in a popup. And if you try to bulk-tag subscribers before you've created any tags at all, the tag picker offers a **Create a tag** shortcut that takes you straight there.

## Tagging subscribers

The most common way to apply a tag is in bulk, from the Subscribers list:

1. Open **Campaign Studio > Subscribers**.
2. Tick the checkbox on each subscriber you want to tag (or **Select all on this page**).
3. From the **Bulk actions** dropdown, choose **Add tag to selected…** (or **Remove tag from selected…** to untag people).
4. Click **Go**.
5. Pick the tag from the list and click **Add tag** (or **Remove tag**).

![The bulk tag picker after choosing "Add tag to selected…" for four subscribers](/static/core/admin/img/help/subscriber-tags/bulk-tag-picker.webp)

Once applied, a tag shows as a small chip on the subscriber's card in the list, alongside their status and source badges. A **Tag** filter also appears in the Subscribers list's filter panel once you have at least one tag, so you can narrow the list down to everyone carrying a specific tag — handy for checking who's in an audience before you build a campaign around it.

![The Subscribers list filtered to the VIP tag, with the Import CSV button and tag chips visible](/static/core/admin/img/help/subscriber-tags/subscriber-list-tag-chips.webp)

You can also add or remove a single subscriber's tags directly from their own edit page, using the same **Tags** field the bulk action manages.

## Using tags in segments

Segments are the saved, rule-based audiences you point campaigns and journeys at. Once you've created at least one tag, a **Has tag** condition becomes available in the segment rule-builder — it doesn't appear on a fresh install with no tags defined, so you won't see a dead option before it's useful to you.

To use it, open **Campaign Studio > Segments**, add (or edit) a dynamic segment, and click **+ Add condition**:

1. Set the condition's field to **Has tag**.
2. Choose an operator — **is** for a single tag, or **is any of** when you'd rather phrase it that way.
3. Pick the tag from the dropdown.

![A "Has tag" condition set to VIP, showing a live count of matching subscribers](/static/core/admin/img/help/subscriber-tags/segment-has-tag-rule.webp)

The count in the top-right updates as you build the rule, so you can see exactly how many subscribers currently qualify before you save. Each **Has tag** condition currently matches one tag at a time — if you want an audience that matches *any* of several tags (say, `VIP` or `Wholesale`), add one **Has tag** condition per tag and set **Match** to **any**.

This is what makes tags useful beyond organisation: a segment built on **Has tag** becomes an audience you can select as the **Segment** on a broadcast or recurring campaign, or as a journey's **Only for segment** setting — so "everyone tagged VIP" can have its own welcome series, its own recurring newsletter, or simply be who you select the next time you send a one-off announcement.

## Tips

- Keep tag names short and specific — they show up as compact chips on subscriber cards, so `VIP` reads better than `Very Important Person - Tier 1`.
- Use the **Tag** filter to sanity-check who's actually tagged before you build a segment or send a campaign around it.
- Tagging is additive — removing a tag from a subscriber never affects any other tag they have, and never touches their status, source, or consent.
- Combine tags with other rule-builder conditions (like **Opted into marketing** or **Total spent**) on the same segment for a more precise audience, not just a tag on its own.
- A subscriber can carry as many tags as you like — there's no limit, so it's fine to use them for several overlapping purposes (a loyalty tier *and* an event list *and* a source note).
- If a tag stops being useful, deleting it from **Subscriber tags** removes it from every subscriber it was applied to and from any segment rules that referenced it — segments using it will simply stop matching on that condition.
