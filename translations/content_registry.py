"""
Centralized registry of all translatable content types.

Maps model identifiers to their translatable fields, display metadata,
and format information. Used by the coverage service and translate-all
system to discover what content needs translation.

"""
from django.apps import apps


TRANSLATABLE_CONTENT_TYPES = [
    # --- Priority 1: Core storefront content ---
    {
        'key': 'catalog.product',
        'model': 'catalog.Product',
        'fields': ['name', 'short_description', 'full_description', 'meta_title', 'meta_description'],
        'label': 'Products',
        'icon': 'fas fa-box',
        'format': 'nested',
        'priority': 1,
    },
    {
        'key': 'catalog.category',
        'model': 'catalog.Category',
        'fields': ['name', 'description', 'meta_title', 'meta_description'],
        'label': 'Categories',
        'icon': 'fas fa-folder',
        'format': 'nested',
        'priority': 1,
    },
    {
        'key': 'page_builder.page',
        'model': 'page_builder.Page',
        'fields': ['title', 'meta_title', 'meta_description', 'meta_keywords'],
        'label': 'Pages',
        'icon': 'fas fa-file-alt',
        'format': 'nested',
        'priority': 1,
    },
    {
        'key': 'core.sitesettings',
        'model': 'core.SiteSettings',
        'fields': ['site_name', 'site_tagline', 'site_description'],
        'label': 'Site Settings',
        'icon': 'fas fa-cog',
        'format': 'nested',
        'singleton': True,
        'priority': 1,
    },
    # --- Priority 2: Content & communications ---
    {
        'key': 'blog.blogpost',
        'model': 'blog.BlogPost',
        'fields': ['title', 'excerpt', 'simple_content', 'meta_title', 'meta_description'],
        'label': 'Blog Posts',
        'icon': 'fas fa-newspaper',
        'format': 'nested',
        'priority': 2,
    },
    {
        'key': 'announcements.announcement',
        'model': 'announcements.Announcement',
        'fields': ['title', 'body', 'link_text'],
        'label': 'Announcements',
        'icon': 'fas fa-bullhorn',
        'format': 'nested',
        'priority': 2,
    },
    {
        'key': 'design.menuitem',
        'model': 'design.MenuItem',
        'fields': ['title', 'badge_text'],
        'label': 'Menu Items',
        'icon': 'fas fa-bars',
        'format': 'nested',
        'priority': 2,
    },
    # --- Priority 3: Supporting content ---
    {
        'key': 'blog.blogcategory',
        'model': 'blog.BlogCategory',
        'fields': ['name', 'description', 'meta_title', 'meta_description'],
        'label': 'Blog Categories',
        'icon': 'fas fa-bookmark',
        'format': 'nested',
        'priority': 3,
    },
    {
        'key': 'subscriptions.subscriptionplan',
        'model': 'subscriptions.SubscriptionPlan',
        'fields': ['name', 'description'],
        'label': 'Subscription Plans',
        'icon': 'fas fa-sync-alt',
        'format': 'nested',
        'priority': 3,
    },
    {
        'key': 'affiliate.affiliatesettings',
        'model': 'affiliate.AffiliateSettings',
        'fields': [
            'hero_title', 'hero_subtitle', 'features_title',
            'how_it_works_title', 'cta_title', 'cta_description',
            'welcome_message',
        ],
        'label': 'Affiliate Portal',
        'icon': 'fas fa-handshake',
        'format': 'nested',
        'singleton': True,
        'priority': 3,
    },
    {
        'key': 'catalog.productattribute',
        'model': 'catalog.ProductAttribute',
        'fields': ['name'],
        'label': 'Product Attributes',
        'icon': 'fas fa-tags',
        'format': 'simple',
        'priority': 3,
    },
    {
        'key': 'catalog.attributevalue',
        'model': 'catalog.AttributeValue',
        'fields': ['value'],
        'label': 'Attribute Values',
        'icon': 'fas fa-tag',
        'format': 'simple',
        'priority': 3,
    },
    {
        'key': 'design.widget',
        'model': 'design.Widget',
        'fields': [],  # Extracted dynamically from widget config
        'label': 'Widgets',
        'icon': 'fas fa-puzzle-piece',
        'format': 'widget_config',
        'priority': 3,
    },
    # --- Priority 4: Low-impact / optional ---
    {
        'key': 'media_library.mediaasset',
        'model': 'media_library.MediaAsset',
        'fields': ['title', 'alt_text', 'description'],
        'label': 'Media Assets',
        'icon': 'fas fa-images',
        'format': 'nested',
        'priority': 4,
    },
]

# Build a fast lookup dict
_REGISTRY_BY_KEY = {ct['key']: ct for ct in TRANSLATABLE_CONTENT_TYPES}


def get_content_type(key):
    """Look up a content type entry by key (e.g. 'catalog.product')."""
    return _REGISTRY_BY_KEY.get(key)


def get_all_content_types():
    """Return all content types sorted by priority then label."""
    return sorted(TRANSLATABLE_CONTENT_TYPES, key=lambda ct: (ct['priority'], ct['label']))


def get_content_type_keys():
    """Return set of all registered content type keys."""
    return set(_REGISTRY_BY_KEY.keys())


def get_model_class(key):
    """Return the Django model class for a content type key."""
    entry = _REGISTRY_BY_KEY.get(key)
    if not entry:
        return None
    app_label, model_name = entry['model'].split('.')
    try:
        return apps.get_model(app_label, model_name)
    except LookupError:
        return None
