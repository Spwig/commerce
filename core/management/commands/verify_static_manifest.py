"""
Verify the collected static manifest is complete and consistent.

Guards against a broken pre-baked static layer: the entrypoint's fast path
trusts the /app/staticfiles/.prebaked marker and skips the full collectstatic,
running only an incremental component-static sync. If the pre-baked core
manifest is missing, or its hashed files were never shipped, WhiteNoise +
NonStrictManifestStorage silently fall back and every core CSS/JS/favicon 404s
— the storefront renders completely unstyled with no hard error to flag it.

This command re-lists the CORE static files (the standard Django finders, i.e.
everything except the component finders) and asserts that each one is present
in staticfiles.json AND that its hashed target actually exists on disk. It
exits non-zero when the manifest is incomplete so the caller (the entrypoint)
can repair it with a full collectstatic.
"""

import json
import sys
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

# Tolerate a tiny fraction of discrepancies (e.g. odd vendor assets) before
# declaring the manifest broken. A fraction (rather than an absolute count)
# scales with the number of core files: a healthy manifest has ~0 misses, while
# the real failure mode misses nearly all of them — so this cleanly separates
# the two regardless of how many static files the install ships.
DISCREPANCY_TOLERANCE_FRACTION = 0.05


class Command(BaseCommand):
    help = "Verify the static manifest covers all core assets (exit 1 if incomplete)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--verbose-misses",
            action="store_true",
            help="List the missing core static files (up to 20)",
        )

    def handle(self, *args, **options):
        complete, stats, misses = self.check_manifest()

        if stats.get("skipped"):
            self.stdout.write("Static manifest check skipped (manifest storage not in use)")
            return

        summary = (
            f"core files: {stats['total']}, "
            f"missing from manifest: {stats['missing_manifest']}, "
            f"hashed file absent on disk: {stats['missing_disk']}"
        )

        if complete:
            self.stdout.write(self.style.SUCCESS(f"Static manifest OK ({summary})"))
            return

        self.stderr.write(self.style.ERROR(f"Static manifest INCOMPLETE ({summary})"))
        if options["verbose_misses"]:
            for m in misses[:20]:
                self.stderr.write(f"  missing: {m}")
        # Non-zero exit so the entrypoint knows to repair with full collectstatic.
        sys.exit(1)

    def check_manifest(self):
        """Return (is_complete, stats, missing_paths) for the core static manifest.

        Kept separate from handle() so it can be exercised directly by tests.
        """
        # In DEBUG the staticfiles backend isn't the hashing manifest storage and
        # no staticfiles.json exists — nothing to verify.
        backend = settings.STORAGES.get("staticfiles", {}).get("BACKEND", "")
        if "Manifest" not in backend:
            return True, {"skipped": True}, []

        static_root = Path(settings.STATIC_ROOT)
        manifest_path = static_root / "staticfiles.json"

        if not manifest_path.exists():
            return False, {"total": 0, "missing_manifest": 0, "missing_disk": 0}, []

        try:
            with open(manifest_path) as fh:
                data = json.load(fh)
            paths = data.get("paths", data)
        except (json.JSONDecodeError, OSError):
            return False, {"total": 0, "missing_manifest": 0, "missing_disk": 0}, []

        core_files = self._iter_core_static_files()

        missing_manifest = 0
        missing_disk = 0
        misses = []
        for rel_path in core_files:
            hashed = paths.get(rel_path)
            if hashed is None:
                missing_manifest += 1
                misses.append(rel_path)
            elif not (static_root / hashed).exists():
                missing_disk += 1
                misses.append(rel_path)

        total = len(core_files)
        stats = {
            "total": total,
            "missing_manifest": missing_manifest,
            "missing_disk": missing_disk,
        }
        # Incomplete if there are core files but the share of discrepancies
        # exceeds the tolerance fraction (or there are no core files at all).
        discrepancies = missing_manifest + missing_disk
        complete = total > 0 and discrepancies <= total * DISCREPANCY_TOLERANCE_FRACTION
        return complete, stats, misses

    def _iter_core_static_files(self):
        """Set of relative paths for CORE static files (standard Django finders).

        The component finders are deliberately excluded — their assets live on a
        runtime volume and are synced by collect_component_statics. Extracted as
        its own method so tests can substitute a deterministic set.
        """
        from django.contrib.staticfiles.finders import (
            AppDirectoriesFinder,
            FileSystemFinder,
        )

        core_files = set()
        for finder in (FileSystemFinder(), AppDirectoriesFinder()):
            for rel_path, _storage in finder.list([]):
                core_files.add(rel_path)
        return core_files
