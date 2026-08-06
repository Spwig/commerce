"""Tests for the create_demo_customizable seeder (the only product type that
previously had no demo command)."""

import pytest
from django.core.management import call_command

pytestmark = [pytest.mark.django_db]


def test_creates_a_buyable_customizable_product(site_settings):
    from catalog.models import CustomizationOption, Product

    call_command("create_demo_customizable", product="personalized_mug")

    product = Product.objects.get(sku="DEMO-CUSTOM-MUG")
    assert product.product_type == "customizable"
    assert product.allow_customization is True
    assert product.status == "published"
    assert str(product.price.currency) == "USD"
    # A required text option exists (the engraving) — the customization surface.
    opt = CustomizationOption.objects.get(product=product, slug="engraving-text")
    assert opt.option_type == "text"
    assert opt.is_required is True


def test_multiple_options_and_idempotent(site_settings):
    from catalog.models import CustomizationOption, Product

    call_command("create_demo_customizable", product="custom_tshirt")
    tee = Product.objects.get(sku="DEMO-CUSTOM-TEE")
    assert CustomizationOption.objects.filter(product=tee).count() == 2  # text + colour

    products = Product.objects.count()
    call_command("create_demo_customizable", product="custom_tshirt")  # re-run
    assert Product.objects.count() == products  # skipped, no duplicate
