"""
Management command to create default navigation menus for the e-commerce platform.
Creates universal menus that work for most stores with sensible defaults.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from design.header_footer_models import Menu, MenuItem

User = get_user_model()


class Command(BaseCommand):
    help = "Creates default navigation menus for header, footer, account, and mobile"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Recreate menus even if they already exist (deletes existing)",
        )

    def handle(self, *args, **options):
        force = options.get("force", False)

        # Get admin user for created_by field
        admin_user = User.objects.filter(is_superuser=True).first()

        # Track results
        created_menus = []
        skipped_menus = []

        # Create all default menus
        menus_to_create = [
            self.get_main_navigation_config(),
            self.get_footer_menu_config(),
            self.get_account_menu_config(),
            self.get_mobile_menu_config(),
        ]

        for menu_config in menus_to_create:
            result = self.create_menu_with_items(menu_config, admin_user, force)
            if result["created"]:
                created_menus.append(result["name"])
            else:
                skipped_menus.append(result["name"])

        # Summary output
        self.stdout.write(self.style.SUCCESS(f"\nMenus created: {len(created_menus)}"))
        if created_menus:
            for name in created_menus:
                self.stdout.write(f"  + {name}")

        if skipped_menus:
            self.stdout.write(
                self.style.WARNING(f"Menus skipped (already exist): {len(skipped_menus)}")
            )
            for name in skipped_menus:
                self.stdout.write(f"  - {name}")

        # Link default menu widget to main navigation
        self.link_default_menu_widget()

    def get_page_by_slug(self, slug):
        """Helper to get page by slug, returns None if not found"""
        try:
            from page_builder.models import Page

            return Page.objects.filter(slug=slug, status="published").first()
        except Exception:
            return None

    def create_menu_with_items(self, config, user, force=False):
        """Create a menu and its items from configuration"""
        slug = config["slug"]

        # Check if menu exists
        existing = Menu.objects.filter(slug=slug).first()
        if existing and not force:
            return {"name": config["name"], "created": False}

        # Delete existing if force mode
        if existing and force:
            existing.delete()
            self.stdout.write(f"  Deleted existing menu: {config['name']}")

        # Create the menu
        menu = Menu.objects.create(
            name=config["name"],
            slug=slug,
            description=config.get("description", ""),
            location=config["location"],
            display_type=config["display_type"],
            is_active=True,
            created_by=user,
        )

        # Create menu items
        self.create_items_recursive(menu, config["items"], parent=None)

        self.stdout.write(f"  Created menu: {config['name']}")
        return {"name": config["name"], "created": True}

    def create_items_recursive(self, menu, items, parent=None):
        """Recursively create menu items with children"""
        for order, item_config in enumerate(items):
            item_data = {
                "menu": menu,
                "parent": parent,
                "order": order,
                "title": item_config.get("title", ""),
                "item_type": item_config.get("item_type", "link"),
                "url": item_config.get("url", ""),
                "icon": item_config.get("icon", ""),
                "target": item_config.get("target", "_self"),
                "is_active": True,
            }

            # Handle page reference
            if item_config.get("page_slug"):
                page = self.get_page_by_slug(item_config["page_slug"])
                if page:
                    item_data["page_reference"] = page
                    item_data["item_type"] = "page"
                else:
                    # Fall back to custom URL if page doesn't exist
                    item_data["item_type"] = "custom_url"
                    item_data["url"] = f"/page/{item_config['page_slug']}/"

            # Handle visibility rules
            if item_config.get("visibility_rules"):
                item_data["visibility_rules"] = item_config["visibility_rules"]

            # Handle tree config for category_tree items
            if item_config.get("tree_config"):
                item_data["tree_config"] = item_config["tree_config"]

            item = MenuItem.objects.create(**item_data)

            # Create children recursively
            if item_config.get("children"):
                self.create_items_recursive(menu, item_config["children"], parent=item)

    def link_default_menu_widget(self):
        """Link the default 'Main Menu' widget to the main-navigation menu"""
        try:
            from design.header_footer_models import Widget

            main_nav = Menu.objects.filter(slug="main-navigation").first()
            if not main_nav:
                return

            # Find the Main Menu widget and update its config
            menu_widget = Widget.objects.filter(name="Main Menu", widget_type="menu").first()

            if menu_widget:
                config = menu_widget.config or {}
                if not config.get("menu_id"):
                    config["menu_id"] = main_nav.id
                    config["display_type"] = "horizontal"
                    menu_widget.config = config
                    menu_widget.save()
                    self.stdout.write(
                        self.style.SUCCESS('\nLinked "Main Menu" widget to main-navigation menu')
                    )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"\nCould not link menu widget: {e}"))

    def get_main_navigation_config(self):
        """Main navigation menu configuration"""
        return {
            "name": "Main Navigation",
            "slug": "main-navigation",
            "description": "Primary header navigation menu",
            "location": "primary",
            "display_type": "horizontal",
            "items": [
                {
                    "title": "Home",
                    "item_type": "link",
                    "url": "/",
                    "icon": "fas fa-home",
                },
                {
                    "title": "Shop",
                    "item_type": "category_tree",
                    "url": "/category/",
                    "tree_config": {
                        "root_category_id": None,
                        "max_depth": 2,
                        "sort_by": "name",
                        "show_empty": False,
                        "show_product_count": False,
                    },
                },
                {
                    "title": "About Us",
                    "item_type": "page",
                    "page_slug": "about",
                },
                {
                    "title": "Contact",
                    "item_type": "page",
                    "page_slug": "contact",
                },
            ],
        }

    def get_footer_menu_config(self):
        """Footer links menu configuration"""
        return {
            "name": "Footer Links",
            "slug": "footer-links",
            "description": "Footer navigation with legal and information pages",
            "location": "footer",
            "display_type": "vertical",
            "items": [
                {
                    "title": "Privacy Policy",
                    "item_type": "page",
                    "page_slug": "privacy-policy",
                },
                {
                    "title": "Terms of Service",
                    "item_type": "page",
                    "page_slug": "terms-of-service",
                },
                {
                    "title": "Shipping Information",
                    "item_type": "page",
                    "page_slug": "shipping-info",
                },
                {
                    "title": "Returns & Refunds",
                    "item_type": "page",
                    "page_slug": "returns",
                },
                {
                    "title": "FAQ",
                    "item_type": "page",
                    "page_slug": "faq",
                },
            ],
        }

    def get_account_menu_config(self):
        """Account menu configuration with visibility rules"""
        return {
            "name": "Account Menu",
            "slug": "account-menu",
            "description": "User account dropdown menu",
            "location": "account",
            "display_type": "dropdown",
            "items": [
                {
                    "title": "My Account",
                    "item_type": "custom_url",
                    "url": "/account/",
                    "icon": "fas fa-user",
                    "visibility_rules": [{"type": "user_status", "value": "logged_in"}],
                },
                {
                    "title": "My Orders",
                    "item_type": "custom_url",
                    "url": "/account/orders/",
                    "icon": "fas fa-box",
                    "visibility_rules": [{"type": "user_status", "value": "logged_in"}],
                },
                {
                    "title": "Wishlist",
                    "item_type": "custom_url",
                    "url": "/wishlist/",
                    "icon": "fas fa-heart",
                    "visibility_rules": [{"type": "user_status", "value": "logged_in"}],
                },
                {
                    "title": "",
                    "item_type": "divider",
                    "visibility_rules": [{"type": "user_status", "value": "logged_in"}],
                },
                {
                    "title": "Sign Out",
                    "item_type": "custom_url",
                    "url": "/accounts/logout/",
                    "icon": "fas fa-sign-out-alt",
                    "visibility_rules": [{"type": "user_status", "value": "logged_in"}],
                },
                {
                    "title": "Sign In",
                    "item_type": "custom_url",
                    "url": "/accounts/login/",
                    "icon": "fas fa-sign-in-alt",
                    "visibility_rules": [{"type": "user_status", "value": "logged_out"}],
                },
                {
                    "title": "Create Account",
                    "item_type": "custom_url",
                    "url": "/accounts/signup/",
                    "icon": "fas fa-user-plus",
                    "visibility_rules": [{"type": "user_status", "value": "logged_out"}],
                },
            ],
        }

    def get_mobile_menu_config(self):
        """Mobile navigation menu configuration"""
        return {
            "name": "Mobile Navigation",
            "slug": "mobile-navigation",
            "description": "Simplified navigation for mobile devices",
            "location": "mobile",
            "display_type": "accordion",
            "items": [
                {
                    "title": "Home",
                    "item_type": "link",
                    "url": "/",
                    "icon": "fas fa-home",
                },
                {
                    "title": "Shop",
                    "item_type": "category_tree",
                    "url": "/category/",
                    "icon": "fas fa-store",
                    "tree_config": {
                        "root_category_id": None,
                        "max_depth": 2,
                        "sort_by": "name",
                        "show_empty": False,
                    },
                },
                {
                    "title": "About",
                    "item_type": "page",
                    "page_slug": "about",
                    "icon": "fas fa-info-circle",
                },
                {
                    "title": "Contact",
                    "item_type": "page",
                    "page_slug": "contact",
                    "icon": "fas fa-envelope",
                },
                {
                    "title": "",
                    "item_type": "divider",
                },
                {
                    "title": "My Account",
                    "item_type": "custom_url",
                    "url": "/account/",
                    "icon": "fas fa-user",
                    "visibility_rules": [{"type": "user_status", "value": "logged_in"}],
                },
                {
                    "title": "Sign In",
                    "item_type": "custom_url",
                    "url": "/accounts/login/",
                    "icon": "fas fa-sign-in-alt",
                    "visibility_rules": [{"type": "user_status", "value": "logged_out"}],
                },
            ],
        }
