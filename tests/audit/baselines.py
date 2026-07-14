"""
Baseline Comparison for Site Health Audits

Save audit results as baselines and compare future runs against them
to detect regressions.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from tests.audit.engine import AuditReport

BASELINE_DIR = Path(__file__).parent / "baselines"


@dataclass
class Regression:
    """A single regression detected between baseline and current run."""

    url: str
    label: str
    field: str
    baseline_value: object
    current_value: object

    def __str__(self):
        return (
            f"{self.label} ({self.url}): "
            f"{self.field} regressed from {self.baseline_value} to {self.current_value}"
        )


def save_baseline(report: AuditReport, name: str | None = None):
    """Save current results as a named baseline."""
    name = name or report.category
    baseline = {}
    for r in report.results:
        baseline[r.url] = {
            "label": r.label,
            "status_code": r.status_code,
            "load_time_ms": r.load_time_ms,
            "console_error_count": len(r.console_errors),
            "console_warning_count": len(r.console_warnings),
            "failed_request_count": len(r.failed_requests),
        }

    BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    path = BASELINE_DIR / f"{name}.json"
    with open(path, "w") as f:
        json.dump(baseline, f, indent=2)
    print(f"  Baseline saved: {path} ({len(baseline)} pages)")


def load_baseline(name: str) -> dict | None:
    """Load a saved baseline. Returns None if not found."""
    path = BASELINE_DIR / f"{name}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def compare_to_baseline(report: AuditReport, baseline: dict) -> list[Regression]:
    """
    Compare current results to a baseline. Returns list of regressions.

    A regression is:
    - Status code was 200, now >= 400
    - New console errors appeared (count increased)
    - New failed sub-resource requests appeared
    - Page became significantly slower (>2x AND >3000ms absolute)
    """
    regressions: list[Regression] = []

    for r in report.results:
        b = baseline.get(r.url)
        if not b:
            continue  # New page — not a regression

        label = r.label

        # Status code regression
        if b["status_code"] == 200 and r.status_code and r.status_code >= 400:
            regressions.append(
                Regression(
                    r.url,
                    label,
                    "status_code",
                    b["status_code"],
                    r.status_code,
                )
            )

        # New console errors
        if len(r.console_errors) > b["console_error_count"]:
            regressions.append(
                Regression(
                    r.url,
                    label,
                    "console_errors",
                    b["console_error_count"],
                    len(r.console_errors),
                )
            )

        # New failed requests
        if len(r.failed_requests) > b["failed_request_count"]:
            regressions.append(
                Regression(
                    r.url,
                    label,
                    "failed_requests",
                    b["failed_request_count"],
                    len(r.failed_requests),
                )
            )

        # Significant slowdown (>2x baseline AND above absolute threshold)
        if (
            b["load_time_ms"] > 0
            and r.load_time_ms > b["load_time_ms"] * 2
            and r.load_time_ms > 3000
        ):
            regressions.append(
                Regression(
                    r.url,
                    label,
                    "load_time_ms",
                    b["load_time_ms"],
                    r.load_time_ms,
                )
            )

    return regressions


def print_regressions(regressions: list[Regression]) -> int:
    """Print regression report. Returns exit code (0=none, 1=regressions found)."""
    if not regressions:
        print("\n\033[92m✓ No regressions detected.\033[0m\n")
        return 0

    print(f"\n\033[91m{'─' * 60}")
    print(f"REGRESSIONS DETECTED ({len(regressions)})")
    print(f"{'─' * 60}\033[0m")
    for reg in regressions:
        print(f"  {reg}")

    print(f"\n\033[91m✗ {len(regressions)} regression(s) found.\033[0m\n")
    return 1
