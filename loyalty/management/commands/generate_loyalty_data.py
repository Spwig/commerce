"""
Management command to generate test loyalty program data based on existing orders and users
"""
import random
from decimal import Decimal
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction

from loyalty.models import (
    LoyaltyMember,
    LoyaltyBalance,
    LoyaltyTransaction,
    LoyaltyCampaign,
    LoyaltyCampaignExecution,
    LoyaltyTier,
    LoyaltySegment,
    LoyaltyReward,
    LoyaltyRule,
    LoyaltyRedemption,
)
from orders.models import Order

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate test loyalty program data from existing orders and users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--members',
            type=int,
            default=None,
            help='Number of loyalty members to create (default: all users)'
        )
        parser.add_argument(
            '--campaigns',
            type=int,
            default=5,
            help='Number of campaigns to create (default: 5)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing loyalty data before generating'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing loyalty data...'))
            self.clear_data()

        self.stdout.write(self.style.SUCCESS('Starting loyalty data generation...'))

        # Create tiers first
        tiers = self.create_tiers()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(tiers)} loyalty tiers'))

        # Create segments
        segments = self.create_segments()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(segments)} customer segments'))

        # Create rules
        rules = self.create_rules()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(rules)} earning rules'))

        # Create rewards
        rewards = self.create_rewards()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(rewards)} rewards'))

        # Create members from users
        members = self.create_members(options['members'], tiers)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(members)} loyalty members'))

        # Generate transactions based on orders
        transaction_count = self.generate_transactions_from_orders(members, rules)
        self.stdout.write(self.style.SUCCESS(f'✓ Generated {transaction_count} transactions from orders'))

        # Generate additional activity
        bonus_count = self.generate_bonus_activity(members)
        self.stdout.write(self.style.SUCCESS(f'✓ Generated {bonus_count} bonus transactions'))

        # Create campaigns (skip segment assignment for now)
        campaigns = self.create_campaigns(options['campaigns'], segments)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {options["campaigns"]} campaigns'))

        # Generate campaign executions
        execution_count = self.generate_campaign_executions(campaigns, members)
        self.stdout.write(self.style.SUCCESS(f'✓ Generated {execution_count} campaign executions'))

        # Generate redemptions
        redemption_count = self.generate_redemptions(members, rewards)
        self.stdout.write(self.style.SUCCESS(f'✓ Generated {redemption_count} redemptions'))

        # Print summary
        self.print_summary()

    def clear_data(self):
        """Clear existing loyalty data"""
        LoyaltyCampaignExecution.objects.all().delete()
        LoyaltyCampaign.objects.all().delete()
        LoyaltyRedemption.objects.all().delete()
        LoyaltyTransaction.objects.all().delete()
        LoyaltyBalance.objects.all().delete()
        LoyaltyMember.objects.all().delete()
        LoyaltyReward.objects.all().delete()
        LoyaltyRule.objects.all().delete()
        LoyaltySegment.objects.all().delete()
        LoyaltyTier.objects.all().delete()

    def create_tiers(self):
        """Create loyalty tiers"""
        from django.utils.text import slugify

        tiers_data = [
            {
                'name': 'Bronze',
                'slug': 'bronze',
                'rank': 1,
                'min_points_earned': 0,
                'points_multiplier': Decimal('1.0'),
                'color': '#CD7F32',
                'description': 'Entry level tier for all new members'
            },
            {
                'name': 'Silver',
                'slug': 'silver',
                'rank': 2,
                'min_points_earned': 500,
                'points_multiplier': Decimal('1.25'),
                'color': '#C0C0C0',
                'description': '25% points bonus and exclusive perks'
            },
            {
                'name': 'Gold',
                'slug': 'gold',
                'rank': 3,
                'min_points_earned': 1500,
                'points_multiplier': Decimal('1.5'),
                'color': '#FFD700',
                'description': '50% points bonus and priority support'
            },
            {
                'name': 'Platinum',
                'slug': 'platinum',
                'rank': 4,
                'min_points_earned': 3000,
                'points_multiplier': Decimal('2.0'),
                'color': '#E5E4E2',
                'description': 'Double points, free shipping, and VIP benefits',
                'has_free_shipping': True,
                'has_early_access': True
            },
        ]

        tiers = []
        for tier_data in tiers_data:
            tier, _ = LoyaltyTier.objects.get_or_create(
                slug=tier_data['slug'],
                defaults=tier_data
            )
            tiers.append(tier)

        return tiers

    def create_segments(self):
        """Create customer segments"""
        segments_data = [
            {
                'name': 'High Value',
                'slug': 'high-value',
                'description': 'Customers with lifetime value > $500',
                'is_active': True
            },
            {
                'name': 'Active Shoppers',
                'slug': 'active-shoppers',
                'description': 'Customers who purchased in last 30 days',
                'is_active': True
            },
            {
                'name': 'At Risk',
                'slug': 'at-risk',
                'description': 'Previously active customers who haven\'t purchased in 60+ days',
                'is_active': True
            },
        ]

        segments = []
        for segment_data in segments_data:
            segment, _ = LoyaltySegment.objects.get_or_create(
                slug=segment_data['slug'],
                defaults=segment_data
            )
            segments.append(segment)

        return segments

    def create_rules(self):
        """Create earning rules"""
        rules_data = [
            {
                'name': 'Purchase Points',
                'description': 'Earn 1 point per $1 spent',
                'rule_type': LoyaltyRule.TYPE_SPEND_BASED,
                'points_rate': Decimal('1.00'),  # 1 point per $1
                'min_order_amount': Decimal('0.00'),
                'is_active': True,
                'priority': 1
            },
            {
                'name': 'Account Creation Bonus',
                'description': 'Welcome bonus for new members',
                'rule_type': LoyaltyRule.TYPE_ACTION_BASED,
                'action_type': LoyaltyRule.ACTION_SIGNUP,
                'points_rate': Decimal('100.00'),  # Fixed 100 points
                'is_active': True,
                'priority': 2
            },
        ]

        rules = []
        for rule_data in rules_data:
            rule, _ = LoyaltyRule.objects.get_or_create(
                name=rule_data['name'],
                defaults=rule_data
            )
            rules.append(rule)

        return rules

    def create_rewards(self):
        """Create rewards catalog"""
        rewards_data = [
            {
                'name': '$5 Off Coupon',
                'slug': '5-off-coupon',
                'description': 'Get $5 off your next purchase',
                'points_cost': 500,
                'reward_type': LoyaltyReward.TYPE_DISCOUNT,
                'is_active': True
            },
            {
                'name': '$10 Off Coupon',
                'slug': '10-off-coupon',
                'description': 'Get $10 off your next purchase',
                'points_cost': 1000,
                'reward_type': LoyaltyReward.TYPE_DISCOUNT,
                'is_active': True
            },
            {
                'name': 'Free Shipping',
                'slug': 'free-shipping',
                'description': 'Free shipping on your next order',
                'points_cost': 750,
                'reward_type': LoyaltyReward.TYPE_SHIPPING,
                'is_active': True
            },
        ]

        rewards = []
        for reward_data in rewards_data:
            reward, _ = LoyaltyReward.objects.get_or_create(
                slug=reward_data['slug'],
                defaults=reward_data
            )
            rewards.append(reward)

        return rewards

    @transaction.atomic
    def create_members(self, count, tiers):
        """Create loyalty members from existing users"""
        users = User.objects.all()
        if count:
            users = users[:count]

        bronze_tier = tiers[0]  # Default to bronze
        members = []

        for user in users:
            # Create member with a join date spread over the past 180 days
            days_ago = random.randint(1, 180)
            enrolled_at = timezone.now() - timedelta(days=days_ago)

            member, created = LoyaltyMember.objects.get_or_create(
                customer=user,
                defaults={
                    'current_tier': bronze_tier,
                    'enrolled_at': enrolled_at,
                    'is_active': True
                }
            )

            if created:
                # Create balance
                LoyaltyBalance.objects.create(
                    member=member,
                    available_points=0,
                    pending_points=0,
                    lifetime_earned=0,
                    lifetime_redeemed=0,
                    lifetime_expired=0
                )

            members.append(member)

        return members

    def generate_transactions_from_orders(self, members, rules):
        """Generate loyalty transactions based on existing orders"""
        purchase_rule = next((r for r in rules if r.rule_type == LoyaltyRule.TYPE_SPEND_BASED), None)
        if not purchase_rule:
            return 0

        transaction_count = 0
        member_map = {m.customer_id: m for m in members}

        orders = Order.objects.select_related('user').filter(
            user__in=[m.customer for m in members],
            status__in=['completed', 'processing', 'shipped']
        )

        for order in orders:
            member = member_map.get(order.user_id)
            if not member:
                continue

            # Calculate points: 1 point per dollar (assuming order.total is in cents)
            points = int(order.total / 100)  # Total is in cents, so divide by 100 for dollars

            # Create transaction
            LoyaltyTransaction.objects.create(
                member=member,
                transaction_type=LoyaltyTransaction.TYPE_EARN,
                points=points,
                description=f'Purchase reward - Order #{order.order_number}',
                related_object_type='order',
                related_object_id=str(order.id),
                created_at=order.created_at
            )

            # Update balance
            balance = member.balance
            balance.available_points += points
            balance.lifetime_earned += points
            balance.last_earned_at = order.created_at
            balance.save()

            transaction_count += 1

        # Update tiers based on lifetime earned
        self.update_member_tiers(members)

        return transaction_count

    def generate_bonus_activity(self, members):
        """Generate additional bonus transactions"""
        bonus_count = 0

        # Select 60% of members for bonus activity to ensure enough have points for redemption
        active_members = random.sample(list(members), int(len(members) * 0.6))

        bonus_types = [
            ('Birthday bonus', 200),
            ('Review bonus', 50),
            ('Referral bonus', 100),
            ('Anniversary bonus', 150),
            ('Social share bonus', 25),
            ('Survey completion bonus', 75),
            ('Welcome bonus', 250),
            ('Milestone bonus', 300),
        ]

        for member in active_members:
            # Give 2-5 random bonuses to ensure members accumulate enough points
            num_bonuses = random.randint(2, 5)

            for _ in range(num_bonuses):
                bonus_type, points = random.choice(bonus_types)
                days_ago = random.randint(1, 120)  # Spread over 120 days
                bonus_date = timezone.now() - timedelta(days=days_ago)

                LoyaltyTransaction.objects.create(
                    member=member,
                    transaction_type=LoyaltyTransaction.TYPE_BONUS,
                    points=points,
                    description=bonus_type,
                    created_at=bonus_date
                )

                # Update balance
                balance = member.balance
                balance.available_points += points
                balance.lifetime_earned += points
                balance.save()

                bonus_count += 1

        # Update tiers again
        self.update_member_tiers(members)

        return bonus_count

    def update_member_tiers(self, members):
        """Update member tiers based on lifetime earned points"""
        tiers = list(LoyaltyTier.objects.order_by('-min_points_earned'))

        for member in members:
            lifetime = member.balance.lifetime_earned

            # Find appropriate tier
            for tier in tiers:
                if lifetime >= tier.min_points_earned:
                    member.current_tier = tier
                    member.save(update_fields=['current_tier'])
                    break

    def assign_segments(self, members, segments):
        """Assign members to segments based on criteria"""
        high_value = segments[0]
        active_shoppers = segments[1]
        at_risk = segments[2]

        thirty_days_ago = timezone.now() - timedelta(days=30)
        sixty_days_ago = timezone.now() - timedelta(days=60)

        for member in members:
            balance = member.balance

            # High value: lifetime earned > 500 points
            if balance.lifetime_earned >= 500:
                member.segments.add(high_value)

            # Active shoppers: earned points in last 30 days
            if balance.last_earned_at and balance.last_earned_at >= thirty_days_ago:
                member.segments.add(active_shoppers)

            # At risk: earned points before 60 days ago but not recently
            if balance.last_earned_at and balance.last_earned_at < sixty_days_ago and balance.lifetime_earned > 0:
                member.segments.add(at_risk)

    def create_campaigns(self, count, segments):
        """Create sample campaigns"""
        campaigns = []

        campaign_templates = [
            {
                'name': 'Welcome Journey',
                'slug': 'welcome-journey',
                'description': 'Multi-step welcome campaign for new members',
                'campaign_type': LoyaltyCampaign.TYPE_TRIGGER,
                'is_journey': True,
                'journey_steps': [
                    {
                        'step': 1,
                        'name': 'Welcome Email',
                        'actions': [{'type': 'send_email', 'template': 'loyalty_welcome'}],
                        'delay_days': 0
                    },
                    {
                        'step': 2,
                        'name': 'Signup Bonus',
                        'actions': [{'type': 'award_points', 'points': 100, 'reason': 'Welcome bonus'}],
                        'delay_days': 0
                    },
                    {
                        'step': 3,
                        'name': 'First Purchase Reminder',
                        'actions': [{'type': 'send_email', 'template': 'first_purchase_reminder'}],
                        'delay_days': 7
                    }
                ],
                'status': LoyaltyCampaign.STATUS_ACTIVE,
                'is_active': True
            },
            {
                'name': 'Birthday Campaign',
                'slug': 'birthday-campaign',
                'description': 'Send birthday rewards to members',
                'campaign_type': LoyaltyCampaign.TYPE_TRIGGER,
                'actions': [
                    {'type': 'award_points', 'points': 200, 'reason': 'Birthday bonus'},
                    {'type': 'send_email', 'template': 'loyalty_birthday'}
                ],
                'status': LoyaltyCampaign.STATUS_ACTIVE,
                'is_active': True
            },
            {
                'name': 'Double Points Weekend',
                'slug': 'double-points-weekend',
                'description': 'Promotional campaign for double points',
                'campaign_type': LoyaltyCampaign.TYPE_SCHEDULED,
                'actions': [
                    {'type': 'send_email', 'template': 'double_points_promo'}
                ],
                'status': LoyaltyCampaign.STATUS_ACTIVE,
                'is_active': True
            },
            {
                'name': 'Win-Back Campaign',
                'slug': 'win-back-campaign',
                'description': 'Re-engage at-risk customers',
                'campaign_type': LoyaltyCampaign.TYPE_TRIGGER,
                'actions': [
                    {'type': 'award_points', 'points': 150, 'reason': 'We miss you!'},
                    {'type': 'send_email', 'template': 'win_back'}
                ],
                'status': LoyaltyCampaign.STATUS_ACTIVE,
                'is_active': True
            },
            {
                'name': 'Tier Upgrade Celebration',
                'slug': 'tier-upgrade-celebration',
                'description': 'Celebrate tier upgrades',
                'campaign_type': LoyaltyCampaign.TYPE_TRIGGER,
                'actions': [
                    {'type': 'send_email', 'template': 'tier_upgrade'},
                    {'type': 'award_points', 'points': 250, 'reason': 'Tier upgrade bonus'}
                ],
                'status': LoyaltyCampaign.STATUS_ACTIVE,
                'is_active': True
            },
        ]

        for i, template in enumerate(campaign_templates[:count]):
            campaign = LoyaltyCampaign.objects.create(**template)
            campaigns.append(campaign)

        return campaigns

    def generate_campaign_executions(self, campaigns, members):
        """Generate campaign execution history"""
        execution_count = 0

        for campaign in campaigns:
            # Select random members who would have triggered this campaign
            num_executions = random.randint(10, min(50, len(members)))
            selected_members = random.sample(list(members), num_executions)

            for member in selected_members:
                days_ago = random.randint(1, 60)
                triggered_at = timezone.now() - timedelta(days=days_ago)

                # 80% completion rate, 15% in progress, 5% failed
                status_roll = random.random()
                if status_roll < 0.80:
                    status = LoyaltyCampaignExecution.STATUS_COMPLETED
                    completed_at = triggered_at + timedelta(hours=random.randint(1, 24))
                elif status_roll < 0.95:
                    status = LoyaltyCampaignExecution.STATUS_PROCESSING
                    completed_at = None
                else:
                    status = LoyaltyCampaignExecution.STATUS_FAILED
                    completed_at = triggered_at + timedelta(hours=1)

                # Calculate points awarded
                points_awarded = 0
                if campaign.actions:
                    for action in campaign.actions:
                        if action.get('type') == 'award_points':
                            points_awarded += action.get('points', 0)

                # Create execution
                execution_data = {
                    'campaign': campaign,
                    'member': member,
                    'triggered_at': triggered_at,
                    'completed_at': completed_at,
                    'status': status,
                    'points_awarded': points_awarded,
                    'emails_sent': ['loyalty@example.com'] if status == LoyaltyCampaignExecution.STATUS_COMPLETED else [],
                    'rewards_issued': [],
                    'steps_completed': [1] if campaign.is_journey and status == LoyaltyCampaignExecution.STATUS_COMPLETED else [],
                }

                if campaign.is_journey:
                    execution_data['current_step'] = 1

                execution = LoyaltyCampaignExecution.objects.create(**execution_data)

                execution_count += 1

        return execution_count

    @transaction.atomic
    def generate_redemptions(self, members, rewards):
        """Generate realistic redemption history"""
        import string

        redemption_count = 0

        # Only allow members with sufficient points to redeem
        # Minimum reward cost is 500 points
        eligible_members = [m for m in members if m.balance.available_points >= 500]

        if not eligible_members:
            return 0

        # Select 15-25% of eligible members to have redeemed
        redemption_rate = random.uniform(0.15, 0.25)
        num_redeemers = int(len(eligible_members) * redemption_rate)

        if num_redeemers == 0:
            return 0

        selected_members = random.sample(eligible_members, num_redeemers)

        for member in selected_members:
            # Each member redeems 1-3 rewards over the past 90 days
            num_redemptions = random.randint(1, min(3, member.balance.available_points // 500))

            for _ in range(num_redemptions):
                # Find rewards the member can afford
                affordable_rewards = [r for r in rewards if r.points_cost <= member.balance.available_points]

                if not affordable_rewards:
                    break

                reward = random.choice(affordable_rewards)
                points_spent = reward.points_cost

                # Random redemption date within last 90 days
                days_ago = random.randint(1, 90)
                redeemed_at = timezone.now() - timedelta(days=days_ago)

                # Generate unique redemption code
                code_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                redemption_code = f'LOYALTY-{code_suffix[:5]}-{code_suffix[5:]}'

                # 90% fulfilled, 5% confirmed, 5% pending
                status_roll = random.random()
                if status_roll < 0.90:
                    status = LoyaltyRedemption.STATUS_FULFILLED
                    confirmed_at = redeemed_at + timedelta(minutes=random.randint(5, 30))
                    fulfilled_at = confirmed_at + timedelta(hours=random.randint(1, 48))
                elif status_roll < 0.95:
                    status = LoyaltyRedemption.STATUS_CONFIRMED
                    confirmed_at = redeemed_at + timedelta(minutes=random.randint(5, 30))
                    fulfilled_at = None
                else:
                    status = LoyaltyRedemption.STATUS_PENDING
                    confirmed_at = None
                    fulfilled_at = None

                # Create redemption record first (without transaction)
                redemption_data = {
                    'member': member,
                    'reward': reward,
                    'points_spent': points_spent,
                    'status': status,
                    'redemption_code': redemption_code,
                    'expires_at': redeemed_at + timedelta(days=90),  # 90 day expiry
                    'confirmed_at': confirmed_at,
                    'fulfilled_at': fulfilled_at,
                }

                redemption = LoyaltyRedemption.objects.create(**redemption_data)

                # Create redemption transaction (points deduction) with redemption reference
                redemption_transaction = LoyaltyTransaction.objects.create(
                    member=member,
                    transaction_type=LoyaltyTransaction.TYPE_REDEEM,
                    points=-points_spent,  # Negative for redemption
                    description=f'Redeemed: {reward.name}',
                    related_object_type='redemption',
                    related_object_id=str(redemption.id),
                    created_at=redeemed_at
                )

                # Link transaction to redemption
                redemption.transaction = redemption_transaction
                redemption.save(update_fields=['transaction'])

                # Update member balance
                balance = member.balance
                balance.available_points -= points_spent
                balance.lifetime_redeemed += points_spent
                balance.save()

                redemption_count += 1

        return redemption_count

    def print_summary(self):
        """Print summary of generated data"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('LOYALTY PROGRAM DATA GENERATION COMPLETE'))
        self.stdout.write('='*60)

        self.stdout.write(f'\nMembers: {LoyaltyMember.objects.count()}')
        self.stdout.write(f'Transactions: {LoyaltyTransaction.objects.count()}')
        self.stdout.write(f'Redemptions: {LoyaltyRedemption.objects.count()}')
        self.stdout.write(f'Campaigns: {LoyaltyCampaign.objects.count()}')
        self.stdout.write(f'Campaign Executions: {LoyaltyCampaignExecution.objects.count()}')
        self.stdout.write(f'Tiers: {LoyaltyTier.objects.count()}')
        self.stdout.write(f'Segments: {LoyaltySegment.objects.count()}')
        self.stdout.write(f'Rules: {LoyaltyRule.objects.count()}')
        self.stdout.write(f'Rewards: {LoyaltyReward.objects.count()}')

        # Tier distribution
        self.stdout.write('\nTier Distribution:')
        for tier in LoyaltyTier.objects.order_by('rank'):
            count = LoyaltyMember.objects.filter(current_tier=tier).count()
            self.stdout.write(f'  {tier.name}: {count} members')

        # Points summary
        from django.db.models import Sum
        total_available = LoyaltyBalance.objects.aggregate(total=Sum('available_points'))['total'] or 0
        total_earned = LoyaltyBalance.objects.aggregate(total=Sum('lifetime_earned'))['total'] or 0
        total_redeemed = LoyaltyBalance.objects.aggregate(total=Sum('lifetime_redeemed'))['total'] or 0
        self.stdout.write(f'\nTotal Available Points: {total_available:,}')
        self.stdout.write(f'Total Earned Points: {total_earned:,}')
        self.stdout.write(f'Total Redeemed Points: {total_redeemed:,}')

        # Redemption statistics
        if total_earned > 0:
            redemption_rate = (total_redeemed / total_earned) * 100
            self.stdout.write(f'Redemption Rate: {redemption_rate:.1f}%')

        self.stdout.write('\n' + '='*60 + '\n')
