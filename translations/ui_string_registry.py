"""
Registry of all frontend UI strings that support merchant translation overrides.

Each key follows the pattern: section.string_identifier
Sections correspond to template groups for organization in the admin editor.

Values are wrapped in gettext_noop() so makemessages can extract them for .po files.
The actual translation happens at runtime via {% mtrans %} which calls gettext().

When adding new strings:
1. Add the entry here
2. Use {% mtrans 'String' %} in the template
3. Run manage.py sync_ui_string_registry to update existing override rows
"""

from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_noop

# Section definitions for admin UI grouping
UI_STRING_SECTIONS = {
    "common": _("Common"),
    "cart": _("Cart"),
    "mini_cart": _("Mini Cart"),
    "checkout": _("Checkout"),
    "product": _("Product Page"),
    "category": _("Category Page"),
    "home": _("Home Page"),
    "stock": _("Stock & Availability"),
    "account": _("Account"),
    "search": _("Search"),
    "blog": _("Blog"),
    "configurator_3d": _("3D Configurator"),
    "form_builder": _("Form Builder"),
    "loyalty": _("Loyalty Program"),
    "social_share": _("Social Share"),
    "widgets": _("Header & Footer Widgets"),
    "cookies": _("Cookie Consent"),
    "js": _("JavaScript Messages"),
    "contact": _("Contact Page"),
    "elements": _("Page Builder Elements"),
    "faq": _("FAQ Page"),
    "footer": _("Footer"),
    "header": _("Header"),
    "order": _("Order Confirmation"),
    "privacy": _("Privacy Policy Page"),
    "returns": _("Returns & Refunds Page"),
    "customizable_product": _("Product Customizer"),
    "booking": _("Booking"),
}


# The registry: key -> English source string
UI_STRING_REGISTRY = {
    # === Common ===
    "common.home": gettext_noop("Home"),
    "common.breadcrumb": gettext_noop("Breadcrumb"),
    "common.continue_shopping": gettext_noop("Continue Shopping"),
    "common.loading": gettext_noop("Loading..."),
    "common.cart": gettext_noop("Cart"),
    "common.or": gettext_noop("or"),
    "common.skip_to_main": gettext_noop("Skip to main content"),
    "common.sale": gettext_noop("Sale"),
    "common.default": gettext_noop("Default"),
    # === Cart ===
    "cart.shopping_cart": gettext_noop("Shopping Cart"),
    "cart.your_cart_is_empty": gettext_noop("Your cart is empty"),
    "cart.havent_added_items": gettext_noop(
        "Looks like you haven't added any items to your cart yet."
    ),
    "cart.loading_your_cart": gettext_noop("Loading your cart..."),
    "cart.order_summary": gettext_noop("Order Summary"),
    "cart.subtotal": gettext_noop("Subtotal"),
    "cart.discount": gettext_noop("Discount"),
    "cart.shipping": gettext_noop("Shipping"),
    "cart.calculated_at_checkout": gettext_noop("Calculated at checkout"),
    "cart.total": gettext_noop("Total"),
    "cart.voucher_code": gettext_noop("Voucher Code"),
    "cart.enter_code": gettext_noop("Enter code"),
    "cart.apply": gettext_noop("Apply"),
    "cart.proceed_to_checkout": gettext_noop("Proceed to Checkout"),
    # === Mini Cart ===
    "mini_cart.shopping_cart": gettext_noop("Shopping Cart"),
    "mini_cart.your_cart": gettext_noop("Your Cart"),
    "mini_cart.close_cart": gettext_noop("Close cart"),
    "mini_cart.your_cart_is_empty": gettext_noop("Your cart is empty"),
    "mini_cart.havent_added_anything": gettext_noop(
        "Looks like you haven't added anything to your cart yet."
    ),
    "mini_cart.start_shopping": gettext_noop("Start Shopping"),
    "mini_cart.subtotal": gettext_noop("Subtotal"),
    "mini_cart.shipping_taxes_note": gettext_noop("Shipping & taxes calculated at checkout"),
    "mini_cart.view_cart": gettext_noop("View Cart"),
    "mini_cart.checkout": gettext_noop("Checkout"),
    "mini_cart.no_payment_providers": gettext_noop("No payment providers configured."),
    "mini_cart.configure_payment": gettext_noop("Configure Payment Providers"),
    "mini_cart.trial_mode": gettext_noop("Payment processing disabled in trial mode."),
    "mini_cart.activate_license": gettext_noop("Activate License"),
    # === Checkout ===
    "checkout.checkout": gettext_noop("Checkout"),
    "checkout.contact": gettext_noop("Contact"),
    "checkout.email": gettext_noop("Email"),
    "checkout.email_placeholder": gettext_noop("your@email.com"),
    "checkout.continue_to_shipping": gettext_noop("Continue to Shipping"),
    "checkout.shipping_address": gettext_noop("Shipping Address"),
    "checkout.search_address": gettext_noop("Search Address"),
    "checkout.start_typing_address": gettext_noop("Start typing your address..."),
    "checkout.full_name": gettext_noop("Full Name"),
    "checkout.company": gettext_noop("Company"),
    "checkout.address_line_1": gettext_noop("Address Line 1"),
    "checkout.address_line_2": gettext_noop("Address Line 2"),
    "checkout.city": gettext_noop("City"),
    "checkout.state_province": gettext_noop("State / Province"),
    "checkout.postal_code": gettext_noop("Postal Code"),
    "checkout.country": gettext_noop("Country"),
    "checkout.phone": gettext_noop("Phone"),
    "checkout.use_different_address": gettext_noop("Use a different address"),
    "checkout.continue_to_shipping_method": gettext_noop("Continue to Shipping Method"),
    "checkout.shipping_method": gettext_noop("Shipping Method"),
    "checkout.loading_shipping_methods": gettext_noop("Loading shipping methods..."),
    "checkout.continue_to_payment": gettext_noop("Continue to Payment"),
    "checkout.payment": gettext_noop("Payment"),
    "checkout.loading_payment_methods": gettext_noop("Loading payment methods..."),
    "checkout.billing_same_as_shipping": gettext_noop("Billing address same as shipping"),
    "checkout.continue_to_review": gettext_noop("Continue to Review"),
    "checkout.review_place_order": gettext_noop("Review & Place Order"),
    "checkout.items": gettext_noop("Items"),
    "checkout.subtotal": gettext_noop("Subtotal"),
    "checkout.shipping": gettext_noop("Shipping"),
    "checkout.calculated_next": gettext_noop("Calculated next"),
    "checkout.discount": gettext_noop("Discount"),
    "checkout.tax": gettext_noop("Tax"),
    "checkout.total": gettext_noop("Total"),
    "checkout.place_order": gettext_noop("Place Order"),
    # === Checkout Return ===
    "checkout.processing_payment": gettext_noop("Processing Payment"),
    "checkout.processing_your_payment": gettext_noop("Processing your payment..."),
    "checkout.please_wait": gettext_noop(
        "Please wait while we confirm your payment. Do not close this page."
    ),
    "checkout.payment_confirmed": gettext_noop("Payment Confirmed!"),
    "checkout.redirecting_confirmation": gettext_noop(
        "Redirecting you to your order confirmation..."
    ),
    "checkout.payment_not_completed": gettext_noop("Payment Not Completed"),
    "checkout.payment_could_not_process": gettext_noop(
        "Your payment could not be processed. Please try again or choose a different payment method."
    ),
    "checkout.return_to_checkout": gettext_noop("Return to Checkout"),
    "checkout.still_processing": gettext_noop("Still Processing"),
    "checkout.still_processing_desc": gettext_noop(
        "Your payment is still being processed. You'll receive an email confirmation once it's complete."
    ),
    # === Product Page ===
    "product.add_to_cart": gettext_noop("Add to Cart"),
    "product.or_checkout_with": gettext_noop("or checkout with"),
    "product.sku": gettext_noop("SKU"),
    "product.category": gettext_noop("Category"),
    "product.description": gettext_noop("Description"),
    "product.specifications": gettext_noop("Specifications"),
    "product.reviews": gettext_noop("Reviews"),
    "product.key_features": gettext_noop("Key Features"),
    "product.free_shipping": gettext_noop("Free Shipping"),
    "product.day_returns": gettext_noop("30-Day Returns"),
    "product.secure_payment": gettext_noop("Secure Payment"),
    "product.you_may_also_like": gettext_noop("You May Also Like"),
    "product.verified_purchase": gettext_noop("Verified Purchase"),
    "product.found_this_helpful": gettext_noop("found this helpful"),
    "product.no_reviews_yet": gettext_noop("No reviews yet. Be the first to review this product!"),
    "product.decrease_quantity": gettext_noop("Decrease quantity"),
    "product.increase_quantity": gettext_noop("Increase quantity"),
    "product.quantity": gettext_noop("Quantity"),
    "product.no_attributes_available": gettext_noop("No attributes available for this product."),
    # === Category Page ===
    "category.product_categories": gettext_noop("Product Categories"),
    "category.browse_collection": gettext_noop("Browse our collection of products"),
    "category.categories": gettext_noop("Categories"),
    "category.subcategories": gettext_noop("Subcategories"),
    "category.products": gettext_noop("Products"),
    "category.items": gettext_noop("items"),
    "category.no_categories": gettext_noop("No categories available yet."),
    "category.no_products": gettext_noop("No products in this category yet."),
    "category.cant_find": gettext_noop("Can't Find What You're Looking For?"),
    "category.use_search": gettext_noop(
        "Use our search feature to find exactly what you need, or contact our support team for personalized assistance."
    ),
    "category.search_products": gettext_noop("Search Products"),
    "category.contact_support": gettext_noop("Contact Support"),
    # List template
    "category.view_product": gettext_noop("View Product"),
    # Carousel template
    "category.previous": gettext_noop("Previous"),
    "category.next": gettext_noop("Next"),
    # Featured template
    "category.featured": gettext_noop("Featured"),
    "category.quick_view": gettext_noop("Quick View"),
    "category.more_products": gettext_noop("More Products"),
    # Accordion template
    "category.explore_categories": gettext_noop("Explore Categories"),
    "category.click_to_expand": gettext_noop("Click to expand"),
    # Sort & pagination
    "category.sort_by": gettext_noop("Sort by"),
    "category.sort_newest": gettext_noop("Newest"),
    "category.sort_price_low": gettext_noop("Price: Low to High"),
    "category.sort_price_high": gettext_noop("Price: High to Low"),
    "category.sort_name_az": gettext_noop("Name: A to Z"),
    "category.sort_name_za": gettext_noop("Name: Z to A"),
    "category.sort_popular": gettext_noop("Most Popular"),
    "category.load_more": gettext_noop("Load More"),
    "category.showing_of": gettext_noop("Showing {count} of {total}"),
    "category.page": gettext_noop("Page"),
    # === Home Page ===
    "home.welcome": gettext_noop("Welcome to Our Shop"),
    "home.discover": gettext_noop(
        "Discover amazing products at great prices. Free shipping on orders over $50."
    ),
    "home.shop_now": gettext_noop("Shop Now"),
    "home.why_choose_us": gettext_noop("Why Choose Us?"),
    "home.experience": gettext_noop(
        "Experience the future of online shopping with our cutting-edge platform."
    ),
    "home.lightning_fast": gettext_noop("Lightning Fast"),
    "home.lightning_fast_desc": gettext_noop("Blazing fast load times for seamless browsing."),
    "home.mobile_first": gettext_noop("Mobile First"),
    "home.mobile_first_desc": gettext_noop("Optimized for all devices and screen sizes."),
    "home.secure": gettext_noop("Secure"),
    "home.secure_desc": gettext_noop("Industry-leading security for your transactions."),
    "home.shop_by_category": gettext_noop("Shop by Category"),
    "home.browse_by_category": gettext_noop("Browse our collection by category"),
    "home.featured_products": gettext_noop("Featured Products"),
    "home.check_out_popular": gettext_noop("Check out our most popular items"),
    "home.no_products_yet": gettext_noop("No products available yet. Check back soon!"),
    "home.ready_to_start": gettext_noop("Ready to Start Shopping?"),
    "home.join_customers": gettext_noop(
        "Join thousands of satisfied customers who love our products."
    ),
    "home.browse_catalog": gettext_noop("Browse Catalog"),
    # === Stock & Availability ===
    "stock.in_stock": gettext_noop("In Stock"),
    "stock.low_stock": gettext_noop("Low Stock"),
    "stock.out_of_stock": gettext_noop("Out of Stock"),
    "stock.check_availability": gettext_noop("Check Availability"),
    "stock.checking_availability": gettext_noop("Checking availability..."),
    "stock.get_notified_back_in_stock": gettext_noop(
        "Get notified when this item is back in stock"
    ),
    "stock.enter_your_email": gettext_noop("Enter your email"),
    "stock.notify_me": gettext_noop("Notify Me"),
    "stock.notify_email_disclaimer": gettext_noop(
        "We'll send you a one-time email when this product is available."
    ),
    "stock.notify_success": gettext_noop("You're on the list! We'll email you when it's back."),
    # === Account ===
    "account.my_account": gettext_noop("My Account"),
    "account.sign_in": gettext_noop("Sign In"),
    "account.sign_out": gettext_noop("Sign Out"),
    "account.register": gettext_noop("Register"),
    "account.orders": gettext_noop("Orders"),
    "account.wishlist": gettext_noop("Wishlist"),
    "account.addresses": gettext_noop("Addresses"),
    # === Account - Messages ===
    "account.my_messages": gettext_noop("My Messages"),
    "account.new_message": gettext_noop("New Message"),
    "account.send_message": gettext_noop("Send a Message"),
    "account.send_follow_up": gettext_noop("Send a Follow-up"),
    "account.send_message_btn": gettext_noop("Send Message"),
    "account.send_follow_up_btn": gettext_noop("Send Follow-up"),
    "account.your_support_conversations": gettext_noop("Your support conversations and inquiries"),
    "account.send_us_a_message": gettext_noop("Send us a message and we'll get back to you"),
    "account.view_support_conversations": gettext_noop(
        "View support conversations and send messages"
    ),
    "account.no_messages_yet": gettext_noop("You have not sent any messages yet."),
    "account.reply_received": gettext_noop("Reply received"),
    "account.back_to_messages": gettext_noop("Back to Messages"),
    "account.message_details": gettext_noop("Message Details"),
    "account.related_order": gettext_noop("Related Order"),
    "account.submitting_as": gettext_noop("Submitting as"),
    "account.your_message": gettext_noop("Your Message"),
    "account.your_follow_up": gettext_noop("Your follow-up message"),
    "account.support_team": gettext_noop("Support Team"),
    "account.you": gettext_noop("You"),
    "account.please_correct_errors": gettext_noop("Please correct the errors below."),
    # === Search ===
    "search.search": gettext_noop("Search"),
    "search.search_products": gettext_noop("Search products..."),
    "search.no_results": gettext_noop("No results found"),
    "search.did_you_mean": gettext_noop("Did you mean:"),
    "search.also_searching_for": gettext_noop("Also searching for:"),
    "search.type": gettext_noop("Type"),
    "search.all": gettext_noop("All"),
    "search.products": gettext_noop("Products"),
    "search.categories": gettext_noop("Categories"),
    "search.brands": gettext_noop("Brands"),
    "search.blog_posts": gettext_noop("Blog Posts"),
    "search.price_range": gettext_noop("Price Range"),
    "search.min": gettext_noop("Min"),
    "search.max": gettext_noop("Max"),
    "search.availability": gettext_noop("Availability"),
    "search.in_stock_only": gettext_noop("In Stock Only"),
    "search.sort_by": gettext_noop("Sort By"),
    "search.relevance": gettext_noop("Relevance"),
    "search.price_low_to_high": gettext_noop("Price: Low to High"),
    "search.price_high_to_low": gettext_noop("Price: High to Low"),
    "search.newest_first": gettext_noop("Newest First"),
    "search.apply_filters": gettext_noop("Apply Filters"),
    "search.clear_filters": gettext_noop("Clear Filters"),
    "search.product": gettext_noop("Product"),
    "search.category": gettext_noop("Category"),
    "search.brand": gettext_noop("Brand"),
    "search.blog": gettext_noop("Blog"),
    "search.content_available_in_language": gettext_noop("Content available in your language"),
    "search.translated": gettext_noop("Translated"),
    "search.in_stock": gettext_noop("In Stock"),
    "search.out_of_stock": gettext_noop("Out of Stock"),
    "search.start_searching": gettext_noop("Start searching"),
    "search.enter_search_term": gettext_noop(
        "Enter a search term to find products, categories, and more."
    ),
    "search.browse_categories": gettext_noop("Browse Categories"),
    "search.previous": gettext_noop("Previous"),
    "search.next": gettext_noop("Next"),
    # === Blog ===
    "blog.blog": gettext_noop("Blog"),
    "blog.search": gettext_noop("Search"),
    "blog.search_posts": gettext_noop("Search posts..."),
    "blog.categories": gettext_noop("Categories"),
    "blog.tags": gettext_noop("Tags"),
    "blog.subscribe": gettext_noop("Subscribe"),
    "blog.your_email_address": gettext_noop("Your email address"),
    "blog.rss_feed": gettext_noop("RSS Feed"),
    "blog.search_results": gettext_noop("Search results"),
    "blog.latest_articles_and_news": gettext_noop("Latest articles and news"),
    "blog.featured": gettext_noop("Featured"),
    "blog.min_read": gettext_noop("min read"),
    "blog.remove_filter": gettext_noop("Remove filter"),
    "blog.clear_search": gettext_noop("Clear search"),
    "blog.read_more": gettext_noop("Read more"),
    "blog.no_posts_matching_search": gettext_noop("No posts found matching your search."),
    "blog.no_posts_yet": gettext_noop("No posts published yet. Check back soon!"),
    "blog.blog_pagination": gettext_noop("Blog pagination"),
    "blog.previous_page": gettext_noop("Previous page"),
    "blog.next_page": gettext_noop("Next page"),
    "blog.views": gettext_noop("views"),
    "blog.share_this_article": gettext_noop("Share this article"),
    "blog.related_articles": gettext_noop("Related Articles"),
    "blog.enjoyed_this_article": gettext_noop("Enjoyed this article?"),
    "blog.subscribe_notification": gettext_noop(
        "Subscribe to get notified when we publish new content."
    ),
    "blog.no_posts_in_category": gettext_noop("No posts in this category yet."),
    "blog.no_posts_with_tag": gettext_noop("No posts with this tag yet."),
    "blog.subscription_preferences": gettext_noop("Subscription Preferences"),
    "blog.preferences": gettext_noop("Preferences"),
    "blog.notification_frequency": gettext_noop("Notification Frequency"),
    "blog.immediately": gettext_noop("Immediately"),
    "blog.get_notified_every_post": gettext_noop("Get notified for every new post"),
    "blog.weekly_digest": gettext_noop("Weekly Digest"),
    "blog.weekly_summary": gettext_noop("A summary of new posts each week"),
    "blog.monthly_digest": gettext_noop("Monthly Digest"),
    "blog.monthly_roundup": gettext_noop("A monthly roundup of posts"),
    "blog.select_categories_interest": gettext_noop(
        "Select categories you're interested in. Leave all unchecked to receive posts from all categories."
    ),
    "blog.save_preferences": gettext_noop("Save Preferences"),
    "blog.unsubscribe_from_all": gettext_noop("Unsubscribe from all notifications"),
    "blog.subscription_verified": gettext_noop("Subscription Verified"),
    "blog.youre_subscribed": gettext_noop("You're subscribed!"),
    "blog.manage_preferences": gettext_noop("Manage Preferences"),
    "blog.back_to_blog": gettext_noop("Back to Blog"),
    "blog.unsubscribe": gettext_noop("Unsubscribe"),
    "blog.unsubscribe_question": gettext_noop("Unsubscribe?"),
    "blog.reason_optional": gettext_noop("Reason (optional):"),
    "blog.tell_us_why_leaving": gettext_noop("Tell us why you are leaving..."),
    "blog.yes_unsubscribe": gettext_noop("Yes, Unsubscribe"),
    "blog.no_keep_subscribed": gettext_noop("No, keep me subscribed"),
    "blog.unsubscribed": gettext_noop("Unsubscribed"),
    "blog.youve_been_unsubscribed": gettext_noop("You've been unsubscribed"),
    "blog.preferences_updated": gettext_noop("Preferences Updated"),
    "blog.preferences_saved": gettext_noop(
        "Your subscription preferences have been saved successfully."
    ),
    # === 3D Configurator ===
    "configurator_3d.start_with_preset": gettext_noop("Start with a preset"),
    "configurator_3d.choose_starting_config": gettext_noop(
        "Choose a starting configuration or build from scratch."
    ),
    "configurator_3d.build_from_scratch": gettext_noop("Build from scratch"),
    "configurator_3d.loading_3d_model": gettext_noop("Loading 3D model..."),
    "configurator_3d.drag_to_rotate": gettext_noop("Drag to rotate, pinch to zoom"),
    "configurator_3d.view_in_ar": gettext_noop("View in AR"),
    "configurator_3d.back": gettext_noop("Back"),
    "configurator_3d.next": gettext_noop("Next"),
    "configurator_3d.your_configuration": gettext_noop("Your Configuration"),
    "configurator_3d.configuration_options": gettext_noop("Configuration options"),
    "configurator_3d.drag_to_resize": gettext_noop("Drag to resize"),
    # === Form Builder ===
    "form_builder.preview_mode": gettext_noop("Preview Mode"),
    "form_builder.preview_info": gettext_noop(
        "Test your form's functionality here. Visual styling options are available when adding this form to a page using the Page Builder."
    ),
    "form_builder.select_an_option": gettext_noop("Select an option"),
    "form_builder.drag_and_drop": gettext_noop("Drag and drop files here or"),
    "form_builder.browse": gettext_noop("browse"),
    "form_builder.allowed": gettext_noop("Allowed:"),
    "form_builder.max_size": gettext_noop("Max size:"),
    "form_builder.max_files": gettext_noop("Max files:"),
    "form_builder.search_products": gettext_noop("Search products..."),
    "form_builder.loading": gettext_noop("Loading..."),
    "form_builder.no_products_found": gettext_noop("No products found"),
    "form_builder.detractors": gettext_noop("Detractors"),
    "form_builder.passives": gettext_noop("Passives"),
    "form_builder.promoters": gettext_noop("Promoters"),
    "form_builder.strongly_disagree": gettext_noop("Strongly Disagree"),
    "form_builder.disagree": gettext_noop("Disagree"),
    "form_builder.neutral": gettext_noop("Neutral"),
    "form_builder.agree": gettext_noop("Agree"),
    "form_builder.strongly_agree": gettext_noop("Strongly Agree"),
    "form_builder.never": gettext_noop("Never"),
    "form_builder.rarely": gettext_noop("Rarely"),
    "form_builder.sometimes": gettext_noop("Sometimes"),
    "form_builder.often": gettext_noop("Often"),
    "form_builder.always": gettext_noop("Always"),
    "form_builder.very_dissatisfied": gettext_noop("Very Dissatisfied"),
    "form_builder.dissatisfied": gettext_noop("Dissatisfied"),
    "form_builder.satisfied": gettext_noop("Satisfied"),
    "form_builder.very_satisfied": gettext_noop("Very Satisfied"),
    # === JavaScript Messages ===
    "js.failed_to_load_checkout": gettext_noop("Failed to load checkout. Please try again."),
    "js.please_enter_valid_email": gettext_noop("Please enter a valid email address."),
    "js.field_required": gettext_noop("This field is required."),
    "js.failed_to_save_address": gettext_noop("Failed to save address. Please try again."),
    "js.failed_to_set_shipping_address": gettext_noop("Failed to set shipping address."),
    "js.please_select_shipping_method": gettext_noop("Please select a shipping method."),
    "js.failed_to_set_shipping_method": gettext_noop("Failed to set shipping method."),
    "js.failed_to_save_shipping_method": gettext_noop(
        "Failed to save shipping method. Please try again."
    ),
    "js.no_shipping_methods": gettext_noop("No shipping methods available for this address."),
    "js.failed_to_load_shipping": gettext_noop("Failed to load shipping methods."),
    "js.please_select_payment_method": gettext_noop("Please select a payment method."),
    "js.failed_to_set_payment_method": gettext_noop("Failed to set payment method."),
    "js.failed_to_save_payment_method": gettext_noop(
        "Failed to save payment method. Please try again."
    ),
    "js.no_payment_methods": gettext_noop("No payment methods available."),
    "js.failed_to_load_payment": gettext_noop("Failed to load payment methods."),
    "js.payment_form_unavailable": gettext_noop("Unable to load payment form"),
    "js.payment_form_error_message": gettext_noop(
        "We could not connect to the payment service. This may be a temporary issue. Please try again or choose a different payment method."
    ),
    "js.payment_form_try_again": gettext_noop("Try Again"),
    "js.payment_form_choose_different": gettext_noop(
        "Or go back to select a different payment method"
    ),
    "js.loading_shipping_methods": gettext_noop("Loading shipping methods..."),
    "js.loading_payment_methods": gettext_noop("Loading payment methods..."),
    "js.free": gettext_noop("Free"),
    "js.use_saved_address": gettext_noop("Use saved address"),
    "js.use_different_address": gettext_noop("Use a different address"),
    "js.product_added": gettext_noop("Product added to cart!"),
    "js.error_adding": gettext_noop("Error adding to cart"),
    "js.adding": gettext_noop("Adding..."),
    "js.added": gettext_noop("Added!"),
    "js.error": gettext_noop("Error"),
    "js.invalid_voucher": gettext_noop("Invalid voucher code"),
    "js.failed_apply_voucher": gettext_noop("Failed to apply voucher. Please try again."),
    "js.qty_prefix": gettext_noop("Qty:"),
    # Search autocomplete
    "js.search_did_you_mean": gettext_noop("Did you mean:"),
    "js.search_products": gettext_noop("Products"),
    "js.search_categories": gettext_noop("Categories"),
    "js.search_brands": gettext_noop("Brands"),
    "js.search_blog": gettext_noop("Blog"),
    "js.search_view_all_results": gettext_noop("View all {count} results"),
    "js.search_in_stock": gettext_noop("In Stock"),
    "js.search_out_of_stock": gettext_noop("Out of Stock"),
    "js.search_products_count": gettext_noop("{count} products"),
    # === Loyalty ===
    # Dashboard
    "loyalty.loyalty_dashboard": gettext_noop("Loyalty Dashboard"),
    "loyalty.your_loyalty_points": gettext_noop("Your Loyalty Points"),
    "loyalty.points_available": gettext_noop("Points Available"),
    "loyalty.points_pending": gettext_noop("points pending"),
    "loyalty.earned": gettext_noop("Earned"),
    "loyalty.redeemed": gettext_noop("Redeemed"),
    "loyalty.badges": gettext_noop("Badges"),
    "loyalty.browse_rewards": gettext_noop("Browse Rewards"),
    "loyalty.redeem_your_points": gettext_noop("Redeem your points for exclusive rewards"),
    "loyalty.transaction_history": gettext_noop("Transaction History"),
    "loyalty.view_your_points_activity": gettext_noop("View your points activity"),
    "loyalty.tier_benefits": gettext_noop("Tier Benefits"),
    "loyalty.unlock_exclusive_perks": gettext_noop("Unlock exclusive perks"),
    "loyalty.featured_rewards": gettext_noop("Featured Rewards"),
    "loyalty.view_all": gettext_noop("View All"),
    "loyalty.points": gettext_noop("points"),
    "loyalty.redeem": gettext_noop("Redeem"),
    "loyalty.need": gettext_noop("Need"),
    "loyalty.more_points": gettext_noop("more points"),
    "loyalty.recent_activity": gettext_noop("Recent Activity"),
    "loyalty.pending_redemptions": gettext_noop("Pending Redemptions"),
    "loyalty.view_details": gettext_noop("View Details"),
    "loyalty.recent_badges": gettext_noop("Recent Badges"),
    "loyalty.start_your_journey": gettext_noop("Start Your Journey!"),
    "loyalty.start_earning_message": gettext_noop(
        "Make purchases, engage with us, and start earning points today."
    ),
    # Rewards Catalog
    "loyalty.rewards_catalog": gettext_noop("Rewards Catalog"),
    "loyalty.your_balance": gettext_noop("Your Balance"),
    "loyalty.reward_type": gettext_noop("Reward Type"),
    "loyalty.sort_by": gettext_noop("Sort By"),
    "loyalty.points_low_to_high": gettext_noop("Points (Low to High)"),
    "loyalty.featured_first": gettext_noop("Featured First"),
    "loyalty.name_a_to_z": gettext_noop("Name (A-Z)"),
    "loyalty.apply_filters": gettext_noop("Apply Filters"),
    "loyalty.clear": gettext_noop("Clear"),
    "loyalty.featured": gettext_noop("FEATURED"),
    "loyalty.unavailable": gettext_noop("Unavailable"),
    "loyalty.previous": gettext_noop("Previous"),
    "loyalty.page": gettext_noop("Page"),
    "loyalty.of": gettext_noop("of"),
    "loyalty.next": gettext_noop("Next"),
    "loyalty.no_rewards_available": gettext_noop("No Rewards Available"),
    "loyalty.check_back_soon": gettext_noop(
        "Check back soon for new rewards to redeem with your points!"
    ),
    "loyalty.back_to_dashboard": gettext_noop("Back to Dashboard"),
    # Transaction History
    "loyalty.view_all_points_activity": gettext_noop("View all your points activity"),
    "loyalty.transaction_type": gettext_noop("Transaction Type"),
    "loyalty.filter": gettext_noop("Filter"),
    "loyalty.clear_filter": gettext_noop("Clear Filter"),
    "loyalty.date": gettext_noop("Date"),
    "loyalty.type": gettext_noop("Type"),
    "loyalty.description": gettext_noop("Description"),
    "loyalty.points_column": gettext_noop("Points"),
    "loyalty.balance_after": gettext_noop("Balance After"),
    "loyalty.no_transactions_yet": gettext_noop("No Transactions Yet"),
    "loyalty.no_transactions_message": gettext_noop(
        "Your transaction history will appear here once you start earning and redeeming points."
    ),
    # Tier Info
    "loyalty.tier_information": gettext_noop("Tier Information"),
    "loyalty.loyalty_tiers": gettext_noop("Loyalty Tiers"),
    "loyalty.unlock_benefits_message": gettext_noop(
        "Unlock exclusive benefits as you earn more points"
    ),
    "loyalty.your_current_tier": gettext_noop("Your Current Tier"),
    "loyalty.current": gettext_noop("Current"),
    "loyalty.achieved": gettext_noop("Achieved"),
    "loyalty.progress": gettext_noop("Progress"),
    "loyalty.benefits": gettext_noop("Benefits"),
    "loyalty.points_multiplier": gettext_noop("Points Multiplier"),
    # Redeem Reward
    "loyalty.redeem_reward": gettext_noop("Redeem Reward"),
    "loyalty.rewards": gettext_noop("Rewards"),
    "loyalty.points_cost": gettext_noop("Points Cost"),
    "loyalty.remaining": gettext_noop("Remaining"),
    "loyalty.required_tier": gettext_noop("Required Tier"),
    "loyalty.your_available_points": gettext_noop("Your Available Points"),
    "loyalty.after_redemption": gettext_noop("After Redemption"),
    "loyalty.enough_points_message": gettext_noop("You have enough points to redeem this reward!"),
    "loyalty.terms_and_conditions": gettext_noop("Terms and Conditions"),
    "loyalty.back_to_rewards": gettext_noop("Back to Rewards"),
    "loyalty.confirm_redemption": gettext_noop("Confirm Redemption"),
    "loyalty.are_you_sure_redeem": gettext_noop("Are you sure you want to redeem this reward?"),
    "loyalty.cannot_redeem": gettext_noop("Cannot Redeem"),
    # Redemption Detail
    "loyalty.redemption_details": gettext_noop("Redemption Details"),
    "loyalty.redemption_successful": gettext_noop("Redemption Successful!"),
    "loyalty.reward_processed_message": gettext_noop(
        "Your reward has been processed. Details below."
    ),
    "loyalty.redemption_code": gettext_noop("Redemption Code"),
    "loyalty.points_spent": gettext_noop("Points Spent"),
    "loyalty.status": gettext_noop("Status"),
    "loyalty.redeemed_on": gettext_noop("Redeemed On"),
    "loyalty.your_voucher_code": gettext_noop("Your Voucher Code"),
    "loyalty.use_voucher_message": gettext_noop("Use this code at checkout to claim your reward."),
    "loyalty.expires_on": gettext_noop("Expires On"),
    "loyalty.at": gettext_noop("at"),
    "loyalty.redemption_timeline": gettext_noop("Redemption Timeline"),
    "loyalty.redemption_created": gettext_noop("Redemption Created"),
    "loyalty.confirmed": gettext_noop("Confirmed"),
    "loyalty.fulfilled": gettext_noop("Fulfilled"),
    "loyalty.cancelled": gettext_noop("Cancelled"),
    # Badges (new page)
    "loyalty.my_badges": gettext_noop("My Badges"),
    "loyalty.your_achievements": gettext_noop("Your achievements and milestones"),
    "loyalty.earned_badges": gettext_noop("Earned Badges"),
    "loyalty.available_badges": gettext_noop("Available Badges"),
    "loyalty.earned_on": gettext_noop("Earned on"),
    "loyalty.no_badges_yet": gettext_noop("No Badges Yet"),
    "loyalty.no_badges_message": gettext_noop(
        "Complete activities to earn badges and bonus points!"
    ),
    "loyalty.points_reward": gettext_noop("points reward"),
    "loyalty.track_achievements": gettext_noop("Track your achievements and unlock new badges"),
    "loyalty.badges_earned": gettext_noop("Badges Earned"),
    "loyalty.available_to_earn": gettext_noop("Available to Earn"),
    "loyalty.no_badges_earned_yet": gettext_noop("No badges earned yet"),
    "loyalty.keep_shopping_message": gettext_noop(
        "Keep shopping and engaging to earn your first badge!"
    ),
    "loyalty.not_yet_earned": gettext_noop("Not yet earned"),
    # Expiration Warning
    "loyalty.points_expiring_soon": gettext_noop("Points Expiring Soon"),
    "loyalty.points_expiring_message": gettext_noop("points expiring within 30 days"),
    "loyalty.redeem_now": gettext_noop("Redeem Now"),
    # === Social Share ===
    "social_share.share": gettext_noop("Share"),
    "social_share.share_on_facebook": gettext_noop("Share on Facebook"),
    "social_share.share_on_twitter": gettext_noop("Share on Twitter"),
    "social_share.share_on_linkedin": gettext_noop("Share on LinkedIn"),
    "social_share.share_on_pinterest": gettext_noop("Share on Pinterest"),
    "social_share.share_on_whatsapp": gettext_noop("Share on WhatsApp"),
    "social_share.share_on_telegram": gettext_noop("Share on Telegram"),
    "social_share.share_via_email": gettext_noop("Share via Email"),
    # === Header & Footer Widgets ===
    # Search widget
    "widgets.search_category": gettext_noop("Search category"),
    "widgets.all_categories": gettext_noop("All Categories"),
    "widgets.voice_search": gettext_noop("Voice search"),
    "widgets.submit_search": gettext_noop("Submit search"),
    "widgets.clear_search": gettext_noop("Clear search"),
    "widgets.close_search": gettext_noop("Close search"),
    "widgets.recent_searches": gettext_noop("Recent Searches"),
    "widgets.searching": gettext_noop("Searching..."),
    # Account widget
    "widgets.account_menu": gettext_noop("Account menu"),
    "widgets.account_options": gettext_noop("Account options"),
    "widgets.create_account": gettext_noop("Create Account"),
    # Cart widget
    "widgets.view_cart": gettext_noop("View cart"),
    "widgets.open_cart": gettext_noop("Open cart"),
    # Currency widget
    "widgets.select_currency": gettext_noop("Select Currency"),
    # Loyalty widgets
    "widgets.view_loyalty_dashboard": gettext_noop("View loyalty dashboard"),
    "widgets.points": gettext_noop("Points"),
    "widgets.view_tier_information": gettext_noop("View tier information"),
    "widgets.max_tier": gettext_noop("Max Tier"),
    # Newsletter widget
    "widgets.subscribe_agreement": gettext_noop("By subscribing, you agree to our"),
    "widgets.privacy_policy": gettext_noop("Privacy Policy"),
    # Menu widget
    "widgets.toggle_menu": gettext_noop("Toggle menu"),
    # === Cookie Consent ===
    "cookies.cookie_consent": gettext_noop("Cookie consent"),
    "cookies.we_use_cookies": gettext_noop("We use cookies"),
    "cookies.default_description": gettext_noop(
        "We use cookies to improve your experience, analyse site traffic and personalise content."
    ),
    "cookies.cookie_policy": gettext_noop("Cookie Policy"),
    "cookies.accept_all": gettext_noop("Accept All"),
    "cookies.reject_all": gettext_noop("Reject All"),
    "cookies.manage_preferences": gettext_noop("Manage Preferences"),
    "cookies.save_preferences": gettext_noop("Save Preferences"),
    "cookies.cookie_preferences": gettext_noop("Cookie Preferences"),
    "cookies.close": gettext_noop("Close"),
    "cookies.necessary": gettext_noop("Necessary"),
    "cookies.always_on": gettext_noop("Always On"),
    "cookies.necessary_desc": gettext_noop(
        "Required for the site to function correctly. Cannot be disabled."
    ),
    "cookies.analytics": gettext_noop("Analytics"),
    "cookies.analytics_desc": gettext_noop(
        "Help us understand how visitors use our site to improve the experience."
    ),
    "cookies.marketing": gettext_noop("Marketing"),
    "cookies.marketing_desc": gettext_noop(
        "Used to show you relevant advertisements on other websites."
    ),
    "cookies.functional": gettext_noop("Functional"),
    "cookies.functional_desc": gettext_noop(
        "Enable enhanced features like live chat and saved preferences."
    ),
    # === Account (additional) ===
    "account.cancel": gettext_noop("Cancel"),
    "account.message": gettext_noop("Message"),
    "account.message_type": gettext_noop("Message Type"),
    "account.order": gettext_noop("Order"),
    "account.replied": gettext_noop("Replied"),
    "account.subject": gettext_noop("Subject"),
    "account.submitted": gettext_noop("Submitted"),
    "account.optional": gettext_noop("optional"),
    # === Cart (additional) ===
    # === Category (additional) ===
    "category.all_products": gettext_noop("All Products"),
    "category.load_more_products": gettext_noop("Load More Products"),
    "category.no_products_available_yet": gettext_noop("No products available yet."),
    "category.page_navigation": gettext_noop("Page navigation"),
    "category.use_our_search_feature_or_contact_our_customer_ser": gettext_noop(
        "Use our search feature or contact our customer service team for personalized assistance."
    ),
    "category.product": gettext_noop("product"),
    # === Checkout (additional) ===
    "checkout.all_prices_are_charged_in": gettext_noop("All prices are charged in"),
    "checkout.change": gettext_noop("Change"),
    "checkout.checkout_progress": gettext_noop("Checkout progress"),
    "checkout.complete_payment": gettext_noop("Complete Payment"),
    "checkout.contact_information": gettext_noop("Contact Information"),
    "checkout.continue_to_delivery": gettext_noop("Continue to Delivery"),
    "checkout.delivery": gettext_noop("Delivery"),
    "checkout.express_checkout": gettext_noop("Express Checkout"),
    "checkout.loading_saved_address": gettext_noop("Loading saved address..."),
    "checkout.order_total": gettext_noop("Order Total"),
    "checkout.password": gettext_noop("Password"),
    "checkout.return_to_cart": gettext_noop("Return to Cart"),
    "checkout.review": gettext_noop("Review"),
    "checkout.review_complete_payment": gettext_noop("Review & Complete Payment"),
    "checkout.show_order_summary": gettext_noop("Show order summary"),
    "checkout.use_this_address": gettext_noop("Use this address"),
    "checkout.use_this_method": gettext_noop("Use this method"),
    "checkout.you_ll_be_able_to_create_an_account_after_placing": gettext_noop(
        "You'll be able to create an account after placing your order"
    ),
    "checkout.or_continue_below": gettext_noop("or continue below"),
    # === Contact Page ===
    "contact.address": gettext_noop("Address"),
    "contact.business_hours": gettext_noop("Business Hours"),
    "contact.feedback": gettext_noop("Feedback"),
    "contact.follow_us": gettext_noop("Follow Us"),
    "contact.get_in_touch": gettext_noop("Get in Touch"),
    "contact.monday_friday_9am_6pm": gettext_noop("Monday - Friday: 9AM - 6PM"),
    "contact.order_inquiry": gettext_noop("Order Inquiry"),
    "contact.order_number": gettext_noop("Order Number"),
    "contact.other": gettext_noop("Other"),
    "contact.product_question": gettext_noop("Product Question"),
    "contact.returns_refunds": gettext_noop("Returns & Refunds"),
    "contact.returns_policy": gettext_noop("Returns Policy"),
    "contact.saturday_10am_4pm": gettext_noop("Saturday: 10AM - 4PM"),
    "contact.select_a_topic": gettext_noop("Select a topic"),
    "contact.send_us_a_message": gettext_noop("Send us a Message"),
    "contact.track_order": gettext_noop("Track Order"),
    "contact.we_d_love_to_hear_from_you_get_in_touch_with_our_t": gettext_noop(
        "We'd love to hear from you. Get in touch with our team."
    ),
    "contact.your_name": gettext_noop("Your Name"),
    # === Page Builder Elements ===
    "elements.add_faq_items_to_display": gettext_noop("Add FAQ items to display"),
    "elements.add_a_video_url_to_display": gettext_noop("Add a video URL to display"),
    "elements.add_frames_to_create_your_image_accordion": gettext_noop(
        "Add frames to create your image accordion"
    ),
    "elements.add_images_to_create_your_gallery": gettext_noop("Add images to create your gallery"),
    "elements.add_products_to_display_in_the_carousel": gettext_noop(
        "Add products to display in the carousel"
    ),
    "elements.add_testimonials_to_showcase_customer_feedback": gettext_noop(
        "Add testimonials to showcase customer feedback"
    ),
    "elements.add_trust_badges_to_display": gettext_noop("Add trust badges to display"),
    "elements.after": gettext_noop("After"),
    "elements.button_click": gettext_noop("Button Click"),
    "elements.button_text": gettext_noop("Button Text"),
    "elements.click_to_add_an_image": gettext_noop("Click to add an image"),
    "elements.click_to_add_text_content": gettext_noop("Click to add text content..."),
    "elements.close_modal": gettext_noop("Close modal"),
    "elements.code_copied_to_clipboard": gettext_noop("Code copied to clipboard!"),
    "elements.configure_the_data_source_or_select_products_manua": gettext_noop(
        "Configure the data source or select products manually."
    ),
    "elements.contact_us": gettext_noop("Contact Us"),
    "elements.copy_code": gettext_noop("Copy code"),
    "elements.custom_amount": gettext_noop("Custom Amount"),
    "elements.days": gettext_noop("Days"),
    "elements.drop_elements_here": gettext_noop("Drop elements here"),
    "elements.drop_elements_here_to_build_your_modal_content": gettext_noop(
        "Drop elements here to build your modal content"
    ),
    "elements.email_address": gettext_noop("Email Address"),
    "elements.ends_in": gettext_noop("Ends in:"),
    "elements.enter_city_postal_code_or_address": gettext_noop(
        "Enter city, postal code, or address"
    ),
    "elements.enter_your_email_address": gettext_noop("Enter your email address"),
    "elements.enter_your_first_name": gettext_noop("Enter your first name"),
    "elements.enter_your_last_name": gettext_noop("Enter your last name"),
    "elements.enter_your_phone_number": gettext_noop("Enter your phone number"),
    "elements.error_loading_store_locations": gettext_noop("Error loading store locations"),
    "elements.exit_intent": gettext_noop("Exit Intent"),
    "elements.expires": gettext_noop("Expires:"),
    "elements.first_name": gettext_noop("First Name"),
    "elements.form_progress": gettext_noop("Form progress"),
    "elements.get_in_touch_with_us_we_d_love_to_hear_from_you": gettext_noop(
        "Get in touch with us. We'd love to hear from you."
    ),
    "elements.gift_card": gettext_noop("Gift Card"),
    "elements.heading_text": gettext_noop("Heading Text"),
    "elements.hrs": gettext_noop("Hrs"),
    "elements.i_agree_to_the": gettext_noop("I agree to the"),
    "elements.instant_delivery": gettext_noop("Instant Delivery"),
    "elements.last_name": gettext_noop("Last Name"),
    "elements.leave_this_empty": gettext_noop("Leave this empty"),
    "elements.load_video": gettext_noop("Load Video"),
    "elements.load_more": gettext_noop("Load more"),
    "elements.locations": gettext_noop("Locations"),
    "elements.login": gettext_noop("Login"),
    "elements.logout": gettext_noop("Logout"),
    "elements.member": gettext_noop("Member"),
    "elements.menu": gettext_noop("Menu"),
    "elements.min": gettext_noop("Min:"),
    "elements.modal_content": gettext_noop("Modal content"),
    "elements.navigation": gettext_noop("Navigation"),
    "elements.never_expires": gettext_noop("Never Expires"),
    "elements.no_categories_to_display": gettext_noop("No categories to display"),
    "elements.no_featured_post_available": gettext_noop("No featured post available"),
    "elements.no_form_selected": gettext_noop("No form selected"),
    "elements.no_menu_selected_configure_this_element_to_select": gettext_noop(
        "No menu selected. Configure this element to select a menu."
    ),
    "elements.no_posts_to_display": gettext_noop("No posts to display"),
    "elements.no_products_to_display": gettext_noop("No products to display"),
    "elements.no_products_to_display_2": gettext_noop("No products to display."),
    "elements.no_related_posts_found": gettext_noop("No related posts found"),
    "elements.no_reviews_yet": gettext_noop("No reviews yet"),
    "elements.no_sale_products_available": gettext_noop("No sale products available"),
    "elements.no_social_links_configured": gettext_noop("No social links configured"),
    "elements.no_store_locations_available": gettext_noop("No store locations available"),
    "elements.no_stores_found_matching_your_search": gettext_noop(
        "No stores found matching your search"
    ),
    "elements.no_vouchers_available_at_this_time": gettext_noop(
        "No vouchers available at this time"
    ),
    "elements.or_enter_custom_amount": gettext_noop("Or enter custom amount:"),
    "elements.page_load": gettext_noop("Page Load"),
    "elements.phone_number": gettext_noop("Phone Number"),
    "elements.pickup_available": gettext_noop("Pickup available"),
    "elements.rating": gettext_noop("Rating"),
    "elements.review_title": gettext_noop("Review Title"),
    "elements.review_image": gettext_noop("Review image"),
    "elements.scroll": gettext_noop("Scroll"),
    "elements.search_suggestions": gettext_noop("Search suggestions"),
    "elements.sec": gettext_noop("Sec"),
    "elements.select_amount": gettext_noop("Select Amount:"),
    "elements.select_a_form_from_the_form_builder_or_create_a_ne": gettext_noop(
        "Select a form from the Form Builder or create a new one in the element settings."
    ),
    "elements.slide": gettext_noop("Slide"),
    "elements.sorry_there_was_an_error_sending_your_message_plea": gettext_noop(
        "Sorry, there was an error sending your message. Please try again."
    ),
    "elements.step": gettext_noop("Step"),
    "elements.submit_review": gettext_noop("Submit Review"),
    "elements.submitting": gettext_noop("Submitting..."),
    "elements.tell_us_how_we_can_help_you": gettext_noop("Tell us how we can help you..."),
    "elements.terms_of_service": gettext_noop("Terms of Service"),
    "elements.thank_you_for_your_message_we_ll_get_back_to_you_s": gettext_noop(
        "Thank you for your message! We'll get back to you soon."
    ),
    "elements.thank_you_for_your_review_it_will_be_visible_once": gettext_noop(
        "Thank you for your review! It will be visible once approved."
    ),
    "elements.time_delay": gettext_noop("Time Delay"),
    "elements.toggle_navigation_menu": gettext_noop("Toggle navigation menu"),
    "elements.using_fallback_language": gettext_noop("Using fallback language:"),
    "elements.view": gettext_noop("View"),
    "elements.view_all_categories": gettext_noop("View All Categories"),
    "elements.view_rewards": gettext_noop("View Rewards"),
    "elements.view_all_results": gettext_noop("View all results"),
    "elements.welcome_back": gettext_noop("Welcome back,"),
    "elements.what_is_this_regarding": gettext_noop("What is this regarding?"),
    "elements.write_a_review": gettext_noop("Write a Review"),
    "elements.you_save": gettext_noop("You save:"),
    "elements.your_review": gettext_noop("Your Review"),
    "elements.your_rewards_progress": gettext_noop("Your Rewards Progress"),
    "elements.your_browser_does_not_support_the_video_tag": gettext_noop(
        "Your browser does not support the video tag."
    ),
    "elements.and": gettext_noop("and"),
    "elements.stars": gettext_noop("stars"),
    "elements.uses_left": gettext_noop("uses left"),
    # === FAQ Page ===
    "faq.account": gettext_noop("Account"),
    "faq.can_i_modify_my_order_after_placing_it": gettext_noop(
        "Can I modify my order after placing it?"
    ),
    "faq.click_log_in_then_forgot_password_enter_your_email": gettext_noop(
        'Click "Log In", then "Forgot Password". Enter your email address and we\'ll send you a link to reset your password.'
    ),
    "faq.click_sign_up_in_the_header_enter_your_email_and_c": gettext_noop(
        'Click "Sign Up" in the header, enter your email and create a password. You can also create an account during checkout.'
    ),
    "faq.do_you_ship_internationally": gettext_noop("Do you ship internationally?"),
    "faq.find_answers_to_common_questions_about_our_product": gettext_noop(
        "Find answers to common questions about our products and services"
    ),
    "faq.frequently_asked_questions": gettext_noop("Frequently Asked Questions"),
    "faq.how_do_i_create_an_account": gettext_noop("How do I create an account?"),
    "faq.how_do_i_place_an_order": gettext_noop("How do I place an order?"),
    "faq.how_do_i_return_an_item": gettext_noop("How do I return an item?"),
    "faq.how_do_i_track_my_order": gettext_noop("How do I track my order?"),
    "faq.i_forgot_my_password_how_do_i_reset_it": gettext_noop(
        "I forgot my password. How do I reset it?"
    ),
    "faq.is_my_payment_information_secure": gettext_noop("Is my payment information secure?"),
    "faq.is_there_free_shipping": gettext_noop("Is there free shipping?"),
    "faq.log_into_your_account_go_to_order_history_select_t": gettext_noop(
        'Log into your account, go to Order History, select the order, and click "Request Return". Follow the instructions to print your return label.'
    ),
    "faq.once_your_order_ships_you_ll_receive_an_email_with": gettext_noop(
        "Once your order ships, you'll receive an email with tracking information. You can also track your order in your account dashboard."
    ),
    "faq.ordering": gettext_noop("Ordering"),
    "faq.our_customer_support_team_is_here_to_help": gettext_noop(
        "Our customer support team is here to help."
    ),
    "faq.refunds_are_processed_within_5_7_business_days_aft": gettext_noop(
        "Refunds are processed within 5-7 business days after we receive your return. The refund will be credited to your original payment method."
    ),
    "faq.simply_browse_our_products_add_items_to_your_cart": gettext_noop(
        "Simply browse our products, add items to your cart, and proceed to checkout. You can create an account or checkout as a guest."
    ),
    "faq.still_have_questions": gettext_noop("Still have questions?"),
    "faq.we_accept_all_major_credit_cards_visa_mastercard_a": gettext_noop(
        "We accept all major credit cards (Visa, Mastercard, American Express), PayPal, and Apple Pay."
    ),
    "faq.we_accept_returns_within_30_days_of_purchase_items": gettext_noop(
        "We accept returns within 30 days of purchase. Items must be unused and in original packaging. See our Returns Policy for full details."
    ),
    "faq.we_offer_free_standard_shipping_on_orders_over_a_c": gettext_noop(
        "We offer free standard shipping on orders over a certain amount. Check the cart for current free shipping thresholds."
    ),
    "faq.we_offer_standard_shipping_5_7_business_days_expre": gettext_noop(
        "We offer standard shipping (5-7 business days), express shipping (2-3 business days), and overnight shipping where available."
    ),
    "faq.what_are_your_shipping_options": gettext_noop("What are your shipping options?"),
    "faq.what_is_your_return_policy": gettext_noop("What is your return policy?"),
    "faq.what_payment_methods_do_you_accept": gettext_noop("What payment methods do you accept?"),
    "faq.when_will_i_receive_my_refund": gettext_noop("When will I receive my refund?"),
    "faq.yes_we_ship_to_most_countries_worldwide_internatio": gettext_noop(
        "Yes, we ship to most countries worldwide. International shipping times and costs vary by destination."
    ),
    "faq.yes_we_use_industry_standard_ssl_encryption_to_pro": gettext_noop(
        "Yes, we use industry-standard SSL encryption to protect your payment information. We never store your full credit card details."
    ),
    "faq.you_can_modify_your_order_within_1_hour_of_placing": gettext_noop(
        "You can modify your order within 1 hour of placing it. After that, please contact our customer service team for assistance."
    ),
    # === Footer ===
    "footer.24_7_support": gettext_noop("24/7 Support"),
    "footer.about_us": gettext_noop("About Us"),
    "footer.all_rights_reserved": gettext_noop("All rights reserved."),
    "footer.cookie_settings": gettext_noop("Cookie Settings"),
    "footer.customer_service": gettext_noop("Customer Service"),
    "footer.easy_returns": gettext_noop("Easy Returns"),
    "footer.faq": gettext_noop("FAQ"),
    "footer.legal": gettext_noop("Legal"),
    "footer.order_tracking": gettext_noop("Order Tracking"),
    "footer.quick_links": gettext_noop("Quick Links"),
    "footer.returns": gettext_noop("Returns"),
    "footer.shipping_info": gettext_noop("Shipping Info"),
    # === Header ===
    "header.about": gettext_noop("About"),
    "header.main_navigation": gettext_noop("Main navigation"),
    "header.mobile_navigation": gettext_noop("Mobile navigation"),
    "header.search_products": gettext_noop("Search products"),
    "header.shop": gettext_noop("Shop"),
    "header.shopping_cart": gettext_noop("Shopping cart"),
    "header.sign_up": gettext_noop("Sign Up"),
    # === Home (additional) ===
    "home.designed_for_all_devices_and_screen_sizes": gettext_noop(
        "Designed for all devices and screen sizes"
    ),
    "home.discover_amazing_products_with_our_modern_fast_and": gettext_noop(
        "Discover amazing products with our modern, fast, and lightweight shopping experience."
    ),
    "home.experience_the_future_of_online_shopping_with_our": gettext_noop(
        "Experience the future of online shopping with our cutting-edge platform"
    ),
    "home.join_thousands_of_satisfied_customers": gettext_noop(
        "Join thousands of satisfied customers"
    ),
    "home.optimized_for_speed_and_performance": gettext_noop("Optimized for speed and performance"),
    "home.welcome_2": gettext_noop("Welcome"),
    "home.your_data_and_transactions_are_always_protected": gettext_noop(
        "Your data and transactions are always protected"
    ),
    "home.products": gettext_noop("products"),
    # === Order Confirmation ===
    "order.billing_address": gettext_noop("Billing Address"),
    "order.choose_a_password": gettext_noop("Choose a Password"),
    "order.confirm_password": gettext_noop("Confirm Password"),
    "order.delivery_details": gettext_noop("Delivery Details"),
    "order.items_ordered": gettext_noop("Items Ordered"),
    "order.minimum_8_characters": gettext_noop("Minimum 8 characters"),
    "order.order_confirmed": gettext_noop("Order Confirmed"),
    "order.qty": gettext_noop("Qty"),
    "order.save_your_order_details": gettext_noop("Save Your Order Details"),
    "order.skip_for_now": gettext_noop("Skip for now"),
    "order.thank_you_for_your_order": gettext_noop("Thank you for your order!"),
    "order.we_ve_sent_a_confirmation_email_to_your_inbox": gettext_noop(
        "We've sent a confirmation email to your inbox."
    ),
    "order.or_sign_up_with": gettext_noop("or sign up with"),
    # === Privacy Policy Page ===
    "privacy.access_controls_and_authentication": gettext_noop(
        "Access controls and authentication"
    ),
    "privacy.access_your_personal_data": gettext_noop("Access your personal data"),
    "privacy.account_credentials": gettext_noop("Account credentials"),
    "privacy.address": gettext_noop("Address:"),
    "privacy.analytics_providers_to_improve_our_services": gettext_noop(
        "Analytics providers to improve our services"
    ),
    "privacy.analyze_site_traffic_and_usage": gettext_noop("Analyze site traffic and usage"),
    "privacy.automatically_collected_information": gettext_noop(
        "Automatically Collected Information"
    ),
    "privacy.by_using_our_website_you_agree_to_the_collection_a": gettext_noop(
        "By using our website, you agree to the collection and use of information in accordance with this policy."
    ),
    "privacy.communicating_with_you_about_your_orders_and_accou": gettext_noop(
        "Communicating with you about your orders and account"
    ),
    "privacy.complying_with_legal_obligations": gettext_noop("Complying with legal obligations"),
    "privacy.contents": gettext_noop("Contents"),
    "privacy.cookies": gettext_noop("Cookies"),
    "privacy.correct_inaccurate_data": gettext_noop("Correct inaccurate data"),
    "privacy.data_security": gettext_noop("Data Security"),
    "privacy.data_portability": gettext_noop("Data portability"),
    "privacy.depending_on_your_location_you_may_have_the_follow": gettext_noop(
        "Depending on your location, you may have the following rights:"
    ),
    "privacy.device_and_browser_information": gettext_noop("Device and browser information"),
    "privacy.email": gettext_noop("Email:"),
    "privacy.how_we_use_your_information": gettext_noop("How We Use Your Information"),
    "privacy.ip_address_and_location_data": gettext_noop("IP address and location data"),
    "privacy.if_you_have_questions_about_this_privacy_policy_or": gettext_noop(
        "If you have questions about this privacy policy or our data practices, please contact us:"
    ),
    "privacy.improving_our_website_and_services": gettext_noop(
        "Improving our website and services"
    ),
    "privacy.information_we_collect": gettext_noop("Information We Collect"),
    "privacy.introduction": gettext_noop("Introduction"),
    "privacy.keep_you_signed_in_to_your_account": gettext_noop(
        "Keep you signed in to your account"
    ),
    "privacy.last_updated": gettext_noop("Last updated:"),
    "privacy.legal_authorities_when_required_by_law": gettext_noop(
        "Legal authorities when required by law"
    ),
    "privacy.marketing_partners_with_your_consent": gettext_noop(
        "Marketing partners (with your consent)"
    ),
    "privacy.name_and_contact_details_email_phone_address": gettext_noop(
        "Name and contact details (email, phone, address)"
    ),
    "privacy.object_to_processing_of_your_data": gettext_noop("Object to processing of your data"),
    "privacy.order_history_and_preferences": gettext_noop("Order history and preferences"),
    "privacy.pages_visited_and_time_spent_on_our_site": gettext_noop(
        "Pages visited and time spent on our site"
    ),
    "privacy.payment_information_processed_securely_by_our_paym": gettext_noop(
        "Payment information (processed securely by our payment providers)"
    ),
    "privacy.payment_processors_to_complete_transactions": gettext_noop(
        "Payment processors to complete transactions"
    ),
    "privacy.personal_information": gettext_noop("Personal Information"),
    "privacy.personalize_content_and_advertisements": gettext_noop(
        "Personalize content and advertisements"
    ),
    "privacy.preventing_fraud_and_ensuring_security": gettext_noop(
        "Preventing fraud and ensuring security"
    ),
    "privacy.processing_and_fulfilling_your_orders": gettext_noop(
        "Processing and fulfilling your orders"
    ),
    "privacy.providing_customer_support": gettext_noop("Providing customer support"),
    "privacy.referral_sources": gettext_noop("Referral sources"),
    "privacy.regular_security_audits_and_updates": gettext_noop(
        "Regular security audits and updates"
    ),
    "privacy.remember_your_preferences_and_cart_contents": gettext_noop(
        "Remember your preferences and cart contents"
    ),
    "privacy.request_deletion_of_your_data": gettext_noop("Request deletion of your data"),
    "privacy.ssl_encryption_for_all_data_transmission": gettext_noop(
        "SSL encryption for all data transmission"
    ),
    "privacy.secure_payment_processing_through_trusted_provider": gettext_noop(
        "Secure payment processing through trusted providers"
    ),
    "privacy.sending_marketing_communications_with_your_consent": gettext_noop(
        "Sending marketing communications (with your consent)"
    ),
    "privacy.sharing_your_information": gettext_noop("Sharing Your Information"),
    "privacy.shipping_carriers_to_deliver_your_orders": gettext_noop(
        "Shipping carriers to deliver your orders"
    ),
    "privacy.to_exercise_these_rights_please_contact_us_using_t": gettext_noop(
        "To exercise these rights, please contact us using the details below."
    ),
    "privacy.we_collect_several_types_of_information_to_provide": gettext_noop(
        "We collect several types of information to provide and improve our services:"
    ),
    "privacy.we_do_not_sell_your_personal_information_to_third": gettext_noop(
        "We do not sell your personal information to third parties."
    ),
    "privacy.we_implement_appropriate_security_measures_to_prot": gettext_noop(
        "We implement appropriate security measures to protect your personal information, including:"
    ),
    "privacy.we_may_share_your_information_with": gettext_noop(
        "We may share your information with:"
    ),
    "privacy.we_respect_your_privacy_and_are_committed_to_prote": gettext_noop(
        "We respect your privacy and are committed to protecting your personal data. This privacy policy explains how we collect, use, and safeguard your information when you visit our website or make a purchase."
    ),
    "privacy.we_use_cookies_and_similar_technologies_to": gettext_noop(
        "We use cookies and similar technologies to:"
    ),
    "privacy.we_use_your_information_for_the_following_purposes": gettext_noop(
        "We use your information for the following purposes:"
    ),
    "privacy.withdraw_consent_for_marketing": gettext_noop("Withdraw consent for marketing"),
    "privacy.you_can_manage_your_cookie_preferences_through_you": gettext_noop(
        "You can manage your cookie preferences through your browser settings. Please note that disabling certain cookies may affect site functionality."
    ),
    "privacy.your_rights": gettext_noop("Your Rights"),
    # === Product (additional) ===
    "product.add_to_wishlist": gettext_noop("Add to wishlist"),
    "product.book_now": gettext_noop("Book Now"),
    "product.bundle": gettext_noop("Bundle"),
    "product.check_in": gettext_noop("Check-in"),
    "product.check_in_date": gettext_noop("Check-in date"),
    "product.check_out": gettext_noop("Check-out"),
    "product.check_out_date": gettext_noop("Check-out date"),
    "product.choose": gettext_noop("Choose"),
    "product.choose_a_provider": gettext_noop("Choose a Provider"),
    "product.choose_a_resource": gettext_noop("Choose a Resource"),
    "product.choose_a_room": gettext_noop("Choose a Room"),
    "product.choose_a_date": gettext_noop("Choose a date..."),
    "product.choose_an_item": gettext_noop("Choose an Item"),
    "product.choose_variant": gettext_noop("Choose variant"),
    "product.decrease": gettext_noop("Decrease"),
    "product.deposit_due_now": gettext_noop("Deposit Due Now"),
    "product.edition": gettext_noop("Edition"),
    "product.email_for_waitlist": gettext_noop("Email for waitlist"),
    "product.fri": gettext_noop("Fri"),
    "product.guests": gettext_noop("Guests"),
    "product.include": gettext_noop("Include"),
    "product.increase": gettext_noop("Increase"),
    "product.instant_digital_delivery": gettext_noop("Instant Digital Delivery"),
    "product.join_waitlist": gettext_noop("Join Waitlist"),
    "product.license": gettext_noop("License"),
    "product.mon": gettext_noop("Mon"),
    "product.next_month": gettext_noop("Next month"),
    "product.number_of_guests": gettext_noop("Number of Guests"),
    "product.play_video": gettext_noop("Play video"),
    "product.previous_month": gettext_noop("Previous month"),
    "product.provider": gettext_noop("Provider"),
    "product.quick_product_view": gettext_noop("Quick product view"),
    "product.quick_view": gettext_noop("Quick view"),
    "product.resource": gettext_noop("Resource"),
    "product.sat": gettext_noop("Sat"),
    "product.select_dates": gettext_noop("Select Dates"),
    "product.select_duration": gettext_noop("Select Duration"),
    "product.select_options": gettext_noop("Select Options"),
    "product.select_a_date": gettext_noop("Select a Date"),
    "product.select_a_time": gettext_noop("Select a Time"),
    "product.select_a_date_first": gettext_noop("Select a date first"),
    "product.select_booking_date": gettext_noop("Select booking date"),
    "product.sold_out": gettext_noop("Sold Out"),
    "product.sun": gettext_noop("Sun"),
    "product.this_product_is_not_available_for_purchase_in_your": gettext_noop(
        "This product is not available for purchase in your region."
    ),
    "product.this_slot_is_fully_booked_join_the_waitlist_to_be": gettext_noop(
        "This slot is fully booked. Join the waitlist to be notified if a spot opens."
    ),
    "product.thu": gettext_noop("Thu"),
    "product.time": gettext_noop("Time"),
    "product.tue": gettext_noop("Tue"),
    "product.variant": gettext_noop("Variant"),
    "product.view_full_details": gettext_noop("View Full Details"),
    "product.view_options": gettext_noop("View Options"),
    "product.view_image": gettext_noop("View image"),
    "product.wed": gettext_noop("Wed"),
    "product.what_s_included": gettext_noop("What's Included"),
    "product.your_timezone": gettext_noop("Your Timezone"),
    "product.bundle_discount_applied": gettext_noop("bundle discount applied"),
    "product.day": gettext_noop("day"),
    "product.hour": gettext_noop("hour"),
    "product.night": gettext_noop("night"),
    "product.person": gettext_noop("person"),
    "product.reviews_2": gettext_noop("reviews"),
    "product.session": gettext_noop("session"),
    # === Returns & Refunds Page ===
    "returns.30_day_returns": gettext_noop("30 Day Returns"),
    "returns.accompanied_by_the_receipt_or_proof_of_purchase": gettext_noop(
        "Accompanied by the receipt or proof of purchase"
    ),
    "returns.choose_the_reason_for_your_return_from_the_dropdow": gettext_noop(
        "Choose the reason for your return from the dropdown menu. This helps us improve our products and services."
    ),
    "returns.credit_debit_cards_3_5_business_days_for_the_refun": gettext_noop(
        "Credit/Debit Cards: 3-5 business days for the refund to appear on your statement"
    ),
    "returns.damaged_or_defective_items": gettext_noop("Damaged or Defective Items"),
    "returns.drop_off_your_package_at_any_authorized_shipping_l": gettext_noop(
        "Drop off your package at any authorized shipping location. Keep your receipt for tracking purposes."
    ),
    "returns.eligible_for_return": gettext_noop("Eligible for Return"),
    "returns.exchanges": gettext_noop("Exchanges"),
    "returns.fast_refunds": gettext_noop("Fast Refunds"),
    "returns.free_returns": gettext_noop("Free Returns"),
    "returns.gift_cards_and_digital_products": gettext_noop("Gift cards and digital products"),
    "returns.hazardous_materials_or_flammable_liquids": gettext_noop(
        "Hazardous materials or flammable liquids"
    ),
    "returns.how_to_return_an_item": gettext_noop("How to Return an Item"),
    "returns.if_you_need_a_different_size_color_or_product_we_r": gettext_noop(
        "If you need a different size, color, or product, we recommend returning the original item for a refund and placing a new order. This ensures the fastest processing time and guarantees availability of your desired item."
    ),
    "returns.if_you_received_a_damaged_or_defective_item_please": gettext_noop(
        "If you received a damaged or defective item, please contact us immediately. We will arrange for a replacement or full refund at no additional cost to you."
    ),
    "returns.in_the_original_packaging_with_all_tags_attached": gettext_noop(
        "In the original packaging with all tags attached"
    ),
    "returns.intimate_or_sanitary_goods": gettext_noop("Intimate or sanitary goods"),
    "returns.items_marked_as_final_sale_or_non_returnable": gettext_noop(
        'Items marked as "Final Sale" or "Non-Returnable"'
    ),
    "returns.items_must_be_unused_with_tags_attached": gettext_noop(
        "Items must be unused with tags attached"
    ),
    "returns.log_into_your_account_and_go_to_order_history_sele": gettext_noop(
        'Log into your account and go to "Order History". Select the order containing the item you wish to return and click "Request Return".'
    ),
    "returns.need_help": gettext_noop("Need Help?"),
    "returns.non_returnable_items": gettext_noop("Non-Returnable Items"),
    "returns.once_approved_you_ll_receive_a_prepaid_shipping_la": gettext_noop(
        "Once approved, you'll receive a prepaid shipping label via email. Print it and attach it to your package."
    ),
    "returns.once_we_receive_and_inspect_your_return_we_ll_proc": gettext_noop(
        "Once we receive and inspect your return, we'll process your refund to the original payment method."
    ),
    "returns.original_packaging": gettext_noop("Original Packaging"),
    "returns.our_customer_service_team_is_available_to_assist_y": gettext_noop(
        "Our customer service team is available to assist you with returns and refunds."
    ),
    "returns.paypal_1_2_business_days": gettext_noop("PayPal: 1-2 business days"),
    "returns.personalized_or_custom_made_items": gettext_noop("Personalized or custom-made items"),
    "returns.please_include_photos_of_the_damage_when_contactin": gettext_noop(
        "Please include photos of the damage when contacting customer support to expedite the process."
    ),
    "returns.print_shipping_label": gettext_noop("Print Shipping Label"),
    "returns.receive_your_refund": gettext_noop("Receive Your Refund"),
    "returns.refund_processing": gettext_noop("Refund Processing"),
    "returns.refunds_are_processed_within_5_7_business_days_aft": gettext_noop(
        "Refunds are processed within 5-7 business days after we receive your return. The refund will be credited to your original payment method:"
    ),
    "returns.refunds_processed_in_5_7_business_days": gettext_noop(
        "Refunds processed in 5-7 business days"
    ),
    "returns.return_within_30_days_of_purchase": gettext_noop("Return within 30 days of purchase"),
    "returns.returned_within_30_days_of_the_delivery_date": gettext_noop(
        "Returned within 30 days of the delivery date"
    ),
    "returns.select_return_reason": gettext_noop("Select Return Reason"),
    "returns.ship_your_return": gettext_noop("Ship Your Return"),
    "returns.start_your_return": gettext_noop("Start Your Return"),
    "returns.store_credit_immediately_available_in_your_account": gettext_noop(
        "Store Credit: Immediately available in your account"
    ),
    "returns.the_following_items_cannot_be_returned": gettext_noop(
        "The following items cannot be returned:"
    ),
    "returns.to_be_eligible_for_a_return_your_item_must_be": gettext_noop(
        "To be eligible for a return, your item must be:"
    ),
    "returns.unused_and_in_the_same_condition_that_you_received": gettext_noop(
        "Unused and in the same condition that you received it"
    ),
    "returns.view_faq": gettext_noop("View FAQ"),
    "returns.we_cover_return_shipping_costs": gettext_noop("We cover return shipping costs"),
    "returns.we_want_you_to_be_completely_satisfied_with_your_p": gettext_noop(
        "We want you to be completely satisfied with your purchase"
    ),
    # === Stock (additional) ===
    "stock.check_store_availability": gettext_noop("Check Store Availability"),
    "stock.store_availability": gettext_noop("Store Availability"),
    # === Product Customizer ===
    "customizable_product.add_text": gettext_noop("Add Text"),
    "customizable_product.align_center": gettext_noop("Align Center"),
    "customizable_product.align_left": gettext_noop("Align Left"),
    "customizable_product.align_right": gettext_noop("Align Right"),
    "customizable_product.bold": gettext_noop("Bold"),
    "customizable_product.brightness": gettext_noop("Brightness"),
    "customizable_product.clipart": gettext_noop("Clipart"),
    "customizable_product.color": gettext_noop("Color"),
    "customizable_product.contrast": gettext_noop("Contrast"),
    "customizable_product.delete_selected": gettext_noop("Delete Selected"),
    "customizable_product.design_fee": gettext_noop("Design fee"),
    "customizable_product.duplicate": gettext_noop("Duplicate"),
    "customizable_product.flip_horizontal": gettext_noop("Flip Horizontal"),
    "customizable_product.flip_vertical": gettext_noop("Flip Vertical"),
    "customizable_product.font": gettext_noop("Font"),
    "customizable_product.image": gettext_noop("Image"),
    "customizable_product.italic": gettext_noop("Italic"),
    "customizable_product.layers": gettext_noop("Layers"),
    "customizable_product.my_designs": gettext_noop("My Designs"),
    "customizable_product.opacity": gettext_noop("Opacity"),
    "customizable_product.outline": gettext_noop("Outline"),
    "customizable_product.redo": gettext_noop("Redo"),
    "customizable_product.remove_color": gettext_noop("Remove Color"),
    "customizable_product.rotate_minus_90": gettext_noop("Rotate -90°"),
    "customizable_product.rotate_90": gettext_noop("Rotate 90°"),
    "customizable_product.rotation": gettext_noop("Rotation"),
    "customizable_product.saturation": gettext_noop("Saturation"),
    "customizable_product.save_design": gettext_noop("Save Design"),
    "customizable_product.search_clipart": gettext_noop("Search clipart..."),
    "customizable_product.size": gettext_noop("Size"),
    "customizable_product.supported_formats": gettext_noop("Supported: JPG, PNG, WebP"),
    "customizable_product.templates": gettext_noop("Templates"),
    "customizable_product.text": gettext_noop("Text"),
    "customizable_product.tint": gettext_noop("Tint"),
    "customizable_product.toggle_fullscreen": gettext_noop("Toggle Fullscreen"),
    "customizable_product.undo": gettext_noop("Undo"),
    "customizable_product.upload_image": gettext_noop("Upload Image"),
    "customizable_product.zoom_in": gettext_noop("Zoom In"),
    "customizable_product.zoom_out": gettext_noop("Zoom Out"),
    # === Booking ===
    "booking.from": gettext_noop("From"),
    "booking.resource_details": gettext_noop("Resource Details"),
    "booking.select_this_room": gettext_noop("Select This Room"),
    "booking.select_date": gettext_noop("Select date"),
    "booking.view_details": gettext_noop("View details"),
    # === Product (additional) ===
    "product.not_available_in_region": gettext_noop("Not available in your region"),
    "product.view_product": gettext_noop("View product"),
    # === 3D Configurator (additional) ===
    "configurator_3d.toggle_fullscreen": gettext_noop("Toggle fullscreen"),
    # === Header (additional) ===
    "header.close_announcement": gettext_noop("Close announcement"),
    "header.close_menu": gettext_noop("Close menu"),
    "header.search_placeholder": gettext_noop("Search..."),
    "header.close": gettext_noop("Close"),
    "header.login": gettext_noop("Login"),
    "header.logout": gettext_noop("Logout"),
    "header.my_account": gettext_noop("My Account"),
    "header.home": gettext_noop("Home"),
    "header.menu": gettext_noop("Menu"),
    # === Widgets (additional) ===
    "widgets.change_language": gettext_noop("Change language"),
    "widgets.logo": gettext_noop("Logo"),
    "widgets.search_placeholder": gettext_noop("Search..."),
    "widgets.subscribe_success": gettext_noop("Thank you for subscribing!"),
    "widgets.subscribe_error": gettext_noop("Subscription failed. Please try again."),
    # === Elements (additional) ===
    "elements.hours": gettext_noop("Hours"),
    "elements.minutes": gettext_noop("Minutes"),
    "elements.seconds": gettext_noop("Seconds"),
    "elements.this_offer_has_ended": gettext_noop("This offer has ended"),
    "elements.read_more": gettext_noop("Read More"),
    "elements.view_all_posts": gettext_noop("View All Posts"),
    "elements.read_article": gettext_noop("Read Article"),
    "elements.view_all_products": gettext_noop("View All Products"),
    "elements.search_products_categories": gettext_noop("Search products, categories..."),
    "elements.no_results_try_different": gettext_noop(
        "No results found. Try a different search term."
    ),
    "elements.find_a_store": gettext_noop("Find a Store"),
    "elements.locate_stores_near_you": gettext_noop(
        "Locate our stores near you for pickup and in-person shopping"
    ),
    "elements.menu_not_available": gettext_noop("Menu not available"),
    "elements.image": gettext_noop("Image"),
    "elements.submit": gettext_noop("Submit"),
}


# Reverse registry: English source string -> registry key
_REVERSE_REGISTRY = None


def get_reverse_registry():
    """Build/return a reverse lookup from English source string to registry key."""
    global _REVERSE_REGISTRY
    if _REVERSE_REGISTRY is None:
        _REVERSE_REGISTRY = {v: k for k, v in UI_STRING_REGISTRY.items()}
    return _REVERSE_REGISTRY


def get_section_for_key(key):
    """Get the section identifier for a registry key."""
    return key.split(".")[0] if "." in key else "common"


def get_strings_by_section():
    """Group registry strings by section for the admin editor."""
    grouped = {}
    for key, value in UI_STRING_REGISTRY.items():
        section = get_section_for_key(key)
        if section not in grouped:
            grouped[section] = {}
        grouped[section][key] = value
    return grouped


def get_total_string_count():
    """Return total number of registered strings."""
    return len(UI_STRING_REGISTRY)
