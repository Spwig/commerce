"""
Storefront Page Audit Runner

Discovers and visits customer-facing storefront pages via Playwright,
collecting health data.
"""
from playwright.sync_api import Page

from tests.audit.engine import (
    AuditReport,
    PageResult,
    print_result_line,
    visit_page_browser,
)


# ── Static pages (always available) ─────────────────────────

STATIC_PAGES = [
    {"url": "/en/", "label": "Home"},
    {"url": "/en/products/", "label": "Products listing"},
    {"url": "/en/cart/", "label": "Cart (empty)"},
    {"url": "/en/blog/", "label": "Blog listing"},
    {"url": "/en/search/?q=test", "label": "Search results"},
]

# ── Authenticated pages ──────────────────────────────────────

AUTHENTICATED_PAGES = [
    {"url": "/en/account/dashboard/", "label": "Account dashboard"},
    {"url": "/en/account/addresses/", "label": "Address list"},
    {"url": "/en/account/profile/", "label": "Profile"},
]


def discover_storefront_pages(
    base_url: str,
    page: Page | None = None,
) -> list[dict]:
    """
    Build list of storefront URLs to audit by parsing live pages for links.
    Falls back to static pages if discovery fails.
    """
    pages = list(STATIC_PAGES)

    if page is None:
        return pages

    # Discover category pages from the home or products page
    try:
        page.goto(f"{base_url}/en/products/", wait_until="networkidle", timeout=15000)
        category_links = page.evaluate("""
            () => {
                const links = [];
                const seen = new Set();
                document.querySelectorAll('a[href*="/category/"]').forEach(a => {
                    const href = a.getAttribute('href');
                    const text = a.textContent.trim();
                    if (href && !seen.has(href) && text) {
                        seen.add(href);
                        links.push({url: href, label: 'Category: ' + text.substring(0, 40)});
                    }
                });
                return links.slice(0, 5);
            }
        """)
        pages.extend(category_links)
    except Exception:
        pass

    # Discover product pages
    try:
        product_links = page.evaluate("""
            () => {
                const links = [];
                const seen = new Set();
                document.querySelectorAll('a[href*="/product/"]').forEach(a => {
                    const href = a.getAttribute('href');
                    const text = a.textContent.trim();
                    if (href && !seen.has(href) && text) {
                        seen.add(href);
                        links.push({url: href, label: 'Product: ' + text.substring(0, 40)});
                    }
                });
                return links.slice(0, 5);
            }
        """)
        pages.extend(product_links)
    except Exception:
        pass

    # Discover blog posts
    try:
        page.goto(f"{base_url}/en/blog/", wait_until="networkidle", timeout=15000)
        blog_links = page.evaluate("""
            () => {
                const links = [];
                const seen = new Set();
                document.querySelectorAll('a[href*="/blog/"]').forEach(a => {
                    const href = a.getAttribute('href');
                    const text = a.textContent.trim();
                    // Skip nav/utility links, only get post links
                    if (href && !seen.has(href) && text &&
                        !href.includes('/category/') && !href.includes('/tag/') &&
                        !href.includes('/subscribe') && !href.includes('/feed/') &&
                        href !== '/en/blog/') {
                        seen.add(href);
                        links.push({url: href, label: 'Blog: ' + text.substring(0, 40)});
                    }
                });
                return links.slice(0, 3);
            }
        """)
        pages.extend(blog_links)
    except Exception:
        pass

    return pages


def login_storefront(page: Page, base_url: str, email: str, password: str):
    """Log in via allauth for storefront access."""
    page.goto(f"{base_url}/accounts/login/")
    page.fill('input[name="login"]', email)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")


def run_storefront_audit(
    page: Page,
    base_url: str,
    include_authenticated: bool = True,
    customer_email: str = "",
    customer_password: str = "",
    verbose: bool = True,
) -> AuditReport:
    """
    Run a full storefront page audit.
    Discovers pages dynamically by parsing links from live pages.
    """
    if verbose:
        print("  Discovering storefront pages...")

    pages = discover_storefront_pages(base_url, page)

    if verbose:
        print(f"  Found {len(pages)} public storefront pages")

    results: list[PageResult] = []

    # Visit public pages
    for i, pg in enumerate(pages, 1):
        result = visit_page_browser(
            page, url=pg["url"], label=pg["label"],
            base_url=base_url, category="storefront",
        )
        results.append(result)
        if verbose:
            print_result_line(i, len(pages), result)

    # Visit authenticated pages
    if include_authenticated and customer_email:
        if verbose:
            print(f"\n  Logging in as customer for authenticated pages...")
        try:
            login_storefront(page, base_url, customer_email, customer_password)
        except Exception as exc:
            if verbose:
                print(f"  \033[93mCustomer login failed: {exc}\033[0m")
            include_authenticated = False

    if include_authenticated and customer_email:
        auth_pages = list(AUTHENTICATED_PAGES)
        if verbose:
            print(f"  Visiting {len(auth_pages)} authenticated pages\n")

        offset = len(results)
        for i, pg in enumerate(auth_pages, 1):
            result = visit_page_browser(
                page, url=pg["url"], label=pg["label"],
                base_url=base_url, category="storefront",
            )
            results.append(result)
            if verbose:
                print_result_line(offset + i, offset + len(auth_pages), result)

    return AuditReport(category="storefront", results=results)
