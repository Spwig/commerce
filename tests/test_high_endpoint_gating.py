"""Regression: the HIGH-severity admin filter endpoints must stay permission-gated.

The staff-permissions audit flagged these as leaking bearer secrets (license
keys, gift-card codes), payment data, customer PII, or affiliate financials to
any staff user. Each was hardened with @requires_permission, which stamps a
``spwig_permission_gate`` marker that survives functools.wraps. This test fails
if a gate is ever removed — cheaper and more stable than driving each endpoint
with a live permission-less user.
"""

import importlib

import pytest

# (module path, function name, expected permission codename)
GATED = [
    ("catalog.catalog_views", "filter_license_keys", "catalog.view_licensekey"),
    ("catalog.catalog_views", "filter_license_pools", "catalog.view_licensepool"),
    ("catalog.catalog_views", "filter_external_sync", "catalog.view_externallicensesync"),
    ("catalog.catalog_views", "filter_digital_assets", "catalog.view_digitalasset"),
    ("catalog.admin_views", "filter_gift_cards", "catalog.view_giftcard"),
    ("catalog.admin_views", "filter_gift_card_transactions", "catalog.view_giftcardtransaction"),
    (
        "payment_providers.admin_views",
        "filter_transactions",
        "payment_providers.view_paymenttransaction",
    ),
    ("payment_providers.admin_views", "filter_webhooks", "payment_providers.view_paymentwebhook"),
    ("accounts.admin_views", "filter_preferences", "accounts.view_communicationpreference"),
    ("accounts.admin_views", "filter_preference_changelogs", "accounts.view_preferencechangelog"),
    ("affiliate.admin_views", "filter_commissions", "affiliate.view_commission"),
    ("affiliate.admin_views", "filter_affiliates", "affiliate.view_affiliate"),
    ("affiliate.admin_views", "filter_payouts", "affiliate.view_payout"),
    ("affiliate.views", "filter_affiliates", "affiliate.view_affiliate"),
    ("affiliate.views", "filter_payouts", "affiliate.view_payout"),
]


@pytest.mark.parametrize("module, func_name, perm", GATED, ids=[f"{m}:{f}" for m, f, _ in GATED])
def test_high_endpoint_is_permission_gated(module, func_name, perm):
    fn = getattr(importlib.import_module(module), func_name)
    gate = getattr(fn, "spwig_permission_gate", None)
    assert gate is not None, f"{module}.{func_name} lost its permission gate"
    assert gate[0] == "permission", (
        f"{module}.{func_name} gate is {gate!r}, expected a permission gate"
    )
    assert perm in gate[1], f"{module}.{func_name} no longer requires {perm} (gate={gate!r})"
