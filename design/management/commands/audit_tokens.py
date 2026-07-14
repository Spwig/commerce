"""
Management command to audit and clean up design tokens.

Usage:
    python manage.py audit_tokens                  # Report-only audit
    python manage.py audit_tokens --sync-missing   # Sync tokens for themes with 0 tokens
    python manage.py audit_tokens --cleanup-orphans # Delete orphaned tokens
    python manage.py audit_tokens --dry-run --cleanup-orphans  # Preview cleanup
"""

from django.core.management.base import BaseCommand
from django.db.models import Count

from design.models import DesignToken
from design.theme_models import Theme


class Command(BaseCommand):
    help = "Audit design token health, sync missing theme tokens, and clean up orphans"

    def add_arguments(self, parser):
        parser.add_argument(
            "--sync-missing",
            action="store_true",
            help="Sync tokens for themes that have 0 DesignToken records",
        )
        parser.add_argument(
            "--cleanup-orphans",
            action="store_true",
            help="Delete orphaned tokens (source=theme with null theme_id, etc.)",
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="Show what would change without making changes"
        )

    def handle(self, *args, **options):
        sync_missing = options["sync_missing"]
        cleanup_orphans = options["cleanup_orphans"]
        dry_run = options["dry_run"]

        # Always run audit report
        self._audit_report()

        if sync_missing:
            self._sync_missing_themes(dry_run)

        if cleanup_orphans:
            self._cleanup_orphans(dry_run)

        if not sync_missing and not cleanup_orphans:
            self.stdout.write(
                "\nUse --sync-missing or --cleanup-orphans to take action. "
                "Add --dry-run to preview changes."
            )

    def _audit_report(self):
        """Print token health report."""
        self.stdout.write(self.style.SUCCESS(f"\n{'=' * 60}"))
        self.stdout.write(self.style.SUCCESS("Token Health Report"))
        self.stdout.write(self.style.SUCCESS(f"{'=' * 60}\n"))

        total = DesignToken.objects.count()
        active = DesignToken.objects.filter(is_active=True).count()
        self.stdout.write(f"Total tokens: {total} ({active} active)")

        # Counts by source
        self.stdout.write("\nBy source:")
        source_counts = (
            DesignToken.objects.values("source").annotate(cnt=Count("id")).order_by("source")
        )
        for row in source_counts:
            self.stdout.write(f"  {row['source']}: {row['cnt']}")

        # Counts by theme
        self.stdout.write("\nTheme token distribution:")
        themes = Theme.objects.all().order_by("name")
        for theme in themes:
            token_count = DesignToken.objects.filter(source="theme", theme=theme).count()
            status = "OK" if token_count > 0 else "NEEDS SYNC"
            style = self.style.SUCCESS if token_count > 0 else self.style.WARNING
            self.stdout.write(
                style(f"  {theme.name} (ID {theme.id}): {token_count} tokens [{status}]")
            )

        if not themes.exists():
            self.stdout.write(self.style.WARNING("  No themes installed"))

        # Orphaned tokens
        orphaned_theme = DesignToken.objects.filter(source="theme", theme__isnull=True).count()
        orphaned_component = DesignToken.objects.filter(
            source="component", component__isnull=True
        ).count()

        self.stdout.write("\nOrphaned tokens:")
        if orphaned_theme == 0 and orphaned_component == 0:
            self.stdout.write(self.style.SUCCESS("  None"))
        else:
            if orphaned_theme > 0:
                self.stdout.write(
                    self.style.WARNING(f"  {orphaned_theme} theme token(s) with no theme FK")
                )
            if orphaned_component > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"  {orphaned_component} component token(s) with no component FK"
                    )
                )

        # Brand builder token coverage
        brand_tokens = DesignToken.objects.filter(source="brand_builder")
        brand_count = brand_tokens.count()
        if brand_count > 0:
            self.stdout.write(f"\nBrand builder tokens: {brand_count}")

            # Check which brand tokens have matching theme tokens
            brand_names = set(brand_tokens.values_list("name", flat=True))
            theme_names = set(
                DesignToken.objects.filter(source="theme").values_list("name", flat=True)
            )
            matched = brand_names & theme_names
            unmatched = brand_names - theme_names

            self.stdout.write(f"  {len(matched)} have matching theme tokens")
            if unmatched:
                self.stdout.write(
                    self.style.WARNING(
                        f"  {len(unmatched)} have no matching theme token (may be stale)"
                    )
                )
                for name in sorted(unmatched)[:10]:
                    self.stdout.write(f"    - {name}")
                if len(unmatched) > 10:
                    self.stdout.write(f"    ... and {len(unmatched) - 10} more")

        self.stdout.write(f"\n{'=' * 60}\n")

    def _sync_missing_themes(self, dry_run):
        """Sync tokens for themes that have 0 DesignToken records."""
        from design.token_sync_service import TokenSyncService

        self.stdout.write(self.style.SUCCESS("\nSyncing missing theme tokens..."))

        themes_needing_sync = []
        for theme in Theme.objects.all():
            if DesignToken.objects.filter(source="theme", theme=theme).count() == 0:
                # Check if theme has tokens in manifest
                tokens = theme.manifest.get("tokens", {}) if theme.manifest else {}
                if tokens:
                    themes_needing_sync.append(theme)

        if not themes_needing_sync:
            self.stdout.write(self.style.SUCCESS("  All themes have tokens synced"))
            return

        for theme in themes_needing_sync:
            if dry_run:
                from design.token_sync_service import TokenSyncService

                token_names = TokenSyncService.get_all_theme_token_names(theme)
                self.stdout.write(
                    f"  [DRY RUN] Would sync {len(token_names)} tokens for {theme.name}"
                )
            else:
                created, updated, deleted = TokenSyncService.sync_theme_to_design_tokens(theme)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {theme.name}: {created} created, {updated} updated, {deleted} deleted"
                    )
                )

    def _cleanup_orphans(self, dry_run):
        """Delete orphaned tokens."""
        self.stdout.write(self.style.SUCCESS("\nCleaning up orphaned tokens..."))

        # Theme tokens with no theme FK
        orphaned_theme_qs = DesignToken.objects.filter(source="theme", theme__isnull=True)
        orphaned_theme_count = orphaned_theme_qs.count()

        # Component tokens with no component FK
        orphaned_component_qs = DesignToken.objects.filter(
            source="component", component__isnull=True
        )
        orphaned_component_count = orphaned_component_qs.count()

        total = orphaned_theme_count + orphaned_component_count

        if total == 0:
            self.stdout.write(self.style.SUCCESS("  No orphaned tokens found"))
            return

        if dry_run:
            if orphaned_theme_count:
                self.stdout.write(
                    f"  [DRY RUN] Would delete {orphaned_theme_count} orphaned theme token(s)"
                )
            if orphaned_component_count:
                self.stdout.write(
                    f"  [DRY RUN] Would delete {orphaned_component_count} orphaned component token(s)"
                )
        else:
            deleted = 0
            if orphaned_theme_count:
                count, _ = orphaned_theme_qs.delete()
                deleted += count
                self.stdout.write(self.style.SUCCESS(f"  Deleted {count} orphaned theme token(s)"))
            if orphaned_component_count:
                count, _ = orphaned_component_qs.delete()
                deleted += count
                self.stdout.write(
                    self.style.SUCCESS(f"  Deleted {count} orphaned component token(s)")
                )

            self.stdout.write(self.style.SUCCESS(f"  Total deleted: {deleted}"))
