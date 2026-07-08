# -*- coding: utf-8 -*-
"""
Shipping Method Configuration Wizard Views
Multi-step wizard for creating and configuring shipping methods
"""
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from decimal import Decimal

from cart.models import ShippingMethod
from cart.forms import ShippingMethodWizardStep1Form
from shipping.models import ShippingZone, Location


@method_decorator(staff_member_required, name='dispatch')
class MethodWizardStep1View(TemplateView):
    """
    Step 1: Method Basics
    Name, type, icon, flat rate cost, carrier info
    """
    template_name = 'admin/cart/method_wizard/step1_basics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 1
        method_data = self.request.session.get('method_wizard_data', {})
        context['method_data'] = method_data

        # Prepare initial data for form
        initial_data = method_data.copy()

        # Load MediaAsset object for ModelChoiceField
        if initial_data.get('image'):
            from media_library.models import MediaAsset
            try:
                initial_data['image'] = MediaAsset.objects.get(id=initial_data['image'])
            except MediaAsset.DoesNotExist:
                initial_data['image'] = None

        # Create form with initial data from session
        context['form'] = ShippingMethodWizardStep1Form(initial=initial_data)
        return context

    def post(self, request, *args, **kwargs):
        # Validate form
        form = ShippingMethodWizardStep1Form(request.POST)

        if not form.is_valid():
            # Re-render with errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

        # Store cleaned data in session
        wizard_data = request.session.get('method_wizard_data', {})
        cleaned = form.cleaned_data

        wizard_data.update({
            'name': cleaned.get('name', ''),
            'description': cleaned.get('description', ''),
            'icon': cleaned.get('icon', ''),
            'image': cleaned['image'].id if cleaned.get('image') else '',
            'is_active': cleaned.get('is_active', True),
            'method_type': cleaned.get('method_type', ''),
        })

        # Conditional fields based on method_type
        method_type = cleaned.get('method_type', '')
        if method_type == 'flat_rate':
            flat_rate_cost = cleaned.get('flat_rate_cost')
            if flat_rate_cost:
                wizard_data['flat_rate_cost'] = str(flat_rate_cost)

        if method_type == 'real_time':
            wizard_data['carrier'] = cleaned.get('carrier', '')
            wizard_data['carrier_service_code'] = cleaned.get('carrier_service_code', '')

        request.session['method_wizard_data'] = wizard_data

        # Redirect to step 2
        return redirect('cart:method_wizard_step2')


@method_decorator(staff_member_required, name='dispatch')
class MethodWizardStep2View(TemplateView):
    """
    Step 2: Additional Options
    Requires shipping address and other options
    """
    template_name = 'admin/cart/method_wizard/step2_conditions.html'

    def get(self, request, *args, **kwargs):
        # Check if step 1 was completed before rendering
        method_data = request.session.get('method_wizard_data', {})
        if not method_data.get('name'):
            messages.warning(request, _('Please complete Step 1 first'))
            return redirect('cart:method_wizard_step1')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 2
        context['method_data'] = self.request.session.get('method_wizard_data', {})
        return context

    def post(self, request, *args, **kwargs):
        # Store step 2 data in session
        wizard_data = request.session.get('method_wizard_data', {})

        wizard_data.update({
            'requires_shipping_address': request.POST.get('requires_shipping_address') == 'on',
        })

        request.session['method_wizard_data'] = wizard_data

        # Redirect to step 3
        return redirect('cart:method_wizard_step3')


@method_decorator(staff_member_required, name='dispatch')
class MethodWizardStep3View(TemplateView):
    """
    Step 3: Geographic Coverage
    Zones (recommended) or legacy country/state selection
    """
    template_name = 'admin/cart/method_wizard/step3_coverage.html'

    def get(self, request, *args, **kwargs):
        # Check if previous steps were completed before rendering
        method_data = request.session.get('method_wizard_data', {})
        if not method_data.get('name'):
            messages.warning(request, _('Please complete the wizard steps'))
            return redirect('cart:method_wizard_step1')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 3
        method_data = self.request.session.get('method_wizard_data', {})
        context['method_data'] = method_data

        # All available zones
        context['all_zones'] = ShippingZone.objects.all().order_by('name')

        return context

    def post(self, request, *args, **kwargs):
        # Store step 3 data in session
        wizard_data = request.session.get('method_wizard_data', {})

        # Zone-based coverage
        zones = request.POST.getlist('zones')
        if zones:
            # Store zone IDs as strings (they are UUIDs)
            wizard_data['zones'] = zones
        else:
            wizard_data['zones'] = []

        request.session['method_wizard_data'] = wizard_data

        # Redirect to step 4
        return redirect('cart:method_wizard_step4')


@method_decorator(staff_member_required, name='dispatch')
class MethodWizardStep4View(TemplateView):
    """
    Step 4: Method Features
    Pickup locations, delivery time, sort order
    """
    template_name = 'admin/cart/method_wizard/step4_features.html'

    def get(self, request, *args, **kwargs):
        # Check if previous steps were completed before rendering
        method_data = request.session.get('method_wizard_data', {})
        if not method_data.get('name'):
            messages.warning(request, _('Please complete the wizard steps'))
            return redirect('cart:method_wizard_step1')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 4
        method_data = self.request.session.get('method_wizard_data', {})
        context['method_data'] = method_data

        # Pickup locations (for local_pickup type)
        if method_data.get('method_type') == 'local_pickup':
            context['all_pickup_locations'] = Location.objects.filter(accepts_pickup=True).order_by('name')

        return context

    def post(self, request, *args, **kwargs):
        # Store step 4 data in session
        wizard_data = request.session.get('method_wizard_data', {})

        # Pickup locations (for local_pickup)
        if wizard_data.get('method_type') == 'local_pickup':
            pickup_locations = request.POST.getlist('pickup_locations')
            wizard_data['pickup_locations'] = [int(loc_id) for loc_id in pickup_locations] if pickup_locations else []

        # Delivery time (for non-local-pickup methods)
        if wizard_data.get('method_type') != 'local_pickup':
            wizard_data.update({
                'min_delivery_days': int(request.POST.get('min_delivery_days', 1)),
                'max_delivery_days': int(request.POST.get('max_delivery_days', 5)),
            })
        else:
            # Local pickup has no delivery time
            wizard_data.update({
                'min_delivery_days': 0,
                'max_delivery_days': 0,
            })

        # Display settings
        wizard_data['sort_order'] = int(request.POST.get('sort_order', 0))

        # Real-time carrier options
        if wizard_data.get('method_type') == 'real_time':
            wizard_data['enable_rate_caching'] = request.POST.get('enable_rate_caching') == 'on'

        request.session['method_wizard_data'] = wizard_data

        # Redirect to step 5 (review)
        return redirect('cart:method_wizard_step5')


@method_decorator(staff_member_required, name='dispatch')
class MethodWizardStep5View(TemplateView):
    """
    Step 5: Review & Create
    Review all configuration and create the shipping method
    """
    template_name = 'admin/cart/method_wizard/step5_review.html'

    def get(self, request, *args, **kwargs):
        # Check if previous steps were completed before rendering
        method_data = request.session.get('method_wizard_data', {})
        if not method_data.get('name'):
            messages.warning(request, _('Please complete the wizard steps'))
            return redirect('cart:method_wizard_step1')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 5
        method_data = self.request.session.get('method_wizard_data', {})
        context['method_data'] = method_data

        # Load zones for display
        context['all_zones'] = ShippingZone.objects.all()

        # Load image object if present
        if method_data.get('image'):
            from media_library.models import MediaAsset
            try:
                method_image = MediaAsset.objects.get(id=method_data['image'])
                context['method_image'] = method_image
                # Get small thumbnail for display in review
                context['method_image_url'] = method_image.get_thumbnail('small')
            except MediaAsset.DoesNotExist:
                context['method_image'] = None
                context['method_image_url'] = None
        else:
            context['method_image'] = None
            context['method_image_url'] = None

        return context

    def post(self, request, *args, **kwargs):
        wizard_data = request.session.get('method_wizard_data', {})

        try:
            from djmoney.money import Money
            from core.utils import get_default_currency
            from media_library.models import MediaAsset

            # Prepare flat_rate_cost as Money object if present
            flat_rate_cost = None
            if wizard_data.get('flat_rate_cost'):
                try:
                    flat_rate_cost = Money(
                        Decimal(str(wizard_data['flat_rate_cost'])),
                        get_default_currency()
                    )
                except (ValueError, TypeError):
                    flat_rate_cost = None

            # Prepare image as MediaAsset instance if present
            image = None
            if wizard_data.get('image'):
                try:
                    image = MediaAsset.objects.get(id=wizard_data['image'])
                except MediaAsset.DoesNotExist:
                    pass

            # Create the shipping method
            method = ShippingMethod.objects.create(
                name=wizard_data.get('name', ''),
                description=wizard_data.get('description', ''),
                method_type=wizard_data.get('method_type', 'flat_rate'),
                is_active=wizard_data.get('is_active', True),
                icon=wizard_data.get('icon', ''),
                image=image,
                flat_rate_cost=flat_rate_cost,
                carrier=wizard_data.get('carrier', ''),
                carrier_service_code=wizard_data.get('carrier_service_code', ''),
                min_delivery_days=wizard_data.get('min_delivery_days', 1),
                max_delivery_days=wizard_data.get('max_delivery_days', 5),
                sort_order=wizard_data.get('sort_order', 0),
            )

            # Set many-to-many relationships
            if wizard_data.get('zones'):
                method.zones.set(wizard_data['zones'])

            if wizard_data.get('pickup_locations'):
                method.pickup_locations.set(wizard_data['pickup_locations'])

            # Clear wizard data from session
            if 'method_wizard_data' in request.session:
                del request.session['method_wizard_data']

            messages.success(
                request,
                _('Shipping method "%(name)s" created successfully!') % {'name': method.name}
            )

            # Redirect based on method type
            if wizard_data.get('method_type') == 'table_rate':
                # Redirect to rate table configuration
                messages.info(
                    request,
                    _('Please configure rate tables for this method.')
                )
                return redirect('admin:cart_shippingmethod_change', method.id)
            else:
                # Redirect to method list
                return redirect('admin:cart_shippingmethod_changelist')

        except Exception as e:
            messages.error(
                request,
                _('Failed to create shipping method: %(error)s') % {'error': str(e)}
            )
            return redirect('cart:method_wizard_step5')

