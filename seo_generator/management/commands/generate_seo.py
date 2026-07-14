"""
Management command for batch SEO generation.

Usage:
    python manage.py generate_seo --model=product
    python manage.py generate_seo --model=category --batch-size=50
    python manage.py generate_seo --model=all --auto-only
"""

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _
from tqdm import tqdm

from core.models import SiteSettings
from seo_generator.api.endpoints import MODEL_MAP, extract_content_from_object
from seo_generator.providers.base import ProviderNotAvailable
from seo_generator.providers.registry import ProviderRegistry

# Model types supported for SEO generation
ALL_MODEL_TYPES = list(MODEL_MAP.keys())


class Command(BaseCommand):
    help = "Generate SEO content for products, categories, brands, pages, or blog content in bulk"

    def add_arguments(self, parser):
        parser.add_argument(
            "--model",
            type=str,
            required=True,
            choices=ALL_MODEL_TYPES + ["all"],
            help=_('Model type to generate SEO for (or "all" for all models)'),
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=50,
            help=_("Number of items to process in each batch (default: 50)"),
        )
        parser.add_argument(
            "--auto-only",
            action="store_true",
            help=_("Only generate SEO for items with seo_auto_generated=True"),
        )
        parser.add_argument(
            "--provider",
            type=str,
            default=None,
            help=_(
                "SEO provider to use (default: primary provider, or deterministic if none configured)"
            ),
        )
        parser.add_argument(
            "--language",
            type=str,
            default=None,
            help=_("Language code for generation (default: site primary language)"),
        )

    def handle(self, *args, **options):
        model_type = options["model"]
        batch_size = options["batch_size"]
        auto_only = options["auto_only"]
        provider_key = options["provider"]
        language = options["language"]

        # Get default language if not specified
        if not language:
            try:
                site_settings = SiteSettings.objects.get(pk=1)
                language = site_settings.default_language
            except SiteSettings.DoesNotExist:
                language = "en"

        self.stdout.write(_("Using language: %(lang)s") % {"lang": language})

        # Get provider instance (with credentials for external providers)
        try:
            provider = ProviderRegistry.get_provider_instance(provider_key)
        except ProviderNotAvailable as e:
            raise CommandError(str(e))
        self.stdout.write(_("Using provider: %(name)s") % {"name": provider.provider_name})

        # Determine which models to process
        model_types = ALL_MODEL_TYPES if model_type == "all" else [model_type]

        # Process each model type
        total_processed = 0
        total_successful = 0
        total_failed = 0

        for mt in model_types:
            processed, successful, failed = self._process_model(
                mt, provider, language, batch_size, auto_only
            )
            total_processed += processed
            total_successful += successful
            total_failed += failed

        # Summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(_("SEO Generation Complete")))
        self.stdout.write(_("Total Processed: %(count)d") % {"count": total_processed})
        self.stdout.write(
            self.style.SUCCESS(_("Successful: %(count)d") % {"count": total_successful})
        )
        if total_failed > 0:
            self.stdout.write(self.style.ERROR(_("Failed: %(count)d") % {"count": total_failed}))
        self.stdout.write("=" * 50)

    def _process_model(self, model_type, provider, language, batch_size, auto_only):
        """Process a single model type."""
        # Get model class from MODEL_MAP
        if model_type not in MODEL_MAP:
            self.stdout.write(
                self.style.WARNING(
                    _("\nSkipping unknown model type: %(type)s") % {"type": model_type}
                )
            )
            return 0, 0, 0

        app_label, model_name = MODEL_MAP[model_type]
        model_class = apps.get_model(app_label, model_name)

        # Get queryset
        queryset = model_class.objects.all()
        if auto_only:
            queryset = queryset.filter(seo_auto_generated=True)

        total_count = queryset.count()

        if total_count == 0:
            self.stdout.write(_("\nNo %(type)s items to process") % {"type": model_type})
            return 0, 0, 0

        self.stdout.write(
            _("\n%(type)s (%(count)d items)")
            % {"type": model_type.capitalize(), "count": total_count}
        )
        self.stdout.write("-" * 50)

        successful = 0
        failed = 0

        # Process in batches with progress bar
        with tqdm(total=total_count, desc=f"Processing {model_type}", unit="item") as pbar:
            for i in range(0, total_count, batch_size):
                batch = queryset[i : i + batch_size]

                for obj in batch:
                    try:
                        # Extract content
                        content = extract_content_from_object(obj, model_type)

                        # Generate SEO
                        result = provider.generate_seo(content, language)

                        # Save to object
                        obj.meta_title = result["meta_title"]
                        obj.meta_description = result["meta_description"]
                        obj.save(update_fields=["meta_title", "meta_description"])

                        successful += 1
                        pbar.set_postfix({"success": successful, "failed": failed})

                    except Exception as e:
                        failed += 1
                        self.stdout.write(
                            self.style.ERROR(
                                _("  Failed %(type)s %(pk)s: %(error)s")
                                % {"type": model_type, "pk": obj.pk, "error": str(e)}
                            )
                        )
                        pbar.set_postfix({"success": successful, "failed": failed})

                    pbar.update(1)

        self.stdout.write(
            self.style.SUCCESS(
                _("  %(type)s: %(success)d successful, %(failed)d failed")
                % {"type": model_type.capitalize(), "success": successful, "failed": failed}
            )
        )

        return total_count, successful, failed
