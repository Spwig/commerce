"""
WalletService under concurrency.

``debit()`` is a read-modify-write on money. Without ``select_for_update`` two
simultaneous debits both read the pre-deduction balance and the second write
overwrites the first — the same value gets spent twice and the wallet ends up
holding money the customer already used.

These tests need real threads against real connections, so they use
``django_db(transaction=True)``: the standard ``django_db`` wraps each test in
a transaction that other connections cannot see, which would make every worker
read an empty database.

Each worker closes its connection in a ``finally`` — a leaked connection holds
a row lock open and the next test blocks until the suite times out rather than
failing with anything readable.
"""

import threading
from decimal import Decimal

import pytest
from django.db import connection
from djmoney.money import Money

from tests.factories import UserFactory
from wallet.models import CustomerWallet, WalletTransaction
from wallet.services import InsufficientBalance, WalletService

pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.integration,
    pytest.mark.wallet,
]


def _run_concurrently(target, worker_count):
    """
    Run ``target(index)`` in ``worker_count`` threads released simultaneously.

    Returns a list of ``("ok", result)`` / ``("error", exception)`` tuples. A
    barrier gets every thread to the call site before any of them proceeds;
    without it the first thread routinely finishes before the second starts and
    the test silently stops testing concurrency at all.
    """
    results = []
    results_lock = threading.Lock()
    barrier = threading.Barrier(worker_count, timeout=20)

    def worker(index):
        try:
            barrier.wait()
            try:
                outcome = ("ok", target(index))
            except Exception as exc:  # noqa: BLE001 — classified by the caller
                outcome = ("error", exc)
            with results_lock:
                results.append(outcome)
        finally:
            connection.close()

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(worker_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30)

    assert not any(t.is_alive() for t in threads), (
        "A worker thread did not finish — most likely deadlocked on a row lock."
    )
    return results


@pytest.fixture(autouse=True)
def _site_settings_for_threads(django_db_setup, django_db_blocker):
    """
    ``transaction=True`` truncates tables between tests, so the SiteSettings
    row the autouse conftest fixture creates has to be re-established here in a
    way the worker threads' own connections can see (i.e. committed).
    """
    from core.models import SiteSettings

    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
            "default_language": "en",
        },
    )
    yield


class TestConcurrentDebits:
    def test_only_one_of_two_racing_debits_succeeds(self):
        """
        Balance covers exactly one of the two debits. Both threads read, both
        decide they can afford it, and only the row lock stops the second from
        spending money that is no longer there.
        """
        user = UserFactory()
        wallet = WalletService.get_or_create_wallet(user)
        wallet.available_balance = Money(Decimal("100.00"), "USD")
        wallet.save()

        def debit(index):
            return WalletService.debit(
                user,
                Decimal("80.00"),
                "USD",
                WalletTransaction.SOURCE_ORDER,
                f"Concurrent spend {index}",
            )

        results = _run_concurrently(debit, worker_count=2)

        successes = [r for kind, r in results if kind == "ok"]
        failures = [r for kind, r in results if kind == "error"]

        assert len(successes) == 1, (
            f"{len(successes)} debits of 80.00 succeeded against a 100.00 "
            "balance. The wallet was double-spent."
        )
        assert len(failures) == 1
        assert isinstance(failures[0], InsufficientBalance), (
            f"The losing debit failed with {type(failures[0]).__name__}: "
            f"{failures[0]}. Expected InsufficientBalance."
        )

        final = CustomerWallet.objects.get(pk=wallet.pk)
        assert final.available_balance == Money(Decimal("20.00"), "USD")
        assert final.lifetime_used == Money(Decimal("80.00"), "USD")

    def test_the_ledger_records_exactly_one_movement(self):
        user = UserFactory()
        wallet = WalletService.get_or_create_wallet(user)
        wallet.available_balance = Money(Decimal("100.00"), "USD")
        wallet.save()

        def debit(index):
            return WalletService.debit(
                user, Decimal("80.00"), "USD", WalletTransaction.SOURCE_ORDER, f"Spend {index}"
            )

        _run_concurrently(debit, worker_count=2)

        ledger = WalletTransaction.objects.filter(wallet=wallet)
        assert ledger.count() == 1, (
            "The refused debit still wrote a ledger row, so the ledger no "
            "longer reconciles to the balance."
        )
        assert ledger.first().balance_after == Money(Decimal("20.00"), "USD")

    def test_concurrent_credits_all_land(self):
        """
        Negative control for the lock: credits never fail on sufficiency, so if
        the serialisation works, five concurrent credits sum exactly. A lost
        update shows up here as a balance below 50.00.
        """
        user = UserFactory()
        wallet = WalletService.get_or_create_wallet(user)
        wallet.available_balance = Money(Decimal("0.00"), "USD")
        wallet.save()

        def credit(index):
            return WalletService.credit(
                user,
                Decimal("10.00"),
                "USD",
                WalletTransaction.SOURCE_PROMOTION,
                f"Concurrent credit {index}",
            )

        results = _run_concurrently(credit, worker_count=5)

        errors = [r for kind, r in results if kind == "error"]
        assert not errors, f"Credits failed unexpectedly: {errors}"

        final = CustomerWallet.objects.get(pk=wallet.pk)
        assert final.available_balance == Money(Decimal("50.00"), "USD"), (
            f"Balance is {final.available_balance}, expected 50.00 — a "
            "concurrent credit was lost to a read-modify-write race."
        )
        assert final.lifetime_credited == Money(Decimal("50.00"), "USD")
