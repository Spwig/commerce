"""
Management command to seed showcase data for marketing screenshots.

Creates 12 months of realistic engagement data across all dashboard widgets:
orders, customers, vouchers, affiliates, loyalty, referrals, traffic,
shipments, email campaigns, reviews, and abandoned carts.

Uses existing products in the database (user must create products first).

Usage:
    python manage.py seed_showcase_data
    python manage.py seed_showcase_data --reset
    python manage.py seed_showcase_data --dry-run
"""

import random
import secrets
import uuid
from contextlib import contextmanager
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone

User = get_user_model()

# ── Constants ──────────────────────────────────────────────────────────────

SHOWCASE_EMAIL_DOMAIN = 'example.com'
SHOWCASE_EMAIL_PREFIX = 'showcase_'
AFFILIATE_EMAIL_PREFIX = 'affiliate_showcase_'
ORDER_PREFIX = 'SC-'

CUSTOMER_NAMES = [
    ('Emma', 'Johnson'), ('Liam', 'Williams'), ('Olivia', 'Brown'),
    ('Noah', 'Jones'), ('Ava', 'Garcia'), ('Elijah', 'Martinez'),
    ('Sophia', 'Davis'), ('James', 'Rodriguez'), ('Isabella', 'Wilson'),
    ('Oliver', 'Anderson'), ('Mia', 'Thomas'), ('Benjamin', 'Taylor'),
    ('Charlotte', 'Moore'), ('Lucas', 'Jackson'), ('Amelia', 'Martin'),
    ('Mason', 'Lee'), ('Harper', 'Perez'), ('Logan', 'Thompson'),
    ('Evelyn', 'White'), ('Alexander', 'Harris'), ('Abigail', 'Sanchez'),
    ('Henry', 'Clark'), ('Emily', 'Lewis'), ('Sebastian', 'Robinson'),
    ('Ella', 'Walker'), ('Jack', 'Young'), ('Scarlett', 'Allen'),
    ('Aiden', 'King'), ('Grace', 'Wright'), ('Samuel', 'Scott'),
    ('Chloe', 'Torres'), ('Owen', 'Nguyen'), ('Victoria', 'Hill'),
    ('Daniel', 'Flores'), ('Lily', 'Green'), ('Matthew', 'Adams'),
    ('Hannah', 'Nelson'), ('Joseph', 'Baker'), ('Zoe', 'Hall'),
    ('David', 'Rivera'), ('Nora', 'Campbell'), ('Carter', 'Mitchell'),
    ('Riley', 'Carter'), ('Wyatt', 'Roberts'), ('Layla', 'Gomez'),
    ('Gabriel', 'Phillips'), ('Penelope', 'Evans'), ('Julian', 'Turner'),
    ('Aria', 'Diaz'), ('Grayson', 'Parker'), ('Camila', 'Cruz'),
    ('Leo', 'Edwards'), ('Aubrey', 'Collins'), ('Isaac', 'Reyes'),
    ('Zoey', 'Stewart'), ('Lincoln', 'Sanchez'), ('Savannah', 'Morris'),
    ('Asher', 'Rogers'), ('Stella', 'Reed'), ('Levi', 'Cook'),
    ('Hazel', 'Morgan'), ('Mateo', 'Bell'), ('Ellie', 'Murphy'),
    ('Ryan', 'Bailey'), ('Aurora', 'Cooper'), ('Caleb', 'Richardson'),
    ('Paisley', 'Cox'), ('Nathan', 'Howard'), ('Willow', 'Ward'),
    ('Ezra', 'Peterson'), ('Addison', 'Gray'), ('Thomas', 'Ramirez'),
    ('Brooklyn', 'James'), ('Hunter', 'Watson'), ('Violet', 'Brooks'),
    ('Jayden', 'Kelly'), ('Bella', 'Sanders'), ('Dylan', 'Price'),
    ('Lucy', 'Bennett'), ('Adrian', 'Wood'),
]

AFFILIATE_NAMES = [
    ('Sarah', 'Miller'), ('Chris', 'Davis'), ('Alex', 'Wilson'),
    ('Jordan', 'Lee'), ('Taylor', 'Brown'), ('Morgan', 'Smith'),
    ('Casey', 'Jones'), ('Pat', 'Garcia'), ('Jamie', 'Martinez'),
    ('Drew', 'Anderson'), ('Sam', 'Thomas'), ('Quinn', 'Jackson'),
    ('Blake', 'White'), ('Avery', 'Harris'), ('Reese', 'Clark'),
    ('Sage', 'Lewis'), ('Parker', 'Walker'), ('Emery', 'Hall'),
]

# Geographic distribution for orders and visitors
COUNTRIES = [
    {'code': 'US', 'name': 'United States', 'cities': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami'], 'weight': 35},
    {'code': 'GB', 'name': 'United Kingdom', 'cities': ['London', 'Manchester', 'Birmingham', 'Leeds'], 'weight': 12},
    {'code': 'DE', 'name': 'Germany', 'cities': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt'], 'weight': 10},
    {'code': 'CA', 'name': 'Canada', 'cities': ['Toronto', 'Vancouver', 'Montreal', 'Calgary'], 'weight': 8},
    {'code': 'AU', 'name': 'Australia', 'cities': ['Sydney', 'Melbourne', 'Brisbane', 'Perth'], 'weight': 7},
    {'code': 'FR', 'name': 'France', 'cities': ['Paris', 'Lyon', 'Marseille', 'Toulouse'], 'weight': 6},
    {'code': 'JP', 'name': 'Japan', 'cities': ['Tokyo', 'Osaka', 'Yokohama', 'Nagoya'], 'weight': 5},
    {'code': 'BR', 'name': 'Brazil', 'cities': ['São Paulo', 'Rio de Janeiro', 'Brasília'], 'weight': 4},
    {'code': 'IN', 'name': 'India', 'cities': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai'], 'weight': 4},
    {'code': 'NL', 'name': 'Netherlands', 'cities': ['Amsterdam', 'Rotterdam', 'Utrecht'], 'weight': 3},
    {'code': 'SE', 'name': 'Sweden', 'cities': ['Stockholm', 'Gothenburg', 'Malmö'], 'weight': 2},
    {'code': 'SG', 'name': 'Singapore', 'cities': ['Singapore'], 'weight': 2},
    {'code': 'AE', 'name': 'UAE', 'cities': ['Dubai', 'Abu Dhabi'], 'weight': 2},
]

REVIEW_TEMPLATES = [
    (5, 'Amazing quality!', 'Exceeded my expectations. The quality is outstanding and delivery was fast.'),
    (5, 'Love it!', 'Exactly what I was looking for. Will definitely buy again.'),
    (5, 'Perfect fit', 'Fits perfectly and looks even better in person. Highly recommend.'),
    (5, 'Great purchase', 'Very happy with this purchase. The material feels premium.'),
    (5, 'Fantastic!', 'Beautiful design and excellent craftsmanship. Worth every penny.'),
    (5, 'Five stars', 'Absolutely love this product. Fast shipping too!'),
    (5, 'Best purchase', 'This is by far the best purchase I\'ve made this year.'),
    (5, 'Impressed', 'Really impressed with the quality. Packaging was also lovely.'),
    (4, 'Very good', 'Great product overall. Minor packaging issue but the item itself is excellent.'),
    (4, 'Really nice', 'Love the design. Slightly smaller than expected but still great.'),
    (4, 'Good quality', 'Nice quality for the price. Would recommend to friends.'),
    (4, 'Happy customer', 'Very satisfied with the product. Shipping was a bit slow but worth the wait.'),
    (4, 'Solid choice', 'Good product, well made. Color is slightly different from the photo.'),
    (4, 'Recommended', 'Would definitely recommend. Just wish there were more color options.'),
    (4, 'Nice product', 'Overall very pleased. The material is high quality.'),
    (4, 'Great value', 'Excellent value for money. Quality exceeded expectations.'),
    (3, 'Decent', 'Decent product but nothing special. Serves its purpose.'),
    (3, 'OK product', 'It\'s okay. Expected slightly better quality at this price point.'),
    (3, 'Average', 'Average quality. Delivery was fine but the product is just okay.'),
    (3, 'Mixed feelings', 'Design is nice but material feels a bit thin. Okay for the price.'),
    (2, 'Disappointed', 'Not as described. The color is quite different from the photos.'),
    (2, 'Below expectations', 'Expected better quality. Stitching seems loose in places.'),
    (2, 'Not great', 'Product arrived late and quality is mediocre. Would not repurchase.'),
    (1, 'Poor quality', 'Very disappointed with the quality. Does not match the description.'),
    (1, 'Would not recommend', 'Product fell apart after first use. Very poor construction.'),
]

UTM_CAMPAIGNS = [
    {'source': 'google', 'medium': 'cpc', 'campaign': 'spring_collection_2025', 'term': 'fashion online', 'content': 'search_ad_v1'},
    {'source': 'facebook', 'medium': 'social', 'campaign': 'new_arrivals', 'term': '', 'content': 'carousel_ad'},
    {'source': 'newsletter', 'medium': 'email', 'campaign': 'weekly_deals', 'term': '', 'content': 'header_cta'},
    {'source': 'instagram', 'medium': 'social', 'campaign': 'influencer_collab', 'term': '', 'content': 'story_swipe'},
    {'source': 'google', 'medium': 'organic', 'campaign': '', 'term': '', 'content': ''},
    {'source': 'tiktok', 'medium': 'social', 'campaign': 'trending_styles', 'term': '', 'content': 'in_feed_ad'},
    {'source': 'youtube', 'medium': 'video', 'campaign': 'style_guide', 'term': '', 'content': 'pre_roll'},
    {'source': 'pinterest', 'medium': 'social', 'campaign': 'lookbook', 'term': '', 'content': 'promoted_pin'},
    {'source': 'bing', 'medium': 'cpc', 'campaign': 'brand_terms', 'term': 'spwig fashion', 'content': 'text_ad'},
]

REFERRER_URLS = [
    ('https://www.google.com/search?q=fashion+online', 25),
    ('https://www.facebook.com/', 12),
    ('https://www.instagram.com/', 8),
    ('https://www.pinterest.com/', 5),
    ('https://www.youtube.com/', 4),
    ('https://www.tiktok.com/', 4),
    ('https://www.reddit.com/r/fashion/', 3),
    ('https://twitter.com/', 3),
    ('https://www.linkedin.com/', 2),
    ('https://news.ycombinator.com/', 2),
    ('https://www.vogue.com/', 2),
    ('https://www.elle.com/', 2),
    ('', 18),  # Direct traffic
    ('https://www.bing.com/', 5),
    ('https://duckduckgo.com/', 3),
    ('https://www.refinery29.com/', 2),
]

VOUCHER_DEFINITIONS = [
    {'code': 'WELCOME10', 'name': 'Welcome 10% Off', 'discount_type': 'percentage', 'discount_value': 10, 'max_uses_total': 200, 'target_uses': 145, 'active': True, 'first_time': False},
    {'code': 'SUMMER25', 'name': 'Summer Sale 25%', 'discount_type': 'percentage', 'discount_value': 25, 'max_uses_total': 100, 'target_uses': 87, 'active': False, 'first_time': False},
    {'code': 'FREESHIP', 'name': 'Free Shipping', 'discount_type': 'fixed', 'discount_value': 0, 'max_uses_total': 500, 'target_uses': 312, 'active': True, 'first_time': False},
    {'code': 'VIP20', 'name': 'VIP 20% Discount', 'discount_type': 'percentage', 'discount_value': 20, 'max_uses_total': 0, 'target_uses': 56, 'active': True, 'first_time': False},
    {'code': 'FLASH50', 'name': 'Flash Sale 50% Off', 'discount_type': 'percentage', 'discount_value': 50, 'max_uses_total': 50, 'target_uses': 50, 'active': False, 'first_time': False},
    {'code': 'NEWUSER', 'name': 'New Customer 15%', 'discount_type': 'percentage', 'discount_value': 15, 'max_uses_total': 0, 'target_uses': 89, 'active': True, 'first_time': True},
    {'code': 'HOLIDAY30', 'name': 'Holiday 30% Off', 'discount_type': 'percentage', 'discount_value': 30, 'max_uses_total': 300, 'target_uses': 201, 'active': False, 'first_time': False},
    {'code': 'LOYALTY15', 'name': 'Loyalty Reward 15%', 'discount_type': 'percentage', 'discount_value': 15, 'max_uses_total': 0, 'target_uses': 34, 'active': True, 'first_time': False},
]

USER_AGENTS = {
    'desktop': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    ],
    'mobile': [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
    ],
    'tablet': [
        'Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 14; SM-X900) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    ],
    'unknown': [
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    ],
}

ABANDONMENT_REASONS_WEIGHTED = [
    ('unknown', 30),
    ('high_shipping', 25),
    ('total_too_high', 20),
    ('comparison_shopping', 15),
    ('save_for_later', 10),
]

CUSTOMER_MESSAGE_TEMPLATES = [
    # (message_type, subject, message, reply_text_or_None)
    ('order', 'Where is my order?',
     'Hi, I placed an order 5 days ago and haven\'t received any tracking info yet. Could you please check on this for me? My order number is {order_number}.',
     'Thank you for reaching out! I\'ve checked your order and it\'s currently being processed. You should receive tracking information within 24 hours. Please don\'t hesitate to contact us if you have any further questions.'),
    ('order', 'Can I change my shipping address?',
     'I just realized I entered the wrong shipping address on my recent order {order_number}. Is it possible to update it before it ships?',
     'I\'ve updated the shipping address on your order. The change has been applied before the package was dispatched. You\'ll receive a confirmation email shortly.'),
    ('order', 'Request for invoice',
     'Could you please send me an invoice for order {order_number}? I need it for my business records.',
     'Of course! I\'ve generated an invoice for your order and sent it to your email address. Let us know if you need anything else.'),
    ('product', 'Product availability question',
     'Hi, I noticed the product I\'m interested in is currently showing low stock. Will you be restocking it soon? I\'d like to buy a few for gifts.',
     'Great news! We have a restock scheduled for next week. I can notify you as soon as it\'s available if you\'d like. We also offer a wishlist feature so you can save items for later.'),
    ('product', 'Size guide question',
     'Could you help me with sizing? I\'m between a medium and large and want to make sure I order the right size.',
     'Thanks for asking! Our items tend to run true to size. If you\'re between sizes, we\'d recommend going with the larger option for a more comfortable fit. We also offer free exchanges if the fit isn\'t quite right.'),
    ('product', 'Do you offer gift wrapping?',
     'I\'m buying this as a birthday present. Do you offer any gift wrapping options?',
     None),
    ('general', 'Wholesale inquiry',
     'We\'re a retail store interested in carrying your products. Do you offer wholesale pricing or bulk discounts? We\'d love to discuss a potential partnership.',
     'Thank you for your interest in our products! We do offer wholesale pricing for qualified retailers. I\'ll have our wholesale team reach out to you within 1-2 business days to discuss pricing and terms.'),
    ('general', 'International shipping',
     'Do you ship to Australia? If so, what are the estimated shipping times and costs?',
     'Yes, we do ship to Australia! Standard international shipping typically takes 7-14 business days. Shipping costs are calculated at checkout based on the weight and dimensions of your order. We also offer express shipping for faster delivery.'),
    ('general', 'Return policy question',
     'What is your return policy? I want to make sure I can return items if they don\'t work out.',
     None),
    ('support', 'Issue with my account',
     'I\'m having trouble logging into my account. I\'ve tried resetting my password but I\'m not receiving the reset email. Can you help?',
     'I\'m sorry to hear about the login issues. I\'ve manually sent a password reset link to your email address. Please also check your spam/junk folder. If you still don\'t receive it within 15 minutes, please let us know and we\'ll assist you further.'),
    ('support', 'Payment declined',
     'My payment keeps getting declined even though my card works everywhere else. Is there an issue with your payment system?',
     'I apologize for the inconvenience. This can sometimes happen due to your bank\'s security settings. Could you try using a different payment method or contacting your bank to authorize the transaction? We also accept PayPal as an alternative.'),
    ('support', 'Damaged item received',
     'I received my order today but unfortunately one of the items arrived damaged. The packaging was intact so it seems like a manufacturing defect. What should I do?',
     'I\'m very sorry about the damaged item. We take product quality seriously. Please don\'t worry - I\'ve arranged for a replacement to be shipped to you immediately at no charge. You don\'t need to return the damaged item. Your replacement tracking number will be sent to your email.'),
    ('support', 'Discount code not working',
     'I\'m trying to use the WELCOME10 discount code but it says it\'s invalid. I\'m a first-time customer so it should work, right?',
     'I apologize for the trouble with the discount code. I\'ve looked into it and applied the 10% discount directly to your account. You should be able to see it applied at checkout now. Let me know if you need any further assistance!'),
    ('product', 'Color accuracy question',
     'The product photos look great but I\'m wondering how accurate the colors are. Is the blue more of a navy or a royal blue?',
     None),
    ('general', 'Sustainability practices',
     'I\'d love to know more about your sustainability practices. Are your products eco-friendly? Do you use sustainable packaging?',
     'Thank you for caring about sustainability! We\'re committed to reducing our environmental impact. Our packaging is made from recycled materials, and we\'re working with our suppliers to improve sustainability across our supply chain. We\'d be happy to share more details about specific products.'),
    ('order', 'Cancel my order',
     'I just placed an order but I changed my mind. Can you please cancel order {order_number} and refund my payment?',
     'I\'ve processed the cancellation for your order. The refund will be credited to your original payment method within 3-5 business days. We\'re sorry to see you go - please don\'t hesitate to reach out if you change your mind!'),
    ('support', 'Website loading slowly',
     'Your website has been really slow for me today. Pages are taking forever to load. Is anyone else experiencing this?',
     None),
    ('general', 'Collaboration opportunity',
     'I\'m a content creator with 50K followers and I\'d love to collaborate with your brand. Do you have an influencer program?',
     'Thank you for reaching out! We love working with content creators. I\'ve forwarded your details to our marketing team and they\'ll be in touch within a few days to discuss potential collaboration opportunities.'),
]


@contextmanager
def disable_auto_now(model, field_names):
    """Temporarily disable auto_now/auto_now_add so explicit values are accepted."""
    modified = []
    for field in model._meta.local_fields:
        if field.name in field_names:
            state = (field, field.auto_now, field.auto_now_add)
            if field.auto_now or field.auto_now_add:
                field.auto_now = False
                field.auto_now_add = False
                modified.append(state)
    try:
        yield
    finally:
        for field, was_auto_now, was_auto_now_add in modified:
            field.auto_now = was_auto_now
            field.auto_now_add = was_auto_now_add


def _weighted_choice(items_with_weights):
    """Select item from list of (item, weight) tuples."""
    items = [i[0] for i in items_with_weights]
    weights = [i[1] for i in items_with_weights]
    return random.choices(items, weights=weights, k=1)[0]


def _pick_country():
    """Pick a random country based on weight distribution."""
    return _weighted_choice([(c, c['weight']) for c in COUNTRIES])


def _bell_curve_amount(low, high, center):
    """Generate a value on a rough bell curve between low and high, centered on center."""
    # Use triangular distribution for simplicity
    return Decimal(str(round(random.triangular(low, high, center), 2)))


class Command(BaseCommand):
    help = 'Seed showcase data for marketing dashboard screenshots'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Delete existing showcase data first')
        parser.add_argument('--dry-run', action='store_true', help='Show what would be created')

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.now = timezone.now()
        self.year_ago = self.now - timedelta(days=365)
        self.currency = 'USD'

        # Seed random for reproducibility
        random.seed(42)

        if options['reset']:
            self._reset()
            if self.dry_run:
                return

        # Validate prerequisites
        if not self._validate_prerequisites():
            return

        # Load existing products
        from catalog.models import Product
        self.products = list(Product.objects.filter(status='published'))
        if not self.products:
            self.products = list(Product.objects.all()[:50])

        # Weight some products as "bestsellers" (first 30% get 3x weight)
        bestseller_count = max(1, len(self.products) // 3)
        self.product_weights = []
        for i, p in enumerate(self.products):
            self.product_weights.append(3 if i < bestseller_count else 1)

        self.stdout.write(self.style.SUCCESS(f'\nUsing {len(self.products)} existing products\n'))

        # Determine currency from SiteSettings
        try:
            from core.models import SiteSettings
            settings = SiteSettings.objects.first()
            if settings and settings.default_currency:
                self.currency = settings.default_currency
        except Exception:
            pass

        self.stdout.write(f'Currency: {self.currency}\n')

        # Run phases in order
        phases = [
            ('Phase 1: Customers', self._create_customers),
            ('Phase 2: Visitors/Traffic', self._create_visitors),
            ('Phase 3: Orders', self._create_orders),
            ('Phase 4: Vouchers', self._create_vouchers),
            ('Phase 5: Affiliates', self._create_affiliates),
            ('Phase 6: Loyalty Program', self._create_loyalty),
            ('Phase 7: Referral Program', self._create_referrals),
            ('Phase 8: Shipments', self._create_shipments),
            ('Phase 9: Email Campaigns', self._create_email_campaigns),
            ('Phase 10: Product Reviews', self._create_reviews),
            ('Phase 11: Abandoned Carts', self._create_abandoned_carts),
            ('Phase 12: Customer Metrics', self._compute_customer_metrics),
            ('Phase 13: Stock Adjustments', self._adjust_stock),
            ('Phase 14: Customer Messages', self._create_customer_messages),
        ]

        for name, func in phases:
            self.stdout.write(f'\n{name}...')
            if self.dry_run:
                self.stdout.write(self.style.WARNING('  [DRY RUN] Skipped'))
                continue
            try:
                func()
                self.stdout.write(self.style.SUCCESS(f'  ✓ {name} complete'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'  ✗ {name} failed: {e}'))
                import traceback
                traceback.print_exc()

        self.stdout.write(self.style.SUCCESS('\n✅ Showcase data seeding complete!\n'))

    # ── Prerequisites ──────────────────────────────────────────────────

    def _validate_prerequisites(self):
        from catalog.models import Product
        product_count = Product.objects.filter(status='published').count()
        if product_count == 0:
            product_count = Product.objects.count()
        if product_count < 5:
            self.stderr.write(self.style.ERROR(
                f'Need at least 5 products in the database (found {product_count}).\n'
                'Create products with prices and cost fields before running this command.'
            ))
            return False
        return True

    # ── Reset ──────────────────────────────────────────────────────────

    def _reset(self):
        self.stdout.write('\nResetting showcase data...')

        if self.dry_run:
            self.stdout.write(self.style.WARNING('  [DRY RUN] Would delete all showcase data'))
            return

        from orders.models import Order, OrderItem
        from geoip.models import VisitorLocation
        from vouchers.models import VoucherCode, VoucherUsage
        from catalog.models import ProductReview
        from customers.models import AbandonedCart, CustomerMetrics
        from cart.models import Cart

        # Delete in reverse dependency order
        showcase_users = User.objects.filter(email__startswith=SHOWCASE_EMAIL_PREFIX, email__endswith=f'@{SHOWCASE_EMAIL_DOMAIN}')
        affiliate_users = User.objects.filter(email__startswith=AFFILIATE_EMAIL_PREFIX, email__endswith=f'@{SHOWCASE_EMAIL_DOMAIN}')
        all_showcase_users = User.objects.filter(
            models.Q(email__startswith=SHOWCASE_EMAIL_PREFIX) | models.Q(email__startswith=AFFILIATE_EMAIL_PREFIX),
            email__endswith=f'@{SHOWCASE_EMAIL_DOMAIN}'
        )
        showcase_orders = Order.objects.filter(order_number__startswith=ORDER_PREFIX)

        # Referrals (PROTECT FKs require explicit deletion before users)
        try:
            from referrals.models import ReferralEvent, ReferralReward, ReferralAttribution, ReferralIdentity, ReferralProgram
        except ImportError:
            pass
        else:
            ReferralEvent.objects.filter(referrer_identity__customer__in=all_showcase_users).delete()
            ReferralReward.objects.filter(customer__in=all_showcase_users).delete()
            ReferralAttribution.objects.filter(referee_customer__in=all_showcase_users).delete()
            ReferralIdentity.objects.filter(customer__in=all_showcase_users).delete()
            ReferralProgram.objects.filter(name='Showcase Referral Program').delete()

        # Loyalty (LoyaltyTransaction/Redemption use PROTECT on member FK)
        try:
            from loyalty.models import LoyaltyRedemption, LoyaltyTransaction, LoyaltyBalance, LoyaltyMember, LoyaltyReward, LoyaltyRule, LoyaltyTier
        except ImportError:
            pass
        else:
            LoyaltyRedemption.objects.filter(member__customer__in=all_showcase_users).delete()
            LoyaltyTransaction.objects.filter(member__customer__in=all_showcase_users).delete()
            LoyaltyBalance.objects.filter(member__customer__in=all_showcase_users).delete()
            LoyaltyMember.objects.filter(customer__in=all_showcase_users).delete()
            LoyaltyReward.objects.filter(name__startswith='Showcase').delete()
            LoyaltyRule.objects.filter(name__startswith='Showcase').delete()
            LoyaltyTier.objects.filter(name__in=['Bronze', 'Silver', 'Gold', 'Platinum']).delete()

        # Affiliates
        try:
            from affiliate.models import Payout, Commission, Click, Link, AffiliateProgramMembership, Affiliate, Program
        except ImportError:
            pass
        else:
            Payout.objects.filter(affiliate__user__in=affiliate_users).delete()
            Commission.objects.filter(affiliate__user__in=affiliate_users).delete()
            Click.objects.filter(link__affiliate__user__in=affiliate_users).delete()
            Link.objects.filter(affiliate__user__in=affiliate_users).delete()
            AffiliateProgramMembership.objects.filter(affiliate__user__in=affiliate_users).delete()
            Affiliate.objects.filter(user__in=affiliate_users).delete()
            Program.objects.filter(name='Spwig Partners').delete()

        # Shipments
        try:
            from shipping.models import TrackingEvent, Shipment
        except ImportError:
            pass
        else:
            showcase_shipments = Shipment.objects.filter(order__in=showcase_orders)
            TrackingEvent.objects.filter(shipment__in=showcase_shipments).delete()
            showcase_shipments.delete()

        # Email
        try:
            from email_system.models import EmailEvent, EmailOutbox
        except ImportError:
            pass
        else:
            showcase_emails = EmailOutbox.objects.filter(to_email__startswith=SHOWCASE_EMAIL_PREFIX)
            EmailEvent.objects.filter(email__in=showcase_emails).delete()
            showcase_emails.delete()

        # Customer messages
        try:
            from admin_api.models import CustomerMessage
        except ImportError:
            pass
        else:
            CustomerMessage.objects.filter(user__in=all_showcase_users).delete()

        # Abandoned carts
        AbandonedCart.objects.filter(user__in=all_showcase_users).delete()
        Cart.objects.filter(session_key__startswith='showcase_').delete()

        # Voucher usage and vouchers
        showcase_codes = [v['code'] for v in VOUCHER_DEFINITIONS]
        VoucherUsage.objects.filter(voucher__code__in=showcase_codes).delete()
        VoucherCode.objects.filter(code__in=showcase_codes).delete()

        # Reviews
        ProductReview.objects.filter(user__in=all_showcase_users).delete()

        # Customer metrics
        CustomerMetrics.objects.filter(user__in=all_showcase_users).delete()

        # Order items and orders
        OrderItem.objects.filter(order__in=showcase_orders).delete()
        showcase_orders.delete()

        # Visitors
        VisitorLocation.objects.filter(session_key__startswith='showcase_').delete()

        # Users (last, since all FK dependencies cleared above)
        affiliate_users.delete()
        showcase_users.delete()

        self.stdout.write(self.style.SUCCESS('  ✓ Showcase data cleared'))

    # ── Phase 1: Customers ─────────────────────────────────────────────

    def _create_customers(self):
        from accounts.models import CustomerProfile

        self.showcase_users = []
        for i, (first, last) in enumerate(CUSTOMER_NAMES[:80]):
            email = f'{SHOWCASE_EMAIL_PREFIX}{i}@{SHOWCASE_EMAIL_DOMAIN}'
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': f'showcase_{i}',
                    'first_name': first,
                    'last_name': last,
                    'is_active': True,
                }
            )
            if not created and not user.first_name:
                user.first_name = first
                user.last_name = last
                user.save(update_fields=['first_name', 'last_name'])
            # Ensure CustomerProfile exists for admin visibility
            CustomerProfile.get_or_create_for_user(user)
            self.showcase_users.append(user)

        self.stdout.write(f'  Created {len(self.showcase_users)} customers')

    # ── Phase 2: Visitors/Traffic ──────────────────────────────────────

    def _create_visitors(self):
        from geoip.models import VisitorLocation

        count = 2000
        # Monthly distribution with growth (more recent = more visitors)
        monthly_weights = [4, 5, 5, 6, 6, 7, 8, 8, 9, 10, 12, 14]  # % per month
        device_types = [('desktop', 38), ('mobile', 48), ('tablet', 10), ('unknown', 4)]

        visitors = []
        for i in range(count):
            # Pick month based on growth weights
            month_idx = _weighted_choice(list(enumerate(monthly_weights)))
            month_offset = 11 - month_idx  # 0 = current month
            base_date = self.now - timedelta(days=month_offset * 30)
            timestamp = base_date - timedelta(
                days=random.randint(0, 29),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )

            country = _pick_country()
            device = _weighted_choice(device_types)
            referrer = _weighted_choice(REFERRER_URLS)

            # 30% chance of UTM tracking
            utm = random.choice(UTM_CAMPAIGNS) if random.random() < 0.3 else None

            session_key = f'showcase_{i}_{random.randint(1000, 9999)}'
            last_seen_ts = timestamp + timedelta(minutes=random.randint(1, 45))

            visitors.append(VisitorLocation(
                session_key=session_key,
                ip_address=f'{random.randint(10, 220)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}',
                resolved_country=country['code'],
                resolved_region='',
                resolved_city=random.choice(country['cities']),
                device_type=device,
                referrer_url=referrer,
                utm_source=utm['source'] if utm else '',
                utm_medium=utm['medium'] if utm else '',
                utm_campaign=utm['campaign'] if utm else '',
                utm_term=utm['term'] if utm else '',
                utm_content=utm['content'] if utm else '',
                user_agent=random.choice(USER_AGENTS.get(device, USER_AGENTS['desktop'])),
                page_views=random.choices(range(1, 21), weights=[15, 20, 18, 12, 8, 6, 5, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1], k=1)[0],
                first_seen=timestamp,
                last_seen=last_seen_ts,
            ))

        with disable_auto_now(VisitorLocation, ['first_seen', 'last_seen']):
            VisitorLocation.objects.bulk_create(visitors, batch_size=500)

        self.stdout.write(f'  Created {count} visitor records')

    # ── Phase 3: Orders ────────────────────────────────────────────────

    def _create_orders(self):
        from orders.models import Order, OrderItem

        # Monthly order targets with growth curve
        monthly_targets = [25, 27, 29, 35, 38, 42, 50, 55, 60, 65, 72, 80]
        total_orders = sum(monthly_targets)

        status_weights = [
            ('delivered', 55), ('shipped', 12), ('processing', 15),
            ('pending', 8), ('cancelled', 6), ('refunded', 4),
        ]
        source_weights = [
            ('direct', 35), ('organic', 25), ('email', 12), ('social', 10),
            ('utm_tracked', 8), ('referral', 5), ('loyalty', 3), ('unknown', 2),
        ]
        payment_weights = [
            ('credit_card', 55), ('paypal', 25), ('bank_transfer', 10), ('apple_pay', 10),
        ]

        self.showcase_orders = []
        order_seq = 0

        with disable_auto_now(Order, ['created_at']):
            for month_idx, target in enumerate(monthly_targets):
                month_offset = 11 - month_idx
                base_date = self.now - timedelta(days=month_offset * 30)

                for _ in range(target):
                    order_seq += 1
                    timestamp = base_date - timedelta(
                        days=random.randint(0, 29),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )

                    status = _weighted_choice(status_weights)
                    source = _weighted_choice(source_weights)
                    payment_method = _weighted_choice(payment_weights)
                    country = _pick_country()
                    user = random.choice(self.showcase_users)

                    # Build order items first so totals are derived from real prices
                    num_items = random.choices([1, 2, 3, 4], weights=[40, 35, 15, 10], k=1)[0]
                    selected_products = random.choices(self.products, weights=self.product_weights, k=num_items)
                    # Deduplicate
                    seen = set()
                    unique_products = []
                    for p in selected_products:
                        if p.pk not in seen:
                            seen.add(p.pk)
                            unique_products.append(p)

                    # Calculate item details and subtotal from actual prices
                    item_details = []
                    subtotal = Decimal('0.00')
                    for product in unique_products:
                        qty = random.choices([1, 2, 3], weights=[70, 20, 10], k=1)[0]
                        unit_price = product.price.amount if hasattr(product.price, 'amount') else Decimal(str(product.price or '29.99'))
                        item_total = (unit_price * qty).quantize(Decimal('0.01'))
                        subtotal += item_total
                        item_details.append((product, qty, unit_price, item_total))

                    # Derive tax, shipping, discount from real subtotal
                    tax_rate = Decimal(str(round(random.uniform(0.08, 0.12), 2)))
                    tax_amount = (subtotal * tax_rate).quantize(Decimal('0.01'))

                    # Shipping: free over $100
                    if subtotal >= 100:
                        shipping_cost = Decimal('0.00')
                    else:
                        shipping_cost = Decimal(str(random.choice([5.99, 9.99, 14.99])))

                    # 25% chance of discount
                    discount_amount = Decimal('0.00')
                    if random.random() < 0.25:
                        discount_pct = Decimal(str(round(random.uniform(0.05, 0.20), 2)))
                        discount_amount = (subtotal * discount_pct).quantize(Decimal('0.01'))

                    total_amount = (subtotal + tax_amount + shipping_cost - discount_amount).quantize(Decimal('0.01'))
                    if total_amount < 0:
                        total_amount = subtotal

                    order_number = f'{ORDER_PREFIX}{self.now.year}{order_seq:05d}'

                    # Payment status
                    if status in ('delivered', 'shipped', 'processing'):
                        payment_status = 'paid'
                    elif status == 'pending':
                        payment_status = random.choice(['unpaid', 'pending', 'paid'])
                    elif status == 'refunded':
                        payment_status = 'refunded'
                    else:
                        payment_status = 'paid'

                    paid_at = timestamp + timedelta(minutes=random.randint(1, 30)) if payment_status == 'paid' else None
                    delivered_at = None
                    if status == 'delivered':
                        delivered_at = timestamp + timedelta(days=random.randint(3, 10))

                    order = Order(
                        order_number=order_number,
                        user=user,
                        status=status,
                        source=source,
                        email=user.email,
                        phone=f'+1{random.randint(2000000000, 9999999999)}',
                        shipping_name=f'{user.first_name} {user.last_name}',
                        shipping_address1=f'{random.randint(100, 9999)} {random.choice(["Main", "Oak", "Elm", "Cedar", "Park", "Maple"])} {random.choice(["St", "Ave", "Blvd", "Dr", "Ln"])}',
                        shipping_address2=f'Apt {random.randint(1, 500)}' if random.random() < 0.3 else '',
                        shipping_city=random.choice(country['cities']),
                        shipping_state='',
                        shipping_postal_code=f'{random.randint(10000, 99999)}',
                        shipping_country=country['code'],
                        billing_same_as_shipping=True,
                        subtotal=subtotal,
                        subtotal_currency=self.currency,
                        tax_amount=tax_amount,
                        tax_amount_currency=self.currency,
                        shipping_cost=shipping_cost,
                        shipping_cost_currency=self.currency,
                        discount_amount=discount_amount,
                        discount_amount_currency=self.currency,
                        gift_card_discount=Decimal('0.00'),
                        gift_card_discount_currency=self.currency,
                        total_amount=total_amount,
                        total_amount_currency=self.currency,
                        payment_status=payment_status,
                        payment_method_type=payment_method,
                        payment_method_last4=f'{random.randint(1000, 9999)}',
                        paid_at=paid_at,
                        amount_paid=total_amount if payment_status == 'paid' else Decimal('0.00'),
                        amount_paid_currency=self.currency,
                        amount_refunded=total_amount if status == 'refunded' else Decimal('0.00'),
                        amount_refunded_currency=self.currency,
                        delivered_at=delivered_at,
                        base_currency=self.currency,
                        created_at=timestamp,
                    )
                    order.compute_base_amounts()
                    order.save()

                    # Create order items from pre-computed details
                    for product, qty, unit_price, item_total in item_details:
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            product_name=product.name,
                            variant_name='',
                            sku=product.sku,
                            quantity=qty,
                            unit_price=unit_price,
                            unit_price_currency=self.currency,
                            total_price=item_total,
                            total_price_currency=self.currency,
                            unit_price_base=unit_price,
                            total_price_base=item_total,
                        )

                    self.showcase_orders.append(order)

        self.stdout.write(f'  Created {len(self.showcase_orders)} orders')

    # ── Phase 4: Vouchers ──────────────────────────────────────────────

    def _create_vouchers(self):
        from vouchers.models import VoucherCode, VoucherUsage

        voucher_objects = []
        for vdef in VOUCHER_DEFINITIONS:
            start_date = self.year_ago
            end_date = self.now + timedelta(days=90) if vdef['active'] else self.now - timedelta(days=30)

            voucher, _ = VoucherCode.objects.get_or_create(
                code=vdef['code'],
                defaults={
                    'name': vdef['name'],
                    'discount_type': vdef['discount_type'],
                    'discount_value': Decimal(str(vdef['discount_value'])),
                    'max_uses_total': vdef['max_uses_total'],
                    'current_uses': vdef['target_uses'],
                    'start_date': start_date,
                    'end_date': end_date,
                    'first_time_customers_only': vdef['first_time'],
                    'application_scope': 'cart',
                }
            )
            voucher_objects.append((voucher, vdef['target_uses']))

        # Create VoucherUsage records
        usable_orders = [o for o in self.showcase_orders if o.status not in ('cancelled',)]
        usage_count = 0
        with disable_auto_now(VoucherUsage, ['used_at']):
            for voucher, target_uses in voucher_objects:
                for _ in range(min(target_uses, len(usable_orders))):
                    order = random.choice(usable_orders)
                    discount_amt = Decimal(str(round(random.uniform(5, 50), 2)))
                    VoucherUsage.objects.create(
                        voucher=voucher,
                        user=order.user,
                        order=order,
                        discount_amount=discount_amt,
                        discount_amount_currency=self.currency,
                        cart_total=order.total_amount,
                        cart_total_currency=self.currency,
                        used_at=order.created_at,
                    )
                    usage_count += 1

        self.stdout.write(f'  Created {len(voucher_objects)} vouchers, {usage_count} usage records')

    # ── Phase 5: Affiliates ────────────────────────────────────────────

    def _create_affiliates(self):
        from affiliate.models import Program, Affiliate, AffiliateProgramMembership, Link, Click, Commission, Payout

        # Get or create admin user for merchant field
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = self.showcase_users[0]

        # Create program
        program, _ = Program.objects.get_or_create(
            name='Spwig Partners',
            defaults={
                'slug': 'spwig-partners',
                'merchant': admin_user,
                'description': 'Earn 10% commission on every sale you refer.',
                'commission_type': 'percentage',
                'commission_value': Decimal('10.00'),
                'cookie_lifetime_days': 30,
                'status': 'active',
                'auto_approve_affiliates': True,
                'minimum_payout': Decimal('50.00'),
            }
        )

        # Create affiliate users and profiles
        affiliate_tiers = [
            (3, 'top', 40, 80),     # 3 top performers
            (5, 'mid', 10, 30),     # 5 mid performers
            (10, 'low', 1, 8),      # 10 low performers
        ]

        all_affiliates = []
        affiliate_idx = 0
        referral_orders = [o for o in self.showcase_orders if o.status in ('delivered', 'shipped', 'processing')]

        for tier_count, tier_name, min_comm, max_comm in affiliate_tiers:
            for _ in range(tier_count):
                first, last = AFFILIATE_NAMES[affiliate_idx]
                email = f'{AFFILIATE_EMAIL_PREFIX}{affiliate_idx}@{SHOWCASE_EMAIL_DOMAIN}'
                aff_user, _ = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'username': f'affiliate_showcase_{affiliate_idx}',
                        'first_name': first,
                        'last_name': last,
                        'is_active': True,
                    }
                )

                aff_code = f'AFF{affiliate_idx:03d}'
                affiliate, _ = Affiliate.objects.get_or_create(
                    user=aff_user,
                    defaults={
                        'affiliate_code': aff_code,
                        'status': 'active',
                        'payment_email': email,
                        'payment_method': 'paypal',
                    }
                )

                # Membership
                AffiliateProgramMembership.objects.get_or_create(
                    affiliate=affiliate,
                    program=program,
                    defaults={'status': 'approved'}
                )

                # Link
                link, _ = Link.objects.get_or_create(
                    affiliate=affiliate,
                    program=program,
                    defaults={
                        'link_code': secrets.token_urlsafe(8)[:12],
                        'destination_url': 'https://shop.example.com/',
                        'label': f'{first} {last} Main Link',
                        'is_active': True,
                    }
                )

                # Clicks
                click_count = random.randint(50 if tier_name == 'top' else 10 if tier_name == 'mid' else 1, 2000 if tier_name == 'top' else 200 if tier_name == 'mid' else 50)
                clicks = []
                for c in range(min(click_count, 100)):  # Cap bulk creates
                    timestamp = self.now - timedelta(days=random.randint(0, 365))
                    clicks.append(Click(
                        link=link,
                        ip_address=f'{random.randint(10, 220)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}',
                        user_agent=random.choice(USER_AGENTS['desktop']),
                        referrer='',
                        session_id=f'aff_sess_{affiliate_idx}_{c}',
                        cookie_value=secrets.token_urlsafe(16),
                        clicked_at=timestamp,
                    ))
                Click.objects.bulk_create(clicks, batch_size=200)

                # Commissions
                num_commissions = random.randint(min_comm, max_comm)
                commission_objects = []
                for _ in range(min(num_commissions, len(referral_orders))):
                    order = random.choice(referral_orders)
                    commission_amount = (order.total_amount.amount * Decimal('0.10')).quantize(Decimal('0.01')) if hasattr(order.total_amount, 'amount') else Decimal('10.00')
                    comm_status = _weighted_choice([('approved', 70), ('pending', 20), ('paid', 10)])
                    comm = Commission.objects.create(
                        affiliate=affiliate,
                        program=program,
                        order=order,
                        amount=commission_amount,
                        currency=self.currency,
                        amount_base=commission_amount,
                        base_currency=self.currency,
                        status=comm_status,
                        created_at=order.created_at + timedelta(hours=1),
                        approved_at=order.created_at + timedelta(days=3) if comm_status in ('approved', 'paid') else None,
                        paid_at=order.created_at + timedelta(days=30) if comm_status == 'paid' else None,
                    )
                    commission_objects.append(comm)

                # Payouts for paid commissions
                paid_comms = [c for c in commission_objects if c.status == 'paid']
                if paid_comms:
                    payout_amount = sum(c.amount for c in paid_comms)
                    payout = Payout.objects.create(
                        affiliate=affiliate,
                        amount=payout_amount,
                        method='paypal',
                        status='completed',
                        currency=self.currency,
                        amount_base=payout_amount,
                        base_currency=self.currency,
                        reference=f'PAY-{secrets.token_urlsafe(8)}',
                        completed_at=self.now - timedelta(days=random.randint(1, 60)),
                    )
                    payout.commissions.set(paid_comms)

                all_affiliates.append(affiliate)
                affiliate_idx += 1

        self.stdout.write(f'  Created {len(all_affiliates)} affiliates with commissions')

    # ── Phase 6: Loyalty Program ───────────────────────────────────────

    def _create_loyalty(self):
        from loyalty.models import (
            LoyaltyTier, LoyaltyRule, LoyaltyReward, LoyaltyMember,
            LoyaltyBalance, LoyaltyTransaction, LoyaltyRedemption
        )

        # Tiers — use existing if available, otherwise create
        tiers = {}
        tier_defs = [
            (0, 'Bronze', 'bronze', 0, '#CD7F32'),
            (1, 'Silver', 'silver', 500, '#C0C0C0'),
            (2, 'Gold', 'gold', 2000, '#FFD700'),
            (3, 'Platinum', 'platinum', 5000, '#E5E4E2'),
        ]
        for rank, name, slug, min_pts, color in tier_defs:
            # Try by slug first, then by rank, then create
            tier = LoyaltyTier.objects.filter(slug=slug).first()
            if not tier:
                tier = LoyaltyTier.objects.filter(rank=rank).first()
            if not tier:
                tier = LoyaltyTier.objects.create(
                    name=name, slug=slug, rank=rank,
                    min_points_earned=min_pts, color=color,
                    description=f'{name} tier membership',
                )
            tiers[name] = tier

        # Rules
        for name, rule_type, action, pts in [
            ('Showcase Purchase Points', 'spend_based', None, 1),
            ('Showcase Review Points', 'action_based', 'review', 50),
            ('Showcase Signup Points', 'action_based', 'signup', 100),
        ]:
            LoyaltyRule.objects.get_or_create(
                name=name,
                defaults={
                    'rule_type': rule_type,
                    'action_type': action or '',
                    'points_rate': Decimal(str(pts)),
                    'is_active': True,
                }
            )

        # Rewards
        rewards = {}
        for name, rtype, dtype, pts, val in [
            ('Showcase $5 Off', 'discount', 'fixed', 500, 5),
            ('Showcase $15 Off', 'discount', 'fixed', 1200, 15),
            ('Showcase Free Shipping', 'shipping', None, 300, 0),
        ]:
            from django.utils.text import slugify
            reward, _ = LoyaltyReward.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': name,
                    'reward_type': rtype,
                    'discount_type': dtype or '',
                    'points_cost': pts,
                    'discount_value': Decimal(str(val)) if val else None,
                    'is_active': True,
                }
            )
            rewards[name] = reward

        # Members: 30 Bronze, 20 Silver, 10 Gold, 5 Platinum
        tier_distribution = [
            ('Bronze', 30), ('Silver', 20), ('Gold', 10), ('Platinum', 5),
        ]

        member_idx = 0
        for tier_name, count in tier_distribution:
            tier = tiers[tier_name]
            for _ in range(count):
                if member_idx >= len(self.showcase_users):
                    break
                user = self.showcase_users[member_idx]
                member_idx += 1

                member, created = LoyaltyMember.objects.get_or_create(
                    customer=user,
                    defaults={
                        'current_tier': tier,
                        'is_active': True,
                        'enrolled_at': self.year_ago + timedelta(days=random.randint(0, 300)),
                    }
                )

                if not created:
                    continue

                # Points based on tier
                points_ranges = {
                    'Bronze': (50, 499),
                    'Silver': (500, 1999),
                    'Gold': (2000, 4999),
                    'Platinum': (5000, 12000),
                }
                min_pts, max_pts = points_ranges[tier_name]
                lifetime_earned = random.randint(min_pts, max_pts)
                redeemed = random.randint(0, int(lifetime_earned * 0.4))
                available = lifetime_earned - redeemed

                LoyaltyBalance.objects.get_or_create(
                    member=member,
                    defaults={
                        'available_points': available,
                        'pending_points': random.randint(0, 50),
                        'lifetime_earned': lifetime_earned,
                        'lifetime_redeemed': redeemed,
                        'lifetime_expired': 0,
                    }
                )

                # Earn transactions
                earn_count = random.randint(3, 15)
                with disable_auto_now(LoyaltyTransaction, ['created_at']):
                    for t in range(earn_count):
                        pts = random.randint(10, 200)
                        LoyaltyTransaction.objects.create(
                            member=member,
                            transaction_type='earn',
                            points=pts,
                            description='Purchase reward',
                            status='available',
                            created_at=member.enrolled_at + timedelta(days=random.randint(0, 300)),
                        )

        # Redemptions
        members = LoyaltyMember.objects.filter(customer__in=self.showcase_users)
        reward_list = list(rewards.values())
        for _ in range(25):
            member = random.choice(list(members))
            reward = random.choice(reward_list)
            LoyaltyRedemption.objects.create(
                member=member,
                reward=reward,
                redemption_code=f'LOYALTY-SC-{secrets.token_hex(5).upper()}',
                points_spent=reward.points_cost,
                status='fulfilled',
                fulfilled_at=self.now - timedelta(days=random.randint(1, 300)),
            )

        self.stdout.write(f'  Created loyalty program with {member_idx} members')

    # ── Phase 7: Referral Program ──────────────────────────────────────

    def _create_referrals(self):
        from referrals.models import (
            ReferralProgram, ReferralIdentity, ReferralAttribution,
            ReferralReward, ReferralEvent
        )

        # Program (singleton)
        program, _ = ReferralProgram.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'Showcase Referral Program',
                'status': 'active',
                'reward_config': {
                    'double_sided': True,
                    'referrer': {'kind': 'credit', 'amount': 10},
                    'referee': {'kind': 'discount', 'percentage': 10},
                },
                'eligibility_rules': {
                    'min_order_value': 25,
                    'new_customer_only': True,
                },
                'timing_config': {
                    'issue_on': 'order_delivered',
                    'refund_window_days': 14,
                },
            }
        )

        # Identities (20 referrers from customer pool)
        referrers = self.showcase_users[:20]
        identities = []
        for user in referrers:
            identity, _ = ReferralIdentity.objects.get_or_create(
                customer=user,
                defaults={
                    'token': secrets.token_urlsafe(16)[:20],
                }
            )
            identities.append(identity)

        # Attributions (35 total)
        referees = self.showcase_users[20:55]
        attribution_count = 0
        orders_for_referral = [o for o in self.showcase_orders if o.status == 'delivered']

        with disable_auto_now(ReferralAttribution, ['created_at']), \
             disable_auto_now(ReferralReward, ['created_at']):
            for i in range(min(35, len(referees), len(orders_for_referral))):
                referrer_id = random.choice(identities)
                referee = referees[i] if i < len(referees) else random.choice(self.showcase_users[20:])
                order = orders_for_referral[i] if i < len(orders_for_referral) else None
                status = _weighted_choice([('approved', 75), ('pending', 15), ('rejected', 10)])

                try:
                    ReferralAttribution.objects.create(
                        program=program,
                        referrer_identity=referrer_id,
                        referee_customer=referee,
                        first_order=order,
                        status=status,
                        created_at=self.now - timedelta(days=random.randint(1, 300)),
                    )
                    attribution_count += 1
                except Exception:
                    # first_order is OneToOne, skip duplicates
                    continue

                # Rewards for approved attributions
                if status == 'approved' and order:
                    reward_created_at = self.now - timedelta(days=random.randint(1, 200))
                    ReferralReward.objects.create(
                        program=program,
                        attribution=ReferralAttribution.objects.filter(
                            referee_customer=referee, program=program
                        ).first(),
                        referrer_identity=referrer_id,
                        customer=referrer_id.customer,
                        recipient_type='referrer',
                        kind='credit',
                        amount=Decimal('10.00'),
                        amount_currency=self.currency,
                        status='issued',
                        issued_at=reward_created_at,
                        created_at=reward_created_at,
                    )

        # Events
        event_specs = [
            ('click', 200), ('signup', 50), ('order', 35), ('approved', 26),
        ]
        with disable_auto_now(ReferralEvent, ['created_at']):
            for event_type, count in event_specs:
                for _ in range(count):
                    identity = random.choice(identities)
                    ReferralEvent.objects.create(
                        program=program,
                        referrer_identity=identity,
                        event_type=event_type,
                        ip_address=f'{random.randint(10, 220)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}',
                        created_at=self.now - timedelta(days=random.randint(0, 365)),
                    )

        # Update denormalized stats
        for identity in identities:
            events = ReferralEvent.objects.filter(referrer_identity=identity)
            identity.total_clicks = events.filter(event_type='click').count()
            identity.total_signups = events.filter(event_type='signup').count()
            identity.total_conversions = events.filter(event_type='approved').count()
            identity.total_rewards_earned = Decimal('10.00') * identity.total_conversions
            identity.save()

        self.stdout.write(f'  Created referral program with {attribution_count} attributions')

    # ── Phase 8: Shipments ─────────────────────────────────────────────

    def _create_shipments(self):
        from shipping.models import Shipment, TrackingEvent, CarrierPreset

        shipped_orders = [o for o in self.showcase_orders if o.status in ('shipped', 'delivered')]
        carrier = CarrierPreset.objects.filter(is_active=True).first()

        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = self.showcase_users[0]

        shipment_status_weights = [
            ('delivered', 65), ('in_transit', 15), ('out_for_delivery', 5),
            ('labeled', 10), ('exception', 3), ('returned', 2),
        ]

        tracking_prefixes = ['1Z999AA1', 'TRK', 'SHIP', '9400111899']

        shipment_count = 0
        with disable_auto_now(Shipment, ['created_at']):
            for order in shipped_orders:
                ship_status = _weighted_choice(shipment_status_weights)
                prefix = random.choice(tracking_prefixes)
                tracking_id = f'{prefix}{random.randint(10000000, 99999999)}'

                ship_created = order.created_at + timedelta(hours=random.randint(2, 48))
                shipment = Shipment.objects.create(
                    order=order,
                    user=admin_user,
                    carrier_preset=carrier,
                    origin_country='US',
                    dest_country=order.shipping_country or 'US',
                    packages=[{'weight_g': random.randint(200, 5000), 'length_cm': 30, 'width_cm': 20, 'height_cm': 15}],
                    service_level=random.choice(['standard', 'express', 'economy']),
                    shipping_cost=order.shipping_cost,
                    shipping_cost_currency=self.currency,
                    tracking_id=tracking_id,
                    status=ship_status,
                    created_at=ship_created,
                )

                # Tracking events (use the explicit timestamp, not shipment.created_at
                # which may still reflect DB default if refresh isn't done)
                base_time = ship_created
                TrackingEvent.objects.create(
                    shipment=shipment,
                    status='info_received',
                    description='Shipment information received',
                    location='Distribution Center',
                    occurred_at=base_time,
                )
                if ship_status in ('in_transit', 'out_for_delivery', 'delivered'):
                    TrackingEvent.objects.create(
                        shipment=shipment,
                        status='in_transit',
                        description='Package in transit',
                        location='Sorting Facility',
                        occurred_at=base_time + timedelta(days=1),
                    )
                if ship_status in ('out_for_delivery', 'delivered'):
                    TrackingEvent.objects.create(
                        shipment=shipment,
                        status='out_for_delivery',
                        description='Out for delivery',
                        location=order.shipping_city or 'Local Facility',
                        occurred_at=base_time + timedelta(days=2),
                    )
                if ship_status == 'delivered':
                    TrackingEvent.objects.create(
                        shipment=shipment,
                        status='delivered',
                        description='Package delivered',
                        location=order.shipping_city or 'Delivered',
                        occurred_at=base_time + timedelta(days=random.randint(3, 7)),
                    )

                shipment_count += 1

        self.stdout.write(f'  Created {shipment_count} shipments with tracking events')

    # ── Phase 9: Email Campaigns ───────────────────────────────────────

    def _create_email_campaigns(self):
        from email_system.models import EmailOutbox, EmailEvent
        from django.contrib.sites.models import Site

        site = Site.objects.get(pk=1)

        # 12 monthly campaigns
        campaign_emails = []
        for month_idx in range(12):
            month_offset = 11 - month_idx
            sent_at = self.now - timedelta(days=month_offset * 30 + 15)  # Mid-month

            campaign_names = [
                'New Collection Launch', 'Flash Sale Weekend', 'Spring Lookbook',
                'Summer Essentials', 'Back to School', 'Mid-Season Sale',
                'Autumn Preview', 'Black Friday Deals', 'Holiday Gift Guide',
                'New Year New You', 'Valentine\'s Special', 'Spring Forward'
            ]

            email = EmailOutbox.objects.create(
                site=site,
                to_email=f'{SHOWCASE_EMAIL_PREFIX}campaign_{month_idx}@{SHOWCASE_EMAIL_DOMAIN}',
                from_email='hello@shop.example.com',
                subject=campaign_names[month_idx % len(campaign_names)],
                html_body=f'<p>Campaign content for month {month_idx + 1}</p>',
                text_body=f'Campaign content for month {month_idx + 1}',
                template_type='admin_report_abandoned_carts_summary',
                status='sent',
                sent_at=sent_at,
                tags=['showcase_campaign'],
            )
            campaign_emails.append(email)

            # Email events: delivered ~90%, opened ~25%, clicked ~3%
            recipient_count = random.randint(800, 2000)
            delivered_count = int(recipient_count * 0.90)
            opened_count = int(recipient_count * random.uniform(0.20, 0.30))
            clicked_count = int(recipient_count * random.uniform(0.02, 0.05))

            events = []
            for _ in range(min(delivered_count, 50)):  # Cap for performance
                events.append(EmailEvent(
                    email=email,
                    event_type='delivered',
                    occurred_at=sent_at + timedelta(minutes=random.randint(1, 60)),
                ))
            for _ in range(min(opened_count, 30)):
                events.append(EmailEvent(
                    email=email,
                    event_type='opened',
                    occurred_at=sent_at + timedelta(hours=random.randint(1, 72)),
                ))
            for _ in range(min(clicked_count, 10)):
                events.append(EmailEvent(
                    email=email,
                    event_type='clicked',
                    occurred_at=sent_at + timedelta(hours=random.randint(1, 48)),
                ))
            EmailEvent.objects.bulk_create(events, batch_size=200)

        # Attribute ~15% of orders to email campaigns
        attributable_orders = [o for o in self.showcase_orders if o.source in ('email', 'direct')]
        sample_size = int(len(attributable_orders) * 0.15)
        for order in random.sample(attributable_orders, min(sample_size, len(attributable_orders))):
            # Find campaign sent within 7 days before order
            for email in campaign_emails:
                if email.sent_at and order.created_at:
                    delta = order.created_at - email.sent_at
                    if timedelta(0) <= delta <= timedelta(days=7):
                        order.attributed_email = email
                        order.save(update_fields=['attributed_email'])
                        break

        self.stdout.write(f'  Created {len(campaign_emails)} email campaigns with events')

    # ── Phase 10: Product Reviews ──────────────────────────────────────

    def _create_reviews(self):
        from catalog.models import ProductReview

        reviews = []
        # Pre-load existing (product, user) pairs to avoid unique constraint violations
        seen_pairs = set(
            ProductReview.objects.filter(user__in=self.showcase_users)
            .values_list('product_id', 'user_id')
        )
        # Weight distribution for star ratings
        rating_weights = [5, 10, 15, 30, 40]  # 1★ to 5★

        for i in range(180):
            product = random.choices(self.products, weights=self.product_weights, k=1)[0]
            user = random.choice(self.showcase_users)

            # Skip duplicate (product, user) pairs
            pair_key = (product.pk, user.pk)
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)

            rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights, k=1)[0]

            # Pick matching review template
            matching = [t for t in REVIEW_TEMPLATES if t[0] == rating]
            if matching:
                _, title, comment = random.choice(matching)
            else:
                title, comment = 'Good product', 'Satisfied with the purchase.'

            # Approval: 70% approved, 20% pending, 10% not approved
            approval_roll = random.random()
            is_approved = approval_roll < 0.70

            reviews.append(ProductReview(
                product=product,
                user=user,
                rating=rating,
                title=title,
                comment=comment,
                is_verified_purchase=random.random() < 0.60,
                is_approved=is_approved,
                helpful_count=random.randint(0, 25) if is_approved else 0,
                created_at=self.now - timedelta(days=random.randint(1, 365)),
            ))

        with disable_auto_now(ProductReview, ['created_at']):
            ProductReview.objects.bulk_create(reviews, batch_size=100)
        self.stdout.write(f'  Created {len(reviews)} product reviews')

    # ── Phase 11: Abandoned Carts ──────────────────────────────────────

    def _create_abandoned_carts(self):
        from cart.models import Cart, CartItem
        from customers.models import AbandonedCart

        count = 150
        recovered_count = 30

        with disable_auto_now(Cart, ['created_at', 'updated_at']), \
             disable_auto_now(AbandonedCart, ['abandoned_at']):
            for i in range(count):
                user = random.choice(self.showcase_users)
                timestamp = self.now - timedelta(days=random.randint(1, 90))

                # Create cart
                cart = Cart.objects.create(
                    user=user,
                    session_key=f'showcase_cart_{i}',
                    currency=self.currency,
                    created_at=timestamp,
                    updated_at=timestamp,
                )

                # Add 1-3 items
                num_items = random.randint(1, 3)
                total_value = Decimal('0.00')
                for _ in range(num_items):
                    product = random.choice(self.products)
                    qty = random.randint(1, 2)
                    price = product.price.amount if hasattr(product.price, 'amount') else Decimal('29.99')
                    CartItem.objects.create(
                        cart=cart,
                        product=product,
                        quantity=qty,
                        unit_price=price,
                        unit_price_currency=self.currency,
                    )
                    total_value += price * qty

                is_recovered = i < recovered_count
                reason = _weighted_choice(ABANDONMENT_REASONS_WEIGHTED)

                AbandonedCart.objects.create(
                    user=user,
                    cart=cart,
                    total_items=num_items,
                    total_value=total_value,
                    total_value_currency=self.currency,
                    recovered=is_recovered,
                    recovered_at=timestamp + timedelta(days=1) if is_recovered else None,
                    estimated_reason=reason,
                    recovery_emails_sent=random.randint(1, 3) if not is_recovered else 0,
                    abandoned_at=timestamp,
                )

        self.stdout.write(f'  Created {count} abandoned carts ({recovered_count} recovered)')

    # ── Phase 12: Customer Metrics ─────────────────────────────────────

    def _compute_customer_metrics(self):
        from customers.models import CustomerMetrics
        from orders.models import Order
        from django.db.models import Sum, Avg, Count, Min, Max

        computed = 0
        for user in self.showcase_users:
            user_orders = Order.objects.filter(
                user=user,
                order_number__startswith=ORDER_PREFIX,
                status__in=('delivered', 'shipped', 'processing'),
            )

            stats = user_orders.aggregate(
                total_spent=Sum('total_amount_base'),
                avg_order=Avg('total_amount_base'),
                count=Count('id'),
                first_purchase=Min('created_at'),
                last_purchase=Max('created_at'),
            )

            if stats['count'] and stats['count'] > 0:
                metrics, _ = CustomerMetrics.objects.get_or_create(
                    user=user,
                    defaults={
                        'total_spent': stats['total_spent'] or 0,
                        'total_spent_currency': self.currency,
                        'lifetime_value': stats['total_spent'] or 0,
                        'lifetime_value_currency': self.currency,
                        'total_orders': stats['count'],
                        'completed_orders': user_orders.filter(status='delivered').count(),
                        'average_order_value': stats['avg_order'] or 0,
                        'average_order_value_currency': self.currency,
                        'first_purchase_date': stats['first_purchase'],
                        'last_purchase_date': stats['last_purchase'],
                    }
                )
                computed += 1

        self.stdout.write(f'  Computed metrics for {computed} customers')

    # ── Phase 13: Stock Adjustments ────────────────────────────────────

    def _adjust_stock(self):
        from catalog.models import StockItem

        # Find products with inventory tracking
        tracked = [p for p in self.products if p.track_inventory]
        if not tracked:
            self.stdout.write('  No tracked-inventory products found, skipping')
            return

        adjusted = 0
        # Set 3 products to low stock
        for product in tracked[:3]:
            stock = StockItem.objects.filter(product=product).first()
            if stock:
                stock.on_hand = random.randint(3, 8)
                stock.save(update_fields=['on_hand'])
                adjusted += 1

        # Set 1 product out of stock
        if len(tracked) > 3:
            stock = StockItem.objects.filter(product=tracked[3]).first()
            if stock:
                stock.on_hand = 0
                stock.save(update_fields=['on_hand'])
                adjusted += 1

        self.stdout.write(f'  Adjusted stock for {adjusted} products')

    # ── Phase 14: Customer Messages ───────────────────────────────────

    def _create_customer_messages(self):
        from admin_api.models import CustomerMessage

        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = self.showcase_users[0]

        # Spread 40 messages across 6 months with increasing volume
        monthly_targets = [3, 4, 5, 7, 9, 12]
        messages_created = 0
        template_idx = 0

        with disable_auto_now(CustomerMessage, ['created_at', 'updated_at']):
            for month_idx, target in enumerate(monthly_targets):
                month_offset = 5 - month_idx
                base_date = self.now - timedelta(days=month_offset * 30)

                for _ in range(target):
                    template = CUSTOMER_MESSAGE_TEMPLATES[template_idx % len(CUSTOMER_MESSAGE_TEMPLATES)]
                    template_idx += 1
                    msg_type, subject, body, reply = template

                    user = random.choice(self.showcase_users)
                    timestamp = base_date - timedelta(
                        days=random.randint(0, 29),
                        hours=random.randint(8, 22),
                        minutes=random.randint(0, 59),
                    )

                    # Substitute order number if applicable
                    order_ref = None
                    if msg_type == 'order' and hasattr(self, 'showcase_orders') and self.showcase_orders:
                        order_ref = random.choice(self.showcase_orders)
                        body = body.format(order_number=order_ref.order_number)
                    else:
                        body = body.replace('{order_number}', 'my recent order')

                    # Determine status
                    if reply:
                        # 70% replied, 20% read, 10% archived
                        status_roll = random.random()
                        if status_roll < 0.70:
                            status = 'replied'
                        elif status_roll < 0.90:
                            status = 'read'
                        else:
                            status = 'archived'
                    else:
                        # No reply template: 40% unread, 40% read, 20% archived
                        status_roll = random.random()
                        if status_roll < 0.40:
                            status = 'unread'
                        elif status_roll < 0.80:
                            status = 'read'
                        else:
                            status = 'archived'

                    read_at = None
                    read_by = None
                    reply_text = ''
                    replied_at = None
                    replied_by = None

                    if status in ('read', 'replied', 'archived'):
                        read_at = timestamp + timedelta(hours=random.randint(1, 8))
                        read_by = admin_user

                    if status == 'replied' and reply:
                        reply_text = reply
                        replied_at = read_at + timedelta(hours=random.randint(1, 24))
                        replied_by = admin_user

                    CustomerMessage.objects.create(
                        name=f'{user.first_name} {user.last_name}',
                        email=user.email,
                        phone=f'+1{random.randint(2000000000, 9999999999)}' if random.random() < 0.3 else '',
                        user=user,
                        subject=subject,
                        message=body,
                        message_type=msg_type,
                        order=order_ref if msg_type == 'order' else None,
                        status=status,
                        read_at=read_at,
                        read_by=read_by,
                        reply_text=reply_text,
                        replied_at=replied_at,
                        replied_by=replied_by,
                        created_at=timestamp,
                        updated_at=replied_at or read_at or timestamp,
                    )
                    messages_created += 1

        # Count statuses for summary
        replied = CustomerMessage.objects.filter(user__in=self.showcase_users, status='replied').count()
        unread = CustomerMessage.objects.filter(user__in=self.showcase_users, status='unread').count()
        self.stdout.write(f'  Created {messages_created} customer messages ({replied} replied, {unread} unread)')
