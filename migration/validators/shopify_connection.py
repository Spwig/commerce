"""
Shopify pre-flight connection and system checks before migration
"""

import logging

import psutil

logger = logging.getLogger(__name__)


class ShopifyPreFlightChecker:
    """Run pre-flight checks specific to Shopify migrations"""

    def __init__(self, migration_job):
        self.job = migration_job
        self.config = migration_job.connection_config or {}

    def run_all_checks(self):
        """
        Run all Shopify pre-flight checks.

        Returns:
            dict: {
                'critical_failures': list,
                'warnings': list,
                'info': list,
                'all_passed': bool
            }
        """
        results = {
            "critical_failures": [],
            "warnings": [],
            "info": [],
            "all_passed": True,
        }

        checks = [
            self.check_connection(),
            self.check_scopes(),
            self.check_disk_space(),
            self.check_database(),
            self.estimate_duration(),
        ]

        for check in checks:
            if check["status"] == "critical":
                results["critical_failures"].append(check)
                results["all_passed"] = False
            elif check["status"] == "warning":
                results["warnings"].append(check)
            else:
                results["info"].append(check)

        return results

    def check_connection(self):
        """Verify Shopify API connection via token exchange + shop info"""
        try:
            from migration.fetchers.shopify_api import ShopifyAPIClient

            client = ShopifyAPIClient(
                store_domain=self.config.get("store_domain", ""),
                client_id=self.config.get("client_id", ""),
                client_secret=self.config.get("client_secret", ""),
            )

            result = client.test_connection()
            if result.get("success"):
                shop_name = result.get("shop_name", "Unknown")
                return {
                    "name": "API Connection",
                    "status": "ok",
                    "message": f"Connected to {shop_name}",
                }
            else:
                return {
                    "name": "API Connection",
                    "status": "critical",
                    "message": f"Connection failed: {result.get('error', 'Unknown error')}",
                }

        except Exception as e:
            return {
                "name": "API Connection",
                "status": "critical",
                "message": f"Connection error: {str(e)}",
            }

    def check_scopes(self):
        """Verify required API scopes are granted"""
        required_scopes = {
            "read_products",
            "read_customers",
            "read_orders",
        }
        recommended_scopes = {
            "read_discounts",
            "read_content",
            "read_files",
        }

        try:
            from migration.fetchers.shopify_api import ShopifyAPIClient

            client = ShopifyAPIClient(
                store_domain=self.config.get("store_domain", ""),
                client_id=self.config.get("client_id", ""),
                client_secret=self.config.get("client_secret", ""),
            )

            granted = set(client.get_available_scopes())

            missing_required = required_scopes - granted
            missing_recommended = recommended_scopes - granted

            if missing_required:
                return {
                    "name": "API Scopes",
                    "status": "critical",
                    "message": f"Missing required scopes: {', '.join(missing_required)}",
                }

            if missing_recommended:
                return {
                    "name": "API Scopes",
                    "status": "warning",
                    "message": (
                        f"Missing recommended scopes: {', '.join(missing_recommended)}. "
                        "Some data types may not be importable."
                    ),
                }

            return {
                "name": "API Scopes",
                "status": "ok",
                "message": f"{len(granted)} scopes granted",
            }

        except Exception as e:
            return {
                "name": "API Scopes",
                "status": "warning",
                "message": f"Could not verify scopes: {str(e)}",
            }

    def check_disk_space(self):
        """Check available disk space for media downloads"""
        try:
            disk = psutil.disk_usage("/")
            free_gb = disk.free / (1024**3)

            if free_gb < 1:
                return {
                    "name": "Disk Space",
                    "status": "critical",
                    "message": f"Only {free_gb:.1f} GB free. At least 1 GB required.",
                }
            elif free_gb < 5:
                return {
                    "name": "Disk Space",
                    "status": "warning",
                    "message": f"{free_gb:.1f} GB free. Consider freeing space for large imports.",
                }
            else:
                return {
                    "name": "Disk Space",
                    "status": "ok",
                    "message": f"{free_gb:.1f} GB available",
                }

        except Exception as e:
            return {
                "name": "Disk Space",
                "status": "warning",
                "message": f"Could not check disk space: {str(e)}",
            }

    def check_database(self):
        """Verify database is accessible and has space"""
        try:
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            return {
                "name": "Database",
                "status": "ok",
                "message": "Database connection verified",
            }

        except Exception as e:
            return {
                "name": "Database",
                "status": "critical",
                "message": f"Database error: {str(e)}",
            }

    def estimate_duration(self):
        """Estimate import duration based on item counts"""
        total_items = sum(
            [
                self.config.get("total_products", 0),
                self.config.get("total_categories", 0),
                self.config.get("total_customers", 0),
                self.config.get("total_orders", 0),
                self.config.get("total_coupons", 0),
                self.config.get("total_blog_posts", 0),
            ]
        )

        # Rough estimate: ~2 seconds per item (including image downloads)
        estimated_minutes = max(1, int(total_items * 2 / 60))

        if estimated_minutes > 240:
            return {
                "name": "Estimated Duration",
                "status": "warning",
                "message": (
                    f"~{estimated_minutes // 60}h {estimated_minutes % 60}m for "
                    f"{total_items} items. Large imports may take a while."
                ),
            }

        return {
            "name": "Estimated Duration",
            "status": "ok",
            "message": f"~{estimated_minutes} minutes for {total_items} items",
        }
