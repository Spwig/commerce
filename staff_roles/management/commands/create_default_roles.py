"""
Management command to create predefined staff roles.

Idempotent - safe to run multiple times. Updates existing predefined roles
but preserves any customizations to permission_categories and pos_permissions.
"""
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from staff_roles.models import StaffRole


PREDEFINED_ROLES = [
    {
        'group_name': 'store_owner',
        'display_name': 'Store Owner',
        'description': 'Full access to all store features. Assigned to the primary store administrator.',
        'icon': 'fas fa-crown',
        'color': 'warning',
        'can_access_admin': True,
        'can_access_pos': True,
        'sort_order': 1,
        'permission_categories': {
            'catalog': 'full',
            'orders': 'full',
            'customers': 'full',
            'content': 'full',
            'design': 'full',
            'marketing': 'full',
            'media': 'full',
            'email': 'full',
            'payments': 'full',
            'search': 'full',
            'settings': 'full',
            'pos_admin': 'full',
            'users': 'full',
            'translations': 'full',
            'custom_fields': 'full',
            'system': 'full',
        },
        'pos_permissions': {
            'pos_access': True,
            'pos_discount_manual': True,
            'pos_discount_max_percent': 100,
            'pos_price_override': True,
            'pos_refund': True,
            'pos_void': True,
            'pos_gift_card_issue': True,
            'pos_gift_card_balance': True,
            'pos_cash_management': True,
            'pos_open_drawer': True,
            'pos_close_shift': True,
            'pos_view_reports': True,
            'pos_stock_adjustment': True,
        },
    },
    {
        'group_name': 'store_manager',
        'display_name': 'Store Manager',
        'description': 'Day-to-day store operations including products, orders, and customer management.',
        'icon': 'fas fa-user-tie',
        'color': 'primary',
        'can_access_admin': True,
        'can_access_pos': True,
        'sort_order': 2,
        'permission_categories': {
            'catalog': 'full',
            'orders': 'full',
            'customers': 'full',
            'content': 'view',
            'design': 'view',
            'marketing': 'full',
            'media': 'full',
            'email': 'view',
            'payments': 'view',
            'search': 'full',
            'settings': 'view',
            'pos_admin': 'full',
            'users': 'view',
            'translations': 'view',
            'custom_fields': 'view',
            'system': 'view',
        },
        'pos_permissions': {
            'pos_access': True,
            'pos_discount_manual': True,
            'pos_discount_max_percent': 50,
            'pos_price_override': True,
            'pos_refund': True,
            'pos_void': True,
            'pos_gift_card_issue': True,
            'pos_gift_card_balance': True,
            'pos_cash_management': True,
            'pos_open_drawer': True,
            'pos_close_shift': True,
            'pos_view_reports': True,
            'pos_stock_adjustment': True,
        },
    },
    {
        'group_name': 'content_editor',
        'display_name': 'Content Editor',
        'description': 'Manages pages, blog posts, design, and media content.',
        'icon': 'fas fa-pen-fancy',
        'color': 'info',
        'can_access_admin': True,
        'can_access_pos': False,
        'sort_order': 3,
        'permission_categories': {
            'catalog': 'view',
            'content': 'full',
            'design': 'full',
            'media': 'full',
            'translations': 'view',
        },
        'pos_permissions': {},
    },
    {
        'group_name': 'order_manager',
        'display_name': 'Order Manager',
        'description': 'Handles orders, shipping, returns, and customer service.',
        'icon': 'fas fa-box',
        'color': 'success',
        'can_access_admin': True,
        'can_access_pos': False,
        'sort_order': 4,
        'permission_categories': {
            'catalog': 'view',
            'orders': 'full',
            'customers': 'full',
        },
        'pos_permissions': {},
    },
    {
        'group_name': 'demo_viewer',
        'display_name': 'Demo Viewer',
        'description': 'Read-only access to all admin sections. Ideal for demos, stakeholders, or auditors.',
        'icon': 'fas fa-eye',
        'color': 'info',
        'can_access_admin': True,
        'can_access_pos': False,
        'sort_order': 5,
        'permission_categories': {
            'catalog': 'view',
            'orders': 'view',
            'customers': 'view',
            'content': 'view',
            'design': 'view',
            'marketing': 'view',
            'media': 'view',
            'email': 'view',
            'payments': 'view',
            'search': 'view',
            'settings': 'view',
            'pos_admin': 'view',
            'users': 'view',
            'translations': 'view',
            'custom_fields': 'view',
            'system': 'view',
        },
        'pos_permissions': {},
    },
    {
        'group_name': 'marketing_manager',
        'display_name': 'Marketing Manager',
        'description': 'Manages promotions, vouchers, affiliate, loyalty, and referral programs.',
        'icon': 'fas fa-bullhorn',
        'color': 'primary',
        'can_access_admin': True,
        'can_access_pos': False,
        'sort_order': 6,
        'permission_categories': {
            'catalog': 'view',
            'customers': 'view',
            'marketing': 'full',
            'media': 'view',
        },
        'pos_permissions': {},
    },
    {
        'group_name': 'cashier',
        'display_name': 'Cashier',
        'description': 'POS-only frontline staff. Can process sales and basic operations.',
        'icon': 'fas fa-cash-register',
        'color': 'default',
        'can_access_admin': False,
        'can_access_pos': True,
        'sort_order': 7,
        'permission_categories': {},
        'pos_permissions': {
            'pos_access': True,
            'pos_discount_manual': False,
            'pos_discount_max_percent': 0,
            'pos_price_override': False,
            'pos_refund': False,
            'pos_void': False,
            'pos_gift_card_issue': False,
            'pos_gift_card_balance': True,
            'pos_cash_management': False,
            'pos_open_drawer': False,
            'pos_close_shift': True,
            'pos_view_reports': False,
            'pos_stock_adjustment': False,
        },
    },
    {
        'group_name': 'senior_cashier',
        'display_name': 'Senior Cashier',
        'description': 'Experienced POS staff with refund, discount, and cash management authority.',
        'icon': 'fas fa-user-check',
        'color': 'success',
        'can_access_admin': False,
        'can_access_pos': True,
        'sort_order': 8,
        'permission_categories': {},
        'pos_permissions': {
            'pos_access': True,
            'pos_discount_manual': True,
            'pos_discount_max_percent': 25,
            'pos_price_override': False,
            'pos_refund': True,
            'pos_void': False,
            'pos_gift_card_issue': False,
            'pos_gift_card_balance': True,
            'pos_cash_management': True,
            'pos_open_drawer': True,
            'pos_close_shift': True,
            'pos_view_reports': True,
            'pos_stock_adjustment': False,
        },
    },
]


class Command(BaseCommand):
    help = 'Create predefined staff roles for the shop'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-update',
            action='store_true',
            help='Force update permission_categories and pos_permissions on existing predefined roles',
        )

    def handle(self, *args, **options):
        force_update = options.get('force_update', False)
        created_count = 0
        updated_count = 0

        for role_def in PREDEFINED_ROLES:
            group, group_created = Group.objects.get_or_create(
                name=role_def['group_name'],
            )

            try:
                role = StaffRole.objects.get(group=group)
                # Update metadata fields always
                role.display_name = role_def['display_name']
                role.description = role_def['description']
                role.icon = role_def['icon']
                role.color = role_def['color']
                role.can_access_admin = role_def['can_access_admin']
                role.can_access_pos = role_def['can_access_pos']
                role.sort_order = role_def['sort_order']
                role.is_predefined = True

                if force_update:
                    role.permission_categories = role_def['permission_categories']
                    role.pos_permissions = role_def['pos_permissions']

                role.save()
                updated_count += 1
                self.stdout.write(f'  Updated: {role_def["display_name"]}')

            except StaffRole.DoesNotExist:
                role = StaffRole.objects.create(
                    group=group,
                    display_name=role_def['display_name'],
                    description=role_def['description'],
                    icon=role_def['icon'],
                    color=role_def['color'],
                    is_predefined=True,
                    can_access_admin=role_def['can_access_admin'],
                    can_access_pos=role_def['can_access_pos'],
                    sort_order=role_def['sort_order'],
                    permission_categories=role_def['permission_categories'],
                    pos_permissions=role_def['pos_permissions'],
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {role_def["display_name"]}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {created_count}, updated {updated_count} roles.'
        ))
