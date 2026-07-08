"""
Provider Common Utilities Unit Tests.

Comprehensive tests covering all functions in providers_common/utils.py:
- load_manifest_translations: file I/O, JSON parsing, translation extraction
- get_translated_provider_fields: language lookup, fallback chain, partial translations
- validate_credential_fields: required, max/min_length, boolean, multiselect, label fallback
- validate_dual_environment_credentials: test/live mode, env-prefixed required fields
"""
import json
import os
import tempfile

import pytest
from django.http import QueryDict

from providers_common.utils import (
    get_translated_provider_fields,
    load_manifest_translations,
    validate_credential_fields,
    validate_dual_environment_credentials,
)

pytestmark = [pytest.mark.providers_common]


# ============================================================
# Helpers
# ============================================================

def _make_querydict(data: dict) -> QueryDict:
    """
    Build a Django QueryDict from a plain dict.

    Supports list values for multiselect fields (key appears multiple times).
    """
    qd = QueryDict(mutable=True)
    for key, value in data.items():
        if isinstance(value, list):
            qd.setlist(key, value)
        else:
            qd[key] = value
    qd._mutable = False
    return qd


# ============================================================
# load_manifest_translations
# ============================================================

class TestLoadManifestTranslations:
    """Tests for loading translations from a component's manifest.json."""

    def test_valid_manifest_with_translations_returns_dict(self, tmp_path):
        """A manifest with a translations dict returns it plus default_language."""
        manifest = {
            'name': 'Stripe',
            'translations': {
                'es': {'meta.name': 'Stripe ES'},
                'fr': {'meta.name': 'Stripe FR'},
            },
        }
        (tmp_path / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

        result = load_manifest_translations(tmp_path)

        assert result is not None
        assert result['es'] == {'meta.name': 'Stripe ES'}
        assert result['fr'] == {'meta.name': 'Stripe FR'}
        # default_language defaults to 'en' when not specified
        assert result['default_language'] == 'en'

    def test_manifest_with_explicit_default_language(self, tmp_path):
        """When default_language is specified in the manifest, it is used."""
        manifest = {
            'name': 'Provider DE',
            'default_language': 'de',
            'translations': {
                'en': {'meta.name': 'Provider EN'},
            },
        }
        (tmp_path / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

        result = load_manifest_translations(tmp_path)

        assert result is not None
        assert result['default_language'] == 'de'

    def test_no_default_language_defaults_to_en(self, tmp_path):
        """When default_language is absent, it defaults to 'en'."""
        manifest = {
            'translations': {'ja': {'meta.name': 'JP Name'}},
        }
        (tmp_path / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

        result = load_manifest_translations(tmp_path)

        assert result is not None
        assert result['default_language'] == 'en'

    def test_manifest_without_translations_key_returns_none(self, tmp_path):
        """A manifest that has no 'translations' key returns None."""
        manifest = {'name': 'PayPal', 'version': '1.0.0'}
        (tmp_path / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

        result = load_manifest_translations(tmp_path)

        assert result is None

    def test_manifest_file_does_not_exist_returns_none(self, tmp_path):
        """A directory with no manifest.json returns None."""
        result = load_manifest_translations(tmp_path)

        assert result is None

    def test_malformed_json_returns_none(self, tmp_path):
        """A manifest with invalid JSON returns None gracefully."""
        (tmp_path / 'manifest.json').write_text('{not valid json!!!', encoding='utf-8')

        result = load_manifest_translations(tmp_path)

        assert result is None

    def test_translations_is_not_a_dict_returns_none(self, tmp_path):
        """When translations is a list or string instead of dict, returns None."""
        manifest = {
            'name': 'Provider',
            'translations': ['es', 'fr'],  # list, not dict
        }
        (tmp_path / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

        result = load_manifest_translations(tmp_path)

        assert result is None

    def test_translations_is_empty_dict_returns_none(self, tmp_path):
        """An empty translations dict is falsy, so returns None."""
        manifest = {
            'name': 'Provider',
            'translations': {},
        }
        (tmp_path / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

        result = load_manifest_translations(tmp_path)

        assert result is None

    def test_translations_is_string_returns_none(self, tmp_path):
        """When translations is a plain string, returns None."""
        manifest = {
            'name': 'Provider',
            'translations': 'some_string',
        }
        (tmp_path / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

        result = load_manifest_translations(tmp_path)

        assert result is None

    def test_does_not_mutate_original_translations(self, tmp_path):
        """Adding default_language to the result does not modify the original translations dict."""
        translations_data = {'es': {'meta.name': 'Nombre'}}
        manifest = {
            'name': 'Provider',
            'translations': translations_data,
        }
        (tmp_path / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

        result = load_manifest_translations(tmp_path)

        # The result has default_language, but re-reading the file should show
        # the original translations remain untouched (the function creates a copy).
        assert 'default_language' in result
        # Read the file again to confirm it was not modified on disk
        with open(tmp_path / 'manifest.json', 'r') as f:
            original = json.load(f)
        assert 'default_language' not in original['translations']

    def test_manifest_with_translations_null_returns_none(self, tmp_path):
        """When translations is explicitly null/None in JSON, returns None."""
        manifest = {
            'name': 'Provider',
            'translations': None,
        }
        (tmp_path / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

        result = load_manifest_translations(tmp_path)

        assert result is None


# ============================================================
# get_translated_provider_fields
# ============================================================

class TestGetTranslatedProviderFields:
    """Tests for translating provider name and description from manifests."""

    def test_requested_lang_matches_default_returns_base(self):
        """When requested lang matches default_language, base name/description returned."""
        manifest = {
            'name': 'Stripe Payment',
            'description': 'Accept credit cards',
            'default_language': 'en',
            'translations': {
                'es': {'meta.name': 'Pago con Stripe', 'meta.description': 'Aceptar tarjetas'},
            },
        }

        result = get_translated_provider_fields(manifest, 'en')

        assert result['name'] == 'Stripe Payment'
        assert result['description'] == 'Accept credit cards'

    def test_requested_lang_has_full_translations(self):
        """When the requested lang has both name and description translations, both are used."""
        manifest = {
            'name': 'Stripe Payment',
            'description': 'Accept credit cards',
            'default_language': 'en',
            'translations': {
                'es': {
                    'meta.name': 'Pago con Stripe',
                    'meta.description': 'Aceptar tarjetas de credito',
                },
            },
        }

        result = get_translated_provider_fields(manifest, 'es')

        assert result['name'] == 'Pago con Stripe'
        assert result['description'] == 'Aceptar tarjetas de credito'

    def test_requested_lang_has_no_translations_falls_back_to_base(self):
        """When the requested lang has no translations, base content is returned."""
        manifest = {
            'name': 'PayPal',
            'description': 'Pay with PayPal',
            'default_language': 'en',
            'translations': {
                'es': {'meta.name': 'PayPal ES'},
            },
        }

        result = get_translated_provider_fields(manifest, 'ja')

        assert result['name'] == 'PayPal'
        assert result['description'] == 'Pay with PayPal'

    def test_partial_translation_only_name(self):
        """When only meta.name is translated, description stays as base."""
        manifest = {
            'name': 'Stripe',
            'description': 'Credit card payments',
            'default_language': 'en',
            'translations': {
                'fr': {'meta.name': 'Stripe FR'},
            },
        }

        result = get_translated_provider_fields(manifest, 'fr')

        assert result['name'] == 'Stripe FR'
        assert result['description'] == 'Credit card payments'

    def test_partial_translation_only_description(self):
        """When only meta.description is translated, name stays as base."""
        manifest = {
            'name': 'Stripe',
            'description': 'Credit card payments',
            'default_language': 'en',
            'translations': {
                'de': {'meta.description': 'Kreditkartenzahlungen'},
            },
        }

        result = get_translated_provider_fields(manifest, 'de')

        assert result['name'] == 'Stripe'
        assert result['description'] == 'Kreditkartenzahlungen'

    def test_empty_manifest_returns_empty_strings(self):
        """An empty manifest returns empty name and description."""
        result = get_translated_provider_fields({}, 'en')

        assert result['name'] == ''
        assert result['description'] == ''

    def test_manifest_without_translations_key(self):
        """A manifest with no translations key returns base name/description."""
        manifest = {
            'name': 'Simple Provider',
            'description': 'No translations available',
        }

        result = get_translated_provider_fields(manifest, 'fr')

        assert result['name'] == 'Simple Provider'
        assert result['description'] == 'No translations available'

    def test_non_default_language_with_empty_lang_dict(self):
        """When the lang exists in translations but is an empty dict, base content returned."""
        manifest = {
            'name': 'Provider',
            'description': 'Base description',
            'default_language': 'en',
            'translations': {
                'ko': {},
            },
        }

        result = get_translated_provider_fields(manifest, 'ko')

        assert result['name'] == 'Provider'
        assert result['description'] == 'Base description'

    def test_default_language_inferred_as_en(self):
        """When default_language is not in the manifest, it defaults to 'en'."""
        manifest = {
            'name': 'Provider',
            'description': 'Desc',
            'translations': {
                'en': {'meta.name': 'Should NOT be used'},
            },
        }

        # Requesting 'en' matches the default ('en'), so base content is returned
        result = get_translated_provider_fields(manifest, 'en')

        assert result['name'] == 'Provider'
        assert result['description'] == 'Desc'

    def test_non_en_default_language(self):
        """When default_language is 'de', requesting 'de' returns base content."""
        manifest = {
            'name': 'Anbieter',
            'description': 'Beschreibung',
            'default_language': 'de',
            'translations': {
                'en': {'meta.name': 'Provider', 'meta.description': 'Description'},
            },
        }

        # Requesting 'de' matches default, returns base
        result_de = get_translated_provider_fields(manifest, 'de')
        assert result_de['name'] == 'Anbieter'
        assert result_de['description'] == 'Beschreibung'

        # Requesting 'en' uses translation
        result_en = get_translated_provider_fields(manifest, 'en')
        assert result_en['name'] == 'Provider'
        assert result_en['description'] == 'Description'

    def test_translation_with_empty_string_values_preserves_base(self):
        """When translations have empty-string values, base content is preserved (falsy check)."""
        manifest = {
            'name': 'Provider',
            'description': 'Base desc',
            'default_language': 'en',
            'translations': {
                'es': {'meta.name': '', 'meta.description': ''},
            },
        }

        result = get_translated_provider_fields(manifest, 'es')

        # Empty strings are falsy, so the if check fails and base content is kept
        assert result['name'] == 'Provider'
        assert result['description'] == 'Base desc'


# ============================================================
# validate_credential_fields
# ============================================================

class TestValidateCredentialFields:
    """Tests for credential field validation against a manifest schema."""

    # --- Text fields: required ---

    def test_required_text_field_present_passes(self):
        """A required text field with a value produces no errors."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'required': True},
        }
        post = _make_querydict({'api_key': 'sk_test_abc123'})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['api_key'] == 'sk_test_abc123'

    def test_required_text_field_missing_produces_error(self):
        """A required text field that is absent produces a required error."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'required': True},
        }
        post = _make_querydict({})

        creds, errors = validate_credential_fields(schema, post)

        assert len(errors) == 1
        assert 'API Key' in errors[0]
        assert 'required' in errors[0].lower()

    def test_required_text_field_empty_string_produces_error(self):
        """A required text field with empty/whitespace-only value is treated as missing."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'required': True},
        }
        post = _make_querydict({'api_key': '   '})

        creds, errors = validate_credential_fields(schema, post)

        assert len(errors) == 1
        assert 'API Key' in errors[0]

    def test_optional_text_field_missing_no_error(self):
        """An optional text field that is absent produces no errors."""
        schema = {
            'webhook_secret': {'type': 'text', 'label': 'Webhook Secret', 'required': False},
        }
        post = _make_querydict({})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['webhook_secret'] == ''

    def test_optional_text_field_with_value_stored(self):
        """An optional text field with a value is stored correctly."""
        schema = {
            'webhook_secret': {'type': 'text', 'label': 'Webhook Secret'},
        }
        post = _make_querydict({'webhook_secret': 'whsec_xyz'})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['webhook_secret'] == 'whsec_xyz'

    # --- Text fields: max_length ---

    def test_max_length_exceeded_produces_error(self):
        """A text value exceeding max_length produces an error."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'max_length': 10},
        }
        post = _make_querydict({'api_key': 'this_is_too_long_value'})

        creds, errors = validate_credential_fields(schema, post)

        assert len(errors) == 1
        assert 'API Key' in errors[0]
        assert 'at most' in errors[0].lower()
        assert '10' in errors[0]

    def test_max_length_exact_boundary_passes(self):
        """A text value at exactly max_length produces no error."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'max_length': 5},
        }
        post = _make_querydict({'api_key': 'abcde'})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []

    def test_max_length_within_limit_passes(self):
        """A text value under max_length passes."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'max_length': 100},
        }
        post = _make_querydict({'api_key': 'short_key'})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []

    def test_non_numeric_max_length_gracefully_skipped(self):
        """A non-numeric max_length in schema does not crash; validation is skipped."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'max_length': 'not_a_number'},
        }
        post = _make_querydict({'api_key': 'any_value_at_all'})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['api_key'] == 'any_value_at_all'

    # --- Text fields: min_length ---

    def test_min_length_not_met_produces_error(self):
        """A text value shorter than min_length produces an error."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'min_length': 10},
        }
        post = _make_querydict({'api_key': 'short'})

        creds, errors = validate_credential_fields(schema, post)

        assert len(errors) == 1
        assert 'API Key' in errors[0]
        assert 'at least' in errors[0].lower()
        assert '10' in errors[0]

    def test_min_length_exact_boundary_passes(self):
        """A text value at exactly min_length produces no error."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'min_length': 5},
        }
        post = _make_querydict({'api_key': 'abcde'})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []

    def test_min_length_above_minimum_passes(self):
        """A text value above min_length passes."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'min_length': 3},
        }
        post = _make_querydict({'api_key': 'long_enough'})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []

    def test_non_numeric_min_length_gracefully_skipped(self):
        """A non-numeric min_length in schema does not crash; validation is skipped."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'min_length': 'bad'},
        }
        post = _make_querydict({'api_key': 'x'})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['api_key'] == 'x'

    def test_min_and_max_length_both_violated(self):
        """Both min_length and max_length errors can be reported for the same field."""
        # This is an unusual but valid schema where min > max (misconfigured).
        # The function reports both violations independently.
        schema = {
            'code': {'type': 'text', 'label': 'Code', 'min_length': 10, 'max_length': 5},
        }
        post = _make_querydict({'code': 'abcdefg'})  # len=7, > max(5) and < min(10)

        creds, errors = validate_credential_fields(schema, post)

        assert len(errors) == 2

    # --- Text fields: empty value skips length checks ---

    def test_empty_optional_field_skips_min_length_check(self):
        """An empty optional field does not trigger min_length validation."""
        schema = {
            'note': {'type': 'text', 'label': 'Note', 'min_length': 5, 'required': False},
        }
        post = _make_querydict({'note': ''})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []

    def test_empty_optional_field_skips_max_length_check(self):
        """An empty optional field does not trigger max_length validation."""
        schema = {
            'note': {'type': 'text', 'label': 'Note', 'max_length': 5, 'required': False},
        }
        post = _make_querydict({'note': ''})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []

    # --- Text fields: whitespace stripping ---

    def test_text_value_is_stripped(self):
        """Leading/trailing whitespace is stripped from text values."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key'},
        }
        post = _make_querydict({'api_key': '  sk_test_123  '})

        creds, errors = validate_credential_fields(schema, post)

        assert creds['api_key'] == 'sk_test_123'

    # --- Boolean fields ---

    def test_boolean_field_with_on_returns_true(self):
        """A boolean field with value 'on' (checkbox checked) returns True."""
        schema = {
            'sandbox_mode': {'type': 'boolean', 'label': 'Sandbox Mode'},
        }
        post = _make_querydict({'sandbox_mode': 'on'})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['sandbox_mode'] is True

    def test_boolean_field_absent_returns_false(self):
        """A boolean field absent from POST (checkbox unchecked) returns False."""
        schema = {
            'sandbox_mode': {'type': 'boolean', 'label': 'Sandbox Mode'},
        }
        post = _make_querydict({})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['sandbox_mode'] is False

    def test_boolean_field_with_non_on_value_returns_false(self):
        """A boolean field with a value other than 'on' returns False."""
        schema = {
            'sandbox_mode': {'type': 'boolean', 'label': 'Sandbox Mode'},
        }
        post = _make_querydict({'sandbox_mode': 'true'})

        creds, errors = validate_credential_fields(schema, post)

        assert creds['sandbox_mode'] is False

    def test_boolean_field_never_produces_required_error(self):
        """Boolean fields skip required validation (checkbox semantics)."""
        schema = {
            'accept_terms': {'type': 'boolean', 'label': 'Accept Terms', 'required': True},
        }
        post = _make_querydict({})

        creds, errors = validate_credential_fields(schema, post)

        # Booleans use 'continue' before required checks, so no error
        assert errors == []
        assert creds['accept_terms'] is False

    # --- Multiselect fields ---

    def test_multiselect_with_valid_options_passes(self):
        """A multiselect field with valid options produces no errors."""
        schema = {
            'currencies': {
                'type': 'multiselect',
                'label': 'Currencies',
                'options': [
                    {'value': 'USD', 'label': 'US Dollar'},
                    {'value': 'EUR', 'label': 'Euro'},
                    {'value': 'GBP', 'label': 'British Pound'},
                ],
            },
        }
        post = _make_querydict({'currencies': ['USD', 'EUR']})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['currencies'] == ['USD', 'EUR']

    def test_multiselect_with_invalid_option_produces_error(self):
        """A multiselect field with an invalid option produces an error."""
        schema = {
            'currencies': {
                'type': 'multiselect',
                'label': 'Currencies',
                'options': [
                    {'value': 'USD', 'label': 'US Dollar'},
                    {'value': 'EUR', 'label': 'Euro'},
                ],
            },
        }
        post = _make_querydict({'currencies': ['USD', 'BTC']})

        creds, errors = validate_credential_fields(schema, post)

        assert len(errors) == 1
        assert 'Currencies' in errors[0]
        assert 'BTC' in errors[0]

    def test_multiselect_required_but_empty_produces_error(self):
        """A required multiselect field with no selection produces an error."""
        schema = {
            'currencies': {
                'type': 'multiselect',
                'label': 'Supported Currencies',
                'required': True,
                'options': [
                    {'value': 'USD', 'label': 'US Dollar'},
                ],
            },
        }
        post = _make_querydict({})

        creds, errors = validate_credential_fields(schema, post)

        assert len(errors) == 1
        assert 'Supported Currencies' in errors[0]
        assert 'required' in errors[0].lower()

    def test_multiselect_optional_empty_no_error(self):
        """An optional multiselect with no selection produces no errors."""
        schema = {
            'currencies': {
                'type': 'multiselect',
                'label': 'Currencies',
                'required': False,
                'options': [
                    {'value': 'USD', 'label': 'US Dollar'},
                ],
            },
        }
        post = _make_querydict({})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['currencies'] == []

    def test_multiselect_no_options_defined_skips_validation(self):
        """A multiselect with no 'options' in schema skips choice validation."""
        schema = {
            'regions': {
                'type': 'multiselect',
                'label': 'Regions',
            },
        }
        post = _make_querydict({'regions': ['us-east', 'eu-west']})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['regions'] == ['us-east', 'eu-west']

    def test_multiselect_all_invalid_options(self):
        """All invalid options are listed in the error message."""
        schema = {
            'modes': {
                'type': 'multiselect',
                'label': 'Modes',
                'options': [
                    {'value': 'a', 'label': 'A'},
                ],
            },
        }
        post = _make_querydict({'modes': ['x', 'y', 'z']})

        creds, errors = validate_credential_fields(schema, post)

        assert len(errors) == 1
        assert 'x' in errors[0]
        assert 'y' in errors[0]
        assert 'z' in errors[0]

    # --- Label fallback: 'label' vs 'title' ---

    def test_label_used_when_present(self):
        """Error messages use 'label' key when both label and title are present."""
        schema = {
            'key': {'type': 'text', 'label': 'API Key Label', 'title': 'API Key Title', 'required': True},
        }
        post = _make_querydict({})

        creds, errors = validate_credential_fields(schema, post)

        assert 'API Key Label' in errors[0]
        assert 'API Key Title' not in errors[0]

    def test_title_used_when_no_label(self):
        """Error messages fall back to 'title' when 'label' is not present."""
        schema = {
            'key': {'type': 'text', 'title': 'API Key Title', 'required': True},
        }
        post = _make_querydict({})

        creds, errors = validate_credential_fields(schema, post)

        assert 'API Key Title' in errors[0]

    def test_field_name_used_when_no_label_or_title(self):
        """Error messages fall back to the field name when both label and title are absent."""
        schema = {
            'secret_key': {'type': 'text', 'required': True},
        }
        post = _make_querydict({})

        creds, errors = validate_credential_fields(schema, post)

        assert 'secret_key' in errors[0]

    # --- Type defaults ---

    def test_type_defaults_to_text_when_absent(self):
        """A field with no type specification is treated as text."""
        schema = {
            'api_key': {'label': 'API Key', 'required': True},
        }
        post = _make_querydict({'api_key': 'value123'})

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds['api_key'] == 'value123'

    # --- Multiple fields ---

    def test_multiple_fields_all_valid(self):
        """Multiple fields, all valid, produce no errors and correct credentials."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'required': True},
            'secret': {'type': 'text', 'label': 'Secret', 'required': True},
            'sandbox': {'type': 'boolean', 'label': 'Sandbox'},
        }
        post = _make_querydict({
            'api_key': 'pk_test_123',
            'secret': 'sk_test_456',
            'sandbox': 'on',
        })

        creds, errors = validate_credential_fields(schema, post)

        assert errors == []
        assert creds == {
            'api_key': 'pk_test_123',
            'secret': 'sk_test_456',
            'sandbox': True,
        }

    def test_multiple_fields_multiple_errors(self):
        """Multiple invalid fields produce multiple error messages."""
        schema = {
            'api_key': {'type': 'text', 'label': 'API Key', 'required': True},
            'secret': {'type': 'text', 'label': 'Secret Key', 'required': True},
            'region': {'type': 'text', 'label': 'Region', 'max_length': 3},
        }
        post = _make_querydict({
            'region': 'us-east-1',  # too long
        })

        creds, errors = validate_credential_fields(schema, post)

        # 2 required errors + 1 max_length error = 3
        assert len(errors) == 3

    def test_required_field_missing_skips_length_validation(self):
        """When a required field is empty, only the required error is reported (not length)."""
        schema = {
            'token': {'type': 'text', 'label': 'Token', 'required': True, 'min_length': 10},
        }
        post = _make_querydict({'token': ''})

        creds, errors = validate_credential_fields(schema, post)

        # Only the required error, not the min_length error
        assert len(errors) == 1
        assert 'required' in errors[0].lower()

    # --- max_length / min_length as string integers ---

    def test_max_length_as_string_integer_works(self):
        """max_length specified as a string integer (from JSON manifest) is parsed correctly."""
        schema = {
            'key': {'type': 'text', 'label': 'Key', 'max_length': '10'},
        }
        post = _make_querydict({'key': 'way_too_long_value'})

        creds, errors = validate_credential_fields(schema, post)

        assert len(errors) == 1
        assert 'at most' in errors[0].lower()

    def test_min_length_as_string_integer_works(self):
        """min_length specified as a string integer (from JSON manifest) is parsed correctly."""
        schema = {
            'key': {'type': 'text', 'label': 'Key', 'min_length': '10'},
        }
        post = _make_querydict({'key': 'short'})

        creds, errors = validate_credential_fields(schema, post)

        assert len(errors) == 1
        assert 'at least' in errors[0].lower()

    # --- Empty schema ---

    def test_empty_schema_returns_empty_credentials(self):
        """An empty schema produces no credentials and no errors."""
        creds, errors = validate_credential_fields({}, _make_querydict({}))

        assert creds == {}
        assert errors == []


# ============================================================
# validate_dual_environment_credentials
# ============================================================

class TestValidateDualEnvironmentCredentials:
    """Tests for dual-environment (test + live) credential validation."""

    @pytest.fixture
    def dual_schema(self):
        """A typical dual-environment credential schema for a payment provider."""
        return {
            'test_mode': {'type': 'boolean', 'label': 'Test Mode'},
            'test_api_key': {'type': 'text', 'label': 'Test API Key', 'required': True},
            'test_secret': {'type': 'text', 'label': 'Test Secret', 'required': True},
            'live_api_key': {'type': 'text', 'label': 'Live API Key', 'required': True},
            'live_secret': {'type': 'text', 'label': 'Live Secret', 'required': True},
            'webhook_url': {'type': 'text', 'label': 'Webhook URL', 'required': False},
        }

    def test_test_mode_on_validates_test_prefixed_fields(self, dual_schema):
        """In test mode, test_ prefixed required fields are validated."""
        post = _make_querydict({
            'test_mode': 'on',
            'test_api_key': 'pk_test_123',
            'test_secret': 'sk_test_456',
            # live fields omitted -- that is fine in test mode
        })

        creds, errors = validate_dual_environment_credentials(dual_schema, post)

        # No dual-env errors for test_ fields (they are provided)
        # basic_errors will have required errors for live_api_key and live_secret
        # but dual env only checks active prefix fields
        test_mode_errors = [e for e in errors if 'test mode' in e.lower()]
        assert test_mode_errors == []
        assert creds['test_mode'] is True
        assert creds['test_api_key'] == 'pk_test_123'
        assert creds['test_secret'] == 'sk_test_456'

    def test_test_mode_off_validates_live_prefixed_fields(self, dual_schema):
        """In live mode, live_ prefixed required fields are validated."""
        post = _make_querydict({
            # test_mode absent -> checkbox unchecked -> False
            'live_api_key': 'pk_live_abc',
            'live_secret': 'sk_live_def',
            # test fields omitted -- that is fine in live mode
        })

        creds, errors = validate_dual_environment_credentials(dual_schema, post)

        production_mode_errors = [e for e in errors if 'production mode' in e.lower()]
        assert production_mode_errors == []
        assert creds['test_mode'] is False
        assert creds['live_api_key'] == 'pk_live_abc'
        assert creds['live_secret'] == 'sk_live_def'

    def test_required_test_field_missing_in_test_mode_produces_error(self, dual_schema):
        """Missing required test_ fields in test mode produce mode-specific errors."""
        post = _make_querydict({
            'test_mode': 'on',
            # test_api_key and test_secret intentionally omitted
        })

        creds, errors = validate_dual_environment_credentials(dual_schema, post)

        test_mode_errors = [e for e in errors if 'test mode' in e.lower()]
        assert len(test_mode_errors) == 2
        field_labels = ' '.join(test_mode_errors)
        assert 'Test API Key' in field_labels
        assert 'Test Secret' in field_labels

    def test_required_live_field_missing_in_live_mode_produces_error(self, dual_schema):
        """Missing required live_ fields in live mode produce mode-specific errors."""
        post = _make_querydict({
            # test_mode absent -> False -> live mode
            # live_api_key and live_secret intentionally omitted
        })

        creds, errors = validate_dual_environment_credentials(dual_schema, post)

        production_errors = [e for e in errors if 'production mode' in e.lower()]
        assert len(production_errors) == 2
        field_labels = ' '.join(production_errors)
        assert 'Live API Key' in field_labels
        assert 'Live Secret' in field_labels

    def test_includes_basic_validation_errors(self, dual_schema):
        """Basic validation errors (from validate_credential_fields) are included."""
        post = _make_querydict({
            'test_mode': 'on',
            'test_api_key': 'pk_test_123',
            'test_secret': 'sk_test_456',
            # live fields missing -> basic required errors for them
        })

        creds, errors = validate_dual_environment_credentials(dual_schema, post)

        # Basic errors come from validate_credential_fields for missing required live_ fields
        basic_required_errors = [e for e in errors if 'is required.' in e and 'mode' not in e]
        assert len(basic_required_errors) == 2

    def test_non_prefixed_fields_not_checked_as_env_fields(self, dual_schema):
        """Fields without test_ or live_ prefix are not subject to environment checks."""
        post = _make_querydict({
            'test_mode': 'on',
            'test_api_key': 'pk_test_123',
            'test_secret': 'sk_test_456',
            # webhook_url is optional and not env-prefixed, should not produce env error
        })

        creds, errors = validate_dual_environment_credentials(dual_schema, post)

        # No webhook_url related errors
        webhook_errors = [e for e in errors if 'webhook' in e.lower()]
        assert webhook_errors == []

    def test_test_mode_skipped_in_env_field_check(self, dual_schema):
        """The test_mode field itself is not checked as a test_ prefixed credential."""
        post = _make_querydict({
            'test_mode': 'on',
            'test_api_key': 'valid',
            'test_secret': 'valid',
        })

        creds, errors = validate_dual_environment_credentials(dual_schema, post)

        # test_mode should not produce "test_mode is required when in test mode"
        test_mode_self_errors = [e for e in errors if 'Test Mode' in e and 'test mode' in e.lower()]
        assert test_mode_self_errors == []

    def test_all_fields_provided_no_errors(self, dual_schema):
        """When all required fields for all environments are provided, no errors."""
        post = _make_querydict({
            'test_mode': 'on',
            'test_api_key': 'pk_test_123',
            'test_secret': 'sk_test_456',
            'live_api_key': 'pk_live_abc',
            'live_secret': 'sk_live_def',
            'webhook_url': 'https://example.com/webhook',
        })

        creds, errors = validate_dual_environment_credentials(dual_schema, post)

        assert errors == []
        assert creds['test_mode'] is True
        assert creds['test_api_key'] == 'pk_test_123'
        assert creds['live_api_key'] == 'pk_live_abc'

    def test_empty_schema_returns_empty(self):
        """An empty schema produces no credentials and no errors."""
        post = _make_querydict({})

        creds, errors = validate_dual_environment_credentials({}, post)

        assert creds == {}
        assert errors == []

    def test_defaults_to_test_mode_when_test_mode_not_in_schema(self):
        """Without test_mode in the schema, defaults to test_mode=True."""
        schema = {
            'test_api_key': {'type': 'text', 'label': 'Test Key', 'required': True},
            'live_api_key': {'type': 'text', 'label': 'Live Key', 'required': True},
        }
        post = _make_querydict({
            'test_api_key': 'valid_key',
        })

        creds, errors = validate_dual_environment_credentials(schema, post)

        # test_mode defaults to True, so test_ fields are checked
        test_mode_errors = [e for e in errors if 'test mode' in e.lower()]
        assert test_mode_errors == []

    def test_max_length_error_propagated_from_basic_validation(self):
        """max_length errors from basic validation are included in the dual-env result."""
        schema = {
            'test_mode': {'type': 'boolean', 'label': 'Test Mode'},
            'test_api_key': {
                'type': 'text',
                'label': 'Test API Key',
                'required': True,
                'max_length': 5,
            },
        }
        post = _make_querydict({
            'test_mode': 'on',
            'test_api_key': 'way_too_long_key',
        })

        creds, errors = validate_dual_environment_credentials(schema, post)

        max_len_errors = [e for e in errors if 'at most' in e.lower()]
        assert len(max_len_errors) == 1

    def test_boolean_credentials_in_env_prefix_handled(self):
        """Boolean fields with test_/live_ prefix are handled correctly."""
        schema = {
            'test_mode': {'type': 'boolean', 'label': 'Test Mode'},
            'test_enable_3ds': {'type': 'boolean', 'label': 'Enable 3DS (Test)', 'required': True},
        }
        post = _make_querydict({
            'test_mode': 'on',
            'test_enable_3ds': 'on',
        })

        creds, errors = validate_dual_environment_credentials(schema, post)

        assert creds['test_enable_3ds'] is True
        # Boolean True is truthy, so env check passes
        env_errors = [e for e in errors if 'test mode' in e.lower()]
        assert env_errors == []

    def test_boolean_env_field_unchecked_in_active_mode_produces_error(self):
        """A required boolean field (unchecked=False) in active env produces mode error."""
        schema = {
            'test_mode': {'type': 'boolean', 'label': 'Test Mode'},
            'test_enable_feature': {'type': 'boolean', 'label': 'Enable Feature (Test)', 'required': True},
        }
        post = _make_querydict({
            'test_mode': 'on',
            # test_enable_feature absent -> False (falsy) -> mode error
        })

        creds, errors = validate_dual_environment_credentials(schema, post)

        assert creds['test_enable_feature'] is False
        env_errors = [e for e in errors if 'test mode' in e.lower()]
        assert len(env_errors) == 1
        assert 'Enable Feature (Test)' in env_errors[0]
