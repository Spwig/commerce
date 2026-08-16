---
slug: visibility-rules
title_i18n_key: Visibility Rules
category: design-content
component: visibility
keywords:
  - visibility
  - visibility rules
  - rule group
  - show
  - hide
  - conditional display
  - market
  - region
  - geo
  - country
  - currency
  - language
  - device
  - mobile
  - logged in
  - members
  - guests
  - cart
  - audience
  - personalization
url_patterns:
  - /admin/visibility/rulegroup/
  - /admin/visibility/visibilityrule/
related:
  - page-builder
  - design-themes
published: true
---

# Visibility Rules

Visibility rules let you show or hide parts of your storefront depending on who
is visiting and where they are. You can gate **page elements**, **menu items**,
and **header/footer widgets** by the same conditions — a customer's market or
region, the language or currency they're viewing in, the time of day, or
per-visitor signals like whether they're signed in.

Everything is built from **rule groups**: a named, reusable bundle of one or more
conditions. You create a rule group once (for example, "New Zealand market" or
"Signed-in members") and then attach it to any element, menu item, or widget you
want it to control. An item with no rule groups attached is always visible.

## How visibility is decided

When more than one rule group is attached to an item, the item is shown if **any**
attached group matches (they combine with OR). Within a single group you choose
whether **all** or **any** of its conditions must match.

Rules fall into two families, and Spwig handles them differently so your store
stays fast and search-engine friendly:

- **Market rules** — region/market, language, currency, and time-based
  conditions. These are decided on the server for each market URL, so the same
  page is delivered identically to every visitor (and every search engine) at
  that address. This keeps pages cacheable and SEO-safe.
- **Per-visitor rules** — signed-in status, cart contents, device, and precise
  location. These depend on the individual visitor, so Spwig resolves them
  privately for each person after the page loads. They are never baked into a
  shared, cached page.

If you disable a rule group, it simply stops applying — the item it was attached
to returns to being visible. Disabling a group is not a way to hide something.

## Creating and attaching rules

There are two ways to work with rule groups.

### Attach them where you design

Wherever you can gate content, you'll see a **visibility control** (the eye icon):

- **Page Builder** — select an element, open its properties, and use the
  visibility control.
- **Menu Builder** — select a menu item and open the **Visibility** tab. This
  works on **any** item, including a sub-menu (dropdown) item nested under another
  — a rule on a child hides just that child, leaving the rest of the menu intact.
- **Header & Footer Builder** — select a widget and open the **Visibility Rule
  Groups** section of its settings.

Rules that depend on the individual visitor — whether they're signed in, what's
in their cart, or their device — are resolved for each shopper without slowing
your store or affecting search engines. Your storefront stays fast and cacheable,
and each visitor still sees only the navigation meant for them.

In the visibility editor you can:

- **Attach** any of your existing rule groups by ticking them.
- **Quick rule** — create a simple rule group on the spot (for example "members
  only", a single market, a currency, a device, or a minimum cart value) and
  attach it in one step.
- **Manage rule groups** — jump to the full builder for advanced rules.

Click **Apply** and the item is gated immediately.

### Build advanced rules

For anything more involved — combining several conditions, nesting groups, or
fine-grained operators — go to **Design → Visibility Rules** (rule groups). There
you can assemble rules with AND/OR logic and reuse them across your whole store.

## Common conditions

| Condition | Use it to… |
|-----------|------------|
| **Region / market** | Show a block only to visitors in a specific market (e.g. New Zealand) |
| **Selected currency** | Show pricing notes or offers only when a certain currency is active |
| **Selected language** | Show content only in a specific language |
| **Date / time / day / business hours** | Run a banner during a sale window or only during opening hours |
| **Signed-in status** | Show "members only" content, or a sign-up prompt to guests |
| **Device type** | Show or hide something on mobile, tablet, or desktop |
| **Cart value / items** | Show a free-shipping nudge once the cart passes a threshold |

## Previewing

In the Page Builder preview you can **preview as a market** and **preview as a
visitor** (signed-in or guest, with a sample cart) to see exactly what each
audience would see — including the per-visitor rules that normally resolve
privately.

## Tips

- Build a small set of well-named rule groups ("NZ market", "Members", "Mobile
  only") and reuse them everywhere — it's easier to manage than one-off rules.
- Market rules are the safe choice for anything you want indexed by search
  engines, because the result is the same for everyone at a given market URL.
- If an item disappears unexpectedly, check its attached rule groups — an item is
  hidden only when it has an active group and none of its groups match the current
  visitor.
