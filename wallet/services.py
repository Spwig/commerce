"""
Wallet Service

Provides credit, debit, and reversal operations on customer wallets.
All balance mutations go through this service to keep the ledger consistent.
"""

import logging
from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from djmoney.money import Money

from core.utils import get_default_currency

from .models import CustomerWallet, WalletTransaction

logger = logging.getLogger(__name__)


class InsufficientBalance(Exception):
    """Raised when a debit exceeds the available wallet balance."""


class WalletFrozen(Exception):
    """Raised when an operation is attempted on a frozen wallet."""


class WalletCurrencyMismatch(Exception):
    """
    Raised when a movement's currency differs from the wallet's.

    Deliberately a hard error rather than a conversion: converting silently is
    how $100 + €50 became €150 before this existed.
    """


class WalletService:
    @staticmethod
    def get_or_create_wallet(user, currency=None):
        """
        Get or create a wallet for the given user.

        A new wallet is opened in the **store's** default currency, not USD.
        The MoneyField declarations hardcode ``default_currency="USD"``, so
        every wallet used to be born holding USD regardless of where the shop
        trades. That was invisible while credit() silently re-stamped the
        currency on first use — but once mixing is refused (see
        :meth:`_assert_currency`), a EUR store's first referral credit would
        hit a USD wallet and raise. The guard is right; this is what had to
        change with it.

        Args:
            user: Customer the wallet belongs to.
            currency: Override the currency for a new wallet. Ignored if the
                wallet already exists — an existing wallet's currency is never
                changed by a lookup.

        Returns:
            CustomerWallet
        """
        from djmoney.money import Money

        wallet = CustomerWallet.objects.filter(customer=user).first()
        if wallet is not None:
            return wallet

        currency = str(currency or get_default_currency())
        zero = Money(Decimal("0"), currency)
        wallet, _ = CustomerWallet.objects.get_or_create(
            customer=user,
            defaults={
                "available_balance": zero,
                "pending_balance": zero,
                "lifetime_credited": zero,
                "lifetime_used": zero,
            },
        )
        return wallet

    @staticmethod
    def _assert_currency(wallet, currency):
        """
        Refuse to mix currencies in one wallet.

        Both credit() and debit() used to add the incoming *number* to the
        stored balance and then re-stamp the wallet with the incoming currency.
        Crediting €50 to a wallet holding $100 produced **€150** — the
        customer's dollars silently became euros, with no error and no log.

        A wallet holds one currency. Converting would need a rate, a record of
        that rate, and a decision about who absorbs the spread; none of that
        exists here, so the only safe answer is to refuse. Callers converting
        deliberately should debit in the old currency and credit in the new,
        leaving both movements on the ledger.
        """
        wallet_currency = str(wallet.available_balance.currency)
        incoming = str(currency)
        if wallet_currency != incoming:
            raise WalletCurrencyMismatch(
                f"Wallet for {wallet.customer_id} holds {wallet_currency}; "
                f"refusing a {incoming} movement. A wallet holds one currency — "
                f"converting requires an explicit debit + credit pair."
            )

    @staticmethod
    def _apply_credit(
        user, amount, currency, transaction_type, source, description, reference_id, created_by
    ):
        """
        Shared implementation for every credit-direction ledger write (a plain
        credit and a refund are the same money movement — value INTO the wallet —
        differing only in ``transaction_type``). Keeping one writer means the two
        can never drift apart (the divergence-is-where-bugs-hide rule the tender
        services follow). Caller is responsible for ``@transaction.atomic``.

        Both types are POSITIVE in the reconciler (I5), so both add to
        ``available_balance`` and bump ``lifetime_credited``.
        """
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Credit amount must be positive")

        wallet = WalletService.get_or_create_wallet(user)
        # Lock the row to prevent concurrent balance corruption
        wallet = CustomerWallet.objects.select_for_update().get(pk=wallet.pk)

        if not wallet.is_active:
            raise WalletFrozen(f"Wallet for {user.email} is frozen")

        WalletService._assert_currency(wallet, currency)
        # Use the WALLET's currency from here on, not the caller's. They are now
        # guaranteed equal, but reading it from the wallet means a future change
        # cannot reintroduce the re-stamping bug.
        currency = str(wallet.available_balance.currency)

        new_balance = wallet.available_balance.amount + amount

        txn = WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=transaction_type,
            amount=Money(amount, currency),
            balance_after=Money(new_balance, currency),
            status=WalletTransaction.STATUS_COMPLETED,
            source=source,
            description=description,
            reference_id=reference_id,
            created_by=created_by,
        )

        wallet.available_balance = Money(new_balance, currency)
        wallet.lifetime_credited = Money(wallet.lifetime_credited.amount + amount, currency)
        wallet.last_credited_at = timezone.now()
        wallet.save(
            update_fields=[
                "available_balance",
                "available_balance_currency",
                "lifetime_credited",
                "lifetime_credited_currency",
                "last_credited_at",
                "updated_at",
            ]
        )

        logger.info(
            f"{transaction_type.capitalize()} {amount} {currency} to wallet for {user.email} "
            f"(txn={txn.id}, source={source})"
        )
        return txn

    @staticmethod
    @transaction.atomic
    def credit(user, amount, currency, source, description, reference_id="", created_by=None):
        """
        Add credit to a customer's wallet.

        Args:
            user: Customer user instance
            amount: Decimal or numeric amount (must be positive)
            currency: Currency code string (e.g. 'USD')
            source: Source choice (e.g. 'referral', 'refund')
            description: Human-readable description
            reference_id: External reference for linking
            created_by: Staff user for manual adjustments

        Returns:
            WalletTransaction
        """
        return WalletService._apply_credit(
            user,
            amount,
            currency,
            WalletTransaction.TYPE_CREDIT,
            source,
            description,
            reference_id,
            created_by,
        )

    @staticmethod
    @transaction.atomic
    def record_refund_transaction(
        user, amount, currency, description, reference_id="", created_by=None
    ):
        """
        Credit a refunded amount back to a customer's wallet as a refund entry.

        A refund is money returned for an order — value into the wallet, like a
        credit, but recorded as its own ``TYPE_REFUND`` ledger row (and always
        ``source='refund'``) so refunds are distinguishable from promotional or
        referral credits in history, reporting, and the reconciler. The
        reconciler already counts refunds as positive, so invariant I5 holds.

        Returns the created WalletTransaction.
        """
        return WalletService._apply_credit(
            user,
            amount,
            currency,
            WalletTransaction.TYPE_REFUND,
            WalletTransaction.SOURCE_REFUND,
            description,
            reference_id,
            created_by,
        )

    @staticmethod
    @transaction.atomic
    def debit(user, amount, currency, source, description, reference_id="", created_by=None):
        """
        Deduct from a customer's wallet.

        Args:
            user: Customer user instance
            amount: Decimal or numeric amount (must be positive)
            currency: Currency code string
            source: Source choice
            description: Human-readable description
            reference_id: External reference
            created_by: Staff user for manual adjustments

        Returns:
            WalletTransaction

        Raises:
            InsufficientBalance: If wallet doesn't have enough funds
            WalletFrozen: If wallet is frozen
        """
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Debit amount must be positive")

        wallet = WalletService.get_or_create_wallet(user)
        # Lock the row to prevent concurrent balance corruption
        wallet = CustomerWallet.objects.select_for_update().get(pk=wallet.pk)

        if not wallet.is_active:
            raise WalletFrozen(f"Wallet for {user.email} is frozen")

        # Before the sufficiency check: comparing a EUR amount against a USD
        # balance is meaningless, so a mismatch must fail as a mismatch rather
        # than as "insufficient funds".
        WalletService._assert_currency(wallet, currency)
        currency = str(wallet.available_balance.currency)

        if wallet.available_balance.amount < amount:
            raise InsufficientBalance(
                f"Wallet balance {wallet.available_balance} is insufficient "
                f"for debit of {amount} {currency}"
            )

        new_balance = wallet.available_balance.amount - amount

        txn = WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.TYPE_DEBIT,
            amount=Money(amount, currency),
            balance_after=Money(new_balance, currency),
            status=WalletTransaction.STATUS_COMPLETED,
            source=source,
            description=description,
            reference_id=reference_id,
            created_by=created_by,
        )

        wallet.available_balance = Money(new_balance, currency)
        wallet.lifetime_used = Money(wallet.lifetime_used.amount + amount, currency)
        wallet.last_used_at = timezone.now()
        wallet.save(
            update_fields=[
                "available_balance",
                "available_balance_currency",
                "lifetime_used",
                "lifetime_used_currency",
                "last_used_at",
                "updated_at",
            ]
        )

        logger.info(
            f"Debited {amount} {currency} from wallet for {user.email} "
            f"(txn={txn.id}, source={source})"
        )
        return txn

    @staticmethod
    @transaction.atomic
    def reverse_transaction(original_txn, reason=""):
        """
        Reverse a completed credit transaction.

        Creates a new reversal entry and deducts the amount from the wallet.

        Args:
            original_txn: WalletTransaction to reverse
            reason: Reason for reversal

        Returns:
            WalletTransaction (the reversal entry)
        """
        if original_txn.status == WalletTransaction.STATUS_REVERSED:
            raise ValueError("Transaction is already reversed")

        if original_txn.transaction_type not in (
            WalletTransaction.TYPE_CREDIT,
            WalletTransaction.TYPE_REFUND,
        ):
            # An ADJUSTMENT is a signed correction whose direction is not stored
            # on the row, so reverse_transaction (which only ever subtracts) would
            # move a decrease-adjustment the WRONG way and quietly destroy funds —
            # and the reconciler, reading the sign from balance_after, would not
            # catch it. Undo an adjustment with an OPPOSITE adjustment instead
            # (WalletService.adjust_balance), which stays honest on the ledger.
            raise ValueError(f"Cannot reverse a {original_txn.transaction_type} transaction")

        # Lock the wallet row to prevent concurrent balance corruption
        wallet = CustomerWallet.objects.select_for_update().get(pk=original_txn.wallet_id)
        amount = original_txn.amount.amount

        # Take the currency from the WALLET, and assert the transaction agrees.
        # Reading it from the transaction and writing it onto the wallet is how
        # the re-stamping bug worked; a reversal must never change what currency
        # a wallet holds.
        WalletService._assert_currency(wallet, original_txn.amount.currency)
        currency = str(wallet.available_balance.currency)

        new_balance = wallet.available_balance.amount - amount
        if new_balance < 0:
            # Previously clamped to zero with max(), which quietly destroyed the
            # difference: reversing a credit the customer had already spent left
            # the books short with no record. Surface it instead — this needs a
            # human decision (claw back, write off, or chase), not a silent
            # rounding to zero.
            raise InsufficientBalance(
                f"Reversing {original_txn.amount} would take the wallet to "
                f"{Money(new_balance, currency)}. The credit has already been "
                f"spent — resolve manually rather than clamping to zero."
            )

        reversal = WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.TYPE_REVERSAL,
            amount=original_txn.amount,
            balance_after=Money(new_balance, currency),
            status=WalletTransaction.STATUS_COMPLETED,
            source=original_txn.source,
            description=reason or f"Reversal of transaction #{original_txn.id}",
            reference_id=original_txn.reference_id,
            reversed_by=None,
        )

        # Mark the original as reversed, pointing to the reversal entry
        original_txn.reversed_by = reversal
        original_txn.status = WalletTransaction.STATUS_REVERSED
        original_txn.save(
            _allow_update=True,
            update_fields=[
                "reversed_by",
                "status",
            ],
        )

        wallet.available_balance = Money(new_balance, currency)
        wallet.save(
            update_fields=[
                "available_balance",
                "available_balance_currency",
                "updated_at",
            ]
        )

        logger.info(
            f"Reversed transaction #{original_txn.id} for {amount} {currency} "
            f"(reversal txn={reversal.id})"
        )
        return reversal

    ADJUST_INCREASE = "increase"
    ADJUST_DECREASE = "decrease"

    @staticmethod
    @transaction.atomic
    def adjust_balance(
        user,
        amount,
        direction,
        currency,
        description,
        created_by,
        reference_id="",
    ):
        """
        Apply a manual staff correction to a wallet balance.

        A first-class, signed ledger correction — the writer the `adjustment`
        transaction type was declared for. Distinct from a credit/debit: it does
        not represent organic value earned or spent, so it is recorded as
        ``TYPE_ADJUSTMENT`` and leaves ``lifetime_credited`` / ``lifetime_used``
        untouched, while still moving ``available_balance`` under the wallet lock
        so invariant I5 holds.

        The sign convention the reconciler could not previously assume is now
        DEFINED here: ``amount`` is always positive and ``direction`` says whether
        it raises or lowers the balance; the row's ``balance_after`` records the
        signed result, and the reconciler reconstructs the effect from it (and
        verifies it against ``amount``). A staff ``created_by`` is required —
        an adjustment with no author is a programming error.

        Raises ValueError (bad direction / missing author / non-positive amount),
        WalletFrozen, WalletCurrencyMismatch, or InsufficientBalance (a decrease
        that would take the wallet below zero).
        """
        if created_by is None:
            raise ValueError("adjust_balance requires created_by (the staff author)")
        if direction not in (WalletService.ADJUST_INCREASE, WalletService.ADJUST_DECREASE):
            raise ValueError(f"direction must be 'increase' or 'decrease', got {direction!r}")

        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Adjustment amount must be positive; direction sets the sign")

        wallet = WalletService.get_or_create_wallet(user)
        wallet = CustomerWallet.objects.select_for_update().get(pk=wallet.pk)

        if not wallet.is_active:
            raise WalletFrozen(f"Wallet for {user.email} is frozen")

        WalletService._assert_currency(wallet, currency)
        currency = str(wallet.available_balance.currency)

        if direction == WalletService.ADJUST_INCREASE:
            new_balance = wallet.available_balance.amount + amount
        else:
            new_balance = wallet.available_balance.amount - amount
            if new_balance < 0:
                raise InsufficientBalance(
                    f"Decreasing by {amount} {currency} would take the wallet "
                    f"below zero (balance {wallet.available_balance})."
                )

        txn = WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.TYPE_ADJUSTMENT,
            amount=Money(amount, currency),
            balance_after=Money(new_balance, currency),
            status=WalletTransaction.STATUS_COMPLETED,
            source=WalletTransaction.SOURCE_MANUAL,
            description=description,
            reference_id=reference_id,
            created_by=created_by,
        )

        wallet.available_balance = Money(new_balance, currency)
        # A correction is neither organic credit nor spend, so lifetime_* are
        # intentionally left as-is; only the activity timestamp moves.
        if direction == WalletService.ADJUST_INCREASE:
            wallet.last_credited_at = timezone.now()
            wallet.save(
                update_fields=[
                    "available_balance",
                    "available_balance_currency",
                    "last_credited_at",
                    "updated_at",
                ]
            )
        else:
            wallet.last_used_at = timezone.now()
            wallet.save(
                update_fields=[
                    "available_balance",
                    "available_balance_currency",
                    "last_used_at",
                    "updated_at",
                ]
            )

        logger.info(
            f"Adjusted wallet for {user.email} by {direction} {amount} {currency} "
            f"(txn={txn.id}, by={getattr(created_by, 'email', created_by)})"
        )
        return txn

    @staticmethod
    def get_balance(user):
        """
        Get available wallet balance for a user.

        Returns:
            Money instance (0 if no wallet exists)
        """
        try:
            wallet = CustomerWallet.objects.get(customer=user)
            return wallet.available_balance
        except CustomerWallet.DoesNotExist:
            return Money(0, get_default_currency())
