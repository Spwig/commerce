"""
Element Builder Registry

Defines which models and fields are available for binding in custom elements.
This is a configuration registry, not a database model.
"""
from django.utils.translation import gettext_lazy as _


# Bindable models configuration
# Each model entry defines:
#   - label: Human-readable name for UI display
#   - icon: Font Awesome icon class
#   - fields: Dict of field configurations
#       - type: 'text' | 'image' | 'url' - determines which element types can bind
#       - label: Human-readable field name
#       - fk_to: For image types, the FK target model (optional, for MediaAsset FKs)
#       - computed: True if this is a property/method, not a DB field
#       - description: Optional help text for the field
#       - group: Optional grouping for UI organization
BINDABLE_MODELS = {
    'catalog.Product': {
        'label': _('Product'),
        'icon': 'fas fa-box',
        'fields': {
            # Basic Info
            'name': {
                'type': 'text',
                'label': _('Product Name'),
                'group': 'basic',
            },
            'short_description': {
                'type': 'text',
                'label': _('Short Description'),
                'group': 'basic',
            },
            'full_description': {
                'type': 'text',
                'label': _('Full Description'),
                'description': _('Rich text product description'),
                'group': 'basic',
            },
            'slug': {
                'type': 'text',
                'label': _('URL Slug'),
                'group': 'basic',
            },
            'sku': {
                'type': 'text',
                'label': _('SKU'),
                'group': 'basic',
            },
            'product_type': {
                'type': 'text',
                'label': _('Product Type'),
                'description': _('simple, variable, digital, bundle, gift_card'),
                'group': 'basic',
            },
            'status': {
                'type': 'text',
                'label': _('Status'),
                'description': _('draft, published, discontinued'),
                'group': 'basic',
            },

            # Images
            'primary_image': {
                'type': 'image',
                'label': _('Main Image'),
                'fk_to': 'media_library.MediaAsset',
                'computed': True,
                'description': _('Primary product image from gallery'),
                'group': 'images',
            },

            # Pricing
            'price': {
                'type': 'text',
                'label': _('Price'),
                'computed': True,
                'description': _('Formatted current price'),
                'group': 'pricing',
            },
            'compare_at_price': {
                'type': 'text',
                'label': _('Compare at Price'),
                'computed': True,
                'description': _('Original price before discount'),
                'group': 'pricing',
            },
            'discount_percentage': {
                'type': 'text',
                'label': _('Discount Percentage'),
                'computed': True,
                'description': _('Percentage off (e.g., "20%")'),
                'group': 'pricing',
            },
            'savings_amount': {
                'type': 'text',
                'label': _('Savings Amount'),
                'computed': True,
                'description': _('Amount saved (e.g., "$10.00")'),
                'group': 'pricing',
            },
            'is_on_sale': {
                'type': 'text',
                'label': _('On Sale'),
                'computed': True,
                'description': _('Whether product has active discount'),
                'group': 'pricing',
            },

            # Stock & Availability
            'stock_status': {
                'type': 'text',
                'label': _('Stock Status'),
                'computed': True,
                'description': _('In Stock / Out of Stock / Low Stock'),
                'group': 'stock',
            },
            'is_in_stock': {
                'type': 'text',
                'label': _('Is In Stock'),
                'computed': True,
                'description': _('Boolean stock availability'),
                'group': 'stock',
            },
            'available_stock': {
                'type': 'text',
                'label': _('Available Stock'),
                'computed': True,
                'description': _('Number of items available'),
                'group': 'stock',
            },

            # Related
            'category_name': {
                'type': 'text',
                'label': _('Category Name'),
                'computed': True,
                'description': _('Primary category name'),
                'group': 'related',
            },
            'brand_name': {
                'type': 'text',
                'label': _('Brand Name'),
                'computed': True,
                'description': _('Brand name if assigned'),
                'group': 'related',
            },

            # Identifiers
            'gtin': {
                'type': 'text',
                'label': _('GTIN'),
                'description': _('Global Trade Item Number'),
                'group': 'identifiers',
            },
            'ean': {
                'type': 'text',
                'label': _('EAN'),
                'description': _('European Article Number'),
                'group': 'identifiers',
            },
            'upc': {
                'type': 'text',
                'label': _('UPC'),
                'description': _('Universal Product Code'),
                'group': 'identifiers',
            },
            'isbn': {
                'type': 'text',
                'label': _('ISBN'),
                'description': _('ISBN for books'),
                'group': 'identifiers',
            },
            'mpn': {
                'type': 'text',
                'label': _('MPN'),
                'description': _('Manufacturer Part Number'),
                'group': 'identifiers',
            },

            # SEO
            'meta_title': {
                'type': 'text',
                'label': _('Meta Title'),
                'description': _('SEO title for search engines'),
                'group': 'seo',
            },
            'meta_description': {
                'type': 'text',
                'label': _('Meta Description'),
                'description': _('SEO meta description'),
                'group': 'seo',
            },

            # Stats
            'views_count': {
                'type': 'text',
                'label': _('View Count'),
                'description': _('Number of product views'),
                'group': 'stats',
            },
            'sales_count': {
                'type': 'text',
                'label': _('Sales Count'),
                'description': _('Number of units sold'),
                'group': 'stats',
            },

            # URLs
            'url': {
                'type': 'url',
                'label': _('Product URL'),
                'computed': True,
                'description': _('Link to product page'),
                'group': 'urls',
            },
        }
    },
    'catalog.Category': {
        'label': _('Category'),
        'icon': 'fas fa-folder',
        'fields': {
            # Basic Info
            'name': {
                'type': 'text',
                'label': _('Category Name'),
                'group': 'basic',
            },
            'description': {
                'type': 'text',
                'label': _('Description'),
                'group': 'basic',
            },
            'slug': {
                'type': 'text',
                'label': _('URL Slug'),
                'group': 'basic',
            },
            'full_path': {
                'type': 'text',
                'label': _('Full Path'),
                'computed': True,
                'description': _('Breadcrumb path including parents'),
                'group': 'basic',
            },

            # Images
            'image_asset': {
                'type': 'image',
                'label': _('Category Image'),
                'fk_to': 'media_library.MediaAsset',
                'group': 'images',
            },
            'banner_asset': {
                'type': 'image',
                'label': _('Banner Image'),
                'fk_to': 'media_library.MediaAsset',
                'description': _('Category banner for headers'),
                'group': 'images',
            },

            # Display
            'icon': {
                'type': 'text',
                'label': _('Icon'),
                'description': _('Icon class or identifier'),
                'group': 'display',
            },
            'display_type': {
                'type': 'text',
                'label': _('Display Type'),
                'description': _('How products are displayed'),
                'group': 'display',
            },

            # Stats
            'product_count': {
                'type': 'text',
                'label': _('Product Count'),
                'computed': True,
                'description': _('Number of products in category'),
                'group': 'stats',
            },

            # Hierarchy
            'parent_name': {
                'type': 'text',
                'label': _('Parent Category'),
                'computed': True,
                'description': _('Name of parent category'),
                'group': 'hierarchy',
            },

            # SEO
            'meta_title': {
                'type': 'text',
                'label': _('Meta Title'),
                'description': _('SEO title'),
                'group': 'seo',
            },
            'meta_description': {
                'type': 'text',
                'label': _('Meta Description'),
                'description': _('SEO description'),
                'group': 'seo',
            },

            # URLs
            'url': {
                'type': 'url',
                'label': _('Category URL'),
                'computed': True,
                'description': _('Link to category page'),
                'group': 'urls',
            },
        }
    },
    'catalog.Brand': {
        'label': _('Brand'),
        'icon': 'fas fa-tag',
        'fields': {
            # Basic Info
            'name': {
                'type': 'text',
                'label': _('Brand Name'),
                'group': 'basic',
            },
            'description': {
                'type': 'text',
                'label': _('Description'),
                'group': 'basic',
            },
            'brand_story': {
                'type': 'text',
                'label': _('Brand Story'),
                'description': _('Extended brand narrative'),
                'group': 'basic',
            },
            'slug': {
                'type': 'text',
                'label': _('URL Slug'),
                'group': 'basic',
            },

            # Images
            'logo': {
                'type': 'image',
                'label': _('Logo'),
                'description': _('Brand logo image'),
                'group': 'images',
            },
            'banner_image': {
                'type': 'image',
                'label': _('Banner Image'),
                'description': _('Brand page banner'),
                'group': 'images',
            },

            # Stats
            'product_count': {
                'type': 'text',
                'label': _('Product Count'),
                'computed': True,
                'description': _('Number of products for brand'),
                'group': 'stats',
            },

            # Contact
            'website': {
                'type': 'url',
                'label': _('Website'),
                'description': _('Brand website URL'),
                'group': 'contact',
            },

            # SEO
            'meta_title': {
                'type': 'text',
                'label': _('Meta Title'),
                'description': _('SEO title'),
                'group': 'seo',
            },
            'meta_description': {
                'type': 'text',
                'label': _('Meta Description'),
                'description': _('SEO description'),
                'group': 'seo',
            },

            # URLs
            'url': {
                'type': 'url',
                'label': _('Brand URL'),
                'computed': True,
                'description': _('Link to brand page'),
                'group': 'urls',
            },
        }
    },
    'blog.BlogPost': {
        'label': _('Blog Post'),
        'icon': 'fas fa-newspaper',
        'fields': {
            # Basic Info
            'title': {
                'type': 'text',
                'label': _('Title'),
                'group': 'basic',
            },
            'excerpt': {
                'type': 'text',
                'label': _('Excerpt'),
                'description': _('Short summary for listings'),
                'group': 'basic',
            },
            'simple_content': {
                'type': 'text',
                'label': _('Content'),
                'description': _('Full post content'),
                'group': 'basic',
            },
            'slug': {
                'type': 'text',
                'label': _('URL Slug'),
                'group': 'basic',
            },
            'status': {
                'type': 'text',
                'label': _('Status'),
                'description': _('draft, scheduled, published, archived'),
                'group': 'basic',
            },

            # Images
            'featured_image': {
                'type': 'image',
                'label': _('Featured Image'),
                'fk_to': 'media_library.MediaAsset',
                'group': 'images',
            },
            'og_image': {
                'type': 'image',
                'label': _('Social Image'),
                'fk_to': 'media_library.MediaAsset',
                'description': _('Image for social media sharing'),
                'group': 'images',
            },

            # Author
            'author_name': {
                'type': 'text',
                'label': _('Author Name'),
                'computed': True,
                'description': _('Author display name'),
                'group': 'author',
            },
            'author_avatar': {
                'type': 'image',
                'label': _('Author Avatar'),
                'computed': True,
                'description': _('Author profile image'),
                'group': 'author',
            },

            # Category & Tags
            'category_name': {
                'type': 'text',
                'label': _('Category'),
                'computed': True,
                'description': _('Blog category name'),
                'group': 'taxonomy',
            },
            'tags_list': {
                'type': 'text',
                'label': _('Tags'),
                'computed': True,
                'description': _('Comma-separated tag names'),
                'group': 'taxonomy',
            },

            # Dates
            'published_at': {
                'type': 'text',
                'label': _('Published Date'),
                'description': _('Publication date'),
                'group': 'dates',
            },
            'created_at': {
                'type': 'text',
                'label': _('Created Date'),
                'group': 'dates',
            },
            'updated_at': {
                'type': 'text',
                'label': _('Updated Date'),
                'group': 'dates',
            },

            # Stats
            'reading_time_minutes': {
                'type': 'text',
                'label': _('Reading Time'),
                'description': _('Estimated minutes to read'),
                'group': 'stats',
            },
            'view_count': {
                'type': 'text',
                'label': _('View Count'),
                'description': _('Number of views'),
                'group': 'stats',
            },

            # SEO
            'meta_title': {
                'type': 'text',
                'label': _('Meta Title'),
                'description': _('SEO title'),
                'group': 'seo',
            },
            'meta_description': {
                'type': 'text',
                'label': _('Meta Description'),
                'description': _('SEO description'),
                'group': 'seo',
            },

            # URLs
            'url': {
                'type': 'url',
                'label': _('Post URL'),
                'computed': True,
                'description': _('Link to blog post'),
                'group': 'urls',
            },
        }
    },
}


def get_bindable_model_choices():
    """Return choices tuple for model selection fields."""
    return [(key, config['label']) for key, config in BINDABLE_MODELS.items()]


def get_model_fields(model_key):
    """Get field configuration for a specific model."""
    model_config = BINDABLE_MODELS.get(model_key, {})
    return model_config.get('fields', {})


def get_fields_by_type(model_key, field_type):
    """Get fields of a specific type (text, image, or url) for a model."""
    fields = get_model_fields(model_key)
    return {
        name: config
        for name, config in fields.items()
        if config.get('type') == field_type
    }


def get_image_fields(model_key):
    """Get all image-compatible fields for a model."""
    return get_fields_by_type(model_key, 'image')


def get_text_fields(model_key):
    """Get all text-compatible fields for a model."""
    return get_fields_by_type(model_key, 'text')


def get_url_fields(model_key):
    """Get all URL fields for a model."""
    return get_fields_by_type(model_key, 'url')


def get_fields_by_group(model_key, group):
    """Get all fields in a specific group for a model."""
    fields = get_model_fields(model_key)
    return {
        name: config
        for name, config in fields.items()
        if config.get('group') == group
    }


def get_field_groups(model_key):
    """Get all unique groups for a model's fields."""
    fields = get_model_fields(model_key)
    groups = set()
    for config in fields.values():
        if 'group' in config:
            groups.add(config['group'])
    return sorted(groups)
