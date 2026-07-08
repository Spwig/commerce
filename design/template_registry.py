"""
Template option schemas and resolution helpers for the Page Template system.

Each template type (checkout/product) has a registry of configurable options.
Options are stored as JSON in PageTemplateConfig and resolved at render time
by merging schema defaults < site config < per-product override.
"""
from django.utils.translation import gettext_lazy as _


# =============================================================================
# Checkout Template Options
# =============================================================================

CHECKOUT_TEMPLATE_OPTIONS = {
    'accordion': {
        'show_order_summary_sidebar': {
            'type': 'bool', 'default': True,
            'label': _('Show order summary sidebar'),
            'help': _('Display the order summary in a sticky sidebar on desktop.'),
        },
        'auto_advance_steps': {
            'type': 'bool', 'default': True,
            'label': _('Auto-advance to next step'),
            'help': _('Automatically open the next step after completing the current one.'),
        },
        'show_step_numbers': {
            'type': 'bool', 'default': True,
            'label': _('Show step numbers'),
            'help': _('Display numbered circles next to each checkout step.'),
        },
        'show_trust_badges': {
            'type': 'bool', 'default': True,
            'label': _('Show trust badges'),
            'help': _('Display security and trust badges below the payment section.'),
        },
        'show_express_checkout': {
            'type': 'bool', 'default': False,
            'label': _('Show express checkout'),
            'help': _('Show express checkout buttons (Apple Pay, Google Pay) at the top.'),
        },
    },
    'multi_step': {
        'show_order_summary_sidebar': {
            'type': 'bool', 'default': True,
            'label': _('Show order summary sidebar'),
            'help': _('Display order summary alongside each step.'),
        },
        'progress_bar_style': {
            'type': 'select', 'default': 'steps',
            'options': ['steps', 'bar', 'dots'],
            'label': _('Progress indicator style'),
            'help': _('How the progress through checkout steps is displayed.'),
        },
        'show_trust_badges': {
            'type': 'bool', 'default': True,
            'label': _('Show trust badges'),
            'help': _('Display security badges on the payment step.'),
        },
        'show_express_checkout': {
            'type': 'bool', 'default': False,
            'label': _('Show express checkout'),
            'help': _('Show express checkout buttons at the top of the first step.'),
        },
        'animation': {
            'type': 'select', 'default': 'slide',
            'options': ['slide', 'fade', 'none'],
            'label': _('Step transition animation'),
            'help': _('Animation style when transitioning between steps.'),
        },
    },
    'single_page': {
        'show_order_summary_sidebar': {
            'type': 'bool', 'default': True,
            'label': _('Show order summary sidebar'),
            'help': _('Display a sticky order summary sidebar.'),
        },
        'sticky_summary': {
            'type': 'bool', 'default': True,
            'label': _('Sticky summary on scroll'),
            'help': _('Keep the order summary visible while scrolling the form.'),
        },
        'show_trust_badges': {
            'type': 'bool', 'default': True,
            'label': _('Show trust badges'),
            'help': _('Display security badges near the payment section.'),
        },
        'show_section_dividers': {
            'type': 'bool', 'default': True,
            'label': _('Show section dividers'),
            'help': _('Display visual dividers between form sections.'),
        },
        'show_express_checkout': {
            'type': 'bool', 'default': False,
            'label': _('Show express checkout'),
            'help': _('Show express checkout buttons at the top.'),
        },
    },
    'express': {
        'show_order_summary': {
            'type': 'bool', 'default': True,
            'label': _('Show order summary'),
            'help': _('Display a compact order summary.'),
        },
        'allow_address_change': {
            'type': 'bool', 'default': True,
            'label': _('Allow address change'),
            'help': _('Allow customers to modify their pre-filled address.'),
        },
        'show_trust_badges': {
            'type': 'bool', 'default': True,
            'label': _('Show trust badges'),
            'help': _('Display security badges below the place order button.'),
        },
        'fallback_template': {
            'type': 'select', 'default': 'accordion',
            'options': ['accordion', 'multi_step', 'single_page'],
            'label': _('Fallback for new customers'),
            'help': _('Template to use when customer has no saved details.'),
        },
    },
}


# =============================================================================
# Product Template Options
# =============================================================================

PRODUCT_TEMPLATE_OPTIONS = {
    'classic': {
        'show_sku': {
            'type': 'bool', 'default': False,
            'label': _('Show SKU'),
            'help': _('Display the product SKU on the product page.'),
        },
        'show_brand': {
            'type': 'bool', 'default': True,
            'label': _('Show brand name'),
            'help': _('Display the brand name above the product title.'),
        },
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation above the product.'),
        },
        'show_short_description': {
            'type': 'bool', 'default': True,
            'label': _('Show short description'),
            'help': _('Display the short description above the add-to-cart button.'),
        },
        'show_social_share': {
            'type': 'bool', 'default': False,
            'label': _('Show social share buttons'),
            'help': _('Display social media sharing buttons.'),
        },
        'show_stock_indicator': {
            'type': 'bool', 'default': True,
            'label': _('Show stock indicator'),
            'help': _('Display stock availability status.'),
        },
        'floating_add_to_cart': {
            'type': 'bool', 'default': False,
            'label': _('Floating add-to-cart bar'),
            'help': _('Show a sticky add-to-cart bar when the main button scrolls out of view.'),
        },
        'floating_position': {
            'type': 'select', 'default': 'bottom',
            'options': ['bottom', 'top'],
            'label': _('Floating bar position'),
            'help': _('Where to show the floating add-to-cart bar.'),
        },
        'image_zoom': {
            'type': 'bool', 'default': True,
            'label': _('Image zoom on hover'),
            'help': _('Enable image magnification on hover.'),
        },
        'tab_style': {
            'type': 'select', 'default': 'tabs',
            'options': ['tabs', 'accordion', 'stacked'],
            'label': _('Info sections layout'),
            'help': _('How description, specifications, and reviews are displayed.'),
        },
    },
    'full_width': {
        'show_sku': {
            'type': 'bool', 'default': False,
            'label': _('Show SKU'),
            'help': _('Display the product SKU.'),
        },
        'show_brand': {
            'type': 'bool', 'default': True,
            'label': _('Show brand name'),
            'help': _('Display the brand name above the product title.'),
        },
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation.'),
        },
        'show_social_share': {
            'type': 'bool', 'default': True,
            'label': _('Show social share buttons'),
            'help': _('Display social sharing buttons.'),
        },
        'show_stock_indicator': {
            'type': 'bool', 'default': True,
            'label': _('Show stock indicator'),
            'help': _('Display stock availability.'),
        },
        'floating_add_to_cart': {
            'type': 'bool', 'default': True,
            'label': _('Floating add-to-cart bar'),
            'help': _('Show a sticky add-to-cart bar on scroll.'),
        },
        'floating_position': {
            'type': 'select', 'default': 'bottom',
            'options': ['bottom', 'top'],
            'label': _('Floating bar position'),
            'help': _('Where to show the floating add-to-cart bar.'),
        },
        'hero_gallery_height': {
            'type': 'select', 'default': 'medium',
            'options': ['small', 'medium', 'large', 'full'],
            'label': _('Gallery hero height'),
            'help': _('Height of the full-width gallery hero section.'),
        },
        'content_alignment': {
            'type': 'select', 'default': 'centered',
            'options': ['centered', 'left'],
            'label': _('Content alignment'),
            'help': _('Alignment of product info below the gallery.'),
        },
        'tab_style': {
            'type': 'select', 'default': 'stacked',
            'options': ['tabs', 'accordion', 'stacked'],
            'label': _('Info sections layout'),
            'help': _('How description, specs, and reviews are displayed.'),
        },
    },
    'gallery_focus': {
        'show_sku': {
            'type': 'bool', 'default': False,
            'label': _('Show SKU'),
            'help': _('Display the product SKU.'),
        },
        'show_brand': {
            'type': 'bool', 'default': True,
            'label': _('Show brand name'),
            'help': _('Display the brand name.'),
        },
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation.'),
        },
        'show_stock_indicator': {
            'type': 'bool', 'default': True,
            'label': _('Show stock indicator'),
            'help': _('Display stock availability.'),
        },
        'sticky_sidebar': {
            'type': 'bool', 'default': True,
            'label': _('Sticky product info'),
            'help': _('Keep product info sidebar visible while scrolling the gallery.'),
        },
        'gallery_columns': {
            'type': 'select', 'default': '2',
            'options': ['1', '2'],
            'label': _('Gallery grid columns'),
            'help': _('Number of columns in the gallery grid.'),
        },
        'image_zoom': {
            'type': 'bool', 'default': True,
            'label': _('Image zoom on hover'),
            'help': _('Enable image magnification on hover.'),
        },
        'tab_style': {
            'type': 'select', 'default': 'accordion',
            'options': ['tabs', 'accordion', 'stacked'],
            'label': _('Info sections layout'),
            'help': _('How description, specs, and reviews are displayed.'),
        },
    },
    'digital': {
        'show_sku': {
            'type': 'bool', 'default': False,
            'label': _('Show SKU'),
            'help': _('Display the product SKU.'),
        },
        'show_brand': {
            'type': 'bool', 'default': True,
            'label': _('Show brand name'),
            'help': _('Display the brand/publisher name.'),
        },
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation.'),
        },
        'show_instant_delivery_badge': {
            'type': 'bool', 'default': True,
            'label': _('Instant delivery badge'),
            'help': _('Show "Instant Digital Delivery" badge near add-to-cart.'),
        },
        'show_features_list': {
            'type': 'bool', 'default': True,
            'label': _('Show features list'),
            'help': _('Display a "What\'s Included" checklist section.'),
        },
        'show_license_info': {
            'type': 'bool', 'default': True,
            'label': _('Show license info'),
            'help': _('Display license type and terms if available.'),
        },
        'show_social_share': {
            'type': 'bool', 'default': True,
            'label': _('Show social share buttons'),
            'help': _('Display social sharing buttons.'),
        },
        'floating_add_to_cart': {
            'type': 'bool', 'default': False,
            'label': _('Floating add-to-cart bar'),
            'help': _('Show a sticky add-to-cart bar on scroll.'),
        },
        'tab_style': {
            'type': 'select', 'default': 'stacked',
            'options': ['tabs', 'accordion', 'stacked'],
            'label': _('Info sections layout'),
            'help': _('How description, specs, and reviews are displayed.'),
        },
    },
    'designer': {
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation above the product.'),
        },
        'show_short_description': {
            'type': 'bool', 'default': True,
            'label': _('Show short description'),
            'help': _('Display the short description in the header bar.'),
        },
        'floating_add_to_cart': {
            'type': 'bool', 'default': False,
            'label': _('Floating add-to-cart bar'),
            'help': _('Show a sticky add-to-cart bar when the main button scrolls out of view.'),
        },
        'floating_position': {
            'type': 'select', 'default': 'bottom',
            'options': ['bottom', 'top'],
            'label': _('Floating bar position'),
            'help': _('Where to show the floating add-to-cart bar.'),
        },
        'tab_style': {
            'type': 'select', 'default': 'tabs',
            'options': ['tabs', 'accordion', 'stacked'],
            'label': _('Info sections layout'),
            'help': _('How description, specifications, and reviews are displayed below the editor.'),
        },
    },
}


# =============================================================================
# Category Template Options
# =============================================================================

CATEGORY_TEMPLATE_OPTIONS = {
    'grid': {
        'show_banner': {
            'type': 'bool', 'default': True,
            'label': _('Show category banner'),
            'help': _('Display a hero banner when the category has a banner image.'),
        },
        'card_image_fallback': {
            'type': 'select', 'default': 'product',
            'options': ['product', 'placeholder'],
            'label': _('Card image fallback'),
            'help': _('When a category has no image: show first product image, or a placeholder icon.'),
        },
        'products_per_page': {
            'type': 'select', 'default': '24',
            'options': ['12', '24', '36', '48'],
            'label': _('Products per page'),
            'help': _('Number of products to display per page.'),
        },
        'products_per_row': {
            'type': 'select', 'default': 'auto',
            'options': ['auto', '3', '4', '5'],
            'label': _('Products per row'),
            'help': _('Number of products per row on desktop. Auto adjusts based on screen size.'),
        },
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation at the top of the page.'),
        },
        'show_subcategories': {
            'type': 'bool', 'default': True,
            'label': _('Show subcategories'),
            'help': _('Display subcategory chips when viewing a category with children.'),
        },
        'show_category_description': {
            'type': 'bool', 'default': True,
            'label': _('Show category description'),
            'help': _('Display the category description below the title.'),
        },
        'show_sort_bar': {
            'type': 'bool', 'default': True,
            'label': _('Show sort bar'),
            'help': _('Display the sort and product count toolbar above the product grid.'),
        },
        'show_product_count': {
            'type': 'bool', 'default': True,
            'label': _('Show product count'),
            'help': _('Display the total number of products in the toolbar.'),
        },
        'show_help_section': {
            'type': 'bool', 'default': True,
            'label': _('Show help section'),
            'help': _('Display the "Can\'t Find What You\'re Looking For?" section at the bottom.'),
        },
        'pagination_style': {
            'type': 'select', 'default': 'numbered',
            'options': ['numbered', 'load_more'],
            'label': _('Pagination style'),
            'help': _('How additional pages of products are loaded.'),
        },
        'default_sort': {
            'type': 'select', 'default': 'newest',
            'options': ['newest', 'price_low', 'price_high', 'name_az', 'name_za'],
            'label': _('Default sort order'),
            'help': _('The default sort order when no sort is specified.'),
        },
    },
    'list': {
        'show_banner': {
            'type': 'bool', 'default': True,
            'label': _('Show category banner'),
            'help': _('Display a hero banner when the category has a banner image.'),
        },
        'show_product_image': {
            'type': 'bool', 'default': True,
            'label': _('Show product image'),
            'help': _('Display product thumbnail images in each list row.'),
        },
        'image_position': {
            'type': 'select', 'default': 'left',
            'options': ['left', 'right'],
            'label': _('Image position'),
            'help': _('Which side of the row the product image appears on.'),
        },
        'show_short_description': {
            'type': 'bool', 'default': True,
            'label': _('Show short description'),
            'help': _('Display the product short description in each list row.'),
        },
        'show_subcategories': {
            'type': 'bool', 'default': True,
            'label': _('Show subcategories'),
            'help': _('Display subcategory chips when viewing a category with children.'),
        },
        'show_category_description': {
            'type': 'bool', 'default': True,
            'label': _('Show category description'),
            'help': _('Display the category description below the title.'),
        },
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation at the top of the page.'),
        },
        'show_sort_bar': {
            'type': 'bool', 'default': True,
            'label': _('Show sort bar'),
            'help': _('Display the sort and product count toolbar above the product list.'),
        },
        'show_product_count': {
            'type': 'bool', 'default': True,
            'label': _('Show product count'),
            'help': _('Display the total number of products in the toolbar.'),
        },
        'show_help_section': {
            'type': 'bool', 'default': True,
            'label': _('Show help section'),
            'help': _('Display the "Can\'t Find What You\'re Looking For?" section at the bottom.'),
        },
        'pagination_style': {
            'type': 'select', 'default': 'numbered',
            'options': ['numbered', 'load_more'],
            'label': _('Pagination style'),
            'help': _('How additional pages of products are loaded.'),
        },
        'default_sort': {
            'type': 'select', 'default': 'newest',
            'options': ['newest', 'price_low', 'price_high', 'name_az', 'name_za'],
            'label': _('Default sort order'),
            'help': _('The default sort order when no sort is specified.'),
        },
        'products_per_page': {
            'type': 'select', 'default': '24',
            'options': ['12', '24', '36', '48'],
            'label': _('Products per page'),
            'help': _('Number of products to display per page.'),
        },
    },
    'carousel': {
        'show_banner': {
            'type': 'bool', 'default': True,
            'label': _('Show category banner'),
            'help': _('Display a hero banner when the category has a banner image.'),
        },
        'slides_per_view': {
            'type': 'select', 'default': '4',
            'options': ['3', '4', '5'],
            'label': _('Slides per view'),
            'help': _('Number of product cards visible at once on desktop.'),
        },
        'autoplay': {
            'type': 'bool', 'default': False,
            'label': _('Autoplay'),
            'help': _('Automatically advance slides without user interaction.'),
        },
        'autoplay_speed': {
            'type': 'select', 'default': '5000',
            'options': ['3000', '5000', '7000'],
            'label': _('Autoplay speed'),
            'help': _('Time in milliseconds between automatic slide transitions.'),
        },
        'show_navigation_arrows': {
            'type': 'bool', 'default': True,
            'label': _('Show navigation arrows'),
            'help': _('Display left and right arrow buttons for manual navigation.'),
        },
        'show_dots': {
            'type': 'bool', 'default': True,
            'label': _('Show dot indicators'),
            'help': _('Display dot navigation below the carousel.'),
        },
        'infinite_loop': {
            'type': 'bool', 'default': True,
            'label': _('Infinite loop'),
            'help': _('Loop back to the beginning after reaching the last slide.'),
        },
        'show_subcategories': {
            'type': 'bool', 'default': True,
            'label': _('Show subcategories'),
            'help': _('Display subcategory chips when viewing a category with children.'),
        },
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation at the top of the page.'),
        },
        'show_sort_bar': {
            'type': 'bool', 'default': True,
            'label': _('Show sort bar'),
            'help': _('Display the sort and product count toolbar above the carousel.'),
        },
        'show_product_count': {
            'type': 'bool', 'default': True,
            'label': _('Show product count'),
            'help': _('Display the total number of products in the toolbar.'),
        },
        'show_help_section': {
            'type': 'bool', 'default': True,
            'label': _('Show help section'),
            'help': _('Display the "Can\'t Find What You\'re Looking For?" section at the bottom.'),
        },
        'pagination_style': {
            'type': 'select', 'default': 'numbered',
            'options': ['numbered', 'load_more'],
            'label': _('Pagination style'),
            'help': _('How additional pages of products are loaded.'),
        },
        'default_sort': {
            'type': 'select', 'default': 'newest',
            'options': ['newest', 'price_low', 'price_high', 'name_az', 'name_za'],
            'label': _('Default sort order'),
            'help': _('The default sort order when no sort is specified.'),
        },
        'row_size': {
            'type': 'select', 'default': '8',
            'options': ['4', '6', '8', '12'],
            'label': _('Products per row'),
            'help': _('Maximum products in each carousel row. Rows stack vertically — extra products create a new row below.'),
        },
        'products_per_page': {
            'type': 'select', 'default': '24',
            'options': ['12', '24', '36', '48'],
            'label': _('Products per page'),
            'help': _('Number of products to display per page.'),
        },
    },
    'masonry': {
        'show_banner': {
            'type': 'bool', 'default': True,
            'label': _('Show category banner'),
            'help': _('Display a hero banner when the category has a banner image.'),
        },
        'columns': {
            'type': 'select', 'default': '3',
            'options': ['2', '3', '4'],
            'label': _('Columns'),
            'help': _('Number of columns in the masonry grid on desktop.'),
        },
        'gap_size': {
            'type': 'select', 'default': 'md',
            'options': ['sm', 'md', 'lg'],
            'label': _('Gap size'),
            'help': _('Spacing between items in the masonry grid.'),
        },
        'show_subcategories': {
            'type': 'bool', 'default': True,
            'label': _('Show subcategories'),
            'help': _('Display subcategory chips when viewing a category with children.'),
        },
        'show_category_description': {
            'type': 'bool', 'default': True,
            'label': _('Show category description'),
            'help': _('Display the category description below the title.'),
        },
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation at the top of the page.'),
        },
        'show_sort_bar': {
            'type': 'bool', 'default': True,
            'label': _('Show sort bar'),
            'help': _('Display the sort and product count toolbar above the masonry grid.'),
        },
        'show_product_count': {
            'type': 'bool', 'default': True,
            'label': _('Show product count'),
            'help': _('Display the total number of products in the toolbar.'),
        },
        'show_help_section': {
            'type': 'bool', 'default': True,
            'label': _('Show help section'),
            'help': _('Display the "Can\'t Find What You\'re Looking For?" section at the bottom.'),
        },
        'pagination_style': {
            'type': 'select', 'default': 'numbered',
            'options': ['numbered', 'load_more'],
            'label': _('Pagination style'),
            'help': _('How additional pages of products are loaded.'),
        },
        'default_sort': {
            'type': 'select', 'default': 'newest',
            'options': ['newest', 'price_low', 'price_high', 'name_az', 'name_za'],
            'label': _('Default sort order'),
            'help': _('The default sort order when no sort is specified.'),
        },
        'products_per_page': {
            'type': 'select', 'default': '24',
            'options': ['12', '24', '36', '48'],
            'label': _('Products per page'),
            'help': _('Number of products to display per page.'),
        },
    },
    'featured': {
        'show_banner': {
            'type': 'bool', 'default': True,
            'label': _('Show category banner'),
            'help': _('Display a hero banner when the category has a banner image.'),
        },
        'featured_products_count': {
            'type': 'select', 'default': '1',
            'options': ['1', '2', '3'],
            'label': _('Featured products count'),
            'help': _('Number of products to highlight in the hero spotlight area.'),
        },
        'hero_layout': {
            'type': 'select', 'default': 'full_width',
            'options': ['full_width', 'split'],
            'label': _('Hero layout'),
            'help': _('Layout of the featured product hero section. Full width spans the page; split shows image and details side by side.'),
        },
        'show_subcategories': {
            'type': 'bool', 'default': True,
            'label': _('Show subcategories'),
            'help': _('Display subcategory chips when viewing a category with children.'),
        },
        'show_category_description': {
            'type': 'bool', 'default': True,
            'label': _('Show category description'),
            'help': _('Display the category description below the title.'),
        },
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation at the top of the page.'),
        },
        'show_sort_bar': {
            'type': 'bool', 'default': True,
            'label': _('Show sort bar'),
            'help': _('Display the sort and product count toolbar above the product grid.'),
        },
        'show_product_count': {
            'type': 'bool', 'default': True,
            'label': _('Show product count'),
            'help': _('Display the total number of products in the toolbar.'),
        },
        'show_help_section': {
            'type': 'bool', 'default': True,
            'label': _('Show help section'),
            'help': _('Display the "Can\'t Find What You\'re Looking For?" section at the bottom.'),
        },
        'pagination_style': {
            'type': 'select', 'default': 'numbered',
            'options': ['numbered', 'load_more'],
            'label': _('Pagination style'),
            'help': _('How additional pages of products are loaded.'),
        },
        'default_sort': {
            'type': 'select', 'default': 'newest',
            'options': ['newest', 'price_low', 'price_high', 'name_az', 'name_za'],
            'label': _('Default sort order'),
            'help': _('The default sort order when no sort is specified.'),
        },
        'products_per_page': {
            'type': 'select', 'default': '24',
            'options': ['12', '24', '36', '48'],
            'label': _('Products per page'),
            'help': _('Number of products to display per page.'),
        },
    },
    'accordion': {
        'panels_per_row': {
            'type': 'select', 'default': '6',
            'options': ['4', '5', '6', '7', '8'],
            'label': _('Panels per row'),
            'help': _('Maximum category panels per accordion row. When categories exceed this, additional rows are created below.'),
        },
        'height': {
            'type': 'select', 'default': 'lg',
            'options': ['sm', 'md', 'lg', 'xl'],
            'label': _('Panel height'),
            'help': _('Height of the accordion panels. Larger values create a more dramatic visual effect.'),
        },
        'expand_ratio': {
            'type': 'select', 'default': '3',
            'options': ['2', '3', '4', '5'],
            'label': _('Expand ratio'),
            'help': _('How much wider the active panel becomes relative to collapsed panels.'),
        },
        'transition_speed': {
            'type': 'select', 'default': '300',
            'options': ['200', '300', '500', '700'],
            'label': _('Transition speed'),
            'help': _('Duration in milliseconds for panel expand and collapse animations.'),
        },
        'overlay_style': {
            'type': 'select', 'default': 'bottom-left',
            'options': ['bottom-left', 'center-center', 'hero-bold', 'card', 'minimal'],
            'label': _('Overlay style'),
            'help': _('How the category name and info are displayed over the panel image.'),
        },
        'mobile_layout': {
            'type': 'select', 'default': 'stack',
            'options': ['stack', 'grid'],
            'label': _('Mobile layout'),
            'help': _('How panels are displayed on mobile devices. Stack shows them vertically; grid uses a compact grid.'),
        },
        'show_product_count_per_category': {
            'type': 'bool', 'default': True,
            'label': _('Show product count per category'),
            'help': _('Display the number of products in each category panel.'),
        },
        'show_breadcrumb': {
            'type': 'bool', 'default': True,
            'label': _('Show breadcrumb'),
            'help': _('Display breadcrumb navigation at the top of the page.'),
        },
        'show_help_section': {
            'type': 'bool', 'default': True,
            'label': _('Show help section'),
            'help': _('Display the "Can\'t Find What You\'re Looking For?" section at the bottom.'),
        },
    },
}


# =============================================================================
# Template file mappings
# =============================================================================

CHECKOUT_TEMPLATES = {
    'accordion': 'page_builder/checkout/accordion.html',
    'multi_step': 'page_builder/checkout/multi_step.html',
    'single_page': 'page_builder/checkout/single_page.html',
    'express': 'page_builder/checkout/express.html',
}

PRODUCT_TEMPLATES = {
    'classic': 'page_builder/product/classic.html',
    'full_width': 'page_builder/product/full_width.html',
    'gallery_focus': 'page_builder/product/gallery_focus.html',
    'digital': 'page_builder/product/digital.html',
    'booking': 'page_builder/product/booking.html',
    'designer': 'page_builder/product/designer.html',
}

CATEGORY_TEMPLATES = {
    'grid': 'page_builder/category/grid.html',
    'list': 'page_builder/category/list.html',
    'carousel': 'page_builder/category/carousel.html',
    'masonry': 'page_builder/category/masonry.html',
    'featured': 'page_builder/category/featured.html',
    'accordion': 'page_builder/category/accordion.html',
    # Backward compatibility
    'default': 'page_builder/category/grid.html',
}

BLOG_POST_TEMPLATES = {
    'classic': 'blog/post_detail.html',
    'minimal': 'blog/post_detail_minimal.html',
    'magazine': 'blog/post_detail_magazine.html',
    'full_width': 'blog/post_detail_full_width.html',
}

BLOG_LIST_TEMPLATES = {
    'grid': 'blog/blog_list.html',
    'list': 'blog/blog_list_list.html',
    'magazine': 'blog/blog_list_magazine.html',
    'minimal': 'blog/blog_list_minimal.html',
}


# =============================================================================
# Template metadata for admin UI
# =============================================================================

CHECKOUT_TEMPLATE_META = {
    'accordion': {
        'name': _('Accordion'),
        'description': _('All checkout steps on one page with collapsible sections. Steps collapse after completion, showing a summary. Great for general-purpose stores.'),
        'icon': 'fa-layer-group',
        'preview_image': 'design/images/templates/checkout/accordion.webp',
    },
    'multi_step': {
        'name': _('Multi-Step'),
        'description': _('One step per screen with a progress bar at top. Clean, focused input with smooth transitions. Ideal for mobile-first stores and impulse purchases.'),
        'icon': 'fa-shoe-prints',
        'preview_image': 'design/images/templates/checkout/multi_step.webp',
    },
    'single_page': {
        'name': _('Single Page'),
        'description': _('All checkout fields visible at once in a two-column layout. No collapsing or stepping. Perfect for B2B, repeat buyers, and digital products.'),
        'icon': 'fa-file-alt',
        'preview_image': 'design/images/templates/checkout/single_page.webp',
    },
    'express': {
        'name': _('Express'),
        'description': _('Streamlined checkout for returning customers with saved addresses and payment methods. Falls back to another template for new customers.'),
        'icon': 'fa-bolt',
        'preview_image': 'design/images/templates/checkout/express.webp',
    },
}

CATEGORY_TEMPLATE_META = {
    'grid': {
        'name': _('Grid'),
        'description': _('Classic responsive grid of product cards with configurable columns. The most versatile layout for general-purpose stores.'),
        'icon': 'fa-th-large',
        'preview_image': 'design/images/templates/category/category_grid.webp',
    },
    'list': {
        'name': _('List'),
        'description': _('Product rows with image and details side by side. Great for categories where customers need to compare specs at a glance.'),
        'icon': 'fa-list',
        'preview_image': 'design/images/templates/category/category_list.webp',
    },
    'carousel': {
        'name': _('Carousel'),
        'description': _('Horizontal product slider with navigation arrows and dot indicators. Ideal for curated collections and featured selections.'),
        'icon': 'fa-images',
        'preview_image': 'design/images/templates/category/category_carousel.webp',
    },
    'masonry': {
        'name': _('Masonry'),
        'description': _('Pinterest-style staggered grid that adapts to varying image heights. Best for visual products like fashion, art, and photography.'),
        'icon': 'fa-columns',
    },
    'featured': {
        'name': _('Featured'),
        'description': _('Large hero spotlight for top products with a supporting grid below. Perfect for categories with standout items or new arrivals.'),
        'icon': 'fa-star',
        'preview_image': 'design/images/templates/category/category_featured.webp',
    },
    'accordion': {
        'name': _('Accordion'),
        'description': _('Interactive horizontal image panels for browsing categories. Each panel expands on hover to reveal the category. Best for 3-8 categories.'),
        'icon': 'fa-layer-group',
    },
}

PRODUCT_TEMPLATE_META = {
    'classic': {
        'name': _('Classic'),
        'description': _('Gallery left, product info right. The familiar two-column layout used by major retailers. Tabs below for details, specs, and reviews.'),
        'icon': 'fa-columns',
        'preview_image': 'design/images/templates/product/classic.webp',
    },
    'full_width': {
        'name': _('Full Width'),
        'description': _('Large hero gallery spanning the full width, with product info centered below. Editorial feel that emphasizes product imagery. Great for lifestyle and luxury brands.'),
        'icon': 'fa-expand-arrows-alt',
        'preview_image': 'design/images/templates/product/full_width.webp',
    },
    'gallery_focus': {
        'name': _('Gallery Focus'),
        'description': _('Gallery-heavy 60/40 layout with a sticky info sidebar. Shows more images by default. Ideal for jewelry, furniture, art, and handmade products.'),
        'icon': 'fa-images',
        'preview_image': 'design/images/templates/product/gallery_focus.webp',
    },
    'digital': {
        'name': _('Digital'),
        'description': _('Optimized for digital products with feature lists, instant delivery badges, license info, and no shipping-related UI. Perfect for software, ebooks, and courses.'),
        'icon': 'fa-download',
        'preview_image': 'design/images/templates/product/digital.webp',
    },
    'designer': {
        'name': _('Designer'),
        'description': _('Full-width design editor with compact product info bar. Optimized for customizable products where the visual editor is the primary interaction.'),
        'icon': 'fa-paint-brush',
        'preview_image': 'design/images/templates/product/designer.webp',
    },
}

BLOG_POST_TEMPLATE_META = {
    'classic': {
        'name': _('Classic'),
        'description': _('Full-width featured image at top, article body below with sidebar. Traditional blog layout with categories, tags, and subscribe.'),
        'icon': 'fa-newspaper',
        'preview_image': 'design/images/templates/blog_post/blog_post_classic.webp',
    },
    'minimal': {
        'name': _('Minimal'),
        'description': _('Clean centered reading experience with no sidebar. Focus on typography and content with comfortable reading width.'),
        'icon': 'fa-align-left',
        'preview_image': 'design/images/templates/blog_post/blog_post_minimal.webp',
    },
    'magazine': {
        'name': _('Magazine'),
        'description': _('Large hero image, author bio section, and editorial feel with sidebar. Great for long-form content and storytelling.'),
        'icon': 'fa-book-open',
        'preview_image': 'design/images/templates/blog_post/blog_post_magazine.webp',
    },
    'full_width': {
        'name': _('Full Width'),
        'description': _('Edge-to-edge featured image hero with wide content area and no sidebar. Immersive layout for visual storytelling.'),
        'icon': 'fa-expand-arrows-alt',
        'preview_image': 'design/images/templates/blog_post/blog_post_fullwidth.webp',
    },
}

BLOG_LIST_TEMPLATE_META = {
    'grid': {
        'name': _('Grid'),
        'description': _('Card-based responsive grid with featured images, titles, and excerpts. Classic blog homepage layout.'),
        'icon': 'fa-th-large',
        'preview_image': 'design/images/templates/blog_list/blog_list_grid.webp',
    },
    'list': {
        'name': _('List'),
        'description': _('Full-width article rows with image on left and text on right. Scannable format for content-heavy blogs.'),
        'icon': 'fa-list',
        'preview_image': 'design/images/templates/blog_list/blog_list_list.webp',
    },
    'magazine': {
        'name': _('Magazine'),
        'description': _('Featured post hero at top with mixed grid and list layout below. Editorial magazine look and feel.'),
        'icon': 'fa-book-open',
        'preview_image': 'design/images/templates/blog_list/blog_list_magazine.webp',
    },
    'minimal': {
        'name': _('Minimal'),
        'description': _('Title-and-date list with no images. Clean, text-focused index page for blogs focused on writing.'),
        'icon': 'fa-align-left',
        'preview_image': 'design/images/templates/blog_list/blog_list_minimal.webp',
    },
}

BLOG_POST_TEMPLATE_OPTIONS = {
    'classic': {
        'show_sidebar': {
            'type': 'bool', 'default': True,
            'label': _('Show sidebar'),
            'help': _('Display sidebar with search, categories, tags, and subscribe.'),
        },
        'show_author': {
            'type': 'bool', 'default': True,
            'label': _('Show author'),
            'help': _('Display the post author name and avatar.'),
        },
        'show_share_buttons': {
            'type': 'bool', 'default': True,
            'label': _('Show share buttons'),
            'help': _('Display social sharing buttons after the article.'),
        },
        'show_related_posts': {
            'type': 'bool', 'default': True,
            'label': _('Show related posts'),
            'help': _('Display related articles after the post content.'),
        },
        'show_subscribe_cta': {
            'type': 'bool', 'default': True,
            'label': _('Show subscribe CTA'),
            'help': _('Display a subscribe call-to-action after the article.'),
        },
    },
    'minimal': {
        'show_author': {
            'type': 'bool', 'default': True,
            'label': _('Show author'),
            'help': _('Display the post author name.'),
        },
        'show_share_buttons': {
            'type': 'bool', 'default': False,
            'label': _('Show share buttons'),
            'help': _('Display social sharing buttons after the article.'),
        },
        'show_related_posts': {
            'type': 'bool', 'default': True,
            'label': _('Show related posts'),
            'help': _('Display related articles after the post content.'),
        },
        'max_width': {
            'type': 'select', 'default': '720px',
            'label': _('Content width'),
            'help': _('Maximum width of the article content.'),
            'options': ['640px', '720px', '800px'],
        },
    },
    'magazine': {
        'show_sidebar': {
            'type': 'bool', 'default': True,
            'label': _('Show sidebar'),
            'help': _('Display sidebar with search, categories, tags, and subscribe.'),
        },
        'show_author_bio': {
            'type': 'bool', 'default': True,
            'label': _('Show author bio'),
            'help': _('Display full author biography section below the article.'),
        },
        'show_share_buttons': {
            'type': 'bool', 'default': True,
            'label': _('Show share buttons'),
            'help': _('Display social sharing buttons after the article.'),
        },
        'show_related_posts': {
            'type': 'bool', 'default': True,
            'label': _('Show related posts'),
            'help': _('Display related articles after the post content.'),
        },
    },
    'full_width': {
        'show_author': {
            'type': 'bool', 'default': True,
            'label': _('Show author'),
            'help': _('Display the post author name and avatar.'),
        },
        'show_share_buttons': {
            'type': 'bool', 'default': True,
            'label': _('Show share buttons'),
            'help': _('Display social sharing buttons after the article.'),
        },
        'show_related_posts': {
            'type': 'bool', 'default': True,
            'label': _('Show related posts'),
            'help': _('Display related articles after the post content.'),
        },
        'show_subscribe_cta': {
            'type': 'bool', 'default': True,
            'label': _('Show subscribe CTA'),
            'help': _('Display a subscribe call-to-action after the article.'),
        },
    },
}

BLOG_LIST_TEMPLATE_OPTIONS = {
    'grid': {
        'columns': {
            'type': 'select', 'default': '3',
            'label': _('Grid columns'),
            'help': _('Number of columns in the blog post grid.'),
            'options': ['2', '3', '4'],
        },
        'show_excerpt': {
            'type': 'bool', 'default': True,
            'label': _('Show excerpt'),
            'help': _('Display post excerpt below the title.'),
        },
        'show_author': {
            'type': 'bool', 'default': True,
            'label': _('Show author'),
            'help': _('Display the post author name.'),
        },
        'show_date': {
            'type': 'bool', 'default': True,
            'label': _('Show date'),
            'help': _('Display the published date.'),
        },
        'show_category': {
            'type': 'bool', 'default': True,
            'label': _('Show category'),
            'help': _('Display the post category badge.'),
        },
    },
    'list': {
        'show_excerpt': {
            'type': 'bool', 'default': True,
            'label': _('Show excerpt'),
            'help': _('Display post excerpt in each row.'),
        },
        'show_image': {
            'type': 'bool', 'default': True,
            'label': _('Show image'),
            'help': _('Display featured image thumbnail.'),
        },
        'show_author': {
            'type': 'bool', 'default': True,
            'label': _('Show author'),
            'help': _('Display the post author name.'),
        },
        'show_reading_time': {
            'type': 'bool', 'default': True,
            'label': _('Show reading time'),
            'help': _('Display estimated reading time.'),
        },
    },
    'magazine': {
        'featured_count': {
            'type': 'select', 'default': '1',
            'label': _('Featured posts'),
            'help': _('Number of featured/hero posts at the top.'),
            'options': ['1', '2', '3'],
        },
        'show_excerpt': {
            'type': 'bool', 'default': True,
            'label': _('Show excerpt'),
            'help': _('Display post excerpt below the title.'),
        },
        'show_category': {
            'type': 'bool', 'default': True,
            'label': _('Show category'),
            'help': _('Display the post category badge.'),
        },
    },
    'minimal': {
        'show_date': {
            'type': 'bool', 'default': True,
            'label': _('Show date'),
            'help': _('Display the published date.'),
        },
        'show_category': {
            'type': 'bool', 'default': True,
            'label': _('Show category'),
            'help': _('Display the post category.'),
        },
        'show_reading_time': {
            'type': 'bool', 'default': False,
            'label': _('Show reading time'),
            'help': _('Display estimated reading time.'),
        },
    },
}


# =============================================================================
# Resolution helpers
# =============================================================================

def get_checkout_options(template_key, merchant_overrides=None):
    """Resolve checkout template options by merging schema defaults with merchant overrides.

    Args:
        template_key: The checkout template key (e.g. 'accordion')
        merchant_overrides: Dict of merchant-saved option values

    Returns:
        Dict of resolved option key -> value
    """
    schema = CHECKOUT_TEMPLATE_OPTIONS.get(template_key, {})
    overrides = merchant_overrides or {}
    resolved = {}
    for key, definition in schema.items():
        resolved[key] = overrides.get(key, definition['default'])
    return resolved


def get_product_options(template_key, site_options=None, product_overrides=None):
    """Resolve product template options with three-level merge.

    Priority: product override > site config > schema default

    Args:
        template_key: The product template key (e.g. 'classic')
        site_options: Dict of site-wide option values from PageTemplateConfig
        product_overrides: Dict of per-product option overrides (currently unused, reserved)

    Returns:
        Dict of resolved option key -> value
    """
    schema = PRODUCT_TEMPLATE_OPTIONS.get(template_key, {})
    site = site_options or {}
    product = product_overrides or {}
    resolved = {}
    for key, definition in schema.items():
        if key in product:
            resolved[key] = product[key]
        elif key in site:
            resolved[key] = site[key]
        else:
            resolved[key] = definition['default']
    return resolved


def get_checkout_template_path(template_key):
    """Get the template file path for a checkout template key."""
    return CHECKOUT_TEMPLATES.get(template_key, CHECKOUT_TEMPLATES['accordion'])


def get_product_template_path(template_key):
    """Get the template file path for a product template key."""
    return PRODUCT_TEMPLATES.get(template_key, PRODUCT_TEMPLATES['classic'])


def get_category_options(template_key, site_options=None, category_overrides=None):
    """Resolve category template options with three-level merge.

    Priority: category override > site config > schema default

    Args:
        template_key: The category template key (e.g. 'grid')
        site_options: Dict of site-wide option values from PageTemplateConfig
        category_overrides: Dict of per-category option overrides

    Returns:
        Dict of resolved option key -> value
    """
    # Backward compatibility
    if template_key == 'default':
        template_key = 'grid'
    schema = CATEGORY_TEMPLATE_OPTIONS.get(template_key, {})
    site = site_options or {}
    category = category_overrides or {}
    resolved = {}
    for key, definition in schema.items():
        if key in category:
            resolved[key] = category[key]
        elif key in site:
            resolved[key] = site[key]
        else:
            resolved[key] = definition['default']
    return resolved


def get_category_template_path(template_key):
    """Get the template file path for a category template key."""
    if template_key == 'default':
        template_key = 'grid'
    return CATEGORY_TEMPLATES.get(template_key, CATEGORY_TEMPLATES['grid'])


def get_blog_post_options(template_key, site_options=None, post_overrides=None):
    """Resolve blog post template options with three-level merge.

    Priority: post override > site config > schema default

    Args:
        template_key: The blog post template key (e.g. 'classic')
        site_options: Dict of site-wide option values from PageTemplateConfig
        post_overrides: Dict of per-post option overrides

    Returns:
        Dict of resolved option key -> value
    """
    schema = BLOG_POST_TEMPLATE_OPTIONS.get(template_key, {})
    site = site_options or {}
    post = post_overrides or {}
    resolved = {}
    for key, definition in schema.items():
        if key in post:
            resolved[key] = post[key]
        elif key in site:
            resolved[key] = site[key]
        else:
            resolved[key] = definition['default']
    return resolved


def get_blog_post_template_path(template_key):
    """Get the template file path for a blog post template key."""
    return BLOG_POST_TEMPLATES.get(template_key, BLOG_POST_TEMPLATES['classic'])


def get_blog_list_options(template_key, site_options=None):
    """Resolve blog list template options.

    Priority: site config > schema default

    Args:
        template_key: The blog list template key (e.g. 'grid')
        site_options: Dict of site-wide option values from PageTemplateConfig

    Returns:
        Dict of resolved option key -> value
    """
    schema = BLOG_LIST_TEMPLATE_OPTIONS.get(template_key, {})
    site = site_options or {}
    resolved = {}
    for key, definition in schema.items():
        if key in site:
            resolved[key] = site[key]
        else:
            resolved[key] = definition['default']
    return resolved


def get_blog_list_template_path(template_key):
    """Get the template file path for a blog list template key."""
    return BLOG_LIST_TEMPLATES.get(template_key, BLOG_LIST_TEMPLATES['grid'])
