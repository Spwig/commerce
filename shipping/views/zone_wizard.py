# -*- coding: utf-8 -*-
"""
Zone Configuration Wizard Views
Multi-step wizard for creating and configuring shipping zones
"""
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from shipping.models import ShippingZone


@method_decorator(staff_member_required, name='dispatch')
class ZoneWizardStep1View(TemplateView):
    """
    Step 1: Basic Information
    Zone name, description, and priority
    """
    template_name = 'admin/shipping/zone_wizard/step1_basic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 1
        context['zone_data'] = self.request.session.get('zone_wizard_data', {})
        return context

    def post(self, request, *args, **kwargs):
        # Store step 1 data in session
        wizard_data = request.session.get('zone_wizard_data', {})
        wizard_data.update({
            'name': request.POST.get('name', ''),
            'description': request.POST.get('description', ''),
            'priority': int(request.POST.get('priority', 0)),
            'is_active': request.POST.get('is_active') == 'on',
        })
        request.session['zone_wizard_data'] = wizard_data

        # Redirect to step 2
        return redirect('shipping:zone_wizard_step2')


@method_decorator(staff_member_required, name='dispatch')
class ZoneWizardStep2View(TemplateView):
    """
    Step 2: Geographic Coverage
    Configure countries, states, and postal code patterns
    """
    template_name = 'admin/shipping/zone_wizard/step2_coverage.html'

    def get(self, request, *args, **kwargs):
        # Check if step 1 was completed before rendering
        zone_data = request.session.get('zone_wizard_data', {})
        if not zone_data.get('name'):
            messages.warning(request, _('Please complete Step 1 first'))
            return redirect('shipping:zone_wizard_step1')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        from django_countries import countries as django_countries_list
        from shipping.state_province_data import get_states_for_countries, get_states_for_country

        context = super().get_context_data(**kwargs)
        context['step'] = 2
        zone_data = self.request.session.get('zone_wizard_data', {})
        context['zone_data'] = zone_data

        # Prepare selected countries from session data
        selected_country_codes = zone_data.get('countries', [])
        context['selected_countries'] = [
            {'code': code, 'name': str(dict(django_countries_list)[code])}
            for code in selected_country_codes
            if code in dict(django_countries_list)
        ]

        # Prepare available countries list from django-countries (exclude selected)
        available_countries = []
        for code, name in django_countries_list:
            if code not in selected_country_codes:
                available_countries.append({
                    'code': code,
                    'name': str(name),  # Convert lazy translation to string
                })
        context['available_countries'] = available_countries

        # Prepare selected states from session data
        selected_states_dict = zone_data.get('states', {})
        selected_states = []
        selected_state_codes = []
        for country_code, state_codes in selected_states_dict.items():
            country_name = str(dict(django_countries_list).get(country_code, country_code))
            country_states = get_states_for_country(country_code)
            for state_code in state_codes:
                state_name = str(country_states.get(state_code, state_code))
                full_code = f"{country_code}:{state_code}"
                selected_state_codes.append(full_code)
                selected_states.append({
                    'code': full_code,
                    'name': f"{state_name} ({country_name})",
                    'country': country_code,
                })
        context['selected_states'] = selected_states

        # Prepare states for selected countries (exclude already selected)
        if selected_country_codes:
            states_data = get_states_for_countries(selected_country_codes)
            # Convert to list format for template
            available_states = []
            for country_code, states in states_data.items():
                country_name = str(dict(django_countries_list).get(country_code, country_code))
                for state_code, state_name in states.items():
                    full_code = f"{country_code}:{state_code}"
                    if full_code not in selected_state_codes:
                        available_states.append({
                            'code': full_code,
                            'name': f"{str(state_name)} ({country_name})",
                            'country': country_code,
                        })
            context['available_states'] = available_states
        else:
            context['available_states'] = []

        return context

    def post(self, request, *args, **kwargs):
        # Store step 2 data in session
        wizard_data = request.session.get('zone_wizard_data', {})

        # Parse selected countries from dual-listbox
        # Format: selected_countries[] = ['US', 'CA', 'MX']
        selected_countries = request.POST.getlist('selected_countries[]')
        countries = [c.strip().upper() for c in selected_countries if c.strip()]

        # Parse selected states from dual-listbox
        # Format: selected_states[] = ['US:CA', 'US:NY', 'CA:ON']
        selected_states = request.POST.getlist('selected_states[]')

        # Convert from ['US:CA', 'US:NY', 'CA:ON'] format
        # To: {'US': ['CA', 'NY'], 'CA': ['ON']} format
        states = {}
        for state_item in selected_states:
            if ':' in state_item:
                country_code, state_code = state_item.split(':', 1)
                country_code = country_code.strip().upper()
                state_code = state_code.strip().upper()
                if country_code not in states:
                    states[country_code] = []
                if state_code not in states[country_code]:
                    states[country_code].append(state_code)

        # Parse postal patterns (one per line)
        postal_patterns_input = request.POST.get('postal_patterns', '').strip()
        if postal_patterns_input:
            # Split by newlines and clean up
            postal_patterns = [
                p.strip()
                for p in postal_patterns_input.split('\n')
                if p.strip()
            ]
        else:
            postal_patterns = []

        wizard_data.update({
            'countries': countries,
            'states': states,
            'postal_code_patterns': postal_patterns,
        })
        request.session['zone_wizard_data'] = wizard_data

        # Redirect to step 3
        return redirect('shipping:zone_wizard_step3')


@method_decorator(staff_member_required, name='dispatch')
class ZoneWizardStep3View(TemplateView):
    """
    Step 3: Review & Create
    Review all zone configuration and create the zone
    """
    template_name = 'admin/shipping/zone_wizard/step3_review.html'

    def get(self, request, *args, **kwargs):
        # Check if previous steps were completed before rendering
        zone_data = request.session.get('zone_wizard_data', {})
        if not zone_data.get('name'):
            messages.warning(request, _('Please complete the wizard steps'))
            return redirect('shipping:zone_wizard_step1')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = 3
        context['zone_data'] = self.request.session.get('zone_wizard_data', {})
        return context

    def post(self, request, *args, **kwargs):
        wizard_data = request.session.get('zone_wizard_data', {})

        try:
            # Create the zone
            zone = ShippingZone.objects.create(
                name=wizard_data.get('name', ''),
                description=wizard_data.get('description', ''),
                priority=wizard_data.get('priority', 0),
                is_active=wizard_data.get('is_active', True),
                countries=wizard_data.get('countries', []),
                states=wizard_data.get('states', {}),
                postal_code_patterns=wizard_data.get('postal_code_patterns', []),
                created_by=request.user,
            )

            # Clear wizard data from session
            if 'zone_wizard_data' in request.session:
                del request.session['zone_wizard_data']

            messages.success(
                request,
                _('Shipping zone "%(name)s" created successfully!') % {'name': zone.name}
            )

            # Redirect to zone admin
            return redirect('admin:shipping_shippingzone_changelist')

        except Exception as e:
            messages.error(
                request,
                _('Failed to create zone: %(error)s') % {'error': str(e)}
            )
            return redirect('shipping:zone_wizard_step3')


# AJAX endpoint for country validation
@staff_member_required
@require_http_methods(["POST"])
def validate_country_code(request):
    """Validate ISO country code via AJAX"""
    import json
    from django_countries import countries

    country_code = request.POST.get('country_code', '').strip().upper()

    if not country_code:
        return JsonResponse({'valid': False, 'error': 'Country code is required'})

    # Check if valid ISO 3166-1 alpha-2 code
    if country_code in dict(countries):
        country_name = dict(countries)[country_code]
        return JsonResponse({
            'valid': True,
            'code': country_code,
            'name': country_name
        })
    else:
        return JsonResponse({
            'valid': False,
            'error': f'Invalid country code: {country_code}'
        })


# AJAX endpoint for postal pattern validation
@staff_member_required
@require_http_methods(["POST"])
def validate_postal_pattern(request):
    """Validate regex postal pattern via AJAX"""
    import json
    import re

    pattern = request.POST.get('pattern', '').strip()
    test_value = request.POST.get('test_value', '').strip()

    if not pattern:
        return JsonResponse({'valid': False, 'error': 'Pattern is required'})

    try:
        # Try to compile the regex
        compiled = re.compile(pattern)

        # If test value provided, test it
        matches = None
        if test_value:
            matches = bool(compiled.match(test_value))

        return JsonResponse({
            'valid': True,
            'pattern': pattern,
            'matches': matches
        })

    except re.error as e:
        return JsonResponse({
            'valid': False,
            'error': f'Invalid regex pattern: {str(e)}'
        })


# AJAX endpoint for fetching states by country
@staff_member_required
@require_http_methods(["POST"])
def get_states_for_countries(request):
    """
    Get states/provinces for selected countries via AJAX.

    This endpoint is called when countries are selected/deselected in the dual-listbox
    to dynamically update the available states list.

    POST data:
        country_codes: Comma-separated list of ISO 3166-1 alpha-2 country codes

    Returns:
        JSON with format:
        {
            'states': {
                'US': [
                    {'code': 'CA', 'name': 'California'},
                    {'code': 'NY', 'name': 'New York'},
                    ...
                ],
                'CA': [
                    {'code': 'ON', 'name': 'Ontario'},
                    ...
                ]
            }
        }
    """
    import json
    from shipping.state_province_data import get_states_for_countries as get_states_data

    country_codes_str = request.POST.get('country_codes', '').strip()

    if not country_codes_str:
        return JsonResponse({'states': {}})

    # Parse country codes (comma-separated)
    country_codes = [code.strip().upper() for code in country_codes_str.split(',') if code.strip()]

    # Get states for these countries
    states_data = get_states_data(country_codes)

    # Convert to format expected by frontend
    # From: {'US': {'CA': 'California', 'NY': 'New York'}}
    # To: {'US': [{'code': 'CA', 'name': 'California'}, {'code': 'NY', 'name': 'New York'}]}
    result = {}
    for country_code, states in states_data.items():
        result[country_code] = [
            {'code': code, 'name': str(name)}  # str() to convert lazy translation
            for code, name in states.items()
        ]

    return JsonResponse({'states': result})
