"""
Rollback utility for migration jobs.

Removes what a migration created, and only what a migration created.

Rows the import created can become load-bearing after go-live: a customer places
a real order against an imported product, a merchant files their own product
under an imported category. Anything in that position is *retained* rather than
deleted, together with everything it depends on, and reported back to the
merchant. See migration/utils/rollback_preflight.py for how that set is derived
from the foreign-key graph.

This is a compensating delete, not a database rollback. The import itself does
not run in a transaction; this undoes it after the fact.
"""

import logging

from django.db import transaction
from django.db.models import ProtectedError

from migration.utils.rollback_preflight import build_retention_plan

logger = logging.getLogger(__name__)

# Chunk deletes to stay clear of PostgreSQL's bind-parameter ceiling.
_CHUNK = 10_000


class RollbackRefused(Exception):
    """Raised when the rollback cannot be performed safely.

    Distinct from a generic failure so the admin can show the merchant why
    rather than surfacing a raw exception string.
    """


def _delete_in_chunks(model, pks):
    """Hard-delete `pks` of `model`, returning the number of rows removed.

    Always uses the base manager. Product and MediaAsset have soft-delete
    default managers whose delete() only sets a flag; that would leave the rows
    in place and the subsequent Category delete would then hit PROTECT.
    """
    if not pks:
        return 0

    total = 0
    pks = list(pks)
    for i in range(0, len(pks), _CHUNK):
        batch = pks[i : i + _CHUNK]
        # Count what the database actually removed for this model, not how many
        # ids were asked for — a row may already be gone, and an operator
        # reading these logs during an incident needs the real number. The
        # per-model breakdown is used because .delete() also reports cascaded
        # rows from other models.
        _, per_model = model._base_manager.filter(pk__in=batch).delete()
        total += per_model.get(model._meta.label, 0)
    return total


def _collect_seeds(job):
    """Everything this migration created, before retention is applied.

    Keyed by model class. Models carrying a migration_job foreign key are read
    directly; the rest are derived from those.
    """
    from django.contrib.auth import get_user_model

    from accounts.models import CustomerProfile
    from blog.models import BlogCategory, BlogPost, BlogTag
    from catalog.models import Category, Product, ProductReview
    from media_library.models import MediaAsset
    from orders.models import Order
    from subscriptions.models import SubscriptionPlan
    from vouchers.models import VoucherCode

    User = get_user_model()

    def by_job(model):
        return set(model._base_manager.filter(migration_job=job).values_list("pk", flat=True))

    seeds = {
        # Subscription plans are the only extension model needing explicit
        # provenance. Everything else the extension importer creates — booking
        # resources, bundle items, configuration slots, customisation options —
        # cascades from Product and is removed with it.
        SubscriptionPlan: by_job(SubscriptionPlan),
        Category: by_job(Category),
        Product: by_job(Product),
        ProductReview: by_job(ProductReview),
        Order: by_job(Order),
        VoucherCode: by_job(VoucherCode),
        MediaAsset: by_job(MediaAsset),
        BlogCategory: by_job(BlogCategory),
        BlogTag: by_job(BlogTag),
        BlogPost: by_job(BlogPost),
    }

    # Customer accounts. CustomerProfile carries the provenance; the User row is
    # what actually has to go, and CustomerProfile/Address/LoyaltyMember all
    # cascade from it.
    profile_user_ids = set(
        CustomerProfile._base_manager.filter(migration_job=job).values_list("user_id", flat=True)
    )

    # Affiliate accounts created by the WooCommerce bridge importer. These users
    # have no CustomerProfile, so provenance for them lives only in the manifest
    # the importer writes to connection_config.
    seeds.update(_affiliate_seeds(job))
    affiliate_user_ids = _affiliate_user_ids(job)

    candidate_user_ids = {uid for uid in (profile_user_ids | affiliate_user_ids) if uid}

    # Never delete a staff or superuser account, whatever the provenance says.
    #
    # Importers link an existing account when the source email matches, and older
    # jobs stamped migration_job on it — so a merchant or staff member sharing an
    # address with a source-store customer looks import-created. Deleting such an
    # account cascades its payment provider credentials, stored payment methods
    # and, through MigrationJob.created_by, that person's other migration records
    # — which SET_NULLs provenance on everything those jobs imported, store-wide.
    #
    # No import legitimately creates a privileged account, so excluding them
    # costs nothing and bounds the blast radius of a mis-stamped row.
    seeds[User] = set(
        User._base_manager.filter(pk__in=candidate_user_ids)
        .exclude(is_staff=True)
        .exclude(is_superuser=True)
        .values_list("pk", flat=True)
    )

    return seeds


def _affiliate_seeds(job):
    """Affiliate rows recorded in the importer's rollback manifest."""
    from affiliate.models import Affiliate, Program

    manifest = (job.connection_config or {}).get("affiliate_rollback_ids") or {}
    affiliate_ids = set(manifest.get("affiliate_ids") or [])
    program_ids = set(manifest.get("program_ids") or [])

    # Commissions, payouts and memberships all cascade from Affiliate/Program,
    # so seeding those two is sufficient. They are listed in the manifest too,
    # but deleting the parents is enough and avoids depending on the manifest
    # being complete.
    return {
        Affiliate: set(
            Affiliate._base_manager.filter(pk__in=affiliate_ids).values_list("pk", flat=True)
        ),
        Program: set(Program._base_manager.filter(pk__in=program_ids).values_list("pk", flat=True)),
    }


def _affiliate_user_ids(job):
    """User accounts the affiliate importer created.

    Read from the manifest's explicit user_ids rather than derived from the
    affiliate rows: the importer attaches an Affiliate to a pre-existing user
    when the email matches, and that account belongs to the merchant, not to
    the migration. Deleting it would destroy a real customer.
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()

    manifest = (job.connection_config or {}).get("affiliate_rollback_ids") or {}
    user_ids = set(manifest.get("user_ids") or [])
    if not user_ids:
        return set()

    # Confirm against the database so a stale or malformed manifest cannot name
    # rows that do not exist.
    return set(User._base_manager.filter(pk__in=user_ids).values_list("pk", flat=True))


def dependent_models():
    """Models whose rows are deleted because of who owns them, not provenance.

    Wallet transactions are deliberately NOT here. No importer creates a wallet
    or a wallet transaction — verified across migration/importers and
    migration/services — so every balance attached to a migrated customer is
    money the merchant granted after go-live: goodwill credit, a refund, a
    referral or promotion reward. None of it is an artefact of the import.

    Leaving them out means WalletTransaction's PROTECT edge to CustomerWallet
    keeps such a customer, which is the right outcome: a rollback should never
    destroy a real balance, and the customer is reported as kept.
    """
    from loyalty.models import LoyaltyRedemption, LoyaltyTransaction
    from shipping.models import Shipment

    return (LoyaltyRedemption, LoyaltyTransaction, Shipment)


def _dependent_seeds_for(user_ids, order_ids):
    """Rows that must go because the owner being deleted requires it.

    These follow their owner's fate rather than carrying provenance of their own:

    * LoyaltyTransaction and LoyaltyRedemption PROTECT LoyaltyMember, which
      cascades from User. They must be cleared for users actually being deleted
      — and left alone for a retained customer, whose points were earned on real
      orders.
    * Shipment PROTECTs Order, so shipments of deleted orders must go first.

    Recomputed on every pass of the planning loop. They cannot be derived once
    from a settled plan: the loyalty rows are the very thing that blocks the
    member, so omitting them causes the owner to be withdrawn, which then
    removes the reason to delete them — a cycle in which nothing is deleted.
    """
    from loyalty.models import LoyaltyMember, LoyaltyRedemption, LoyaltyTransaction
    from shipping.models import Shipment

    deleted_user_ids = user_ids
    deleted_order_ids = order_ids

    member_ids = (
        set(
            LoyaltyMember._base_manager.filter(customer_id__in=deleted_user_ids).values_list(
                "pk", flat=True
            )
        )
        if deleted_user_ids
        else set()
    )

    # Always return an entry for every dependent model, even when empty, so the
    # caller can drop rows whose owner has since been withdrawn.
    extra = {
        LoyaltyRedemption: set(),
        LoyaltyTransaction: set(),
        Shipment: set(),
    }

    if member_ids:
        extra[LoyaltyRedemption] = set(
            LoyaltyRedemption._base_manager.filter(member_id__in=member_ids).values_list(
                "pk", flat=True
            )
        )
        extra[LoyaltyTransaction] = set(
            LoyaltyTransaction._base_manager.filter(member_id__in=member_ids).values_list(
                "pk", flat=True
            )
        )

    if deleted_order_ids:
        extra[Shipment] = set(
            Shipment._base_manager.filter(order_id__in=deleted_order_ids).values_list(
                "pk", flat=True
            )
        )

    return extra


def _deletion_order():
    """Models in an order that satisfies every PROTECT edge between them.

    The retention plan guarantees nothing *outside* the delete set protects
    anything inside it. This ordering resolves the PROTECT edges *within* the
    set. Rows not listed here are removed by cascade from something that is.
    """
    from django.contrib.auth import get_user_model

    from affiliate.models import Affiliate, Program
    from blog.models import BlogCategory, BlogPost, BlogTag
    from catalog.models import Category, Product, ProductReview
    from loyalty.models import LoyaltyRedemption, LoyaltyTransaction
    from media_library.models import MediaAsset
    from orders.models import Order
    from shipping.models import Shipment
    from subscriptions.models import SubscriptionPlan
    from vouchers.models import VoucherCode

    return [
        # PROTECT LoyaltyMember, which cascades from User further down.
        (LoyaltyRedemption, "loyalty_redemptions"),
        (LoyaltyTransaction, "loyalty_transactions"),
        # Shipment PROTECTs Order.
        (Shipment, "shipments"),
        # Order cascades OrderItem, which PROTECTs Product — so orders must go
        # before products. OrderItem is never deleted directly.
        (Order, "orders"),
        (ProductReview, "reviews"),
        (VoucherCode, "coupons"),
        (BlogPost, "blog_posts"),
        (BlogTag, "blog_tags"),
        (BlogCategory, "blog_categories"),
        # Cascades its pricing tiers. Independent of Product, so ordering
        # relative to the catalogue does not matter.
        (SubscriptionPlan, "subscription_plans"),
        # Product cascades ProductImage, which PROTECTs MediaAsset — so products
        # must go before media assets.
        (Product, "products"),
        # Product.category PROTECTs Category.
        (Category, "categories"),
        # Cascades memberships, commissions and payouts.
        (Affiliate, "affiliates"),
        (Program, "affiliate_programs"),
        # Cascades CustomerProfile, Address, LoyaltyMember and Shipment.
        (get_user_model(), "customers"),
        # Last: the widest set of PROTECT referrers points here.
        (MediaAsset, "media_assets"),
    ]


def plan_rollback(job):
    """Work out what a rollback of `job` would do, without changing anything."""
    from django.contrib.auth import get_user_model

    from orders.models import Order

    User = get_user_model()

    provenance = _collect_seeds(job)

    # Seed owner-dependent rows from provenance up front, then reconcile them
    # against the settled plan and re-plan until both agree.
    #
    # They cannot be added only at the end. Loyalty transactions PROTECT the
    # member, which cascades from the customer, so leaving them out makes the
    # customer look undeletable — the planner withdraws them, which then removes
    # the reason to delete the transactions. Nothing is deleted and the whole
    # import survives its own rollback.
    #
    # Equally they cannot simply be seeded and left: once a customer is retained
    # for a genuine reason, their loyalty history must be spared with them.
    # Recomputing each pass converges on both.
    deletable = dict(provenance)
    for model, pks in _dependent_seeds_for(
        provenance.get(User, set()), provenance.get(Order, set())
    ).items():
        deletable[model] = set(pks)

    plan = build_retention_plan(deletable)

    for _ in range(10):
        wanted = _dependent_seeds_for(plan.pks(User), plan.pks(Order))
        current = {model: plan.pks(model) for model in dependent_models()}
        if all(wanted[model] == current[model] for model in dependent_models()):
            return plan

        next_deletable = dict(plan.deletable)
        for model in dependent_models():
            next_deletable[model] = set(wanted[model])

        plan = build_retention_plan(next_deletable, carry_retained=plan.retained)

    # Do not fall back to the last plan. Its dependent rows were derived from the
    # previous, larger owner set and never re-filtered, so it can delete the
    # loyalty points and store credit of a customer the same plan decided to
    # keep. Refuse instead — an unrunnable rollback is recoverable, a customer
    # silently stripped of their balance is not.
    raise RollbackRefused(
        "Spwig could not work out a safe set of data to remove for this "
        "migration. Nothing has been deleted. Please report this."
    )


def summarise(plan):
    """Merchant-facing summary of a plan: what goes, what stays and why.

    Reports the whole cascade closure, not only the models deleted explicitly.
    A customer account cascades into wallets, stored payment methods and
    subscriptions; listing just "customers" would understate what confirming
    this actually destroys, which is the one thing a consent screen must not do.
    """
    from migration.utils.rollback_preflight import cascade_closure

    closure = cascade_closure(plan.deletable)

    deleted = {}
    for model, pks in closure.items():
        if not pks:
            continue
        name = str(model._meta.verbose_name_plural).strip()
        label = name[:1].upper() + name[1:] if name else model._meta.label
        deleted[label] = deleted.get(label, 0) + len(pks)

    return {
        # Largest first: the things worth noticing sit at the top.
        "deleted": dict(sorted(deleted.items(), key=lambda kv: (-kv[1], kv[0]))),
        "retained": plan.retained_counts(),
    }


def rollback_migration(job, dry_run=False):
    """Delete what this migration created, keeping anything still depended on.

    Returns a report dict of what was deleted and what was retained. With
    dry_run=True nothing is written — used to show the merchant the consequences
    before they confirm.
    """
    logger.info("Planning rollback for migration job %s", job.id)
    plan = plan_rollback(job)
    report = summarise(plan)

    if dry_run:
        return report

    logger.info("Rollback plan for job %s: %s", job.id, report)

    try:
        with transaction.atomic():
            for model, label in _deletion_order():
                pks = plan.pks(model)
                if not pks:
                    continue
                removed = _delete_in_chunks(model, pks)
                logger.info("Rollback %s: removed %d %s", job.id, removed, label)

            job.status = "rolled_back"
            job.can_rollback = False
            job.save(update_fields=["status", "can_rollback"])

    except ProtectedError as exc:
        # The retention plan should make this unreachable. If it fires, the FK
        # graph has an edge the closure did not account for; fail closed with a
        # message that names it rather than corrupting the store.
        logger.exception("Rollback of job %s aborted on a protected reference", job.id)
        raise RollbackRefused(
            "Rollback stopped because something in your store still depends on "
            "data this import created, and Spwig could not determine what. "
            "Nothing has been deleted."
        ) from exc

    logger.info("Rollback completed for migration job %s", job.id)
    return report
