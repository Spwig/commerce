# Architecture

This document is a tour of how Spwig is put together — for contributors,
integrators, and anyone deciding whether the platform fits their use case.

## High-level

- **Django 5 modular monolith.** Not a microservice mesh. A single Django
  process handles storefront + admin + REST API + Celery tasks. Simple to
  deploy, simple to reason about, simple to fork.
- **Single-tenant per install.** Every deployment is one store with one
  Django `Site`. Multi-store or multi-tenant scenarios run one Spwig
  installation each. See [Single-tenant model](#single-tenant-model) below.
- **PostgreSQL + Redis + optional MinIO/S3.** Standard stack — no exotic
  dependencies. Django 5, gunicorn/uvicorn, Celery + Celery Beat.
- **Docker-first.** Ships as a set of containers with `docker compose`. Bare
  metal works too; nothing container-specific in the code.
- **Provider-driven.** Anything that touches an external system (payments,
  shipping, exchange rates, translation, GeoIP, geocoding, push, SEO)
  is a pluggable provider component installed from a marketplace.
- **Editions gated at runtime, not at build time.** Community and Pro run
  the same binary; a signed licence file switches feature flags.

## Directory layout

```
core/                 Licence, activation, telemetry, hosted-service clients, admin theme
accounts/             Customer + staff accounts, MFA, OAuth, roles
catalog/              Products, variants, categories, inventory
cart/                 Session cart, checkout, discounts
orders/               Order lifecycle, refunds, digital downloads
payment_providers/    Provider registry + provider apps (installed via marketplace)
payout_providers/     Provider registry for outgoing payments (PayPal, Wise, ...)
shipping/             Provider registry + shipping rate quoting
design/               Themes, tokens, page builder, storefront rendering
page_builder/         Page + section models used by design
element_builder/      Widget system used by page builder
admin_api/            REST API used by mobile admin app
email_system/         Templates, sending backends, providers
sms_system/           SMS providers (Twilio, ...)
translations/         AI translation service integration
exchange_rates/       Multi-currency + exchange-rate providers
geoip/                Visitor location resolution (pluggable providers)
address_autocomplete/ Address autocomplete during checkout
subscriptions/        Recurring products
loyalty/              Points, tiers, rewards
vouchers/             Discount codes + gift cards
affiliate/            Referral tracking, commissions
blog/                 Storefront blog with SEO
seo_generator/        AI-assisted SEO copy
webhooks/             Outbound webhooks
component_updates/    Marketplace client (talks to updates.spwig.com)
license_checkout/     Paid-tier activation flow
marketplace_checkout/ Paid-component checkout flow
pos_app/              POS terminal SPA (Community: upgrade CTA)
pos_api/              POS REST API
developer_portal/     Portal for component authors
migration/            One-shot imports from Shopify, WooCommerce, ...
help_content/         Merchant-facing help articles
staff_roles/          Granular admin permissions
enterprise_sso/       Azure AD / Okta / SAML (Enterprise-only)
setup_wizard/         First-boot wizard
management/           Analytics + dashboard views
domain_ssl/           Domain + SSL cert management
```

Standard Django apps you'd expect (templates/, static/, tests/, locale/, etc.)
sit alongside.

## Single-tenant model

Each Spwig installation is **one store, one merchant, one Django Site**.

- `SITE_ID = 1` is hard-coded. There is no multi-site UI.
- Django's Sites framework is present because `django-allauth` requires it,
  not because we use it for multi-tenancy.
- Multi-store merchants run one Spwig install per store. The **hosted
  fleet** at `*.myspwig.com` orchestrates thousands of these; the OSS
  release does not include that orchestration layer.

Why single-tenant: simpler mental model, simpler queries, simpler backups,
no cross-tenant data leaks. The trade-off is you can't run 10 stores in one
process. We think this is the right trade for the merchant persona.

## Provider system

Anything that talks to an external system is a **provider component**. Each
provider is a Django app with a `manifest.json`, an entry-point class, and
config surfaced in the admin.

```
components/integrations/payments/stripe/
├── manifest.json          # slug, version, capabilities, config schema
├── provider.py            # class StripeProvider(PaymentProviderBase)
├── setup_instructions.html # rendered in admin during setup
├── requirements.txt       # provider-specific Python deps
├── checkout-handler.js    # storefront-side hook (Stripe.js)
└── logo.svg
```

Providers install into `components_data/` via the marketplace client, which
downloads signed component packages from
[`updates.spwig.com`](https://updates.spwig.com) (the update server). Once
installed, provider config lives in the DB per-installation.

**Building your own provider:** start with one of the SDKs at
[`Spwig/provider-sdks`](https://github.com/Spwig/provider-sdks). Each SDK is
a small framework + working example for a specific provider type (payment,
shipping, SMS, terminal, etc.).

## Hosted services

Some capabilities are optionally backed by Spwig-hosted infrastructure:

| Service | Host | Community access |
|---|---|---|
| Marketplace + component downloads | `updates.spwig.com` | Yes |
| Anonymous deployment telemetry sink | `updates.spwig.com/api/v1/telemetry/` | Yes (opt-out via `SPWIG_TELEMETRY=0`) |
| GeoIP (visitor country + ASN) | `geoip.spwig.com` | Free tier · rate limited |
| Address autocomplete | `geocoder.spwig.com` | Free tier · rate limited |
| Push notifications (iOS admin app) | `push.spwig.com` | Free tier · rate limited |
| SSO broker (community forum login) | `sso.spwig.com` | Yes |
| Hosted email gateway (warm IP, DKIM) | `mail-gw.spwig.com` | Paid only |

**Community tier limits** are enforced at the service ingress. When a
Community install exceeds its quota, the service returns HTTP 429 with an
`upgrade_url` in the body. The client caches the "over limit" state locally
(`Retry-After` seconds) so it doesn't hammer the server, and the admin shows
a usage tile + 80% banner + optional 90% email once per month.

Configuration is centralised on the update server at
`GET /api/v1/tiers/` — hosted services poll every 5 minutes and hot-reload
their limits without redeployment.

## Licence & activation

- **On first boot**, `core.apps:CoreConfig.ready()` runs a one-shot
  bootstrap that ensures a Community licence exists at
  `settings.LICENSE_PATH`. The Community licence is a signed JSON blob
  shipped in the repo at `core/data/community_licence.json` (verified
  against `core/keys/license-public-key.pem`).
- Paid installs run the same activation flow as before — a setup token
  swapped for a signed licence via `updates.spwig.com`.
- **`ActivationMiddleware`** stops being a blocker under Community (the
  file exists → middleware becomes a no-op).
- Community licence has `entitlements.pos_module: false` → POS admin views
  render the upgrade CTA instead of the terminal UI. Runtime check only —
  the POS code isn't stripped from the repo.

## Telemetry

`core/telemetry/` handles a small daily ping to
`updates.spwig.com/api/v1/telemetry/`. Payload:

- Install UUID (`UpdateServerConfig.installation_uuid`, stored locally)
- Spwig version (`core.__version__`)
- Edition (`community` / `pro` / `enterprise` / `trial` / `dev`)
- Country (resolved from IP at ingress, IP is not stored)
- Active feature flags (payment providers configured, themes installed —
  bucket counts, never raw customer/order numbers)

Opt out with `SPWIG_TELEMETRY=0` — that flips `settings.SPWIG_TELEMETRY_ENABLED`
and the daily beat task exits early. The `README` privacy section spells
this out for merchants.

## Storefront rendering

- **Server-side rendering by default.** Django templates + design tokens
  + theme-provided CSS. Fast time-to-first-byte, works without JavaScript.
- **Themes** live in `Spwig/components` and install via the marketplace.
  A theme is a directory of tokens (`tokens.json`), Django templates, CSS
  (generated from tokens + hand-written overrides), and a manifest.
- **Page builder** in `page_builder/` + `element_builder/` — merchants
  build pages from reusable widgets and preview live in the admin.
- **Headless option.** The [`Spwig/headless-sdk`](https://github.com/Spwig/headless-sdk)
  fronts the storefront via API. React consumers get the
  [`Spwig/react`](https://github.com/Spwig/react) hooks + components package.
  The Cocos Botanica reference storefront (Next.js 16) is one example.

## Admin

- Django admin with a heavy custom skin (`core/static/core/admin/css/*`).
- Custom sidebar with per-role visibility.
- Dashboard renders analytics + a hosted-services usage tile (Community).
- License-status banner + hosted-services 80% banner ride in the same
  context processor (`core/context_processors.py:license_status`).
- **Mobile admin app** communicates via `admin_api/` — full REST with JWT
  auth, push notifications go through `push.spwig.com`.

## Marketplace & update server

- **`component_updates/`** is the client. Talks to `updates.spwig.com`.
- Components install as packaged directories under `components_data/`.
- Version pinning + signature verification handled server-side; the client
  verifies against a public key shipped in `core/keys/`.
- Removing the marketplace client is possible but leaves you without an
  easy way to install themes and integrations. Point `UPGRADE_SERVER_URL`
  at your own registry if you want to self-host the marketplace.

## Testing

- `tests/` — top-level integration + community-edition tests
- App-level tests live inside each app (`accounts/tests/`, `catalog/tests/`, ...)
- Django's test runner works; `pytest` also works with the config in
  `pyproject.toml`
- CI runs the full suite on every PR + push to `main`

## Deployment

- **Development:** `docker compose -f docker-compose.dev.yml up`
- **Production:** the [`Spwig/spwig` installer](https://github.com/Spwig/spwig)
  wraps `docker-compose.production.yml` with a one-line install script that
  handles Docker, SSL (Let's Encrypt via Cloudflare or self-signed), admin
  user, database migrations, and a first-boot wizard.
- **Env vars:** `.env.example` is the source of truth. All configuration
  is environment-driven. No hard-coded secrets in the repo.

## Distribution model

Spwig ships in **two artefact forms**, both AGPL-3.0-or-later, both fully
functional:

| Form | Where it comes from | What's in it | Who runs it |
|---|---|---|---|
| **Source-form** | This repo (`Spwig/commerce`) | Pure Python source, no compilation | Anyone who clones + builds from source, self-hosters, contributors, forks |
| **Signed release** | `updates.spwig.com` (paid tier) and the Spwig-hosted fleet | Same code, plus Cython-compiled `.so` for `auth` / `licensing` / `payments`, `.pyc` bytecode everywhere else, and a signed `.integrity_manifest.json` verified at boot | Paying merchants who pull our Docker images; the `*.myspwig.com` hosted fleet |

**Both forms run the same feature set.** Editions are gated at runtime
by the signed licence file, not at build time. A source-form build with
a paid licence unlocks Pro/Enterprise features exactly like the signed
release does.

**Why the signed release exists:** it's a hardened distribution for
commercial customers — mildly harder to tamper with, and the integrity
manifest lets us detect casual on-disk modification. It is *not* DRM.
Per AGPL §3, we cannot and do not use anti-circumvention laws (DMCA
§1201 and analogues) against anyone who bypasses the integrity check.
If you fork this repo and patch out the licence check, that's fine —
AGPL allows it. You just can't call the result "Spwig" or use our
trademarks.

**Why the source form is first-class:** because AGPL demands it, and
because open-source projects that ship only-obfuscated binaries alongside
their repo signal distrust of their own community. Every one of our own
CI jobs, the reference `docker-compose.dev.yml`, and the contributor
workflow runs against source form. If a change breaks the signed-release
build we fix the build, not the source.

**Practical consequences for contributors:**
- Everything in the `deploy/code_protection/` directory of our private
  build tree is out of scope for `Spwig/commerce` — you will never see
  it in this repo, and you never need it to develop or run Spwig.
- Bug reports for the signed release are welcome, but a repro against
  `docker compose -f docker-compose.dev.yml up` is much faster to
  triage. Reproduce from source when you can.
- The `sync-to-open.sh` script that mirrors our internal working tree
  to `Spwig/commerce` explicitly blocklists the build-protection
  tooling, so it can't accidentally leak.

## Non-goals

- **Multi-tenant** in one process — see [Single-tenant model](#single-tenant-model).
- **A JavaScript SPA admin** — the admin is server-rendered Django.
  Individual pages get JS enhancements; the whole thing is not a React app.
- **Reinventing payment SDKs** — we integrate the vendor SDK (Stripe, Adyen,
  PayPal), we don't wrap it.
- **A component marketplace clone** — the marketplace client is intentionally
  minimal so anyone can point it at their own registry.
- **A hosted panel like Vercel/Netlify** — that's what
  [`*.myspwig.com`](https://myspwig.com) is, and it's not open source.
  The OSS release is for merchants who want to self-host.

## Where to go next

- [CONTRIBUTING.md](CONTRIBUTING.md) — dev setup, PR conventions
- [SECURITY.md](SECURITY.md) — vulnerability disclosure policy
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — community standards
- [docs.spwig.com](https://docs.spwig.com) — merchant-facing docs
