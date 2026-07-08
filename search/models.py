from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class SearchSettings(models.Model):
    """
    Singleton model for merchant-configurable search settings.
    Following the pattern of BlogSettings, AffiliateSettings.
    """

    # General Settings
    is_enabled = models.BooleanField(
        _('Search Enabled'),
        default=True,
        help_text=_('Enable or disable search functionality globally')
    )
    min_query_length = models.PositiveIntegerField(
        _('Minimum Query Length'),
        default=2,
        help_text=_('Minimum number of characters required to trigger search')
    )

    # Autocomplete Settings
    autocomplete_enabled = models.BooleanField(
        _('Autocomplete Enabled'),
        default=True,
        help_text=_('Show predictive search suggestions as user types')
    )
    autocomplete_max_results = models.PositiveIntegerField(
        _('Autocomplete Max Results'),
        default=8,
        help_text=_('Maximum number of suggestions per content type')
    )
    autocomplete_debounce_ms = models.PositiveIntegerField(
        _('Autocomplete Debounce (ms)'),
        default=300,
        help_text=_('Delay in milliseconds before triggering autocomplete')
    )
    show_thumbnails = models.BooleanField(
        _('Show Thumbnails'),
        default=True,
        help_text=_('Display product/content thumbnails in search results')
    )

    # Autocomplete Display Settings - Products
    autocomplete_product_thumbnail = models.BooleanField(
        _('Show Product Thumbnail'),
        default=True,
        help_text=_('Display product images in autocomplete dropdown')
    )
    autocomplete_product_description = models.BooleanField(
        _('Show Product Description'),
        default=False,
        help_text=_('Display short description in autocomplete dropdown')
    )
    autocomplete_product_price = models.BooleanField(
        _('Show Product Price'),
        default=True,
        help_text=_('Display price in autocomplete dropdown')
    )
    autocomplete_product_sku = models.BooleanField(
        _('Show Product SKU'),
        default=True,
        help_text=_('Display SKU in autocomplete dropdown')
    )
    autocomplete_product_stock_status = models.BooleanField(
        _('Show Product Stock Status'),
        default=False,
        help_text=_('Display stock availability badge in autocomplete dropdown')
    )

    # Autocomplete Display Settings - Blog Posts
    autocomplete_blog_thumbnail = models.BooleanField(
        _('Show Blog Featured Image'),
        default=True,
        help_text=_('Display featured image in blog post autocomplete results')
    )
    autocomplete_blog_excerpt = models.BooleanField(
        _('Show Blog Excerpt'),
        default=True,
        help_text=_('Display excerpt in blog post autocomplete results')
    )
    autocomplete_blog_excerpt_length = models.PositiveIntegerField(
        _('Blog Excerpt Length'),
        default=60,
        help_text=_('Maximum characters to show for blog excerpts')
    )

    # Autocomplete Display Settings - Categories
    autocomplete_category_thumbnail = models.BooleanField(
        _('Show Category Thumbnail'),
        default=False,
        help_text=_('Display category image in autocomplete dropdown')
    )
    autocomplete_category_product_count = models.BooleanField(
        _('Show Category Product Count'),
        default=True,
        help_text=_('Display product count in category autocomplete results')
    )

    # Autocomplete Display Settings - Brands
    autocomplete_brand_logo = models.BooleanField(
        _('Show Brand Logo'),
        default=False,
        help_text=_('Display brand logo in autocomplete dropdown')
    )
    autocomplete_brand_product_count = models.BooleanField(
        _('Show Brand Product Count'),
        default=True,
        help_text=_('Display product count in brand autocomplete results')
    )

    # Content Type Settings
    search_products = models.BooleanField(
        _('Search Products'),
        default=True,
        help_text=_('Include products in search results')
    )
    search_categories = models.BooleanField(
        _('Search Categories'),
        default=True,
        help_text=_('Include categories in search results')
    )
    search_brands = models.BooleanField(
        _('Search Brands'),
        default=True,
        help_text=_('Include brands in search results')
    )
    search_blog_posts = models.BooleanField(
        _('Search Blog Posts'),
        default=True,
        help_text=_('Include blog posts in search results')
    )

    # Deep Indexing Settings
    index_skus = models.BooleanField(
        _('Index SKUs'),
        default=True,
        help_text=_('Include product SKUs in search')
    )
    index_attributes = models.BooleanField(
        _('Index Attributes'),
        default=True,
        help_text=_('Include product attributes (color, size, etc.) in search')
    )
    index_custom_fields = models.BooleanField(
        _('Index Custom Fields'),
        default=True,
        help_text=_('Include custom product fields in search')
    )
    index_reviews = models.BooleanField(
        _('Index Reviews'),
        default=True,
        help_text=_('Include product review content in search')
    )
    index_documents = models.BooleanField(
        _('Index Documents'),
        default=False,
        help_text=_('Index text content from digital asset documents (PDFs, Office files)')
    )

    # Fuzzy Matching Settings
    fuzzy_enabled = models.BooleanField(
        _('Fuzzy Matching Enabled'),
        default=True,
        help_text=_('Enable typo tolerance in search queries')
    )
    fuzzy_threshold = models.DecimalField(
        _('Fuzzy Threshold'),
        max_digits=3,
        decimal_places=2,
        default=0.80,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_('Similarity threshold for fuzzy matching (0-1, higher = stricter)')
    )
    fuzzy_max_edits = models.PositiveIntegerField(
        _('Fuzzy Max Edits'),
        default=2,
        help_text=_('Maximum character edits allowed for fuzzy matching')
    )

    # Relevance Weight Settings (0.0 - 2.0)
    weight_name = models.DecimalField(
        _('Name Weight'),
        max_digits=3,
        decimal_places=2,
        default=1.50,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_('Relevance weight for product/item names')
    )
    weight_sku = models.DecimalField(
        _('SKU Weight'),
        max_digits=3,
        decimal_places=2,
        default=1.20,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_('Relevance weight for SKUs')
    )
    weight_description = models.DecimalField(
        _('Description Weight'),
        max_digits=3,
        decimal_places=2,
        default=0.80,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_('Relevance weight for descriptions')
    )
    weight_attributes = models.DecimalField(
        _('Attributes Weight'),
        max_digits=3,
        decimal_places=2,
        default=0.70,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_('Relevance weight for product attributes and custom fields')
    )
    weight_reviews = models.DecimalField(
        _('Reviews Weight'),
        max_digits=3,
        decimal_places=2,
        default=0.50,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_('Relevance weight for review content')
    )
    weight_categories = models.DecimalField(
        _('Categories Weight'),
        max_digits=3,
        decimal_places=2,
        default=0.80,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_('Relevance weight for category names')
    )
    weight_brands = models.DecimalField(
        _('Brands Weight'),
        max_digits=3,
        decimal_places=2,
        default=0.70,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_('Relevance weight for brand names')
    )
    weight_blog_posts = models.DecimalField(
        _('Blog Posts Weight'),
        max_digits=3,
        decimal_places=2,
        default=0.60,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_('Relevance weight for blog post content')
    )

    # Caching Settings
    cache_autocomplete_ttl = models.PositiveIntegerField(
        _('Autocomplete Cache TTL'),
        default=60,
        help_text=_('Time to live for autocomplete cache in seconds')
    )
    cache_results_ttl = models.PositiveIntegerField(
        _('Results Cache TTL'),
        default=300,
        help_text=_('Time to live for full search results cache in seconds')
    )

    # Analytics Settings
    track_search_queries = models.BooleanField(
        _('Track Search Queries'),
        default=True,
        help_text=_('Store search queries for analytics and trending searches')
    )
    track_clicks = models.BooleanField(
        _('Track Clicks'),
        default=True,
        help_text=_('Track clicks on search results for analytics')
    )
    track_zero_results = models.BooleanField(
        _('Track Zero Results'),
        default=True,
        help_text=_('Flag and track queries that return no results')
    )

    # Pagination Settings
    results_per_page = models.PositiveIntegerField(
        _('Results Per Page'),
        default=20,
        help_text=_('Number of results to display per page')
    )

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Search Settings')
        verbose_name_plural = _('Search Settings')

    def __str__(self):
        return str(_('Search Settings'))

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create the singleton settings instance."""
        settings_obj, _ = cls.objects.get_or_create(pk=1)
        return settings_obj


class SearchEngine(models.Model):
    """
    Multiple search engines for different contexts (shop vs blog).
    """
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('Engine name (e.g., "Shop Search", "Blog Search")')
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=100,
        unique=True,
        help_text=_('URL-safe identifier')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Enable or disable this search engine')
    )
    content_types = models.JSONField(
        _('Content Types'),
        default=list,
        blank=True,
        help_text=_('List of searchable content types for this engine (e.g., ["product", "category"])')
    )
    weight_overrides = models.JSONField(
        _('Weight Overrides'),
        default=dict,
        blank=True,
        help_text=_('Engine-specific weight adjustments (e.g., {"weight_name": 2.0})')
    )
    excluded_categories = models.ManyToManyField(
        'catalog.Category',
        blank=True,
        related_name='excluded_from_engines',
        verbose_name=_('Excluded Categories'),
        help_text=_('Categories to exclude from this engine')
    )
    excluded_brands = models.ManyToManyField(
        'catalog.Brand',
        blank=True,
        related_name='excluded_from_engines',
        verbose_name=_('Excluded Brands'),
        help_text=_('Brands to exclude from this engine')
    )

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Search Engine')
        verbose_name_plural = _('Search Engines')
        ordering = ['name']

    def __str__(self):
        return self.name


class Synonym(models.Model):
    """
    Merchant-defined term mappings for search expansion.
    """
    term = models.CharField(
        _('Term'),
        max_length=100,
        help_text=_('Original search term')
    )
    synonyms = models.JSONField(
        _('Synonyms'),
        default=list,
        help_text=_('List of equivalent terms (e.g., ["sweater", "pullover"])')
    )
    is_bidirectional = models.BooleanField(
        _('Bidirectional'),
        default=True,
        help_text=_('Apply mapping both ways (e.g., jumper ↔ sweater)')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    language = models.CharField(
        _('Language'),
        max_length=10,
        blank=True,
        null=True,
        help_text=_('Language code (e.g., "en", "es"). Leave blank for all languages.')
    )
    engine = models.ForeignKey(
        SearchEngine,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='synonyms',
        verbose_name=_('Search Engine'),
        help_text=_('Apply to specific engine only. Leave blank for all engines.')
    )

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Synonym')
        verbose_name_plural = _('Synonyms')
        ordering = ['term']
        indexes = [
            models.Index(fields=['term', 'is_active']),
            models.Index(fields=['language', 'is_active']),
        ]

    def __str__(self):
        synonyms_preview = ', '.join(self.synonyms[:3])
        if len(self.synonyms) > 3:
            synonyms_preview += '...'
        return f'{self.term} → {synonyms_preview}'


class SearchRedirect(models.Model):
    """
    Smart redirects for specific search terms.
    """
    MATCH_TYPE_CHOICES = [
        ('exact', _('Exact Match')),
        ('contains', _('Contains')),
        ('starts_with', _('Starts With')),
        ('regex', _('Regular Expression')),
    ]

    REDIRECT_TYPE_CHOICES = [
        ('temporary', _('Temporary (302)')),
        ('permanent', _('Permanent (301)')),
    ]

    term = models.CharField(
        _('Search Term'),
        max_length=200,
        help_text=_('Search term to trigger redirect')
    )
    match_type = models.CharField(
        _('Match Type'),
        max_length=20,
        choices=MATCH_TYPE_CHOICES,
        default='exact',
        help_text=_('How to match the search term')
    )
    redirect_url = models.CharField(
        _('Redirect URL'),
        max_length=500,
        help_text=_('Target URL (can be relative like /products/sale/ or absolute)')
    )
    redirect_type = models.CharField(
        _('Redirect Type'),
        max_length=20,
        choices=REDIRECT_TYPE_CHOICES,
        default='temporary',
        help_text=_('HTTP redirect status code')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True
    )
    hit_count = models.PositiveIntegerField(
        _('Hit Count'),
        default=0,
        help_text=_('Number of times this redirect was triggered')
    )
    engine = models.ForeignKey(
        SearchEngine,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='redirects',
        verbose_name=_('Search Engine'),
        help_text=_('Apply to specific engine only. Leave blank for all engines.')
    )

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Search Redirect')
        verbose_name_plural = _('Search Redirects')
        ordering = ['-hit_count', 'term']
        indexes = [
            models.Index(fields=['term', 'match_type', 'is_active']),
        ]

    def __str__(self):
        return f'{self.term} → {self.redirect_url}'

    def increment_hit_count(self):
        """Increment the hit count atomically."""
        SearchRedirect.objects.filter(pk=self.pk).update(
            hit_count=models.F('hit_count') + 1
        )


class SearchQuery(models.Model):
    """
    Track search queries for analytics and trending searches.
    """
    query = models.CharField(
        _('Query'),
        max_length=500,
        help_text=_('Original search query')
    )
    query_normalized = models.CharField(
        _('Normalized Query'),
        max_length=500,
        db_index=True,
        help_text=_('Lowercase, trimmed query for aggregation')
    )
    result_count = models.PositiveIntegerField(
        _('Result Count'),
        default=0,
        help_text=_('Number of results returned')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='search_queries',
        verbose_name=_('User')
    )
    session_key = models.CharField(
        _('Session Key'),
        max_length=40,
        blank=True,
        help_text=_('For anonymous user tracking')
    )
    language = models.CharField(
        _('Language'),
        max_length=10,
        default='en',
        help_text=_('Language code of the search')
    )
    engine = models.ForeignKey(
        SearchEngine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='queries',
        verbose_name=_('Search Engine')
    )
    is_zero_result = models.BooleanField(
        _('Zero Results'),
        default=False,
        help_text=_('Whether this query returned no results')
    )
    response_time_ms = models.PositiveIntegerField(
        _('Response Time (ms)'),
        default=0,
        help_text=_('Search response time in milliseconds')
    )

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Search Query')
        verbose_name_plural = _('Search Queries')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['query_normalized', 'created_at']),
            models.Index(fields=['is_zero_result', 'created_at']),
            models.Index(fields=['language', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'"{self.query}" ({self.result_count} results)'

    def save(self, *args, **kwargs):
        # Normalize the query
        self.query_normalized = self.query.lower().strip()
        self.is_zero_result = self.result_count == 0
        super().save(*args, **kwargs)


class SearchClick(models.Model):
    """
    Track clicks on search results for analytics.
    """
    search_query = models.ForeignKey(
        SearchQuery,
        on_delete=models.CASCADE,
        related_name='clicks',
        verbose_name=_('Search Query')
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('Content Type')
    )
    object_id = models.PositiveIntegerField(_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    position = models.PositiveIntegerField(
        _('Position'),
        default=0,
        help_text=_('Position of the clicked item in search results')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='search_clicks',
        verbose_name=_('User')
    )
    session_key = models.CharField(
        _('Session Key'),
        max_length=40,
        blank=True
    )

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Search Click')
        verbose_name_plural = _('Search Clicks')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['search_query', 'created_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f'Click on {self.content_type.model} #{self.object_id}'


class SearchIndex(models.Model):
    """
    Pre-indexed document content for document search (PDFs, Office files).
    """
    FILE_TYPE_CHOICES = [
        ('pdf', _('PDF')),
        ('docx', _('Word Document')),
        ('xlsx', _('Excel Spreadsheet')),
        ('txt', _('Text File')),
        ('other', _('Other')),
    ]

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('Content Type')
    )
    object_id = models.PositiveIntegerField(_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    extracted_text = models.TextField(
        _('Extracted Text'),
        blank=True,
        help_text=_('Text content extracted from the document')
    )
    file_type = models.CharField(
        _('File Type'),
        max_length=10,
        choices=FILE_TYPE_CHOICES,
        default='other'
    )
    checksum = models.CharField(
        _('Checksum'),
        max_length=64,
        blank=True,
        help_text=_('File checksum for change detection')
    )

    indexed_at = models.DateTimeField(_('Indexed At'), auto_now=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Search Index')
        verbose_name_plural = _('Search Indexes')
        unique_together = ['content_type', 'object_id']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['file_type']),
        ]

    def __str__(self):
        return f'Index for {self.content_type.model} #{self.object_id}'
