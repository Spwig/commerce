from core.management.commands._seed_base import SeedCommand
from page_builder.management.commands._element_translations import ELEMENT_TRANSLATIONS


class Command(SeedCommand):
    seed_name = 'page_elements'
    seed_version = 2
    help = 'Create default page elements for all default pages'

    def seed(self) -> int:
        from page_builder.models import Page, Element

        total = 0
        total += self._seed_404_elements(Page, Element)
        total += self._seed_500_elements(Page, Element)
        total += self._seed_about_elements(Page, Element)
        total += self._seed_contact_elements(Page, Element)
        total += self._seed_faq_elements(Page, Element)
        total += self._seed_privacy_elements(Page, Element)
        total += self._seed_terms_elements(Page, Element)
        total += self._seed_shipping_elements(Page, Element)
        total += self._seed_returns_elements(Page, Element)
        total += self._seed_cookie_elements(Page, Element)
        total += self._seed_home_elements(Page, Element)
        total += self._seed_maintenance_elements(Page, Element)

        # Apply pre-baked translations from _element_translations.py
        self._apply_translations(Element)

        return total

    def _page_needs_seeding(self, Page, Element, slug):
        """Check if a page exists AND has no elements (needs seeding)."""
        try:
            page = Page.objects.get(slug=slug)
        except Page.DoesNotExist:
            return None
        if Element.objects.filter(page=page).exists():
            return None
        return page

    def _apply_translations(self, Element):
        """Apply pre-baked translations to elements using page-qualified keys."""
        from page_builder.models import Page
        for key, translations in ELEMENT_TRANSLATIONS.items():
            if ':' in key:
                page_slug, element_name = key.split(':', 1)
                try:
                    page = Page.objects.get(slug=page_slug)
                except Page.DoesNotExist:
                    continue
                page_element_ids = self._get_page_element_ids(page, Element)
                Element.objects.filter(
                    id__in=page_element_ids, name=element_name
                ).update(translations=translations)
            else:
                Element.objects.filter(
                    name=key
                ).update(translations=translations)

    def _get_page_element_ids(self, page, Element):
        """Get all element IDs for a page, including nested children."""
        ids = set()
        parent_ids = set(
            Element.objects.filter(page=page).values_list('id', flat=True)
        )
        ids.update(parent_ids)
        for _ in range(5):
            child_ids = set(
                Element.objects.filter(
                    parent_element_id__in=parent_ids
                ).values_list('id', flat=True)
            )
            if not child_ids:
                break
            ids.update(child_ids)
            parent_ids = child_ids
        return ids

    # =========================================================================
    # 404 PAGE ELEMENTS (from migration 0026)
    # =========================================================================
    def _seed_404_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, '404')
        if not page:
            return 0

        count = 0
        order = 0

        # Top Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Top Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        # Main Heading
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='heading', name='Main Title',
            order=order, column_span=12, text_align='center',
            content={'text': 'Oops! Page Not Found', 'tag': 'h1', 'size': '4xl', 'weight': 'bold', 'color': '#1f2937'},
            is_active=True,
        )

        # Title Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Title Spacer',
            order=order, column_span=12,
            content={'height': 20, 'height_unit': 'px'}, is_active=True,
        )

        # Description
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='text', name='Description',
            order=order, column_span=12, text_align='center',
            content={
                'text': "We couldn't find the page you're looking for. It might have been moved, deleted, or perhaps the URL was mistyped.",
                'size': 'lg', 'color': '#6b7280', 'max_width': 'prose',
            },
            is_active=True,
        )

        # Button Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Button Spacer',
            order=order, column_span=12,
            content={'height': 30, 'height_unit': 'px'}, is_active=True,
        )

        # Button Container
        order += 1; count += 1
        button_container = Element.objects.create(
            page=page, element_type='container', name='Button Container',
            order=order, column_span=12, text_align='center',
            content={'display': 'flex', 'justify_content': 'center', 'align_items': 'center', 'gap': '16px', 'flex_wrap': 'wrap'},
            is_active=True,
        )

        # Home Button
        count += 1
        Element.objects.create(
            page=None, parent_element=button_container, element_type='button', name='Home Button',
            order=1, column_span=12,
            content={'text': 'Return to Home', 'url': '/', 'style': 'primary', 'size': 'lg', 'icon': 'fa-home', 'icon_position': 'left'},
            link_url='/', link_target='_self', is_active=True,
        )

        # Products Button
        count += 1
        Element.objects.create(
            page=None, parent_element=button_container, element_type='button', name='Products Button',
            order=2, column_span=12,
            content={'text': 'Browse Products', 'url': '/products/', 'style': 'outline', 'size': 'lg', 'icon': 'fa-shopping-bag', 'icon_position': 'left'},
            link_url='/products/', link_target='_self', is_active=True,
        )

        # Divider Top Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Divider Top Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        # Divider
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='divider', name='Section Divider',
            order=order, column_span=12,
            content={'style': 'solid', 'color': '#e5e7eb', 'thickness': 1, 'width': '50%', 'alignment': 'center'},
            is_active=True,
        )

        # Divider Bottom Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Divider Bottom Spacer',
            order=order, column_span=12,
            content={'height': 30, 'height_unit': 'px'}, is_active=True,
        )

        # Categories Title
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='heading', name='Categories Title',
            order=order, column_span=12, text_align='center',
            content={'text': 'Popular Categories', 'tag': 'h3', 'size': 'xl', 'weight': 'semibold', 'color': '#374151'},
            is_active=True,
        )

        # Categories Description
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='text', name='Categories Description',
            order=order, column_span=12, text_align='center',
            content={'text': 'Or explore our most popular sections:', 'size': 'base', 'color': '#6b7280'},
            is_active=True,
        )

        # Categories Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Categories Spacer',
            order=order, column_span=12,
            content={'height': 16, 'height_unit': 'px'}, is_active=True,
        )

        # Category Buttons Container
        order += 1; count += 1
        cat_container = Element.objects.create(
            page=page, element_type='container', name='Category Buttons Container',
            order=order, column_span=12, text_align='center',
            content={'display': 'flex', 'justify_content': 'center', 'align_items': 'center', 'gap': '12px', 'flex_wrap': 'wrap'},
            is_active=True,
        )

        # Category Link Buttons
        category_links = [
            {'text': 'New Arrivals', 'url': '/products/?sort=newest'},
            {'text': 'Best Sellers', 'url': '/products/?sort=bestselling'},
            {'text': 'On Sale', 'url': '/products/?on_sale=true'},
        ]
        for idx, cat in enumerate(category_links, start=1):
            count += 1
            Element.objects.create(
                page=None, parent_element=cat_container, element_type='button',
                name=f'{cat["text"]} Link', order=idx, column_span=12,
                content={'text': cat['text'], 'url': cat['url'], 'style': 'ghost', 'size': 'md'},
                link_url=cat['url'], link_target='_self', is_active=True,
            )

        # Bottom Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Bottom Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        return count

    # =========================================================================
    # 500 PAGE ELEMENTS (from migration 0026)
    # =========================================================================
    def _seed_500_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, '500')
        if not page:
            return 0

        count = 0
        order = 0

        # Top Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Top Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        # Warning Icon
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='icon', name='Warning Icon',
            order=order, column_span=12, text_align='center',
            content={'icon': 'fa-exclamation-triangle', 'icon_style': 'solid', 'size': 64, 'size_unit': 'px', 'color': '#f59e0b'},
            is_active=True,
        )

        # Icon Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Icon Spacer',
            order=order, column_span=12,
            content={'height': 20, 'height_unit': 'px'}, is_active=True,
        )

        # Main Title
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='heading', name='Main Title',
            order=order, column_span=12, text_align='center',
            content={'text': 'Something Went Wrong', 'tag': 'h1', 'size': '3xl', 'weight': 'bold', 'color': '#1f2937'},
            is_active=True,
        )

        # Title Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Title Spacer',
            order=order, column_span=12,
            content={'height': 16, 'height_unit': 'px'}, is_active=True,
        )

        # Description
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='text', name='Description',
            order=order, column_span=12, text_align='center',
            content={
                'text': "We're experiencing technical difficulties. Our team has been notified and is working to fix the issue. Please try again in a few moments.",
                'size': 'lg', 'color': '#6b7280', 'max_width': 'prose',
            },
            is_active=True,
        )

        # Button Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Button Spacer',
            order=order, column_span=12,
            content={'height': 30, 'height_unit': 'px'}, is_active=True,
        )

        # Button Container
        order += 1; count += 1
        button_container = Element.objects.create(
            page=page, element_type='container', name='Button Container',
            order=order, column_span=12, text_align='center',
            content={'display': 'flex', 'justify_content': 'center', 'align_items': 'center', 'gap': '16px', 'flex_wrap': 'wrap'},
            is_active=True,
        )

        # Try Again Button
        count += 1
        Element.objects.create(
            page=None, parent_element=button_container, element_type='button', name='Try Again Button',
            order=1, column_span=12,
            content={'text': 'Try Again', 'style': 'primary', 'size': 'lg', 'icon': 'fa-redo', 'icon_position': 'left', 'onclick': 'location.reload()'},
            is_active=True,
        )

        # Home Button
        count += 1
        Element.objects.create(
            page=None, parent_element=button_container, element_type='button', name='Home Button',
            order=2, column_span=12,
            content={'text': 'Return to Home', 'url': '/', 'style': 'outline', 'size': 'lg', 'icon': 'fa-home', 'icon_position': 'left'},
            link_url='/', link_target='_self', is_active=True,
        )

        # Support Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Support Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        # Support Contact
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='text', name='Support Contact',
            order=order, column_span=12, text_align='center',
            content={
                'text': 'If the problem persists, please contact us at {{ site_settings.support_email|default:"support@example.com" }}',
                'size': 'sm', 'color': '#9ca3af',
            },
            is_active=True,
        )

        # Bottom Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Bottom Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        return count

    # =========================================================================
    # ABOUT PAGE ELEMENTS (from migration 0027)
    # =========================================================================
    def _seed_about_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, 'about')
        if not page:
            return 0

        count = 0
        order = 0

        # Hero
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='hero', name='About Hero',
            order=order, column_span=12,
            content={'title': 'Our Story', 'subtitle': 'Building quality products since we first opened our doors', 'text_align': 'center'},
            is_active=True,
        )

        # Hero Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Hero Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        # Welcome Container
        order += 1; count += 1
        welcome_container = Element.objects.create(
            page=page, element_type='container', name='Welcome Container',
            order=order, column_span=12,
            content={'layout': 'flex', 'direction': 'column', 'gap': '0px', 'max_width': '1024px', 'spacing': 'margin: 0 auto;', 'layout_initialized': True},
            is_active=True,
        )

        # Welcome Title
        count += 1
        Element.objects.create(
            page=None, parent_element=welcome_container, element_type='heading', name='Welcome Title',
            order=1, column_span=12, text_align='center',
            content={'text': 'Welcome to Our Store', 'tag': 'h2'}, is_active=True,
        )

        # Title Spacer
        count += 1
        Element.objects.create(
            page=None, parent_element=welcome_container, element_type='spacer', name='Title Spacer',
            order=2, column_span=12,
            content={'height': 20, 'height_unit': 'px'}, is_active=True,
        )

        # Welcome Text
        count += 1
        Element.objects.create(
            page=None, parent_element=welcome_container, element_type='text', name='Welcome Text',
            order=3, column_span=12, text_align='center',
            content={
                'text': "We're passionate about delivering exceptional products and outstanding customer service. Founded with a simple mission: to provide quality products at fair prices, we've grown into a trusted destination for thousands of satisfied customers.\n\nOur team works tirelessly to source the best products, ensure fast shipping, and provide support that truly cares about your experience.",
            },
            is_active=True,
        )

        # Features Top Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Features Top Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        # Features Title
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='heading', name='Features Title',
            order=order, column_span=12, text_align='center',
            content={'text': 'What Sets Us Apart', 'tag': 'h2'}, is_active=True,
        )

        # Features Cards Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Features Cards Spacer',
            order=order, column_span=12,
            content={'height': 30, 'height_unit': 'px'}, is_active=True,
        )

        # Features Grid
        order += 1; count += 1
        features_grid = Element.objects.create(
            page=page, element_type='container', name='Features Grid',
            order=order, column_span=12,
            content={
                'layout': 'flex', 'direction': 'row', 'gap': '32px', 'wrap': 'wrap',
                'width': '100%', 'max_width': '1200px', 'spacing': 'margin: 0 auto;',
                'mobile_stack': True, 'layout_initialized': True,
            },
            is_active=True,
        )

        # Feature Cards
        features = [
            {'icon': 'fa-gem', 'title': 'Quality Products', 'description': 'We carefully select every item in our catalog, ensuring it meets our high standards for quality and value.'},
            {'icon': 'fa-truck', 'title': 'Fast Shipping', 'description': 'Quick and reliable delivery to your doorstep. We partner with trusted carriers to ensure your order arrives safely.'},
            {'icon': 'fa-headset', 'title': 'Customer Support', 'description': 'Our friendly team is here to help with any questions or concerns. We believe in building lasting relationships.'},
        ]

        for idx, feature in enumerate(features, start=1):
            count += 1
            card = Element.objects.create(
                page=None, parent_element=features_grid, element_type='container',
                name=f'{feature["title"]} Card', order=idx, column_span=12, text_align='center',
                content={'layout': 'flex', 'direction': 'column', 'gap': '0px', 'flex': '1', 'align_items': 'center', 'layout_initialized': True},
                is_active=True,
            )
            count += 1
            Element.objects.create(
                page=None, parent_element=card, element_type='icon',
                name=f'{feature["title"]} Icon', order=1, column_span=12, text_align='center',
                content={'icon': feature['icon'], 'icon_style': 'solid', 'size': 48, 'size_unit': 'px'},
                is_active=True,
            )
            count += 1
            Element.objects.create(
                page=None, parent_element=card, element_type='spacer',
                name=f'{feature["title"]} Spacer', order=2, column_span=12,
                content={'height': 16, 'height_unit': 'px'}, is_active=True,
            )
            count += 1
            Element.objects.create(
                page=None, parent_element=card, element_type='heading',
                name=f'{feature["title"]} Title', order=3, column_span=12, text_align='center',
                content={'text': feature['title'], 'tag': 'h3'}, is_active=True,
            )
            count += 1
            Element.objects.create(
                page=None, parent_element=card, element_type='text',
                name=f'{feature["title"]} Description', order=4, column_span=12, text_align='center',
                content={'text': feature['description']}, is_active=True,
            )

        # CTA Top Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='CTA Top Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        # Shop CTA
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='cta_banner', name='Shop CTA',
            order=order, column_span=12,
            content={
                'title': 'Ready to Explore?',
                'subtitle': "Browse our collection and find something you'll love.",
                'cta_text': 'Shop Now', 'cta_url': '/products/', 'cta_style': 'solid',
            },
            is_active=True,
        )

        # Bottom Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Bottom Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        return count

    # =========================================================================
    # CONTACT PAGE ELEMENTS (from migration 0027)
    # =========================================================================
    def _seed_contact_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, 'contact')
        if not page:
            return 0

        count = 0
        order = 0

        # Hero
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='hero', name='Contact Hero',
            order=order, column_span=12,
            content={
                'title': 'Get in Touch',
                'subtitle': "We'd love to hear from you. Send us a message and we'll respond as soon as possible.",
                'text_align': 'center', 'padding_y': '60px', 'min_height': '300px', 'title_size': '3xl', 'subtitle_size': 'lg',
            },
            is_active=True,
        )

        # Hero Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Hero Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        # Main Content Row
        order += 1; count += 1
        row = Element.objects.create(
            page=page, element_type='container', name='Main Content',
            order=order, column_span=12,
            content={
                'layout': 'flex', 'direction': 'row', 'gap': '48px', 'wrap': 'wrap',
                'width': '100%', 'max_width': '1200px', 'spacing': 'margin: 0 auto;',
                'mobile_stack': True, 'layout_initialized': True,
            },
            is_active=True,
        )

        # Left Column: Form
        count += 1
        left_col = Element.objects.create(
            page=None, parent_element=row, element_type='container', name='Form Column',
            order=1, column_span=12,
            content={'layout': 'flex', 'direction': 'column', 'gap': '16px', 'flex': '1', 'layout_initialized': True},
            is_active=True,
        )

        count += 1
        Element.objects.create(
            page=None, parent_element=left_col, element_type='heading', name='Form Title',
            order=1, column_span=12,
            content={'text': 'Send Us a Message', 'tag': 'h2', 'size': 'xl', 'weight': 'semibold', 'alignment': 'left'},
            is_active=True,
        )

        count += 1
        Element.objects.create(
            page=None, parent_element=left_col, element_type='contact_form', name='Contact Form',
            order=2, column_span=12,
            content={
                'fields': [
                    {'name': 'name', 'type': 'text', 'label': 'Your Name', 'required': True},
                    {'name': 'email', 'type': 'email', 'label': 'Email Address', 'required': True},
                    {'name': 'subject', 'type': 'text', 'label': 'Subject', 'required': True},
                    {'name': 'message', 'type': 'textarea', 'label': 'Message', 'rows': 5, 'required': True},
                ],
                'button_text': 'Send Message', 'button_style': 'primary',
                'success_message': "Thank you for your message! We'll get back to you soon.",
            },
            is_active=True,
        )

        # Right Column: Info
        count += 1
        right_col = Element.objects.create(
            page=None, parent_element=row, element_type='container', name='Info Column',
            order=2, column_span=12,
            content={'layout': 'flex', 'direction': 'column', 'gap': '16px', 'flex': '1', 'layout_initialized': True},
            is_active=True,
        )

        count += 1
        Element.objects.create(
            page=None, parent_element=right_col, element_type='heading', name='Info Title',
            order=1, column_span=12,
            content={'text': 'Contact Information', 'tag': 'h2', 'size': 'xl', 'weight': 'semibold', 'alignment': 'left'},
            is_active=True,
        )

        count += 1
        Element.objects.create(
            page=None, parent_element=right_col, element_type='spacer', name='Info Title Spacer',
            order=2, column_span=12,
            content={'height': 8, 'height_unit': 'px'}, is_active=True,
        )

        # Contact Info Items
        contact_items = [
            {'icon': 'fa-envelope', 'label': 'Email', 'value': 'support@example.com'},
            {'icon': 'fa-phone', 'label': 'Phone', 'value': '+1 (555) 123-4567'},
            {'icon': 'fa-map-marker-alt', 'label': 'Address', 'value': '123 Business Street, City, Country'},
            {'icon': 'fa-clock', 'label': 'Hours', 'value': 'Monday - Friday: 9:00 AM - 5:00 PM'},
        ]

        for idx, item in enumerate(contact_items, start=3):
            count += 1
            info_row = Element.objects.create(
                page=None, parent_element=right_col, element_type='container',
                name=f'{item["label"]} Row', order=idx, column_span=12,
                content={'layout': 'flex', 'direction': 'row', 'align_items': 'flex-start', 'gap': '16px', 'layout_initialized': True},
                is_active=True,
            )
            count += 1
            Element.objects.create(
                page=None, parent_element=info_row, element_type='icon',
                name=f'{item["label"]} Icon', order=1, column_span=12,
                content={'icon': item['icon'], 'icon_style': 'solid', 'size': 20, 'size_unit': 'px'},
                is_active=True,
            )
            count += 1
            text_container = Element.objects.create(
                page=None, parent_element=info_row, element_type='container',
                name=f'{item["label"]} Text', order=2, column_span=12,
                content={'layout': 'flex', 'direction': 'column', 'gap': '4px', 'layout_initialized': True},
                is_active=True,
            )
            count += 1
            Element.objects.create(
                page=None, parent_element=text_container, element_type='text',
                name=f'{item["label"]} Label', order=1, column_span=12,
                content={'text': item['label'], 'size': 'sm', 'weight': 'semibold'}, is_active=True,
            )
            count += 1
            Element.objects.create(
                page=None, parent_element=text_container, element_type='text',
                name=f'{item["label"]} Value', order=2, column_span=12,
                content={'text': item['value'], 'size': 'base'}, is_active=True,
            )

        # Social Links Section
        count += 1
        Element.objects.create(
            page=None, parent_element=right_col, element_type='spacer', name='Social Spacer',
            order=10, column_span=12,
            content={'height': 24, 'height_unit': 'px'}, is_active=True,
        )

        count += 1
        Element.objects.create(
            page=None, parent_element=right_col, element_type='heading', name='Social Title',
            order=11, column_span=12,
            content={'text': 'Follow Us', 'tag': 'h3', 'size': 'lg', 'weight': 'semibold', 'alignment': 'left'},
            is_active=True,
        )

        count += 1
        Element.objects.create(
            page=None, parent_element=right_col, element_type='spacer', name='Social Links Spacer',
            order=12, column_span=12,
            content={'height': 12, 'height_unit': 'px'}, is_active=True,
        )

        count += 1
        Element.objects.create(
            page=None, parent_element=right_col, element_type='social_links', name='Social Media Links',
            order=13, column_span=12,
            content={
                'style': 'icons', 'size': 'lg', 'color_scheme': 'brand',
                'platforms': [
                    {'platform': 'facebook', 'url': '#'},
                    {'platform': 'twitter', 'url': '#'},
                    {'platform': 'instagram', 'url': '#'},
                    {'platform': 'linkedin', 'url': '#'},
                ],
            },
            is_active=True,
        )

        # Bottom Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Bottom Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        return count

    # =========================================================================
    # FAQ PAGE ELEMENTS (from migration 0027)
    # =========================================================================
    def _seed_faq_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, 'faq')
        if not page:
            return 0

        count = 0
        order = 0

        # Hero
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='hero', name='FAQ Hero',
            order=order, column_span=12,
            content={
                'title': 'Frequently Asked Questions',
                'subtitle': 'Find answers to common questions about orders, shipping, returns, and more.',
                'text_align': 'center', 'padding_y': '50px', 'min_height': '280px', 'title_size': '3xl', 'subtitle_size': 'lg',
            },
            is_active=True,
        )

        # Hero Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Hero Spacer',
            order=order, column_span=12,
            content={'height': 50, 'height_unit': 'px'}, is_active=True,
        )

        # Main Container
        order += 1; count += 1
        main_container = Element.objects.create(
            page=page, element_type='container', name='FAQ Content',
            order=order, column_span=12,
            content={
                'layout': 'flex', 'direction': 'column', 'gap': '24px',
                'max_width': '3xl', 'spacing': 'margin: 0 auto;', 'padding_x': '24px', 'layout_initialized': True,
            },
            is_active=True,
        )

        # FAQ Sections
        faq_sections = [
            {
                'name': 'Orders & Shipping FAQ',
                'title': 'Orders & Shipping',
                'items': [
                    {'question': 'How do I track my order?', 'answer': "Once your order ships, you'll receive an email with a tracking number and link. You can also track your order by logging into your account and viewing your order history.", 'is_open': True},
                    {'question': 'How long does shipping take?', 'answer': 'Standard shipping typically takes 5-7 business days. Express shipping options are available at checkout for faster delivery (2-3 business days).', 'is_open': False},
                    {'question': 'Do you ship internationally?', 'answer': 'Yes! We ship to most countries worldwide. International shipping times vary by destination, typically 7-14 business days. Please note that customs fees may apply.', 'is_open': False},
                ],
            },
            {
                'name': 'Returns & Refunds FAQ',
                'title': 'Returns & Refunds',
                'items': [
                    {'question': 'What is your return policy?', 'answer': 'We offer a 30-day return policy for most items. Products must be unused and in original packaging. Some items like personalized products may not be eligible for return.', 'is_open': False},
                    {'question': 'How do I return an item?', 'answer': 'To initiate a return, log into your account, go to Order History, and select the item you wish to return. Follow the prompts to print a return label and ship the item back to us.', 'is_open': False},
                    {'question': 'When will I receive my refund?', 'answer': 'Refunds are processed within 5-7 business days after we receive your returned item. The refund will be credited to your original payment method.', 'is_open': False},
                ],
            },
            {
                'name': 'Payment & Security FAQ',
                'title': 'Payment & Security',
                'items': [
                    {'question': 'What payment methods do you accept?', 'answer': 'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and various local payment methods depending on your region.', 'is_open': False},
                    {'question': 'Is my payment information secure?', 'answer': 'Absolutely. We use industry-standard SSL encryption to protect your data. We never store your full credit card details on our servers.', 'is_open': False},
                ],
            },
        ]

        for child_order, section in enumerate(faq_sections, start=1):
            count += 1
            Element.objects.create(
                page=None, parent_element=main_container, element_type='faq_accordion',
                name=section['name'], order=child_order, column_span=12,
                content={
                    'title': section['title'], 'subtitle': '', 'style': 'bordered',
                    'behavior': 'single', 'animate': True, 'icon_style': 'chevron',
                    'icon_position': 'right', 'gap': 'sm', 'enable_schema': True,
                    'items': section['items'],
                },
                is_active=True,
            )

        # CTA Top Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='CTA Top Spacer',
            order=order, column_span=12,
            content={'height': 20, 'height_unit': 'px'}, is_active=True,
        )

        # Contact CTA
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='cta_banner', name='Contact CTA',
            order=order, column_span=12,
            content={
                'title': 'Still have questions?',
                'subtitle': "Our support team is ready to help. Don't hesitate to reach out.",
                'cta_text': 'Contact Us', 'cta_url': '/en/page/contact-us/', 'cta_style': 'primary',
            },
            is_active=True,
        )

        # Bottom Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Bottom Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        return count

    # =========================================================================
    # PRIVACY POLICY ELEMENTS (from migration 0028)
    # =========================================================================
    def _seed_privacy_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, 'privacy-policy')
        if not page:
            return 0
        return self._seed_legal_page(page, Element, 'Privacy Policy', self._privacy_sections())

    # =========================================================================
    # TERMS OF USE ELEMENTS (from migration 0028)
    # =========================================================================
    def _seed_terms_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, 'terms-of-use')
        if not page:
            return 0
        return self._seed_legal_page(page, Element, 'Terms of Use', self._terms_sections())

    # =========================================================================
    # COOKIE POLICY ELEMENTS (from migration 0028)
    # =========================================================================
    def _seed_cookie_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, 'cookie-policy')
        if not page:
            return 0
        return self._seed_legal_page(page, Element, 'Cookie Policy', self._cookie_sections())

    # =========================================================================
    # SHIPPING INFO ELEMENTS (from migration 0028)
    # =========================================================================
    def _seed_shipping_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, 'shipping-info')
        if not page:
            return 0

        count = 0
        order = 0

        # Hero
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='hero', name='Shipping Hero',
            order=order, column_span=12,
            content={
                'title': 'Shipping Information',
                'subtitle': 'Everything you need to know about our shipping options and delivery times',
                'text_align': 'center', 'padding_y': '50px', 'min_height': '280px', 'title_size': '3xl', 'subtitle_size': 'lg',
            },
            is_active=True,
        )

        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Hero Spacer',
            order=order, column_span=12,
            content={'height': 50, 'height_unit': 'px'}, is_active=True,
        )

        # Shipping Options Row
        order += 1; count += 1
        options_row = Element.objects.create(
            page=page, element_type='container', name='Shipping Options',
            order=order, column_span=12,
            content={
                'layout': 'flex', 'direction': 'row', 'gap': '24px', 'wrap': 'wrap',
                'width': '100%', 'max_width': '5xl', 'spacing': 'margin: 0 auto;', 'padding_x': '24px',
                'mobile_stack': True, 'layout_initialized': True,
            },
            is_active=True,
        )

        shipping_options = [
            {'icon': 'fa-box', 'title': 'Standard Shipping', 'time': '5-7 Business Days', 'price': 'From $4.99'},
            {'icon': 'fa-shipping-fast', 'title': 'Express Shipping', 'time': '2-3 Business Days', 'price': 'From $9.99'},
            {'icon': 'fa-gift', 'title': 'Free Shipping', 'time': '5-7 Business Days', 'price': 'Orders over $50'},
        ]

        for idx, opt in enumerate(shipping_options, start=1):
            count += 1
            card = Element.objects.create(
                page=None, parent_element=options_row, element_type='container',
                name=f'{opt["title"]} Card', order=idx, column_span=12, text_align='center',
                content={
                    'layout': 'flex', 'direction': 'column', 'align_items': 'center', 'gap': '8px',
                    'flex': '1', 'min_width': '200px', 'spacing': 'padding: 32px;',
                    'border': '1px solid var(--theme-color-border, #e5e7eb)',
                    'custom_styles': 'border-radius: 12px;', 'layout_initialized': True,
                },
                is_active=True,
            )
            for child_order, (etype, ename, econtent) in enumerate([
                ('icon', f'{opt["title"]} Icon', {'icon': opt['icon'], 'icon_style': 'solid', 'size': 40, 'size_unit': 'px'}),
                ('spacer', f'{opt["title"]} Spacer', {'height': 8, 'height_unit': 'px'}),
                ('heading', f'{opt["title"]} Title', {'text': opt['title'], 'tag': 'h3', 'size': 'lg', 'weight': 'semibold'}),
                ('text', f'{opt["title"]} Time', {'text': opt['time'], 'size': 'base'}),
                ('text', f'{opt["title"]} Price', {'text': opt['price'], 'size': 'lg', 'weight': 'bold'}),
            ], start=1):
                count += 1
                Element.objects.create(
                    page=None, parent_element=card, element_type=etype,
                    name=ename, order=child_order, column_span=12,
                    text_align='center' if etype != 'spacer' else 'left',
                    content=econtent, is_active=True,
                )

        # Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Options FAQ Spacer',
            order=order, column_span=12,
            content={'height': 50, 'height_unit': 'px'}, is_active=True,
        )

        # Shipping FAQ
        order += 1; count += 1
        faq_container = Element.objects.create(
            page=page, element_type='container', name='FAQ Container',
            order=order, column_span=12,
            content={
                'layout': 'flex', 'direction': 'column', 'gap': '24px',
                'max_width': '3xl', 'spacing': 'margin: 0 auto;', 'padding_x': '24px', 'layout_initialized': True,
            },
            is_active=True,
        )

        count += 1
        Element.objects.create(
            page=None, parent_element=faq_container, element_type='faq_accordion', name='Shipping FAQ',
            order=1, column_span=12,
            content={
                'title': 'Shipping Questions', 'subtitle': '', 'style': 'bordered',
                'behavior': 'single', 'animate': True, 'icon_style': 'chevron',
                'icon_position': 'right', 'gap': 'sm', 'enable_schema': True,
                'items': [
                    {'question': 'How long does shipping take?', 'answer': 'Standard shipping takes 5-7 business days and Express shipping takes 2-3 business days. Delivery times start after your order has been processed (typically 1-2 business days).', 'is_open': True},
                    {'question': 'How can I track my order?', 'answer': 'Once your order ships, you will receive an email with tracking information. You can also track your order by logging into your account and viewing your order history.', 'is_open': False},
                    {'question': 'Do you ship internationally?', 'answer': 'Yes, we ship to most countries worldwide. International shipping typically takes 7-14 business days depending on the destination. Customers are responsible for any customs duties or import taxes.', 'is_open': False},
                    {'question': 'What if my package is lost or damaged?', 'answer': "If your order hasn't arrived within the estimated delivery window, contact us with your order number. For damaged packages, contact us within 48 hours of delivery with photos of the packaging and damaged items.", 'is_open': False},
                    {'question': 'Can I change my shipping address after ordering?', 'answer': 'Address changes can be made before your order is dispatched. Contact us as soon as possible at support@example.com with your order number and the corrected address.', 'is_open': False},
                    {'question': 'Are there any shipping restrictions?', 'answer': 'Some products may have shipping restrictions due to size, weight, or destination regulations. If your order cannot be shipped to your location, we will contact you to arrange an alternative or provide a refund.', 'is_open': False},
                ],
            },
            is_active=True,
        )

        # Policy section (same pattern as legal pages)
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='FAQ Policy Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='heading', name='Policy Heading',
            order=order, column_span=12, text_align='center',
            content={'text': 'Full Shipping Policy', 'tag': 'h2', 'size': 'xl', 'weight': 'semibold'},
            is_active=True,
        )

        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='text', name='Policy Last Updated',
            order=order, column_span=12, text_align='center',
            content={'text': 'Last updated: [Date]', 'size': 'sm'}, is_active=True,
        )

        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Policy Heading Spacer',
            order=order, column_span=12,
            content={'height': 24, 'height_unit': 'px'}, is_active=True,
        )

        # Policy Content Container
        order += 1; count += 1
        content_container = Element.objects.create(
            page=page, element_type='container', name='Policy Container',
            order=order, column_span=12,
            content={
                'layout': 'flex', 'direction': 'column', 'gap': '8px',
                'max_width': '3xl', 'spacing': 'margin: 0 auto;', 'padding_x': '24px', 'layout_initialized': True,
            },
            is_active=True,
        )

        # Intro
        count += 1
        Element.objects.create(
            page=None, parent_element=content_container, element_type='text', name='Intro Text',
            order=1, column_span=12,
            content={'text': 'This Shipping Policy applies to orders placed through [Store Name] ("we", "us", "our") on [Website URL].', 'size': 'base', 'line_height': '1.75'},
            is_active=True,
        )

        # Shipping policy sections
        count += self._create_legal_sections(content_container, Element, self._shipping_sections())

        # Bottom Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Bottom Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        return count

    # =========================================================================
    # RETURNS POLICY ELEMENTS (from migration 0028)
    # =========================================================================
    def _seed_returns_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, 'returns-policy')
        if not page:
            return 0

        count = 0
        order = 0

        # Header
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Top Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='heading', name='Page Title',
            order=order, column_span=12, text_align='center',
            content={'text': 'Returns & Refunds', 'tag': 'h1', 'size': '3xl', 'weight': 'bold'},
            is_active=True,
        )

        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='text', name='Last Updated',
            order=order, column_span=12, text_align='center',
            content={'text': 'Last updated: [Date]', 'size': 'sm'}, is_active=True,
        )

        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Header Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        # FAQ Container
        order += 1; count += 1
        faq_container = Element.objects.create(
            page=page, element_type='container', name='FAQ Container',
            order=order, column_span=12,
            content={
                'layout': 'flex', 'direction': 'column', 'gap': '24px',
                'max_width': '3xl', 'spacing': 'margin: 0 auto;', 'padding_x': '24px', 'layout_initialized': True,
            },
            is_active=True,
        )

        count += 1
        Element.objects.create(
            page=None, parent_element=faq_container, element_type='faq_accordion', name='Returns FAQ',
            order=1, column_span=12,
            content={
                'title': 'Common Questions', 'subtitle': '', 'style': 'bordered',
                'behavior': 'single', 'animate': True, 'icon_style': 'chevron',
                'icon_position': 'right', 'gap': 'sm', 'enable_schema': True,
                'items': [
                    {'question': 'What is your return policy?', 'answer': 'We offer a return window of [X] days from delivery. Items must be unused, unworn, and in original condition with packaging and tags. Some items are excluded, including sale/clearance items, gift cards, personalized products, hygiene-sealed items once opened, and perishable goods.', 'is_open': True},
                    {'question': 'How do I return an item?', 'answer': '1. Contact us at support@example.com with your order number and reason for return.\n2. We will confirm eligibility and provide return instructions.\n3. Send the item to the return address provided.\n4. Keep your tracking number and shipping receipt.', 'is_open': False},
                    {'question': 'What if my item arrived damaged or incorrect?', 'answer': 'Contact us within [X] days of delivery with your order number, a description of the issue, and photos/videos where helpful. You may be entitled to a repair, replacement, or refund as required by law.', 'is_open': False},
                    {'question': 'Who pays for return shipping?', 'answer': 'For change-of-mind returns, the customer pays return shipping unless stated otherwise. For faulty, damaged, or incorrect items, we cover return shipping (or reimburse reasonable costs).', 'is_open': False},
                    {'question': 'When will I receive my refund?', 'answer': 'Refunds are processed to your original payment method within [X] business days after we receive and inspect the return. Your bank or payment provider may take additional time to post the refund. Original shipping fees are not refunded unless required by law.', 'is_open': False},
                    {'question': 'Can I exchange an item instead?', 'answer': 'Yes, we offer exchanges for size, color, or variant within [X] days, subject to stock availability. If the requested item is unavailable, we will issue a refund or store credit.', 'is_open': False},
                    {'question': 'Can I cancel my order before it ships?', 'answer': 'Yes, orders can be cancelled before dispatch by contacting support@example.com as soon as possible. If the order has already shipped, it will be treated as a return subject to this policy.', 'is_open': False},
                ],
            },
            is_active=True,
        )

        # Policy section
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='FAQ Policy Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='heading', name='Policy Heading',
            order=order, column_span=12, text_align='center',
            content={'text': 'Full Returns & Refunds Policy', 'tag': 'h2', 'size': 'xl', 'weight': 'semibold'},
            is_active=True,
        )

        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Policy Heading Spacer',
            order=order, column_span=12,
            content={'height': 24, 'height_unit': 'px'}, is_active=True,
        )

        # Policy Content Container
        order += 1; count += 1
        content_container = Element.objects.create(
            page=page, element_type='container', name='Policy Container',
            order=order, column_span=12,
            content={
                'layout': 'flex', 'direction': 'column', 'gap': '8px',
                'max_width': '3xl', 'spacing': 'margin: 0 auto;', 'padding_x': '24px', 'layout_initialized': True,
            },
            is_active=True,
        )

        # Intro
        count += 1
        Element.objects.create(
            page=None, parent_element=content_container, element_type='text', name='Intro Text',
            order=1, column_span=12,
            content={
                'text': 'This Returns & Refunds Policy applies to purchases made through [Store Name] ("we", "us", "our") via [Website URL]. It explains return eligibility, how to request a return, refund timelines, and related terms.',
                'size': 'base', 'line_height': '1.75',
            },
            is_active=True,
        )

        count += self._create_legal_sections(content_container, Element, self._returns_sections())

        # Bottom Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Bottom Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        return count

    # =========================================================================
    # HOME PAGE ELEMENTS (from migration 0029)
    # =========================================================================
    def _seed_home_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, 'home')
        if not page:
            return 0

        count = 0
        order = 0

        # Hero
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='hero', name='Main Hero',
            order=order, column_span=12,
            content={
                'title': 'Welcome to Our Store',
                'subtitle': 'Discover amazing products at great prices. Quality you can trust, service you deserve.',
                'text_align': 'center', 'min_height': '500px', 'padding_y': '100px',
                'button_text': 'Shop Now', 'button_url': '/category/', 'button_style': 'primary', 'button_size': 'xl',
            },
            is_active=True,
        )

        # Hero Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Hero Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        # Category Showcase
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='category_showcase', name='Category Showcase',
            order=order, column_span=12,
            content={
                'title': 'Shop by Category', 'style': 'cards', 'columns': '4',
                'source_type': 'top_level', 'max_categories': '6',
                'show_image': True, 'image_ratio': '1/1', 'show_description': True,
                'show_product_count': True, 'data_source': 'dynamic',
            },
            is_active=True,
        )

        # Featured Products Grid
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='product_grid', name='Featured Products Grid',
            order=order, column_span=12,
            content={
                'title': 'Our Products', 'subtitle': 'Browse our complete collection of products',
                'layout': 'grid', 'source_type': 'all', 'sort_order': 'bestselling',
                'columns': '2', 'gap': '24px', 'gap_size': 'md', 'spacing': 'tight',
                'max_products': '12', 'products_per_page': '12',
                'show_price': True, 'show_rating': True, 'show_badges': True,
                'show_add_to_cart': True, 'show_quick_view': True, 'show_quick_actions': True,
                'show_filters': True, 'show_sort': True, 'show_pagination': True,
                'hide_out_of_stock': True, 'button_text': 'Add to Cart',
                'view_all_link': '/products/', 'view_all_text': 'View All Products',
                'data_source': 'dynamic',
            },
            is_active=True,
        )

        # Newsletter Top Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Newsletter Top Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        # Newsletter
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='newsletter', name='Newsletter Signup',
            order=order, column_span=12,
            content={
                'title': 'Stay Updated',
                'description': 'Subscribe to our newsletter for exclusive offers and the latest updates.',
                'button_text': 'Subscribe', 'placeholder': 'Enter your email', 'padding_y': '60px',
            },
            is_active=True,
        )

        # Bottom Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Bottom Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        return count

    # =========================================================================
    # MAINTENANCE PAGE ELEMENTS (from migration 0033)
    # =========================================================================
    def _seed_maintenance_elements(self, Page, Element):
        page = self._page_needs_seeding(Page, Element, 'maintenance')
        if not page:
            return 0

        Element.objects.create(
            page=page, element_type='hero', name='Maintenance Hero',
            order=1, column_span=12,
            content={
                'title': "We'll Be Right Back",
                'subtitle': "We're performing scheduled maintenance to improve your experience. Please check back soon.",
                'title_size': '5xl', 'subtitle_size': 'xl',
                'title_color': '#ffffff', 'subtitle_color': '#ffffff',
                'text_align': 'center', 'min_height': 'screen', 'vertical_align': 'center',
                'background': 'linear-gradient(45deg, #ff9a56 0%, #ff6a88 100%)',
                'background_type': 'gradient',
                'background_data': {
                    'normal': {
                        'type': 'gradient', 'color': '#ffffff',
                        'gradient': 'linear-gradient(45deg, #ff9a56 0%, #ff6a88 100%)',
                        'image': {'url': '', 'size': 'cover', 'repeat': 'no-repeat', 'position': 'center center', 'attachment': 'scroll'},
                        'video': {'url': '', 'loop': True, 'muted': True, 'poster': '', 'autoplay': True},
                        'overlay': {'color': '#000000', 'enabled': False, 'opacity': 0.5},
                    },
                    'hover': {
                        'type': 'color', 'color': '#f0f0f0',
                        'gradient': 'linear-gradient(90deg, #8b5cf6 0%, #3b82f6 100%)',
                        'image': {'url': '', 'size': 'cover', 'repeat': 'no-repeat', 'position': 'center center', 'attachment': 'scroll'},
                        'video': {'url': '', 'loop': True, 'muted': True, 'poster': '', 'autoplay': True},
                        'overlay': {'color': '#000000', 'enabled': False, 'opacity': 0.5},
                        'enabled': False,
                    },
                },
                'overlay_opacity': 0,
                'padding_top': '8', 'padding_bottom': '8', 'padding_y': '0px', 'opacity': '1',
                'show_cta': False, 'show_scroll_indicator': False,
                'button_url': '#', 'button_style': 'solid', 'button_size': 'md', 'button_target': '_self',
                'secondary_button_url': '#', 'secondary_button_style': 'outline',
                'secondary_button_size': 'md', 'secondary_button_target': '_self',
                'animation_type': '', 'animation_duration': '0.5s', 'animation_delay': '0s',
                'animation_timing': 'ease-out', 'animation_repeat': '1',
                'hover_animation_type': '', 'hover_animation_duration': '0.3s', 'hover_animation_timing': 'ease-out',
            },
            is_active=True,
        )

        return 1

    # =========================================================================
    # HELPER: Legal page pattern (Privacy, Terms, Cookie)
    # =========================================================================
    def _seed_legal_page(self, page, Element, title, sections):
        """Shared pattern for Privacy Policy, Terms of Use, and Cookie Policy pages."""
        count = 0
        order = 0

        # Top Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Top Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        # Page Title
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='heading', name='Page Title',
            order=order, column_span=12, text_align='center',
            content={'text': title, 'tag': 'h1', 'size': '3xl', 'weight': 'bold'},
            is_active=True,
        )

        # Last Updated
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='text', name='Last Updated',
            order=order, column_span=12, text_align='center',
            content={'text': 'Last updated: [Date]', 'size': 'sm'},
            is_active=True,
        )

        # Header Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Header Spacer',
            order=order, column_span=12,
            content={'height': 40, 'height_unit': 'px'}, is_active=True,
        )

        # Content Container
        order += 1; count += 1
        content_container = Element.objects.create(
            page=page, element_type='container', name='Content Container',
            order=order, column_span=12,
            content={
                'layout': 'flex', 'direction': 'column', 'gap': '8px',
                'max_width': '3xl', 'spacing': 'margin: 0 auto;', 'padding_x': '24px', 'layout_initialized': True,
            },
            is_active=True,
        )

        # Intro Text
        count += 1
        intro_text = sections.pop(0)
        Element.objects.create(
            page=None, parent_element=content_container, element_type='text', name='Intro Text',
            order=1, column_span=12,
            content={'text': intro_text, 'size': 'base', 'line_height': '1.75', 'preserve_whitespace': True},
            is_active=True,
        )

        # Sections
        count += self._create_legal_sections(content_container, Element, sections)

        # Bottom Spacer
        order += 1; count += 1
        Element.objects.create(
            page=page, element_type='spacer', name='Bottom Spacer',
            order=order, column_span=12,
            content={'height': 60, 'height_unit': 'px'}, is_active=True,
        )

        return count

    def _create_legal_sections(self, container, Element, sections):
        """Create heading/spacer/text triples for legal page sections."""
        count = 0
        # Start child_order after intro text (order=1)
        child_order = 1
        for section in sections:
            child_order += 1; count += 1
            Element.objects.create(
                page=None, parent_element=container, element_type='heading',
                name=section['title'], order=child_order, column_span=12,
                content={'text': section['title'], 'tag': 'h3', 'size': 'lg', 'weight': 'semibold'},
                is_active=True,
            )
            child_order += 1; count += 1
            Element.objects.create(
                page=None, parent_element=container, element_type='spacer',
                name=f'{section["title"]} Spacer', order=child_order, column_span=12,
                content={'height': 8, 'height_unit': 'px'}, is_active=True,
            )
            child_order += 1; count += 1
            Element.objects.create(
                page=None, parent_element=container, element_type='text',
                name=f'{section["title"]} Content', order=child_order, column_span=12,
                content={'text': section['content'], 'size': 'base', 'line_height': '1.75', 'preserve_whitespace': True},
                is_active=True,
            )
        return count

    # =========================================================================
    # SECTION DATA
    # =========================================================================
    def _privacy_sections(self):
        """Return privacy policy sections. First item is intro text."""
        return [
            # Intro text (will be popped in _seed_legal_page)
            '[Store Name] (\u201cwe\u201d, \u201cus\u201d, \u201cour\u201d) is committed to protecting your privacy. This Privacy Policy explains how we collect, use, share, and protect your personal information when you visit or make a purchase from [Website URL] (the \u201cSite\u201d).\n\nBy using the Site, you agree to the collection and use of information in accordance with this policy. This policy should be read together with our Terms of Use and Cookie Policy.',
            {'title': '1) Information we collect', 'content': 'We collect information you provide directly to us, as well as information collected automatically when you use the Site.\n\nInformation you provide:\n\n\u2022 Account details (name, email address, password)\n\u2022 Shipping and billing addresses\n\u2022 Phone number\n\u2022 Payment information (processed securely by our payment providers \u2014 we do not store full card details)\n\u2022 Order history and purchase preferences\n\u2022 Product reviews, ratings, and comments\n\u2022 Messages sent through our contact forms or customer support\n\nInformation collected automatically:\n\n\u2022 IP address and approximate location\n\u2022 Browser type and version\n\u2022 Device type and operating system\n\u2022 Pages visited, time spent, and navigation patterns\n\u2022 Referring website or link\n\u2022 Cookies and similar tracking technologies (see our Cookie Policy for details)'},
            {'title': '2) How we use your information', 'content': 'We use the information we collect to:\n\n\u2022 Process and fulfill your orders, including shipping and payment\n\u2022 Create and manage your account\n\u2022 Send order confirmations, shipping updates, and delivery notifications\n\u2022 Respond to your questions, requests, and provide customer support\n\u2022 Send promotional communications and offers (only with your consent)\n\u2022 Personalize your shopping experience and show relevant products\n\u2022 Improve our Site, products, and services\n\u2022 Detect, prevent, and address fraud or security issues\n\u2022 Comply with legal obligations and enforce our Terms of Use\n\nWe will never sell your personal information to third parties for their marketing purposes.'},
            {'title': '3) Legal basis for processing', 'content': 'We process your personal information based on the following legal grounds:\n\n\u2022 Contract performance \u2014 To fulfill orders and provide services you have requested\n\u2022 Consent \u2014 For marketing communications and non-essential cookies (you can withdraw consent at any time)\n\u2022 Legitimate interests \u2014 To improve our services, prevent fraud, and ensure security\n\u2022 Legal obligation \u2014 To comply with applicable laws, regulations, and legal processes'},
            {'title': '4) Information sharing', 'content': 'We may share your information with the following categories of third parties:\n\n\u2022 Payment providers \u2014 To process transactions securely\n\u2022 Shipping carriers \u2014 To deliver your orders\n\u2022 Email service providers \u2014 To send transactional and promotional communications\n\u2022 Analytics providers \u2014 To help us understand Site usage and improve performance\n\u2022 Customer support tools \u2014 To manage and respond to your inquiries\n\nWe may also share information when required by law, to protect our rights, or in connection with a business transfer (e.g., merger or acquisition).\n\nAll third-party service providers are contractually obligated to handle your data securely and only for the purposes we specify.'},
            {'title': '5) Data security', 'content': 'We take the security of your personal information seriously and implement appropriate measures to protect it, including:\n\n\u2022 SSL/TLS encryption for all data transmitted between your browser and our Site\n\u2022 Secure payment processing through PCI DSS-compliant providers\n\u2022 Hashed and salted password storage\n\u2022 Regular security reviews and software updates\n\u2022 Access controls limiting who can view personal data\n\nWhile we strive to protect your information, no method of transmission over the Internet or electronic storage is completely secure. We cannot guarantee absolute security, but we are committed to protecting your data to the best of our ability.'},
            {'title': '6) Data retention', 'content': 'We retain your personal information for as long as necessary to:\n\n\u2022 Maintain your account and provide our services\n\u2022 Comply with legal, accounting, and reporting obligations\n\u2022 Resolve disputes and enforce our agreements\n\nWhen your data is no longer needed, we will securely delete or anonymize it. Order records may be retained for a period required by tax and accounting regulations.'},
            {'title': '7) Your rights', 'content': 'Depending on your location and applicable laws, you may have the following rights regarding your personal information:\n\n\u2022 Access \u2014 Request a copy of the personal data we hold about you\n\u2022 Correction \u2014 Ask us to update or correct inaccurate information\n\u2022 Deletion \u2014 Request that we delete your personal data\n\u2022 Portability \u2014 Receive your data in a structured, commonly used format\n\u2022 Restriction \u2014 Ask us to limit how we use your data\n\u2022 Objection \u2014 Object to processing based on legitimate interests\n\u2022 Withdraw consent \u2014 Opt out of marketing communications at any time\n\nTo exercise any of these rights, please contact us using the details in the Contact section below. We will respond within 30 days.'},
            {'title': '8) Cookies and tracking', 'content': 'We use cookies and similar technologies to operate the Site, remember your preferences, and analyze usage. You can manage your cookie preferences through your browser settings or our cookie preference center.\n\nFor full details on the cookies we use and how to control them, please see our Cookie Policy.'},
            {'title': '9) Marketing communications', 'content': 'With your consent, we may send you promotional emails about products, offers, and news. You can opt out at any time by:\n\n\u2022 Clicking the \u201cunsubscribe\u201d link in any marketing email\n\u2022 Updating your communication preferences in your account settings\n\u2022 Contacting us directly\n\nOpting out of marketing communications will not affect transactional messages related to your orders.'},
            {'title': '10) Children\u2019s privacy', 'content': 'Our Site is not intended for children under the age of 16 (or such other age as required by applicable law). We do not knowingly collect personal information from children. If you believe a child has provided us with personal data, please contact us and we will take steps to delete that information.'},
            {'title': '11) International data transfers', 'content': 'Your information may be transferred to and processed in countries other than your own. These countries may have data protection laws that differ from those in your jurisdiction.\n\nWhere we transfer data internationally, we take steps to ensure appropriate safeguards are in place to protect your information in accordance with applicable data protection laws.'},
            {'title': '12) Third-party links', 'content': 'Our Site may contain links to third-party websites, services, or social media platforms. We are not responsible for the privacy practices or content of these external sites.\n\nWe encourage you to review the privacy policies of any third-party sites you visit before providing any personal information.'},
            {'title': '13) Changes to this Privacy Policy', 'content': 'We may update this Privacy Policy from time to time to reflect changes in our practices, legal requirements, or for other reasons. The \u201cLast updated\u201d date at the top of this page indicates when changes were last made.\n\nWe encourage you to review this page periodically. Continued use of the Site after changes are posted constitutes your acceptance of the updated policy.'},
            {'title': '14) Contact', 'content': 'If you have questions about this Privacy Policy, want to exercise your rights, or have concerns about how we handle your data, please contact us:\n\n[Store Name]\nEmail: support@example.com\nAddress: [Business Address]\n\nWe will respond to your inquiry within 30 days.'},
        ]

    def _terms_sections(self):
        """Return terms of use sections. First item is intro text."""
        return [
            'Welcome to [Store Name]. These Terms of Use (\u201cTerms\u201d) govern your access to and use of [Website URL] (the \u201cSite\u201d), including any purchases you make. By using the Site, you agree to be bound by these Terms and our Privacy Policy.\n\nIf you do not agree to these Terms, please do not use the Site.',
            {'title': '1) General conditions', 'content': 'We reserve the right to refuse service to anyone for any reason at any time. We may modify or discontinue the Site (or any part of it) at any time without notice.\n\nThese Terms apply to all users of the Site, including browsers, customers, and merchants who register for an account.\n\nYou agree not to reproduce, duplicate, copy, sell, or exploit any portion of the Site without our express written permission.'},
            {'title': '2) Account registration', 'content': 'To access certain features, you may need to create an account. When you do, you agree to:\n\n\u2022 Provide accurate, current, and complete information\n\u2022 Keep your login credentials confidential\n\u2022 Accept responsibility for all activity under your account\n\u2022 Notify us immediately if you suspect unauthorized access\n\nWe reserve the right to suspend or terminate accounts that violate these Terms or that we believe are being used fraudulently.'},
            {'title': '3) Products and pricing', 'content': 'We make every effort to display accurate product descriptions, images, and pricing. However, we do not guarantee that all information is error-free.\n\nWe reserve the right to:\n\n\u2022 Correct errors in pricing or product information at any time\n\u2022 Refuse or cancel orders affected by pricing errors\n\u2022 Limit quantities available for purchase\n\u2022 Discontinue any product without prior notice\n\nPrices are displayed in the currency indicated on the Site and may be subject to applicable taxes and shipping charges.'},
            {'title': '4) Orders and payment', 'content': 'By placing an order, you are making an offer to purchase. We reserve the right to accept or decline your order for any reason, including stock availability, errors in product or pricing information, or suspected fraud.\n\nPayment must be made at the time of purchase using one of our accepted payment methods. You agree that the payment information you provide is accurate and that you are authorized to use the payment method.\n\nOnce an order is confirmed, you will receive an email acknowledgement. This confirmation does not constitute acceptance of your order \u2014 acceptance occurs when the item is dispatched.'},
            {'title': '5) Shipping and delivery', 'content': 'Delivery times and shipping costs are estimates and may vary depending on your location and the shipping method selected. We are not responsible for delays caused by carriers, customs, or other circumstances beyond our control.\n\nRisk of loss and title for items pass to you upon delivery to the carrier. Please refer to our Shipping Policy for full details.'},
            {'title': '6) Returns and refunds', 'content': 'We want you to be satisfied with your purchase. If you are not, you may be eligible for a return or exchange subject to the conditions outlined in our Returns & Refunds Policy.\n\nCertain items (e.g., personalized goods, perishable items, digital downloads) may not be eligible for return. Please review our Returns & Refunds Policy before making a purchase.'},
            {'title': '7) Prohibited uses', 'content': 'You agree not to use the Site:\n\n\u2022 For any unlawful purpose or to solicit others to perform unlawful acts\n\u2022 To violate any international, national, or local regulations or laws\n\u2022 To infringe upon or violate our intellectual property rights or the rights of others\n\u2022 To harass, abuse, discriminate, or intimidate others\n\u2022 To submit false or misleading information\n\u2022 To upload or transmit viruses, malware, or any other malicious code\n\u2022 To interfere with or circumvent the security features of the Site\n\u2022 To scrape, data-mine, or use automated tools to access the Site without permission'},
            {'title': '8) Intellectual property', 'content': 'All content on this Site \u2014 including text, graphics, logos, images, product descriptions, and software \u2014 is the property of [Store Name] or its licensors and is protected by copyright, trademark, and other intellectual property laws.\n\nYou may not reproduce, distribute, modify, create derivative works from, or publicly display any content from this Site without our prior written consent.'},
            {'title': '9) User content', 'content': 'By submitting content to the Site (such as product reviews, comments, or other feedback), you grant us a non-exclusive, royalty-free, perpetual, and worldwide license to use, reproduce, modify, and display that content in connection with operating the Site.\n\nYou are responsible for the content you submit and agree that it will not:\n\n\u2022 Violate any third-party rights\n\u2022 Contain defamatory, obscene, or offensive material\n\u2022 Contain spam, advertising, or solicitations\n\u2022 Contain false or misleading statements'},
            {'title': '10) Disclaimer of warranties', 'content': 'The Site and all products and services are provided on an \u201cas is\u201d and \u201cas available\u201d basis without warranties of any kind, whether express or implied.\n\nWe do not warrant that:\n\n\u2022 The Site will be uninterrupted, secure, or error-free\n\u2022 Results obtained from the Site will be accurate or reliable\n\u2022 The quality of any products or services will meet your expectations\n\nThis disclaimer does not affect your statutory rights as a consumer.'},
            {'title': '11) Limitation of liability', 'content': 'To the fullest extent permitted by law, [Store Name] shall not be liable for any indirect, incidental, special, consequential, or punitive damages arising from:\n\n\u2022 Your use of or inability to use the Site\n\u2022 Any products purchased through the Site\n\u2022 Unauthorized access to or alteration of your data\n\u2022 Any interruption or cessation of service\n\u2022 Any bugs, viruses, or other harmful code transmitted through the Site\n\nOur total liability to you for any claim arising from or related to these Terms shall not exceed the amount you paid for the relevant product or service.'},
            {'title': '12) Indemnification', 'content': 'You agree to indemnify, defend, and hold harmless [Store Name], its officers, directors, employees, and agents from any claims, damages, losses, liabilities, or expenses (including legal fees) arising from your use of the Site, your violation of these Terms, or your violation of any rights of a third party.'},
            {'title': '13) Third-party links', 'content': 'The Site may contain links to third-party websites or services that are not owned or controlled by us. We have no control over and assume no responsibility for the content, privacy policies, or practices of any third-party sites.\n\nWe encourage you to review the terms and privacy policies of any third-party sites you visit.'},
            {'title': '14) Governing law', 'content': 'These Terms shall be governed by and construed in accordance with the laws of [Jurisdiction]. Any disputes arising from these Terms or your use of the Site shall be subject to the exclusive jurisdiction of the courts in [Jurisdiction].\n\nIf any provision of these Terms is found to be unenforceable, the remaining provisions shall continue in full force and effect.'},
            {'title': '15) Changes to these Terms', 'content': 'We may update these Terms from time to time to reflect changes in our practices, legal requirements, or for other reasons. The \u201cLast updated\u201d date at the top of this page indicates when changes were last made.\n\nContinued use of the Site after changes are posted constitutes your acceptance of the revised Terms. We encourage you to review this page periodically.'},
            {'title': '16) Contact', 'content': 'If you have questions about these Terms of Use, contact:\n[Store Name]\nEmail: support@example.com\nAddress: [Business Address]'},
        ]

    def _cookie_sections(self):
        """Return cookie policy sections. First item is intro text."""
        return [
            'This Cookie Policy explains how [Store Name] (\u201cwe\u201d, \u201cus\u201d, \u201cour\u201d) uses cookies and similar technologies on [Website URL] (the \u201cSite\u201d). It describes what these technologies are, why we use them, and how you can manage your preferences.\n\nThis policy should be read together with our Privacy Policy.',
            {'title': '1) What are cookies?', 'content': 'Cookies are small text files placed on your device when you visit a website. They help websites function, remember preferences, and provide reporting information.\n\nWe may also use similar technologies such as:\n\n\u2022 Pixels / tags (small code snippets that measure engagement)\n\u2022 Local storage (browser storage for preferences)\n\u2022 SDKs (tools used in apps to provide features and analytics)\n\nFor simplicity, we refer to all these as \u201ccookies\u201d.'},
            {'title': '2) Why we use cookies', 'content': 'We use cookies to:\n\n\u2022 make the Site work properly (e.g., login, cart, checkout)\n\u2022 remember your preferences (e.g., language, currency, region)\n\u2022 improve performance and reliability\n\u2022 understand how the Site is used (analytics)\n\u2022 personalize content and marketing (where enabled)\n\u2022 prevent fraud and protect accounts'},
            {'title': '3) Types of cookies we use', 'content': 'Cookies used on the Site fall into the following categories:\n\nA) Strictly necessary cookies\nThese are required for core functionality and cannot be disabled.\n\u2022 Session management (login, shopping cart, checkout)\n\u2022 Security and fraud prevention\n\nB) Preferences / functional cookies\nThese remember choices you make to improve your experience.\n\u2022 Language and currency selection\n\u2022 Region preferences\n\nC) Analytics / performance cookies\nThese help us understand site usage and improve performance.\n\u2022 Page views, clicks, session duration\n\u2022 Error reporting and performance diagnostics\n\nD) Marketing / advertising cookies\nThese may be used to show relevant ads and measure marketing effectiveness.\n\u2022 Referral and affiliate tracking\n\u2022 Conversion tracking\n\nE) Third-party cookies\nSome cookies may be set by third-party services integrated into this Site (e.g., payment providers, analytics tools, or embedded content). These services may collect information directly from your device in accordance with their own privacy policies.'},
            {'title': '4) Cookies we use', 'content': 'The following cookies are used on this Site:\n\nStrictly Necessary:\n\u2022 sessionid \u2014 Manages your browsing session (login, cart) \u2014 30 days\n\u2022 csrftoken \u2014 Security cookie that helps protect your data \u2014 Browser session\n\nPreferences:\n\u2022 lang \u2014 Stores your language preference \u2014 1 year\n\u2022 selected_currency \u2014 Stores your currency preference \u2014 1 year\n\nMarketing:\n\u2022 ref_token \u2014 Tracks referral attribution \u2014 30 days\n\nAdditional third-party cookies may be set by payment providers, analytics services, or social login providers integrated into this Site. These are governed by the respective third-party privacy policies.'},
            {'title': '5) Consent and cookie controls', 'content': 'Where required by law, we will ask for your consent before using non-essential cookies (e.g., analytics and marketing).\n\nYou can manage cookies by:\n\n\u2022 Using our cookie banner / preference center (if available)\n\u2022 Adjusting your browser settings to block or delete cookies\n\u2022 Using device-level controls (for mobile apps, if applicable)\n\nBlocking some cookies may impact Site functionality (e.g., cart or checkout may not work correctly).'},
            {'title': '6) How to control cookies in browsers', 'content': 'Most browsers allow you to:\n\n\u2022 View which cookies are stored\n\u2022 Delete cookies\n\u2022 Block all or selected cookies\n\u2022 Block third-party cookies\n\nBrowser instructions vary; refer to your browser\'s help section for the latest steps.'},
            {'title': '7) Do Not Track signals', 'content': 'Some browsers offer \u201cDo Not Track\u201d (DNT) signals. Because there is no consistent industry standard for DNT, our response to DNT signals may vary. Please refer to our Privacy Policy for more details on how we handle tracking preferences.'},
            {'title': '8) Updates to this Cookie Policy', 'content': 'We may update this policy from time to time to reflect changes in our practices or for legal/regulatory reasons. The \u201cLast updated\u201d date at the top of this page indicates when changes were last made.'},
            {'title': '9) Contact', 'content': 'If you have questions about this Cookie Policy, contact:\n[Store Name]\nEmail: support@example.com\nAddress: [Business Address]'},
        ]

    def _shipping_sections(self):
        """Return shipping policy sections (no intro - handled separately)."""
        return [
            {'title': '1) Order processing times', 'content': 'Orders are typically processed within [X\u2013Y] business days (excluding weekends and public holidays) after payment is confirmed.\n\nProcessing may take longer during:\n\n\u2022 peak seasons and promotional periods\n\u2022 product launches or backorders\n\u2022 adverse weather or carrier disruptions\n\nIf there is a significant delay, we will contact you at the email/phone provided at checkout.'},
            {'title': '2) Shipping destinations', 'content': 'We ship to: [Countries/Regions]\n\nWe do not ship to: [Excluded Countries/Regions]\n\nIf your location is not listed, contact support@example.com.'},
            {'title': '3) Shipping rates and delivery estimates', 'content': 'Shipping fees are calculated at checkout based on:\n\n\u2022 destination\n\u2022 parcel weight/size\n\u2022 selected shipping method\n\u2022 applicable promotions\n\nEstimated delivery times (after dispatch):\n\n\u2022 Standard: [X\u2013Y] business days\n\u2022 Express: [X\u2013Y] business days\n\u2022 Same-day / Next-day (if offered): [Details, cutoff times]\n\nNotes:\n\n\u2022 Delivery estimates are not guarantees.\n\u2022 Remote areas may require additional time.\n\u2022 Carrier delays may occur outside our control.'},
            {'title': '4) Free shipping (if offered)', 'content': 'Free shipping eligibility: [Minimum spend / Regions / Methods]\nFree shipping method used: [Standard / Economy / Other]\nConditions/exclusions: [Sale items excluded, bulky items excluded, etc.]'},
            {'title': '5) Order tracking', 'content': 'If tracking is available for your shipping method, you will receive a tracking link via email once your order ships.\n\nTracking updates may take 24\u201348 hours to appear after dispatch.'},
            {'title': '6) Delivery address and failed delivery', 'content': 'Customers are responsible for providing accurate shipping details.\n\nIf a package is returned due to:\n\n\u2022 incorrect/incomplete address\n\u2022 failure to collect from a pickup point\n\u2022 refusal of delivery\n\nwe will contact you to arrange reshipment. Reshipping fees: [Customer pays / We pay / Case-by-case].'},
            {'title': '7) Duties, taxes, and customs (international orders)', 'content': 'For international shipments, your order may be subject to:\n\n\u2022 import duties\n\u2022 taxes (VAT/GST)\n\u2022 customs fees or brokerage charges\n\nThese charges are [paid by the customer / included at checkout if available] and are determined by your local customs authority. We do not control these fees and cannot predict the amount.\n\nCustoms clearance may cause delays.'},
            {'title': '8) Shipping restrictions', 'content': 'We may be unable to ship certain items to some locations due to:\n\n\u2022 carrier restrictions\n\u2022 local regulations\n\u2022 hazardous materials rules\n\nRestricted items (if any): [List]\n\nIf your order contains restricted items, we will contact you to adjust the order or issue a refund for affected items.'},
            {'title': '9) Lost, delayed, or damaged packages', 'content': "Delayed shipments: If your order hasn't arrived within [X] days of the estimated delivery window, contact support@example.com with your order number.\n\nLost packages: A shipment may be considered lost after [X] days with no tracking updates (carrier-dependent). We will work with the carrier to investigate and, where appropriate, offer a replacement or refund.\n\nDamaged in transit: If your order arrives damaged:\n\n\u2022 contact us within [48 hours / X days] of delivery\n\u2022 include photos of the packaging and the damaged items\n\nWe may require carrier inspection or additional documentation."},
            {'title': '10) Split shipments', 'content': 'If your order includes multiple items, we may ship items separately to ensure faster delivery or due to stock availability. You will receive separate tracking details where applicable.'},
            {'title': '11) Pre-orders and backorders', 'content': 'For pre-ordered or backordered items:\n\n\u2022 expected dispatch date: [Date/Window]\n\u2022 if your order includes in-stock items, we will [ship together / ship separately]'},
            {'title': '12) Pickup / local delivery (if offered)', 'content': 'Local pickup: [Location], [hours], [requirements]\nLocal delivery: [Eligible areas], [fees], [cutoff times]'},
            {'title': '13) Contact', 'content': 'For shipping questions, contact:\n[Store Name]\nEmail: support@example.com\nAddress: [Business Address]\nPhone (optional): [Phone]'},
        ]

    def _returns_sections(self):
        """Return returns & refunds policy sections (no intro - handled separately)."""
        return [
            {'title': '1) Change of mind returns', 'content': 'If you change your mind, you may request a return within [X] days of delivery, provided that:\n\n\u2022 the item is unused, unworn, and in original condition\n\u2022 it includes original packaging, tags, manuals, and accessories (if applicable)\n\u2022 you can provide proof of purchase (order number / receipt)\n\nNot eligible for change-of-mind returns:\n\n\u2022 sale/clearance items (unless required by law)\n\u2022 gift cards / digital products\n\u2022 personalized or made-to-order items\n\u2022 items sealed for hygiene reasons once opened (e.g., cosmetics, underwear)\n\u2022 perishable goods'},
            {'title': '2) Faulty, damaged, or incorrect items', 'content': 'If your item is faulty, damaged, or not what you ordered, contact us within [X] days of delivery with:\n\n\u2022 your order number\n\u2022 a description of the issue\n\u2022 photos/videos where helpful\n\nWhere required by law, you may be entitled to a repair, replacement, or refund.'},
            {'title': '3) Return window', 'content': 'Returns must be requested within [X] days of delivery and shipped back within [X] days after approval.'},
            {'title': '4) How to request a return', 'content': '1. Contact us at support@example.com with your order number and reason for return.\n2. We will confirm eligibility and provide return instructions and (if applicable) a return authorization.\n3. Send the item to: [Return Address]\n4. Keep your tracking number and shipping receipt.'},
            {'title': '5) Return shipping costs', 'content': '\u2022 Change of mind: customer pays return shipping unless stated otherwise.\n\u2022 Faulty/damaged/incorrect: we cover return shipping (or reimburse reasonable costs) where applicable.\n\u2022 If you choose a shipping method without tracking/insurance, returns are sent at your risk.'},
            {'title': '6) Condition checks and restocking fees', 'content': 'We inspect all returns. If the item is not returned in original condition, we may:\n\n\u2022 refuse the return, or\n\u2022 issue a partial refund reflecting loss in value'},
            {'title': '7) Refunds', 'content': 'If approved, refunds are processed to the original payment method:\n\n\u2022 Processing time: [X] business days after we receive and inspect the return\n\u2022 Banks/payment providers may take additional time to post the refund\n\nOriginal shipping fees are not refunded unless required by law.'},
            {'title': '8) Exchanges', 'content': 'We offer exchanges for size/color/variant within [X] days, subject to stock availability.\n\nIf the requested exchange item is unavailable, we will issue a refund or store credit (as selected).'},
            {'title': '9) Cancellations (before dispatch)', 'content': 'Orders can be cancelled before dispatch by contacting support@example.com as soon as possible. If the order has already shipped, it will be treated as a return (subject to this policy).'},
            {'title': '10) Gifts', 'content': 'If the item was marked as a gift:\n\n\u2022 refunds may be issued as store credit to the gift recipient, or\n\u2022 refunded to the original purchaser (depending on circumstances and local law)'},
            {'title': '11) Digital products and services', 'content': 'Unless required by law, digital products, downloads, and online services are non-refundable once delivered or accessed.'},
            {'title': '12) Local law and consumer rights', 'content': 'This policy is intended to comply with applicable consumer protection laws. Where local laws provide mandatory rights (e.g., for faulty goods), those rights are not limited by this policy.'},
            {'title': '13) Contact', 'content': 'Email: support@example.com\nAddress: [Business Address]\nPhone (optional): [Phone]'},
        ]
