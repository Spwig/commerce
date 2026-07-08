#!/bin/bash
# =============================================================================
# APPLY HOTFIXES
# =============================================================================
# Called by docker-entrypoint.sh at container startup to overlay any pending
# hotfix files onto /app before the application starts.
#
# Hotfix packages are downloaded by the upgrader service to /app/hotfixes/
# (a persistent volume). Each hotfix is a directory containing:
#   - hotfix_manifest.json  (metadata + file checksums)
#   - compiled files (.pyc/.so) in their original directory structure
#
# Hotfixes are independent: each patches specific files. All hotfixes for
# the current version are applied in numerical order.
#
# Marker format: "1.3.0:1,2,3" (version:comma-separated applied numbers)
# Legacy format: "1.3.0-hf2" (treated as having applied [2])
# =============================================================================

set -e

HOTFIX_DIR="/app/hotfixes"
APPLIED_MARKER="$HOTFIX_DIR/.applied"

# Exit early if no hotfixes directory or it's empty
if [ ! -d "$HOTFIX_DIR" ] || [ -z "$(ls -A "$HOTFIX_DIR" 2>/dev/null)" ]; then
    exit 0
fi

# Get current platform version
PLATFORM_VERSION=$(python3 -c "
import sys
sys.path.insert(0, '/app')
try:
    import core
    print(getattr(core, '__version__', ''))
except Exception:
    # Try reading from version file
    try:
        with open('/app/.platform_version') as f:
            print(f.read().strip())
    except Exception:
        print('')
" 2>/dev/null)

if [ -z "$PLATFORM_VERSION" ]; then
    echo "  Could not determine platform version — skipping hotfix check"
    exit 0
fi

# Find hotfix directories for this version
# Convention: /app/hotfixes/{version}/hf{number}/
VERSION_DIR="$HOTFIX_DIR/$PLATFORM_VERSION"
if [ ! -d "$VERSION_DIR" ]; then
    exit 0
fi

# Parse the applied marker to get list of already-applied hotfix numbers
APPLIED_LIST=""
if [ -f "$APPLIED_MARKER" ]; then
    MARKER_CONTENT=$(cat "$APPLIED_MARKER" 2>/dev/null)
    if echo "$MARKER_CONTENT" | grep -q ':'; then
        # New format: "1.3.0:1,2,3"
        APPLIED_LIST=$(echo "$MARKER_CONTENT" | cut -d: -f2)
    elif echo "$MARKER_CONTENT" | grep -q '\-hf'; then
        # Legacy format: "1.3.0-hf2"
        APPLIED_LIST=$(echo "$MARKER_CONTENT" | sed 's/.*-hf//')
    fi
fi

# Helper: check if a number is in the comma-separated applied list
is_applied() {
    local num="$1"
    local IFS=','
    for applied_num in $APPLIED_LIST; do
        if [ "$applied_num" = "$num" ]; then
            return 0
        fi
    done
    return 1
}

# Verify that applied hotfixes are actually present on disk.
# The marker lives on a persistent volume but the patched files live in the
# container's writable layer — if the container was recreated (docker compose
# down/up, or image upgrade), the patches are lost but the marker persists.
# Detect this by checking that at least one patched file from the first
# "applied" hotfix actually exists at its target path in /app.
if [ -n "$APPLIED_LIST" ]; then
    FIRST_APPLIED=$(echo "$APPLIED_LIST" | cut -d, -f1)
    FIRST_HF_DIR="$VERSION_DIR/hf${FIRST_APPLIED}"
    FIRST_MANIFEST="$FIRST_HF_DIR/hotfix_manifest.json"
    if [ -f "$FIRST_MANIFEST" ]; then
        # Check the first file from the manifest
        PROBE_PATH=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    m = json.load(f)
files = m.get('files', [])
if files:
    print(files[0]['path'])
" "$FIRST_MANIFEST" 2>/dev/null)
        if [ -n "$PROBE_PATH" ] && [ ! -f "/app/$PROBE_PATH" ]; then
            echo "  Container recreated — hotfix files lost, re-applying all"
            APPLIED_LIST=""
            rm -f "$APPLIED_MARKER"
        fi
    fi
fi

# Collect all hotfix directories sorted by number
HF_DIRS=()
for hf_dir in "$VERSION_DIR"/hf*/; do
    [ -d "$hf_dir" ] || continue
    HF_DIRS+=("$hf_dir")
done

if [ ${#HF_DIRS[@]} -eq 0 ]; then
    exit 0
fi

# Sort by hotfix number (numerical order)
IFS=$'\n' HF_DIRS=($(for d in "${HF_DIRS[@]}"; do
    num=$(basename "$d" | sed 's/hf//')
    echo "$num $d"
done | sort -n | awk '{print $2}'))
unset IFS

# Apply each unapplied hotfix in order
APPLIED_COUNT=0
TOTAL_FILES=0
for hf_dir in "${HF_DIRS[@]}"; do
    hf_num=$(basename "$hf_dir" | sed 's/hf//')

    # Skip if already applied
    if is_applied "$hf_num"; then
        continue
    fi

    MANIFEST="$hf_dir/hotfix_manifest.json"
    if [ ! -f "$MANIFEST" ]; then
        echo "  No manifest in $hf_dir — skipping hf${hf_num}"
        continue
    fi

    echo "Applying hotfix v${PLATFORM_VERSION}-hf${hf_num}..."

    # Apply hotfix files with checksum verification
    python3 -c "
import json, hashlib, shutil, sys
from pathlib import Path

manifest_path = Path(sys.argv[1])
app_dir = Path('/app')
hotfix_dir = manifest_path.parent

with open(manifest_path) as f:
    manifest = json.load(f)

files = manifest.get('files', [])
applied = 0
errors = 0

for entry in files:
    src_path = hotfix_dir / entry['path']
    dst_path = app_dir / entry['path']

    if not src_path.exists():
        print(f'  Missing: {entry[\"path\"]}')
        errors += 1
        continue

    # Verify checksum
    expected = entry.get('checksum', '')
    if expected.startswith('sha256:'):
        expected_hash = expected[7:]
        h = hashlib.sha256()
        with open(src_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        if h.hexdigest() != expected_hash:
            print(f'  Checksum mismatch: {entry[\"path\"]}')
            errors += 1
            continue

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dst_path)
    print(f'  Patched: {entry[\"path\"]}')
    applied += 1

if errors > 0:
    print(f'{errors} file(s) had errors')
    sys.exit(1)

print(f'Applied {applied} file(s)')
" "$MANIFEST"

    # Add this hotfix number to the applied list and write marker immediately
    # (so progress is preserved if a later hotfix fails)
    if [ -n "$APPLIED_LIST" ]; then
        APPLIED_LIST="${APPLIED_LIST},${hf_num}"
    else
        APPLIED_LIST="${hf_num}"
    fi
    echo "${PLATFORM_VERSION}:${APPLIED_LIST}" > "$APPLIED_MARKER"

    APPLIED_COUNT=$((APPLIED_COUNT + 1))
    echo "  Hotfix hf${hf_num} applied"
done

if [ "$APPLIED_COUNT" -eq 0 ]; then
    echo "  All hotfixes already applied"
    exit 0
fi

echo "Applied ${APPLIED_COUNT} hotfix(es) for v${PLATFORM_VERSION} (total applied: ${APPLIED_LIST})"
