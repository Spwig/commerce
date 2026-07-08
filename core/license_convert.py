"""
License Conversion Utilities

Handles auto-conversion of expired trial licenses to dev (staging-only) licenses
by phoning home to the update server.
"""

import json
import logging
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)


def attempt_trial_to_dev_conversion():
    """
    Phone home to the update server to convert an expired trial to a dev license.

    On success:
    - Writes the new signed license.json to disk
    - Reloads the license manager
    - Installation continues in sandbox/development mode

    On failure:
    - Logs the error
    - Installation continues in sandbox mode anyway (trials never lock out)
    """
    import requests
    from core.license import get_license_manager, reload_license_manager

    license_manager = get_license_manager()
    license_data = license_manager.get_license_data()
    if not license_data:
        logger.warning("No license data found for trial-to-dev conversion")
        return False

    license_info = license_data.get('license', {})
    license_key = license_info.get('license_key', '')

    if not license_key:
        logger.warning("No license key found for trial-to-dev conversion")
        return False

    # Get installation UUID from UpdateServerConfig
    try:
        from component_updates.models import UpdateServerConfig
        config = UpdateServerConfig.get_instance()
        installation_uuid = str(config.installation_uuid)
        server_url = config.server_url.rstrip('/')
    except Exception as e:
        logger.error(f"Failed to get update server config: {e}")
        return False

    # Phone home to convert-to-dev endpoint
    url = f"{server_url}/api/v1/licenses/convert-to-dev/"
    payload = {
        'license_key': license_key,
        'installation_uuid': installation_uuid,
    }

    try:
        response = requests.post(url, json=payload, timeout=15)

        if response.status_code == 200:
            data = response.json()
            if data.get('converted'):
                # Write the new license file
                license_path = getattr(
                    settings,
                    'LICENSE_PATH',
                    '/opt/shop-platform/license/license.json'
                )

                new_license_file = {
                    'license': data['license'],
                    'signature': data['signature'],
                }

                license_path = Path(license_path)
                license_path.parent.mkdir(parents=True, exist_ok=True)

                with open(license_path, 'w') as f:
                    json.dump(new_license_file, f, indent=2)

                logger.info(
                    f"Trial license {license_key} successfully converted to dev. "
                    f"License file written to {license_path}"
                )

                # Reload the license manager with new data
                reload_license_manager()

                return True
            else:
                logger.warning(f"Trial-to-dev conversion returned unexpected response: {data}")
                return False

        elif response.status_code == 400:
            data = response.json()
            error = data.get('error', '')
            if error == 'not_a_trial':
                # License has already been converted or is no longer a trial
                logger.info("License is no longer a trial - may have already been converted or upgraded")
                return False
            logger.warning(f"Trial-to-dev conversion rejected: {data.get('message', '')}")
            return False

        else:
            logger.warning(
                f"Trial-to-dev conversion failed with status {response.status_code}: "
                f"{response.text[:200]}"
            )
            return False

    except requests.exceptions.ConnectionError:
        logger.info("Update server unreachable for trial-to-dev conversion - will retry later")
        return False
    except requests.exceptions.Timeout:
        logger.info("Update server timed out for trial-to-dev conversion - will retry later")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during trial-to-dev conversion: {e}")
        return False
