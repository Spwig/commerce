"""
Form Builder Admin AJAX Views.
Provides AJAX filter endpoints for admin change list pages.
"""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin, messages
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Q

from .models import Form


@staff_member_required
@require_GET
def filter_forms(request):
    """AJAX filter endpoint for Form entries."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    queryset = Form.objects.all()

    # Search filter
    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    # Status filter
    status = request.GET.get('status', '').strip()
    if status == 'active':
        queryset = queryset.filter(is_active=True)
    elif status == 'inactive':
        queryset = queryset.filter(is_active=False)

    # Multi-step filter
    multistep = request.GET.get('multistep', '').strip()
    if multistep == 'single':
        queryset = queryset.filter(is_multi_step=False)
    elif multistep == 'multi':
        queryset = queryset.filter(is_multi_step=True)

    total_count = queryset.count()
    forms = queryset.order_by('-created_at')[:100]

    html = render_to_string(
        'admin/form_builder/partials/form_cards.html',
        {'forms': forms},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': total_count,
    })


@staff_member_required
def form_recycle_bin(request):
    """View for form recycle bin - manage soft-deleted forms."""

    if request.method == 'POST':
        action = request.POST.get('action')
        form_ids = request.POST.getlist('form_ids')

        if action == 'restore':
            forms = Form.all_objects.filter(id__in=form_ids, is_deleted=True)
            count = 0
            for form in forms:
                form.restore()
                count += 1
            if count:
                messages.success(request, _('Restored %d form(s).') % count)

        elif action == 'permanent_delete':
            forms = Form.all_objects.filter(id__in=form_ids, is_deleted=True)
            count = 0
            errors = []
            for form in forms:
                try:
                    form.hard_delete()
                    count += 1
                except models.ProtectedError:
                    errors.append(form.name)
            if count:
                messages.success(
                    request,
                    _('Permanently deleted %d form(s).') % count
                )
            if errors:
                messages.error(
                    request,
                    _('Some forms could not be deleted: %s') % ', '.join(errors)
                )

        elif action == 'empty_bin':
            deleted_forms = Form.all_objects.filter(is_deleted=True)
            count = 0
            errors = []
            for form in deleted_forms:
                try:
                    form.hard_delete()
                    count += 1
                except models.ProtectedError:
                    errors.append(form.name)
            if count:
                messages.success(
                    request,
                    _('Recycle bin emptied (%d forms permanently deleted).') % count
                )
            if errors:
                messages.warning(
                    request,
                    _('%d forms with responses were skipped: %s')
                    % (len(errors), ', '.join(errors[:5]))
                )

    deleted_forms = Form.all_objects.filter(
        is_deleted=True
    ).select_related('deleted_by').order_by('-deleted_at')

    context = {
        'deleted_forms': deleted_forms,
        'title': _('Form Recycle Bin'),
        'has_permission': True,
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
        'opts': Form._meta,
    }

    return render(request, 'admin/form_builder/form/recycle_bin.html', context)
