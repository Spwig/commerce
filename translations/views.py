import json
import logging
import os

import psutil
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import models
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


def _is_shared_fleet():
    """Check if this is a shared fleet hosted installation."""
    from core.license import get_license_manager

    return get_license_manager().is_shared_fleet()


def shared_fleet_blocked(view_func):
    """Block view for shared fleet installations (translator is managed by Spwig)."""
    from functools import wraps

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if _is_shared_fleet():
            return JsonResponse(
                {
                    "success": False,
                    "error": _(
                        "This feature is not available on your hosting plan. "
                        "The translation service is managed by Spwig."
                    ),
                },
                status=403,
            )
        return view_func(request, *args, **kwargs)

    return wrapper


from .client import get_translator_client
from .docker_utils import DockerManager
from .models import (
    InstalledModel,
    SiteLanguage,
    TranslationJob,
    TranslationMeta,
    TranslationProvider,
    TranslationProviderAccount,
)


def get_quantization_friendly_name(quantization, model_id=None):
    """Get friendly name for quantization level"""
    # Model-specific friendly names
    model_names = {
        "m2m100_418m": "M2M100 Standard",
        "m2m100_1.2b": "M2M100 Premium",
        "nllb_200": "NLLB 200+",
    }

    # Quantization quality names
    quality_names = {
        "int8": "Speed Priority",
        "int16": "Balanced",
        "float16": "Quality",
        "float32": "Maximum Quality",
        "fp32": "Maximum Quality",
    }

    quality = quality_names.get(quantization, quantization)

    if model_id and model_id in model_names:
        return f"{model_names[model_id]} - {quality}"
    return quality


@staff_member_required
def dashboard_view(request):
    """Main translation service dashboard"""

    # Get translator service status
    client = get_translator_client()
    service_info = client.get_system_info()

    # Statistics
    stats = {
        "total_providers": TranslationProvider.objects.count(),
        "active_providers": TranslationProvider.objects.filter(is_active=True).count(),
        "pending_jobs": TranslationJob.objects.filter(status="pending").count(),
        "completed_jobs": TranslationJob.objects.filter(status="completed").count(),
        "failed_jobs": TranslationJob.objects.filter(status="failed").count(),
        "locked_translations": TranslationMeta.objects.filter(is_locked=True).count(),
        "installed_models": InstalledModel.objects.filter(is_downloaded=True).count(),
        "total_characters": TranslationJob.objects.aggregate(total=Sum("total_characters"))["total"]
        or 0,
    }

    # Recent jobs
    recent_jobs = TranslationJob.objects.select_related("provider", "created_by")[:10]

    # Active providers
    providers = TranslationProvider.objects.filter(is_active=True).order_by("-priority")

    # System validation (skip for shared fleet — translator is managed by Spwig)
    is_shared_fleet = _is_shared_fleet()
    if is_shared_fleet:
        system_check = {
            "meets_requirements": True,
            "cpu_cores": 0,
            "ram_gb": 0,
            "disk_free_gb": 0,
            "warnings": [],
        }
    else:
        system_info = psutil.virtual_memory()
        cpu_count = psutil.cpu_count()
        disk = psutil.disk_usage("/")

        system_check = {
            "meets_requirements": True,
            "cpu_cores": cpu_count,
            "ram_gb": system_info.total / (1024**3),
            "disk_free_gb": disk.free / (1024**3),
            "warnings": [],
        }

        if cpu_count < 4:
            system_check["meets_requirements"] = False
            system_check["warnings"].append(
                _("CPU: %(cores)d cores (minimum: 4)") % {"cores": cpu_count}
            )

        if system_info.total / (1024**3) < 8:
            system_check["meets_requirements"] = False
            system_check["warnings"].append(
                _("RAM: %(ram).1fGB (minimum: 8GB)") % {"ram": system_info.total / (1024**3)}
            )

        if disk.free / (1024**3) < 3:
            system_check["meets_requirements"] = False
            system_check["warnings"].append(
                _("Disk: %(disk).1fGB free (minimum: 3GB)") % {"disk": disk.free / (1024**3)}
            )

    # Translation coverage
    from .coverage_service import TranslationCoverageService

    try:
        coverage = TranslationCoverageService().get_site_coverage()
    except Exception as e:
        logger.warning(f"Coverage calculation failed: {e}")
        coverage = {
            "overall_percentage": 0,
            "has_languages": False,
            "languages": [],
            "content_types": [],
        }

    context = {
        "title": _("Translation Service Dashboard"),
        "system_check": system_check,
        "service_info": service_info,
        "stats": stats,
        "recent_jobs": recent_jobs,
        "providers": providers,
        "translator_enabled": os.getenv("TRANSLATOR_ENABLED", "true").lower() == "true",
        "coverage": coverage,
        "is_shared_fleet": is_shared_fleet,
    }

    return render(request, "admin/translations/dashboard.html", context)


def sync_models_with_service(client):
    """Sync Django database with Docker service model state"""
    if not client or not client.is_available():
        return

    try:
        # Get actual models from Docker service
        service_models = client.get_models()
        system_info = client.get_system_info()
        # Delegate to the data-based sync function
        sync_models_with_service_data(service_models, system_info)
    except Exception as e:
        logger.error(f"Error syncing models: {e}")


def sync_models_with_service_data(service_models, system_info):
    """Sync Django database with Docker service model state using provided data"""
    if not service_models:
        return

    try:
        # Get current loaded model from Docker
        loaded_model_name = system_info.get("model_name") if system_info else None

        # Map of model IDs we expect (with underscores)
        expected_models = {
            "m2m100_418m": {
                "display_name": "M2M100 Standard",
                "version": "1.0.0",
                "model_type": "M2M100",
                "size_mb": 1500.0,
                "languages": 100,
                "device": "cpu",
            },
            "m2m100_1.2b": {
                "display_name": "M2M100 Premium",
                "version": "1.2.0",
                "model_type": "M2M100",
                "size_mb": 4800.0,
                "languages": 100,
                "device": "cpu",
            },
            "nllb_200": {
                "display_name": "NLLB 200+",
                "version": "1.0.0",
                "model_type": "NLLB",
                "size_mb": 2400.0,
                "languages": 200,
                "device": "cpu",
            },
        }

        # Track which models exist on disk
        models_on_disk = set()

        if service_models:
            for svc_model in service_models:
                if isinstance(svc_model, dict):
                    model_name = svc_model.get("name", "")
                    # Handle both naming conventions
                    if model_name.replace("-", "_") in expected_models:
                        model_name = model_name.replace("-", "_")

                    if model_name in expected_models:
                        models_on_disk.add(model_name)

                        # Get or create the model record
                        model_info = expected_models[model_name]
                        installed_model, created = InstalledModel.objects.get_or_create(
                            name=model_name,
                            defaults={
                                "version": model_info["version"],
                                "model_type": model_info["model_type"],
                                "size_mb": svc_model.get("size_mb", model_info["size_mb"]),
                                "languages": model_info["languages"],
                                "device": svc_model.get("device", "cpu"),
                                "is_downloaded": svc_model.get("status") != "not_installed",
                                "is_active": True,
                            },
                        )

                        # Update download status based on service
                        if not created:
                            installed_model.is_downloaded = (
                                svc_model.get("status") != "not_installed"
                            )
                            installed_model.size_mb = svc_model.get(
                                "size_mb", installed_model.size_mb
                            )
                            installed_model.save()

                        # Set as default if it's the loaded model
                        if loaded_model_name and (
                            model_name == loaded_model_name
                            or model_name.replace("_", "-") == loaded_model_name
                        ):
                            # Clear other defaults
                            InstalledModel.objects.exclude(name=model_name).update(is_default=False)
                            installed_model.is_default = True
                            installed_model.save()

        # Create or update entries for all expected models
        for model_name, model_info in expected_models.items():
            if model_name not in models_on_disk:
                # Model not on disk - create/update as not downloaded
                installed_model, created = InstalledModel.objects.get_or_create(
                    name=model_name,
                    defaults={
                        "version": model_info["version"],
                        "model_type": model_info["model_type"],
                        "size_mb": model_info["size_mb"],
                        "languages": model_info["languages"],
                        "device": model_info["device"],
                        "is_downloaded": False,
                        "is_active": False,
                        "is_default": False,
                    },
                )
                if not created:
                    installed_model.is_downloaded = False
                    installed_model.save()

        # If no model is set as default but we have downloaded models, set the first one
        if not InstalledModel.objects.filter(is_default=True).exists():
            first_downloaded = InstalledModel.objects.filter(is_downloaded=True).first()
            if first_downloaded:
                first_downloaded.is_default = True
                first_downloaded.save()

    except Exception as e:
        logger.error(f"Error syncing models with service: {e}")


@staff_member_required
def local_service_view(request):
    """Local translation service management - returns template immediately for progressive loading"""
    if _is_shared_fleet():
        messages.info(
            request, _("The translation service is managed by Spwig on your hosting plan.")
        )
        return redirect("translations:dashboard")

    # Just return the template with minimal context
    # All data will be loaded via AJAX for better performance
    context = {
        "title": _("Local Translation Service"),
        # Progressive loading - all data fetched via AJAX
    }

    return render(request, "admin/translations/local_service.html", context)


@staff_member_required
def local_service_data_api(request):
    """API endpoint for local service data - returns JSON for progressive loading"""

    client = get_translator_client()

    # Sync database with service state before reading
    sync_models_with_service(client)

    # Use the optimized full-status endpoint if available
    if client.is_available():
        full_status = client.get_full_status()
        if full_status:
            # Process the data for frontend consumption
            response_data = {
                "service_available": True,
                "system": full_status.get("system", {}),
                "hardware": full_status.get("hardware", {}),
                "disk": full_status.get("disk", {}),
                "models": full_status.get("models", []),
                "quantizations": full_status.get("quantizations", {}),
            }

            # Add processed model configs for the template
            model_configs = []
            all_models = {
                "m2m100_418m": {
                    "display_name": "M2M100 Standard",
                    "description": "Fast and efficient multilingual translation model",
                    "size_gb": 1.5,
                    "languages": 100,
                    "recommended": True,
                    "high_quality": False,
                },
                "m2m100_1.2b": {
                    "display_name": "M2M100 Premium",
                    "description": "High quality translation model with superior accuracy",
                    "size_gb": 4.8,
                    "languages": 100,
                    "recommended": False,
                    "high_quality": True,
                },
                "nllb_200": {
                    "display_name": "NLLB 200+",
                    "description": "Supports over 200 languages including rare ones",
                    "size_gb": 2.4,
                    "languages": 200,
                    "recommended": False,
                    "high_quality": False,
                },
            }

            # Get installed models from database (for metadata like size_mb, languages)
            installed_models = InstalledModel.objects.all()

            # Build a lookup map for API model data (source of truth for download status)
            api_models_map = {}
            for api_model in full_status.get("models", []):
                model_name = api_model.get("name", "")
                # Handle both naming conventions (hyphens and underscores)
                normalized_name = model_name.replace("-", "_")
                api_models_map[normalized_name] = api_model

            for model_id, model_info in all_models.items():
                db_model = installed_models.filter(name=model_id).first()
                api_model = api_models_map.get(model_id)

                # Get quantizations for this model
                model_quants = full_status.get("quantizations", {}).get(model_id, [])
                available_quantizations = []
                for quant in model_quants:
                    if quant.get("exists"):
                        available_quantizations.append(quant.get("name"))

                # Check if this model is loaded
                is_loaded = full_status.get("system", {}).get("model_name") == model_id
                loaded_quant = (
                    full_status.get("system", {}).get("quantization") if is_loaded else None
                )

                # Determine is_downloaded from API (source of truth), not database
                # API returns models with 'path' field when downloaded
                is_downloaded = bool(api_model and api_model.get("path"))

                config = {
                    "id": model_id,
                    "display_name": model_info["display_name"],
                    "description": model_info["description"],
                    "size_gb": round(db_model.size_mb / 1024.0, 2)
                    if db_model and db_model.size_mb > 0
                    else model_info["size_gb"],
                    "languages": db_model.languages if db_model else model_info["languages"],
                    "recommended": model_info["recommended"],
                    "high_quality": model_info["high_quality"],
                    "is_downloaded": is_downloaded,  # Now uses API data (source of truth)
                    "is_default": db_model.is_default if db_model else False,
                    "quantizations": ["int8", "int16", "float16", "float32"],
                    "available_quantizations": available_quantizations,
                    "hardware_supported_quantizations": full_status.get("hardware", {}).get(
                        "supported_quantizations", []
                    ),
                    "is_loaded": is_loaded,
                    "loaded_quantization": loaded_quant,
                }
                model_configs.append(config)

            response_data["model_configs"] = model_configs

            # Process hardware message
            hardware_message = ""
            hardware = full_status.get("hardware", {})
            if hardware.get("gpu", {}).get("available"):
                if hardware["gpu"].get("total_memory_gb", 0) < 2.0:
                    hardware_message = "GPU detected but VRAM insufficient, using CPU"
                else:
                    gpu_name = hardware["gpu"].get("devices", [{}])[0].get("name", "Unknown GPU")
                    hardware_message = f"GPU active (CUDA) - {gpu_name}"
            elif hardware.get("cpu", {}).get("avx2"):
                hardware_message = "CPU AVX2 – good performance"
            elif hardware.get("cpu", {}).get("avx"):
                hardware_message = "CPU AVX – moderate performance"
            else:
                hardware_message = "CPU lacks vector extensions – expect slow translations"

            response_data["hardware_message"] = hardware_message

            # Add service status HTML
            model_loaded = full_status.get("system", {}).get("model_loaded", False)
            any_model_downloaded = any(mc["is_downloaded"] for mc in model_configs)

            if model_loaded:
                status_class = "online"
                status_html = (
                    f'<h3><i class="fas fa-check-circle"></i> {_("Translation Service Ready")}</h3>'
                    f"<p>{_('Your AI translation service is running and ready to translate content.')}</p>"
                    f'<p class="hardware-status">'
                    f"<strong>{_('Hardware:')}</strong> {hardware_message}"
                    f"</p>"
                )
            elif any_model_downloaded:
                status_class = "degraded"
                status_html = (
                    f'<h3><i class="fas fa-hourglass-half"></i> {_("Service Starting Up")}</h3>'
                    f"<p>{_("Translation models are installed but need to be activated. Click 'Load Model' below to start translating.")}</p>"
                )
            else:
                status_class = "offline"
                status_html = (
                    f'<h3><i class="fas fa-download"></i> {_("Setup Required")}</h3>'
                    f"<p>{_('Install a translation model below to start using the AI translation service.')}</p>"
                )

            response_data["service_status"] = {"class": status_class, "html": status_html}

            # Add quality settings for each model
            quality_settings = {}
            for config in model_configs:
                model_id = config["id"]
                qualities = []

                for quant in ["int8", "int16", "float16", "float32"]:
                    q = {
                        "name": quant,
                        "is_active": config["is_loaded"] and config["loaded_quantization"] == quant,
                        "is_available": quant in config["available_quantizations"],
                        "is_supported": quant in config["hardware_supported_quantizations"],
                        "model_downloaded": config["is_downloaded"],
                        "subtitle": {
                            "int8": _("Fastest Performance"),
                            "int16": _("Good Balance"),
                            "float16": _("Better Accuracy"),
                            "float32": _("Best Possible"),
                        }.get(quant, ""),
                        "description": {
                            "int8": _("Uses least memory. Best for high-volume translations."),
                            "int16": _("Good mix of speed and accuracy for most use cases."),
                            "float16": _("Higher accuracy for professional content."),
                            "float32": _("Maximum accuracy. Requires most resources."),
                        }.get(quant, ""),
                        "error_message": {
                            "int8": _("Not supported on current hardware"),
                            "int16": _("Requires CPU with AVX support"),
                            "float16": _("Requires GPU or CPU with F16C support"),
                            "float32": _("Not supported on current hardware"),
                        }.get(quant, ""),
                        "metrics": "",  # Metrics HTML will be generated on frontend
                    }
                    qualities.append(q)

                quality_settings[model_id] = qualities

            response_data["quality_settings"] = quality_settings

            # Add disk usage
            disk_info = full_status.get("disk", {})
            response_data["disk_usage"] = {
                "disk_usage_gb": disk_info.get("models_size_gb", 0),
                "disk_free_gb": disk_info.get("free_gb", 0),
                "disk_total_gb": disk_info.get("total_gb", 0),
                "system_used_gb": disk_info.get("total_gb", 0)
                - disk_info.get("free_gb", 0)
                - disk_info.get("models_size_gb", 0),
            }

            return JsonResponse(response_data)

    # Service not available
    return JsonResponse(
        {"service_available": False, "error": "Translation service is not available"}
    )


@staff_member_required
@require_http_methods(["POST"])
def quick_translate_view(request):
    """Quick translation test endpoint"""

    text = request.POST.get("text")
    source_lang = request.POST.get("source_lang", "en")
    target_lang = request.POST.get("target_lang")

    if not text or not target_lang:
        return JsonResponse({"success": False, "error": _("Missing required fields")})

    client = get_translator_client()

    start_time = timezone.now()
    translated = client.translate(text, source_lang, target_lang)
    duration = (timezone.now() - start_time).total_seconds() * 1000

    if translated:
        return JsonResponse(
            {
                "success": True,
                "translated_text": translated,
                "duration_ms": duration,
                "chars_per_second": len(text) / (duration / 1000) if duration > 0 else 0,
            }
        )
    else:
        return JsonResponse({"success": False, "error": _("Translation failed")})


@staff_member_required
@require_http_methods(["POST"])
def run_benchmark_view(request):
    """Run translation benchmark"""

    source_lang = request.POST.get("source_lang", "en")
    target_lang = request.POST.get("target_lang", "es")
    num_samples = int(request.POST.get("num_samples", 50))
    sample_length = request.POST.get("sample_length", "medium")

    client = get_translator_client()
    results = client.run_benchmark(source_lang, target_lang, num_samples, sample_length)

    if results:
        return JsonResponse({"success": True, "results": results})
    else:
        return JsonResponse({"success": False, "error": _("Benchmark failed")})


@staff_member_required
@require_http_methods(["GET"])
def download_status_view(request):
    """Get model download status"""

    client = get_translator_client()
    status = client.get_download_status()

    if status:
        return JsonResponse(status)
    else:
        return JsonResponse({"status": "unknown", "error": _("Could not get download status")})


@staff_member_required
@shared_fleet_blocked
@require_http_methods(["POST"])
def start_download_view(request):
    """Start model download"""

    model = request.POST.get("model")
    quantization = request.POST.get("quantization", "int8")  # Default to int8 if not specified
    client = get_translator_client()

    # Use the client's API to start download
    try:
        params = {}
        if model:
            params["model"] = model
        if quantization:
            params["quantization"] = quantization

        # FastAPI expects query parameters for this endpoint
        endpoint = "/download/start"
        if params:
            query_params = "&".join([f"{k}={v}" for k, v in params.items()])
            endpoint = f"{endpoint}?{query_params}"
        response = client._request("POST", endpoint)
        if response:
            return JsonResponse({"success": True, "message": _("Download started")})
    except Exception as e:
        logger.error(f"Failed to start download: {e}")

    return JsonResponse({"success": False, "error": _("Failed to start download")})


@staff_member_required
@shared_fleet_blocked
@require_http_methods(["POST"])
def toggle_translation_service_view(request):
    """Toggle translation service on/off"""

    enabled = request.POST.get("enabled") == "true"

    # Would save this to settings/database
    os.environ["TRANSLATOR_ENABLED"] = "true" if enabled else "false"

    return JsonResponse(
        {
            "success": True,
            "enabled": enabled,
            "message": _("Translation service enabled")
            if enabled
            else _("Translation service disabled"),
        }
    )


# Docker Container Management Views


@staff_member_required
@shared_fleet_blocked
@require_http_methods(["GET"])
def docker_status_view(request):
    """Get Docker container status"""

    # Check if Docker is installed
    docker_installed = DockerManager.check_docker_installed()
    if not docker_installed:
        return JsonResponse(
            {
                "success": False,
                "error": _("Docker is not installed or not accessible"),
                "docker_installed": False,
            }
        )

    # Get container status
    status = DockerManager.get_container_status()

    return JsonResponse({"success": True, "docker_installed": True, "container": status})


@staff_member_required
@shared_fleet_blocked
@require_http_methods(["POST"])
def docker_start_view(request):
    """Start the Docker container"""

    success, message = DockerManager.start_container()

    if success:
        messages.success(request, _("Docker container started successfully"))
    else:
        messages.error(request, _(f"Failed to start container: {message}"))

    return JsonResponse({"success": success, "message": message})


@staff_member_required
@shared_fleet_blocked
@require_http_methods(["POST"])
def docker_stop_view(request):
    """Stop the Docker container"""

    success, message = DockerManager.stop_container()

    if success:
        messages.success(request, _("Docker container stopped successfully"))
    else:
        messages.error(request, _(f"Failed to stop container: {message}"))

    return JsonResponse({"success": success, "message": message})


@staff_member_required
@shared_fleet_blocked
@require_http_methods(["POST"])
def docker_restart_view(request):
    """Restart the Docker container"""

    success, message = DockerManager.restart_container()

    if success:
        messages.success(request, _("Docker container restarted successfully"))
    else:
        messages.error(request, _(f"Failed to restart container: {message}"))

    return JsonResponse({"success": success, "message": message})


@staff_member_required
@shared_fleet_blocked
@require_http_methods(["GET"])
def docker_logs_view(request):
    """Get Docker container logs"""

    lines = int(request.GET.get("lines", 50))
    logs = DockerManager.get_container_logs(lines)

    return JsonResponse({"success": True, "logs": logs})


@staff_member_required
@shared_fleet_blocked
@require_http_methods(["POST"])
def docker_pull_view(request):
    """Pull the latest Docker image"""

    success, message = DockerManager.pull_image()

    if success:
        messages.success(request, _("Docker image updated successfully"))
    else:
        messages.error(request, _(f"Failed to pull image: {message}"))

    return JsonResponse({"success": success, "message": message})


# Quantization Management Views


@staff_member_required
@require_http_methods(["GET"])
def quantization_list_view(request):
    """List available quantization levels"""

    # Get translator client
    client = get_translator_client()

    # Check if service is running
    if not client.is_available():
        return JsonResponse(
            {
                "success": False,
                "error": _("Translation service is not running"),
                "quantizations": [],
            }
        )

    # Get list of quantizations from API
    try:
        response = client._request("GET", "/quantizations")
        if response:
            return JsonResponse(
                {
                    "success": True,
                    "current": response.get("current", "int8"),
                    "quantizations": response.get("available", []),
                }
            )
    except Exception as e:
        logger.error(f"Failed to get quantizations: {e}")

    return JsonResponse(
        {"success": False, "error": _("Failed to get quantization list"), "quantizations": []}
    )


@staff_member_required
@shared_fleet_blocked
@require_http_methods(["POST"])
def quantization_set_view(request):
    """Set the active quantization level"""

    quantization = request.POST.get("quantization")
    model_id = request.POST.get("model")  # Get model ID if provided

    if not quantization:
        return JsonResponse({"success": False, "error": _("No quantization level specified")})

    # Validate quantization
    valid_quants = ["int8", "int16", "float16", "float32"]
    if quantization not in valid_quants:
        return JsonResponse({"success": False, "error": _("Invalid quantization level")})

    # Get translator client
    client = get_translator_client()

    # Set quantization via API
    try:
        # Include model parameter if provided
        url = f"/quantization/set?quantization={quantization}"
        if model_id:
            url += f"&model={model_id}"
        response = client._request("POST", url)
        if response:
            # Update the default model in Django database
            if model_id:
                # Clear all defaults first
                InstalledModel.objects.update(is_default=False)
                # Set the new default
                model_name = model_id.replace("-", "_")  # Normalize to underscore format
                InstalledModel.objects.filter(name=model_name).update(is_default=True)

            # Sync database with service to reflect the activated model
            sync_models_with_service(client)

            friendly_name = get_quantization_friendly_name(quantization, model_id)
            messages.success(request, _(f"Successfully switched to {friendly_name}"))
            return JsonResponse(
                {
                    "success": True,
                    "message": response.get("message", f"Switched to {friendly_name}"),
                }
            )
    except Exception as e:
        logger.error(f"Failed to set quantization: {e}")

    return JsonResponse({"success": False, "error": _("Failed to set quantization level")})


@staff_member_required
@shared_fleet_blocked
@require_http_methods(["POST"])
def quantization_download_view(request):
    """Download specific quantization level"""

    model = request.POST.get("model")
    quantization = request.POST.get("quantization")
    download_all = request.POST.get("download_all", "false").lower() == "true"

    # Get translator client
    client = get_translator_client()

    # Start download via API
    try:
        params = {"download_all": download_all}
        if model:
            params["model"] = model
        if quantization:
            params["quantization"] = quantization

        # FastAPI expects query parameters for this endpoint
        endpoint = "/download/start"
        if params:
            query_params = "&".join([f"{k}={v}" for k, v in params.items()])
            endpoint = f"{endpoint}?{query_params}"
        response = client._request("POST", endpoint)
        if response:
            # Sync database with service to reflect download progress
            sync_models_with_service(client)

            # Create friendly message
            friendly_name = get_quantization_friendly_name(quantization, model)
            message = _(f"Download started for {friendly_name}")
            messages.success(request, message)
            return JsonResponse({"success": True, "message": str(message)})
    except Exception as e:
        logger.error(f"Failed to start download: {e}")

    return JsonResponse({"success": False, "error": _("Failed to start download")})


# Language Management Views
@staff_member_required
def language_management_view(request):
    """Language management interface"""

    # Get all languages grouped by support level
    languages = SiteLanguage.objects.all().order_by("order", "name")

    # Separate active and available languages
    active_languages = languages.filter(is_active=True).order_by("order")
    available_languages = languages.filter(is_active=False)

    # Group available by support level for display
    available_by_support = {
        "full": available_languages.filter(m2m100_support="full"),
        "limited": available_languages.filter(m2m100_support="limited"),
        "nllb_only": available_languages.filter(requires_nllb=True),
    }

    # Check which models are installed
    installed_models = InstalledModel.objects.filter(is_downloaded=True)
    has_nllb = installed_models.filter(model_type="nllb").exists()
    has_m2m100_large = installed_models.filter(name__contains="1.2b").exists()

    context = {
        "title": _("Language Management"),
        "active_languages": active_languages,
        "available_languages": available_languages,
        "available_by_support": available_by_support,
        "total_languages": languages.count(),
        "active_count": active_languages.count(),
        "has_nllb": has_nllb,
        "has_m2m100_large": has_m2m100_large,
    }

    return render(request, "admin/translations/languages.html", context)


@staff_member_required
@require_http_methods(["GET"])
def languages_list_api(request):
    """API endpoint to get all languages with their status"""

    languages = SiteLanguage.objects.all().order_by("order", "name")

    language_data = []
    for lang in languages:
        language_data.append(
            {
                "id": lang.id,
                "code": lang.code,
                "name": lang.name,
                "native_name": lang.native_name,
                "flag": lang.flag,
                "is_active": lang.is_active,
                "is_default": lang.is_default,
                "order": lang.order,
                "rtl": lang.rtl,
                "m2m100_support": lang.m2m100_support,
                "nllb_support": lang.nllb_support,
                "requires_nllb": lang.requires_nllb,
                "support_indicator": lang.get_support_indicator(),
            }
        )

    return JsonResponse(
        {
            "success": True,
            "languages": language_data,
            "total": len(language_data),
            "active_count": sum(1 for lang in language_data if lang["is_active"]),
        }
    )


@staff_member_required
@require_http_methods(["POST"])
def language_activate_api(request):
    """Activate or deactivate a language"""

    language_id = request.POST.get("language_id")
    activate = request.POST.get("activate", "true").lower() == "true"

    try:
        language = SiteLanguage.objects.get(id=language_id)
        language.is_active = activate

        # If activating and no default language, make this default
        if activate and not SiteLanguage.objects.filter(is_default=True).exists():
            language.is_default = True

        language.save()

        return JsonResponse(
            {
                "success": True,
                "message": _("Language updated successfully"),
                "language": {
                    "id": language.id,
                    "code": language.code,
                    "name": language.name,
                    "is_active": language.is_active,
                    "is_default": language.is_default,
                },
            }
        )
    except SiteLanguage.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Language not found")}, status=404)
    except Exception as e:
        logger.error(f"Failed to update language: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def languages_reorder_api(request):
    """Reorder languages"""

    try:
        language_ids = json.loads(request.body).get("language_ids", [])

        # Update order for each language
        for index, lang_id in enumerate(language_ids):
            SiteLanguage.objects.filter(id=lang_id).update(order=index)

        return JsonResponse({"success": True, "message": _("Language order updated successfully")})
    except Exception as e:
        logger.error(f"Failed to reorder languages: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def languages_bulk_update_api(request):
    """Bulk update language activation status"""

    try:
        data = json.loads(request.body)
        activate_ids = data.get("activate_ids", [])
        deactivate_ids = data.get("deactivate_ids", [])

        # Activate languages
        if activate_ids:
            SiteLanguage.objects.filter(id__in=activate_ids).update(is_active=True)

        # Deactivate languages (but not default)
        if deactivate_ids:
            SiteLanguage.objects.filter(id__in=deactivate_ids).exclude(is_default=True).update(
                is_active=False
            )

        # Ensure at least one default language
        if not SiteLanguage.objects.filter(is_default=True).exists():
            first_active = SiteLanguage.objects.filter(is_active=True).first()
            if first_active:
                first_active.is_default = True
                first_active.save()

        # Get updated counts
        active_count = SiteLanguage.objects.filter(is_active=True).count()
        total_count = SiteLanguage.objects.count()

        return JsonResponse(
            {
                "success": True,
                "message": _("Languages updated successfully"),
                "active_count": active_count,
                "total_count": total_count,
            }
        )
    except Exception as e:
        logger.error(f"Failed to bulk update languages: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# External Providers Views
@login_required
@user_passes_test(lambda u: u.is_superuser)
def external_providers_view(request):
    """View for managing external translation providers (component-based)"""
    from component_updates.models import ComponentRegistry
    from translations.providers.registry import ProviderRegistry

    # Provider icon mapping (keyed by slug)
    PROVIDER_ICONS = {
        "deepl": "fas fa-language",
        "google_translate": "fab fa-google",
        "azure_translator": "fab fa-microsoft",
        "aws_translate": "fab fa-aws",
    }

    # Get installed translation provider components
    components = ComponentRegistry.objects.filter(
        component_type="translation_provider",
    ).order_by("name")

    # Get configured accounts
    accounts = TranslationProviderAccount.objects.select_related("component").order_by("priority")
    accounts_by_slug = {}
    for account in accounts:
        accounts_by_slug[account.component.slug] = account

    # Build provider card data from installed components + manifests
    provider_cards = []
    for component in components:
        manifest = ProviderRegistry.get_manifest(component.slug) or {}
        account = accounts_by_slug.get(component.slug)
        provider_info = manifest.get("provider_info", {})

        provider_cards.append(
            {
                "slug": component.slug,
                "name": component.name,
                "icon": PROVIDER_ICONS.get(component.slug, "fas fa-cog"),
                "description": component.description,
                "features": provider_info.get("features", []),
                "signup_url": manifest.get("signup_url", ""),
                "account": account,
                "is_configured": account is not None,
                "is_active": account.is_active if account else False,
                "connection_status": account.connection_status if account else "unknown",
                "total_translations": account.total_translations if account else 0,
                "last_used_at": account.last_used_at if account else None,
            }
        )

    context = {
        "title": _("External Translation Providers"),
        "provider_cards": provider_cards,
    }

    return render(request, "admin/translations/external_providers.html", context)


def _safe_external_url(url):
    """Validate URL protocol — only allow http(s) and relative paths."""
    if not url or not isinstance(url, str):
        return ""
    url = url.strip()
    if url.startswith(("https://", "http://", "/")):
        return url
    return ""


@login_required
@user_passes_test(lambda u: u.is_superuser)
def browse_providers_view(request):
    """Browse available translation providers from the update server"""
    from django.utils.translation import get_language

    from component_updates.models import ComponentRegistry
    from component_updates.services import UpdateManager
    from providers_common.utils import get_translated_provider_fields

    available_from_server = []
    has_update_server = False

    try:
        update_manager = UpdateManager()
        available_from_server = update_manager.list_available_components(
            component_type="translation_provider"
        )
        has_update_server = True
    except Exception as e:
        logger.warning("Could not fetch from update server: %s", e)

    # Get installed providers for version comparison
    installed_db = {
        p.slug: p.current_version
        for p in ComponentRegistry.objects.filter(component_type="translation_provider")
    }

    lang = get_language() or "en"

    all_providers = []
    for provider in available_from_server:
        slug = provider.get("slug")
        latest_version = provider.get("current_version") or provider.get("version")
        manifest = provider.get("manifest", {})
        capabilities = provider.get("capabilities") or manifest.get("capabilities", {})

        is_installed = slug in installed_db
        current_version = installed_db.get(slug, "")
        has_update = False

        if is_installed and current_version and latest_version:
            try:
                from packaging import version

                has_update = version.parse(latest_version) > version.parse(current_version)
            except Exception:
                has_update = False

        translated = get_translated_provider_fields(manifest, lang)

        provider_data = {
            "slug": slug,
            "name": translated["name"] or provider.get("name", ""),
            "description": translated["description"] or provider.get("description", ""),
            "version": latest_version,
            "thumbnail_url": _safe_external_url(provider.get("thumbnail_url", "")),
            "homepage_url": _safe_external_url(provider.get("homepage_url", "")),
            "documentation_url": _safe_external_url(
                provider.get("documentation_url") or manifest.get("documentation_url", "")
            ),
            "capabilities": capabilities,
            "is_installed": is_installed,
            "current_version": current_version,
            "latest_version": latest_version,
            "has_update": has_update,
            "translations": manifest.get("translations", {}),
            "default_language": manifest.get("default_language", "en"),
        }
        all_providers.append(provider_data)

    total_count = len(all_providers)
    installed_count = sum(1 for p in all_providers if p["is_installed"])

    # Build modal data
    from django.urls import reverse

    providers_for_modal = []
    for p in all_providers:
        providers_for_modal.append(
            {
                "slug": p["slug"],
                "name": p["name"],
                "description": p["description"],
                "thumbnail_url": _safe_external_url(p["thumbnail_url"]),
                "homepage_url": _safe_external_url(p.get("homepage_url", "")),
                "documentation_url": _safe_external_url(p.get("documentation_url", "")),
                "capabilities": p["capabilities"],
                "translations": dict(
                    p.get("translations", {}), default_language=p.get("default_language", "en")
                ),
                "is_installed": p["is_installed"],
                "current_version": p.get("current_version", ""),
                "latest_version": p.get("latest_version", ""),
                "has_update": p.get("has_update", False),
                "configure_url": reverse("translations:provider_wizard", args=[p["slug"]]),
            }
        )

    context = {
        "title": _("Browse Translation Providers"),
        "providers": all_providers,
        "providers_for_modal": providers_for_modal,
        "total_count": total_count,
        "installed_count": installed_count,
        "has_update_server": has_update_server,
    }

    return render(request, "admin/translations/browse_providers.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def install_translation_provider_ajax(request, provider_slug):
    """AJAX endpoint to install a translation provider from the update server"""
    from django.db import transaction
    from django.urls import reverse

    from component_updates.models import ComponentRegistry

    # Check if already installed
    try:
        ComponentRegistry.objects.get(slug=provider_slug, component_type="translation_provider")
        return JsonResponse(
            {
                "success": True,
                "already_installed": True,
                "message": _("Provider is already installed. Configure it now."),
                "redirect_url": reverse("translations:provider_wizard", args=[provider_slug]),
            }
        )
    except ComponentRegistry.DoesNotExist:
        pass

    try:
        from component_updates.services import UpdateManager

        update_manager = UpdateManager()

        available = update_manager.list_available_components(component_type="translation_provider")

        provider_info = None
        for p in available:
            if p.get("slug") == provider_slug:
                provider_info = p
                break

        if not provider_info:
            return JsonResponse(
                {"success": False, "error": _("Provider not found on update server.")}, status=404
            )

        latest_version = provider_info.get("current_version") or provider_info.get("version")
        provider_name = provider_info.get("name", provider_slug)
        provider_description = provider_info.get("description", "")

        if not latest_version:
            return JsonResponse(
                {"success": False, "error": _("Could not determine provider version.")}, status=400
            )

        with transaction.atomic():
            component = ComponentRegistry.objects.create(
                slug=provider_slug,
                name=provider_name,
                description=provider_description,
                component_type="translation_provider",
                current_version=latest_version,
            )

            try:
                package_path = update_manager.download_component(component, latest_version)
            except Exception:
                logger.exception("Failed to download translation provider %s", provider_slug)
                component.delete()
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Failed to download provider. Please try again later."),
                    },
                    status=500,
                )

            try:
                update_manager._install_package(component, package_path, latest_version)
            except Exception:
                logger.exception("Failed to install translation provider %s", provider_slug)
                component.delete()
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Failed to install provider. Please try again later."),
                    },
                    status=500,
                )

            # Reload provider registry and invalidate cache for other workers
            try:
                from component_updates.integration_paths import touch_provider_cache_marker
                from translations.providers.registry import ProviderRegistry

                ProviderRegistry.reload_providers()
                touch_provider_cache_marker("translation_provider")
            except Exception as e:
                logger.warning(
                    "Could not reload providers after installing %s: %s", provider_slug, e
                )

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "%(name)s" installed successfully! Configure it now.')
                % {"name": provider_name},
                "redirect_url": reverse("translations:provider_wizard", args=[provider_slug]),
            }
        )

    except Exception:
        logger.exception("Error installing translation provider")
        return JsonResponse(
            {"success": False, "error": _("An unexpected error occurred during installation.")},
            status=500,
        )


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def update_translation_provider_ajax(request, provider_slug):
    """AJAX endpoint to update a translation provider to the latest version"""
    from django.db import transaction
    from django.urls import reverse

    from component_updates.models import ComponentRegistry

    try:
        try:
            component = ComponentRegistry.objects.get(
                slug=provider_slug, component_type="translation_provider"
            )
        except ComponentRegistry.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": _("Provider not installed.")}, status=404
            )

        from component_updates.services import UpdateManager

        update_manager = UpdateManager()

        try:
            available = update_manager.list_available_components(
                component_type="translation_provider"
            )
        except Exception:
            logger.exception("Could not connect to update server for translation provider update")
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Could not connect to update server. Please try again later."),
                },
                status=500,
            )

        provider_info = None
        for p in available:
            if p.get("slug") == provider_slug:
                provider_info = p
                break

        if not provider_info:
            return JsonResponse(
                {"success": False, "error": _("Provider not found on update server.")}, status=404
            )

        latest_version = provider_info.get("current_version") or provider_info.get("version")
        provider_name = provider_info.get("name", provider_slug)

        if not latest_version:
            return JsonResponse(
                {"success": False, "error": _("Could not determine latest version.")}, status=400
            )

        if component.current_version == latest_version:
            return JsonResponse(
                {
                    "success": True,
                    "message": _('Provider "%(name)s" is already up to date (v%(version)s).')
                    % {"name": provider_name, "version": latest_version},
                    "redirect_url": reverse("translations:browse_providers"),
                }
            )

        with transaction.atomic():
            try:
                package_path = update_manager.download_component(component, latest_version)
            except Exception:
                logger.exception("Failed to download translation provider update %s", provider_slug)
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Failed to download update. Please try again later."),
                    },
                    status=500,
                )

            try:
                update_manager._install_package(component, package_path, latest_version)
            except Exception:
                logger.exception("Failed to install translation provider update %s", provider_slug)
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Failed to install update. Please try again later."),
                    },
                    status=500,
                )

            # Reload provider registry and invalidate cache for other workers
            try:
                from component_updates.integration_paths import touch_provider_cache_marker
                from translations.providers.registry import ProviderRegistry

                ProviderRegistry.reload_providers()
                touch_provider_cache_marker("translation_provider")
            except Exception as e:
                logger.warning("Could not reload providers after updating %s: %s", provider_slug, e)

            component.current_version = latest_version
            component.save()

        return JsonResponse(
            {
                "success": True,
                "message": _('Provider "%(name)s" updated successfully to v%(version)s!')
                % {"name": provider_name, "version": latest_version},
                "redirect_url": reverse("translations:browse_providers"),
            }
        )

    except Exception:
        logger.exception("Error updating translation provider %s", provider_slug)
        return JsonResponse(
            {"success": False, "error": _("An unexpected error occurred during update.")},
            status=500,
        )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def provider_wizard_view(request, provider_type):
    """Wizard view for setting up a specific provider (component-based)"""
    from component_updates.models import ComponentRegistry
    from translations.providers.registry import ProviderRegistry
    from translations.utils.encryption import decrypt_credentials

    # Look up the component
    component = ComponentRegistry.objects.filter(
        component_type="translation_provider",
        slug=provider_type,
    ).first()

    if not component:
        from django.http import Http404

        raise Http404(f"Translation provider '{provider_type}' not installed")

    # Load manifest for credential schema and provider info
    manifest = ProviderRegistry.get_manifest(provider_type) or {}
    credential_schema = manifest.get("credential_schema", {})
    provider_info = manifest.get("provider_info", {})

    # Load setup instructions from provider package
    from component_updates.integration_paths import INTEGRATIONS_DIR

    instructions_html = ""
    has_instructions = False

    component_path = INTEGRATIONS_DIR / "translation_provider" / provider_type / "current"
    instructions_file = component_path / "setup_instructions.html"

    if instructions_file.exists():
        from django.template import Context as TemplateContext
        from django.template import Template
        from django.utils.safestring import mark_safe

        with open(instructions_file, encoding="utf-8") as f:
            instructions_content = f.read()

        template = Template(instructions_content)
        ctx = TemplateContext({"component": component})
        instructions_html = mark_safe(template.render(ctx))
        has_instructions = True

    # Get existing account if configured
    existing_account = TranslationProviderAccount.objects.filter(
        component=component,
    ).first()

    # Decrypt existing credentials for pre-filling form (redacted)
    existing_credentials = {}
    if existing_account and existing_account.credentials_encrypted:
        try:
            existing_credentials = decrypt_credentials(existing_account.credentials_encrypted)
        except Exception:
            pass

    context = {
        "title": _("Setup %(name)s") % {"name": component.name},
        "provider_type": provider_type,
        "component": component,
        "manifest": manifest,
        "credential_schema": credential_schema,
        "provider_info": provider_info,
        "existing_account": existing_account,
        "existing_credentials": existing_credentials,
        "instructions_html": instructions_html,
        "has_instructions": has_instructions,
        "provider_config": {
            "name": component.name,
            "docs_url": manifest.get("support_url", ""),
            "signup_url": manifest.get("signup_url", ""),
            "free_tier": provider_info.get("free_tier", ""),
            "pricing": provider_info.get("pricing", ""),
        },
    }

    return render(request, "admin/translations/provider_wizard.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def test_provider_api(request):
    """Test API connection for a translation provider component."""
    from translations.providers.registry import ProviderRegistry

    try:
        provider_type = request.POST.get("provider_type")
        if not provider_type:
            return JsonResponse(
                {"success": False, "error": _("Provider type is required")}, status=400
            )

        # Look up the provider class from the registry
        provider_class = ProviderRegistry.get_provider(provider_type)
        if not provider_class:
            # Fall through for 'custom' built-in type
            if provider_type == "custom":
                return _test_custom_provider(request)
            return JsonResponse(
                {
                    "success": False,
                    "error": _('Provider "%(type)s" is not installed') % {"type": provider_type},
                },
                status=400,
            )

        # Build credentials dict from POST data using manifest schema
        manifest = ProviderRegistry.get_manifest(provider_type) or {}
        credential_schema = manifest.get("credential_schema", {})
        credentials = {}
        for field_key, field_def in credential_schema.items():
            value = request.POST.get(field_key, "").strip()
            if field_def.get("required") and not value:
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("%(field)s is required")
                        % {"field": field_def.get("label", field_key)},
                    },
                    status=400,
                )
            credentials[field_key] = value or field_def.get("default", "")

        # Instantiate provider and test connection
        provider = provider_class(credentials=credentials)
        result = provider.test_connection()

        return JsonResponse(result)

    except Exception:
        logger.exception("Provider test failed")
        return JsonResponse(
            {
                "success": False,
                "error": _("Provider test failed. Please check your credentials and try again."),
            },
            status=500,
        )


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def test_translation_api(request):
    """Test an actual translation using the provider being configured."""
    from translations.providers.registry import ProviderRegistry

    try:
        provider_type = request.POST.get("provider_type")
        text = request.POST.get("text", "").strip()
        target_lang = request.POST.get("target_lang", "").strip()
        source_lang = request.POST.get("source_lang", "en").strip()

        if not provider_type:
            return JsonResponse(
                {"success": False, "error": _("Provider type is required")}, status=400
            )

        if not text:
            return JsonResponse(
                {"success": False, "error": _("Please enter text to translate")}, status=400
            )

        if not target_lang:
            return JsonResponse(
                {"success": False, "error": _("Please select a target language")}, status=400
            )

        if provider_type == "custom":
            return _test_custom_translation(request, text, source_lang, target_lang)

        # Look up the provider class from the registry
        provider_class = ProviderRegistry.get_provider(provider_type)
        if not provider_class:
            return JsonResponse(
                {
                    "success": False,
                    "error": _('Provider "%(type)s" is not installed') % {"type": provider_type},
                },
                status=400,
            )

        # Build credentials dict from POST data using manifest schema
        manifest = ProviderRegistry.get_manifest(provider_type) or {}
        credential_schema = manifest.get("credential_schema", {})
        credentials = {}
        for field_key, field_def in credential_schema.items():
            value = request.POST.get(field_key, "").strip()
            credentials[field_key] = value or field_def.get("default", "")

        # Instantiate provider and translate
        provider = provider_class(credentials=credentials)
        translated = provider.translate(text, source_lang, target_lang)

        return JsonResponse(
            {
                "success": True,
                "translated_text": translated,
                "source_lang": source_lang,
                "target_lang": target_lang,
            }
        )

    except Exception as e:
        logger.exception("Translation test failed")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def _test_custom_translation(request, text, source_lang, target_lang):
    """Test translation via a custom/self-hosted API."""
    import requests as http_requests

    api_key = request.POST.get("api_key", "").strip()
    api_endpoint = request.POST.get("api_endpoint", "").strip()

    if not api_endpoint:
        return JsonResponse(
            {"success": False, "error": _("API endpoint URL is required for custom providers")},
            status=400,
        )

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    test_data = {"q": text, "source": source_lang, "target": target_lang}
    if api_key:
        test_data["api_key"] = api_key

    try:
        response = http_requests.post(api_endpoint, json=test_data, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            translated = data.get("translatedText", data.get("translated_text", str(data)))
            return JsonResponse(
                {
                    "success": True,
                    "translated_text": translated,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                }
            )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "error": f"API returned status code {response.status_code}: {response.text[:200]}",
                }
            )
    except http_requests.exceptions.RequestException as e:
        return JsonResponse({"success": False, "error": f"Connection error: {str(e)}"})
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Translation failed: {str(e)}"})


def _test_custom_provider(request):
    """Test a custom/self-hosted translation API (built-in, not a component)."""
    import requests as http_requests

    api_key = request.POST.get("api_key", "").strip()
    api_endpoint = request.POST.get("api_endpoint", "").strip()

    if not api_endpoint:
        return JsonResponse(
            {"success": False, "error": _("API endpoint URL is required for custom providers")},
            status=400,
        )

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    test_data = {"q": "Hello", "source": "en", "target": "es"}
    if api_key:
        test_data["api_key"] = api_key

    try:
        response = http_requests.post(api_endpoint, json=test_data, headers=headers, timeout=10)
        if response.status_code == 200:
            return JsonResponse(
                {
                    "success": True,
                    "message": _("Custom API connection successful!"),
                }
            )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "error": f"API returned status code {response.status_code}: {response.text[:200]}",
                }
            )
    except http_requests.exceptions.RequestException as e:
        return JsonResponse({"success": False, "error": f"Connection error: {str(e)}"})
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Test failed: {str(e)}"})


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def save_provider_api(request):
    """Save provider configuration to a TranslationProviderAccount."""
    from component_updates.models import ComponentRegistry
    from translations.providers.registry import ProviderRegistry
    from translations.utils.encryption import encrypt_credentials

    try:
        provider_type = request.POST.get("provider_type")
        display_name = request.POST.get("name", "").strip()

        if not provider_type:
            return JsonResponse(
                {"success": False, "error": _("Provider type is required")}, status=400
            )

        # Resolve the component
        component = ComponentRegistry.objects.filter(
            component_type="translation_provider",
            slug=provider_type,
        ).first()

        if not component:
            return JsonResponse(
                {
                    "success": False,
                    "error": _('Provider "%(type)s" is not installed') % {"type": provider_type},
                },
                status=400,
            )

        # Build credentials dict from POST data using manifest schema
        manifest = ProviderRegistry.get_manifest(provider_type) or {}
        credential_schema = manifest.get("credential_schema", {})
        credentials = {}
        for field_key, field_def in credential_schema.items():
            value = request.POST.get(field_key, "").strip()
            if field_def.get("required") and not value:
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("%(field)s is required")
                        % {"field": field_def.get("label", field_key)},
                    },
                    status=400,
                )
            credentials[field_key] = value or field_def.get("default", "")

        # Build settings from optional form fields
        account_settings = {}
        rate_limit = request.POST.get("rate_limit")
        max_chars = request.POST.get("max_chars_per_request")
        timeout = request.POST.get("timeout_seconds")
        if rate_limit:
            account_settings["rate_limit"] = int(rate_limit)
        if max_chars:
            account_settings["max_chars_per_request"] = int(max_chars)
        if timeout:
            account_settings["timeout"] = int(timeout)

        # Encrypt credentials
        encrypted = encrypt_credentials(credentials)

        # Get or create the account
        account, created = TranslationProviderAccount.objects.update_or_create(
            component=component,
            defaults={
                "user": request.user,
                "display_name": display_name or component.name,
                "credentials_encrypted": encrypted,
                "settings": account_settings,
                "signup_url": manifest.get("signup_url", ""),
                "is_active": True,
            },
        )

        # Update priority if provided
        priority = request.POST.get("priority")
        if priority:
            account.priority = int(priority)
            account.save(update_fields=["priority"])

        return JsonResponse(
            {
                "success": True,
                "message": _("Provider configuration saved successfully"),
                "account_id": str(account.id),
            }
        )

    except Exception:
        logger.exception("Failed to save provider")
        return JsonResponse(
            {
                "success": False,
                "error": _("Failed to save provider configuration. Please try again."),
            },
            status=500,
        )


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def toggle_provider_api(request, account_id):
    """Toggle a TranslationProviderAccount active status."""
    try:
        account = TranslationProviderAccount.objects.get(id=account_id)
        account.is_active = not account.is_active
        account.save(update_fields=["is_active"])

        return JsonResponse(
            {
                "success": True,
                "is_active": account.is_active,
                "message": _("Provider {} successfully").format(
                    _("activated") if account.is_active else _("deactivated")
                ),
            }
        )

    except TranslationProviderAccount.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": _("Provider account not found")}, status=404
        )
    except Exception:
        logger.exception("Failed to toggle provider")
        return JsonResponse(
            {"success": False, "error": _("Failed to update provider status. Please try again.")},
            status=500,
        )


# ============================================================================
# Translation Job Management Views
# ============================================================================


@staff_member_required
@login_required
def translation_jobs_redirect(request):
    """Redirect from old Django admin URL to new interface"""
    from django.contrib import messages
    from django.shortcuts import redirect

    messages.info(request, _("Translation Jobs management has moved to a new interface"))
    return redirect("admin:translations:translation_jobs")


@staff_member_required
@login_required
def translation_jobs_view(request):
    """Main view for translation job management"""

    # Get job statistics
    jobs_stats = {
        "pending": TranslationJob.objects.filter(status="pending").count(),
        "processing": TranslationJob.objects.filter(status="processing").count(),
        "completed": TranslationJob.objects.filter(status="completed").count(),
        "failed": TranslationJob.objects.filter(status="failed").count(),
        "cancelled": TranslationJob.objects.filter(status="cancelled").count(),
    }

    # Get recent jobs
    recent_jobs = TranslationJob.objects.select_related("provider", "created_by").order_by(
        "-created_at"
    )[:10]

    # Get available languages
    languages = SiteLanguage.objects.filter(is_active=True).order_by("name")

    # Get providers
    providers = TranslationProvider.objects.filter(is_active=True).order_by("priority")

    # Get service health information
    service_info = {
        "is_available": False,
        "degraded": False,
        "degraded_reason": None,
        "active_providers": 0,
        "loaded_models": 0,
    }

    # Check translation service health
    try:
        # Check local service
        client = get_translator_client()
        if client and client.is_available():
            service_info["is_available"] = True

            # Try to get actual loaded model info from service
            try:
                system_info = client.get_system_info()
                if system_info and system_info.get("model_loaded"):
                    service_info["loaded_models"] = 1
                    # Update the loaded model info in database
                    loaded_model_name = system_info.get("model_name") or system_info.get(
                        "current_model"
                    )
                    if loaded_model_name:
                        # Mark the loaded model as active
                        InstalledModel.objects.filter(
                            name=loaded_model_name.replace("-", "_")
                        ).update(is_active=True)
                else:
                    # Fall back to database count
                    models = InstalledModel.objects.filter(is_downloaded=True, is_active=True)
                    service_info["loaded_models"] = models.count()
            except Exception:
                # Fall back to database count
                models = InstalledModel.objects.filter(is_downloaded=True, is_active=True)
                service_info["loaded_models"] = models.count()

        # Check external providers
        active_providers = TranslationProvider.objects.filter(is_active=True)
        service_info["active_providers"] = active_providers.count()

        # Service is available if we have either local service or external providers
        if not service_info["is_available"] and service_info["active_providers"] > 0:
            service_info["is_available"] = True

        # Check for degraded state
        if service_info["is_available"]:
            failed_providers = TranslationProvider.objects.filter(
                is_active=True, total_errors__gt=0
            ).count()

            if failed_providers > 0:
                service_info["degraded"] = True
                service_info["degraded_reason"] = _(
                    "%(count)d provider(s) are experiencing errors"
                ) % {"count": failed_providers}

    except Exception as e:
        logger.error(f"Error checking service health: {e}")

    context = {
        "title": _("Translation Jobs"),
        "jobs_stats": jobs_stats,
        "recent_jobs": recent_jobs,
        "languages": languages,
        "providers": providers,
        "service_info": service_info,
    }

    return render(request, "admin/translations/translation_jobs.html", context)


@staff_member_required
@require_http_methods(["GET"])
def jobs_list_api(request):
    """API endpoint to list translation jobs with filtering and pagination"""

    # Get filter parameters
    status = request.GET.get("status", "")
    job_type = request.GET.get("job_type", "")
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 20))
    order_by = request.GET.get("order_by", "-created_at")

    # Build query
    jobs = TranslationJob.objects.select_related("provider", "created_by")

    if status:
        jobs = jobs.filter(status=status)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    # Order
    jobs = jobs.order_by(order_by)

    # Pagination
    total = jobs.count()
    start = (page - 1) * per_page
    end = start + per_page
    jobs = jobs[start:end]

    # Serialize
    jobs_data = []
    for job in jobs:
        jobs_data.append(
            {
                "id": job.id,
                "job_type": job.job_type,
                "status": job.status,
                "priority": job.priority,
                "source_language": job.source_language,
                "target_languages": job.target_languages,
                "progress": job.progress,
                "total_characters": job.total_characters,
                "translated_characters": job.translated_characters,
                "provider": job.provider.name if job.provider else None,
                "created_by": job.created_by.username if job.created_by else None,
                "created_at": job.created_at.isoformat(),
                "started_at": job.started_at.isoformat() if job.started_at else None,
                "completed_at": job.completed_at.isoformat() if job.completed_at else None,
                "error_message": job.error_message,
            }
        )

    return JsonResponse(
        {
            "success": True,
            "jobs": jobs_data,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }
    )


@staff_member_required
@require_http_methods(["POST"])
def create_job_api(request):
    """API endpoint to create a new translation job"""

    try:
        data = json.loads(request.body)

        # Validate required fields
        required_fields = ["job_type", "source_language", "target_languages"]
        for field in required_fields:
            if field not in data:
                return JsonResponse(
                    {"success": False, "error": f"Missing required field: {field}"}, status=400
                )

        # Create job
        job = TranslationJob.objects.create(
            job_type=data["job_type"],
            source_language=data["source_language"],
            target_languages=data["target_languages"],
            priority=data.get("priority", 0),
            content_type=data.get("content_type"),
            object_id=data.get("object_id"),
            fields_to_translate=data.get("fields_to_translate", []),
            provider_id=data.get("provider_id"),
            created_by=request.user,
        )

        # If immediate execution requested, start processing
        if data.get("execute_now", False):
            from translations.tasks import process_translation_job

            process_translation_job(job.id)

        return JsonResponse(
            {
                "success": True,
                "job_id": job.id,
                "message": _("Translation job created successfully"),
            }
        )

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": _("Invalid JSON data")}, status=400)
    except Exception as e:
        logger.error(f"Failed to create translation job: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["GET"])
def job_detail_api(request, job_id):
    """API endpoint to get translation job details"""

    try:
        job = TranslationJob.objects.select_related("provider", "created_by").get(id=job_id)

        job_data = {
            "id": job.id,
            "job_type": job.job_type,
            "status": job.status,
            "priority": job.priority,
            "source_language": job.source_language,
            "target_languages": job.target_languages,
            "content_type": job.content_type,
            "object_id": job.object_id,
            "fields_to_translate": job.fields_to_translate,
            "progress": job.progress,
            "total_characters": job.total_characters,
            "translated_characters": job.translated_characters,
            "provider": {
                "id": job.provider.id,
                "name": job.provider.name,
                "type": job.provider.provider_type,
            }
            if job.provider
            else None,
            "created_by": {
                "id": job.created_by.id,
                "username": job.created_by.username,
                "email": job.created_by.email,
            }
            if job.created_by
            else None,
            "created_at": job.created_at.isoformat(),
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "error_message": job.error_message,
            "retry_count": job.retry_count,
            "max_retries": job.max_retries,
        }

        return JsonResponse(
            {
                "success": True,
                "job": job_data,
            }
        )

    except TranslationJob.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Job not found")}, status=404)
    except Exception as e:
        logger.error(f"Failed to get job details: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["PATCH"])
def update_job_api(request, job_id):
    """API endpoint to update a translation job"""

    try:
        job = TranslationJob.objects.get(id=job_id)
        data = json.loads(request.body)

        # Update allowed fields
        updatable_fields = ["priority", "status", "provider_id"]
        for field in updatable_fields:
            if field in data:
                if field == "provider_id":
                    job.provider_id = data[field]
                else:
                    setattr(job, field, data[field])

        job.save()

        return JsonResponse(
            {
                "success": True,
                "message": _("Job updated successfully"),
            }
        )

    except TranslationJob.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Job not found")}, status=404)
    except Exception as e:
        logger.error(f"Failed to update job: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["DELETE"])
def cancel_job_api(request, job_id):
    """API endpoint to cancel a translation job"""

    try:
        job = TranslationJob.objects.get(id=job_id)

        # Only allow cancelling pending or processing jobs
        if job.status not in ["pending", "processing"]:
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Cannot cancel job with status: {}").format(job.status),
                },
                status=400,
            )

        job.status = "cancelled"
        job.save()

        return JsonResponse(
            {
                "success": True,
                "message": _("Job cancelled successfully"),
            }
        )

    except TranslationJob.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Job not found")}, status=404)
    except Exception as e:
        logger.error(f"Failed to cancel job: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def retry_job_api(request, job_id):
    """API endpoint to retry a failed translation job"""

    try:
        job = TranslationJob.objects.get(id=job_id)

        # Only allow retrying failed jobs
        if job.status != "failed":
            return JsonResponse(
                {"success": False, "error": _("Can only retry failed jobs")}, status=400
            )

        # Check retry limit
        if job.retry_count >= job.max_retries:
            return JsonResponse(
                {"success": False, "error": _("Maximum retry limit reached")}, status=400
            )

        # Reset status and increment retry count
        job.status = "pending"
        job.retry_count += 1
        job.error_message = ""
        job.save()

        # Start processing if requested
        if json.loads(request.body).get("execute_now", False):
            from translations.tasks import process_translation_job

            process_translation_job(job.id)

        return JsonResponse(
            {
                "success": True,
                "message": _("Job queued for retry"),
            }
        )

    except TranslationJob.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Job not found")}, status=404)
    except Exception as e:
        logger.error(f"Failed to retry job: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def start_job_api(request, job_id):
    """API endpoint to manually start a translation job"""

    try:
        job = TranslationJob.objects.get(id=job_id)

        # Only allow starting pending jobs
        if job.status != "pending":
            return JsonResponse(
                {"success": False, "error": _("Can only start pending jobs")}, status=400
            )

        # Start processing
        from translations.tasks import process_translation_job

        process_translation_job(job.id)

        return JsonResponse(
            {
                "success": True,
                "message": _("Job started successfully"),
            }
        )

    except TranslationJob.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Job not found")}, status=404)
    except Exception as e:
        logger.error(f"Failed to start job: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["GET"])
def queue_status_api(request):
    """API endpoint to get translation queue statistics"""

    from django.db.models import Avg, Count

    # Get queue statistics
    stats = TranslationJob.objects.aggregate(
        total=Count("id"),
        pending=Count("id", filter=models.Q(status="pending")),
        processing=Count("id", filter=models.Q(status="processing")),
        completed=Count("id", filter=models.Q(status="completed")),
        failed=Count("id", filter=models.Q(status="failed")),
        cancelled=Count("id", filter=models.Q(status="cancelled")),
        avg_progress=Avg("progress"),
        total_chars=models.Sum("total_characters"),
        translated_chars=models.Sum("translated_characters"),
    )

    # Get jobs by priority
    priority_breakdown = (
        TranslationJob.objects.filter(status__in=["pending", "processing"])
        .values("priority")
        .annotate(count=Count("id"))
        .order_by("-priority")
    )

    # Get estimated wait time
    pending_jobs = TranslationJob.objects.filter(status="pending").count()
    processing_jobs = TranslationJob.objects.filter(status="processing").count()

    # Simple estimate: 1 minute per job (can be refined based on actual data)
    estimated_wait_minutes = (pending_jobs + processing_jobs) * 1

    return JsonResponse(
        {
            "success": True,
            "stats": stats,
            "priority_breakdown": list(priority_breakdown),
            "estimated_wait_minutes": estimated_wait_minutes,
        }
    )


@staff_member_required
@require_http_methods(["POST"])
def bulk_create_jobs_api(request):
    """API endpoint to create multiple translation jobs"""

    try:
        data = json.loads(request.body)
        jobs = data.get("jobs", [])

        if not jobs:
            return JsonResponse({"success": False, "error": _("No jobs provided")}, status=400)

        created_jobs = []
        for job_data in jobs:
            job = TranslationJob.objects.create(
                job_type=job_data.get("job_type", "custom"),
                source_language=job_data["source_language"],
                target_languages=job_data["target_languages"],
                priority=job_data.get("priority", 0),
                content_type=job_data.get("content_type"),
                object_id=job_data.get("object_id"),
                fields_to_translate=job_data.get("fields_to_translate", []),
                provider_id=job_data.get("provider_id"),
                created_by=request.user,
            )
            created_jobs.append(job.id)

        return JsonResponse(
            {
                "success": True,
                "job_ids": created_jobs,
                "message": _("Created {} translation jobs").format(len(created_jobs)),
            }
        )

    except Exception as e:
        logger.error(f"Failed to create bulk jobs: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# ============================================================================
# UI Translation Editor Views
# ============================================================================


@staff_member_required
def ui_translations_editor_view(request):
    """UI Translation editor — main view."""
    from translations.coverage_service import TranslationCoverageService
    from translations.models import SiteLanguage, UITranslationOverride
    from translations.templatetags.merchant_trans import BUILTIN_LANGUAGES
    from translations.ui_string_registry import (
        UI_STRING_REGISTRY,
        UI_STRING_SECTIONS,
        get_total_string_count,
    )

    # Exclude default language — it's the source language
    active_languages = SiteLanguage.objects.filter(is_active=True, is_default=False).order_by(
        "order"
    )

    total = get_total_string_count()
    coverage_service = TranslationCoverageService()

    # Get completion stats for each language
    language_stats = []
    for lang in active_languages:
        try:
            override = UITranslationOverride.objects.get(language=lang)
        except UITranslationOverride.DoesNotExist:
            override = None

        is_builtin = lang.code in BUILTIN_LANGUAGES and lang.code != "en"
        if is_builtin:
            translated = coverage_service._count_effective_ui_coverage(
                lang.code, override, UI_STRING_REGISTRY
            )
        else:
            translated = override.translated_count if override else 0

        verified = override.verified_count if override else 0
        completion = round((translated / total * 100), 1) if total > 0 else 0

        stats = {
            "language": lang,
            "translated": translated,
            "verified": verified,
            "total": total,
            "completion": completion,
            "is_builtin": is_builtin,
        }
        language_stats.append(stats)

    context = {
        "title": _("UI Translations"),
        "language_stats": language_stats,
        "sections": UI_STRING_SECTIONS,
        "total_strings": total,
    }

    return render(request, "admin/translations/ui_translations_editor.html", context)


@staff_member_required
@require_http_methods(["GET"])
def ui_translations_api(request, language_code):
    """Get all UI strings with translations for a specific language."""
    from django.utils.translation import gettext
    from django.utils.translation import override as translation_override

    from translations.models import SiteLanguage, UITranslationOverride
    from translations.templatetags.merchant_trans import BUILTIN_LANGUAGES
    from translations.ui_string_registry import (
        UI_STRING_REGISTRY,
        UI_STRING_SECTIONS,
        get_strings_by_section,
        get_total_string_count,
    )

    try:
        site_lang = SiteLanguage.objects.get(code=language_code, is_active=True)
    except SiteLanguage.DoesNotExist:
        return JsonResponse({"success": False, "error": "Language not found"}, status=404)

    try:
        override = UITranslationOverride.objects.get(language=site_lang)
        overrides = override.overrides or {}
        meta_info = override.meta_info or {}
    except UITranslationOverride.DoesNotExist:
        overrides = {}
        meta_info = {}

    is_builtin = language_code in BUILTIN_LANGUAGES and language_code != "en"

    # Load .po translations for built-in languages
    po_translations = {}
    if is_builtin:
        with translation_override(language_code):
            for key, english_value in UI_STRING_REGISTRY.items():
                po_val = gettext(english_value)
                if po_val and po_val != english_value:
                    po_translations[key] = po_val

    # Build response grouped by section
    sections = {}
    strings_by_section = get_strings_by_section()
    effective_count = 0

    for section_key, strings in strings_by_section.items():
        section_data = {
            "label": str(UI_STRING_SECTIONS.get(section_key, section_key)),
            "strings": {},
        }
        for string_key, english_value in strings.items():
            merchant_override = overrides.get(string_key, "")
            po_default = po_translations.get(string_key, "")

            if merchant_override:
                source = "override"
                translation = merchant_override
            elif po_default:
                source = "shipped"
                translation = po_default
            else:
                source = ""
                translation = ""

            if translation:
                effective_count += 1

            section_data["strings"][string_key] = {
                "english": english_value,
                "translation": translation,
                "source": source,
                "meta": meta_info.get(string_key, {}),
            }
        sections[section_key] = section_data

    return JsonResponse(
        {
            "success": True,
            "language": {
                "code": site_lang.code,
                "name": site_lang.name,
                "native_name": site_lang.native_name,
                "flag": site_lang.flag,
            },
            "sections": sections,
            "total_strings": get_total_string_count(),
            "translated_count": effective_count,
            "is_builtin": is_builtin,
        }
    )


@staff_member_required
@require_http_methods(["POST"])
def ui_translations_save_api(request, language_code):
    """Save UI translations for a specific language."""
    from translations.models import SiteLanguage, UITranslationOverride
    from translations.ui_string_registry import UI_STRING_REGISTRY, get_total_string_count

    try:
        site_lang = SiteLanguage.objects.get(code=language_code, is_active=True)
    except SiteLanguage.DoesNotExist:
        return JsonResponse({"success": False, "error": "Language not found"}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    translations = data.get("translations", {})
    if not isinstance(translations, dict):
        return JsonResponse({"success": False, "error": "translations must be a dict"}, status=400)

    # Validate keys exist in registry
    valid_translations = {}
    for key, value in translations.items():
        if key in UI_STRING_REGISTRY:
            valid_translations[key] = value

    override_obj, created = UITranslationOverride.objects.get_or_create(
        language=site_lang, defaults={"total_strings": get_total_string_count()}
    )

    # Merge with existing overrides
    existing = override_obj.overrides or {}
    meta_info = override_obj.meta_info or {}
    now = timezone.now().isoformat()

    # Determine locked keys (skip them during save)
    locked_keys = {k for k, v in meta_info.items() if isinstance(v, dict) and v.get("locked")}

    for key, value in valid_translations.items():
        if key in locked_keys:
            continue  # Skip locked strings
        existing[key] = value
        if key in meta_info:
            meta_info[key]["verified"] = True
            meta_info[key]["edited_at"] = now
        else:
            meta_info[key] = {
                "auto": False,
                "verified": True,
                "translated_at": now,
            }

    override_obj.overrides = existing
    override_obj.meta_info = meta_info
    override_obj.total_strings = get_total_string_count()
    override_obj.translated_count = sum(1 for v in existing.values() if v)
    override_obj.verified_count = sum(1 for m in meta_info.values() if m.get("verified"))
    override_obj.save()

    # Invalidate caches
    from django.core.cache import cache

    cache_key = f"ui_trans_overrides:{language_code}"
    cache.delete(cache_key)
    from translations.coverage_service import invalidate_coverage_cache

    invalidate_coverage_cache()

    # Return effective translated count (including .po for built-in langs)
    from translations.templatetags.merchant_trans import BUILTIN_LANGUAGES

    is_builtin = language_code in BUILTIN_LANGUAGES and language_code != "en"
    if is_builtin:
        from translations.coverage_service import TranslationCoverageService

        effective_count = TranslationCoverageService()._count_effective_ui_coverage(
            language_code, override_obj, UI_STRING_REGISTRY
        )
    else:
        effective_count = override_obj.translated_count

    return JsonResponse(
        {
            "success": True,
            "translated_count": effective_count,
            "total_strings": override_obj.total_strings,
            "message": _("Translations saved successfully"),
        }
    )


@staff_member_required
@require_http_methods(["POST"])
def ui_translations_auto_translate_api(request, language_code):
    """Trigger auto-translation for a specific language."""
    from translations.models import SiteLanguage

    try:
        site_lang = SiteLanguage.objects.get(code=language_code, is_active=True)
    except SiteLanguage.DoesNotExist:
        return JsonResponse({"success": False, "error": "Language not found"}, status=404)

    from translations.tasks import auto_translate_ui_strings

    auto_translate_ui_strings.delay(site_lang.id)

    return JsonResponse(
        {
            "success": True,
            "message": _("Auto-translation started for {}").format(site_lang.name),
        }
    )


@staff_member_required
@require_http_methods(["GET"])
def ui_translations_export_api(request, language_code):
    """Export UI translations for a language as a downloadable JSON file."""
    from translations.models import SiteLanguage, UITranslationOverride
    from translations.ui_string_registry import UI_STRING_REGISTRY, get_total_string_count

    try:
        site_lang = SiteLanguage.objects.get(code=language_code, is_active=True)
    except SiteLanguage.DoesNotExist:
        return JsonResponse({"success": False, "error": "Language not found"}, status=404)

    try:
        override = UITranslationOverride.objects.get(language=site_lang)
        overrides = override.overrides or {}
    except UITranslationOverride.DoesNotExist:
        overrides = {}

    # Build pack with ALL registry keys — empty string for untranslated
    strings = {}
    for key in sorted(UI_STRING_REGISTRY.keys()):
        strings[key] = overrides.get(key, "")

    pack = {
        "format_version": "1.0",
        "platform": "spwig",
        "language_code": site_lang.code,
        "language_name": site_lang.name,
        "exported_at": timezone.now().isoformat(),
        "registry_version": get_total_string_count(),
        "strings": strings,
    }

    response = JsonResponse(pack, json_dumps_params={"indent": 2, "ensure_ascii": False})
    response["Content-Disposition"] = (
        f'attachment; filename="ui-translations-{site_lang.code}.json"'
    )
    return response


def _validate_import_file(request, language_code):
    """Shared validation for import preview and apply. Returns (pack, site_lang, error_response)."""
    from translations.models import SiteLanguage

    try:
        site_lang = SiteLanguage.objects.get(code=language_code, is_active=True)
    except SiteLanguage.DoesNotExist:
        return (
            None,
            None,
            JsonResponse({"success": False, "error": "Language not found"}, status=404),
        )

    upload = request.FILES.get("file")
    if not upload:
        return None, None, JsonResponse({"success": False, "error": "No file provided"}, status=400)

    if upload.size > 1_048_576:
        return (
            None,
            None,
            JsonResponse({"success": False, "error": "File too large (max 1MB)"}, status=400),
        )

    try:
        raw = upload.read().decode("utf-8")
        pack = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return (
            None,
            None,
            JsonResponse({"success": False, "error": "Invalid JSON file"}, status=400),
        )

    if not isinstance(pack, dict) or "strings" not in pack:
        return (
            None,
            None,
            JsonResponse(
                {"success": False, "error": 'Invalid pack format: missing "strings" field'},
                status=400,
            ),
        )

    pack_lang = pack.get("language_code", "")
    if pack_lang and pack_lang != language_code:
        return (
            None,
            None,
            JsonResponse(
                {
                    "success": False,
                    "error": f'Language mismatch: file is for "{pack_lang}" but you are editing "{language_code}"',
                },
                status=400,
            ),
        )

    strings = pack.get("strings", {})
    if not isinstance(strings, dict):
        return (
            None,
            None,
            JsonResponse(
                {"success": False, "error": 'Invalid pack format: "strings" must be a dictionary'},
                status=400,
            ),
        )

    return pack, site_lang, None


@staff_member_required
@require_http_methods(["POST"])
def ui_translations_import_preview_api(request, language_code):
    """Validate an import file and return a preview summary without applying."""
    from translations.models import UITranslationOverride
    from translations.ui_string_registry import UI_STRING_REGISTRY, get_total_string_count

    pack, site_lang, error = _validate_import_file(request, language_code)
    if error:
        return error

    try:
        override = UITranslationOverride.objects.get(language=site_lang)
        existing = override.overrides or {}
    except UITranslationOverride.DoesNotExist:
        existing = {}

    strings = pack["strings"]
    new_count = 0
    updated_count = 0
    unchanged_count = 0
    skipped_keys = []

    for key, value in strings.items():
        if key not in UI_STRING_REGISTRY:
            skipped_keys.append(key)
            continue
        if not value:
            continue
        if key not in existing or not existing[key]:
            new_count += 1
        elif existing[key] != value:
            updated_count += 1
        else:
            unchanged_count += 1

    return JsonResponse(
        {
            "success": True,
            "preview": {
                "new": new_count,
                "updated": updated_count,
                "unchanged": unchanged_count,
                "skipped": len(skipped_keys),
                "skipped_keys": skipped_keys[:20],
                "total_in_file": len(strings),
                "pack_language": pack.get("language_code", ""),
                "pack_registry_version": pack.get("registry_version", 0),
                "current_registry_version": get_total_string_count(),
            },
        }
    )


@staff_member_required
@require_http_methods(["POST"])
def ui_translations_import_apply_api(request, language_code):
    """Apply an imported translation pack to the language."""
    from translations.models import UITranslationOverride
    from translations.ui_string_registry import UI_STRING_REGISTRY, get_total_string_count

    pack, site_lang, error = _validate_import_file(request, language_code)
    if error:
        return error

    override_obj, created = UITranslationOverride.objects.get_or_create(
        language=site_lang, defaults={"total_strings": get_total_string_count()}
    )
    existing = override_obj.overrides or {}
    meta_info = override_obj.meta_info or {}
    now = timezone.now().isoformat()

    imported = 0
    for key, value in pack["strings"].items():
        if key not in UI_STRING_REGISTRY:
            continue
        if not value:
            continue
        existing[key] = value
        meta_info[key] = {
            "auto": False,
            "verified": False,
            "translated_at": now,
            "imported": True,
        }
        imported += 1

    override_obj.overrides = existing
    override_obj.meta_info = meta_info
    override_obj.total_strings = get_total_string_count()
    override_obj.translated_count = sum(1 for v in existing.values() if v)
    override_obj.verified_count = sum(
        1 for m in meta_info.values() if isinstance(m, dict) and m.get("verified")
    )
    override_obj.save()

    # Invalidate cache
    from django.core.cache import cache

    cache.delete(f"ui_trans_overrides:{language_code}")

    return JsonResponse(
        {
            "success": True,
            "imported": imported,
            "translated_count": override_obj.translated_count,
            "total_strings": override_obj.total_strings,
            "message": f"Successfully imported {imported} translations",
        }
    )


@staff_member_required
@require_http_methods(["POST"])
def ui_translations_translate_string_api(request, language_code):
    """Translate a single UI string on-demand using the AI translation service."""
    import json as json_module

    from translations.models import SiteLanguage
    from translations.ui_string_registry import UI_STRING_REGISTRY

    try:
        SiteLanguage.objects.get(code=language_code, is_active=True)
    except SiteLanguage.DoesNotExist:
        return JsonResponse({"success": False, "error": "Language not found"}, status=404)

    try:
        data = json_module.loads(request.body)
    except (json_module.JSONDecodeError, ValueError):
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    string_key = data.get("key", "")
    if string_key not in UI_STRING_REGISTRY:
        return JsonResponse({"success": False, "error": "Unknown string key"}, status=400)

    english_text = UI_STRING_REGISTRY[string_key]
    if not english_text:
        return JsonResponse({"success": False, "error": "No source text for this key"}, status=400)

    from translations.client import get_translator_client

    client = get_translator_client()
    if not client.enabled:
        return JsonResponse(
            {"success": False, "error": "Translation service is not available"}, status=503
        )

    translated = client.translate(
        text=english_text,
        source_lang="en",
        target_lang=language_code,
    )
    if not translated:
        return JsonResponse({"success": False, "error": "Translation failed"}, status=500)

    return JsonResponse(
        {
            "success": True,
            "key": string_key,
            "translated_text": translated,
        }
    )


# ============================================================================
# Translation Coverage Views
# ============================================================================


@staff_member_required
def coverage_detail_view(request):
    """Translation coverage detail page."""
    from .coverage_service import TranslationCoverageService

    try:
        coverage = TranslationCoverageService().get_site_coverage()
    except Exception as e:
        logger.warning(f"Coverage calculation failed: {e}")
        coverage = {
            "overall_percentage": 0,
            "has_languages": False,
            "languages": [],
            "content_types": [],
        }

    # Group content types by priority
    groups = {}
    priority_labels = {
        1: _("Core Storefront"),
        2: _("Content & Communications"),
        3: _("Supporting Content"),
        4: _("Optional"),
    }
    for ct in coverage.get("content_types", []):
        p = ct.get("priority", 4)
        label = priority_labels.get(p, _("Other"))
        groups.setdefault(p, {"label": label, "items": []})
        groups[p]["items"].append(ct)

    sorted_groups = [groups[k] for k in sorted(groups.keys())]

    # Serialize for JS
    import json as json_module

    from django.utils.safestring import mark_safe

    coverage_json = mark_safe(json_module.dumps(coverage, default=str))

    context = {
        "title": _("Translation Coverage"),
        "coverage": coverage,
        "coverage_json": coverage_json,
        "groups": sorted_groups,
    }
    return render(request, "admin/translations/coverage_detail.html", context)


@staff_member_required
@require_http_methods(["GET"])
def coverage_api(request):
    """API endpoint returning coverage data as JSON."""
    from .coverage_service import TranslationCoverageService

    try:
        coverage = TranslationCoverageService().get_site_coverage()
        return JsonResponse({"success": True, **coverage})
    except Exception as e:
        logger.error(f"Coverage API error: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def coverage_refresh_api(request):
    """Invalidate coverage cache and return fresh data."""
    from .coverage_service import TranslationCoverageService, invalidate_coverage_cache

    invalidate_coverage_cache()
    try:
        coverage = TranslationCoverageService().get_site_coverage(use_cache=False)
        return JsonResponse({"success": True, **coverage})
    except Exception as e:
        logger.error(f"Coverage refresh error: {e}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# ============================================================================
# Translate All Views
# ============================================================================


@staff_member_required
@require_http_methods(["GET"])
def translate_all_estimate_api(request):
    """Estimate the scope of a translate-all operation."""
    from .coverage_service import TranslationCoverageService

    service = TranslationCoverageService()
    target_languages = service._get_target_languages()

    if not target_languages:
        return JsonResponse(
            {
                "success": True,
                "total_jobs": 0,
                "total_fields": 0,
                "content_types": [],
                "languages": [],
                "is_large": False,
            }
        )

    [lang["code"] for lang in target_languages]
    coverage = service.get_site_coverage()
    content_estimates = []
    total_missing = 0
    total_jobs = 0

    for ct_data in coverage.get("content_types", []):
        ct_key = ct_data["key"]
        missing = ct_data["total_fields"] - ct_data["translated_fields"]
        if missing <= 0:
            continue

        # Estimate job count: one per language, split into batches of 50 items
        item_count = ct_data.get("item_count", 0)
        jobs_for_ct = 0
        for lang in target_languages:
            code = lang["code"]
            bl = ct_data.get("by_language", {}).get(code, {})
            lang_missing = bl.get("total", 0) - bl.get("translated", 0)
            if lang_missing > 0:
                batches = max(1, (item_count + 49) // 50) if item_count > 50 else 1
                jobs_for_ct += batches

        total_missing += missing
        total_jobs += jobs_for_ct
        content_estimates.append(
            {
                "key": ct_key,
                "label": ct_data["label"],
                "icon": ct_data["icon"],
                "missing_fields": missing,
                "jobs": jobs_for_ct,
            }
        )

    return JsonResponse(
        {
            "success": True,
            "total_jobs": total_jobs,
            "total_fields": total_missing,
            "content_types": content_estimates,
            "languages": [
                {"code": lang["code"], "name": lang["name"]} for lang in target_languages
            ],
            "is_large": total_missing > 1000 or total_jobs > 20,
        }
    )


@staff_member_required
@require_http_methods(["POST"])
def translate_all_api(request):
    """Create translation jobs for all missing content."""
    from .content_registry import get_all_content_types, get_content_type_keys, get_model_class
    from .coverage_service import TranslationCoverageService
    from .tasks import process_translation_job

    service = TranslationCoverageService()
    target_languages = service._get_target_languages()

    if not target_languages:
        return JsonResponse({"success": False, "error": _("No active languages")}, status=400)

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        data = {}

    data.get("scope", "all")
    filter_ct = data.get("content_type")
    filter_lang = data.get("language")

    if filter_lang:
        target_languages = [lang for lang in target_languages if lang["code"] == filter_lang]

    job_ids = []
    get_content_type_keys()

    for ct_entry in get_all_content_types():
        ct_key = ct_entry["key"]
        if filter_ct and ct_key != filter_ct:
            continue

        model_class = get_model_class(ct_key)
        if not model_class:
            continue

        fields = ct_entry["fields"]
        is_simple = ct_entry.get("format") == "simple"

        # Query all instances
        try:
            all_instances = list(model_class.objects.values_list("pk", "translations", *fields))
        except Exception as e:
            logger.warning(f"Translate-all: failed to query {ct_key}: {e}")
            continue

        # Collect all PKs for lock lookups
        all_pks = [row[0] for row in all_instances]

        for lang in target_languages:
            code = lang["code"]

            # Get locked fields for this content type + language
            from translations.lock_service import get_locked_fields

            locked = get_locked_fields(ct_key, all_pks, code)

            # Find instances that need translation for this language
            missing_pks = []
            for row in all_instances:
                pk = row[0]
                translations = row[1] or {}
                source_values = row[2:]

                needs_translation = False
                for i, field_name in enumerate(fields):
                    # Skip locked fields
                    if (pk, field_name) in locked:
                        continue

                    src_val = source_values[i] if i < len(source_values) else None
                    if not src_val:
                        continue

                    if is_simple:
                        if not translations.get(code):
                            needs_translation = True
                            break
                    else:
                        lang_data = translations.get(code, {})
                        if not isinstance(lang_data, dict) or not lang_data.get(field_name):
                            needs_translation = True
                            break

                if needs_translation:
                    missing_pks.append(pk)

            if not missing_pks:
                continue

            # Split into batches of 50
            batch_size = 50
            for i in range(0, len(missing_pks), batch_size):
                batch_pks = missing_pks[i : i + batch_size]
                job = TranslationJob.objects.create(
                    job_type="bulk",
                    source_language="en",
                    target_languages=[code],
                    content_type=ct_key,
                    fields_to_translate=fields,
                    created_by=request.user,
                    translated_data={
                        "object_ids": batch_pks,
                        "language": code,
                        "registry_key": ct_key,
                    },
                )
                process_translation_job.delay(job.id)
                job_ids.append(job.id)

    # UI strings — dispatch auto-translate for each language
    from .tasks import auto_translate_ui_strings

    for lang in target_languages:
        try:
            auto_translate_ui_strings.delay(lang["code"])
        except Exception as e:
            logger.warning(f"Failed to dispatch UI string auto-translate for {lang['code']}: {e}")

    # Email templates — delegate to existing service
    try:
        from email_system.services.translation_service import EmailTemplateTranslationService

        email_service = EmailTemplateTranslationService()
        lang_codes = [lang["code"] for lang in target_languages]
        try:
            email_service.bulk_translate_all_templates(
                target_languages=lang_codes, user=request.user
            )
        except Exception as e:
            logger.warning(f"Failed to translate email templates: {e}")
    except ImportError:
        pass

    return JsonResponse(
        {
            "success": True,
            "job_ids": job_ids,
            "message": _("Created {} translation jobs").format(len(job_ids)),
        }
    )


@staff_member_required
@require_http_methods(["GET"])
def translate_all_status_api(request):
    """Poll status of translate-all jobs."""
    job_ids_str = request.GET.get("job_ids", "")
    if not job_ids_str:
        return JsonResponse(
            {
                "success": True,
                "total_jobs": 0,
                "completed": 0,
                "processing": 0,
                "pending": 0,
                "failed": 0,
                "overall_progress": 0,
            }
        )

    try:
        job_ids = [int(x) for x in job_ids_str.split(",") if x.strip()]
    except ValueError:
        return JsonResponse({"success": False, "error": "Invalid job IDs"}, status=400)

    jobs = TranslationJob.objects.filter(id__in=job_ids)
    total = jobs.count()
    completed = jobs.filter(status="completed").count()
    processing = jobs.filter(status="processing").count()
    pending = jobs.filter(status="pending").count()
    failed = jobs.filter(status="failed").count()

    overall_progress = round((completed / total * 100), 0) if total > 0 else 0

    return JsonResponse(
        {
            "success": True,
            "total_jobs": total,
            "completed": completed,
            "processing": processing,
            "pending": pending,
            "failed": failed,
            "overall_progress": int(overall_progress),
        }
    )


# ============================================================
# Translation Lock Endpoints
# ============================================================


@staff_member_required
@require_http_methods(["POST"])
def toggle_translation_lock_api(request):
    """Toggle lock on a model-field translation."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    content_type = data.get("content_type")
    object_id = data.get("object_id")
    field_name = data.get("field_name")
    language = data.get("language")

    if not all([content_type, object_id, field_name, language]):
        return JsonResponse(
            {
                "success": False,
                "error": "content_type, object_id, field_name, and language are required",
            },
            status=400,
        )

    from .lock_service import toggle_field_lock

    is_locked = toggle_field_lock(content_type, object_id, field_name, language, request.user)

    return JsonResponse({"success": True, "is_locked": is_locked})


@staff_member_required
@require_http_methods(["POST"])
def ui_translation_lock_api(request, language_code):
    """Toggle lock on a UI string translation."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    string_key = data.get("key")
    if not string_key:
        return JsonResponse({"success": False, "error": "key is required"}, status=400)

    from .models import SiteLanguage, UITranslationOverride

    try:
        site_lang = SiteLanguage.objects.get(code=language_code, is_active=True)
    except SiteLanguage.DoesNotExist:
        return JsonResponse({"success": False, "error": "Language not found"}, status=404)

    override, _ = UITranslationOverride.objects.get_or_create(
        language=site_lang, defaults={"total_strings": 0}
    )

    meta = override.meta_info or {}
    key_meta = meta.get(string_key, {})
    if not isinstance(key_meta, dict):
        key_meta = {}
    key_meta["locked"] = not key_meta.get("locked", False)
    meta[string_key] = key_meta
    override.meta_info = meta
    override.save(update_fields=["meta_info"])

    # Invalidate cache
    from django.core.cache import cache

    cache.delete(f"ui_trans_overrides:{language_code}")

    return JsonResponse({"success": True, "is_locked": key_meta["locked"]})


# ============================================================================
# Translation Jobs Bulk Actions
# ============================================================================


@staff_member_required
@require_http_methods(["POST"])
def bulk_job_action_api(request):
    """Handle bulk actions on translation jobs via AJAX"""
    try:
        data = json.loads(request.body)
        action = data.get("action")
        job_ids = data.get("job_ids", [])

        if not action or not job_ids:
            return JsonResponse(
                {"success": False, "error": _("Action and job IDs required")}, status=400
            )

        jobs = TranslationJob.objects.filter(id__in=job_ids)

        if action == "cancel":
            cancellable = jobs.filter(status__in=["pending", "processing"])
            count = cancellable.update(status="cancelled")
            message = _("{} job(s) cancelled").format(count)

        elif action == "retry":
            retryable = jobs.filter(status="failed")
            count = 0
            for job in retryable:
                job.status = "pending"
                job.retry_count = getattr(job, "retry_count", 0) + 1
                job.error_message = ""
                job.save(update_fields=["status", "retry_count", "error_message"])
                count += 1
            message = _("{} job(s) queued for retry").format(count)

        elif action == "delete":
            count = jobs.count()
            jobs.delete()
            message = _("{} job(s) deleted").format(count)

        else:
            return JsonResponse({"success": False, "error": _("Unknown action")}, status=400)

        return JsonResponse({"success": True, "message": str(message)})

    except Exception as e:
        logger.error("Translation job bulk action error: %s", e, exc_info=True)
        return JsonResponse(
            {"success": False, "error": _("An unexpected error occurred. Please try again.")},
            status=500,
        )
