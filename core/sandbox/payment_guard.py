"""
Sandbox Payment Gateway Guard

Validates that payment providers use test/sandbox credentials when
the platform is in sandbox mode. Prevents live charges in sandbox.

This module is under core/ and will be Cython-compiled in production builds,
making it harder to patch out.
"""

import logging

from core.license import is_sandbox_mode

logger = logging.getLogger(__name__)


class SandboxPaymentError(Exception):
    """Raised when live credentials are detected in sandbox mode."""

    pass


# Accepted test/sandbox environment values (universal across all providers)
_TEST_ENVIRONMENTS = frozenset(
    {
        "test",
        "sandbox",
        "demo",
        "development",
        "dev",
    }
)

# Live environment values that should be rejected in sandbox mode
_LIVE_ENVIRONMENTS = frozenset(
    {
        "live",
        "production",
        "prod",
    }
)

# Provider-specific key prefix rules (for providers whose keys encode the mode)
_KEY_PREFIX_RULES = {
    "stripe": {
        "secret_key": {
            "test_prefixes": ("sk_test_",),
            "live_prefixes": ("sk_live_",),
        },
        "publishable_key": {
            "test_prefixes": ("pk_test_",),
            "live_prefixes": ("pk_live_",),
        },
    },
    "revolut": {
        "secret_key": {
            "test_prefixes": ("sk_test_", "sk_sandbox_"),
            "live_prefixes": ("sk_live_",),
        },
    },
}


def validate_provider_credentials(provider_slug: str, credentials: dict) -> None:
    """
    Validate that provider credentials are for test/sandbox when in sandbox mode.

    This function is a no-op in production mode for zero overhead.

    Supports both NEW dual-credential structure (test_mode boolean + prefixed fields)
    and LEGACY single-credential structure (environment string field).

    Args:
        provider_slug: The provider's slug identifier (e.g., 'stripe', 'airwallex')
        credentials: Decrypted credentials dict

    Raises:
        SandboxPaymentError: If live credentials are detected in sandbox mode
    """
    if not is_sandbox_mode():
        return  # Production mode — no restrictions

    if not credentials:
        return  # No credentials to check

    # Check NEW dual-credential structure first
    test_mode = credentials.get("test_mode")
    if test_mode is not None:  # New structure detected
        if test_mode is False:
            raise SandboxPaymentError(
                f"SANDBOX MODE: Payment provider '{provider_slug}' has test_mode=False. "
                f"Only test credentials are permitted in sandbox mode. Please enable "
                f"test mode in Payment Providers → Edit → Credentials."
            )

        # Ensure test credentials are present
        test_fields = [k for k in credentials if k.startswith("test_")]
        if not test_fields:
            raise SandboxPaymentError(
                f"SANDBOX MODE: Payment provider '{provider_slug}' has test_mode=True "
                f"but no test credentials configured. Please configure test credentials."
            )

        return  # New structure validated, exit early

    # LEGACY: Check old environment field for backward compatibility
    environment = credentials.get("environment", "")
    if isinstance(environment, str) and environment:
        env_lower = environment.lower()

        if env_lower in _LIVE_ENVIRONMENTS:
            raise SandboxPaymentError(
                f"SANDBOX MODE: Payment provider '{provider_slug}' is configured "
                f"with environment='{environment}'. Live/production credentials are "
                f"not permitted in sandbox mode. Please switch to test/sandbox "
                f"credentials in Payment Providers settings."
            )

        if env_lower not in _TEST_ENVIRONMENTS:
            # Unknown environment value — warn but allow (could be a custom value)
            logger.warning(
                f"[SANDBOX] Payment provider '{provider_slug}' has unrecognized "
                f"environment='{environment}'. Expected one of: {_TEST_ENVIRONMENTS}"
            )

    # Check 2: Key prefix validation (Stripe, Revolut)
    prefix_rules = _KEY_PREFIX_RULES.get(provider_slug)
    if prefix_rules:
        for field_name, rules in prefix_rules.items():
            value = credentials.get(field_name, "")
            if not value or not isinstance(value, str):
                continue

            # Check if this looks like a live key
            live_prefixes = rules.get("live_prefixes", ())
            if any(value.startswith(prefix) for prefix in live_prefixes):
                test_prefixes = rules.get("test_prefixes", ())
                raise SandboxPaymentError(
                    f"SANDBOX MODE: Payment provider '{provider_slug}' has a live "
                    f"key for '{field_name}' (starts with "
                    f"'{value[:8]}...'). Only test keys are permitted in sandbox "
                    f"mode. Expected prefix: {test_prefixes}"
                )
