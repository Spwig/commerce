from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import BooleanField, Case, Count, Q, Value, When
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

from catalog.models import Warehouse
from .license import pos_license_is_valid, get_pos_license_status, activate_pos_license
from .models import (
    POSTerminal, POSShift, POSPayment, ReceiptTemplate, PromoSlide,
    POSTerminalProvider, POSTerminalReader,
)


@staff_member_required
def pos_dashboard(request):
    """POS Dashboard — shows status and quick actions if licensed, info page if not."""
    license_status = get_pos_license_status()

    if not license_status['valid']:
        return render(request, 'admin/pos_app/dashboard_upsell.html', {
            'title': 'Point of Sale',
            'license_status': license_status,
        })

    # --- Licensed: build dashboard context ---
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Terminal stats — annotate online status for template use
    online_cutoff = now - timedelta(seconds=300)
    terminals = list(
        POSTerminal.objects
        .filter(is_active=True)
        .prefetch_related('assigned_users')
        .order_by('name')
    )
    for t in terminals:
        t.is_online = bool(t.last_heartbeat and t.last_heartbeat >= online_cutoff)
    total_terminals = len(terminals)
    online_terminals = sum(1 for t in terminals if t.is_online)

    # Today's shift stats
    todays_shifts = POSShift.objects.filter(started_at__gte=today_start)
    open_shifts = todays_shifts.filter(ended_at__isnull=True).count()

    # Today's sales from payments
    todays_payments = POSPayment.objects.filter(created_at__gte=today_start)
    todays_sales = sum(float(p.amount) for p in todays_payments)
    todays_transactions = todays_payments.values('order').distinct().count()

    # Recent shifts (last 5 closed)
    recent_shifts = (
        POSShift.objects
        .filter(ended_at__isnull=False)
        .select_related('cashier', 'terminal')
        .order_by('-ended_at')[:5]
    )

    context = {
        'title': 'Point of Sale',
        'license_status': license_status,
        'total_terminals': total_terminals,
        'online_terminals': online_terminals,
        'open_shifts': open_shifts,
        'todays_sales': f'{todays_sales:.2f}',
        'todays_transactions': todays_transactions,
        'recent_shifts': recent_shifts,
        'all_terminals': terminals,
        'now': now,
    }

    return render(request, 'admin/pos_app/dashboard.html', context)


@staff_member_required
def filter_terminals(request):
    """AJAX endpoint for filtering POS terminals."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    search = request.GET.get('search', '')
    warehouse = request.GET.get('warehouse', '')
    status = request.GET.get('status', '')
    connection = request.GET.get('connection', '')

    online_cutoff = timezone.now() - timedelta(seconds=300)

    queryset = (
        POSTerminal.objects
        .select_related('warehouse')
        .prefetch_related('assigned_users')
        .annotate(
            shift_count=Count('shifts', distinct=True),
            staff_count=Count('assigned_users', distinct=True),
            is_online=Case(
                When(last_heartbeat__gte=online_cutoff, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .order_by('name')
    )

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(pairing_code__icontains=search)
        )
    if warehouse:
        queryset = queryset.filter(warehouse_id=warehouse)
    if status == 'active':
        queryset = queryset.filter(is_active=True)
    elif status == 'inactive':
        queryset = queryset.filter(is_active=False)
    if connection == 'online':
        queryset = queryset.filter(last_heartbeat__gte=online_cutoff)
    elif connection == 'offline':
        queryset = queryset.filter(
            Q(last_heartbeat__lt=online_cutoff) | Q(last_heartbeat__isnull=True)
        )

    html = render_to_string(
        'admin/pos_app/posterminal/partials/terminal_cards.html',
        {'terminals': queryset, 'request': request},
        request=request,
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count(),
    })


@staff_member_required
def filter_shifts(request):
    """AJAX endpoint for filtering POS shifts."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    search = request.GET.get('search', '')
    terminal = request.GET.get('terminal', '')
    shift_status = request.GET.get('shift_status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    queryset = (
        POSShift.objects
        .select_related('terminal', 'terminal__warehouse', 'cashier')
        .order_by('-started_at')
    )

    if search:
        queryset = queryset.filter(
            Q(cashier__first_name__icontains=search) |
            Q(cashier__last_name__icontains=search) |
            Q(cashier__username__icontains=search)
        )
    if terminal:
        queryset = queryset.filter(terminal_id=terminal)
    if shift_status == 'open':
        queryset = queryset.filter(ended_at__isnull=True)
    elif shift_status == 'closed':
        queryset = queryset.filter(ended_at__isnull=False)
    if date_from:
        queryset = queryset.filter(started_at__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(started_at__date__lte=date_to)

    html = render_to_string(
        'admin/pos_app/posshift/partials/shift_cards.html',
        {'shifts': queryset, 'request': request},
        request=request,
    )

    # Counts for tabs (apply search/terminal/date filters but not status)
    base_qs = (
        POSShift.objects
        .select_related('terminal', 'terminal__warehouse', 'cashier')
    )
    if search:
        base_qs = base_qs.filter(
            Q(cashier__first_name__icontains=search) |
            Q(cashier__last_name__icontains=search) |
            Q(cashier__username__icontains=search)
        )
    if terminal:
        base_qs = base_qs.filter(terminal_id=terminal)
    if date_from:
        base_qs = base_qs.filter(started_at__date__gte=date_from)
    if date_to:
        base_qs = base_qs.filter(started_at__date__lte=date_to)

    return JsonResponse({
        'html': html,
        'count': queryset.count(),
        'counts': {
            'all': base_qs.count(),
            'open': base_qs.filter(ended_at__isnull=True).count(),
            'closed': base_qs.filter(ended_at__isnull=False).count(),
        },
    })


@staff_member_required
def enable_store_location(request):
    """AJAX endpoint to mark a warehouse as a POS retail store location."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    warehouse_id = request.POST.get('warehouse_id')
    display_name = request.POST.get('pos_display_name', '').strip()

    if not warehouse_id:
        return JsonResponse({'error': 'Warehouse ID required'}, status=400)

    try:
        warehouse = Warehouse.objects.get(pk=warehouse_id, is_active=True)
    except Warehouse.DoesNotExist:
        return JsonResponse({'error': 'Warehouse not found'}, status=404)

    warehouse.is_retail_location = True
    if display_name:
        warehouse.pos_display_name = display_name
    warehouse.save(update_fields=['is_retail_location', 'pos_display_name'])

    return JsonResponse({
        'success': True,
        'warehouse_id': warehouse.pk,
        'name': warehouse.pos_display_name or warehouse.name,
    })


@staff_member_required
def filter_promo_slides(request):
    """AJAX endpoint for filtering POS promo slides."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    scope = request.GET.get('scope', '')
    status = request.GET.get('status', '')

    queryset = (
        PromoSlide.objects
        .select_related('warehouse', 'store_group', 'image')
        .order_by('sort_order', 'created_at')
    )

    # Parse scope: "group:123" or "store:456" or empty
    if scope:
        if scope.startswith('group:'):
            group_id = scope.split(':')[1]
            queryset = queryset.filter(store_group_id=group_id)
        elif scope.startswith('store:'):
            warehouse_id = scope.split(':')[1]
            queryset = queryset.filter(warehouse_id=warehouse_id)

    if status == 'active':
        queryset = queryset.filter(is_active=True)
    elif status == 'inactive':
        queryset = queryset.filter(is_active=False)

    html = render_to_string(
        'admin/pos_app/promoslide/partials/slide_cards.html',
        {'slides': queryset, 'request': request},
        request=request,
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count(),
    })


@staff_member_required
def filter_receipt_templates(request):
    """AJAX endpoint for filtering POS receipt templates."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    scope = request.GET.get('scope', '').strip()
    paper_width = request.GET.get('paper_width', '').strip()
    qr_enabled = request.GET.get('qr_enabled', '').strip()

    # Build queryset
    queryset = ReceiptTemplate.objects.select_related(
        'warehouse', 'store_group', 'logo'
    ).all()

    # Apply filters
    if search:
        queryset = queryset.filter(name__icontains=search)

    if scope == 'default':
        queryset = queryset.filter(warehouse__isnull=True, store_group__isnull=True)
    elif scope == 'store_group':
        queryset = queryset.filter(store_group__isnull=False)
    elif scope == 'warehouse':
        queryset = queryset.filter(warehouse__isnull=False)

    if paper_width:
        queryset = queryset.filter(paper_width=paper_width)

    if qr_enabled == 'true':
        queryset = queryset.filter(qr_enabled=True)
    elif qr_enabled == 'false':
        queryset = queryset.filter(qr_enabled=False)

    # Order by name
    queryset = queryset.order_by('name')

    html = render_to_string(
        'admin/pos_app/receipttemplate/partials/template_cards.html',
        {'templates': queryset, 'request': request},
        request=request,
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count(),
    })


@staff_member_required
def filter_terminal_providers(request):
    """AJAX endpoint for filtering POS terminal providers."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    status = request.GET.get('status', '')
    connection = request.GET.get('connection', '')

    queryset = (
        POSTerminalProvider.objects
        .annotate(reader_count=Count('readers', distinct=True))
        .order_by('display_name')
    )

    if status == 'active':
        queryset = queryset.filter(is_active=True)
    elif status == 'inactive':
        queryset = queryset.filter(is_active=False)

    if connection == 'connected':
        queryset = queryset.filter(connection_status='connected')
    elif connection == 'error':
        queryset = queryset.filter(connection_status='error')
    elif connection == 'not_tested':
        queryset = queryset.filter(connection_status='not_tested')

    html = render_to_string(
        'admin/pos_app/posterminalprovider/partials/provider_cards.html',
        {'providers': queryset, 'request': request},
        request=request,
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count(),
    })


@staff_member_required
def filter_terminal_readers(request):
    """AJAX endpoint for filtering POS terminal readers."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    search = request.GET.get('search', '')
    provider = request.GET.get('provider', '')
    status = request.GET.get('status', '')
    assigned = request.GET.get('assigned', '')

    queryset = (
        POSTerminalReader.objects
        .select_related('provider', 'terminal', 'terminal__warehouse')
        .order_by('reader_label', 'provider_reader_id')
    )

    if search:
        queryset = queryset.filter(
            Q(reader_label__icontains=search) |
            Q(serial_number__icontains=search) |
            Q(provider_reader_id__icontains=search)
        )
    if provider:
        queryset = queryset.filter(provider_id=provider)
    if status:
        queryset = queryset.filter(status=status)
    if assigned == 'assigned':
        queryset = queryset.filter(terminal__isnull=False)
    elif assigned == 'unassigned':
        queryset = queryset.filter(terminal__isnull=True)

    # Get terminals for quick assign dropdown
    terminals = POSTerminal.objects.filter(is_active=True).order_by('name')

    html = render_to_string(
        'admin/pos_app/posterminalreader/partials/reader_cards.html',
        {'readers': queryset, 'terminals': terminals, 'request': request},
        request=request,
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count(),
    })


@staff_member_required
def sync_readers(request):
    """AJAX endpoint to sync readers from all active terminal providers."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    synced = 0
    errors = []

    for provider in POSTerminalProvider.objects.filter(is_active=True):
        try:
            instance = provider.get_provider_instance()

            # Skip manual provider (no reader discovery)
            if provider.provider_key == 'manual':
                continue

            result = instance.list_readers()

            if result.get('success'):
                for r in result.get('readers', []):
                    reader, created = POSTerminalReader.objects.update_or_create(
                        provider=provider,
                        provider_reader_id=r['id'],
                        defaults={
                            'reader_label': r.get('label', ''),
                            'reader_type': r.get('type', ''),
                            'serial_number': r.get('serial_number', ''),
                            'ip_address': r.get('ip_address') or None,
                            'status': 'online' if r.get('status') == 'online' else 'offline',
                            'last_seen_at': timezone.now(),
                        }
                    )
                    synced += 1
            else:
                errors.append(f"{provider.display_name}: {result.get('message', 'Unknown error')}")

        except Exception as e:
            errors.append(f"{provider.display_name}: {str(e)}")

    return JsonResponse({
        'success': len(errors) == 0,
        'synced': synced,
        'errors': errors,
    })


@staff_member_required
def quick_assign_reader(request):
    """AJAX endpoint to quickly assign/unassign a reader to/from a terminal."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    reader_id = request.POST.get('reader_id')
    terminal_id = request.POST.get('terminal_id')  # Empty string = unassign

    if not reader_id:
        return JsonResponse({'error': 'Reader ID required'}, status=400)

    try:
        reader = POSTerminalReader.objects.get(id=reader_id)
    except POSTerminalReader.DoesNotExist:
        return JsonResponse({'error': 'Reader not found'}, status=404)

    if terminal_id:
        try:
            from .models import POSTerminal
            terminal = POSTerminal.objects.get(id=terminal_id)

            # Unassign any existing reader from this terminal
            POSTerminalReader.objects.filter(terminal=terminal).exclude(id=reader_id).update(terminal=None)

            # Assign this reader to the terminal
            reader.terminal = terminal
            reader.save(update_fields=['terminal'])

            return JsonResponse({
                'success': True,
                'reader_id': str(reader.id),
                'terminal_id': str(terminal.id),
                'terminal_name': terminal.name,
                'message': f'Reader assigned to {terminal.name}',
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Unassign
        old_terminal = reader.terminal
        reader.terminal = None
        reader.save(update_fields=['terminal'])

        return JsonResponse({
            'success': True,
            'reader_id': str(reader.id),
            'terminal_id': None,
            'message': 'Reader unassigned',
        })


@staff_member_required
def refresh_reader_status(request, reader_id):
    """AJAX endpoint to refresh status for a specific reader from provider."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        reader = POSTerminalReader.objects.select_related('provider').get(id=reader_id)
    except POSTerminalReader.DoesNotExist:
        return JsonResponse({'error': 'Reader not found'}, status=404)

    # Skip for manual provider
    if reader.provider.provider_key == 'manual':
        return JsonResponse({
            'success': True,
            'reader_id': str(reader.id),
            'status': 'online',
            'message': 'Manual readers are always online',
        })

    try:
        instance = reader.provider.get_provider_instance()
        result = instance.list_readers()

        if result.get('success'):
            # Find this specific reader in the list
            for r in result.get('readers', []):
                if r['id'] == reader.provider_reader_id:
                    reader.status = 'online' if r.get('status') == 'online' else 'offline'
                    reader.last_seen_at = timezone.now()
                    reader.save(update_fields=['status', 'last_seen_at'])

                    return JsonResponse({
                        'success': True,
                        'reader_id': str(reader.id),
                        'status': reader.status,
                        'last_seen': reader.last_seen_at.isoformat() if reader.last_seen_at else None,
                    })

            # Reader not found in provider list
            reader.status = 'offline'
            reader.save(update_fields=['status'])
            return JsonResponse({
                'success': True,
                'reader_id': str(reader.id),
                'status': 'offline',
                'message': 'Reader not found in provider account',
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result.get('message', 'Failed to fetch reader status'),
            })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
        }, status=500)


@staff_member_required
def unlock_terminal(request):
    """AJAX endpoint to remotely unlock a POS terminal."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

    terminal_id = request.POST.get('terminal_id')
    if not terminal_id:
        return JsonResponse({'success': False, 'error': 'Missing terminal_id'}, status=400)

    try:
        terminal = POSTerminal.objects.get(pk=terminal_id)
    except POSTerminal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Terminal not found'}, status=404)

    terminal.remote_unlock_at = timezone.now()
    terminal.save(update_fields=['remote_unlock_at'])

    return JsonResponse({
        'success': True,
        'message': f'Unlock signal sent to {terminal.name}',
    })


@staff_member_required
def activate_license(request):
    """AJAX endpoint to activate a POS license key."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    import json
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST

    license_key = data.get('license_key', '').strip().upper()
    if not license_key:
        return JsonResponse({'success': False, 'error': 'License key is required'}, status=400)

    result = activate_pos_license(license_key)
    status_code = 200 if result['success'] else 400
    return JsonResponse(result, status=status_code)
