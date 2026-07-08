"""
Credential Transfer Handler

Handles secure credential transfer between Spwig installations.
Strategy: decrypt on source, transmit over HTTPS, re-encrypt on target.
Sandbox credentials are auto-excluded when syncing to production.
"""
import logging

logger = logging.getLogger(__name__)

# Map category keys to their app's encryption module path
CREDENTIAL_ENCRYPTION_MAP = {
    'email_config': {
        'module': 'email_system.utils.encryption',
        'models': {
            'EmailAccount': {
                'field': 'credentials',
                'type': 'binary',  # BinaryField - encrypt returns bytes
            },
        },
    },
    'payment_providers': {
        'module': 'payment_providers.utils.encryption',
        'models': {
            'PaymentProviderAccount': {
                'field': 'credentials_encrypted',
                'type': 'json',  # JSONField - encrypt returns dict
            },
        },
    },
    'shipping_config': {
        'module': 'shipping.utils.encryption',
        'models': {
            'ProviderAccount': {
                'field': 'credentials_encrypted',
                'type': 'json',
            },
        },
    },
    'tax_currency': {
        'module': 'exchange_rates.utils.encryption',
        'models': {
            'ExchangeRateProviderAccount': {
                'field': 'credentials',
                'type': 'binary',
            },
        },
    },
    'sms_config': {
        'module': 'email_system.utils.encryption',  # SMS reuses email encryption utils
        'models': {
            'SMSProviderAccount': {
                'field': 'credentials',
                'type': 'binary',
            },
        },
    },
    'webhooks_integrations': {
        # OAuth provider settings may have encrypted secrets
        'module': None,  # handled per-model
        'models': {},
    },
    'seo_providers': {
        'module': 'seo_generator.utils.encryption',
        'models': {
            'SEOProviderAccount': {
                'field': 'credentials',
                'type': 'binary',
            },
        },
    },
    'product_feed_providers': {
        'module': 'product_feeds.utils.encryption',
        'models': {
            'FeedProviderAccount': {
                'field': 'credentials',
                'type': 'binary',
            },
        },
    },
    'social_connectors': {
        'module': 'email_system.utils.encryption',  # reuses email encryption
        'models': {
            'SocialConnectorAccount': {
                'field': 'credentials',
                'type': 'binary',
            },
        },
    },
    'pos_config': {
        'module': 'payment_providers.utils.encryption',  # reuses payment encryption
        'models': {
            'POSTerminalProvider': {
                'field': 'credentials_encrypted',
                'type': 'json',
            },
        },
    },
}


def _load_encryption_module(module_path):
    """Dynamically import an app's encryption module."""
    import importlib
    try:
        return importlib.import_module(module_path)
    except ImportError:
        logger.warning(f"Encryption module not found: {module_path}")
        return None


def decrypt_credentials_for_export(category_key, model_name, instance):
    """
    Decrypt credentials from a model instance for export.

    Args:
        category_key: Sync category key
        model_name: Model class name (e.g., 'EmailAccount')
        instance: Model instance with encrypted credentials

    Returns:
        dict: Decrypted credential data, or None if decryption fails
    """
    config = CREDENTIAL_ENCRYPTION_MAP.get(category_key, {})
    model_config = config.get('models', {}).get(model_name)
    if not model_config:
        return None

    module = _load_encryption_module(config['module'])
    if not module:
        return None

    field_name = model_config['field']
    encrypted_value = getattr(instance, field_name, None)
    if not encrypted_value:
        return None

    try:
        return module.decrypt_credentials(encrypted_value)
    except Exception as e:
        logger.error(f"Failed to decrypt {model_name}.{field_name}: {e}")
        return None


def encrypt_credentials_for_import(category_key, model_name, plaintext_credentials):
    """
    Re-encrypt credentials for import on the target instance.

    Args:
        category_key: Sync category key
        model_name: Model class name
        plaintext_credentials: dict of plaintext credential data

    Returns:
        Encrypted credentials (bytes or dict depending on the app)
    """
    config = CREDENTIAL_ENCRYPTION_MAP.get(category_key, {})
    model_config = config.get('models', {}).get(model_name)
    if not model_config:
        return None

    module = _load_encryption_module(config['module'])
    if not module:
        return None

    try:
        return module.encrypt_credentials(plaintext_credentials)
    except Exception as e:
        logger.error(f"Failed to encrypt credentials for {model_name}: {e}")
        return None


def redact_credentials(credentials_dict):
    """
    Redact credential values for preview display.
    Shows field names with masked values.

    Args:
        credentials_dict: dict of plaintext credentials

    Returns:
        dict: Same keys with redacted values
    """
    if not credentials_dict:
        return {}

    redacted = {}
    for key, value in credentials_dict.items():
        if value and isinstance(value, str) and len(value) > 4:
            redacted[key] = value[:2] + '***' + value[-2:]
        elif value:
            redacted[key] = '***'
        else:
            redacted[key] = ''
    return redacted


def filter_sandbox_credentials(category_key, item_data, target_is_production):
    """
    Filter out sandbox/test credentials when syncing to production.

    Args:
        category_key: Sync category key
        item_data: dict of item data being synced
        target_is_production: bool

    Returns:
        tuple: (filtered_data, was_filtered)
    """
    if not target_is_production:
        return item_data, False

    if category_key != 'payment_providers':
        return item_data, False

    # Check for sandbox indicators
    sandbox_indicators = [
        'sandbox', 'test', 'staging', 'demo',
        'sk_test_', 'pk_test_',  # Stripe test keys
        'sandbox.paypal',  # PayPal sandbox
    ]

    credentials = item_data.get('_credentials', {})
    if not credentials:
        return item_data, False

    for key, value in credentials.items():
        if isinstance(value, str):
            value_lower = value.lower()
            for indicator in sandbox_indicators:
                if indicator in value_lower:
                    logger.info(
                        f"Filtered sandbox credentials for {item_data.get('name', 'unknown')} "
                        f"(matched '{indicator}' in {key})"
                    )
                    filtered = dict(item_data)
                    filtered.pop('_credentials', None)
                    return filtered, True

    return item_data, False


def get_credential_field_name(category_key, model_name):
    """Get the credential field name for a category/model combination."""
    config = CREDENTIAL_ENCRYPTION_MAP.get(category_key, {})
    model_config = config.get('models', {}).get(model_name)
    if model_config:
        return model_config['field']
    return None
