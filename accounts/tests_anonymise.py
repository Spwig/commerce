"""
GDPR erasure: anonymise the person, keep the money (P2.5a-7).

Two properties carry the risk:

* **The balance guard.** A wallet balance is money the store OWES the
  customer. Erasure is a privacy action; forfeiting money is an accounting
  decision — so a non-zero balance refuses unless forfeiture is explicit, and
  a forfeit is a ledger debit (I5 holds through erasure).
* **PROTECT beats CASCADE.** Deleting a user with wallet tender history would
  CASCADE into CustomerWallet and erase the audit trail of real payments; the
  PROTECT FK on PaymentTransaction.wallet blocks it, and this flow is the
  sanctioned alternative.
"""

from datetime import timedelta
from decimal import Decimal

import pytest
from django.db.models import ProtectedError
from django.utils import timezone
from djmoney.money import Money

from accounts.services.anonymise_service import (
    AnonymiseError,
    WalletHoldsBalance,
    anonymise_customer,
)
from tests.factories import CartFactory, UserFactory
from wallet.models import CustomerWallet, WalletTransaction
from wallet.services import WalletService

pytestmark = [pytest.mark.django_db, pytest.mark.r2]


@pytest.fixture(autouse=True)
def _site_settings(db):
    """Single-tenant fixture — wallet currency resolution needs SiteSettings."""
    from core.models import SiteSettings

    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
            "default_language": "en",
        },
    )
    return settings


def _customer_with_balance(amount="40.00"):
    user = UserFactory()
    if Decimal(amount) > 0:
        WalletService.credit(user, Decimal(amount), "USD", "manual", "seed")
    else:
        WalletService.get_or_create_wallet(user)
    return user


class TestRawDeletionIsBlocked:
    def test_deleting_a_user_with_tender_history_raises_protected(self):
        from cart.models import CheckoutSession
        from payment_providers.models import PaymentTransaction
        from wallet.tender_service import WalletTenderService

        user = _customer_with_balance("40.00")
        session = CheckoutSession.objects.create(
            cart=CartFactory(user=user),
            expires_at=timezone.now() + timedelta(hours=1),
        )
        session.total_amount = Money(Decimal("30.00"), "USD")
        session.save(update_fields=["total_amount"])
        WalletTenderService.authorize_for_session(session, user)

        with pytest.raises(ProtectedError):
            user.delete()

        assert PaymentTransaction.objects.filter(wallet__customer=user).exists()


class TestAnonymise:
    def test_refuses_while_the_wallet_holds_a_balance(self):
        user = _customer_with_balance("40.00")

        with pytest.raises(WalletHoldsBalance, match="owes this"):
            anonymise_customer(user)

        user.refresh_from_db()
        assert user.is_active is True, "A refused erasure must change nothing."
        assert "erased" not in user.username

    def test_explicit_forfeit_zeroes_via_the_ledger(self):
        """I5 must hold through erasure: the forfeit is a debit row, not a raw zero."""
        user = _customer_with_balance("40.00")

        summary = anonymise_customer(user, forfeit_balance=True)

        wallet = CustomerWallet.objects.get(customer=user)
        assert wallet.available_balance.amount == Decimal("0.00")
        assert wallet.is_active is False
        assert summary["forfeited"] == "$40.00"
        assert (
            WalletTransaction.objects.filter(
                wallet=wallet,
                transaction_type=WalletTransaction.TYPE_DEBIT,
                description__contains="forfeited",
            ).exists()
            or WalletTransaction.objects.filter(
                wallet=wallet,
                transaction_type=WalletTransaction.TYPE_DEBIT,
                description__contains="Forfeited",
            ).exists()
        )

    def test_identity_is_blanked_and_money_rows_still_join(self):
        user = _customer_with_balance("0.00")
        original_pk = user.pk

        anonymise_customer(user)

        user.refresh_from_db()
        assert user.pk == original_pk, "The pk must survive so financial rows join."
        assert user.username == f"erased-{original_pk}"
        assert user.email.endswith("@anonymised.invalid")
        assert user.first_name == "" and user.last_name == ""
        assert user.is_active is False
        assert not user.has_usable_password()
        # The wallet row survives, joined to the anonymised user.
        assert CustomerWallet.objects.filter(customer_id=original_pk).exists()

    def test_a_zero_balance_wallet_needs_no_forfeit_flag(self):
        user = _customer_with_balance("0.00")
        anonymise_customer(user)  # must not raise

    def test_staff_accounts_are_refused(self):
        staff = UserFactory(is_staff=True)

        with pytest.raises(AnonymiseError, match="Staff"):
            anonymise_customer(staff)
