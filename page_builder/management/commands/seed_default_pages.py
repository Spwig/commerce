from core.management.commands._seed_base import SeedCommand


class Command(SeedCommand):
    seed_name = "default_pages"
    seed_version = 2
    help = "Create all default pages that ship with the platform"

    def seed(self) -> int:
        from django.utils import timezone

        from core.models import SiteSettings
        from page_builder.models import Page

        # Get or create site settings
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            site_settings = SiteSettings(pk=1)
            site_settings.save(skip_validation=True)

        now = timezone.now()
        count = 0

        # =====================================================================
        # All default pages with their SiteSettings assignment fields
        # =====================================================================
        default_pages = [
            # =================================================================
            # SYSTEM PAGES (Protected, is_system_page=True)
            # =================================================================
            {
                "title": "Home",
                "slug": "home",
                "page_type": "home",
                "status": "published",
                "is_default_for_type": True,
                "is_system_page": True,
                "requires_auth": False,
                "meta_title": "Welcome to Our Store",
                "meta_description": "Discover amazing products at great prices. Shop our collection of quality items with fast shipping and excellent customer service.",
                "published_at": now,
                "assignment_field": "home_page",
            },
            # =================================================================
            # CONTENT PAGES (Editable, is_system_page=False)
            # =================================================================
            {
                "title": "About Us",
                "slug": "about",
                "page_type": "about",
                "status": "published",
                "is_default_for_type": True,
                "is_system_page": False,
                "requires_auth": False,
                "meta_title": "About Us - Our Story",
                "meta_description": "Learn about our company, our mission, and the team behind our products. We are committed to quality and customer satisfaction.",
                "published_at": now,
                "assignment_field": None,
            },
            {
                "title": "Contact Us",
                "slug": "contact",
                "page_type": "contact",
                "status": "published",
                "is_default_for_type": True,
                "is_system_page": False,
                "requires_auth": False,
                "meta_title": "Contact Us",
                "meta_description": "Get in touch with our team. We are here to help with any questions or concerns you may have.",
                "published_at": now,
                "assignment_field": None,
            },
            {
                "title": "Frequently Asked Questions",
                "slug": "faq",
                "page_type": "custom",
                "status": "published",
                "is_default_for_type": False,
                "is_system_page": False,
                "requires_auth": False,
                "meta_title": "FAQ - Frequently Asked Questions",
                "meta_description": "Find answers to common questions about orders, shipping, returns, and more.",
                "published_at": now,
                "assignment_field": None,
            },
            # =================================================================
            # LEGAL PAGES (Important policy pages)
            # =================================================================
            {
                "title": "Privacy Policy",
                "slug": "privacy-policy",
                "page_type": "custom",
                "status": "published",
                "is_default_for_type": False,
                "is_system_page": False,
                "requires_auth": False,
                "meta_title": "Privacy Policy",
                "meta_description": "Our privacy policy explains how we collect, use, and protect your personal information.",
                "published_at": now,
                "assignment_field": "privacy_page",
            },
            {
                "title": "Terms of Use",
                "slug": "terms-of-use",
                "page_type": "custom",
                "status": "published",
                "is_default_for_type": False,
                "is_system_page": False,
                "requires_auth": False,
                "meta_title": "Terms of Use",
                "meta_description": "Read our terms of service to understand the rules and conditions for using our store.",
                "published_at": now,
                "assignment_field": "terms_page",
            },
            {
                "title": "Cookie Policy",
                "slug": "cookie-policy",
                "page_type": "custom",
                "status": "published",
                "is_default_for_type": False,
                "is_system_page": False,
                "requires_auth": False,
                "meta_title": "Cookie Policy",
                "meta_description": "Learn how we use cookies to improve your shopping experience.",
                "published_at": now,
                "assignment_field": "cookie_page",
            },
            {
                "title": "Shipping Information",
                "slug": "shipping-info",
                "page_type": "custom",
                "status": "published",
                "is_default_for_type": False,
                "is_system_page": False,
                "requires_auth": False,
                "meta_title": "Shipping Information",
                "meta_description": "Learn about our shipping options, delivery times, and costs.",
                "published_at": now,
                "assignment_field": "shipping_page",
            },
            {
                "title": "Returns & Refunds",
                "slug": "returns-policy",
                "page_type": "custom",
                "status": "published",
                "is_default_for_type": False,
                "is_system_page": False,
                "requires_auth": False,
                "meta_title": "Returns & Refunds Policy",
                "meta_description": "Our hassle-free returns policy. Learn how to return items and get refunds.",
                "published_at": now,
                "assignment_field": "returns_page",
            },
            # =================================================================
            # ERROR PAGES (Customizable error handling)
            # =================================================================
            {
                "title": "Page Not Found",
                "slug": "404",
                "page_type": "custom",
                "status": "published",
                "is_default_for_type": False,
                "is_system_page": False,
                "requires_auth": False,
                "meta_title": "Page Not Found",
                "meta_description": "The page you are looking for could not be found.",
                "published_at": now,
                "assignment_field": "error_404_page",
            },
            {
                "title": "Server Error",
                "slug": "500",
                "page_type": "custom",
                "status": "published",
                "is_default_for_type": False,
                "is_system_page": False,
                "requires_auth": False,
                "meta_title": "Server Error",
                "meta_description": "An unexpected error occurred. Please try again later.",
                "published_at": now,
                "assignment_field": "error_500_page",
            },
            # =================================================================
            # MAINTENANCE PAGE (System page, header/footer hidden)
            # =================================================================
            {
                "title": "We'll Be Right Back",
                "slug": "maintenance",
                "page_type": "custom",
                "status": "published",
                "is_default_for_type": False,
                "is_system_page": True,
                "requires_auth": False,
                "hide_header": True,
                "hide_footer": True,
                "meta_title": "Site Under Maintenance",
                "meta_description": "We are currently performing scheduled maintenance to improve your experience. Please check back soon.",
                "meta_keywords": "maintenance, under construction, coming soon",
                "seo_auto_generated": False,
                "published_at": now,
                "assignment_field": "maintenance_page",
                "translations": {
                    "de": {
                        "title": "Wartung",
                        "meta_title": "Seite wird gewartet",
                        "meta_description": "Wir führen derzeit geplante Wartungsarbeiten durch, um Ihr Erlebnis zu verbessern. Bitte schauen Sie bald wieder vorbei.",
                    },
                    "fr": {
                        "title": "Maintenance",
                        "meta_title": "Site en maintenance",
                        "meta_description": "Nous effectuons actuellement une maintenance programmée pour améliorer votre expérience. Veuillez revenir bientôt.",
                    },
                    "es": {
                        "title": "Mantenimiento",
                        "meta_title": "Sitio en mantenimiento",
                        "meta_description": "Actualmente estamos realizando un mantenimiento programado para mejorar su experiencia. Por favor, vuelva pronto.",
                    },
                    "ar": {
                        "title": "\u0635\u064a\u0627\u0646\u0629",
                        "meta_title": "\u0627\u0644\u0645\u0648\u0642\u0639 \u0642\u064a\u062f \u0627\u0644\u0635\u064a\u0627\u0646\u0629",
                        "meta_description": "\u0646\u0642\u0648\u0645 \u062d\u0627\u0644\u064a\u0627\u064b \u0628\u0625\u062c\u0631\u0627\u0621 \u0635\u064a\u0627\u0646\u0629 \u0645\u062c\u062f\u0648\u0644\u0629 \u0644\u062a\u062d\u0633\u064a\u0646 \u062a\u062c\u0631\u0628\u062a\u0643. \u064a\u0631\u062c\u0649 \u0627\u0644\u0639\u0648\u062f\u0629 \u0642\u0631\u064a\u0628\u0627\u064b.",
                    },
                    "ru": {
                        "title": "\u0422\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043e\u0431\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u043d\u0438\u0435",
                        "meta_title": "\u0421\u0430\u0439\u0442 \u043d\u0430 \u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u043c \u043e\u0431\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u043d\u0438\u0438",
                        "meta_description": "\u0412 \u043d\u0430\u0441\u0442\u043e\u044f\u0449\u0435\u0435 \u0432\u0440\u0435\u043c\u044f \u043c\u044b \u043f\u0440\u043e\u0432\u043e\u0434\u0438\u043c \u043f\u043b\u0430\u043d\u043e\u0432\u043e\u0435 \u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043e\u0431\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0443\u043b\u0443\u0447\u0448\u0435\u043d\u0438\u044f \u0432\u0430\u0448\u0435\u0433\u043e \u043e\u043f\u044b\u0442\u0430. \u041f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430, \u0437\u0430\u0439\u0434\u0438\u0442\u0435 \u043f\u043e\u0437\u0436\u0435.",
                    },
                    "zh_hans": {
                        "title": "\u7ef4\u62a4\u4e2d",
                        "meta_title": "\u7f51\u7ad9\u7ef4\u62a4\u4e2d",
                        "meta_description": "\u6211\u4eec\u76ee\u524d\u6b63\u5728\u8fdb\u884c\u5b9a\u671f\u7ef4\u62a4\u4ee5\u6539\u5584\u60a8\u7684\u4f53\u9a8c\u3002\u8bf7\u7a0d\u540e\u518d\u6765\u3002",
                    },
                },
            },
        ]

        # Create pages and assign to site settings
        for page_data in default_pages:
            assignment_field = page_data.pop("assignment_field")

            # Use get_or_create by slug to avoid duplicates
            page, created = Page.objects.get_or_create(
                slug=page_data["slug"],
                defaults=page_data,
            )

            if created:
                count += 1

            # Assign to site settings if this page has an assignment field
            if assignment_field and hasattr(site_settings, assignment_field):
                current_value = getattr(site_settings, assignment_field)
                if current_value is None:
                    setattr(site_settings, assignment_field, page)

        # Save site settings with all assignments (skip validation to avoid
        # unrelated validation errors from existing data state)
        site_settings.save(skip_validation=True)

        return count
