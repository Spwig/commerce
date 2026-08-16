"""
WalletService — store credit ledger safety.

The wallet app shipped with zero tests while handling real customer money.
This suite pins the P2.1 hardening of ``WalletService``, and in particular the
defect that motivated it:

    ``credit()`` and ``debit()`` added the incoming *amount* to the stored
    balance and then re-stamped the wallet with the incoming *currency*.
    Crediting €50 to a wallet holding $100 produced **€150** — the customer's
    dollars silently became euros, with no error and no log entry.

The fix is a refusal, not a conversion: a wallet holds one currency, and
mixing requires an explicit debit + credit pair so both movements land on the
ledger. Every cross-currency test below therefore asserts the *balance and
currency after the failed call*, not merely that an exception was raised — a
service that raised but had already written would pass the weaker assertion
while still corrupting the books.

Also pinned: the removal of the ``max(balance - amount, 0)`` clamp in
``reverse_transaction``, which silently destroyed the difference when
reversing a credit the customer had already spent.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R2, P2.1)
"""

from decimal import Decimal

import pytest
from djmoney.money import Money

from tests.factories import UserFactory
from wallet.models import CustomerWallet, WalletTransaction
from wallet.services import (
    InsufficientBalance,
    WalletCurrencyMismatch,
    WalletFrozen,
    WalletService,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.wallet,
]


# ============================================================
# Helpers
# ============================================================


def _wallet_for(user, amount="0.00", currency="USD", is_active=True):
    """
    Build a wallet holding a known balance in a known currency.

    ``CustomerWallet`` MoneyFields all default to USD, so a wallet that is
    meant to hold euros has to be stamped explicitly — including the lifetime
    counters, which are separate MoneyFields and would otherwise stay USD and
    make the accumulation assertions ambiguous.
    """
    wallet = WalletService.get_or_create_wallet(user)
    wallet.available_balance = Money(Decimal(amount), currency)
    wallet.lifetime_credited = Money(Decimal("0.00"), currency)
    wallet.lifetime_used = Money(Decimal("0.00"), currency)
    wallet.is_active = is_active
    wallet.save()
    return wallet


def _reread(wallet):
    """Re-read from the database — never trust the in-memory copy after a call."""
    return CustomerWallet.objects.get(pk=wallet.pk)


# ============================================================
# get_or_create_wallet
# ============================================================


class TestGetOrCreateWallet:
    def test_creates_a_wallet_on_first_call(self):
        user = UserFactory()
        assert not CustomerWallet.objects.filter(customer=user).exists()

        wallet = WalletService.get_or_create_wallet(user)

        assert wallet.pk is not None
        assert wallet.customer_id == user.pk
        assert wallet.available_balance == Money(Decimal("0.00"), "USD")

    def test_is_idempotent(self):
        user = UserFactory()

        first = WalletService.get_or_create_wallet(user)
        second = WalletService.get_or_create_wallet(user)

        assert first.pk == second.pk
        assert CustomerWallet.objects.filter(customer=user).count() == 1, (
            "A second call created a second wallet. The customer's balance "
            "would then depend on which row a given code path happened to load."
        )

    def test_does_not_reset_an_existing_balance(self):
        user = UserFactory()
        _wallet_for(user, "75.00")

        wallet = WalletService.get_or_create_wallet(user)

        assert wallet.available_balance == Money(Decimal("75.00"), "USD")


# ============================================================
# credit — same currency
# ============================================================


class TestCreditSameCurrency:
    def test_a_single_credit_lands_on_the_balance(self):
        user = UserFactory()
        _wallet_for(user, "0.00")

        txn = WalletService.credit(
            user, Decimal("50.00"), "USD", WalletTransaction.SOURCE_REFERRAL, "Referral reward"
        )

        assert _reread(txn.wallet).available_balance == Money(Decimal("50.00"), "USD")
        assert txn.transaction_type == WalletTransaction.TYPE_CREDIT
        assert txn.amount == Money(Decimal("50.00"), "USD")
        assert txn.status == WalletTransaction.STATUS_COMPLETED

    def test_credits_accumulate(self):
        user = UserFactory()
        wallet = _wallet_for(user, "10.00")

        WalletService.credit(
            user, Decimal("15.00"), "USD", WalletTransaction.SOURCE_PROMOTION, "Promo"
        )
        WalletService.credit(
            user, Decimal("25.50"), "USD", WalletTransaction.SOURCE_REFUND, "Refund"
        )

        assert _reread(wallet).available_balance == Money(Decimal("50.50"), "USD")

    def test_lifetime_credited_accumulates_and_lifetime_used_does_not_move(self):
        user = UserFactory()
        wallet = _wallet_for(user, "0.00")

        WalletService.credit(
            user, Decimal("20.00"), "USD", WalletTransaction.SOURCE_MANUAL, "Goodwill"
        )
        WalletService.credit(
            user, Decimal("30.00"), "USD", WalletTransaction.SOURCE_MANUAL, "Goodwill again"
        )

        wallet = _reread(wallet)
        assert wallet.lifetime_credited == Money(Decimal("50.00"), "USD")
        assert wallet.lifetime_used == Money(Decimal("0.00"), "USD")

    def test_last_credited_at_is_stamped(self):
        user = UserFactory()
        wallet = _wallet_for(user, "0.00")
        assert wallet.last_credited_at is None

        WalletService.credit(user, Decimal("5.00"), "USD", WalletTransaction.SOURCE_MANUAL, "Stamp")

        assert _reread(wallet).last_credited_at is not None

    def test_credited_by_is_recorded_for_manual_adjustments(self):
        user = UserFactory()
        staff = UserFactory(staff=True)
        _wallet_for(user, "0.00")

        txn = WalletService.credit(
            user,
            Decimal("10.00"),
            "USD",
            WalletTransaction.SOURCE_MANUAL,
            "Manual credit",
            created_by=staff,
        )

        assert txn.created_by_id == staff.pk

    @pytest.mark.parametrize("bad_amount", [Decimal("0.00"), Decimal("-1.00")])
    def test_a_non_positive_credit_is_refused(self, bad_amount):
        user = UserFactory()
        wallet = _wallet_for(user, "40.00")

        with pytest.raises(ValueError):
            WalletService.credit(
                user, bad_amount, "USD", WalletTransaction.SOURCE_MANUAL, "Nonsense"
            )

        assert _reread(wallet).available_balance == Money(Decimal("40.00"), "USD")
        assert WalletTransaction.objects.filter(wallet=wallet).count() == 0


# ============================================================
# debit — same currency
# ============================================================


class TestDebitSameCurrency:
    def test_a_debit_deducts(self):
        user = UserFactory()
        wallet = _wallet_for(user, "100.00")

        txn = WalletService.debit(
            user, Decimal("30.00"), "USD", WalletTransaction.SOURCE_ORDER, "Order payment"
        )

        assert _reread(wallet).available_balance == Money(Decimal("70.00"), "USD")
        assert txn.transaction_type == WalletTransaction.TYPE_DEBIT
        assert txn.amount == Money(Decimal("30.00"), "USD"), (
            "The ledger amount must stay positive; transaction_type carries the "
            "direction. A negative amount here would double-count on any sum()."
        )

    def test_debiting_the_whole_balance_is_allowed(self):
        user = UserFactory()
        wallet = _wallet_for(user, "42.00")

        WalletService.debit(
            user, Decimal("42.00"), "USD", WalletTransaction.SOURCE_ORDER, "Full spend"
        )

        assert _reread(wallet).available_balance == Money(Decimal("0.00"), "USD")

    def test_debiting_more_than_the_balance_is_refused(self):
        user = UserFactory()
        wallet = _wallet_for(user, "20.00")

        with pytest.raises(InsufficientBalance):
            WalletService.debit(
                user, Decimal("20.01"), "USD", WalletTransaction.SOURCE_ORDER, "Overspend"
            )

        assert _reread(wallet).available_balance == Money(Decimal("20.00"), "USD")
        assert WalletTransaction.objects.filter(wallet=wallet).count() == 0

    def test_lifetime_used_accumulates_and_lifetime_credited_does_not_move(self):
        user = UserFactory()
        wallet = _wallet_for(user, "100.00")

        WalletService.debit(user, Decimal("10.00"), "USD", WalletTransaction.SOURCE_ORDER, "Spend")
        WalletService.debit(
            user, Decimal("15.00"), "USD", WalletTransaction.SOURCE_ORDER, "Spend again"
        )

        wallet = _reread(wallet)
        assert wallet.lifetime_used == Money(Decimal("25.00"), "USD")
        assert wallet.lifetime_credited == Money(Decimal("0.00"), "USD")

    @pytest.mark.parametrize("bad_amount", [Decimal("0.00"), Decimal("-5.00")])
    def test_a_non_positive_debit_is_refused(self, bad_amount):
        user = UserFactory()
        wallet = _wallet_for(user, "40.00")

        with pytest.raises(ValueError):
            WalletService.debit(user, bad_amount, "USD", WalletTransaction.SOURCE_ORDER, "Nonsense")

        assert _reread(wallet).available_balance == Money(Decimal("40.00"), "USD")

    def test_a_negative_debit_cannot_be_used_to_top_up(self):
        """
        Without the positive-amount guard, ``debit(-100)`` passes the
        sufficiency check trivially and *adds* to the balance — a free top-up
        reachable from anywhere that lets a customer influence an amount.
        """
        user = UserFactory()
        wallet = _wallet_for(user, "10.00")

        with pytest.raises(ValueError):
            WalletService.debit(
                user, Decimal("-100.00"), "USD", WalletTransaction.SOURCE_ORDER, "Exploit"
            )

        assert _reread(wallet).available_balance == Money(Decimal("10.00"), "USD")


# ============================================================
# Currency safety — the $100 + €50 = €150 defect
# ============================================================


class TestCurrencyIsNeverMixed:
    def test_a_cross_currency_credit_raises(self):
        user = UserFactory()
        _wallet_for(user, "100.00", "USD")

        with pytest.raises(WalletCurrencyMismatch):
            WalletService.credit(
                user, Decimal("50.00"), "EUR", WalletTransaction.SOURCE_REFUND, "EUR refund"
            )

    def test_a_cross_currency_credit_leaves_the_balance_completely_untouched(self):
        """
        The original defect: $100 + €50 became €150. Both the number and the
        currency were wrong, so both are asserted here.
        """
        user = UserFactory()
        wallet = _wallet_for(user, "100.00", "USD")

        with pytest.raises(WalletCurrencyMismatch):
            WalletService.credit(
                user, Decimal("50.00"), "EUR", WalletTransaction.SOURCE_REFUND, "EUR refund"
            )

        wallet = _reread(wallet)
        assert wallet.available_balance == Money(Decimal("100.00"), "USD"), (
            f"Balance is {wallet.available_balance}, expected USD 100.00. "
            "Crediting EUR onto a USD wallet moved the balance."
        )
        assert str(wallet.available_balance.currency) == "USD", (
            "The wallet was re-stamped with the incoming currency. This is the "
            "exact mechanism that turned $100 into €150."
        )
        assert wallet.lifetime_credited == Money(Decimal("0.00"), "USD")
        assert WalletTransaction.objects.filter(wallet=wallet).count() == 0, (
            "A ledger row was written for a movement that was refused."
        )

    def test_a_cross_currency_debit_leaves_the_balance_completely_untouched(self):
        user = UserFactory()
        wallet = _wallet_for(user, "100.00", "USD")

        with pytest.raises(WalletCurrencyMismatch):
            WalletService.debit(
                user, Decimal("50.00"), "EUR", WalletTransaction.SOURCE_ORDER, "EUR spend"
            )

        wallet = _reread(wallet)
        assert wallet.available_balance == Money(Decimal("100.00"), "USD")
        assert str(wallet.available_balance.currency) == "USD"
        assert wallet.lifetime_used == Money(Decimal("0.00"), "USD")
        assert WalletTransaction.objects.filter(wallet=wallet).count() == 0

    def test_a_cross_currency_debit_fails_as_a_mismatch_not_as_insufficient_funds(self):
        """
        Comparing a EUR amount against a USD balance is meaningless, so the
        currency check must run *before* the sufficiency check.

        Ordering them the other way round is worse than cosmetic: the customer
        is told "insufficient balance" for a wallet that holds plenty, and — in
        the case below — a €5 debit against $100 would have *succeeded*,
        deducting five dollars to settle a five euro obligation.
        """
        user = UserFactory()
        wallet = _wallet_for(user, "100.00", "USD")

        with pytest.raises(WalletCurrencyMismatch):
            WalletService.debit(
                user, Decimal("5.00"), "EUR", WalletTransaction.SOURCE_ORDER, "Small EUR spend"
            )

        assert _reread(wallet).available_balance == Money(Decimal("100.00"), "USD")

    def test_insufficient_balance_is_not_raised_for_a_currency_mismatch(self):
        """``InsufficientBalance`` here would send the caller down a top-up path."""
        user = UserFactory()
        _wallet_for(user, "1.00", "USD")

        with pytest.raises(WalletCurrencyMismatch):
            # 500 EUR against a 1 USD balance: insufficient *and* mismatched.
            # The mismatch is the true reason and must win.
            WalletService.debit(
                user, Decimal("500.00"), "EUR", WalletTransaction.SOURCE_ORDER, "Both wrong"
            )

    def test_a_eur_wallet_accepts_eur_and_refuses_usd(self):
        """The rule is symmetric — it is not "USD is special"."""
        user = UserFactory()
        wallet = _wallet_for(user, "100.00", "EUR")

        WalletService.credit(
            user, Decimal("50.00"), "EUR", WalletTransaction.SOURCE_PROMOTION, "EUR promo"
        )
        assert _reread(wallet).available_balance == Money(Decimal("150.00"), "EUR")

        with pytest.raises(WalletCurrencyMismatch):
            WalletService.credit(
                user, Decimal("50.00"), "USD", WalletTransaction.SOURCE_PROMOTION, "USD promo"
            )

        assert _reread(wallet).available_balance == Money(Decimal("150.00"), "EUR")


# ============================================================
# Frozen wallets
# ============================================================


class TestFrozenWallet:
    def test_credit_is_refused_on_an_inactive_wallet(self):
        user = UserFactory()
        wallet = _wallet_for(user, "10.00", is_active=False)

        with pytest.raises(WalletFrozen):
            WalletService.credit(
                user, Decimal("5.00"), "USD", WalletTransaction.SOURCE_MANUAL, "Credit"
            )

        assert _reread(wallet).available_balance == Money(Decimal("10.00"), "USD")

    def test_debit_is_refused_on_an_inactive_wallet(self):
        user = UserFactory()
        wallet = _wallet_for(user, "10.00", is_active=False)

        with pytest.raises(WalletFrozen):
            WalletService.debit(
                user, Decimal("5.00"), "USD", WalletTransaction.SOURCE_ORDER, "Spend"
            )

        assert _reread(wallet).available_balance == Money(Decimal("10.00"), "USD")

    def test_unfreezing_restores_normal_operation(self):
        """Negative control: the refusal is caused by the flag, nothing else."""
        user = UserFactory()
        wallet = _wallet_for(user, "10.00", is_active=False)

        wallet.is_active = True
        wallet.save(update_fields=["is_active"])

        WalletService.debit(user, Decimal("5.00"), "USD", WalletTransaction.SOURCE_ORDER, "Spend")
        assert _reread(wallet).available_balance == Money(Decimal("5.00"), "USD")


# ============================================================
# balance_after ledger integrity
# ============================================================


class TestBalanceAfterSnapshots:
    def test_balance_after_matches_the_wallet_after_each_movement(self):
        """
        ``balance_after`` is what reconciliation and customer-facing statements
        read. If it drifts from the wallet, the ledger stops being evidence of
        anything.
        """
        user = UserFactory()
        wallet = _wallet_for(user, "0.00")

        movements = [
            ("credit", Decimal("100.00"), Decimal("100.00")),
            ("debit", Decimal("30.00"), Decimal("70.00")),
            ("credit", Decimal("5.50"), Decimal("75.50")),
            ("debit", Decimal("75.50"), Decimal("0.00")),
        ]

        for kind, amount, expected in movements:
            if kind == "credit":
                txn = WalletService.credit(
                    user, amount, "USD", WalletTransaction.SOURCE_MANUAL, f"{kind} {amount}"
                )
            else:
                txn = WalletService.debit(
                    user, amount, "USD", WalletTransaction.SOURCE_ORDER, f"{kind} {amount}"
                )

            live = _reread(wallet).available_balance
            assert txn.balance_after == Money(expected, "USD")
            assert txn.balance_after == live, (
                f"After {kind} of {amount}: ledger says {txn.balance_after}, wallet says {live}."
            )

    def test_the_ledger_reconciles_to_the_balance(self):
        user = UserFactory()
        wallet = _wallet_for(user, "0.00")

        WalletService.credit(
            user, Decimal("80.00"), "USD", WalletTransaction.SOURCE_REFERRAL, "Reward"
        )
        WalletService.debit(user, Decimal("25.00"), "USD", WalletTransaction.SOURCE_ORDER, "Spend")

        credited = sum(
            (
                t.amount.amount
                for t in WalletTransaction.objects.filter(
                    wallet=wallet, transaction_type=WalletTransaction.TYPE_CREDIT
                )
            ),
            Decimal("0"),
        )
        debited = sum(
            (
                t.amount.amount
                for t in WalletTransaction.objects.filter(
                    wallet=wallet, transaction_type=WalletTransaction.TYPE_DEBIT
                )
            ),
            Decimal("0"),
        )

        assert credited - debited == _reread(wallet).available_balance.amount


# ============================================================
# reverse_transaction
# ============================================================


class TestReverseTransaction:
    def test_a_normal_reversal_deducts_and_marks_the_original(self):
        user = UserFactory()
        wallet = _wallet_for(user, "0.00")
        original = WalletService.credit(
            user, Decimal("40.00"), "USD", WalletTransaction.SOURCE_REFERRAL, "Reward"
        )

        reversal = WalletService.reverse_transaction(original, reason="Fraudulent referral")

        original.refresh_from_db()
        assert reversal.transaction_type == WalletTransaction.TYPE_REVERSAL
        assert reversal.amount == Money(Decimal("40.00"), "USD")
        assert original.status == WalletTransaction.STATUS_REVERSED
        assert original.reversed_by_id == reversal.pk, (
            "The original must point at its reversal, or the two entries cannot "
            "be paired up during an audit."
        )
        assert _reread(wallet).available_balance == Money(Decimal("0.00"), "USD")
        assert reversal.balance_after == Money(Decimal("0.00"), "USD")

    def test_reversing_a_spent_credit_raises_instead_of_clamping_to_zero(self):
        """
        The clamp was ``max(balance - amount, 0)``. Reversing a €40 credit the
        customer had already spent down to €10 left the wallet at 0 and quietly
        destroyed the missing €30 — the books were short with no record of it.

        Surfacing it is the point: this needs a human decision (claw back,
        write off, or chase), not a silent rounding.
        """
        user = UserFactory()
        wallet = _wallet_for(user, "0.00")
        original = WalletService.credit(
            user, Decimal("40.00"), "USD", WalletTransaction.SOURCE_REFERRAL, "Reward"
        )
        WalletService.debit(
            user, Decimal("30.00"), "USD", WalletTransaction.SOURCE_ORDER, "Spent it"
        )

        with pytest.raises(InsufficientBalance):
            WalletService.reverse_transaction(original, reason="Fraudulent referral")

        wallet = _reread(wallet)
        assert wallet.available_balance == Money(Decimal("10.00"), "USD"), (
            f"Balance is {wallet.available_balance}. A clamped reversal would "
            "have written 0.00 and destroyed the 30.00 difference."
        )

        original.refresh_from_db()
        assert original.status == WalletTransaction.STATUS_COMPLETED, (
            "The original was marked reversed even though the reversal failed."
        )
        assert not WalletTransaction.objects.filter(
            wallet=wallet, transaction_type=WalletTransaction.TYPE_REVERSAL
        ).exists()

    def test_a_reversal_can_never_change_what_currency_a_wallet_holds(self):
        """
        Reading the currency off the transaction and writing it onto the wallet
        is the same re-stamping mechanism as the credit/debit defect. If the two
        ever disagree, the reversal must refuse rather than pick one.
        """
        user = UserFactory()
        wallet = _wallet_for(user, "100.00", "USD")
        original = WalletService.credit(
            user, Decimal("40.00"), "USD", WalletTransaction.SOURCE_REFERRAL, "Reward"
        )

        # Simulate drift between the ledger row and the wallet.
        WalletTransaction.objects.filter(pk=original.pk).update(amount_currency="EUR")
        original.refresh_from_db()

        with pytest.raises(WalletCurrencyMismatch):
            WalletService.reverse_transaction(original)

        wallet = _reread(wallet)
        assert str(wallet.available_balance.currency) == "USD"
        assert wallet.available_balance == Money(Decimal("140.00"), "USD")

    def test_reversing_twice_is_refused(self):
        user = UserFactory()
        _wallet_for(user, "0.00")
        original = WalletService.credit(
            user, Decimal("40.00"), "USD", WalletTransaction.SOURCE_REFERRAL, "Reward"
        )
        WalletService.reverse_transaction(original)
        original.refresh_from_db()

        with pytest.raises(ValueError):
            WalletService.reverse_transaction(original)

    def test_a_debit_cannot_be_reversed(self):
        user = UserFactory()
        wallet = _wallet_for(user, "50.00")
        debit = WalletService.debit(
            user, Decimal("20.00"), "USD", WalletTransaction.SOURCE_ORDER, "Spend"
        )

        with pytest.raises(ValueError):
            WalletService.reverse_transaction(debit)

        assert _reread(wallet).available_balance == Money(Decimal("30.00"), "USD")


# ============================================================
# Ledger immutability
# ============================================================


class TestLedgerImmutability:
    def test_an_existing_transaction_cannot_be_updated(self):
        user = UserFactory()
        _wallet_for(user, "0.00")
        txn = WalletService.credit(
            user, Decimal("10.00"), "USD", WalletTransaction.SOURCE_MANUAL, "Credit"
        )

        txn.amount = Money(Decimal("999.00"), "USD")
        with pytest.raises(ValueError):
            txn.save()

        txn.refresh_from_db()
        assert txn.amount == Money(Decimal("10.00"), "USD")


# ============================================================
# Known defect — wallets on a non-USD store
# ============================================================


class TestWalletCurrencyOnANonUsdStore:
    """
    ``CustomerWallet``'s MoneyFields declare ``default_currency="USD"`` and
    ``get_or_create_wallet`` does not stamp the store's currency, so every
    wallet is born holding USD regardless of what the merchant sells in.

    On a EUR store that makes the currency guard — correct in itself — fire on
    the *first* credit any customer ever receives. Per D2, referral credit and
    loyalty fixed-value rewards mint wallet credit, so those payouts fail on
    every non-USD install.
    """

    @pytest.fixture
    def eur_store(self, _wallet_site_settings):
        _wallet_site_settings.default_currency = "EUR"
        _wallet_site_settings.save(update_fields=["default_currency"])
        return _wallet_site_settings

    def test_a_fresh_wallet_is_born_in_the_store_currency(self, eur_store):
        """
        A new wallet opens in the STORE's currency, not USD.

        The MoneyField declarations hardcode default_currency="USD", so every
        wallet used to be born holding USD wherever the shop traded. That was
        invisible while credit() silently re-stamped the currency, and became a
        hard failure once mixing was refused — the first EUR credit on a EUR
        store hit a USD wallet and raised.
        """
        user = UserFactory()

        wallet = WalletService.get_or_create_wallet(user)

        assert str(wallet.available_balance.currency) == "EUR"

    def test_get_balance_reports_the_store_currency_consistently(self, eur_store):
        """
        The reported currency must NOT change when a wallet row appears.

        It used to: EUR 0.00 from the no-wallet fallback, then USD 0.00 once the
        row existed. Same customer, same store, two different currencies
        depending on whether anyone had touched their wallet yet.
        """
        user = UserFactory()

        assert WalletService.get_balance(user) == Money(Decimal("0"), "EUR")

        WalletService.get_or_create_wallet(user)

        assert WalletService.get_balance(user) == Money(Decimal("0.00"), "EUR")

    # FIXED in P2.1: get_or_create_wallet opens the wallet in the store's
    # currency. Without this, the currency guard added alongside it would have
    # broken referral credit and loyalty rewards on every non-USD install.
    def test_the_first_credit_on_a_eur_store_succeeds(self, eur_store):
        user = UserFactory()

        WalletService.credit(
            user, Decimal("50.00"), "EUR", WalletTransaction.SOURCE_REFERRAL, "Referral reward"
        )

        assert WalletService.get_balance(user) == Money(Decimal("50.00"), "EUR")


# ============================================================
# get_balance
# ============================================================


class TestGetBalance:
    def test_returns_zero_in_the_store_currency_when_no_wallet_exists(self):
        user = UserFactory()
        assert not CustomerWallet.objects.filter(customer=user).exists()

        assert WalletService.get_balance(user) == Money(Decimal("0"), "USD")

    def test_returns_the_live_balance(self):
        user = UserFactory()
        _wallet_for(user, "37.50")

        assert WalletService.get_balance(user) == Money(Decimal("37.50"), "USD")


# ============================================================
# record_refund_transaction — the TYPE_REFUND writer
# ============================================================


class TestRecordRefundTransaction:
    def test_a_refund_credits_the_balance_as_a_refund_typed_row(self):
        user = UserFactory()
        wallet = _wallet_for(user, "10.00")

        txn = WalletService.record_refund_transaction(
            user, Decimal("15.00"), "USD", "Refund of order #1", reference_id="ref-1"
        )

        assert txn.transaction_type == WalletTransaction.TYPE_REFUND
        assert txn.source == WalletTransaction.SOURCE_REFUND
        assert txn.amount == Money(Decimal("15.00"), "USD")
        assert _reread(wallet).available_balance == Money(Decimal("25.00"), "USD")

    def test_a_refund_bumps_lifetime_credited_like_a_credit(self):
        user = UserFactory()
        wallet = _wallet_for(user, "0.00")
        WalletService.record_refund_transaction(user, Decimal("20.00"), "USD", "Refund")
        wallet = _reread(wallet)
        assert wallet.lifetime_credited == Money(Decimal("20.00"), "USD")
        assert wallet.lifetime_used == Money(Decimal("0.00"), "USD")

    def test_a_cross_currency_refund_is_refused_and_writes_nothing(self):
        user = UserFactory()
        wallet = _wallet_for(user, "100.00", "USD")
        with pytest.raises(WalletCurrencyMismatch):
            WalletService.record_refund_transaction(user, Decimal("5.00"), "EUR", "EUR refund")
        assert _reread(wallet).available_balance == Money(Decimal("100.00"), "USD")
        assert WalletTransaction.objects.filter(wallet=wallet).count() == 0

    def test_a_refund_on_a_frozen_wallet_is_refused(self):
        user = UserFactory()
        wallet = _wallet_for(user, "10.00", is_active=False)
        with pytest.raises(WalletFrozen):
            WalletService.record_refund_transaction(user, Decimal("5.00"), "USD", "Refund")
        assert _reread(wallet).available_balance == Money(Decimal("10.00"), "USD")

    @pytest.mark.parametrize("bad_amount", [Decimal("0.00"), Decimal("-1.00")])
    def test_a_non_positive_refund_is_refused(self, bad_amount):
        user = UserFactory()
        wallet = _wallet_for(user, "40.00")
        with pytest.raises(ValueError):
            WalletService.record_refund_transaction(user, bad_amount, "USD", "Nonsense")
        assert _reread(wallet).available_balance == Money(Decimal("40.00"), "USD")


# ============================================================
# adjust_balance — the signed TYPE_ADJUSTMENT writer
# ============================================================


class TestAdjustBalance:
    def _staff(self):
        return UserFactory(staff=True)

    def test_an_increase_raises_the_balance_as_an_adjustment_row(self):
        user = UserFactory()
        wallet = _wallet_for(user, "20.00")
        staff = self._staff()

        txn = WalletService.adjust_balance(
            user, Decimal("5.00"), "increase", "USD", "Goodwill correction", created_by=staff
        )

        assert txn.transaction_type == WalletTransaction.TYPE_ADJUSTMENT
        assert txn.source == WalletTransaction.SOURCE_MANUAL
        assert txn.amount == Money(Decimal("5.00"), "USD")  # positive; direction carries the sign
        assert txn.balance_after == Money(Decimal("25.00"), "USD")
        assert txn.created_by_id == staff.pk
        assert _reread(wallet).available_balance == Money(Decimal("25.00"), "USD")

    def test_a_decrease_lowers_the_balance(self):
        user = UserFactory()
        wallet = _wallet_for(user, "20.00")

        txn = WalletService.adjust_balance(
            user, Decimal("8.00"), "decrease", "USD", "Clawback", created_by=self._staff()
        )

        assert txn.amount == Money(Decimal("8.00"), "USD")
        assert txn.balance_after == Money(Decimal("12.00"), "USD")
        assert _reread(wallet).available_balance == Money(Decimal("12.00"), "USD")

    def test_adjustments_do_not_move_lifetime_counters(self):
        # A correction is neither organic credit nor spend.
        user = UserFactory()
        wallet = _wallet_for(user, "50.00")
        WalletService.adjust_balance(
            user, Decimal("10.00"), "increase", "USD", "c", created_by=self._staff()
        )
        WalletService.adjust_balance(
            user, Decimal("5.00"), "decrease", "USD", "c", created_by=self._staff()
        )
        wallet = _reread(wallet)
        assert wallet.lifetime_credited == Money(Decimal("0.00"), "USD")
        assert wallet.lifetime_used == Money(Decimal("0.00"), "USD")

    def test_a_decrease_below_zero_is_refused(self):
        user = UserFactory()
        wallet = _wallet_for(user, "5.00")
        with pytest.raises(InsufficientBalance):
            WalletService.adjust_balance(
                user, Decimal("5.01"), "decrease", "USD", "Over", created_by=self._staff()
            )
        assert _reread(wallet).available_balance == Money(Decimal("5.00"), "USD")
        assert WalletTransaction.objects.filter(wallet=wallet).count() == 0

    def test_a_missing_author_is_a_programming_error(self):
        user = UserFactory()
        _wallet_for(user, "5.00")
        with pytest.raises(ValueError, match="created_by"):
            WalletService.adjust_balance(
                user, Decimal("1.00"), "increase", "USD", "x", created_by=None
            )

    def test_an_unknown_direction_is_refused(self):
        user = UserFactory()
        _wallet_for(user, "5.00")
        with pytest.raises(ValueError, match="direction"):
            WalletService.adjust_balance(
                user, Decimal("1.00"), "sideways", "USD", "x", created_by=self._staff()
            )

    @pytest.mark.parametrize("bad_amount", [Decimal("0.00"), Decimal("-1.00")])
    def test_a_non_positive_adjustment_is_refused(self, bad_amount):
        user = UserFactory()
        _wallet_for(user, "5.00")
        with pytest.raises(ValueError):
            WalletService.adjust_balance(
                user, bad_amount, "increase", "USD", "x", created_by=self._staff()
            )

    def test_a_cross_currency_adjustment_is_refused_and_writes_nothing(self):
        user = UserFactory()
        wallet = _wallet_for(user, "100.00", "USD")
        with pytest.raises(WalletCurrencyMismatch):
            WalletService.adjust_balance(
                user, Decimal("5.00"), "increase", "EUR", "x", created_by=self._staff()
            )
        assert _reread(wallet).available_balance == Money(Decimal("100.00"), "USD")
        assert WalletTransaction.objects.filter(wallet=wallet).count() == 0

    def test_an_adjustment_on_a_frozen_wallet_is_refused(self):
        user = UserFactory()
        wallet = _wallet_for(user, "10.00", is_active=False)
        with pytest.raises(WalletFrozen):
            WalletService.adjust_balance(
                user, Decimal("1.00"), "increase", "USD", "x", created_by=self._staff()
            )
        assert _reread(wallet).available_balance == Money(Decimal("10.00"), "USD")

    def test_an_adjustment_cannot_be_reversed(self):
        # reverse_transaction only ever subtracts, so it would move a decrease
        # adjustment the wrong way and destroy funds. Undo an adjustment with an
        # opposite adjustment instead; reversing one is refused outright.
        user = UserFactory()
        wallet = _wallet_for(user, "100.00")
        adj = WalletService.adjust_balance(
            user, Decimal("30.00"), "decrease", "USD", "clawback", created_by=self._staff()
        )
        assert _reread(wallet).available_balance == Money(Decimal("70.00"), "USD")

        with pytest.raises(ValueError, match="Cannot reverse"):
            WalletService.reverse_transaction(adj, reason="oops")

        # Balance untouched; the correct undo is an opposite (increase) adjustment.
        assert _reread(wallet).available_balance == Money(Decimal("70.00"), "USD")
        WalletService.adjust_balance(
            user, Decimal("30.00"), "increase", "USD", "undo clawback", created_by=self._staff()
        )
        assert _reread(wallet).available_balance == Money(Decimal("100.00"), "USD")
