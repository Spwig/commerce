"""
Regression suite for storefront header overlay containment.

Background
----------
Every viewport-level overlay on the storefront used to be a DOM descendant of
``<header class="site-header">``. That header is ``position: sticky`` with
``z-index: var(--theme-z-sticky, 1020)``, so it forms a stacking context; and
below 768px it carried ``overflow-x: hidden``, which computes ``overflow-y``
to ``auto`` and turns the header into a clip/scroll container. Two failures
followed, both reproduced in Chromium *and* WebKit:

1. ``.widget-account-menu`` (``position: absolute; top: 100%``) was clipped
   away by the header's overflow.
2. Any containing-block property (``transform`` / ``filter`` /
   ``backdrop-filter`` / ``will-change`` / ``contain``) landing on the header
   or one of its zones collapsed the ``position: fixed`` search overlay from
   full-viewport into the header strip (measured 390x664 -> 390x76).

The fix moves ``#mobile-menu`` / ``#announcement-modal`` out of ``<header>``,
drops ``overflow-x`` from ``.site-header``, and portals the search overlay to a
body-level root via ``window.SpwigPortal``.

Testing notes
-------------
``getBoundingClientRect()`` does NOT reveal clipping — a clipped element still
reports its full untruncated rect. Every coverage assertion here therefore
uses ``document.elementFromPoint()`` hit-testing as the primary signal, with
rects used only for supporting geometry.
"""

import pytest

pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.e2e,
    pytest.mark.header_overlays,
]

# Both engines. WebKit is the closest local proxy for iOS Safari, which is
# where the original stacking-context and overflow bugs actually bit users.
ENGINES = ["chromium", "webkit"]

#: Containing-block / stacking-context properties that a theme could plausibly
#: apply to the header or one of its zones. Each of these collapsed the
#: ``position: fixed`` search overlay into the header strip before the fix.
#:
#: Each entry is (id, css, probe_target, probe_property, expected_substring).
#: The last three exist so the test can prove the injected rule actually took
#: effect — a selector typo would otherwise leave the assertions passing
#: against an unmodified page.
CONTAINING_BLOCK_STYLES = [
    (
        "backdrop_filter_on_zone",
        ".header-zone { backdrop-filter: blur(10px); }",
        "zone",
        "backdropFilter",
        "blur",
    ),
    (
        "transform_on_zone",
        ".header-zone { transform: translateZ(0); }",
        "zone",
        "transform",
        "matrix",
    ),
    (
        "will_change_on_zone",
        ".header-zone { will-change: transform; }",
        "zone",
        "willChange",
        "transform",
    ),
    (
        "contain_paint_on_zone",
        ".header-zone { contain: paint; }",
        "zone",
        "contain",
        "paint",
    ),
    (
        "filter_on_header",
        ".site-header { filter: drop-shadow(0 2px 4px rgba(0,0,0,.2)); }",
        "header",
        "filter",
        "drop-shadow",
    ),
]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def storefront_header(db, site_settings):
    """Default HeaderTemplate carrying a search widget and an account widget.

    Sticky is switched on deliberately: ``position: sticky`` is what makes
    ``.site-header`` a stacking context, and that is half of the bug being
    guarded here. A non-sticky header would not reproduce it.
    """
    from django.core.cache import cache

    from announcements.models import Announcement
    from design.header_footer_models import HeaderTemplate, Widget, WidgetPlacement

    # The suite runs with --reuse-db and these tests use transaction=True, so a
    # crashed run can leave rows behind. Reconcile rather than assume a clean
    # table, otherwise the next run dies on the unique slug.
    HeaderTemplate.objects.filter(slug="e2e-overlay-header").delete()
    Widget.objects.filter(name__in=["E2E Search", "E2E Account"]).delete()
    Announcement.objects.filter(title="E2E announcement").delete()

    header = HeaderTemplate.objects.create(
        name="E2E Overlay Header",
        slug="e2e-overlay-header",
        layout_type="classic",
        is_sticky=True,
        is_active=True,
        is_default=True,
        enable_notification_zone=True,
        mobile_menu_position="right",
    )

    search_widget = Widget.objects.create(
        name="E2E Search",
        widget_type="search",
        config={"autocomplete_enabled": False, "search_url": "/search/"},
        is_active=True,
    )
    account_widget = Widget.objects.create(
        name="E2E Account",
        widget_type="account",
        config={},
        is_active=True,
    )

    # Both live in the main-header right section so they stay on the header
    # strip at mobile widths (the centre section wraps to its own row there).
    WidgetPlacement.objects.create(
        widget=search_widget, header=header, zone="main-header_right", order=0
    )
    WidgetPlacement.objects.create(
        widget=account_widget, header=header, zone="main-header_right", order=1
    )

    # An announcement with a modal is required for #announcement-modal to
    # render at all — without it the structural assertion would pass vacuously.
    Announcement.objects.create(
        title="E2E announcement",
        body="Announcement detail body",
        link_text="Details",
        show_modal=True,
        is_enabled=True,
        priority=1,
    )

    # render_header() queries directly, but get_active_announcements() and the
    # default header/footer lookups are cached in Redis for 5 minutes and the
    # suite runs with --reuse-db against a shared cache. Drop the exact keys
    # rather than cache.clear(), which would nuke the dev environment's cache.
    for key in (
        "active_announcements",
        "active_announcements_en",
        "default_header_template",
        "default_footer_template",
    ):
        cache.delete(key)

    yield header

    for key in ("active_announcements", "active_announcements_en", "default_header_template"):
        cache.delete(key)


# ============================================================
# Helpers
# ============================================================


def _dismiss_cookie_banner(page):
    """Remove the cookie banner from the DOM.

    Clicking "Accept" is flaky under load (the banner animates in and the
    handler is bound on DOMContentLoaded), and a stray banner steals
    hit-tests at the bottom of the viewport — exactly where the overlay
    coverage probes land.
    """
    page.evaluate(
        """
        () => {
            document
                .querySelectorAll('[class*=cookie-banner], #cookie-banner')
                .forEach(n => n.remove());
        }
        """
    )


def _open_storefront(page):
    """Load the storefront home page and wait for widget JS to initialise.

    ``networkidle`` times out against the dev server under repeated loads, so
    wait on ``domcontentloaded`` plus explicit selectors instead. The
    ``data-*-initialized`` attributes are set by the widget scripts themselves
    and are the only reliable signal that their listeners are bound.
    """
    page.goto(f"{page._live_server_url}/en/", wait_until="domcontentloaded")
    page.wait_for_selector("header.site-header", state="attached", timeout=20000)
    # state="attached", not "visible": the search trigger is correctly hidden
    # at desktop widths, so "visible" would fail the desktop guard test.
    page.wait_for_selector(
        ".widget-search[data-search-initialized='true']", state="attached", timeout=20000
    )
    page.wait_for_selector(
        ".widget-account[data-account-initialized='true']", state="attached", timeout=20000
    )
    page.wait_for_function("() => !!window.SpwigPortal", timeout=20000)
    _dismiss_cookie_banner(page)


def _probe(page, x_frac, y_frac):
    """Hit-test a viewport-relative point and describe what is on top.

    Returns the topmost element's tag/id/classes plus the ancestor chain
    predicates the assertions care about. ``elementFromPoint`` is the only
    signal that actually reflects clipping and stacking; a bounding rect does
    not.
    """
    return page.evaluate(
        """
        ([xf, yf]) => {
            const x = Math.min(window.innerWidth - 1, Math.max(0, Math.round(window.innerWidth * xf)));
            const y = Math.min(window.innerHeight - 1, Math.max(0, Math.round(window.innerHeight * yf)));
            const el = document.elementFromPoint(x, y);
            if (!el) {
                return {point: [x, y], found: false};
            }
            const cls = typeof el.className === 'string' ? el.className : '';
            return {
                point: [x, y],
                found: true,
                tag: el.tagName,
                id: el.id,
                className: cls,
                inPortalRoot: !!el.closest('#spwig-overlay-root'),
                inHeader: !!el.closest('header.site-header'),
                isSearchBackdrop: !!el.closest('.search-mobile-backdrop'),
                isSearchForm: !!el.closest('.search-form'),
                isMobileMenu: !!el.closest('#mobile-menu'),
                isAccountMenu: !!el.closest('.widget-account-menu'),
            };
        }
        """,
        [x_frac, y_frac],
    )


#: Probe points covering the whole viewport: top strip (over the header),
#: centre (where the search form sits), lower band and both bottom corners.
#: Pre-fix, everything below the header strip fell through to page content.
FULL_VIEWPORT_PROBES = [
    ("top_centre", 0.5, 0.05),
    ("centre", 0.5, 0.5),
    ("lower_band", 0.5, 0.8),
    ("bottom_left", 0.02, 0.98),
    ("bottom_right", 0.98, 0.98),
]


def _assert_overlay_owns_viewport(page, label=""):
    """Every probe point must resolve inside the body-level portal root."""
    failures = []
    for name, xf, yf in FULL_VIEWPORT_PROBES:
        hit = _probe(page, xf, yf)
        if not hit.get("found") or not hit["inPortalRoot"]:
            failures.append((name, hit))
    assert not failures, (
        f"Search overlay does not cover the full viewport{' (' + label + ')' if label else ''}. "
        f"Points that hit something outside #spwig-overlay-root: {failures}"
    )


def _open_mobile_search(page, preserve_scroll=False):
    """Tap the mobile search trigger and wait for the portal to mount.

    ``preserve_scroll`` dispatches the click directly instead of going through
    Playwright's actionability path. That path calls ``scrollIntoViewIfNeeded``
    first, and for a button inside a ``position: sticky`` header Chromium
    sometimes scrolls the document to the header's *layout* position (the top),
    which silently resets ``window.scrollY`` to 0 before the handler runs. The
    scroll-lock tests then compare against a position the page no longer had.
    Use it only where the scroll offset is the thing under test.
    """
    if preserve_scroll:
        page.dispatch_event(".search-mobile-trigger", "click")
    else:
        page.click(".search-mobile-trigger")
    page.wait_for_selector("#spwig-overlay-root .search-mobile-backdrop", timeout=10000)
    # The overlay form has no transition, but give the portal a frame to paint
    # before hit-testing.
    page.wait_for_timeout(150)


def _px(value):
    """Parse a CSS pixel string ('-500px') to a float.

    Compared numerically rather than by string equality: ``window.scrollY`` is
    fractional on high-DPR mobile contexts, so ``top: -500.5px`` would never
    equal an f-string built from a Python int.
    """
    return float(str(value).replace("px", "").strip() or 0)


def _make_page_scrollable(page, height=3000):
    page.evaluate(
        """
        (h) => {
            const spacer = document.createElement('div');
            spacer.id = 'e2e-scroll-spacer';
            spacer.style.height = h + 'px';
            (document.querySelector('main') || document.body).appendChild(spacer);
        }
        """,
        height,
    )


# ============================================================
# 1. Structural: overlays are not header descendants
# ============================================================


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_viewport_overlays_are_not_header_descendants(mobile_page, storefront_header):
    """#mobile-menu and #announcement-modal must be siblings of <header>.

    Nested inside it they inherit the header's stacking context and, below
    768px, its clip container.
    """
    _open_storefront(mobile_page)

    result = mobile_page.evaluate(
        """
        () => {
            const out = {};
            for (const id of ['mobile-menu', 'announcement-modal']) {
                const el = document.getElementById(id);
                out[id] = {
                    present: !!el,
                    headerAncestor: el ? !!el.closest('header.site-header') : null,
                    parentTag: el && el.parentElement ? el.parentElement.tagName : null,
                };
            }
            return out;
        }
        """
    )

    assert result["mobile-menu"]["present"], "#mobile-menu did not render"
    assert result["announcement-modal"]["present"], (
        "#announcement-modal did not render — the storefront_header fixture must "
        "create an enabled Announcement with show_modal=True, otherwise this test "
        "passes vacuously"
    )

    assert result["mobile-menu"]["headerAncestor"] is False, (
        "#mobile-menu is a descendant of header.site-header — it will be trapped "
        "in the header's stacking context"
    )
    assert result["announcement-modal"]["headerAncestor"] is False, (
        "#announcement-modal is a descendant of header.site-header — it will be "
        "trapped in the header's stacking context"
    )
    assert result["mobile-menu"]["parentTag"] == "BODY"
    assert result["announcement-modal"]["parentTag"] == "BODY"


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_header_template_leaks_no_comment_markup(mobile_page, storefront_header):
    """The header component must not emit template comment prose into the page.

    Regression guard. Django's lexer (``tag_re``) is not compiled with
    ``re.DOTALL``, so a ``{#`` ... ``#}`` comment spanning newlines is never
    recognised as a comment and renders verbatim. A multi-line one in
    header.html did exactly that: its prose contained literal ``<header>``
    tags, the parser opened three phantom header elements, and #mobile-menu
    was adopted into the last of them — silently defeating the "overlays are
    body-level siblings" invariant while the visible page showed developer
    prose to shoppers.

    Asserting on rendered text rather than the template source keeps this
    honest for any comment style that leaks.
    """
    _open_storefront(mobile_page)

    findings = mobile_page.evaluate(
        """
        () => {
            const text = document.body.innerText || '';
            const markers = ['{#', '#}', '{%', '%}', 'Viewport-level overlays'];
            const headers = Array.from(document.querySelectorAll('header'));
            return {
                leaked: markers.filter(m => text.includes(m)),
                emptyClassHeaders: headers.filter(h => !h.className.trim()).length,
                headerCount: headers.length,
            };
        }
        """
    )

    assert findings["leaked"] == [], (
        f"Template comment markup leaked into the rendered page: {findings['leaked']}. "
        "Django's {# #} is single-line only — use {% comment %}...{% endcomment %} "
        "for multi-line notes."
    )
    assert findings["emptyClassHeaders"] == 0, (
        f"{findings['emptyClassHeaders']} unstyled <header> element(s) rendered "
        f"(total {findings['headerCount']}). Phantom headers usually mean literal "
        "markup escaped from a template comment."
    )


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_site_header_is_not_a_clip_container_on_mobile(mobile_page, storefront_header):
    """.site-header must not compute a clipping overflow at mobile widths.

    ``overflow-x: hidden`` computes ``overflow-y`` to ``auto``, which is what
    scissored the account dropdown. Overflow containment belongs on
    ``.header-zone__inner`` instead, which an absolutely-positioned dropdown
    can escape.
    """
    _open_storefront(mobile_page)

    styles = mobile_page.evaluate(
        """
        () => {
            const h = document.querySelector('header.site-header');
            const cs = getComputedStyle(h);
            return {x: cs.overflowX, y: cs.overflowY};
        }
        """
    )

    assert styles["x"] == "visible", (
        f"header.site-header has overflow-x: {styles['x']} at mobile width; "
        "any non-visible value makes it a clip container and scissors dropdowns"
    )
    assert styles["y"] == "visible", (
        f"header.site-header has overflow-y: {styles['y']} at mobile width; "
        "any non-visible value makes it a clip container and scissors dropdowns"
    )


# ============================================================
# 2. Search overlay portals out of the header
# ============================================================


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_search_overlay_is_portaled_to_body_level(mobile_page, storefront_header):
    """Opening mobile search relocates the backdrop and form to the portal root."""
    _open_storefront(mobile_page)
    _open_mobile_search(mobile_page)

    placement = mobile_page.evaluate(
        """
        () => {
            const backdrop = document.querySelector('.search-mobile-backdrop');
            const form = document.querySelector('.search-form');
            const root = document.getElementById('spwig-overlay-root');
            return {
                rootExists: !!root,
                rootIsBodyChild: root ? root.parentElement === document.body : null,
                rootIsLastChild: root ? root === document.body.lastElementChild : null,
                backdropInRoot: backdrop ? !!backdrop.closest('#spwig-overlay-root') : null,
                backdropInHeader: backdrop ? !!backdrop.closest('header.site-header') : null,
                formInRoot: form ? !!form.closest('#spwig-overlay-root') : null,
                formInHeader: form ? !!form.closest('header.site-header') : null,
                hostClass: backdrop && backdrop.parentElement
                    ? backdrop.parentElement.className : null,
            };
        }
        """
    )

    assert placement["rootExists"], "#spwig-overlay-root was never created"
    assert placement["rootIsBodyChild"], "#spwig-overlay-root must be a direct child of <body>"
    assert placement["rootIsLastChild"], (
        "#spwig-overlay-root must be the last child of <body> so it paints above "
        "earlier body content"
    )
    assert placement["backdropInRoot"] and not placement["backdropInHeader"], (
        "The search backdrop is still inside <header> — it will be capped at the "
        "header's z-index and clipped by its overflow"
    )
    assert placement["formInRoot"] and not placement["formInHeader"], (
        "The search form is still inside <header>"
    )
    # The host must carry the widget's classes or `.widget-search .search-form`
    # rules stop matching and the overlay renders unstyled.
    assert "widget-search" in placement["hostClass"]
    assert "is-open" in placement["hostClass"]


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_search_overlay_covers_full_viewport(mobile_page, storefront_header):
    """The open overlay owns every probe point, including both bottom corners."""
    _open_storefront(mobile_page)
    _open_mobile_search(mobile_page)

    _assert_overlay_owns_viewport(mobile_page)

    # Points clear of the centred form must be the backdrop specifically, not
    # some other element that merely happens to sit in the portal root.
    for name, xf, yf in [
        ("lower_band", 0.5, 0.8),
        ("bottom_left", 0.02, 0.98),
        ("bottom_right", 0.98, 0.98),
    ]:
        hit = _probe(mobile_page, xf, yf)
        assert hit["isSearchBackdrop"], (
            f"Probe {name} at {hit['point']} hit "
            f"<{hit.get('tag')} class='{hit.get('className')}'> instead of "
            ".search-mobile-backdrop"
        )

    # And the viewport centre must be the form itself.
    centre = _probe(mobile_page, 0.5, 0.5)
    assert centre["isSearchForm"], (
        f"Viewport centre hit <{centre.get('tag')} class='{centre.get('className')}'>, "
        "expected the search form"
    )


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_search_form_is_centred_in_viewport(mobile_page, storefront_header):
    """The portaled form centres on the viewport, not on the header strip."""
    _open_storefront(mobile_page)
    _open_mobile_search(mobile_page)

    geometry = mobile_page.evaluate(
        """
        () => {
            const form = document.querySelector('#spwig-overlay-root .search-form');
            const r = form.getBoundingClientRect();
            return {
                centreX: r.left + r.width / 2,
                centreY: r.top + r.height / 2,
                width: r.width,
                height: r.height,
                vw: window.innerWidth,
                vh: window.innerHeight,
            };
        }
        """
    )

    assert abs(geometry["centreX"] - geometry["vw"] / 2) <= 2, (
        f"Form is not horizontally centred: {geometry}"
    )
    assert abs(geometry["centreY"] - geometry["vh"] / 2) <= 2, (
        f"Form is not vertically centred — if it sits near the top it is being "
        f"positioned against the header rather than the viewport: {geometry}"
    )
    # Sanity: a collapsed-into-the-header overlay would be far narrower.
    assert geometry["width"] > geometry["vw"] * 0.5, (
        f"Form is unexpectedly narrow, suggesting it is laid out inside a header "
        f"zone rather than the viewport: {geometry}"
    )


# ============================================================
# 3. Immunity regression — the test that would have caught the bug
# ============================================================


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
@pytest.mark.parametrize(
    "style_name,style_css,probe_target,probe_property,expected_substring",
    CONTAINING_BLOCK_STYLES,
    ids=[s[0] for s in CONTAINING_BLOCK_STYLES],
)
def test_search_overlay_survives_containing_block_on_header(
    mobile_page,
    storefront_header,
    style_name,
    style_css,
    probe_target,
    probe_property,
    expected_substring,
):
    """A containing-block property on the header must not collapse the overlay.

    ``transform`` / ``filter`` / ``backdrop-filter`` / ``will-change`` /
    ``contain`` all make an ancestor the containing block for
    ``position: fixed`` descendants. Before the fix, any one of them shrank
    the search overlay from the full viewport (390x664) to the header strip
    (390x76). Because the overlay is now portaled to a body-level root, none
    of the header's properties can reach it.

    This is the canary: a future change that re-parents the overlay back under
    <header> fails here even if every other test still passes.
    """
    _open_storefront(mobile_page)

    # Injected before opening, the way a theme stylesheet would ship it.
    mobile_page.add_style_tag(content=style_css)
    mobile_page.wait_for_timeout(100)

    _open_mobile_search(mobile_page)

    # Guard the guard: if the selector never matched, the test proves nothing.
    # Read back the one property this case injects — checking a bag of tokens
    # against the whole computed-style dict would match its own key names and
    # pass unconditionally.
    actual = mobile_page.evaluate(
        """
        ([target, prop]) => {
            const el = target === 'zone'
                ? document.querySelector('.header-zone')
                : document.querySelector('header.site-header');
            if (!el) return null;
            const cs = getComputedStyle(el);
            return cs[prop] || cs['webkit' + prop[0].toUpperCase() + prop.slice(1)] || '';
        }
        """,
        [probe_target, probe_property],
    )
    assert actual is not None, f"No element matched target {probe_target!r}"
    assert expected_substring in actual, (
        f"Injected style {style_name!r} did not take effect: computed "
        f"{probe_property} on {probe_target} is {actual!r}, expected it to contain "
        f"{expected_substring!r}. Without the property applied this test proves nothing."
    )

    _assert_overlay_owns_viewport(mobile_page, label=style_name)

    # And the geometry must still be viewport-sized, not header-sized.
    backdrop = mobile_page.evaluate(
        """
        () => {
            const b = document.querySelector('#spwig-overlay-root .search-mobile-backdrop');
            const r = b.getBoundingClientRect();
            return {width: r.width, height: r.height, top: r.top,
                    vw: window.innerWidth, vh: window.innerHeight};
        }
        """
    )
    assert backdrop["height"] >= backdrop["vh"] - 1, (
        f"Backdrop collapsed to {backdrop['width']}x{backdrop['height']} inside a "
        f"{backdrop['vw']}x{backdrop['vh']} viewport under {style_name!r} — the "
        "header has become its containing block"
    )
    assert backdrop["width"] >= backdrop["vw"] - 1, f"Backdrop is not full-width: {backdrop}"


# ============================================================
# 4. Account dropdown is not clipped by the header
# ============================================================


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_account_dropdown_overhangs_header_unclipped(mobile_page, storefront_header):
    """The account menu hangs below the header and must stay hit-testable.

    It is anchored under its button (``position: absolute; top: 100%``), so it
    starts inside the header box and must overhang the bottom edge. When the
    header was a clip container the overhanging part vanished — while
    ``getBoundingClientRect()`` still reported the full, untruncated rect.
    That is why this asserts via ``elementFromPoint``.
    """
    _open_storefront(mobile_page)

    mobile_page.click(".widget-account-button")
    mobile_page.wait_for_selector(".widget-account.is-open", timeout=10000)
    # .widget-account-menu transitions opacity/visibility over 150ms; hit-tests
    # against a visibility:hidden element would fail spuriously.
    mobile_page.wait_for_timeout(400)

    geometry = mobile_page.evaluate(
        """
        () => {
            const menu = document.querySelector('.widget-account-menu');
            const header = document.querySelector('header.site-header');
            const mr = menu.getBoundingClientRect();
            const hr = header.getBoundingClientRect();
            const cs = getComputedStyle(menu);
            return {
                menu: {top: mr.top, bottom: mr.bottom, left: mr.left, right: mr.right,
                       width: mr.width, height: mr.height},
                header: {top: hr.top, bottom: hr.bottom},
                visibility: cs.visibility,
                opacity: cs.opacity,
            };
        }
        """
    )

    assert geometry["visibility"] == "visible", f"Account menu did not become visible: {geometry}"
    assert geometry["menu"]["height"] > 0, f"Account menu has no height: {geometry}"

    # The overhang is the whole point — without it there is nothing to clip and
    # the hit-test below would prove nothing.
    assert geometry["menu"]["bottom"] > geometry["header"]["bottom"], (
        f"Account menu does not extend past the header's bottom edge "
        f"({geometry['menu']['bottom']} <= {geometry['header']['bottom']}), so this "
        "test cannot detect clipping. Check the header/widget layout."
    )

    # Hit-test inside the overhanging portion. A clipped menu still reports the
    # rect above but loses the hit-test to whatever is underneath.
    overhang_top = max(geometry["header"]["bottom"], geometry["menu"]["top"])
    probe_y = (overhang_top + geometry["menu"]["bottom"]) / 2
    probe_x = (geometry["menu"]["left"] + geometry["menu"]["right"]) / 2

    hit = mobile_page.evaluate(
        """
        ([x, y]) => {
            const el = document.elementFromPoint(x, y);
            if (!el) return {found: false};
            const cls = typeof el.className === 'string' ? el.className : '';
            return {
                found: true,
                tag: el.tagName,
                className: cls,
                inAccountMenu: !!el.closest('.widget-account-menu'),
            };
        }
        """,
        [probe_x, probe_y],
    )

    assert hit["found"], f"No element at the overhang probe point ({probe_x}, {probe_y})"
    assert hit["inAccountMenu"], (
        f"The account dropdown is clipped: the point ({probe_x:.0f}, {probe_y:.0f}) lies "
        f"inside its reported rect but hit <{hit['tag']} class='{hit['className']}'>. "
        "This is the overflow-clipping regression — getBoundingClientRect() would not "
        "have caught it."
    )


# ============================================================
# 5. Portal lifecycle
# ============================================================


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_portal_restores_dom_position_on_close(mobile_page, storefront_header):
    """unmount() returns the nodes to their exact original slot and cleans up."""
    _open_storefront(mobile_page)

    before = mobile_page.evaluate(
        """
        () => {
            const widget = document.querySelector('.widget-search');
            return {
                childOrder: Array.from(widget.children).map(c => c.className || c.tagName),
            };
        }
        """
    )

    _open_mobile_search(mobile_page)
    mobile_page.click(".search-mobile-close")
    mobile_page.wait_for_selector(".widget-search.is-open", state="detached", timeout=10000)
    mobile_page.wait_for_timeout(150)

    after = mobile_page.evaluate(
        """
        () => {
            const widget = document.querySelector('.widget-search');
            const backdrop = document.querySelector('.search-mobile-backdrop');
            const form = document.querySelector('.search-form');
            const root = document.getElementById('spwig-overlay-root');

            // Count leftover placeholder comment markers anywhere in the document.
            const walker = document.createTreeWalker(
                document.documentElement, NodeFilter.SHOW_COMMENT
            );
            let markers = 0;
            while (walker.nextNode()) {
                if (walker.currentNode.nodeValue.includes('spwig-portal-placeholder')) {
                    markers += 1;
                }
            }

            return {
                childOrder: Array.from(widget.children).map(c => c.className || c.tagName),
                backdropInWidget: backdrop ? widget.contains(backdrop) : null,
                formInWidget: form ? widget.contains(form) : null,
                backdropInHeader: backdrop ? !!backdrop.closest('header.site-header') : null,
                rootChildCount: root ? root.children.length : null,
                markers: markers,
                bodyPosition: getComputedStyle(document.body).position,
            };
        }
        """
    )

    assert after["backdropInWidget"], "Backdrop was not returned to .widget-search"
    assert after["formInWidget"], "Search form was not returned to .widget-search"
    assert after["backdropInHeader"], (
        "Backdrop should be back inside the header after close — it only lives at "
        "body level while the overlay is open"
    )
    assert after["childOrder"] == before["childOrder"], (
        f"DOM order inside .widget-search changed across a portal round-trip: "
        f"{before['childOrder']} -> {after['childOrder']}"
    )
    assert after["rootChildCount"] == 0, (
        f"#spwig-overlay-root still holds {after['rootChildCount']} host(s) after close"
    )
    assert after["markers"] == 0, (
        f"{after['markers']} spwig-portal-placeholder comment marker(s) leaked into the DOM"
    )
    assert after["bodyPosition"] != "fixed", (
        "Scroll lock was not released — body is still position: fixed"
    )


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_search_overlay_locks_and_restores_scroll(mobile_page, storefront_header):
    """The iOS-safe scroll lock pins the body and restores the exact offset."""
    _open_storefront(mobile_page)
    _make_page_scrollable(mobile_page)

    mobile_page.evaluate("() => window.scrollTo(0, 500)")
    mobile_page.wait_for_timeout(150)
    scroll_before = mobile_page.evaluate("() => window.scrollY")
    assert scroll_before > 0, "Page did not scroll, so the restore assertion below would be vacuous"

    _open_mobile_search(mobile_page, preserve_scroll=True)

    locked = mobile_page.evaluate(
        """
        () => ({
            position: document.body.style.position,
            top: document.body.style.top,
            overflow: document.body.style.overflow,
        })
        """
    )
    assert locked["position"] == "fixed", (
        f"Body was not pinned while the overlay is open: {locked}. iOS Safari "
        "ignores overflow: hidden on <body> for touch scrolling."
    )
    assert _px(locked["top"]) == pytest.approx(-scroll_before, abs=1), (
        f"Body offset does not preserve the scroll position: {locked} "
        f"(expected top: about -{scroll_before}px)"
    )

    mobile_page.click(".search-mobile-close")
    mobile_page.wait_for_selector(".widget-search.is-open", state="detached", timeout=10000)
    mobile_page.wait_for_timeout(200)

    after = mobile_page.evaluate(
        """
        () => ({
            scrollY: window.scrollY,
            position: getComputedStyle(document.body).position,
            inlinePosition: document.body.style.position,
        })
        """
    )
    assert after["inlinePosition"] == "", f"Scroll lock styles were not cleared: {after}"
    assert after["scrollY"] == pytest.approx(scroll_before, abs=1), (
        f"Scroll position was not restored: {after['scrollY']} != {scroll_before}"
    )


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_escape_closes_portaled_search(mobile_page, storefront_header):
    """Escape must still close once focus has moved into the portaled input.

    The keydown listener is bound on ``document`` precisely because the focused
    input is no longer a descendant of the widget after the move.
    """
    _open_storefront(mobile_page)
    _open_mobile_search(mobile_page)

    focused_outside_widget = mobile_page.evaluate(
        """
        () => {
            const widget = document.querySelector('.widget-search');
            const input = document.querySelector('#spwig-overlay-root .search-input');
            if (input) input.focus();
            return !widget.contains(document.activeElement);
        }
        """
    )
    assert focused_outside_widget, (
        "The focused element is still inside .widget-search, so a widget-scoped "
        "keydown listener would also pass — this test would prove nothing"
    )

    mobile_page.keyboard.press("Escape")
    mobile_page.wait_for_selector(".widget-search.is-open", state="detached", timeout=10000)

    root_children = mobile_page.evaluate(
        "() => document.getElementById('spwig-overlay-root').children.length"
    )
    assert root_children == 0, "Escape closed the widget but left the portal host mounted"


# ============================================================
# 6. Desktop guard
# ============================================================


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_search_is_never_portaled_at_desktop_width(desktop_page, storefront_header):
    """Above the breakpoint the search is an inline header field, not an overlay."""
    _open_storefront(desktop_page)

    state = desktop_page.evaluate(
        """
        () => {
            const trigger = document.querySelector('.search-mobile-trigger');
            const form = document.querySelector('.search-form');
            return {
                triggerDisplay: getComputedStyle(trigger).display,
                formInHeader: !!form.closest('header.site-header'),
                formPosition: getComputedStyle(form).position,
                rootExists: !!document.getElementById('spwig-overlay-root'),
                matchesOverlayQuery: window.matchMedia('(max-width: 767.98px)').matches,
            };
        }
        """
    )

    assert state["matchesOverlayQuery"] is False, (
        "Desktop context unexpectedly matches the mobile overlay media query"
    )
    assert state["triggerDisplay"] == "none", (
        f"The mobile search trigger is visible at desktop width "
        f"(display: {state['triggerDisplay']})"
    )
    assert state["formInHeader"], "The search form left the header at desktop width"
    assert state["formPosition"] != "fixed", (
        f"The search form is position: {state['formPosition']} at desktop width; "
        "it should be an inline header field"
    )
    assert not state["rootExists"], (
        "#spwig-overlay-root was created at desktop width — nothing should portal here"
    )


# ============================================================
# 7. Mobile menu
# ============================================================


@pytest.mark.parametrize("browser_engine", ENGINES, indirect=True)
def test_mobile_menu_covers_viewport_and_locks_scroll(mobile_page, storefront_header):
    """The slide-out drawer owns the viewport and pins the page behind it.

    ``body.menu-open`` had no stylesheet rule at all, so the page scrolled
    behind the open drawer. The drawer now drives SpwigPortal's refcounted
    scroll lock instead.
    """
    _open_storefront(mobile_page)
    _make_page_scrollable(mobile_page)

    mobile_page.evaluate("() => window.scrollTo(0, 400)")
    mobile_page.wait_for_timeout(150)
    scroll_before = mobile_page.evaluate("() => window.scrollY")
    assert scroll_before > 0, "Page did not scroll; the restore assertion would be vacuous"

    # dispatch_event, not click: Playwright's actionability path scrolls the
    # element into view first, and for a button inside a position: sticky
    # header that can reset window.scrollY to 0 before the handler runs —
    # which is precisely the value this test is asserting on.
    mobile_page.dispatch_event("[data-menu-toggle]", "click")
    mobile_page.wait_for_selector("#mobile-menu.is-open", timeout=10000)
    # .mobile-menu animates transform over 0.3s; probe after it settles.
    mobile_page.wait_for_timeout(500)

    locked = mobile_page.evaluate(
        """
        () => ({
            position: document.body.style.position,
            top: document.body.style.top,
            ariaHidden: document.getElementById('mobile-menu').getAttribute('aria-hidden'),
            ariaExpanded: document
                .querySelector('[data-menu-toggle]').getAttribute('aria-expanded'),
        })
        """
    )
    assert locked["position"] == "fixed", f"Mobile menu did not lock scroll: {locked}"
    assert _px(locked["top"]) == pytest.approx(-scroll_before, abs=1), (
        f"Scroll offset not preserved: {locked} (expected about -{scroll_before}px)"
    )
    assert locked["ariaHidden"] == "false"
    assert locked["ariaExpanded"] == "true"

    failures = []
    for name, xf, yf in FULL_VIEWPORT_PROBES:
        hit = _probe(mobile_page, xf, yf)
        if not hit.get("found") or not hit["isMobileMenu"]:
            failures.append((name, hit))
    assert not failures, (
        f"The open mobile menu does not cover the full viewport. Points that hit "
        f"something outside #mobile-menu: {failures}"
    )

    mobile_page.click("[data-menu-close]")
    mobile_page.wait_for_selector("#mobile-menu.is-open", state="detached", timeout=10000)
    mobile_page.wait_for_timeout(200)

    after = mobile_page.evaluate(
        """
        () => ({
            scrollY: window.scrollY,
            inlinePosition: document.body.style.position,
            ariaHidden: document.getElementById('mobile-menu').getAttribute('aria-hidden'),
            bodyHasMenuOpen: document.body.classList.contains('menu-open'),
        })
        """
    )
    assert after["inlinePosition"] == "", f"Scroll lock was not released: {after}"
    assert after["scrollY"] == pytest.approx(scroll_before, abs=1), (
        f"Scroll position not restored after closing the menu: "
        f"{after['scrollY']} != {scroll_before}"
    )
    assert after["ariaHidden"] == "true"
    assert after["bodyHasMenuOpen"] is False
