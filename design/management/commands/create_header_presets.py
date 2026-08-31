"""
Management command to create default header presets
Following rules.md: NO inline colors, uses theme CSS variables

Updated for new architecture where:
- layout_type determines preset class (.header-preset-{type})
- Theme CSS provides all visual styling via preset-specific tokens
- zone_overrides only stores merchant customizations (empty for base presets)
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from design.header_footer_models import HeaderTemplate, Menu, Widget, WidgetPlacement

User = get_user_model()

# Namespace reserving preset-owned widgets so their names never collide with the
# merchant-facing default widgets from ``create_default_widgets``.
PRESET_WIDGET_PREFIX = "Header Preset: "

PRESET_SLUGS = [
    "preset-classic-ecommerce",
    "preset-centered-boutique",
    "preset-minimal-startup",
    "preset-mega-menu-store",
    "preset-promotional-marketing",
    "preset-split-navigation",
]


class Command(BaseCommand):
    help = "Creates 6 default header presets for the header builder"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing presets and recreate them",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            deleted, _ = HeaderTemplate.objects.filter(slug__in=PRESET_SLUGS).delete()
            self.stdout.write(f"Deleted {deleted} existing preset objects")

        self.stdout.write("Creating header presets...")

        # Get or create system user for presets
        system_user, _ = User.objects.get_or_create(
            username="system", defaults={"is_staff": True, "is_superuser": True}
        )

        # Get existing widgets
        widgets = self.get_or_create_widgets()

        # Create all 6 presets
        presets = [
            self.create_classic_ecommerce(system_user, widgets),
            self.create_centered_boutique(system_user, widgets),
            self.create_minimal_startup(system_user, widgets),
            self.create_mega_menu_store(system_user, widgets),
            self.create_promotional_marketing(system_user, widgets),
            self.create_split_navigation(system_user, widgets),
        ]

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(presets)} header presets"))

    def get_or_create_widgets(self):
        """Get or create dedicated preset widgets by a preset-reserved name.

        Widgets are looked up by an exact (widget_type, name) pair whose name is
        namespaced with PRESET_WIDGET_PREFIX so it can never collide with the
        default widgets created by ``create_default_widgets`` (which use the
        bare names, e.g. "Main Menu"). This guarantees a preset never adopts a
        merchant-customized widget of the same type and inherits its custom
        config (e.g. a menu widget already bound to an unrelated menu_id).
        """
        widget_defaults = {
            "logo": {"name": f"{PRESET_WIDGET_PREFIX}Site Logo", "config": {"height": 40}},
            "menu": {"name": f"{PRESET_WIDGET_PREFIX}Main Menu", "config": {"style": "horizontal"}},
            "search": {"name": f"{PRESET_WIDGET_PREFIX}Search Bar", "config": {}},
            "cart": {
                "name": f"{PRESET_WIDGET_PREFIX}Shopping Cart",
                "config": {"show_count": True},
            },
            "account": {"name": f"{PRESET_WIDGET_PREFIX}Account Menu", "config": {}},
            "language": {"name": f"{PRESET_WIDGET_PREFIX}Language Selector", "config": {}},
        }

        widgets = {}
        for key, defaults in widget_defaults.items():
            widget, created = Widget.objects.get_or_create(
                widget_type=key,
                name=defaults["name"],
                defaults={"config": defaults["config"], "is_active": True},
            )
            if created:
                self.stdout.write(f"  Created widget: {widget.name}")
            widgets[key] = widget

        # Ensure menu widget is linked to main-navigation menu
        menu_widget = widgets["menu"]
        if not menu_widget.config.get("menu_id"):
            main_nav = Menu.objects.filter(slug="main-navigation", is_active=True).first()
            if main_nav:
                menu_widget.config["menu_id"] = main_nav.id
                menu_widget.config["display_type"] = "horizontal"
                menu_widget.save()
                self.stdout.write(f'  Linked menu widget to "{main_nav.name}"')

        return widgets

    def _prune_foreign_placements(self, header, widgets):
        """Drop placements from earlier runs that reference non-preset widgets.

        Older versions of this command placed merchant-facing widgets into
        preset zones. Those placements survive a plain rerun (``_place`` keys on
        the widget, so the new preset-owned widget yields a separate row), which
        would leave a preset rendering both the stale merchant widget and its
        replacement. Removing every placement not owned by a preset widget keeps
        reruns idempotent without needing ``--reset``.
        """
        preset_widget_ids = [widget.id for widget in widgets.values()]
        WidgetPlacement.objects.filter(header=header).exclude(
            widget_id__in=preset_widget_ids
        ).delete()

    def _place(self, header, widget, zone, order, override_config=None):
        """Idempotently place a widget in a header zone (safe to re-run)."""
        WidgetPlacement.objects.update_or_create(
            header=header,
            widget=widget,
            zone=zone,
            defaults={"order": order, "override_config": override_config or {}},
        )

    def create_classic_ecommerce(self, user, widgets):
        """Classic layout: logo + search top, menu bar below"""
        with transaction.atomic():
            header, created = HeaderTemplate.objects.get_or_create(
                slug="preset-classic-ecommerce",
                defaults={
                    "name": "Classic E-commerce",
                    "description": "Traditional online store layout with search bar, actions, and navigation bar",
                    "layout_type": "classic",
                    "is_preset": True,
                    "is_default": True,
                    "preset_category": "ecommerce",
                    "is_active": True,
                    "is_sticky": True,
                    "created_by": user,
                    "zone_overrides": {},
                    "zone_layouts": {
                        "main-header": ["left", "center", "right"],
                        "bottom-bar": ["full"],
                    },
                    "enable_notification_zone": True,
                },
            )

            self._prune_foreign_placements(header, widgets)
            # Main header: logo left, search center, utility right
            self._place(header, widgets["logo"], "main-header_left", 0)
            self._place(header, widgets["search"], "main-header_center", 0)
            self._place(header, widgets["cart"], "main-header_right", 0)
            self._place(header, widgets["account"], "main-header_right", 1)
            self._place(header, widgets["language"], "main-header_right", 2)
            # Bottom bar: navigation
            self._place(header, widgets["menu"], "bottom-bar_full", 0)

        if created:
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header

    def create_centered_boutique(self, user, widgets):
        """Boutique layout: utility icons flanking centered logo, nav below"""
        with transaction.atomic():
            header, created = HeaderTemplate.objects.get_or_create(
                slug="preset-centered-boutique",
                defaults={
                    "name": "Centered Boutique",
                    "description": "Elegant centered logo design perfect for fashion and lifestyle brands",
                    "layout_type": "boutique",
                    "is_preset": True,
                    "preset_category": "modern",
                    "is_active": True,
                    "is_sticky": True,
                    "created_by": user,
                    "zone_overrides": {},
                    "zone_layouts": {
                        "main-header": ["left", "center", "right"],
                        "bottom-bar": ["full"],
                    },
                    "enable_notification_zone": True,
                },
            )

            self._prune_foreign_placements(header, widgets)
            # Main header: search left, logo center (large), cart/account/lang right
            self._place(header, widgets["search"], "main-header_left", 0)
            self._place(
                header, widgets["logo"], "main-header_center", 0, override_config={"height": 60}
            )
            self._place(header, widgets["cart"], "main-header_right", 0)
            self._place(header, widgets["account"], "main-header_right", 1)
            self._place(header, widgets["language"], "main-header_right", 2)
            # Bottom bar: centered navigation
            self._place(header, widgets["menu"], "bottom-bar_full", 0)

        if created:
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header

    def create_minimal_startup(self, user, widgets):
        """Minimal layout: logo left, menu + account right"""
        with transaction.atomic():
            header, created = HeaderTemplate.objects.get_or_create(
                slug="preset-minimal-startup",
                defaults={
                    "name": "Minimal Startup",
                    "description": "Clean, modern single-row layout perfect for SaaS and tech companies",
                    "layout_type": "minimal",
                    "is_preset": True,
                    "preset_category": "minimal",
                    "is_active": True,
                    "is_sticky": True,
                    "created_by": user,
                    "zone_overrides": {},
                    "zone_layouts": {"main-header": ["left", "right"]},
                    "enable_notification_zone": False,
                },
            )

            self._prune_foreign_placements(header, widgets)
            self._place(header, widgets["logo"], "main-header_left", 0)
            self._place(header, widgets["menu"], "main-header_right", 0)
            self._place(header, widgets["cart"], "main-header_right", 1)
            self._place(header, widgets["account"], "main-header_right", 2)

        if created:
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header

    def create_mega_menu_store(self, user, widgets):
        """Mega layout: full header with mega menu navigation bar"""
        with transaction.atomic():
            header, created = HeaderTemplate.objects.get_or_create(
                slug="preset-mega-menu-store",
                defaults={
                    "name": "Mega Menu Store",
                    "description": "Perfect for large catalogs with expandable mega menu navigation",
                    "layout_type": "mega",
                    "is_preset": True,
                    "preset_category": "ecommerce",
                    "is_active": True,
                    "is_sticky": True,
                    "created_by": user,
                    "zone_overrides": {},
                    "zone_layouts": {
                        "main-header": ["left", "center", "right"],
                        "mega-menu-bar": ["full"],
                    },
                    "enable_notification_zone": True,
                },
            )

            self._prune_foreign_placements(header, widgets)
            # Main header: logo, search, utility icons
            self._place(header, widgets["logo"], "main-header_left", 0)
            self._place(header, widgets["search"], "main-header_center", 0)
            self._place(header, widgets["cart"], "main-header_right", 0)
            self._place(header, widgets["account"], "main-header_right", 1)
            self._place(header, widgets["language"], "main-header_right", 2)
            # Mega menu bar: category navigation
            self._place(header, widgets["menu"], "mega-menu-bar_full", 0)

        if created:
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header

    def create_promotional_marketing(self, user, widgets):
        """Promotional layout: header with navigation bar below for campaigns"""
        with transaction.atomic():
            header, created = HeaderTemplate.objects.get_or_create(
                slug="preset-promotional-marketing",
                defaults={
                    "name": "Promotional Marketing",
                    "description": "Perfect for sales campaigns with navigation bar and promotional banner",
                    "layout_type": "promotional",
                    "is_preset": True,
                    "preset_category": "ecommerce",
                    "is_active": True,
                    "is_sticky": True,
                    "created_by": user,
                    "zone_overrides": {},
                    "zone_layouts": {
                        "main-header": ["left", "center", "right"],
                        "bottom-bar": ["full"],
                    },
                    "enable_notification_zone": True,
                },
            )

            self._prune_foreign_placements(header, widgets)
            # Main header: logo, search, utility icons
            self._place(header, widgets["logo"], "main-header_left", 0)
            self._place(header, widgets["search"], "main-header_center", 0)
            self._place(header, widgets["cart"], "main-header_right", 0)
            self._place(header, widgets["account"], "main-header_right", 1)
            self._place(header, widgets["language"], "main-header_right", 2)
            # Bottom bar: navigation
            self._place(header, widgets["menu"], "bottom-bar_full", 0)

        if created:
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header

    def create_split_navigation(self, user, widgets):
        """Split layout: branding + utility top, navigation below"""
        with transaction.atomic():
            header, created = HeaderTemplate.objects.get_or_create(
                slug="preset-split-navigation",
                defaults={
                    "name": "Split Navigation",
                    "description": "Two-row layout perfect for content-heavy sites and editorial commerce",
                    "layout_type": "split",
                    "is_preset": True,
                    "preset_category": "classic",
                    "is_active": True,
                    "is_sticky": True,
                    "created_by": user,
                    "zone_overrides": {},
                    "zone_layouts": {
                        "top-bar": ["left", "right"],
                        "main-header": ["left", "center", "right"],
                    },
                    "enable_notification_zone": False,
                },
            )

            self._prune_foreign_placements(header, widgets)
            # Top bar: logo + utility
            self._place(header, widgets["logo"], "top-bar_left", 0)
            self._place(header, widgets["search"], "top-bar_right", 0)
            self._place(header, widgets["cart"], "top-bar_right", 1)
            self._place(header, widgets["account"], "top-bar_right", 2)
            self._place(header, widgets["language"], "top-bar_right", 3)
            # Main header: full-width navigation
            self._place(header, widgets["menu"], "main-header_left", 0)

        if created:
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header
