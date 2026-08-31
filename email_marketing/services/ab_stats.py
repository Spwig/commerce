"""Statistical significance for A/B tests — a two-proportion z-test.

Lets a merchant trust a winner only when the data supports it: given the two
leading arms' engagement, return the confidence their true rates differ, so a
lucky split on a small audience isn't mistaken for a real result. Pure stdlib
(``statistics.NormalDist`` for the normal CDF) — no third-party dependency.
"""

import math
from statistics import NormalDist

_NORMAL = NormalDist()

# The normal approximation behind the z-test only holds with enough events per
# arm. Below this many expected events (and non-events) under the pooled rate, a
# lopsided tiny sample can read as "significant" when it isn't — so we call that
# "not enough data yet" rather than trusting the figure.
MIN_EXPECTED_PER_ARM = 5


def two_proportion_confidence(successes_a, n_a, successes_b, n_b) -> float:
    """Confidence in [0, 1] that two proportions differ (pooled two-proportion z-test).

    Two-sided: ``1 - p_value``. Returns 0.0 when either arm has no recipients or
    there is nothing to distinguish (both all-miss or both all-hit).
    """
    if n_a <= 0 or n_b <= 0:
        return 0.0
    pooled = (successes_a + successes_b) / (n_a + n_b)
    if pooled <= 0.0 or pooled >= 1.0:
        return 0.0
    se = math.sqrt(pooled * (1.0 - pooled) * (1.0 / n_a + 1.0 / n_b))
    if se == 0.0:
        return 0.0
    z = abs(successes_a / n_a - successes_b / n_b) / se
    return max(0.0, min(1.0, 2.0 * _NORMAL.cdf(z) - 1.0))


def is_reliable(successes_a, n_a, successes_b, n_b) -> bool:
    """Whether there's enough data for the confidence figure to be trustworthy.

    Each arm needs at least ``MIN_EXPECTED_PER_ARM`` expected events *and*
    non-events under the pooled rate. When this fails, a tiny lopsided split can
    look "significant" — so the result should read as "not enough data" instead
    of a verdict.
    """
    if n_a <= 0 or n_b <= 0:
        return False
    pooled = (successes_a + successes_b) / (n_a + n_b)
    for n in (n_a, n_b):
        if n * pooled < MIN_EXPECTED_PER_ARM or n * (1.0 - pooled) < MIN_EXPECTED_PER_ARM:
            return False
    return True


def assess(winner, variants, metric) -> dict:
    """How confident we are the winner beat its closest rival — and if we can trust it.

    The A/B decision is "is the leader ahead of the next best?", so this compares
    the winner against the highest-rate other arm (a two-arm test is the common
    case). Returns ``{"confidence": float in [0, 1], "reliable": bool}``:
    ``reliable`` is False when the sample was too small for the confidence figure
    to mean anything, so the caller can say "not enough data" instead of a verdict.
    """
    from email_marketing.models import ABTest

    rivals = [v for v in variants if v.id != winner.id]
    if not rivals:
        return {"confidence": 0.0, "reliable": False}
    runner_up = max(rivals, key=lambda v: v.rate(metric))

    def _successes(variant):
        return variant.clicked if metric == ABTest.METRIC_CLICKS else variant.opened

    w_succ, w_n = _successes(winner), winner.recipients
    r_succ, r_n = _successes(runner_up), runner_up.recipients
    return {
        "confidence": two_proportion_confidence(w_succ, w_n, r_succ, r_n),
        "reliable": is_reliable(w_succ, w_n, r_succ, r_n),
    }
