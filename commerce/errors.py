"""Exceptions raised by the commerce service layer."""

from __future__ import annotations


class CommerceError(Exception):
    """Base class for every error raised by `commerce`."""


class QuoteDriftError(CommerceError):
    """
    A caller asserted a price and a fresh quote disagreed.

    Raised -- rather than returned -- because a caller that states an expected
    total and gets a different one has a broken contract, not a user-facing
    event. A customer whose cart merely changed under them gets a soft refusal
    instead, so they can re-review.
    """

    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual
        super().__init__(f"Quote drift: caller expected {expected}, fresh quote is {actual}")
