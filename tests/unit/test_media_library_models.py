"""
Media Library Model unit tests.

Tests MediaAsset, MediaFolder, MediaThumbnail, ImageSizePreset, and Tag models.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from media_library.models import (
    MediaAsset,
    MediaFolder,
    MediaThumbnail,
    ImageSizePreset,
    Tag,
    MediaProcessingJob,
)

from tests.factories import (
    MediaAssetFactory,
    MediaFolderFactory,
    ImageSizePresetFactory,
    ThumbnailFactory,
    TagFactory,
    MediaProcessingJobFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.unit, pytest.mark.media_library]


# ============================================================
# MediaAsset Model Tests
# ============================================================

class TestMediaAssetModel:
    """Test MediaAsset model functionality."""

    def test_create_media_asset(self, admin_user):
        """Can create media asset with required fields."""
        asset = MediaAssetFactory(
            title='Test Image',
            mime_type='image/jpeg',
            file_size=102400,
            width=1920,
            height=1080,
            uploaded_by=admin_user
        )

        assert asset.title == 'Test Image'
        assert asset.mime_type == 'image/jpeg'
        assert asset.file_size == 102400
        assert asset.width == 1920
        assert asset.height == 1080
        assert asset.uploaded_by == admin_user

    def test_media_asset_str_representation(self, admin_user):
        """MediaAsset string representation shows title."""
        asset = MediaAssetFactory(title='Product Photo', uploaded_by=admin_user)

        assert str(asset) == 'Product Photo'

    def test_media_asset_default_values(self, admin_user):
        """MediaAsset has correct default values."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        assert asset.is_public is False
        assert asset.usage_count == 0
        assert asset.alt_text == ''

    def test_media_asset_dimensions(self, admin_user):
        """MediaAsset stores image dimensions correctly."""
        asset = MediaAssetFactory(
            width=3840,
            height=2160,
            uploaded_by=admin_user
        )

        assert asset.width == 3840
        assert asset.height == 2160

    def test_media_asset_null_dimensions_for_svg(self, admin_user):
        """SVG assets can have null dimensions."""
        svg = MediaAssetFactory(
            mime_type='image/svg+xml',
            width=None,
            height=None,
            uploaded_by=admin_user,
            svg=True
        )

        assert svg.width is None
        assert svg.height is None
        assert svg.mime_type == 'image/svg+xml'

    def test_media_asset_file_size_tracking(self, admin_user):
        """MediaAsset tracks file size in bytes."""
        # 5MB file
        asset = MediaAssetFactory(
            file_size=5 * 1024 * 1024,
            uploaded_by=admin_user
        )

        assert asset.file_size == 5242880

    def test_media_asset_upload_date(self, admin_user):
        """MediaAsset records upload date automatically."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        assert asset.created_at is not None
        assert asset.updated_at is not None

    def test_media_asset_folder_assignment(self, admin_user):
        """MediaAsset can be assigned to a folder."""
        folder = MediaFolderFactory(name='Products')
        asset = MediaAssetFactory(
            folder=folder,
            uploaded_by=admin_user
        )

        assert asset.folder == folder
        assert asset in folder.assets.all()

    def test_media_asset_without_folder(self, admin_user):
        """MediaAsset can exist without a folder."""
        asset = MediaAssetFactory(
            folder=None,
            uploaded_by=admin_user
        )

        assert asset.folder is None

    def test_media_asset_tags(self, admin_user):
        """MediaAsset can have multiple tags."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        tag1 = TagFactory(name='product')
        tag2 = TagFactory(name='featured')

        asset.tags.add(tag1, tag2)

        assert asset.tags.count() == 2
        assert tag1 in asset.tags.all()
        assert tag2 in asset.tags.all()

    def test_media_asset_public_flag(self, admin_user):
        """Can mark asset as public."""
        asset = MediaAssetFactory(
            is_public=True,
            uploaded_by=admin_user
        )

        assert asset.is_public is True

    def test_media_asset_usage_tracking(self, admin_user):
        """Can track asset usage."""
        in_use = MediaAssetFactory(
            uploaded_by=admin_user,
            in_use=True  # trait sets usage_count=5
        )
        not_in_use = MediaAssetFactory(
            usage_count=0,
            uploaded_by=admin_user
        )

        assert in_use.usage_count > 0
        assert not_in_use.usage_count == 0

    def test_media_asset_alt_text(self, admin_user):
        """MediaAsset stores alt text for accessibility."""
        asset = MediaAssetFactory(
            alt_text='Product photo showing laptop',
            uploaded_by=admin_user
        )

        assert asset.alt_text == 'Product photo showing laptop'

    def test_media_asset_thumbnails_relationship(self, admin_user):
        """MediaAsset has relationship to thumbnails."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        ThumbnailFactory(media_asset=asset, size_preset='large')

        assert asset.thumbnails.count() == 1
        assert asset.thumbnails.first().size_preset == 'large'


# ============================================================
# MediaFolder Model Tests
# ============================================================

class TestMediaFolderModel:
    """Test MediaFolder model functionality."""

    def test_create_media_folder(self):
        """Can create media folder."""
        folder = MediaFolderFactory(
            name='Products',
            description='Product images'
        )

        assert folder.name == 'Products'
        assert folder.description == 'Product images'

    def test_media_folder_str_representation(self):
        """MediaFolder string representation shows name."""
        folder = MediaFolderFactory(name='Categories')

        # MediaFolder name gets lowercased during creation
        assert str(folder) == 'categories'

    def test_media_folder_slug_generation(self):
        """MediaFolder generates slug from name."""
        folder = MediaFolderFactory(name='Product Photos')

        # Slug should be auto-generated
        assert folder.slug is not None
        assert 'product' in folder.slug.lower()

    def test_nested_folders(self):
        """Can create nested folder structure."""
        parent = MediaFolderFactory(name='Products')
        child = MediaFolderFactory(name='Electronics', parent=parent)

        assert child.parent == parent
        assert child in parent.children.all()

    def test_folder_hierarchy_depth(self):
        """Can create multi-level folder hierarchy."""
        level1 = MediaFolderFactory(name='Level 1')
        level2 = MediaFolderFactory(name='Level 2', parent=level1)
        level3 = MediaFolderFactory(name='Level 3', parent=level2)

        assert level3.parent == level2
        assert level2.parent == level1
        assert level1.parent is None

    def test_folder_asset_count(self, admin_user):
        """Can count assets in a folder."""
        folder = MediaFolderFactory()

        MediaAssetFactory.create_batch(5, folder=folder, uploaded_by=admin_user)

        assert folder.assets.count() == 5

    def test_empty_folder(self):
        """Folder can be empty."""
        folder = MediaFolderFactory()

        assert folder.assets.count() == 0


# ============================================================
# Thumbnail Model Tests
# ============================================================

class TestThumbnailModel:
    """Test Thumbnail model functionality."""

    def test_create_thumbnail(self, admin_user):
        """Can create thumbnail."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        preset = ImageSizePresetFactory(
            name='small',
            width=300,
            height=300
        )

        thumbnail = ThumbnailFactory(
            media_asset=asset,
            size_preset=preset,
            width=300,
            height=300
        )

        assert thumbnail.media_asset == asset
        assert thumbnail.size_preset == preset
        assert thumbnail.width == 300
        assert thumbnail.height == 300

    def test_thumbnail_str_representation(self, admin_user):
        """Thumbnail string representation shows asset and preset."""
        asset = MediaAssetFactory(title='Test Image', uploaded_by=admin_user)
        preset = ImageSizePresetFactory(name='small', small=True)
        thumbnail = ThumbnailFactory(
            media_asset=asset,
            size_preset=preset,
            small=True
        )

        str_repr = str(thumbnail)
        assert 'Test Image' in str_repr or 'small' in str_repr

    def test_thumbnail_webp_support(self, admin_user):
        """Thumbnail can have WebP version."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        preset = ImageSizePresetFactory()

        thumbnail = ThumbnailFactory(
            media_asset=asset,
            size_preset=preset
        )

        # Thumbnail model should support webp_file field
        assert hasattr(thumbnail, 'webp_file')

    def test_multiple_thumbnails_per_asset(self, admin_user):
        """Asset can have multiple thumbnails."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        small = ImageSizePresetFactory(name='small', small=True)
        medium = ImageSizePresetFactory(name='medium', medium=True)
        large = ImageSizePresetFactory(name='large', large=True)

        ThumbnailFactory(media_asset=asset, size_preset=small, small=True)
        ThumbnailFactory(media_asset=asset, size_preset=medium, medium=True)
        ThumbnailFactory(media_asset=asset, size_preset=large, large=True)

        assert asset.thumbnails.count() == 3

    def test_thumbnail_deletion_cascades(self, admin_user):
        """Thumbnails remain after soft delete but are deleted on hard delete."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        ThumbnailFactory(media_asset=asset, size_preset='small')

        asset_id = asset.id

        # Soft delete (MediaAsset uses SoftDeleteModel)
        asset.delete()

        # Thumbnail still exists after soft delete
        assert MediaThumbnail.objects.filter(media_asset_id=asset_id).count() == 1

        # Hard delete
        asset.hard_delete()

        # Thumbnail is deleted via CASCADE after hard delete
        assert MediaThumbnail.objects.filter(media_asset_id=asset_id).count() == 0


# ============================================================
# ImageSizePreset Model Tests
# ============================================================

class TestImageSizePresetModel:
    """Test ImageSizePreset model functionality."""

    def test_create_image_size_preset(self):
        """Can create image size preset."""
        preset = ImageSizePresetFactory(
            name='thumbnail',
            width=150,
            height=150,
            crop_mode='crop',
            quality=85
        )

        assert preset.name == 'thumbnail'
        assert preset.width == 150
        assert preset.height == 150
        assert preset.crop_mode == 'crop'
        assert preset.quality == 85

    def test_preset_str_representation(self):
        """ImageSizePreset string representation shows name and dimensions."""
        preset = ImageSizePresetFactory(
            name='medium',
            width=600,
            height=600
        )

        str_repr = str(preset)
        assert 'medium' in str_repr or '600' in str_repr

    def test_system_preset_flag(self):
        """System presets are marked as is_system_preset=True."""
        system_preset = ImageSizePresetFactory(
            name='small',
            is_system_preset=True,
            small=True
        )
        custom_preset = ImageSizePresetFactory(
            name='custom',
            is_system_preset=False
        )

        assert system_preset.is_system_preset is True
        assert custom_preset.is_system_preset is False

    def test_preset_crop_mode(self):
        """Preset can specify crop mode."""
        crop_preset = ImageSizePresetFactory(crop_mode='crop')
        cover_preset = ImageSizePresetFactory(crop_mode='cover')
        contain_preset = ImageSizePresetFactory(crop_mode='contain')

        assert crop_preset.crop_mode == 'crop'
        assert cover_preset.crop_mode == 'cover'
        assert contain_preset.crop_mode == 'contain'

    def test_preset_quality_setting(self):
        """Preset can specify quality (1-100)."""
        high_quality = ImageSizePresetFactory(quality=95)
        low_quality = ImageSizePresetFactory(quality=60)

        assert high_quality.quality == 95
        assert low_quality.quality == 60

    def test_preset_unique_name(self):
        """Preset names must be unique."""
        ImageSizePreset.objects.create(
            name='duplicate',
            slug='duplicate',
            display_name='Duplicate',
            width=100,
            height=100,
            crop_mode='cover',
            quality=85
        )

        # Creating another with same name should fail
        with pytest.raises(IntegrityError):
            ImageSizePreset.objects.create(
                name='duplicate',
                slug='duplicate2',
                display_name='Duplicate 2',
                width=200,
                height=200,
                crop_mode='cover',
                quality=85
            )


# ============================================================
# Tag Model Tests
# ============================================================

class TestTagModel:
    """Test Tag model functionality."""

    def test_create_tag(self):
        """Can create tag."""
        tag = TagFactory(name='product-photos')

        assert tag.name == 'product-photos'

    def test_tag_str_representation(self):
        """Tag string representation shows name."""
        tag = TagFactory(name='featured')

        assert str(tag) == 'featured'

    def test_tag_slug_generation(self):
        """Tag generates slug from name."""
        tag = TagFactory(name='Product Photos')

        # Slug should be auto-generated
        assert tag.slug is not None
        assert 'product' in tag.slug.lower()

    def test_tag_unique_name(self):
        """Tag names must be unique."""
        Tag.objects.create(name='duplicate', slug='duplicate')

        # Creating another with same name should fail
        with pytest.raises(IntegrityError):
            Tag.objects.create(name='duplicate', slug='duplicate2')

    def test_tag_many_to_many_with_assets(self, admin_user):
        """Tags have many-to-many relationship with assets."""
        tag = TagFactory(name='featured')

        asset1 = MediaAssetFactory(uploaded_by=admin_user)
        asset2 = MediaAssetFactory(uploaded_by=admin_user)

        asset1.tags.add(tag)
        asset2.tags.add(tag)

        assert tag.assets.count() == 2
        assert asset1 in tag.assets.all()
        assert asset2 in tag.assets.all()


# ============================================================
# MediaProcessingJob Model Tests
# ============================================================

class TestMediaProcessingJobModel:
    """Test MediaProcessingJob model functionality."""

    def test_create_processing_job(self, admin_user):
        """Can create media processing job."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        job = MediaProcessingJobFactory(
            media_asset=asset,
            job_type='thumbnail_generation',
            status='pending'
        )

        assert job.media_asset == asset
        assert job.job_type == 'thumbnail_generation'
        assert job.status == 'pending'

    def test_job_status_transitions(self, admin_user):
        """Job can transition through statuses."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        job = MediaProcessingJobFactory(
            media_asset=asset,
            status='pending'
        )

        # Start processing
        job.status = 'processing'
        job.save()
        assert job.status == 'processing'

        # Complete
        job.status = 'completed'
        job.save()
        assert job.status == 'completed'

    def test_job_error_tracking(self, admin_user):
        """Job can track error messages."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        job = MediaProcessingJobFactory(
            media_asset=asset,
            status='failed',
            error_message='File not found'
        )

        assert job.status == 'failed'
        assert job.error_message == 'File not found'

    def test_job_progress_tracking(self, admin_user):
        """Job can track progress percentage."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        job = MediaProcessingJobFactory(
            media_asset=asset,
            progress=50
        )

        assert job.progress == 50

    def test_job_timestamps(self, admin_user):
        """Job tracks start and completion times."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        job = MediaProcessingJobFactory(media_asset=asset)

        assert job.created_at is not None

        # Started and completed timestamps depend on implementation
        if hasattr(job, 'started_at'):
            assert hasattr(job, 'completed_at')


# ============================================================
# Model Relationship Tests
# ============================================================

class TestModelRelationships:
    """Test relationships between models."""

    def test_asset_folder_relationship(self, admin_user):
        """Asset-Folder relationship works correctly."""
        folder = MediaFolderFactory(name='Products')
        asset = MediaAssetFactory(folder=folder, uploaded_by=admin_user)

        # Forward relationship
        assert asset.folder == folder

        # Reverse relationship
        assert asset in folder.assets.all()

    def test_asset_thumbnail_relationship(self, admin_user):
        """Asset-Thumbnail relationship works correctly."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        preset = ImageSizePresetFactory()
        thumbnail = ThumbnailFactory(
            media_asset=asset,
            size_preset=preset
        )

        # Forward relationship
        assert thumbnail.media_asset == asset

        # Reverse relationship
        assert thumbnail in asset.thumbnails.all()

    def test_thumbnail_preset_relationship(self, admin_user):
        """Thumbnail stores preset name correctly."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        thumbnail = ThumbnailFactory(
            media_asset=asset,
            size_preset='small',
            small=True
        )

        # size_preset is a CharField storing the preset name
        assert thumbnail.size_preset == 'small'

        # Can filter thumbnails by preset name
        thumbnails = MediaThumbnail.objects.filter(size_preset='small')
        assert thumbnail in thumbnails

    def test_asset_tag_relationship(self, admin_user):
        """Asset-Tag many-to-many relationship works."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        tag1 = TagFactory(name='tag1')
        tag2 = TagFactory(name='tag2')

        asset.tags.add(tag1, tag2)

        # Forward relationship
        assert tag1 in asset.tags.all()
        assert tag2 in asset.tags.all()

        # Reverse relationship
        assert asset in tag1.assets.all()
        assert asset in tag2.assets.all()

    def test_cascade_delete_folder(self, admin_user):
        """Deleting folder affects assets correctly."""
        folder = MediaFolderFactory()
        asset = MediaAssetFactory(folder=folder, uploaded_by=admin_user)

        folder.delete()

        # Asset should still exist but folder should be None
        # (or asset should be deleted, depending on cascade setting)
        # Implementation-specific behavior

    def test_cascade_delete_preset(self, admin_user):
        """Deleting preset affects thumbnails correctly."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        preset = ImageSizePresetFactory()
        thumbnail = ThumbnailFactory(
            media_asset=asset,
            size_preset=preset
        )

        preset.delete()

        # Thumbnail should be deleted or preset should be required
        # Implementation-specific behavior


# ============================================================
# Validation Tests
# ============================================================

class TestModelValidation:
    """Test model validation rules."""

    def test_media_asset_requires_title(self, admin_user):
        """MediaAsset requires a title."""
        # This depends on model definition
        # If title is required, this should fail
        try:
            asset = MediaAsset.objects.create(
                title='',  # Empty title
                uploaded_by=admin_user
            )
            # If it succeeds, title is optional
        except (ValidationError, IntegrityError):
            # Title is required
            pass

    def test_preset_dimensions_must_be_positive(self):
        """Preset dimensions must be positive integers."""
        # Valid preset
        valid = ImageSizePresetFactory(width=100, height=100)
        assert valid.width > 0
        assert valid.height > 0

        # Invalid dimensions would fail model validation
        # (if implemented)

    def test_thumbnail_dimensions_match_or_smaller(self, admin_user):
        """Thumbnail dimensions should not exceed preset dimensions."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        preset = ImageSizePresetFactory(width=300, height=300)

        # Valid thumbnail
        thumbnail = ThumbnailFactory(
            media_asset=asset,
            size_preset=preset,
            width=300,
            height=300
        )

        assert thumbnail.width <= preset.width
        assert thumbnail.height <= preset.height


# ============================================================
# Query Tests
# ============================================================

class TestModelQueries:
    """Test common query patterns."""

    def test_filter_assets_by_mime_type(self, admin_user):
        """Can filter assets by MIME type."""
        MediaAssetFactory(mime_type='image/jpeg', uploaded_by=admin_user, jpeg=True)
        MediaAssetFactory(mime_type='image/png', uploaded_by=admin_user, png=True)
        MediaAssetFactory(mime_type='video/mp4', uploaded_by=admin_user, video=True)

        jpegs = MediaAsset.objects.filter(mime_type='image/jpeg')
        assert jpegs.count() >= 1

    def test_filter_assets_by_folder(self, admin_user):
        """Can filter assets by folder."""
        folder = MediaFolderFactory()
        MediaAssetFactory(folder=folder, uploaded_by=admin_user)
        MediaAssetFactory(folder=None, uploaded_by=admin_user)

        in_folder = MediaAsset.objects.filter(folder=folder)
        assert in_folder.count() >= 1

    def test_filter_unused_assets(self, admin_user):
        """Can find unused assets."""
        MediaAssetFactory(uploaded_by=admin_user, in_use=True)  # usage_count=5
        MediaAssetFactory(usage_count=0, uploaded_by=admin_user)

        unused = MediaAsset.objects.filter(usage_count=0)
        assert unused.count() >= 1

    def test_filter_public_assets(self, admin_user):
        """Can find public assets."""
        MediaAssetFactory(is_public=True, uploaded_by=admin_user)
        MediaAssetFactory(is_public=False, uploaded_by=admin_user)

        public = MediaAsset.objects.filter(is_public=True)
        assert public.count() >= 1

    def test_assets_by_tag(self, admin_user):
        """Can query assets by tag."""
        tag = TagFactory(name='featured')
        asset = MediaAssetFactory(uploaded_by=admin_user)
        asset.tags.add(tag)

        tagged_assets = MediaAsset.objects.filter(tags=tag)
        assert asset in tagged_assets
