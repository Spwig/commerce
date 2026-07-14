from core.management.commands._seed_base import SeedCommand


class Command(SeedCommand):
    seed_name = "affiliate_form"
    seed_version = 1
    help = "Seed default affiliate registration form"

    FIELDS = [
        {
            "field_name": "company_name",
            "field_type": "text",
            "label": "Company Name",
            "placeholder": "Your company or business name",
            "help_text": "Optional - Enter your business name if applicable",
            "is_required": False,
            "order": 0,
            "width": "half",
        },
        {
            "field_name": "website",
            "field_type": "url",
            "label": "Website",
            "placeholder": "https://yourwebsite.com",
            "help_text": "Your website or social media profile where you'll promote products",
            "is_required": False,
            "order": 1,
            "width": "half",
        },
        {
            "field_name": "payment_email",
            "field_type": "email",
            "label": "Payment Email",
            "placeholder": "payment@example.com",
            "help_text": "Email address for receiving payments (PayPal, etc.)",
            "is_required": True,
            "order": 2,
            "width": "full",
        },
        {
            "field_name": "payment_method",
            "field_type": "select",
            "label": "Preferred Payment Method",
            "help_text": "How would you like to receive your commissions?",
            "is_required": True,
            "order": 3,
            "width": "half",
            "options": [
                {"value": "paypal", "label": "PayPal"},
                {"value": "bank_transfer", "label": "Bank Transfer"},
            ],
        },
        {
            "field_name": "how_heard",
            "field_type": "select",
            "label": "How did you hear about us?",
            "help_text": "Optional - Help us understand how you found our program",
            "is_required": False,
            "order": 4,
            "width": "half",
            "options": [
                {"value": "", "label": "-- Select --"},
                {"value": "search", "label": "Search Engine"},
                {"value": "social", "label": "Social Media"},
                {"value": "friend", "label": "Friend/Colleague"},
                {"value": "blog", "label": "Blog/Article"},
                {"value": "other", "label": "Other"},
            ],
        },
        {
            "field_name": "promotion_methods",
            "field_type": "textarea",
            "label": "How do you plan to promote our products?",
            "placeholder": "Describe your promotional strategy...",
            "help_text": "Optional - Tell us about your marketing channels and audience",
            "is_required": False,
            "order": 5,
            "width": "full",
            "max_length": 1000,
        },
    ]

    def seed(self) -> int:
        from form_builder.models import Form, FormField

        form, created = Form.objects.get_or_create(
            slug="affiliate-registration",
            defaults={
                "name": "Affiliate Registration",
                "title": "Affiliate Registration",
                "description": "Complete your affiliate application",
                "submit_button_text": "Submit Application",
                "success_message": "Thank you! Your affiliate application has been submitted for review.",
                "error_message": "Something went wrong. Please check your information and try again.",
                "is_active": True,
                "is_multi_step": False,
                "require_login": False,
                "spam_protection": "honeypot",
            },
        )

        if not created:
            return 0

        for field_data in self.FIELDS:
            FormField.objects.create(form=form, **field_data)
        return 1 + len(self.FIELDS)
