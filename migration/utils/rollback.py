"""
Rollback utility for migration jobs
Safely deletes all imported data from a migration job
"""
import logging
from django.db import transaction, models
from django.utils import timezone

logger = logging.getLogger(__name__)


def rollback_migration(job):
    """
    Rollback a migration by deleting all imported data

    Args:
        job: MigrationJob instance

    Returns:
        dict: Statistics of deleted items
    """
    from catalog.models import Category, Product, ProductReview
    from orders.models import Order, OrderItem, Address
    from vouchers.models import VoucherCode
    from accounts.models import CustomerProfile
    from media_library.models import MediaAsset
    from shipping.models import Shipment
    from blog.models import BlogPost, BlogCategory
    from loyalty.models import LoyaltyMember, LoyaltyTransaction, LoyaltyRedemption
    from django.contrib.auth import get_user_model

    User = get_user_model()

    stats = {
        'categories': 0,
        'products': 0,
        'customers': 0,
        'orders': 0,
        'reviews': 0,
        'coupons': 0,
        'media_assets': 0,
        'blog_posts': 0,
        'blog_categories': 0,
    }

    logger.info(f"Starting rollback for migration job: {job} (ID: {job.id})")

    with transaction.atomic():
        # CRITICAL: Delete in reverse order of dependencies!
        # Each step removes PROTECT FK references that would block later steps.

        # Step 1: Delete OrderItems for orders from this migration
        order_ids = list(Order.objects.filter(migration_job=job).values_list('id', flat=True))
        deleted_order_items = 0
        if order_ids:
            order_items = OrderItem.objects.filter(order_id__in=order_ids)
            deleted_order_items = order_items.count()
            order_items.delete()
            logger.info(f"Deleted {deleted_order_items} order items from this migration")

        # Step 2: Delete OrderItems that reference products from this migration
        # (handles products ordered AFTER migration but BEFORE rollback)
        # Use all_objects to include soft-deleted products
        product_ids = list(Product.all_objects.filter(migration_job=job).values_list('id', flat=True))
        if product_ids:
            additional_items = OrderItem.objects.filter(product_id__in=product_ids)
            additional_count = additional_items.count()
            additional_items.delete()
            deleted_order_items += additional_count
            logger.info(f"Deleted {additional_count} additional order items referencing migrated products")

        # Step 2b: Delete Shipments for orders from this migration
        # (Shipment.order has PROTECT FK — must delete before Orders)
        if order_ids:
            shipment_count = Shipment.objects.filter(order_id__in=order_ids).count()
            if shipment_count:
                Shipment.objects.filter(order_id__in=order_ids).delete()
                logger.info(f"Deleted {shipment_count} shipments from this migration")

        # Step 3: Delete Orders from this migration
        deleted_orders = Order.objects.filter(migration_job=job).count()
        Order.objects.filter(migration_job=job).delete()
        stats['orders'] = deleted_orders
        logger.info(f"Deleted {deleted_orders} orders from this migration")

        # Step 4: Delete ProductReviews from this migration
        deleted_reviews = ProductReview.objects.filter(migration_job=job).count()
        ProductReview.objects.filter(migration_job=job).delete()
        stats['reviews'] = deleted_reviews
        logger.info(f"Deleted {deleted_reviews} reviews from this migration")

        # Step 5: Delete VoucherCodes from this migration
        deleted_coupons = VoucherCode.objects.filter(migration_job=job).count()
        VoucherCode.objects.filter(migration_job=job).delete()
        stats['coupons'] = deleted_coupons
        logger.info(f"Deleted {deleted_coupons} coupons from this migration")

        # Step 6: Hard-delete Products from this migration
        # Must use all_objects (base Manager) because Product.objects uses soft-delete.
        # all_objects returns a standard QuerySet whose .delete() is a real DB delete,
        # which is required so Category deletion in Step 7 doesn't hit PROTECT constraints.
        product_qs = Product.all_objects.filter(migration_job=job)
        deleted_products = product_qs.count()
        # ProductImage and ProductVariant will be cascade deleted with products
        product_qs.delete()
        stats['products'] = deleted_products
        logger.info(f"Deleted {deleted_products} products from this migration")

        # Step 7: Delete Categories from this migration
        deleted_categories = Category.objects.filter(migration_job=job).count()
        Category.objects.filter(migration_job=job).delete()
        stats['categories'] = deleted_categories
        logger.info(f"Deleted {deleted_categories} categories from this migration")

        # Step 7b: Delete Blog content from this migration
        deleted_blog_posts = BlogPost.objects.filter(migration_job=job).count()
        BlogPost.objects.filter(migration_job=job).delete()
        stats['blog_posts'] = deleted_blog_posts

        deleted_blog_categories = BlogCategory.objects.filter(migration_job=job).count()
        BlogCategory.objects.filter(migration_job=job).delete()
        stats['blog_categories'] = deleted_blog_categories

        if deleted_blog_posts or deleted_blog_categories:
            logger.info(
                f"Deleted {deleted_blog_posts} blog posts, "
                f"{deleted_blog_categories} blog categories from this migration"
            )

        # Step 8: Delete addresses from migrated customers
        customer_user_ids = CustomerProfile.objects.filter(migration_job=job).values_list('user_id', flat=True)
        if customer_user_ids:
            Address.objects.filter(user_id__in=customer_user_ids).delete()

        # Step 8b: Collect user IDs and clean up loyalty data before User deletion
        # The loyalty post_save signal auto-enrolls new users, creating LoyaltyMember,
        # LoyaltyTransaction, and LoyaltyRedemption records. These have PROTECT FKs
        # that block LoyaltyMember deletion (which would CASCADE from User deletion).
        deleted_customers = CustomerProfile.objects.filter(migration_job=job).count()
        user_ids = list(CustomerProfile.objects.filter(migration_job=job).values_list('user_id', flat=True))

        if user_ids:
            # Step 8c: Delete ALL orders referencing migrated users
            # (includes showcase/seed orders and any orders not tagged with migration_job)
            # Order.user has PROTECT FK — must clean up before User deletion.
            user_order_ids = list(
                Order.objects.filter(user_id__in=user_ids).values_list('id', flat=True)
            )
            if user_order_ids:
                OrderItem.objects.filter(order_id__in=user_order_ids).delete()
                Shipment.objects.filter(order_id__in=user_order_ids).delete()
                extra_orders = Order.objects.filter(id__in=user_order_ids).count()
                Order.objects.filter(id__in=user_order_ids).delete()
                stats['orders'] += extra_orders
                logger.info(f"Deleted {extra_orders} additional orders referencing migrated users")

            # Step 8d: Delete loyalty data (auto-created by post_save signal on User)
            # LoyaltyTransaction and LoyaltyRedemption have PROTECT FK to LoyaltyMember,
            # which CASCADE-deletes when User is deleted — so clear them first.
            loyalty_member_ids = list(
                LoyaltyMember.objects.filter(customer_id__in=user_ids).values_list('id', flat=True)
            )
            if loyalty_member_ids:
                LoyaltyRedemption.objects.filter(member_id__in=loyalty_member_ids).delete()
                LoyaltyTransaction.objects.filter(member_id__in=loyalty_member_ids).delete()
                logger.info(f"Deleted loyalty data for {len(loyalty_member_ids)} members")

        # Step 9: Delete CustomerProfiles and Users from this migration
        CustomerProfile.objects.filter(migration_job=job).delete()
        User.objects.filter(id__in=user_ids).delete()
        stats['customers'] = deleted_customers
        logger.info(f"Deleted {deleted_customers} customers from this migration")

        # Step 10: Delete MediaAssets from this migration
        deleted_media = MediaAsset.objects.filter(migration_job=job).count()
        MediaAsset.objects.filter(migration_job=job).delete()
        stats['media_assets'] = deleted_media
        logger.info(f"Deleted {deleted_media} media assets from this migration")

        # Mark job as rolled back
        job.status = 'rolled_back'
        job.save()

        logger.info(f"Rollback completed for migration job: {job}")
        logger.info(f"Rollback statistics: {stats}")

    return stats
