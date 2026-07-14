"""
Fast incremental static file collection for component statics only.

Instead of running full collectstatic (which re-hashes all 15,000+ files),
this command:
1. Reads the existing staticfiles.json manifest (pre-baked at build time)
2. Finds only component static files (ComponentStaticFinder + IntegrationStaticFinder)
3. Copies + hashes only those files into STATIC_ROOT
4. Merges the new entries into the existing manifest
5. Compresses only the new files (.gz, .br)

Reduces container startup from 3-5 minutes to 5-10 seconds for hosted instances
that have components installed on the components_data volume.
"""

import hashlib
import json
import shutil
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Incrementally collect component static files into STATIC_ROOT"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List files that would be collected without copying",
        )

    def handle(self, *args, **options):
        start = time.monotonic()
        dry_run = options["dry_run"]
        verbosity = options["verbosity"]

        static_root = Path(settings.STATIC_ROOT)
        manifest_path = static_root / "staticfiles.json"

        # Load existing manifest (pre-baked at build time)
        manifest = {}
        if manifest_path.exists():
            try:
                with open(manifest_path) as f:
                    data = json.load(f)
                # WhiteNoise manifest format: {"version": "1.0", "paths": {...}}
                manifest = data.get("paths", data)
            except (json.JSONDecodeError, KeyError):
                self.stderr.write(
                    self.style.WARNING("Could not parse existing manifest, starting fresh")
                )

        # Instantiate component finders
        from component_updates.finders import (
            ComponentStaticFinder,
            IntegrationStaticFinder,
        )

        finders = [ComponentStaticFinder(), IntegrationStaticFinder()]

        collected = 0
        skipped = 0

        for finder in finders:
            for rel_path, storage in finder.list([]):
                source_path = Path(storage.path(rel_path))

                if not source_path.exists():
                    continue

                # Compute content hash (same algorithm as Django's ManifestStaticFilesStorage)
                file_hash = self._md5_hash(source_path)
                hashed_name = self._hashed_name(rel_path, file_hash)

                # Check if this file is already in the manifest with same hash
                if rel_path in manifest:
                    existing_hashed = manifest[rel_path]
                    if existing_hashed == hashed_name:
                        skipped += 1
                        continue

                if dry_run:
                    self.stdout.write(f"  Would collect: {rel_path} -> {hashed_name}")
                    collected += 1
                    continue

                # Copy original file
                dest_path = static_root / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(source_path), str(dest_path))

                # Copy hashed version
                hashed_dest = static_root / hashed_name
                hashed_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(source_path), str(hashed_dest))

                # Compress both versions
                self._compress(dest_path)
                self._compress(hashed_dest)

                # Update manifest
                manifest[rel_path] = hashed_name
                collected += 1

                if verbosity >= 2:
                    self.stdout.write(f"  {rel_path} -> {hashed_name}")

        if not dry_run and collected > 0:
            # Write updated manifest
            manifest_data = {"version": "1.0", "paths": manifest}
            with open(manifest_path, "w") as f:
                json.dump(manifest_data, f, indent=2)

        elapsed = time.monotonic() - start
        action = "Would collect" if dry_run else "Collected"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} {collected} component static files "
                f"({skipped} unchanged) in {elapsed:.1f}s"
            )
        )

    def _md5_hash(self, path, block_size=65536):
        """Compute MD5 hash of a file (matches Django's ManifestStaticFilesStorage)."""
        md5 = hashlib.md5()
        with open(path, "rb") as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()[:12]

    def _hashed_name(self, name, file_hash):
        """Generate hashed filename: name.HASH.ext"""
        path = Path(name)
        return str(path.with_suffix(f".{file_hash}{path.suffix}"))

    def _compress(self, path):
        """Create .gz and .br compressed versions of a file."""
        import gzip

        # gzip
        gz_path = Path(str(path) + ".gz")
        try:
            with (
                open(path, "rb") as f_in,
                gzip.open(gz_path, "wb", compresslevel=9) as f_out,
            ):
                shutil.copyfileobj(f_in, f_out)
        except Exception:
            pass

        # brotli (optional — may not be installed)
        try:
            import brotli

            br_path = Path(str(path) + ".br")
            with open(path, "rb") as f_in:
                data = f_in.read()
                compressed = brotli.compress(data, quality=6)
                with open(br_path, "wb") as f_out:
                    f_out.write(compressed)
        except ImportError:
            pass
        except Exception:
            pass
