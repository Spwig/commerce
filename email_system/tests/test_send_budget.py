"""Per-account SMTP send budget (transactional-first throttling)."""

from django.test import TestCase, override_settings

from email_system.services import send_budget


class SendBudgetTests(TestCase):
    ACCT = "budget-test-acct"

    def setUp(self):
        # Real Redis (cache backend); clear this account's current-window key so each
        # test starts from zero.
        try:
            send_budget._redis().delete(send_budget._key(self.ACCT))
        except Exception:
            self.skipTest("Redis not available")

    def test_disabled_budget_allows_everything(self):
        # ceiling unset (0) → no throttling, records are no-ops.
        for _ in range(100):
            self.assertTrue(send_budget.try_marketing_send(self.ACCT))
        send_budget.note_transactional_send(self.ACCT)  # no error

    @override_settings(
        EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE=5, EMAIL_TRANSACTIONAL_RESERVE_PER_MINUTE=2
    )
    def test_marketing_capped_at_ceiling_minus_reserve(self):
        # cap = 5 - 2 = 3 marketing sends per minute.
        allowed = [send_budget.try_marketing_send(self.ACCT) for _ in range(5)]
        self.assertEqual(allowed, [True, True, True, False, False])

    @override_settings(
        EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE=5, EMAIL_TRANSACTIONAL_RESERVE_PER_MINUTE=2
    )
    def test_transactional_load_reduces_marketing_headroom(self):
        # cap = 3, but two transactional sends already consumed the window → marketing
        # gets only 1 before hitting the cap.
        send_budget.note_transactional_send(self.ACCT)
        send_budget.note_transactional_send(self.ACCT)
        allowed = [send_budget.try_marketing_send(self.ACCT) for _ in range(3)]
        self.assertEqual(allowed, [True, False, False])

    @override_settings(
        EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE=3, EMAIL_TRANSACTIONAL_RESERVE_PER_MINUTE=1
    )
    def test_transactional_is_never_blocked(self):
        # Marketing is capped at 2, but transactional keeps going regardless.
        for _ in range(10):
            send_budget.note_transactional_send(self.ACCT)  # never raises / never blocks
        # And marketing is now fully shut out (transactional load exceeded the cap).
        self.assertFalse(send_budget.try_marketing_send(self.ACCT))

    @override_settings(
        EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE=2, EMAIL_TRANSACTIONAL_RESERVE_PER_MINUTE=0
    )
    def test_accounts_are_isolated(self):
        other = "budget-test-acct-2"
        send_budget._redis().delete(send_budget._key(other))
        self.assertTrue(send_budget.try_marketing_send(self.ACCT))
        self.assertTrue(send_budget.try_marketing_send(self.ACCT))
        self.assertFalse(send_budget.try_marketing_send(self.ACCT))  # ACCT exhausted
        self.assertTrue(send_budget.try_marketing_send(other))  # other unaffected
