# -*- coding: utf-8 -*-
"""
Search Engine Setup Wizard Views
Multi-step wizard for creating and configuring search engines
"""
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils.text import slugify

from search.models import SearchEngine


# Content type choices for the wizard
CONTENT_TYPE_CHOICES = [
    ('product', _('Products'), 'fas fa-box', _('Include products in search results')),
    ('category', _('Categories'), 'fas fa-folder', _('Include categories in search results')),
    ('brand', _('Brands'), 'fas fa-tag', _('Include brands in search results')),
    ('blog_post', _('Blog Posts'), 'fas fa-newspaper', _('Include blog posts in search results')),
]

# Weight fields that can be customized
WEIGHT_FIELDS = [
    ('weight_name', _('Name Weight'), 1.5, _('Relevance weight for product/item names')),
    ('weight_sku', _('SKU Weight'), 1.2, _('Relevance weight for SKUs')),
    ('weight_description', _('Description Weight'), 0.8, _('Relevance weight for descriptions')),
    ('weight_attributes', _('Attributes Weight'), 0.7, _('Relevance weight for product attributes')),
    ('weight_categories', _('Categories Weight'), 0.8, _('Relevance weight for category names')),
    ('weight_brands', _('Brands Weight'), 0.7, _('Relevance weight for brand names')),
]


class WizardSessionMixin:
    """Mixin for managing wizard session data."""

    SESSION_KEY = 'search_engine_wizard_data'

    def get_wizard_data(self):
        """Get wizard data from session."""
        return self.request.session.get(self.SESSION_KEY, {})

    def set_wizard_data(self, data):
        """Set wizard data in session."""
        self.request.session[self.SESSION_KEY] = data
        self.request.session.modified = True

    def update_wizard_data(self, **kwargs):
        """Update wizard data with new values."""
        data = self.get_wizard_data()
        data.update(kwargs)
        self.set_wizard_data(data)

    def clear_wizard_data(self):
        """Clear wizard data from session."""
        if self.SESSION_KEY in self.request.session:
            del self.request.session[self.SESSION_KEY]


@method_decorator(staff_member_required, name='dispatch')
class EngineWizardStep1View(WizardSessionMixin, TemplateView):
    """
    Step 1: Basic Information
    Engine name, slug, and description
    """
    template_name = 'admin/search/wizard/step1_basic.html'

    def get(self, request, *args, **kwargs):
        # Clear wizard data when starting fresh
        self.clear_wizard_data()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 1
        context['total_steps'] = 4
        context['wizard_data'] = self.get_wizard_data()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '').strip()
        slug = request.POST.get('slug', '').strip()
        is_active = request.POST.get('is_active') == 'on'

        # Validation
        if not name:
            messages.error(request, _('Engine name is required.'))
            return self.get(request, *args, **kwargs)

        # Auto-generate slug if not provided
        if not slug:
            slug = slugify(name)

        # Check for duplicate slug
        if SearchEngine.objects.filter(slug=slug).exists():
            messages.error(request, _('An engine with this slug already exists.'))
            return self.get(request, *args, **kwargs)

        # Store in session
        self.update_wizard_data(
            name=name,
            slug=slug,
            is_active=is_active,
        )

        return redirect('search_admin:engine_wizard_step2')


@method_decorator(staff_member_required, name='dispatch')
class EngineWizardStep2View(WizardSessionMixin, TemplateView):
    """
    Step 2: Content Types
    Select which content types this engine will search
    """
    template_name = 'admin/search/wizard/step2_content.html'

    def get(self, request, *args, **kwargs):
        # Verify step 1 completed
        wizard_data = self.get_wizard_data()
        if not wizard_data.get('name'):
            messages.warning(request, _('Please complete Step 1 first.'))
            return redirect('search_admin:engine_wizard_step1')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 2
        context['total_steps'] = 4
        context['wizard_data'] = self.get_wizard_data()
        context['content_type_choices'] = CONTENT_TYPE_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        # Get selected content types
        content_types = request.POST.getlist('content_types')

        # Store in session
        self.update_wizard_data(
            content_types=content_types,
        )

        return redirect('search_admin:engine_wizard_step3')


@method_decorator(staff_member_required, name='dispatch')
class EngineWizardStep3View(WizardSessionMixin, TemplateView):
    """
    Step 3: Weight Configuration (Optional)
    Customize relevance weights for this engine
    """
    template_name = 'admin/search/wizard/step3_weights.html'

    def get(self, request, *args, **kwargs):
        # Verify previous steps completed
        wizard_data = self.get_wizard_data()
        if not wizard_data.get('name'):
            messages.warning(request, _('Please complete the wizard steps.'))
            return redirect('search_admin:engine_wizard_step1')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 3
        context['total_steps'] = 4
        context['wizard_data'] = self.get_wizard_data()
        context['weight_fields'] = WEIGHT_FIELDS
        return context

    def post(self, request, *args, **kwargs):
        use_custom_weights = request.POST.get('use_custom_weights') == 'on'

        weight_overrides = {}
        if use_custom_weights:
            for field_name, label, default, help_text in WEIGHT_FIELDS:
                value = request.POST.get(field_name, '').strip()
                if value:
                    try:
                        float_value = float(value)
                        # Only store if different from default
                        if float_value != default:
                            weight_overrides[field_name] = float_value
                    except ValueError:
                        pass

        # Store in session
        self.update_wizard_data(
            use_custom_weights=use_custom_weights,
            weight_overrides=weight_overrides,
        )

        return redirect('search_admin:engine_wizard_step4')


@method_decorator(staff_member_required, name='dispatch')
class EngineWizardStep4View(WizardSessionMixin, TemplateView):
    """
    Step 4: Review & Create
    Review configuration and create the engine
    """
    template_name = 'admin/search/wizard/step4_review.html'

    def get(self, request, *args, **kwargs):
        # Verify previous steps completed
        wizard_data = self.get_wizard_data()
        if not wizard_data.get('name'):
            messages.warning(request, _('Please complete the wizard steps.'))
            return redirect('search_admin:engine_wizard_step1')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 4
        context['total_steps'] = 4
        context['wizard_data'] = self.get_wizard_data()
        context['content_type_choices'] = CONTENT_TYPE_CHOICES
        context['weight_fields'] = WEIGHT_FIELDS
        return context

    def post(self, request, *args, **kwargs):
        wizard_data = self.get_wizard_data()

        try:
            # Create the search engine
            engine = SearchEngine.objects.create(
                name=wizard_data.get('name', ''),
                slug=wizard_data.get('slug', ''),
                is_active=wizard_data.get('is_active', True),
                content_types=wizard_data.get('content_types', []),
                weight_overrides=wizard_data.get('weight_overrides', {}),
            )

            # Clear wizard session data
            self.clear_wizard_data()

            messages.success(
                request,
                _('Search engine "%(name)s" created successfully!') % {'name': engine.name}
            )

            return redirect('admin:search_searchengine_changelist')

        except Exception as e:
            messages.error(
                request,
                _('Failed to create engine: %(error)s') % {'error': str(e)}
            )
            return redirect('search_admin:engine_wizard_step4')
