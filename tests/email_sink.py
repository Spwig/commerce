"""
Shared email-sink oracle.

Spwig does not send order/refund/fulfilment mail through Django's mail
backend — ``mail.outbox`` is always empty. Every message is persisted as an
``email_system.EmailOutbox`` row and dispatched asynchronously. So a
lifecycle test must assert on ``EmailOutbox`` rows, and there was no shared
helper for it. ``EmailSink`` is that helper.

It never sends anything; it queries rows that the code under test created
inside the test's own transaction, so it is automatically isolated per test.

Assert on the message the customer/merchant would actually receive:
recipient, template, rendered subject/body content, exactly-once delivery,
and — crucially — that **no** mail went out when an order never completed.
"""

from __future__ import annotations


class EmailSink:
    """Query + assertion facade over ``EmailOutbox`` for a single test."""

    def _qs(self, *, to: str | None = None, template_type: str | None = None):
        from email_system.models import EmailOutbox

        qs = EmailOutbox.objects.all()
        if to is not None:
            qs = qs.filter(to_email=to)
        if template_type is not None:
            qs = qs.filter(template_type=template_type)
        return qs.order_by("created_at")

    def all(self, *, to: str | None = None, template_type: str | None = None) -> list:
        return list(self._qs(to=to, template_type=template_type))

    def count(self, *, to: str | None = None, template_type: str | None = None) -> int:
        return self._qs(to=to, template_type=template_type).count()

    def assert_sent(
        self,
        *,
        to: str,
        template_type: str | None = None,
        contains: str | list[str] | None = None,
        not_contains: str | list[str] | None = None,
        once: bool = True,
    ):
        """Assert a matching email exists (and, by default, exactly one).

        ``contains`` / ``not_contains`` are checked against subject + both
        body parts — use them to prove amounts/links render and, for
        ``not_contains``, that secrets/internal ids never leak into mail.
        Returns the matched row (or the newest, when ``once=False``).
        """
        rows = self.all(to=to, template_type=template_type)
        label = f"to={to!r}" + (f" template_type={template_type!r}" if template_type else "")
        if not rows:
            raise AssertionError(f"expected an email ({label}) but none was recorded")
        if once and len(rows) != 1:
            raise AssertionError(
                f"expected exactly one email ({label}) but found {len(rows)} — "
                "duplicate mail is a real defect (e.g. a replayed webhook)"
            )
        row = rows[-1]
        haystack = f"{row.subject}\n{row.html_body}\n{row.text_body}"
        for needle in _as_list(contains):
            if needle not in haystack:
                raise AssertionError(f"email ({label}) does not contain {needle!r}")
        for needle in _as_list(not_contains):
            if needle in haystack:
                raise AssertionError(
                    f"email ({label}) leaked {needle!r} — it must never appear in mail"
                )
        return row

    def assert_none(self, *, to: str | None = None, template_type: str | None = None) -> None:
        """Assert no matching email was recorded.

        The load-bearing case: an order that never completed must produce no
        confirmation mail. Called with no filters it asserts total silence.
        """
        rows = self.all(to=to, template_type=template_type)
        if rows:
            label = (
                ", ".join(
                    filter(
                        None,
                        [
                            f"to={to!r}" if to else "",
                            f"template_type={template_type!r}" if template_type else "",
                        ],
                    )
                )
                or "any"
            )
            raise AssertionError(
                f"expected no email ({label}) but found {len(rows)}: "
                f"{[(r.template_type, r.to_email) for r in rows]}"
            )


def _as_list(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)
