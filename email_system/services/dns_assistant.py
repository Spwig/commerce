"""
DNS Assistant Service

Validates email DNS records (SPF, DKIM, DMARC) across multiple DNS resolvers
to detect propagation status and ensure optimal email deliverability.
"""

import logging
from datetime import datetime

import dns.exception
import dns.resolver
from django.core.cache import cache
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class DNSAssistant:
    """
    DNS validation service for email deliverability.

    Checks SPF, DKIM, and DMARC records across multiple DNS resolvers
    to validate configuration and detect propagation status.
    """

    # Public DNS resolvers for propagation checking
    DNS_RESOLVERS = [
        "8.8.8.8",  # Google Public DNS
        "1.1.1.1",  # Cloudflare DNS
        "9.9.9.9",  # Quad9 DNS
    ]

    # Cache TTL (5 minutes)
    CACHE_TTL = 300

    def __init__(
        self,
        domain: str,
        dkim_selector: str | None = None,
        server_ip: str | None = None,
        mx_hostname: str | None = None,
        spf_include: str | None = None,
    ):
        """
        Initialize DNS Assistant for a domain.

        Args:
            domain: Domain to validate (e.g., 'example.com')
            dkim_selector: DKIM selector for validation (e.g., 'mail', 'google', 'selector1')
            server_ip: Server's external IP address for MX validation (optional)
            mx_hostname: Hostname for MX record recommendations (e.g., 'shop.example.com') - defaults to domain
            spf_include: Expected SPF include for external providers (e.g., 'spf.protection.outlook.com').
                         If provided, SPF validation checks for this include instead of mx/a mechanisms.
        """
        self.domain = domain.lower().strip()
        self.dkim_selector = dkim_selector
        self.server_ip = server_ip
        self.mx_hostname = mx_hostname if mx_hostname else self.domain
        # Normalize spf_include - strip 'include:' prefix if present
        if spf_include and spf_include.startswith("include:"):
            spf_include = spf_include[len("include:") :]
        self.spf_include = spf_include
        self.results = {
            "domain": self.domain,
            "checked_at": datetime.now(),
            "mx": {},
            "spf": {},
            "dkim": {},
            "dmarc": {},
            "propagation": {},
            "overall": {},
        }

    def check_all(self) -> dict:
        """
        Run all DNS checks (SPF, DKIM, DMARC, MX) and return results.

        Returns:
            Dictionary containing all validation results
        """
        logger.info(f"Starting DNS validation for domain: {self.domain}")

        # Check MX records
        self.results["mx"] = self.check_mx()

        # Check SPF
        self.results["spf"] = self.check_spf()

        # Check DKIM (if selector provided)
        if self.dkim_selector:
            self.results["dkim"] = self.check_dkim()
        else:
            self.results["dkim"] = {
                "status": "warn",
                "record": "",
                "errors": _("DKIM selector not provided"),
                "message": _("DKIM validation skipped - no selector available"),
            }

        # Check DMARC
        self.results["dmarc"] = self.check_dmarc()

        # Calculate overall status
        self.results["overall"] = self._calculate_overall_status()

        logger.info(f"DNS validation complete. Overall status: {self.results['overall']['status']}")

        return self.results

    def check_mx(self) -> dict:
        """
        Check MX records for the domain.

        Returns:
            Dictionary with status, records, and recommendations
        """
        cache_key = f"dns_mx_{self.domain}"
        cached = cache.get(cache_key)
        if cached:
            logger.debug(f"MX cache hit for {self.domain}")
            return cached

        logger.info(f"Checking MX records for {self.domain}")

        result = {
            "status": "warn",
            "records": [],
            "has_self_hosted": False,
            "errors": "",
            "message": "",
        }

        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            resolver.lifetime = 5

            # Query MX records
            answers = resolver.resolve(self.domain, "MX")

            mx_records = []
            for rdata in answers:
                mx_host = str(rdata.exchange).rstrip(".")
                mx_records.append({"priority": rdata.preference, "host": mx_host})

            result["records"] = sorted(mx_records, key=lambda x: x["priority"])

            if mx_records:
                result["status"] = "pass"
                result["message"] = _("MX records found")

                # Check if any MX points to self (domain's A record)
                # This would indicate self-hosted email
                for mx in mx_records:
                    if self.domain in mx["host"]:
                        result["has_self_hosted"] = True
                        break

                # Enhanced validation: Check if MX points to our server IP
                if self.server_ip:
                    mx_points_to_server = False
                    warnings = []

                    for mx in mx_records:
                        try:
                            # Resolve MX hostname to IP addresses
                            mx_answers = resolver.resolve(mx["host"], "A")
                            mx_ips = [str(ip) for ip in mx_answers]

                            # Check if our server IP is in the list
                            if self.server_ip in mx_ips:
                                mx_points_to_server = True
                                result["message"] = _(
                                    f"MX record correctly points to this server ({mx['host']})"
                                )
                                break
                            else:
                                warnings.append(
                                    _(
                                        f"MX {mx['host']} points to {mx_ips[0]}, not this server ({self.server_ip})"
                                    )
                                )
                        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                            warnings.append(_(f"Could not resolve MX hostname {mx['host']}"))
                        except Exception as e:
                            logger.debug(f"Error resolving MX {mx['host']}: {e}")

                    # If no MX points to our server, show warning with recommendation
                    if not mx_points_to_server and warnings:
                        result["status"] = "warn"
                        result["message"] = _(
                            "MX record should point to this server for built-in SMTP to work"
                        )
                        result["errors"] = " | ".join(warnings)
                        result["recommendation"] = {
                            "type": "MX",
                            "name": "@",
                            "priority": "10",
                            "value": self.mx_hostname,
                            "note": _("Points to your server at {ip}").format(ip=self.server_ip),
                        }
            else:
                result["status"] = "warn"
                result["message"] = _("No MX records found - email delivery may fail")

        except dns.resolver.NXDOMAIN:
            result["status"] = "fail"
            result["errors"] = _("Domain does not exist")
            result["message"] = _("Cannot configure email for non-existent domain")

        except dns.resolver.NoAnswer:
            result["status"] = "warn"
            result["errors"] = _("No MX records configured")
            result["message"] = _("No MX records found. Add MX record pointing to your server.")
            if self.server_ip:
                result["recommendation"] = {
                    "type": "MX",
                    "name": "@",
                    "priority": "10",
                    "value": self.mx_hostname,
                    "note": _("Points to your server at {ip}").format(ip=self.server_ip),
                }

        except dns.exception.DNSException as e:
            logger.warning(f"MX check failed: {str(e)}")
            result["status"] = "error"
            result["errors"] = str(e)
            result["message"] = _("Error checking MX records")

        except Exception as e:
            logger.error(f"MX validation error for {self.domain}: {str(e)}")
            result["status"] = "error"
            result["errors"] = str(e)
            result["message"] = _("Error checking MX records")

        # Cache result
        cache.set(cache_key, result, self.CACHE_TTL)

        return result

    def check_spf(self) -> dict:
        """
        Validate SPF record for the domain.

        Returns:
            Dictionary with status, record, errors, propagation info
        """
        cache_key = f"dns_spf_{self.domain}"
        cached = cache.get(cache_key)
        if cached:
            logger.debug(f"SPF cache hit for {self.domain}")
            return cached

        logger.info(f"Checking SPF for {self.domain}")

        result = {"status": "fail", "record": "", "errors": "", "message": "", "resolvers": {}}

        try:
            # Check SPF across multiple resolvers
            records_by_resolver = {}

            for resolver_ip in self.DNS_RESOLVERS:
                try:
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = [resolver_ip]
                    resolver.timeout = 5
                    resolver.lifetime = 5

                    # Query TXT records
                    answers = resolver.resolve(self.domain, "TXT")

                    # Find SPF record (starts with "v=spf1")
                    spf_record = None
                    for rdata in answers:
                        txt_data = b"".join(rdata.strings).decode("utf-8")
                        if txt_data.startswith("v=spf1"):
                            spf_record = txt_data
                            break

                    if spf_record:
                        records_by_resolver[resolver_ip] = {
                            "status": "success",
                            "record": spf_record,
                        }
                    else:
                        records_by_resolver[resolver_ip] = {"status": "not_found", "record": ""}

                except dns.exception.DNSException as e:
                    logger.warning(f"SPF check failed on {resolver_ip}: {str(e)}")
                    records_by_resolver[resolver_ip] = {"status": "error", "error": str(e)}

            result["resolvers"] = records_by_resolver

            # Analyze propagation
            propagation = self._analyze_propagation(records_by_resolver)
            result["propagation_status"] = propagation["status"]

            if propagation["status"] == "full":
                # All resolvers have SPF record
                result["status"] = "pass"
                result["record"] = propagation["record"]
                result["message"] = _("SPF record found and fully propagated")

                # Validate SPF record syntax and content
                validation = self._validate_spf_syntax(result["record"])
                if not validation["valid"] or validation.get("has_warnings", False):
                    result["status"] = "warn"
                    result["errors"] = validation["errors"]
                    if validation.get("has_warnings", False):
                        if self.spf_include:
                            result["message"] = _(
                                "SPF record should include your email provider's servers"
                            )
                        else:
                            result["message"] = _(
                                "Update required: SPF record must be updated to include built-in SMTP server"
                            )
                    else:
                        result["message"] = _("SPF record found but has warnings")

            elif propagation["status"] == "partial":
                result["status"] = "warn"
                result["record"] = propagation["record"] if propagation["record"] else ""
                result["errors"] = _("SPF record partially propagated")
                result["message"] = _("SPF record found on some DNS servers but not all")

            else:
                result["status"] = "fail"
                result["errors"] = _("No SPF record found")
                result["message"] = _("SPF record not found on any DNS server")

        except Exception as e:
            logger.error(f"SPF validation error for {self.domain}: {str(e)}")
            result["status"] = "error"
            result["errors"] = str(e)
            result["message"] = _("Error checking SPF record")

        # Cache result
        cache.set(cache_key, result, self.CACHE_TTL)

        return result

    def check_dkim(self) -> dict:
        """
        Validate DKIM record for the domain.

        Returns:
            Dictionary with status, record, errors, propagation info
        """
        if not self.dkim_selector:
            return {
                "status": "error",
                "record": "",
                "errors": _("DKIM selector not provided"),
                "message": _("Cannot validate DKIM without selector"),
            }

        # Construct DKIM DNS hostname
        # Normalize: ensure ._domainkey is in the hostname
        if "._domainkey" in self.dkim_selector:
            dkim_hostname = f"{self.dkim_selector}.{self.domain}"
        else:
            dkim_hostname = f"{self.dkim_selector}._domainkey.{self.domain}"
        cache_key = f"dns_dkim_{dkim_hostname}"
        cached = cache.get(cache_key)
        if cached:
            logger.debug(f"DKIM cache hit for {dkim_hostname}")
            return cached

        logger.info(f"Checking DKIM for {dkim_hostname}")

        result = {
            "status": "fail",
            "record": "",
            "errors": "",
            "message": "",
            "selector": self.dkim_selector,
            "hostname": dkim_hostname,
            "resolvers": {},
        }

        try:
            records_by_resolver = {}

            for resolver_ip in self.DNS_RESOLVERS:
                try:
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = [resolver_ip]
                    resolver.timeout = 5
                    resolver.lifetime = 5

                    # Query TXT records for DKIM
                    answers = resolver.resolve(dkim_hostname, "TXT")

                    # DKIM record should contain v=DKIM1
                    dkim_record = None
                    for rdata in answers:
                        txt_data = b"".join(rdata.strings).decode("utf-8")
                        if "v=DKIM1" in txt_data or "k=rsa" in txt_data or "p=" in txt_data:
                            dkim_record = txt_data
                            break

                    if dkim_record:
                        records_by_resolver[resolver_ip] = {
                            "status": "success",
                            "record": dkim_record,
                        }
                    else:
                        records_by_resolver[resolver_ip] = {"status": "not_found", "record": ""}

                except dns.resolver.NXDOMAIN:
                    records_by_resolver[resolver_ip] = {"status": "not_found", "record": ""}
                except dns.exception.DNSException as e:
                    logger.warning(f"DKIM check failed on {resolver_ip}: {str(e)}")
                    records_by_resolver[resolver_ip] = {"status": "error", "error": str(e)}

            result["resolvers"] = records_by_resolver

            # Analyze propagation
            propagation = self._analyze_propagation(records_by_resolver)
            result["propagation_status"] = propagation["status"]

            if propagation["status"] == "full":
                result["status"] = "pass"
                result["record"] = propagation["record"]
                result["message"] = _("DKIM record found and fully propagated")

                # Validate DKIM record
                validation = self._validate_dkim_syntax(result["record"])
                if not validation["valid"]:
                    result["status"] = "warn"
                    result["errors"] = validation["errors"]
                    result["message"] = _("DKIM record found but has warnings")

            elif propagation["status"] == "partial":
                result["status"] = "warn"
                result["record"] = propagation["record"] if propagation["record"] else ""
                result["errors"] = _("DKIM record partially propagated")
                result["message"] = _("DKIM record found on some DNS servers but not all")

            else:
                result["status"] = "fail"
                result["errors"] = _("No DKIM record found")
                result["message"] = _(
                    "DKIM record not found. Please configure DKIM in your email provider."
                )

        except Exception as e:
            logger.error(f"DKIM validation error for {dkim_hostname}: {str(e)}")
            result["status"] = "error"
            result["errors"] = str(e)
            result["message"] = _("Error checking DKIM record")

        # Cache result
        cache.set(cache_key, result, self.CACHE_TTL)

        return result

    def check_dmarc(self) -> dict:
        """
        Validate DMARC record for the domain.

        Returns:
            Dictionary with status, record, errors, propagation info
        """
        dmarc_hostname = f"_dmarc.{self.domain}"
        cache_key = f"dns_dmarc_{dmarc_hostname}"
        cached = cache.get(cache_key)
        if cached:
            logger.debug(f"DMARC cache hit for {dmarc_hostname}")
            return cached

        logger.info(f"Checking DMARC for {dmarc_hostname}")

        result = {
            "status": "fail",
            "record": "",
            "errors": "",
            "message": "",
            "hostname": dmarc_hostname,
            "resolvers": {},
        }

        try:
            records_by_resolver = {}

            for resolver_ip in self.DNS_RESOLVERS:
                try:
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = [resolver_ip]
                    resolver.timeout = 5
                    resolver.lifetime = 5

                    # Query TXT records for DMARC
                    answers = resolver.resolve(dmarc_hostname, "TXT")

                    # DMARC record should start with v=DMARC1
                    dmarc_record = None
                    for rdata in answers:
                        txt_data = b"".join(rdata.strings).decode("utf-8")
                        if txt_data.startswith("v=DMARC1"):
                            dmarc_record = txt_data
                            break

                    if dmarc_record:
                        records_by_resolver[resolver_ip] = {
                            "status": "success",
                            "record": dmarc_record,
                        }
                    else:
                        records_by_resolver[resolver_ip] = {"status": "not_found", "record": ""}

                except dns.resolver.NXDOMAIN:
                    records_by_resolver[resolver_ip] = {"status": "not_found", "record": ""}
                except dns.exception.DNSException as e:
                    logger.warning(f"DMARC check failed on {resolver_ip}: {str(e)}")
                    records_by_resolver[resolver_ip] = {"status": "error", "error": str(e)}

            result["resolvers"] = records_by_resolver

            # Analyze propagation
            propagation = self._analyze_propagation(records_by_resolver)
            result["propagation_status"] = propagation["status"]

            if propagation["status"] == "full":
                result["status"] = "pass"
                result["record"] = propagation["record"]
                result["message"] = _("DMARC record found and fully propagated")

                # Validate DMARC record syntax and alignment settings
                validation = self._validate_dmarc_syntax(result["record"])
                if not validation["valid"]:
                    result["status"] = "warn"
                    result["errors"] = validation["errors"]
                    result["message"] = _("DMARC record found but has issues")
                elif validation.get("has_warnings", False):
                    result["status"] = "warn"
                    result["errors"] = validation["errors"]
                    result["message"] = _(
                        "Update required: DMARC record needs relaxed alignment for multi-provider compatibility"
                    )
                elif validation.get("has_info", False):
                    # Info-only items don't change status - record is valid
                    result["info"] = validation.get("info", "")

            elif propagation["status"] == "partial":
                result["status"] = "warn"
                result["record"] = propagation["record"] if propagation["record"] else ""
                result["errors"] = _("DMARC record partially propagated")
                result["message"] = _("DMARC record found on some DNS servers but not all")

            else:
                result["status"] = "warn"  # DMARC is recommended but not required
                result["errors"] = _("No DMARC record found")
                result["message"] = _(
                    "DMARC record not found. Recommended for email authentication."
                )

        except Exception as e:
            logger.error(f"DMARC validation error for {dmarc_hostname}: {str(e)}")
            result["status"] = "error"
            result["errors"] = str(e)
            result["message"] = _("Error checking DMARC record")

        # Cache result
        cache.set(cache_key, result, self.CACHE_TTL)

        return result

    def _analyze_propagation(self, records_by_resolver: dict) -> dict:
        """
        Analyze DNS propagation across resolvers.

        Majority consensus: If 2/3 resolvers agree, consider it propagated.

        Args:
            records_by_resolver: Dict mapping resolver IP to result

        Returns:
            Dict with status ('full'/'partial'/'none') and consensus record
        """
        successful_records = []
        error_count = 0
        not_found_count = 0

        for _resolver_ip, data in records_by_resolver.items():
            if data["status"] == "success":
                successful_records.append(data["record"])
            elif data["status"] == "not_found":
                not_found_count += 1
            else:
                error_count += 1

        total_resolvers = len(records_by_resolver)
        success_count = len(successful_records)

        # Check for consensus (2 out of 3 = majority)
        majority_threshold = (total_resolvers + 1) // 2  # Ceiling division

        if success_count >= majority_threshold:
            # Majority have the record
            # Find most common record value
            from collections import Counter

            if successful_records:
                most_common = Counter(successful_records).most_common(1)[0][0]
                if success_count == total_resolvers:
                    return {"status": "full", "record": most_common}
                else:
                    return {"status": "partial", "record": most_common}

        # No consensus or minority have record
        if success_count > 0:
            return {
                "status": "partial",
                "record": successful_records[0] if successful_records else "",
            }
        else:
            return {"status": "none", "record": ""}

    def _validate_spf_syntax(self, spf_record: str) -> dict:
        """
        Validate SPF record syntax and check for provider-specific authorization.

        When spf_include is set (external provider), checks for the include: mechanism.
        When spf_include is not set (built-in SMTP), checks for mx/a mechanisms.

        Args:
            spf_record: SPF record string

        Returns:
            Dict with 'valid' (bool), 'has_warnings' (bool), and 'errors' (str)
        """
        errors = []
        warnings = []

        if not spf_record.startswith("v=spf1"):
            errors.append(_('SPF record must start with "v=spf1"'))

        # Parse SPF tokens for mechanism analysis
        tokens = spf_record.split()
        mechanisms = set()
        lookup_count = 0
        lookup_mechanisms = {"include", "a", "mx", "ptr", "exists", "redirect"}

        for token in tokens:
            if token.startswith("v="):
                continue
            # Strip qualifier prefix (+, -, ~, ?)
            bare = token.lstrip("+-~?")
            # Get mechanism name (before : or / or =)
            for sep in (":", "/", "="):
                if sep in bare:
                    mech_name = bare.split(sep)[0]
                    break
            else:
                mech_name = bare
            mechanisms.add(mech_name.lower())
            # Count DNS lookups
            if mech_name.lower() in lookup_mechanisms:
                lookup_count += 1

        # Check for common issues
        if "+all" in spf_record or "?all" in spf_record:
            errors.append(_('SPF record should end with "~all" or "-all" for better security'))

        # Check DNS lookup limit (max 10 lookups per RFC 7208)
        if lookup_count > 10:
            warnings.append(
                _("SPF record has %(count)d DNS lookups (max 10 allowed)") % {"count": lookup_count}
            )

        # Provider-specific validation
        if self.spf_include:
            # External provider: check for the required include: mechanism
            if f"include:{self.spf_include}" not in spf_record:
                warnings.append(
                    _('SPF record should include "include:%(include)s" for your email provider')
                    % {"include": self.spf_include}
                )
        else:
            # Built-in SMTP: check for mx and/or a mechanisms
            has_mx = "mx" in mechanisms
            has_a = "a" in mechanisms
            if not has_mx and not has_a:
                warnings.append(
                    _(
                        'SPF record does not include "mx" or "a" mechanisms required for built-in SMTP server'
                    )
                )

        # Combine errors and warnings
        all_issues = errors + warnings

        return {
            "valid": len(errors) == 0,
            "has_warnings": len(warnings) > 0,
            "errors": " | ".join(all_issues) if all_issues else "",
        }

    def _validate_dkim_syntax(self, dkim_record: str) -> dict:
        """
        Validate DKIM record syntax.

        Args:
            dkim_record: DKIM record string

        Returns:
            Dict with 'valid' (bool) and 'errors' (str)
        """
        errors = []

        # Check for required fields
        if "p=" not in dkim_record:
            errors.append(_("DKIM record must contain public key (p=)"))

        # Check for empty public key (revoked)
        if "p=;" in dkim_record or "p= ;" in dkim_record:
            errors.append(_("DKIM public key is empty (revoked)"))

        # Recommended fields
        if "v=DKIM1" not in dkim_record:
            errors.append(_("DKIM record should specify version (v=DKIM1)"))

        return {"valid": len(errors) == 0, "errors": " | ".join(errors) if errors else ""}

    def _validate_dmarc_syntax(self, dmarc_record: str) -> dict:
        """
        Validate DMARC record syntax and alignment settings for multi-provider compatibility.

        Separates issues into three categories:
        - errors: Invalid record (missing version/policy)
        - warnings: Issues affecting deliverability (strict alignment, missing rua)
        - info: Optional best practices (missing ruf, fo, p=none)

        Args:
            dmarc_record: DMARC record string

        Returns:
            Dict with 'valid', 'has_warnings', 'has_info', 'errors', 'info'
        """
        errors = []
        warnings = []
        info = []

        if not dmarc_record.startswith("v=DMARC1"):
            errors.append(_('DMARC record must start with "v=DMARC1"'))

        # Check for required policy
        if "p=" not in dmarc_record:
            errors.append(_("DMARC record must have a policy (p=none/quarantine/reject)"))

        # Check for reporting address (important for monitoring)
        if "rua=" not in dmarc_record:
            warnings.append(_("DMARC record should include aggregate report address (rua=)"))

        # Check policy strictness (informational)
        if "p=none" in dmarc_record:
            info.append(
                _(
                    'DMARC policy is set to "none" - consider using "quarantine" or "reject" for better security'
                )
            )

        # Check alignment modes for multi-provider compatibility
        has_aspf = "aspf=" in dmarc_record
        has_adkim = "adkim=" in dmarc_record
        has_strict_spf = "aspf=s" in dmarc_record
        has_strict_dkim = "adkim=s" in dmarc_record

        # Strict alignment is a real deliverability problem
        if has_strict_spf:
            warnings.append(
                _(
                    "DMARC has strict SPF alignment (aspf=s) - this may break multi-provider email. Use aspf=r for relaxed alignment"
                )
            )
        elif not has_aspf:
            info.append(
                _(
                    "DMARC missing SPF alignment setting (aspf) - defaults to relaxed, but aspf=r recommended for clarity"
                )
            )

        if has_strict_dkim:
            warnings.append(
                _(
                    "DMARC has strict DKIM alignment (adkim=s) - this may break multi-provider email. Use adkim=r for relaxed alignment"
                )
            )
        elif not has_adkim:
            info.append(
                _(
                    "DMARC missing DKIM alignment setting (adkim) - defaults to relaxed, but adkim=r recommended for clarity"
                )
            )

        # Failure reporting settings are optional best practices
        if "ruf=" not in dmarc_record:
            info.append(
                _("Consider adding failure report address (ruf=mailto:postmaster@%(domain)s)")
                % {"domain": self.domain}
            )

        if "fo=" not in dmarc_record:
            info.append(_("Consider adding failure reporting options (fo=1) for detailed reports"))

        # Combine errors and warnings (not info) for backward compatibility
        all_issues = errors + warnings

        return {
            "valid": len(errors) == 0,
            "has_warnings": len(warnings) > 0,
            "has_info": len(info) > 0,
            "errors": " | ".join(all_issues) if all_issues else "",
            "info": " | ".join(info) if info else "",
        }

    def _calculate_overall_status(self) -> dict:
        """
        Calculate overall DNS validation status based on individual checks.

        Returns:
            Dict with overall status and message
        """
        spf_status = self.results["spf"].get("status", "error")
        dkim_status = self.results["dkim"].get("status", "error")
        dmarc_status = self.results["dmarc"].get("status", "error")

        # Check if any critical records failed
        if spf_status == "fail" or dkim_status == "fail":
            return {"status": "fail", "message": _("Required DNS records missing or invalid")}

        # SPF and DKIM must pass for overall pass
        if spf_status == "pass" and dkim_status == "pass":
            if dmarc_status == "pass":
                return {"status": "pass", "message": _("All DNS records configured correctly")}
            elif dmarc_status == "warn" and not self.results["dmarc"].get("errors"):
                # DMARC has info-only items (no actual errors/warnings) - still pass
                return {"status": "pass", "message": _("All DNS records configured correctly")}
            elif dmarc_status == "warn":
                return {
                    "status": "warn",
                    "message": _("SPF and DKIM configured, DMARC needs attention"),
                }
            else:
                return {
                    "status": "warn",
                    "message": _("SPF and DKIM configured, DMARC recommended"),
                }

        return {"status": "warn", "message": _("Some DNS records have warnings")}

    def get_existing_spf_record(self) -> str | None:
        """
        Fetch the existing SPF record from DNS.

        Returns:
            Existing SPF record string or None if not found
        """
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            resolver.lifetime = 5

            # Query TXT records
            answers = resolver.resolve(self.domain, "TXT")

            # Find SPF record (starts with "v=spf1")
            for rdata in answers:
                txt_data = b"".join(rdata.strings).decode("utf-8")
                if txt_data.startswith("v=spf1"):
                    logger.info(f"Found existing SPF record for {self.domain}: {txt_data}")
                    return txt_data

            logger.info(f"No existing SPF record found for {self.domain}")
            return None

        except dns.resolver.NXDOMAIN:
            logger.info(f"Domain {self.domain} does not exist")
            return None
        except dns.exception.DNSException as e:
            logger.warning(f"Error fetching SPF record for {self.domain}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching SPF record: {e}")
            return None

    def merge_spf_record(self, existing_spf: str | None = None) -> str:
        """
        Merge existing SPF record with built-in SMTP server requirements.

        Args:
            existing_spf: Existing SPF record (if None, will fetch from DNS)

        Returns:
            Merged SPF record with built-in server included
        """
        # Fetch existing record if not provided
        if existing_spf is None:
            existing_spf = self.get_existing_spf_record()

        # Required mechanisms for built-in SMTP server
        required_mechanisms = ["mx", "a"]

        if existing_spf:
            # Parse existing SPF record
            parts = existing_spf.split()

            # Extract version and mechanisms
            mechanisms = []
            qualifier = "~all"  # Default qualifier

            for part in parts:
                if part.startswith("v=spf1"):
                    continue  # Skip version
                elif part.endswith("all"):
                    qualifier = part  # Save the qualifier (e.g., ~all, -all)
                else:
                    mechanisms.append(part)

            # Add required mechanisms if not present
            for req in required_mechanisms:
                if req not in mechanisms:
                    mechanisms.insert(0, req)  # Add at beginning

            # Rebuild SPF record
            merged = f"v=spf1 {' '.join(mechanisms)} {qualifier}"
            logger.info(f"Merged SPF record: {merged}")
            return merged

        else:
            # No existing record - create new one with strict policy
            # Using -all (hardfail) for better security - rejects unauthorized senders
            new_spf = "v=spf1 mx a -all"
            logger.info(f"Created new SPF record: {new_spf}")
            return new_spf

    def get_existing_dmarc_record(self) -> str | None:
        """
        Fetch the existing DMARC record from DNS.

        Returns:
            Existing DMARC record string or None if not found
        """
        try:
            dmarc_hostname = f"_dmarc.{self.domain}"
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            resolver.lifetime = 5

            # Query TXT records
            answers = resolver.resolve(dmarc_hostname, "TXT")

            # Find DMARC record (starts with "v=DMARC1")
            for rdata in answers:
                txt_data = b"".join(rdata.strings).decode("utf-8")
                if txt_data.startswith("v=DMARC1"):
                    logger.info(f"Found existing DMARC record for {self.domain}: {txt_data}")
                    return txt_data

            logger.info(f"No existing DMARC record found for {self.domain}")
            return None

        except dns.resolver.NXDOMAIN:
            logger.info(f"Domain _dmarc.{self.domain} does not exist")
            return None
        except dns.exception.DNSException as e:
            logger.warning(f"Error fetching DMARC record for {self.domain}: {e}")
            return None

    def merge_dmarc_record(self, existing_dmarc: str | None = None) -> str:
        """
        Merge existing DMARC record to ensure proper alignment settings.

        Args:
            existing_dmarc: Existing DMARC record (if None, will fetch from DNS)

        Returns:
            Merged DMARC record with proper alignment settings
        """
        # Fetch existing record if not provided
        if existing_dmarc is None:
            existing_dmarc = self.get_existing_dmarc_record()

        if existing_dmarc:
            # Parse existing DMARC record
            params = {}
            parts = [p.strip() for p in existing_dmarc.split(";") if p.strip()]

            for part in parts:
                if "=" in part:
                    key, value = part.split("=", 1)
                    params[key.strip()] = value.strip()

            # Ensure required parameters for multi-provider setup
            params["v"] = "DMARC1"  # Version must be DMARC1

            # Set relaxed alignment for multi-provider compatibility
            # This allows subdomains and different From: domains
            params["aspf"] = "r"  # Relaxed SPF alignment
            params["adkim"] = "r"  # Relaxed DKIM alignment

            # Ensure reasonable policy (at least quarantine)
            if "p" not in params:
                params["p"] = "quarantine"
            elif params["p"] == "none":
                # Upgrade from 'none' to 'quarantine' for better security
                params["p"] = "quarantine"
                logger.info("Upgraded DMARC policy from 'none' to 'quarantine'")

            # Ensure reporting addresses exist (keep existing if present)
            if "rua" not in params:
                params["rua"] = f"mailto:postmaster@{self.domain}"

            if "ruf" not in params:
                params["ruf"] = f"mailto:postmaster@{self.domain}"

            # Ensure failure reporting option
            if "fo" not in params:
                params["fo"] = "1"  # Generate reports for any failure

            # Rebuild DMARC record
            # Order: v, p, aspf, adkim, rua, ruf, fo, then others
            ordered_keys = ["v", "p", "aspf", "adkim", "rua", "ruf", "fo"]
            other_keys = [k for k in params if k not in ordered_keys]
            all_keys = ordered_keys + other_keys

            parts = [f"{key}={params[key]}" for key in all_keys if key in params]
            merged = "; ".join(parts)

            logger.info(f"Merged DMARC record: {merged}")
            return merged

        else:
            # No existing record - create new one
            new_dmarc = f"v=DMARC1; p=quarantine; aspf=r; adkim=r; rua=mailto:postmaster@{self.domain}; ruf=mailto:postmaster@{self.domain}; fo=1"
            logger.info(f"Created new DMARC record: {new_dmarc}")
            return new_dmarc

    def detect_dns_provider(self) -> dict:
        """
        Detect which DNS provider is being used for this domain by analyzing nameservers.

        Returns:
            Dictionary with provider name, nameservers list, and confidence level
            {
                'provider': 'cloudflare',  # or 'godaddy', 'namecheap', 'route53', 'unknown'
                'provider_display': 'Cloudflare',
                'nameservers': ['ns1.example.com', 'ns2.example.com'],
                'confidence': 'high'  # or 'medium', 'low'
            }
        """
        result = {
            "provider": "unknown",
            "provider_display": "Other",
            "nameservers": [],
            "confidence": "unknown",
        }

        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            resolver.lifetime = 5

            # Query NS records
            answers = resolver.resolve(self.domain, "NS")

            # Collect all nameservers
            nameservers = [str(rdata.target).rstrip(".").lower() for rdata in answers]
            result["nameservers"] = nameservers

            if not nameservers:
                logger.warning(f"No nameservers found for {self.domain}")
                return result

            # Analyze nameservers to detect provider
            # Use first nameserver for primary detection, but check all for confidence
            primary_ns = nameservers[0]

            # Provider detection patterns
            providers = [
                # Pattern, provider_key, display_name
                ("cloudflare.com", "cloudflare", "Cloudflare"),
                ("domaincontrol.com", "godaddy", "GoDaddy"),
                ("godaddy", "godaddy", "GoDaddy"),
                ("registrar-servers.com", "namecheap", "Namecheap"),
                ("namecheap", "namecheap", "Namecheap"),
                ("awsdns", "route53", "AWS Route 53"),
                ("route53", "route53", "AWS Route 53"),
                ("googledomains.com", "google", "Google Domains"),
                ("azure-dns", "azure", "Azure DNS"),
                ("dnsimple.com", "dnsimple", "DNSimple"),
                ("ns1.com", "ns1", "NS1"),
                ("nsone.net", "ns1", "NS1"),
                ("hover.com", "hover", "Hover"),
                ("name.com", "namecom", "Name.com"),
                ("networksolutions.com", "networksolutions", "Network Solutions"),
            ]

            # Check each nameserver against patterns
            for pattern, provider_key, display_name in providers:
                if pattern in primary_ns:
                    result["provider"] = provider_key
                    result["provider_display"] = display_name

                    # Check if all nameservers match (high confidence)
                    if all(pattern in ns for ns in nameservers):
                        result["confidence"] = "high"
                    else:
                        result["confidence"] = "medium"

                    logger.info(
                        f"Detected DNS provider for {self.domain}: {display_name} (confidence: {result['confidence']})"
                    )
                    break

            # If no provider detected, mark as unknown with low confidence
            if result["provider"] == "unknown":
                result["confidence"] = "low"
                logger.info(
                    f"Could not detect DNS provider for {self.domain}. Nameservers: {', '.join(nameservers)}"
                )

        except dns.resolver.NXDOMAIN:
            logger.warning(f"Domain {self.domain} does not exist")
        except dns.exception.DNSException as e:
            logger.warning(f"Error detecting DNS provider for {self.domain}: {e}")

        return result

    @staticmethod
    def clear_cache(domain: str, dkim_selector: str | None = None):
        """
        Clear cached DNS results for a domain.

        Args:
            domain: Domain to clear cache for
            dkim_selector: Specific DKIM selector to clear (optional)
        """
        cache.delete(f"dns_mx_{domain}")
        cache.delete(f"dns_spf_{domain}")
        # Clear specific selector if provided
        if dkim_selector:
            # Handle both formats: with and without ._domainkey
            if "._domainkey" in dkim_selector:
                cache.delete(f"dns_dkim_{dkim_selector}.{domain}")
            else:
                cache.delete(f"dns_dkim_{dkim_selector}._domainkey.{domain}")
        # Also clear common selectors used by known providers
        for selector in [
            "mail",
            "default",
            "google",
            "k1",
            "selector1",
            "selector2",
            "s1",
            "s2",
            "mailo",
        ]:
            cache.delete(f"dns_dkim_{selector}._domainkey.{domain}")
        cache.delete(f"dns_dmarc__dmarc.{domain}")
        logger.info(f"Cleared DNS cache for {domain}")
