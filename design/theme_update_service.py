"""
Theme Update Service
Handles communication with update server for theme information
"""

import logging
from typing import List, Dict, Any, Optional
from django.core.cache import cache

logger = logging.getLogger(__name__)


class ThemeUpdateService:
    """Service for fetching theme information from update server"""

    CACHE_TIMEOUT = 300  # 5 minutes
    ALL_THEMES_CACHE_KEY = 'theme_update_service_all_themes'

    @classmethod
    def _get_all_themes_cached(cls) -> List[Dict[str, Any]]:
        """
        Fetch full theme list from update server, cached for CACHE_TIMEOUT.
        Single API call used by get_theme_info() and sync methods.
        """
        cached = cache.get(cls.ALL_THEMES_CACHE_KEY)
        if cached is not None:
            return cached

        try:
            from component_updates.services import UpdateManager
            update_manager = UpdateManager()
            themes = update_manager.list_available_components(component_type='theme')
            if not isinstance(themes, list):
                themes = []
            cache.set(cls.ALL_THEMES_CACHE_KEY, themes, cls.CACHE_TIMEOUT)
            return themes
        except Exception as e:
            logger.error(f"Error fetching all themes: {e}")
            return []

    @classmethod
    def get_available_themes(cls) -> List[Dict[str, Any]]:
        """
        Get all available themes from update server.

        Returns:
            List of theme dictionaries with name, slug, version, author, thumbnail, etc.
        """
        try:
            from component_updates.models import ComponentRegistry

            components = cls._get_all_themes_cached()

            if not components:
                logger.warning("Could not fetch available themes from update server")
                return []

            # Get list of installed theme slugs from ComponentRegistry
            installed_slugs = set(
                ComponentRegistry.objects.filter(component_type='theme')
                .values_list('slug', flat=True)
            )

            # Annotate each component with installation status
            available_themes = []
            for component in components:
                slug = component.get('slug')
                is_installed = slug in installed_slugs

                component['is_installed'] = is_installed

                # Add registry info if exists
                if is_installed:
                    try:
                        registry_comp = ComponentRegistry.objects.get(
                            slug=slug,
                            component_type='theme'
                        )
                        component['registry_current_version'] = registry_comp.current_version
                        component['has_update'] = registry_comp.update_available
                    except ComponentRegistry.DoesNotExist:
                        pass

                available_themes.append(component)

            return available_themes

        except Exception as e:
            logger.error(f"Error fetching available themes: {e}")
            return []

    PAGINATED_CACHE_TIMEOUT = 600  # 10 minutes for paginated results

    @classmethod
    def get_available_themes_paginated(
        cls, page: int = 1, page_size: int = 24, search: str = ''
    ) -> Dict[str, Any]:
        """
        Get paginated available themes from update server.
        Results are cached per page/search combination to avoid repeated API calls.

        Returns:
            Dict with keys: results (list), count, page, page_size, total_pages
        """
        # Check cache first (keyed by page, page_size, search)
        cache_key = f'theme_paginated_p{page}_s{page_size}_q{search or ""}'
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            from component_updates.services import UpdateManager

            update_manager = UpdateManager()
            result = update_manager.list_available_components(
                component_type='theme',
                page=page,
                page_size=page_size,
                search=search or None,
            )

            # If we got a paginated dict back, annotate with install status
            if isinstance(result, dict) and 'results' in result:
                from component_updates.models import ComponentRegistry
                installed_slugs = set(
                    ComponentRegistry.objects.filter(component_type='theme')
                    .values_list('slug', flat=True)
                )
                for component in result['results']:
                    slug = component.get('slug')
                    component['is_installed'] = slug in installed_slugs
                cache.set(cache_key, result, cls.PAGINATED_CACHE_TIMEOUT)
                return result

            # Fallback: unpaginated response (shouldn't happen with page param)
            fallback = {
                'results': result if isinstance(result, list) else [],
                'count': len(result) if isinstance(result, list) else 0,
                'page': 1,
                'page_size': page_size,
                'total_pages': 1,
            }
            cache.set(cache_key, fallback, cls.PAGINATED_CACHE_TIMEOUT)
            return fallback

        except Exception as e:
            logger.error(f"Error fetching paginated themes: {e}")
            return {
                'results': [],
                'count': 0,
                'page': 1,
                'page_size': page_size,
                'total_pages': 0,
            }

    @classmethod
    def get_theme_info(cls, slug: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific theme.
        Uses the cached full theme list (single API call) instead of
        fetching the full list per slug.
        """
        # Check per-slug cache first
        cache_key = f'theme_info_{slug}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        try:
            themes = cls._get_all_themes_cached()

            # Find the specific theme
            component_data = None
            for theme in themes:
                if theme.get('slug') == slug:
                    component_data = theme
                    break

            if component_data:
                cache.set(cache_key, component_data, cls.CACHE_TIMEOUT)
                return component_data
            else:
                logger.debug(f"Theme {slug} not found on update server")
                return None

        except Exception as e:
            logger.error(f"Error fetching theme {slug}: {e}")
            return None

    @classmethod
    def sync_installed_theme_metadata(cls) -> int:
        """
        Sync metadata for all installed themes from the update server
        in a single API call. Returns count of themes updated.

        This replaces the old per-theme sync that made N API requests.
        """
        from component_updates.models import ComponentRegistry

        try:
            themes = cls._get_all_themes_cached()
            if not themes:
                return 0

            # Build lookup by slug
            server_themes = {t.get('slug'): t for t in themes if t.get('slug')}

            installed_themes = ComponentRegistry.objects.filter(component_type='theme')
            updated = 0

            for theme_pkg in installed_themes:
                server_data = server_themes.get(theme_pkg.slug)
                if not server_data:
                    continue

                changed = False
                latest_version = server_data.get('current_version')
                if latest_version and theme_pkg.latest_version != latest_version:
                    theme_pkg.latest_version = latest_version
                    theme_pkg.update_available = latest_version != theme_pkg.current_version
                    changed = True

                for field, key in [
                    ('author', 'author_name'),
                    ('thumbnail_url', 'thumbnail_url'),
                ]:
                    val = server_data.get(key)
                    if val and getattr(theme_pkg, field) != val:
                        setattr(theme_pkg, field, val)
                        changed = True

                for field in ('author_details', 'preview_images', 'preview_videos'):
                    val = server_data.get(field)
                    if val and getattr(theme_pkg, field) != val:
                        setattr(theme_pkg, field, val)
                        changed = True

                if changed:
                    theme_pkg.save()
                    updated += 1

            return updated

        except Exception as e:
            logger.warning(f"Failed to sync theme metadata: {e}")
            return 0

    @classmethod
    def check_for_updates(cls, current_version: str, slug: str) -> Dict[str, Any]:
        """
        Check if a newer version is available for a theme.
        """
        try:
            theme_info = cls.get_theme_info(slug)

            if not theme_info:
                return {
                    'has_update': False,
                    'error': f'Theme {slug} not found on update server'
                }

            latest_version = theme_info.get('current_version')

            if not latest_version:
                return {
                    'has_update': False,
                    'error': 'No version information available'
                }

            has_update = latest_version != current_version

            return {
                'has_update': has_update,
                'current_version': current_version,
                'latest_version': latest_version,
                'theme': theme_info
            }

        except Exception as e:
            logger.error(f"Error checking updates for {slug}: {e}")
            return {
                'has_update': False,
                'error': str(e)
            }

    @classmethod
    def clear_cache(cls, slug: Optional[str] = None):
        """Clear theme info cache for specific theme or all themes"""
        cache.delete(cls.ALL_THEMES_CACHE_KEY)
        # Clear paginated caches by deleting keys with a known prefix pattern.
        # Django's default cache doesn't support wildcard deletes, so we use
        # delete_pattern if available (django-redis), otherwise we rely on TTL expiry.
        try:
            if hasattr(cache, 'delete_pattern'):
                cache.delete_pattern('theme_paginated_*')
            else:
                # For LocMemCache/memcached: clear a reasonable set of paginated keys
                for p in range(1, 100):
                    cache.delete(f'theme_paginated_p{p}_s24_q')
        except Exception:
            pass  # Best-effort; TTL will expire stale entries anyway

        if slug:
            cache.delete(f'theme_info_{slug}')
        else:
            from component_updates.models import ComponentRegistry
            themes = ComponentRegistry.objects.filter(component_type='theme')
            for theme in themes:
                cache.delete(f'theme_info_{theme.slug}')
