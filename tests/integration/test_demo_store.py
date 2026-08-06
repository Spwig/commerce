"""Tests for the ``demo_store`` seeder.

demo_store builds the deployed-target catalog the spwig-e2e certification suite
buys against. These prove it produces a coherent, *purchasable* store, is
idempotent (safe to re-run on a cert host that resets nightly), and that the
full profile adds the whole catalog-state matrix.
"""

from decimal import Decimal

import pytest
from django.core.management import call_command

pytestmark = [pytest.mark.django_db]


def test_smoke_profile_builds_a_purchasable_store(site_settings):
    call_command("demo_store")  # default profile = smoke

    from cart.models import ShippingMethod, TaxRate
    from catalog.models import GiftCard, Product, StockItem
    from shipping.models import ShippingCountry
    from vouchers.models import VoucherCode

    # A physical simple product: published, ships, in stock.
    tee = Product.objects.get(sku="DEMO-TEE")
    assert tee.status == "published"
    assert tee.requires_shipping is True and tee.is_digital is False
    assert StockItem.objects.get(product=tee, variant__isnull=True).on_hand == 50

    # A digital product: save() flips is_digital on and requires_shipping off.
    ebook = Product.objects.get(sku="DEMO-EBOOK")
    assert ebook.is_digital is True and ebook.requires_shipping is False

    # A redeemable gift card with a known code and $25 balance.
    card = GiftCard.objects.get(code="DEMOGIFT25")
    assert card.product.product_type == "gift_card"
    assert card.current_balance.amount == Decimal("25.00")
    assert card.is_active is True

    # Vouchers: reusable fixed, single-use fixed, reusable percentage.
    assert VoucherCode.objects.get(code="DEMO5").discount_type == "fixed"
    assert VoucherCode.objects.get(code="DEMOONCE").max_uses_total == 1
    pct = VoucherCode.objects.get(code="DEMO20PCT")
    assert pct.discount_type == "percentage" and pct.discount_value == Decimal("20.00")

    # A US checkout can reach payment (shipping method + shipping-country) and
    # carry tax.
    assert ShippingMethod.objects.filter(name="Standard Shipping", is_active=True).exists()
    assert ShippingCountry.objects.filter(country_code="US", is_active=True).exists()
    assert TaxRate.objects.filter(country="US").exists()


def test_is_idempotent_under_forced_rerun(site_settings):
    from catalog.models import GiftCard, Product, StockItem

    call_command("demo_store")
    products = Product.objects.count()
    stock = StockItem.objects.count()
    cards = GiftCard.objects.count()

    # --force bypasses the version-skip and re-runs the create path; get-or-create
    # keying means nothing duplicates.
    call_command("demo_store", force=True)
    assert Product.objects.count() == products
    assert StockItem.objects.count() == stock
    assert GiftCard.objects.count() == cards


def test_rerun_restores_consumed_gift_card_and_voucher(site_settings):
    """A cert host reseeds a known-good store. After a purchase depletes the
    gift card and exhausts the single-use voucher, re-running must top them back
    up — otherwise the next night's flows fail on empty stored value."""
    from decimal import Decimal

    from djmoney.money import Money

    from catalog.models import GiftCard
    from vouchers.models import VoucherCode

    call_command("demo_store")

    # Simulate a prior run consuming both.
    card = GiftCard.objects.get(code="DEMOGIFT25")
    card.current_balance = Money(Decimal("0.00"), "USD")
    card.is_active = False
    card.save()
    once = VoucherCode.objects.get(code="DEMOONCE")
    once.current_uses = 1  # single-use, now exhausted
    once.is_active = False
    once.save()

    call_command("demo_store", force=True)

    card.refresh_from_db()
    once.refresh_from_db()
    assert card.current_balance.amount == Decimal("25.00")
    assert card.is_active is True
    assert once.current_uses == 0
    assert once.is_active is True


def test_full_profile_adds_the_catalog_matrix(site_settings):
    call_command("demo_store", profile="full")

    from catalog.models import BundleItem, Product, ProductVariant, StockItem

    # Variable product with three variants, each stocked.
    hoodie = Product.objects.get(sku="DEMO-HOODIE")
    assert hoodie.product_type == "variable"
    variants = ProductVariant.objects.filter(product=hoodie)
    assert variants.count() == 3
    assert all(StockItem.objects.filter(product=hoodie, variant=v).exists() for v in variants)

    # Bundle with two components.
    bundle = Product.objects.get(sku="DEMO-BUNDLE")
    assert bundle.product_type == "bundle"
    assert BundleItem.objects.filter(bundle=bundle).count() == 2

    # The stock-state matrix.
    assert StockItem.objects.get(product__sku="DEMO-LOW", variant__isnull=True).on_hand == 2
    assert StockItem.objects.get(product__sku="DEMO-OOS", variant__isnull=True).on_hand == 0
    assert Product.objects.get(sku="DEMO-BACKORDER").allow_backorders is True
    assert Product.objects.get(sku="DEMO-PREORDER").is_preorder is True


def test_activates_the_test_gateway_provider(site_settings):
    """seed installs the test_gateway account inactive, so it never surfaces at
    checkout — a demo store can't be paid. demo_store must activate it (the
    filter needs is_active=True + connection_status='connected')."""
    from payment_providers.models import PaymentProviderAccount
    from tests.factories import ComponentRegistryFactory, PaymentProviderAccountFactory

    component = ComponentRegistryFactory(slug="test_gateway", name="Test Gateway")
    account = PaymentProviderAccountFactory(component=component)
    PaymentProviderAccount.objects.filter(pk=account.pk).update(
        is_active=False
    )  # as seed leaves it

    call_command("demo_store")

    account.refresh_from_db()
    assert account.is_active is True
    assert account.connection_status == "connected"


def test_smoke_profile_omits_the_full_matrix(site_settings):
    """Guard-the-guard: the matrix products only exist under --profile full, so
    the smoke set stays minimal."""
    from catalog.models import Product

    call_command("demo_store")  # smoke
    assert not Product.objects.filter(sku="DEMO-HOODIE").exists()
    assert not Product.objects.filter(sku="DEMO-BUNDLE").exists()
