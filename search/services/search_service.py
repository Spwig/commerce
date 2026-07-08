"""
Core search service with language-aware searching.

Provides autocomplete, full search, synonym expansion, and redirect checking.
Searches both base fields and translations JSONField for multilingual support.
"""
import hashlib
import time
import re
from typing import Optional, List, Dict, Any
from decimal import Decimal

from django.db.models import Q, F, Value, Case, When, IntegerField
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from core.utils import get_default_currency

from ..models import (
    SearchSettings,
    SearchEngine,
    Synonym,
    SearchRedirect,
    SearchQuery,
)


class SearchService:
    """
    Core search orchestration service with language support.

    Handles autocomplete, full search, synonym expansion, redirect checking,
    and relevance scoring with caching.
    """

    def __init__(self):
        self._settings = None
        self._settings_loaded_at = None

    @property
    def settings(self) -> SearchSettings:
        """Get cached search settings."""
        # Cache settings for 60 seconds in memory
        if self._settings is None or (
            self._settings_loaded_at and
            time.time() - self._settings_loaded_at > 60
        ):
            self._settings = SearchSettings.get_settings()
            self._settings_loaded_at = time.time()
        return self._settings

    def get_engine(self, engine_slug: str = 'shop') -> Optional[SearchEngine]:
        """Get a search engine by slug."""
        try:
            return SearchEngine.objects.get(slug=engine_slug, is_active=True)
        except SearchEngine.DoesNotExist:
            return None

    def _get_cache_key(self, prefix: str, query: str, language: str,
                       engine: str = 'shop', **kwargs) -> str:
        """Generate a cache key including language."""
        # Create a hash of query + filters for the cache key
        key_data = f"{query}:{language}:{engine}"
        for k, v in sorted(kwargs.items()):
            if v is not None:
                key_data += f":{k}={v}"
        key_hash = hashlib.md5(key_data.encode()).hexdigest()[:16]
        return f"search:{prefix}:{engine}:{language}:{key_hash}"

    def _build_translation_query(self, field: str, query: str, language: str) -> Q:
        """
        Build Q object that searches both base field and translation.

        For language='es' and field='name':
        Q(name__icontains=query) | Q(translations__es__name__icontains=query)
        """
        base_query = Q(**{f'{field}__icontains': query})

        if language and language != 'en':
            # JSONField lookup: translations__<lang>__<field>__icontains
            trans_lookup = f'translations__{language}__{field}__icontains'
            trans_query = Q(**{trans_lookup: query})
            return base_query | trans_query

        return base_query

    def _get_localized_value(self, obj, field: str, language: str) -> str:
        """
        Get field value in requested language, falling back to base field.

        Checks obj.translations[language][field] first, then getattr(obj, field).
        """
        if language and language != 'en' and hasattr(obj, 'translations'):
            translations = obj.translations or {}
            lang_data = translations.get(language, {})
            if field in lang_data and lang_data[field]:
                return lang_data[field]
        return getattr(obj, field, '') or ''

    def check_redirect(self, query: str, engine_slug: str = 'shop') -> Optional[Dict]:
        """
        Check if query triggers a redirect.

        Returns redirect info dict or None.
        """
        query_lower = query.lower().strip()

        # Get redirects for this engine (or global redirects)
        redirects = SearchRedirect.objects.filter(
            is_active=True
        ).filter(
            Q(engine__isnull=True) | Q(engine__slug=engine_slug)
        )

        for redirect in redirects:
            term = redirect.term.lower()
            matched = False

            if redirect.match_type == 'exact':
                matched = query_lower == term
            elif redirect.match_type == 'contains':
                matched = term in query_lower
            elif redirect.match_type == 'starts_with':
                matched = query_lower.startswith(term)
            elif redirect.match_type == 'regex':
                try:
                    matched = bool(re.search(redirect.term, query, re.IGNORECASE))
                except re.error:
                    pass

            if matched:
                # Increment hit count asynchronously
                redirect.increment_hit_count()
                return {
                    'url': redirect.redirect_url,
                    'type': redirect.redirect_type,
                    'matched_term': redirect.term,
                }

        return None

    def expand_synonyms(self, query: str, language: str = 'en',
                        engine_slug: str = 'shop') -> List[str]:
        """
        Expand query with synonyms, considering language-specific synonyms.

        Returns list of all terms to search (original + synonyms).
        """
        query_lower = query.lower().strip()
        terms = [query_lower]

        # Get synonyms for this engine and language
        synonyms = Synonym.objects.filter(
            is_active=True
        ).filter(
            Q(engine__isnull=True) | Q(engine__slug=engine_slug)
        ).filter(
            Q(language__isnull=True) | Q(language='') | Q(language=language)
        )

        for synonym in synonyms:
            term_lower = synonym.term.lower()

            # Check if query matches this synonym's term
            if term_lower == query_lower or term_lower in query_lower.split():
                terms.extend(s.lower() for s in synonym.synonyms if s.lower() not in terms)

            # Check bidirectional: if query matches any synonym
            if synonym.is_bidirectional:
                for syn in synonym.synonyms:
                    if syn.lower() == query_lower or syn.lower() in query_lower.split():
                        if term_lower not in terms:
                            terms.append(term_lower)
                        # Also add other synonyms
                        terms.extend(
                            s.lower() for s in synonym.synonyms
                            if s.lower() not in terms and s.lower() != query_lower
                        )
                        break

        return terms

    def _search_products(self, query: str, language: str, limit: int = None,
                         engine: SearchEngine = None, **filters) -> List[Dict]:
        """Search products with language support."""
        from catalog.models import Product

        # Build query for multiple terms (including synonyms)
        terms = self.expand_synonyms(query, language, engine.slug if engine else 'shop')

        q_objects = Q()
        for term in terms:
            # Name
            q_objects |= self._build_translation_query('name', term, language)

            # SKU
            if self.settings.index_skus:
                q_objects |= Q(sku__icontains=term)
                # Also search variant SKUs
                q_objects |= Q(variants__sku__icontains=term)

            # Description
            q_objects |= self._build_translation_query('short_description', term, language)
            q_objects |= self._build_translation_query('full_description', term, language)

            # Brand name
            q_objects |= Q(brand__name__icontains=term)

            # Category name
            q_objects |= Q(category__name__icontains=term)

        # Apply engine exclusions
        # Note: Product uses status='published' instead of is_active
        products = Product.objects.filter(
            q_objects,
            status='published',
        ).select_related(
            'brand', 'category'
        ).prefetch_related(
            'images'
        ).distinct()

        if engine:
            if engine.excluded_categories.exists():
                products = products.exclude(category__in=engine.excluded_categories.all())
            if engine.excluded_brands.exists():
                products = products.exclude(brand__in=engine.excluded_brands.all())

        # Apply additional filters
        if filters.get('category'):
            products = products.filter(category_id=filters['category'])
        if filters.get('brand'):
            products = products.filter(brand_id=filters['brand'])
        if filters.get('in_stock'):
            # Products that don't track inventory are always "in stock"
            # Products that track inventory need available stock > 0 or allow backorders
            products = products.with_stock_totals().filter(
                Q(track_inventory=False) |
                Q(allow_backorders=True) |
                Q(total_available__gt=0)
            )
        if filters.get('min_price'):
            products = products.filter(price__gte=filters['min_price'])
        if filters.get('max_price'):
            products = products.filter(price__lte=filters['max_price'])

        if limit:
            products = products[:limit]

        results = []
        for product in products:
            # Get localized values
            name = self._get_localized_value(product, 'name', language)
            description = self._get_localized_value(product, 'short_description', language)

            # Determine if content is translated
            is_translated = (
                language != 'en' and
                hasattr(product, 'translations') and
                product.translations and
                language in product.translations and
                'name' in product.translations[language]
            )

            # Get thumbnail using product's listing-size thumbnail (400x400)
            thumbnail = product.primary_image_listing_url

            results.append({
                'id': product.id,
                'type': 'product',
                'name': name,
                'name_base': product.name if is_translated else None,
                'slug': product.slug,
                'url': f'/product/{product.slug}/',
                'price': str(product.price.amount) if hasattr(product.price, 'amount') else str(product.price),
                'currency': str(product.price.currency) if hasattr(product.price, 'currency') else get_default_currency(),
                'thumbnail': thumbnail,
                'sku': product.sku,
                'in_stock': product.is_in_stock,
                'is_translated': is_translated,
                'description': description[:200] if description else '',
            })

        return results

    def _search_categories(self, query: str, language: str, limit: int = None,
                           engine: SearchEngine = None) -> List[Dict]:
        """Search categories with language support."""
        from catalog.models import Category

        terms = self.expand_synonyms(query, language, engine.slug if engine else 'shop')

        q_objects = Q()
        for term in terms:
            q_objects |= self._build_translation_query('name', term, language)
            q_objects |= self._build_translation_query('description', term, language)

        categories = Category.objects.filter(
            q_objects,
            is_active=True,
        ).distinct()

        if engine and engine.excluded_categories.exists():
            categories = categories.exclude(pk__in=engine.excluded_categories.all())

        if limit:
            categories = categories[:limit]

        results = []
        for category in categories:
            name = self._get_localized_value(category, 'name', language)
            is_translated = (
                language != 'en' and
                hasattr(category, 'translations') and
                category.translations and
                language in category.translations
            )

            # Get category thumbnail (uses MediaAsset thumbnail)
            thumbnail = category.get_image_thumbnail('category_thumbnail')

            results.append({
                'id': category.id,
                'type': 'category',
                'name': name,
                'name_base': category.name if is_translated else None,
                'slug': category.slug,
                'url': f'/category/{category.slug}/',
                'thumbnail': thumbnail,
                'product_count': category.products.filter(status='published').count(),
                'is_translated': is_translated,
            })

        return results

    def _search_brands(self, query: str, language: str, limit: int = None,
                       engine: SearchEngine = None) -> List[Dict]:
        """Search brands."""
        from catalog.models import Brand

        terms = self.expand_synonyms(query, language, engine.slug if engine else 'shop')

        q_objects = Q()
        for term in terms:
            q_objects |= Q(name__icontains=term)
            q_objects |= Q(description__icontains=term)

        brands = Brand.objects.filter(
            q_objects,
            is_active=True,
        ).distinct()

        if engine and engine.excluded_brands.exists():
            brands = brands.exclude(pk__in=engine.excluded_brands.all())

        if limit:
            brands = brands[:limit]

        results = []
        for brand in brands:
            # Get brand logo
            logo = None
            if hasattr(brand, 'logo') and brand.logo:
                logo = brand.logo.url

            results.append({
                'id': brand.id,
                'type': 'brand',
                'name': brand.name,
                'slug': brand.slug,
                'url': f'/brand/{brand.slug}/',
                'logo': logo,
                'product_count': brand.products.filter(status='published').count(),
            })

        return results

    def _search_blog_posts(self, query: str, language: str, limit: int = None,
                           engine: SearchEngine = None) -> List[Dict]:
        """Search blog posts with language support."""
        from blog.models import BlogPost

        terms = self.expand_synonyms(query, language, engine.slug if engine else 'shop')

        q_objects = Q()
        for term in terms:
            q_objects |= self._build_translation_query('title', term, language)
            q_objects |= self._build_translation_query('excerpt', term, language)
            q_objects |= Q(simple_content__icontains=term)
            q_objects |= Q(tags__name__icontains=term)

        posts = BlogPost.objects.filter(
            q_objects,
            status='published',
        ).select_related('featured_image').distinct()

        if limit:
            posts = posts[:limit]

        results = []
        for post in posts:
            title = self._get_localized_value(post, 'title', language)
            excerpt = self._get_localized_value(post, 'excerpt', language)
            is_translated = (
                language != 'en' and
                hasattr(post, 'translations') and
                post.translations and
                language in post.translations
            )

            # Get blog post thumbnail (featured image)
            thumbnail = None
            if hasattr(post, 'featured_image') and post.featured_image:
                thumbnail = post.featured_image.thumbnail_small

            results.append({
                'id': post.id,
                'type': 'blog_post',
                'title': title,
                'title_base': post.title if is_translated else None,
                'slug': post.slug,
                'url': f'/blog/{post.slug}/',
                'thumbnail': thumbnail,
                'excerpt': excerpt[:200] if excerpt else '',
                'is_translated': is_translated,
            })

        return results

    def autocomplete(self, query: str, language: str = 'en', engine_slug: str = 'shop',
                     limit: int = None) -> Dict[str, Any]:
        """
        Fast autocomplete with caching and language support.

        Returns grouped results by content type.
        """
        if not self.settings.is_enabled or not self.settings.autocomplete_enabled:
            return {'products': [], 'categories': [], 'brands': [], 'blog_posts': [],
                    'total_count': 0, 'query': query, 'language': language}

        query = query.strip()
        if len(query) < self.settings.min_query_length:
            return {'products': [], 'categories': [], 'brands': [], 'blog_posts': [],
                    'total_count': 0, 'query': query, 'language': language}

        # Check for redirect first
        redirect = self.check_redirect(query, engine_slug)
        if redirect:
            return {
                'redirect': redirect,
                'query': query,
                'language': language,
            }

        # Check cache
        cache_key = self._get_cache_key('auto', query, language, engine_slug)
        cached = cache.get(cache_key)
        if cached:
            return cached

        start_time = time.time()

        # Get engine
        engine = self.get_engine(engine_slug)

        # Determine limit per type
        max_results = limit or self.settings.autocomplete_max_results

        results = {
            'query': query,
            'language': language,
            'did_you_mean': None,  # Will be populated by fuzzy service
            'redirect': None,
            'products': [],
            'categories': [],
            'brands': [],
            'blog_posts': [],
        }

        # Search enabled content types
        if self.settings.search_products:
            results['products'] = self._search_products(
                query, language, limit=max_results, engine=engine
            )

        if self.settings.search_categories:
            results['categories'] = self._search_categories(
                query, language, limit=max_results, engine=engine
            )

        if self.settings.search_brands:
            results['brands'] = self._search_brands(
                query, language, limit=max_results, engine=engine
            )

        if self.settings.search_blog_posts:
            results['blog_posts'] = self._search_blog_posts(
                query, language, limit=max_results, engine=engine
            )

        # Calculate total count
        results['total_count'] = (
            len(results['products']) +
            len(results['categories']) +
            len(results['brands']) +
            len(results['blog_posts'])
        )

        # Response time
        results['response_time_ms'] = int((time.time() - start_time) * 1000)

        # Cache the results
        cache.set(cache_key, results, self.settings.cache_autocomplete_ttl)

        return results

    def search(self, query: str, language: str = 'en', engine_slug: str = 'shop',
               filters: Dict = None, page: int = 1, per_page: int = None,
               sort: str = 'relevance') -> Dict[str, Any]:
        """
        Full search with pagination, facets, and language support.

        Returns paginated results with facets for filtering.
        """
        if not self.settings.is_enabled:
            return {'results': [], 'total_count': 0, 'query': query, 'language': language}

        query = query.strip()
        filters = filters or {}
        per_page = per_page or self.settings.results_per_page

        # Check for redirect first
        redirect = self.check_redirect(query, engine_slug)
        if redirect:
            return {
                'redirect': redirect,
                'query': query,
                'language': language,
            }

        # Check cache
        cache_key = self._get_cache_key(
            'results', query, language, engine_slug,
            page=page, per_page=per_page, sort=sort, **filters
        )
        cached = cache.get(cache_key)
        if cached:
            return cached

        start_time = time.time()

        # Get engine
        engine = self.get_engine(engine_slug)

        # Get all results (we'll paginate later)
        all_results = []

        # Search enabled content types
        type_filter = filters.get('type')

        if self.settings.search_products and (not type_filter or type_filter == 'product'):
            products = self._search_products(query, language, engine=engine, **filters)
            all_results.extend(products)

        if self.settings.search_categories and (not type_filter or type_filter == 'category'):
            categories = self._search_categories(query, language, engine=engine)
            all_results.extend(categories)

        if self.settings.search_brands and (not type_filter or type_filter == 'brand'):
            brands = self._search_brands(query, language, engine=engine)
            all_results.extend(brands)

        if self.settings.search_blog_posts and (not type_filter or type_filter == 'blog_post'):
            blog_posts = self._search_blog_posts(query, language, engine=engine)
            all_results.extend(blog_posts)

        # Sort results
        if sort == 'price_asc':
            all_results.sort(key=lambda x: Decimal(x.get('price', '999999')))
        elif sort == 'price_desc':
            all_results.sort(key=lambda x: Decimal(x.get('price', '0')), reverse=True)
        elif sort == 'newest':
            # Products first (newest), then others
            all_results.sort(key=lambda x: x.get('id', 0), reverse=True)
        # 'relevance' is the default order from queries

        total_count = len(all_results)

        # Paginate
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = all_results[start_idx:end_idx]

        # Build facets
        facets = self._build_facets(all_results)

        # Get applied synonyms
        applied_synonyms = self.expand_synonyms(query, language, engine_slug)
        applied_synonyms = [s for s in applied_synonyms if s != query.lower()]

        results = {
            'query': query,
            'language': language,
            'did_you_mean': None,
            'redirect': None,
            'results': paginated_results,
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page,
            'facets': facets,
            'applied_synonyms': applied_synonyms,
            'response_time_ms': int((time.time() - start_time) * 1000),
        }

        # Cache the results
        cache.set(cache_key, results, self.settings.cache_results_ttl)

        return results

    def _build_facets(self, results: List[Dict]) -> Dict:
        """Build facets from search results."""
        facets = {
            'types': {},
            'categories': [],
            'brands': [],
            'price_range': {'min': None, 'max': None},
            'in_stock': {'true': 0, 'false': 0},
        }

        category_counts = {}
        brand_counts = {}

        for result in results:
            # Type counts
            result_type = result.get('type', 'unknown')
            facets['types'][result_type] = facets['types'].get(result_type, 0) + 1

            # Price range (products only)
            if result_type == 'product':
                try:
                    price = Decimal(result.get('price', '0'))
                    if facets['price_range']['min'] is None or price < facets['price_range']['min']:
                        facets['price_range']['min'] = price
                    if facets['price_range']['max'] is None or price > facets['price_range']['max']:
                        facets['price_range']['max'] = price

                    # Stock status
                    if result.get('in_stock'):
                        facets['in_stock']['true'] += 1
                    else:
                        facets['in_stock']['false'] += 1
                except (ValueError, TypeError):
                    pass

        # Convert price range to strings
        if facets['price_range']['min']:
            facets['price_range']['min'] = str(facets['price_range']['min'])
        if facets['price_range']['max']:
            facets['price_range']['max'] = str(facets['price_range']['max'])

        return facets

    def track_query(self, query: str, result_count: int, language: str = 'en',
                    engine_slug: str = 'shop', response_time_ms: int = 0,
                    user=None, session_key: str = '') -> Optional[SearchQuery]:
        """Track a search query for analytics."""
        if not self.settings.track_search_queries:
            return None

        engine = self.get_engine(engine_slug)

        search_query = SearchQuery.objects.create(
            query=query,
            result_count=result_count,
            language=language,
            engine=engine,
            response_time_ms=response_time_ms,
            user=user if user and user.is_authenticated else None,
            session_key=session_key,
        )

        return search_query

    # Whitelist of first-party searchable content types. Each entry maps a
    # bare model name (the public wire format) to its explicit
    # (app_label, model) tuple, so resolution is deterministic across all
    # installations — even ones where a third-party provider package
    # registers a model with the same bare name.
    SEARCHABLE_CONTENT_TYPES: dict[str, tuple[str, str]] = {
        'product':  ('catalog', 'product'),
        'category': ('catalog', 'category'),
        'brand':    ('catalog', 'brand'),
        'blogpost': ('blog', 'blogpost'),
    }

    def track_click(self, search_query_id: int, content_type_str: str, object_id: int,
                    position: int = 0, user=None, session_key: str = '') -> bool:
        """Track a click on a search result.

        content_type_str accepts either:
          - Just the model name, e.g. "product", "category", "brand", "blogpost"
          - Or the fully qualified "app_label.model" form, e.g. "catalog.product"
        The bare model form is preferred for headless frontends because they
        don't know (and shouldn't need to know) the app_label.

        Both forms are resolved through SEARCHABLE_CONTENT_TYPES, so the
        same input always points at the same first-party Spwig model even
        in installations where third-party apps register a same-named model.
        """
        if not self.settings.track_clicks:
            return False

        try:
            from ..models import SearchClick

            search_query = SearchQuery.objects.get(pk=search_query_id)

            # Resolve ContentType — accept bare model name OR "app_label.model"
            ct_str = (content_type_str or '').strip().lower()
            if '.' in ct_str:
                app_label, model = ct_str.split('.', 1)
            else:
                model = ct_str
                app_label = None

            expected = self.SEARCHABLE_CONTENT_TYPES.get(model)
            if expected is None:
                return False
            # If a qualified form was passed, reject app_label mismatches
            if app_label is not None and app_label != expected[0]:
                return False

            content_type = ContentType.objects.get(
                app_label=expected[0], model=expected[1]
            )

            SearchClick.objects.create(
                search_query=search_query,
                content_type=content_type,
                object_id=object_id,
                position=position,
                user=user if user and user.is_authenticated else None,
                session_key=session_key,
            )

            return True
        except Exception:
            return False
