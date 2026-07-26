"""
Wallet as a payment tender — hold at checkout, debit on payment.

Mirrors ``catalog.services.gift_card_tender_service`` deliberately: the wallet
is the second internal tender on the same rail, and every divergence between
the two services is a place a future bug hides. Where this file differs, the
difference is the point:

* **Wallets belong to accounts.** No code entry — the wallet is looked up from
  the authenticated user, and guests are refused upstream. A spend path never
  ``get_or_create``s: a customer with no wallet has nothing to spend, and
  creating one here would turn a typo'd request into a new empty ledger.
* **Holds move no money** (same as gift cards). An authorize row reserves value;
  ``spendable_balance`` subtracts live holds across ALL of the user's sessions,
  so two tabs cannot promise the same pound twice. Abandoned checkouts cost
  nothing — the sweeper voids status rows and never touches a balance, so a
  crashed sweeper can never strand customer funds.
* **Capture debits through WalletService** — the ledger row and the stored
  balance move together under the wallet lock, keeping invariant I5 (balance ==
  signed ledger sum) intact, which the nightly reconciler verifies.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R2, P2.5a)
"""

import logging
from datetime import timedelta
from decimal import Decimal

from django.db import transaction as db_transaction
from django.utils import timezone
from djmoney.money import Money

logger = logging.getLogger(__name__)


class WalletTenderError(Exception):
    """The wallet cannot tender for this checkout."""


class InsufficientWalletBalance(WalletTenderError):
    """Nothing (or not enough) left to hold."""


class WalletTenderService:
    # Same lifetime as gift card holds: the sweeper task releases anything
    # older, and capture caps at what the order actually owes regardless.
    HOLD_MINUTES = 30

    # ------------------------------------------------------------------
    # id helpers — idempotency lives in these
    # ------------------------------------------------------------------

    @staticmethod
    def _auth_txn_id(session_id, wallet_id):
        return f"wt-auth:{session_id}:{wallet_id}"

    @staticmethod
    def _capture_txn_id(order_id, wallet_id):
        return f"wt-cap:{order_id}:{wallet_id}"

    # ------------------------------------------------------------------
    # authorize
    # ------------------------------------------------------------------

    @classmethod
    @db_transaction.atomic
    def authorize_for_session(cls, checkout_session, user, amount=None):
        """
        Place a hold on the user's wallet for an in-progress checkout.

        Args:
            checkout_session: CheckoutSession the hold belongs to.
            user: the authenticated customer. Guests are refused by the view;
                this re-checks because money code never trusts its caller.
            amount: Money to hold. Defaults to ``min(spendable, amount_due)`` —
                unlike gift cards there is no "hold the whole card" instinct to
                honour, and holding a large balance in full for a small order
                would lock the customer's own money for HOLD_MINUTES for no
                benefit.

        Returns:
            PaymentTransaction: the authorize row.

        Raises:
            WalletTenderError: no wallet, frozen wallet, currency mismatch.
            InsufficientWalletBalance: nothing left to hold.
        """
        from payment_providers.models import PaymentTransaction
        from wallet.models import CustomerWallet

        if user is None or not getattr(user, "is_authenticated", False):
            raise WalletTenderError("Wallet payment requires a signed-in account")

        # Existing, active wallet only — never get_or_create on a spend path.
        wallet = CustomerWallet.objects.select_for_update().filter(customer=user).first()
        if wallet is None:
            raise WalletTenderError("No wallet exists for this account")
        if not wallet.is_active:
            # Frozen is a merchant decision (chargeback, fraud flag) — same
            # stance as deactivated gift cards: refuse, never work around.
            raise WalletTenderError("This wallet is frozen")

        currency = wallet.available_balance.currency

        # D5 applies to the wallet exactly as to gift cards: stored value is
        # single-currency and never converted. A GBP wallet cannot part-pay a
        # EUR order.
        session_currency = checkout_session.total_amount.currency
        if str(currency) != str(session_currency):
            raise WalletTenderError(f"Wallet holds {currency}; this order is in {session_currency}")
        if amount is not None and amount.currency != currency:
            raise WalletTenderError(
                f"Hold currency {amount.currency} does not match the wallet's {currency}"
            )

        # Supersede this session's own earlier wallet holds before computing
        # what is spendable — a re-submit must not be blocked by its own
        # previous hold. Same fix, same reasoning, as the gift card service's
        # third-attempt 500.
        superseded = PaymentTransaction.objects.filter(
            wallet=wallet,
            checkout_session=checkout_session,
            tender_type=PaymentTransaction.TENDER_WALLET,
            transaction_type="authorize",
            status="authorized",
        ).update(status="voided")
        if superseded:
            logger.info(
                f"Superseded {superseded} wallet hold(s) for checkout {checkout_session.pk}"
            )

        spendable = cls.spendable_balance(wallet)
        if spendable.amount <= 0:
            raise InsufficientWalletBalance("No wallet balance available")

        if amount is None:
            due = checkout_session.amount_due
            amount = Money(min(spendable.amount, due.amount), currency)
            if amount.amount <= 0:
                raise WalletTenderError("Nothing is due on this checkout")
        elif amount.amount <= 0:
            raise WalletTenderError("Hold amount must be greater than zero")
        elif amount > spendable:
            raise InsufficientWalletBalance(
                f"Wallet has {spendable} spendable, cannot hold {amount}"
            )

        base_id = cls._auth_txn_id(checkout_session.pk, wallet.pk)
        txn_id = base_id
        attempt = 0
        while PaymentTransaction.objects.filter(transaction_id=txn_id).exists():
            attempt += 1
            txn_id = f"{base_id}:{attempt}"

        hold = PaymentTransaction.objects.create(
            transaction_id=txn_id,
            tender_type=PaymentTransaction.TENDER_WALLET,
            transaction_type="authorize",
            status="authorized",
            wallet=wallet,
            checkout_session=checkout_session,
            amount=amount,
            settlement_amount=amount,
            exchange_rate=Decimal("1.00000000"),
            provider_account=None,
        )
        logger.info(f"Held {amount} of wallet {wallet.pk} for checkout {checkout_session.pk}")
        return hold

    @classmethod
    def spendable_balance(cls, wallet):
        """
        What the wallet can still promise: stored balance minus live holds.

        Holds are counted across ALL sessions — the second tab sees the first
        tab's hold. The stored ``available_balance`` itself is untouched by
        holds (invariant I5 pins it to the ledger, and holds are not ledger
        rows); this property is the checkout-facing view.
        """
        from django.db.models import Sum

        from payment_providers.models import PaymentTransaction

        held = PaymentTransaction.objects.filter(
            wallet=wallet,
            tender_type=PaymentTransaction.TENDER_WALLET,
            transaction_type="authorize",
            status="authorized",
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

        remaining = wallet.available_balance.amount - held
        return Money(max(remaining, Decimal("0")), wallet.available_balance.currency)

    # ------------------------------------------------------------------
    # capture
    # ------------------------------------------------------------------

    @classmethod
    @db_transaction.atomic
    def capture_for_order(cls, order, checkout_session=None):
        """
        Settle every wallet hold attached to a paid order.

        Debits the wallet through WalletService (ledger row + balance together,
        under the wallet lock), writes the capture row, and voids the hold —
        one transaction, so a partial settlement cannot leave a wallet debited
        with its hold still live.

        Idempotent per (order, wallet): a retried payment webhook finds the
        existing capture row and skips.

        The capture is capped at what the order still owes **counting every
        tender type** — see the `remaining` computation. Capping against only
        wallet captures would let a gift card leg and a wallet leg each settle
        "the rest of the order" on a cart that shrank between hold and payment.
        """
        from django.db.models import Q

        from payment_providers.models import PaymentTransaction
        from wallet.models import CustomerWallet
        from wallet.services import WalletService

        # Same scope construction as the gift card rail — divergence between
        # the two services is where bugs hide.
        outstanding = PaymentTransaction.objects.filter(
            tender_type=PaymentTransaction.TENDER_WALLET,
            transaction_type="authorize",
            status="authorized",
        ).select_related("wallet")
        scope = Q(order=order)
        if checkout_session is not None:
            scope |= Q(checkout_session=checkout_session)
        holds = list(outstanding.filter(scope))
        if not holds:
            return []

        # What the order still needs, after EVERY completed capture and charge
        # regardless of tender type. This is the joint over-capture guard: the
        # gift card rail runs before this one in the settlement receiver, and
        # its captures must shrink what the wallet may take.
        remaining = order.total_amount
        already = PaymentTransaction.objects.filter(
            order=order,
            transaction_type__in=("capture", "charge"),
            status="completed",
        )
        for prior in already:
            remaining -= prior.settlement_amount or prior.amount

        captures = []
        for hold in holds:
            wallet = CustomerWallet.objects.select_for_update().get(pk=hold.wallet_id)
            capture_id = cls._capture_txn_id(order.pk, wallet.pk)

            existing = PaymentTransaction.objects.filter(transaction_id=capture_id).first()
            if existing is not None:
                captures.append(existing)
                continue

            if remaining.amount <= 0:
                # Order already fully funded (cart shrank, or another tender
                # covered it). Release the hold; debit nothing.
                hold.status = "voided"
                hold.save(update_fields=["status", "updated_at"])
                logger.info(
                    f"Voided wallet hold {hold.transaction_id}: order "
                    f"{order.order_number} is already fully funded"
                )
                continue

            capture_amount = Money(min(hold.amount.amount, remaining.amount), hold.amount.currency)

            # Ledger debit and stored balance move together here; the capture
            # row's id doubles as the ledger reference for cross-auditing.
            WalletService.debit(
                wallet.customer,
                capture_amount.amount,
                str(capture_amount.currency),
                "order",
                f"Payment for order {order.order_number}",
                reference_id=capture_id,
            )

            capture = PaymentTransaction.objects.create(
                transaction_id=capture_id,
                tender_type=PaymentTransaction.TENDER_WALLET,
                transaction_type="capture",
                status="completed",
                wallet=wallet,
                order=order,
                parent_transaction=hold,
                amount=capture_amount,
                settlement_amount=capture_amount,
                exchange_rate=Decimal("1.00000000"),
                provider_account=None,
                completed_at=timezone.now(),
            )
            hold.status = "voided"
            hold.save(update_fields=["status", "updated_at"])

            remaining -= capture_amount
            captures.append(capture)
            logger.info(
                f"Captured {capture_amount} from wallet {wallet.pk} for order {order.order_number}"
            )

        return captures

    # ------------------------------------------------------------------
    # void / sweep
    # ------------------------------------------------------------------

    @classmethod
    def void_holds(cls, checkout_session):
        """Release every live wallet hold on a session. Moves no money."""
        from payment_providers.models import PaymentTransaction

        count = PaymentTransaction.objects.filter(
            checkout_session=checkout_session,
            tender_type=PaymentTransaction.TENDER_WALLET,
            transaction_type="authorize",
            status="authorized",
        ).update(status="voided")
        if count:
            logger.info(f"Voided {count} wallet hold(s) for checkout {checkout_session.pk}")
        return count

    @classmethod
    def expire_stale_holds(cls):
        """
        Void wallet holds older than HOLD_MINUTES.

        A status flip, never a balance movement — a crashed sweeper can strand
        nothing. The generalised beat task covers both internal tenders.
        """
        from payment_providers.models import PaymentTransaction

        cutoff = timezone.now() - timedelta(minutes=cls.HOLD_MINUTES)
        count = PaymentTransaction.objects.filter(
            tender_type=PaymentTransaction.TENDER_WALLET,
            transaction_type="authorize",
            status="authorized",
            created_at__lt=cutoff,
        ).update(status="voided")
        if count:
            logger.info(f"Expired {count} stale wallet hold(s) older than {cls.HOLD_MINUTES}m")
        return count

    # ------------------------------------------------------------------
    # refund
    # ------------------------------------------------------------------

    @classmethod
    @db_transaction.atomic
    def refund_to_wallet(cls, capture, amount=None, reason="", refund_ref=None):
        """
        Return captured value to the wallet.

        Idempotency is an EXPLICIT pre-lookup on the refund id, not a
        rely-on-IntegrityError: WalletService.credit also bumps
        lifetime-credited counters, so the money side must not run at all on a
        retry — catching the constraint violation afterwards would be too late.

        Args:
            capture: the wallet capture being refunded.
            amount: Money to return; defaults to the full captured amount.
            reason: recorded on the ledger entry.
            refund_ref: the caller's Refund pk — required, same stance as the
                allocator: a missing identity is a programming error.
        """
        from django.db.models import Sum

        from payment_providers.models import PaymentTransaction
        from wallet.models import CustomerWallet
        from wallet.services import WalletService

        if refund_ref is None:
            raise WalletTenderError("refund_to_wallet requires refund_ref for idempotency")
        if capture.transaction_type not in ("capture", "charge"):
            raise WalletTenderError(f"Cannot refund a {capture.transaction_type} transaction")

        amount = amount or capture.amount
        if amount.currency != capture.amount.currency:
            raise WalletTenderError("Refund currency must match the capture")

        refund_id = f"wt-ref:{capture.transaction_id}:{refund_ref}"
        existing = PaymentTransaction.objects.filter(transaction_id=refund_id).first()
        if existing is not None:
            return existing

        # Capacity per capture row (I3), pending counted.
        already = PaymentTransaction.objects.filter(
            parent_transaction=capture,
            transaction_type="refund",
            status__in=("pending", "completed"),
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        if already + amount.amount > capture.amount.amount:
            raise WalletTenderError(
                f"Refunding {amount} would exceed the {capture.amount} captured "
                f"({already} already refunded)"
            )

        wallet = CustomerWallet.objects.select_for_update().get(pk=capture.wallet_id)
        if not wallet.is_active:
            # Same policy as deactivated gift cards (f17e1ef99): frozen is a
            # merchant decision; auto-crediting would hand back frozen value.
            # There is no bearer-instrument replacement to mint for a wallet —
            # the money belongs to this account or nowhere.
            raise WalletTenderError(
                f"Wallet {wallet.pk} is frozen; refund this leg by hand after "
                f"confirming it should be released"
            )

        WalletService.credit(
            wallet.customer,
            amount.amount,
            str(amount.currency),
            "refund",
            reason or f"Refund of {capture.transaction_id}",
            reference_id=refund_id,
        )

        return PaymentTransaction.objects.create(
            transaction_id=refund_id,
            tender_type=PaymentTransaction.TENDER_WALLET,
            transaction_type="refund",
            status="completed",
            wallet=wallet,
            order=capture.order,
            parent_transaction=capture,
            amount=amount,
            settlement_amount=amount,
            exchange_rate=capture.exchange_rate,
            provider_account=None,
            completed_at=timezone.now(),
        )
