"""
Display GeoIP statistics
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Count, F
from django.utils import timezone

from geoip.models import BusinessRule, GeoIPProvider, GeoLocation, VisitorLocation


class Command(BaseCommand):
    help = "Display GeoIP statistics"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="Number of days to include in statistics (default: 7)",
        )

    def handle(self, *args, **options):
        days = options["days"]
        since = timezone.now() - timedelta(days=days)

        self.stdout.write(f"GeoIP Statistics (Last {days} days)")
        self.stdout.write("=" * 60)

        # Cache statistics
        self.stdout.write("\n📦 Cache Statistics:")
        total_cached = GeoLocation.objects.count()
        recent_cached = GeoLocation.objects.filter(resolved_at__gte=since).count()
        expired = GeoLocation.objects.filter(expires_at__lt=timezone.now()).count()

        self.stdout.write(f"  Total cached locations: {total_cached:,}")
        self.stdout.write(f"  Recently resolved: {recent_cached:,}")
        self.stdout.write(f"  Expired entries: {expired:,}")

        # Top countries
        self.stdout.write("\n🌍 Top Countries:")
        top_countries = (
            GeoLocation.objects.filter(resolved_at__gte=since)
            .values("country_code")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        for country in top_countries:
            code = country["country_code"] or "Unknown"
            flag = self._country_flag(code)
            self.stdout.write(f"  {flag} {code}: {country['count']:,}")

        # Provider statistics
        self.stdout.write("\n🔌 Provider Statistics:")
        providers = GeoIPProvider.objects.filter(is_active=True).order_by("priority")

        for provider in providers:
            accuracy = provider.accuracy_rate
            avg_ms = provider.average_response_ms

            status = "✓" if provider.is_active else "✗"
            color = (
                self.style.SUCCESS
                if accuracy >= 90
                else self.style.WARNING
                if accuracy >= 70
                else self.style.ERROR
            )

            self.stdout.write(f"  {status} {provider.name}")
            self.stdout.write(f"     Type: {provider.get_provider_type_display()}")
            self.stdout.write(color(f"     Accuracy: {accuracy:.1f}%"))
            self.stdout.write(f"     Avg Response: {avg_ms:.1f}ms")
            self.stdout.write(f"     Total Lookups: {provider.total_lookups:,}")

        # Visitor statistics
        self.stdout.write("\n👥 Visitor Statistics:")
        total_visitors = VisitorLocation.objects.filter(last_seen__gte=since).count()
        returning_visitors = VisitorLocation.objects.filter(
            last_seen__gte=since, page_views__gt=1
        ).count()

        # Correction rate
        corrected = (
            VisitorLocation.objects.filter(last_seen__gte=since)
            .exclude(actual_country__isnull=True)
            .exclude(actual_country=F("resolved_country"))
            .count()
        )

        correction_rate = (corrected / total_visitors * 100) if total_visitors > 0 else 0

        self.stdout.write(f"  Total visitors: {total_visitors:,}")
        self.stdout.write(f"  Returning visitors: {returning_visitors:,}")
        self.stdout.write(f"  Location corrections: {corrected:,} ({correction_rate:.1f}%)")

        # Detection statistics
        self.stdout.write("\n🔍 Detection Statistics:")
        vpn_detected = GeoLocation.objects.filter(resolved_at__gte=since, is_vpn=True).count()
        proxy_detected = GeoLocation.objects.filter(resolved_at__gte=since, is_proxy=True).count()
        tor_detected = GeoLocation.objects.filter(resolved_at__gte=since, is_tor=True).count()
        mobile_detected = GeoLocation.objects.filter(resolved_at__gte=since, is_mobile=True).count()

        if recent_cached > 0:
            self.stdout.write(
                f"  VPN: {vpn_detected:,} ({vpn_detected / recent_cached * 100:.1f}%)"
            )
            self.stdout.write(
                f"  Proxy: {proxy_detected:,} ({proxy_detected / recent_cached * 100:.1f}%)"
            )
            self.stdout.write(
                f"  Tor: {tor_detected:,} ({tor_detected / recent_cached * 100:.1f}%)"
            )
            self.stdout.write(
                f"  Mobile: {mobile_detected:,} ({mobile_detected / recent_cached * 100:.1f}%)"
            )

        # Business rules
        self.stdout.write("\n📋 Business Rules:")
        active_rules = BusinessRule.objects.filter(is_active=True).order_by("-times_triggered")[:5]

        if active_rules:
            for rule in active_rules:
                self.stdout.write(f"  {rule.name}")
                self.stdout.write(f"     Triggered: {rule.times_triggered:,} times")
                if rule.last_triggered:
                    self.stdout.write(
                        f"     Last: {rule.last_triggered.strftime('%Y-%m-%d %H:%M')}"
                    )
        else:
            self.stdout.write("  No active business rules")

        # Confidence levels
        self.stdout.write("\n📊 Confidence Distribution:")
        confidence_ranges = [
            (0.9, 1.0, "High (90-100%)"),
            (0.7, 0.9, "Medium (70-90%)"),
            (0.5, 0.7, "Low (50-70%)"),
            (0.0, 0.5, "Very Low (<50%)"),
        ]

        for min_conf, max_conf, label in confidence_ranges:
            count = GeoLocation.objects.filter(
                resolved_at__gte=since, confidence__gte=min_conf, confidence__lt=max_conf
            ).count()

            if recent_cached > 0:
                percentage = count / recent_cached * 100
                bar = "█" * int(percentage / 2)
                self.stdout.write(f"  {label:20} {bar} {count:,} ({percentage:.1f}%)")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Statistics complete!"))

    def _country_flag(self, country_code):
        """Convert country code to flag emoji"""
        if not country_code or len(country_code) != 2:
            return "  "
        return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in country_code.upper())
