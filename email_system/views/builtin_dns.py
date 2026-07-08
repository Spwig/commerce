"""
DNS Configuration View for Built-in SMTP Server

Reuses the DNSAssistant from Phase 9 to provide DNS validation
and configuration guidance for the built-in SMTP server.
"""
import socket
import logging
from typing import Optional
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.models import Site
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from email_system.models import EmailAccount
from email_system.services.dns_assistant import DNSAssistant
from email_system.smtp_server.dkim_handler import DKIMHandler
from email_system.utils.domain import extract_domain

logger = logging.getLogger(__name__)


def get_server_ip() -> Optional[str]:
    """
    Auto-detect the server's public IP address.

    Returns:
        Server IP address or None if detection fails
    """
    try:
        # Try to get hostname
        hostname = socket.gethostname()

        # Get IP address for hostname
        ip_address = socket.gethostbyname(hostname)

        # If it's localhost, try another method
        if ip_address.startswith('127.'):
            # Connect to external server to get public IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()

        return ip_address

    except Exception as e:
        logger.error(f"Failed to detect server IP: {e}")
        return None


def generate_spf_record(domain: str, server_ip: Optional[str] = None) -> str:
    """
    Generate recommended SPF record for the domain.

    Args:
        domain: Domain name
        server_ip: Server IP address (optional)

    Returns:
        SPF record value
    """
    if server_ip:
        return f"v=spf1 ip4:{server_ip} ~all"
    else:
        return "v=spf1 a mx ~all"


def generate_dmarc_record(domain: str, policy: str = 'quarantine') -> str:
    """
    Generate recommended DMARC record.

    Args:
        domain: Domain name
        policy: DMARC policy (none, quarantine, reject)

    Returns:
        DMARC record value
    """
    # Get site for admin email
    site = Site.objects.get_current()
    admin_email = f"postmaster@{domain}"

    return f"v=DMARC1; p={policy}; rua=mailto:{admin_email}; ruf=mailto:{admin_email}; fo=1"


@staff_member_required
@require_http_methods(["GET", "POST"])
def builtin_smtp_dns_config(request, account_id: Optional[int] = None):
    """
    DNS configuration view for built-in SMTP server.

    Shows DNS requirements and validates configuration using DNSAssistant.
    """
    # Get EmailAccount if specified
    account = None
    if account_id:
        account = get_object_or_404(EmailAccount, pk=account_id)
    else:
        # Get default built-in account
        account = EmailAccount.objects.filter(
            component__component_type='email_provider',
            component__key='builtin_smtp'
        ).first()

    # Extract domain from account or site
    if account and account.from_email:
        domain = extract_domain(account.from_email)
    else:
        site = Site.objects.get_current()
        domain = site.domain

    # Handle domain override from form
    if request.method == 'POST':
        domain_override = request.POST.get('domain', '').strip()
        if domain_override:
            domain = domain_override

    # Get server IP
    server_ip = get_server_ip()

    # Get DKIM selector from account or use default
    dkim_selector = 'mail'
    if account:
        credentials = account.get_credentials() or {}
        dkim_selector = credentials.get('dkim_selector', 'mail')

    # Initialize DKIM handler
    dkim_handler = DKIMHandler(domain=domain, selector=dkim_selector)

    # Get DKIM public key and DNS record
    dkim_public_key = dkim_handler.get_public_key(account)
    dkim_dns_record = dkim_handler.get_dns_record(account)
    dkim_dns_hostname = f"{dkim_selector}._domainkey.{domain}"

    # Generate recommended SPF and DMARC records
    spf_recommendation = generate_spf_record(domain, server_ip)
    dmarc_recommendation = generate_dmarc_record(domain)

    # Initialize DNSAssistant with full selector
    dns_assistant = DNSAssistant(domain=domain, dkim_selector=dkim_selector)

    # Perform DNS validation
    dns_results = dns_assistant.check_all()

    # Check if email domain differs from site domain
    site = Site.objects.get_current()
    email_domain_differs = (domain != site.domain)

    # Prepare context
    context = {
        'account': account,
        'domain': domain,
        'server_ip': server_ip,
        'dkim_selector': dkim_selector,
        'dkim_public_key': dkim_public_key,
        'dkim_dns_record': dkim_dns_record,
        'dkim_dns_hostname': dkim_dns_hostname,
        'spf_recommendation': spf_recommendation,
        'dmarc_recommendation': dmarc_recommendation,
        'dns_results': dns_results,
        'email_domain_differs': email_domain_differs,
        'site_domain': site.domain,

        # DNS record hostnames for clarity
        'spf_hostname': domain,
        'dmarc_hostname': f"_dmarc.{domain}",

        # Status flags
        'dkim_keys_exist': dkim_public_key is not None,
        'dns_validated': dns_results['overall']['status'] == 'pass',
    }

    # Render the dns_requirements.html template directly
    # This matches the pattern used by external providers
    import os
    from django.template import Template, Context
    from django.conf import settings

    # Load the built-in provider's dns_requirements.html
    template_path = os.path.join(
        settings.BASE_DIR,
        'email_system',
        'providers',
        'builtin',
        'dns_requirements.html'
    )

    with open(template_path, 'r') as f:
        template_content = f.read()

    template = Template(template_content)
    rendered_html = template.render(Context(context))

    from django.http import HttpResponse
    return HttpResponse(rendered_html)


@staff_member_required
@require_http_methods(["POST"])
def validate_dns_ajax(request):
    """
    AJAX endpoint for live DNS validation.

    Returns JSON with validation results.
    """
    domain = request.POST.get('domain', '').strip()
    dkim_selector = request.POST.get('dkim_selector', 'mail').strip()

    if not domain:
        return JsonResponse({
            'success': False,
            'error': _('Domain is required')
        }, status=400)

    try:
        # Run DNS validation
        dns_assistant = DNSAssistant(domain=domain, dkim_selector=dkim_selector)
        results = dns_assistant.check_all()

        return JsonResponse({
            'success': True,
            'results': results
        })

    except Exception as e:
        logger.error(f"DNS validation failed: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
