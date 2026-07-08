"""
Shipping Services
Business logic layer for shipping operations
"""
from .provider_service import ProviderService
from .rule_service import ShippingPromotionService

# Backward compatibility alias
ShippingRuleService = ShippingPromotionService

__all__ = ['ProviderService', 'ShippingPromotionService', 'ShippingRuleService']
