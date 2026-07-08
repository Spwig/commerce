from core.management.commands._seed_base import SeedCommand


class Command(SeedCommand):
    seed_name = 'trust_badges'
    seed_version = 1
    help = 'Seed default trust badges for checkout and product pages'

    CHECKOUT_BADGES = [
        {"icon": "fas fa-lock", "text": "Secure Checkout"},
        {"icon": "fas fa-shield-alt", "text": "Data Protected"},
    ]
    PRODUCT_BADGES = [
        {"icon": "fas fa-truck", "text": "Free Shipping"},
        {"icon": "fas fa-undo", "text": "30-Day Returns"},
        {"icon": "fas fa-shield-alt", "text": "Secure Payment"},
    ]
    DIGITAL_BADGES = [
        {"icon": "fas fa-bolt", "text": "Instant Delivery"},
        {"icon": "fas fa-infinity", "text": "Lifetime Access"},
        {"icon": "fas fa-shield-alt", "text": "Secure Download"},
    ]

    def seed(self) -> int:
        from design.models import PageTemplateConfig

        count = 0
        # Only populate empty badge fields (don't overwrite merchant customizations)
        count += PageTemplateConfig.objects.filter(
            checkout_trust_badges=[]
        ).update(checkout_trust_badges=self.CHECKOUT_BADGES)

        count += PageTemplateConfig.objects.filter(
            product_trust_badges=[]
        ).update(product_trust_badges=self.PRODUCT_BADGES)

        count += PageTemplateConfig.objects.filter(
            digital_trust_badges=[]
        ).update(digital_trust_badges=self.DIGITAL_BADGES)

        return count
