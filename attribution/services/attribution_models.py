"""The attribution models — pure functions that split 1.0 across a journey.

Each takes the ordered touch list (oldest → newest) and returns a list of
``(touchpoint, weight)`` whose weights sum to exactly ``1`` (the last weight
absorbs any rounding remainder so the split is exact). Adding a model here and
registering it in ``constants.ATTRIBUTION_MODEL_CHOICES`` is all it takes — no
data migration, because attribution is a recomputable projection over the
retained touch stream.
"""

from decimal import Decimal

from attribution.constants import (
    MODEL_FIRST_TOUCH,
    MODEL_LAST_NON_DIRECT,
    MODEL_LINEAR,
    MODEL_POSITION_BASED,
    MODEL_TIME_DECAY,
)

ONE = Decimal("1")
WEIGHT_Q = Decimal("0.00000001")  # 8dp, matches Attribution.weight field


def _finalize(touches, raw):
    """Normalise raw weights to sum to exactly 1 and pair with touches."""
    total = sum(raw)
    if total <= 0:
        # Degenerate (should not happen) — fall back to equal split.
        raw = [ONE for _ in touches]
        total = Decimal(len(touches))
    weights = [(w / total).quantize(WEIGHT_Q) for w in raw]
    # Absorb rounding drift into the last element so the sum is exactly 1.
    drift = ONE - sum(weights)
    weights[-1] = (weights[-1] + drift).quantize(WEIGHT_Q)
    return list(zip(touches, weights, strict=True))


def _last_non_direct(touches, order_time, half_life_days):
    # Every recorded touch is non-direct by capture design, so this is simply
    # the most recent touch.
    raw = [Decimal("0")] * len(touches)
    raw[-1] = ONE
    return _finalize(touches, raw)


def _first_touch(touches, order_time, half_life_days):
    raw = [Decimal("0")] * len(touches)
    raw[0] = ONE
    return _finalize(touches, raw)


def _linear(touches, order_time, half_life_days):
    raw = [ONE for _ in touches]
    return _finalize(touches, raw)


def _time_decay(touches, order_time, half_life_days):
    half_life = Decimal(str(max(half_life_days, 1)))
    raw = []
    for t in touches:
        age_days = Decimal(str((order_time - t.occurred_at).total_seconds() / 86400.0))
        # 2 ** (-age/half_life)
        raw.append(Decimal(2) ** (-(age_days / half_life)))
    return _finalize(touches, raw)


def _position_based(touches, order_time, half_life_days):
    n = len(touches)
    if n == 1:
        raw = [ONE]
    elif n == 2:
        raw = [Decimal("0.5"), Decimal("0.5")]
    else:
        middle = Decimal("0.2") / Decimal(n - 2)
        raw = [middle] * n
        raw[0] = Decimal("0.4")
        raw[-1] = Decimal("0.4")
    return _finalize(touches, raw)


_MODELS = {
    MODEL_LAST_NON_DIRECT: _last_non_direct,
    MODEL_FIRST_TOUCH: _first_touch,
    MODEL_LINEAR: _linear,
    MODEL_TIME_DECAY: _time_decay,
    MODEL_POSITION_BASED: _position_based,
}


def compute_weights(touches, model, order_time, half_life_days=7):
    """Split 1.0 across ``touches`` under ``model``.

    ``touches`` must be ordered oldest → newest. Returns ``[(touch, weight)]``
    summing to exactly 1. Unknown models fall back to last-non-direct.
    """
    if not touches:
        return []
    fn = _MODELS.get(model, _last_non_direct)
    return fn(touches, order_time, half_life_days)
