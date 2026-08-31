"""Bulk-import subscribers from an uploaded CSV/XLSX (P2 audiences).

Mirrors the structure of ``vouchers/services/voucher_importer`` — the repo's
proven upload → map → partition → dedup → ``import_batch`` pipeline — keyed on a
subscriber's ``(site, email)`` uniqueness instead of a voucher code.

Consent: an admin CSV import is a merchant asserting they already have opt-in for
these contacts (the affirmation checkbox on the upload form). Imported rows are
recorded as consented with ``source="import"`` and full consent evidence, so they
behave exactly like any other opted-in subscriber at send time.
"""

import csv
import io
import logging
from dataclasses import dataclass, field
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("email_marketing")

MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB
MAX_ROWS = 5_000
ALLOWED_EXTENSIONS = (".csv", ".xlsx")

#: Import targets and the header spellings that auto-map to them. Only ``email``
#: is required; the rest are optional personalisation fields.
MAPPABLE_FIELDS: dict[str, dict[str, Any]] = {
    "email": {
        "label": _("Email"),
        "required": True,
        "max_length": 254,
        "aliases": ("email", "email_address", "e-mail", "mail", "emailaddress"),
    },
    "first_name": {
        "label": _("First name"),
        "required": False,
        "max_length": 100,
        "aliases": ("first_name", "firstname", "first", "given_name", "fname"),
    },
    "last_name": {
        "label": _("Last name"),
        "required": False,
        "max_length": 100,
        "aliases": ("last_name", "lastname", "last", "surname", "family_name", "lname"),
    },
    "language": {
        "label": _("Language"),
        "required": False,
        "max_length": 10,
        "aliases": ("language", "lang", "locale", "language_code"),
    },
}

DUPLICATE_STRATEGIES = ("skip", "update")


@dataclass
class ParsedFile:
    headers: list[str]
    rows: list[dict[str, str]]
    row_count: int


@dataclass
class InvalidRow:
    line: int
    email: str
    reason: str


@dataclass
class ImportPreview:
    parsed: ParsedFile
    mapping: dict[str, str]
    valid_count: int
    invalid_rows: list[InvalidRow]
    existing_emails: set[str]
    sample_duplicates: list[str] = field(default_factory=list)

    @property
    def new_count(self) -> int:
        return self.valid_count - len(self.existing_emails)


@dataclass
class ImportResult:
    created: int
    updated: int
    skipped: int
    invalid: int


# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------


def _normalise_header(h: str) -> str:
    return "".join(ch for ch in h.strip().lower() if ch.isalnum() or ch in ("_", "-")).replace(
        "-", "_"
    )


def normalise_email(value: str) -> str:
    return (value or "").strip().lower()


def parse_file(uploaded_file) -> ParsedFile:
    """Read a CSV/XLSX upload into a normalised (headers, rows) shape."""
    name = (getattr(uploaded_file, "name", "") or "").lower()
    if not name.endswith(ALLOWED_EXTENSIONS):
        raise ValidationError(_("Unsupported file type. Upload a .csv or .xlsx file."))
    size = getattr(uploaded_file, "size", None)
    if size is not None and size > MAX_UPLOAD_BYTES:
        raise ValidationError(_("File is too large. Maximum upload size is 5 MB."))

    if name.endswith(".csv"):
        headers, rows = _parse_csv(uploaded_file)
    else:
        headers, rows = _parse_xlsx(uploaded_file)

    if len(rows) > MAX_ROWS:
        raise ValidationError(
            _("Too many rows (%(count)d). Maximum is %(limit)d per import.")
            % {"count": len(rows), "limit": MAX_ROWS}
        )
    return ParsedFile(headers=headers, rows=rows, row_count=len(rows))


def _parse_csv(uploaded_file) -> tuple[list[str], list[dict[str, str]]]:
    raw = uploaded_file.read()
    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)
    text = raw.decode("utf-8-sig", errors="replace") if isinstance(raw, bytes) else raw
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.reader(io.StringIO(text), dialect=dialect)
    rows_iter = iter(reader)
    try:
        headers = [str(h).strip() for h in next(rows_iter)]
    except StopIteration:
        return [], []
    out: list[dict[str, str]] = []
    for row in rows_iter:
        cells = [str(v).strip() if v is not None else "" for v in row]
        if not any(cells):
            continue
        cells = (cells + [""] * len(headers))[: len(headers)]
        out.append(dict(zip(headers, cells, strict=True)))
        _guard_row_count(out)
    return headers, out


def _guard_row_count(out) -> None:
    """Stop reading the moment we pass the cap — before a huge file materialises.

    An .xlsx compresses extremely well, so a small upload can expand to millions
    of rows; enforcing the cap only after building the full list would OOM first.
    """
    if len(out) > MAX_ROWS:
        raise ValidationError(
            _("Too many rows. Maximum is %(limit)d per import.") % {"limit": MAX_ROWS}
        )


def _parse_xlsx(uploaded_file) -> tuple[list[str], list[dict[str, str]]]:
    import openpyxl

    try:
        wb = openpyxl.load_workbook(uploaded_file, read_only=True, data_only=True)
    except Exception as exc:  # noqa: BLE001 — any parse failure is a bad-file, not a 500
        raise ValidationError(_("This file isn't a readable Excel workbook.")) from exc
    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)
    ws = wb.active
    if ws is None:
        return [], []
    rows_iter = ws.iter_rows(values_only=True)
    try:
        header_row = next(rows_iter)
    except StopIteration:
        return [], []
    headers = [str(h).strip() if h is not None else "" for h in header_row]
    out: list[dict[str, str]] = []
    for row in rows_iter:
        cells = ["" if v is None else str(v).strip() for v in row]
        if not any(cells):
            continue
        cells = (cells + [""] * len(headers))[: len(headers)]
        out.append(dict(zip(headers, cells, strict=True)))
        _guard_row_count(out)
    return headers, out


# ---------------------------------------------------------------------------
# Map + partition
# ---------------------------------------------------------------------------


def auto_detect_mapping(headers) -> dict[str, str]:
    suggestion: dict[str, str] = {}
    normalised = [(_normalise_header(h), h) for h in headers]
    for target, spec in MAPPABLE_FIELDS.items():
        aliases = set(spec["aliases"])
        for norm, original in normalised:
            if norm in aliases:
                suggestion[target] = original
                break
    return suggestion


def validate_mapping(mapping: dict[str, str], headers) -> dict[str, str]:
    """Keep only known targets that point at a real header; require ``email``."""
    headers_set = set(headers)
    cleaned = {
        target: source
        for target, source in mapping.items()
        if target in MAPPABLE_FIELDS and source in headers_set
    }
    if "email" not in cleaned:
        raise ValidationError(_("You must map a column to Email."))
    return cleaned


def _row_targets(row: dict[str, str], mapping: dict[str, str]) -> dict[str, str]:
    # Cap each value to its field's max length here (not just at DB write) so the
    # session stash between preview and confirm can't hold oversized cells.
    out = {}
    for target, source in mapping.items():
        value = (row.get(source, "") or "").strip()
        max_len = MAPPABLE_FIELDS[target]["max_length"]
        out[target] = value[:max_len] if max_len else value
    return out


def partition_rows(rows, mapping) -> tuple[list[dict[str, str]], list[InvalidRow]]:
    """Split rows into importable ones and rejected ones (with a reason)."""
    valid: list[dict[str, str]] = []
    invalid: list[InvalidRow] = []
    seen: set[str] = set()

    for idx, row in enumerate(rows, start=2):  # row 1 is the header
        targets = _row_targets(row, mapping)
        email = normalise_email(targets.get("email", ""))
        if not email:
            invalid.append(InvalidRow(idx, "", str(_("Email is empty"))))
            continue
        try:
            validate_email(email)
        except ValidationError:
            invalid.append(InvalidRow(idx, email, str(_("Not a valid email address"))))
            continue
        if len(email) > MAPPABLE_FIELDS["email"]["max_length"]:
            invalid.append(InvalidRow(idx, email, str(_("Email is too long"))))
            continue
        if email in seen:
            invalid.append(InvalidRow(idx, email, str(_("Duplicate of an earlier row"))))
            continue
        seen.add(email)
        targets["email"] = email  # store normalised
        valid.append(targets)

    return valid, invalid


def find_existing(site, emails) -> set[str]:
    from email_marketing.models import Subscriber

    emails = list(emails)
    if not emails:
        return set()
    # all_objects: the (site, email) unique constraint also covers soft-deleted
    # rows, so a since-deleted contact still counts as "already on the list" —
    # otherwise creating it would raise IntegrityError and abort the whole import.
    return set(
        Subscriber.all_objects.filter(site=site, email__in=emails).values_list("email", flat=True)
    )


def build_preview(site, parsed: ParsedFile, mapping: dict[str, str]) -> ImportPreview:
    valid, invalid = partition_rows(parsed.rows, mapping)
    existing = find_existing(site, (r["email"] for r in valid))
    return ImportPreview(
        parsed=parsed,
        mapping=mapping,
        valid_count=len(valid),
        invalid_rows=invalid,
        existing_emails=existing,
        sample_duplicates=sorted(existing)[:10],
    )


# ---------------------------------------------------------------------------
# Import
# ---------------------------------------------------------------------------


@transaction.atomic
def import_batch(
    site,
    rows: list[dict[str, str]],
    *,
    duplicate_strategy: str = "skip",
    tag=None,
    now=None,
) -> ImportResult:
    """Create (and optionally update) subscribers from validated rows.

    Every created row is recorded as consented (``source="import"``) — the
    merchant asserted opt-in on the upload form. Duplicates are skipped, or their
    name/language updated when ``duplicate_strategy="update"``. An optional
    ``tag`` is applied to every imported/updated subscriber.
    """
    from email_marketing.models import Subscriber

    now = now or timezone.now()
    # all_objects so soft-deleted rows are seen — the unique (site,email) covers
    # them, so a create() would otherwise IntegrityError and roll back the batch.
    existing_by_email = {
        s.email: s
        for s in Subscriber.all_objects.filter(
            site=site, email__in=[r["email"] for r in rows]
        ).only("id", "email", "is_deleted")
    }

    created = updated = skipped = 0
    for row in rows:
        email = row["email"]
        existing = existing_by_email.get(email)
        if existing:
            # Never resurrect a soft-deleted contact via import — leave it deleted.
            if existing.is_deleted:
                skipped += 1
                continue
            # The chosen tag applies to existing contacts regardless of strategy —
            # tagging an import is additive and is usually the whole point.
            if tag:
                existing.tags.add(tag)
            if duplicate_strategy == "update":
                changed = []
                for src, dst in (
                    ("first_name", "first_name"),
                    ("last_name", "last_name"),
                    ("language", "language_code"),
                ):
                    val = row.get(src, "")
                    if val and getattr(existing, dst) != val:
                        setattr(existing, dst, val[: Subscriber._meta.get_field(dst).max_length])
                        changed.append(dst)
                if changed:
                    existing.save(update_fields=[*changed, "updated_at"])
                updated += 1
            else:
                skipped += 1
            continue

        subscriber = Subscriber.objects.create(
            site=site,
            email=email,
            first_name=row.get("first_name", "")[:100],
            last_name=row.get("last_name", "")[:100],
            language_code=row.get("language", "")[:10],
            source="import",
            status=Subscriber.STATUS_ACTIVE,
            marketing_opt_in=True,
            marketing_verified=True,
            consent_source="csv_import",
            consent_timestamp=now,
        )
        if tag:
            subscriber.tags.add(tag)
        created += 1

    logger.info(
        "CSV import into site %s: %d created, %d updated, %d skipped",
        getattr(site, "pk", site),
        created,
        updated,
        skipped,
    )
    return ImportResult(created=created, updated=updated, skipped=skipped, invalid=0)
