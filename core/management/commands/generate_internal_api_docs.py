"""
Management command to generate internal API documentation
This is for development use only - NOT for merchant deployments
"""

import inspect
import json
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin


class Command(BaseCommand):
    help = "Generate internal API documentation in markdown format"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-dir",
            default=".claude_code/api_docs",
            help="Output directory for documentation",
        )
        parser.add_argument(
            "--format",
            choices=["markdown", "json", "both"],
            default="markdown",
            help="Output format for documentation",
        )

    def handle(self, *args, **options):
        if not getattr(settings, "ENABLE_API_DOCS", False) and not settings.DEBUG:
            self.stdout.write(
                self.style.ERROR(
                    "API documentation is disabled. Set ENABLE_API_DOCS=True or DEBUG=True"
                )
            )
            return

        output_dir = Path(settings.BASE_DIR) / options["output_dir"]
        output_dir.mkdir(parents=True, exist_ok=True)

        self.stdout.write("Generating internal API documentation...")

        # Collect API information
        api_data = self.collect_api_data()

        # Generate documentation
        if options["format"] in ["markdown", "both"]:
            self.generate_markdown_docs(api_data, output_dir)
            self.stdout.write(
                self.style.SUCCESS(f"Markdown documentation generated in {output_dir}")
            )

        if options["format"] in ["json", "both"]:
            self.generate_json_docs(api_data, output_dir)
            self.stdout.write(self.style.SUCCESS(f"JSON documentation generated in {output_dir}"))

    def collect_api_data(self):
        """Collect information about all APIs in the project"""
        api_data = {"apps": {}, "viewsets": [], "api_views": [], "endpoints": []}

        # Iterate through all installed apps
        for app_config in apps.get_app_configs():
            app_name = app_config.name

            # Skip Django's built-in apps and third-party apps
            if app_name.startswith("django.") or app_name in ["rest_framework", "allauth"]:
                continue

            try:
                # Try to import api views/viewsets
                views_module = None
                viewsets_module = None

                # Check for api_views.py
                try:
                    views_module = __import__(f"{app_name}.api_views", fromlist=[""])
                except ImportError:
                    pass

                # Check for viewsets.py
                try:
                    viewsets_module = __import__(f"{app_name}.viewsets", fromlist=[""])
                except ImportError:
                    pass

                # Check for api package
                try:
                    __import__(f"{app_name}.api", fromlist=[""])
                except ImportError:
                    pass

                # Collect ViewSets and APIViews
                app_apis = {"viewsets": [], "api_views": [], "urls": []}

                # Process views module
                if views_module:
                    for name, obj in inspect.getmembers(views_module):
                        if inspect.isclass(obj):
                            if issubclass(obj, ViewSetMixin):
                                app_apis["viewsets"].append(
                                    {
                                        "name": name,
                                        "docstring": inspect.getdoc(obj) or "No documentation",
                                        "methods": self.get_viewset_methods(obj),
                                    }
                                )
                            elif issubclass(obj, APIView):
                                app_apis["api_views"].append(
                                    {
                                        "name": name,
                                        "docstring": inspect.getdoc(obj) or "No documentation",
                                        "methods": self.get_api_view_methods(obj),
                                    }
                                )

                # Process viewsets module
                if viewsets_module:
                    for name, obj in inspect.getmembers(viewsets_module):
                        if inspect.isclass(obj) and issubclass(obj, ViewSetMixin):
                            app_apis["viewsets"].append(
                                {
                                    "name": name,
                                    "docstring": inspect.getdoc(obj) or "No documentation",
                                    "methods": self.get_viewset_methods(obj),
                                }
                            )

                if app_apis["viewsets"] or app_apis["api_views"]:
                    api_data["apps"][app_name] = app_apis
                    self.stdout.write(f"  Found APIs in {app_name}")

            except Exception as e:
                self.stdout.write(f"  Skipping {app_name}: {str(e)}")

        return api_data

    def get_viewset_methods(self, viewset_class):
        """Extract methods from a ViewSet"""
        methods = []
        standard_actions = ["list", "create", "retrieve", "update", "partial_update", "destroy"]

        for action in standard_actions:
            if hasattr(viewset_class, action):
                method = getattr(viewset_class, action)
                if callable(method) and not action.startswith("_"):
                    methods.append(
                        {
                            "name": action,
                            "docstring": inspect.getdoc(method) or f"Standard {action} action",
                        }
                    )

        # Look for custom actions
        for name, method in inspect.getmembers(viewset_class):
            if hasattr(method, "mapping"):  # It's an @action decorator
                methods.append(
                    {
                        "name": name,
                        "docstring": inspect.getdoc(method) or f"Custom action: {name}",
                        "custom": True,
                    }
                )

        return methods

    def get_api_view_methods(self, api_view_class):
        """Extract HTTP methods from an APIView"""
        methods = []
        http_methods = ["get", "post", "put", "patch", "delete"]

        for method_name in http_methods:
            if hasattr(api_view_class, method_name):
                method = getattr(api_view_class, method_name)
                if callable(method) and not method_name.startswith("_"):
                    methods.append(
                        {
                            "name": method_name.upper(),
                            "docstring": inspect.getdoc(method) or f"{method_name.upper()} method",
                        }
                    )

        return methods

    def generate_markdown_docs(self, api_data, output_dir):
        """Generate markdown documentation files"""
        # Update the main index
        index_path = output_dir / "API_INDEX.md"
        with open(index_path, "w") as f:
            f.write("# API Index - Auto-Generated\n\n")
            f.write("This is an auto-generated index of all APIs in the project.\n\n")

            for app_name, app_apis in api_data["apps"].items():
                f.write(f"## {app_name}\n\n")

                if app_apis["viewsets"]:
                    f.write("### ViewSets\n")
                    for viewset in app_apis["viewsets"]:
                        f.write(
                            f"- **{viewset['name']}**: {viewset['docstring'].split('\\n')[0]}\n"
                        )
                        if viewset["methods"]:
                            f.write(
                                "  - Actions: "
                                + ", ".join(m["name"] for m in viewset["methods"])
                                + "\n"
                            )
                    f.write("\n")

                if app_apis["api_views"]:
                    f.write("### API Views\n")
                    for view in app_apis["api_views"]:
                        f.write(f"- **{view['name']}**: {view['docstring'].split('\\n')[0]}\n")
                        if view["methods"]:
                            f.write(
                                "  - Methods: "
                                + ", ".join(m["name"] for m in view["methods"])
                                + "\n"
                            )
                    f.write("\n")

        # Generate app-specific documentation
        apps_dir = output_dir / "generated"
        apps_dir.mkdir(exist_ok=True)

        for app_name, app_apis in api_data["apps"].items():
            app_doc_path = apps_dir / f"{app_name}_api.md"
            with open(app_doc_path, "w") as f:
                f.write(f"# {app_name.title()} API Documentation\n\n")
                f.write("*Auto-generated documentation*\n\n")

                if app_apis["viewsets"]:
                    f.write("## ViewSets\n\n")
                    for viewset in app_apis["viewsets"]:
                        f.write(f"### {viewset['name']}\n\n")
                        f.write(f"{viewset['docstring']}\n\n")

                        if viewset["methods"]:
                            f.write("#### Available Actions:\n\n")
                            for method in viewset["methods"]:
                                custom = method.get("custom", False)
                                marker = " (custom)" if custom else ""
                                f.write(f"- **{method['name']}{marker}**: {method['docstring']}\n")
                            f.write("\n")

                if app_apis["api_views"]:
                    f.write("## API Views\n\n")
                    for view in app_apis["api_views"]:
                        f.write(f"### {view['name']}\n\n")
                        f.write(f"{view['docstring']}\n\n")

                        if view["methods"]:
                            f.write("#### HTTP Methods:\n\n")
                            for method in view["methods"]:
                                f.write(f"- **{method['name']}**: {method['docstring']}\n")
                            f.write("\n")

    def generate_json_docs(self, api_data, output_dir):
        """Generate JSON documentation files"""
        json_path = output_dir / "api_documentation.json"
        with open(json_path, "w") as f:
            json.dump(api_data, f, indent=2)

        # Also generate OpenAPI schema if drf-spectacular is available
        try:
            from drf_spectacular.generators import SchemaGenerator

            generator = SchemaGenerator()
            schema = generator.get_schema()

            openapi_path = output_dir / "openapi_schema.json"
            with open(openapi_path, "w") as f:
                json.dump(schema, f, indent=2)

            self.stdout.write(self.style.SUCCESS(f"OpenAPI schema generated: {openapi_path}"))
        except ImportError:
            self.stdout.write(
                self.style.WARNING("drf-spectacular not available for OpenAPI schema generation")
            )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not generate OpenAPI schema: {str(e)}"))
