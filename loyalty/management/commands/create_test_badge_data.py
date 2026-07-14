"""
Management command to create test badge achievement data.

Usage:
    python manage.py create_test_badge_data
"""

import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from loyalty.models import LoyaltyBadge, LoyaltyMember, LoyaltyMemberBadge, LoyaltyTransaction

User = get_user_model()


class Command(BaseCommand):
    help = "Creates test data for badge achievements"

    def handle(self, *args, **options):
        """Create test badge achievement data"""

        # Get existing badges
        badges = list(LoyaltyBadge.objects.filter(is_active=True))
        if not badges:
            self.stdout.write(self.style.ERROR("No badges found. Please create badges first."))
            return

        # Get or create test users
        test_users = []
        for i in range(1, 11):  # Create 10 test users
            username = f"loyaltytest{i}"
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username,
                    email=f"loyaltytest{i}@example.com",
                    first_name="Loyalty",
                    last_name=f"Tester {i}",
                )
            test_users.append(user)

        # Create or get loyalty members for these users
        members = []
        for user in test_users:
            member, created = LoyaltyMember.objects.get_or_create(
                customer=user,
                defaults={
                    "is_active": True,
                },
            )
            members.append(member)
            if created:
                self.stdout.write(f"  Created loyalty member for {user.username}")

        # Award badges to members (random distribution)
        awarded_count = 0
        for badge in badges:
            # Award each badge to a random number of members (0-7 members)
            num_awards = random.randint(0, 7)
            selected_members = random.sample(members, min(num_awards, len(members)))

            for member in selected_members:
                # Check if already awarded
                if not LoyaltyMemberBadge.objects.filter(member=member, badge=badge).exists():
                    # Create transaction for points reward
                    transaction = None
                    if badge.points_reward > 0:
                        transaction = LoyaltyTransaction.objects.create(
                            member=member,
                            transaction_type="earn",
                            points=badge.points_reward,
                            description=f"Earned badge: {badge.name}",
                            status="completed",
                        )

                    # Award badge
                    LoyaltyMemberBadge.objects.create(
                        member=member, badge=badge, transaction=transaction
                    )
                    awarded_count += 1
                    self.stdout.write(f'  Awarded "{badge.name}" to {member.customer.username}')

        # Summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(members)} loyalty members"))
        self.stdout.write(self.style.SUCCESS(f"✓ Awarded {awarded_count} badges"))

        # Show badge stats
        self.stdout.write("\n" + "Badge Achievement Stats:")
        for badge in badges[:10]:  # Show first 10
            count = badge.earned_by.count()
            self.stdout.write(f"  {badge.name}: {count} members")

        self.stdout.write("=" * 50)
