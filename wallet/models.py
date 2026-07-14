"""
Customer Wallet Models

Ledger-based store credit system. CustomerWallet holds the cached balance,
WalletTransaction is the immutable authoritative ledger of all balance changes.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

User = get_user_model()


class CustomerWallet(models.Model):
    """
    Store credit wallet for a customer.

    Cached balance derived from the WalletTransaction ledger.
    """

    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wallet",
        verbose_name=_("Customer"),
    )

    available_balance = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        default=0,
        verbose_name=_("Available Balance"),
        help_text=_("Current spendable balance"),
    )

    pending_balance = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        default=0,
        verbose_name=_("Pending Balance"),
        help_text=_("Credits not yet available (e.g. pending refund window)"),
    )

    lifetime_credited = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        default=0,
        verbose_name=_("Lifetime Credited"),
    )

    lifetime_used = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        default=0,
        verbose_name=_("Lifetime Used"),
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=_("Active"),
        help_text=_("Deactivate to freeze this wallet"),
    )

    last_credited_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Credited At"),
    )
    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Used At"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Customer Wallet")
        verbose_name_plural = _("Customer Wallets")
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["last_credited_at"]),
        ]

    def __str__(self):
        name = self.customer.get_full_name() or self.customer.email
        return f"{name} — {self.available_balance}"


class WalletTransaction(models.Model):
    """
    Immutable ledger entry for wallet balance changes.

    Never updated or deleted — only new compensating entries are added.
    """

    TYPE_CREDIT = "credit"
    TYPE_DEBIT = "debit"
    TYPE_REFUND = "refund"
    TYPE_ADJUSTMENT = "adjustment"
    TYPE_REVERSAL = "reversal"

    TRANSACTION_TYPES = [
        (TYPE_CREDIT, _("Credit")),
        (TYPE_DEBIT, _("Debit")),
        (TYPE_REFUND, _("Refund")),
        (TYPE_ADJUSTMENT, _("Adjustment")),
        (TYPE_REVERSAL, _("Reversal")),
    ]

    STATUS_COMPLETED = "completed"
    STATUS_PENDING = "pending"
    STATUS_REVERSED = "reversed"

    STATUS_CHOICES = [
        (STATUS_COMPLETED, _("Completed")),
        (STATUS_PENDING, _("Pending")),
        (STATUS_REVERSED, _("Reversed")),
    ]

    SOURCE_REFERRAL = "referral"
    SOURCE_REFUND = "refund"
    SOURCE_PROMOTION = "promotion"
    SOURCE_MANUAL = "manual"
    SOURCE_ORDER = "order"

    SOURCE_CHOICES = [
        (SOURCE_REFERRAL, _("Referral Reward")),
        (SOURCE_REFUND, _("Order Refund")),
        (SOURCE_PROMOTION, _("Promotion")),
        (SOURCE_MANUAL, _("Manual Adjustment")),
        (SOURCE_ORDER, _("Order Payment")),
    ]

    wallet = models.ForeignKey(
        CustomerWallet,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name=_("Wallet"),
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        db_index=True,
        verbose_name=_("Type"),
    )

    amount = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        verbose_name=_("Amount"),
        help_text=_("Always positive; transaction_type determines direction"),
    )

    balance_after = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        verbose_name=_("Balance After"),
        help_text=_("Wallet balance snapshot after this transaction"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_COMPLETED,
        db_index=True,
        verbose_name=_("Status"),
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        db_index=True,
        verbose_name=_("Source"),
    )

    description = models.CharField(
        max_length=500,
        verbose_name=_("Description"),
    )

    reference_id = models.CharField(
        max_length=100,
        blank=True,
        default="",
        db_index=True,
        verbose_name=_("Reference ID"),
        help_text=_("External reference (reward ID, order number, etc.)"),
    )

    reversed_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reversal_of_set",
        verbose_name=_("Reversed By"),
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wallet_transactions_created",
        verbose_name=_("Created By"),
        help_text=_("Staff user for manual adjustments"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Created At"),
    )

    class Meta:
        verbose_name = _("Wallet Transaction")
        verbose_name_plural = _("Wallet Transactions")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["wallet", "transaction_type"]),
            models.Index(fields=["wallet", "status"]),
            models.Index(fields=["wallet", "created_at"]),
            models.Index(fields=["source", "reference_id"]),
        ]

    def __str__(self):
        return f"{self.get_transaction_type_display()} {self.amount} — {self.description[:50]}"

    def save(self, *args, **kwargs):
        if self.pk and not kwargs.pop("_allow_update", False):
            raise ValueError(
                "WalletTransaction records are immutable. "
                "Create a new reversal transaction instead of updating."
            )
        super().save(*args, **kwargs)
