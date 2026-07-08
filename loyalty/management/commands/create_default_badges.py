"""
Management command to create default loyalty badges.

Usage:
    python manage.py create_default_badges
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from loyalty.models import LoyaltyBadge


class Command(BaseCommand):
    help = 'Creates a set of default loyalty badges for the program'

    def handle(self, *args, **options):
        """Create default badges"""

        badges_data = [
            # First-Time Achievements
            {
                'name': 'Welcome Aboard',
                'description': 'Joined the loyalty program',
                'icon': 'fa-handshake',
                'criteria_type': 'program_join',
                'criteria_value': 1,
                'points_reward': 50,
                'display_order': 10,
            },
            {
                'name': 'First Purchase',
                'description': 'Made your first purchase',
                'icon': 'fa-shopping-bag',
                'criteria_type': 'order_count',
                'criteria_value': 1,
                'points_reward': 100,
                'display_order': 20,
            },
            {
                'name': 'Review Master',
                'description': 'Left your first product review',
                'icon': 'fa-star',
                'criteria_type': 'review_count',
                'criteria_value': 1,
                'points_reward': 75,
                'display_order': 30,
            },
            {
                'name': 'Social Butterfly',
                'description': 'Shared 5 products on social media',
                'icon': 'fa-share-nodes',
                'criteria_type': 'social_share',
                'criteria_value': 5,
                'points_reward': 100,
                'display_order': 40,
            },

            # Spending Milestones
            {
                'name': 'Bronze Spender',
                'description': 'Spent $100 in total',
                'icon': 'fa-medal',
                'criteria_type': 'total_spend',
                'criteria_value': 100,
                'points_reward': 150,
                'display_order': 100,
            },
            {
                'name': 'Silver Spender',
                'description': 'Spent $500 in total',
                'icon': 'fa-medal',
                'criteria_type': 'total_spend',
                'criteria_value': 500,
                'points_reward': 300,
                'display_order': 110,
            },
            {
                'name': 'Gold Spender',
                'description': 'Spent $1,000 in total',
                'icon': 'fa-medal',
                'criteria_type': 'total_spend',
                'criteria_value': 1000,
                'points_reward': 500,
                'display_order': 120,
            },
            {
                'name': 'Platinum Spender',
                'description': 'Spent $5,000 in total',
                'icon': 'fa-trophy',
                'criteria_type': 'total_spend',
                'criteria_value': 5000,
                'points_reward': 1000,
                'display_order': 130,
            },
            {
                'name': 'Diamond Elite',
                'description': 'Spent $10,000 in total',
                'icon': 'fa-gem',
                'criteria_type': 'total_spend',
                'criteria_value': 10000,
                'points_reward': 2500,
                'display_order': 140,
            },

            # Order Count Milestones
            {
                'name': 'Regular Customer',
                'description': 'Completed 5 orders',
                'icon': 'fa-cart-shopping',
                'criteria_type': 'order_count',
                'criteria_value': 5,
                'points_reward': 200,
                'display_order': 200,
            },
            {
                'name': 'Frequent Buyer',
                'description': 'Completed 10 orders',
                'icon': 'fa-cart-shopping',
                'criteria_type': 'order_count',
                'criteria_value': 10,
                'points_reward': 350,
                'display_order': 210,
            },
            {
                'name': 'Shopping Expert',
                'description': 'Completed 25 orders',
                'icon': 'fa-bags-shopping',
                'criteria_type': 'order_count',
                'criteria_value': 25,
                'points_reward': 600,
                'display_order': 220,
            },
            {
                'name': 'VIP Shopper',
                'description': 'Completed 50 orders',
                'icon': 'fa-crown',
                'criteria_type': 'order_count',
                'criteria_value': 50,
                'points_reward': 1000,
                'display_order': 230,
            },
            {
                'name': 'Century Club',
                'description': 'Completed 100 orders',
                'icon': 'fa-trophy',
                'criteria_type': 'order_count',
                'criteria_value': 100,
                'points_reward': 2000,
                'display_order': 240,
            },

            # Review & Engagement
            {
                'name': 'Helpful Reviewer',
                'description': 'Left 5 product reviews',
                'icon': 'fa-star-half-stroke',
                'criteria_type': 'review_count',
                'criteria_value': 5,
                'points_reward': 250,
                'display_order': 300,
            },
            {
                'name': 'Review Enthusiast',
                'description': 'Left 10 product reviews',
                'icon': 'fa-stars',
                'criteria_type': 'review_count',
                'criteria_value': 10,
                'points_reward': 500,
                'display_order': 310,
            },
            {
                'name': 'Super Reviewer',
                'description': 'Left 25 product reviews',
                'icon': 'fa-award',
                'criteria_type': 'review_count',
                'criteria_value': 25,
                'points_reward': 1000,
                'display_order': 320,
            },

            # Social Engagement
            {
                'name': 'Social Advocate',
                'description': 'Shared 20 products on social media',
                'icon': 'fa-bullhorn',
                'criteria_type': 'social_share',
                'criteria_value': 20,
                'points_reward': 400,
                'display_order': 400,
            },
            {
                'name': 'Brand Ambassador',
                'description': 'Shared 50 products on social media',
                'icon': 'fa-megaphone',
                'criteria_type': 'social_share',
                'criteria_value': 50,
                'points_reward': 1000,
                'display_order': 410,
            },

            # Loyalty Streak
            {
                'name': 'Monthly Regular',
                'description': 'Made purchases 3 months in a row',
                'icon': 'fa-calendar-check',
                'criteria_type': 'monthly_streak',
                'criteria_value': 3,
                'points_reward': 300,
                'display_order': 500,
            },
            {
                'name': 'Quarterly Loyal',
                'description': 'Made purchases 6 months in a row',
                'icon': 'fa-calendar-days',
                'criteria_type': 'monthly_streak',
                'criteria_value': 6,
                'points_reward': 600,
                'display_order': 510,
            },
            {
                'name': 'Yearly Champion',
                'description': 'Made purchases 12 months in a row',
                'icon': 'fa-calendar-star',
                'criteria_type': 'monthly_streak',
                'criteria_value': 12,
                'points_reward': 1500,
                'display_order': 520,
            },

            # Special Achievements
            {
                'name': 'Early Bird',
                'description': 'Placed 3 orders before 9 AM',
                'icon': 'fa-sun',
                'criteria_type': 'early_morning_orders',
                'criteria_value': 3,
                'points_reward': 150,
                'display_order': 600,
                'is_visible': False,  # Hidden achievement
            },
            {
                'name': 'Night Owl',
                'description': 'Placed 3 orders after 9 PM',
                'icon': 'fa-moon',
                'criteria_type': 'late_night_orders',
                'criteria_value': 3,
                'points_reward': 150,
                'display_order': 610,
                'is_visible': False,  # Hidden achievement
            },
            {
                'name': 'Weekend Warrior',
                'description': 'Placed 5 orders on weekends',
                'icon': 'fa-sun-bright',
                'criteria_type': 'weekend_orders',
                'criteria_value': 5,
                'points_reward': 200,
                'display_order': 620,
                'is_visible': False,  # Hidden achievement
            },
            {
                'name': 'Birthday Shopper',
                'description': 'Made a purchase during your birthday month',
                'icon': 'fa-cake-candles',
                'criteria_type': 'birthday_purchase',
                'criteria_value': 1,
                'points_reward': 250,
                'display_order': 630,
            },
            {
                'name': 'Quick Returner',
                'description': 'Made a second purchase within 24 hours',
                'icon': 'fa-bolt',
                'criteria_type': 'quick_return',
                'criteria_value': 1,
                'points_reward': 150,
                'display_order': 640,
                'is_visible': False,  # Hidden achievement
            },
            {
                'name': 'Wishlist Master',
                'description': 'Added 20 items to your wishlist',
                'icon': 'fa-heart',
                'criteria_type': 'wishlist_items',
                'criteria_value': 20,
                'points_reward': 100,
                'display_order': 650,
            },
            {
                'name': 'Referral Champion',
                'description': 'Referred 5 friends who made purchases',
                'icon': 'fa-user-group',
                'criteria_type': 'referrals',
                'criteria_value': 5,
                'points_reward': 500,
                'display_order': 700,
            },
            {
                'name': 'Big Ticket Buyer',
                'description': 'Made a single order over $500',
                'icon': 'fa-sack-dollar',
                'criteria_type': 'single_order_value',
                'criteria_value': 500,
                'points_reward': 300,
                'display_order': 710,
            },
            {
                'name': 'Bulk Buyer',
                'description': 'Ordered 10+ items in a single order',
                'icon': 'fa-boxes-stacked',
                'criteria_type': 'items_per_order',
                'criteria_value': 10,
                'points_reward': 200,
                'display_order': 720,
            },
        ]

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for badge_data in badges_data:
            # Auto-generate slug from name
            slug = slugify(badge_data['name'])
            badge_data['slug'] = slug

            # Set auto_award to True for all default badges
            badge_data.setdefault('auto_award', True)

            # Check if badge already exists
            try:
                badge = LoyaltyBadge.objects.get(slug=slug)
                # Update existing badge
                for key, value in badge_data.items():
                    setattr(badge, key, value)
                badge.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'  Updated: {badge.name}')
                )
            except LoyaltyBadge.DoesNotExist:
                # Create new badge
                badge = LoyaltyBadge.objects.create(**badge_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  Created: {badge.name}')
                )

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} new badges'))
        if updated_count > 0:
            self.stdout.write(self.style.WARNING(f'↻ Updated {updated_count} existing badges'))
        self.stdout.write(self.style.SUCCESS(f'Total badges: {LoyaltyBadge.objects.count()}'))
        self.stdout.write('='*50)
