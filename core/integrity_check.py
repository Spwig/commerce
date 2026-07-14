"""
Runtime Integrity Verification for Spwig
==========================================
Add this to your Django app's AppConfig.ready() or wsgi.py to verify
that compiled files haven't been tampered with at startup.

Usage in wsgi.py:
    from integrity_check import verify_integrity
    verify_integrity("/app/build")

Usage in AppConfig:
    class CoreConfig(AppConfig):
        def ready(self):
            from integrity_check import verify_integrity
            verify_integrity(settings.BASE_DIR)
"""

import hashlib
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger("spwig.integrity")


class IntegrityError(Exception):
    """Raised when file integrity verification fails."""

    pass


def compute_hash(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_integrity(
    base_dir: str | Path,
    strict: bool = True,
    check_subset: list[str] | None = None,
) -> bool:
    """
    Verify file integrity against the build manifest.

    Args:
        base_dir:     Root of the compiled project
        strict:       If True, raise IntegrityError on failure.
                      If False, log warnings and return False.
        check_subset: Optional list of relative paths to check.
                      If None, checks everything in the manifest.

    Returns:
        True if all checks pass, False otherwise.
    """
    base_dir = Path(base_dir)
    manifest_path = base_dir / ".integrity_manifest.json"

    if not manifest_path.exists():
        msg = f"Integrity manifest not found: {manifest_path}"
        if strict:
            raise IntegrityError(msg)
        logger.warning(msg)
        return False

    try:
        manifest = json.loads(manifest_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        msg = f"Failed to read integrity manifest: {e}"
        if strict:
            raise IntegrityError(msg)
        logger.warning(msg)
        return False

    files_to_check = manifest.get("files", {})
    if check_subset:
        files_to_check = {k: v for k, v in files_to_check.items() if k in check_subset}

    tampered = []
    missing = []

    for rel_path, expected in files_to_check.items():
        filepath = base_dir / rel_path

        if not filepath.exists():
            missing.append(rel_path)
            continue

        actual_hash = compute_hash(filepath)
        if actual_hash != expected["sha256"]:
            tampered.append(rel_path)

    if tampered or missing:
        details = []
        if tampered:
            details.append(f"Modified files: {', '.join(tampered)}")
        if missing:
            details.append(f"Missing files: {', '.join(missing)}")

        msg = f"Integrity check FAILED — {'; '.join(details)}"

        if strict:
            logger.critical(msg)
            raise IntegrityError(msg)
        else:
            logger.warning(msg)
            return False

    logger.info(f"Integrity check passed: {len(files_to_check)} files verified")
    return True


def verify_or_die(base_dir: str | Path):
    """
    Hard exit if integrity fails. Use in wsgi.py / asgi.py.

    If no manifest exists (unprotected/dev build), silently passes.
    Only fatal when manifest exists but verification fails (tampering).
    """
    base_dir = Path(base_dir)
    manifest_path = base_dir / ".integrity_manifest.json"

    if not manifest_path.exists():
        # No manifest = not a protected build, nothing to verify
        return

    try:
        verify_integrity(base_dir, strict=True)
    except IntegrityError as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(78)  # EX_CONFIG
