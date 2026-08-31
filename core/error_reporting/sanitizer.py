"""
Data sanitizer for error reports.

Masks all PII and sensitive data before error reports leave the installation.
This is the most security-critical component of the error reporting system.
"""

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


class DataSanitizer:
    """Masks all PII and sensitive data before error reports leave the installation."""

    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    IPV6_PATTERN = re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}\b")
    PHONE_PATTERN = re.compile(
        r"(?<!\d)(?:\+?\d{1,3}[\s\-.]?)?\(?\d{2,4}\)?[\s\-.]?\d{3,4}[\s\-.]?\d{3,4}(?!\d)"
    )

    # Sensitive key patterns for dict/JSON scrubbing
    SENSITIVE_KEYS = re.compile(
        r"(?i)(password|passwd|secret|token|api[_\-]?key|auth|credential|"
        r"private[_\-]?key|access[_\-]?key|cookie|session|jwt|bearer|"
        r"database[_\-]?url|db[_\-]?pass|dsn|stripe|paypal|airwallex|"
        r"credit[_\-]?card|card[_\-]?number|cvv|ssn|social[_\-]?security|"
        r"phone|address|full[_\-]?name|first[_\-]?name|last[_\-]?name)"
    )

    # Absolute paths that reveal server structure
    ABSOLUTE_PATH_PATTERN = re.compile(
        r"(/home/[^/\s:]+/|/opt/[^/\s:]+/|/var/[^/\s:]+/|/mnt/[^/\s:]+/|"
        r"/srv/[^/\s:]+/|/root/)"
    )

    # Key=value patterns in tracebacks/logs. The value alternatives are
    # quote-aware so a quoted value containing whitespace is matched whole,
    # with a trailing fallback that still masks a malformed (unterminated)
    # quoted value so a secret can never leak through an unbalanced quote.
    KEY_VALUE_PATTERN = re.compile(
        r"(?i)(password|passwd|secret|token|api_key|auth_key|access_key|"
        r"db_pass|database_url|dsn)\s*[=:]\s*"
        r"(?:\"[^\"]*\"|'[^']*'|[\"'][^\s]*|[^\s'\"]+)"
    )

    @classmethod
    def sanitize_traceback(cls, tb_string):
        """Sanitize a Python traceback string."""
        return cls._sanitize_value(tb_string)

    @classmethod
    def sanitize_dict(cls, data):
        """Deep-sanitize a dictionary, masking sensitive keys and values."""
        if not isinstance(data, dict):
            return data
        sanitized = {}
        for key, value in data.items():
            if cls.SENSITIVE_KEYS.search(str(key)):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = cls.sanitize_dict(value)
            elif isinstance(value, (list, tuple)):
                sanitized[key] = cls._sanitize_sequence(value)
            elif isinstance(value, str):
                sanitized[key] = cls._sanitize_value(value)
            else:
                sanitized[key] = value
        return sanitized

    @classmethod
    def sanitize_headers(cls, headers):
        """Sanitize HTTP headers, removing cookies, auth, etc."""
        safe_headers = {}
        skip_keys = {
            "cookie",
            "authorization",
            "x-csrftoken",
            "x-api-key",
            "set-cookie",
            "proxy-authorization",
        }
        url_keys = {"referer", "origin"}
        for key, value in headers.items():
            lower_key = cls._normalize_header_key(key)
            if lower_key in skip_keys:
                safe_headers[key] = "[REDACTED]"
            elif lower_key in url_keys:
                safe_headers[key] = cls.sanitize_url(str(value))
            else:
                safe_headers[key] = cls._mask_emails(str(value))
        return safe_headers

    @classmethod
    def sanitize_url(cls, url):
        """Strip query parameters that may contain tokens/PII."""
        try:
            parsed = urlparse(url)
            if not parsed.query:
                return cls._mask_emails(url)
            safe_params = {}
            for key, values in parse_qs(parsed.query, keep_blank_values=True).items():
                if cls.SENSITIVE_KEYS.search(key):
                    safe_params[key] = ["[REDACTED]"]
                else:
                    safe_params[key] = [cls._sanitize_value(v) for v in values]
            clean_url = urlunparse(parsed._replace(query=urlencode(safe_params, doseq=True)))
            return cls._mask_emails(clean_url)
        except Exception:
            return "[URL_PARSE_ERROR]"

    @classmethod
    def _sanitize_sequence(cls, items):
        """Deep-sanitize a list/tuple, recursing and preserving the type.

        Named tuples are reconstructed positionally so their type survives;
        plain lists and tuples are rebuilt from the sanitized iterable.
        """
        sanitized = [cls._sanitize_item(item) for item in items]
        if isinstance(items, tuple) and hasattr(items, "_fields"):
            return type(items)(*sanitized)
        return type(items)(sanitized)

    @classmethod
    def _sanitize_item(cls, item):
        """Sanitize a single container item, dispatching on its type."""
        if isinstance(item, dict):
            return cls.sanitize_dict(item)
        if isinstance(item, (list, tuple)):
            return cls._sanitize_sequence(item)
        return cls._sanitize_value(item)

    @classmethod
    def _normalize_header_key(cls, key):
        """Normalize a header name so Django request.META keys match plain ones.

        ``HTTP_X_API_KEY`` becomes ``x-api-key`` so it compares equal to the
        canonical lowercase, hyphenated header names used in the skip lists.
        """
        lower_key = str(key).lower()
        if lower_key.startswith("http_"):
            lower_key = lower_key[len("http_") :]
        return lower_key.replace("_", "-")

    @classmethod
    def _sanitize_value(cls, value):
        """Apply all masking to a single string value."""
        if not isinstance(value, str):
            return value
        result = cls._mask_key_values(value)
        result = cls._mask_emails(result)
        result = cls._mask_ips(result)
        result = cls._mask_phones(result)
        result = cls._normalize_paths(result)
        return result

    @classmethod
    def _mask_emails(cls, text):
        return cls.EMAIL_PATTERN.sub("[EMAIL]", text)

    @classmethod
    def _mask_ips(cls, text):
        text = cls.IP_PATTERN.sub("[IP]", text)
        text = cls.IPV6_PATTERN.sub("[IPV6]", text)
        return text

    @classmethod
    def _mask_phones(cls, text):
        return cls.PHONE_PATTERN.sub("[PHONE]", text)

    @classmethod
    def _normalize_paths(cls, text):
        return cls.ABSOLUTE_PATH_PATTERN.sub("[PATH]/", text)

    @classmethod
    def _mask_key_values(cls, text):
        """Mask values in key=value or key: value patterns for sensitive keys."""
        return cls.KEY_VALUE_PATTERN.sub(r"\1=[REDACTED]", text)
