"""
Site Health Audit Engine

Reusable core for auditing web pages via Playwright (browser) or plain HTTP.
Collects HTTP status, console errors/warnings, failed sub-resource requests,
Django error pages, and load times.
"""
import json
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

import requests as http_requests
from playwright.sync_api import Page, ConsoleMessage

# ── Patterns to ignore in console output ─────────────────────
IGNORED_PATTERNS = [
    "The Cross-Origin-Opener-Policy header has been ignored",
    "Download the React DevTools",
]


@dataclass
class PageResult:
    """Result of visiting a single page."""
    url: str
    label: str
    category: str = "unknown"  # "admin", "storefront", "api"
    status_code: int | None = None
    load_time_ms: float = 0
    console_errors: list = field(default_factory=list)
    console_warnings: list = field(default_factory=list)
    failed_requests: list = field(default_factory=list)
    django_error: str | None = None
    exception: str | None = None

    @property
    def has_issues(self) -> bool:
        return bool(
            self.console_errors
            or self.failed_requests
            or self.django_error
            or self.exception
            or (self.status_code and self.status_code >= 400)
        )


@dataclass
class AuditReport:
    """Collection of page results for a single audit run."""
    category: str
    results: list[PageResult] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def total_pages(self) -> int:
        return len(self.results)

    @property
    def http_errors(self) -> list[PageResult]:
        return [r for r in self.results if r.status_code and r.status_code >= 400]

    @property
    def error_pages(self) -> list[PageResult]:
        return [r for r in self.results if r.console_errors]

    @property
    def warning_pages(self) -> list[PageResult]:
        return [r for r in self.results if r.console_warnings]

    @property
    def failed_request_pages(self) -> list[PageResult]:
        return [r for r in self.results if r.failed_requests]

    @property
    def exception_pages(self) -> list[PageResult]:
        return [r for r in self.results if r.exception]

    def slow_pages(self, threshold_ms: int = 3000) -> list[PageResult]:
        return [r for r in self.results if r.load_time_ms > threshold_ms]

    @property
    def has_issues(self) -> bool:
        return any(r.has_issues for r in self.results)


# ── Browser-based page visiting ──────────────────────────────

def should_ignore(msg_text: str) -> bool:
    """Return True if the console message matches an ignored pattern."""
    return any(pattern in msg_text for pattern in IGNORED_PATTERNS)


def visit_page_browser(
    page: Page,
    url: str,
    label: str,
    base_url: str,
    category: str = "unknown",
    timeout: int = 30000,
) -> PageResult:
    """
    Visit a page with Playwright, collecting console errors, failed
    sub-resource requests, and load timing.
    """
    result = PageResult(url=url, label=label, category=category)
    console_messages: list[ConsoleMessage] = []
    failed_reqs: list[dict] = []

    handler = lambda msg: console_messages.append(msg)
    page.on("console", handler)

    full_url = url if url.startswith("http") else base_url + url

    def on_response(response):
        if response.status >= 400 and response.url != full_url:
            failed_reqs.append({"url": response.url, "status": response.status})

    page.on("response", on_response)

    try:
        start = time.monotonic()
        response = page.goto(full_url, wait_until="networkidle", timeout=timeout)
        result.load_time_ms = round((time.monotonic() - start) * 1000)
        result.status_code = response.status if response else None

        page.wait_for_timeout(500)

        if result.status_code and result.status_code >= 400:
            error_el = page.query_selector(
                "#summary h1, #info h2, .errornote, title"
            )
            if error_el:
                result.django_error = error_el.text_content().strip()[:300]

    except Exception as exc:
        result.exception = str(exc)[:300]

    page.remove_listener("console", handler)
    page.remove_listener("response", on_response)

    result.failed_requests = [
        f"[{r['status']}] {r['url']}" for r in failed_reqs
    ]

    for msg in console_messages:
        text = msg.text
        if should_ignore(text):
            continue
        if msg.type == "error":
            result.console_errors.append(text[:500])
        elif msg.type == "warning":
            result.console_warnings.append(text[:500])

    return result


# ── HTTP-only page visiting (for APIs) ───────────────────────

def visit_url_http(
    url: str,
    base_url: str = "http://localhost:8000",
    label: str = "",
    category: str = "api",
    session: http_requests.Session | None = None,
    expected_statuses: list[int] | None = None,
) -> PageResult:
    """
    Visit a URL with plain HTTP (no browser). Suitable for API endpoints.
    """
    result = PageResult(url=url, label=label or url, category=category)
    full_url = url if url.startswith("http") else base_url + url

    try:
        sess = session or http_requests.Session()
        start = time.monotonic()
        resp = sess.get(full_url, timeout=15, allow_redirects=True)
        result.load_time_ms = round((time.monotonic() - start) * 1000)
        result.status_code = resp.status_code

        if expected_statuses and resp.status_code not in expected_statuses:
            result.console_errors.append(
                f"Expected status {expected_statuses}, got {resp.status_code}"
            )
        elif resp.status_code >= 500:
            result.console_errors.append(f"Server error: {resp.status_code}")
            try:
                result.django_error = resp.text[:300]
            except Exception:
                pass

    except http_requests.ConnectionError as exc:
        result.exception = f"Connection refused: {exc}"
    except http_requests.Timeout:
        result.exception = "Request timed out (15s)"
    except Exception as exc:
        result.exception = str(exc)[:300]

    return result


# ── Terminal output ──────────────────────────────────────────

def print_result_line(i: int, total: int, result: PageResult):
    """Print a single-line progress indicator."""
    status = result.status_code or "ERR"
    issues = []
    if result.console_errors:
        issues.append(f"\033[91m{len(result.console_errors)} error(s)\033[0m")
    if result.failed_requests:
        issues.append(f"\033[91m{len(result.failed_requests)} 404(s)\033[0m")
    if result.console_warnings:
        issues.append(f"\033[93m{len(result.console_warnings)} warning(s)\033[0m")
    if result.django_error:
        issues.append(f"\033[91mDjango: {result.django_error[:60]}\033[0m")
    if result.exception:
        issues.append(f"\033[91mException: {result.exception[:60]}\033[0m")

    status_color = "\033[92m" if result.status_code == 200 else "\033[91m"
    issue_str = f"  [{', '.join(issues)}]" if issues else ""
    time_str = f"{result.load_time_ms}ms"

    print(
        f"  [{i}/{total}] {status_color}{status}\033[0m  "
        f"{time_str:>7}  {result.label:<35} {result.url}{issue_str}"
    )


def print_report_summary(report: AuditReport, title: str | None = None) -> int:
    """Print a colored terminal summary. Returns exit code (0=clean, 1=issues)."""
    title = title or f"{report.category.upper()} AUDIT SUMMARY"
    slow = report.slow_pages()

    total_console_errors = sum(len(r.console_errors) for r in report.results)
    total_console_warnings = sum(len(r.console_warnings) for r in report.results)
    total_failed_requests = sum(len(r.failed_requests) for r in report.results)

    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(f"  Pages visited:       {report.total_pages}")
    print(f"  HTTP errors (4xx/5xx): {len(report.http_errors)}")
    print(f"  Navigation failures: {len(report.exception_pages)}")
    print(f"  Failed requests:     {total_failed_requests} across {len(report.failed_request_pages)} page(s)")
    print(f"  Console errors:      {total_console_errors} across {len(report.error_pages)} page(s)")
    print(f"  Console warnings:    {total_console_warnings} across {len(report.warning_pages)} page(s)")
    print(f"  Slow pages (>3s):    {len(slow)}")

    if report.http_errors:
        print(f"\n\033[91m{'─' * 60}")
        print("HTTP ERRORS")
        print(f"{'─' * 60}\033[0m")
        for r in report.http_errors:
            print(f"  [{r.status_code}] {r.label}: {r.url}")
            if r.django_error:
                print(f"        Django: {r.django_error}")

    if report.exception_pages:
        print(f"\n\033[91m{'─' * 60}")
        print("NAVIGATION FAILURES")
        print(f"{'─' * 60}\033[0m")
        for r in report.exception_pages:
            print(f"  {r.label}: {r.url}")
            print(f"        {r.exception}")

    if report.failed_request_pages:
        print(f"\n\033[91m{'─' * 60}")
        print("FAILED RESOURCE REQUESTS (404s etc.)")
        print(f"{'─' * 60}\033[0m")
        for r in report.failed_request_pages:
            print(f"\n  {r.label} ({r.url}):")
            for req in r.failed_requests:
                print(f"    - {req[:200]}")

    if report.error_pages:
        print(f"\n\033[91m{'─' * 60}")
        print("CONSOLE ERRORS")
        print(f"{'─' * 60}\033[0m")
        for r in report.error_pages:
            print(f"\n  {r.label} ({r.url}):")
            for err in r.console_errors:
                print(f"    - {err[:120]}")

    if report.warning_pages:
        print(f"\n\033[93m{'─' * 60}")
        print("CONSOLE WARNINGS")
        print(f"{'─' * 60}\033[0m")
        for r in report.warning_pages:
            print(f"\n  {r.label} ({r.url}):")
            for warn in r.console_warnings:
                print(f"    - {warn[:120]}")

    if slow:
        print(f"\n\033[93m{'─' * 60}")
        print("SLOW PAGES (>3s)")
        print(f"{'─' * 60}\033[0m")
        for r in sorted(slow, key=lambda x: -x.load_time_ms):
            print(f"  {r.load_time_ms}ms  {r.label}: {r.url}")

    if report.has_issues:
        print(f"\n\033[91m✗ Issues found — review above.\033[0m\n")
    else:
        print(f"\n\033[92m✓ All {report.total_pages} pages loaded cleanly.\033[0m\n")

    return 1 if report.has_issues else 0


# ── File reporters ───────────────────────────────────────────

def save_json_report(report: AuditReport, path: str):
    """Save report as JSON."""
    data = {
        "timestamp": report.timestamp,
        "category": report.category,
        "total_pages": report.total_pages,
        "results": [],
    }
    for r in report.results:
        data["results"].append({
            "label": r.label,
            "url": r.url,
            "category": r.category,
            "status_code": r.status_code,
            "load_time_ms": r.load_time_ms,
            "failed_requests": r.failed_requests,
            "console_errors": r.console_errors,
            "console_warnings": r.console_warnings,
            "django_error": r.django_error,
            "exception": r.exception,
        })
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  JSON report saved to: {path}")


def save_junit_report(report: AuditReport, path: str):
    """Save report as JUnit XML for CI systems."""
    failures = sum(1 for r in report.results if r.has_issues)
    suite = ET.Element("testsuite", {
        "name": f"site-health-{report.category}",
        "tests": str(report.total_pages),
        "failures": str(failures),
        "timestamp": report.timestamp,
    })

    for r in report.results:
        tc = ET.SubElement(suite, "testcase", {
            "name": r.label,
            "classname": r.category,
            "time": str(round(r.load_time_ms / 1000, 3)),
        })
        if r.has_issues:
            issues = []
            if r.status_code and r.status_code >= 400:
                issues.append(f"HTTP {r.status_code}")
            if r.django_error:
                issues.append(f"Django: {r.django_error}")
            if r.console_errors:
                issues.extend(r.console_errors[:3])
            if r.failed_requests:
                issues.extend(r.failed_requests[:3])
            if r.exception:
                issues.append(r.exception)
            ET.SubElement(tc, "failure", {
                "message": issues[0][:200] if issues else "Unknown issue",
            }).text = "\n".join(issues)

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(suite)
    ET.indent(tree, space="  ")
    tree.write(path, encoding="unicode", xml_declaration=True)
    print(f"  JUnit report saved to: {path}")
