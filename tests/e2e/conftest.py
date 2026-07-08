"""
Playwright E2E test fixtures.

Provides browser, page, and checkout helper fixtures for
end-to-end browser testing against a live Django server.
"""
import os
import pytest
import time
from decimal import Decimal
from playwright.sync_api import sync_playwright, Page

# Allow Django DB access from async context (needed for pytest-playwright + live_server)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


# ============================================================
# Browser lifecycle (session-scoped for performance)
# ============================================================

@pytest.fixture(scope='session')
def browser_type_launch_args():
    """Playwright launch arguments."""
    return {'headless': True}


@pytest.fixture(scope='session')
def browser_instance():
    """Single browser instance reused across the entire test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance, live_server):
    """Fresh browser page per test, wired to the live server."""
    pg = browser_instance.new_page()
    pg._live_server_url = live_server.url
    yield pg
    pg.close()


# ============================================================
# Authentication
# ============================================================

@pytest.fixture
def authenticated_page(page, customer_user, site_settings):
    """Browser page with logged-in customer.

    Depends on site_settings to ensure SiteSettings exists before any
    browser navigation (required by CurrencyMiddleware).
    """
    base = page._live_server_url
    # allauth URLs are outside i18n_patterns - no /en/ prefix
    page.goto(f'{base}/accounts/login/')
    page.fill('input[name="login"]', customer_user.email)
    page.fill('input[name="password"]', 'testpass123')
    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle')
    return page


# ============================================================
# Checkout Helper
# ============================================================

class CheckoutHelper:
    """
    High-level helper for driving the checkout flow in Playwright.

    Usage:
        def test_checkout(checkout):
            checkout.add_to_cart(product.id)
            checkout.go_to_checkout()
            checkout.submit_contact()
            checkout.fill_address(country='US', city='NYC', state='NY', ...)
            checkout.submit_address()
            checkout.select_shipping_method('Standard Shipping')
            ...
    """

    def __init__(self, page: Page):
        self.page = page
        self.base_url = page._live_server_url

    # --- Cart operations ---

    def _get_csrf_token(self) -> str:
        """Get CSRF token from httponly cookie via Playwright API."""
        cookies = self.page.context.cookies()
        for cookie in cookies:
            if cookie['name'] == 'csrftoken':
                return cookie['value']
        return ''

    def _inject_csrf_token(self):
        """Inject CSRF token into the DOM so checkout JS can read it.

        The checkout JS getCsrfToken() tries document.cookie first (fails
        because CSRF_COOKIE_HTTPONLY=True), then falls back to reading
        [name=csrfmiddlewaretoken] from the DOM. We inject that element
        so the fallback succeeds.
        """
        csrf = self._get_csrf_token()
        if csrf:
            self.page.evaluate(f'''
                () => {{
                    if (!document.querySelector('[name=csrfmiddlewaretoken]')) {{
                        const input = document.createElement('input');
                        input.type = 'hidden';
                        input.name = 'csrfmiddlewaretoken';
                        input.value = '{csrf}';
                        document.body.appendChild(input);
                    }}
                }}
            ''')

    def add_to_cart(self, product_id: int, quantity: int = 1):
        """Add product to cart via API (faster than UI clicks)."""
        # CSRF_COOKIE_HTTPONLY=True prevents JS from reading the cookie,
        # so we use Playwright's cookie API to get the token
        csrf = self._get_csrf_token()
        self.page.evaluate(f'''
            async () => {{
                await fetch('/api/cart/add/', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{csrf}',
                    }},
                    body: JSON.stringify({{product_id: {product_id}, quantity: {quantity}}}),
                }});
            }}
        ''')

    # --- Navigation ---

    def go_to_checkout(self):
        """Navigate to checkout page and wait for it to load."""
        self.page.goto(f'{self.base_url}/en/checkout/')
        self.page.wait_for_load_state('networkidle')
        # Inject CSRF token into DOM so checkout JS API calls can find it
        # (CSRF_COOKIE_HTTPONLY=True prevents JS from reading the cookie)
        self._inject_csrf_token()
        # Wait for checkout JS to initialize (accordion uses .checkout-step,
        # multi-step uses .multistep__step)
        self.page.wait_for_selector(
            '.checkout-step, .multistep__step, #checkout-steps',
            timeout=10000,
        )

    def go_to_cart(self):
        """Navigate to cart page."""
        self.page.goto(f'{self.base_url}/en/cart/')
        self.page.wait_for_load_state('networkidle')

    # --- Step: Contact ---

    def submit_contact(self, email: str = None):
        """Submit contact step (email)."""
        if email:
            self.page.fill('#checkout-email', email)
        self.page.click('[data-action="continue-contact"]')
        self.page.wait_for_timeout(500)

    # --- Step: Shipping Address ---

    def fill_address(
        self, name='Test User', address1='456 Broadway',
        city='New York', state='NY', postal_code='10013', country='US',
        use_new=True,
    ):
        """Fill the shipping address form."""
        if use_new:
            # Click "Use a different address" if saved addresses exist
            toggle = self.page.query_selector('[data-action="toggle-new-address"]')
            if toggle:
                toggle.click()
                self.page.wait_for_timeout(200)

        self.page.fill('#shipping-name', name)
        self.page.fill('#shipping-address1', address1)
        self.page.fill('#shipping-city', city)
        self.page.fill('#shipping-state', state)
        self.page.fill('#shipping-postal-code', postal_code)
        self.page.fill('#shipping-country', country)

    def submit_address(self):
        """Submit the shipping address and wait for shipping methods to load."""
        self.page.click('[data-action="continue-shipping"]')
        # fetchShippingMethods() first shows a loading spinner (.checkout-empty-state
        # with .fa-spinner), then replaces it with actual results. We need to wait
        # for the spinner to disappear AND the final state to appear.
        # Wait for shipping-method step to become active (address submitted)
        self.page.wait_for_timeout(500)
        # Wait for shipping methods API call to complete (spinner goes away)
        self.page.wait_for_selector(
            '.shipping-method-card, .checkout-empty-state .fa-exclamation-circle',
            timeout=15000,
        )

    # --- Step: Shipping Method ---

    def select_shipping_method(self, method_name: str):
        """Select a shipping method by name and submit."""
        cards = self.page.query_selector_all('.shipping-method-card')
        for card in cards:
            name_el = card.query_selector('.shipping-method-card__name')
            if name_el and method_name in name_el.text_content():
                card.query_selector('input[type="radio"]').click()
                break
        self.page.click('[data-action="continue-shipping-method"]')
        self.page.wait_for_timeout(1000)

    def wait_for_payment_step(self):
        """Wait for payment step to finish loading after shipping method submit.

        fetchPaymentProviders() shows a spinner first (.fa-spinner), then
        renders either payment cards or empty state (.fa-credit-card).
        Wait for the spinner to disappear (i.e. final state rendered).
        """
        self.page.wait_for_selector(
            '.payment-provider-card, .checkout-empty-state .fa-credit-card',
            timeout=15000,
        )

    def get_available_shipping_methods(self) -> list:
        """Get list of available shipping method names."""
        cards = self.page.query_selector_all('.shipping-method-card__name')
        return [card.text_content().strip() for card in cards]

    def get_shipping_method_cost(self, method_name: str) -> str:
        """Get the displayed cost for a shipping method."""
        cards = self.page.query_selector_all('.shipping-method-card')
        for card in cards:
            name_el = card.query_selector('.shipping-method-card__name')
            if name_el and method_name in name_el.text_content():
                price_el = card.query_selector('.shipping-method-card__price')
                return price_el.text_content().strip() if price_el else ''
        return ''

    # --- Step: Payment ---

    def select_payment_provider(self, provider_name: str = None):
        """Select a payment provider (first one if name not specified)."""
        if provider_name:
            cards = self.page.query_selector_all('.payment-provider-card')
            for card in cards:
                name_el = card.query_selector('.payment-provider-card__name')
                if name_el and provider_name in name_el.text_content():
                    card.query_selector('input[type="radio"]').click()
                    break
        else:
            # Select first available
            first = self.page.query_selector('.payment-provider-card input[type="radio"]')
            if first:
                first.click()

        self.page.click('[data-action="continue-payment"]')
        self.page.wait_for_timeout(500)

    # --- Order Summary ---

    def get_summary(self) -> dict:
        """Read the order summary sidebar values."""
        return self.page.evaluate('''
            () => ({
                subtotal: document.getElementById('summary-subtotal')?.textContent || '',
                shipping: document.getElementById('summary-shipping')?.textContent || '',
                discount: document.getElementById('summary-discount')?.textContent || '',
                tax: document.getElementById('summary-tax')?.textContent || '',
                total: document.getElementById('summary-total')?.textContent || '',
            })
        ''')

    # --- Step State ---

    def get_step_state(self, step_name: str) -> str:
        """Get step state: 'active', 'completed', or 'disabled'."""
        el = self.page.query_selector(f'[data-step="{step_name}"]')
        if not el:
            return 'missing'
        classes = el.get_attribute('class') or ''
        if '--active' in classes:
            return 'active'
        if '--completed' in classes:
            return 'completed'
        return 'disabled'

    def get_current_step(self) -> str:
        """Get the name of the currently active step."""
        el = self.page.query_selector(
            '.checkout-step--active, .multistep__step--active'
        )
        return el.get_attribute('data-step') if el else None

    # --- Performance ---

    def measure_transition(self, action_callable) -> float:
        """Measure time in ms for an action to complete."""
        start = time.monotonic()
        action_callable()
        return (time.monotonic() - start) * 1000

    # --- Review step ---

    def get_review_data(self) -> dict:
        """Read review step data."""
        return self.page.evaluate('''
            () => ({
                contact: document.getElementById('review-contact')?.textContent || '',
                shipping: document.getElementById('review-shipping')?.textContent || '',
                shippingMethod: document.getElementById('review-shipping-method')?.textContent || '',
                payment: document.getElementById('review-payment')?.textContent || '',
            })
        ''')


@pytest.fixture
def checkout(authenticated_page, site_settings, warehouse):
    """
    Checkout helper fixture.

    Provides a CheckoutHelper instance with an authenticated browser page.
    Requires site_settings and warehouse to exist.
    """
    return CheckoutHelper(authenticated_page)


# ============================================================
# Admin Authentication
# ============================================================

@pytest.fixture
def admin_authenticated_page(page, admin_user, site_settings):
    """Browser page with logged-in admin user via Django admin.

    Depends on site_settings to ensure SiteSettings exists before any
    browser navigation (required by CurrencyMiddleware).
    """
    base = page._live_server_url
    page.goto(f'{base}/en/admin/login/')
    page.fill('input[name="username"]', admin_user.username)
    page.fill('input[name="password"]', 'testpass123')
    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle')
    return page


# ============================================================
# Payment Provider Fixtures
# ============================================================

@pytest.fixture
def stripe_provider(db, admin_user):
    """Create a test Stripe payment provider account with encrypted credentials."""
    import os
    from tests.factories import PaymentProviderAccountFactory

    return PaymentProviderAccountFactory(
        user=admin_user,
        display_name='Test Stripe',
        checkout_mode='hosted',
    )


# ============================================================
# Product Page Helper
# ============================================================

class ProductPageHelper:
    """Helper for navigating to and verifying product pages."""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = page._live_server_url

    def go_to_product(self, product_slug: str):
        """Navigate to product detail page."""
        self.page.goto(f'{self.base_url}/en/product/{product_slug}/')
        self.page.wait_for_load_state('networkidle')

    def get_product_title(self) -> str:
        """Get product title text."""
        el = self.page.query_selector('.product-info__title')
        return el.text_content().strip() if el else ''

    def get_product_price(self) -> str:
        """Get product price text."""
        el = self.page.query_selector('#product-price .price')
        return el.text_content().strip() if el else ''

    def get_product_sku(self) -> str:
        """Get product SKU text."""
        el = self.page.query_selector('#product-sku')
        return el.text_content().strip() if el else ''

    def has_add_to_cart_button(self) -> bool:
        """Check if Add to Cart button exists."""
        return self.page.query_selector('#add-to-cart') is not None

    def has_variant_selector(self) -> bool:
        """Check if variant selector exists."""
        return self.page.query_selector('#variant-selector') is not None

    def get_variant_selector_mode(self) -> str:
        """Get variant selector mode ('attributes' or 'direct')."""
        el = self.page.query_selector('#variant-selector')
        return el.get_attribute('data-mode') if el else ''

    def get_variant_swatches(self) -> list:
        """Get all variant swatch elements."""
        return self.page.query_selector_all('.variant-swatch')

    def has_bundle_contents(self) -> bool:
        """Check if bundle contents section exists."""
        return self.page.query_selector('#bundle-contents') is not None

    def get_bundle_item_names(self) -> list:
        """Get bundle item names."""
        elements = self.page.query_selector_all('.bundle-item__name')
        return [el.text_content().strip() for el in elements]

    def get_bundle_item_quantities(self) -> list:
        """Get bundle item quantity strings."""
        elements = self.page.query_selector_all('.bundle-item__qty')
        return [el.text_content().strip() for el in elements]

    def has_digital_badge(self) -> bool:
        """Check if instant delivery badge exists."""
        return self.page.query_selector('.digital-badge--delivery') is not None

    def has_features_list(self) -> bool:
        """Check if features list exists."""
        return self.page.query_selector('.product-features__list') is not None

    def get_feature_items(self) -> list:
        """Get feature list items text."""
        elements = self.page.query_selector_all('.product-features__item')
        return [el.text_content().strip() for el in elements]

    def has_breadcrumb(self) -> bool:
        """Check if breadcrumb navigation exists."""
        return self.page.query_selector('.breadcrumb') is not None

    def get_layout_class(self) -> str:
        """Detect which product template layout is rendering."""
        for layout in ['classic', 'gallery-focus', 'full-width', 'digital']:
            if self.page.query_selector(f'.product-layout--{layout}'):
                return layout
        return 'unknown'

    def has_gallery_focus_sidebar(self) -> bool:
        """Check if gallery focus template sidebar exists."""
        return self.page.query_selector('.product-gallery-focus__sidebar') is not None

    def has_hero_section(self) -> bool:
        """Check if full-width hero section exists."""
        return self.page.query_selector('.product-hero') is not None

    def click_add_to_cart(self):
        """Click the Add to Cart button."""
        self.page.click('#add-to-cart')
        self.page.wait_for_timeout(500)

    def get_page_status_code(self) -> int:
        """Get the HTTP status code of the current page."""
        response = self.page.goto(self.page.url)
        return response.status if response else 0


@pytest.fixture
def product_page(authenticated_page, site_settings):
    """ProductPageHelper fixture with authenticated browser page."""
    return ProductPageHelper(authenticated_page)


@pytest.fixture
def product_page_anon(page, site_settings):
    """ProductPageHelper fixture with anonymous browser page."""
    return ProductPageHelper(page)


# ============================================================
# Admin Product Helper
# ============================================================

class AdminProductHelper:
    """Helper for creating and managing products in Django admin.

    The product admin uses a custom tabbed UI with tabs:
    Basic Info, Media, Pricing, Inventory, SEO, Advanced, Subscriptions, Custom Fields
    Plus conditional tabs: Variations, Bundle Items, Gift Card, Digital Assets,
    Licensing, Customization, Configuration, 3D Viewer
    """

    def __init__(self, page: Page):
        self.page = page
        self.base_url = page._live_server_url

    # --- Navigation ---

    def go_to_product_add(self):
        """Navigate to product add page."""
        self.page.goto(f'{self.base_url}/en/admin/catalog/product/add/')
        self.page.wait_for_load_state('networkidle')

    def go_to_product_list(self):
        """Navigate to product change list (custom card-based view)."""
        self.page.goto(f'{self.base_url}/en/admin/catalog/product/')
        self.page.wait_for_load_state('networkidle')

    def go_to_product_edit(self, product_id: int):
        """Navigate to product change form."""
        self.page.goto(f'{self.base_url}/en/admin/catalog/product/{product_id}/change/')
        self.page.wait_for_load_state('networkidle')

    def go_to_order_list(self):
        """Navigate to order change list."""
        self.page.goto(f'{self.base_url}/en/admin/orders/order/')
        self.page.wait_for_load_state('networkidle')

    def go_to_order_edit(self, order_id):
        """Navigate to order change form."""
        self.page.goto(f'{self.base_url}/en/admin/orders/order/{order_id}/change/')
        self.page.wait_for_load_state('networkidle')

    # --- Tab navigation ---

    def click_tab(self, tab_id: str):
        """Click a tab button by its ID (e.g. 'tab-pricing', 'tab-inventory')."""
        self.page.click(f'#{tab_id}')
        self.page.wait_for_timeout(300)

    # --- Form filling ---

    def fill_basic_info(self, name: str, sku: str, product_type: str = 'simple'):
        """Fill the Basic Information fieldset (on Basic Info tab)."""
        self.click_tab('tab-basic-info')
        self.page.fill('#id_name', name)
        self.page.wait_for_timeout(200)
        self.page.fill('#id_sku', sku)
        self.page.select_option('#id_product_type', product_type)
        # Wait for conditional tabs to show/hide based on product type
        self.page.wait_for_timeout(300)

    def fill_price(self, price: str):
        """Fill the price field (on Pricing tab)."""
        self.click_tab('tab-pricing')
        self.page.fill('#id_price_0', price)

    def set_status(self, status: str):
        """Set the product status (on Basic Info tab)."""
        self.page.select_option('#id_status', status)

    def set_category(self, category_id: int):
        """Set the category by selecting its ID (on Basic Info tab)."""
        self.page.select_option('#id_category', str(category_id))

    # --- Save actions ---

    def save_product(self):
        """Click the Save button and wait for page load."""
        self.page.click('button[name="_save"]')
        self.page.wait_for_load_state('networkidle')

    def save_and_continue(self):
        """Click Save and continue editing (JS-driven button)."""
        self.page.click('#save-continue-btn')
        self.page.wait_for_load_state('networkidle')

    # --- Page inspection ---

    def get_success_message(self) -> str:
        """Get the success message after save."""
        el = self.page.query_selector('.messagelist .success')
        return el.text_content().strip() if el else ''

    def has_fieldset(self, fieldset_id: str) -> bool:
        """Check if a fieldset exists on the page."""
        return self.page.query_selector(f'#{fieldset_id}') is not None

    def has_inline(self, inline_class: str) -> bool:
        """Check if an inline section exists."""
        return self.page.query_selector(f'.{inline_class}') is not None

    def is_tab_visible(self, tab_id: str) -> bool:
        """Check if a conditional tab is visible (not hidden)."""
        el = self.page.query_selector(f'#{tab_id}')
        if not el:
            return False
        classes = el.get_attribute('class') or ''
        return 'hidden' not in classes

    def get_product_id_from_url(self) -> str:
        """Extract product ID from the admin URL after save."""
        import re
        url = self.page.url
        match = re.search(r'/product/(\d+)/change/', url)
        return match.group(1) if match else ''


@pytest.fixture
def admin_product(admin_authenticated_page, site_settings):
    """AdminProductHelper fixture with authenticated admin browser page."""
    return AdminProductHelper(admin_authenticated_page)
