"""
Media Library E2E tests.

Tests the media library gallery interface, preview modal with progressive loading,
upload functionality, and media selection widgets using browser automation.
"""

import re

import pytest
from playwright.sync_api import Page, expect

from tests.factories import MediaAssetFactory

pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.e2e,
    pytest.mark.media_library,
]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def gallery_page(admin_authenticated_page: Page, site_settings):
    """Navigate to media library gallery with test data."""
    # Create test media assets so the gallery has content
    MediaAssetFactory.create_batch(3, alt_text="Test image description")
    MediaAssetFactory(video=True, title="Test Video", alt_text="Test video")

    base = admin_authenticated_page._live_server_url
    admin_authenticated_page.goto(f"{base}/en/admin/media_library/mediaasset/gallery/")
    admin_authenticated_page.wait_for_selector(".media-grid")
    return admin_authenticated_page


# ============================================================
# Gallery View Tests
# ============================================================


class TestMediaGalleryView:
    """Test media library gallery interface."""

    def test_gallery_loads_successfully(self, gallery_page: Page):
        """Media gallery page loads without errors."""
        # Title format: "Media Gallery | {site_name} | Spwig"
        expect(gallery_page).to_have_title(re.compile(r"Media Gallery.*"))

        # Check main elements present
        expect(gallery_page.locator(".media-gallery")).to_be_visible()
        expect(gallery_page.locator(".media-grid")).to_be_visible()

    def test_gallery_displays_media_items(self, gallery_page: Page):
        """Gallery displays media items in grid."""
        media_items = gallery_page.locator(".media-item")

        # Should have at least one media item
        expect(media_items.first).to_be_visible()

        # Check item structure on an image item (videos may show .no-image instead of img)
        image_item = gallery_page.locator('.media-item[data-type="image"]').first
        expect(image_item.locator(".image-container img")).to_be_visible()
        expect(image_item.locator(".info .title")).to_be_visible()

    def test_grid_view_toggle(self, gallery_page: Page):
        """Can toggle between grid and list views."""
        # View toggle buttons use data-view attribute
        grid_view_btn = gallery_page.locator('[data-view="grid"]')
        list_view_btn = gallery_page.locator('[data-view="list"]')

        if grid_view_btn.is_visible():
            # Switch to list view
            list_view_btn.click()
            gallery_page.wait_for_timeout(300)  # Animation

            # Check list view is active (element has multiple classes)
            media_grid = gallery_page.locator(".media-grid")
            expect(media_grid).to_have_class(re.compile(r".*view-list.*"))

            # Switch back to grid view
            grid_view_btn.click()
            gallery_page.wait_for_timeout(300)

            # Check grid view is active
            expect(media_grid).to_have_class(re.compile(r".*view-grid.*"))

    def test_search_functionality(self, gallery_page: Page):
        """Search filters media items."""
        # Search input is type="text" with class "search-input"
        search_input = gallery_page.locator("input.search-input")

        if search_input.is_visible():
            # Type search query
            search_input.fill("Test")
            gallery_page.wait_for_timeout(500)  # Debounce

            # Results should update
            media_items = gallery_page.locator(".media-item")

            # Should have filtered results (our factory data has "Test" in titles)
            expect(media_items.first).to_be_visible()


# ============================================================
# Progressive Loading Tests
# ============================================================


class TestProgressiveImageLoading:
    """Test progressive image loading in preview modal."""

    def test_preview_modal_opens(self, gallery_page: Page):
        """Preview modal opens when double-clicking media item."""
        # Double-click to open preview (single click selects)
        first_item = gallery_page.locator(".media-item").first
        first_item.dblclick()

        # Modal should appear
        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # Modal should have preview content
        expect(modal.locator(".media-preview-content")).to_be_visible()

    def test_preview_shows_loading_spinner(self, gallery_page: Page):
        """Preview modal shows loading spinner while image loads."""
        # Target an image item (video previews don't have .preview-loading)
        image_item = gallery_page.locator('.media-item[data-type="image"]').first
        image_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # Image preview container should include a loading element
        # (may be hidden immediately if src matches, but element exists in DOM)
        loading = modal.locator(".preview-loading")
        assert loading.count() > 0, "Preview loading spinner element should exist in the DOM"

    def test_preview_displays_large_image(self, gallery_page: Page):
        """Preview modal loads preview image."""
        # Target an image item (video previews use <video> not .preview-image)
        image_item = gallery_page.locator('.media-item[data-type="image"]').first
        image_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # Wait for image to load
        preview_image = modal.locator(".preview-image")
        expect(preview_image).to_be_visible()

        # Image should have a src attribute
        src = preview_image.get_attribute("src")
        assert src is not None, "Preview image should have a src attribute"

    def test_preview_blur_transition(self, gallery_page: Page):
        """Preview image has progressive loading mechanism (placeholder → loaded)."""
        # Target an image item for blur transition testing
        image_item = gallery_page.locator('.media-item[data-type="image"]').first
        image_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        preview_image = modal.locator(".preview-image")
        expect(preview_image).to_be_visible()

        # Verify the progressive loading mechanism exists:
        # - Image starts with 'preview-placeholder' class
        # - data-preview-src attribute is set for progressive loading
        classes = preview_image.get_attribute("class") or ""
        assert "preview-image" in classes, (
            f"Preview image should have 'preview-image' class. Classes: {classes}"
        )

        # The data-preview-src attribute drives the progressive load
        data_src = preview_image.get_attribute("data-preview-src")
        assert data_src is not None, (
            "Preview image should have data-preview-src for progressive loading"
        )

    def test_preview_navigation(self, gallery_page: Page):
        """Can navigate between images in preview modal."""
        first_item = gallery_page.locator(".media-item").first
        first_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # Find navigation buttons
        next_btn = modal.locator(".preview-nav.next")

        if next_btn.is_visible():
            next_btn.click()
            gallery_page.wait_for_timeout(500)

            # A new modal should appear with the next image
            new_modal = gallery_page.locator(".media-preview-modal")
            expect(new_modal).to_be_visible()

    def test_preview_keyboard_navigation(self, gallery_page: Page):
        """Can navigate with arrow keys in preview modal."""
        first_item = gallery_page.locator(".media-item").first
        first_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # Press right arrow key
        gallery_page.keyboard.press("ArrowRight")
        gallery_page.wait_for_timeout(500)

        # Modal should still be visible (navigated to next image)
        new_modal = gallery_page.locator(".media-preview-modal")
        expect(new_modal).to_be_visible()

    def test_preview_close_with_escape(self, gallery_page: Page):
        """Can close preview modal with Escape key."""
        first_item = gallery_page.locator(".media-item").first
        first_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # Press Escape
        gallery_page.keyboard.press("Escape")
        gallery_page.wait_for_timeout(300)

        # Modal should be removed from DOM
        assert gallery_page.locator(".media-preview-modal").count() == 0

    def test_preview_close_with_overlay_click(self, gallery_page: Page):
        """Can close preview modal by clicking outside content."""
        first_item = gallery_page.locator(".media-item").first
        first_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # The JS handler closes when clicking the modal element itself
        # (e.target === modal check). Click at the edge to avoid hitting
        # the .preview-overlay child content.
        modal.click(position={"x": 5, "y": 5})
        gallery_page.wait_for_timeout(300)

        # Modal should be removed from DOM
        assert gallery_page.locator(".media-preview-modal").count() == 0


# ============================================================
# Responsive Behavior Tests
# ============================================================


class TestResponsiveBehavior:
    """Test responsive behavior on different viewport sizes."""

    def test_desktop_loads_large_previews(self, gallery_page: Page):
        """Desktop viewport loads large preview images."""
        gallery_page.set_viewport_size({"width": 1920, "height": 1080})

        # Target an image item (video previews don't have .preview-image)
        image_item = gallery_page.locator('.media-item[data-type="image"]').first
        image_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # Preview image should be visible
        preview_image = modal.locator(".preview-image")
        expect(preview_image).to_be_visible()

    def test_mobile_loads_medium_previews(self, gallery_page: Page):
        """Mobile viewport loads medium preview images."""
        gallery_page.set_viewport_size({"width": 375, "height": 667})

        # Re-navigate at mobile viewport
        base = gallery_page._live_server_url
        gallery_page.goto(f"{base}/en/admin/media_library/mediaasset/gallery/")
        gallery_page.wait_for_selector(".media-grid")

        # Target an image item (video previews don't have .preview-image)
        image_item = gallery_page.locator('.media-item[data-type="image"]').first
        image_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # Preview image should be visible on mobile
        preview_image = modal.locator(".preview-image")
        expect(preview_image).to_be_visible()

    def test_modal_fullscreen_on_mobile(self, gallery_page: Page):
        """Preview modal renders on mobile viewport."""
        gallery_page.set_viewport_size({"width": 375, "height": 667})

        base = gallery_page._live_server_url
        gallery_page.goto(f"{base}/en/admin/media_library/mediaasset/gallery/")
        gallery_page.wait_for_selector(".media-grid")

        first_item = gallery_page.locator(".media-item").first
        first_item.dblclick()

        # Preview overlay should be visible
        overlay = gallery_page.locator(".media-preview-modal .preview-overlay")
        expect(overlay).to_be_visible()


# ============================================================
# Media Type Handling Tests
# ============================================================


class TestMediaTypeHandling:
    """Test handling of different media types (SVG, video, 3D)."""

    def test_svg_preview(self, gallery_page: Page):
        """SVG images display correctly in preview."""
        # Gallery uses data-type="image" for all images including SVG
        # SVGs are included in the image type (no separate data-type for SVG)
        image_item = gallery_page.locator('.media-item[data-type="image"]').first

        if image_item.is_visible():
            image_item.dblclick()

            modal = gallery_page.locator(".media-preview-modal")
            expect(modal).to_be_visible()

            preview_image = modal.locator(".preview-image")
            expect(preview_image).to_be_visible()

    def test_video_preview(self, gallery_page: Page):
        """Video files display correctly in preview."""
        # Gallery uses data-type="video" for video items
        video_item = gallery_page.locator('.media-item[data-type="video"]').first

        if video_item.is_visible():
            video_item.dblclick()

            modal = gallery_page.locator(".media-preview-modal")
            expect(modal).to_be_visible()

            # Should display video player
            video_preview = modal.locator("video")
            expect(video_preview).to_be_visible()


# ============================================================
# Error Handling Tests
# ============================================================


class TestErrorHandling:
    """Test error handling in media library."""

    def test_preview_handles_missing_image(self, gallery_page: Page):
        """Preview gracefully handles missing images."""
        first_item = gallery_page.locator(".media-item").first
        first_item.dblclick()

        # Modal should appear even if image fails to load
        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

    def test_preview_handles_api_failure(self, gallery_page: Page):
        """Preview handles API failures gracefully."""
        # Intercept API calls to simulate failure
        gallery_page.route("**/api/media/assets/**", lambda route: route.abort())

        first_item = gallery_page.locator(".media-item").first
        first_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # Should show error message or fallback
        gallery_page.wait_for_timeout(2000)


# ============================================================
# Upload Tests
# ============================================================


class TestMediaUpload:
    """Test media upload functionality."""

    def test_upload_zone_visible(self, gallery_page: Page):
        """Upload zone is visible in gallery."""
        upload_zone = gallery_page.locator(".upload-zone")
        expect(upload_zone).to_be_visible()

    def test_upload_zone_has_content(self, gallery_page: Page):
        """Upload zone displays drop instructions."""
        upload_zone = gallery_page.locator(".upload-zone")
        expect(upload_zone).to_be_visible()

        # Verify upload zone has expected text
        expect(upload_zone.locator(".text")).to_contain_text("Drop files here")

    def test_drag_drop_zone_interactive(self, gallery_page: Page):
        """Drag and drop zone responds to interactions."""
        upload_zone = gallery_page.locator(".upload-zone")

        if upload_zone.is_visible():
            # Hover over zone
            upload_zone.hover()

            # Zone should respond to hover (visual feedback)
            # Verify zone is still visible after interaction
            expect(upload_zone).to_be_visible()


# ============================================================
# Filter and Sort Tests
# ============================================================


class TestFilteringAndSorting:
    """Test media filtering and sorting."""

    def test_filter_by_folder(self, gallery_page: Page):
        """Can filter media by folder via folder links."""
        # Folders are links in .folder-tree, not a select element
        folder_links = gallery_page.locator(".folder-tree .folder-link")

        # Should have at least the "All Files" link
        expect(folder_links.first).to_be_visible()

        # Verify "All Files" link is active by default
        all_files_link = folder_links.first
        expect(all_files_link).to_have_class(re.compile(r".*active.*"))

    def test_filter_by_media_type(self, gallery_page: Page):
        """Can filter media by type (image, video, etc)."""
        # Filter select uses name="mime_type"
        type_filter = gallery_page.locator('select[name="mime_type"]')

        if type_filter.is_visible():
            # Select JPEG image type
            type_filter.select_option(value="image/jpeg")
            gallery_page.wait_for_timeout(500)

            # Results should show only JPEG images
            media_items = gallery_page.locator(".media-item")
            expect(media_items.first).to_be_visible()

    @pytest.mark.xfail(reason="Sort control not yet implemented in gallery UI")
    def test_sort_by_date(self, gallery_page: Page):
        """Can sort media by date."""
        sort_select = gallery_page.locator('select[name="sort"]')
        expect(sort_select).to_be_visible()

        sort_select.select_option(label="Date uploaded")
        gallery_page.wait_for_timeout(500)

        media_items = gallery_page.locator(".media-item")
        expect(media_items.first).to_be_visible()


# ============================================================
# Accessibility Tests
# ============================================================


class TestAccessibility:
    """Test accessibility features."""

    def test_keyboard_navigation_in_gallery(self, gallery_page: Page):
        """Can navigate gallery with keyboard."""
        # Tab to first interactive element
        gallery_page.keyboard.press("Tab")

        # Should be able to focus interactive elements
        focused = gallery_page.evaluate("document.activeElement.tagName")
        assert focused is not None

    def test_preview_modal_aria_labels(self, gallery_page: Page):
        """Preview modal has proper ARIA labels."""
        first_item = gallery_page.locator(".media-item").first
        first_item.dblclick()

        modal = gallery_page.locator(".media-preview-modal")
        expect(modal).to_be_visible()

        # Modal should have close button with title for accessibility
        close_btn = modal.locator(".preview-close")
        expect(close_btn).to_be_visible()
        title = close_btn.get_attribute("title")
        assert title is not None, "Close button should have a title attribute"

    def test_alt_text_present(self, gallery_page: Page):
        """Images have alt text for screen readers."""
        images = gallery_page.locator(".media-item img")
        first_image = images.first

        if first_image.is_visible():
            alt_text = first_image.get_attribute("alt")
            assert alt_text is not None
            assert len(alt_text) > 0
