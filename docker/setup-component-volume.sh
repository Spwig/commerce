#!/bin/bash
# =============================================================================
# Component Volume Setup
# =============================================================================
# Ensures the persistent volume structure exists for installed components.
# Component installation is handled by the install_bundled_components
# management command (for themes/utilities) and by the marketplace update
# system (for provider integrations).
#
# Volume mount: components_data -> /app/components_data
# All component types use direct paths (settings.py points to /app/components_data)
# =============================================================================
set -e

DATA_DIR="/app/components_data"

# Skip if no volume mounted
if [ ! -d "$DATA_DIR" ]; then
    echo "No component data volume mounted at $DATA_DIR, skipping."
    exit 0
fi

echo "=== Component Volume Setup ==="

# Ensure directory structure
# All component types: direct paths (no symlinks needed — settings.py points here)
mkdir -p "$DATA_DIR/static/utilities" \
         "$DATA_DIR/static/design/themes" \
         "$DATA_DIR/templates/utilities" \
         "$DATA_DIR/registries" \
         "$DATA_DIR/integrations"
chown -R spwig:spwig "$DATA_DIR" 2>/dev/null || true

# === One-time migrations for existing Docker deployments ===

# Migrate old utility data layout if present
if [ -d "$DATA_DIR/utilities_static" ] && [ ! -d "$DATA_DIR/static/utilities" ] || [ -z "$(ls -A "$DATA_DIR/static/utilities" 2>/dev/null)" ]; then
    if [ -d "$DATA_DIR/utilities_static" ] && [ -n "$(ls -A "$DATA_DIR/utilities_static" 2>/dev/null)" ]; then
        echo "Migrating utilities_static -> static/utilities..."
        cp -a "$DATA_DIR/utilities_static/"* "$DATA_DIR/static/utilities/" 2>/dev/null || true
    fi
fi
if [ -d "$DATA_DIR/utilities_templates" ] && [ ! -d "$DATA_DIR/templates/utilities" ] || [ -z "$(ls -A "$DATA_DIR/templates/utilities" 2>/dev/null)" ]; then
    if [ -d "$DATA_DIR/utilities_templates" ] && [ -n "$(ls -A "$DATA_DIR/utilities_templates" 2>/dev/null)" ]; then
        echo "Migrating utilities_templates -> templates/utilities..."
        cp -a "$DATA_DIR/utilities_templates/"* "$DATA_DIR/templates/utilities/" 2>/dev/null || true
    fi
fi

# Migrate old theme data layout: themes/ -> static/design/themes/
if [ -d "$DATA_DIR/themes" ] && [ -n "$(ls -A "$DATA_DIR/themes" 2>/dev/null)" ]; then
    if [ -z "$(ls -A "$DATA_DIR/static/design/themes" 2>/dev/null)" ]; then
        echo "Migrating themes/ -> static/design/themes/..."
        cp -a "$DATA_DIR/themes/"* "$DATA_DIR/static/design/themes/" 2>/dev/null || true
    fi
fi

# Normalize utility directory names: replace hyphens with underscores
# (preinstalled packages use hyphen slugs like 'color-picker', but all template
# code expects underscore paths like 'utilities/color_picker/current/...')
# This is idempotent — no-op if names already use underscores.
for d in "$DATA_DIR/static/utilities"/*/; do
    [ -d "$d" ] || continue
    old="$(basename "$d")"
    new="${old//-/_}"
    if [ "$old" != "$new" ]; then
        mv "$DATA_DIR/static/utilities/$old" "$DATA_DIR/static/utilities/$new" 2>/dev/null || true
        echo "  Normalized utility: $old -> $new"
    fi
done
for d in "$DATA_DIR/templates/utilities"/*/; do
    [ -d "$d" ] || continue
    old="$(basename "$d")"
    new="${old//-/_}"
    if [ "$old" != "$new" ]; then
        mv "$DATA_DIR/templates/utilities/$old" "$DATA_DIR/templates/utilities/$new" 2>/dev/null || true
    fi
done

# Clean up broken symlinks in persistent volume
find "$DATA_DIR" -xtype l -delete 2>/dev/null || true

echo "=== Component Volume Ready ==="
