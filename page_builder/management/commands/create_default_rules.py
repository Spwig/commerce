"""
Create default visibility rule groups for the platform.

These provide merchants with ready-to-use targeting rules for
announcements, page elements, and other visibility-controlled content.

"""
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from page_builder.models import VisibilityRule, RuleGroup, RuleGroupMember


# Default rules: (name, description, rule_type, operator, value)
DEFAULT_RULES = [
    # User & Authentication
    ('User is Logged In', 'Matches when the visitor is authenticated', 'user_logged_in', 'is_true', {}),
    ('User is Guest', 'Matches when the visitor is not logged in', 'user_logged_in', 'is_false', {}),
    ('Has Purchased Before', 'Matches returning customers who placed at least one order', 'has_purchased', 'is_true', {}),
    ('First Time Visitor', 'Matches visitors on their first session', 'first_visit', 'is_true', {}),
    ('Returning Visitor', 'Matches visitors who have been to the site before', 'first_visit', 'is_false', {}),

    # Device
    ('Device is Mobile', 'Matches mobile phones', 'device_type', 'equals', {'value': 'mobile'}),
    ('Device is Desktop', 'Matches desktop computers', 'device_type', 'equals', {'value': 'desktop'}),
    ('Device is Tablet', 'Matches tablets', 'device_type', 'equals', {'value': 'tablet'}),

    # E-commerce
    ('Cart Has Items', 'Matches when the cart contains at least one item', 'cart_items', 'greater_than', {'value': 0}),
    ('Cart is Empty', 'Matches when the cart is empty', 'cart_items', 'equals', {'value': 0}),
    ('Has Wishlist Items', 'Matches visitors with items in their wishlist', 'wishlist_items', 'is_true', {}),
]

# Default rule groups: (name, description, logic_operator, [rule_names])
DEFAULT_GROUPS = [
    ('Logged In Users', 'Show only to authenticated users', 'AND', ['User is Logged In']),
    ('Guest Users', 'Show only to visitors who are not logged in', 'AND', ['User is Guest']),
    ('Mobile Devices', 'Show only on mobile phones', 'AND', ['Device is Mobile']),
    ('Desktop Devices', 'Show only on desktop computers', 'AND', ['Device is Desktop']),
    ('Tablet Devices', 'Show only on tablets', 'AND', ['Device is Tablet']),
    ('Returning Customers', 'Show to visitors who have purchased before', 'AND', ['Has Purchased Before']),
    ('First Time Visitors', 'Show to first-time visitors only', 'AND', ['First Time Visitor']),
    ('Returning Visitors', 'Show to visitors who have been here before', 'AND', ['Returning Visitor']),
    ('Non-Empty Cart', 'Show when the visitor has items in their cart', 'AND', ['Cart Has Items']),
    ('Empty Cart', 'Show when the visitor has an empty cart', 'AND', ['Cart is Empty']),
]


class Command(BaseCommand):
    help = 'Create default visibility rules and rule groups'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Recreate rules even if they already exist',
        )

    def handle(self, *args, **options):
        force = options['force']
        rules_created = 0
        groups_created = 0

        # Create rules
        rule_objects = {}
        for name, description, rule_type, operator, value in DEFAULT_RULES:
            rule, created = VisibilityRule.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'rule_type': rule_type,
                    'operator': operator,
                    'value': value,
                    'is_active': True,
                }
            )
            if created:
                rules_created += 1
                self.stdout.write(self.style.SUCCESS(f'  Created rule: {name}'))
            elif force:
                rule.description = description
                rule.rule_type = rule_type
                rule.operator = operator
                rule.value = value
                rule.save()
                self.stdout.write(f'  Updated rule: {name}')
            rule_objects[name] = rule

        # Create groups
        for name, description, logic_op, rule_names in DEFAULT_GROUPS:
            group, created = RuleGroup.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'logic_operator': logic_op,
                    'is_active': True,
                }
            )
            if created:
                groups_created += 1
                for order, rule_name in enumerate(rule_names):
                    if rule_name in rule_objects:
                        RuleGroupMember.objects.get_or_create(
                            rule_group=group,
                            rule=rule_objects[rule_name],
                            defaults={'order': order}
                        )
                self.stdout.write(self.style.SUCCESS(f'  Created group: {name}'))
            elif force:
                group.description = description
                group.logic_operator = logic_op
                group.save()
                # Rebuild members
                group.rulegroupmember_set.all().delete()
                for order, rule_name in enumerate(rule_names):
                    if rule_name in rule_objects:
                        RuleGroupMember.objects.create(
                            rule_group=group,
                            rule=rule_objects[rule_name],
                            order=order,
                        )
                self.stdout.write(f'  Updated group: {name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone: {rules_created} rules created, {groups_created} groups created'
        ))
