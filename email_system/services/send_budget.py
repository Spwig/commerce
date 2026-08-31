"""Per-account SMTP send budget — keeps marketing from starving transactional mail.

A merchant's own SMTP / gateway has finite throughput. Marketing (campaigns and
journeys) must never consume so much of it that transactional mail (order
confirmations, password resets) gets deferred at the provider. A per-account,
per-minute counter in Redis enforces that: marketing may send only while the total
sends this minute stay under ``ceiling - reserve``; transactional always sends and
is still counted, so a burst of transactional mail makes marketing yield *more*.
This guarantees at least ``reserve`` sends/minute of headroom for transactional and
throttles marketing to ``ceiling - reserve``. NOTE: transactional is never blocked,
so total sends CAN exceed ``ceiling`` during a transactional burst — set the ceiling
below the provider's hard limit with margin. This protects transactional from
marketing, not the provider from a transactional spike.

Opt-in: a no-op that allows everything unless ``EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE``
is set — the platform can't guess a merchant's SMTP limit. Fails OPEN on any Redis
hiccup (email delivery must never hinge on the budget's own availability).
"""

import logging
import time

from django.conf import settings

logger = logging.getLogger("email_system")

# Atomically reserve a MARKETING slot: allow (and INCR) only while the minute's
# running total is under the marketing cap. Returns 1 (allowed) or 0 (defer).
_TRY_MARKETING_LUA = """
local used = tonumber(redis.call('GET', KEYS[1]) or '0')
if used >= tonumber(ARGV[1]) then
  return 0
end
local n = redis.call('INCR', KEYS[1])
if n == 1 then
  redis.call('EXPIRE', KEYS[1], tonumber(ARGV[2]))
end
return 1
"""

# Count a send and (atomically) set the window TTL if this created the key — so a
# first-writer crash between INCR and EXPIRE can't orphan a no-TTL key forever.
_NOTE_LUA = """
local n = redis.call('INCR', KEYS[1])
if n == 1 then
  redis.call('EXPIRE', KEYS[1], tonumber(ARGV[1]))
end
return n
"""

_WINDOW_TTL = 120  # seconds — two 60s windows, self-cleaning


def _ceiling():
    raw = getattr(settings, "EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE", None)
    try:
        return int(raw) if raw else 0
    except (TypeError, ValueError):
        return 0


def _reserve():
    try:
        return max(0, int(getattr(settings, "EMAIL_TRANSACTIONAL_RESERVE_PER_MINUTE", 0) or 0))
    except (TypeError, ValueError):
        return 0


def _key(account_id):
    return f"emailbudget:{account_id}:{int(time.time() // 60)}"


def _redis():
    from django_redis import get_redis_connection

    return get_redis_connection("default")


def try_marketing_send(account_id) -> bool:
    """Reserve one marketing send slot for this account this minute.

    True → a slot was atomically reserved (proceed). False → the marketing cap
    (``ceiling - reserve``) is reached; the caller must defer (leave the row queued).
    Always True when the budget is disabled or the account is unknown.
    """
    ceiling = _ceiling()
    if not ceiling or not account_id:
        return True
    cap = max(0, ceiling - _reserve())
    try:
        allowed = _redis().eval(_TRY_MARKETING_LUA, 1, _key(account_id), cap, _WINDOW_TTL)
        return bool(allowed)
    except Exception:  # noqa: BLE001 — never block a send on the budget's own failure
        logger.warning("Send-budget marketing check failed; allowing", exc_info=True)
        return True


def note_transactional_send(account_id) -> None:
    """Count a transactional send against the account's per-minute window.

    Transactional mail is never blocked, but it must consume budget so marketing
    (which checks the same counter) yields more headroom when transactional is busy.
    """
    if not _ceiling() or not account_id:
        return
    try:
        _redis().eval(_NOTE_LUA, 1, _key(account_id), _WINDOW_TTL)
    except Exception:  # noqa: BLE001 — recording is best-effort
        logger.warning("Send-budget transactional record failed", exc_info=True)
