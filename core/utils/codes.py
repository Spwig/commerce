"""
Shared generation of customer-facing redeemable codes.

Voucher codes, gift card codes, loyalty redemption codes and referral reward
codes are all bearer credentials: anyone who knows the string can spend the
value behind it. They must therefore be unguessable.

Before this module there were five independent generators, three of which used
``random`` (the Mersenne Twister). That PRNG is deterministic and its internal
state is recoverable from a modest number of observed outputs, so a customer who
collects a handful of their own codes can predict other customers'. One of the
five also had no uniqueness check at all, relying on a database
``IntegrityError`` to notice a collision.

Everything here uses :mod:`secrets`. Use these helpers rather than writing a
generator; if a new code format is needed, add it here.
"""

from __future__ import annotations

import secrets
import string
from collections.abc import Callable

# Uppercase alphanumerics minus the four characters people reliably mis-read or
# mis-type when copying a code off a screen, an email or a printed card.
UNAMBIGUOUS_ALPHABET = "".join(
    c for c in (string.ascii_uppercase + string.digits) if c not in "0O1I"
)

# Full uppercase alphanumeric set. Used where codes are machine-handled or where
# an existing format must be preserved exactly.
ALPHANUMERIC_ALPHABET = string.ascii_uppercase + string.digits

# Attempts before giving up on finding an unused code. Collisions are vanishingly
# rare at these lengths; repeated collisions mean the keyspace is too small or
# the uniqueness check is wrong, and both should surface loudly.
MAX_ATTEMPTS = 10


class CodeGenerationError(RuntimeError):
    """Raised when a unique code could not be generated within MAX_ATTEMPTS."""


def random_string(length: int, alphabet: str = ALPHANUMERIC_ALPHABET) -> str:
    """Return a cryptographically secure random string of ``length``."""
    if length < 1:
        raise ValueError("length must be >= 1")
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_unique_code(
    exists: Callable[[str], bool],
    *,
    length: int = 8,
    prefix: str = "",
    separator: str = "-",
    groups: int = 1,
    alphabet: str = ALPHANUMERIC_ALPHABET,
    max_attempts: int = MAX_ATTEMPTS,
) -> str:
    """
    Generate a code that ``exists`` reports as unused.

    Args:
        exists: Callable taking a candidate code and returning True if it is
            already taken. Typically ``lambda c: Model.objects.filter(code=c).exists()``.
        length: Characters per group.
        prefix: Optional leading segment, e.g. ``"GC"`` or ``"LOYALTY"``.
        separator: Joins prefix and groups.
        groups: Number of ``length``-character groups. ``groups=3, length=4``
            with prefix ``"GC"`` gives ``GC-XXXX-XXXX-XXXX``.
        alphabet: Character set to draw from.
        max_attempts: Attempts before raising.

    Returns:
        An unused code.

    Raises:
        CodeGenerationError: If no unused code was found. Callers should let
            this propagate — silently returning a duplicate would let two
            customers share one balance, and falling back to a UUID produces a
            code in a different format from every other code in the system.
    """
    if groups < 1:
        raise ValueError("groups must be >= 1")

    for _attempt in range(max_attempts):
        body = separator.join(random_string(length, alphabet) for _ in range(groups))
        code = f"{prefix}{separator}{body}" if prefix else body

        if not exists(code):
            return code

    raise CodeGenerationError(
        f"Could not generate a unique code after {max_attempts} attempts "
        f"(prefix={prefix!r}, length={length}, groups={groups}). The keyspace is "
        f"likely exhausted or the uniqueness check is wrong."
    )
