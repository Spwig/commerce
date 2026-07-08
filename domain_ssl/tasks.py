"""
Celery tasks for Domain & SSL configuration.

Tasks:
- configure_domain_task: Full domain+SSL pipeline (triggered by admin UI)
- check_certificate_renewal: Periodic check for certificates nearing expiry
"""

import logging

from celery import shared_task

from domain_ssl.models import DomainConfiguration

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=0, time_limit=600, soft_time_limit=540)
def configure_domain_task(self, domain, ssl_mode, email='',
                          cloudflare_token='', cloudflare_zone_id='',
                          custom_cert_pem='', custom_key_pem=''):
    """
    Full domain + SSL configuration pipeline.
    Triggered from the admin UI when the merchant saves domain settings.
    """
    from domain_ssl.services import domain_service

    config = DomainConfiguration.get_instance()
    config.task_id = self.request.id or ''
    config.save(update_fields=['task_id'])

    logger.info('Starting domain configuration: %s (SSL: %s)', domain, ssl_mode)

    success, message = domain_service.configure_domain(
        domain=domain,
        ssl_mode=ssl_mode,
        email=email,
        cloudflare_token=cloudflare_token,
        cloudflare_zone_id=cloudflare_zone_id,
        custom_cert_pem=custom_cert_pem,
        custom_key_pem=custom_key_pem,
    )

    # Clear task_id when done
    config.refresh_from_db()
    config.task_id = ''
    config.save(update_fields=['task_id'])

    if success:
        logger.info('Domain configuration completed: %s', domain)
    else:
        logger.error('Domain configuration failed: %s — %s', domain, message)

    return {'success': success, 'message': message}


@shared_task(bind=True, max_retries=1, time_limit=300)
def check_certificate_renewal(self):
    """
    Periodic task: check if certificate needs renewal (< 30 days).
    Runs every 12 hours via Celery Beat.
    """
    from domain_ssl.services import ssl_service, docker_service

    try:
        config = DomainConfiguration.objects.filter(pk=1).first()
    except Exception:
        return {'skipped': True, 'reason': 'No configuration found'}

    if not config or not config.auto_renew:
        return {'skipped': True, 'reason': 'Auto-renew disabled'}

    # Handle managed externally: verify upstream SSL is still valid
    if config.ssl_mode == DomainConfiguration.SSLMode.MANAGED_EXTERNALLY:
        if not config.domain:
            return {'skipped': True, 'reason': 'No domain configured'}

        logger.info('Verifying external SSL for %s', config.domain)
        valid, info = ssl_service.verify_external_ssl(config.domain)

        if valid:
            config.cert_domain = info.get('domain', config.cert_domain)
            config.cert_issuer = info.get('issuer', config.cert_issuer)
            config.cert_expires_at = info.get('expires_at')
            config.last_error = ''
            config.save()
            logger.info('External SSL verified for %s', config.domain)
            return {'success': True, 'message': 'External SSL verified'}
        else:
            error_msg = info.get('error', 'Unknown error')
            config.last_error = f'External SSL check failed: {error_msg}'
            config.save(update_fields=['last_error', 'updated_at'])
            logger.warning(
                'External SSL verification failed for %s: %s',
                config.domain, error_msg,
            )
            return {'success': False, 'message': error_msg}

    if config.ssl_mode not in (
        DomainConfiguration.SSLMode.LETSENCRYPT,
        DomainConfiguration.SSLMode.LETSENCRYPT_DNS,
    ):
        return {'skipped': True, 'reason': 'Not a Let\'s Encrypt certificate'}

    if not config.needs_renewal:
        days = config.cert_days_remaining
        return {
            'skipped': True,
            'reason': f'Certificate valid for {days} more days',
        }

    logger.info(
        'Certificate for %s expires in %d days — renewing',
        config.domain, config.cert_days_remaining or 0
    )

    config.set_status(DomainConfiguration.Status.OBTAINING_CERT)

    success, message = ssl_service.renew_certificates(domain=config.domain)

    if success:
        # Parse renewed cert metadata
        cert_info = ssl_service.parse_certificate()
        if cert_info:
            config.cert_expires_at = cert_info.get('expires_at')
            config.cert_issuer = cert_info.get('issuer', config.cert_issuer)
            config.save()

        config.set_status(DomainConfiguration.Status.IDLE)
        logger.info('Certificate renewed successfully for %s', config.domain)
    else:
        config.set_error(f'Renewal failed: {message}')
        logger.error('Certificate renewal failed for %s: %s', config.domain, message)

    return {'success': success, 'message': message}
