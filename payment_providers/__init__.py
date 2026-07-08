"""
Payment Providers Component
Payment gateway integrations and payment processing via provider framework.
"""

__version__ = "1.0.0"
__component_name__ = "payment_providers"
__description__ = "Payment provider integrations (Stripe, PayPal, AirWallex, etc.)"
__requires_platform__ = "1.x"

default_app_config = 'payment_providers.apps.PaymentProvidersConfig'
