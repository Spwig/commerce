"""
Orchestrator for all seed data commands.

Usage:
    python manage.py seed              # Run all seeds in dependency order
    python manage.py seed --force      # Force re-run all seeds
    python manage.py seed --dry-run    # Show what would run
    python manage.py seed --only email_templates  # Run specific seed
    python manage.py seed --list       # Show all seeds and their status
"""

import time

from django.core.management import call_command
from django.core.management.base import BaseCommand

# Seed registry: ordered list of (seed_name, management_command_name)
# Order defines execution sequence -- dependencies are implicit in ordering.
SEED_REGISTRY = [
    # Phase 1 - Foundation (no dependencies)
    ("site_defaults", "seed_site_defaults"),
    ("languages", "populate_languages"),
    ("image_presets", "setup_system_presets"),
    ("staff_roles", "create_default_roles"),
    # Phase 2 - Reference data
    ("country_mappings", "seed_country_mappings"),
    ("geoip_provider", "geoip_seed"),
    ("customer_segments", "seed_customer_segments"),
    ("tax_presets", "seed_tax_presets"),
    ("carrier_presets", "seed_carrier_presets"),
    ("default_warehouse", "setup_default_warehouse", {"skip_stock_migration": True}),
    ("seo_provider", "seed_seo_provider"),
    # Phase 3 - Design system (widgets before headers, menus before headers)
    ("design_tokens", "seed_design_tokens"),
    ("page_tiers", "seed_page_tiers"),
    ("trust_badges", "seed_trust_badges"),
    ("default_widgets", "create_default_widgets"),
    ("default_menus", "create_default_menus"),
    ("header_presets", "create_header_presets"),
    # Phase 4 - Content (depends on design system)
    ("default_pages", "seed_default_pages"),
    ("page_elements", "seed_page_elements"),
    ("email_account", "seed_email_account"),
    ("email_templates", "seed_email_templates"),
    ("affiliate_form", "seed_affiliate_form"),
    # Phase 5 - Content indexing (depends on content)
    # sync_help --no-index: load help topics without generating embeddings.
    # Embeddings are pre-built on GPU and shipped as a fixture.
    ("help_content", "sync_help", {"no_index": True}),
    ("help_embeddings", "load_embeddings_fixture", {"run_async": True}),
    ("ui_strings", "sync_ui_string_registry"),
    # Phase 6 - Bundled components (independent, last because heaviest)
    ("bundled_components", "install_bundled_components"),
]


class Command(BaseCommand):
    help = "Run all seed data commands in dependency order"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force re-run all seeds regardless of version",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making changes",
        )
        parser.add_argument(
            "--only",
            type=str,
            help="Run only the specified seed (by seed_name)",
        )
        parser.add_argument(
            "--list",
            action="store_true",
            dest="list_seeds",
            help="List all seeds with their version status",
        )

    def handle(self, *args, **options):
        if options["list_seeds"]:
            return self._list_seeds()

        seeds_to_run = SEED_REGISTRY
        if options["only"]:
            seeds_to_run = [s for s in SEED_REGISTRY if s[0] == options["only"]]
            if not seeds_to_run:
                valid = ", ".join(s[0] for s in SEED_REGISTRY)
                self.stderr.write(
                    self.style.ERROR(f"Unknown seed: '{options['only']}'\nValid seeds: {valid}")
                )
                return

        total = len(seeds_to_run)
        self.stdout.write(self.style.SUCCESS(f"\nRunning {total} seed commands...\n"))

        start_time = time.time()
        succeeded = 0
        failed = 0

        for entry in seeds_to_run:
            seed_name = entry[0]
            command_name = entry[1]
            fixed_kwargs = entry[2] if len(entry) > 2 else {}
            try:
                kwargs = dict(fixed_kwargs)
                # Pass flags to commands that support them
                if options["force"]:
                    kwargs["force"] = True
                if options["dry_run"]:
                    kwargs["dry_run"] = True

                # Some legacy commands use different flag names or don't
                # support --force/--dry-run. Try with flags first, then
                # fall back to calling without them.
                try:
                    call_command(command_name, **kwargs)
                except TypeError:
                    # Command doesn't accept these kwargs
                    call_command(command_name, **fixed_kwargs)

                succeeded += 1
            except Exception as e:
                failed += 1
                self.stderr.write(self.style.ERROR(f"  FAILED: {seed_name} - {e}"))

        elapsed = time.time() - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeed complete: {succeeded} succeeded, {failed} failed ({elapsed:.1f}s)\n"
            )
        )

        # Post-conditions: verify critical first-boot invariants actually hold
        # after seeding. Guards against a silent regression (e.g. a preinstalled
        # manifest build dropping every theme) that leaves the store technically
        # booted but visibly broken. Skipped on --dry-run (nothing was created).
        if not options["dry_run"]:
            ran_names = {s[0] for s in seeds_to_run}
            self._verify_postconditions(ran_names)

    def _verify_postconditions(self, ran_names):
        """Assert first-boot invariants a themeless/CSS-less store would violate.

        Runs after seeding so a regression surfaces loudly in the boot log
        instead of silently shipping a store that renders on fallback CSS.
        Intentionally non-fatal: a degraded-but-serving store beats an aborted
        boot (`set -e` in docker-entrypoint.sh would turn a raise into a boot
        failure over what is only a styling problem).
        """
        # Only meaningful once theme installation has had a chance to run.
        if "bundled_components" not in ran_names:
            return

        self.stdout.write("Verifying post-conditions...")
        self._verify_active_theme()

    def _verify_active_theme(self):
        """A storefront theme must be installed, active, and have compiled CSS.

        Two distinct failure modes both produce the fallback-CSS symptom:
        no active theme at all, or an active theme whose compiled_css is empty
        (the `theme_css` tag only emits the stylesheet link when get_css_url()
        is truthy).
        """
        from design.theme_utils import get_active_theme

        theme = get_active_theme()
        if theme is None:
            self._postcondition_error(
                "No storefront theme is installed or active.",
                "install_bundled_components installed no theme -- the "
                "preinstalled manifest likely contains no 'theme' components.",
            )
            return

        if not theme.get_css_url():
            self._postcondition_error(
                f"Active theme '{theme.slug}' has no compiled CSS.",
                "The theme row exists but compiled_css is empty, so the "
                "storefront still renders on fallback CSS.",
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f"  OK: active storefront theme '{theme.slug}' with compiled CSS")
        )

    def _postcondition_error(self, problem, cause):
        bar = "=" * 72
        self.stderr.write(
            self.style.ERROR(
                f"\n{bar}\n"
                f"POST-CONDITION FAILED: {problem}\n"
                f"The storefront will render with fallback CSS only.\n\n"
                f"Cause: {cause}\n\n"
                f"Fix:\n"
                f"  python manage.py build_preinstalled_packages --type theme\n"
                f"  python manage.py seed --only bundled_components\n"
                f"{bar}\n"
            )
        )

    def _list_seeds(self):
        from core.models import SeedVersion

        versions = {sv.seed_name: sv for sv in SeedVersion.objects.all()}

        self.stdout.write(self.style.SUCCESS("\nSeed Registry:\n"))
        self.stdout.write(f"  {'Name':<25} {'Command':<35} {'Status'}")
        self.stdout.write(f"  {'─' * 25} {'─' * 35} {'─' * 25}")

        for entry in SEED_REGISTRY:
            seed_name = entry[0]
            command_name = entry[1]
            sv = versions.get(seed_name)
            if sv:
                status = f"v{sv.version} applied {sv.applied_at:%Y-%m-%d %H:%M}"
            else:
                status = "not yet applied"
            self.stdout.write(f"  {seed_name:<25} {command_name:<35} {status}")

        self.stdout.write("")
