"""
Migration Admin Interface
Modern, intuitive admin interface for WooCommerce/Shopify migrations.
Follows established admin patterns with wizard-based migration flow.
"""
import logging
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.utils import timezone
from datetime import timedelta

from .models import MigrationJob, MigrationStep, MigrationLog, MigrationMapping

logger = logging.getLogger(__name__)


@admin.register(MigrationJob)
class MigrationJobAdmin(admin.ModelAdmin):
    """
    Modern admin interface for migration jobs with wizard-based workflow.
    """
    list_display = [
        'migration_id_display',
        'platform_badge',
        'status_badge',
        'progress_bar',
        'items_summary',
        'created_display',
        'actions_column'
    ]
    list_filter = ['status', 'platform', 'created_at']
    search_fields = ['id', 'created_by__username', 'created_by__email']
    readonly_fields = [
        'id', 'created_at', 'created_by', 'started_at', 'completed_at',
        'duration_seconds', 'transaction_id'
    ]

    # Custom template for list view
    change_list_template = 'admin/migration/migrationjob/change_list.html'

    # Disable add functionality - use wizard instead
    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        """Custom changelist view with migration tools"""
        extra_context = extra_context or {}
        extra_context['title'] = _('Data Migrations')
        extra_context['management_tools'] = [
            {
                'title': _('Start New Migration'),
                'url': reverse('admin:migration_wizard_start'),
                'description': _('Migrate from WooCommerce, Shopify, Magento, or CSV files'),
                'class': 'addlink',
                'icon': 'fas fa-rocket'
            },
            {
                'title': _('Migration History'),
                'url': reverse('admin:migration_migrationjob_changelist'),
                'description': _('View all past migrations'),
                'class': 'viewlink',
                'icon': 'fas fa-history'
            },
        ]

        # Get statistics
        total_jobs = MigrationJob.objects.count()
        completed_jobs = MigrationJob.objects.filter(status='completed').count()
        failed_jobs = MigrationJob.objects.filter(status='failed').count()
        running_jobs = MigrationJob.objects.filter(status='running').count()

        extra_context['stats'] = {
            'total': total_jobs,
            'completed': completed_jobs,
            'failed': failed_jobs,
            'running': running_jobs,
        }

        # Get all migrations ordered by creation date (newest first)
        extra_context['migrations'] = MigrationJob.objects.all().order_by('-created_at')

        return super().changelist_view(request, extra_context)

    def migration_id_display(self, obj):
        """Display shortened migration ID"""
        short_id = str(obj.id)[:8]
        return format_html(
            '<code style="background: var(--darkened-bg, #f8f9fa); padding: 4px 8px; '
            'border-radius: 4px; font-size: 12px; font-family: monospace;">{}</code>',
            short_id
        )
    migration_id_display.short_description = _('ID')

    def platform_badge(self, obj):
        """Display platform with icon"""
        platform_icons = {
            'woocommerce': ('fab fa-wordpress', '#21759b'),
            'shopify': ('fab fa-shopify', '#96bf48'),
            'magento': ('fab fa-magento', '#f26322'),
            'csv': ('fas fa-file-csv', '#4caf50'),
        }

        icon, color = platform_icons.get(obj.platform, ('fas fa-box', '#666'))

        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<i class="{}" style="color: {}; font-size: 16px;"></i>'
            '<span style="font-weight: 500;">{}</span>'
            '</div>',
            icon, color, obj.get_platform_display()
        )
    platform_badge.short_description = _('Platform')

    def status_badge(self, obj):
        """Display status with colored badge"""
        status_colors = {
            'pending': ('#ffa500', '#fff'),
            'connecting': ('#2196f3', '#fff'),
            'previewing': ('#9c27b0', '#fff'),
            'running': ('#2196f3', '#fff'),
            'paused': ('#ff9800', '#fff'),
            'completed': ('#4caf50', '#fff'),
            'failed': ('#f44336', '#fff'),
            'rolling_back': ('#ff5722', '#fff'),
            'rolled_back': ('#607d8b', '#fff'),
        }

        bg_color, text_color = status_colors.get(obj.status, ('#999', '#fff'))

        # Add icon
        icons = {
            'pending': 'fas fa-clock',
            'running': 'fas fa-spinner fa-spin',
            'completed': 'fas fa-check-circle',
            'failed': 'fas fa-times-circle',
        }
        icon = icons.get(obj.status, 'fas fa-circle')

        return format_html(
            '<span style="background: {}; color: {}; padding: 6px 12px; '
            'border-radius: 16px; font-size: 12px; font-weight: 600; '
            'display: inline-flex; align-items: center; gap: 6px;">'
            '<i class="{}"></i> {}'
            '</span>',
            bg_color, text_color, icon, obj.get_status_display()
        )
    status_badge.short_description = _('Status')

    def progress_bar(self, obj):
        """Display progress bar"""
        if obj.status not in ['running', 'paused', 'completed']:
            return '-'

        percent = obj.progress_percent
        color = '#4caf50' if percent == 100 else '#2196f3'

        return format_html(
            '<div style="width: 120px;">'
            '<div style="background: var(--darkened-bg, #e0e0e0); '
            'height: 20px; border-radius: 10px; overflow: hidden; position: relative;">'
            '<div style="background: {}; width: {}%; height: 100%; '
            'transition: width 0.3s ease;"></div>'
            '<span style="position: absolute; top: 0; left: 0; right: 0; '
            'text-align: center; line-height: 20px; font-size: 11px; '
            'font-weight: 600; color: var(--body-fg, #333);">{}%</span>'
            '</div>'
            '</div>',
            color, percent, percent
        )
    progress_bar.short_description = _('Progress')

    def items_summary(self, obj):
        """Display items summary"""
        if obj.total_items == 0:
            return format_html('<span style="color: var(--body-quiet-color, #999);">No data</span>')

        return format_html(
            '<div style="font-size: 12px; line-height: 1.5;">'
            '<div><strong>{}</strong> total</div>'
            '<div style="color: #4caf50;">✓ {} imported</div>'
            '<div style="color: #ff9800;">⊘ {} skipped</div>'
            '<div style="color: #f44336;">✗ {} failed</div>'
            '</div>',
            obj.total_items,
            obj.total_imported,
            obj.total_skipped,
            obj.total_failed
        )
    items_summary.short_description = _('Items')

    def created_display(self, obj):
        """Display creation time"""
        time_str = timezone.localtime(obj.created_at).strftime('%b %d, %Y %I:%M %p')

        if obj.completed_at:
            duration = obj.duration_seconds
            if duration:
                mins = duration // 60
                secs = duration % 60
                duration_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"
            else:
                duration_str = '-'
        else:
            duration_str = '-'

        return format_html(
            '<div style="font-size: 12px; line-height: 1.5;">'
            '<div>{}</div>'
            '<div style="color: var(--body-quiet-color, #999);">by {}</div>'
            '<div style="color: var(--body-quiet-color, #999);">Duration: {}</div>'
            '</div>',
            time_str,
            obj.created_by.username,
            duration_str
        )
    created_display.short_description = _('Created')

    def actions_column(self, obj):
        """Display action buttons"""
        buttons = []

        # Resume - for incomplete wizard migrations (pending status)
        if obj.status == 'pending':
            resume_url = reverse('admin:migration_wizard_step2', args=[obj.pk])
            buttons.append(
                f'<a href="{resume_url}" class="button" '
                f'style="margin-right: 5px; background: var(--button-primary, #1a73e8); color: white;">'
                f'<i class="fas fa-play"></i> {_("Resume")}</a>'
            )

        # Retry - for failed migrations
        if obj.status == 'failed':
            retry_url = reverse('admin:migration_job_retry', args=[obj.pk])
            buttons.append(
                f'<a href="{retry_url}" class="button" '
                f'style="margin-right: 5px; background: var(--warning-color, #ff9800); color: white;">'
                f'<i class="fas fa-redo"></i> {_("Retry")}</a>'
            )

        # View Details - link to appropriate wizard step
        view_url = self._get_wizard_url(obj)
        buttons.append(
            f'<a href="{view_url}" class="button" style="margin-right: 5px;">'
            f'<i class="fas fa-eye"></i> {_("View")}</a>'
        )

        # Rollback (if eligible)
        if obj.is_rollbackable:
            rollback_url = reverse('admin:migration_job_rollback', args=[obj.pk])
            buttons.append(
                f'<a href="{rollback_url}" class="button" '
                f'style="margin-right: 5px; background: var(--error-color, #f44336); color: white;" '
                f'onclick="return confirm(\'{_("Are you sure you want to rollback this migration? This will delete all imported data.")}\');">'
                f'<i class="fas fa-undo"></i> {_("Rollback")}</a>'
            )

        # Download Report (if completed)
        if obj.status == 'completed' and obj.report_file:
            buttons.append(
                f'<a href="{obj.report_file.url}" class="button" download>'
                f'<i class="fas fa-download"></i> {_("Report")}</a>'
            )

        # Delete - for pending or failed migrations that can be cleaned up
        if obj.status in ['pending', 'failed']:
            delete_url = reverse('admin:migration_job_delete', args=[obj.pk])
            buttons.append(
                f'<a href="{delete_url}" class="button" '
                f'style="margin-right: 5px; background: var(--body-quiet-color, #666); color: white;" '
                f'onclick="return confirm(\'{_("Are you sure you want to delete this migration?")}\');">'
                f'<i class="fas fa-trash"></i> {_("Delete")}</a>'
            )

        return format_html(' '.join(buttons))
    actions_column.short_description = _('Actions')

    def _get_wizard_url(self, obj):
        """Return the appropriate wizard step URL based on job status."""
        if obj.status == 'pending':
            return reverse('admin:migration_wizard_step2', args=[obj.pk])
        elif obj.status == 'running':
            return reverse('admin:migration_wizard_step5', args=[obj.pk])
        else:
            # completed, failed, rolled_back → results page
            return reverse('admin:migration_wizard_step6', args=[obj.pk])

    def get_urls(self):
        """Add custom URLs for wizard and actions"""
        urls = super().get_urls()
        custom_urls = [
            # Migration Wizard
            path('wizard/', self.admin_site.admin_view(self.wizard_start), name='migration_wizard_start'),
            path('wizard/step1/', self.admin_site.admin_view(self.wizard_step1), name='migration_wizard_step1'),
            path('wizard/step2/<uuid:job_id>/', self.admin_site.admin_view(self.wizard_step2), name='migration_wizard_step2'),
            path('wizard/step3/<uuid:job_id>/', self.admin_site.admin_view(self.wizard_step3), name='migration_wizard_step3'),
            path('wizard/step4/<uuid:job_id>/', self.admin_site.admin_view(self.wizard_step4), name='migration_wizard_step4'),
            path('wizard/step5/<uuid:job_id>/', self.admin_site.admin_view(self.wizard_step5), name='migration_wizard_step5'),
            path('wizard/step6/<uuid:job_id>/', self.admin_site.admin_view(self.wizard_step6), name='migration_wizard_step6'),

            # Actions
            path('<uuid:job_id>/rollback/', self.admin_site.admin_view(self.rollback_migration), name='migration_job_rollback'),
            path('<uuid:job_id>/retry/', self.admin_site.admin_view(self.retry_migration), name='migration_job_retry'),
            path('<uuid:job_id>/cancel/', self.admin_site.admin_view(self.cancel_migration), name='migration_job_cancel'),
            path('<uuid:job_id>/delete/', self.admin_site.admin_view(self.delete_migration), name='migration_job_delete'),
            path('<uuid:job_id>/progress/', self.admin_site.admin_view(self.get_progress), name='migration_job_progress'),
            path('<uuid:job_id>/logs/', self.admin_site.admin_view(self.get_logs), name='migration_job_logs'),

            # API endpoints
            path('api/test-connection/<uuid:job_id>/', self.admin_site.admin_view(self.test_connection), name='migration_test_connection'),
            path('api/preview-data/<uuid:job_id>/', self.admin_site.admin_view(self.preview_data), name='migration_preview_data'),
            path('api/start-import/<uuid:job_id>/', self.admin_site.admin_view(self.start_import), name='migration_start_import'),
            path('api/download-template/<str:template_type>/', self.admin_site.admin_view(self.download_template), name='migration_download_template'),
            path('api/download-bridge-plugin/', self.admin_site.admin_view(self.download_bridge_plugin), name='migration_download_bridge_plugin'),
            path('api/download-report/<uuid:job_id>/', self.admin_site.admin_view(self.download_report), name='migration_download_report'),
            path('api/download-logs/<uuid:job_id>/', self.admin_site.admin_view(self.download_logs), name='migration_download_logs'),

            # Link rewriting endpoints
            path('api/content-links/<uuid:job_id>/update/', self.admin_site.admin_view(self.update_content_link), name='migration_update_content_link'),
            path('api/content-links/<uuid:job_id>/apply/', self.admin_site.admin_view(self.apply_content_links), name='migration_apply_content_links'),
            path('api/content-links/<uuid:job_id>/bulk-approve/', self.admin_site.admin_view(self.bulk_approve_content_links), name='migration_bulk_approve_content_links'),
        ]
        return custom_urls + urls

    # Wizard Views (placeholders - will implement next)
    def wizard_start(self, request):
        """Step 0: Welcome screen"""
        return redirect('admin:migration_wizard_step1')

    def wizard_step1(self, request):
        """Step 1: Choose platform"""
        if request.method == 'POST':
            platform = request.POST.get('platform')
            if not platform:
                messages.error(request, _('Please select a platform.'))
                return render(request, 'admin/migration/wizard/step1_platform.html', {
                    'title': _('Migration Wizard - Choose Platform'),
                    'opts': self.model._meta,
                    'current_step': 1,
                })

            # Create new migration job
            # Determine method based on platform
            method = 'api' if platform in ['woocommerce', 'shopify', 'magento'] else 'csv'

            job = MigrationJob.objects.create(
                platform=platform,
                method=method,
                status='pending',
                created_by=request.user
            )

            messages.success(request, _('Migration job created. Please configure the connection.'))
            return redirect('admin:migration_wizard_step2', job_id=job.id)

        return render(request, 'admin/migration/wizard/step1_platform.html', {
            'title': _('Migration Wizard - Choose Platform'),
            'opts': self.model._meta,
            'current_step': 1,
        })

    def wizard_step2(self, request, job_id):
        """Step 2: Connection configuration"""
        job = get_object_or_404(MigrationJob, pk=job_id)

        if request.method == 'POST':
            # Save connection configuration
            if job.platform == 'woocommerce':
                store_url = request.POST.get('store_url', '').strip()
                consumer_key = request.POST.get('consumer_key', '').strip()
                consumer_secret = request.POST.get('consumer_secret', '').strip()

                if not all([store_url, consumer_key, consumer_secret]):
                    messages.error(request, _('Please fill in all required fields.'))
                    return render(request, 'admin/migration/wizard/step2_connection.html', {
                        'title': _('Migration Wizard - Connection'),
                        'opts': self.model._meta,
                        'job': job,
                        'current_step': 2,
                    })

                # Save to job connection_config
                job.connection_config = {
                    'store_url': store_url,
                    'consumer_key': consumer_key,
                    'consumer_secret': consumer_secret,
                }
                job.save()

                messages.success(request, _('Connection configured successfully.'))
                return redirect('admin:migration_wizard_step3', job_id=job.id)

            elif job.platform == 'shopify':
                store_domain = request.POST.get('store_domain', '').strip()
                client_id = request.POST.get('client_id', '').strip()
                client_secret = request.POST.get('client_secret', '').strip()

                # Normalize domain: strip protocol and trailing slash
                store_domain = store_domain.replace('https://', '').replace('http://', '').rstrip('/')

                if not all([store_domain, client_id, client_secret]):
                    messages.error(request, _('Please fill in all required fields.'))
                    return render(request, 'admin/migration/wizard/step2_connection.html', {
                        'title': _('Migration Wizard - Connection'),
                        'opts': self.model._meta,
                        'job': job,
                        'current_step': 2,
                    })

                job.connection_config = {
                    'store_domain': store_domain,
                    'client_id': client_id,
                    'client_secret': client_secret,
                }
                job.save()

                messages.success(request, _('Connection configured successfully.'))
                return redirect('admin:migration_wizard_step3', job_id=job.id)

            elif job.platform == 'magento':
                store_url = request.POST.get('store_url', '').strip()
                access_token = request.POST.get('access_token', '').strip()

                if not all([store_url, access_token]):
                    messages.error(request, _('Please fill in all required fields.'))
                    return render(request, 'admin/migration/wizard/step2_connection.html', {
                        'title': _('Migration Wizard - Connection'),
                        'opts': self.model._meta,
                        'job': job,
                        'current_step': 2,
                    })

                # Normalize URL: strip trailing slash
                store_url = store_url.rstrip('/')

                job.connection_config = {
                    'store_url': store_url,
                    'access_token': access_token,
                }
                job.save()

                messages.success(request, _('Connection configured successfully.'))
                return redirect('admin:migration_wizard_step3', job_id=job.id)

            elif job.platform == 'csv':
                import csv
                from django.core.files.storage import default_storage

                csv_files = {}
                file_types = ['products', 'categories', 'customers', 'orders', 'reviews']

                for file_type in file_types:
                    uploaded = request.FILES.get(f'{file_type}_csv')
                    if not uploaded:
                        continue

                    # Read and validate header row
                    try:
                        first_line = uploaded.readline().decode('utf-8-sig').strip()
                        uploaded.seek(0)
                        # Use csv.reader to properly handle quoted headers
                        headers = [h.strip() for h in next(csv.reader([first_line])) if h.strip()]
                        if not headers:
                            messages.error(request, _('{} CSV has no headers.').format(file_type.title()))
                            return render(request, 'admin/migration/wizard/step2_connection.html', {
                                'title': _('Migration Wizard - Connection'),
                                'opts': self.model._meta,
                                'job': job,
                                'current_step': 2,
                            })
                    except Exception as e:
                        messages.error(request, _('{} CSV could not be read: {}').format(file_type.title(), str(e)))
                        return render(request, 'admin/migration/wizard/step2_connection.html', {
                            'title': _('Migration Wizard - Connection'),
                            'opts': self.model._meta,
                            'job': job,
                            'current_step': 2,
                        })

                    # Save file to media storage
                    save_path = f'migration_csv/{job.id}/{file_type}.csv'
                    saved_name = default_storage.save(save_path, uploaded)

                    csv_files[file_type] = {
                        'path': saved_name,
                        'headers': headers,
                    }

                if 'products' not in csv_files:
                    messages.error(request, _('Products CSV is required.'))
                    return render(request, 'admin/migration/wizard/step2_connection.html', {
                        'title': _('Migration Wizard - Connection'),
                        'opts': self.model._meta,
                        'job': job,
                        'current_step': 2,
                    })

                job.connection_config = {'csv_files': csv_files}
                job.save()

                messages.success(request, _('CSV files uploaded successfully.'))
                return redirect('admin:migration_wizard_step3', job_id=job.id)

        return render(request, 'admin/migration/wizard/step2_connection.html', {
            'title': _('Migration Wizard - Connection'),
            'opts': self.model._meta,
            'job': job,
            'current_step': 2,
        })

    def wizard_step3(self, request, job_id):
        """Step 3: Preview data"""
        job = get_object_or_404(MigrationJob, pk=job_id)

        # Initialize preview data
        preview = {
            'products_count': 0,
            'categories_count': 0,
            'customers_count': 0,
            'orders_count': 0,
            'reviews_count': 0,
            'coupons_count': 0,
            'blog_posts_count': 0,
            'blog_categories_count': 0,
            'blog_tags_count': 0,
            'sample_products': [],
        }

        # Fetch data preview for Shopify
        if job.platform == 'shopify' and job.connection_config:
            try:
                from .fetchers.shopify_api import ShopifyAPIClient

                client = ShopifyAPIClient(
                    store_domain=job.connection_config.get('store_domain'),
                    client_id=job.connection_config.get('client_id'),
                    client_secret=job.connection_config.get('client_secret'),
                )

                counts = client.get_total_counts()
                preview['products_count'] = counts.get('products', 0)
                preview['categories_count'] = counts.get('collections', 0)
                preview['customers_count'] = counts.get('customers', 0)
                preview['orders_count'] = counts.get('orders', 0)
                preview['coupons_count'] = counts.get('discounts', 0)
                preview['blog_posts_count'] = counts.get('articles', 0)

                # Fetch sample products (first 5)
                if preview['products_count'] > 0:
                    sample_products = client.fetch_products(limit=5)
                    # Normalize Shopify product format for template
                    for p in sample_products:
                        # Shopify uses 'title', normalize to 'name'
                        if 'title' in p and 'name' not in p:
                            p['name'] = p['title']
                        if 'images' in p and p['images']:
                            p['_thumbnail_url'] = p['images'][0].get('src', '')
                        if 'variants' in p and p['variants']:
                            v = p['variants'][0]
                            p['price'] = v.get('price', '0.00')
                            if 'sku' not in p or not p['sku']:
                                p['sku'] = v.get('sku', '')

                    preview['sample_products'] = sample_products

            except Exception as e:
                logger.error(f"Failed to fetch Shopify preview data: {e}")
                messages.error(request, _('Failed to fetch preview data: {}').format(str(e)))

        # Fetch data preview for Magento
        elif job.platform == 'magento' and job.connection_config:
            try:
                from .fetchers.magento_api import MagentoAPIClient

                client = MagentoAPIClient(
                    store_url=job.connection_config.get('store_url'),
                    access_token=job.connection_config.get('access_token'),
                    verify_ssl=job.connection_config.get('verify_ssl', True),
                )

                counts = client.get_total_counts()
                preview['products_count'] = counts.get('products', 0)
                preview['categories_count'] = counts.get('categories', 0)
                preview['customers_count'] = counts.get('customers', 0)
                preview['orders_count'] = counts.get('orders', 0)
                preview['reviews_count'] = counts.get('reviews', 0)
                preview['coupons_count'] = counts.get('coupons', 0)
                preview['blog_posts_count'] = counts.get('cms_pages', 0)

                # Fetch sample products (first 5)
                if preview['products_count'] > 0:
                    sample_products = client.fetch_products(limit=5)
                    # Normalize Magento status (1/2) to template values
                    magento_status_map = {1: 'active', '1': 'active', 2: 'draft', '2': 'draft'}
                    for p in sample_products:
                        p['status'] = magento_status_map.get(p.get('status'), 'draft')
                    preview['sample_products'] = sample_products

            except Exception as e:
                logger.error(f"Failed to fetch Magento preview data: {e}")
                messages.error(request, _('Failed to fetch preview data: {}').format(str(e)))

        # Fetch data preview if WooCommerce
        elif job.platform == 'woocommerce' and job.connection_config:
            try:
                from .fetchers.woocommerce_api import WooCommerceAPIClient

                # Create API client
                client = WooCommerceAPIClient(
                    store_url=job.connection_config.get('store_url'),
                    consumer_key=job.connection_config.get('consumer_key'),
                    consumer_secret=job.connection_config.get('consumer_secret')
                )

                # Get counts
                counts = client.get_total_counts()
                preview['products_count'] = counts.get('products', 0)
                preview['categories_count'] = counts.get('categories', 0)
                preview['customers_count'] = counts.get('customers', 0)
                preview['orders_count'] = counts.get('orders', 0)
                preview['reviews_count'] = counts.get('reviews', 0)
                preview['coupons_count'] = counts.get('coupons', 0)

                # Fetch sample products (first 5)
                if preview['products_count'] > 0:
                    sample_products = client.fetch_products(page=1, per_page=5)
                    preview['sample_products'] = sample_products

                # Also fetch WordPress blog counts (uses wp-json/wp/v2 API)
                try:
                    from .fetchers.wordpress_api import WordPressAPIClient
                    wp_client = WordPressAPIClient(
                        site_url=job.connection_config.get('store_url')
                    )
                    blog_counts = wp_client.get_total_counts()
                    preview['blog_posts_count'] = blog_counts.get('posts', 0)
                    preview['blog_categories_count'] = blog_counts.get('categories', 0)
                    preview['blog_tags_count'] = blog_counts.get('tags', 0)
                except Exception as blog_e:
                    logger.warning(f"Failed to fetch blog counts: {blog_e}")

                # Probe Spwig Migration Bridge for affiliate data
                try:
                    from .fetchers.spwig_bridge_api import SpwigBridgeAPIClient
                    bridge_client = SpwigBridgeAPIClient(
                        store_url=job.connection_config.get('store_url'),
                        consumer_key=job.connection_config.get('consumer_key'),
                        consumer_secret=job.connection_config.get('consumer_secret'),
                    )
                    bridge_info = bridge_client.get_info()
                    if bridge_info and bridge_info.get('detected_plugin') != 'none':
                        preview['bridge_available'] = True
                        preview['bridge_plugin_name'] = bridge_info.get('plugin_name', '')
                        bridge_counts = bridge_info.get('counts', {})
                        preview['affiliates_count'] = bridge_counts.get('affiliates', 0)
                        preview['commissions_count'] = bridge_counts.get('referrals', 0)
                        preview['payouts_count'] = bridge_counts.get('payouts', 0)
                        preview['plans_count'] = bridge_counts.get('plans', 0)
                except Exception as bridge_e:
                    logger.debug(f"Spwig Bridge not available: {bridge_e}")

            except Exception as e:
                logger.error(f"Failed to fetch preview data: {e}")
                messages.error(request, _('Failed to fetch preview data: {}').format(str(e)))

        elif job.platform == 'csv' and job.connection_config:
            try:
                from .fetchers.csv_reader import CSVDataReader

                csv_files = job.connection_config.get('csv_files', {})
                reader = CSVDataReader(csv_files)
                counts = reader.get_total_counts()

                preview['products_count'] = counts.get('products', 0)
                preview['categories_count'] = counts.get('categories', 0)
                preview['customers_count'] = counts.get('customers', 0)
                preview['orders_count'] = counts.get('orders', 0)
                preview['reviews_count'] = counts.get('reviews', 0)

                # Fetch sample products (first 5)
                if preview['products_count'] > 0:
                    sample_products = reader.fetch_products(page=1, per_page=5)
                    preview['sample_products'] = sample_products

            except Exception as e:
                logger.error(f"Failed to read CSV preview data: {e}")
                messages.error(request, _('Failed to read CSV files: {}').format(str(e)))

        if request.method == 'POST':
            # Save import selections
            import_options = {
                'import_categories': 'import_categories' in request.POST,
                'import_products': 'import_products' in request.POST,
                'import_customers': 'import_customers' in request.POST,
                'import_orders': 'import_orders' in request.POST,
                'import_reviews': 'import_reviews' in request.POST,
                'import_coupons': 'import_coupons' in request.POST,
                'import_blog': 'import_blog' in request.POST,
                'import_affiliates': 'import_affiliates' in request.POST,
                'skip_existing': 'skip_existing' in request.POST,
                'import_images': 'import_images' in request.POST,
                'preserve_ids': 'preserve_ids' in request.POST,
                'batch_size': int(request.POST.get('batch_size', 25)),
            }

            # Update job connection_config with import options
            job.connection_config.update(import_options)

            # Save counts for accurate progress calculation
            if job.platform == 'magento' and preview:
                job.connection_config.update({
                    'total_categories': preview.get('categories_count', 0),
                    'total_products': preview.get('products_count', 0),
                    'total_customers': preview.get('customers_count', 0),
                    'total_orders': preview.get('orders_count', 0),
                    'total_reviews': preview.get('reviews_count', 0),
                    'total_coupons': preview.get('coupons_count', 0),
                    'total_cms_pages': preview.get('blog_posts_count', 0),
                    'total_blog_posts': preview.get('blog_posts_count', 0),
                    'total_blog_categories': 0,
                    'total_blog_tags': 0,
                })

            elif job.platform == 'shopify' and preview:
                job.connection_config.update({
                    'total_categories': preview.get('categories_count', 0),
                    'total_products': preview.get('products_count', 0),
                    'total_customers': preview.get('customers_count', 0),
                    'total_orders': preview.get('orders_count', 0),
                    'total_reviews': 0,
                    'total_coupons': preview.get('coupons_count', 0),
                    'total_blog_posts': preview.get('blog_posts_count', 0),
                    'total_blog_categories': 0,
                    'total_blog_tags': 0,
                })

            elif job.platform == 'woocommerce' and preview:
                job.connection_config.update({
                    'total_categories': preview.get('categories_count', 0),
                    'total_products': preview.get('products_count', 0),
                    'total_customers': preview.get('customers_count', 0),
                    'total_orders': preview.get('orders_count', 0),
                    'total_reviews': preview.get('reviews_count', 0),
                    'total_coupons': preview.get('coupons_count', 0),
                    'total_blog_posts': preview.get('blog_posts_count', 0),
                    'total_blog_categories': preview.get('blog_categories_count', 0),
                    'total_blog_tags': preview.get('blog_tags_count', 0),
                    'total_affiliates': preview.get('affiliates_count', 0),
                    'total_commissions': preview.get('commissions_count', 0),
                    'total_payouts': preview.get('payouts_count', 0),
                })

            job.save()

            messages.success(request, _('Import options saved.'))
            return redirect('admin:migration_wizard_step4', job_id=job.id)

        return render(request, 'admin/migration/wizard/step3_preview.html', {
            'title': _('Migration Wizard - Preview Data'),
            'opts': self.model._meta,
            'job': job,
            'current_step': 3,
            'preview': preview,
        })

    def wizard_step4(self, request, job_id):
        """Step 4: Field mapping (optional)"""
        job = get_object_or_404(MigrationJob, pk=job_id)

        if request.method == 'POST':
            # Save custom field mappings
            for key in request.POST:
                if key.startswith('mapping_'):
                    field_id = key.replace('mapping_', '')
                    dest_field = request.POST[key]
                    transform_type = request.POST.get(f'transform_{field_id}', 'string')

                    if dest_field:  # Only create if not skipped
                        # Parse dest_field: "Product.custom_field_1" → model + field
                        try:
                            dest_model, dest_field_name = dest_field.split('.', 1)

                            MigrationMapping.objects.create(
                                job=job,
                                source_type='product',
                                source_field=field_id,
                                dest_model=dest_model,
                                dest_field=dest_field_name,
                                transform_type=transform_type,
                                is_auto_detected=False,
                            )
                        except ValueError:
                            logger.warning(f"Invalid dest_field format: {dest_field}")

            # Save CSV column mappings if CSV platform
            if job.platform == 'csv':
                csv_column_mappings = {}
                csv_files = job.connection_config.get('csv_files', {})
                for file_type, file_info in csv_files.items():
                    headers = file_info.get('headers', [])
                    file_mappings = {}
                    for idx, header in enumerate(headers):
                        field_name = f'csv_map_{file_type}_{idx}'
                        expected_field = request.POST.get(field_name, '__skip__')
                        if expected_field and expected_field != '__skip__':
                            file_mappings[header] = expected_field
                    if file_mappings:
                        csv_column_mappings[file_type] = file_mappings
                job.connection_config['csv_column_mappings'] = csv_column_mappings

            # Save other settings to connection_config
            job.connection_config.update({
                'price_adjustment_type': request.POST.get('price_adjustment_type', 'none'),
                'price_adjustment_value': request.POST.get('price_adjustment_value', '0'),
                'import_tax_settings': 'import_tax_settings' in request.POST,
                'import_shipping_settings': 'import_shipping_settings' in request.POST,
                'unmapped_category_action': request.POST.get('unmapped_category_action', 'create'),
            })
            job.save()

            messages.success(request, _('Field mappings configured successfully.'))
            return redirect('admin:migration_wizard_step5', job_id=job.id)

        # GET: Auto-detect and show mappings
        from .utils.field_detector import create_standard_mappings, detect_custom_fields, _get_platform_config

        # Map config keys to step 3 import flags (platform-aware)
        if job.platform == 'shopify':
            IMPORT_FLAG_MAP = {
                'products': 'import_products',
                'collections': 'import_categories',
                'customers': 'import_customers',
                'orders': 'import_orders',
                'discounts': 'import_coupons',
                'articles': 'import_blog',
            }
        elif job.platform == 'magento':
            IMPORT_FLAG_MAP = {
                'products': 'import_products',
                'categories': 'import_categories',
                'customers': 'import_customers',
                'orders': 'import_orders',
                'reviews': 'import_reviews',
                'coupons': 'import_coupons',
                'cms_pages': 'import_blog',
            }
        else:
            IMPORT_FLAG_MAP = {
                'products': 'import_products',
                'categories': 'import_categories',
                'customers': 'import_customers',
                'orders': 'import_orders',
                'reviews': 'import_reviews',
                'coupons': 'import_coupons',
                'blog_posts': 'import_blog',
                'blog_categories': 'import_blog',
                'blog_tags': 'import_blog',
            }

        # Build set of selected config types for filtering
        import_flags = job.connection_config or {}
        selected_types = {
            cfg_key for cfg_key, flag in IMPORT_FLAG_MAP.items()
            if import_flags.get(flag, False)
        }

        # Create standard mappings if not exists (only for selected types)
        if not job.mappings.exists():
            count = create_standard_mappings(job, job.platform, selected_types=selected_types or None)
            logger.info(f"Created {count} standard field mappings for job {job.id}")

        # Get mappings from config, filtered by step 3 selections
        auto_mappings = []
        config = _get_platform_config(job.platform)

        for source_type_plural, field_map in config.items():
            # Skip types not selected for import in step 3
            flag = IMPORT_FLAG_MAP.get(source_type_plural)
            if flag and not import_flags.get(flag, False):
                continue

            # Singularize type for display
            if source_type_plural.endswith('ies'):
                source_type = source_type_plural[:-3] + 'y'
            elif source_type_plural.endswith('s'):
                source_type = source_type_plural[:-1]
            else:
                source_type = source_type_plural

            for source_field, (dest_model, dest_field, transform_type) in field_map.items():
                # Create a mapping-like dict for template
                auto_mappings.append({
                    'source_type': source_type,
                    'source_field': source_field,
                    'source_field_label': source_field.replace('_', ' ').replace('.', ' ').title(),
                    'dest_model': dest_model,
                    'dest_field': dest_field,
                    'dest_field_label': dest_field.replace('_', ' ').title(),
                    'transform_type': transform_type,
                })

        # Sort by source_type and source_field
        auto_mappings.sort(key=lambda x: (x['source_type'], x['source_field']))

        # Detect custom fields from sample data (only for selected types)
        custom_fields = []
        if job.platform == 'woocommerce' and job.connection_config:
            try:
                from .fetchers.woocommerce_api import WooCommerceAPIClient
                client = WooCommerceAPIClient(
                    store_url=job.connection_config['store_url'],
                    consumer_key=job.connection_config['consumer_key'],
                    consumer_secret=job.connection_config['consumer_secret']
                )

                if import_flags.get('import_products'):
                    sample = client.fetch_products(page=1, per_page=10)
                    custom_fields.extend(detect_custom_fields(sample, source_type='product'))

                if import_flags.get('import_customers'):
                    sample = client.fetch_customers(page=1, per_page=10)
                    custom_fields.extend(detect_custom_fields(sample, source_type='customer'))

                if import_flags.get('import_orders'):
                    sample = client.fetch_orders(page=1, per_page=10)
                    custom_fields.extend(detect_custom_fields(sample, source_type='order'))

            except Exception as e:
                logger.error(f"Failed to detect custom fields: {e}")
                messages.warning(request, _('Could not analyze custom fields. You can still proceed with the import.'))

        elif job.platform == 'shopify' and job.connection_config:
            # Shopify custom field detection is limited (metafields require
            # separate API calls). For now, we rely on standard mappings.
            # Custom metafield detection can be added in Phase 4 if needed.
            pass

        # Build CSV column mapping context
        csv_column_mappings = []
        if job.platform == 'csv' and job.connection_config:
            from .fetchers.csv_reader import CSVDataReader

            csv_files = job.connection_config.get('csv_files', {})
            existing_mappings = job.connection_config.get('csv_column_mappings', {})

            FILE_TYPE_LABELS = {
                'products': _('Products'),
                'categories': _('Categories'),
                'customers': _('Customers'),
                'orders': _('Orders'),
                'reviews': _('Reviews'),
            }

            for file_type, file_info in csv_files.items():
                # Skip file types not selected for import
                flag = IMPORT_FLAG_MAP.get(file_type)
                if flag and not import_flags.get(flag, False):
                    continue

                csv_headers = file_info.get('headers', [])
                expected_fields = CSVDataReader.EXPECTED_FIELDS.get(file_type, [])

                # Use existing mappings if available, otherwise auto-detect
                if file_type in existing_mappings:
                    auto_detected = existing_mappings[file_type]
                else:
                    auto_detected = CSVDataReader.auto_detect_mappings(csv_headers, file_type)

                csv_column_mappings.append({
                    'file_type': file_type,
                    'file_type_label': FILE_TYPE_LABELS.get(file_type, file_type.title()),
                    'csv_headers': csv_headers,
                    'expected_fields': expected_fields,
                    'auto_detected': auto_detected,
                })

        return render(request, 'admin/migration/wizard/step4_mapping.html', {
            'title': _('Migration Wizard - Field Mapping'),
            'opts': self.model._meta,
            'job': job,
            'current_step': 4,
            'auto_mappings': auto_mappings,
            'custom_fields': custom_fields,
            'category_mapping_needed': import_flags.get('import_categories', False),
            'csv_column_mappings': csv_column_mappings,
        })

    def wizard_step5(self, request, job_id):
        """Step 5: Import progress"""
        job = get_object_or_404(MigrationJob, pk=job_id)

        # Auto-start import if job is still pending
        if job.status == 'pending':
            try:
                from .tasks import run_migration_job

                # Delete old steps and logs from any previous attempts
                job.steps.all().delete()
                job.logs.all().delete()

                # Dispatch Celery task to run migration asynchronously
                task = run_migration_job.delay(str(job.id))

                # Store task ID for monitoring
                job.connection_config['celery_task_id'] = task.id
                job.status = 'running'
                job.started_at = timezone.now()
                job.save()

                logger.info(f"Dispatched migration job {job.id} to Celery task {task.id}")
                messages.success(request, _('Migration started! You can safely close this window and check back later.'))

            except Exception as e:
                logger.error(f"Failed to start import: {e}")
                messages.error(request, _('Failed to start import: {}').format(str(e)))

        return render(request, 'admin/migration/wizard/step5_import.html', {
            'title': _('Migration Wizard - Importing'),
            'opts': self.model._meta,
            'job': job,
            'current_step': 5,
        })

    def wizard_step6(self, request, job_id):
        """Step 6: Complete — includes link rewriting review"""
        from migration.models import ContentLink
        from itertools import groupby
        from operator import attrgetter

        job = get_object_or_404(MigrationJob, pk=job_id)

        # Get content links for this job
        content_links = ContentLink.objects.filter(job=job).order_by(
            'source_type', 'source_title', 'original_url'
        )
        pending_count = content_links.filter(status='pending').count()
        high_confidence_count = content_links.filter(
            status='pending', confidence__gte=0.85
        ).count()
        applied_count = content_links.filter(status='applied').count()
        total_links = content_links.count()

        # Group links by source object for display
        grouped_links = []
        if total_links > 0:
            # Group by source_type + source_object_id
            for link in content_links:
                # Find or create group
                group_key = f"{link.source_type}_{link.source_object_id}"
                existing_group = None
                for g in grouped_links:
                    if g['key'] == group_key:
                        existing_group = g
                        break

                if not existing_group:
                    # Determine icon and admin URL
                    icon = 'file-alt'
                    admin_url = ''
                    source_type_display = link.get_source_type_display()
                    if link.source_product_id:
                        icon = 'box'
                        admin_url = f'/en/admin/catalog/product/{link.source_product_id}/change/'
                    elif link.source_blog_post_id:
                        icon = 'blog'
                        admin_url = f'/en/admin/blog/blogpost/{link.source_blog_post_id}/change/'
                    elif link.source_category_id:
                        icon = 'folder'
                        admin_url = f'/en/admin/catalog/category/{link.source_category_id}/change/'

                    existing_group = {
                        'key': group_key,
                        'source_type_display': source_type_display,
                        'source_title': link.source_title,
                        'icon': icon,
                        'admin_url': admin_url,
                        'links': [],
                    }
                    grouped_links.append(existing_group)

                existing_group['links'].append(link)

        # Get steps for the summary table
        steps = job.steps.all()

        context = {
            'title': _('Migration Complete'),
            'opts': self.model._meta,
            'job': job,
            'steps': steps,
            'grouped_links': grouped_links,
            'total_links': total_links,
            'pending_count': pending_count,
            'high_confidence_count': high_confidence_count,
            'applied_count': applied_count,
        }

        return render(request, 'admin/migration/wizard/step6_complete.html', context)

    def update_content_link(self, request, job_id):
        """API: Update a single ContentLink status/URL"""
        import json
        from django.http import JsonResponse
        from migration.models import ContentLink

        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)

        job = get_object_or_404(MigrationJob, pk=job_id)

        try:
            data = json.loads(request.body)
            link_id = data.get('link_id')
            action = data.get('action')  # 'approve', 'skip', 'modify'
            custom_url = data.get('custom_url', '')

            link = ContentLink.objects.get(pk=link_id, job=job)

            if action == 'approve':
                link.status = 'approved'
            elif action == 'skip':
                link.status = 'skipped'
            elif action == 'modify':
                link.status = 'modified'
                link.final_url = custom_url
            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)

            link.save(update_fields=['status', 'final_url'])

            return JsonResponse({
                'success': True,
                'link_id': link.id,
                'status': link.status,
            })

        except ContentLink.DoesNotExist:
            return JsonResponse({'error': 'Link not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def bulk_approve_content_links(self, request, job_id):
        """API: Auto-approve all high confidence links"""
        from django.http import JsonResponse
        from migration.models import ContentLink

        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)

        job = get_object_or_404(MigrationJob, pk=job_id)

        count = ContentLink.objects.filter(
            job=job,
            status='pending',
            confidence__gte=0.85,
            suggested_url__gt='',
        ).update(status='approved')

        return JsonResponse({
            'success': True,
            'approved_count': count,
        })

    def apply_content_links(self, request, job_id):
        """API: Apply all approved/modified content links"""
        from django.http import JsonResponse
        from urllib.parse import urlparse
        from migration.services.content_link_processor import ContentLinkProcessor

        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)

        job = get_object_or_404(MigrationJob, pk=job_id)

        store_url = job.connection_config.get('store_url', '')
        source_domain = urlparse(store_url).netloc if store_url else ''

        processor = ContentLinkProcessor(
            source_domain=source_domain,
            migration_job=job,
        )

        stats = processor.apply_approved_links()

        return JsonResponse({
            'success': True,
            'applied': stats['applied'],
            'failed': stats['failed'],
            'skipped': stats['skipped'],
        })

    def rollback_migration(self, request, job_id):
        """Rollback a completed migration"""
        job = get_object_or_404(MigrationJob, pk=job_id)

        if not job.is_rollbackable:
            messages.error(request, _('This migration cannot be rolled back.'))
            return redirect('admin:migration_migrationjob_changelist')

        if request.method == 'POST':
            try:
                # Import rollback utility
                from .utils.rollback import rollback_migration
                rollback_migration(job)
                messages.success(request, _('Migration rolled back successfully!'))
            except Exception as e:
                messages.error(request, _('Rollback failed: {}').format(str(e)))

            return redirect('admin:migration_migrationjob_changelist')

        return render(request, 'admin/migration/confirm_rollback.html', {
            'title': _('Confirm Rollback'),
            'opts': self.model._meta,
            'job': job,
        })

    def retry_migration(self, request, job_id):
        """Retry a failed migration"""
        job = get_object_or_404(MigrationJob, pk=job_id)

        if job.status != 'failed':
            messages.error(request, _('Only failed migrations can be retried.'))
            return redirect('admin:migration_migrationjob_changelist')

        # Delete old steps and logs from previous attempt
        job.steps.all().delete()
        job.logs.all().delete()

        # Reset the migration job to pending state
        job.status = 'pending'
        job.progress_percent = 0
        job.current_step = ''
        job.error_summary = ''
        job.started_at = None
        job.completed_at = None
        job.duration_seconds = None

        # Reset statistics
        job.products_imported = 0
        job.products_failed = 0
        job.products_skipped = 0
        job.categories_imported = 0
        job.categories_failed = 0
        job.categories_skipped = 0
        job.customers_imported = 0
        job.customers_failed = 0
        job.customers_skipped = 0
        job.orders_imported = 0
        job.orders_failed = 0
        job.orders_skipped = 0
        job.reviews_imported = 0
        job.reviews_failed = 0
        job.reviews_skipped = 0
        job.coupons_imported = 0
        job.coupons_failed = 0
        job.coupons_skipped = 0

        job.save()

        # Start the migration immediately via Celery
        try:
            from .tasks import run_migration_job

            # Dispatch Celery task to run migration asynchronously
            task = run_migration_job.delay(str(job.id))

            # Store task ID for monitoring
            job.connection_config['celery_task_id'] = task.id
            job.status = 'running'
            job.started_at = timezone.now()
            job.save()

            logger.info(f"Retrying migration job {job.id} via Celery task {task.id}")
            messages.success(request, _('Migration restarted! Redirecting to progress page...'))
            return redirect('admin:migration_wizard_step5', job_id=job.id)

        except Exception as e:
            logger.error(f"Failed to restart migration: {e}")
            messages.error(request, _('Failed to restart migration: {}').format(str(e)))
            return redirect('admin:migration_wizard_step2', job_id=job.id)

    def cancel_migration(self, request, job_id):
        """Cancel a running migration"""
        job = get_object_or_404(MigrationJob, pk=job_id)

        if job.status != 'running':
            messages.error(request, _('Only running migrations can be cancelled.'))
            return redirect('admin:migration_migrationjob_changelist')

        # Update job status to failed/cancelled
        job.status = 'failed'
        job.error_summary = _('Migration cancelled by user')
        job.completed_at = timezone.now()

        # Calculate duration if started
        if job.started_at:
            duration = timezone.now() - job.started_at
            job.duration_seconds = int(duration.total_seconds())

        job.save()

        # Add log entry
        MigrationLog.objects.create(
            job=job,
            level='warning',
            message=_('Migration cancelled by {}').format(request.user.username),
            source_type='system',
            source_id='cancel_action'
        )

        messages.success(request, _('Migration cancelled successfully.'))
        return redirect('admin:migration_migrationjob_changelist')

    def delete_migration(self, request, job_id):
        """Delete a pending, failed, or running migration"""
        job = get_object_or_404(MigrationJob, pk=job_id)

        if job.status not in ['pending', 'failed', 'running']:
            messages.error(request, _('Only pending, failed, or running migrations can be deleted.'))
            return redirect('admin:migration_migrationjob_changelist')

        # Special warning for running migrations
        if job.status == 'running':
            messages.warning(request, _('Deleted a running migration. If this was stuck, the operation has been cleaned up.'))

        # Delete the migration job (cascade will clean up logs, steps, etc.)
        job.delete()
        messages.success(request, _('Migration deleted successfully.'))
        return redirect('admin:migration_migrationjob_changelist')

    def get_progress(self, request, job_id):
        """API endpoint for progress updates"""
        job = get_object_or_404(MigrationJob, pk=job_id)

        # Get recent steps with progress data
        steps_data = []
        for step in job.steps.all():
            total = step.items_total or 1  # Avoid division by zero
            # Progress includes imported, skipped, AND failed items (all are "processed")
            processed = step.items_imported + step.items_skipped + step.items_failed
            progress = (processed / total * 100) if total > 0 else 0

            steps_data.append({
                'step_type': step.step_type,
                'status': step.status,
                'total': step.items_total,
                'imported': step.items_imported,
                'skipped': step.items_skipped,
                'failed': step.items_failed,
                'progress': min(100, progress),
                'current_item': step.current_item or '',
            })

        # Get recent logs
        recent_logs = job.logs.order_by('-timestamp')[:20]
        logs_data = [{
            'timestamp': log.timestamp.strftime('%H:%M:%S'),
            'level': log.level,
            'message': log.message,
        } for log in recent_logs]

        # Calculate overall progress - only for selected import types
        config = job.connection_config or {}

        total_imported = 0
        total_skipped = 0
        total_failed = 0
        total_items = 0

        # Map of import flag → (total_key, imported_attr, skipped_attr, failed_attr)
        TYPE_COUNTERS = {
            'import_categories': ('total_categories', 'categories_imported', 'categories_skipped', 'categories_failed'),
            'import_products': ('total_products', 'products_imported', 'products_skipped', 'products_failed'),
            'import_customers': ('total_customers', 'customers_imported', 'customers_skipped', 'customers_failed'),
            'import_orders': ('total_orders', 'orders_imported', 'orders_skipped', 'orders_failed'),
            'import_reviews': ('total_reviews', 'reviews_imported', 'reviews_skipped', 'reviews_failed'),
            'import_coupons': ('total_coupons', 'coupons_imported', 'coupons_skipped', 'coupons_failed'),
            'import_blog': ('total_blog_posts', 'blog_posts_imported', 'blog_posts_skipped', 'blog_posts_failed'),
        }

        for flag, (total_key, imp_attr, skip_attr, fail_attr) in TYPE_COUNTERS.items():
            if config.get(flag, False):
                total_items += config.get(total_key, 0)
                total_imported += getattr(job, imp_attr, 0)
                total_skipped += getattr(job, skip_attr, 0)
                total_failed += getattr(job, fail_attr, 0)

        # For blog, also add categories and tags to totals
        if config.get('import_blog', False):
            total_items += config.get('total_blog_categories', 0) + config.get('total_blog_tags', 0)
            total_imported += getattr(job, 'blog_categories_imported', 0) + getattr(job, 'blog_tags_imported', 0)
            total_skipped += getattr(job, 'blog_categories_skipped', 0) + getattr(job, 'blog_tags_skipped', 0)

        # Fallback to dynamic calculation if saved counts not available (for old migrations)
        if total_items == 0:
            total_items = sum(step.items_total for step in job.steps.all() if step.items_total > 0)

        # When job is running, use real-time step-level data for more accurate progress
        if job.status == 'running' and steps_data:
            step_imported = sum(s['imported'] for s in steps_data)
            step_skipped = sum(s['skipped'] for s in steps_data)
            step_failed = sum(s['failed'] for s in steps_data)
            # Use step data if it has more progress than job-level counters
            if (step_imported + step_skipped + step_failed) > (total_imported + total_skipped + total_failed):
                total_imported = step_imported
                total_skipped = step_skipped
                total_failed = step_failed
            # Also use step totals if they're more accurate (set during import)
            step_total = sum(s['total'] for s in steps_data)
            if step_total > 0:
                total_items = step_total

        total_processed = total_imported + total_skipped + total_failed
        overall_progress = (total_processed / total_items * 100) if total_items > 0 else job.progress_percent

        return JsonResponse({
            'status': job.status,
            'status_display': job.get_status_display(),
            'overall_progress': min(100, overall_progress),
            'steps': steps_data,
            'recent_logs': logs_data,
            'total_items': total_items,
            'total_imported': total_imported,
            'total_skipped': total_skipped,
            'total_failed': total_failed,
        })

    def get_logs(self, request, job_id):
        """Get full logs for a job"""
        job = get_object_or_404(MigrationJob, pk=job_id)
        level = request.GET.get('level', None)

        logs = job.logs.all()
        if level:
            logs = logs.filter(level=level)

        logs_data = [{
            'timestamp': log.timestamp.isoformat(),
            'level': log.level,
            'message': log.message,
            'source_type': log.source_type,
            'source_id': log.source_id,
        } for log in logs[:500]]  # Limit to 500 logs

        return JsonResponse({'logs': logs_data})

    def test_connection(self, request, job_id):
        """Test API connection"""
        job = get_object_or_404(MigrationJob, pk=job_id)

        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

        if job.platform == 'shopify':
            return self._test_shopify_connection(request, job)

        if job.platform == 'magento':
            return self._test_magento_connection(request, job)

        # WooCommerce connection test
        store_url = request.POST.get('store_url', '').strip()
        consumer_key = request.POST.get('consumer_key', '').strip()
        consumer_secret = request.POST.get('consumer_secret', '').strip()

        if not all([store_url, consumer_key, consumer_secret]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required credentials'
            })

        try:
            from .fetchers.woocommerce_api import WooCommerceAPIClient

            logger.info(f"Testing WooCommerce connection to {store_url}...")

            client = WooCommerceAPIClient(
                store_url=store_url,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret
            )

            result = client.test_connection()

            if result.get('success'):
                api_version = client.get_api_version()
                logger.info(f"Connection to {store_url} successful (API: {api_version})")
                return JsonResponse({
                    'success': True,
                    'message': f'Connected successfully to {store_url}',
                    'api_version': api_version
                })
            else:
                error_msg = result.get('error', 'Connection test failed.')
                logger.warning(f"Connection to {store_url} failed: {error_msg}")
                return JsonResponse({
                    'success': False,
                    'error': error_msg
                })

        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    def _test_shopify_connection(self, request, job):
        """Test Shopify API connection using client credentials."""
        store_domain = request.POST.get('store_domain', '').strip()
        client_id = request.POST.get('client_id', '').strip()
        client_secret = request.POST.get('client_secret', '').strip()

        # Normalize domain
        store_domain = store_domain.replace('https://', '').replace('http://', '').rstrip('/')

        if not all([store_domain, client_id, client_secret]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required credentials (store domain, client ID, and client secret are all required)'
            })

        try:
            from .fetchers.shopify_api import ShopifyAPIClient

            logger.info(f"Testing Shopify connection to {store_domain}...")

            client = ShopifyAPIClient(
                store_domain=store_domain,
                client_id=client_id,
                client_secret=client_secret,
            )

            result = client.test_connection()

            if result.get('success'):
                shop_info = result.get('shop_info', {})
                shop_name = shop_info.get('name', store_domain)
                logger.info(f"Shopify connection to {store_domain} successful (shop: {shop_name})")

                # Also check scopes
                scopes = client.get_available_scopes()
                required_scopes = {'read_products', 'read_customers', 'read_orders'}
                granted = set(scopes)
                missing = required_scopes - granted

                response_data = {
                    'success': True,
                    'message': f'Connected successfully to {shop_name}',
                    'shop_name': shop_name,
                    'scopes': scopes,
                }

                if missing:
                    response_data['warning'] = f'Missing recommended scopes: {", ".join(sorted(missing))}'

                return JsonResponse(response_data)
            else:
                error_msg = result.get('error', 'Connection test failed.')
                logger.warning(f"Shopify connection to {store_domain} failed: {error_msg}")
                return JsonResponse({
                    'success': False,
                    'error': error_msg
                })

        except Exception as e:
            logger.error(f"Shopify connection test failed: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    def _test_magento_connection(self, request, job):
        """Test Magento REST API connection using Bearer token."""
        store_url = request.POST.get('store_url', '').strip().rstrip('/')
        access_token = request.POST.get('access_token', '').strip()

        if not all([store_url, access_token]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required credentials (store URL and access token are both required)'
            })

        try:
            from .fetchers.magento_api import MagentoAPIClient

            logger.info(f"Testing Magento connection to {store_url}...")

            client = MagentoAPIClient(
                store_url=store_url,
                access_token=access_token,
            )

            result = client.test_connection()

            if result.get('success'):
                store_info = result.get('store_info', {})
                currency = store_info.get('currency', 'USD')
                logger.info(f"Magento connection to {store_url} successful (currency: {currency})")
                return JsonResponse({
                    'success': True,
                    'message': f'Connected successfully to Magento store (currency: {currency})',
                })
            else:
                error_msg = result.get('error', 'Connection test failed.')
                logger.warning(f"Magento connection to {store_url} failed: {error_msg}")
                return JsonResponse({
                    'success': False,
                    'error': error_msg
                })

        except Exception as e:
            logger.error(f"Magento connection test failed: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    def preview_data(self, request, job_id):
        """Preview available data"""
        job = get_object_or_404(MigrationJob, pk=job_id)
        # Will implement with fetchers
        return JsonResponse({'success': True, 'data': {}})

    def start_import(self, request, job_id):
        """Start the import process"""
        job = get_object_or_404(MigrationJob, pk=job_id)
        # Will implement with importers
        return JsonResponse({'success': True, 'job_id': str(job.id)})

    def download_template(self, request, template_type):
        """Download CSV template for data import"""
        # Will implement CSV template generation
        from django.http import HttpResponse
        import csv

        templates = {
            'products': ['id', 'name', 'slug', 'description', 'price', 'sku', 'stock_quantity', 'category'],
            'categories': ['id', 'name', 'slug', 'description', 'parent_id'],
            'customers': ['id', 'email', 'first_name', 'last_name', 'phone'],
            'orders': ['id', 'customer_email', 'order_date', 'status', 'total', 'currency'],
            'reviews': ['id', 'product_id', 'customer_email', 'rating', 'comment', 'date'],
        }

        if template_type not in templates:
            return JsonResponse({'error': 'Invalid template type'}, status=400)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{template_type}_template.csv"'

        writer = csv.writer(response)
        writer.writerow(templates[template_type])

        return response

    def download_bridge_plugin(self, request):
        """Download the Spwig Migration Bridge WordPress plugin ZIP."""
        import os
        zip_path = os.path.join(
            os.path.dirname(__file__),
            'static', 'migration', 'downloads',
            'spwig-migration-bridge.zip'
        )

        if not os.path.exists(zip_path):
            return JsonResponse(
                {'error': 'Plugin ZIP not found. Run: python manage.py build_bridge_plugin_zip'},
                status=404
            )

        return FileResponse(
            open(zip_path, 'rb'),
            as_attachment=True,
            filename='spwig-migration-bridge.zip',
            content_type='application/zip'
        )

    def download_report(self, request, job_id):
        """Download migration report as CSV or PDF"""
        from django.http import HttpResponse
        import csv

        job = get_object_or_404(MigrationJob, pk=job_id)
        report_format = request.GET.get('format', 'csv')

        if report_format == 'pdf':
            return self._generate_pdf_report(job)

        # Default: CSV report
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="migration_report_{job.id}.csv"'

        writer = csv.writer(response)

        # Job metadata
        writer.writerow(['Migration Report'])
        writer.writerow(['Job ID', str(job.id)])
        writer.writerow(['Platform', job.get_platform_display()])
        writer.writerow(['Status', job.get_status_display()])
        writer.writerow(['Started', job.started_at.isoformat() if job.started_at else ''])
        writer.writerow(['Completed', job.completed_at.isoformat() if job.completed_at else ''])
        writer.writerow(['Duration (seconds)', job.duration_seconds or ''])
        writer.writerow(['Success Rate', f'{job.success_rate}%'])
        writer.writerow([])

        # Summary
        writer.writerow(['Summary'])
        writer.writerow(['Total Items', job.total_items])
        writer.writerow(['Imported', job.total_imported])
        writer.writerow(['Skipped', job.total_skipped])
        writer.writerow(['Failed', job.total_failed])
        writer.writerow([])

        # Per-step breakdown
        writer.writerow(['Step Breakdown'])
        writer.writerow(['Step', 'Status', 'Total', 'Imported', 'Skipped', 'Failed', 'Started', 'Completed'])
        for step in job.steps.all().order_by('started_at'):
            writer.writerow([
                step.get_step_type_display(),
                step.get_status_display(),
                step.items_total,
                step.items_imported,
                step.items_skipped,
                step.items_failed,
                step.started_at.isoformat() if step.started_at else '',
                step.completed_at.isoformat() if step.completed_at else '',
            ])

        # Error summary
        errors = job.logs.filter(level='error').values_list('message', flat=True)[:50]
        if errors:
            writer.writerow([])
            writer.writerow(['Errors (up to 50)'])
            writer.writerow(['Message'])
            for error_msg in errors:
                writer.writerow([error_msg])

        return response

    def _generate_pdf_report(self, job):
        """Generate a PDF migration report using reportlab"""
        from django.http import HttpResponse
        from io import BytesIO
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib import colors

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
            title=f'Migration Report - {job.id}'
        )

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
        ))
        styles.add(ParagraphStyle(
            name='SectionHead',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=16,
        ))

        story = []

        # Title
        story.append(Paragraph('Migration Report', styles['ReportTitle']))
        story.append(Spacer(1, 0.3 * inch))

        # Job metadata table
        meta_data = [
            [_('Job ID'), str(job.id)],
            [_('Platform'), job.get_platform_display()],
            [_('Status'), job.get_status_display()],
            [_('Started'), job.started_at.strftime('%Y-%m-%d %H:%M:%S') if job.started_at else '-'],
            [_('Completed'), job.completed_at.strftime('%Y-%m-%d %H:%M:%S') if job.completed_at else '-'],
            [_('Duration'), f'{job.duration_seconds}s' if job.duration_seconds else '-'],
            [_('Success Rate'), f'{job.success_rate}%'],
        ]
        meta_table = Table(meta_data, colWidths=[2 * inch, 4 * inch])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.3 * inch))

        # Summary stats
        story.append(Paragraph(_('Summary'), styles['SectionHead']))
        summary_data = [
            [_('Total Items'), _('Imported'), _('Skipped'), _('Failed')],
            [str(job.total_items), str(job.total_imported), str(job.total_skipped), str(job.total_failed)],
        ]
        summary_table = Table(summary_data, colWidths=[1.5 * inch] * 4)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3 * inch))

        # Step breakdown
        steps = job.steps.all().order_by('started_at')
        if steps.exists():
            story.append(Paragraph(_('Step Breakdown'), styles['SectionHead']))
            step_data = [[_('Step'), _('Status'), _('Total'), _('Imported'), _('Skipped'), _('Failed')]]
            for step in steps:
                step_data.append([
                    step.get_step_type_display(),
                    step.get_status_display(),
                    str(step.items_total),
                    str(step.items_imported),
                    str(step.items_skipped),
                    str(step.items_failed),
                ])
            step_table = Table(step_data, colWidths=[1.5 * inch, 1 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch])
            step_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            ]))
            story.append(step_table)
            story.append(Spacer(1, 0.3 * inch))

        # Top errors
        errors = list(job.logs.filter(level='error').values_list('message', flat=True)[:20])
        if errors:
            from xml.sax.saxutils import escape as xml_escape
            story.append(Paragraph(_('Errors'), styles['SectionHead']))
            for err in errors:
                # Truncate long error messages and XML-escape for reportlab Paragraph
                display_err = err[:200] + '...' if len(err) > 200 else err
                story.append(Paragraph(f'• {xml_escape(display_err)}', styles['Normal']))

        doc.build(story)

        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="migration_report_{job.id}.pdf"'
        return response

    def download_logs(self, request, job_id):
        """Download migration logs as CSV"""
        from django.http import HttpResponse
        import csv

        job = get_object_or_404(MigrationJob, pk=job_id)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="migration_logs_{job.id}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Timestamp', 'Level', 'Message', 'Source Type', 'Source ID', 'Action'])

        for log in job.logs.all().order_by('timestamp'):
            writer.writerow([
                log.timestamp.isoformat(),
                log.level,
                log.message,
                log.source_type,
                log.source_id,
                log.action,
            ])

        return response


# Register other models for reference
@admin.register(MigrationStep)
class MigrationStepAdmin(admin.ModelAdmin):
    list_display = ['job', 'step_type', 'status', 'items_imported', 'items_failed', 'duration_seconds']
    list_filter = ['status', 'step_type']
    readonly_fields = ['job', 'savepoint_id', 'started_at', 'completed_at', 'duration_seconds']

    def has_add_permission(self, request):
        return False


@admin.register(MigrationLog)
class MigrationLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'job', 'level', 'message_preview', 'source_type', 'source_id']
    list_filter = ['level', 'source_type', 'timestamp']
    search_fields = ['message', 'source_id']
    readonly_fields = ['job', 'step', 'timestamp', 'level', 'message', 'source_type', 'source_id', 'context']

    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = _('Message')

    def has_add_permission(self, request):
        return False


@admin.register(MigrationMapping)
class MigrationMappingAdmin(admin.ModelAdmin):
    list_display = ['job', 'source_type', 'mapping_display', 'transform_type', 'times_used', 'times_failed']
    list_filter = ['source_type', 'dest_model', 'transform_type', 'is_auto_detected']
    search_fields = ['source_field', 'dest_field']

    def mapping_display(self, obj):
        return f"{obj.source_field} → {obj.dest_model}.{obj.dest_field}"
    mapping_display.short_description = _('Mapping')

    def has_add_permission(self, request):
        return False


# Import sync admin registrations so Django autodiscovery picks them up
from . import sync_admin  # noqa: F401, E402
