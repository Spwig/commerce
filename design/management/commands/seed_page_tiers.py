from core.management.commands._seed_base import SeedCommand


class Command(SeedCommand):
    seed_name = "page_tiers"
    seed_version = 1
    help = "Seed page tier configurations (security tiers A/B/C)"

    TIER_A_CSP = {
        "default-src": ["'self'"],
        "script-src": ["'self'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:", "https:"],
        "font-src": ["'self'"],
        "connect-src": ["'self'"],
        "frame-src": ["'none'"],
        "object-src": ["'none'"],
    }
    TIER_B_CSP = {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:", "https:"],
        "font-src": ["'self'", "https:"],
        "connect-src": ["'self'"],
        "frame-src": ["'self'"],
        "object-src": ["'none'"],
    }
    TIER_C_CSP = {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["*"],
        "font-src": ["*"],
        "connect-src": ["*"],
        "frame-src": ["*"],
        "object-src": ["'self'"],
    }

    TIERS = [
        {
            "page_type": "checkout",
            "tier": "A",
            "display_name": "Checkout Page",
            "description": "Checkout and payment processing page. Highest security tier.",
            "schema": {
                "regions": {
                    "header": {
                        "label": "Header",
                        "description": "Checkout header area",
                        "locked": True,
                    },
                    "breadcrumb": {
                        "label": "Breadcrumb",
                        "description": "Checkout progress indicator",
                        "locked": True,
                    },
                    "main": {
                        "label": "Main Content",
                        "description": "Checkout form and cart summary",
                        "locked": True,
                    },
                    "footer": {
                        "label": "Footer",
                        "description": "Minimal checkout footer",
                        "locked": True,
                    },
                },
                "required_components": ["checkout_form", "cart_summary", "payment_method_selector"],
            },
            "csp_policy": TIER_A_CSP,
            "max_external_scripts": 0,
            "allows_custom_html": False,
            "locked_regions": ["header", "breadcrumb", "main", "footer"],
        },
        {
            "page_type": "cart",
            "tier": "A",
            "display_name": "Shopping Cart",
            "description": "Shopping cart page. System-critical for commerce operations.",
            "schema": {
                "regions": {
                    "header": {
                        "label": "Header",
                        "description": "Cart page header",
                        "locked": False,
                    },
                    "main": {
                        "label": "Cart Content",
                        "description": "Cart items and totals",
                        "locked": True,
                    },
                    "recommendations": {
                        "label": "Recommendations",
                        "description": "Product recommendations",
                        "locked": False,
                    },
                    "footer": {"label": "Footer", "description": "Cart footer", "locked": False},
                },
                "required_components": ["cart_items", "cart_totals", "checkout_button"],
            },
            "csp_policy": TIER_A_CSP,
            "max_external_scripts": 0,
            "allows_custom_html": False,
            "locked_regions": ["main"],
        },
        {
            "page_type": "product",
            "tier": "B",
            "display_name": "Product Page",
            "description": "Individual product detail pages. Controlled customization allowed.",
            "schema": {
                "regions": {
                    "header": {
                        "label": "Header",
                        "description": "Product page header",
                        "locked": False,
                    },
                    "breadcrumb": {
                        "label": "Breadcrumb",
                        "description": "Navigation breadcrumb",
                        "locked": False,
                    },
                    "hero": {
                        "label": "Hero Section",
                        "description": "Product images and primary info",
                        "locked": False,
                    },
                    "main": {
                        "label": "Main Content",
                        "description": "Product details and add to cart",
                        "locked": True,
                    },
                    "sidebar": {
                        "label": "Sidebar",
                        "description": "Additional product info",
                        "locked": False,
                    },
                    "related": {
                        "label": "Related Products",
                        "description": "Related products section",
                        "locked": False,
                    },
                    "footer": {
                        "label": "Footer",
                        "description": "Product page footer",
                        "locked": False,
                    },
                },
                "required_components": ["product_info", "add_to_cart_button", "product_gallery"],
            },
            "csp_policy": TIER_B_CSP,
            "max_external_scripts": 3,
            "allows_custom_html": False,
            "locked_regions": ["main"],
        },
        {
            "page_type": "collection",
            "tier": "B",
            "display_name": "Collection Page",
            "description": "Product collection and category pages. Moderate customization allowed.",
            "schema": {
                "regions": {
                    "header": {
                        "label": "Header",
                        "description": "Collection page header",
                        "locked": False,
                    },
                    "breadcrumb": {
                        "label": "Breadcrumb",
                        "description": "Navigation breadcrumb",
                        "locked": False,
                    },
                    "hero": {
                        "label": "Collection Hero",
                        "description": "Collection banner",
                        "locked": False,
                    },
                    "filters": {
                        "label": "Filters Sidebar",
                        "description": "Product filtering",
                        "locked": True,
                    },
                    "main": {
                        "label": "Product Grid",
                        "description": "Product listing grid",
                        "locked": True,
                    },
                    "footer": {
                        "label": "Footer",
                        "description": "Collection page footer",
                        "locked": False,
                    },
                },
                "required_components": ["product_grid", "filter_sidebar", "pagination"],
            },
            "csp_policy": TIER_B_CSP,
            "max_external_scripts": 3,
            "allows_custom_html": False,
            "locked_regions": ["filters", "main"],
        },
        {
            "page_type": "home",
            "tier": "C",
            "display_name": "Homepage",
            "description": "Store homepage. Full customization flexibility for marketing.",
            "schema": {
                "regions": {
                    "header": {
                        "label": "Header",
                        "description": "Homepage header",
                        "locked": False,
                    },
                    "hero": {
                        "label": "Hero Section",
                        "description": "Main hero/banner area",
                        "locked": False,
                    },
                    "featured": {
                        "label": "Featured Section",
                        "description": "Featured products or content",
                        "locked": False,
                    },
                    "content_1": {
                        "label": "Content Block 1",
                        "description": "First content section",
                        "locked": False,
                    },
                    "content_2": {
                        "label": "Content Block 2",
                        "description": "Second content section",
                        "locked": False,
                    },
                    "content_3": {
                        "label": "Content Block 3",
                        "description": "Third content section",
                        "locked": False,
                    },
                    "footer": {
                        "label": "Footer",
                        "description": "Homepage footer",
                        "locked": False,
                    },
                },
                "required_components": [],
            },
            "csp_policy": TIER_C_CSP,
            "max_external_scripts": -1,
            "allows_custom_html": True,
            "locked_regions": [],
        },
        {
            "page_type": "landing",
            "tier": "C",
            "display_name": "Landing Page",
            "description": "Marketing landing pages. Maximum flexibility for campaigns.",
            "schema": {
                "regions": {
                    "header": {
                        "label": "Header",
                        "description": "Landing page header",
                        "locked": False,
                    },
                    "hero": {
                        "label": "Hero Section",
                        "description": "Landing hero section",
                        "locked": False,
                    },
                    "content": {
                        "label": "Main Content",
                        "description": "Landing page content",
                        "locked": False,
                    },
                    "cta": {
                        "label": "Call to Action",
                        "description": "CTA section",
                        "locked": False,
                    },
                    "footer": {
                        "label": "Footer",
                        "description": "Landing page footer",
                        "locked": False,
                    },
                },
                "required_components": [],
            },
            "csp_policy": TIER_C_CSP,
            "max_external_scripts": -1,
            "allows_custom_html": True,
            "locked_regions": [],
        },
    ]

    def seed(self) -> int:
        from design.models import PageTier

        count = 0
        for data in self.TIERS:
            _, created = PageTier.objects.update_or_create(
                page_type=data["page_type"],
                defaults=data,
            )
            if created:
                count += 1
        return count
