"""
GDPR erasure: anonymise the person, keep the money.

The right to erasure (Art. 17) is not absolute — Art. 17(3)(b) exempts data
retained under a legal obligation, and financial record-keeping is the
canonical case (EU merchants must keep transaction records 6–10 years). So the
correct pattern, and the one major platforms use, is anonymise-in-place:

* Identity fields are blanked. The person is gone.
* Orders, tender rows and the wallet ledger keep their FKs to the anonymised
  rows, so the money graph stays fully walkable — an auditor can verify every
  pound by order number and ledger id. They just can't learn the customer's
  name, which is precisely what erasure demanded.
* Identity trace-back is deliberately impossible. A reversible key would be
  pseudonymisation — still personal data, request not honoured.

THE BALANCE GUARD is the part that is easy to get wrong: a wallet balance is
money owed TO the customer, and anonymising an account holding £40 silently
destroys a liability. Erasure is a privacy action; forfeiting money is an
accounting decision a human makes explicitly. So this refuses while the wallet
holds a balance unless the caller passes ``forfeit_balance=True``, and a
forfeit is written as a ledger debit — invariant I5 holds through erasure.

Raw ``User.delete()`` on an account with tender history now raises
ProtectedError (PaymentTransaction.wallet is PROTECT), which Django admin
surfaces as a blocked deletion — this service is the sanctioned path.
"""

import logging

from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)


class AnonymiseError(Exception):
    """The account cannot be anonymised as requested."""


class WalletHoldsBalance(AnonymiseError):
    """The wallet still owes the customer money — a human must decide."""


def anonymise_customer(user, performed_by=None, forfeit_balance=False):
    """
    Erase a customer's identity while keeping the financial records lawful
    retention requires.

    Args:
        user: the customer to anonymise.
        performed_by: staff user actioning the request (audit trail).
        forfeit_balance: explicitly zero a remaining wallet balance via a
            ledger debit before freezing. Without it, a non-zero balance
            refuses — see WalletHoldsBalance.

    Returns:
        dict summarising what was done, for the caller's messaging.

    Raises:
        WalletHoldsBalance: wallet balance > 0 and forfeit_balance is False.
        AnonymiseError: staff/superuser accounts are refused outright.
    """
    from wallet.models import CustomerWallet
    from wallet.services import WalletService

    if user.is_staff or user.is_superuser:
        # Erasing a staff account is an org-structure change, not a customer
        # privacy request; doing it through this path would also anonymise
        # audit trails that point AT the staff member.
        raise AnonymiseError("Staff accounts cannot be anonymised through this flow")

    summary = {"user_id": user.pk, "wallet": None, "forfeited": None}

    with transaction.atomic():
        wallet = CustomerWallet.objects.select_for_update().filter(customer=user).first()

        if wallet is not None:
            # Pending credit is money owed to the customer that has not yet
            # become spendable (e.g. inside a refund window). The forfeit path
            # below is a ledger debit against available_balance and has no way
            # to zero pending, so a wallet holding pending credit must have it
            # resolved — matured to available then forfeited, or reversed —
            # before erasure. Freezing it here would strand that liability.
            pending = wallet.pending_balance
            if pending.amount > 0:
                raise WalletHoldsBalance(
                    f"Wallet holds {pending} in pending credit the store may "
                    f"still owe this customer. Resolve it (let it mature and "
                    f"forfeit, or reverse it) before erasing."
                )

            balance = wallet.available_balance
            if balance.amount > 0:
                if not forfeit_balance:
                    raise WalletHoldsBalance(
                        f"Wallet holds {balance} the store still owes this "
                        f"customer. Refund it, or re-run with explicit "
                        f"forfeiture, before erasing."
                    )
                # Forfeit as a ledger debit, never a raw zeroing: the nightly
                # reconciler (I5) must still find balance == signed ledger sum
                # after the person is gone.
                WalletService.debit(
                    user,
                    balance.amount,
                    str(balance.currency),
                    "manual",
                    "Balance forfeited on account erasure (GDPR)",
                )
                summary["forfeited"] = str(balance)

            wallet.refresh_from_db()
            wallet.is_active = False
            wallet.save(update_fields=["is_active", "updated_at"])
            summary["wallet"] = wallet.pk

        # Blank identity. The pk survives so financial rows keep joining;
        # the placeholder is derived from it, carries nothing personal, and
        # keeps username/email unique.
        placeholder = f"erased-{user.pk}"
        user.username = placeholder
        user.email = f"{placeholder}@anonymised.invalid"
        user.first_name = ""
        user.last_name = ""
        user.is_active = False
        user.set_unusable_password()
        user.save()

    # The erasure event is itself a compliance record — logged with row ids
    # only, no erased PII.
    logger.info(
        f"Anonymised customer {user.pk} "
        f"(wallet={summary['wallet']}, forfeited={summary['forfeited']}, "
        f"by={getattr(performed_by, 'pk', None)} at {timezone.now().isoformat()})"
    )
    return summary
