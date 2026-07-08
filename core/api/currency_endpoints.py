"""
Multi-Currency Management API Endpoints

These endpoints provide RESTful access to currency configuration,
supporting the drag-and-drop UI and external integrations.
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from moneyed import CURRENCIES
from core.supported_currency_model import SupportedCurrency


# Obsolete/historical currencies that should be excluded
OBSOLETE_CURRENCIES = {
    'ADP', 'AFA', 'ALK', 'AOK', 'AON', 'AOR', 'ARA', 'ARL', 'ARM', 'ARP', 'ATS', 'AZM',
    'BAD', 'BAN', 'BEC', 'BEF', 'BEL', 'BGL', 'BGO', 'BOL', 'BRB', 'BRC', 'BRE', 'BRN', 'BRR', 'BRZ', 'BYB', 'BYR',
    'CLE', 'CSD', 'CSK', 'CYP', 'DDM', 'DEM', 'ECS', 'ECV', 'EEK',
    'ESA', 'ESB', 'ESP', 'FIM', 'FRF', 'GHC', 'GRD', 'GWP',
    'HRD', 'IEP', 'ILR', 'ILP', 'ISJ', 'ITL', 'KRH', 'KRO', 'LTL', 'LUC', 'LUF', 'LUL', 'LVL',
    'MGF', 'MKN', 'MLF', 'MRO', 'MTL', 'MVP', 'MXP', 'MZM',
    'NIC', 'NLG', 'PEI', 'PES', 'PLZ', 'PTE', 'ROL',
    'RUR', 'SDD', 'SDP', 'SIT', 'SKK', 'SLL', 'SRG', 'STD', 'SUR', 'TJR', 'TMM',
    'TPE', 'TRL', 'TVD', 'UAK', 'UGS', 'UYP', 'VEB', 'VEF', 'VNN',
    'XEU', 'YDD', 'YUD', 'YUM', 'YUN', 'YUR',
    'ZAL', 'ZMK', 'ZRN', 'ZRZ', 'ZWD', 'ZWN', 'ZWR',
    # Additional obsolete currencies
    'BUK', 'GEK', 'GNS', 'GQE', 'GWE', 'LTT', 'LVR', 'MAF', 'MCF', 'MTP', 'MZE', 'RHD',
}

# Special/non-circulating currencies and special purpose codes
SPECIAL_CURRENCIES = {
    'XAU',  # Gold
    'XAG',  # Silver
    'XPT',  # Platinum
    'XPD',  # Palladium
    'XDR',  # IMF Special Drawing Rights
    'XSU',  # Sucre
    'XUA',  # ADB Unit of Account
    'XXX',  # No currency
    'XTS',  # Test currency
    'XBA',  # European Composite Unit (EURCO)
    'XBB',  # European Monetary Unit (E.M.U.-6)
    'XBC',  # European Unit of Account 9 (E.U.A.-9)
    'XBD',  # European Unit of Account 17 (E.U.A.-17)
    'XFO',  # Gold-Franc
    'XRE',  # RINET Funds Code
    'CHE',  # WIR Euro (complementary currency)
    'CHW',  # WIR Franc (complementary currency)
    'CLF',  # Unidad de Fomento (funds code)
    'MXV',  # Mexican Unidad de Inversion (UDI) (funds code)
    'USN',  # US Dollar Next Day (funds code)
    'USS',  # US Dollar Same Day (funds code)
    'UYI',  # Uruguay Peso en Unidades Indexadas (funds code)
    'UYW',  # Unidad Previsional (funds code)
    'NPW',  # Special drawing rights (Nepal - not for general use)
    'BOV',  # Bolivian Mvdol (funds code)
    'COU',  # Unidad de Valor Real (funds code)
    'CUC',  # Cuban Convertible Peso (obsolete 2021)
    'KPW',  # North Korean Won (not tradable)
    'MDC',  # Moldovan Cupon (obsolete)
    'XBR',  # Special settlement currency
    'XFU',  # UIC-Franc (special settlement)
    'XPF',  # CFP Franc (special purpose)
}

# Cryptocurrencies (keep for now, merchants may want them)
CRYPTOCURRENCIES = {
    'BTC',  # Bitcoin
    'ETH',  # Ethereum
    'XRP',  # Ripple
    'LTC',  # Litecoin
    'BCH',  # Bitcoin Cash
    'ADA',  # Cardano
    'DOT',  # Polkadot
    'DOGE', # Dogecoin
}


def get_currency_flag(currency_code):
    """Get country flag image path for a currency code"""
    currency_to_country = {
        # Major currencies
        'USD': 'US', 'EUR': 'EU', 'GBP': 'GB', 'JPY': 'JP', 'CNY': 'CN',
        'AUD': 'AU', 'CAD': 'CA', 'CHF': 'CH', 'INR': 'IN', 'MXN': 'MX',
        'BRL': 'BR', 'ZAR': 'ZA', 'AED': 'AE', 'SAR': 'SA', 'SGD': 'SG',
        'HKD': 'HK', 'NZD': 'NZ', 'SEK': 'SE', 'NOK': 'NO', 'DKK': 'DK',
        'PLN': 'PL', 'THB': 'TH', 'IDR': 'ID', 'MYR': 'MY', 'PHP': 'PH',
        'CZK': 'CZ', 'ILS': 'IL', 'CLP': 'CL', 'VND': 'VN', 'KRW': 'KR',
        'TRY': 'TR', 'RUB': 'RU', 'HUF': 'HU', 'RON': 'RO', 'ARS': 'AR',
        'COP': 'CO', 'PEN': 'PE', 'UAH': 'UA', 'EGP': 'EG', 'PKR': 'PK',
        'BDT': 'BD', 'NGN': 'NG', 'MAD': 'MA', 'KES': 'KE',

        # European currencies
        'ALL': 'AL', 'BAM': 'BA', 'BGN': 'BG', 'HRK': 'HR', 'ISK': 'IS',
        'MKD': 'MK', 'MDL': 'MD', 'RSD': 'RS', 'GEL': 'GE', 'AMD': 'AM',
        'AZN': 'AZ', 'BYN': 'BY', 'KZT': 'KZ', 'UZS': 'UZ', 'KGS': 'KG',
        'TJS': 'TJ', 'TMT': 'TM',

        # Asia Pacific
        'AFN': 'AF', 'BDT': 'BD', 'BTN': 'BT', 'BND': 'BN', 'KHR': 'KH',
        'FJD': 'FJ', 'LAK': 'LA', 'MOP': 'MO', 'MVR': 'MV', 'MMK': 'MM',
        'NPR': 'NP', 'PGK': 'PG', 'LKR': 'LK', 'TWD': 'TW', 'MNT': 'MN',

        # Middle East
        'BHD': 'BH', 'IQD': 'IQ', 'IRR': 'IR', 'JOD': 'JO', 'KWD': 'KW',
        'LBP': 'LB', 'OMR': 'OM', 'QAR': 'QA', 'SYP': 'SY', 'YER': 'YE',

        # Africa
        'DZD': 'DZ', 'AOA': 'AO', 'BWP': 'BW', 'BIF': 'BI', 'XAF': 'CM',
        'CVE': 'CV', 'KMF': 'KM', 'CDF': 'CD', 'DJF': 'DJ', 'ERN': 'ER',
        'ETB': 'ET', 'GMD': 'GM', 'GHS': 'GH', 'GNF': 'GN', 'KES': 'KE',
        'LSL': 'LS', 'LRD': 'LR', 'LYD': 'LY', 'MGA': 'MG', 'MWK': 'MW',
        'MRU': 'MR', 'MUR': 'MU', 'MAD': 'MA', 'MZN': 'MZ', 'NAD': 'NA',
        'NGN': 'NG', 'RWF': 'RW', 'STN': 'ST', 'SCR': 'SC', 'SLL': 'SL',
        'SOS': 'SO', 'SSP': 'SS', 'SDG': 'SD', 'SZL': 'SZ', 'TZS': 'TZ',
        'TND': 'TN', 'UGX': 'UG', 'ZMW': 'ZM', 'ZWL': 'ZW',

        # Americas
        'ARS': 'AR', 'BOB': 'BO', 'BRL': 'BR', 'CLP': 'CL', 'COP': 'CO',
        'CRC': 'CR', 'CUP': 'CU', 'DOP': 'DO', 'GTQ': 'GT', 'HTG': 'HT',
        'HNL': 'HN', 'JMD': 'JM', 'NIO': 'NI', 'PAB': 'PA', 'PYG': 'PY',
        'PEN': 'PE', 'SRD': 'SR', 'TTD': 'TT', 'UYU': 'UY', 'VES': 'VE',
        'BBD': 'BB', 'BZD': 'BZ', 'BMD': 'BM', 'BSD': 'BS', 'KYD': 'KY',
        'XCD': 'AG',  # East Caribbean Dollar
        'ANG': 'CW',  # Netherlands Antillean Guilder (Curacao)
        'AWG': 'AW',  # Aruban Florin
        'FKP': 'FK',  # Falkland Islands Pound
        'GYD': 'GY',  # Guyanese Dollar
        'SVC': 'SV',  # Salvadoran Colon (now uses USD officially)
        'VED': 'VE',  # Venezuelan Bolívar Digital

        # Pacific
        'WST': 'WS', 'TOP': 'TO', 'VUV': 'VU', 'SBD': 'SB', 'NZD': 'NZ',
        'AUD': 'AU', 'FJD': 'FJ', 'PGK': 'PG',

        # Special territories and dependencies
        'GIP': 'GI',  # Gibraltar Pound
        'SHP': 'SH',  # Saint Helena Pound
        'IMP': 'IM',  # Isle of Man Pound
        'XOF': 'SN',  # West African CFA Franc (Senegal as representative)

        # Additional currencies
        'BGM': 'BG',  # Bulgarian Lev (old form, BGN is current)
        'BOP': 'BO',  # Bolivian Peso (obsolete, BOB is current)
        'BOV': 'BO',  # Bolivian Mvdol (funds code)
        'CNH': 'HK',  # Chinese Yuan (offshore, traded in Hong Kong)
        'CNX': 'CN',  # Chinese People's Bank Dollar (not widely used)
        'SLE': 'SL',  # Sierra Leonean Leone (new, replaced SLL)
    }

    country_code = currency_to_country.get(currency_code, '')
    if country_code:
        try:
            from django_countries.fields import Country
            country = Country(country_code)
            return country.flag  # Returns path like /static/flags/us.gif
        except (ImportError, AttributeError):
            pass

    return ''


@staff_member_required
@require_http_methods(["GET"])
def list_all_currencies(request):
    """
    Get all ISO 4217 currencies with active status.

    Query Parameters:
        - search: Filter by code or name (optional)
        - active_only: If true, return only active currencies (optional)

    Returns:
        {
            "success": true,
            "currencies": [
                {
                    "code": "USD",
                    "name": "United States Dollar",
                    "symbol": "$",
                    "is_active": true,
                    "order": 0,
                    "flag": "🇺🇸",
                    "settings": {
                        "show_flag": true,
                        "show_symbol": true,
                        "custom_symbol": null
                    }
                },
                ...
            ],
            "total": 150,
            "active_count": 12
        }
    """
    try:
        search = request.GET.get('search', '').strip().upper()
        active_only = request.GET.get('active_only', '').lower() == 'true'

        # Get active currencies from database
        active_currencies = {
            curr.code: curr
            for curr in SupportedCurrency.objects.all()
        }

        # Build currency list from moneyed library
        currencies = []
        for code, currency_obj in CURRENCIES.items():
            # Skip obsolete and special currencies
            if code in OBSOLETE_CURRENCIES or code in SPECIAL_CURRENCIES:
                continue

            # Apply search filter
            if search and search not in code and search not in currency_obj.name.upper():
                continue

            db_currency = active_currencies.get(code)
            is_active = db_currency.is_active if db_currency else False

            # Apply active filter
            if active_only and not is_active:
                continue

            currencies.append({
                'code': code,
                'name': getattr(currency_obj, 'name', code),
                'symbol': getattr(currency_obj, 'symbol', code),
                'is_active': is_active,
                'order': db_currency.order if db_currency else 999,
                'flag': get_currency_flag(code),
                'settings': {
                    'show_flag': db_currency.show_flag if db_currency else True,
                    'show_symbol': db_currency.show_symbol if db_currency else True,
                    'custom_symbol': db_currency.custom_symbol if db_currency else None,
                } if db_currency else None
            })

        # Sort by active status and order
        currencies.sort(key=lambda x: (not x['is_active'], x['order'], x['code']))

        return JsonResponse({
            'success': True,
            'currencies': currencies,
            'total': len(currencies),
            'active_count': sum(1 for c in currencies if c['is_active'])
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
@require_http_methods(["GET"])
def list_active_currencies(request):
    """
    Get only active currencies in display order.

    Returns:
        {
            "success": true,
            "currencies": [...],
            "count": 12
        }
    """
    try:
        currencies = []
        for curr in SupportedCurrency.get_active_currencies():
            currencies.append({
                'code': curr.code,
                'name': curr.get_currency_name(),
                'symbol': curr.symbol,
                'order': curr.order,
                'flag': curr.get_country_flag(),
                'settings': {
                    'show_flag': curr.show_flag,
                    'show_symbol': curr.show_symbol,
                    'custom_symbol': curr.custom_symbol,
                }
            })

        return JsonResponse({
            'success': True,
            'currencies': currencies,
            'count': len(currencies)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
@require_http_methods(["POST"])
def activate_currencies(request):
    """
    Activate one or more currencies.

    POST Data:
        {
            "codes": ["USD", "EUR", "GBP"]  // Single code or array
        }

    Returns:
        {
            "success": true,
            "activated": ["USD", "EUR"],
            "already_active": ["GBP"],
            "message": "Activated 2 currencies"
        }
    """
    try:
        data = json.loads(request.body)
        codes = data.get('codes', [])

        # Ensure codes is a list
        if isinstance(codes, str):
            codes = [codes]

        if not codes:
            return JsonResponse({
                'success': False,
                'error': 'No currency codes provided'
            }, status=400)

        activated = []
        already_active = []
        invalid = []

        with transaction.atomic():
            for code in codes:
                code = code.upper()

                # Validate currency code
                if code not in CURRENCIES:
                    invalid.append(code)
                    continue

                currency, created = SupportedCurrency.objects.get_or_create(
                    code=code,
                    defaults={'is_active': True}
                )

                if created or not currency.is_active:
                    currency.is_active = True
                    currency.save(update_fields=['is_active'])
                    activated.append(code)
                else:
                    already_active.append(code)

        response = {
            'success': True,
            'activated': activated,
            'already_active': already_active,
            'message': f'Activated {len(activated)} currencies'
        }

        if invalid:
            response['invalid'] = invalid

        return JsonResponse(response)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
@require_http_methods(["POST"])
def deactivate_currencies(request):
    """
    Deactivate one or more currencies.

    POST Data:
        {
            "codes": ["USD", "EUR"]
        }

    Returns:
        {
            "success": true,
            "deactivated": ["USD"],
            "already_inactive": ["EUR"],
            "message": "Deactivated 1 currency"
        }
    """
    try:
        data = json.loads(request.body)
        codes = data.get('codes', [])

        if isinstance(codes, str):
            codes = [codes]

        if not codes:
            return JsonResponse({
                'success': False,
                'error': 'No currency codes provided'
            }, status=400)

        deactivated = []
        already_inactive = []
        not_found = []

        with transaction.atomic():
            for code in codes:
                code = code.upper()

                try:
                    currency = SupportedCurrency.objects.get(code=code)
                    if currency.is_active:
                        currency.is_active = False
                        currency.save(update_fields=['is_active'])
                        deactivated.append(code)
                    else:
                        already_inactive.append(code)
                except SupportedCurrency.DoesNotExist:
                    not_found.append(code)

        return JsonResponse({
            'success': True,
            'deactivated': deactivated,
            'already_inactive': already_inactive,
            'not_found': not_found,
            'message': f'Deactivated {len(deactivated)} currencies'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
@require_http_methods(["POST"])
def reorder_currencies(request):
    """
    Update display order of active currencies.

    POST Data:
        {
            "codes": ["EUR", "USD", "GBP"]  // Codes in desired order
        }

    Returns:
        {
            "success": true,
            "updated": 3,
            "message": "Currency order updated"
        }
    """
    try:
        data = json.loads(request.body)
        codes = data.get('codes', [])

        if not isinstance(codes, list):
            return JsonResponse({
                'success': False,
                'error': 'codes must be an array'
            }, status=400)

        updated = 0
        with transaction.atomic():
            for order, code in enumerate(codes):
                try:
                    currency = SupportedCurrency.objects.get(code=code.upper())
                    currency.order = order
                    currency.save(update_fields=['order'])
                    updated += 1
                except SupportedCurrency.DoesNotExist:
                    pass  # Skip invalid codes

        return JsonResponse({
            'success': True,
            'updated': updated,
            'message': 'Currency order updated'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
@require_http_methods(["PATCH"])
def update_currency_settings(request, code):
    """
    Update display settings for a specific currency.

    PATCH Data:
        {
            "show_flag": true,
            "show_symbol": false,
            "custom_symbol": "$US"
        }

    Returns:
        {
            "success": true,
            "currency": {
                "code": "USD",
                "settings": {...}
            }
        }
    """
    try:
        currency = SupportedCurrency.objects.get(code=code.upper())
        data = json.loads(request.body)

        # Update allowed fields
        allowed_fields = ['show_flag', 'show_symbol', 'custom_symbol']
        updated_fields = []

        for field in allowed_fields:
            if field in data:
                setattr(currency, field, data[field])
                updated_fields.append(field)

        if updated_fields:
            currency.save(update_fields=updated_fields)

        return JsonResponse({
            'success': True,
            'currency': {
                'code': currency.code,
                'settings': {
                    'show_flag': currency.show_flag,
                    'show_symbol': currency.show_symbol,
                    'custom_symbol': currency.custom_symbol,
                }
            }
        })

    except SupportedCurrency.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'Currency {code} not found'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
@require_http_methods(["POST"])
def bulk_update_currencies(request):
    """
    Bulk update multiple currency settings.

    POST Data:
        {
            "updates": [
                {"code": "USD", "is_active": true, "order": 0},
                {"code": "EUR", "is_active": true, "order": 1},
                {"code": "GBP", "is_active": false}
            ]
        }

    Returns:
        {
            "success": true,
            "updated": 3,
            "errors": []
        }
    """
    try:
        data = json.loads(request.body)
        updates = data.get('updates', [])

        if not isinstance(updates, list):
            return JsonResponse({
                'success': False,
                'error': 'updates must be an array'
            }, status=400)

        updated = 0
        errors = []

        with transaction.atomic():
            for update in updates:
                code = update.get('code', '').upper()
                if not code:
                    continue

                try:
                    currency, created = SupportedCurrency.objects.get_or_create(
                        code=code,
                        defaults={'is_active': update.get('is_active', False)}
                    )

                    # Update fields
                    for field in ['is_active', 'order', 'show_flag', 'show_symbol', 'custom_symbol']:
                        if field in update:
                            setattr(currency, field, update[field])

                    currency.save()
                    updated += 1

                except Exception as e:
                    errors.append({
                        'code': code,
                        'error': str(e)
                    })

        return JsonResponse({
            'success': len(errors) == 0,
            'updated': updated,
            'errors': errors
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
