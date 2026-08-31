"""Email suppression (list hygiene) — the do-not-mail list and its writers.

A suppressed address must never receive marketing mail: a hard bounce, a spam
complaint, or a manual block. Suppression is keyed on the email ADDRESS (not a
Subscriber row), so it protects future/anonymous subscribers and is independent
of consent. ``suppress()`` is the single writer; the send path consults
``is_suppressed`` / ``suppressed_emails`` before queuing.
"""

import logging

logger = logging.getLogger("email_marketing")


def _normalise(email):
    return (email or "").strip().lower()


def is_suppressed(site, email):
    """True if this address is on the site's do-not-mail list."""
    from email_marketing.models import SuppressionEntry

    email = _normalise(email)
    if not email:
        return False
    return SuppressionEntry.objects.filter(site=site, email=email).exists()


def suppressed_emails(site):
    """The set of suppressed (lowercased) addresses for a site.

    Preload once per broadcast and test membership in-loop (O(1)) instead of a
    query per recipient.
    """
    from email_marketing.models import SuppressionEntry

    return set(SuppressionEntry.objects.filter(site=site).values_list("email", flat=True))


def suppress(site, email, reason, source=None, detail="", reflect=True):
    """Add (or refresh) an address on the do-not-mail list. Idempotent.

    When ``reflect`` (the default), also reflects the outcome onto the matching
    Subscriber: a hard/soft bounce flips an active subscriber to BOUNCED; a
    complaint flips it to COMPLAINED and forces an unsubscribe (so the address also
    drops out of the consent layer). A manual block suppresses sending without
    relabelling the subscriber.

    Pass ``reflect=False`` when the address has NO send trail on this install (e.g.
    a gateway-poll record with no matching outbox): the address-level block still
    stops sending, but a registered subscriber's status/consent is NOT changed off
    an unverified external address. Returns the ``SuppressionEntry`` (or None for a
    blank email).
    """
    from email_marketing.models import SuppressionEntry

    email = _normalise(email)
    if not email:
        return None

    source = source or SuppressionEntry.SOURCE_MANUAL
    # all_objects: re-suppressing a previously released (soft-deleted) address must
    # restore that row, not collide with the (site, email) unique constraint.
    entry, created = SuppressionEntry.all_objects.get_or_create(
        site=site,
        email=email,
        defaults={"reason": reason, "source": source, "detail": detail},
    )
    if not created:
        entry.reason = reason
        entry.source = source
        if detail:
            entry.detail = detail
        entry.is_deleted = False
        entry.deleted_at = None
        entry.deleted_by = None
        entry.save(
            update_fields=[
                "reason",
                "source",
                "detail",
                "is_deleted",
                "deleted_at",
                "deleted_by",
                "updated_at",
            ]
        )

    if reflect:
        _reflect_on_subscriber(site, email, reason)
    logger.info("Suppressed %s for site %s (%s, %s)", email, site.pk, reason, source)
    return entry


def release(site, email):
    """Lift the address-level block (soft-delete the entry). Idempotent.

    Removes the suppression gate only — a Subscriber previously flipped to
    BOUNCED/COMPLAINED keeps that status (re-activating a subscriber is a separate,
    deliberate action), so a released address sends again unless its subscriber is
    non-active for another reason.
    """
    from email_marketing.models import SuppressionEntry

    email = _normalise(email)
    entry = SuppressionEntry.objects.filter(site=site, email=email).first()
    if entry is not None:
        entry.delete()  # soft-delete
    return entry


def _reflect_on_subscriber(site, email, reason):
    """Best-effort: flip the matching Subscriber's status and, for a complaint,
    force an unsubscribe so the address also drops out of the consent layer."""
    from email_marketing.models import Subscriber, SuppressionEntry

    try:
        # Subscriber email casing is not guaranteed; match case-insensitively.
        sub = Subscriber.objects.filter(site=site, email__iexact=email).first()
        if sub is None:
            return
        if reason == SuppressionEntry.REASON_COMPLAINT:
            if sub.status != Subscriber.STATUS_COMPLAINED or sub.marketing_opt_in:
                sub.status = Subscriber.STATUS_COMPLAINED
                sub.marketing_opt_in = False
                sub.save(update_fields=["status", "marketing_opt_in", "updated_at"])
            _force_unsubscribe(sub)
        elif reason in (
            SuppressionEntry.REASON_HARD_BOUNCE,
            SuppressionEntry.REASON_SOFT_BOUNCE,
        ):
            if sub.status == Subscriber.STATUS_ACTIVE:
                sub.status = Subscriber.STATUS_BOUNCED
                sub.save(update_fields=["status", "updated_at"])
        # manual: the suppression entry alone gates sending; don't relabel.
    except Exception:  # noqa: BLE001 — reflection is best-effort
        logger.warning("Suppression subscriber-reflect failed for %s", email, exc_info=True)


def _force_unsubscribe(sub):
    """Mirror a complaint into the consent layer for a registered subscriber."""
    if not sub.user_id:
        return
    try:
        from accounts.services.preference_service import PreferenceService

        PreferenceService.unsubscribe_all(sub.user, reason="spam_complaint")
    except Exception:  # noqa: BLE001
        logger.warning("Complaint unsubscribe_all failed for %s", sub.email, exc_info=True)
