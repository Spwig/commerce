"""
Content Link Processor for Post-Import Link Rewriting.

Scans imported HTML content for same-origin links pointing to the old
WordPress/WooCommerce site, auto-suggests replacement URLs by matching
to Spwig objects, and applies approved replacements.

Follows the same pattern as ContentImageProcessor.
"""

import logging
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

from migration.models.content_link import ContentLink

logger = logging.getLogger(__name__)


class ContentLinkProcessor:
    """
    Scan imported HTML content for same-origin links and suggest replacements.

    Usage:
        processor = ContentLinkProcessor(
            source_domain='oldsite.com',
            migration_job=job
        )
        processor.scan_all_content()
        processor.auto_match_links()

    Then after merchant review:
        processor.apply_approved_links()
    """

    def __init__(self, source_domain: str, migration_job):
        """
        Initialize the content link processor.

        Args:
            source_domain: The WordPress/WooCommerce site domain
            migration_job: MigrationJob instance
        """
        # Extract just the hostname from the source domain/URL
        parsed_source = urlparse(source_domain.lower().rstrip("/"))
        self.source_domain = (parsed_source.netloc or parsed_source.path).split(":")[0]
        if self.source_domain.startswith("www."):
            self.source_domain = self.source_domain[4:]
        self.migration_job = migration_job

        # Cache for URL matching: url -> match result dict
        self.url_match_cache: dict[str, dict] = {}

        # Statistics
        self.stats = {
            "links_found": 0,
            "links_same_origin": 0,
            "links_external_skipped": 0,
            "links_matched": 0,
            "links_unmatched": 0,
        }

    def is_same_origin(self, url: str) -> bool:
        """
        Check if a URL is from the source WordPress site.

        Same logic as ContentImageProcessor.is_same_origin().
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            # Skip empty, relative, and special URLs.
            # No domain + starts with single "/" = relative URL (same-origin).
            if not domain:
                return url.startswith("/") and not url.startswith("//")

            # Remove www. prefix for comparison
            if domain.startswith("www."):
                domain = domain[4:]

            source = self.source_domain
            if source.startswith("www."):
                source = source[4:]

            # Remove port for comparison
            if ":" in domain:
                domain = domain.split(":")[0]
            if ":" in source:
                source = source.split(":")[0]

            return domain == source or domain.endswith("." + source)

        except Exception as e:
            logger.warning(f"Error parsing URL {url}: {e}")
            return False

    def scan_all_content(self):
        """
        Scan all imported objects for same-origin links.

        Iterates through Products, BlogPosts, and Categories
        that belong to this migration job.
        """
        from blog.models import BlogPost
        from catalog.models import Category, Product

        logger.info(f"Scanning imported content for links from {self.source_domain}...")

        # Scan products
        products = Product.objects.filter(migration_job=self.migration_job)
        for product in products:
            if product.full_description:
                self._scan_field(
                    html=product.full_description,
                    source_type="product_full_desc",
                    source_product=product,
                    source_title=product.name,
                )
            if product.short_description:
                self._scan_field(
                    html=product.short_description,
                    source_type="product_short_desc",
                    source_product=product,
                    source_title=product.name,
                )

        # Scan blog posts
        blog_posts = BlogPost.objects.filter(migration_job=self.migration_job)
        for post in blog_posts:
            if post.simple_content:
                self._scan_field(
                    html=post.simple_content,
                    source_type="blog_post_content",
                    source_blog_post=post,
                    source_title=post.title,
                )

        # Scan categories
        categories = Category.objects.filter(migration_job=self.migration_job)
        for cat in categories:
            if cat.description:
                self._scan_field(
                    html=cat.description,
                    source_type="category_description",
                    source_category=cat,
                    source_title=cat.name,
                )

        logger.info(
            f"Link scan complete: {self.stats['links_found']} found, "
            f"{self.stats['links_same_origin']} same-origin, "
            f"{self.stats['links_external_skipped']} external skipped"
        )

    def _scan_field(
        self,
        html: str,
        source_type: str,
        source_title: str = "",
        source_product=None,
        source_blog_post=None,
        source_category=None,
    ):
        """
        Parse HTML field with BeautifulSoup and extract same-origin links.

        Creates ContentLink records for each discovered same-origin link.
        """
        if not html:
            return

        soup = BeautifulSoup(html, "html.parser")

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            self.stats["links_found"] += 1

            # Skip anchors, mailto, tel, javascript, data URLs
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue

            # Skip WordPress API/system URLs
            if (
                "/wp-json/" in href
                or "/wp-admin/" in href
                or "/wp-content/" in href
                or "/wp-includes/" in href
            ):
                continue

            # Check same-origin
            if not self.is_same_origin(href):
                self.stats["links_external_skipped"] += 1
                continue

            self.stats["links_same_origin"] += 1

            # Get anchor text
            anchor_text = a_tag.get_text(strip=True)[:500]

            # Create ContentLink record
            ContentLink.objects.create(
                job=self.migration_job,
                source_type=source_type,
                source_product=source_product,
                source_blog_post=source_blog_post,
                source_category=source_category,
                source_title=source_title[:300],
                original_url=href[:2000],
                anchor_text=anchor_text,
            )

    def auto_match_links(self):
        """
        For each pending ContentLink, try to find a matching Spwig object.

        Uses a priority cascade of matching strategies.
        Results are cached so the same URL is only looked up once.
        """
        pending_links = ContentLink.objects.filter(
            job=self.migration_job,
            status="pending",
        )

        # Get unique URLs to match
        unique_urls = set(pending_links.values_list("original_url", flat=True))

        logger.info(f"Auto-matching {len(unique_urls)} unique URLs...")

        for url in unique_urls:
            if url in self.url_match_cache:
                result = self.url_match_cache[url]
            else:
                result = self._match_url(url)
                self.url_match_cache[url] = result

            # Update all ContentLinks with this URL
            update_kwargs = {
                "suggested_url": result.get("suggested_url", ""),
                "match_type": result.get("match_type", "none"),
                "target_type": result.get("target_type", "unknown"),
                "target_id": result.get("target_id"),
                "confidence": result.get("confidence", 0.0),
            }

            updated = ContentLink.objects.filter(
                job=self.migration_job,
                original_url=url,
                status="pending",
            ).update(**update_kwargs)

            if result.get("confidence", 0) > 0:
                self.stats["links_matched"] += updated
            else:
                self.stats["links_unmatched"] += updated

        logger.info(
            f"Auto-matching complete: {self.stats['links_matched']} matched, "
            f"{self.stats['links_unmatched']} unmatched"
        )

    def _match_url(self, url: str) -> dict:
        """
        Match a URL to a Spwig object using priority cascade.

        Returns dict with: suggested_url, match_type, target_type, target_id, confidence
        """

        parsed = urlparse(url)
        path = parsed.path.strip("/")
        path_segments = [s for s in path.split("/") if s]
        query = parse_qs(parsed.query)

        # Strategy 1: Stored permalink match (confidence 1.0)
        result = self._match_by_permalink(url)
        if result:
            return result

        # Strategy 2: WordPress URL path patterns (confidence 0.95)
        result = self._match_by_path_pattern(path_segments)
        if result:
            return result

        # Strategy 3: Query parameter ?p=ID (confidence 0.95)
        post_id = query.get("p", [None])[0] or query.get("page_id", [None])[0]
        if post_id:
            result = self._match_by_external_id(post_id)
            if result:
                return result

        # Strategy 4: Default WordPress permalink /{slug}/ (confidence 0.9)
        if len(path_segments) == 1:
            slug = path_segments[0]
            result = self._match_slug_to_blog_post(slug, confidence=0.9)
            if result:
                return result

        # Strategy 5: Last path segment slug fallback (confidence 0.7)
        if path_segments:
            slug = path_segments[-1]
            result = self._match_slug_across_models(slug, confidence=0.7)
            if result:
                return result

        # No match
        return {
            "suggested_url": "",
            "match_type": "none",
            "target_type": "unknown",
            "target_id": None,
            "confidence": 0.0,
        }

    def _match_by_permalink(self, url: str) -> dict | None:
        """Strategy 1: Match against stored permalinks in imported_meta."""
        from blog.models import BlogPost
        from catalog.models import Category, Product

        # Try products
        product = Product.objects.filter(
            migration_job=self.migration_job,
            imported_meta__woocommerce_permalink=url,
        ).first()
        if product:
            return self._make_result(product, "product", "permalink", 1.0)

        # Try categories
        category = Category.objects.filter(
            migration_job=self.migration_job,
            imported_meta__woocommerce_permalink=url,
        ).first()
        if category:
            return self._make_result(category, "category", "permalink", 1.0)

        # Try blog posts
        post = BlogPost.objects.filter(
            migration_job=self.migration_job,
            imported_meta__wordpress_permalink=url,
        ).first()
        if post:
            return self._make_result(post, "blog_post", "permalink", 1.0)

        return None

    def _match_by_path_pattern(self, path_segments: list[str]) -> dict | None:
        """Strategy 2: Match by known WordPress URL patterns."""
        from blog.models import BlogCategory, BlogPost
        from catalog.models import Category, Product

        if not path_segments:
            return None

        # /product/{slug}/
        if len(path_segments) >= 2 and path_segments[0] == "product":
            slug = path_segments[1]
            product = Product.objects.filter(slug=slug).first()
            if product:
                return self._make_result(product, "product", "path_pattern", 0.95)

        # /product-category/{slug}/ or /product-category/parent/{slug}/
        if path_segments[0] == "product-category":
            slug = path_segments[-1]  # Last segment is the actual category
            category = Category.objects.filter(slug=slug).first()
            if category:
                return self._make_result(category, "category", "path_pattern", 0.95)

        # /category/{slug}/ (some WP installs)
        if len(path_segments) >= 2 and path_segments[0] == "category":
            slug = path_segments[1]
            # Try blog category first
            blog_cat = BlogCategory.objects.filter(slug=slug).first()
            if blog_cat:
                return {
                    "suggested_url": f"/blog/category/{slug}/",
                    "match_type": "path_pattern",
                    "target_type": "blog_category",
                    "target_id": blog_cat.id,
                    "confidence": 0.95,
                }
            # Then product category
            category = Category.objects.filter(slug=slug).first()
            if category:
                return self._make_result(category, "category", "path_pattern", 0.9)

        # /blog/{slug}/ or /posts/{slug}/
        if len(path_segments) >= 2 and path_segments[0] in ("blog", "posts", "post"):
            slug = path_segments[1]
            post = BlogPost.objects.filter(slug=slug).first()
            if post:
                return self._make_result(post, "blog_post", "path_pattern", 0.95)

        # /shop/ or /shop/{anything}
        if path_segments[0] == "shop" and len(path_segments) >= 2:
            slug = path_segments[-1]
            # Try product first, then category
            product = Product.objects.filter(slug=slug).first()
            if product:
                return self._make_result(product, "product", "path_pattern", 0.85)
            category = Category.objects.filter(slug=slug).first()
            if category:
                return self._make_result(category, "category", "path_pattern", 0.85)

        return None

    def _match_by_external_id(self, external_id: str) -> dict | None:
        """Strategy 3: Match by external_id from query params."""
        from blog.models import BlogPost
        from catalog.models import Product

        # Try product
        product = Product.objects.filter(external_id=external_id).first()
        if product:
            return self._make_result(product, "product", "external_id", 0.95)

        # Try blog post
        post = BlogPost.objects.filter(external_id=external_id).first()
        if post:
            return self._make_result(post, "blog_post", "external_id", 0.95)

        return None

    def _match_slug_to_blog_post(self, slug: str, confidence: float = 0.9) -> dict | None:
        """Match a bare slug to a blog post (WordPress default permalink)."""
        from blog.models import BlogPost

        post = BlogPost.objects.filter(slug=slug).first()
        if post:
            return self._make_result(post, "blog_post", "slug_exact", confidence)

        return None

    def _match_slug_across_models(self, slug: str, confidence: float = 0.7) -> dict | None:
        """Fallback: try matching slug across all importable models."""
        from blog.models import BlogPost
        from catalog.models import Category, Product

        # Try product
        product = Product.objects.filter(slug=slug).first()
        if product:
            return self._make_result(product, "product", "slug_fallback", confidence)

        # Try category
        category = Category.objects.filter(slug=slug).first()
        if category:
            return self._make_result(category, "category", "slug_fallback", confidence)

        # Try blog post
        post = BlogPost.objects.filter(slug=slug).first()
        if post:
            return self._make_result(post, "blog_post", "slug_fallback", confidence)

        return None

    def _make_result(self, obj, target_type: str, match_type: str, confidence: float) -> dict:
        """Create a match result dict from a matched object."""
        try:
            # Use get_absolute_url() without language prefix — Django's LocaleMiddleware
            # auto-redirects to the visitor's active language (302 /product/slug/ → /en/product/slug/)
            # This ensures links work correctly in all languages rather than hardcoding one.
            suggested_url = obj.get_absolute_url()
        except Exception:
            suggested_url = ""

        return {
            "suggested_url": suggested_url,
            "match_type": match_type,
            "target_type": target_type,
            "target_id": obj.pk,
            "confidence": confidence,
        }

    def apply_approved_links(self) -> dict:
        """
        Replace URLs in HTML content for all approved/modified ContentLinks.

        Groups links by source object to minimize DB writes.
        Returns statistics dict.
        """

        apply_stats = {"applied": 0, "failed": 0, "skipped": 0}

        approved = ContentLink.objects.filter(
            job=self.migration_job,
            status__in=["approved", "modified"],
        ).order_by("source_type", "source_product_id", "source_blog_post_id", "source_category_id")

        if not approved.exists():
            return apply_stats

        # Group by source object
        current_key = None
        current_links = []

        for link in approved:
            key = (link.source_type, link.source_object_id)
            if key != current_key:
                # Process previous group
                if current_links:
                    self._apply_link_group(current_links, apply_stats)
                current_key = key
                current_links = [link]
            else:
                current_links.append(link)

        # Process last group
        if current_links:
            self._apply_link_group(current_links, apply_stats)

        logger.info(
            f"Link application complete: {apply_stats['applied']} applied, "
            f"{apply_stats['failed']} failed, {apply_stats['skipped']} skipped"
        )

        return apply_stats

    def _apply_link_group(self, links: list[ContentLink], stats: dict):
        """
        Apply URL replacements for a group of links belonging to the same source object.

        Parses HTML once, replaces all matched URLs, saves once.
        """
        first_link = links[0]

        # Get the source object and field
        obj, field_name = self._get_source_object_and_field(first_link)
        if not obj or not field_name:
            for link in links:
                link.status = "failed"
                link.error_message = "Source object not found"
                link.save(update_fields=["status", "error_message"])
                stats["failed"] += 1
            return

        # Get current HTML content
        html = getattr(obj, field_name, "")
        if not html:
            for link in links:
                link.status = "failed"
                link.error_message = "Source field is empty"
                link.save(update_fields=["status", "error_message"])
                stats["failed"] += 1
            return

        # Parse HTML once
        soup = BeautifulSoup(html, "html.parser")
        any_replaced = False

        # Group links by original_url to handle duplicates within same content
        url_groups: dict[str, list[ContentLink]] = {}
        for link in links:
            new_url = link.get_effective_url()
            if not new_url:
                link.status = "skipped"
                link.save(update_fields=["status"])
                stats["skipped"] += 1
                continue
            url_groups.setdefault(link.original_url, []).append(link)

        for original_url, url_links in url_groups.items():
            new_url = url_links[0].get_effective_url()

            # Find and replace matching <a> tags
            replaced = False
            for a_tag in soup.find_all("a", href=original_url):
                a_tag["href"] = new_url
                replaced = True
                any_replaced = True

            # Mark all links with this URL as applied or failed
            for link in url_links:
                if replaced:
                    link.status = "applied"
                    link.save(update_fields=["status"])
                    stats["applied"] += 1
                else:
                    link.status = "failed"
                    link.error_message = "Link not found in current HTML content"
                    link.save(update_fields=["status", "error_message"])
                    stats["failed"] += 1

        # Save the modified HTML back to the object
        if any_replaced:
            setattr(obj, field_name, str(soup))
            obj.save(update_fields=[field_name])

    def _get_source_object_and_field(self, link: ContentLink):
        """
        Get the source Django object and field name for a ContentLink.

        Returns (object, field_name) tuple.
        """
        field_map = {
            "product_full_desc": ("source_product", "full_description"),
            "product_short_desc": ("source_product", "short_description"),
            "blog_post_content": ("source_blog_post", "simple_content"),
            "category_description": ("source_category", "description"),
        }

        fk_field, model_field = field_map.get(link.source_type, (None, None))
        if not fk_field:
            return None, None

        obj = getattr(link, fk_field, None)
        return obj, model_field

    def get_stats(self) -> dict:
        """Get processing statistics."""
        return self.stats.copy()
