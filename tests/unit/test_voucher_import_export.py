"""
Tests for the voucher import/export service and admin wizard.

Covers:
 - CSV + XLSX parsing into normalised rows
 - Column auto-detection from header aliases
 - Row partitioning (valid / invalid with reason)
 - The three duplicate strategies (skip / overwrite / fail)
 - Batch settings apply uniformly to every imported row
 - `external_id` and `migration_job` linkage
 - Code-length validation (no silent truncation)
 - Export → re-import round-trip with `overwrite`
 - Export column schema matches the importer's mappable shape

The tests build their CSV/XLSX bytes in-memory so they don't depend on
fixture files on disk.
"""
from __future__ import annotations

import io
from datetime import datetime
from decimal import Decimal

import openpyxl
import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from djmoney.money import Money

from migration.models import MigrationJob
from tests.factories import UserFactory
from vouchers.models import VoucherCode
from vouchers.services.voucher_importer import (
    EXPORT_COLUMNS,
    MAPPABLE_FIELDS,
    auto_detect_mapping,
    build_preview,
    export_queryset,
    import_batch,
    parse_file,
    partition_rows,
)


pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _csv_upload(text: str, name: str = "vouchers.csv") -> SimpleUploadedFile:
    return SimpleUploadedFile(
        name,
        text.encode("utf-8"),
        content_type="text/csv",
    )


def _xlsx_upload(headers, rows, name="vouchers.xlsx") -> SimpleUploadedFile:
    buf = io.BytesIO()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(list(headers))
    for row in rows:
        ws.append(list(row))
    wb.save(buf)
    buf.seek(0)
    return SimpleUploadedFile(
        name,
        buf.read(),
        content_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )


def _batch_settings() -> dict:
    return {
        "discount_type": "percentage",
        "discount_value": Decimal("10.00"),
        "application_scope": "cart",
        "start_date": timezone.now(),
        "max_uses_per_customer": 1,
        "is_active": True,
    }


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def test_parse_csv_strips_whitespace_and_drops_blank_rows():
    csv_body = (
        "Voucher Code,Member ID,Notes\n"
        "BD-001 , 1001 , Alice\n"
        "\n"
        "  BD-002,1002,Bob\n"
    )
    parsed = parse_file(_csv_upload(csv_body))
    assert parsed.row_count == 2
    assert parsed.headers == ["Voucher Code", "Member ID", "Notes"]
    assert parsed.rows[0] == {"Voucher Code": "BD-001", "Member ID": "1001", "Notes": "Alice"}
    assert parsed.rows[1] == {"Voucher Code": "BD-002", "Member ID": "1002", "Notes": "Bob"}


def test_parse_xlsx_matches_csv_shape():
    upload = _xlsx_upload(
        ["Voucher Code", "Member ID", "Notes"],
        [["BD-001", 1001, "Alice"], ["BD-002", 1002, "Bob"]],
    )
    parsed = parse_file(upload)
    assert parsed.row_count == 2
    assert parsed.headers == ["Voucher Code", "Member ID", "Notes"]
    assert parsed.rows[0]["Voucher Code"] == "BD-001"
    assert parsed.rows[0]["Member ID"] == "1001"


def test_parse_rejects_unsupported_extension():
    with pytest.raises(ValidationError):
        parse_file(SimpleUploadedFile("notes.txt", b"hello", content_type="text/plain"))


# ---------------------------------------------------------------------------
# Mapping
# ---------------------------------------------------------------------------

def test_auto_detect_mapping_matches_aliases():
    detected = auto_detect_mapping(["Voucher Code", "Member Name", "Member ID", "Birthday"])
    assert detected["code"] == "Voucher Code"
    assert detected["external_id"] == "Member ID"
    # Member Name and Birthday don't match any required target.
    assert "name" not in detected
    assert "description" not in detected


# ---------------------------------------------------------------------------
# Validation / partition
# ---------------------------------------------------------------------------

def test_partition_rejects_blank_codes_and_overlength_codes_and_dupes_in_batch():
    rows = [
        {"Code": "BD-001"},
        {"Code": "   "},                       # blank → invalid
        {"Code": "X" * 60},                    # too long → invalid
        {"Code": "BD-001"},                    # duplicate within file → invalid
        {"Code": "BD-002"},
    ]
    valid, invalid = partition_rows(rows, mapping={"code": "Code"})
    assert [r["code"] for r in valid] == ["BD-001", "BD-002"]
    reasons = {row.code or "(empty)": row.reason for row in invalid}
    assert "(empty)" in reasons
    assert any("50 characters" in r for r in reasons.values())
    assert any("more than once" in r for r in reasons.values())


# ---------------------------------------------------------------------------
# Import: duplicate strategies
# ---------------------------------------------------------------------------

def _parsed_from_codes(codes):
    rows = [{"Code": c, "Member": f"M{i}"} for i, c in enumerate(codes)]
    csv_text = "Code,Member\n" + "\n".join(f"{r['Code']},{r['Member']}" for r in rows)
    return parse_file(_csv_upload(csv_text))


def test_import_skip_strategy_keeps_existing_and_creates_new(db):
    user = UserFactory()
    # Pre-existing voucher with one of our codes:
    VoucherCode.objects.create(
        code="BD-001", name="Existing", discount_type="percentage",
        discount_value=Decimal("50.00"), application_scope="cart", created_by=user,
    )

    parsed = _parsed_from_codes(["BD-001", "BD-002", "BD-003"])
    result = import_batch(
        parsed=parsed,
        mapping={"code": "Code"},
        batch_settings=_batch_settings(),
        dup_strategy="skip",
        user=user,
    )
    assert result.imported == 2
    assert result.updated == 0
    assert result.skipped_duplicate == 1
    # Pre-existing row's settings are untouched.
    pre = VoucherCode.objects.get(code="BD-001")
    assert pre.discount_value == Decimal("50.00")
    assert pre.name == "Existing"


def test_import_overwrite_strategy_updates_existing_settings_without_touching_identity(db):
    user = UserFactory()
    existing = VoucherCode.objects.create(
        code="BD-001", name="Existing", discount_type="fixed",
        discount_value=Decimal("5.00"), application_scope="cart", created_by=user,
        current_uses=3,
    )
    original_created_at = existing.created_at

    parsed = _parsed_from_codes(["BD-001", "BD-002"])
    result = import_batch(
        parsed=parsed,
        mapping={"code": "Code"},
        batch_settings=_batch_settings(),  # percentage 10%
        dup_strategy="overwrite",
        user=user,
    )
    assert result.imported == 1   # BD-002
    assert result.updated == 1    # BD-001

    updated = VoucherCode.objects.get(code="BD-001")
    assert updated.discount_type == "percentage"
    assert updated.discount_value == Decimal("10.00")
    # Identity / lifecycle preserved:
    assert updated.current_uses == 3
    assert updated.created_at == original_created_at


def test_import_fail_strategy_aborts_entire_batch_on_any_duplicate(db):
    user = UserFactory()
    VoucherCode.objects.create(
        code="BD-001", name="Existing", discount_type="percentage",
        discount_value=Decimal("50.00"), application_scope="cart", created_by=user,
    )
    parsed = _parsed_from_codes(["BD-001", "BD-002", "BD-003"])

    with pytest.raises(ValidationError):
        import_batch(
            parsed=parsed,
            mapping={"code": "Code"},
            batch_settings=_batch_settings(),
            dup_strategy="fail",
            user=user,
        )
    # None of the new codes got created.
    assert VoucherCode.objects.filter(code__in=["BD-002", "BD-003"]).count() == 0


# ---------------------------------------------------------------------------
# Linkage + uniform settings
# ---------------------------------------------------------------------------

def test_batch_settings_applied_uniformly_and_external_id_mapped(db):
    user = UserFactory()
    csv_text = (
        "Code,Member ID\n"
        "BD-100,1001\n"
        "BD-101,1002\n"
    )
    parsed = parse_file(_csv_upload(csv_text))
    settings = _batch_settings()
    settings["max_uses_per_customer"] = 2

    result = import_batch(
        parsed=parsed,
        mapping={"code": "Code", "external_id": "Member ID"},
        batch_settings=settings,
        dup_strategy="skip",
        user=user,
    )
    assert result.imported == 2

    created = VoucherCode.objects.filter(code__in=["BD-100", "BD-101"]).order_by("code")
    assert {v.discount_value for v in created} == {Decimal("10.00")}
    assert {v.max_uses_per_customer for v in created} == {2}
    assert {v.external_id for v in created} == {"1001", "1002"}
    # Every row points at the same migration job.
    job_ids = {v.migration_job_id for v in created}
    assert len(job_ids) == 1
    job = MigrationJob.objects.get(id=job_ids.pop())
    assert job.platform == "csv"
    assert job.coupons_imported == 2


# ---------------------------------------------------------------------------
# Preview surfaces duplicates and invalid rows
# ---------------------------------------------------------------------------

def test_build_preview_counts_duplicates_and_invalid_rows(db):
    user = UserFactory()
    VoucherCode.objects.create(
        code="BD-001", name="x", discount_type="percentage",
        discount_value=Decimal("10.00"), application_scope="cart", created_by=user,
    )
    csv_text = (
        "Code\n"
        "BD-001\n"
        "BD-002\n"
        "BD-002\n"        # duplicate in batch → invalid
        "\n"
        "" + ("X" * 60) + "\n"  # too long → invalid
    )
    parsed = parse_file(_csv_upload(csv_text))
    preview = build_preview(parsed, mapping={"code": "Code"})
    assert preview.valid_count == 2   # BD-001 + BD-002
    assert preview.duplicate_count == 1
    assert preview.new_count == 1
    assert any("more than once" in r.reason for r in preview.invalid_rows)
    assert any("50 characters" in r.reason for r in preview.invalid_rows)


# ---------------------------------------------------------------------------
# Export + roundtrip
# ---------------------------------------------------------------------------

def test_export_columns_cover_every_mappable_import_field():
    # If an importer-mappable field isn't represented on export, the
    # round-trip would silently lose data. Guard against drift.
    for target in MAPPABLE_FIELDS:
        assert target in EXPORT_COLUMNS


def test_export_xlsx_round_trips_through_overwrite(db):
    user = UserFactory()
    # Seed two vouchers
    VoucherCode.objects.create(
        code="RT-001", name="One", discount_type="percentage",
        discount_value=Decimal("15.00"), application_scope="cart", created_by=user,
    )
    VoucherCode.objects.create(
        code="RT-002", name="Two", discount_type="percentage",
        discount_value=Decimal("25.00"), application_scope="cart", created_by=user,
    )

    queryset = VoucherCode.objects.filter(code__in=["RT-001", "RT-002"]).order_by("code")
    response = export_queryset(queryset, fmt="xlsx", filename="t")
    assert response["Content-Type"].startswith(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Re-parse the exported file and feed it back through the importer with
    # `overwrite` so the existing rows pick up the batch settings.
    upload = SimpleUploadedFile("export.xlsx", response.content)
    parsed = parse_file(upload)
    assert "code" in parsed.headers
    assert {row["code"] for row in parsed.rows} == {"RT-001", "RT-002"}

    new_settings = _batch_settings()
    new_settings["discount_value"] = Decimal("40.00")
    result = import_batch(
        parsed=parsed,
        mapping={"code": "code"},
        batch_settings=new_settings,
        dup_strategy="overwrite",
        user=user,
    )
    assert result.imported == 0
    assert result.updated == 2
    refreshed = VoucherCode.objects.filter(code__in=["RT-001", "RT-002"]).order_by("code")
    assert {v.discount_value for v in refreshed} == {Decimal("40.00")}
