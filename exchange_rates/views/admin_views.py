"""
Admin AJAX views for exchange rate provider account management
Handles quick actions, bulk operations, and list filtering
"""

import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST

from exchange_rates.models import ExchangeRateProviderAccount, ManualExchangeRate
from exchange_rates.providers.registry import ProviderRegistry
from exchange_rates.utils.encryption import decrypt_credentials

logger = logging.getLogger(__name__)


@staff_member_required
@require_GET
def filter_exchange_rate_providers(request):
    """
    AJAX endpoint for filtering exchange rate providers in admin.

    Supports filtering by:
    - search: Provider name
    - sync_status: success, error, pending
    - is_active: active/inactive
    - component: Component slug
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Get filter parameters (support both naming conventions)
    search = request.GET.get("search", "").strip() or request.GET.get("q", "").strip()
    sync_status = request.GET.get("sync_status", "").strip()
    is_active = request.GET.get("is_active", "").strip()
    component = request.GET.get("component", "").strip()

    # Build query
    providers = ExchangeRateProviderAccount.objects.select_related("component", "site").order_by(
        "-is_primary", "-is_active", "priority", "name"
    )

    # Apply filters
    if search:
        providers = providers.filter(
            Q(name__icontains=search) | Q(component__name__icontains=search)
        )

    if sync_status:
        providers = providers.filter(sync_status=sync_status)

    if is_active == "1" or is_active.lower() == "active":
        providers = providers.filter(is_active=True)
    elif is_active == "0" or is_active.lower() == "inactive":
        providers = providers.filter(is_active=False)

    if component:
        providers = providers.filter(component__slug=component)

    # Render results - need to wrap in grid container
    provider_cards_html = "".join(
        [
            render_to_string(
                "admin/exchange_rates/exchangerateprovideraccount/provider_card.html",
                {
                    "provider": provider,
                },
                request=request,
            )
            for provider in providers
        ]
    )

    if providers.exists():
        html = f'<div class="providers-grid">{provider_cards_html}</div>'
    else:
        empty_title = _("No provider accounts found")
        empty_text = _("Try adjusting your filters or search query.")
        html = (
            f'<div class="empty-state">'
            f'<i class="fas fa-exchange-alt"></i>'
            f"<h2>{empty_title}</h2>"
            f"<p>{empty_text}</p>"
            f"</div>"
        )

    return JsonResponse({"html": html, "count": providers.count()})


@staff_member_required
@require_POST
def toggle_provider_active(request, provider_id):
    """Toggle provider account active status via AJAX"""
    try:
        provider = get_object_or_404(ExchangeRateProviderAccount, id=provider_id)

        # Toggle active status
        provider.is_active = not provider.is_active
        provider.save()

        return JsonResponse(
            {
                "success": True,
                "is_active": provider.is_active,
                "message": _("Provider {} successfully").format(
                    _("enabled") if provider.is_active else _("disabled")
                ),
            }
        )
    except Exception as e:
        logger.error("Error toggling provider %s active status: %s", provider_id, e, exc_info=True)
        return JsonResponse(
            {"success": False, "message": _("An error occurred while updating the provider.")},
            status=400,
        )


@staff_member_required
@require_POST
def set_provider_primary(request, provider_id):
    """Set provider account as primary via AJAX"""
    try:
        provider = get_object_or_404(ExchangeRateProviderAccount, id=provider_id)

        # Use transaction to ensure atomic operation
        with transaction.atomic():
            # Remove primary from all other providers for this site
            ExchangeRateProviderAccount.objects.filter(site=provider.site).update(is_primary=False)

            # Set this provider as primary
            provider.is_primary = True
            provider.save()

        return JsonResponse(
            {
                "success": True,
                "message": _('"{}" set as primary provider').format(
                    provider.name or provider.component.name
                ),
            }
        )
    except Exception as e:
        logger.error("Error setting provider %s as primary: %s", provider_id, e, exc_info=True)
        return JsonResponse(
            {
                "success": False,
                "message": _("An error occurred while setting the primary provider."),
            },
            status=400,
        )


@staff_member_required
@require_POST
def sync_provider_rates(request, provider_id):
    """Sync exchange rates from provider via AJAX"""
    try:
        provider = get_object_or_404(ExchangeRateProviderAccount, id=provider_id)

        # Get provider class from registry
        provider_class = ProviderRegistry.get_provider(provider.component.slug)

        if not provider_class:
            return JsonResponse(
                {"success": False, "message": _("Provider implementation not found")}, status=404
            )

        # Decrypt credentials
        try:
            credentials = decrypt_credentials(provider.credentials)
        except Exception as decrypt_error:
            logger.error(
                "Failed to decrypt credentials for provider %s: %s",
                provider_id,
                decrypt_error,
                exc_info=True,
            )
            return JsonResponse(
                {
                    "success": False,
                    "message": _(
                        "Failed to decrypt provider credentials. Please reconfigure the provider."
                    ),
                },
                status=500,
            )

        # Create provider instance
        provider_instance = provider_class(credentials=credentials, config=provider.settings or {})

        # Fetch exchange rates
        try:
            # Get base currency and enabled currencies from site settings
            from core.models import SiteSettings

            site_settings = SiteSettings.objects.first()

            if not site_settings:
                return JsonResponse(
                    {"success": False, "message": _("Site settings not configured")}, status=400
                )

            # Get base currency from site settings
            base_currency = site_settings.default_currency or "USD"

            # Fetch ALL rates from provider for the base currency
            # The provider will return all available rates, not just active ones
            rates = provider_instance.get_rates(base_currency)

            logger.info(f"Provider returned {len(rates)} exchange rates")

            if not rates:
                provider.sync_status = "error"
                provider.sync_error_message = _("No rates returned from provider")
                provider.save(update_fields=["sync_status", "sync_error_message"])

                return JsonResponse(
                    {"success": False, "message": _("No rates returned from provider")}
                )

            # Update ExchangeRate model with fetched rates
            from decimal import Decimal

            from exchange_rates.models import ExchangeRate

            updated_count = 0
            for target_currency, rate in rates.items():
                if target_currency == base_currency:
                    continue

                try:
                    ExchangeRate.objects.update_or_create(
                        base_currency=base_currency,
                        target_currency=target_currency,
                        provider_account=provider,
                        defaults={"rate": Decimal(str(rate)), "fetched_at": timezone.now()},
                    )
                    updated_count += 1
                except Exception as e:
                    logger.error(f"Failed to save rate for {target_currency}: {e}")

            logger.info(f"Successfully saved {updated_count} exchange rates to database")

            # Update provider sync status
            provider.sync_status = "success"
            provider.sync_error_message = ""
            provider.last_sync_at = timezone.now()
            provider.save(update_fields=["sync_status", "sync_error_message", "last_sync_at"])

            return JsonResponse(
                {
                    "success": True,
                    "message": _("Successfully synced {} exchange rate(s)").format(updated_count),
                    "stats": {
                        "rates_received": len(rates),
                        "rates_saved": updated_count,
                        "base_currency": base_currency,
                        "provider": provider.component.name,
                    },
                }
            )

        except Exception as sync_error:
            # Update provider with error status
            logger.error(
                "Error syncing rates for provider %s: %s", provider_id, sync_error, exc_info=True
            )
            provider.sync_status = "error"
            provider.sync_error_message = str(sync_error)
            provider.save(update_fields=["sync_status", "sync_error_message"])

            return JsonResponse(
                {
                    "success": False,
                    "message": _(
                        "Failed to sync exchange rates. Check the provider configuration."
                    ),
                },
                status=500,
            )

    except Exception as e:
        logger.error(
            "Unexpected error in sync_provider_rates for %s: %s", provider_id, e, exc_info=True
        )
        return JsonResponse(
            {"success": False, "error": _("An unexpected error occurred.")}, status=500
        )


@staff_member_required
@require_POST
def delete_provider(request, provider_id):
    """Delete provider account via AJAX"""
    try:
        provider = get_object_or_404(ExchangeRateProviderAccount, id=provider_id)

        provider_name = provider.name or provider.component.name
        provider.delete()

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "{}" successfully deleted').format(provider_name),
            }
        )
    except Exception as e:
        logger.error("Error deleting provider %s: %s", provider_id, e, exc_info=True)
        return JsonResponse(
            {"success": False, "message": _("An error occurred while deleting the provider.")},
            status=400,
        )


@staff_member_required
@require_POST
def provider_bulk_action(request):
    """Handle bulk actions on provider accounts via AJAX"""
    try:
        data = json.loads(request.body)
        action = data.get("action")
        provider_ids = data.get("provider_ids", [])

        if not action or not provider_ids:
            return JsonResponse(
                {"success": False, "message": _("Invalid action or no providers selected")},
                status=400,
            )

        providers = ExchangeRateProviderAccount.objects.filter(id__in=provider_ids)

        if action == "enable":
            providers.update(is_active=True)
            message = _("{} provider(s) enabled").format(providers.count())

        elif action == "disable":
            providers.update(is_active=False)
            message = _("{} provider(s) disabled").format(providers.count())

        elif action == "set_primary":
            if providers.count() != 1:
                return JsonResponse(
                    {
                        "success": False,
                        "message": _("Please select exactly one provider to set as primary"),
                    },
                    status=400,
                )

            provider = providers.first()

            # Use transaction to ensure atomic operation
            with transaction.atomic():
                # Remove primary from all providers for this site
                ExchangeRateProviderAccount.objects.filter(site=provider.site).update(
                    is_primary=False
                )

                # Set selected as primary
                provider.is_primary = True
                provider.save()

            message = _('"{}" set as primary provider').format(
                provider.name or provider.component.name
            )

        elif action == "sync_rates":
            # Queue sync for each provider
            synced_count = 0
            errors = []

            for provider in providers:
                try:
                    # Get provider class
                    provider_class = ProviderRegistry.get_provider(provider.component.slug)
                    if not provider_class:
                        errors.append(f"{provider.name}: Provider implementation not found")
                        continue

                    # Decrypt credentials and create instance
                    credentials = decrypt_credentials(provider.credentials)
                    provider_class(credentials=credentials, config=provider.settings or {})

                    # Simplified sync - you may want to queue this as a background task
                    provider.sync_status = "pending"
                    provider.save(update_fields=["sync_status"])
                    synced_count += 1

                except Exception as e:
                    errors.append(f"{provider.name}: {str(e)}")

            if errors:
                message = _("{} provider(s) queued for sync, {} errors: {}").format(
                    synced_count, len(errors), "; ".join(errors)
                )
            else:
                message = _("{} provider(s) queued for sync").format(synced_count)

        elif action == "delete":
            deleted_count = providers.count()
            providers.delete()
            message = _("{} provider(s) deleted").format(deleted_count)

        else:
            return JsonResponse(
                {"success": False, "message": _("Unknown action: {}").format(action)}, status=400
            )

        return JsonResponse({"success": True, "message": message})

    except Exception as e:
        logger.error("Error in provider bulk action: %s", e, exc_info=True)
        return JsonResponse(
            {"success": False, "message": _("An error occurred while performing the bulk action.")},
            status=400,
        )


@staff_member_required
@require_POST
def toggle_manual_rate_active(request, rate_id):
    """Toggle manual exchange rate active status via AJAX"""
    try:
        rate = get_object_or_404(ManualExchangeRate, id=rate_id)

        rate.is_active = not rate.is_active
        rate.save(update_fields=["is_active", "updated_at"])

        # Invalidate Redis cache for this currency pair
        from django.core.cache import cache

        cache_key = f"exchange_rate:{rate.base_currency}:{rate.target_currency}"
        cache.delete(cache_key)

        return JsonResponse(
            {
                "success": True,
                "is_active": rate.is_active,
                "message": _("Rate {} successfully").format(
                    _("activated") if rate.is_active else _("deactivated")
                ),
                "active_label": str(_("Active")),
                "inactive_label": str(_("Inactive")),
            }
        )
    except Exception as e:
        logger.error("Error toggling manual rate %s: %s", rate_id, e, exc_info=True)
        return JsonResponse(
            {"success": False, "message": _("An error occurred while updating the rate.")},
            status=400,
        )


@staff_member_required
@require_POST
def toggle_manual_rate_locked(request, rate_id):
    """Toggle the exclude_from_auto_sync flag on a manual exchange rate via AJAX"""
    try:
        rate = get_object_or_404(ManualExchangeRate, id=rate_id)

        rate.exclude_from_auto_sync = not rate.exclude_from_auto_sync
        rate.save(update_fields=["exclude_from_auto_sync", "updated_at"])

        return JsonResponse(
            {
                "success": True,
                "exclude_from_auto_sync": rate.exclude_from_auto_sync,
                "message": _("Rate {} successfully").format(
                    _("locked") if rate.exclude_from_auto_sync else _("unlocked")
                ),
                "locked_label": str(_("Locked")),
                "unlocked_label": str(_("Unlocked")),
            }
        )
    except Exception as e:
        logger.error("Error toggling manual rate locked %s: %s", rate_id, e, exc_info=True)
        return JsonResponse(
            {"success": False, "message": _("An error occurred while updating the rate.")},
            status=400,
        )


@staff_member_required
@require_POST
def sync_from_provider(request):
    """
    Sync manual rates from provider rates.
    Creates/updates ManualExchangeRate for each supported currency pair
    WHERE exclude_from_auto_sync=False.
    """
    from django.contrib.sites.models import Site
    from django.core.cache import cache

    from core.models import SiteSettings
    from exchange_rates.models import ExchangeRate

    try:
        site = Site.objects.get(pk=1)
        settings = SiteSettings.get_settings()
        base_currency = settings.default_currency

        # Get target currencies
        if settings.supported_currencies:
            target_currencies = [c for c in settings.supported_currencies if c != base_currency]
        else:
            from core.utils.currency_helpers import get_common_currencies

            target_currencies = [
                code for code, _ in get_common_currencies() if code != base_currency
            ]

        created = 0
        updated = 0
        skipped = 0
        errors = []

        for target_currency in target_currencies:
            # Check if locked
            existing = ManualExchangeRate.objects.filter(
                site=site, base_currency=base_currency, target_currency=target_currency
            ).first()

            if existing and existing.exclude_from_auto_sync:
                skipped += 1
                continue

            # Get provider rate from DB cache
            db_rate = (
                ExchangeRate.objects.filter(
                    base_currency=base_currency,
                    target_currency=target_currency,
                    provider_account__is_active=True,
                )
                .order_by("-fetched_at")
                .first()
            )

            if not db_rate:
                errors.append(f"No provider rate for {base_currency}/{target_currency}")
                continue

            try:
                _obj, was_created = ManualExchangeRate.objects.update_or_create(
                    site=site,
                    base_currency=base_currency,
                    target_currency=target_currency,
                    defaults={
                        "rate": db_rate.rate,
                        "is_active": True,
                        "notes": _("Synced from provider on %(date)s")
                        % {"date": timezone.now().strftime("%Y-%m-%d %H:%M")},
                    },
                )

                # Invalidate Redis cache
                cache.delete(f"exchange_rate:{base_currency}:{target_currency}")

                if was_created:
                    created += 1
                else:
                    updated += 1
            except Exception as e:
                errors.append(f"{base_currency}/{target_currency}: {str(e)}")

        return JsonResponse(
            {
                "success": len(errors) == 0,
                "message": _(
                    "Sync complete: %(created)d created, %(updated)d updated, %(skipped)d locked (skipped)"
                )
                % {"created": created, "updated": updated, "skipped": skipped},
                "created": created,
                "updated": updated,
                "skipped": skipped,
                "errors": errors if errors else None,
            }
        )

    except Exception as e:
        logger.error("Error in sync_from_provider: %s", e, exc_info=True)
        return JsonResponse(
            {"success": False, "message": _("An error occurred during sync.")}, status=500
        )
