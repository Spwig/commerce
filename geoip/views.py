from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
import json
import requests

from .models import GeoIPProvider


@staff_member_required
def provider_dashboard(request):
    """Dashboard showing all configured GeoIP providers"""
    providers = GeoIPProvider.objects.all().order_by('priority')

    # Provider configurations with setup information
    provider_configs = {
        'spwig': {
            'name': 'Spwig GeoIP',
            'description': _('Production GeoIP service with BGP routing data for 98% accuracy'),
            'icon': 'fas fa-rocket',
            'free_tier': True,
            'setup_difficulty': 'none',
            'accuracy': 'very_high',
            'coverage': 'global',
            'badge': 'DEFAULT',
            'features': [
                '458K+ IP ranges from RIR registries',
                '135K+ BGP prefixes from 13K+ ASNs',
                '98% accuracy with BGP routing data',
                'No setup required - works out of the box',
                'JWT authentication with platform secret',
                'Redis caching for fast lookups',
            ],
        },
        'maxmind': {
            'name': 'MaxMind GeoLite2',
            'description': _('Free and commercial IP geolocation database with high accuracy'),
            'icon': 'fas fa-globe-americas',
            'free_tier': True,
            'setup_difficulty': 'easy',
            'accuracy': 'high',
            'coverage': 'global',
        },
        'ip2location': {
            'name': 'IP2Location',
            'description': _('Comprehensive IP geolocation database with multiple data points'),
            'icon': 'fas fa-map-marked-alt',
            'free_tier': True,
            'setup_difficulty': 'easy',
            'accuracy': 'very_high',
            'coverage': 'global',
        },
        'ipapi': {
            'name': 'ipapi',
            'description': _('Simple REST API for IP geolocation with generous free tier'),
            'icon': 'fas fa-network-wired',
            'free_tier': True,
            'setup_difficulty': 'very_easy',
            'accuracy': 'good',
            'coverage': 'global',
        },
        'ipgeolocation': {
            'name': 'ipgeolocation.io',
            'description': _('Real-time IP geolocation API with timezone and currency data'),
            'icon': 'fas fa-location-dot',
            'free_tier': True,
            'setup_difficulty': 'very_easy',
            'accuracy': 'high',
            'coverage': 'global',
        },
        'ipinfo': {
            'name': 'IPinfo',
            'description': _('Fast and accurate IP data API with ASN and company information'),
            'icon': 'fas fa-info-circle',
            'free_tier': True,
            'setup_difficulty': 'very_easy',
            'accuracy': 'very_high',
            'coverage': 'global',
        },
        'abstractapi': {
            'name': 'Abstract API',
            'description': _('Modern IP geolocation API with security and VPN detection'),
            'icon': 'fas fa-shield-alt',
            'free_tier': True,
            'setup_difficulty': 'easy',
            'accuracy': 'high',
            'coverage': 'global',
        },
    }

    # Check which providers are configured
    configured_types = [p.provider_type for p in providers]

    context = {
        'title': _('GeoIP Provider Management'),
        'providers': providers,
        'provider_configs': provider_configs,
        'configured_types': configured_types,
    }

    return render(request, 'admin/geoip/provider_dashboard.html', context)


@staff_member_required
def provider_wizard(request, provider_type):
    """Wizard for setting up a specific GeoIP provider"""

    # Get existing provider if it exists
    existing_provider = GeoIPProvider.objects.filter(provider_type=provider_type).first()

    # Provider-specific configurations
    provider_configs = {
        'maxmind': {
            'name': 'MaxMind GeoLite2',
            'signup_url': 'https://www.maxmind.com/en/geolite2/signup',
            'dashboard_url': 'https://www.maxmind.com/en/account',
            'docs_url': 'https://dev.maxmind.com/geoip/geolite2-free-geolocation-data',
            'requires': ['license_key'],
            'supports_batch': True,
            'free_tier': 'GeoLite2 databases - Free forever',
            'paid_tier': 'GeoIP2 - From $100/month',
            'update_frequency': 'Weekly (free) / Daily (paid)',
            'data_points': ['Country', 'City', 'Postal Code', 'Latitude/Longitude', 'Time Zone', 'ISP', 'Domain'],
        },
        'ip2location': {
            'name': 'IP2Location',
            'signup_url': 'https://www.ip2location.com/sign-up',
            'dashboard_url': 'https://www.ip2location.com/dashboard',
            'docs_url': 'https://www.ip2location.com/development-libraries/ip2location/python',
            'requires': ['api_key'],
            'supports_batch': False,
            'free_tier': 'LITE databases - Free forever',
            'paid_tier': 'From $49/year',
            'update_frequency': 'Monthly (free) / Daily (paid)',
            'data_points': ['Country', 'Region', 'City', 'Latitude/Longitude', 'ZIP Code', 'Time Zone', 'ISP', 'Domain', 'Net Speed', 'Mobile Info'],
        },
        'ipapi': {
            'name': 'ipapi',
            'signup_url': 'https://ipapi.com/signup',
            'dashboard_url': 'https://ipapi.com/dashboard',
            'docs_url': 'https://ipapi.com/documentation',
            'requires': ['api_key'],
            'supports_batch': True,
            'free_tier': '1,000 requests/month',
            'paid_tier': 'From $12/month for 50,000 requests',
            'update_frequency': 'Real-time API',
            'data_points': ['Country', 'Region', 'City', 'ZIP', 'Latitude/Longitude', 'Time Zone', 'Currency', 'Connection Type', 'ISP'],
        },
        'ipgeolocation': {
            'name': 'ipgeolocation.io',
            'signup_url': 'https://app.ipgeolocation.io/signup',
            'dashboard_url': 'https://app.ipgeolocation.io/dashboard',
            'docs_url': 'https://ipgeolocation.io/documentation.html',
            'requires': ['api_key'],
            'supports_batch': True,
            'free_tier': '1,000 requests/day (30,000/month)',
            'paid_tier': 'From $15/month for 150,000 requests',
            'update_frequency': 'Real-time API',
            'data_points': ['Country', 'State', 'City', 'ZIP', 'Latitude/Longitude', 'Time Zone', 'Currency', 'ISP', 'Organization', 'AS Number'],
        },
        'ipinfo': {
            'name': 'IPinfo',
            'signup_url': 'https://ipinfo.io/signup',
            'dashboard_url': 'https://ipinfo.io/account',
            'docs_url': 'https://ipinfo.io/developers',
            'requires': ['api_key'],
            'supports_batch': True,
            'free_tier': '50,000 requests/month',
            'paid_tier': 'From $49/month for 250,000 requests',
            'update_frequency': 'Real-time API',
            'data_points': ['Country', 'Region', 'City', 'Postal', 'Latitude/Longitude', 'Time Zone', 'ASN', 'Company', 'Carrier', 'Privacy Detection'],
        },
        'abstractapi': {
            'name': 'Abstract API',
            'signup_url': 'https://app.abstractapi.com/sign-up',
            'dashboard_url': 'https://app.abstractapi.com/dashboard',
            'docs_url': 'https://docs.abstractapi.com/ip-geolocation',
            'requires': ['api_key'],
            'supports_batch': False,
            'free_tier': '1,000 requests/month',
            'paid_tier': 'From $9/month for 20,000 requests',
            'update_frequency': 'Real-time API',
            'data_points': ['Country', 'Region', 'City', 'Postal Code', 'Latitude/Longitude', 'Time Zone', 'ISP', 'VPN Detection', 'Security Info'],
        },
    }

    # Get the specific provider config
    provider_config = provider_configs.get(provider_type)
    if not provider_config:
        messages.error(request, _('Invalid provider type'))
        return redirect('admin:geoip_geolocation_changelist')

    if request.method == 'POST':
        # Handle provider setup
        step = request.POST.get('step', '1')

        if step == '4':  # Final step - save configuration
            try:
                if existing_provider:
                    provider = existing_provider
                else:
                    provider = GeoIPProvider()

                provider.name = provider_config['name']
                provider.provider_type = provider_type
                provider.is_active = request.POST.get('is_active', 'on') == 'on'
                provider.priority = int(request.POST.get('priority', 10))

                # Build configuration based on provider requirements
                config = {}
                if 'api_key' in provider_config['requires']:
                    config['api_key'] = request.POST.get('api_key', '')
                if 'license_key' in provider_config['requires']:
                    config['license_key'] = request.POST.get('license_key', '')
                if 'api_secret' in provider_config['requires']:
                    config['api_secret'] = request.POST.get('api_secret', '')

                # Add additional settings
                config['cache_duration'] = int(request.POST.get('cache_duration', 86400))
                config['timeout'] = int(request.POST.get('timeout', 5))
                config['batch_size'] = int(request.POST.get('batch_size', 100))

                provider.config = config
                provider.save()

                messages.success(request, _('%(name)s has been configured successfully!') % {'name': provider_config['name']})

                # Test the provider if requested
                if request.POST.get('test_connection'):
                    import time as _time
                    _provider_class_map = {
                        'spwig': 'geoip.providers.SpwigProvider',
                        'edge_header': 'geoip.providers.EdgeHeaderProvider',
                        'browser_hint': 'geoip.providers.BrowserHintProvider',
                    }
                    _provider_path = _provider_class_map.get(provider_type)
                    if _provider_path:
                        try:
                            _mod_path, _cls_name = _provider_path.rsplit('.', 1)
                            _mod = __import__(_mod_path, fromlist=[_cls_name])
                            _cls = getattr(_mod, _cls_name)
                            _inst = _cls(config)
                            if _inst.initialize():
                                _start = _time.time()
                                _result = _inst.lookup('8.8.8.8')
                                _elapsed = (_time.time() - _start) * 1000
                                if _result:
                                    messages.success(request, _('Test passed — resolved 8.8.8.8 in %(ms).0f ms') % {'ms': _elapsed})
                                else:
                                    messages.warning(request, _('Test returned no data for 8.8.8.8'))
                                _inst.close()
                            else:
                                messages.warning(request, _('Provider failed to initialize during test'))
                        except Exception as _e:
                            messages.warning(request, _('Test failed: %(error)s') % {'error': str(_e)})

                return redirect('admin:geoip_geolocation_changelist')

            except Exception as e:
                messages.error(request, _('Error saving configuration: %(error)s') % {'error': str(e)})

    context = {
        'title': _('Setup %(name)s') % {'name': provider_config['name']},
        'provider_type': provider_type,
        'provider_config': provider_config,
        'existing_provider': existing_provider,
        'step': request.GET.get('step', '1'),
    }

    return render(request, 'admin/geoip/provider_wizard.html', context)


@staff_member_required
@require_http_methods(['POST'])
def test_provider(request, provider_type):
    """Test a GeoIP provider configuration by resolving a known IP"""
    import time

    test_ip = request.POST.get('test_ip', '8.8.8.8')

    try:
        provider = get_object_or_404(GeoIPProvider, provider_type=provider_type)

        # Attempt to resolve using the configured provider
        geoip_config = getattr(settings, 'GEOIP_CONFIG', {})
        provider_config = geoip_config.get('PROVIDER_CONFIG', {})

        # Try to instantiate and test the appropriate provider class
        provider_class_map = {
            'spwig': 'geoip.providers.SpwigProvider',
            'edge_header': 'geoip.providers.EdgeHeaderProvider',
            'browser_hint': 'geoip.providers.BrowserHintProvider',
        }

        provider_path = provider_class_map.get(provider_type)
        if provider_path:
            module_path, class_name = provider_path.rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            provider_cls = getattr(module, class_name)
            instance = provider_cls(provider_config)

            if instance.initialize():
                start_time = time.time()
                location_data = instance.lookup(test_ip)
                elapsed = (time.time() - start_time) * 1000

                if location_data:
                    result = {
                        'success': True,
                        'message': _('Connection successful!'),
                        'response_ms': round(elapsed, 2),
                        'data': location_data,
                    }
                else:
                    result = {
                        'success': False,
                        'message': _('Provider returned no data for IP: %(ip)s') % {'ip': test_ip},
                    }
            else:
                result = {
                    'success': False,
                    'message': _('Provider failed to initialize. Check configuration.'),
                }
        else:
            # Database/API providers without a provider class implementation
            result = {
                'success': True,
                'message': _('%(name)s is configured. This provider type will be tested on first real request.') % {'name': provider.name},
                'data': {'provider': provider.name, 'type': provider_type, 'active': provider.is_active},
            }

    except GeoIPProvider.DoesNotExist:
        result = {
            'success': False,
            'message': _('Provider not configured'),
        }
    except Exception as e:
        result = {
            'success': False,
            'message': str(e),
        }

    return JsonResponse(result)


@staff_member_required
@require_http_methods(['POST'])
def toggle_provider(request, provider_id):
    """Toggle a provider's active status"""

    try:
        provider = get_object_or_404(GeoIPProvider, pk=provider_id)
        provider.is_active = not provider.is_active
        provider.save()

        status = _('activated') if provider.is_active else _('deactivated')
        messages.success(request, _('%(name)s has been %(status)s') % {
            'name': provider.name,
            'status': status
        })

    except Exception as e:
        messages.error(request, _('Error toggling provider: %(error)s') % {'error': str(e)})

    return redirect('admin:geoip_geolocation_changelist')


@staff_member_required
@require_http_methods(['POST'])
def update_database(request, provider_id):
    """Check database availability and update timestamp for a GeoIP provider"""

    DATABASE_PROVIDER_TYPES = {'maxmind', 'dbip', 'ip2location', 'custom'}

    try:
        provider = get_object_or_404(GeoIPProvider, pk=provider_id)

        if provider.provider_type not in DATABASE_PROVIDER_TYPES:
            return JsonResponse({
                'success': False,
                'message': _('%(name)s does not use a local database') % {'name': provider.name},
            })

        if not provider.database_url:
            return JsonResponse({
                'success': False,
                'message': _('No database URL configured for %(name)s') % {'name': provider.name},
            })

        response = requests.head(provider.database_url, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            provider.last_update = timezone.now()
            provider.save(update_fields=['last_update', 'updated_at'])
            return JsonResponse({
                'success': True,
                'message': _('Database check passed for %(name)s') % {'name': provider.name},
                'last_update': provider.last_update.strftime('%b %d, %Y'),
            })
        else:
            return JsonResponse({
                'success': False,
                'message': _('%(name)s: HTTP %(status)s from database URL') % {
                    'name': provider.name,
                    'status': response.status_code,
                },
            })

    except GeoIPProvider.DoesNotExist:
        return JsonResponse({'success': False, 'message': _('Provider not found')})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})