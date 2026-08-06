"""
Provider-agnostic client bundle for storefront-mounted provider UIs.

Both the one-time charge flow and the subscription reusable-method setup flow
need to tell the client WHICH provider to render and load its SDK + handler.
This builds that bundle purely from the provider component's manifest — no
gateway is ever named — including resolving ``{{VAR}}`` templates in the SDK
URLs from the account's credentials (e.g. PayPal's ``client-id={{CLIENT_ID}}``),
mirroring the charge flow so setup loads the same, correctly-parameterised SDKs.
"""

import logging

logger = logging.getLogger(__name__)


def resolve_sdk_dependencies(provider_account) -> list[str]:
    """Resolve ``{{VAR}}`` templates in a provider's manifest sdk_dependencies.

    Supports direct credential substitution (``{{CLIENT_ID}}`` / ``{{client_id}}``)
    and mapped variables via ``frontend.sdk_variable_map`` (e.g. environment →
    host). Returns the URLs unchanged if there is nothing to resolve.
    """
    component = getattr(provider_account, "component", None)
    if not component:
        return []
    try:
        manifest = component.get_manifest() or {}
    except Exception:
        logger.exception("Could not load manifest for %s", getattr(component, "slug", "?"))
        return []

    frontend = manifest.get("frontend") or {}
    urls = frontend.get("sdk_dependencies") or []
    if not urls:
        return []

    try:
        from payment_providers.utils.encryption import decrypt_credentials

        settings = decrypt_credentials(provider_account.credentials_encrypted) or {}
    except Exception:
        settings = {}
    variable_map = frontend.get("sdk_variable_map", {}) or {}

    resolved = []
    for url in urls:
        # Mapped variables first (e.g. environment name → hostname).
        for var_name, mapping in variable_map.items():
            placeholder = "{{" + var_name + "}}"
            if placeholder in url and isinstance(mapping, dict):
                source_key = mapping.get("_source", var_name)
                credential_value = settings.get(source_key, "")
                resolved_value = mapping.get(credential_value, "")
                if resolved_value:
                    url = url.replace(placeholder, str(resolved_value))
        # Then direct credential substitutions (upper and lower case).
        for key, value in settings.items():
            url = url.replace("{{" + key.upper() + "}}", str(value))
            url = url.replace("{{" + key + "}}", str(value))
        resolved.append(url)
    return resolved


def build_client_bundle(provider_account) -> dict:
    """Manifest-driven client bundle: ``{provider_key, handler_url, sdk_dependencies}``.

    No gateway is named — every field comes from the component's manifest
    (``frontend.checkout_handler`` / ``frontend.sdk_dependencies``). The client
    dispatches on ``provider_key`` through the shared ``window.PaymentHandlers``
    registry.
    """
    component = getattr(provider_account, "component", None)
    slug = component.slug if component else ""
    bundle = {"provider_key": slug, "handler_url": None, "sdk_dependencies": []}
    if not component:
        return bundle
    try:
        manifest = component.get_manifest() or {}
        frontend = manifest.get("frontend") or {}
        handler_file = frontend.get("checkout_handler")
        if handler_file:
            bundle["handler_url"] = f"/components/payments/{slug}/current/{handler_file}"
        bundle["sdk_dependencies"] = resolve_sdk_dependencies(provider_account)
    except Exception:
        logger.exception("Failed to build client bundle for %s", slug)
    return bundle
