"""
API views for the Exchange Rates app.
Provides CRUD operations for manual exchange rates.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
)

from core.api.api_descriptions import (
    VALIDATION_ERROR as API_VALIDATION_ERROR,
)

from exchange_rates.models import ManualExchangeRate
from exchange_rates.serializers import (
    ManualExchangeRateSerializer,
    ManualExchangeRateListSerializer,
    ManualExchangeRateBulkSerializer,
)

import logging

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        tags=['Exchange Rates'],
        summary=_("List manual exchange rates"),
        description=_("Returns all manual exchange rates for the current site. "
                    "Staff authentication required."),
        responses={200: ManualExchangeRateListSerializer(many=True)},
    ),
    create=extend_schema(
        tags=['Exchange Rates'],
        summary=_("Create a manual exchange rate"),
        description=_("Create a new manual exchange rate for a currency pair. "
                    "Only one rate per currency pair is allowed. "
                    "Manual rates take precedence over provider rates when active."),
        request=ManualExchangeRateSerializer,
        responses={
            201: OpenApiResponse(description=_("Rate created successfully")),
            400: OpenApiResponse(description=_("Validation error (duplicate pair, invalid rate, etc.)")),
        },
    ),
    retrieve=extend_schema(
        tags=['Exchange Rates'],
        summary=_("Get manual exchange rate details"),
        description=_("Retrieve a specific manual exchange rate by ID."),
        responses={200: ManualExchangeRateSerializer},
    ),
    update=extend_schema(
        tags=['Exchange Rates'],
        summary=_("Update a manual exchange rate"),
        description=_("Fully update a manual exchange rate. All fields required."),
        request=ManualExchangeRateSerializer,
        responses={
            200: OpenApiResponse(description=_("Rate updated successfully")),
            400: OpenApiResponse(description=API_VALIDATION_ERROR),
        },
    ),
    partial_update=extend_schema(
        tags=['Exchange Rates'],
        summary=_("Partially update a manual exchange rate"),
        description=_("Update specific fields of a manual exchange rate. "
                    "Commonly used to update just the rate value."),
        request=ManualExchangeRateSerializer,
        responses={
            200: OpenApiResponse(description=_("Rate updated successfully")),
            400: OpenApiResponse(description=API_VALIDATION_ERROR),
        },
    ),
    destroy=extend_schema(
        tags=['Exchange Rates'],
        summary=_("Delete a manual exchange rate"),
        description=_("Permanently delete a manual exchange rate. "
                    "The system will fall back to provider rates for this currency pair."),
        responses={
            200: OpenApiResponse(description=_("Rate deleted successfully")),
        },
    ),
)
class ManualExchangeRateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing manual exchange rates.

    list:    GET    /api/exchange-rates/manual/
    create:  POST   /api/exchange-rates/manual/
    retrieve: GET   /api/exchange-rates/manual/{id}/
    update:  PUT    /api/exchange-rates/manual/{id}/
    partial: PATCH  /api/exchange-rates/manual/{id}/
    destroy: DELETE /api/exchange-rates/manual/{id}/
    """
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return ManualExchangeRateListSerializer
        if self.action == 'bulk_upsert':
            return ManualExchangeRateBulkSerializer
        return ManualExchangeRateSerializer

    def get_queryset(self):
        return ManualExchangeRate.objects.filter(
            site=Site.objects.get(pk=1)
        ).order_by('base_currency', 'target_currency')

    def _invalidate_rate_cache(self, base_currency, target_currency):
        """Invalidate Redis cache for a currency pair"""
        cache_key = f'exchange_rate:{base_currency}:{target_currency}'
        cache.delete(cache_key)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(site=Site.objects.get(pk=1))
            self._invalidate_rate_cache(
                serializer.validated_data['base_currency'],
                serializer.validated_data['target_currency']
            )
            return Response({
                'success': True,
                'message': str(_('Manual exchange rate created successfully.')),
                'data': ManualExchangeRateSerializer(serializer.instance).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': str(_('Failed to create manual exchange rate.')),
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            self._invalidate_rate_cache(instance.base_currency, instance.target_currency)
            # Also invalidate new pair if currencies changed
            new_base = serializer.validated_data.get('base_currency', instance.base_currency)
            new_target = serializer.validated_data.get('target_currency', instance.target_currency)
            if new_base != instance.base_currency or new_target != instance.target_currency:
                self._invalidate_rate_cache(new_base, new_target)
            return Response({
                'success': True,
                'message': str(_('Manual exchange rate updated successfully.')),
                'data': ManualExchangeRateSerializer(serializer.instance).data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'message': str(_('Failed to update manual exchange rate.')),
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        base = instance.base_currency
        target = instance.target_currency
        instance.delete()
        self._invalidate_rate_cache(base, target)
        return Response({
            'success': True,
            'message': str(_('Manual exchange rate deleted successfully.'))
        }, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Exchange Rates'],
        summary=_("Toggle manual rate active status"),
        description=_("Toggle the active/inactive status of a manual exchange rate. "
                    "When deactivated, the system falls back to provider rates."),
        responses={
            200: OpenApiResponse(description=_("Status toggled successfully")),
        },
    )
    @action(detail=True, methods=['post'], url_path='toggle-active')
    def toggle_active(self, request, pk=None):
        """POST /api/exchange-rates/manual/{id}/toggle-active/"""
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save(update_fields=['is_active', 'updated_at'])
        self._invalidate_rate_cache(instance.base_currency, instance.target_currency)
        return Response({
            'success': True,
            'is_active': instance.is_active,
            'message': str(_('Rate {} successfully').format(
                _('activated') if instance.is_active else _('deactivated')
            )),
            'data': ManualExchangeRateSerializer(instance).data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Exchange Rates'],
        summary=_("Bulk create or update manual rates"),
        description=_("Create or update multiple manual exchange rates in a single request. "
                    "Each rate is identified by its base_currency + target_currency pair. "
                    "If a rate for the pair already exists, it is updated; otherwise a new one is created. "
                    "Maximum 100 rates per request.\n\n"
                    "**Request body example:**\n"
                    "```json\n"
                    "{\n"
                    "  \"rates\": [\n"
                    "    {\"base_currency\": \"USD\", \"target_currency\": \"EUR\", \"rate\": \"0.92\"},\n"
                    "    {\"base_currency\": \"USD\", \"target_currency\": \"GBP\", \"rate\": \"0.79\", \"is_active\": true}\n"
                    "  ]\n"
                    "}\n"
                    "```"),
        request=ManualExchangeRateBulkSerializer,
        responses={
            200: OpenApiResponse(description=_("Bulk operation completed")),
            400: OpenApiResponse(description=API_VALIDATION_ERROR),
        },
    )
    @action(detail=False, methods=['post'], url_path='bulk')
    def bulk_upsert(self, request):
        """POST /api/exchange-rates/manual/bulk/"""
        serializer = ManualExchangeRateBulkSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': str(_('Invalid request data.')),
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        rates_data = serializer.validated_data['rates']
        site = Site.objects.get(pk=1)
        created_count = 0
        updated_count = 0
        errors = []

        with transaction.atomic():
            for i, rate_data in enumerate(rates_data):
                base = rate_data.get('base_currency', '').upper().strip()
                target = rate_data.get('target_currency', '').upper().strip()
                rate_value = rate_data.get('rate')

                if not base or not target or rate_value is None:
                    errors.append({
                        'index': i,
                        'error': str(_('base_currency, target_currency, and rate are required.'))
                    })
                    continue

                if base == target:
                    errors.append({
                        'index': i,
                        'error': str(_('Base and target currencies must be different.'))
                    })
                    continue

                try:
                    from decimal import Decimal, InvalidOperation
                    rate_decimal = Decimal(str(rate_value))
                    if rate_decimal <= 0:
                        errors.append({
                            'index': i,
                            'error': str(_('Exchange rate must be greater than zero.'))
                        })
                        continue
                except (InvalidOperation, ValueError):
                    errors.append({
                        'index': i,
                        'error': str(_('Invalid rate value.'))
                    })
                    continue

                defaults = {'rate': rate_decimal}
                if 'is_active' in rate_data:
                    defaults['is_active'] = bool(rate_data['is_active'])
                if 'notes' in rate_data:
                    defaults['notes'] = str(rate_data['notes'])

                _obj, created = ManualExchangeRate.objects.update_or_create(
                    site=site,
                    base_currency=base,
                    target_currency=target,
                    defaults=defaults
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

                self._invalidate_rate_cache(base, target)

        return Response({
            'success': len(errors) == 0,
            'message': str(_('Bulk operation completed: %(created)d created, %(updated)d updated.') % {
                'created': created_count, 'updated': updated_count
            }),
            'created': created_count,
            'updated': updated_count,
            'errors': errors if errors else None
        }, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Exchange Rates'],
        summary=_("Sync manual rates from provider"),
        description=_("Auto-populate manual exchange rates from the latest provider rates. "
                    "Rates marked as locked (exclude_from_auto_sync) will be skipped. "
                    "Creates new manual rates or updates existing unlocked ones."),
        responses={
            200: OpenApiResponse(description=_("Sync completed")),
            500: OpenApiResponse(description=_("Sync failed")),
        },
    )
    @action(detail=False, methods=['post'], url_path='sync-from-provider')
    def sync_from_provider(self, request):
        """POST /api/exchange-rates/manual/sync-from-provider/"""
        from core.models import SiteSettings
        from exchange_rates.models import ExchangeRate
        from decimal import Decimal
        from django.utils import timezone

        try:
            site = Site.objects.get(pk=1)
            settings = SiteSettings.get_settings()
            base_currency = settings.default_currency

            # Get target currencies
            if settings.supported_currencies:
                target_currencies = [c for c in settings.supported_currencies if c != base_currency]
            else:
                from core.utils.currency_helpers import get_common_currencies
                target_currencies = [code for code, _ in get_common_currencies() if code != base_currency]

            created_count = 0
            updated_count = 0
            skipped_count = 0
            errors = []

            for target_currency in target_currencies:
                # Check if locked
                existing = ManualExchangeRate.objects.filter(
                    site=site, base_currency=base_currency, target_currency=target_currency
                ).first()

                if existing and existing.exclude_from_auto_sync:
                    skipped_count += 1
                    continue

                # Get provider rate from DB cache
                db_rate = ExchangeRate.objects.filter(
                    base_currency=base_currency,
                    target_currency=target_currency,
                    provider_account__is_active=True
                ).order_by('-fetched_at').first()

                if not db_rate:
                    errors.append({
                        'currency': f'{base_currency}/{target_currency}',
                        'error': str(_('No provider rate available'))
                    })
                    continue

                try:
                    _obj, was_created = ManualExchangeRate.objects.update_or_create(
                        site=site,
                        base_currency=base_currency,
                        target_currency=target_currency,
                        defaults={
                            'rate': db_rate.rate,
                            'is_active': True,
                            'notes': str(_('Synced from provider on %(date)s') % {
                                'date': timezone.now().strftime('%Y-%m-%d %H:%M')
                            }),
                        }
                    )

                    self._invalidate_rate_cache(base_currency, target_currency)

                    if was_created:
                        created_count += 1
                    else:
                        updated_count += 1
                except Exception as e:
                    errors.append({
                        'currency': f'{base_currency}/{target_currency}',
                        'error': str(e)
                    })

            return Response({
                'success': len(errors) == 0,
                'message': str(
                    _('Sync complete: %(created)d created, %(updated)d updated, %(skipped)d locked (skipped)') % {
                        'created': created_count, 'updated': updated_count, 'skipped': skipped_count
                    }
                ),
                'created': created_count,
                'updated': updated_count,
                'skipped': skipped_count,
                'errors': errors if errors else None
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Error in sync_from_provider API: %s", e, exc_info=True)
            return Response({
                'success': False,
                'message': str(_('An error occurred during sync.'))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
