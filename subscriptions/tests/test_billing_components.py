"""
Recurring-cycle pricing components: add-ons and discounts folded into
``SubscriptionManager.process_billing_cycle``.

Before this, the models declared per-cycle add-ons and subscription discounts (with
once/forever/repeating durations and remaining-cycle semantics) but the fallback
billing engine never applied them — every renewal charged the bare plan price and
``BillingCycleLog.addons_amount`` / ``discount_amount`` stayed zero. These pin:
the amounts fold into the charge and the log breakdown, discounts are *consumed*
only after a charge succeeds, and a currency-mismatched add-on is skipped rather
than silently mixed.

setup_fee / one-time add-ons are a subscription-START (checkout) charge, not a
recurring one — see the skipped test at the end.
"""

from decimal import Decimal

import pytest
from djmoney.money import Money

from subscriptions.models import (
    CustomerSubscriptionAddon,
    PlanAddon,
    SubscriptionDiscount,
)
from tests.factories import (
    CustomerSubscriptionFactory,
    PaymentProviderAccountFactory,
    PaymentTokenFactory,
    ProductFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _manager_for(subscription):
    from subscriptions.manager import SubscriptionManager

    return SubscriptionManager(subscription.payment_provider_account)


def _cycle_currency(subscription):
    price = subscription.pricing_tier.calculate_price(subscription.product, subscription.variant)
    return str(price.currency)


def _add_addon(subscription, amount, *, frequency="per_cycle", quantity=1, currency=None):
    currency = currency or _cycle_currency(subscription)
    addon = PlanAddon.objects.create(
        plan=subscription.plan,
        name="Priority Support",
        price=Money(Decimal(amount), currency),
        billing_frequency=frequency,
    )
    return CustomerSubscriptionAddon.objects.create(
        subscription=subscription, addon=addon, quantity=quantity, is_active=True
    )


def _add_discount(subscription, **kwargs):
    kwargs.setdefault("discount_type", "percentage")
    kwargs.setdefault("value", Decimal("10.00"))
    kwargs.setdefault("duration_type", "forever")
    kwargs.setdefault("is_active", True)
    return SubscriptionDiscount.objects.create(subscription=subscription, **kwargs)


class TestAddons:
    def test_per_cycle_addon_increases_the_charge_and_is_recorded(self):
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        _add_addon(sub, "5.00", quantity=2)  # 2 × 5.00 = 10.00

        log = _manager_for(sub).process_billing_cycle(sub)

        assert log.status == "successful"
        assert log.addons_amount == Money(Decimal("10.00"), log.base_amount.currency)
        assert log.total_amount == log.base_amount + Money(
            Decimal("10.00"), log.base_amount.currency
        )

    def test_one_time_addons_are_not_charged_per_cycle(self):
        # one_time add-ons are a start charge, not recurring — excluded here.
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        _add_addon(sub, "9.00", frequency="one_time")

        log = _manager_for(sub).process_billing_cycle(sub)

        assert log.addons_amount.amount == Decimal("0.00")
        assert log.total_amount == log.base_amount

    def test_inactive_addon_is_not_charged(self):
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        active = _add_addon(sub, "5.00")
        active.is_active = False
        active.save(update_fields=["is_active"])

        log = _manager_for(sub).process_billing_cycle(sub)
        assert log.addons_amount.amount == Decimal("0.00")

    def test_currency_mismatched_addon_is_skipped_never_mixed(self):
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        other = "EUR" if _cycle_currency(sub) != "EUR" else "GBP"
        _add_addon(sub, "5.00", currency=other)

        log = _manager_for(sub).process_billing_cycle(sub)
        # Skipped, not summed into a differently-currencied cycle.
        assert log.addons_amount.amount == Decimal("0.00")
        assert log.total_amount == log.base_amount


class TestDiscounts:
    def test_a_forever_discount_reduces_every_charge_and_never_deactivates(self):
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        discount = _add_discount(sub, duration_type="forever", value=Decimal("10.00"))

        log = _manager_for(sub).process_billing_cycle(sub)

        expected = (log.base_amount.amount * Decimal("0.10")).quantize(Decimal("0.01"))
        assert log.discount_amount.amount == expected
        assert log.total_amount.amount == log.base_amount.amount - expected
        discount.refresh_from_db()
        assert discount.is_active is True  # forever is never consumed

    def test_a_once_discount_is_consumed_after_a_successful_cycle(self):
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        discount = _add_discount(sub, duration_type="once")

        _manager_for(sub).process_billing_cycle(sub)

        discount.refresh_from_db()
        assert discount.is_active is False

    def test_a_repeating_discount_decrements_remaining_cycles(self):
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        discount = _add_discount(
            sub, duration_type="repeating", duration_months=3, remaining_cycles=3
        )

        _manager_for(sub).process_billing_cycle(sub)

        discount.refresh_from_db()
        assert discount.remaining_cycles == 2
        assert discount.is_active is True

    def test_a_repeating_discount_deactivates_on_its_last_cycle(self):
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        discount = _add_discount(sub, duration_type="repeating", remaining_cycles=1)

        _manager_for(sub).process_billing_cycle(sub)

        discount.refresh_from_db()
        assert discount.remaining_cycles == 0
        assert discount.is_active is False

    def test_a_fixed_amount_discount_cannot_reduce_the_charge_below_zero(self):
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        _add_discount(sub, discount_type="fixed_amount", value=Decimal("100000.00"))

        log = _manager_for(sub).process_billing_cycle(sub)

        # Discount is capped at the base; the charge floors at zero, never negative.
        assert log.discount_amount.amount == log.base_amount.amount
        assert log.total_amount.amount == Decimal("0.00")
        assert log.total_amount.amount >= Decimal("0.00")

    def test_a_percentage_discount_is_quantized_to_the_minor_unit(self):
        # 10% of a 9.99 base is 0.999 — it must land on the ledger and the card
        # as a 2-decimal amount, never a sub-cent value the gateway can't take.
        from decimal import ROUND_HALF_UP

        sub = CustomerSubscriptionFactory(
            due=True, billing_cycle_count=0, product=ProductFactory(price=Decimal("9.99"))
        )
        _add_discount(sub, duration_type="forever", value=Decimal("10.00"))

        log = _manager_for(sub).process_billing_cycle(sub)

        base = log.base_amount.amount
        expected = (base * Decimal("0.10")).quantize(Decimal("0.01"), ROUND_HALF_UP)
        assert log.discount_amount.amount == expected
        # The charged total is exactly base - discount, at 2 decimals, no residue.
        assert log.total_amount.amount == base - expected
        assert log.total_amount.amount == log.total_amount.amount.quantize(Decimal("0.01"))

    def test_multiple_percentage_discounts_sum_against_base_not_compound(self):
        # Two 10% discounts take 20% off the base, not 19% (compounding on the
        # already-discounted remainder would under-apply stacked discounts).
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        _add_discount(sub, duration_type="forever", value=Decimal("10.00"))
        _add_discount(sub, duration_type="forever", value=Decimal("10.00"))

        log = _manager_for(sub).process_billing_cycle(sub)

        each = (log.base_amount.amount * Decimal("0.10")).quantize(Decimal("0.01"))
        assert log.discount_amount.amount == each * 2
        assert log.total_amount.amount == log.base_amount.amount - each * 2

    def test_a_zero_value_discount_is_not_consumed(self):
        # A 0% coupon reduces nothing this cycle, so a limited once/repeating
        # discount must not be burned for a cycle it gave no benefit on.
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        discount = _add_discount(
            sub, duration_type="once", discount_type="percentage", value=Decimal("0.00")
        )

        log = _manager_for(sub).process_billing_cycle(sub)

        assert log.discount_amount.amount == Decimal("0.00")
        discount.refresh_from_db()
        assert discount.is_active is True  # not consumed — gave no benefit

    def test_a_failed_charge_does_not_consume_the_discount(self):
        # The customer must not lose a discount cycle for a charge that never
        # went through — consumption is strictly post-success.
        user = UserFactory()
        declining = PaymentProviderAccountFactory(declining=True)
        token = PaymentTokenFactory(user=user, provider_account=declining)
        sub = CustomerSubscriptionFactory(
            due=True,
            billing_cycle_count=0,
            user=user,
            payment_token=token,
            payment_provider_account=declining,
        )
        discount = _add_discount(sub, duration_type="once")

        log = _manager_for(sub).process_billing_cycle(sub)

        assert log.status == "failed"
        discount.refresh_from_db()
        assert discount.is_active is True  # not burned
        # It was still recorded on the (failed) log for transparency.
        assert log.discount_amount.amount > Decimal("0.00")

    def test_a_recovered_retry_consumes_the_discount_that_priced_the_log(self):
        # A discounted cycle that fails then recovers via retry MUST burn the
        # once/repeating discount recorded on the log — the failed attempt didn't,
        # and the recovery must, or it re-applies next cycle and undercharges.
        from subscriptions.tasks import retry_billing_cycle
        from tests.factories import BillingCycleLogFactory

        sub = CustomerSubscriptionFactory(billing_cycle_count=0)  # succeeding provider
        discount = _add_discount(sub, duration_type="once")
        currency = _cycle_currency(sub)
        log = BillingCycleLogFactory(
            subscription=sub,
            cycle_number=1,
            failed=True,
            retry_count=0,
            max_retries=3,
            base_amount=Money(Decimal("10.00"), currency),
            total_amount=Money(Decimal("9.00"), currency),
            # The failed attempt recorded which discount priced the cycle.
            billing_breakdown={"applied_discount_ids": [str(discount.id)]},
        )

        result = retry_billing_cycle(log.id)

        assert result["status"] == "successful"
        discount.refresh_from_db()
        assert discount.is_active is False  # burned by the recovery, not left live

    def test_consuming_a_cycle_twice_burns_a_repeating_discount_only_once(self):
        # Idempotent per log: a second recovery of the same cycle (a retry racing
        # the dunning sweep) must not double-decrement remaining_cycles.
        from tests.factories import BillingCycleLogFactory

        sub = CustomerSubscriptionFactory(billing_cycle_count=0)
        discount = _add_discount(sub, duration_type="repeating", remaining_cycles=3)
        currency = _cycle_currency(sub)
        log = BillingCycleLogFactory(
            subscription=sub,
            cycle_number=1,
            base_amount=Money(Decimal("10.00"), currency),
            total_amount=Money(Decimal("9.00"), currency),
            billing_breakdown={"applied_discount_ids": [str(discount.id)]},
        )
        mgr = _manager_for(sub)

        mgr.consume_cycle_discounts(sub, log)
        mgr.consume_cycle_discounts(sub, log)  # second call is a no-op (marker set)

        discount.refresh_from_db()
        assert discount.remaining_cycles == 2  # burned exactly once

    def test_a_discount_added_after_the_failure_is_not_burned_on_retry(self):
        # Recovery burns only the discounts the log recorded — a discount added to
        # the subscription AFTER the failed attempt never priced this cycle and
        # must not be consumed (the retry charged the log's stored amount).
        from subscriptions.tasks import retry_billing_cycle
        from tests.factories import BillingCycleLogFactory

        sub = CustomerSubscriptionFactory(billing_cycle_count=0)
        currency = _cycle_currency(sub)
        log = BillingCycleLogFactory(
            subscription=sub,
            cycle_number=1,
            failed=True,
            retry_count=0,
            max_retries=3,
            base_amount=Money(Decimal("10.00"), currency),
            total_amount=Money(Decimal("10.00"), currency),
            billing_breakdown={"applied_discount_ids": []},  # priced with no discount
        )
        late = _add_discount(sub, duration_type="once")  # added only now

        result = retry_billing_cycle(log.id)

        assert result["status"] == "successful"
        late.refresh_from_db()
        assert late.is_active is True  # never priced this cycle — not consumed


class TestAddonAndDiscountTogether:
    def test_addon_and_discount_combine_in_the_cycle_total(self):
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        _add_addon(sub, "20.00")
        _add_discount(sub, duration_type="forever", value=Decimal("10.00"))  # 10% of base

        log = _manager_for(sub).process_billing_cycle(sub)

        discount = (log.base_amount.amount * Decimal("0.10")).quantize(Decimal("0.01"))
        expected_total = log.base_amount.amount + Decimal("20.00") - discount
        assert log.total_amount.amount == expected_total
        assert log.addons_amount.amount == Decimal("20.00")
        assert log.discount_amount.amount == discount


class TestRenewalOrderConsistency:
    """The paid renewal Order must stay internally consistent AND match the charge
    once add-ons/discounts are in play — subtotal - discount == total == amount_paid
    == the cycle charge, and the fulfilment line total == subtotal."""

    def test_renewal_order_reconciles_to_the_charge_with_an_addon(self):
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        _add_addon(sub, "20.00")
        _add_discount(sub, duration_type="forever", value=Decimal("10.00"))

        log = _manager_for(sub).process_billing_cycle(sub)
        order = log.order
        assert order is not None

        # Matched to the charge, and internally consistent.
        assert order.total_amount == log.total_amount
        assert order.amount_paid == log.total_amount
        assert order.subtotal.amount == log.base_amount.amount + log.addons_amount.amount
        assert (order.subtotal.amount - order.discount_amount.amount) == order.total_amount.amount
        # The single fulfilment line carries the gross (product + add-ons).
        item = order.items.first()
        assert item.total_price.amount == order.subtotal.amount

    def test_a_fully_discounted_cycle_creates_a_zero_total_renewal_order(self):
        # A $0 charge (fully discounted) must produce a $0 renewal order — a zero
        # Money is falsy, so the charged fallback must use an explicit None check,
        # not `or gross`.
        sub = CustomerSubscriptionFactory(due=True, billing_cycle_count=0)
        _add_discount(sub, discount_type="fixed_amount", value=Decimal("100000.00"))

        log = _manager_for(sub).process_billing_cycle(sub)
        assert log.total_amount.amount == Decimal("0.00")

        order = log.order
        assert order is not None
        assert order.total_amount.amount == Decimal("0.00")
        assert order.amount_paid.amount == Decimal("0.00")
        assert (order.subtotal.amount - order.discount_amount.amount) == Decimal("0.00")


@pytest.mark.skip(
    reason="charge_setup_fee is planned-not-built: setup_fee (and one_time PlanAddons) "
    "are a subscription-START charge that belongs in the checkout that charges cycle 1 "
    "— a surface still being hardened. The recurring engine deliberately does NOT charge "
    "them (it would bill every cycle). See the setup_fee note in subscriptions/models.py."
)
def test_charge_setup_fee_not_yet_implemented():
    # Intended contract: the one-time setup_fee (and one_time add-ons) are charged
    # exactly once, at subscription start, alongside the first cycle — not by the
    # recurring engine. No wired charge path exists yet.
    raise AssertionError("setup fee / one-time add-on charging is not implemented")
