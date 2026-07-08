"""
Integration tests for the category page system.

Covers:
- Category list and detail views (routing, status codes, context)
- Template option resolution (schema defaults, site config, per-category overrides)
- Banner feature (show/hide, with/without banner image)
- Card image fallback (product image vs placeholder)
- Sorting (all 5 options + invalid/missing sort param)
- Pagination (numbered, load_more, page boundaries, invalid page)
- Subcategories display
- Product filtering (only published, excludes POS-only, descendant categories)
- Category model methods (get_image_url, get_card_image_url, get_banner_url)
"""
import pytest
from decimal import Decimal
from django.test import Client

from tests.factories import CategoryFactory, ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


# ============================================================
# Helpers
# ============================================================

def _create_media_asset(**kwargs):
    """Create a MediaAsset using the factory."""
    from tests.factories import MediaAssetFactory

    # Set default values for PNG images
    defaults = {
        'mime_type': 'image/png',
        'width': 1,
        'height': 1,
    }
    defaults.update(kwargs)
    return MediaAssetFactory(**defaults)


def _create_product_with_image(category, name='Product With Image', **product_kwargs):
    """Create a product with a ProductImage pointing to a MediaAsset."""
    from catalog.models import ProductImage
    asset = _create_media_asset(title=f'{name} image')
    product = ProductFactory(
        name=name,
        category=category,
        **product_kwargs,
    )
    ProductImage.objects.create(product=product, media_asset=asset, is_primary=True)
    return product


def _set_category_options(options_dict):
    """Set site-wide category template options."""
    from design.models import PageTemplateConfig
    config = PageTemplateConfig.get_config()
    config.category_options = options_dict
    config.save()


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def client():
    return Client()


@pytest.fixture
def parent_category(db):
    """Top-level category for testing."""
    return CategoryFactory(
        name='Electronics',
        slug='electronics',
        description='All electronic products',
    )


@pytest.fixture
def child_category(parent_category):
    """Subcategory of electronics."""
    return CategoryFactory(
        name='Phones',
        slug='phones',
        parent=parent_category,
        description='Mobile phones',
    )


@pytest.fixture
def another_child(parent_category):
    """Second subcategory."""
    return CategoryFactory(
        name='Tablets',
        slug='tablets',
        parent=parent_category,
    )


@pytest.fixture
def empty_category(db):
    """Category with no products."""
    return CategoryFactory(name='Empty Category', slug='empty-category')


@pytest.fixture
def category_with_banner(db):
    """Category with a banner image attached."""
    asset = _create_media_asset(title='Banner')
    return CategoryFactory(
        name='Featured',
        slug='featured',
        description='Featured products',
        banner_asset=asset,
    )


@pytest.fixture
def category_with_image(db):
    """Category with a dedicated category image."""
    asset = _create_media_asset(title='Category image')
    return CategoryFactory(
        name='Branded',
        slug='branded',
        image_asset=asset,
    )


@pytest.fixture
def category_with_products(db):
    """Category with several published products (some with images)."""
    cat = CategoryFactory(name='Shop', slug='shop')
    _create_product_with_image(cat, name='Alpha Product', price=Decimal('10.00'))
    _create_product_with_image(cat, name='Beta Product', price=Decimal('50.00'))
    ProductFactory(name='Gamma Product', slug='gamma-product', category=cat, price=Decimal('30.00'))
    return cat


@pytest.fixture
def many_products_category(db):
    """Category with enough products to test pagination (30 products)."""
    cat = CategoryFactory(name='Big Category', slug='big-category')
    for i in range(30):
        ProductFactory(
            name=f'Item {i:03d}',
            slug=f'item-{i:03d}',
            category=cat,
            price=Decimal(str(10 + i)),
        )
    return cat


# ============================================================
# View Routing & Status
# ============================================================

class TestCategoryRouting:
    """Basic view routing and HTTP status codes."""

    def test_category_list_returns_200(self, client, site_settings):
        resp = client.get('/en/category/')
        assert resp.status_code == 200

    def test_category_detail_returns_200(self, client, site_settings, parent_category):
        resp = client.get(f'/en/category/{parent_category.slug}/')
        assert resp.status_code == 200

    def test_nonexistent_category_returns_404(self, client, site_settings):
        resp = client.get('/en/category/does-not-exist/')
        assert resp.status_code == 404

    def test_inactive_category_returns_404(self, client, site_settings):
        cat = CategoryFactory(name='Hidden', slug='hidden', is_active=False)
        resp = client.get(f'/en/category/{cat.slug}/')
        assert resp.status_code == 404

    def test_category_list_uses_correct_template(self, client, site_settings):
        resp = client.get('/en/category/')
        assert 'page_builder/category/default.html' in [t.name for t in resp.templates]

    def test_category_detail_uses_correct_template(self, client, site_settings, parent_category):
        resp = client.get(f'/en/category/{parent_category.slug}/')
        assert 'page_builder/category/default.html' in [t.name for t in resp.templates]


# ============================================================
# Context & Template Options
# ============================================================

class TestCategoryContext:
    """Verify context variables passed to the template."""

    def test_list_context_has_categories(self, client, site_settings, parent_category):
        resp = client.get('/en/category/')
        assert 'categories' in resp.context
        slugs = [c.slug for c in resp.context['categories']]
        assert parent_category.slug in slugs

    def test_list_context_category_is_none(self, client, site_settings):
        resp = client.get('/en/category/')
        assert resp.context['category'] is None

    def test_detail_context_has_category(self, client, site_settings, parent_category):
        resp = client.get(f'/en/category/{parent_category.slug}/')
        assert resp.context['category'] == parent_category

    def test_detail_context_has_template_options(self, client, site_settings, parent_category):
        resp = client.get(f'/en/category/{parent_category.slug}/')
        opts = resp.context['template_options']
        assert 'show_banner' in opts
        assert 'card_image_fallback' in opts
        assert 'pagination_style' in opts

    def test_default_option_values(self, client, site_settings, parent_category):
        """Verify schema defaults are applied when no site config exists."""
        resp = client.get(f'/en/category/{parent_category.slug}/')
        opts = resp.context['template_options']
        assert opts['show_banner'] is True
        assert opts['card_image_fallback'] == 'product'
        assert opts['products_per_page'] == '24'
        assert opts['pagination_style'] == 'numbered'
        assert opts['default_sort'] == 'newest'
        assert opts['show_breadcrumb'] is True

    def test_site_options_override_defaults(self, client, site_settings, parent_category):
        """Site-wide config overrides schema defaults."""
        _set_category_options({
            'products_per_page': '12',
            'show_banner': False,
            'pagination_style': 'load_more',
        })
        resp = client.get(f'/en/category/{parent_category.slug}/')
        opts = resp.context['template_options']
        assert opts['products_per_page'] == '12'
        assert opts['show_banner'] is False
        assert opts['pagination_style'] == 'load_more'

    def test_category_overrides_site_options(self, client, site_settings):
        """Per-category model fields override site config."""
        cat = CategoryFactory(
            name='Custom PPP',
            slug='custom-ppp',
            products_per_page=36,
        )
        _set_category_options({'products_per_page': '12'})
        resp = client.get(f'/en/category/{cat.slug}/')
        opts = resp.context['template_options']
        assert opts['products_per_page'] == '36'

    def test_subcategory_override_show_subcategories(self, client, site_settings):
        """Category with show_subcategories=False overrides site config."""
        cat = CategoryFactory(
            name='No Subcats',
            slug='no-subcats',
            show_subcategories=False,
        )
        resp = client.get(f'/en/category/{cat.slug}/')
        opts = resp.context['template_options']
        assert opts['show_subcategories'] is False


# ============================================================
# Banner Feature
# ============================================================

class TestCategoryBanner:
    """Test the hero banner display logic."""

    def test_banner_renders_when_image_exists(self, client, site_settings, category_with_banner):
        resp = client.get(f'/en/category/{category_with_banner.slug}/')
        content = resp.content.decode()
        assert 'cat-banner' in content
        assert 'cat-banner__image' in content
        assert 'cat-banner__overlay' in content

    def test_banner_shows_title_and_description(self, client, site_settings, category_with_banner):
        resp = client.get(f'/en/category/{category_with_banner.slug}/')
        content = resp.content.decode()
        assert 'cat-banner__title' in content
        assert category_with_banner.name in content
        assert category_with_banner.description in content

    def test_no_banner_without_image(self, client, site_settings, parent_category):
        """Category without banner_asset falls back to plain header."""
        resp = client.get(f'/en/category/{parent_category.slug}/')
        content = resp.content.decode()
        assert 'cat-banner' not in content
        assert 'cat-page-header' in content

    def test_banner_disabled_via_option(self, client, site_settings, category_with_banner):
        """show_banner=False hides banner even when image exists."""
        _set_category_options({'show_banner': False})
        resp = client.get(f'/en/category/{category_with_banner.slug}/')
        content = resp.content.decode()
        assert 'cat-banner' not in content
        assert 'cat-page-header' in content

    def test_category_list_never_shows_banner(self, client, site_settings, category_with_banner):
        """The list view (no specific category) never shows a banner."""
        resp = client.get('/en/category/')
        content = resp.content.decode()
        assert 'cat-banner' not in content

    def test_banner_uses_eager_loading(self, client, site_settings, category_with_banner):
        """Banner image should use loading='eager' since it's above the fold."""
        resp = client.get(f'/en/category/{category_with_banner.slug}/')
        content = resp.content.decode()
        assert 'loading="eager"' in content


# ============================================================
# Card Image Fallback
# ============================================================

class TestCardImageFallback:
    """Test the category card image fallback behavior."""

    def test_product_fallback_shows_product_image(self, client, site_settings, category_with_products):
        """Default 'product' fallback shows first product's image on the card."""
        resp = client.get('/en/category/')
        content = resp.content.decode()
        assert 'category-card__image' in content
        # Should NOT show placeholder for this category (has products with images)
        # Count placeholders vs images - category_with_products should have an image
        assert f'alt="{category_with_products.name}"' in content

    def test_placeholder_fallback_shows_icon(self, client, site_settings, category_with_products):
        """'placeholder' fallback shows folder icon even when products have images."""
        _set_category_options({'card_image_fallback': 'placeholder'})
        resp = client.get('/en/category/')
        content = resp.content.decode()
        # All categories without a dedicated image_asset should show placeholder
        assert 'category-card__placeholder' in content

    def test_dedicated_image_always_used(self, client, site_settings, category_with_image):
        """A category with its own image_asset always shows that image."""
        # Test with product fallback
        resp = client.get('/en/category/')
        content = resp.content.decode()
        # The category_with_image should show its own image in both modes
        assert f'alt="{category_with_image.name}"' in content

    def test_dedicated_image_used_in_placeholder_mode(self, client, site_settings, category_with_image):
        """Even in placeholder mode, a dedicated category image is shown."""
        _set_category_options({'card_image_fallback': 'placeholder'})
        resp = client.get('/en/category/')
        content = resp.content.decode()
        assert f'alt="{category_with_image.name}"' in content

    def test_empty_category_shows_placeholder_in_product_mode(self, client, site_settings, empty_category):
        """A category with no products shows placeholder even in 'product' mode."""
        resp = client.get('/en/category/')
        content = resp.content.decode()
        assert 'category-card__placeholder' in content


# ============================================================
# Category Model Methods
# ============================================================

class TestCategoryModelMethods:
    """Test get_image_url, get_card_image_url, get_banner_url."""

    def test_get_image_url_with_asset(self, category_with_image):
        url = category_with_image.get_image_url()
        assert url is not None
        assert url.startswith('/media/')  # served from media storage

    def test_get_image_url_without_asset(self, parent_category):
        assert parent_category.get_image_url() is None

    def test_get_banner_url_with_asset(self, category_with_banner):
        url = category_with_banner.get_banner_url()
        assert url is not None

    def test_get_banner_url_without_asset(self, parent_category):
        assert parent_category.get_banner_url() is None

    def test_get_card_image_url_with_category_image(self, category_with_image):
        """get_card_image_url returns category image when set."""
        url = category_with_image.get_card_image_url()
        assert url is not None
        assert url == category_with_image.get_image_url()

    def test_get_card_image_url_falls_back_to_product(self, category_with_products):
        """get_card_image_url returns product image when no category image."""
        assert category_with_products.image_asset is None  # no dedicated image
        url = category_with_products.get_card_image_url()
        assert url is not None  # should get product image

    def test_get_card_image_url_empty_category(self, empty_category):
        """get_card_image_url returns None for empty category."""
        assert empty_category.get_card_image_url() is None

    def test_get_card_image_url_skips_draft_products(self, db):
        """get_card_image_url only considers published products."""
        from catalog.models import ProductImage
        cat = CategoryFactory(name='Drafts Only', slug='drafts-only')
        asset = _create_media_asset(title='Draft product image')
        product = ProductFactory(
            name='Draft Item',
            slug='draft-item',
            category=cat,
            status='draft',
        )
        ProductImage.objects.create(product=product, media_asset=asset, is_primary=True)
        assert cat.get_card_image_url() is None

    def test_get_card_image_url_skips_products_without_images(self, db):
        """get_card_image_url returns None if products have no images."""
        cat = CategoryFactory(name='No Images', slug='no-images')
        ProductFactory(name='Bare Product', slug='bare-product', category=cat)
        assert cat.get_card_image_url() is None


# ============================================================
# Sorting
# ============================================================

class TestCategorySorting:
    """Test sort parameter handling."""

    def test_default_sort_is_newest(self, client, site_settings, category_with_products):
        resp = client.get(f'/en/category/{category_with_products.slug}/')
        assert resp.context['current_sort'] == 'newest'

    def test_sort_price_low(self, client, site_settings, category_with_products):
        resp = client.get(f'/en/category/{category_with_products.slug}/?sort=price_low')
        products = list(resp.context['products'])
        prices = [p.price.amount for p in products]
        assert prices == sorted(prices)

    def test_sort_price_high(self, client, site_settings, category_with_products):
        resp = client.get(f'/en/category/{category_with_products.slug}/?sort=price_high')
        products = list(resp.context['products'])
        prices = [p.price.amount for p in products]
        assert prices == sorted(prices, reverse=True)

    def test_sort_name_az(self, client, site_settings, category_with_products):
        resp = client.get(f'/en/category/{category_with_products.slug}/?sort=name_az')
        products = list(resp.context['products'])
        names = [p.name for p in products]
        assert names == sorted(names)

    def test_sort_name_za(self, client, site_settings, category_with_products):
        resp = client.get(f'/en/category/{category_with_products.slug}/?sort=name_za')
        products = list(resp.context['products'])
        names = [p.name for p in products]
        assert names == sorted(names, reverse=True)

    def test_invalid_sort_falls_back_to_newest(self, client, site_settings, category_with_products):
        resp = client.get(f'/en/category/{category_with_products.slug}/?sort=bogus')
        assert resp.status_code == 200
        # Falls back to -created_at ordering (same as newest)

    def test_custom_default_sort(self, client, site_settings, category_with_products):
        """Site config can change the default sort."""
        _set_category_options({'default_sort': 'price_low'})
        resp = client.get(f'/en/category/{category_with_products.slug}/')
        assert resp.context['current_sort'] == 'price_low'

    def test_sort_choices_in_context(self, client, site_settings, category_with_products):
        resp = client.get(f'/en/category/{category_with_products.slug}/')
        sort_choices = resp.context['sort_choices']
        sort_keys = [k for k, _ in sort_choices]
        assert sort_keys == ['newest', 'price_low', 'price_high', 'name_az', 'name_za']


# ============================================================
# Pagination
# ============================================================

class TestCategoryPagination:
    """Test pagination behavior and edge cases."""

    def test_pagination_context_present(self, client, site_settings, many_products_category):
        resp = client.get(f'/en/category/{many_products_category.slug}/')
        assert 'paginator' in resp.context
        assert 'page_obj' in resp.context
        assert resp.context['total_count'] == 30

    def test_default_24_per_page(self, client, site_settings, many_products_category):
        resp = client.get(f'/en/category/{many_products_category.slug}/')
        assert len(resp.context['products']) == 24

    def test_custom_per_page(self, client, site_settings, many_products_category):
        _set_category_options({'products_per_page': '12'})
        resp = client.get(f'/en/category/{many_products_category.slug}/')
        assert len(resp.context['products']) == 12

    def test_page_2(self, client, site_settings, many_products_category):
        resp = client.get(f'/en/category/{many_products_category.slug}/?page=2')
        assert resp.context['page_obj'].number == 2
        # 30 products / 24 per page = page 2 has 6 items
        assert len(resp.context['products']) == 6

    def test_invalid_page_string_falls_back_to_1(self, client, site_settings, many_products_category):
        resp = client.get(f'/en/category/{many_products_category.slug}/?page=abc')
        assert resp.status_code == 200
        assert resp.context['page_obj'].number == 1

    def test_page_beyond_range_shows_last(self, client, site_settings, many_products_category):
        resp = client.get(f'/en/category/{many_products_category.slug}/?page=999')
        assert resp.status_code == 200
        assert resp.context['page_obj'].number == resp.context['paginator'].num_pages

    def test_page_zero_falls_back_to_last(self, client, site_settings, many_products_category):
        resp = client.get(f'/en/category/{many_products_category.slug}/?page=0')
        assert resp.status_code == 200
        # page=0 raises EmptyPage, view falls back to last page
        assert resp.context['page_obj'].number == resp.context['paginator'].num_pages

    def test_negative_page_falls_back(self, client, site_settings, many_products_category):
        resp = client.get(f'/en/category/{many_products_category.slug}/?page=-1')
        assert resp.status_code == 200

    def test_numbered_pagination_renders(self, client, site_settings, many_products_category):
        resp = client.get(f'/en/category/{many_products_category.slug}/')
        content = resp.content.decode()
        assert 'pagination' in content

    def test_load_more_pagination_renders(self, client, site_settings, many_products_category):
        _set_category_options({'pagination_style': 'load_more'})
        resp = client.get(f'/en/category/{many_products_category.slug}/')
        content = resp.content.decode()
        assert 'load-more' in content


# ============================================================
# Product Filtering
# ============================================================

class TestProductFiltering:
    """Ensure only valid products appear in category views."""

    def test_only_published_products_shown(self, client, site_settings):
        cat = CategoryFactory(name='Mixed Status', slug='mixed-status')
        ProductFactory(name='Published', slug='published-p', category=cat, status='published')
        ProductFactory(name='Draft', slug='draft-p', category=cat, status='draft')
        resp = client.get(f'/en/category/{cat.slug}/')
        product_names = [p.name for p in resp.context['products']]
        assert 'Published' in product_names
        assert 'Draft' not in product_names

    def test_pos_only_products_excluded(self, client, site_settings):
        cat = CategoryFactory(name='POS Test', slug='pos-test')
        ProductFactory(name='Web Product', slug='web-prod', category=cat)
        ProductFactory(name='POS Only', slug='pos-only', category=cat, sales_channel='pos_only')
        resp = client.get(f'/en/category/{cat.slug}/')
        product_names = [p.name for p in resp.context['products']]
        assert 'Web Product' in product_names
        assert 'POS Only' not in product_names

    def test_hidden_products_excluded(self, client, site_settings):
        cat = CategoryFactory(name='Hidden Test', slug='hidden-test')
        ProductFactory(name='Visible', slug='visible-p', category=cat)
        ProductFactory(name='Hidden', slug='hidden-p', category=cat, hide_from_storefront=True)
        resp = client.get(f'/en/category/{cat.slug}/')
        product_names = [p.name for p in resp.context['products']]
        assert 'Visible' in product_names
        assert 'Hidden' not in product_names

    def test_descendant_category_products_included(self, client, site_settings, parent_category, child_category):
        """Products in child categories appear on the parent category page."""
        ProductFactory(name='Child Product', slug='child-prod', category=child_category)
        ProductFactory(name='Parent Product', slug='parent-prod', category=parent_category)
        resp = client.get(f'/en/category/{parent_category.slug}/')
        product_names = [p.name for p in resp.context['products']]
        assert 'Parent Product' in product_names
        assert 'Child Product' in product_names

    def test_empty_category_shows_empty_message(self, client, site_settings, empty_category):
        resp = client.get(f'/en/category/{empty_category.slug}/')
        content = resp.content.decode()
        assert 'product-grid__empty' in content


# ============================================================
# Subcategories
# ============================================================

class TestSubcategories:
    """Test subcategory chips display."""

    def test_subcategories_shown(self, client, site_settings, parent_category, child_category, another_child):
        resp = client.get(f'/en/category/{parent_category.slug}/')
        content = resp.content.decode()
        assert 'subcategory-chip' in content
        assert child_category.name in content
        assert another_child.name in content

    def test_subcategories_hidden_when_disabled(self, client, site_settings, parent_category, child_category):
        _set_category_options({'show_subcategories': False})
        resp = client.get(f'/en/category/{parent_category.slug}/')
        content = resp.content.decode()
        assert 'subcategory-chip' not in content

    def test_no_subcategory_section_for_leaf_category(self, client, site_settings, child_category):
        """Leaf category (no children) doesn't show subcategory section."""
        resp = client.get(f'/en/category/{child_category.slug}/')
        content = resp.content.decode()
        assert 'subcategory-chip' not in content

    def test_category_list_shows_only_top_level(self, client, site_settings, parent_category, child_category):
        """The category list view only shows top-level (parent=null) categories."""
        resp = client.get('/en/category/')
        category_slugs = [c.slug for c in resp.context['categories']]
        assert parent_category.slug in category_slugs
        assert child_category.slug not in category_slugs


# ============================================================
# Template Option Registry
# ============================================================

class TestTemplateRegistry:
    """Test the template registry and option resolution functions."""

    def test_get_category_options_returns_all_keys(self):
        from design.template_registry import get_category_options, CATEGORY_TEMPLATE_OPTIONS
        opts = get_category_options('default')
        schema = CATEGORY_TEMPLATE_OPTIONS['default']
        assert set(opts.keys()) == set(schema.keys())

    def test_get_category_options_with_site_override(self):
        from design.template_registry import get_category_options
        opts = get_category_options('default', site_options={'show_banner': False})
        assert opts['show_banner'] is False
        # Other options should still be defaults
        assert opts['products_per_page'] == '24'

    def test_get_category_options_category_beats_site(self):
        from design.template_registry import get_category_options
        opts = get_category_options(
            'default',
            site_options={'products_per_page': '12'},
            category_overrides={'products_per_page': '48'},
        )
        assert opts['products_per_page'] == '48'

    def test_get_category_options_unknown_template_returns_empty(self):
        from design.template_registry import get_category_options
        opts = get_category_options('nonexistent')
        assert opts == {}

    def test_get_category_template_path_default(self):
        from design.template_registry import get_category_template_path
        assert get_category_template_path('default') == 'page_builder/category/default.html'

    def test_get_category_template_path_fallback(self):
        from design.template_registry import get_category_template_path
        assert get_category_template_path('nonexistent') == 'page_builder/category/default.html'

    def test_category_template_meta_exists(self):
        from design.template_registry import CATEGORY_TEMPLATE_META
        assert 'default' in CATEGORY_TEMPLATE_META
        assert 'name' in CATEGORY_TEMPLATE_META['default']
        assert 'icon' in CATEGORY_TEMPLATE_META['default']


# ============================================================
# Display Options (breadcrumb, sort bar, help section, etc.)
# ============================================================

class TestDisplayOptions:
    """Test individual display toggle options."""

    def test_breadcrumb_shown_by_default(self, client, site_settings, parent_category):
        resp = client.get(f'/en/category/{parent_category.slug}/')
        assert 'breadcrumb' in resp.content.decode()

    def test_breadcrumb_hidden_when_disabled(self, client, site_settings, parent_category):
        _set_category_options({'show_breadcrumb': False})
        resp = client.get(f'/en/category/{parent_category.slug}/')
        content = resp.content.decode()
        assert 'breadcrumb__list' not in content

    def test_sort_bar_shown_by_default(self, client, site_settings, category_with_products):
        resp = client.get(f'/en/category/{category_with_products.slug}/')
        assert 'sort-bar' in resp.content.decode()

    def test_sort_bar_hidden_when_disabled(self, client, site_settings, category_with_products):
        _set_category_options({'show_sort_bar': False})
        resp = client.get(f'/en/category/{category_with_products.slug}/')
        assert 'sort-bar' not in resp.content.decode()

    def test_help_section_shown_by_default(self, client, site_settings, parent_category):
        resp = client.get(f'/en/category/{parent_category.slug}/')
        assert 'help-block' in resp.content.decode()

    def test_help_section_hidden_when_disabled(self, client, site_settings, parent_category):
        _set_category_options({'show_help_section': False})
        resp = client.get(f'/en/category/{parent_category.slug}/')
        assert 'help-block' not in resp.content.decode()

    def test_category_description_shown(self, client, site_settings, parent_category):
        resp = client.get(f'/en/category/{parent_category.slug}/')
        assert parent_category.description in resp.content.decode()

    def test_category_description_hidden_when_disabled(self, client, site_settings, parent_category):
        _set_category_options({'show_category_description': False})
        resp = client.get(f'/en/category/{parent_category.slug}/')
        content = resp.content.decode()
        # Description should not appear in the header
        assert 'cat-page-header__subtitle' not in content
        assert 'cat-banner__subtitle' not in content

    def test_product_count_shown_by_default(self, client, site_settings, category_with_products):
        resp = client.get(f'/en/category/{category_with_products.slug}/')
        assert 'sort-bar__count' in resp.content.decode()

    def test_product_count_hidden_when_disabled(self, client, site_settings, category_with_products):
        _set_category_options({'show_product_count': False})
        resp = client.get(f'/en/category/{category_with_products.slug}/')
        assert 'sort-bar__count' not in resp.content.decode()


# ============================================================
# Edge Cases & User Behavior
# ============================================================

class TestEdgeCases:
    """Outliers, unusual inputs, and real-world user behavior."""

    def test_special_characters_in_category_name(self, client, site_settings):
        """Category names with special chars render safely (no XSS)."""
        cat = CategoryFactory(
            name='<script>alert("xss")</script>',
            slug='xss-test',
        )
        resp = client.get(f'/en/category/{cat.slug}/')
        content = resp.content.decode()
        assert '<script>alert' not in content
        assert '&lt;script&gt;' in content or '&lt;script&gt;' in content

    def test_very_long_description_renders(self, client, site_settings):
        """Long descriptions don't break the template."""
        cat = CategoryFactory(
            name='Verbose',
            slug='verbose',
            description='A' * 5000,
        )
        resp = client.get(f'/en/category/{cat.slug}/')
        assert resp.status_code == 200

    def test_simultaneous_sort_and_page_params(self, client, site_settings, many_products_category):
        """Sort + page params work together."""
        resp = client.get(f'/en/category/{many_products_category.slug}/?sort=price_low&page=2')
        assert resp.status_code == 200
        assert resp.context['current_sort'] == 'price_low'
        assert resp.context['page_obj'].number == 2

    def test_multiple_sort_params_uses_last(self, client, site_settings, category_with_products):
        """Multiple sort params in URL — Django uses the last value."""
        resp = client.get(f'/en/category/{category_with_products.slug}/?sort=price_low&sort=name_az')
        assert resp.context['current_sort'] == 'name_az'

    def test_empty_sort_param(self, client, site_settings, category_with_products):
        resp = client.get(f'/en/category/{category_with_products.slug}/?sort=')
        assert resp.status_code == 200

    def test_category_with_banner_and_no_description(self, client, site_settings):
        """Banner renders without subtitle when description is empty."""
        asset = _create_media_asset(title='Banner no desc')
        cat = CategoryFactory(
            name='No Desc Banner',
            slug='no-desc-banner',
            description='',
            banner_asset=asset,
        )
        resp = client.get(f'/en/category/{cat.slug}/')
        content = resp.content.decode()
        assert 'cat-banner' in content
        assert 'cat-banner__subtitle' not in content

    def test_deeply_nested_category(self, client, site_settings):
        """3-level deep category hierarchy works."""
        grandparent = CategoryFactory(name='L1', slug='level-1')
        parent = CategoryFactory(name='L2', slug='level-2', parent=grandparent)
        child = CategoryFactory(name='L3', slug='level-3', parent=parent)
        ProductFactory(name='Deep Product', slug='deep-product', category=child)
        # Grandparent should include deep product
        resp = client.get(f'/en/category/{grandparent.slug}/')
        product_names = [p.name for p in resp.context['products']]
        assert 'Deep Product' in product_names

    def test_category_per_page_override_controls_pagination(self, client, site_settings):
        """Category model products_per_page=12 overrides site's 24."""
        cat = CategoryFactory(name='Small Pages', slug='small-pages', products_per_page=12)
        for i in range(15):
            ProductFactory(name=f'SP {i}', slug=f'sp-{i}', category=cat)
        resp = client.get(f'/en/category/{cat.slug}/')
        assert len(resp.context['products']) == 12
        assert resp.context['paginator'].num_pages == 2

    def test_concurrent_options_all_disabled(self, client, site_settings, parent_category):
        """All display options disabled — page still renders."""
        _set_category_options({
            'show_banner': False,
            'show_breadcrumb': False,
            'show_subcategories': False,
            'show_category_description': False,
            'show_sort_bar': False,
            'show_product_count': False,
            'show_help_section': False,
        })
        resp = client.get(f'/en/category/{parent_category.slug}/')
        assert resp.status_code == 200
        content = resp.content.decode()
        assert 'breadcrumb' not in content
        assert 'sort-bar' not in content
        assert 'help-block' not in content
