"""
Developer Portal Admin Views
AJAX filter endpoints for developer portal admin change_list pages.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q

from .models import DeveloperProfile, ComponentSubmission, DeveloperLicenseRequest


@staff_member_required
@require_GET
def filter_submissions(request):
    """
    AJAX endpoint for filtering component submissions in admin.

    Query Parameters:
    - search: Search by name, slug, or developer name
    - review_status: Filter by review status
    - validation: Filter by validation status
    - published: Filter by published (yes/no)
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    submissions = ComponentSubmission.objects.select_related('developer', 'reviewer')

    # Search filter
    search = request.GET.get('search', '').strip()
    if search:
        submissions = submissions.filter(
            Q(component_name__icontains=search) |
            Q(component_slug__icontains=search) |
            Q(developer__display_name__icontains=search)
        )

    # Review status filter
    review_status = request.GET.get('review_status', '')
    if review_status:
        submissions = submissions.filter(review_status=review_status)

    # Validation status filter
    validation = request.GET.get('validation', '')
    if validation:
        submissions = submissions.filter(validation_status=validation)

    # Published filter
    published = request.GET.get('published', '')
    if published == 'yes':
        submissions = submissions.filter(is_published=True)
    elif published == 'no':
        submissions = submissions.filter(is_published=False)

    submissions = submissions.order_by('-submitted_at')
    count = submissions.count()

    html = render_to_string(
        'admin/developer_portal/componentsubmission/partials/submission_cards.html',
        {'items': submissions[:100]},
        request=request,
    )

    return JsonResponse({'html': html, 'count': count})


@staff_member_required
@require_GET
def filter_developers(request):
    """
    AJAX endpoint for filtering developer profiles in admin.

    Query Parameters:
    - search: Search by name, slug, or email
    - status: Filter by status
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    developers = DeveloperProfile.objects.select_related('user').prefetch_related('submissions')

    # Search filter
    search = request.GET.get('search', '').strip()
    if search:
        developers = developers.filter(
            Q(display_name__icontains=search) |
            Q(developer_slug__icontains=search) |
            Q(user__email__icontains=search)
        )

    # Status filter
    status = request.GET.get('status', '')
    if status:
        developers = developers.filter(status=status)

    developers = developers.order_by('-created_at')
    count = developers.count()

    html = render_to_string(
        'admin/developer_portal/developerprofile/partials/developer_cards.html',
        {'items': developers[:100]},
        request=request,
    )

    return JsonResponse({'html': html, 'count': count})


@staff_member_required
@require_GET
def filter_license_requests(request):
    """
    AJAX endpoint for filtering developer license requests in admin.

    Query Parameters:
    - search: Search by developer name or email
    - status: Filter by status (pending/approved/rejected)
    - license_type: Filter by license type
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    requests_qs = DeveloperLicenseRequest.objects.select_related(
        'developer', 'developer__user', 'reviewed_by'
    )

    search = request.GET.get('search', '').strip()
    if search:
        requests_qs = requests_qs.filter(
            Q(developer__display_name__icontains=search) |
            Q(developer__user__email__icontains=search) |
            Q(license_key__icontains=search)
        )

    status = request.GET.get('status', '').strip()
    if status:
        requests_qs = requests_qs.filter(status=status)

    license_type = request.GET.get('license_type', '').strip()
    if license_type:
        requests_qs = requests_qs.filter(license_type=license_type)

    requests_qs = requests_qs.order_by('-created_at')
    count = requests_qs.count()

    html = render_to_string(
        'admin/developer_portal/developerlicenserequest/partials/request_cards.html',
        {'items': requests_qs[:100]},
        request=request,
    )

    return JsonResponse({'html': html, 'count': count})
