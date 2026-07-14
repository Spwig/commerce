"""
Admin Sidebar Audit Runner

Discovers all links in the Django admin sidebar and visits each one,
collecting health data via the audit engine.
"""

import time

from playwright.sync_api import Page

from tests.audit.engine import (
    AuditReport,
    PageResult,
    print_result_line,
    visit_page_browser,
)


def login_admin(page: Page, base_url: str, username: str, password: str):
    """Log in to Django admin."""
    page.goto(f"{base_url}/en/admin/login/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")
    if "/login/" in page.url:
        raise RuntimeError(f"Admin login failed — still on {page.url}")


def discover_sidebar_links(page: Page) -> list[dict]:
    """Extract all sidebar <a> links with their text and href."""
    page.evaluate("""
        () => {
            document.querySelectorAll('.submenu-container.collapsed')
                .forEach(el => el.classList.remove('collapsed'));
        }
    """)
    time.sleep(0.3)

    links = page.evaluate("""
        () => {
            const seen = new Set();
            const results = [];
            document.querySelectorAll('.sidebar-menu a.menu-item').forEach(a => {
                const href = a.getAttribute('href');
                const text = (a.querySelector('.menu-text')?.textContent || '').trim();
                if (href && text && !seen.has(href)) {
                    const target = a.getAttribute('target');
                    seen.add(href);
                    results.push({href, text, target_blank: target === '_blank'});
                }
            });
            return results;
        }
    """)
    return links


def run_admin_audit(
    page: Page,
    base_url: str,
    skip_target_blank: bool = True,
    verbose: bool = True,
) -> AuditReport:
    """
    Run a full admin sidebar audit.

    Expects the page to already be logged in and on an admin page.
    Discovers sidebar links, visits each one, returns an AuditReport.
    """
    # Navigate to admin root to discover sidebar
    page.goto(f"{base_url}/en/admin/")
    page.wait_for_load_state("networkidle")

    links = discover_sidebar_links(page)

    if skip_target_blank:
        skipped = [link for link in links if link.get("target_blank")]
        links = [link for link in links if not link.get("target_blank")]
        if skipped and verbose:
            print(
                f"  Skipping {len(skipped)} target=_blank links: "
                f"{', '.join(lang['text'] for lang in skipped)}"
            )

    if verbose:
        print(f"  Found {len(links)} admin sidebar links to audit\n")

    results: list[PageResult] = []
    for i, link in enumerate(links, 1):
        result = visit_page_browser(
            page,
            url=link["href"],
            label=link["text"],
            base_url=base_url,
            category="admin",
        )
        results.append(result)
        if verbose:
            print_result_line(i, len(links), result)

    return AuditReport(category="admin", results=results)
