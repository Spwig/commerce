"""
Tests for shipping promotions engine (ShippingPromotion, ShippingRateTable, ShippingRuleService)
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from djmoney.money import Money
from decimal import Decimal
from datetime import timedelta

from shipping.models import (
    ShippingZone,
    ShippingPromotion,
    ShippingRateTable,
    ShippingRateTier,
)
from shipping.services import ShippingRuleService
from cart.models import Cart, CartItem, ShippingMethod
from catalog.models import Product, Category
from orders.models import Order

User = get_user_model()


class ShippingPromotionModelTest(TestCase):
    """Test ShippingPromotion model methods"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create a shipping zone
        self.zone = ShippingZone.objects.create(
            name='USA',
            priority=0,
            is_active=True,
            countries=['US'],
        )

        # Create a cart for testing
        self.cart = Cart.objects.create(user=self.user)

        # Create a category and product
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            sku='TEST-001',
            category=self.category,
            price=Money('100.00', 'USD'),
            weight=Decimal('2.5')
        )

        # Add item to cart
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
            unit_price=self.product.price
        )

    def test_create_rule_free_shipping(self):
        """Test creating a free shipping rule"""
        rule = ShippingPromotion.objects.create(
            name='Free Shipping Over $50',
            promotion_type='free_shipping',
            min_cart_value=Money('50.00', 'USD'),
            priority=10,
            is_active=True,
        )

        self.assertEqual(rule.name, 'Free Shipping Over $50')
        self.assertEqual(rule.promotion_type, 'free_shipping')
        self.assertTrue(rule.is_active)

    def test_rule_is_time_valid_no_restrictions(self):
        """Test rule with no time restrictions is always valid"""
        rule = ShippingPromotion.objects.create(
            name='Always Valid',
            promotion_type='free_shipping',
            is_active=True,
        )

        self.assertTrue(rule.is_time_valid())

    def test_rule_is_time_valid_future_start(self):
        """Test rule with future start date is not valid"""
        future = timezone.now() + timedelta(days=1)
        rule = ShippingPromotion.objects.create(
            name='Future Rule',
            promotion_type='free_shipping',
            start_date=future,
            is_active=True,
        )

        self.assertFalse(rule.is_time_valid())

    def test_rule_is_time_valid_past_end(self):
        """Test rule with past end date is not valid"""
        past = timezone.now() - timedelta(days=1)
        rule = ShippingPromotion.objects.create(
            name='Expired Rule',
            promotion_type='free_shipping',
            end_date=past,
            is_active=True,
        )

        self.assertFalse(rule.is_time_valid())

    def test_rule_is_time_valid_active_period(self):
        """Test rule within valid time period"""
        past = timezone.now() - timedelta(days=1)
        future = timezone.now() + timedelta(days=1)
        rule = ShippingPromotion.objects.create(
            name='Active Rule',
            promotion_type='free_shipping',
            start_date=past,
            end_date=future,
            is_active=True,
        )

        self.assertTrue(rule.is_time_valid())

    def test_matches_cart_value_within_range(self):
        """Test cart value matching"""
        rule = ShippingPromotion.objects.create(
            name='Value Rule',
            promotion_type='discount_percentage',
            min_cart_value=Money('50.00', 'USD'),
            max_cart_value=Money('300.00', 'USD'),
        )

        # Cart has $200 ($100 x 2)
        self.assertTrue(rule.matches_cart_value(self.cart.subtotal))

    def test_matches_cart_value_below_minimum(self):
        """Test cart value below minimum doesn't match"""
        rule = ShippingPromotion.objects.create(
            name='High Value Rule',
            promotion_type='discount_percentage',
            min_cart_value=Money('500.00', 'USD'),
        )

        # Cart has $200
        self.assertFalse(rule.matches_cart_value(self.cart.subtotal))

    def test_matches_cart_value_above_maximum(self):
        """Test cart value above maximum doesn't match"""
        rule = ShippingPromotion.objects.create(
            name='Low Value Rule',
            promotion_type='discount_percentage',
            max_cart_value=Money('100.00', 'USD'),
        )

        # Cart has $200
        self.assertFalse(rule.matches_cart_value(self.cart.subtotal))

    def test_matches_cart_weight(self):
        """Test cart weight matching"""
        rule = ShippingPromotion.objects.create(
            name='Light Package',
            promotion_type='discount_fixed',
            min_cart_weight=Decimal('1.0'),
            max_cart_weight=Decimal('10.0'),
        )

        # Cart has 5kg (2.5kg x 2)
        self.assertTrue(rule.matches_cart_weight(self.cart.total_weight))

    def test_matches_cart_weight_too_heavy(self):
        """Test cart weight above maximum doesn't match"""
        rule = ShippingPromotion.objects.create(
            name='Very Light Only',
            promotion_type='discount_fixed',
            max_cart_weight=Decimal('2.0'),
        )

        # Cart has 5kg
        self.assertFalse(rule.matches_cart_weight(self.cart.total_weight))

    def test_matches_item_count(self):
        """Test item count matching"""
        rule = ShippingPromotion.objects.create(
            name='Bulk Order',
            promotion_type='discount_percentage',
            min_item_count=1,
            max_item_count=5,
        )

        # Cart has 2 items
        self.assertTrue(rule.matches_item_count(self.cart.total_items))

    def test_matches_item_count_too_few(self):
        """Test item count below minimum doesn't match"""
        rule = ShippingPromotion.objects.create(
            name='Large Bulk Only',
            promotion_type='discount_percentage',
            min_item_count=10,
        )

        # Cart has 2 items
        self.assertFalse(rule.matches_item_count(self.cart.total_items))

    def test_matches_address_with_zone(self):
        """Test address matching with zone restriction"""
        rule = ShippingPromotion.objects.create(
            name='USA Only Rule',
            promotion_type='free_shipping',
        )
        rule.zones.add(self.zone)

        # US address should match
        self.assertTrue(rule.matches_address({'country': 'US', 'state': 'CA'}))

        # Non-US address should not match
        self.assertFalse(rule.matches_address({'country': 'CA', 'state': 'ON'}))

    def test_matches_address_no_zone_restriction(self):
        """Test address matching with no zone restriction applies to all"""
        rule = ShippingPromotion.objects.create(
            name='Worldwide Rule',
            promotion_type='free_shipping',
        )

        # Any address should match
        self.assertTrue(rule.matches_address({'country': 'US'}))
        self.assertTrue(rule.matches_address({'country': 'CA'}))
        self.assertTrue(rule.matches_address({'country': 'GB'}))

    def test_matches_cart_products_requires(self):
        """Test rule requiring specific products"""
        rule = ShippingPromotion.objects.create(
            name='Electronics Discount',
            promotion_type='discount_fixed',
        )
        rule.requires_products.add(self.product)

        # Cart contains required product
        self.assertTrue(rule.matches_cart_products(self.cart))

    def test_matches_cart_products_requires_not_in_cart(self):
        """Test rule requiring products not in cart"""
        other_product = Product.objects.create(
            name='Other Product',
            slug='other-product',
            sku='OTHER-001',
            price=Money('50.00', 'USD'),
            category=self.category
        )

        rule = ShippingPromotion.objects.create(
            name='Other Product Discount',
            promotion_type='discount_fixed',
        )
        rule.requires_products.add(other_product)

        # Cart doesn't contain required product
        self.assertFalse(rule.matches_cart_products(self.cart))

    def test_matches_cart_products_excludes(self):
        """Test rule excluding specific products"""
        rule = ShippingPromotion.objects.create(
            name='No Electronics',
            promotion_type='discount_fixed',
        )
        rule.excludes_products.add(self.product)

        # Cart contains excluded product
        self.assertFalse(rule.matches_cart_products(self.cart))

    def test_matches_cart_products_requires_category(self):
        """Test rule requiring specific category"""
        rule = ShippingPromotion.objects.create(
            name='Electronics Shipping',
            promotion_type='surcharge_fixed',
        )
        rule.requires_categories.add(self.category)

        # Cart contains product from required category
        self.assertTrue(rule.matches_cart_products(self.cart))

    def test_calculate_adjustment_free_shipping(self):
        """Test free shipping rule adjustment"""
        rule = ShippingPromotion.objects.create(
            name='Free Shipping',
            promotion_type='free_shipping',
        )

        base_cost = Money('15.00', 'USD')
        adjusted = rule.calculate_adjustment(base_cost)

        self.assertEqual(adjusted, Money('0.00', 'USD'))

    def test_calculate_adjustment_override_cost(self):
        """Test override cost promotion adjustment"""
        rule = ShippingPromotion.objects.create(
            name='Flat $5 Shipping',
            promotion_type='override_cost',
            promotion_value=Money('5.00', 'USD'),
        )

        base_cost = Money('15.00', 'USD')
        adjusted = rule.calculate_adjustment(base_cost)

        self.assertEqual(adjusted, Money('5.00', 'USD'))

    def test_calculate_adjustment_discount_percentage(self):
        """Test percentage discount rule adjustment"""
        rule = ShippingPromotion.objects.create(
            name='50% Off Shipping',
            promotion_type='discount_percentage',
            promotion_value=Money('50.00', 'USD'),  # 50%
        )

        base_cost = Money('20.00', 'USD')
        adjusted = rule.calculate_adjustment(base_cost)

        self.assertEqual(adjusted, Money('10.00', 'USD'))

    def test_calculate_adjustment_discount_fixed(self):
        """Test fixed discount rule adjustment"""
        rule = ShippingPromotion.objects.create(
            name='$5 Off Shipping',
            promotion_type='discount_fixed',
            promotion_value=Money('5.00', 'USD'),
        )

        base_cost = Money('20.00', 'USD')
        adjusted = rule.calculate_adjustment(base_cost)

        self.assertEqual(adjusted, Money('15.00', 'USD'))

    def test_calculate_adjustment_discount_cannot_go_negative(self):
        """Test discount cannot result in negative cost"""
        rule = ShippingPromotion.objects.create(
            name='Big Discount',
            promotion_type='discount_fixed',
            promotion_value=Money('30.00', 'USD'),
        )

        base_cost = Money('20.00', 'USD')
        adjusted = rule.calculate_adjustment(base_cost)

        self.assertEqual(adjusted, Money('0.00', 'USD'))

    def test_calculate_adjustment_surcharge_fixed(self):
        """Test fixed surcharge rule adjustment"""
        rule = ShippingPromotion.objects.create(
            name='Remote Area Surcharge',
            promotion_type='surcharge_fixed',
            promotion_value=Money('10.00', 'USD'),
        )

        base_cost = Money('15.00', 'USD')
        adjusted = rule.calculate_adjustment(base_cost)

        self.assertEqual(adjusted, Money('25.00', 'USD'))

    def test_calculate_adjustment_surcharge_percentage(self):
        """Test percentage surcharge rule adjustment"""
        rule = ShippingPromotion.objects.create(
            name='20% Surcharge',
            promotion_type='surcharge_percentage',
            promotion_value=Money('20.00', 'USD'),  # 20%
        )

        base_cost = Money('100.00', 'USD')
        adjusted = rule.calculate_adjustment(base_cost)

        self.assertEqual(adjusted, Money('120.00', 'USD'))


class ShippingRateTableModelTest(TestCase):
    """Test ShippingRateTable and ShippingRateTier models"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create a shipping method
        self.shipping_method = ShippingMethod.objects.create(
            name='Standard Shipping',
            method_type='table_rate',
        )

    def test_create_rate_table(self):
        """Test creating a rate table"""
        table = ShippingRateTable.objects.create(
            name='Weight-Based Rates',
            basis_type='weight',
            shipping_method=self.shipping_method,
            is_active=True,
        )

        self.assertEqual(table.name, 'Weight-Based Rates')
        self.assertEqual(table.basis_type, 'weight')
        self.assertTrue(table.is_active)

    def test_create_rate_tiers(self):
        """Test creating rate tiers"""
        table = ShippingRateTable.objects.create(
            name='Weight Tiers',
            basis_type='weight',
            shipping_method=self.shipping_method,
        )

        # Create tiers
        tier1 = ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('0'),
            max_value=Decimal('5'),
            rate=Money('10.00', 'USD'),
        )

        tier2 = ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('5'),
            max_value=Decimal('10'),
            rate=Money('15.00', 'USD'),
        )

        self.assertEqual(table.tiers.count(), 2)
        self.assertEqual(tier1.rate, Money('10.00', 'USD'))
        self.assertEqual(tier2.rate, Money('15.00', 'USD'))

    def test_get_rate_for_value_matches_first_tier(self):
        """Test rate lookup for value in first tier"""
        table = ShippingRateTable.objects.create(
            name='Weight Tiers',
            basis_type='weight',
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('0'),
            max_value=Decimal('5'),
            rate=Money('10.00', 'USD'),
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('5'),
            max_value=Decimal('10'),
            rate=Money('15.00', 'USD'),
        )

        # 3kg should match first tier
        rate = table.get_rate_for_value(Decimal('3.0'))
        self.assertEqual(rate, Money('10.00', 'USD'))

    def test_get_rate_for_value_matches_second_tier(self):
        """Test rate lookup for value in second tier"""
        table = ShippingRateTable.objects.create(
            name='Weight Tiers',
            basis_type='weight',
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('0'),
            max_value=Decimal('5'),
            rate=Money('10.00', 'USD'),
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('5'),
            max_value=Decimal('10'),
            rate=Money('15.00', 'USD'),
        )

        # 7kg should match second tier
        rate = table.get_rate_for_value(Decimal('7.0'))
        self.assertEqual(rate, Money('15.00', 'USD'))

    def test_get_rate_for_value_no_match(self):
        """Test rate lookup for value with no matching tier"""
        table = ShippingRateTable.objects.create(
            name='Weight Tiers',
            basis_type='weight',
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('0'),
            max_value=Decimal('5'),
            rate=Money('10.00', 'USD'),
        )

        # 20kg has no matching tier
        rate = table.get_rate_for_value(Decimal('20.0'))
        self.assertIsNone(rate)

    def test_get_rate_for_value_open_ended_tier(self):
        """Test rate lookup with open-ended tier (no max)"""
        table = ShippingRateTable.objects.create(
            name='Weight Tiers',
            basis_type='weight',
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('0'),
            max_value=Decimal('10'),
            rate=Money('15.00', 'USD'),
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('10'),
            max_value=None,  # No maximum
            rate=Money('25.00', 'USD'),
        )

        # 50kg should match open-ended tier
        rate = table.get_rate_for_value(Decimal('50.0'))
        self.assertEqual(rate, Money('25.00', 'USD'))

    def test_tier_contains_value(self):
        """Test tier value containment check"""
        tier = ShippingRateTier(
            min_value=Decimal('5'),
            max_value=Decimal('10'),
            rate=Money('15.00', 'USD'),
        )

        self.assertTrue(tier.contains_value(Decimal('7.0')))
        self.assertTrue(tier.contains_value(Decimal('5.0')))
        self.assertTrue(tier.contains_value(Decimal('10.0')))
        self.assertFalse(tier.contains_value(Decimal('3.0')))
        self.assertFalse(tier.contains_value(Decimal('15.0')))

    def test_applies_to_address_with_zone(self):
        """Test rate table applies to specific zone"""
        zone = ShippingZone.objects.create(
            name='USA',
            countries=['US'],
        )

        table = ShippingRateTable.objects.create(
            name='USA Rates',
            basis_type='weight',
        )
        table.zones.add(zone)

        # US address should apply
        self.assertTrue(table.applies_to_address({'country': 'US'}))

        # Non-US address should not apply
        self.assertFalse(table.applies_to_address({'country': 'CA'}))

    def test_applies_to_address_no_zone_restriction(self):
        """Test rate table with no zone restriction applies to all"""
        table = ShippingRateTable.objects.create(
            name='Worldwide Rates',
            basis_type='weight',
        )

        # Any address should apply
        self.assertTrue(table.applies_to_address({'country': 'US'}))
        self.assertTrue(table.applies_to_address({'country': 'CA'}))
        self.assertTrue(table.applies_to_address({'country': 'GB'}))


class ShippingPromotionServiceTest(TestCase):
    """Test ShippingPromotionService"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create category for products
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Create cart with product
        self.cart = Cart.objects.create(user=self.user)
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            sku='TEST-SERVICE-001',
            price=Money('100.00', 'USD'),
            weight=Decimal('5.0'),
            category=self.category
        )
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
            unit_price=self.product.price
        )

        # Create shipping method
        self.shipping_method = ShippingMethod.objects.create(
            name='Standard',
            method_type='flat_rate',
            flat_rate_cost=Money('20.00', 'USD'),
            is_active=True,
        )

        # Create address
        self.address = {
            'country': 'US',
            'state': 'CA',
            'postal_code': '90210'
        }

    def test_evaluate_rules_no_rules(self):
        """Test evaluate_rules with no rules defined"""
        rules = ShippingRuleService.evaluate_rules(
            cart=self.cart,
            address=self.address,
            shipping_method=self.shipping_method,
            user=self.user
        )

        self.assertEqual(len(rules), 0)

    def test_evaluate_rules_single_matching_rule(self):
        """Test evaluate_rules with single matching rule"""
        rule = ShippingPromotion.objects.create(
            name='Free Shipping Over $100',
            promotion_type='free_shipping',
            min_cart_value=Money('100.00', 'USD'),
            priority=10,
            is_active=True,
        )

        rules = ShippingRuleService.evaluate_rules(
            cart=self.cart,
            address=self.address,
            shipping_method=self.shipping_method,
            user=self.user
        )

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0][0], rule)

    def test_evaluate_rules_non_matching_rule(self):
        """Test evaluate_rules with non-matching rule"""
        ShippingPromotion.objects.create(
            name='Free Shipping Over $500',
            promotion_type='free_shipping',
            min_cart_value=Money('500.00', 'USD'),  # Cart only has $200
            priority=10,
            is_active=True,
        )

        rules = ShippingRuleService.evaluate_rules(
            cart=self.cart,
            address=self.address,
            shipping_method=self.shipping_method,
            user=self.user
        )

        self.assertEqual(len(rules), 0)

    def test_evaluate_rules_priority_ordering(self):
        """Test rules are returned in priority order"""
        rule1 = ShippingPromotion.objects.create(
            name='Low Priority',
            promotion_type='discount_fixed',
            promotion_value=Money('5.00', 'USD'),
            priority=5,
            is_active=True,
        )

        rule2 = ShippingPromotion.objects.create(
            name='High Priority',
            promotion_type='discount_percentage',
            promotion_value=Money('10.00', 'USD'),
            priority=20,
            is_active=True,
        )

        rule3 = ShippingPromotion.objects.create(
            name='Medium Priority',
            promotion_type='override_cost',
            promotion_value=Money('10.00', 'USD'),
            priority=10,
            is_active=True,
        )

        rules = ShippingRuleService.evaluate_rules(
            cart=self.cart,
            address=self.address,
            shipping_method=self.shipping_method,
            user=self.user
        )

        # Should be ordered by priority descending
        self.assertEqual(len(rules), 3)
        self.assertEqual(rules[0][0], rule2)  # Priority 20
        self.assertEqual(rules[1][0], rule3)  # Priority 10
        self.assertEqual(rules[2][0], rule1)  # Priority 5

    def test_evaluate_rules_stop_further_promotions(self):
        """Test stop_further_promotions flag stops evaluation"""
        rule1 = ShippingPromotion.objects.create(
            name='High Priority Stop',
            promotion_type='free_shipping',
            priority=20,
            stop_further_promotions=True,
            is_active=True,
        )

        rule2 = ShippingPromotion.objects.create(
            name='Lower Priority',
            promotion_type='discount_fixed',
            promotion_value=Money('5.00', 'USD'),
            priority=10,
            is_active=True,
        )

        rules = ShippingRuleService.evaluate_rules(
            cart=self.cart,
            address=self.address,
            shipping_method=self.shipping_method,
            user=self.user
        )

        # Only first rule should be returned
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0][0], rule1)

    def test_calculate_shipping_with_rules_no_rules(self):
        """Test calculate_shipping_with_rules with no rules"""
        base_cost = Money('20.00', 'USD')

        result = ShippingRuleService.calculate_shipping_with_rules(
            base_cost=base_cost,
            cart=self.cart,
            address=self.address,
            shipping_method=self.shipping_method,
            user=self.user
        )

        self.assertEqual(result['base_cost'], base_cost)
        self.assertEqual(result['final_cost'], base_cost)
        self.assertEqual(len(result['rules_applied']), 0)
        self.assertEqual(result['total_discount'], Money('0.00', 'USD'))

    def test_calculate_shipping_with_rules_free_shipping(self):
        """Test calculate_shipping_with_rules with free shipping rule"""
        ShippingPromotion.objects.create(
            name='Free Shipping',
            promotion_type='free_shipping',
            min_cart_value=Money('100.00', 'USD'),
            priority=10,
            is_active=True,
        )

        base_cost = Money('20.00', 'USD')

        result = ShippingRuleService.calculate_shipping_with_rules(
            base_cost=base_cost,
            cart=self.cart,
            address=self.address,
            shipping_method=self.shipping_method,
            user=self.user
        )

        self.assertEqual(result['base_cost'], Money('20.00', 'USD'))
        self.assertEqual(result['final_cost'], Money('0.00', 'USD'))
        self.assertEqual(len(result['rules_applied']), 1)
        self.assertEqual(result['total_discount'], Money('20.00', 'USD'))

    def test_calculate_shipping_with_rules_multiple_rules(self):
        """Test calculate_shipping_with_rules with multiple rules"""
        # First: 50% discount (priority 20)
        ShippingPromotion.objects.create(
            name='50% Off',
            promotion_type='discount_percentage',
            promotion_value=Money('50.00', 'USD'),
            priority=20,
            is_active=True,
        )

        # Second: $5 additional discount (priority 10)
        ShippingPromotion.objects.create(
            name='$5 Off',
            promotion_type='discount_fixed',
            promotion_value=Money('5.00', 'USD'),
            priority=10,
            is_active=True,
        )

        base_cost = Money('20.00', 'USD')

        result = ShippingRuleService.calculate_shipping_with_rules(
            base_cost=base_cost,
            cart=self.cart,
            address=self.address,
            shipping_method=self.shipping_method,
            user=self.user
        )

        # $20 -> 50% off = $10 -> $5 off = $5
        self.assertEqual(result['base_cost'], Money('20.00', 'USD'))
        self.assertEqual(result['final_cost'], Money('5.00', 'USD'))
        self.assertEqual(len(result['rules_applied']), 2)
        self.assertEqual(result['total_discount'], Money('15.00', 'USD'))

    def test_calculate_rate_table_cost_weight_based(self):
        """Test calculate_rate_table_cost with weight-based table"""
        table = ShippingRateTable.objects.create(
            name='Weight Rates',
            basis_type='weight',
            shipping_method=self.shipping_method,
            is_active=True,
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('0'),
            max_value=Decimal('10'),
            rate=Money('15.00', 'USD'),
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('10'),
            max_value=None,
            rate=Money('25.00', 'USD'),
        )

        # Cart has 10kg (5kg x 2)
        cost = ShippingRuleService.calculate_rate_table_cost(
            shipping_method=self.shipping_method,
            cart=self.cart,
            address=self.address
        )

        self.assertEqual(cost, Money('15.00', 'USD'))

    def test_calculate_rate_table_cost_price_based(self):
        """Test calculate_rate_table_cost with price-based table"""
        # Change shipping method to price_based
        self.shipping_method.method_type = 'price_based'
        self.shipping_method.save()

        table = ShippingRateTable.objects.create(
            name='Price Rates',
            basis_type='price',
            shipping_method=self.shipping_method,
            is_active=True,
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('0'),
            max_value=Decimal('100'),
            rate=Money('10.00', 'USD'),
        )

        ShippingRateTier.objects.create(
            rate_table=table,
            min_value=Decimal('100'),
            max_value=None,
            rate=Money('5.00', 'USD'),
        )

        # Cart has $200
        cost = ShippingRuleService.calculate_rate_table_cost(
            shipping_method=self.shipping_method,
            cart=self.cart,
            address=self.address
        )

        self.assertEqual(cost, Money('5.00', 'USD'))

    def test_calculate_shipping_for_cart_complete(self):
        """Test complete shipping calculation for cart"""
        # Create rule
        ShippingPromotion.objects.create(
            name='25% Off',
            promotion_type='discount_percentage',
            promotion_value=Money('25.00', 'USD'),
            priority=10,
            is_active=True,
        )

        result = ShippingRuleService.calculate_shipping_for_cart(
            cart=self.cart,
            shipping_method=self.shipping_method,
            address=self.address,
            user=self.user
        )

        self.assertEqual(result['method_name'], 'Standard')
        self.assertEqual(result['method_type'], 'flat_rate')
        self.assertEqual(result['base_cost'], Money('20.00', 'USD'))
        self.assertEqual(result['final_cost'], Money('15.00', 'USD'))  # 25% off
        self.assertEqual(len(result['rules_applied']), 1)
        self.assertIn('calculation_breakdown', result)


class CartShippingIntegrationTest(TestCase):
    """Test Cart.calculate_shipping() integration with rule engine"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create category for products
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Create cart with product
        self.cart = Cart.objects.create(user=self.user)
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            sku='TEST-CART-001',
            price=Money('100.00', 'USD'),
            weight=Decimal('5.0'),
            category=self.category,
        )
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
            unit_price=self.product.price
        )

        # Create shipping method
        self.shipping_method = ShippingMethod.objects.create(
            name='Standard',
            method_type='flat_rate',
            flat_rate_cost=Money('20.00', 'USD'),
            is_active=True,
        )

        self.address = {
            'country': 'US',
            'state': 'CA',
            'postal_code': '90210'
        }

    def test_calculate_shipping_with_method_and_rules(self):
        """Test Cart.calculate_shipping() with method and rules"""
        # Create free shipping rule
        ShippingPromotion.objects.create(
            name='Free Shipping Over $100',
            promotion_type='free_shipping',
            min_cart_value=Money('100.00', 'USD'),
            priority=10,
            is_active=True,
        )

        result = self.cart.calculate_shipping(
            shipping_address=self.address,
            shipping_method=self.shipping_method,
            user=self.user
        )

        self.assertEqual(result['shipping_cost'], Money('0.00', 'USD'))
        self.assertEqual(result['base_cost'], Money('20.00', 'USD'))
        self.assertEqual(len(result['rules_applied']), 1)
        self.assertIn('Free Shipping Over $100', result['rules_applied'][0]['promotion_name'])

    def test_calculate_shipping_get_available_methods_with_rules(self):
        """Test getting available methods with rule-adjusted costs"""
        # Create another method
        ShippingMethod.objects.create(
            name='Express',
            method_type='flat_rate',
            flat_rate_cost=Money('50.00', 'USD'),
            is_active=True,
        )

        # Create rule that gives 50% off
        ShippingPromotion.objects.create(
            name='50% Off All Shipping',
            promotion_type='discount_percentage',
            promotion_value=Money('50.00', 'USD'),
            priority=10,
            is_active=True,
        )

        result = self.cart.calculate_shipping(
            shipping_address=self.address,
            shipping_method=None,  # Get all methods
            user=self.user
        )

        self.assertEqual(len(result['available_methods']), 2)

        # Find methods by name (order not guaranteed)
        methods_by_name = {m['name']: m for m in result['available_methods']}

        # Check Standard method
        standard = methods_by_name['Standard']
        self.assertEqual(standard['base_cost'], Money('20.00', 'USD'))
        self.assertEqual(standard['cost'], Money('10.00', 'USD'))  # 50% off

        # Check Express method
        express = methods_by_name['Express']
        self.assertEqual(express['base_cost'], Money('50.00', 'USD'))
        self.assertEqual(express['cost'], Money('25.00', 'USD'))  # 50% off

    def test_calculate_shipping_no_shipping_required(self):
        """Test calculate_shipping for digital products (no shipping)"""
        # Make product digital
        self.product.product_type = 'digital'
        self.product.save()

        result = self.cart.calculate_shipping(
            shipping_address=self.address,
            shipping_method=self.shipping_method,
            user=self.user
        )

        self.assertEqual(result['shipping_cost'], Money('0.00', 'USD'))
        self.assertIn('No shipping required', result['message'])
