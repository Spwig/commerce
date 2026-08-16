"""
File-upload hardening for public form file fields.

The upload endpoint is public and unauthenticated, and uploaded files are served
from the merchant's own origin — so an attacker who can store an active-content
file (HTML/SVG/JS/PHP) gets stored-XSS or code execution on the merchant domain.
This module enforces a deny-by-default policy: a hard denylist of dangerous
types regardless of merchant config, a safe default allowlist when a field
leaves ``allowed_types`` empty, magic-byte content sniffing (not just the
extension), and a sanitised, non-traversable stored filename.
"""

from __future__ import annotations

import logging
import uuid

from django.utils.text import slugify

logger = logging.getLogger(__name__)

# Never accepted, whatever the merchant configures — active/executable content
# that can run in a browser or on the server when served from MEDIA.
DANGEROUS_EXTENSIONS = frozenset(
    {
        "html",
        "htm",
        "xhtml",
        "shtml",
        "svg",
        "xml",
        "xsl",
        "mhtml",
        "js",
        "mjs",
        "jsx",
        "php",
        "php3",
        "php4",
        "php5",
        "phtml",
        "phar",
        "pht",
        "asp",
        "aspx",
        "jsp",
        "jspx",
        "cgi",
        "pl",
        "py",
        "rb",
        "sh",
        "bash",
        "exe",
        "dll",
        "bat",
        "cmd",
        "com",
        "msi",
        "jar",
        "war",
        "vbs",
        "ps1",
        "htaccess",
        "swf",
    }
)

# Used when a file field's ``allowed_types`` is empty (deny-by-default → allow
# only common inert document/image/media types).
SAFE_DEFAULT_EXTENSIONS = frozenset(
    {
        "pdf",
        "txt",
        "csv",
        "rtf",
        "odt",
        "ods",
        "odp",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "jpg",
        "jpeg",
        "png",
        "gif",
        "webp",
        "avif",
        "bmp",
        "tiff",
        "heic",
        "mp3",
        "wav",
        "ogg",
        "mp4",
        "webm",
        "mov",
        "zip",
    }
)

# Extensions whose sniffed MIME we can meaningfully cross-check.
_MIME_PREFIX_BY_EXT = {
    "jpg": "image/",
    "jpeg": "image/",
    "png": "image/",
    "gif": "image/",
    "webp": "image/",
    "bmp": "image/",
    "tiff": "image/",
    "avif": "image/",
    "pdf": "application/pdf",
    "mp4": "video/",
    "webm": "video/",
    "mov": "video/",
    "mp3": "audio/",
    "wav": "audio/",
    "ogg": "audio/",
}


class UploadRejected(Exception):
    """Raised with a user-safe message when an upload is not allowed."""


def _extension(name: str) -> str:
    base = (name or "").rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    return base.rsplit(".", 1)[-1].lower() if "." in base else ""


def validate_upload(file, allowed_types: list[str] | None) -> str:
    """Validate an uploaded file. Returns the safe extension, or raises
    ``UploadRejected``. ``allowed_types`` is the field's merchant config."""
    ext = _extension(file.name)
    if not ext:
        raise UploadRejected("Files must have a valid extension.")

    # Hard denylist always wins — even if a merchant whitelisted it.
    if ext in DANGEROUS_EXTENSIONS:
        raise UploadRejected(f"File type .{ext} not allowed.")

    # Merchant allowlist, or the safe default when they configured none.
    allow = {a.lower().lstrip(".") for a in (allowed_types or [])} or SAFE_DEFAULT_EXTENSIONS
    if ext not in allow:
        raise UploadRejected(f"File type .{ext} not allowed.")

    # Content sniff (magic bytes) — reject an extension/content mismatch, e.g.
    # HTML/script bytes disguised as .png.
    try:
        import magic  # python-magic

        head = file.read(2048)
        file.seek(0)
        sniffed = magic.from_buffer(head, mime=True) or ""
        if "html" in sniffed or sniffed in ("application/x-dosexec", "text/x-shellscript"):
            raise UploadRejected("File content is not permitted.")
        expected = _MIME_PREFIX_BY_EXT.get(ext)
        if expected and not sniffed.startswith(expected):
            raise UploadRejected("File content does not match its extension.")
    except UploadRejected:
        raise
    except Exception:
        # Fail closed for extensions whose content we cross-check (image/pdf/
        # media): if libmagic is unavailable we can't prove the bytes match, so
        # rejecting is safer than letting disguised active content through. Inert
        # types with no MIME cross-check (txt/docx/…) are allowed through.
        logger.warning("form_builder: content sniff unavailable/failed", exc_info=True)
        if ext in _MIME_PREFIX_BY_EXT:
            raise UploadRejected("File content could not be verified.") from None

    return ext


def safe_stored_name(form_slug: str, original_name: str, ext: str) -> str:
    """Build a sanitised, non-traversable storage path: no attacker-controlled
    path segments, slugified base, validated extension."""
    base = (original_name or "").rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    stem = base.rsplit(".", 1)[0] if "." in base else base
    safe_stem = slugify(stem)[:60] or "upload"
    return f"{slugify(form_slug)}/{uuid.uuid4().hex[:8]}_{safe_stem}.{ext}"
