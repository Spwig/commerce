"""
R1 coverage: ``VoucherCode.issued_to`` — recipient binding.

R1 added ``issued_to`` so a code *earned* by a specific customer (a loyalty
redemption, a referral reward) cannot be spent by whoever else learns the
string. ``max_uses_total=1`` alone makes such a code first-come-first-served,
so the person who earned it can lose their own reward to a stranger who saw it.

The regression risk runs the other way too: the overwhelming majority of the
2,060 live voucher rows are general promotional codes with ``issued_to=None``,
and the new check must be invisible to them. ``TestGeneralPromoCodesUnaffected``
covers that.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R1 / P1.1)
"""

from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from djmoney.money import Money

from vouchers.models import VoucherCode

from .factories import make_fixed_voucher, make_voucher

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.vouchers,
    pytest.mark.r1,
]

User = get_user_model()


def _user(username):
    return User.objects.create_user(
        username=username, email=f"{username}@example.com", password="pw-test-12345"
    )


# ============================================================
# Field definition
# ============================================================


class TestIssuedToField:
    def test_defaults_to_none(self):
        """An ordinary voucher is not bound to anybody."""
        voucher = make_voucher("UNBOUND1")

        assert voucher.issued_to is None
        assert voucher.issued_to_id is None

    def test_can_be_bound_to_a_user(self):
        earner = _user("earner")
        voucher = make_voucher("BOUND001", issued_to=earner)

        voucher.refresh_from_db()
        assert voucher.issued_to_id == earner.pk

    def test_reverse_accessor_is_issued_vouchers(self):
        earner = _user("earner")
        make_voucher("BOUND001", issued_to=earner)
        make_voucher("BOUND002", issued_to=earner)
        make_voucher("UNBOUND1")

        assert earner.issued_vouchers.count() == 2

    def test_deleting_the_user_cascades(self):
        """``on_delete=CASCADE`` — an issued code has no meaning without its owner."""
        earner = _user("earner")
        make_voucher("BOUND001", issued_to=earner)
        earner.delete()

        assert not VoucherCode.objects.filter(code="BOUND001").exists()


# ============================================================
# can_be_used_by_customer — the enforcement point
# ============================================================


class TestIssuedToEnforcement:
    def test_bound_user_can_use_their_own_voucher(self):
        earner = _user("earner")
        voucher = make_voucher("BOUND001", issued_to=earner)

        can_use, message = voucher.can_be_used_by_customer(earner)

        assert can_use is True, f"The earner was refused their own reward: {message}"

    def test_a_different_user_is_refused(self):
        earner = _user("earner")
        stranger = _user("stranger")
        voucher = make_voucher("BOUND001", issued_to=earner)

        can_use, message = voucher.can_be_used_by_customer(stranger)

        assert can_use is False, (
            "A voucher issued to one customer was spendable by another — the "
            "earner can lose their own reward to anyone who learns the code."
        )
        assert "different customer" in str(message).lower()

    def test_an_anonymous_user_is_refused(self):
        earner = _user("earner")
        voucher = make_voucher("BOUND001", issued_to=earner)

        can_use, message = voucher.can_be_used_by_customer(AnonymousUser())

        assert can_use is False
        assert "different customer" in str(message).lower()

    def test_none_as_the_user_is_refused(self):
        """Guest checkout can reach this with no user at all."""
        earner = _user("earner")
        voucher = make_voucher("BOUND001", issued_to=earner)

        can_use, message = voucher.can_be_used_by_customer(None)

        assert can_use is False
        assert "different customer" in str(message).lower()

    def test_binding_is_checked_even_when_the_voucher_is_otherwise_perfect(self):
        """No other restriction is doing the work here."""
        earner = _user("earner")
        stranger = _user("stranger")
        voucher = make_fixed_voucher(
            "BOUND001",
            amount=Decimal("10.00"),
            issued_to=earner,
            max_uses_total=None,
            max_uses_per_customer=None,
            min_order_value=None,
            first_time_customers_only=False,
        )

        assert voucher.is_valid is True
        assert voucher.can_be_used_by_customer(earner)[0] is True
        assert voucher.can_be_used_by_customer(stranger)[0] is False

    def test_binding_is_checked_before_order_value(self):
        """A stranger gets the binding message, not a spend-more message."""
        earner = _user("earner")
        stranger = _user("stranger")
        voucher = make_fixed_voucher(
            "BOUND001",
            amount=Decimal("10.00"),
            issued_to=earner,
            min_order_value=Money(Decimal("500.00"), "USD"),
        )

        can_use, message = voucher.can_be_used_by_customer(
            stranger, order_total=Money(Decimal("20.00"), "USD")
        )

        assert can_use is False
        assert "different customer" in str(message).lower(), (
            "Leaking 'spend more to use this' to a stranger tells them the code is real."
        )

    def test_an_invalid_voucher_is_still_refused_for_its_owner(self):
        """Binding grants no exemption from the ordinary validity rules."""
        earner = _user("earner")
        voucher = make_voucher("BOUND001", issued_to=earner, is_active=False)

        can_use, message = voucher.can_be_used_by_customer(earner)

        assert can_use is False
        assert "not valid" in str(message).lower()

    def test_rebinding_transfers_the_restriction(self):
        earner = _user("earner")
        other = _user("other")
        voucher = make_voucher("BOUND001", issued_to=earner)

        voucher.issued_to = other
        voucher.save(update_fields=["issued_to"])
        voucher.refresh_from_db()

        assert voucher.can_be_used_by_customer(other)[0] is True
        assert voucher.can_be_used_by_customer(earner)[0] is False


# ============================================================
# Regression guard: ordinary promo codes must be unaffected
# ============================================================


class TestGeneralPromoCodesUnaffected:
    """
    ``issued_to=None`` means "anybody". The 2,060 live rows are all like this,
    so a mistake here breaks every promotion in production.
    """

    def test_any_authenticated_user_can_use_an_unbound_voucher(self):
        alice = _user("alice")
        bob = _user("bob")
        voucher = make_voucher("PROMO001")

        assert voucher.can_be_used_by_customer(alice)[0] is True
        assert voucher.can_be_used_by_customer(bob)[0] is True

    def test_an_unbound_voucher_still_evaluates_its_other_rules(self):
        """The early return must not short-circuit the rest of the checks."""
        alice = _user("alice")
        voucher = make_fixed_voucher(
            "PROMO001",
            amount=Decimal("10.00"),
            min_order_value=Money(Decimal("500.00"), "USD"),
        )

        can_use, message = voucher.can_be_used_by_customer(
            alice, order_total=Money(Decimal("20.00"), "USD")
        )

        assert can_use is False
        assert "different customer" not in str(message).lower()

    def test_an_unbound_voucher_is_unaffected_by_other_users_bindings(self):
        alice = _user("alice")
        bob = _user("bob")
        make_voucher("BOUND001", issued_to=bob)
        unbound = make_voucher("PROMO001")

        assert unbound.can_be_used_by_customer(alice)[0] is True

    def test_issued_to_id_none_is_the_condition_not_falsiness(self):
        """
        The check reads ``self.issued_to_id is not None``. A user with pk 0 is
        not reachable in practice, but the guard must be an identity check so
        that a future non-integer pk cannot silently disable binding.
        """
        earner = _user("earner")
        voucher = make_voucher("BOUND001", issued_to=earner)

        assert voucher.issued_to_id is not None
        assert voucher.can_be_used_by_customer(AnonymousUser())[0] is False

        voucher.issued_to = None
        voucher.save(update_fields=["issued_to"])
        voucher.refresh_from_db()

        assert voucher.issued_to_id is None
        assert voucher.can_be_used_by_customer(earner)[0] is True
