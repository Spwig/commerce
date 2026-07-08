# CLAUDE.md

Notes for Claude Code (and any other AI coding assistant) working on this
repo. Human contributors should read [CONTRIBUTING.md](CONTRIBUTING.md) and
[ARCHITECTURE.md](ARCHITECTURE.md) first — this file assumes you've
skimmed both.

Every rule below is a non-negotiable constraint. Read the section that
matches your change before you write code.

---

## What Spwig is

Self-hosted e-commerce platform. Django 5, PostgreSQL, Redis, Docker.
AGPL-3.0-or-later. Every solution should be built with ease of use,
modern aesthetics, and speed, with the merchant and their customers at
the centre of focus.

**Branding rule.** Spwig merchants and their customers don't know about
Django. When you write documentation, error messages, admin copy, or any
merchant/customer-facing text, use "Spwig" instead of naming the
underlying framework.

## Terminology

- **Merchant** — the store owner/admin who runs a Spwig install.
- **Community / Pro / Enterprise** — runtime editions gated by a signed
  licence file. Community is the default when the platform
  auto-bootstraps a licence.
- **Provider** — a pluggable component that integrates an external
  system (payments, shipping, exchange rates, translation, GeoIP, SMS,
  email). Lives in [Spwig/components](https://github.com/Spwig/components).
- **Marketplace / update server** — `updates.spwig.com`; where
  components are published and where anonymous telemetry pings go.
  Client code lives in `component_updates/`.

---

## Architecture: single-tenant by design

Each Spwig installation is **one store, one merchant, one Django Site**.

- `SITE_ID = 1` is hard-coded. There is no multi-site UI.
- Django's Sites framework exists because `django-allauth` needs it —
  not because we use it for multi-tenancy.
- The Sites admin is unregistered in `core/admin.py` so merchants
  can't create additional sites.
- All code assumes `Site.objects.get(pk=1)`.
- Multi-store merchants run one Spwig install per store.
- **Do NOT implement multi-site / multi-tenant features.**

Models with Site foreign keys (`EmailAccount`, `EmailTemplate`,
`EmailOutbox`, `ExchangeRateProviderAccount`) always use Site ID=1.

More background: [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Editions & licence bootstrap

- `core.apps:CoreConfig.ready()` bootstraps a signed **Community**
  licence at `settings.LICENSE_PATH` on first boot. Template lives at
  `core/data/community_licence.json`.
- `ActivationMiddleware` becomes a no-op once any valid licence file
  exists — Community installs never see an `/activate/` redirect loop.
- Feature-gating is **runtime**, not build-time.
  `LicenseManager.is_community()` /
  `is_hosted_service_available('geoip')` are the gates.
  Don't strip Pro-only code from the OSS build — keep it and gate.
- **POS module.** `pos_app/` and `pos_api/` ship in the repo but the
  admin surface renders an upgrade CTA under Community. See
  `pos_app/community_gate.py`.

### When something is Pro-only

Two gating patterns:

1. **`LicenseManager.is_community()`** — early-returns a "requires paid
   tier" response.
2. **`is_hosted_service_available('service_name')`** — Community can
   use `geoip` / `geocoder` / `push` (rate-limited by the hosted
   service); only `mail_gateway` is Pro-only.

Prefer #2 when adding features that consume Spwig-hosted infrastructure.

---

## URL structure and routing

Decide before touching URLs: does the endpoint belong **inside**
`i18n_patterns` (localised URLs, `/en/...`) or **outside** (APIs and
webhooks, no language prefix)?

### Hierarchy

- **Non-i18n group** (no language prefix) lives outside `i18n_patterns`
  in `core/urls.py`. Use for APIs (`/api/...`), webhooks
  (`/webhooks/...`), health endpoints, and dev static/media helpers.
- **i18n group** (language prefix) lives inside `i18n_patterns`. Use for
  Django admin (`/en/admin/` etc.), admin sub-apps, all localised user
  pages.

```python
# non-i18n
path('api/set-currency/', set_currency, name='set_currency')

# i18n
urlpatterns += i18n_patterns(
    path('admin/loyalty/', include('loyalty.urls')),
    path('admin/', admin.site.urls),
)
```

### Conventions

- Admin apps live under `/admin/...` (e.g. `/en/admin/shipping/providers/`).
- APIs live under `/api/...` with no language prefix (e.g. `/api/cart/add/`).
- Use `include()` at a common prefix so the app-level `urls.py` inherits
  the prefix.

### JavaScript URL building

- Admin URLs: derive the language from
  `document.documentElement.lang` or call `AdminUtils.buildAdminUrl(path)`.
- API URLs: call directly with no `/lang/` prefix.

```javascript
const lang = document.documentElement.lang || 'en';
const adminUrl = `/${lang}/admin/loyalty/members/filter/`;
const apiUrl = '/api/set-currency/';
```

### Anti-patterns

- `/loyalty/...` without `/admin/` → 404.
- `/en/api/...` → 404. APIs never carry a language prefix.

---

## Translations — three distinct systems

Do not conflate them.

### 1. Admin interface i18n (`{% trans %}` / `gettext`)

- Standard Django i18n; strings extracted with `makemessages` into
  `.po` files.
- Admin-facing strings only (sidebar, admin forms, admin buttons).
- **Do NOT manually translate `.po` files.** Extract only; translation
  is handled by the platform translation system.
- Supported admin languages: `en`, `es`, `fr`, `de`, `ja`, `pt`,
  `zh-hans`, `zh-hant`, `ru`, `ar`, `hi`, `id`, `ko`, `tr`, `vi`,
  `it`, `th`.
- Wrap user-facing strings: `{% trans %}`, `{% blocktrans %}`, `_()`.
  Add context when ambiguous: `{% trans "Order" context "noun" %}`.
- Translation keys must be descriptive — no `btn_1`.

### 2. Merchant content translation (JSONField)

AI translations for **merchant-authored content** (products, pages,
SEO). Runs on the merchant's host.

- Data lives in a `translations = models.JSONField(default=dict)` on
  the model. Never use a different storage pattern.
- Payload shape:
  ```json
  {
    "es": {
      "title": "Mi título",
      "description": "Descripción",
      "_meta": {"auto": true, "verified": false, "translated_at": "..."}
    }
  }
  ```
- Wire the admin with `TranslatableFieldWidget` in the form and
  `TranslatableAdminMixin` in the ModelAdmin. Declare
  `translatable_fields`. Load `Media.js` / `Media.css`.
- In custom change-form templates, include
  `translation_editor_assets.html` in `extrahead` and
  `translation_editor_init.html` inside `field_sets`.
- API lives at `/api/translation/...` (`status/`, `translate/`, `save/`,
  `languages/`, `health/`). `model_type` is `app_label.model_name`.
- Multi-sentence text is auto-split, batch-translated, reconstructed —
  no manual work.
- Reference implementations: `catalog.Product`, `page_builder`,
  `core.SiteSettings`.
- **Don't**: use `modeltranslation`, create `name_en` columns,
  hardcode language lists, ship a custom UI, or mix admin i18n with
  this system.

### 3. Storefront UI chrome (`{% mtrans %}`)

Merchant overrides for **static storefront UI strings** (cart,
checkout, product buttons, headers). Distinct from admin i18n and from
merchant content translation.

**When to use which:**
- Customer sees it → `{% mtrans %}` (with `{% trans %}` fallback).
- Only the admin sees it → `{% trans %}`.

**Adding a new storefront string:**

1. Register in `translations/ui_string_registry.py` under the right
   section (`common`, `cart`, `checkout`, `product`, `account`,
   `search`, `js`, etc.). Keys are `section.snake_case`
   (`cart.shopping_cart`, `product.add_to_cart`).
2. Use in template:
   ```django
   {% load i18n static merchant_trans %}
   <button>{% mtrans 'Add to Cart' %}</button>
   ```
   The tag argument must **exactly match** the registered English value.
3. JavaScript strings register under `js.*` and are accessed as
   `window.UI_STRINGS['js.product_added']`.
4. Run `./manage.py sync_ui_string_registry` after adding keys.

**Anti-patterns:**
- `{% mtrans %}` in admin templates.
- Adding storefront strings without registering them.
- Dynamic/variable arguments to `{% mtrans %}` — literals only.
- Forgetting `{% load merchant_trans %}`.

---

## Static files & CSS discipline

### Static files

- Always `{% load static %}` and reference assets via `{% static '...' %}`.
- Organise as `app/static/app/{css,js,images}/`.
- Never hardcode `/static/...` paths.
- **Never edit anything under `staticfiles/`** — that directory is
  populated by `collectstatic` from the app-level source directories.
  Edit the source, then run
  `./manage.py collectstatic --noinput`.

### Copyright headers

Every new CSS and JS source file should begin with:

```
/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
```

Do NOT add this header to:
- Third-party / vendor files (`*.min.js`, `*.min.css`, anything under
  `core/static/core/js/vendor/`).
- Files under `staticfiles/` (edit the source).
- Files under `components/themes/*/tokens.css` — generated by
  `design.services.token_css_generator`; the generator applies the
  header automatically.

### Admin theme files

- Edit `core/static/core/admin/css/themes/{light.css,dark.css}` in
  development, then `collectstatic`.
- Update both light and dark variants when a shared style changes.
- Theme files store variables; concrete CSS classes belong in
  app-scoped styles.

### CSS best practices

- **CSP-safe.** No inline `<style>` tags. No inline `style=""`
  attributes. Everything in external CSS via `<link rel="stylesheet">`.
  Dynamic values ride on `data-*` attributes + CSS custom properties.
  See [CSP hardening](#security--csp-hardening) below.
- **Mobile first.** ~80% of storefront traffic is mobile. Write
  responsive CSS with a mobile-first mindset — this applies to both
  storefront and admin.
- Scope app CSS: `.product-form-container .form-row { ... }` — never
  ship unscoped selectors from an app.

### Admin form styling — three tiers

1. **Django defaults** (`staticfiles/admin/css/forms.css`) — never
   modify.
2. **Global admin overrides** (`core/static/core/admin/css/admin-base.css`)
   — single source for shared spacing, inputs, labels, `.required`,
   `.help`.
3. **App overrides** (`app/static/app/css/*.css`) — must be scoped
   (e.g. `.product-form-container .form-row {...}`).

**Cascade:** `forms.css` → `admin-base.css` → scoped app CSS.

**Decision:** shared style → tier 2; page-specific → tier 3.
Don't duplicate tier 2 rules in app CSS.

### Vendor scripts

- Third-party JS libs go in `core/static/core/js/vendor/`.
- Never load from CDNs — serve locally for CSP compliance.

---

## Admin theme integration for app templates

- Read the `admin_theme` context variable (from
  `core.context_processors.admin_theme`) and attach to
  `<body data-theme="{{ admin_theme|default:'light' }}">`.
- In JS: `const currentTheme = '{{ admin_theme|default:"light" }}';`.
- Never build client-side theme state (no cookies / localStorage). Only
  react to `admin-theme-changed` events emitted by the core.
- Isolate canvases/previews (Page Builder etc.) so they don't inherit
  admin theme colours.

---

## Admin sidebar policy

- Sidebar lives exclusively in `templates/admin/base_site.html`. Extend
  Django admin templates so they inherit.
- Any navigation change happens there.
- Structure menu groups logically; use Font Awesome icons; build URLs
  with `{% url %}` and honour language prefixes (`/en/...`).
- Follow the existing collapsible pattern — icons + labels are
  mandatory for consistency.

## Admin page titles

Set `<title>` to `[Page purpose] | [default site URL from Site Settings] | Spwig`.
Example: `Members | example.com | Spwig`.

```django
{% block title %}
  {% trans "Members" %} | {{ site_title|default:_('Site Admin') }} | Spwig
{% endblock %}
```

## Site Settings admin

- Admin class: `SiteSettingsAdmin` in `core/admin.py`.
- Template: `core/templates/admin/core/sitesettings/change_form.html`
  (tabs: General, Contact, Currency & Locale, Images, E-Commerce,
  Shipping, Payments, Authentication, SEO, Advanced).
- Styles: `core/static/core/admin/css/site_settings.css`
  (uses `.two-column-layout` + responsive breakpoints).
- After CSS tweaks: run `./manage.py collectstatic --noinput`.

---

## List views and change lists

### List row cards

Card-based layout (`admin-base.css` supplies the styles) when tables
are limiting or when metadata/badges improve scanning. Skip cards for
simple 2–3 column tables.

- Structure: checkbox, icon/avatar, content (title/subtitle/meta/badges/stats),
  action buttons.
- Badge variants: default, `.primary`, `.success`, `.warning`, `.error`.
- Card states: `.selected`, `.disabled`.
- Icon-only actions: use `admin-base.css` utility classes.
- Responsive: horizontal on desktop, stacked <768px, ellipsis for long
  text.

### Filters panel

Always place filters above the list. Use AJAX (no page reload). Good
when there are ≥ 2 filterable fields.

**ALWAYS use `admin-list-filters.js`.** Do not write bespoke filter JS.

Three components — all three must be present:

1. Load in `{% block extrahead %}`:
   ```django
   <link rel="stylesheet" href="{% static 'app/css/custom.css' %}">
   <script src="{% static 'core/admin/js/admin-list-filters.js' %}" defer></script>
   ```
2. Buttons use `data-action` attributes, **never** `onclick`:
   ```html
   <button data-action="toggle-filters">…</button>
   <button data-action="apply-filters">Apply</button>
   <button data-action="clear-filters">Clear</button>
   ```
3. Initialise inside `{% block content %}`:
   ```javascript
   const lang = document.documentElement.lang || 'en';
   window.AdminListFilters.init({
     url: `/${lang}/admin/app/model/filter/`,
     resultsContainer: 'item-results',
     resultsCount: 'item-count'
   });
   ```

**Anti-patterns:**
- `onclick` / `onchange` inline handlers — use `data-action`.
- Bespoke `toggleFilters()` / `applyFilters()` — the module already
  handles it.
- `{% block extrajs %}` — doesn't exist in Django admin; scripts are
  silently discarded.

Django view pattern:
- Verify `X-Requested-With: XMLHttpRequest`.
- Parse query params, filter queryset, render a partial with
  `render_to_string`.
- Return `JsonResponse({'html': ..., 'count': ...})`.

### Custom changelist pages

- Extend `admin/change_list.html`, `{% load i18n static admin_list %}`,
  override `{% block content %}`.
- Render dashboards / stats / cards **before** `{{ block.super }}` so
  filters/search/pagination still work.
- Provide extra context via `changelist_view` and `extra_context`.

### Action bars in card views

- **Do not override** `{% block object-tools %}`. Use
  `.change-list-header` and `.change-list-header-actions` (from
  `admin-base.css`) for a flex-based action bar with a heading and an
  Add button gated on `has_add_permission`.
- **No inline styles** — CSS classes in external files, using CSS
  variables for theme safety.

---

## Change forms with dashboard cards

- Extend `admin/change_form.html`, load `i18n static`, add dashboard
  CSS via **external file** in `extrastyle`, render cards above
  `{{ block.super }}` inside `{% if original %}`.
- Grid: `.dashboard-stats-grid` (`admin-base.css`) or custom grid with
  `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))`.
- Show cards **only when editing an existing object**. Keep inline
  forms collapsed, not removed.
- Cards summarise + surface quick actions. Reuse Font Awesome icons.
- **No inline `<style>` tags.** All CSS goes in external files
  (CSP). Use `{% block extrastyle %}` in change forms (not
  `extrahead`).

```django
{% extends "admin/change_form.html" %}
{% load i18n static %}

{% block extrastyle %}
{{ block.super }}
<link rel="stylesheet" href="{% static 'app/css/model_change_form.css' %}">
{% endblock %}

{% block content %}
{% if original %}
<div class="dashboard-stats-grid">
  <div class="dashboard-stat-card">
    <div class="icon"><i class="fas fa-coins"></i></div>
    <div class="value">{{ original.balance.available_points|floatformat:0 }}</div>
    <div class="label">{% trans "Available Points" %}</div>
  </div>
</div>
{% endif %}
{{ block.super }}
{% endblock %}
```

---

## Icons and tabs

- Prefer Font Awesome for UI. Use emojis only for
  merchant-generated content or rare celebratory cues.
- Tabs use the shared `.admin-tabs` / `.admin-tab-btn` components in
  `admin-base.css`. Switching is handled by `window.AdminTabs`
  (`admin-tabs.js`) — do not write bespoke tab JS.
- Preferred panel pattern: `.admin-tab-content` with `id="tab-{name}"`.

`AdminTabs` API:

- `AdminTabs.init({storageKey, onTabChange, persistHash})` — manual
  init.
- `AdminTabs.switchTo(tabName)` — programmatic switch.
- `AdminTabs.getActiveTab()` — current tab.
- `AdminTabs.addErrorBadge(tabName, count)` /
  `AdminTabs.clearErrorBadges()` / `AdminTabs.scanForErrors()`.

---

## JavaScript inside admin — `AdminUtils`

Auto-loaded globally as `window.AdminUtils`, file at
`core/static/core/admin/js/admin-utils.js`.

- Never hardcode language prefixes or maintain regex language lists.
- Never re-implement CSRF cookie lookup.

Helpers:

- `AdminUtils.getLanguagePrefix()` → `/en`, `/fr`, …
- `AdminUtils.buildAdminUrl(path)` — attaches the prefix.
- `AdminUtils.getCsrfToken()` — canonical CSRF lookup.
- `AdminUtils.buildFetchOptions(method, data, headers)` — standardised
  fetch config (JSON body + headers).

---

## Model standards

Every model needs:

- Translated `verbose_name` / `verbose_name_plural`.
- A meaningful `__str__`.
- `created_at` and `updated_at` fields.
- Relevant indexes on the fields your heavy queries hit.
- **Django Money fields** for every monetary value. The platform
  supports optional multi-currency — every currency value must use the
  shared money handling.

If a model supports admin deletions and fits the recycle-bin workflow,
integrate so deletions go through recycle bin, not hard deletes.

---

## Security & CSP hardening

- **Enforce CSRF everywhere.**
- Validate every user input rigorously — especially cart, checkout,
  payment operations.
- Respect Django permissions for all admin functionality.
- Sanitise product descriptions and every user-generated content
  surface.

### CSP: no inline JS / CSS

Content Security Policy blocks inline scripts and styles to prevent
XSS. This is critical for an e-commerce platform handling payments.

**JavaScript:**
- No inline `<script>` tags.
- No `onclick` / `onload` / other inline event handlers.
- Everything in external `.js` files loaded via `<script src="...">`.
- Bind events with `addEventListener` inside the external file.
- Pass data from Django templates to JS via `data-*` attributes.

**CSS:**
- No inline `<style>` tags.
- No `style=""` attributes.
- Everything in external `.css` files loaded via
  `<link rel="stylesheet">`.
- Apply styles via classes; use `data-*` + CSS custom properties for
  dynamic values.

The one grey area: templates that carry a data-driven value
(e.g. progress-bar width) may keep a minimal inline `style` on that
attribute only. Static styles go external.

---

## API standards

### Documentation stack

- Interactive docs (dev only): `/internal/api/docs/`.
- Production sets `ENABLE_API_DOCS=False`.
- `/internal/api/*` requires authentication.
- `drf-spectacular` lives in `requirements-dev.txt`.

### Building or changing an API

1. Review existing endpoints first.
2. Follow DRF standards: ViewSets for CRUD, RESTful naming, proper
   auth (Token / Session), permission classes, `django-filter`,
   20/page pagination, `Accept-Language` where relevant.
3. Document with `drf-spectacular`:
   - ViewSets → `@extend_schema_view(...)` covering
     list/retrieve/create/update/partial_update/destroy plus every
     custom action.
   - Function views → `@extend_schema(...)` and `@api_view`.
   - Tags must match the approved list exactly (see the tag registry
     in the docs code).
4. Describe endpoints thoroughly:
   - `summary` (≤ 60 chars) + `description` (purpose, security, use
     cases, warnings).
   - Request + response schemas with examples.
   - Every response status (200, 201, 400, 401, 403, 404, 429, 500).
   - `OpenApiParameter` for query/path params.
5. URL organisation:
   - APIs stay outside `i18n_patterns`.
   - Split app routing: `app/api_urls.py` (under
     `path('api/app/', include(...))`) vs `app/urls.py` (inside
     `i18n_patterns`).
6. Regenerate docs after changes:
   ```bash
   ./manage.py generate_internal_api_docs
   ./manage.py spectacular --format openapi-json > api-schema.json
   ```

### Admin API (mobile app) — `/api/admin/`

Used by the Spwig Merchant mobile app.

**URL structure**
- Everything at `/api/admin/` outside `i18n_patterns`.
- No language prefix.
- Namespace: `admin_api`.

**Authentication**
- Refresh-token auth (not DRF's simple Token).
- Access tokens: 30 min. Refresh tokens: 14 days, rotated on use.
- Stored in `MobileAuthToken`.
- Every endpoint requires `IsStaffUser`.
- Backend: `admin_api.authentication.MobileTokenAuthentication`.

**Audit logging**
- Every state-changing operation must create an audit entry:
  who / what / when / old / new.
- Use `AdminAPIAuditLog` via `AuditService.log()`.
- Never log passwords or full tokens.
- Required for order status, stock adjustments, product status.

**Documentation**
- Tag every endpoint with `Admin`.
- Include rate-limiting info in descriptions.

**Rate limits**
- Login: 5/min (`admin_auth`).
- General admin API: 300/min (`admin_api`).
- Sensitive ops (stock, status): 30/min (`admin_sensitive`).

**Error responses**
- `{success: bool, error: {code, message, reference}}`.
- Never expose stack traces or internal details.
- Unique error references (format `ERR-XXXXXX`) for debugging.
- Standard HTTP status codes.

**Push notifications**
- Device registration: `/api/admin/devices/register/`.
- APNs (iOS) first.
- Types: `new_order`, `low_stock`, `customer_message`.
- Delivery via Celery tasks.
- Store APNs credentials in environment variables — never in code.

**Request headers**
- `Authorization: Bearer <access_token>`.
- `X-Device-ID: <device_uuid>` (audit + tracking).
- `X-Device-Name: <device_name>` (optional, for admin display).

---

## Currency

Always use Django Money fields for monetary values. The platform
supports optional multi-currency; every price/tax/discount/refund/etc.
must flow through the shared money handling.

---

## Theme tokens workflow

Themes live in [Spwig/components](https://github.com/Spwig/components),
not in this repo. When you change tokens:

1. Edit `tokens.json` in the target theme.
2. `./manage.py generate_tokens_css --all` — regenerates `tokens.css`.
3. `./manage.py update_theme_css --all` — writes `Theme.compiled_css`
   in the DB.
4. **Never manually edit `tokens.css`** — the generator overwrites it.

Supported token categories: `colors`, `dark`, `typography`, `spacing`,
`borders`, `shadows`, `transitions`, `breakpoints`, `responsive`,
`z-index`, `container`; component tokens (menu, header, footer, search,
button/card variants); element tokens (hero, button, spacer, etc.);
widget tokens.

**Dark mode.** Add a `dark` section to `tokens.json` with `bg-*`,
`surface-*`, `text-*`, `border-*`, `overlay` tokens — the generator
emits both `@media (prefers-color-scheme: dark)` and
`[data-theme="dark"]` overrides.

---

## Celery workers during development

When you change code that Celery workers run, kill and restart the
workers so your changes are picked up. Autoreload only covers the dev
server, not Celery.

---

## Testing

Run the full suite:

```bash
./manage.py test
# or
pytest tests/
```

- New features ship with tests.
- Bug fixes should include a regression test.
- CI runs the whole suite plus lint + security on every PR.

---

## Telemetry

Anonymous daily ping to `updates.spwig.com/api/v1/telemetry/`. Payload:
install UUID, Spwig version, edition, country (from IP; the IP itself
is not stored), bucket counts of active feature flags.

Opt out: `SPWIG_TELEMETRY=0`. See `core/telemetry/` and the
[README privacy section](README.md#privacy--telemetry).

---

## Design rules (visual / CSS / components)

For themes, refer to the design rules doc bundled with each theme in
the components repo. Key rules:

- Prefer design tokens over hardcoded values.
- Support RTL.
- Match the existing dark-mode pattern.
- Inline `style="..."` is for **data-driven values only** (e.g. a
  progress bar's width). Static styling goes in external CSS.

---

## Affiliate payment system invariants

If you touch the affiliate subsystem, preserve these invariants:

- Commission amounts are immutable after creation.
- Timestamps are read-only and auto-generated.
- One commission per order — duplicates forbidden.
- Marking a payout complete updates commissions atomically.
- Everything is reversible with a full audit trail.
- Balances derive from source data:
  - `total_earned == outstanding_balance + total_paid`
  - `outstanding_balance >= 0`
  - `payout.amount == sum(commission.amount)`

Consult the affiliate app's own docs before making changes.

---

## Final reminders for AI execution

1. **Map the change to the sections above before writing code.** If a
   section is silent on what you're doing, ask before assuming.
2. **Preserve every invariant.** No section here is decorative.
3. **Reuse shared helpers.** Translation widgets, `AdminUtils`,
   `AdminTabs`, `AdminListFilters`, `admin-base.css` — check what
   exists before rolling your own.
4. **Keep it theme-aware, responsive, and i18n-ready.**
5. **Update this file when new rules emerge** so future runs stay
   aligned.
