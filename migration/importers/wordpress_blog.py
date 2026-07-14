"""
WordPress Blog Importers.

Imports WordPress blog posts, categories, and tags to Spwig blog system.
"""

import logging
from urllib.parse import urlparse

from django.db import transaction
from tqdm import tqdm

from blog.models import BlogCategory, BlogPost, BlogTag
from media_library.models import MediaAsset
from migration.fetchers.wordpress_api import WordPressAPIClient
from migration.mappers.wordpress_blog import (
    WordPressBlogCategoryMapper,
    WordPressBlogPostMapper,
    WordPressBlogTagMapper,
)
from migration.services.content_image_processor import ContentImageProcessor
from migration.utils.transformers import parse_woocommerce_datetime

logger = logging.getLogger(__name__)


class WordPressBlogCategoryImporter:
    """
    Import WordPress categories to Spwig BlogCategory.

    Handles hierarchical structure by importing parents first,
    then mapping child categories to their imported parents.
    """

    def __init__(
        self,
        category_map: dict[int, int] | None = None,
        skip_existing: bool = True,
        step=None,
        migration_job=None,
    ):
        """
        Initialize the category importer.

        Args:
            category_map: Optional existing mapping of WP category ID -> Spwig category ID
            skip_existing: If True, skip categories that already exist (by slug)
            step: Optional MigrationStep for real-time progress tracking
            migration_job: Optional MigrationJob for tracking imported content
        """
        self.mapper = WordPressBlogCategoryMapper()
        self.category_map: dict[int, int] = category_map or {}
        self.skip_existing = skip_existing
        self.step = step
        self.migration_job = migration_job
        self.stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}

    def import_categories(
        self, categories: list[dict], progress_bar: bool = True
    ) -> dict[int, int]:
        """
        Import WordPress categories to Spwig.

        Args:
            categories: List of WordPress category data
            progress_bar: Whether to show tqdm progress bar

        Returns:
            Mapping of WordPress category ID -> Spwig BlogCategory ID
        """
        # Sort categories to import parents first (parent=0 first, then by parent id)
        sorted_categories = sorted(categories, key=lambda c: c.get("parent", 0))

        iterator = tqdm(
            sorted_categories, desc="📁 Blog Categories", unit="cat", disable=not progress_bar
        )

        for wp_category in iterator:
            try:
                self._import_single_category(wp_category)
                # Update step progress in real-time
                if self.step:
                    self.step.items_imported = self.stats["created"] + self.stats["updated"]
                    self.step.items_skipped = self.stats["skipped"]
                    self.step.items_failed = self.stats["errors"]
                    name = wp_category.get("name", "")
                    self.step.current_item = f"Category: {name}"
                    self.step.save()
            except Exception as e:
                self.stats["errors"] += 1
                logger.error(f"Error importing category {wp_category.get('id')}: {e}")
                if self.step:
                    self.step.items_failed = self.stats["errors"]
                    self.step.save()

        logger.info(
            f"Blog category import complete: "
            f"created={self.stats['created']}, updated={self.stats['updated']}, "
            f"skipped={self.stats['skipped']}, errors={self.stats['errors']}"
        )

        return self.category_map

    def _import_single_category(self, wp_category: dict) -> BlogCategory | None:
        """Import a single WordPress category."""
        wp_id = wp_category.get("id")

        # Skip if already imported
        if wp_id in self.category_map:
            self.stats["skipped"] += 1
            return None

        # Map WordPress data to Spwig format
        mapped_data = self.mapper.map(wp_category)

        # Handle parent reference
        wp_parent_id = wp_category.get("parent", 0)
        parent = None
        if wp_parent_id and wp_parent_id in self.category_map:
            parent = BlogCategory.objects.filter(pk=self.category_map[wp_parent_id]).first()

        # Ensure unique slug
        slug = mapped_data["slug"]
        original_slug = slug
        counter = 1
        while BlogCategory.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        # Check if category already exists (by slug)
        existing = BlogCategory.objects.filter(slug=original_slug).first()

        if existing:
            if self.skip_existing:
                self.category_map[wp_id] = existing.id
                self.stats["skipped"] += 1
                return existing
            # Update existing
            existing.name = mapped_data["name"]
            existing.description = mapped_data["description"]
            if parent:
                existing.parent = parent
            existing.save()
            self.category_map[wp_id] = existing.id
            self.stats["updated"] += 1
            return existing
        else:
            # Create new
            create_kwargs = {
                "name": mapped_data["name"],
                "slug": slug,
                "description": mapped_data["description"],
                "parent": parent,
                "is_active": True,
                "external_id": str(wp_id),
            }
            if self.migration_job:
                create_kwargs["migration_job"] = self.migration_job
                create_kwargs["imported_meta"] = {
                    "wordpress_category_id": str(wp_id),
                    "wordpress_permalink": wp_category.get("link", ""),
                }
            category = BlogCategory.objects.create(**create_kwargs)
            self.category_map[wp_id] = category.id
            self.stats["created"] += 1
            return category


class WordPressBlogTagImporter:
    """
    Import WordPress tags to Spwig BlogTag.
    """

    def __init__(
        self,
        tag_map: dict[int, int] | None = None,
        skip_existing: bool = True,
        step=None,
        migration_job=None,
    ):
        """
        Initialize the tag importer.

        Args:
            tag_map: Optional existing mapping of WP tag ID -> Spwig tag ID
            skip_existing: If True, skip tags that already exist (by name)
            step: Optional MigrationStep for real-time progress tracking
            migration_job: Optional MigrationJob for tracking imported content
        """
        self.mapper = WordPressBlogTagMapper()
        self.tag_map: dict[int, int] = tag_map or {}
        self.skip_existing = skip_existing
        self.step = step
        self.migration_job = migration_job
        self.stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}

    def import_tags(self, tags: list[dict], progress_bar: bool = True) -> dict[int, int]:
        """
        Import WordPress tags to Spwig.

        Args:
            tags: List of WordPress tag data
            progress_bar: Whether to show tqdm progress bar

        Returns:
            Mapping of WordPress tag ID -> Spwig BlogTag ID
        """
        # Capture base offsets from previous import phases (categories)
        if self.step:
            self._base_imported = self.step.items_imported
            self._base_skipped = self.step.items_skipped
            self._base_failed = self.step.items_failed
        else:
            self._base_imported = self._base_skipped = self._base_failed = 0

        iterator = tqdm(tags, desc="🏷️  Blog Tags", unit="tag", disable=not progress_bar)

        for wp_tag in iterator:
            try:
                self._import_single_tag(wp_tag)
                # Update step progress in real-time
                if self.step:
                    self.step.items_imported = (
                        self._base_imported + self.stats["created"] + self.stats["updated"]
                    )
                    self.step.items_skipped = self._base_skipped + self.stats["skipped"]
                    self.step.items_failed = self._base_failed + self.stats["errors"]
                    name = wp_tag.get("name", "")
                    self.step.current_item = f"Tag: {name}"
                    self.step.save()
            except Exception as e:
                self.stats["errors"] += 1
                logger.error(f"Error importing tag {wp_tag.get('id')}: {e}")
                if self.step:
                    self.step.items_failed = self._base_failed + self.stats["errors"]
                    self.step.save()

        logger.info(
            f"Blog tag import complete: "
            f"created={self.stats['created']}, updated={self.stats['updated']}, "
            f"skipped={self.stats['skipped']}, errors={self.stats['errors']}"
        )

        return self.tag_map

    def _import_single_tag(self, wp_tag: dict) -> BlogTag | None:
        """Import a single WordPress tag."""
        wp_id = wp_tag.get("id")

        # Skip if already imported
        if wp_id in self.tag_map:
            self.stats["skipped"] += 1
            return None

        # Map WordPress data to Spwig format
        mapped_data = self.mapper.map(wp_tag)

        # Ensure unique slug
        slug = mapped_data["slug"]
        original_slug = slug
        counter = 1
        while BlogTag.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        # Check if tag exists by name (tags have unique names)
        existing = BlogTag.objects.filter(name=mapped_data["name"]).first()

        if existing:
            self.tag_map[wp_id] = existing.id
            self.stats["skipped"] += 1
            return existing
        else:
            create_kwargs = {
                "name": mapped_data["name"],
                "slug": slug,
                "external_id": str(wp_id),
            }
            if self.migration_job:
                create_kwargs["migration_job"] = self.migration_job
            tag = BlogTag.objects.create(**create_kwargs)
            self.tag_map[wp_id] = tag.id
            self.stats["created"] += 1
            return tag


class WordPressBlogPostImporter:
    """
    Import WordPress posts to Spwig BlogPost.

    Handles:
    - Featured image download
    - Content image extraction and download (same-origin only)
    - Category and tag mapping
    - Date preservation
    """

    def __init__(
        self,
        source_url: str,
        category_map: dict[int, int],
        tag_map: dict[int, int],
        media_map: dict[int, int] | None = None,
        migration_job=None,
        skip_existing: bool = True,
        step=None,
    ):
        """
        Initialize the post importer.

        Args:
            source_url: WordPress site URL (for same-origin image detection)
            category_map: Mapping of WP category ID -> Spwig BlogCategory ID
            tag_map: Mapping of WP tag ID -> Spwig BlogTag ID
            media_map: Optional existing mapping of WP media ID -> Spwig MediaAsset ID
            migration_job: Optional MigrationJob for media tracking
            skip_existing: If True, skip posts that already exist (by slug)
            step: Optional MigrationStep for real-time progress tracking
        """
        self.source_url = source_url
        self.source_domain = urlparse(source_url).netloc
        self.mapper = WordPressBlogPostMapper()
        self.category_map = category_map
        self.tag_map = tag_map
        self.media_map: dict[int, int] = media_map or {}
        self.migration_job = migration_job
        self.skip_existing = skip_existing
        self.step = step
        self.content_processor = ContentImageProcessor(
            source_domain=self.source_domain,
            migration_job=migration_job,
        )
        self.stats = {
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0,
            "images_imported": 0,
        }

    def import_posts(
        self, posts: list[dict], wp_client: WordPressAPIClient, progress_bar: bool = True
    ) -> tuple[dict[int, int], dict]:
        """
        Import WordPress posts to Spwig.

        Args:
            posts: List of WordPress post data
            wp_client: WordPress API client for fetching media
            progress_bar: Whether to show tqdm progress bar

        Returns:
            Tuple of (post_map, stats) where post_map is WP post ID -> Spwig post ID
        """
        post_map: dict[int, int] = {}

        # Capture base offsets from previous import phases (categories + tags)
        if self.step:
            self._base_imported = self.step.items_imported
            self._base_skipped = self.step.items_skipped
            self._base_failed = self.step.items_failed
        else:
            self._base_imported = self._base_skipped = self._base_failed = 0

        iterator = tqdm(posts, desc="📝 Blog Posts", unit="post", disable=not progress_bar)

        for wp_post in iterator:
            try:
                title = (
                    wp_post.get("title", {}).get("rendered", "")
                    if isinstance(wp_post.get("title"), dict)
                    else wp_post.get("title", "")
                )
                # Update current_item before processing (so UI shows what's being worked on)
                if self.step:
                    self.step.current_item = f"Importing post: {title[:80]}"
                    self.step.save()

                result = self._import_single_post(wp_post, wp_client)
                if result:
                    post_map[wp_post.get("id")] = result.id

                # Update step progress after each post
                if self.step:
                    self.step.items_imported = (
                        self._base_imported + self.stats["created"] + self.stats["updated"]
                    )
                    self.step.items_skipped = self._base_skipped + self.stats["skipped"]
                    self.step.items_failed = self._base_failed + self.stats["errors"]
                    self.step.save()
            except Exception as e:
                self.stats["errors"] += 1
                logger.error(f"Error importing post {wp_post.get('id')}: {e}")
                if self.step:
                    self.step.items_failed = self._base_failed + self.stats["errors"]
                    self.step.save()

        logger.info(
            f"Blog post import complete: "
            f"created={self.stats['created']}, updated={self.stats['updated']}, "
            f"skipped={self.stats['skipped']}, errors={self.stats['errors']}, "
            f"images={self.stats['images_imported']}"
        )

        return post_map, self.stats

    @transaction.atomic
    def _import_single_post(self, wp_post: dict, wp_client: WordPressAPIClient) -> BlogPost | None:
        """Import a single WordPress post with all its media."""
        wp_id = wp_post.get("id")

        # Map WordPress data to Spwig format
        mapped_data = self.mapper.map(wp_post)

        # Check if post already exists by slug
        slug = mapped_data["slug"]
        original_slug = slug
        existing = BlogPost.objects.filter(slug=original_slug).first()

        if existing and self.skip_existing:
            self.stats["skipped"] += 1
            logger.debug(f"Post '{original_slug}' already exists, skipping")
            return existing

        # Ensure unique slug if not skipping
        counter = 1
        while BlogPost.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        # Get featured image
        featured_image = None
        featured_media_id = mapped_data.get("featured_media_id")
        if featured_media_id:
            featured_image = self._get_or_import_media(featured_media_id, wp_client)
            if featured_image:
                self.stats["images_imported"] += 1

        # Process content images
        content = mapped_data.get("simple_content", "")
        if content:
            content, content_stats = self.content_processor.process_content(content)
            self.stats["images_imported"] += content_stats.get("images_downloaded", 0)

        # Map category
        category = None
        wp_category_ids = mapped_data.get("category_ids", [])
        for wp_cat_id in wp_category_ids:
            if wp_cat_id in self.category_map:
                category = BlogCategory.objects.filter(pk=self.category_map[wp_cat_id]).first()
                break  # Use first matching category

        # Parse original dates from WordPress (preserve creation date)
        create_kwargs = {
            "title": mapped_data["title"],
            "slug": slug,
            "status": mapped_data["status"],
            "excerpt": mapped_data.get("excerpt", ""),
            "simple_content": content,
            "featured_image": featured_image,
            "category": category,
            "external_id": str(wp_id),
        }

        # Track migration job and WordPress metadata
        if self.migration_job:
            create_kwargs["migration_job"] = self.migration_job
            create_kwargs["imported_meta"] = {
                "wordpress_post_id": str(wp_id),
                "wordpress_permalink": wp_post.get("link", ""),
            }

        date_created = mapped_data.get("date_created_gmt") or mapped_data.get("date_created")
        if date_created:
            parsed_date = parse_woocommerce_datetime(date_created)
            if parsed_date:
                create_kwargs["created_at"] = parsed_date
                if mapped_data["status"] == "published":
                    create_kwargs["published_at"] = parsed_date

        # Create post with original dates in one DB write
        post = BlogPost.objects.create(**create_kwargs)

        # Set tags (M2M relationship)
        wp_tag_ids = mapped_data.get("tag_ids", [])
        spwig_tags = []
        for wp_tag_id in wp_tag_ids:
            if wp_tag_id in self.tag_map:
                spwig_tag_id = self.tag_map[wp_tag_id]
                tag = BlogTag.objects.filter(pk=spwig_tag_id).first()
                if tag:
                    spwig_tags.append(tag)
        if spwig_tags:
            post.tags.set(spwig_tags)

        self.stats["created"] += 1
        return post

    def _get_or_import_media(
        self, wp_media_id: int, wp_client: WordPressAPIClient
    ) -> MediaAsset | None:
        """Get existing or import new media asset from WordPress."""
        # Check if already imported
        if wp_media_id in self.media_map:
            return MediaAsset.objects.filter(pk=self.media_map[wp_media_id]).first()

        # Fetch media info from WordPress
        try:
            media_data = wp_client.fetch_media(wp_media_id)
            if not media_data:
                return None

            # Get source URL
            source_url = None
            if "source_url" in media_data:
                source_url = media_data["source_url"]
            elif "media_details" in media_data:
                sizes = media_data["media_details"].get("sizes", {})
                if "full" in sizes:
                    source_url = sizes["full"].get("source_url")

            if not source_url:
                return None

            # Download and create MediaAsset
            from migration.utils.media_helpers import download_and_create_media_asset

            asset = download_and_create_media_asset(
                url=source_url,
                alt_text=media_data.get("alt_text", ""),
                title=media_data.get("title", {}).get("rendered", ""),
                migration_job=self.migration_job,
            )

            if asset:
                self.media_map[wp_media_id] = asset.id

            return asset

        except Exception as e:
            logger.warning(f"Failed to import media {wp_media_id}: {e}")
            return None


class WordPressBlogImporter:
    """
    Main orchestrator for WordPress blog import.

    Coordinates import of categories, tags, and posts in the correct order.
    """

    def __init__(
        self,
        source_url: str,
        consumer_key: str = None,
        consumer_secret: str = None,
        migration_job=None,
        skip_existing: bool = True,
    ):
        """
        Initialize the blog importer.

        Args:
            source_url: WordPress site URL
            consumer_key: Not used for WordPress REST API (public endpoints)
            consumer_secret: Not used for WordPress REST API (public endpoints)
            migration_job: Optional MigrationJob for media tracking
            skip_existing: If True, skip items that already exist
        """
        self.source_url = source_url
        self.wp_client = WordPressAPIClient(source_url)
        self.migration_job = migration_job
        self.skip_existing = skip_existing
        self.stats = {
            "categories": {"created": 0, "updated": 0, "skipped": 0, "errors": 0},
            "tags": {"created": 0, "updated": 0, "skipped": 0, "errors": 0},
            "posts": {"created": 0, "updated": 0, "skipped": 0, "errors": 0},
            "media": {"imported": 0},
        }

    def import_all(self, progress_bar: bool = True, step=None) -> dict:
        """
        Import all blog content from WordPress.

        Import order:
        1. Categories (for parent references)
        2. Tags
        3. Posts (with media)

        Args:
            progress_bar: Whether to show tqdm progress bars
            step: Optional MigrationStep for real-time progress tracking

        Returns:
            Import statistics
        """
        logger.info(f"Starting WordPress blog import from {self.source_url}")

        # Fetch all data first, updating current_item during fetch phase
        if step:
            step.current_item = "Fetching blog categories..."
            step.save()
        logger.info("Fetching categories...")
        categories = self.wp_client.fetch_all_categories()
        logger.info(f"Found {len(categories)} categories")

        if step:
            step.current_item = "Fetching blog tags..."
            step.save()
        logger.info("Fetching tags...")
        tags = self.wp_client.fetch_all_tags()
        logger.info(f"Found {len(tags)} tags")

        if step:
            step.current_item = "Fetching blog posts..."
            step.save()
        logger.info("Fetching posts...")
        posts = self.wp_client.fetch_all_posts()
        logger.info(f"Found {len(posts)} posts")

        # Set total items on step now that we know the real counts
        if step:
            step.items_total = len(categories) + len(tags) + len(posts)
            step.current_item = (
                f"Importing {len(categories)} categories, {len(tags)} tags, {len(posts)} posts..."
            )
            step.save()

        # Import in order
        # 1. Categories
        category_importer = WordPressBlogCategoryImporter(
            skip_existing=self.skip_existing,
            step=step,
            migration_job=self.migration_job,
        )
        category_map = category_importer.import_categories(categories, progress_bar=progress_bar)
        self.stats["categories"] = category_importer.stats

        # 2. Tags
        tag_importer = WordPressBlogTagImporter(
            skip_existing=self.skip_existing,
            step=step,
            migration_job=self.migration_job,
        )
        tag_map = tag_importer.import_tags(tags, progress_bar=progress_bar)
        self.stats["tags"] = tag_importer.stats

        # 3. Posts
        post_importer = WordPressBlogPostImporter(
            source_url=self.source_url,
            category_map=category_map,
            tag_map=tag_map,
            migration_job=self.migration_job,
            skip_existing=self.skip_existing,
            step=step,
        )
        post_map, post_stats = post_importer.import_posts(
            posts, self.wp_client, progress_bar=progress_bar
        )
        self.stats["posts"] = post_stats
        self.stats["media"]["imported"] = post_stats.get("images_imported", 0)

        # Clear current_item when done
        if step:
            step.current_item = ""
            step.save()

        logger.info("WordPress blog import complete!")
        logger.info(f"Stats: {self.stats}")

        return self.stats

    def import_categories_only(self, progress_bar: bool = True) -> dict[int, int]:
        """Import only categories."""
        categories = self.wp_client.fetch_all_categories()
        category_importer = WordPressBlogCategoryImporter()
        return category_importer.import_categories(categories, progress_bar=progress_bar)

    def import_tags_only(self, progress_bar: bool = True) -> dict[int, int]:
        """Import only tags."""
        tags = self.wp_client.fetch_all_tags()
        tag_importer = WordPressBlogTagImporter()
        return tag_importer.import_tags(tags, progress_bar=progress_bar)

    def import_posts_only(
        self, category_map: dict[int, int], tag_map: dict[int, int], progress_bar: bool = True
    ) -> tuple[dict[int, int], dict]:
        """Import only posts (requires category and tag maps)."""
        posts = self.wp_client.fetch_all_posts()
        post_importer = WordPressBlogPostImporter(
            source_url=self.source_url,
            category_map=category_map,
            tag_map=tag_map,
        )
        return post_importer.import_posts(posts, self.wp_client, progress_bar=progress_bar)
