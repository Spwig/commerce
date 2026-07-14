"""
Email Configuration Sync Serializer

Handles export/import of email models:
- EmailAccount (with encrypted credentials)
- EmailTemplate (with nested EmailTemplateTranslation)
"""

import logging

from django.contrib.sites.models import Site
from django.db import transaction

from ..credential_handler import (
    decrypt_credentials_for_export,
    encrypt_credentials_for_import,
    redact_credentials,
)
from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

EMAIL_ACCOUNT_FIELDS = [
    "provider_key",
    "name",
    "from_email",
    "from_name",
    "reply_to",
    "is_active",
    "is_default",
    "settings",
    "dns_validated",
    "dns_domain",
]

EMAIL_TEMPLATE_FIELDS = [
    "template_type",
    "language_code",
    "subject",
    "html_content",
    "text_content",
    "is_active",
    "is_system",
    "version",
]

EMAIL_TEMPLATE_TRANSLATION_FIELDS = [
    "language_code",
    "subject",
    "html_content",
    "text_content",
    "is_verified",
    "quality_score",
    "base_template_version",
]


class EmailConfigSerializer(CollectionSyncSerializer):
    """Serializer for email accounts and templates."""

    category_key = "email_config"
    natural_key_fields = ["name"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from email_system.models import EmailAccount

        self.model_class = EmailAccount

    def get_count(self):
        from email_system.models import EmailAccount, EmailTemplate, EmailTemplateTranslation

        return (
            EmailAccount.objects.count()
            + EmailTemplate.objects.filter(is_deleted=False).count()
            + EmailTemplateTranslation.objects.count()
        )

    def export(self, credential_mode="redact"):
        from email_system.models import EmailAccount, EmailTemplate

        accounts = []
        for account in EmailAccount.objects.all():
            data = {field: getattr(account, field) for field in EMAIL_ACCOUNT_FIELDS}
            data["_source_pk"] = str(account.pk)
            data["_model"] = "EmailAccount"

            # Handle credentials based on mode
            if credential_mode == "decrypt":
                creds = decrypt_credentials_for_export("email_config", "EmailAccount", account)
                if creds:
                    data["_credentials"] = creds
            elif credential_mode == "redact":
                creds = decrypt_credentials_for_export("email_config", "EmailAccount", account)
                if creds:
                    data["_credentials_redacted"] = redact_credentials(creds)

            # Store component slug for matching on import
            if account.component:
                data["_component_slug"] = account.component.slug

            accounts.append(data)

        templates = []
        for template in EmailTemplate.objects.filter(
            is_deleted=False,
        ).prefetch_related("translations"):
            data = {field: getattr(template, field) for field in EMAIL_TEMPLATE_FIELDS}
            data["_source_pk"] = str(template.pk)
            data["_model"] = "EmailTemplate"

            # Nested translations
            data["_translations"] = []
            for trans in template.translations.all().order_by("language_code"):
                t_data = {f: getattr(trans, f) for f in EMAIL_TEMPLATE_TRANSLATION_FIELDS}
                data["_translations"].append(t_data)

            templates.append(data)

        return {
            "category": self.category_key,
            "sync_type": "collection",
            "items": accounts + templates,
            "total": len(accounts) + len(templates),
        }

    def import_data(self, data, dry_run=False, sync_mode="additive"):
        if dry_run:
            return self.generate_diff(data)

        items = data.get("items", [])
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        try:
            with transaction.atomic():
                site = Site.objects.get(pk=1)

                for item in items:
                    model_type = item.get("_model")
                    try:
                        if model_type == "EmailAccount":
                            self._import_account(item, site)
                            synced += 1
                        elif model_type == "EmailTemplate":
                            self._import_template(item, site)
                            synced += 1
                        else:
                            skipped += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"{item.get('name', 'Unknown')}: {e}")

        except Exception as e:
            logger.error(f"Email config import failed: {e}")
            return {"synced": 0, "skipped": 0, "failed": 1, "errors": [str(e)]}

        return {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

    def _import_account(self, item, site):
        """Import or update an email account."""
        from email_system.models import EmailAccount

        # Try to match by name
        existing = EmailAccount.objects.filter(name=item["name"]).first()

        if existing:
            for field in EMAIL_ACCOUNT_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            # Re-encrypt credentials if provided
            if "_credentials" in item and item["_credentials"]:
                encrypted = encrypt_credentials_for_import(
                    "email_config", "EmailAccount", item["_credentials"]
                )
                if encrypted:
                    existing.credentials = encrypted
            existing.save()
        else:
            account = EmailAccount(site=site)
            for field in EMAIL_ACCOUNT_FIELDS:
                if field in item:
                    setattr(account, field, item[field])
            # Encrypt credentials
            if "_credentials" in item and item["_credentials"]:
                encrypted = encrypt_credentials_for_import(
                    "email_config", "EmailAccount", item["_credentials"]
                )
                if encrypted:
                    account.credentials = encrypted
            # Resolve component reference
            if "_component_slug" in item:
                try:
                    from component_updates.models import ComponentRegistry

                    account.component = ComponentRegistry.objects.get(slug=item["_component_slug"])
                except Exception:
                    pass
            account.save()

    def _import_template(self, item, site):
        """Import or update an email template with nested translations."""
        from email_system.models import EmailTemplate, EmailTemplateTranslation

        # Match by template_type + language_code
        existing = EmailTemplate.objects.filter(
            template_type=item["template_type"],
            language_code=item.get("language_code", "en"),
            is_deleted=False,
        ).first()

        if existing:
            for field in EMAIL_TEMPLATE_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            existing.save()
            template = existing
        else:
            template = EmailTemplate(site=site)
            for field in EMAIL_TEMPLATE_FIELDS:
                if field in item:
                    setattr(template, field, item[field])
            template.save()

        # Import nested translations (replace all for this template)
        translations_data = item.get("_translations", [])
        if translations_data:
            template.translations.all().delete()
            for t_data in translations_data:
                trans = EmailTemplateTranslation(template=template)
                for f in EMAIL_TEMPLATE_TRANSLATION_FIELDS:
                    if f in t_data:
                        setattr(trans, f, t_data[f])
                trans.save()

    def generate_diff(self, remote_data):
        from email_system.models import EmailAccount, EmailTemplate

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            model_type = item.get("_model")
            if model_type == "EmailAccount":
                existing = EmailAccount.objects.filter(name=item.get("name")).first()
                if existing:
                    field_changes = self._compute_field_diff(existing, item, EMAIL_ACCOUNT_FIELDS)
                    if field_changes:
                        changes.append(
                            {
                                "type": "modify",
                                "model": "EmailAccount",
                                "name": item.get("name", "Unknown"),
                                "changes": field_changes,
                            }
                        )
                else:
                    changes.append(
                        {
                            "type": "add",
                            "model": "EmailAccount",
                            "name": item.get("name", "Unknown"),
                            "fields": {k: v for k, v in item.items() if not k.startswith("_")},
                        }
                    )
            elif model_type == "EmailTemplate":
                existing = EmailTemplate.objects.filter(
                    template_type=item.get("template_type"),
                    language_code=item.get("language_code", "en"),
                    is_deleted=False,
                ).first()
                if existing:
                    field_changes = self._compute_field_diff(existing, item, EMAIL_TEMPLATE_FIELDS)
                    if field_changes:
                        changes.append(
                            {
                                "type": "modify",
                                "model": "EmailTemplate",
                                "name": f"{item.get('template_type')} ({item.get('language_code', 'en')})",
                                "changes": field_changes,
                            }
                        )
                else:
                    changes.append(
                        {
                            "type": "add",
                            "model": "EmailTemplate",
                            "name": f"{item.get('template_type')} ({item.get('language_code', 'en')})",
                            "fields": {k: v for k, v in item.items() if not k.startswith("_")},
                        }
                    )

        adds = sum(1 for c in changes if c["type"] == "add")
        mods = sum(1 for c in changes if c["type"] == "modify")
        parts = []
        if adds:
            parts.append(f"{adds} addition(s)")
        if mods:
            parts.append(f"{mods} modification(s)")

        return {
            "changes": changes,
            "warnings": [],
            "summary": ", ".join(parts) if parts else "No changes",
        }

    def snapshot_current(self):
        return self.export(credential_mode="skip")

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {"restored": result.get("synced", 0), "errors": result.get("errors", [])}
        except Exception as e:
            return {"restored": 0, "errors": [str(e)]}
