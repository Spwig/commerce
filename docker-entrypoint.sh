#!/bin/bash
set -e

# Default Gunicorn workers (can be overridden by env var for fleet deployments)
export GUNICORN_WORKERS="${GUNICORN_WORKERS:-4}"

# Wait for database/connection pooler to be ready
if [ -n "${PGBOUNCER_HOST:-}" ]; then
    echo "Waiting for PgBouncer at ${PGBOUNCER_HOST}:${PGBOUNCER_PORT:-6432}..."
    while ! nc -z "$PGBOUNCER_HOST" "${PGBOUNCER_PORT:-6432}"; do
        sleep 0.1
    done
    echo "PgBouncer is ready!"
elif [ -n "${DB_HOST:-}" ]; then
    echo "Waiting for database at ${DB_HOST}:${DB_PORT:-5432}..."
    while ! nc -z "${DB_HOST}" "${DB_PORT:-5432}"; do
        sleep 0.1
    done
    echo "Database is ready!"
fi

# Ensure media directories exist and are writable
echo "Ensuring media directories exist and are writable..."
mkdir -p /app/media/media_library/thumbnails
mkdir -p /app/media/design
mkdir -p /app/media/themes
chown -R spwig:spwig /app/media 2>/dev/null || true

# Set setgid bit on media directories so new subdirectories created by any
# user (e.g. root via docker exec) inherit the spwig group and remain
# writable by the spwig user running gunicorn.
find /app/media -type d -exec chmod g+ws {} + 2>/dev/null || true

# Ensure license directory exists and is writable
echo "Ensuring license directory exists and is writable..."
mkdir -p /opt/shop-platform/license
chown -R spwig:spwig /opt/shop-platform 2>/dev/null || true

# Verify the spwig user can actually write to the media directory
# (entrypoint runs as root, so we must test as spwig explicitly)
if ! su -s /bin/sh spwig -c "touch /app/media/.write_test" 2>/dev/null; then
    echo "Media directory not writable by spwig, attempting to fix permissions..."
    chown -R spwig:spwig /app/media 2>/dev/null || true
    find /app/media -type d -exec chmod g+ws {} + 2>/dev/null || true
fi
rm -f /app/media/.write_test

# Final verification as spwig user
if ! su -s /bin/sh spwig -c "touch /app/media/.write_test" 2>/dev/null; then
    echo "ERROR: Media directory /app/media is not writable by spwig user!"
    echo "Please ensure the volume has correct permissions for user 'spwig'"
    exit 1
fi
rm -f /app/media/.write_test
echo "✓ Media directory is ready"

# Setup component volume structure and symlinks
if [ -f /docker/setup-component-volume.sh ]; then
    /docker/setup-component-volume.sh
fi

# Clean up broken symlinks in persistent volume (e.g. "current" symlinks
# pointing to version directories that don't exist yet in the image)
find /app/components_data -xtype l -delete 2>/dev/null || true

# Fix components_data ownership if needed (volume may have been created by root)
if [ -d "/app/components_data" ]; then
    if ! touch /app/components_data/.write_test 2>/dev/null; then
        echo "Components data directory not writable, attempting to fix permissions..."
        chown -R spwig:spwig /app/components_data 2>/dev/null || true
    fi
    rm -f /app/components_data/.write_test

    # Final verification
    if ! touch /app/components_data/.write_test 2>/dev/null; then
        echo "WARNING: Components data directory /app/components_data is not writable!"
        echo "Provider installations from marketplace may fail."
        echo "Please ensure the volume has correct permissions for user 'spwig'"
    else
        rm -f /app/components_data/.write_test
        echo "✓ Components data directory is ready"
    fi
fi

# Grant Docker socket access to spwig user (for log viewer container status)
# The Docker socket GID varies across hosts, so detect it dynamically
if [ -S /var/run/docker.sock ]; then
    DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
    if ! getent group "$DOCKER_GID" > /dev/null 2>&1; then
        groupadd -g "$DOCKER_GID" docker_host 2>/dev/null || true
    fi
    DOCKER_GROUP=$(getent group "$DOCKER_GID" | cut -d: -f1)
    if [ -n "$DOCKER_GROUP" ]; then
        usermod -aG "$DOCKER_GROUP" spwig 2>/dev/null || true
        echo "✓ Docker socket access configured for log viewer"
    fi
fi

# Apply pending hotfixes (before any Python code runs)
# Hotfixes are compiled files (.pyc/.so) overlaid onto /app from a persistent volume.
# This must run for both web and celery containers so all processes use patched code.
if [ -f /docker/apply-hotfixes.sh ]; then
    /docker/apply-hotfixes.sh
fi

# Detect if we're running as a celery worker (not the web server)
IS_CELERY=false
if echo "$@" | grep -q "celery"; then
    IS_CELERY=true
    echo "Running as Celery worker - skipping web-only setup steps"
fi

# Run migrations (web server only - celery should not race with migrations)
if [ "$IS_CELERY" = false ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput

    # Auto-activate from SETUP_TOKEN env var (cloud/automated installs)
    if [ -n "${SETUP_TOKEN:-}" ] && [ ! -f /opt/shop-platform/license/license.json ]; then
        echo "Activating with setup token..."
        ACTIVATION_DOMAIN="${ALLOWED_HOSTS%%,*}"  # First entry from ALLOWED_HOSTS
        ACTIVATION_DOMAIN="${ACTIVATION_DOMAIN:-localhost}"
        python manage.py activate_with_token "$SETUP_TOKEN" --domain "$ACTIVATION_DOMAIN" || {
            echo "WARNING: Auto-activation failed. Visit http://your-domain/activate/ to activate manually."
        }
    fi

    # Setup default data (idempotent - safe to run on every startup)
    # Runs all seed commands in dependency order with version tracking.
    # Individual seeds skip automatically if already at current version.
    echo "Setting up system defaults..."
    python manage.py seed

    # Collect static files
    if [ -f /app/staticfiles/.prebaked ]; then
        echo "Static files pre-baked at build time"
        # Components (themes, providers, utilities) install static files into
        # the components_data/ volume which is NOT pre-baked. After a container
        # restart or upgrade the writable layer is gone, so we must re-collect
        # component statics into /app/staticfiles/ for WhiteNoise to serve them.
        component_statics=$(find /app/components_data/static /app/components_data/integrations \
            -type f \( -name "*.css" -o -name "*.js" -o -name "*.png" -o -name "*.jpg" \
            -o -name "*.svg" -o -name "*.woff2" -o -name "*.woff" -o -name "*.ico" \) \
            2>/dev/null | head -1)
        if [ -n "$component_statics" ]; then
            echo "Syncing component static files (incremental)..."
            python manage.py collect_component_statics || {
                echo "Incremental sync failed, falling back to full collectstatic..."
                python manage.py collectstatic --noinput
            }
            chown -R spwig:spwig /app/staticfiles 2>/dev/null || true
        fi
    else
        echo "Clearing old static files..."
        rm -rf /app/staticfiles/* 2>/dev/null || true
        echo "Collecting static files..."
        python manage.py collectstatic --noinput
        chown -R spwig:spwig /app/staticfiles 2>/dev/null || true
    fi

    # Create superuser if specified (supports both SPWIG_ADMIN_* and legacy DJANGO_SUPERUSER_* env vars)
    ADMIN_USERNAME="${SPWIG_ADMIN_USERNAME:-$DJANGO_SUPERUSER_USERNAME}"
    ADMIN_EMAIL="${SPWIG_ADMIN_EMAIL:-$DJANGO_SUPERUSER_EMAIL}"
    ADMIN_PASSWORD="${SPWIG_ADMIN_PASSWORD:-$DJANGO_SUPERUSER_PASSWORD}"

    if [ "$ADMIN_USERNAME" ] && [ "$ADMIN_EMAIL" ] && [ "$ADMIN_PASSWORD" ]; then
        export DJANGO_SUPERUSER_PASSWORD="$ADMIN_PASSWORD"
        python manage.py createsuperuser \
            --noinput \
            --username "$ADMIN_USERNAME" \
            --email "$ADMIN_EMAIL" \
            2>/dev/null || echo "Superuser already exists"
        unset DJANGO_SUPERUSER_PASSWORD
    fi

    # Wait for Postfix to start (managed by supervisor)
    echo "Waiting for Postfix to start..."
    for i in {1..15}; do
        if supervisorctl status postfix 2>/dev/null | grep -q RUNNING; then
            echo "✓ Postfix is running"
            break
        fi
        if [ $i -eq 15 ]; then
            echo "⚠ Warning: Postfix may not have started"
            echo "Check logs with: supervisorctl tail postfix stderr"
        fi
        sleep 1
    done
else
    # Celery workers just need to wait for the database
    echo "Waiting for migrations to complete..."
    sleep 5
fi

# Execute the main command
exec "$@"
