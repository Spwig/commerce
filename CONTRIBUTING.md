# Contributing to Spwig

Thanks for considering a contribution. This repo is the core Django platform
that powers [Spwig](https://spwig.com) — a self-hostable, merchant-focused
e-commerce platform. Every contribution counts, from a typo fix in the docs to
a whole new payment provider.

## TL;DR

1. Fork the repo and create a branch from `main`
2. Make your change (see [dev setup](#dev-setup))
3. Commit with **`git commit -s`** (the `-s` adds the DCO sign-off line — required)
4. Push and open a pull request against `Spwig/commerce:main`

That's the whole flow. Details below.

## Ways to contribute

- **Report a bug** — open an [issue](https://github.com/Spwig/commerce/issues)
  with reproduction steps and expected vs. actual behaviour
- **Fix a bug** — pick an issue labelled `good first issue` or `help wanted`
  and submit a PR
- **Add a feature** — for anything non-trivial please open an issue first so we
  can discuss shape and scope before you invest the time
- **Improve documentation** — README, ARCHITECTURE, code comments, admin help
  text. Doc PRs are always welcome
- **Write a theme or integration** — those live in
  [`Spwig/components`](https://github.com/Spwig/components), not here. Start
  with the [`spwig-theme-sdk`](https://github.com/Spwig/theme-sdk) or
  [`spwig-provider-sdks`](https://github.com/Spwig/provider-sdks)

## Developer Certificate of Origin (DCO)

We use the [Developer Certificate of Origin](https://developercertificate.org/)
instead of a Contributor License Agreement. It's a short, well-understood
statement that you have the right to submit your contribution under this
project's licence (AGPL-3.0-or-later).

To sign off, add `-s` to every commit:

```bash
git commit -s -m "Add support for X"
```

That appends a line like:

```
Signed-off-by: Your Name <your.email@example.com>
```

The sign-off must match your git `user.name` and `user.email`. If you forget on
a commit, amend the last commit with `git commit --amend --signoff`, or
sign-off a range with `git rebase --signoff HEAD~N`.

CI blocks PRs without a sign-off on every commit.

## Dev setup

You develop against **source form** — pure Python, no compilation step.
That's exactly what CI runs, what our `docker-compose.dev.yml` runs, and
what a fresh clone of this repo gives you. If you've heard about the
Cython-compiled "signed release" of Spwig, that's a downstream build
target (see [ARCHITECTURE.md → Distribution model](ARCHITECTURE.md#distribution-model))
— it lives outside this repo and you don't need it to develop.

You need Python 3.12+, Node 18+, PostgreSQL 15+, Redis 7+.

```bash
# 1. Fork + clone
git clone git@github.com:YOUR_USER/commerce.git spwig-commerce
cd spwig-commerce

# 2. Python venv
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Node dependencies (for linting)
npm install

# 4. Local PostgreSQL + Redis via docker-compose
docker compose -f docker-compose.dev.yml up -d

# 5. Environment
cp .env.example .env
# edit .env — DB_*, REDIS_*, SECRET_KEY at minimum

# 6. Migrate + create a superuser
./manage.py migrate
./manage.py createsuperuser

# 7. Run the shop
./manage.py runserver
# Storefront: http://localhost:8000
# Admin:      http://localhost:8000/en/admin/
```

## Repository layout

Spwig is a modular Django monolith. The most-touched apps:

| App | What it does |
|-----|--------------|
| `core/` | Licence, activation, telemetry, hosted-service clients, admin theme |
| `accounts/` | Customer + staff accounts, MFA, OAuth |
| `catalog/` | Products, variants, categories, inventory |
| `cart/` | Session cart, checkout, discounts |
| `orders/` | Order lifecycle, refunds |
| `payment_providers/` | Payment provider registry + provider apps |
| `shipping/` | Shipping providers + rate quoting |
| `design/` | Themes, page builder, storefront rendering |
| `admin_api/` | REST API used by the mobile admin |
| `email_system/` | Transactional email, templates, sending backends |
| `pos_app/`, `pos_api/` | Point-of-sale (Community edition shows an upgrade CTA) |

Full tour in [ARCHITECTURE.md](ARCHITECTURE.md).

## Coding style

- **Python**: PEP 8. Run `ruff check .` and `ruff format .` — both are already
  configured in [`pyproject.toml`](pyproject.toml). CI runs both.
- **JavaScript**: no build step required for admin JS. Use vanilla DOM APIs
  where possible; keep the bundle small. `eslint` config is in the repo.
- **CSS**: prefer design tokens (`css/tokens.css` per theme) over hardcoded
  values. Support RTL where the component may render in Arabic/Hebrew stores.
- **File headers**: keep them terse. When adding a new source file, use
  `/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */`
  (or the language-appropriate comment syntax) if you're adding any header at
  all — most files don't need one.
- **Translations**: user-facing strings should use `{% trans %}` /
  `gettext_lazy`. Do NOT translate `.po` files manually — extraction happens
  through `makemessages` and translation is handled by our translation system.

## Testing

```bash
# Full suite
./manage.py test

# Or with pytest
pytest tests/

# A specific area
pytest tests/community_edition/
```

New features should ship with tests. Bug fixes should ideally include a
regression test.

## Submitting a pull request

1. **One logical change per PR** — small PRs merge faster and are easier to
   review
2. **Describe the *why*** — the diff shows the *what*. Explain motivation,
   trade-offs, and anything reviewers should focus on
3. **Screenshots for visual changes** — admin UI, storefront, page builder
4. **Test plan** — how you verified the change; what regressions you looked for
5. **Sign off every commit** — see [DCO](#developer-certificate-of-origin-dco)

A maintainer will review, may suggest changes, and merge when ready. Be
patient — this is a self-funded project and reviews happen in cycles.

## Getting help

- **Community forum**: [community.spwig.com](https://community.spwig.com) —
  open-ended discussion, ideas, questions
- **Documentation**: [docs.spwig.com](https://docs.spwig.com)
- **Bug reports / feature requests**:
  [github.com/Spwig/commerce/issues](https://github.com/Spwig/commerce/issues)

Please don't email maintainers directly for issues that could be discussed
publicly — a public thread lets others find the answer later.

## Licence

By contributing to this repository, you agree that your contribution is
licensed under the [AGPL-3.0-or-later](LICENSE) licence, the same licence as
this project.
