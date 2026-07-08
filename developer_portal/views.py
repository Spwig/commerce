"""
Developer Portal Views
Provides views for developer registration, dashboard, submission management,
and analytics. Follows the affiliate portal pattern (standalone views with
own base template, outside the admin).
"""

import json
import zipfile
import logging
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _, gettext
from django.utils import timezone
from django.db.models import Count, Sum, Q, Avg

from .models import (
    DeveloperProfile, ComponentSubmission, SubmissionReview,
    ComponentAnalytics, DailyDownloadStat, ComponentReviewMirror,
    DeveloperLicenseRequest,
)
from .services.validation import validate_package
from .services.component_types import get_submittable_types

logger = logging.getLogger(__name__)


# ============================================
# Mixins
# ============================================

class DeveloperPortalBrandingMixin:
    """Mixin to provide Spwig branding context to developer portal views."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            from design.theme_models import ThemeBranding
            branding = ThemeBranding.objects.first()
            if branding:
                context['brand_css_url'] = branding.get_css_url()
        except Exception:
            pass

        # Unread review count for nav badge
        if (self.request.user.is_authenticated
                and hasattr(self.request.user, 'developer_profile')
                and self.request.user.developer_profile.is_approved):
            context['unread_reviews_count'] = (
                self.request.user.developer_profile.component_reviews
                .filter(is_read=False).count()
            )

        return context


class DeveloperRequiredMixin(UserPassesTestMixin):
    """Mixin to require user to have an approved developer profile."""

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return (
            hasattr(self.request.user, 'developer_profile')
            and self.request.user.developer_profile.is_approved
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('account_login')
        if hasattr(self.request.user, 'developer_profile'):
            profile = self.request.user.developer_profile
            if profile.status == DeveloperProfile.Status.PENDING:
                messages.info(self.request, _('Your developer application is pending review.'))
            elif profile.status == DeveloperProfile.Status.REJECTED:
                messages.error(self.request, _('Your developer application was not approved.'))
            elif profile.status == DeveloperProfile.Status.SUSPENDED:
                messages.error(self.request, _('Your developer account has been suspended.'))
        else:
            messages.info(self.request, _('You need a developer account to access this page.'))
        return redirect('developer_portal:portal')


# ============================================
# Public Views
# ============================================

class PortalView(DeveloperPortalBrandingMixin, TemplateView):
    """Landing page for the developer program."""
    template_name = 'developer_portal/portal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_developers'] = DeveloperProfile.objects.filter(
            status=DeveloperProfile.Status.APPROVED
        ).count()
        context['total_components'] = ComponentSubmission.objects.filter(
            is_published=True
        ).count()

        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'developer_profile'):
                context['has_profile'] = True
                context['profile'] = self.request.user.developer_profile
            else:
                context['has_profile'] = False
                context['can_register'] = True

        return context


# ============================================
# Terms & Conditions
# ============================================

class TermsView(DeveloperPortalBrandingMixin, TemplateView):
    """Developer Terms of Service page."""
    template_name = 'developer_portal/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['show_register_cta'] = not hasattr(self.request.user, 'developer_profile')
        return context


# ============================================
# Registration
# ============================================

class RegistrationView(DeveloperPortalBrandingMixin, LoginRequiredMixin, TemplateView):
    """Developer registration form."""
    template_name = 'developer_portal/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'developer_profile'):
            messages.info(request, _('You already have a developer profile.'))
            return redirect('developer_portal:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['terms_url'] = reverse('developer_portal:terms')
        return context

    def post(self, request, *args, **kwargs):
        developer_slug = request.POST.get('developer_slug', '').strip()
        display_name = request.POST.get('display_name', '').strip()
        bio = request.POST.get('bio', '').strip()
        website = request.POST.get('website', '').strip()
        terms_accepted = request.POST.get('terms_accepted') == 'on'

        errors = {}
        if not developer_slug:
            errors['developer_slug'] = _('Developer slug is required.')
        elif DeveloperProfile.objects.filter(developer_slug=developer_slug).exists():
            errors['developer_slug'] = _('This slug is already taken.')
        if not display_name:
            errors['display_name'] = _('Display name is required.')
        if not terms_accepted:
            errors['terms_accepted'] = _('You must accept the developer terms.')

        if errors:
            return render(request, self.template_name, {
                'errors': errors,
                'form_data': request.POST,
                'terms_url': reverse('developer_portal:terms'),
            })

        profile = DeveloperProfile.objects.create(
            user=request.user,
            developer_slug=developer_slug,
            display_name=display_name,
            bio=bio,
            website=website,
            terms_accepted_at=timezone.now() if terms_accepted else None,
        )

        # Log to Sales Bell
        try:
            from core.models import SalesBellEvent
            SalesBellEvent.log_developer_signup(profile)
        except Exception:
            pass

        # Send registration acknowledgement email
        from .services.email_service import DeveloperEmailService
        DeveloperEmailService.send_registration_ack(profile)

        messages.success(
            request,
            _('Your developer application has been submitted. We will review it shortly.')
        )
        return redirect('developer_portal:portal')


# ============================================
# Dashboard
# ============================================

class DashboardView(DeveloperPortalBrandingMixin, LoginRequiredMixin, DeveloperRequiredMixin, TemplateView):
    """Main developer dashboard."""
    template_name = 'developer_portal/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.developer_profile

        submissions = profile.submissions.all()
        context['total_submissions'] = submissions.count()
        context['published_components'] = submissions.filter(is_published=True).count()
        context['pending_reviews'] = submissions.filter(
            review_status=ComponentSubmission.ReviewStatus.PENDING,
            validation_status=ComponentSubmission.ValidationStatus.PASSED,
        ).count()
        context['revision_requested'] = submissions.filter(
            review_status=ComponentSubmission.ReviewStatus.REVISION_REQUESTED,
        ).count()
        context['recent_submissions'] = submissions[:5]
        context['profile'] = profile
        context['has_free_license'] = profile.has_free_license

        return context


# ============================================
# Submissions
# ============================================

class SubmissionListView(DeveloperPortalBrandingMixin, LoginRequiredMixin, DeveloperRequiredMixin, ListView):
    """List all submissions for the current developer."""
    template_name = 'developer_portal/submissions/list.html'
    context_object_name = 'submissions'
    paginate_by = 20

    def get_queryset(self):
        return self.request.user.developer_profile.submissions.all()


class SubmissionCreateView(DeveloperPortalBrandingMixin, LoginRequiredMixin, DeveloperRequiredMixin, TemplateView):
    """Component submission wizard - upload and validate a component package."""
    template_name = 'developer_portal/submissions/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['component_types'] = get_submittable_types()
        return context

    def post(self, request, *args, **kwargs):
        package_file = request.FILES.get('package_file')
        description = request.POST.get('description', '').strip()
        changelog = request.POST.get('changelog', '').strip()
        pricing_model = request.POST.get('pricing_model', 'free')
        price = request.POST.get('price', '0')
        component_type = request.POST.get('component_type', 'theme')

        # Validate component_type is in the submittable list
        valid_slugs = [t['slug'] for t in get_submittable_types()]
        if component_type not in valid_slugs:
            messages.error(request, _('Invalid component type.'))
            return render(request, self.template_name, {
                'form_data': request.POST,
                'component_types': get_submittable_types(),
            })

        if not package_file:
            messages.error(request, _('Please upload a component package.'))
            return render(request, self.template_name, {
                'form_data': request.POST,
                'component_types': get_submittable_types(),
            })

        # Validate the package using the appropriate validator
        validation_result = validate_package(package_file, component_type)

        if not validation_result['valid']:
            messages.error(request, _('Package validation failed.'))
            return render(request, self.template_name, {
                'form_data': request.POST,
                'validation_errors': validation_result['errors'],
                'component_types': get_submittable_types(),
            })

        manifest = validation_result['manifest']
        profile = request.user.developer_profile

        # Create the submission
        submission = ComponentSubmission(
            developer=profile,
            component_type=component_type,
            component_slug=manifest.get('name', manifest.get('slug', '')),
            component_name=manifest.get('display_name', manifest.get('name', '')),
            version=manifest.get('version', '0.0.0'),
            description=description or manifest.get('description', ''),
            changelog=changelog,
            package_file=package_file,
            manifest_data=manifest,
            package_size_bytes=package_file.size,
            pricing_model=pricing_model,
            price=price if pricing_model == 'paid' else 0,
            validation_status=ComponentSubmission.ValidationStatus.PASSED,
            validation_results=validation_result,
            validated_at=timezone.now(),
        )
        submission.package_checksum = submission.calculate_checksum()
        submission.save()

        # Create validation review entry
        SubmissionReview.objects.create(
            submission=submission,
            reviewer=request.user,
            action=SubmissionReview.Action.VALIDATION_PASSED,
            comment=_('Automated validation passed.'),
        )

        # Send submission received email
        from .services.email_service import DeveloperEmailService
        DeveloperEmailService.send_submission_received(submission)

        messages.success(
            request,
            _('%(type)s "%(name)s" v%(version)s submitted successfully. It will be reviewed by our team.') % {
                'type': submission.type_display,
                'name': submission.component_name,
                'version': submission.version,
            }
        )
        return redirect('developer_portal:submission_detail', pk=submission.pk)


class SubmissionDetailView(DeveloperPortalBrandingMixin, LoginRequiredMixin, DeveloperRequiredMixin, DetailView):
    """View submission details and review timeline."""
    template_name = 'developer_portal/submissions/detail.html'
    context_object_name = 'submission'

    def get_queryset(self):
        return self.request.user.developer_profile.submissions.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_timeline'] = self.object.reviews.select_related('reviewer').all()
        return context


# ============================================
# Profile
# ============================================

class ProfileView(DeveloperPortalBrandingMixin, LoginRequiredMixin, DeveloperRequiredMixin, TemplateView):
    """Developer profile settings."""
    template_name = 'developer_portal/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.developer_profile
        return context

    def post(self, request, *args, **kwargs):
        profile = request.user.developer_profile
        profile.display_name = request.POST.get('display_name', profile.display_name).strip()
        profile.bio = request.POST.get('bio', profile.bio).strip()
        profile.website = request.POST.get('website', profile.website).strip()

        # Notification preferences
        review_pref = request.POST.get('review_notification_preference', '')
        if review_pref in ('immediate', 'daily', 'weekly', 'none'):
            profile.review_notification_preference = review_pref

        update_fields = ['display_name', 'bio', 'website', 'review_notification_preference', 'updated_at']

        # Handle logo upload
        logo_file = request.FILES.get('logo')
        if logo_file:
            from media_library.serializers import MediaAssetCreateSerializer
            title = logo_file.name.rsplit('.', 1)[0] if '.' in logo_file.name else logo_file.name
            serializer = MediaAssetCreateSerializer(
                data={'original_file': logo_file, 'title': title, 'alt_text': profile.display_name},
                context={'request': request}
            )
            if serializer.is_valid():
                try:
                    asset = serializer.save(uploaded_by=request.user)
                    profile.logo = asset
                    update_fields.append('logo')
                except Exception as e:
                    logger.error('Logo upload failed for %s: %s', profile.developer_slug, e)
                    messages.error(request, _('Logo upload failed. Please try JPG or PNG format.'))
            else:
                messages.error(request, _('Invalid logo file. Please use JPG, PNG, or WebP.'))

        # Handle logo removal
        if request.POST.get('remove_logo') == '1' and profile.logo:
            profile.logo = None
            update_fields.append('logo')

        profile.save(update_fields=update_fields)

        # Sync profile to upgrade server (non-blocking — local save succeeds regardless)
        self._sync_to_upgrade_server(profile)

        messages.success(request, _('Profile updated successfully.'))
        return redirect('developer_portal:profile')

    def _sync_to_upgrade_server(self, profile):
        """Sync developer profile data (including logo) to the upgrade server."""
        import requests as http_requests
        from django.conf import settings as django_settings

        base_url = getattr(django_settings, 'UPGRADE_SERVER_URL', '')
        api_key = getattr(django_settings, 'UPGRADE_SERVER_INTERNAL_API_KEY', '')
        if not base_url or not api_key:
            return

        try:
            data = {
                'slug': profile.developer_slug,
                'name': profile.display_name,
                'description': profile.bio,
                'homepage': profile.website,
            }

            files = {}
            if profile.logo and profile.logo.original_file:
                profile.logo.original_file.open('rb')
                fname = profile.logo.original_file.name.rsplit('/', 1)[-1] if profile.logo.original_file.name else 'logo.png'
                files['logo'] = (
                    fname,
                    profile.logo.original_file,
                    profile.logo.mime_type or 'image/png',
                )

            response = http_requests.post(
                f'{base_url}/api/v1/internal/authors/',
                data=data,
                files=files if files else None,
                headers={'X-API-KEY': api_key},
                timeout=15,
            )
            response.raise_for_status()

            # Store author slug if not set yet
            if not profile.upgrade_server_author_slug:
                result = response.json()
                profile.upgrade_server_author_slug = result.get('slug', profile.developer_slug)
                profile.save(update_fields=['upgrade_server_author_slug'])

        except Exception as e:
            logger.warning('Failed to sync profile to upgrade server: %s', str(e))


class RegenerateApiKeyView(LoginRequiredMixin, DeveloperRequiredMixin, View):
    """Regenerate the developer's API key."""

    def post(self, request, *args, **kwargs):
        profile = request.user.developer_profile
        new_key = profile.regenerate_api_key()
        messages.success(request, _('API key regenerated. Your new key is shown below.'))
        return redirect('developer_portal:profile')


# ============================================
# Analytics
# ============================================

class AnalyticsView(DeveloperPortalBrandingMixin, LoginRequiredMixin, DeveloperRequiredMixin, TemplateView):
    """Developer analytics - download stats, earnings."""
    template_name = 'developer_portal/analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.developer_profile
        context['profile'] = profile

        # Per-component stats from local mirror
        component_stats = profile.component_analytics.all()
        context['component_stats'] = component_stats
        context['total_downloads'] = sum(c.downloads_total for c in component_stats)
        context['total_downloads_period'] = sum(c.downloads_period for c in component_stats)
        context['total_published'] = component_stats.filter(is_published=True).count()

        # Daily download chart data (last 30 days)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        daily_stats = profile.daily_download_stats.filter(
            date__gte=thirty_days_ago
        ).order_by('date')
        context['chart_labels'] = json.dumps([str(d.date) for d in daily_stats])
        context['chart_data'] = json.dumps([d.downloads for d in daily_stats])

        # Review summary
        reviews = profile.component_reviews.all()
        context['total_reviews'] = reviews.count()
        avg = reviews.aggregate(avg=Avg('rating'))['avg']
        context['average_rating'] = round(avg, 1) if avg else 0
        context['unresponded_reviews'] = reviews.filter(developer_response='').count()

        context['total_earnings'] = 0  # Placeholder for revenue sharing

        return context


# ============================================
# Reviews
# ============================================

class ReviewsView(DeveloperPortalBrandingMixin, LoginRequiredMixin, DeveloperRequiredMixin, ListView):
    """View and respond to component reviews."""
    template_name = 'developer_portal/reviews.html'
    context_object_name = 'reviews'
    paginate_by = 20

    def get_queryset(self):
        profile = self.request.user.developer_profile
        qs = profile.component_reviews.all()

        # Filter by component
        component_slug = self.request.GET.get('component')
        if component_slug:
            qs = qs.filter(component_slug=component_slug)

        # Filter by responded/unresponded
        status_filter = self.request.GET.get('status')
        if status_filter == 'unresponded':
            qs = qs.filter(developer_response='')
        elif status_filter == 'responded':
            qs = qs.exclude(developer_response='')

        # Filter by rating
        rating = self.request.GET.get('rating')
        if rating and rating.isdigit():
            qs = qs.filter(rating=int(rating))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.developer_profile
        context['profile'] = profile

        # Unique component slugs for filter dropdown
        context['components'] = (
            profile.component_reviews
            .values('component_slug', 'component_name')
            .distinct()
            .order_by('component_name')
        )
        context['current_component'] = self.request.GET.get('component', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_rating'] = self.request.GET.get('rating', '')

        # Mark displayed reviews as read
        displayed_ids = [r.pk for r in context['reviews']]
        if displayed_ids:
            profile.component_reviews.filter(
                pk__in=displayed_ids, is_read=False
            ).update(is_read=True)

        return context


class ReviewRespondView(LoginRequiredMixin, DeveloperRequiredMixin, View):
    """AJAX endpoint for developers to respond to reviews."""

    def post(self, request, pk):
        profile = request.user.developer_profile
        review = get_object_or_404(
            ComponentReviewMirror, pk=pk, developer=profile
        )

        response_text = request.POST.get('response', '').strip()

        if not response_text:
            return JsonResponse({'error': _('Response text is required.')}, status=400)

        if len(response_text) > 2000:
            return JsonResponse({'error': _('Response must be under 2000 characters.')}, status=400)

        # Save locally and mark for sync
        review.developer_response = response_text
        review.developer_response_at = timezone.now()
        review.response_synced = False
        review.save(update_fields=[
            'developer_response', 'developer_response_at',
            'response_synced', 'last_synced_at',
        ])

        # Attempt immediate push to upgrade server (best effort)
        try:
            from .services.analytics_service import AnalyticsService
            service = AnalyticsService()
            success = service.push_review_response(
                review_id=review.upgrade_server_review_id,
                author_slug=profile.upgrade_server_author_slug,
                response_text=response_text,
            )
            if success:
                review.response_synced = True
                review.save(update_fields=['response_synced'])
        except Exception:
            pass  # Will sync on next Celery beat cycle

        return JsonResponse({
            'success': True,
            'response': review.developer_response,
            'responded_at': review.developer_response_at.isoformat(),
        })


# ============================================
# Developer Licenses
# ============================================

class LicenseView(DeveloperPortalBrandingMixin, LoginRequiredMixin, DeveloperRequiredMixin, TemplateView):
    """
    Developer license management page.

    - First license: free, auto-provisioned via update server
    - Additional licenses: EUR 100 via Airwallex checkout
    """
    template_name = 'developer_portal/license_request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.developer_profile
        context['profile'] = profile

        # All non-rejected licenses
        licenses = profile.license_requests.exclude(
            status=DeveloperLicenseRequest.Status.REJECTED
        ).order_by('-created_at')
        context['licenses'] = licenses
        context['has_free_license'] = profile.has_free_license

        # Country choices for the form
        from django_countries import countries
        context['countries'] = list(countries)

        return context

    def post(self, request, *args, **kwargs):
        """Claim free developer license."""
        profile = request.user.developer_profile

        # Guard: only one free license allowed
        if profile.has_free_license:
            messages.warning(request, _('You have already claimed your free developer license.'))
            return redirect('developer_portal:license')

        # Collect and save company/country to profile
        company_name = request.POST.get('company_name', '').strip()
        country_code = request.POST.get('country', '').strip()

        if not company_name:
            messages.error(request, _('Company or organization name is required.'))
            return redirect('developer_portal:license')

        if not country_code:
            messages.error(request, _('Country is required.'))
            return redirect('developer_portal:license')

        profile.company_name = company_name
        profile.country = country_code
        profile.save(update_fields=['company_name', 'country', 'updated_at'])

        # Create the license request
        license_request = DeveloperLicenseRequest.objects.create(
            developer=profile,
            is_free=True,
            license_type=DeveloperLicenseRequest.LicenseType.BOTH,
            reason=_('Free developer license'),
        )

        # Auto-provision via update server
        from .services.license_provisioning import provision_dev_license
        try:
            provision_dev_license(license_request)
            messages.success(
                request,
                _('Your free developer license has been provisioned! '
                  'Use the setup token below to activate your Spwig installation.')
            )
        except Exception as e:
            logger.error(f"Failed to provision free dev license: {e}")
            messages.error(
                request,
                _('Could not provision your license at this time. '
                  'Please try again later or contact support.')
            )

        return redirect('developer_portal:license')


class PurchaseAdditionalLicenseView(LoginRequiredMixin, DeveloperRequiredMixin, View):
    """Initiate Airwallex checkout for an additional developer license (EUR 100)."""

    def post(self, request, *args, **kwargs):
        from decimal import Decimal
        from django.conf import settings as django_settings
        from djmoney.money import Money

        profile = request.user.developer_profile

        # Find or create the dev license product
        from catalog.models import Product, Category
        marketplace_category, _ = Category.objects.get_or_create(
            slug='marketplace',
            defaults={'name': 'Marketplace'},
        )
        product, _ = Product.objects.get_or_create(
            sku='dev-license-additional',
            defaults={
                'name': 'Additional Developer License (Shop + POS)',
                'slug': 'developer-license-additional',
                'product_type': 'digital',
                'price': Money(Decimal('100.00'), 'EUR'),
                'status': 'published',
                'track_inventory': False,
                'category': marketplace_category,
            }
        )

        # Create cart
        from cart.models import Cart, CheckoutSession
        from cart.services.cart_service import CartService

        cart = Cart.objects.create(user=request.user)
        success, msg, cart_item = CartService.add_item(
            cart=cart,
            product_id=product.id,
            quantity=1,
        )
        if not success:
            messages.error(request, _('Failed to create cart: %(msg)s') % {'msg': msg})
            return redirect('developer_portal:license')

        # Create checkout session
        session = CheckoutSession.objects.create(
            cart=cart,
            subtotal=product.price,
            total_amount=product.price,
            step_completed='payment',
            metadata={
                'dev_license_purchase': True,
                'developer_profile_id': profile.id,
            },
            expires_at=timezone.now() + timedelta(hours=2),
        )

        # Find active payment provider (hosted checkout)
        from payment_providers.models import PaymentProviderAccount
        provider_account = PaymentProviderAccount.objects.filter(
            is_active=True,
            connection_status='connected',
            checkout_mode='hosted',
        ).first()

        if not provider_account:
            messages.error(request, _('Payment is not configured. Please contact support.'))
            return redirect('developer_portal:license')

        session.payment_provider = provider_account
        session.save(update_fields=['payment_provider'])

        # Create payment intent
        from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService

        frontend_base = request.build_absolute_uri('/').rstrip('/')
        return_url = f"{frontend_base}/developer-portal/license/?payment=success"
        cancel_url = f"{frontend_base}/developer-portal/license/?payment=cancelled"

        success, intent, message = PaymentOrchestrationService.create_payment_intent(
            checkout_session=session,
            provider_account=provider_account,
            return_url=return_url,
            cancel_url=cancel_url,
            metadata={
                'dev_license_purchase': True,
                'developer_profile_id': profile.id,
            }
        )

        if not success:
            messages.error(request, _('Payment initialization failed: %(msg)s') % {'msg': message})
            return redirect('developer_portal:license')

        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(intent.checkout_url)


class RegenerateSetupTokenView(LoginRequiredMixin, DeveloperRequiredMixin, View):
    """Regenerate an expired setup token for a developer license."""

    def post(self, request, pk):
        profile = request.user.developer_profile
        license_request = get_object_or_404(
            DeveloperLicenseRequest,
            pk=pk,
            developer=profile,
            status=DeveloperLicenseRequest.Status.APPROVED,
        )

        if not license_request.license_key:
            messages.error(request, _('This license has not been provisioned yet.'))
            return redirect('developer_portal:license')

        from .services.license_provisioning import regenerate_setup_token
        try:
            regenerate_setup_token(license_request)
            messages.success(request, _('Setup token regenerated successfully.'))
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            logger.error(f"Failed to regenerate setup token: {e}")
            messages.error(
                request,
                _('Could not regenerate the setup token. Please try again later.')
            )

        return redirect('developer_portal:license')


# ============================================
# AJAX API Endpoints
# ============================================

@login_required
@require_POST
def validate_package_api(request):
    """AJAX endpoint to validate a component package before submission."""
    package_file = request.FILES.get('package_file')
    if not package_file:
        return JsonResponse({'valid': False, 'errors': ['No file uploaded']})

    component_type = request.POST.get('component_type', 'theme')
    result = validate_package(package_file, component_type)
    return JsonResponse(result)
