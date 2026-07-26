"""
Characterisation tests for ``vouchers.VoucherRestriction.evaluate``.

Six restriction axes, each combinable with an ``is_inclusive`` flag that
inverts the result (``True`` = must match, ``False`` = must not match). The
evaluator returns ``True`` when the restriction *passes*, i.e. when the
voucher may be used.

Two implementation details worth stating up front, because both are pinned
below and both are easy to break in a refactor:

* ``restriction_value`` is parsed as JSON only when it starts with ``[``;
  otherwise it is comma-split. Both forms are in the wild.
* A restriction whose axis has **no** corresponding context key evaluates to
  ``match = False``. With ``is_inclusive=True`` that fails closed (the
  voucher is refused); with ``is_inclusive=False`` it passes open. So a
  missing context key is not neutral — its effect depends on the flag.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (P1.0)
"""

from datetime import time
from decimal import Decimal

import pytest
from django.contrib.auth.models import Group

from .factories import make_restriction, make_voucher

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.vouchers,
]


@pytest.fixture
def user(db):
    from tests.factories import UserFactory

    return UserFactory(email="buyer@example.com")


@pytest.fixture
def voucher(db):
    return make_voucher("RESTRICT")


# ============================================================
# Axis 1 — user_group
# ============================================================


class TestUserGroupRestriction:
    def test_user_in_the_named_group_passes(self, voucher, user):
        group = Group.objects.create(name="vip")
        user.groups.add(group)
        restriction = make_restriction(voucher, "user_group", "vip")

        assert restriction.evaluate({"user": user}) is True

    def test_user_outside_the_named_group_fails(self, voucher, user):
        Group.objects.create(name="vip")
        restriction = make_restriction(voucher, "user_group", "vip")

        assert restriction.evaluate({"user": user}) is False

    def test_membership_of_any_listed_group_is_enough(self, voucher, user):
        Group.objects.create(name="vip")
        wholesale = Group.objects.create(name="wholesale")
        user.groups.add(wholesale)
        restriction = make_restriction(voucher, "user_group", "vip,wholesale")

        assert restriction.evaluate({"user": user}) is True

    def test_exclusive_flag_bars_members_of_the_group(self, voucher, user):
        """``is_inclusive=False`` turns the list into a blocklist."""
        group = Group.objects.create(name="staff-discount")
        user.groups.add(group)
        restriction = make_restriction(voucher, "user_group", "staff-discount", is_inclusive=False)

        assert restriction.evaluate({"user": user}) is False

    def test_exclusive_flag_admits_non_members(self, voucher, user):
        Group.objects.create(name="staff-discount")
        restriction = make_restriction(voucher, "user_group", "staff-discount", is_inclusive=False)

        assert restriction.evaluate({"user": user}) is True

    def test_missing_user_in_context_fails_an_inclusive_restriction(self, voucher):
        restriction = make_restriction(voucher, "user_group", "vip")

        assert restriction.evaluate({}) is False


# ============================================================
# Axis 2 — user_email_domain
# ============================================================


class TestEmailDomainRestriction:
    def test_matching_domain_passes(self, voucher, user):
        restriction = make_restriction(voucher, "user_email_domain", "example.com")

        assert restriction.evaluate({"user": user}) is True

    def test_non_matching_domain_fails(self, voucher, user):
        restriction = make_restriction(voucher, "user_email_domain", "partner.com")

        assert restriction.evaluate({"user": user}) is False

    def test_domain_comparison_is_case_insensitive(self, voucher, user):
        restriction = make_restriction(voucher, "user_email_domain", "EXAMPLE.COM")

        assert restriction.evaluate({"user": user}) is True

    def test_multiple_domains_are_accepted(self, voucher, user):
        restriction = make_restriction(voucher, "user_email_domain", "partner.com, example.com")

        assert restriction.evaluate({"user": user}) is True

    def test_exclusive_flag_bars_the_listed_domain(self, voucher, user):
        restriction = make_restriction(
            voucher, "user_email_domain", "example.com", is_inclusive=False
        )

        assert restriction.evaluate({"user": user}) is False

    def test_user_without_an_email_fails_an_inclusive_restriction(self, voucher):
        from tests.factories import UserFactory

        user = UserFactory(email="")
        restriction = make_restriction(voucher, "user_email_domain", "example.com")

        assert restriction.evaluate({"user": user}) is False


# ============================================================
# Axis 3 — shipping_country
# ============================================================


class TestShippingCountryRestriction:
    def test_matching_country_passes(self, voucher):
        restriction = make_restriction(voucher, "shipping_country", "US")

        assert restriction.evaluate({"shipping_country": "US"}) is True

    def test_country_comparison_is_case_insensitive(self, voucher):
        restriction = make_restriction(voucher, "shipping_country", "us")

        assert restriction.evaluate({"shipping_country": "Us"}) is True

    def test_non_matching_country_fails(self, voucher):
        restriction = make_restriction(voucher, "shipping_country", "US,CA")

        assert restriction.evaluate({"shipping_country": "GB"}) is False

    def test_any_listed_country_passes(self, voucher):
        restriction = make_restriction(voucher, "shipping_country", "US,CA,GB")

        assert restriction.evaluate({"shipping_country": "CA"}) is True

    def test_exclusive_flag_bars_the_listed_countries(self, voucher):
        """Typical use: a promotion excluded from specific territories."""
        restriction = make_restriction(voucher, "shipping_country", "US,CA", is_inclusive=False)

        assert restriction.evaluate({"shipping_country": "US"}) is False
        assert restriction.evaluate({"shipping_country": "GB"}) is True

    def test_missing_country_fails_an_inclusive_restriction(self, voucher):
        """
        The context key defaults to ``""``, which matches nothing — so an
        inclusive country restriction fails closed when checkout has not yet
        collected an address.
        """
        restriction = make_restriction(voucher, "shipping_country", "US")

        assert restriction.evaluate({}) is False


# ============================================================
# Axis 4 — payment_method
# ============================================================


class TestPaymentMethodRestriction:
    def test_matching_method_passes(self, voucher):
        restriction = make_restriction(voucher, "payment_method", "card")

        assert restriction.evaluate({"payment_method": "card"}) is True

    def test_method_comparison_is_case_insensitive(self, voucher):
        restriction = make_restriction(voucher, "payment_method", "CARD")

        assert restriction.evaluate({"payment_method": "Card"}) is True

    def test_non_matching_method_fails(self, voucher):
        restriction = make_restriction(voucher, "payment_method", "card")

        assert restriction.evaluate({"payment_method": "paypal"}) is False

    def test_exclusive_flag_bars_the_listed_method(self, voucher):
        """Typical use: excluding a high-fee tender from a thin-margin promo."""
        restriction = make_restriction(
            voucher, "payment_method", "cash_on_delivery", is_inclusive=False
        )

        assert restriction.evaluate({"payment_method": "cash_on_delivery"}) is False
        assert restriction.evaluate({"payment_method": "card"}) is True

    def test_missing_method_fails_an_inclusive_restriction(self, voucher):
        restriction = make_restriction(voucher, "payment_method", "card")

        assert restriction.evaluate({}) is False


# ============================================================
# Axis 5 — day_of_week
# ============================================================


class TestDayOfWeekRestriction:
    def test_matching_day_passes(self, voucher):
        restriction = make_restriction(voucher, "day_of_week", "Monday")

        assert restriction.evaluate({"current_day": "Monday"}) is True

    def test_day_comparison_is_case_insensitive(self, voucher):
        restriction = make_restriction(voucher, "day_of_week", "monday")

        assert restriction.evaluate({"current_day": "MONDAY"}) is True

    def test_non_matching_day_fails(self, voucher):
        restriction = make_restriction(voucher, "day_of_week", "Saturday,Sunday")

        assert restriction.evaluate({"current_day": "Wednesday"}) is False

    def test_any_listed_day_passes(self, voucher):
        restriction = make_restriction(voucher, "day_of_week", "Saturday,Sunday")

        assert restriction.evaluate({"current_day": "Sunday"}) is True

    def test_exclusive_flag_bars_the_listed_days(self, voucher):
        restriction = make_restriction(
            voucher, "day_of_week", "Saturday,Sunday", is_inclusive=False
        )

        assert restriction.evaluate({"current_day": "Sunday"}) is False
        assert restriction.evaluate({"current_day": "Monday"}) is True

    def test_absent_current_day_falls_back_to_now(self, voucher):
        """
        With no ``current_day`` the evaluator reads the clock. Passing every
        weekday name makes the assertion deterministic regardless of when the
        suite runs — a test asserting a specific day would be a time bomb.
        """
        every_day = "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday"
        restriction = make_restriction(voucher, "day_of_week", every_day)

        assert restriction.evaluate({}) is True


# ============================================================
# Axis 6 — time_of_day
# ============================================================


class TestTimeOfDayRestriction:
    def test_time_inside_the_window_passes(self, voucher):
        restriction = make_restriction(voucher, "time_of_day", "09:00-17:00")

        assert restriction.evaluate({"current_time": time(12, 30)}) is True

    def test_time_outside_the_window_fails(self, voucher):
        restriction = make_restriction(voucher, "time_of_day", "09:00-17:00")

        assert restriction.evaluate({"current_time": time(18, 0)}) is False

    def test_window_boundaries_are_inclusive_at_both_ends(self, voucher):
        """The comparison is ``start <= t <= end``, so both edges are inside."""
        restriction = make_restriction(voucher, "time_of_day", "09:00-17:00")

        assert restriction.evaluate({"current_time": time(9, 0)}) is True
        assert restriction.evaluate({"current_time": time(17, 0)}) is True

    def test_a_minute_before_the_window_fails(self, voucher):
        restriction = make_restriction(voucher, "time_of_day", "09:00-17:00")

        assert restriction.evaluate({"current_time": time(8, 59)}) is False

    def test_multiple_windows_are_supported(self, voucher):
        """Happy hour twice a day."""
        restriction = make_restriction(voucher, "time_of_day", "09:00-11:00,15:00-17:00")

        assert restriction.evaluate({"current_time": time(10, 0)}) is True
        assert restriction.evaluate({"current_time": time(16, 0)}) is True
        assert restriction.evaluate({"current_time": time(13, 0)}) is False

    def test_exclusive_flag_bars_the_window(self, voucher):
        restriction = make_restriction(voucher, "time_of_day", "00:00-06:00", is_inclusive=False)

        assert restriction.evaluate({"current_time": time(3, 0)}) is False
        assert restriction.evaluate({"current_time": time(12, 0)}) is True

    def test_a_window_that_wraps_past_midnight_never_matches(self, voucher):
        """
        Quirk, pinned: ``22:00-02:00`` is evaluated as ``22:00 <= t <= 02:00``,
        which is unsatisfiable. Overnight windows silently match nothing
        rather than erroring, so a merchant configuring a late-night promo
        gets no discount and no warning.
        """
        restriction = make_restriction(voucher, "time_of_day", "22:00-02:00")

        assert restriction.evaluate({"current_time": time(23, 0)}) is False
        assert restriction.evaluate({"current_time": time(1, 0)}) is False

    def test_malformed_window_is_skipped_without_raising(self, voucher):
        """A bad entry is swallowed by the parser and simply never matches."""
        restriction = make_restriction(voucher, "time_of_day", "not-a-time")

        assert restriction.evaluate({"current_time": time(12, 0)}) is False

    def test_malformed_window_does_not_prevent_a_valid_one_from_matching(self, voucher):
        restriction = make_restriction(voucher, "time_of_day", "nonsense,09:00-17:00")

        assert restriction.evaluate({"current_time": time(12, 0)}) is True


# ============================================================
# restriction_value parsing
# ============================================================


class TestRestrictionValueParsing:
    """``restriction_value`` accepts a JSON array or a comma-separated string."""

    def test_json_array_form_is_parsed(self, voucher):
        restriction = make_restriction(voucher, "shipping_country", '["US", "CA"]')

        assert restriction.evaluate({"shipping_country": "CA"}) is True

    def test_comma_separated_form_is_parsed(self, voucher):
        restriction = make_restriction(voucher, "shipping_country", "US,CA")

        assert restriction.evaluate({"shipping_country": "CA"}) is True

    def test_surrounding_whitespace_is_stripped(self, voucher):
        restriction = make_restriction(voucher, "shipping_country", "  US ,  CA  ")

        assert restriction.evaluate({"shipping_country": "CA"}) is True

    def test_single_value_needs_no_separator(self, voucher):
        restriction = make_restriction(voucher, "shipping_country", "US")

        assert restriction.evaluate({"shipping_country": "US"}) is True

    def test_malformed_json_array_falls_back_to_comma_splitting(self, voucher):
        """
        A value starting with ``[`` that is not valid JSON is comma-split
        instead of raising. The brackets then survive into the compared
        token, so ``["US"`` does not match ``US``.
        """
        restriction = make_restriction(voucher, "shipping_country", '["US"')

        assert restriction.evaluate({"shipping_country": "US"}) is False


# ============================================================
# Integration with can_be_used_by_customer
# ============================================================


class TestRestrictionsViaCanBeUsedByCustomer:
    """
    ``can_be_used_by_customer`` runs restrictions only when a ``context`` dict
    is supplied — and every restriction must pass for the voucher to be usable.
    """

    def test_context_is_required_for_restrictions_to_run_at_all(self, voucher, user):
        """
        Quirk, pinned: with ``context=None`` restrictions are skipped entirely.
        A caller that forgets to pass context bypasses every rule the
        merchant configured.
        """
        make_restriction(voucher, "shipping_country", "US")

        can_use, _message = voucher.can_be_used_by_customer(user)

        assert can_use is True

    def test_a_failing_restriction_blocks_the_voucher(self, voucher, user):
        make_restriction(voucher, "shipping_country", "US")

        can_use, message = voucher.can_be_used_by_customer(user, context={"shipping_country": "GB"})

        assert can_use is False
        assert "restrictions" in str(message)

    def test_a_passing_restriction_allows_the_voucher(self, voucher, user):
        make_restriction(voucher, "shipping_country", "US")

        can_use, _message = voucher.can_be_used_by_customer(
            user, context={"shipping_country": "US"}
        )

        assert can_use is True

    def test_all_restrictions_must_pass(self, voucher, user):
        """Restrictions are ANDed — one failure is enough to refuse."""
        make_restriction(voucher, "shipping_country", "US")
        make_restriction(voucher, "payment_method", "card")

        allowed, _message = voucher.can_be_used_by_customer(
            user, context={"shipping_country": "US", "payment_method": "card"}
        )
        refused, _message = voucher.can_be_used_by_customer(
            user, context={"shipping_country": "US", "payment_method": "paypal"}
        )

        assert allowed is True
        assert refused is False

    def test_the_user_is_injected_into_the_context_automatically(self, voucher, user):
        """
        Callers need not put ``user`` in the context — ``can_be_used_by_customer``
        adds it, so user-scoped axes work with a context that only carries
        checkout facts.
        """
        make_restriction(voucher, "user_email_domain", "example.com")

        can_use, _message = voucher.can_be_used_by_customer(
            user, context={"shipping_country": "US"}
        )

        assert can_use is True

    def test_an_explicit_user_in_the_context_is_not_overwritten(self, voucher, user):
        """
        ``setdefault`` is used, so a caller may deliberately evaluate against
        a different user than the one being checked.
        """
        from tests.factories import UserFactory

        other = UserFactory(email="buyer@partner.com")
        make_restriction(voucher, "user_email_domain", "partner.com")

        can_use, _message = voucher.can_be_used_by_customer(user, context={"user": other})

        assert can_use is True

    def test_restrictions_run_after_the_cheaper_eligibility_checks(self, voucher, user):
        """
        An invalid voucher is refused before any restriction is evaluated, so
        the message reflects validity rather than restrictions.
        """
        voucher.is_active = False
        voucher.save()
        make_restriction(voucher, "shipping_country", "US")

        can_use, message = voucher.can_be_used_by_customer(user, context={"shipping_country": "US"})

        assert can_use is False
        assert "not valid" in str(message)

    def test_restrictions_combine_with_min_order_value(self, voucher, user):
        from djmoney.money import Money

        voucher.min_order_value = Money(Decimal("50.00"), "USD")
        voucher.save()
        make_restriction(voucher, "shipping_country", "US")

        can_use, message = voucher.can_be_used_by_customer(
            user,
            order_total=Money(Decimal("10.00"), "USD"),
            context={"shipping_country": "US"},
        )

        assert can_use is False
        assert "minimum" in str(message)
