"""
Blog Content Sync Serializer

Handles export/import of blog content models:
- BlogCategory (hierarchical, with inline MediaAsset)
- BlogPost (with tags, MediaAsset references)
- BlogTag (auto-created inline)
"""

import logging

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

BLOG_CATEGORY_FIELDS = [
    "name",
    "slug",
    "description",
    "translations",
    "meta_title",
    "meta_description",
    "seo_auto_generated",
    "is_active",
    "sort_order",
    "external_id",
    "template_variant",
    "css_classes",
    "layout_config",
    "style_overrides",
    "responsive_config",
    "inherit_parent_theme",
]

BLOG_POST_FIELDS = [
    "title",
    "slug",
    "status",
    "page_template",
    "excerpt",
    "simple_content",
    "use_page_builder",
    "translations",
    "meta_title",
    "meta_description",
    "seo_auto_generated",
    "published_at",
    "scheduled_at",
    "is_featured",
    "is_pinned",
    "reading_time_minutes",
    "notify_subscribers",
    "notification_sent",
    "auto_share_facebook",
    "auto_share_instagram",
    "auto_share_linkedin",
    "social_share_message",
    "external_id",
    "template_variant",
    "css_classes",
    "layout_config",
    "style_overrides",
    "responsive_config",
    "inherit_parent_theme",
]


class BlogContentSerializer(CollectionSyncSerializer):
    """Serializer for blog posts and categories.

    Models handled:
        - BlogCategory: Blog category hierarchy (with inline MediaAsset for image)
        - BlogPost: Blog post content with tag references
        - BlogTag: Auto-created during post import
    """

    category_key = "blog_content"
    natural_key_fields = ["slug"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from blog.models import BlogPost

        self.model_class = BlogPost

    def get_count(self):
        from blog.models import BlogCategory, BlogPost

        return BlogPost.objects.count() + BlogCategory.objects.count()

    def export(self, credential_mode="redact"):
        from blog.models import BlogCategory, BlogPost

        items = []

        # Categories
        for cat in BlogCategory.objects.select_related("parent", "image_asset").all():
            data = {f: getattr(cat, f) for f in BLOG_CATEGORY_FIELDS}
            data["_source_pk"] = cat.pk
            data["_model"] = "BlogCategory"
            data["_parent_slug"] = cat.parent.slug if cat.parent else None

            # Serialize datetime fields
            if data.get("created_at"):
                data["created_at"] = (
                    cat.created_at.isoformat()
                    if hasattr(cat.created_at, "isoformat")
                    else str(cat.created_at)
                )

            items.append(data)

        # Posts
        for post in (
            BlogPost.objects.select_related(
                "category",
                "featured_image",
                "og_image",
                "created_by",
            )
            .prefetch_related("tags")
            .all()
        ):
            data = {f: getattr(post, f) for f in BLOG_POST_FIELDS}
            data["_source_pk"] = post.pk
            data["_model"] = "BlogPost"
            data["_category_slug"] = post.category.slug if post.category else None
            data["_tag_slugs"] = list(post.tags.values_list("slug", flat=True))
            data["_tag_names"] = {t.slug: t.name for t in post.tags.all()}

            # Serialize datetime fields
            for dt_field in ["published_at", "scheduled_at"]:
                val = data.get(dt_field)
                if val and hasattr(val, "isoformat"):
                    data[dt_field] = val.isoformat()

            items.append(data)

        return {
            "category": self.category_key,
            "sync_type": "collection",
            "items": items,
            "total": len(items),
        }

    def import_data(self, data, dry_run=False, sync_mode="additive"):
        if dry_run:
            return self.generate_diff(data)

        items = data.get("items", [])
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        # Pass 1: Categories (without parent)
        for item in items:
            if item.get("_model") != "BlogCategory":
                continue
            try:
                with transaction.atomic():
                    self._import_category(item, set_parent=False)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Category {item.get('name', '?')}: {e}")

        # Pass 2: Set category parents
        for item in items:
            if item.get("_model") != "BlogCategory":
                continue
            if item.get("_parent_slug"):
                try:
                    self._set_category_parent(item)
                except Exception as e:
                    errors.append(f"Category parent {item.get('slug', '?')}: {e}")

        # Pass 3: Posts
        for item in items:
            if item.get("_model") != "BlogPost":
                continue
            try:
                with transaction.atomic():
                    self._import_post(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Post {item.get('title', '?')}: {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_category(self, item, set_parent=False):
        from blog.models import BlogCategory

        existing = BlogCategory.objects.filter(slug=item["slug"]).first()

        if existing:
            cat = existing
            for f in BLOG_CATEGORY_FIELDS:
                if f in item:
                    setattr(cat, f, item[f])
        else:
            cat = BlogCategory()
            for f in BLOG_CATEGORY_FIELDS:
                if f in item:
                    setattr(cat, f, item[f])

        if not set_parent:
            cat.parent = None

        cat.save()

    def _set_category_parent(self, item):
        from blog.models import BlogCategory

        cat = BlogCategory.objects.filter(slug=item["slug"]).first()
        if not cat:
            return
        parent = BlogCategory.objects.filter(slug=item["_parent_slug"]).first()
        if parent:
            cat.parent = parent
            cat.save(update_fields=["parent"])

    def _import_post(self, item):
        from blog.models import BlogCategory, BlogPost, BlogTag

        existing = BlogPost.objects.filter(slug=item["slug"]).first()

        if existing:
            post = existing
            for f in BLOG_POST_FIELDS:
                if f in item:
                    setattr(post, f, item[f])
        else:
            post = BlogPost()
            for f in BLOG_POST_FIELDS:
                if f in item:
                    setattr(post, f, item[f])

        # Resolve category
        cat_slug = item.get("_category_slug")
        if cat_slug:
            post.category = BlogCategory.objects.filter(slug=cat_slug).first()
        else:
            post.category = None

        post.save()

        # Handle tags - auto-create
        tag_slugs = item.get("_tag_slugs", [])
        tag_names = item.get("_tag_names", {})
        if tag_slugs:
            tags = []
            for slug in tag_slugs:
                tag, _ = BlogTag.objects.get_or_create(
                    slug=slug,
                    defaults={"name": tag_names.get(slug, slug)},
                )
                tags.append(tag)
            post.tags.set(tags)
        else:
            post.tags.clear()

    def _delete_absent(self, remote_items):
        from blog.models import BlogCategory, BlogPost

        remote_post_slugs = set()
        remote_cat_slugs = set()
        for item in remote_items:
            if item.get("_model") == "BlogPost":
                remote_post_slugs.add(item.get("slug"))
            elif item.get("_model") == "BlogCategory":
                remote_cat_slugs.add(item.get("slug"))

        deleted = 0
        # Delete posts first (no FK constraints from posts to categories for deletion)
        for post in BlogPost.objects.all():
            if post.slug not in remote_post_slugs:
                post.delete()
                deleted += 1
        for cat in BlogCategory.objects.all():
            if cat.slug not in remote_cat_slugs:
                try:
                    cat.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete blog category {cat.slug}: {e}")
        return deleted

    def generate_diff(self, remote_data):
        from blog.models import BlogCategory, BlogPost

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            model_type = item.get("_model")
            slug = item.get("slug")
            name = item.get("name") or item.get("title", slug or "Unknown")

            if model_type == "BlogCategory":
                existing = BlogCategory.objects.filter(slug=slug).first()
                fields = BLOG_CATEGORY_FIELDS
            elif model_type == "BlogPost":
                existing = BlogPost.objects.filter(slug=slug).first()
                fields = BLOG_POST_FIELDS
            else:
                continue

            if existing:
                field_changes = self._compute_field_diff(existing, item, fields)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": model_type,
                            "name": name,
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append(
                    {
                        "type": "add",
                        "model": model_type,
                        "name": name,
                        "fields": {k: v for k, v in item.items() if not k.startswith("_")},
                    }
                )

        adds = sum(1 for c in changes if c["type"] == "add")
        mods = sum(1 for c in changes if c["type"] == "modify")
        parts = []
        if adds:
            parts.append(f"{adds} addition(s)")
        if mods:
            parts.append(f"{mods} modification(s)")

        return {
            "changes": changes,
            "warnings": [],
            "summary": ", ".join(parts) if parts else "No changes",
        }

    def snapshot_current(self):
        return self.export(credential_mode="skip")

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {"restored": result.get("synced", 0), "errors": result.get("errors", [])}
        except Exception as e:
            return {"restored": 0, "errors": [str(e)]}
