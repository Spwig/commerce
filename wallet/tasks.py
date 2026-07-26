"""Celery tasks for the wallet app."""

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="wallet.reconcile_wallet_balances", ignore_result=True)
def reconcile_wallet_balances():
    """
    Nightly I5 check: every wallet balance equals its signed ledger sum.

    Read-only — this task never fixes. Drift here means a money-movement bug
    landed somewhere upstream, and the right response is a human reading the
    log, not an automatic re-stamp that erases the evidence.
    """
    from django.core.management import call_command

    try:
        call_command("reconcile_wallet_balances")
        logger.info("Wallet reconciliation clean")
        return True
    except SystemExit:
        logger.error(
            "WALLET DRIFT DETECTED: stored balances disagree with their ledgers. "
            "Run `manage.py reconcile_wallet_balances` for detail; --fix only "
            "after understanding the cause."
        )
        return False
