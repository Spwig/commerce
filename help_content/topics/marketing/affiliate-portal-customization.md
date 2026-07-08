---
slug: affiliate-portal-customization
title_i18n_key: Affiliate Portal Customization
category: affiliates
component: affiliate
keywords:
  - affiliate portal
  - customize portal
  - affiliate landing page
  - portal settings
  - affiliate registration
  - portal customization
  - portal branding
  - affiliate features
  - portal hero
  - affiliate signup
  - portal layout
  - affiliate welcome
url_patterns:
  - /en/admin/affiliate/affiliatesettings/
  - /affiliate/
related:
  - affiliate-program-overview
  - creating-affiliate-programs
published: true
---

The Spwig Affiliate Portal is the public-facing landing page where potential affiliates learn about your program and sign up. Customizing this portal lets you align the messaging, branding, and call-to-action with your store's unique positioning. A well-designed portal attracts high-quality affiliates and converts visitors into active partners.

## What is the Affiliate Portal?

The affiliate portal is accessible at `/affiliate/` on your store's domain. It serves as:

- **Discovery page** — Where potential affiliates learn about your commission structure, benefits, and requirements
- **Registration entry point** — Sign-up form for new affiliates (guest registration or account-based)
- **Login gateway** — Existing affiliates can sign in to access their dashboard
- **Brand showcase** — Reflects your store's identity and affiliate program value proposition

The portal is fully customizable through the Affiliate Settings admin, including hero messaging, feature highlights, step-by-step flows, and registration options.

![Affiliate Portal Landing Page](/static/core/admin/img/help/affiliate-portal-customization/portal-landing.webp)

## Accessing Settings

Navigate to **Marketing > Affiliate Program > Portal Settings** to customize the portal.

The Affiliate Settings model is a **singleton** — you have exactly one settings record for your entire store. All fields are **translatable** using Spwig's translation system, so you can customize messaging for each language your store supports.

## Hero Section

The hero section is the first thing potential affiliates see. It includes:

- **Title** — Main headline (e.g., "Join Our Affiliate Program")
- **Subtitle** — Supporting text explaining the program value (e.g., "Earn commissions by promoting premium products to your audience")
- **Statistics** — Auto-displayed metrics:
  - Total active programs
  - Total active affiliates
  - Average commission rate (calculated across all active programs)
- **CTA Buttons** — Automatically generated:
  - **Sign In** — For existing affiliates
  - **Become an Affiliate** — Triggers registration flow

### Customizing Hero Messaging

| Field | Example Value | Purpose |
|-------|--------------|---------|
| **Hero Title** | "Partner With Us & Earn" | Grab attention with benefit-focused headline |
| **Hero Subtitle** | "Join 500+ affiliates earning competitive commissions on every sale you refer" | Provide social proof and clarify the offer |

The statistics are **automatically calculated** and update in real-time based on your active programs and affiliates. You cannot manually edit these values.

## Features Section

The features section highlights **6 customizable benefit cards** that explain why affiliates should join your program. Each feature card contains:

- **Icon** — FontAwesome icon class (e.g., `fa-dollar-sign`, `fa-chart-line`, `fa-headset`)
- **Title** — Benefit headline (e.g., "Competitive Commissions")
- **Description** — 1-2 sentence explanation (e.g., "Earn up to 15% on every sale you refer")

### Default Features

Spwig provides default features when you first install the affiliate app:

| Icon | Title | Description |
|------|-------|-------------|
| `fa-dollar-sign` | Competitive Commissions | Earn generous commissions on every sale you refer |
| `fa-link` | Easy Tracking Links | Get unique tracking links that work anywhere |
| `fa-chart-line` | Real-Time Analytics | Track clicks, conversions, and earnings in your dashboard |
| `fa-calendar-check` | Reliable Payouts | Get paid on time via PayPal or bank transfer |
| `fa-headset` | Dedicated Support | Our team is here to help you succeed |
| `fa-gift` | Marketing Materials | Access banners, images, and promotional content |

### Customizing Features

Features are stored as a **JSON array** in the database. Edit them directly in the admin form:

```json
[
  {
    "icon": "fa-percent",
    "title": "Up to 20% Commission",
    "description": "Earn industry-leading commissions on premium product sales"
  },
  {
    "icon": "fa-rocket",
    "title": "Fast Approval",
    "description": "Get approved in 24 hours and start promoting immediately"
  },
  {
    "icon": "fa-mobile-alt",
    "title": "Mobile Dashboard",
    "description": "Manage your links and track earnings from any device"
  }
]
```

**Icon Reference:** Use any FontAwesome 5 Free icon class. Browse icons at [fontawesome.com/icons](https://fontawesome.com/icons) and use the class name (e.g., `fa-trophy`, `fa-users`, `fa-star`).

## How It Works Section

The "How It Works" section displays a **4-step visual flow** that explains the affiliate journey. Each step includes:

- **Title** — Step name (e.g., "Sign Up")
- **Description** — 1-2 sentence explanation of what happens

### Default Steps

| Step | Title | Description |
|------|-------|-------------|
| 1 | Sign Up | Create your free affiliate account in minutes |
| 2 | Get Your Links | Generate unique tracking links for any product or page |
| 3 | Promote | Share your links with your audience through content, social media, or email |
| 4 | Earn Commissions | Get paid when customers purchase using your referral links |

### Customizing Steps

Steps are stored as a **JSON array**. You can edit them in the admin:

```json
[
  {
    "title": "Apply to Join",
    "description": "Submit your application and tell us about your platform"
  },
  {
    "title": "Get Approved",
    "description": "Our team reviews your application within 24 hours"
  },
  {
    "title": "Create Links",
    "description": "Access your dashboard and generate tracking links instantly"
  },
  {
    "title": "Start Earning",
    "description": "Earn commissions on every sale you refer — paid monthly via PayPal"
  }
]
```

The visual flow automatically numbers each step (1, 2, 3, 4) on the landing page.

## CTA Section

The final section before the registration form is the **Call-to-Action (CTA) section**. It provides one last push to encourage sign-ups.

| Field | Example Value | Purpose |
|-------|--------------|---------|
| **CTA Title** | "Ready to Start Earning?" | Direct question creates urgency |
| **CTA Description** | "Join our affiliate program today and start earning commissions on products you already love and recommend." | Reinforce benefits and eliminate friction |

The CTA section automatically displays the **Become an Affiliate** button below the text.

## Registration Settings

Control how new affiliates sign up and what information they provide.

### Custom Registration Form

**Field:** `custom_form` (ForeignKey to FormBuilder form)

If you have a custom registration form built with Spwig's Form Builder, select it here. This allows you to collect additional information during sign-up (e.g., website URL, audience size, promotion channels).

**Leave blank** to use the default affiliate registration form (email, password, payment details).

### Allow Guest Registration

**Field:** `allow_guest_registration` (Boolean)

- **Checked** — Visitors can apply without creating a Spwig account first
- **Unchecked** — Visitors must log in or create a customer account before applying

**Recommendation:** Enable guest registration to reduce friction. You can always require approval to vet affiliates before activating them.

### Require Approval

**Field:** `require_approval` (Boolean)

- **Checked** — New affiliates must wait for manual approval before accessing their dashboard
- **Unchecked** — New affiliates are auto-approved and can create links immediately

**Recommendation:** Enable manual approval if you want to vet affiliates for brand fit, fraud prevention, or exclusive programs.

### Terms & Conditions URL

**Field:** `terms_url` (URL)

Optional link to your affiliate program terms and conditions. If provided, the registration form displays a checkbox requiring affiliates to agree to your terms before signing up.

**Example:** `/pages/affiliate-terms/`

### Welcome Message

**Field:** `welcome_message` (Text)

Message displayed to affiliates immediately after successful registration. Use this to:

- Thank them for joining
- Explain next steps (e.g., "We'll review your application within 24 hours")
- Link to getting started resources

**Example:**
```
Welcome to our affiliate program! We've received your application and will review it within 24 hours. Check your email for approval confirmation and login instructions.
```

## Multi-Language Support

All text fields in Affiliate Settings are **translatable** using Spwig's translation widget:

- Hero Title
- Hero Subtitle
- Features (JSON translated per language)
- How It Works steps (JSON translated per language)
- CTA Title
- CTA Description
- Welcome Message

### How Translation Works

When you edit a translatable field, you'll see a translation widget that lets you provide content for each enabled language. For JSON fields (features, steps), you provide separate JSON objects per language:

**English:**
```json
[
  {"icon": "fa-dollar-sign", "title": "Competitive Commissions", "description": "Earn up to 15% on every sale"}
]
```

**Spanish:**
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones Competitivas", "description": "Gana hasta el 15% en cada venta"}
]
```

The portal automatically displays the correct language version based on the visitor's language preference.

## Preview Your Changes

After customizing the portal settings:

1. **Save** your changes in the admin
2. Visit `/affiliate/` on your store's frontend (open in a new tab)
3. **Test the registration flow** by clicking "Become an Affiliate"
4. **Verify branding consistency** — does the portal match your store's design and messaging?

You can make iterative changes and refresh the page to see updates immediately.

## Example Customizations

### Scenario 1: E-Commerce Fashion Store

**Goal:** Recruit fashion influencers and bloggers.

| Setting | Value |
|---------|-------|
| Hero Title | "Promote Styles You Love & Earn" |
| Hero Subtitle | "Join 1,200+ influencers earning 12% commissions on every sale" |
| Feature 1 | Icon: `fa-tshirt`, Title: "Curated Fashion Collections", Description: "Promote premium apparel and accessories" |
| Feature 2 | Icon: `fa-percentage`, Title: "12% Commission", Description: "Industry-leading rates on all products" |
| Feature 3 | Icon: `fa-camera`, Title: "Exclusive Content", Description: "Access product photos, videos, and campaign assets" |
| Allow Guest Registration | Checked |
| Require Approval | Checked (manual review for brand fit) |

### Scenario 2: B2B SaaS Partner Program

**Goal:** Recruit business consultants and agencies for enterprise software referrals.

| Setting | Value |
|---------|-------|
| Hero Title | "Partner With Us to Grow Revenue" |
| Hero Subtitle | "Earn $500 per enterprise referral through our B2B partner program" |
| Feature 1 | Icon: `fa-handshake`, Title: "$500 Per Referral", Description: "Fixed commission for qualified enterprise leads" |
| Feature 2 | Icon: `fa-clock`, Title: "180-Day Cookie", Description: "Long attribution window for complex sales cycles" |
| Feature 3 | Icon: `fa-user-tie`, Title: "Dedicated Partner Manager", Description: "White-glove support for your clients" |
| Allow Guest Registration | Unchecked (B2B requires account) |
| Require Approval | Checked (invite-only program) |
| Terms URL | `/pages/partner-program-terms/` |

## Tips

- Customize your **hero title** to focus on benefits, not features — "Earn While You Sleep" is more compelling than "Affiliate Program Sign-Up"
- Use **social proof** in the subtitle (e.g., "Join 500+ affiliates") to build trust and credibility
- Choose **FontAwesome icons** that visually reinforce each benefit — the icon should instantly communicate the value
- Keep feature descriptions to **1-2 sentences** — the portal is about conversion, not exhaustive explanation
- Test the **registration flow** yourself before promoting the portal — catch friction points like confusing form fields or broken links
- Enable **guest registration** to reduce sign-up friction, then use **require approval** to vet affiliates after they've submitted
- Use the **welcome message** to set expectations (approval timeline, next steps, support contact) and reduce support inquiries
- Update the portal **seasonally** to align with campaigns — highlight special commission promotions or product launches
