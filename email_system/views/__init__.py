"""
Email System Views
"""
from email_system.views.oauth import (
    oauth_setup_form,
    oauth_initiate,
    oauth_callback,
    test_connection,
)
from email_system.views.provider_browse import (
    ProviderBrowseView,
    install_provider_ajax,
    update_provider_ajax,
)

__all__ = [
    # OAuth views
    'oauth_setup_form',
    'oauth_initiate',
    'oauth_callback',
    'test_connection',
    # Provider browse views
    'ProviderBrowseView',
    'install_provider_ajax',
    'update_provider_ajax',
]
