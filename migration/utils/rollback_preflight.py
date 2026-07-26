"""
Rollback preflight: work out what a migration rollback can safely delete.

A migration rollback must remove what the import created without touching
anything else in the store. That is harder than filtering on provenance alone,
because rows the import created can become load-bearing afterwards: a customer
places a real order, a merchant puts an imported product in a bundle, an
imported image gets attached to the merchant's own category.

The database already encodes those relationships as PROTECT foreign keys, so
this module derives the answer from the FK graph rather than from a hand-written
list of models. Hand-written lists drift behind the schema; there are 24 PROTECT
edges into the models a rollback touches, spread across catalog, orders,
shipping, loyalty, pos_app, configurator_3d and customizable_product.

The rule
--------
A row may be deleted only if every PROTECT reference to it comes from a row that
is also being deleted. Applied to a fixpoint, this yields:

* nothing outside the migration is ever deleted;
* every PROTECT constraint is satisfied by construction, so the delete cannot
  fail partway through and abort the surrounding transaction;
* whatever is retained is reported, with the reason.

Retention is transitive. If an imported product is kept because a real order
references it, the product's category is kept too (Product.category is PROTECT),
and so is that category's ancestor chain, and so are the media assets its images
point at. The fixpoint loop below produces that closure without naming any of
those models.
"""

import logging
from collections import defaultdict

from django.db import models
from django.db.models.deletion import get_candidate_relations_to_delete

logger = logging.getLogger(__name__)


def _incoming_relations(model):
    """Relations Django's deleter would follow into `model`.

    Uses Django's own helper rather than `_meta.related_objects`, which silently
    omits hidden reverse relations — those declared with related_name="+".
    MediaAsset alone has 13 such edges, and two of them matter here:
    customizable_product.CustomFont.regular is PROTECT (missing it produces a
    plan that dies at execution and can never succeed), and pos_app.PromoSlide
    .image is CASCADE (missing it destroys a merchant's promo slide without
    listing it on the confirmation screen).

    This module reimplements the Collector's traversal, so it has to follow the
    same edges the Collector does or the two silently diverge.
    """
    return get_candidate_relations_to_delete(model._meta)


# Keep well clear of PostgreSQL's 65,535 bind-parameter ceiling on the extended
# protocol. A large catalogue migration can exceed it in a single IN clause.
_CHUNK = 10_000


def _chunked(pks):
    """Yield pk batches small enough for an IN clause."""
    pks = list(pks)
    for i in range(0, len(pks), _CHUNK):
        yield pks[i : i + _CHUNK]


def _pks_referencing(model, field_name, target_pks, exclude_pks=None):
    """Return pks of `model` rows whose `field_name` points into `target_pks`.

    Uses the base manager so soft-delete managers cannot hide rows. A hidden row
    still holds a real FK and still protects its target.
    """
    found = set()
    exclude_pks = exclude_pks or set()
    for batch in _chunked(target_pks):
        qs = model._base_manager.filter(**{f"{field_name}__in": batch})
        found.update(qs.values_list("pk", flat=True))
    return found - exclude_pks


def cascade_closure(seeds):
    """Expand `seeds` into everything that would disappear with them.

    `seeds` maps model class -> set of pks. Returns the same shape, including
    every row reachable through a CASCADE foreign key.

    This is deliberately not django.db.models.deletion.Collector. Collector
    raises ProtectedError as soon as it meets a PROTECT edge, even when the
    protecting row is itself part of the same delete — which is exactly the
    situation a rollback is in (an imported order's items protect the imported
    products). We need the traversal without the veto.
    """
    closure, _ = cascade_closure_with_ancestry(seeds)
    return closure


def cascade_closure_with_ancestry(seeds):
    """Like `cascade_closure`, but also reports where each row came from.

    Returns (closure, ancestry). `ancestry` maps (model, pk) to the (model, pk)
    seed it descends from.

    The ancestry is what makes the retention fixpoint sound. When a row is
    blocked by a surviving PROTECT reference, it is often not a seed but a
    cascade descendant of one — a migrated customer's wallet, say, held by a
    wallet transaction. Such a row cannot be withdrawn from the delete set
    directly, because nothing put it there; the only way to spare it is to spare
    the ancestor that would have cascaded into it. Without this mapping the
    blocked row is silently ignored, the loop settles on a plan that still
    violates PROTECT, and the delete aborts at execution time.
    """
    closure = {m: set(pks) for m, pks in seeds.items() if pks}
    frontier = {m: set(pks) for m, pks in closure.items()}

    ancestry = {}
    for model, pks in closure.items():
        for pk in pks:
            ancestry[(model, pk)] = (model, pk)

    while frontier:
        next_frontier = defaultdict(set)

        for model, pks in frontier.items():
            for rel in _incoming_relations(model):
                if rel.field.remote_field.on_delete is not models.CASCADE:
                    continue

                child = rel.related_model
                already = closure.get(child, set())
                field = child._meta.get_field(rel.field.name)

                for batch in _chunked(pks):
                    rows = child._base_manager.filter(
                        **{f"{rel.field.name}__in": batch}
                    ).values_list("pk", field.attname)

                    for child_pk, parent_pk in rows:
                        if child_pk in already or (child, child_pk) in ancestry:
                            continue
                        ancestry[(child, child_pk)] = ancestry.get(
                            (model, parent_pk), (model, parent_pk)
                        )
                        closure.setdefault(child, set()).add(child_pk)
                        next_frontier[child].add(child_pk)

        frontier = next_frontier

    return closure, ancestry


def protect_edges_into(models_of_interest):
    """Return the PROTECT edges pointing at any model in `models_of_interest`.

    Yields (target_model, referring_model, field_name).
    """
    edges = []
    for target in models_of_interest:
        for rel in _incoming_relations(target):
            if rel.field.remote_field.on_delete is models.PROTECT:
                edges.append((target, rel.related_model, rel.field.name))
    return edges


def find_blocked(planned):
    """Find rows in `planned` that a surviving row protects.

    `planned` is the full cascade closure of the delete. A row is blocked when
    something outside that closure holds a PROTECT reference to it.

    Returns model -> {pk: reason}, where reason names the referring model so the
    merchant can be told why an item was kept.
    """
    blocked = defaultdict(dict)

    for target, referrer, field_name in protect_edges_into(planned.keys()):
        target_pks = planned.get(target)
        if not target_pks:
            continue

        doomed_referrers = planned.get(referrer, set())
        field = referrer._meta.get_field(field_name)

        for batch in _chunked(target_pks):
            qs = referrer._base_manager.filter(**{f"{field_name}__in": batch})

            # Filter the doomed referrers out in Python rather than with
            # exclude(pk__in=...): that set can be far larger than the
            # bind-parameter ceiling, and chunking an exclude is not a simple
            # union the way chunking a filter is.
            for referrer_pk, blocked_pk in qs.values_list("pk", field.attname):
                if blocked_pk is None or referrer_pk in doomed_referrers:
                    continue
                blocked[target].setdefault(blocked_pk, referrer._meta.label)

    return blocked


class RetentionPlan:
    """What a rollback will delete, what it will keep, and why."""

    def __init__(self, deletable, retained):
        # model -> set of pks that are safe to delete
        self.deletable = deletable
        # model -> {pk: label of the model that protects it}
        self.retained = retained

    def pks(self, model):
        return self.deletable.get(model, set())

    def retained_counts(self):
        """model label -> (count kept, protecting model label)."""
        out = {}
        for model, entries in self.retained.items():
            if not entries:
                continue
            reasons = sorted(set(entries.values()))
            out[model._meta.label] = (len(entries), reasons)
        return out

    @property
    def has_retentions(self):
        return any(entries for entries in self.retained.values())


def build_retention_plan(seeds, max_passes=25, carry_retained=None):
    """Reduce `seeds` to the subset that can be deleted without breaking PROTECT.

    Iterates because retention propagates: keeping an order keeps its items,
    which keeps the products they reference, which keeps those products'
    categories, and so on up the graph. Each pass removes newly blocked rows and
    re-expands the cascade closure over what remains.
    """
    deletable = {m: set(pks) for m, pks in seeds.items() if pks}

    # Retention decisions from an earlier pass must be carried forward, not
    # recomputed. A later pass starts from the previous pass's delete set, so
    # rows already withdrawn are simply absent and would otherwise vanish from
    # the report — telling the merchant nothing was kept when things were.
    retained = defaultdict(dict)
    for model, entries in (carry_retained or {}).items():
        retained[model].update(entries)

    for pass_no in range(max_passes):
        planned, ancestry = cascade_closure_with_ancestry(deletable)
        blocked = find_blocked(planned)

        progress = False
        for model, entries in blocked.items():
            for pk, reason in entries.items():
                # A blocked seed is withdrawn directly.
                if pk in deletable.get(model, set()):
                    target_model, target_pk = model, pk
                else:
                    # A blocked cascade descendant cannot be withdrawn — nothing
                    # put it in the set. Spare the seed it descends from, which
                    # is the only thing that would have cascaded into it.
                    target_model, target_pk = ancestry.get((model, pk), (None, None))
                    if target_model is None or target_pk not in deletable.get(target_model, set()):
                        continue

                deletable[target_model].discard(target_pk)
                retained[target_model].setdefault(target_pk, reason)
                progress = True

        if not progress:
            logger.info(
                "Rollback retention plan settled after %d pass(es): %d model(s) with retained rows",
                pass_no + 1,
                sum(1 for v in retained.values() if v),
            )
            return RetentionPlan(deletable, retained)

    # A fixpoint should be reached well inside max_passes; the graph is finite
    # and every pass strictly shrinks the delete set. Refuse rather than delete
    # against a plan we could not prove stable.
    raise RuntimeError(
        f"Rollback retention plan did not converge after {max_passes} passes. "
        "Refusing to delete against an unstable plan."
    )
