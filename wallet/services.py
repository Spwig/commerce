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


class WalletService:

    @staticmethod
    def get_or_create_wallet(user):
        """
        Get or create a wallet for the given user.

        Returns:
            CustomerWallet
        """
        wallet, _ = CustomerWallet.objects.get_or_create(customer=user)
        return wallet

    @staticmethod
    @transaction.atomic
    def credit(user, amount, currency, source, description,
               reference_id='', created_by=None):
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
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Credit amount must be positive")

        wallet = WalletService.get_or_create_wallet(user)
        # Lock the row to prevent concurrent balance corruption
        wallet = CustomerWallet.objects.select_for_update().get(pk=wallet.pk)

        if not wallet.is_active:
            raise WalletFrozen(f"Wallet for {user.email} is frozen")

        new_balance = wallet.available_balance.amount + amount

        txn = WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.TYPE_CREDIT,
            amount=Money(amount, currency),
            balance_after=Money(new_balance, currency),
            status=WalletTransaction.STATUS_COMPLETED,
            source=source,
            description=description,
            reference_id=reference_id,
            created_by=created_by,
        )

        wallet.available_balance = Money(new_balance, currency)
        wallet.lifetime_credited = Money(
            wallet.lifetime_credited.amount + amount, currency
        )
        wallet.last_credited_at = timezone.now()
        wallet.save(update_fields=[
            'available_balance', 'available_balance_currency',
            'lifetime_credited', 'lifetime_credited_currency',
            'last_credited_at', 'updated_at',
        ])

        logger.info(
            f"Credited {amount} {currency} to wallet for {user.email} "
            f"(txn={txn.id}, source={source})"
        )
        return txn

    @staticmethod
    @transaction.atomic
    def debit(user, amount, currency, source, description,
              reference_id=''):
        """
        Deduct from a customer's wallet.

        Args:
            user: Customer user instance
            amount: Decimal or numeric amount (must be positive)
            currency: Currency code string
            source: Source choice
            description: Human-readable description
            reference_id: External reference

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
        )

        wallet.available_balance = Money(new_balance, currency)
        wallet.lifetime_used = Money(
            wallet.lifetime_used.amount + amount, currency
        )
        wallet.last_used_at = timezone.now()
        wallet.save(update_fields=[
            'available_balance', 'available_balance_currency',
            'lifetime_used', 'lifetime_used_currency',
            'last_used_at', 'updated_at',
        ])

        logger.info(
            f"Debited {amount} {currency} from wallet for {user.email} "
            f"(txn={txn.id}, source={source})"
        )
        return txn

    @staticmethod
    @transaction.atomic
    def reverse_transaction(original_txn, reason=''):
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
            WalletTransaction.TYPE_ADJUSTMENT,
        ):
            raise ValueError(
                f"Cannot reverse a {original_txn.transaction_type} transaction"
            )

        # Lock the wallet row to prevent concurrent balance corruption
        wallet = CustomerWallet.objects.select_for_update().get(pk=original_txn.wallet_id)
        amount = original_txn.amount.amount
        currency = str(original_txn.amount.currency)

        new_balance = max(wallet.available_balance.amount - amount, Decimal('0'))

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
        original_txn.save(_allow_update=True, update_fields=[
            'reversed_by', 'status',
        ])

        wallet.available_balance = Money(new_balance, currency)
        wallet.save(update_fields=[
            'available_balance', 'available_balance_currency', 'updated_at',
        ])

        logger.info(
            f"Reversed transaction #{original_txn.id} for {amount} {currency} "
            f"(reversal txn={reversal.id})"
        )
        return reversal

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
