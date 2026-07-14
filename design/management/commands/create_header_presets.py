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

from design.header_footer_models import HeaderTemplate, Menu, Widget, WidgetPlacement

User = get_user_model()

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
        """Get existing widgets by type, or create them if none exist.

        Uses widget_type only for lookup to avoid name mismatches
        (e.g. 'Account' vs 'Account Menu').
        """
        widget_defaults = {
            "logo": {"name": "Site Logo", "config": {"height": 40}},
            "menu": {"name": "Main Menu", "config": {"style": "horizontal"}},
            "search": {"name": "Search Bar", "config": {}},
            "cart": {"name": "Shopping Cart", "config": {"show_count": True}},
            "account": {"name": "Account Menu", "config": {}},
            "language": {"name": "Language Selector", "config": {}},
        }

        widgets = {}
        for key, defaults in widget_defaults.items():
            widget = Widget.objects.filter(widget_type=key, is_active=True).first()
            if not widget:
                widget = Widget.objects.create(
                    widget_type=key,
                    name=defaults["name"],
                    config=defaults["config"],
                    is_active=True,
                )
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

    def create_classic_ecommerce(self, user, widgets):
        """Classic layout: logo + search top, menu bar below"""
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

        if created:
            # Main header: logo left, search center, utility right
            WidgetPlacement.objects.create(
                header=header, widget=widgets["logo"], zone="main-header_left", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["search"], zone="main-header_center", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["cart"], zone="main-header_right", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["account"], zone="main-header_right", order=1
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["language"], zone="main-header_right", order=2
            )
            # Bottom bar: navigation
            WidgetPlacement.objects.create(
                header=header, widget=widgets["menu"], zone="bottom-bar_full", order=0
            )
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header

    def create_centered_boutique(self, user, widgets):
        """Boutique layout: utility icons flanking centered logo, nav below"""
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

        if created:
            # Main header: search left, logo center (large), cart/account/lang right
            WidgetPlacement.objects.create(
                header=header, widget=widgets["search"], zone="main-header_left", order=0
            )
            WidgetPlacement.objects.create(
                header=header,
                widget=widgets["logo"],
                zone="main-header_center",
                order=0,
                override_config={"height": 60},
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["cart"], zone="main-header_right", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["account"], zone="main-header_right", order=1
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["language"], zone="main-header_right", order=2
            )
            # Bottom bar: centered navigation
            WidgetPlacement.objects.create(
                header=header, widget=widgets["menu"], zone="bottom-bar_full", order=0
            )
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header

    def create_minimal_startup(self, user, widgets):
        """Minimal layout: logo left, menu + account right"""
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

        if created:
            WidgetPlacement.objects.create(
                header=header, widget=widgets["logo"], zone="main-header_left", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["menu"], zone="main-header_right", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["cart"], zone="main-header_right", order=1
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["account"], zone="main-header_right", order=2
            )
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header

    def create_mega_menu_store(self, user, widgets):
        """Mega layout: full header with mega menu navigation bar"""
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

        if created:
            # Main header: logo, search, utility icons
            WidgetPlacement.objects.create(
                header=header, widget=widgets["logo"], zone="main-header_left", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["search"], zone="main-header_center", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["cart"], zone="main-header_right", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["account"], zone="main-header_right", order=1
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["language"], zone="main-header_right", order=2
            )
            # Mega menu bar: category navigation
            WidgetPlacement.objects.create(
                header=header, widget=widgets["menu"], zone="mega-menu-bar_full", order=0
            )
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header

    def create_promotional_marketing(self, user, widgets):
        """Promotional layout: header with navigation bar below for campaigns"""
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

        if created:
            # Main header: logo, search, utility icons
            WidgetPlacement.objects.create(
                header=header, widget=widgets["logo"], zone="main-header_left", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["search"], zone="main-header_center", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["cart"], zone="main-header_right", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["account"], zone="main-header_right", order=1
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["language"], zone="main-header_right", order=2
            )
            # Bottom bar: navigation
            WidgetPlacement.objects.create(
                header=header, widget=widgets["menu"], zone="bottom-bar_full", order=0
            )
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header

    def create_split_navigation(self, user, widgets):
        """Split layout: branding + utility top, navigation below"""
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

        if created:
            # Top bar: logo + utility
            WidgetPlacement.objects.create(
                header=header, widget=widgets["logo"], zone="top-bar_left", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["search"], zone="top-bar_right", order=0
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["cart"], zone="top-bar_right", order=1
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["account"], zone="top-bar_right", order=2
            )
            WidgetPlacement.objects.create(
                header=header, widget=widgets["language"], zone="top-bar_right", order=3
            )
            # Main header: full-width navigation
            WidgetPlacement.objects.create(
                header=header, widget=widgets["menu"], zone="main-header_left", order=0
            )
            self.stdout.write(f"  \u2713 Created: {header.name}")

        return header
