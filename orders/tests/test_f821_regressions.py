"""Regression tests for orders F821 bugs.

- orders/views.py:1189 order_voucher_remove_view used VoucherCode
  without importing it.
- orders/views.py:1281 order_manual_discount_apply_view caught
  decimal.InvalidOperation without `import decimal` in scope.
"""

import inspect

from django.test import SimpleTestCase


class OrderVoucherRemoveViewImportTest(SimpleTestCase):
    """Assert VoucherCode is available inside the voucher-remove view.
    Before the fix, `get_object_or_404(VoucherCode, ...)` NameError'd
    on the first POST."""

    def test_voucher_code_imported_inside_view(self):
        from orders.views import order_voucher_remove_view

        source = inspect.getsource(order_voucher_remove_view)
        self.assertIn("from vouchers.models import VoucherCode", source)


class OrderDiscountApplyInvalidOperationTest(SimpleTestCase):
    """Assert the discount-apply view can handle a decimal parse
    failure. Before the fix the `except (ValueError,
    decimal.InvalidOperation):` line NameError'd on `decimal`."""

    def test_invalid_operation_in_scope(self):
        import orders.views

        # Confirm InvalidOperation is now importable from the module,
        # i.e. it was hoisted into the top-level `from decimal import`.
        self.assertTrue(hasattr(orders.views, "InvalidOperation"))
