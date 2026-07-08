#!/usr/bin/env bash
#
# Spwig POS Frontend Build Script
#
# Builds the React PWA and deploys the output into the Django pos_app
# so it can be served without any Nginx configuration changes.
#
# Usage:
#   ./pos_app/build.sh                    # Build and deploy
#   ./pos_app/build.sh --frontend-dir /path/to/frontend   # Custom frontend path
#
# Prerequisites:
#   - Node.js 18+ and npm installed
#   - POS frontend source at the expected path
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHOP_DIR="$(dirname "$SCRIPT_DIR")"

# Frontend source location — override with a positional argument or the
# SPWIG_POS_FRONTEND_DIR env var. The POS frontend lives in a separate
# repo; check out beside the Spwig repo and point this at it.
FRONTEND_DIR="${1:-${SPWIG_POS_FRONTEND_DIR:-../spwig-pos/frontend}}"

# Where built files go inside the Django app
DIST_DIR="$SCRIPT_DIR/frontend_build"
TEMPLATE_DIR="$SCRIPT_DIR/templates/pos"

echo "=== Spwig POS Frontend Build ==="
echo "Frontend source: $FRONTEND_DIR"
echo "Output:          $DIST_DIR"
echo ""

# Validate frontend exists
if [ ! -f "$FRONTEND_DIR/package.json" ]; then
    echo "ERROR: Frontend not found at $FRONTEND_DIR"
    echo "Pass the frontend path as an argument: ./pos_app/build.sh /path/to/frontend"
    exit 1
fi

# Install dependencies if needed
echo ">> Installing dependencies..."
cd "$FRONTEND_DIR"
if [ ! -d "node_modules" ]; then
    npm install
fi

# Build
echo ">> Building frontend..."
npm run build

echo ">> Deploying to Django app..."

# Clean previous build
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Copy all built files to dist/ (assets, SW, manifest, icons)
cp -r "$FRONTEND_DIR/dist/." "$DIST_DIR/"

# Copy index.html as Django template (overwrite the placeholder)
mkdir -p "$TEMPLATE_DIR"
cp "$FRONTEND_DIR/dist/index.html" "$TEMPLATE_DIR/index.html"

echo ""
echo "=== Build complete ==="
echo "Template: $TEMPLATE_DIR/index.html"
echo "Assets:   $DIST_DIR/"
echo ""
echo "Restart Django to pick up the new template."
echo "For production, run: python manage.py collectstatic --noinput"
