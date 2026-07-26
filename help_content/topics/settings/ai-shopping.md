---
slug: ai-shopping
title_i18n_key: AI Shopping
category: settings
component: agentic
keywords:
  - ai shopping
  - agentic commerce
  - shopping agents
  - ai assistants
  - ucp
  - universal commerce protocol
  - agent checkout
  - discovery
  - emergency stop
  - kill switch
  - agent visibility
url_patterns:
  - /admin/agentic/agenticsettings/
  - /admin/agentic/agentidentity/
  - /admin/agentic/agentevent/
related:
  - site-settings-overview
  - payment-terminal-providers
published: true
---

AI Shopping lets AI shopping assistants find your products and, when you allow it, buy from your store on a customer's behalf. It is **off by default** — turning it on is a deliberate choice, and until you do, your store exposes nothing to these assistants.

## Turning it on

Open **Settings → AI Shopping** and switch **Agentic commerce enabled** on. From that point, assistants that support the Universal Commerce Protocol can discover your store and read your catalogue. Nothing about your normal storefront changes.

## The readiness dashboard

The top of the AI Shopping page answers one question in a single sentence: **can AI assistants actually buy from your store right now?**

- **"AI assistants can buy from your store"** — everything needed for a purchase is in place.
- **"AI assistants can browse your store, but can't buy yet"** — your store is discoverable, but something is missing before a purchase can complete (usually a connected payment provider).
- **"Emergency stop is on"** or **"Agentic commerce is off"** — nothing is being served to assistants.

Below the verdict you'll see a short checklist — payment provider connected, shipping can be quoted, products are visible to assistants — with a hint next to anything that still needs attention. The counters show how many products assistants can sell, how many you've hidden from them, how many assistants have visited, and how many you've blocked.

The checklist reflects your **live** setup: connect a payment provider or add a shipping method and the verdict updates the next time you open the page.

## The emergency stop

The **Emergency stop** is a separate switch from the main one. Use it to halt all assistant activity immediately — for example if something looks wrong — without unpicking your configuration. Clear it to resume. Think of the main switch as "is this feature configured on" and the emergency stop as "stop everything right now".

## What assistants can do

Two levels of access, controlled separately:

- **Reading** (discovery and browsing) is lower-risk. An assistant can find your store and read product details.
- **Checkout** (actually buying) is higher-stakes and stays closed to unverified assistants unless you allow it.

A store can be discoverable without being purchasable — a useful way to start.

## Hiding specific products

Every product has a **Visible to AI shopping agents** setting (on by default). Switch it off to keep a particular product off assistants while it stays on your storefront — handy for items you'd rather sell only through your own site.

## Managing individual assistants

When an assistant first buys — or tries to — Spwig records it under **AI Shopping → Agent Identities**. Each entry shows the assistant's verified home (the directory it signs with) and how many requests it has made. The name and logo an assistant presents are shown only as *claimed* details — treat them as a label, not proof of identity; the verified home is the part that can be trusted.

New assistants start **capped**: they can transact, but within limits. To stop one, select it and choose **Block selected assistants** — open checkouts end and the assistant can no longer buy, while any payment already taken is left untouched. **Unblock selected assistants** returns it to the capped state (never straight to unlimited — lifting limits is always a separate, deliberate step).

## The activity record

**AI Shopping → Agent Events** is a tamper-evident record of what assistants did — every verified request, every blocked attempt, every change you made. It is view-only and cannot be edited or deleted, so it stands as your evidence trail if a purchase an assistant made is ever disputed.

## A note on the assistant platforms

The companies running these assistants (and the rules for appearing in them) are new and change often. Some require you to apply or meet regional conditions before your products can be bought through them. Spwig makes your store ready; whether a given assistant lists you is up to that assistant.
