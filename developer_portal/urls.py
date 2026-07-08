"""
Developer Portal URL Configuration
Defines URL patterns for the developer portal, dashboard, and submission management.
Only loaded when SPWIG_IS_HQ=true.
"""

from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'developer_portal'

urlpatterns = [
    # Public landing page
    path('', views.PortalView.as_view(), name='portal'),

    # Terms & Registration
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('register/', views.RegistrationView.as_view(), name='register'),

    # Dashboard (requires approved developer profile)
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # Submissions
    path('submissions/', views.SubmissionListView.as_view(), name='submissions'),
    path('submissions/new/', views.SubmissionCreateView.as_view(), name='submit'),
    path('submissions/<uuid:pk>/', views.SubmissionDetailView.as_view(), name='submission_detail'),

    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/regenerate-key/', views.RegenerateApiKeyView.as_view(), name='regenerate_key'),

    # Analytics
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),

    # Reviews
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),

    # Developer Licenses
    path('license/', views.LicenseView.as_view(), name='license'),
    path('license/purchase/', views.PurchaseAdditionalLicenseView.as_view(), name='license_purchase'),
    path('license/<uuid:pk>/regenerate-token/', views.RegenerateSetupTokenView.as_view(), name='regenerate_token'),
    # Backwards-compat redirect from old URL
    path('license-request/', RedirectView.as_view(pattern_name='developer_portal:license', permanent=True), name='license_request'),

    # AJAX API endpoints
    path('api/validate-package/', views.validate_package_api, name='validate_package'),
    path('api/reviews/<int:pk>/respond/', views.ReviewRespondView.as_view(), name='review_respond'),
]
