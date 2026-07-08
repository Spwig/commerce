"""
POS-specific permission flags.

These are NOT Django model permissions. They are boolean/integer flags
stored in StaffRole.pos_permissions JSONField, checked at the POS API layer.
"""
from django.utils.translation import gettext_lazy as _


POS_PERMISSION_FLAGS = {
    'pos_access': {
        'label': _('POS Access'),
        'description': _('Can use the POS system'),
        'type': 'bool',
        'default': False,
        'group': 'general',
    },
    'pos_discount_manual': {
        'label': _('Manual Discounts'),
        'description': _('Can apply manual line-item or cart-level discounts'),
        'type': 'bool',
        'default': False,
        'group': 'sales',
    },
    'pos_discount_max_percent': {
        'label': _('Maximum Discount %'),
        'description': _('Maximum manual discount percentage allowed (0-100)'),
        'type': 'integer',
        'default': 0,
        'min': 0,
        'max': 100,
        'group': 'sales',
    },
    'pos_price_override': {
        'label': _('Price Override'),
        'description': _('Can override product prices at the register'),
        'type': 'bool',
        'default': False,
        'group': 'sales',
    },
    'pos_refund': {
        'label': _('Process Refunds'),
        'description': _('Can process refunds on POS orders'),
        'type': 'bool',
        'default': False,
        'group': 'refunds',
    },
    'pos_void': {
        'label': _('Void Orders'),
        'description': _('Can void POS orders from the current shift'),
        'type': 'bool',
        'default': False,
        'group': 'refunds',
    },
    'pos_gift_card_issue': {
        'label': _('Issue Gift Cards'),
        'description': _('Can issue new gift cards at the register'),
        'type': 'bool',
        'default': False,
        'group': 'gift_cards',
    },
    'pos_gift_card_balance': {
        'label': _('Check Gift Card Balance'),
        'description': _('Can look up gift card balances'),
        'type': 'bool',
        'default': True,
        'group': 'gift_cards',
    },
    'pos_cash_management': {
        'label': _('Cash Management'),
        'description': _('Can perform cash-in and cash-out operations'),
        'type': 'bool',
        'default': False,
        'group': 'cash',
    },
    'pos_open_drawer': {
        'label': _('Open Cash Drawer'),
        'description': _('Can open the cash drawer without a sale'),
        'type': 'bool',
        'default': False,
        'group': 'cash',
    },
    'pos_close_shift': {
        'label': _('Close Shifts'),
        'description': _('Can close shifts and perform cash reconciliation'),
        'type': 'bool',
        'default': False,
        'group': 'cash',
    },
    'pos_view_reports': {
        'label': _('View POS Reports'),
        'description': _('Can view shift reports and sales summaries'),
        'type': 'bool',
        'default': False,
        'group': 'reports',
    },
    'pos_stock_adjustment': {
        'label': _('Stock Adjustments'),
        'description': _('Can adjust stock levels (receive, damage, recount, return)'),
        'type': 'bool',
        'default': False,
        'group': 'inventory',
    },
}

# Groups for UI display
POS_PERMISSION_GROUPS = {
    'general': {
        'label': _('General'),
        'icon': 'fas fa-cash-register',
    },
    'sales': {
        'label': _('Sales & Discounts'),
        'icon': 'fas fa-percentage',
    },
    'refunds': {
        'label': _('Refunds & Voids'),
        'icon': 'fas fa-undo',
    },
    'gift_cards': {
        'label': _('Gift Cards'),
        'icon': 'fas fa-gift',
    },
    'cash': {
        'label': _('Cash Management'),
        'icon': 'fas fa-money-bill-wave',
    },
    'reports': {
        'label': _('Reporting'),
        'icon': 'fas fa-chart-bar',
    },
    'inventory': {
        'label': _('Inventory'),
        'icon': 'fas fa-boxes-stacked',
    },
}
