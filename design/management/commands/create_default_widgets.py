"""
Management command to create default widgets for headers and footers
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from design.header_footer_models import Widget

User = get_user_model()


class Command(BaseCommand):
    help = "Creates default widgets for header/footer builder"

    def handle(self, *args, **options):
        # Get or create admin user
        admin_user = User.objects.filter(is_superuser=True).first()

        # Default widgets to create
        default_widgets = [
            # Navigation widgets
            {
                "name": "Site Logo",
                "widget_type": "logo",
                "config": {"height": 40, "link": "/", "alt": "Site Logo"},
            },
            {
                "name": "Main Menu",
                "widget_type": "menu",
                "config": {
                    "menu_id": None,  # Will be linked to main-navigation menu below
                    "display_type": "horizontal",
                    "show_icons": False,
                },
            },
            {
                "name": "Search Bar",
                "widget_type": "search",
                "config": {"placeholder": "Search products...", "show_icon": True},
            },
            # Shop widgets
            {
                "name": "Shopping Cart",
                "widget_type": "cart",
                "config": {"show_count": True, "show_total": False},
            },
            {
                "name": "Account Menu",
                "widget_type": "account",
                "config": {"show_icon": True, "show_label": True},
            },
            {
                "name": "Language Selector",
                "widget_type": "language",
                "config": {"display": "dropdown", "show_flags": True},
            },
            # Content widgets
            {
                "name": "About Us Text",
                "widget_type": "text",
                "content": "<p>We are a leading e-commerce platform...</p>",
                "config": {},
            },
            {
                "name": "Quick Links",
                "widget_type": "links",
                "config": {
                    "title": "Quick Links",
                    "links": [
                        {"text": "About", "url": "/about/"},
                        {"text": "Contact", "url": "/contact/"},
                        {"text": "FAQ", "url": "/faq/"},
                    ],
                },
            },
            {
                "name": "Newsletter Signup",
                "widget_type": "newsletter",
                "config": {
                    "title": "Subscribe to our newsletter",
                    "placeholder": "Enter your email",
                    "button_text": "Subscribe",
                },
            },
            {
                "name": "Contact Info",
                "widget_type": "contact",
                "config": {
                    "email": "info@example.com",
                    "phone": "+1 234 567 8900",
                    "address": "123 Main St, City, State 12345",
                },
            },
            # Social widgets
            {
                "name": "Social Media Links",
                "widget_type": "social",
                "config": {
                    "title": "Follow Us",
                    "facebook": "https://facebook.com/yourpage",
                    "twitter": "https://twitter.com/yourpage",
                    "instagram": "https://instagram.com/yourpage",
                    "show_text": False,
                },
            },
            # Site Variable widget (displays any site setting)
            {
                "name": "Site Variable",
                "widget_type": "site_variable",
                "config": {
                    "variable": "site_name",
                    "enable_link": False,
                    "show_icon": False,
                },
            },
        ]

        created_count = 0
        for widget_data in default_widgets:
            # Check if widget already exists
            if not Widget.objects.filter(
                name=widget_data["name"], widget_type=widget_data["widget_type"]
            ).exists():
                Widget.objects.create(created_by=admin_user, is_active=True, **widget_data)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created widget: {widget_data['name']}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Widget already exists: {widget_data['name']}")
                )

        self.stdout.write(self.style.SUCCESS(f"\nTotal widgets created: {created_count}"))
        self.stdout.write(
            self.style.SUCCESS(f"Total widgets in database: {Widget.objects.count()}")
        )

        # Link Main Menu widget to the main-navigation menu if it exists
        self._link_menu_widget()

    def _link_menu_widget(self):
        """Link the Main Menu widget to the main-navigation menu"""
        from design.header_footer_models import Menu

        main_nav = Menu.objects.filter(slug="main-navigation").first()
        if not main_nav:
            return

        menu_widget = Widget.objects.filter(name="Main Menu", widget_type="menu").first()

        if menu_widget:
            config = menu_widget.config or {}
            if not config.get("menu_id"):
                config["menu_id"] = main_nav.id
                config["display_type"] = "horizontal"
                menu_widget.config = config
                menu_widget.save()
                self.stdout.write(
                    self.style.SUCCESS('Linked "Main Menu" widget to main-navigation menu')
                )
