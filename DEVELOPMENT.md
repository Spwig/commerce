# Running Spwig locally without Docker

This guide gets a fresh clone of Spwig running **natively** on your machine —
no containers — on **Ubuntu/Debian**, **macOS**, or **Windows**. It's the
metal-and-venv counterpart to the Docker quick-start in
[CONTRIBUTING.md](CONTRIBUTING.md#dev-setup); either path gives you the same
source-form app that CI runs.

> **Why you might want this:** faster edit/reload, a debugger attached to the
> real process, and no Docker layer between you and Postgres/Redis. The
> trade-off is that you install and run PostgreSQL, Redis, and a couple of
> system libraries yourself.

You develop against **source form** — pure Python, no compilation step. A fresh
clone is immediately runnable; the Cython-compiled "signed release" is a
downstream build target you don't need for development
(see [ARCHITECTURE.md → Distribution model](ARCHITECTURE.md#distribution-model)).

---

## 1. What you need

| Component | Version | Why |
|-----------|---------|-----|
| **Python** | 3.12+ | `requires-python >=3.12` (`pyproject.toml`) |
| **PostgreSQL** | 15+ | Primary datastore |
| **pgvector** | 0.5+ | Postgres extension — the first migration runs `CREATE EXTENSION vector` for help-search embeddings. **Postgres will not migrate without it.** |
| **Redis** | 7+ | Cache, sessions, Celery broker, Channels layer |
| **libmagic** | — | System library used by `python-magic` for upload MIME sniffing |
| **Node.js** | 18+ | *Optional* — only for `eslint`/`prettier`/pre-commit. Not needed to run the server (admin JS has no build step). |

**Windows users:** the smoothest path by far is **WSL2 + Ubuntu**, then follow
the Ubuntu instructions inside the WSL shell. Redis has no official native
Windows build and pgvector is awkward to compile on Windows, so WSL2 saves you
real pain. Native-Windows notes are in [§8](#8-windows-native-fallback) if you
can't use WSL2.

---

## 2. Install the system dependencies

### Ubuntu / Debian (and WSL2)

```bash
# Python 3.12 (Ubuntu 24.04 ships it; on 22.04 add the deadsnakes PPA first)
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev build-essential

# PostgreSQL + pgvector — match the pgvector package to your PG major version
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y postgresql-16-pgvector   # or postgresql-15-pgvector, etc.

# Redis
sudo apt install -y redis-server

# libmagic (python-magic runtime dependency)
sudo apt install -y libmagic1

# (optional) Node for linting
sudo apt install -y nodejs npm
```

Start the services:

```bash
sudo service postgresql start     # or: sudo systemctl start postgresql
sudo service redis-server start   # or: sudo systemctl start redis-server
```

> If `apt` has no `postgresql-16-pgvector` package for your release, install
> pgvector from source: `sudo apt install postgresql-server-dev-16 make gcc`,
> then `git clone https://github.com/pgvector/pgvector && cd pgvector && make && sudo make install`.

### macOS (Homebrew)

```bash
brew install python@3.12 postgresql@16 pgvector redis libmagic
brew install node                 # optional, for linting

brew services start postgresql@16
brew services start redis
```

Homebrew's `pgvector` formula installs the extension into the Homebrew
PostgreSQL, so no source build is needed.

---

## 3. Create the database, role, and extension

Open a superuser `psql` session:

```bash
# Ubuntu/WSL2:
sudo -u postgres psql
# macOS (Homebrew):
psql -d postgres
```

Then run (these values match the defaults in `.env.example`):

```sql
CREATE USER shop_user WITH PASSWORD 'changeme';
CREATE DATABASE shop_db OWNER shop_user;

-- Let the role create databases (needed so the test suite can build test_shop_db)
ALTER USER shop_user CREATEDB;

-- Pre-create the vector extension as superuser so the migration's
-- CREATE EXTENSION becomes a no-op even for a non-superuser role.
\c shop_db
CREATE EXTENSION IF NOT EXISTS vector;

\q
```

> **About `CREATE EXTENSION vector`.** pgvector isn't a "trusted" extension, so
> a plain role normally can't create it. Two ways to satisfy this:
> - **Pre-create it** in `shop_db` as shown above (covers running the server).
> - **For the test suite:** Django drops and recreates `test_shop_db` on every
>   run, re-running the extension migration in a database you can't pre-seed.
>   The pragmatic local-dev fix is to grant the role superuser:
>   `ALTER USER shop_user WITH SUPERUSER;` — **local machines only**, never in
>   production.

---

## 4. Clone, create a venv, install requirements

```bash
git clone git@github.com:YOUR_USER/commerce.git spwig-commerce
cd spwig-commerce

python3.12 -m venv .venv
source .venv/bin/activate          # Windows (native): .venv\Scripts\activate
python -m pip install --upgrade pip

# Runtime deps only:
pip install -r requirements.txt
# ...or, to also get pytest / ruff / debug-toolbar for contributing:
pip install -r requirements-dev.txt
```

`requirements.txt` pins binary wheels for the heavy native packages
(`psycopg2-binary`, `Pillow`, `cryptography`, `onnxruntime`), so there's no
C toolchain compile beyond what `build-essential` covers.

If you want to run linting/pre-commit, also `npm install` in the repo root.

---

## 5. Configure `.env`

Spwig reads a `.env` file at the repo root via `django-environ`
(`core/settings.py`). Start from the example:

```bash
cp .env.example .env
```

Then edit `.env`. The minimum for a working local install:

```dotenv
# --- Django ---
DEBUG=True                                   # serves static files + shows tracebacks
DJANGO_SECRET_KEY=<paste a generated key>    # see command below
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# --- Database (match what you created in §3) ---
DB_NAME=shop_db
DB_USER=shop_user
DB_PASSWORD=changeme
DB_HOST=localhost
DB_PORT=5432

# --- Redis ---
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# --- Licence path (IMPORTANT for non-Docker dev) ---
# Default is /opt/shop-platform/license/license.json, which isn't writable
# off-Docker. Point it somewhere local and writable so the Community licence
# bootstraps cleanly on first boot.
LICENSE_PATH=./.spwig/license.json

# --- Optional but recommended ---
# Encrypts stored email/shipping provider credentials at rest.
EMAIL_ENCRYPTION_KEY=<paste a Fernet key>
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Generate the two keys:

```bash
# Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Fernet encryption key (for EMAIL_ENCRYPTION_KEY / SHIPPING_ENCRYPTION_KEY)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

> **Why `LICENSE_PATH` matters:** on first startup `core.apps.CoreConfig.ready()`
> bootstraps a signed **Community** licence to `LICENSE_PATH`. Once a valid
> licence file exists, `ActivationMiddleware` becomes a no-op and you skip the
> `/activate/` redirect. Bootstrapping is non-fatal if it can't write, but a
> local writable path gives you a clean Community edition out of the box. The
> keys `SPWIG_SECRET_KEY` / `SPWIG_ALLOWED_HOSTS` are also accepted and take
> precedence over the `DJANGO_*` names if you prefer them.

---

## 6. Migrate, seed, bootstrap the licence, create a superuser

```bash
# Apply migrations (runs CREATE EXTENSION vector — §3 must be done first)
./manage.py migrate

# Seed the baseline data a store can't run without. REQUIRED — do not skip.
./manage.py seed

# Bootstrap the Community licence into LICENSE_PATH (ready() also does this,
# but running it explicitly surfaces any path/permission problem immediately)
./manage.py bootstrap_community_licence

# Create your admin login
./manage.py createsuperuser

# Collect static assets (required when DEBUG=False; harmless with DEBUG=True)
./manage.py collectstatic --noinput
```

> **Don't skip `seed`.** It's the exact step the Docker entrypoint runs after
> migrating, and it creates the singletons the app assumes always exist — the
> `SiteSettings` row, Django `Site` id=1, a default sales region and warehouse,
> header presets, default pages, and more. **Without it, a freshly migrated
> database 500s on every page** with `ValidationError: {'admin_email': ['This
> field cannot be blank.']}`, because the code lazily tries to create a blank
> `SiteSettings` singleton and it fails validation. `seed` is idempotent and
> version-tracked — re-running it only fills in what's missing. (It seeds an
> empty admin email; set your real store details in **Admin → Site Settings**
> once you're logged in.)

---

## 7. Run it

```bash
./manage.py runserver
```

- **Storefront:** http://localhost:8000
- **Admin:** http://localhost:8000/en/admin/

`daphne` is first in `INSTALLED_APPS`, so `runserver` serves over ASGI (needed
for the Channels/WebSocket features) — no extra command required.

**First request → one-time licence acceptance.** On a brand-new install every
route redirects (HTTP 302) to `/license/accept/`. This is expected: it's the
one-time AGPL acceptance gate, not an error. Tick the box and submit; you're
redirected back to the storefront and the admin, and the gate doesn't appear
again. (If that page itself returns a 500 instead of rendering, you skipped
`./manage.py seed` in §6 — run it and reload.)

### Background jobs (optional)

Email sending, translations, product feeds, and other async work run on Celery.
The dev server does **not** run them; start workers in separate shells (with the
venv active) when you need them:

```bash
celery -A core worker -l info
celery -A core beat   -l info      # periodic tasks (django-celery-beat)
```

> Celery does **not** autoreload. After changing code a worker runs, kill and
> restart it.

### Run the tests

```bash
pytest tests/            # or: ./manage.py test
```

Requires `requirements-dev.txt` installed and a role that can create
`test_shop_db` with the vector extension (see the superuser note in §3).

---

## 8. Windows (native) fallback

Use this only if WSL2 isn't an option — it's the harder road.

- **Python 3.12** — install from python.org; activate the venv with
  `.venv\Scripts\activate`.
- **PostgreSQL** — the EnterpriseDB installer. Install **pgvector** with a
  prebuilt binary from the [pgvector releases](https://github.com/pgvector/pgvector/releases)
  matching your PG version (or build it with MSVC). Then create the DB/role/
  extension exactly as in §3 using **pgAdmin** or the SQL Shell (`psql`).
- **Redis** — no official Windows build. Use **Memurai** (a Redis-compatible
  Windows service) or run Redis inside WSL2.
- **libmagic** — `python-magic` can't find libmagic on Windows by default.
  Install the bundled binaries: `pip install python-magic-bin`.

Everything from §4 onward (venv, `.env`, migrate, runserver) is identical; just
use Windows path separators for `LICENSE_PATH` (e.g. a folder in your home
directory).

---

## 9. Troubleshooting

| Symptom | Cause & fix |
|---------|-------------|
| `django.db.utils.OperationalError: could not connect` | Postgres isn't running or `DB_*` in `.env` don't match §3. Confirm with `psql -U shop_user -h localhost -d shop_db`. |
| `permission denied to create extension "vector"` during `migrate` or tests | The role can't create the extension. Pre-create it in `shop_db` (§3), and grant the role superuser for the test DB. |
| `type "vector" does not exist` | pgvector isn't installed **on the server**, only the Python client. Install the `postgresql-<ver>-pgvector` package / Homebrew `pgvector`, then `CREATE EXTENSION vector;`. |
| Every page 500s with `admin_email … cannot be blank` (often on `/license/accept/`) | You migrated but didn't seed. Run `./manage.py seed` (§6) — it creates the `SiteSettings` singleton the app expects. |
| `ImportError: failed to find libmagic` | Install `libmagic1` (Ubuntu) / `libmagic` (brew) / `python-magic-bin` (Windows). |
| `redis.exceptions.ConnectionError` | Redis isn't running or `REDIS_*` are wrong. `redis-cli ping` should return `PONG`. |
| Redirected to `/activate/` in a loop | The Community licence didn't bootstrap. Set `LICENSE_PATH` to a writable local path (§5) and run `./manage.py bootstrap_community_licence`. |
| Static files 404 with `DEBUG=False` | Run `./manage.py collectstatic --noinput`, or set `DEBUG=True` for dev. |
| `SECRET_KEY` insecure warning | Set `DJANGO_SECRET_KEY` in `.env` (§5). |

---

For the wider architecture, app layout, and contribution flow, see
[ARCHITECTURE.md](ARCHITECTURE.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
