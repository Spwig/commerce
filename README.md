<p align="center">
  <strong>English</strong> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <a href="README.pt.md">Português</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.hi.md">हिन्दी</a> |
  <a href="README.id.md">Bahasa Indonesia</a> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.tr.md">Türkçe</a> |
  <a href="README.vi.md">Tiếng Việt</a> |
  <a href="README.th.md">ไทย</a>
</p>

<p align="center">
  <img src="https://spwig.com/images/logo.svg" alt="Spwig" width="200">
</p>

<h1 align="center">Spwig</h1>

<p align="center">
  <strong>Self-hosted e-commerce for merchants who want to own their store.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">Website</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">Documentation</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">Community</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/en/marketplace">Marketplace</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/en/demos">Live Demos</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## What is Spwig?

Spwig is a full-featured e-commerce platform: catalogue, cart, checkout,
orders, customers, payments, shipping, themes, page builder, admin API,
POS, subscriptions, loyalty, blog, SEO — the whole stack. Built with
**Django 5**, **PostgreSQL**, and **Redis**, ships as a set of Docker
containers, runs on a $5 VPS or on your own metal.

Unlike hosted platforms, **you own the code, the database, and the
customer data.** No per-transaction fees. No lock-in. If you want to
fork it and go your own way, the licence explicitly permits that.

<br />

## Editions

Same binary. A signed licence file toggles feature flags at runtime.
Community is what you get by default when you `docker compose up`;
upgrading is a key you paste into the admin.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| Full e-commerce platform (storefront, admin, checkout, orders) | ✓ | ✓ | ✓ |
| Point-of-sale terminal, page builder, themes | ✓ | ✓ | ✓ |
| Bring-your-own payment + shipping providers | ✓ | ✓ | ✓ |
| Marketplace access (premium themes + integrations) | ✓ | ✓ | ✓ |
| Spwig-hosted address autocomplete | Free · rate-limited | Higher limit | Highest limit |
| Spwig-hosted GeoIP (visitor location) | Free · rate-limited | Higher limit | Highest limit |
| Push notifications (iOS admin app) | Free · rate-limited | Higher limit | Highest limit |
| Hosted email gateway with warm IPs + DKIM | – | ✓ | ✓ |
| Priority support | – | ✓ | ✓ |
| Enterprise SSO (Azure AD, Okta) | – | – | ✓ |

<br />

## Quick start

### Option 1 — One-line install (recommended)

The [Spwig installer](https://github.com/Spwig/spwig) sets everything up
in one command: Docker, PostgreSQL, Redis, MinIO, TLS via Cloudflare or
self-signed, first-boot wizard, admin user. Signed images pulled from
`registry.spwig.com`.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

Upgrades happen through the admin — see [UPGRADING.md](UPGRADING.md).

### Option 2 — From source

You want to build from this repo, hack on it, or ship a fork:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

Storefront on `http://localhost`, admin on `http://localhost/en/admin/`.
Community edition auto-activates on first boot — no licence server
round-trip, no key required. Upgrade later with `git pull` and
`docker compose build`.

<br />

## Features

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Storefront & checkout</h3>
      <p>Server-rendered by default — fast time-to-first-byte, works
      without JavaScript, mobile-first (80% of traffic is small
      screens). Optional headless mode via the
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> and <a href="https://github.com/Spwig/react">React
      components</a>.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/storefront-product.webp" alt="Storefront product page">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/page-builder.webp" alt="Page builder">
    </td>
    <td width="50%" valign="top">
      <h3>Page builder</h3>
      <p>Merchants build storefront pages from reusable widgets — hero
      sections, product grids, testimonials, embeds — and preview live
      in the admin. Widgets install from the marketplace or from your
      own component repository.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Order & customer management</h3>
      <p>Every order, refund, subscription renewal, digital download,
      and customer touchpoint in one place. Bulk operations,
      permission-scoped staff roles, exportable to CSV/XLSX, mobile
      admin app (iOS) with push notifications.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/order-management.webp" alt="Order management">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/branding-builder.webp" alt="Branding builder">
    </td>
    <td width="50%" valign="top">
      <h3>Themes & branding</h3>
      <p>Design tokens (colours, typography, spacing) drive every
      surface — storefront and admin. Change a token, everything
      updates. Themes live in
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      and install through the marketplace; write your own with the
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a>.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Point of sale</h3>
      <p>Full POS terminal for brick-and-mortar merchants: barcode
      scanning, split payments, receipt printing, cash drawer
      integration, customer-facing display, offline mode. Included
      in every edition — no upgrade required.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/pos-terminal.webp" alt="POS terminal">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/developer-portal.webp" alt="Developer portal">
    </td>
    <td width="50%" valign="top">
      <h3>Provider ecosystem</h3>
      <p>Anything that talks to an external system — payments,
      shipping, exchange rates, translation, GeoIP, SMS, email — is a
      pluggable provider. Build your own with the
      <a href="https://github.com/Spwig/provider-sdks">provider SDKs</a>,
      publish to the marketplace, or self-host a private registry.</p>
    </td>
  </tr>
</table>

<br />

## Architecture

- **Single-tenant.** Each install is one store, one merchant, one
  Django Site. Multi-store merchants run one Spwig install per store.
- **Modular monolith.** Not a microservice mesh. A single Django
  process handles storefront + admin + REST API + Celery workers.
  Simple to deploy, reason about, and fork.
- **Runtime feature gates.** Community/Pro/Enterprise all run the
  same binary. A signed licence toggles flags — no code stripping.

Full tour: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## Community & support

- **Discussions.** Open-ended questions, ideas, show-and-tell:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **Community forum.** [community.spwig.com](https://community.spwig.com)
  — long-form threads, best-practice recipes, extension showcases.
- **Bug reports.** [Issues](https://github.com/Spwig/commerce/issues)
  with reproduction steps. See [SECURITY.md](SECURITY.md) for
  vulnerability disclosure.
- **Commercial support.** Available for Pro and Enterprise licences.

<br />

## Contributing

We use **DCO** (Developer Certificate of Origin) — every commit is
signed off with `git commit -s`. No paperwork, no CLA. Full guide in
[CONTRIBUTING.md](CONTRIBUTING.md).

Notes for AI coding assistants working on the repo are in
[CLAUDE.md](CLAUDE.md).

<br />

## Ecosystem

Related open-source projects under the [Spwig org](https://github.com/Spwig):

| Repo | What it is |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | This repo — the core platform (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | One-line installer |
| [Spwig/components](https://github.com/Spwig/components) | Themes, integrations, and utilities (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK for building themes (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | SDKs for building payment / shipping / etc. providers (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | Headless / API client SDK (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | React component library (Apache-2.0) |

<br />

## Licence

Spwig is [AGPL-3.0-or-later](LICENSE). You can run it, modify it,
distribute it, offer it as a hosted service — all permitted. Modified
versions offered over a network must make their source available to
their users. That's the whole point of AGPL over GPL.

Provider integrations built with the SDKs are Apache-2.0, so building a
proprietary payment / shipping / SMS integration on top of the SDKs
does not trigger AGPL. This is intentional — we want a thriving
provider ecosystem.

<br />

## Privacy & telemetry

Spwig sends one anonymous ping per day to `updates.spwig.com/api/v1/telemetry/`:

- Install UUID (generated on first boot, stored locally)
- Spwig version
- Edition (community / pro / enterprise / trial / dev)
- Country (resolved from IP at ingress; the IP itself is not stored)
- Bucket counts of feature flags (payment providers configured, themes
  installed) — never raw customer or order data

**Opt out** with `SPWIG_TELEMETRY=0` in your environment. That flips
`settings.SPWIG_TELEMETRY_ENABLED` and the daily beat task no-ops.

<br />

<p align="center">
  <sub>
    Built with care in Singapore.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">community</a>
  </sub>
</p>
