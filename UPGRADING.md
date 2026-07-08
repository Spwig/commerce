# Upgrading Spwig

Two paths exist depending on how you installed Spwig. Pick the one
that matches your setup.

---

## 1. Installer-based install (recommended)

If you installed Spwig with the
[Spwig/spwig installer](https://github.com/Spwig/spwig), your host
runs pre-built signed container images pulled from Spwig's registry.
Upgrades happen through the platform admin.

**In the admin:**

1. Navigate to **Admin → Platform → Updates**.
2. Click *Check for updates*.
3. Review the release notes for the version offered.
4. Click *Install update*.

The upgrader service (running in your compose stack as
`docker compose --profile upgrader up -d`) pulls the new signed images
from `registry.spwig.com`, runs a database migration, and restarts the
containers. Zero-downtime rolling is not currently supported —
downtime during the upgrade is typically 15–30 seconds.

**Command line equivalent** (if you prefer):

```bash
docker compose pull
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py collectstatic --noinput
```

**⚠ Do not use this path if you've modified the code.** The signed
images are built from a specific commit on `Spwig/commerce`; any
edits you've made to Python, templates, or static files inside the
container filesystem are replaced. Custom components installed
through the marketplace live in a separate volume (`components_data`)
and survive upgrades.

---

## 2. Source-form install (git clone + build)

If you cloned this repo and built the images yourself (`docker compose
build`), you own the upgrade path. Standard git workflow:

```bash
# From the repo root
git pull origin main
docker compose build
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py collectstatic --noinput
```

Read the release notes at
[github.com/Spwig/commerce/releases](https://github.com/Spwig/commerce/releases)
before pulling — some releases include breaking migrations or config
changes that need attention.

**If you've forked with local changes**, rebase or merge your fork
against `Spwig/commerce/main` before rebuilding. Standard git conflict
resolution applies.

**Do NOT enable the `--profile upgrader` compose profile on a
source-form install.** The upgrader replaces containers with signed
images from `registry.spwig.com` — it will overwrite the local build
you produced from your own source.

---

## Component updates (both paths)

Themes, providers, widgets, and other marketplace components install
into `components_data/` in a separate Docker volume. They never touch
core code and can be upgraded independently at any time via the
**Admin → Marketplace** UI, regardless of which install path you're on.

---

## Data migrations

Both paths run `./manage.py migrate` as part of the upgrade. The
Django ORM handles schema changes idempotently — safe to re-run if
interrupted. Take a database backup before upgrading in production:

```bash
docker compose exec db pg_dump -U ${DB_USER:-shop_user} ${DB_NAME:-shop_db} \
  | gzip > backups/pre-upgrade-$(date +%Y%m%d-%H%M%S).sql.gz
```

Restoring:

```bash
gunzip -c backups/pre-upgrade-YYYYMMDD-HHMMSS.sql.gz \
  | docker compose exec -T db psql -U ${DB_USER:-shop_user} ${DB_NAME:-shop_db}
```

---

## Rollback

**Installer-based**: Admin → Platform → Updates → *Rollback to previous
version* (available for 7 days after each upgrade; the upgrader keeps
the previous image tagged locally).

**Source-form**: `git checkout` the previous tag, `docker compose
build`, restart. Restore the pre-upgrade database backup if the new
version had migrations that don't rollback cleanly.

---

## Support

Bug reports and questions:
[github.com/Spwig/commerce/issues](https://github.com/Spwig/commerce/issues).
Security-related issues: see [SECURITY.md](SECURITY.md).
