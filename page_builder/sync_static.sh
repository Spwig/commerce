#!/bin/bash

# Page Builder Static Files Sync Script
# Copies development files to Django app static directory

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}=== Page Builder Static Files Sync ===${NC}"
echo ""

# Source directories
UTILITIES_SRC="${SCRIPT_DIR}/utilities"
JS_SRC="${SCRIPT_DIR}/js"

# Destination directory (app static)
STATIC_DEST="${SCRIPT_DIR}/static/page_builder"

# Create destination directories if they don't exist
mkdir -p "${STATIC_DEST}/utilities"
mkdir -p "${STATIC_DEST}/js"

# Function to sync files
sync_files() {
    local src="$1"
    local dest="$2"
    local name="$3"

    if [ -d "$src" ]; then
        echo -e "${GREEN}✓${NC} Syncing $name..."
        cp -r "$src"/* "$dest/" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo -e "  ${GREEN}Success${NC}: $name synced"
        else
            echo -e "  ${RED}Warning${NC}: No files to sync in $name"
        fi
    else
        echo -e "${RED}✗${NC} Source not found: $src"
    fi
}

# Sync utilities
echo -e "${BLUE}Syncing Utilities...${NC}"
for utility in color_picker gradient_creator border_editor shadow_editor unit_selector spacing_editor; do
    if [ -d "${UTILITIES_SRC}/$utility" ]; then
        sync_files "${UTILITIES_SRC}/$utility" "${STATIC_DEST}/utilities/$utility" "$utility"
    fi
done

echo ""

# Sync JavaScript files
echo -e "${BLUE}Syncing JavaScript files...${NC}"
sync_files "$JS_SRC" "${STATIC_DEST}/js" "JS files"

echo ""

# Optional: Run collectstatic
read -p "Run 'python manage.py collectstatic' to copy to STATIC_ROOT? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "${SCRIPT_DIR}/.."
    python manage.py collectstatic --noinput
    echo -e "${GREEN}✓${NC} Static files collected"
fi

echo ""
echo -e "${GREEN}=== Sync Complete ===${NC}"
echo ""
echo "Development files location:"
echo "  Utilities: ${UTILITIES_SRC}"
echo "  JS Files:  ${JS_SRC}"
echo ""
echo "App static location:"
echo "  ${STATIC_DEST}"