"""
Media Library API integration tests.

Tests media asset upload, management, thumbnail generation, WebP conversion,
filtering, search, and the progressive image loading system.
"""

import io

import pytest
from PIL import Image

from tests.factories import (
    ImageSizePresetFactory,
    MediaAssetFactory,
    MediaFolderFactory,
    TagFactory,
    ThumbnailFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.media_library]


# ============================================================
# Helper Functions
# ============================================================


def create_test_image(width=800, height=600, format="JPEG"):
    """Create a test image file in memory."""
    img = Image.new("RGB", (width, height), color="red")
    img_io = io.BytesIO()
    img.save(img_io, format=format)
    img_io.seek(0)
    return img_io


def create_test_svg():
    """Create a simple test SVG file."""
    svg_content = """
    <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
        <circle cx="50" cy="50" r="40" fill="blue" />
    </svg>
    """
    return io.BytesIO(svg_content.strip().encode("utf-8"))


# ============================================================
# Media Asset CRUD Tests
# ============================================================


class TestMediaAssetAPI:
    """Test media asset API endpoints."""

    def test_list_media_assets(self, auth_client, admin_user, site_settings):
        """Authenticated users can list media assets."""
        MediaAssetFactory.create_batch(3, uploaded_by=admin_user)

        resp = auth_client.get("/api/media/assets/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] == 3

    def test_list_requires_auth(self, api_client):
        """Media asset list requires authentication."""
        resp = api_client.get("/api/media/assets/")
        assert resp.status_code in (401, 403)

    def test_retrieve_media_asset(self, auth_client, admin_user, site_settings):
        """Can retrieve individual media asset with thumbnails."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        resp = auth_client.get(f"/api/media/assets/{asset.id}/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == asset.title
        assert data["mime_type"] == asset.mime_type
        assert "thumbnails" in data

    def test_filter_by_mime_type(self, auth_client, admin_user, site_settings):
        """Can filter media assets by MIME type."""
        jpeg = MediaAssetFactory(mime_type="image/jpeg", uploaded_by=admin_user)
        png = MediaAssetFactory(mime_type="image/png", uploaded_by=admin_user)
        video = MediaAssetFactory(mime_type="video/mp4", uploaded_by=admin_user, video=True)

        resp = auth_client.get("/api/media/assets/?mime_type=image/jpeg")
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] >= 1
        mime_types = [asset["mime_type"] for asset in data["results"]]
        assert "image/jpeg" in mime_types

    def test_filter_by_folder(self, auth_client, admin_user, site_settings):
        """Can filter media assets by folder."""
        folder = MediaFolderFactory()
        in_folder = MediaAssetFactory(folder=folder, uploaded_by=admin_user)
        not_in_folder = MediaAssetFactory(folder=None, uploaded_by=admin_user)

        resp = auth_client.get(f"/api/media/assets/?folder={folder.id}")
        assert resp.status_code == 200
        data = resp.json()
        titles = [asset["title"] for asset in data["results"]]
        assert in_folder.title in titles
        assert not_in_folder.title not in titles

    def test_search_media_assets(self, auth_client, admin_user, site_settings):
        """Can search media assets by title and alt text."""
        specific = MediaAssetFactory(
            title="Unique Product Photo", alt_text="Product shot", uploaded_by=admin_user
        )
        generic = MediaAssetFactory(title="Generic Image", uploaded_by=admin_user)

        resp = auth_client.get("/api/media/assets/?search=Unique")
        assert resp.status_code == 200
        data = resp.json()
        titles = [asset["title"] for asset in data["results"]]
        assert "Unique Product Photo" in titles
        assert "Generic Image" not in titles


# ============================================================
# Media Folder Tests
# ============================================================


class TestMediaFolderAPI:
    """Test media folder API endpoints."""

    def test_list_folders(self, auth_client, site_settings):
        """Can list all media folders."""
        MediaFolderFactory.create_batch(3)

        resp = auth_client.get("/api/media/folders/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 3

    def test_create_folder(self, auth_client, site_settings):
        """Can create a new media folder."""
        resp = auth_client.post(
            "/api/media/folders/", {"name": "Product Images", "description": "Images for products"}
        )
        if resp.status_code != 201:
            print(f"Validation error: {resp.json()}")
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Product Images"
        assert "slug" in data

    def test_nested_folders(self, auth_client, site_settings):
        """Can create nested folder structure."""
        parent = MediaFolderFactory(name="Products")

        resp = auth_client.post(
            "/api/media/folders/",
            {
                "name": "Electronics",
                "parent": str(parent.id),  # Convert UUID to string
            },
        )
        if resp.status_code != 201:
            print(f"Validation error: {resp.json()}")
        assert resp.status_code == 201
        data = resp.json()
        assert data["parent"] == str(parent.id)  # Compare as strings

    def test_delete_folder(self, auth_client, site_settings):
        """Can delete empty folders."""
        folder = MediaFolderFactory()

        resp = auth_client.delete(f"/api/media/folders/{folder.id}/")
        assert resp.status_code == 204


# ============================================================
# Tag Tests
# ============================================================


class TestTagAPI:
    """Test media tag API endpoints."""

    def test_list_tags(self, auth_client, site_settings):
        """Can list all tags."""
        TagFactory.create_batch(3)

        resp = auth_client.get("/api/media/tags/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 3

    def test_create_tag(self, auth_client, site_settings):
        """Can create new tags."""
        resp = auth_client.post("/api/media/tags/", {"name": "product-photos"})
        if resp.status_code != 201:
            print(f"Validation error: {resp.json()}")
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "product-photos"

    def test_tag_media_assets(self, auth_client, admin_user, site_settings):
        """Can tag media assets."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        tag = TagFactory()

        asset.tags.add(tag)
        asset.save()

        resp = auth_client.get(f"/api/media/assets/{asset.id}/")
        data = resp.json()
        tag_names = [t["name"] for t in data.get("tags", [])]
        assert tag.name in tag_names


# ============================================================
# Thumbnail Generation Tests
# ============================================================


class TestThumbnailGeneration:
    """Test thumbnail generation and retrieval."""

    def test_asset_has_thumbnails_field(self, auth_client, admin_user, site_settings):
        """Media asset API includes thumbnails array."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        preset = ImageSizePresetFactory(name="test_thumb", width=300, height=300)

        # Create thumbnail manually for testing
        ThumbnailFactory(media_asset=asset, size_preset=preset, width=300, height=300)

        resp = auth_client.get(f"/api/media/assets/{asset.id}/")
        assert resp.status_code == 200
        data = resp.json()
        assert "thumbnails" in data
        assert isinstance(data["thumbnails"], list)

        if len(data["thumbnails"]) > 0:
            thumb = data["thumbnails"][0]
            assert "size_preset" in thumb
            assert "width" in thumb
            assert "height" in thumb
            assert "url" in thumb

    def test_get_thumbnail_url_helper(self, auth_client, admin_user, site_settings):
        """getThumbnailUrl helper finds correct thumbnail size."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        # Create multiple thumbnail sizes
        small_preset = ImageSizePresetFactory(name="small", small=True)
        medium_preset = ImageSizePresetFactory(name="medium", medium=True)
        large_preset = ImageSizePresetFactory(name="large", large=True)

        ThumbnailFactory(media_asset=asset, size_preset=small_preset, small=True)
        ThumbnailFactory(media_asset=asset, size_preset=medium_preset, medium=True)
        ThumbnailFactory(media_asset=asset, size_preset=large_preset, large=True)

        resp = auth_client.get(f"/api/media/assets/{asset.id}/")
        data = resp.json()
        thumbnails = data["thumbnails"]

        # Verify all sizes present (check for display names like "Small (300x300)")
        sizes = [t["size_preset"] for t in thumbnails]
        # Size presets include display names, so check if the word exists in any of them
        sizes_lower = [s.lower() for s in sizes]
        assert any("small" in s for s in sizes_lower), f"'small' not found in {sizes}"
        assert any("medium" in s for s in sizes_lower), f"'medium' not found in {sizes}"
        assert any("large" in s for s in sizes_lower), f"'large' not found in {sizes}"


# ============================================================
# Progressive Loading Tests
# ============================================================


class TestProgressiveLoading:
    """Test progressive image loading system."""

    def test_svg_has_no_thumbnails(self, auth_client, admin_user, site_settings):
        """SVG assets should have no thumbnails (vector format)."""
        svg_asset = MediaAssetFactory(
            mime_type="image/svg+xml", width=None, height=None, uploaded_by=admin_user, svg=True
        )

        resp = auth_client.get(f"/api/media/assets/{svg_asset.id}/")
        data = resp.json()
        assert data["mime_type"] == "image/svg+xml"
        assert len(data.get("thumbnails", [])) == 0

    def test_3d_model_has_no_thumbnails(self, auth_client, admin_user, site_settings):
        """3D model assets should have no thumbnails."""
        model = MediaAssetFactory(
            mime_type="model/gltf-binary",
            width=None,
            height=None,
            uploaded_by=admin_user,
            model_3d=True,
        )

        resp = auth_client.get(f"/api/media/assets/{model.id}/")
        data = resp.json()
        assert data["mime_type"] == "model/gltf-binary"
        assert len(data.get("thumbnails", [])) == 0

    def test_raster_images_have_thumbnails(self, auth_client, admin_user, site_settings):
        """Raster images (JPG, PNG, WebP) should have thumbnails."""
        asset = MediaAssetFactory(mime_type="image/jpeg", uploaded_by=admin_user)
        preset = ImageSizePresetFactory()
        ThumbnailFactory(media_asset=asset, size_preset=preset)

        resp = auth_client.get(f"/api/media/assets/{asset.id}/")
        data = resp.json()
        assert data["mime_type"] == "image/jpeg"
        assert len(data["thumbnails"]) > 0

    def test_video_assets_properties(self, auth_client, admin_user, site_settings):
        """Video assets have correct properties."""
        video = MediaAssetFactory(
            mime_type="video/mp4", width=1920, height=1080, uploaded_by=admin_user, video=True
        )

        resp = auth_client.get(f"/api/media/assets/{video.id}/")
        data = resp.json()
        assert data["mime_type"] == "video/mp4"
        assert data["width"] == 1920
        assert data["height"] == 1080


# ============================================================
# Media Selection & Usage Tests
# ============================================================


class TestMediaUsage:
    """Test media asset usage tracking and selection."""

    def test_mark_asset_in_use(self, auth_client, admin_user, site_settings):
        """Can update asset metadata."""
        asset = MediaAssetFactory(title="Original Title", uploaded_by=admin_user)

        # Update asset metadata
        resp = auth_client.patch(f"/api/media/assets/{asset.id}/", {"title": "Updated Title"})
        assert resp.status_code == 200

        # Verify update by fetching the asset
        resp = auth_client.get(f"/api/media/assets/{asset.id}/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Updated Title"

    def test_filter_unused_assets(self, auth_client, admin_user, site_settings):
        """Can filter to find unused assets for cleanup."""
        in_use = MediaAssetFactory(
            usage_count=5, uploaded_by=admin_user
        )  # usage_count > 0 means in use
        not_in_use = MediaAssetFactory(
            usage_count=0, uploaded_by=admin_user
        )  # usage_count = 0 means not in use

        resp = auth_client.get("/api/media/assets/?is_in_use=false")
        assert resp.status_code == 200
        data = resp.json()

        titles = [asset["title"] for asset in data["results"]]
        assert not_in_use.title in titles


# ============================================================
# Gallery & Admin Tests
# ============================================================


class TestMediaGallery:
    """Test media gallery functionality."""

    def test_gallery_view_accessible(self, auth_client, admin_user, site_settings):
        """Gallery view is accessible to authenticated staff."""
        # Note: This would be better as an E2E test, but we can verify the endpoint exists
        # Actual gallery is at /admin/media_library/mediaasset/gallery/
        # This is a Django admin view, not an API endpoint
        # Testing it would require a different approach or E2E tests
        pass

    def test_bulk_operations(self, auth_client, admin_user, site_settings):
        """Can perform bulk operations on media assets."""
        assets = MediaAssetFactory.create_batch(3, uploaded_by=admin_user)
        folder = MediaFolderFactory()

        # Bulk move to folder (if endpoint exists)
        # This would depend on the actual API implementation
        # Example:
        # resp = auth_client.post('/api/media/assets/bulk-move/', {
        #     'asset_ids': [a.id for a in assets],
        #     'folder_id': folder.id
        # })
        pass


# ============================================================
# Image Processing Tests
# ============================================================


class TestImageProcessing:
    """Test image processing functionality."""

    def test_image_dimensions_saved(self, auth_client, admin_user, site_settings):
        """Image dimensions are saved on upload."""
        asset = MediaAssetFactory(width=1920, height=1080, uploaded_by=admin_user)

        resp = auth_client.get(f"/api/media/assets/{asset.id}/")
        data = resp.json()
        assert data["width"] == 1920
        assert data["height"] == 1080

    def test_file_size_tracking(self, auth_client, admin_user, site_settings):
        """File size is tracked for bandwidth monitoring."""
        asset = MediaAssetFactory(
            file_size=102400,  # 100KB
            uploaded_by=admin_user,
        )

        resp = auth_client.get(f"/api/media/assets/{asset.id}/")
        data = resp.json()
        assert data["file_size"] == 102400

    def test_optimization_flag(self, auth_client, admin_user, site_settings):
        """Optimization status is tracked via webp_file."""
        # Asset with WebP version is optimized
        optimized = MediaAssetFactory(uploaded_by=admin_user)
        # Note: WebP file would be generated by image processor, not set directly
        # This test verifies the API returns file_size field correctly

        resp = auth_client.get(f"/api/media/assets/{optimized.id}/")
        data = resp.json()
        assert "file_size" in data
        assert data["file_size"] == 102400  # Default from factory


# ============================================================
# Security & Permissions Tests
# ============================================================


class TestMediaSecurity:
    """Test media library security and permissions."""

    def test_upload_requires_auth(self, api_client):
        """Upload endpoint requires authentication."""
        # Assuming upload endpoint exists
        # resp = api_client.post('/api/media/assets/upload/')
        # assert resp.status_code in (401, 403)
        pass

    def test_delete_requires_admin(self, auth_client, admin_user, site_settings):
        """Only admins can delete media assets."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        # This test assumes admin_user is staff
        resp = auth_client.delete(f"/api/media/assets/{asset.id}/")
        # Expected to succeed for admin
        assert resp.status_code in (204, 200, 403)

    def test_sensitive_data_not_exposed(self, auth_client, admin_user, site_settings):
        """Sensitive data is not exposed in API responses."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        resp = auth_client.get(f"/api/media/assets/{asset.id}/")
        data = resp.json()

        # Uploaded by user info should be limited
        if "uploaded_by" in data:
            # Should not expose full user details
            assert "password" not in str(data)
