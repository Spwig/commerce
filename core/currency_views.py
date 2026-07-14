"""
Views for multi-currency support.
"""

import json
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from moneyed import CURRENCIES

from core.models import SiteSettings

logger = logging.getLogger(__name__)


@require_POST
def set_currency(request):
    """
    AJAX view to set the user's selected currency.

    Expects JSON body:
        {"currency": "EUR"}

    Returns:
        JSON response with success status
    """
    try:
        # Parse JSON body
        data = json.loads(request.body)
        currency_code = data.get("currency", "").upper()

        if not currency_code:
            return JsonResponse(
                {"success": False, "error": "Currency code is required"}, status=400
            )

        # Validate currency code
        if currency_code not in CURRENCIES:
            return JsonResponse(
                {"success": False, "error": f"Invalid currency code: {currency_code}"}, status=400
            )

        # Check if currency is in supported currencies
        settings = SiteSettings.get_settings()
        if settings.supported_currencies and currency_code not in settings.supported_currencies:
            return JsonResponse(
                {"success": False, "error": f"Currency not supported: {currency_code}"}, status=400
            )

        # Set currency in session
        request.session["currency"] = currency_code

        logger.info(
            f"Currency changed to {currency_code} for session {request.session.session_key}"
        )

        return JsonResponse(
            {
                "success": True,
                "currency": currency_code,
                "message": f"Currency changed to {currency_code}",
            }
        )

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON in request body"}, status=400)

    except Exception as e:
        logger.error(f"Error setting currency: {e}")
        return JsonResponse(
            {"success": False, "error": "An error occurred while changing currency"}, status=500
        )
