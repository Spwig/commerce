"""
Feed Service - Core service for generating product feeds.

Converts Spwig products to standardized feed format and uses
formatters to output XML, CSV, or JSON.
"""

import logging
from typing import Dict, Any, List, Optional, Iterator, Type
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import QuerySet, Prefetch
from django.utils import timezone

from core.utils import get_default_currency
from .formatters.base import BaseFeedFormatter, ProductFeedItem
from .formatters import XMLFeedFormatter, CSVFeedFormatter, JSONFeedFormatter

logger = logging.getLogger(__name__)


class FeedService:
    """
    Service for generating product feeds.

    Handles:
    - Converting Spwig products to ProductFeedItem format
    - Applying attribute mapping from provider config
    - Generating feeds in various formats (XML, CSV, JSON)
    - Feed caching and storage
    """

    # Available formatters
    FORMATTERS: Dict[str, Type[BaseFeedFormatter]] = {
        'xml': XMLFeedFormatter,
        'csv': CSVFeedFormatter,
        'json': JSONFeedFormatter,
    }

    def __init__(self, account: 'FeedProviderAccount'):
        """
        Initialize feed service for a specific provider account.

        Args:
            account: FeedProviderAccount instance
        """
        from product_feeds.models import FeedProviderAccount
        self.account = account
        self.config = account.config or {}
        self.attribute_mapping = self.config.get('attribute_mapping', {})

    def generate_feed(
        self,
        format: str = 'xml',
        product_ids: Optional[List[int]] = None,
        save_to_db: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a complete product feed.

        Args:
            format: Feed format ('xml', 'csv', 'json')
            product_ids: Optional list of specific product IDs to include
            save_to_db: Whether to save generated feed to database
            metadata: Optional feed metadata

        Returns:
            Generated feed content as string

        Raises:
            ValueError: If format is not supported
        """
        if format not in self.FORMATTERS:
            raise ValueError(f"Unsupported feed format: {format}")

        # Get products
        products = self._get_products_queryset(product_ids)

        # Convert to feed items
        feed_items = self._convert_products_to_feed_items(products)

        # Get formatter
        formatter_class = self.FORMATTERS[format]
        formatter_config = self._get_formatter_config(format)
        formatter = formatter_class(config=formatter_config)

        # Build metadata
        feed_metadata = self._build_feed_metadata(metadata)

        # Generate feed
        feed_content = formatter.format_feed(feed_items, feed_metadata)

        # Save to database if requested
        if save_to_db:
            self._save_feed_to_db(feed_content, format, len(feed_items))

        return feed_content

    def generate_feed_streaming(
        self,
        format: str = 'xml',
        product_ids: Optional[List[int]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Iterator[str]:
        """
        Generate feed content as a stream for large catalogs.

        Args:
            format: Feed format
            product_ids: Optional list of specific product IDs
            metadata: Optional feed metadata

        Yields:
            Feed content chunks
        """
        if format not in self.FORMATTERS:
            raise ValueError(f"Unsupported feed format: {format}")

        # Get products iterator
        products = self._get_products_queryset(product_ids)

        # Convert to feed items iterator
        feed_items = self._convert_products_to_feed_items_iterator(products)

        # Get formatter
        formatter_class = self.FORMATTERS[format]
        formatter_config = self._get_formatter_config(format)
        formatter = formatter_class(config=formatter_config)

        # Build metadata
        feed_metadata = self._build_feed_metadata(metadata)

        # Stream feed
        yield from formatter.stream_feed(feed_items, feed_metadata)

    def _get_products_queryset(self, product_ids: Optional[List[int]] = None) -> QuerySet:
        """
        Get products queryset with optimized loading.

        Args:
            product_ids: Optional list of specific product IDs

        Returns:
            Optimized QuerySet of products
        """
        from catalog.models import Product, ProductImage

        # Base queryset - only active, published products
        queryset = Product.objects.filter(
            is_active=True,
            status='published'
        ).select_related(
            'category',
            'brand',
            'primary_image',
        ).prefetch_related(
            Prefetch(
                'images',
                queryset=ProductImage.objects.filter(is_active=True).order_by('sort_order')
            ),
        )

        # Apply product filter if specified
        if product_ids:
            queryset = queryset.filter(id__in=product_ids)

        # Apply config filters
        filters = self.config.get('product_filters', {})
        if filters:
            if filters.get('categories'):
                queryset = queryset.filter(category_id__in=filters['categories'])
            if filters.get('exclude_out_of_stock'):
                queryset = queryset.filter(stock_quantity__gt=0)
            if filters.get('min_price'):
                queryset = queryset.filter(price__gte=filters['min_price'])

        return queryset.order_by('id')

    def _convert_products_to_feed_items(self, products: QuerySet) -> List[ProductFeedItem]:
        """
        Convert products queryset to list of ProductFeedItem.

        Args:
            products: QuerySet of Product objects

        Returns:
            List of ProductFeedItem objects
        """
        return list(self._convert_products_to_feed_items_iterator(products))

    def _convert_products_to_feed_items_iterator(self, products: QuerySet) -> Iterator[ProductFeedItem]:
        """
        Convert products to feed items as an iterator.

        Args:
            products: QuerySet of Product objects

        Yields:
            ProductFeedItem objects
        """
        from django.contrib.sites.models import Site

        # Get site for building URLs
        try:
            site = Site.objects.get_current()
            base_url = f"https://{site.domain}"
        except Exception:
            base_url = getattr(settings, 'SITE_URL', 'https://example.com')

        for product in products.iterator():
            try:
                yield self._product_to_feed_item(product, base_url)
            except Exception as e:
                logger.warning(f"Failed to convert product {product.id}: {e}")
                continue

    def _product_to_feed_item(self, product: 'Product', base_url: str) -> ProductFeedItem:
        """
        Convert a single Product to ProductFeedItem.

        Args:
            product: Product model instance
            base_url: Base URL for building links

        Returns:
            ProductFeedItem instance
        """
        # Get default language content
        default_lang = getattr(settings, 'LANGUAGE_CODE', 'en').split('-')[0]
        translations = product.translations.get(default_lang, {})

        # Build title and description
        title = translations.get('name', product.name)
        description = translations.get('description_text', '')
        if not description:
            description = translations.get('short_description_text', product.name)

        # Build product URL
        link = f"{base_url}/product/{product.slug}/"

        # Get primary image
        image_link = ''
        if hasattr(product, 'primary_image') and product.primary_image:
            if hasattr(product.primary_image, 'image') and product.primary_image.image:
                image_link = f"{base_url}{product.primary_image.image.url}"
            elif hasattr(product.primary_image, 'asset') and product.primary_image.asset:
                image_link = f"{base_url}{product.primary_image.asset.file.url}"

        # Get additional images
        additional_images = []
        if hasattr(product, 'images'):
            for img in list(product.images.all())[:10]:
                if hasattr(img, 'image') and img.image:
                    additional_images.append(f"{base_url}{img.image.url}")
                elif hasattr(img, 'asset') and img.asset:
                    additional_images.append(f"{base_url}{img.asset.file.url}")

        # Build price string
        price = self._format_price(product)
        sale_price = self._format_sale_price(product)
        sale_effective_date = self._format_sale_effective_date(product)

        # Determine availability
        availability = self._get_availability(product)

        # Get category path
        product_type = self._get_category_path(product)

        # Get brand
        brand_name = product.brand.name if product.brand else ''

        # Get identifiers from imported_meta or specifications
        gtin = ''
        mpn = ''
        if product.imported_meta:
            gtin = product.imported_meta.get('gtin', '') or product.imported_meta.get('ean', '') or product.imported_meta.get('upc', '')
            mpn = product.imported_meta.get('mpn', '')
        if product.specifications:
            gtin = gtin or product.specifications.get('gtin', '') or product.specifications.get('ean', '')
            mpn = mpn or product.specifications.get('mpn', '')

        # Get product attributes
        color = product.specifications.get('color', '') if product.specifications else ''
        size = product.specifications.get('size', '') if product.specifications else ''
        material = product.specifications.get('material', '') if product.specifications else ''
        gender = product.specifications.get('gender', '') if product.specifications else ''
        age_group = product.specifications.get('age_group', '') if product.specifications else ''

        # Item group ID for variants
        item_group_id = ''
        if product.product_type == 'variable' and hasattr(product, 'parent_product'):
            item_group_id = str(product.parent_product.id) if product.parent_product else ''

        # Build feed item
        return ProductFeedItem(
            id=str(product.id),
            title=title[:150],  # Google limit
            description=description[:5000],  # Google limit
            link=link,
            image_link=image_link,
            price=price,
            availability=availability,
            product_type=product_type,
            google_product_category=self._get_google_category(product),
            brand=brand_name,
            gtin=gtin,
            mpn=mpn or product.sku,
            sale_price=sale_price,
            sale_price_effective_date=sale_effective_date,
            condition='new',  # Default to new
            color=color,
            size=size,
            material=material,
            gender=gender,
            age_group=age_group,
            item_group_id=item_group_id,
            additional_image_links=additional_images,
            quantity=self._get_stock_quantity(product),
            custom_label_0=self._get_custom_label(product, 0),
            custom_label_1=self._get_custom_label(product, 1),
            custom_label_2=self._get_custom_label(product, 2),
            custom_label_3=self._get_custom_label(product, 3),
            custom_label_4=self._get_custom_label(product, 4),
        )

    def _format_price(self, product: 'Product') -> str:
        """Format product price as 'XX.XX CUR' string."""
        if hasattr(product.price, 'amount') and hasattr(product.price, 'currency'):
            return f"{product.price.amount:.2f} {product.price.currency}"
        return f"{float(product.price):.2f} {get_default_currency()}"

    def _format_sale_price(self, product: 'Product') -> str:
        """Get sale price if applicable."""
        if product.sale_type == 'none':
            return ''

        now = timezone.now()

        # Check sale dates
        if product.sale_start_date and now < product.sale_start_date:
            return ''
        if product.sale_end_date and now > product.sale_end_date:
            return ''

        # Calculate sale price
        if product.sale_type == 'fixed_price' and product.sale_value:
            sale_amount = float(product.sale_value)
        elif product.sale_type == 'amount_off' and product.sale_value:
            sale_amount = float(product.price.amount) - float(product.sale_value)
        elif product.sale_type == 'percentage_off' and product.sale_value:
            sale_amount = float(product.price.amount) * (1 - float(product.sale_value) / 100)
        else:
            return ''

        if sale_amount <= 0:
            return ''

        currency = product.price.currency if hasattr(product.price, 'currency') else get_default_currency()
        return f"{sale_amount:.2f} {currency}"

    def _format_sale_effective_date(self, product: 'Product') -> str:
        """Format sale effective date range."""
        if product.sale_type == 'none':
            return ''

        if not product.sale_start_date and not product.sale_end_date:
            return ''

        start = product.sale_start_date.strftime('%Y-%m-%dT%H:%M%z') if product.sale_start_date else ''
        end = product.sale_end_date.strftime('%Y-%m-%dT%H:%M%z') if product.sale_end_date else ''

        if start and end:
            return f"{start}/{end}"
        elif end:
            return f"/{end}"
        return ''

    def _get_availability(self, product: 'Product') -> str:
        """Determine product availability status."""
        if not product.is_active or product.status == 'discontinued':
            return 'out_of_stock'

        # Check stock quantity if available
        stock = self._get_stock_quantity(product)
        if stock == 0:
            return 'out_of_stock'
        elif stock < 0:  # Backorder allowed
            return 'backorder'

        return 'in_stock'

    def _get_stock_quantity(self, product: 'Product') -> int:
        """Get stock quantity from product."""
        if hasattr(product, 'stock_quantity'):
            return product.stock_quantity or 0
        if hasattr(product, 'inventory') and product.inventory:
            return product.inventory.quantity or 0
        return 0

    def _get_category_path(self, product: 'Product') -> str:
        """Get full category path for product_type field."""
        if not product.category:
            return ''

        path_parts = []
        category = product.category
        while category:
            path_parts.insert(0, category.name)
            category = category.parent

        return ' > '.join(path_parts)

    def _get_google_category(self, product: 'Product') -> str:
        """Get Google product category taxonomy ID."""
        # Check if mapped in config
        category_mapping = self.config.get('google_category_mapping', {})
        if product.category and str(product.category.id) in category_mapping:
            return category_mapping[str(product.category.id)]

        # Check if stored on category
        if product.category and hasattr(product.category, 'imported_meta'):
            google_cat = product.category.imported_meta.get('google_product_category', '')
            if google_cat:
                return google_cat

        return ''

    def _get_custom_label(self, product: 'Product', index: int) -> str:
        """Get custom label value for segmentation."""
        custom_labels = self.config.get('custom_labels', {})
        label_config = custom_labels.get(f'label_{index}', {})

        if not label_config:
            return ''

        # Labels can be based on various product attributes
        label_type = label_config.get('type', '')

        if label_type == 'category':
            return product.category.name if product.category else ''
        elif label_type == 'brand':
            return product.brand.name if product.brand else ''
        elif label_type == 'price_tier':
            return self._get_price_tier(product, label_config.get('tiers', []))
        elif label_type == 'margin_tier':
            return self._get_margin_tier(product, label_config.get('tiers', []))
        elif label_type == 'sale_status':
            return 'On Sale' if product.sale_type != 'none' else 'Regular Price'
        elif label_type == 'custom':
            return label_config.get('value', '')

        return ''

    def _get_price_tier(self, product: 'Product', tiers: List[Dict]) -> str:
        """Determine price tier label."""
        if not tiers:
            return ''

        price = float(product.price.amount) if hasattr(product.price, 'amount') else float(product.price)

        for tier in tiers:
            if price <= tier.get('max', float('inf')):
                return tier.get('label', '')

        return ''

    def _get_margin_tier(self, product: 'Product', tiers: List[Dict]) -> str:
        """Determine margin tier label."""
        if not tiers or not product.cost:
            return ''

        price = float(product.price.amount) if hasattr(product.price, 'amount') else float(product.price)
        cost = float(product.cost.amount) if hasattr(product.cost, 'amount') else float(product.cost)

        if cost <= 0:
            return ''

        margin = ((price - cost) / price) * 100

        for tier in tiers:
            if margin <= tier.get('max', float('inf')):
                return tier.get('label', '')

        return ''

    def _get_formatter_config(self, format: str) -> Dict[str, Any]:
        """Get formatter-specific configuration."""
        format_config = self.config.get('format_config', {})
        return format_config.get(format, {})

    def _build_feed_metadata(self, custom_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build feed metadata."""
        from django.contrib.sites.models import Site

        try:
            site = Site.objects.get_current()
            site_name = site.name
            site_url = f"https://{site.domain}"
        except Exception:
            site_name = 'Store'
            site_url = getattr(settings, 'SITE_URL', 'https://example.com')

        metadata = {
            'title': f'{site_name} Product Feed',
            'description': f'Product catalog for {site_name}',
            'link': site_url,
            'updated': timezone.now().isoformat(),
        }

        if custom_metadata:
            metadata.update(custom_metadata)

        return metadata

    def _save_feed_to_db(self, content: str, format: str, product_count: int) -> 'ProductFeed':
        """
        Save generated feed to database.

        Args:
            content: Feed content string
            format: Feed format
            product_count: Number of products in feed

        Returns:
            ProductFeed instance
        """
        from product_feeds.models import ProductFeed

        # Calculate expiry based on config
        cache_hours = self.config.get('cache_hours', 24)
        expires_at = timezone.now() + timedelta(hours=cache_hours)

        feed = ProductFeed.objects.create(
            account=self.account,
            feed_format=format,
            content=content if len(content) < 1_000_000 else '',  # Store inline if small
            file_size=len(content.encode('utf-8')),
            product_count=product_count,
            expires_at=expires_at,
            stats={
                'generated_at': timezone.now().isoformat(),
                'product_count': product_count,
                'format': format,
            }
        )

        # Save large feeds to file
        if len(content) >= 1_000_000:
            self._save_feed_to_file(feed, content)

        # Update account stats
        self.account.products_in_feed = product_count
        self.account.save(update_fields=['products_in_feed', 'updated_at'])

        return feed

    def _save_feed_to_file(self, feed: 'ProductFeed', content: str) -> None:
        """Save large feed to file system."""
        import os
        from django.conf import settings

        # Create feeds directory
        feeds_dir = os.path.join(settings.MEDIA_ROOT, 'product_feeds', str(self.account.id))
        os.makedirs(feeds_dir, exist_ok=True)

        # Generate filename
        filename = f"feed_{feed.id}.{feed.feed_format}"
        filepath = os.path.join(feeds_dir, filename)

        # Write content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        # Update feed record
        feed.file_path = filepath
        feed.save(update_fields=['file_path'])

    def get_latest_feed(self, format: Optional[str] = None) -> Optional['ProductFeed']:
        """
        Get the latest cached feed.

        Args:
            format: Optional format filter

        Returns:
            ProductFeed instance or None
        """
        from product_feeds.models import ProductFeed

        queryset = ProductFeed.objects.filter(
            account=self.account,
            expires_at__gt=timezone.now()
        )

        if format:
            queryset = queryset.filter(feed_format=format)

        return queryset.order_by('-generated_at').first()
