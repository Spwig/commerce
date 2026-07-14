"""
Celery tasks for customer metrics and LTV calculations
"""

import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.celery_utils import BackgroundDBTask

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task(name="customers.calculate_customer_ltv")
def calculate_customer_ltv_task(user_id):
    """
    Calculate LTV for a single customer
    Args:
        user_id: ID of the user to calculate LTV for
    """
    from customers.models import CustomerMetrics, LTVSettings
    from customers.services.cohort_service import CohortService
    from customers.services.probabilistic_ltv_service import ProbabilisticLTVService

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return {"success": False, "error": "User not found"}

    # Get calculation method from settings
    settings = LTVSettings.get_settings()
    method = settings.calculation_method

    try:
        if method == "simple":
            # Simple RFM-based calculation (already in calculate_for_user)
            CustomerMetrics.calculate_for_user(user)
            return {"success": True, "method": "simple", "user_id": user_id}

        elif method == "cohort":
            # First ensure customer metrics are up to date
            metrics = CustomerMetrics.calculate_for_user(user)

            if metrics and metrics.cohort_month:
                # Build/update cohort if needed
                CohortService.build_all_cohorts()

                # Update customer's LTV based on cohort
                result = CohortService.update_customer_cohort_ltv()
                return {
                    "success": True,
                    "method": "cohort",
                    "user_id": user_id,
                    "customers_updated": result.get("customers_updated", 0),
                }
            else:
                # Fall back to simple if no cohort data
                return {"success": True, "method": "simple (fallback)", "user_id": user_id}

        elif method == "probabilistic":
            # Probabilistic BG/NBD calculation
            service = ProbabilisticLTVService()

            # Fit models (cached internally)
            fit_result = service.fit_models()

            if not fit_result["success"]:
                # Fall back to simple if fitting fails
                CustomerMetrics.calculate_for_user(user)
                return {
                    "success": True,
                    "method": "simple (fallback)",
                    "user_id": user_id,
                    "error": fit_result.get("error"),
                }

            # Predict for this customer
            prediction = service.predict_customer_ltv(user)

            if prediction["success"]:
                from djmoney.money import Money

                from customers.services.probabilistic_ltv_service import (
                    ProbabilisticLTVService as PLTVService,
                )

                metrics = CustomerMetrics.objects.get(user=user)
                default_currency = PLTVService.get_default_currency()

                metrics.lifetime_value = Money(prediction["ltv"], default_currency)
                metrics.probability_alive = prediction["probability_alive"]
                metrics.predicted_purchases_12m = prediction["predicted_purchases"]
                metrics.ltv_confidence_score = prediction["confidence"]
                metrics.ltv_calculation_method = "probabilistic"
                metrics.ltv_last_calculated = timezone.now()
                metrics.save()

                return {
                    "success": True,
                    "method": "probabilistic",
                    "user_id": user_id,
                    "ltv": prediction["ltv"],
                }
            else:
                # Fall back to simple
                CustomerMetrics.calculate_for_user(user)
                return {
                    "success": True,
                    "method": "simple (fallback)",
                    "user_id": user_id,
                    "error": prediction.get("error"),
                }

    except Exception as e:
        logger.error(f"Error calculating LTV for user {user_id}: {str(e)}")
        return {"success": False, "error": str(e), "user_id": user_id}


@shared_task(name="customers.calculate_all_customer_ltv", base=BackgroundDBTask, ignore_result=True)
def calculate_all_customer_ltv_task():
    """
    Calculate LTV for all customers (nightly batch job)
    """
    from customers.models import CustomerMetrics, LTVSettings
    from customers.services.cohort_service import CohortService
    from customers.services.probabilistic_ltv_service import ProbabilisticLTVService

    logger.info("Starting nightly LTV calculation for all customers")

    # Get calculation method from settings
    settings = LTVSettings.get_settings()
    method = settings.calculation_method

    start_time = timezone.now()

    try:
        if method == "simple":
            # Simple RFM-based calculation for all customers
            customers_updated = 0
            customers = User.objects.filter(is_active=True).exclude(username__startswith="guest_")

            for user in customers:
                try:
                    CustomerMetrics.calculate_for_user(user)
                    customers_updated += 1
                except Exception as e:
                    logger.error(f"Error calculating metrics for user {user.id}: {str(e)}")

            result = {
                "success": True,
                "method": "simple",
                "customers_updated": customers_updated,
                "duration_seconds": (timezone.now() - start_time).total_seconds(),
            }

        elif method == "cohort":
            # Cohort-based calculation
            # Step 1: Build cohorts
            cohort_result = CohortService.build_all_cohorts()

            # Step 2: Calculate cohort metrics
            CohortService.calculate_cohort_metrics()

            # Step 3: Update customer LTV from cohorts
            update_result = CohortService.update_customer_cohort_ltv()

            result = {
                "success": True,
                "method": "cohort",
                "cohorts_created": cohort_result.get("cohorts_created", 0),
                "cohorts_updated": cohort_result.get("cohorts_updated", 0),
                "customers_updated": update_result.get("customers_updated", 0),
                "duration_seconds": (timezone.now() - start_time).total_seconds(),
            }

        elif method == "probabilistic":
            # Probabilistic BG/NBD calculation
            service = ProbabilisticLTVService()
            result = service.update_all_customer_ltv()
            result["duration_seconds"] = (timezone.now() - start_time).total_seconds()

        else:
            result = {"success": False, "error": f"Unknown calculation method: {method}"}

        # Update settings with last run time
        if result.get("success"):
            settings.last_calculation_run = timezone.now()
            settings.save(update_fields=["last_calculation_run"])

        logger.info(f"Completed nightly LTV calculation: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in nightly LTV calculation: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "duration_seconds": (timezone.now() - start_time).total_seconds(),
        }


@shared_task(name="customers.rebuild_cohorts", base=BackgroundDBTask, ignore_result=True)
def rebuild_cohorts_task():
    """
    Rebuild all customer cohorts and recalculate metrics
    """
    from customers.services.cohort_service import CohortService

    logger.info("Starting cohort rebuild task")
    start_time = timezone.now()

    try:
        # Step 1: Build cohorts
        cohort_result = CohortService.build_all_cohorts()

        # Step 2: Calculate metrics for all cohorts
        metrics_result = CohortService.calculate_cohort_metrics()

        result = {
            "success": True,
            "cohorts_created": cohort_result.get("cohorts_created", 0),
            "cohorts_updated": cohort_result.get("cohorts_updated", 0),
            "metrics_created": metrics_result.get("metrics_created", 0),
            "metrics_updated": metrics_result.get("metrics_updated", 0),
            "duration_seconds": (timezone.now() - start_time).total_seconds(),
        }

        logger.info(f"Completed cohort rebuild: {result}")
        return result

    except Exception as e:
        logger.error(f"Error rebuilding cohorts: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "duration_seconds": (timezone.now() - start_time).total_seconds(),
        }


@shared_task(name="customers.fit_probabilistic_models", base=BackgroundDBTask)
def fit_probabilistic_models_task():
    """
    Fit BG/NBD and Gamma-Gamma models
    (Can be run separately from LTV calculation)
    """
    from customers.services.probabilistic_ltv_service import ProbabilisticLTVService

    logger.info("Starting probabilistic model fitting")
    start_time = timezone.now()

    try:
        service = ProbabilisticLTVService()
        result = service.fit_models()
        result["duration_seconds"] = (timezone.now() - start_time).total_seconds()

        logger.info(f"Completed model fitting: {result}")
        return result

    except Exception as e:
        logger.error(f"Error fitting probabilistic models: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "duration_seconds": (timezone.now() - start_time).total_seconds(),
        }


@shared_task(name="customers.check_ltv_data_quality", base=BackgroundDBTask)
def check_ltv_data_quality_task():
    """
    Check if data quality is sufficient for advanced LTV methods
    """
    from customers.services.probabilistic_ltv_service import ProbabilisticLTVService

    try:
        quality_check = ProbabilisticLTVService.check_data_quality()
        logger.info(f"LTV data quality check: {quality_check}")
        return quality_check

    except Exception as e:
        logger.error(f"Error checking data quality: {str(e)}")
        return {"success": False, "error": str(e)}
