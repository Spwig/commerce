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
  - agent policy
  - verify assistant
  - spend cap
  - agent trust level
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

When an assistant first buys — or tries to — Spwig records it under **AI Shopping → Agent Identities**. Each entry shows the assistant's verified home (the directory it signs with), its trust level, and how many requests it has made. The name and logo an assistant presents are shown only as *claimed* details — treat them as a label, not proof of identity; the verified home is the part that can be trusted.

Every assistant sits in one of three trust levels:

| Trust level | What it means |
|---|---|
| **Capped (verified, limited)** | The default for a new assistant. Spwig has recorded its identity, and it carries the order-value cap, spend cap, and tender restrictions set on its policy (see below). |
| **Verified (limits removed)** | A deliberate decision by you to trust this assistant fully. Its order-value and daily spend caps are cleared. |
| **Blocked** | The assistant can no longer buy from your store. Open checkouts end, though any payment already taken is left untouched. |

To stop an assistant, select it in the list and choose **Block selected assistants**. **Unblock selected assistants** always returns it to **Capped** — never straight to Verified — because lifting limits is a separate, deliberate step.

To lift an assistant's limits entirely, select it and choose **Promote to verified (remove limits)**. This clears its max order value and daily spend cap and moves the assistant to the Verified state. A blocked assistant is skipped — unblock it first, then promote it. Treat this as a real trust decision: only promote an assistant you're confident about, since verification removes the guardrails a new assistant starts with.

## Setting an assistant's limits

Open an assistant's detail page and use the **Policy (limits & allowed tenders)** section to set what it's allowed to do:

| Field | What it controls |
|---|---|
| **Max order value** | The largest single order this assistant can place. Leave blank for no cap. |
| **Daily spend cap** | The most this assistant can spend across all orders in a day. Leave blank for no cap. |
| **Allow discount codes** | Whether the assistant can apply voucher codes at checkout. |
| **Allow gift cards** | Whether the assistant can redeem gift cards. |
| **Allow digital goods** | Whether the assistant can buy digital products. |
| **Rate limit (per minute)** | How many requests the assistant can make to your store per minute. |

A new assistant starts capped with concrete order-value and spend caps, and with discount codes, gift cards, and digital goods switched off — the deliberately conservative default. Change any of these fields and save; every change is written to **Agent Events** with the before and after values, so you always have a record of who changed what, and when. Promoting an assistant to Verified clears its Max order value and Daily spend cap for you — you don't need to blank them out by hand first.

## The activity record

**AI Shopping → Agent Events** is a tamper-evident record of what assistants did — every verified request, every blocked attempt, every change you made. It is view-only and cannot be edited or deleted, so it stands as your evidence trail if a purchase an assistant made is ever disputed.

## A note on the assistant platforms

The companies running these assistants (and the rules for appearing in them) are new and change often. Some require you to apply or meet regional conditions before your products can be bought through them. Spwig makes your store ready; whether a given assistant lists you is up to that assistant.
