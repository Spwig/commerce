"""
Management command to export help content bundle for AI training and analysis.
This creates a structured JSON export suitable for feeding to Claude or other AI systems.
"""

import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import HelpCategory, HelpFeedback, HelpTopic


class Command(BaseCommand):
    help = "Export help content bundle for AI training and analysis"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default="help_bundle.json",
            help="Output file path (default: help_bundle.json)",
        )
        parser.add_argument(
            "--include-stats",
            action="store_true",
            help="Include usage statistics and feedback",
        )
        parser.add_argument(
            "--component",
            type=str,
            help="Export only specific component (default: all)",
        )
        parser.add_argument(
            "--format",
            type=str,
            choices=["json", "markdown", "jsonl"],
            default="json",
            help="Output format (default: json)",
        )

    def handle(self, *args, **options):
        output_path = Path(options["output"])
        include_stats = options["include_stats"]
        component = options["component"]
        output_format = options["format"]

        # Get topics
        topics_qs = HelpTopic.objects.filter(is_published=True)
        if component:
            topics_qs = topics_qs.filter(component=component)

        topics_qs = topics_qs.select_related("category").prefetch_related("related_topics")

        self.stdout.write(f"Exporting {topics_qs.count()} help topics...")

        if output_format == "json":
            self._export_json(output_path, topics_qs, include_stats)
        elif output_format == "markdown":
            self._export_markdown(output_path, topics_qs, include_stats)
        elif output_format == "jsonl":
            self._export_jsonl(output_path, topics_qs, include_stats)

        self.stdout.write(self.style.SUCCESS(f"Export completed: {output_path}"))

    def _export_json(self, output_path, topics_qs, include_stats):
        """Export as structured JSON"""
        # Build categories map
        categories = {}
        for category in HelpCategory.objects.all():
            categories[category.slug] = {
                "name": category.name,
                "slug": category.slug,
                "icon": category.icon,
                "description": category.description,
                "order": category.order,
            }

        # Build topics
        topics = []
        for topic in topics_qs:
            topic_data = {
                "slug": topic.slug,
                "title_i18n_key": topic.title_i18n_key,
                "category": topic.category.slug,
                "component": topic.component,
                "content": topic.content_markdown,
                "keywords": topic.keywords,
                "url_patterns": topic.url_patterns,
                "min_version": topic.min_version or None,
                "max_version": topic.max_version or None,
                "related_topics": [t.slug for t in topic.related_topics.all()],
                "created_at": topic.created_at.isoformat(),
                "updated_at": topic.updated_at.isoformat(),
            }

            if include_stats:
                topic_data["stats"] = {
                    "view_count": topic.view_count,
                    "helpful_count": topic.helpful_count,
                    "not_helpful_count": topic.not_helpful_count,
                    "helpfulness_percentage": topic.helpfulness_percentage,
                }

                # Get recent feedback
                recent_feedback = (
                    HelpFeedback.objects.filter(topic=topic, comment__isnull=False)
                    .exclude(comment="")
                    .order_by("-created_at")[:10]
                )

                topic_data["recent_feedback"] = [
                    {
                        "helpful": fb.helpful,
                        "comment": fb.comment,
                        "created_at": fb.created_at.isoformat(),
                    }
                    for fb in recent_feedback
                ]

            topics.append(topic_data)

        # Build bundle
        bundle = {
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "platform_version": getattr(settings, "PLATFORM_VERSION", "1.0.0"),
            "topics_count": len(topics),
            "categories_count": len(categories),
            "categories": categories,
            "topics": topics,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=2, ensure_ascii=False)

    def _export_markdown(self, output_path, topics_qs, include_stats):
        """Export as single markdown document"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Help Content Export\n\n")
            f.write(f"Exported: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n")
            f.write(f"Topics: {topics_qs.count()}\n\n")
            f.write("---\n\n")

            # Group by category
            current_category = None
            for topic in topics_qs.order_by("category__order", "category__name", "slug"):
                if current_category != topic.category.slug:
                    current_category = topic.category.slug
                    f.write(f"\n## {topic.category.name}\n\n")

                f.write(f"### {topic.slug}\n\n")
                f.write(f"**Component:** {topic.component}\n\n")

                if topic.keywords:
                    f.write(f"**Keywords:** {', '.join(topic.keywords)}\n\n")

                if topic.min_version or topic.max_version:
                    version_info = []
                    if topic.min_version:
                        version_info.append(f"≥ {topic.min_version}")
                    if topic.max_version:
                        version_info.append(f"≤ {topic.max_version}")
                    f.write(f"**Versions:** {' '.join(version_info)}\n\n")

                if include_stats:
                    f.write(f"**Views:** {topic.view_count} | ")
                    f.write(
                        f"**Helpful:** {topic.helpful_count}/{topic.helpful_count + topic.not_helpful_count}"
                    )
                    if topic.helpfulness_percentage:
                        f.write(f" ({topic.helpfulness_percentage:.1f}%)")
                    f.write("\n\n")

                f.write(topic.content_markdown)
                f.write("\n\n---\n\n")

    def _export_jsonl(self, output_path, topics_qs, include_stats):
        """Export as JSONL (one JSON object per line) - useful for AI training"""
        with open(output_path, "w", encoding="utf-8") as f:
            for topic in topics_qs:
                topic_data = {
                    "id": topic.slug,
                    "category": topic.category.name,
                    "component": topic.component,
                    "title_key": topic.title_i18n_key,
                    "content": topic.content_markdown,
                    "keywords": " ".join(topic.keywords) if topic.keywords else "",
                }

                if include_stats and topic.view_count > 0:
                    topic_data["popularity_score"] = topic.view_count
                    if topic.helpfulness_percentage:
                        topic_data["quality_score"] = topic.helpfulness_percentage / 100

                f.write(json.dumps(topic_data, ensure_ascii=False) + "\n")
