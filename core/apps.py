"""
Core application configuration
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the core app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core Platform"

    def ready(self):
        """
        Called when Django starts. Connects signals and fetches platform secrets
        from license server in background thread if not already initialized.
        """
        import logging
        import sys
        import threading

        logger = logging.getLogger(__name__)

        # Connect signal handlers for 2FA trusted device management
        from core.signals import connect_signals

        connect_signals()

        # Register Django system checks
        from . import checks  # noqa

        # Patch MoneyField currency defaults to use merchant's configured currency
        _patch_money_field_currency_defaults(logger)

        # Bootstrap Community licence if no licence file exists. Safe to run
        # for every management command (no DB access, idempotent). Skipped
        # during makemigrations to avoid coupling migrations to filesystem state.
        if "makemigrations" not in sys.argv:
            _bootstrap_community_licence(logger)

        # Determine if we're running as a web server (not management command/migrations)
        is_server = False
        if sys.argv:
            # Check for runserver, gunicorn, or uvicorn
            cmd = sys.argv[0] if sys.argv else ""
            args = " ".join(sys.argv)
            if "runserver" in args or "gunicorn" in cmd or "uvicorn" in cmd:
                is_server = True

        # Also check for Celery worker (needs secrets too)
        is_celery = "celery" in " ".join(sys.argv) if sys.argv else False

        if not (is_server or is_celery):
            return

        def fetch_secrets_and_activate_license():
            """
            Background task to:
            1. Activate license if LICENSE_KEY is set but no valid license file exists
            2. Fetch platform secrets from license server
            Runs in daemon thread so it doesn't block startup.
            """
            import os
            import time

            # Brief delay to ensure DB connections are ready
            time.sleep(2)

            # Step 1: Check and activate license if needed
            try:
                from component_updates.models import UpdateServerConfig
                from core.license import get_license_manager

                license_manager = get_license_manager()

                # Check if we already have a valid license
                if not license_manager.is_valid():
                    # Check if LICENSE_KEY is set in environment
                    env_license_key = os.environ.get("LICENSE_KEY", "").strip()

                    # Also check UpdateServerConfig
                    update_config = UpdateServerConfig.get_instance()

                    # If env has license key but config doesn't, update config
                    if env_license_key and not update_config.license_key:
                        update_config.license_key = env_license_key
                        update_config.save()
                        logger.info("Stored LICENSE_KEY from environment in UpdateServerConfig")

                    license_key = update_config.license_key or env_license_key

                    if license_key:
                        logger.info("No valid license file found, attempting auto-activation...")
                        _auto_activate_license(license_key, update_config, logger)
                    else:
                        logger.info(
                            "No license key configured - running in Trial mode (payment processing disabled)"
                        )
                else:
                    logger.debug("Valid license file already exists")

                    # Ensure UpdateServerConfig has the license key synced from license.json
                    # This covers cases where the license file was deployed directly
                    # (e.g. Docker volume, manual copy) without going through the
                    # admin activation flow that normally syncs both.
                    update_config = UpdateServerConfig.get_instance()
                    if not update_config.license_key:
                        license_data = license_manager.get_license_data() or {}
                        license_info = license_data.get("license", {})
                        file_key = license_info.get("license_key", "")
                        if file_key:
                            update_config.license_key = file_key
                            update_config.save()
                            logger.info(
                                "Synced license key from license.json to UpdateServerConfig"
                            )

            except Exception as e:
                logger.warning(f"License activation check failed: {e}")
                # Non-fatal - shop will run in trial mode

            # Step 2: Fetch platform secrets
            try:
                from core.models import PlatformSecrets

                secrets = PlatformSecrets.get_secrets()

                if not secrets.is_initialized:
                    logger.info("Platform secrets not initialized, fetching from license server...")
                    from component_updates.services import UpdateManager

                    manager = UpdateManager()
                    # This will authenticate and store secrets
                    manager._ensure_authenticated()

                    # Verify secrets were stored
                    secrets.refresh_from_db()
                    if secrets.is_initialized:
                        logger.info("✅ Platform secrets fetched and stored successfully")
                    else:
                        logger.warning("⚠️ Authenticated but platform secrets not fully initialized")
                else:
                    logger.debug("Platform secrets already initialized")

            except Exception as e:
                logger.warning(f"Could not fetch platform secrets on startup: {e}")
                # Non-fatal - services will fall back to env vars or retry later

            # Step 3: Startup telemetry ping (best-effort, opt-out via SPWIG_TELEMETRY=0)
            try:
                from django.conf import settings as dj_settings

                if getattr(dj_settings, "SPWIG_TELEMETRY_ENABLED", True):
                    from core.telemetry.client import send_telemetry

                    send_telemetry()
                else:
                    logger.debug("Telemetry disabled; startup ping skipped")
            except Exception as e:
                logger.debug(f"Startup telemetry ping failed: {e}")
                # Non-fatal — daily beat task will retry.

        # Run in background thread to not block startup
        thread = threading.Thread(
            target=fetch_secrets_and_activate_license, daemon=True, name="platform-startup"
        )
        thread.start()
        logger.debug("Started background platform startup thread")


def _bootstrap_community_licence(logger):
    """
    Install the Community licence at LICENSE_PATH if no licence exists.

    Called from CoreConfig.ready() on every startup. Idempotent — a paid
    licence at LICENSE_PATH is never overwritten. Reuses the template path
    defined by the ``bootstrap_community_licence`` management command so both
    entry points stay in sync.
    """
    import shutil
    from pathlib import Path

    from django.conf import settings

    try:
        from core.management.commands.bootstrap_community_licence import (
            COMMUNITY_LICENCE_TEMPLATE,
        )
    except Exception as e:
        logger.warning(f"Could not load Community licence bootstrap: {e}")
        return

    try:
        target = Path(settings.LICENSE_PATH)
        if target.exists():
            return  # Respect any existing licence (Community or paid)

        if not COMMUNITY_LICENCE_TEMPLATE.exists():
            logger.warning(
                f"Community licence template missing at {COMMUNITY_LICENCE_TEMPLATE}. "
                "Run tools/oss/sign_community_licence.py to generate it."
            )
            return

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(COMMUNITY_LICENCE_TEMPLATE, target)
        logger.info(f"Bootstrapped Community licence at {target}")
    except Exception as e:
        # Non-fatal — logs and continues. Downstream code that expects a
        # licence will surface a clearer error.
        logger.warning(f"Community licence bootstrap failed: {e}")


def _patch_money_field_currency_defaults(logger):
    """
    Patch all MoneyField companion CurrencyFields to use the merchant's
    configured default currency instead of hardcoded 'USD'.

    django-money's MoneyField.default_currency only accepts a string literal,
    but the companion CurrencyField inherits from Django's CharField, which
    natively supports callables for the `default` parameter via
    Field.get_default(). We patch _currency_field.default to a callable that
    reads SiteSettings.default_currency at record-creation time.

    Skipped during makemigrations to avoid spurious migration detection.
    """
    import sys

    if "makemigrations" in sys.argv:
        return

    from django.apps import apps

    try:
        from djmoney.models.fields import MoneyField as DjMoneyField
    except ImportError:
        return

    def _get_merchant_currency():
        try:
            from core.utils import get_default_currency

            return get_default_currency()
        except Exception:
            return "USD"

    SKIP_APP_LABELS = {"license_checkout"}
    patched = 0

    for model in apps.get_models():
        if model._meta.app_label in SKIP_APP_LABELS:
            continue
        for field in model._meta.get_fields():
            if isinstance(field, DjMoneyField) and hasattr(field, "_currency_field"):
                if field.default_currency is None:
                    continue  # Multi-currency fields — stay None
                field._currency_field.default = _get_merchant_currency
                patched += 1

    logger.debug(f"Patched {patched} MoneyField currency defaults to use SiteSettings")


def _auto_activate_license(license_key, update_config, logger):
    """
    Attempt to activate license by calling the update server API.
    """
    import hashlib
    import hmac
    import json
    import secrets as secrets_module
    from pathlib import Path

    import requests

    import core

    try:
        # Generate random challenge
        challenge = secrets_module.token_urlsafe(32)
        installation_uuid = str(update_config.installation_uuid)
        platform_version = core.__version__

        # Get domain from SiteSettings (set during installation from $DOMAIN)
        domain = ""
        try:
            from core.models import SiteSettings

            site_settings = SiteSettings.objects.filter(pk=1).first()
            if site_settings and site_settings.site_url:
                from urllib.parse import urlparse

                parsed = urlparse(site_settings.site_url)
                domain = parsed.netloc or parsed.path
        except Exception:
            pass

        # Call update server activation API
        activation_url = f"{update_config.server_url}/api/v1/licenses/activate/"

        payload = {
            "license_key": license_key,
            "installation_uuid": installation_uuid,
            "domain": domain,
            "platform_version": platform_version,
            "environment_type": "production",
            "challenge": challenge,
        }

        response = requests.post(activation_url, json=payload, timeout=30)

        if response.status_code != 200:
            error_data = (
                response.json()
                if response.headers.get("content-type", "").startswith("application/json")
                else {}
            )
            logger.warning(
                f"License activation failed: {error_data.get('message', 'Unknown error')}"
            )
            return

        activation_data = response.json()

        # Verify challenge response
        expected_response = hmac.new(
            license_key.encode(), (challenge + installation_uuid).encode(), hashlib.sha256
        ).hexdigest()

        if activation_data.get("challenge_response") != expected_response:
            logger.error("License activation failed: challenge verification failed")
            return

        # Build license file
        license_data = {
            "license": activation_data["license"],
            "signature": activation_data["signature"],
        }

        # Verify signature locally
        from core.license import get_license_manager, reload_license_manager

        license_manager = get_license_manager()

        if not license_manager.verify_signature(license_data):
            logger.error("License activation failed: signature verification failed")
            return

        # Save license file
        license_path = Path(license_manager.license_path)
        license_path.parent.mkdir(parents=True, exist_ok=True)

        with open(license_path, "w") as f:
            json.dump(license_data, f, indent=2)

        # Ensure UpdateServerConfig has the canonical key from the server response
        canonical_key = activation_data["license"].get("license_key", "")
        if canonical_key and update_config.license_key != canonical_key:
            update_config.license_key = canonical_key
            update_config.save()

        # Reload license manager
        reload_license_manager()

        license_type = activation_data["license"].get("license_type", "unknown")
        logger.info(f"✅ License activated successfully! Type: {license_type}")

    except requests.exceptions.Timeout:
        logger.warning("License activation timeout - will retry on next startup")
    except requests.exceptions.ConnectionError:
        logger.warning("Could not connect to update server for license activation")
    except Exception as e:
        logger.warning(f"License auto-activation failed: {e}")
