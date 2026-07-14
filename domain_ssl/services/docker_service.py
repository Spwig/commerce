"""
Docker Service for Domain & SSL

Manages Docker container operations: NGINX reload, certbot container runs,
and .env file updates. Follows the same Docker SDK pattern as
management/services/docker_log_service.py.
"""

import fcntl
import logging
import os
import re

logger = logging.getLogger(__name__)

# Container prefix from environment (matches docker-compose naming)
CONTAINER_PREFIX = os.environ.get("CONTAINER_PREFIX", "spwig")

# Domain validation for certbot arguments
_DOMAIN_RE = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*\.[A-Za-z]{2,}$")


def _get_docker_client():
    """Get a Docker client connected via the mounted socket."""
    import docker

    return docker.DockerClient(base_url="unix:///var/run/docker.sock")


def get_nginx_container():
    """Get the NGINX container by name."""
    client = _get_docker_client()
    name = f"{CONTAINER_PREFIX}_nginx"
    try:
        return client.containers.get(name)
    except Exception:
        logger.error("NGINX container %s not found", name)
        raise


def test_nginx_config():
    """Run nginx -t to validate configuration. Returns (success, output)."""
    container = get_nginx_container()
    result = container.exec_run("nginx -t")
    output = result.output.decode("utf-8", errors="replace")
    success = result.exit_code == 0
    if not success:
        logger.error("NGINX config test failed: %s", output)
    return success, output


def reload_nginx():
    """Reload NGINX configuration gracefully. Returns (success, output)."""
    # Always test first
    ok, test_output = test_nginx_config()
    if not ok:
        return False, f"Config test failed: {test_output}"

    container = get_nginx_container()
    result = container.exec_run("nginx -s reload")
    output = result.output.decode("utf-8", errors="replace")
    success = result.exit_code == 0
    if success:
        logger.info("NGINX reloaded successfully")
    else:
        logger.error("NGINX reload failed: %s", output)
    return success, output


def run_certbot(domain, email, webroot_path="/var/www/certbot", certs_path="/etc/letsencrypt"):
    """
    Run certbot as a one-off Docker container to obtain a certificate.

    Args:
        domain: Domain name for the certificate
        email: Contact email for Let's Encrypt
        webroot_path: Host path for ACME webroot challenge files
        certs_path: Host path for certificate storage

    Returns:
        (success, output) tuple
    """
    # Validate domain to prevent command injection
    if not _DOMAIN_RE.match(domain):
        return False, f"Invalid domain format: {domain}"

    client = _get_docker_client()

    # Build command as a list to prevent shell injection
    certbot_cmd = [
        "certonly",
        "--webroot",
        "-w",
        "/var/www/certbot",
        "-d",
        domain,
        "--email",
        email,
        "--agree-tos",
        "--non-interactive",
        "--preferred-challenges",
        "http-01",
    ]

    logger.info("Running certbot for %s", domain)

    try:
        output = client.containers.run(
            "certbot/certbot:latest",
            certbot_cmd,
            volumes={
                certs_path: {"bind": "/etc/letsencrypt", "mode": "rw"},
                webroot_path: {"bind": "/var/www/certbot", "mode": "rw"},
            },
            remove=True,
            network_mode="host",
        )
        output_str = output.decode("utf-8", errors="replace") if output else ""
        logger.info("Certbot completed successfully for %s", domain)
        return True, output_str
    except Exception as e:
        error_msg = str(e)
        logger.error("Certbot failed for %s: %s", domain, error_msg)
        return False, error_msg


def run_certbot_renew(certs_path="/etc/letsencrypt", webroot_path="/var/www/certbot"):
    """
    Run certbot renew for all certificates.

    Returns:
        (success, output) tuple
    """
    client = _get_docker_client()

    certbot_cmd = [
        "renew",
        "--webroot",
        "-w",
        "/var/www/certbot",
        "--non-interactive",
    ]

    try:
        output = client.containers.run(
            "certbot/certbot:latest",
            certbot_cmd,
            volumes={
                certs_path: {"bind": "/etc/letsencrypt", "mode": "rw"},
                webroot_path: {"bind": "/var/www/certbot", "mode": "rw"},
            },
            remove=True,
            network_mode="host",
        )
        output_str = output.decode("utf-8", errors="replace") if output else ""
        logger.info("Certbot renewal completed")
        return True, output_str
    except Exception as e:
        error_msg = str(e)
        logger.error("Certbot renewal failed: %s", error_msg)
        return False, error_msg


def update_env_file(key, value, env_path="/app/host_env"):
    """
    Update a key=value pair in the host .env file.
    The .env is bind-mounted at env_path.

    Uses file locking to prevent race conditions when multiple
    updates happen concurrently.
    """
    if not os.path.exists(env_path):
        logger.warning(".env file not found at %s", env_path)
        return False

    try:
        with open(env_path, "r+") as f:
            # Acquire exclusive lock
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                lines = f.readlines()

                # Update or append the key using exact boundary matching
                found = False
                new_lines = []
                for line in lines:
                    stripped = line.strip()
                    # Match KEY= exactly (not KEY_SUFFIX= or OTHERKEY=)
                    if stripped == f"{key}=" or stripped.startswith(f"{key}="):
                        # Verify it's an exact key match, not a prefix
                        eq_pos = stripped.index("=")
                        line_key = stripped[:eq_pos].rstrip()
                        if line_key == key:
                            new_lines.append(f"{key}={value}\n")
                            found = True
                            continue
                    new_lines.append(line)

                if not found:
                    new_lines.append(f"{key}={value}\n")

                # Rewrite the file
                f.seek(0)
                f.truncate()
                f.writelines(new_lines)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

        logger.info("Updated %s in .env", key)
        return True
    except Exception as e:
        logger.error("Failed to update %s in .env: %s", key, e)
        return False
