"""
Tests for ContentSanitizer - Comprehensive XSS prevention testing.

Based on OWASP XSS Cheat Sheet and real-world attack vectors.
"""

import pytest
from design.content_sanitizer import ContentSanitizer


@pytest.mark.django_db
class TestContentSanitizerBasics:
    """Test basic sanitizer functionality."""

    def test_initialize_tier_a(self):
        """Test initialization with Tier A."""
        sanitizer = ContentSanitizer(tier='A')
        assert sanitizer.tier == 'A'
        assert 'p' in sanitizer.allowed_tags
        assert 'script' not in sanitizer.allowed_tags

    def test_initialize_tier_b(self):
        """Test initialization with Tier B."""
        sanitizer = ContentSanitizer(tier='B')
        assert sanitizer.tier == 'B'
        assert 'h1' in sanitizer.allowed_tags
        assert 'img' in sanitizer.allowed_tags

    def test_initialize_tier_c(self):
        """Test initialization with Tier C."""
        sanitizer = ContentSanitizer(tier='C')
        assert sanitizer.tier == 'C'
        assert 'div' in sanitizer.allowed_tags
        assert 'iframe' in sanitizer.allowed_tags

    def test_initialize_invalid_tier(self):
        """Test that invalid tier raises error."""
        with pytest.raises(ValueError, match='Invalid tier'):
            ContentSanitizer(tier='D')

    def test_custom_allowed_domains(self):
        """Test custom allowed domains."""
        sanitizer = ContentSanitizer(tier='C', allowed_domains=['example.com'])
        assert 'example.com' in sanitizer.allowed_domains
        assert 'fonts.googleapis.com' in sanitizer.allowed_domains  # Default still there


@pytest.mark.django_db
class TestTierAAllowedTags:
    """Test Tier A allowed tags (most restrictive)."""

    def test_allows_basic_text_tags(self):
        """Test that Tier A allows basic text formatting."""
        sanitizer = ContentSanitizer(tier='A')
        html = '<p>Hello <strong>world</strong> and <em>everyone</em>!</p>'
        result = sanitizer.sanitize_html(html)
        assert '<p>' in result
        assert '<strong>' in result
        assert '<em>' in result

    def test_blocks_headings(self):
        """Test that Tier A blocks headings."""
        sanitizer = ContentSanitizer(tier='A')
        html = '<h1>Title</h1><p>Content</p>'
        result = sanitizer.sanitize_html(html)
        assert '<h1>' not in result
        assert '<p>Content</p>' in result

    def test_blocks_links(self):
        """Test that Tier A blocks links."""
        sanitizer = ContentSanitizer(tier='A')
        html = '<a href="https://example.com">Link</a>'
        result = sanitizer.sanitize_html(html)
        assert '<a' not in result
        assert 'Link' in result  # Text preserved

    def test_blocks_images(self):
        """Test that Tier A blocks images."""
        sanitizer = ContentSanitizer(tier='A')
        html = '<img src="image.jpg" alt="Image">'
        result = sanitizer.sanitize_html(html)
        assert '<img' not in result

    def test_blocks_divs(self):
        """Test that Tier A blocks divs."""
        sanitizer = ContentSanitizer(tier='A')
        html = '<div class="container"><p>Text</p></div>'
        result = sanitizer.sanitize_html(html)
        assert '<div' not in result
        assert '<p>Text</p>' in result


@pytest.mark.django_db
class TestTierBAllowedTags:
    """Test Tier B allowed tags (moderate)."""

    def test_allows_headings(self):
        """Test that Tier B allows headings."""
        sanitizer = ContentSanitizer(tier='B')
        html = '<h1>Title</h1><h2>Subtitle</h2><p>Content</p>'
        result = sanitizer.sanitize_html(html)
        assert '<h1>' in result
        assert '<h2>' in result
        assert '<p>' in result

    def test_allows_links(self):
        """Test that Tier B allows links."""
        sanitizer = ContentSanitizer(tier='B')
        html = '<a href="https://example.com" title="Link">Click</a>'
        result = sanitizer.sanitize_html(html)
        assert '<a' in result
        assert 'href="https://example.com"' in result

    def test_allows_images(self):
        """Test that Tier B allows images."""
        sanitizer = ContentSanitizer(tier='B')
        html = '<img src="image.jpg" alt="Image" width="100">'
        result = sanitizer.sanitize_html(html)
        assert '<img' in result
        assert 'src="image.jpg"' in result
        assert 'alt="Image"' in result

    def test_allows_lists(self):
        """Test that Tier B allows lists."""
        sanitizer = ContentSanitizer(tier='B')
        html = '<ul><li>Item 1</li><li>Item 2</li></ul>'
        result = sanitizer.sanitize_html(html)
        assert '<ul>' in result
        assert '<li>' in result

    def test_blocks_divs(self):
        """Test that Tier B still blocks divs."""
        sanitizer = ContentSanitizer(tier='B')
        html = '<div class="container"><p>Text</p></div>'
        result = sanitizer.sanitize_html(html)
        assert '<div' not in result


@pytest.mark.django_db
class TestTierCAllowedTags:
    """Test Tier C allowed tags (most permissive)."""

    def test_allows_divs_and_sections(self):
        """Test that Tier C allows structural elements."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<div><section><article><p>Text</p></article></section></div>'
        result = sanitizer.sanitize_html(html)
        assert '<div>' in result
        assert '<section>' in result
        assert '<article>' in result

    def test_allows_iframes_with_sandbox(self):
        """Test that Tier C allows iframes."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<iframe src="https://example.com" sandbox="allow-scripts"></iframe>'
        result = sanitizer.sanitize_html(html)
        assert '<iframe' in result

    def test_allows_video(self):
        """Test that Tier C allows video elements."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<video src="video.mp4" controls></video>'
        result = sanitizer.sanitize_html(html)
        assert '<video' in result

    def test_allows_tables(self):
        """Test that Tier C allows tables."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<table><tr><th>Header</th></tr><tr><td>Data</td></tr></table>'
        result = sanitizer.sanitize_html(html)
        assert '<table>' in result
        assert '<tr>' in result
        assert '<th>' in result
        assert '<td>' in result


@pytest.mark.django_db
class TestXSSPreventionScriptInjection:
    """Test XSS prevention - Script injection attacks."""

    def test_blocks_script_tags(self):
        """Test blocking of script tags."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<script>alert("XSS")</script><p>Safe content</p>'
        result = sanitizer.sanitize_html(html)
        assert '<script' not in result.lower()
        assert '<p>Safe content</p>' in result

    def test_blocks_script_with_src(self):
        """Test blocking of external script tags."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<script src="https://evil.com/xss.js"></script>'
        result = sanitizer.sanitize_html(html)
        assert '<script' not in result.lower()

    def test_blocks_javascript_protocol_in_links(self):
        """Test blocking of javascript: protocol in links."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<a href="javascript:alert(\'XSS\')">Click</a>'
        result = sanitizer.sanitize_html(html)
        # Link should be removed or href stripped
        assert 'javascript:' not in result.lower()

    def test_blocks_javascript_protocol_in_images(self):
        """Test blocking of javascript: protocol in images."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<img src="javascript:alert(\'XSS\')">'
        result = sanitizer.sanitize_html(html)
        assert 'javascript:' not in result.lower()


@pytest.mark.django_db
class TestXSSPreventionEventHandlers:
    """Test XSS prevention - Event handler attacks."""

    def test_blocks_onclick(self):
        """Test blocking of onclick event handlers."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<div onclick="alert(\'XSS\')">Click me</div>'
        result = sanitizer.sanitize_html(html)
        assert 'onclick' not in result.lower()

    def test_blocks_onerror(self):
        """Test blocking of onerror event handlers."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<img src="x" onerror="alert(\'XSS\')">'
        result = sanitizer.sanitize_html(html)
        assert 'onerror' not in result.lower()

    def test_blocks_onload(self):
        """Test blocking of onload event handlers."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<body onload="alert(\'XSS\')">Content</body>'
        result = sanitizer.sanitize_html(html)
        assert 'onload' not in result.lower()

    def test_blocks_onmouseover(self):
        """Test blocking of onmouseover event handlers."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<div onmouseover="alert(\'XSS\')">Hover</div>'
        result = sanitizer.sanitize_html(html)
        assert 'onmouseover' not in result.lower()

    def test_blocks_onauxclick(self):
        """Test blocking of onauxclick event handlers."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<div onauxclick="alert(\'XSS\')">Click</div>'
        result = sanitizer.sanitize_html(html)
        assert 'onauxclick' not in result.lower()


@pytest.mark.django_db
class TestXSSPreventionDataURIs:
    """Test XSS prevention - Data URI attacks."""

    def test_blocks_data_uri_with_script(self):
        """Test blocking of data: URIs with embedded scripts."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<a href="data:text/html,<script>alert(\'XSS\')</script>">Click</a>'
        result = sanitizer.sanitize_html(html)
        assert 'data:text/html' not in result.lower()

    def test_blocks_data_uri_base64_script(self):
        """Test blocking of base64-encoded data URIs."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<iframe src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="></iframe>'
        result = sanitizer.sanitize_html(html)
        assert 'data:text/html' not in result.lower()


@pytest.mark.django_db
class TestXSSPreventionCSSInjection:
    """Test XSS prevention - CSS injection attacks."""

    def test_blocks_css_expression(self):
        """Test blocking of CSS expressions (IE)."""
        sanitizer = ContentSanitizer(tier='C')
        css = 'width: expression(alert("XSS"));'
        result = sanitizer.sanitize_css(css)
        assert 'expression' not in result.lower()

    def test_blocks_css_behavior(self):
        """Test blocking of CSS behaviors (IE)."""
        sanitizer = ContentSanitizer(tier='C')
        css = 'behavior: url(xss.htc);'
        result = sanitizer.sanitize_css(css)
        assert 'behavior' not in result.lower()

    def test_blocks_css_import(self):
        """Test blocking of @import rules."""
        sanitizer = ContentSanitizer(tier='C')
        css = '@import url("https://evil.com/xss.css");'
        result = sanitizer.sanitize_css(css)
        assert '@import' not in result.lower()

    def test_blocks_moz_binding(self):
        """Test blocking of -moz-binding (Firefox)."""
        sanitizer = ContentSanitizer(tier='C')
        css = '-moz-binding: url("https://evil.com/xss.xml#xss");'
        result = sanitizer.sanitize_css(css)
        assert '-moz-binding' not in result.lower()

    def test_allows_safe_css(self):
        """Test that safe CSS properties pass through."""
        sanitizer = ContentSanitizer(tier='C')
        css = 'color: red; background: blue; font-size: 16px;'
        result = sanitizer.sanitize_css(css)
        assert 'color: red' in result
        assert 'background: blue' in result


@pytest.mark.django_db
class TestURLSanitization:
    """Test URL sanitization and validation."""

    def test_allows_https_url(self):
        """Test that HTTPS URLs are allowed."""
        sanitizer = ContentSanitizer(tier='C')
        url = 'https://example.com/page'
        result = sanitizer.sanitize_url(url)
        assert result == url

    def test_allows_http_url(self):
        """Test that HTTP URLs are allowed."""
        sanitizer = ContentSanitizer(tier='C')
        url = 'http://example.com/page'
        result = sanitizer.sanitize_url(url)
        assert result == url

    def test_allows_mailto_url(self):
        """Test that mailto: URLs are allowed."""
        sanitizer = ContentSanitizer(tier='C')
        url = 'mailto:user@example.com'
        result = sanitizer.sanitize_url(url)
        assert result == url

    def test_allows_tel_url(self):
        """Test that tel: URLs are allowed."""
        sanitizer = ContentSanitizer(tier='C')
        url = 'tel:+1234567890'
        result = sanitizer.sanitize_url(url)
        assert result == url

    def test_blocks_javascript_url(self):
        """Test that javascript: URLs are blocked."""
        sanitizer = ContentSanitizer(tier='C')
        url = 'javascript:alert("XSS")'
        result = sanitizer.sanitize_url(url)
        assert result is None

    def test_blocks_vbscript_url(self):
        """Test that vbscript: URLs are blocked."""
        sanitizer = ContentSanitizer(tier='C')
        url = 'vbscript:msgbox("XSS")'
        result = sanitizer.sanitize_url(url)
        assert result is None

    def test_blocks_data_url(self):
        """Test that data: URLs are blocked."""
        sanitizer = ContentSanitizer(tier='C')
        url = 'data:text/html,<script>alert(1)</script>'
        result = sanitizer.sanitize_url(url)
        assert result is None

    def test_validates_external_domain_allowed(self):
        """Test that whitelisted external domains are allowed."""
        sanitizer = ContentSanitizer(tier='C')
        url = 'https://fonts.googleapis.com/css?family=Roboto'
        result = sanitizer.sanitize_url(url)
        assert result == url

    def test_validates_external_domain_blocked(self):
        """Test that non-whitelisted external domains are blocked in Tier A/B."""
        sanitizer = ContentSanitizer(tier='B')  # Tier A/B require whitelisting
        url = 'https://evil-site.com/malware.js'
        result = sanitizer.sanitize_url(url)
        assert result is None

    def test_allows_relative_urls(self):
        """Test that relative URLs are allowed."""
        sanitizer = ContentSanitizer(tier='C')
        url = '/products/item-123'
        result = sanitizer.sanitize_url(url)
        assert result == url


@pytest.mark.django_db
class TestIframeSandboxValidation:
    """Test iframe sandbox attribute validation."""

    def test_detects_iframe_without_sandbox(self):
        """Test detection of iframe without sandbox."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<iframe src="https://example.com"></iframe>'
        result = sanitizer.validate_iframe_sandbox(html)
        assert result is False

    def test_allows_iframe_with_sandbox(self):
        """Test that iframe with sandbox is allowed."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<iframe src="https://example.com" sandbox="allow-scripts"></iframe>'
        result = sanitizer.validate_iframe_sandbox(html)
        assert result is True

    def test_blocks_iframe_in_tier_a(self):
        """Test that iframes are blocked in Tier A."""
        sanitizer = ContentSanitizer(tier='A')
        html = '<iframe src="https://example.com" sandbox="allow-scripts"></iframe>'
        result = sanitizer.validate_iframe_sandbox(html)
        assert result is False

    def test_blocks_iframe_in_tier_b(self):
        """Test that iframes are blocked in Tier B."""
        sanitizer = ContentSanitizer(tier='B')
        html = '<iframe src="https://example.com" sandbox="allow-scripts"></iframe>'
        result = sanitizer.validate_iframe_sandbox(html)
        assert result is False


@pytest.mark.django_db
class TestDangerousPatternDetection:
    """Test detection of dangerous patterns."""

    def test_detects_script_tag_pattern(self):
        """Test detection of script tag pattern."""
        sanitizer = ContentSanitizer(tier='C')
        content = 'Some text <script>alert(1)</script> more text'
        result = sanitizer._contains_dangerous_pattern(content)
        assert result is True

    def test_detects_event_handler_pattern(self):
        """Test detection of event handler pattern."""
        sanitizer = ContentSanitizer(tier='C')
        content = '<div onclick="alert(1)">Click</div>'
        result = sanitizer._contains_dangerous_pattern(content)
        assert result is True

    def test_detects_javascript_protocol(self):
        """Test detection of javascript: protocol."""
        sanitizer = ContentSanitizer(tier='C')
        content = '<a href="javascript:void(0)">Link</a>'
        result = sanitizer._contains_dangerous_pattern(content)
        assert result is True

    def test_safe_content_passes(self):
        """Test that safe content doesn't trigger detection."""
        sanitizer = ContentSanitizer(tier='C')
        content = '<p>This is <strong>safe</strong> content</p>'
        result = sanitizer._contains_dangerous_pattern(content)
        assert result is False


@pytest.mark.django_db
class TestExternalDomainValidation:
    """Test external domain whitelisting."""

    def test_allows_exact_match(self):
        """Test exact domain match."""
        sanitizer = ContentSanitizer(tier='C')
        result = sanitizer._is_domain_allowed('fonts.googleapis.com')
        assert result is True

    def test_allows_subdomain_match(self):
        """Test subdomain matching."""
        sanitizer = ContentSanitizer(tier='C')
        result = sanitizer._is_domain_allowed('cdn.example.com')
        assert result is False  # Not in whitelist

    def test_blocks_unknown_domain(self):
        """Test blocking of unknown domains."""
        sanitizer = ContentSanitizer(tier='C')
        result = sanitizer._is_domain_allowed('malicious-site.com')
        assert result is False

    def test_strips_port_from_domain(self):
        """Test that port is stripped before checking."""
        sanitizer = ContentSanitizer(tier='C')
        result = sanitizer._is_domain_allowed('fonts.googleapis.com:443')
        assert result is True


@pytest.mark.django_db
class TestSanitizationReport:
    """Test sanitization reporting."""

    def test_generates_basic_report(self):
        """Test basic sanitization report generation."""
        sanitizer = ContentSanitizer(tier='A')
        html = '<div><script>alert(1)</script><p>Text</p></div>'
        report = sanitizer.get_sanitization_report(html)

        assert report['tier'] == 'A'
        assert report['has_dangerous_patterns'] is True
        assert 'script' in report['disallowed_tags']
        assert 'div' in report['disallowed_tags']

    def test_report_shows_allowed_content(self):
        """Test that report doesn't flag allowed content."""
        sanitizer = ContentSanitizer(tier='A')
        html = '<p>Safe <strong>content</strong></p>'
        report = sanitizer.get_sanitization_report(html)

        assert report['has_dangerous_patterns'] is False
        assert 'p' not in report['disallowed_tags']


@pytest.mark.django_db
class TestEdgeCases:
    """Test edge cases and unusual inputs."""

    def test_empty_string(self):
        """Test sanitizing empty string."""
        sanitizer = ContentSanitizer(tier='C')
        result = sanitizer.sanitize_html('')
        assert result == ''

    def test_none_value(self):
        """Test sanitizing None value."""
        sanitizer = ContentSanitizer(tier='C')
        result = sanitizer.sanitize_html(None)
        assert result == ''

    def test_very_long_html(self):
        """Test sanitizing very long HTML."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<p>Text</p>' * 1000
        result = sanitizer.sanitize_html(html)
        assert '<p>Text</p>' in result
        assert '<script>' not in result

    def test_nested_tags(self):
        """Test deeply nested tags."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<div><div><div><div><p>Deep</p></div></div></div></div>'
        result = sanitizer.sanitize_html(html)
        assert '<p>Deep</p>' in result

    def test_malformed_html(self):
        """Test malformed HTML."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<p>Unclosed paragraph<div>Div</div>'
        result = sanitizer.sanitize_html(html)
        # Should handle gracefully
        assert isinstance(result, str)

    def test_unicode_content(self):
        """Test Unicode content."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<p>Hello 世界 🌍</p>'
        result = sanitizer.sanitize_html(html)
        assert '世界' in result
        assert '🌍' in result

    def test_case_insensitive_tag_blocking(self):
        """Test that tag blocking is case-insensitive."""
        sanitizer = ContentSanitizer(tier='C')
        html = '<SCRIPT>alert(1)</SCRIPT><ScRiPt>alert(2)</ScRiPt>'
        result = sanitizer.sanitize_html(html)
        assert 'script' not in result.lower()


@pytest.mark.django_db
class TestPerformance:
    """Test performance benchmarks."""

    def test_sanitize_1kb_html_performance(self):
        """Test sanitizing 1KB of HTML."""
        import time
        sanitizer = ContentSanitizer(tier='C')
        html = '<p>Test content</p>' * 50  # ~1KB

        start = time.time()
        result = sanitizer.sanitize_html(html)
        elapsed = (time.time() - start) * 1000  # Convert to ms

        assert elapsed < 50  # Should be <50ms
        assert len(result) > 0

    def test_sanitize_10kb_html_performance(self):
        """Test sanitizing 10KB of HTML."""
        import time
        sanitizer = ContentSanitizer(tier='C')
        html = '<p>Test content with some text</p>' * 200  # ~10KB

        start = time.time()
        result = sanitizer.sanitize_html(html)
        elapsed = (time.time() - start) * 1000

        assert elapsed < 100  # Should be <100ms (target is <50ms, but generous for CI)
        assert len(result) > 0
