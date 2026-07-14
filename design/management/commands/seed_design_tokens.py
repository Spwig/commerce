from core.management.commands._seed_base import SeedCommand


class Command(SeedCommand):
    seed_name = "design_tokens"
    seed_version = 1
    help = "Seed default system design tokens (colors, typography, spacing, etc.)"

    # Token definitions: (name, value, description)
    PRIMARY_COLORS = [
        ("primary-50", "#EFF6FF", "Lightest primary blue"),
        ("primary-100", "#DBEAFE", "Very light primary blue"),
        ("primary-200", "#BFDBFE", "Light primary blue"),
        ("primary-300", "#93C5FD", "Medium light primary blue"),
        ("primary-400", "#60A5FA", "Medium primary blue"),
        ("primary-500", "#3B82F6", "Base primary blue"),
        ("primary-600", "#2563EB", "Medium dark primary blue"),
        ("primary-700", "#1D4ED8", "Dark primary blue"),
        ("primary-800", "#1E40AF", "Very dark primary blue"),
        ("primary-900", "#1E3A8A", "Darkest primary blue"),
    ]
    SECONDARY_COLORS = [
        ("secondary-50", "#FAF5FF", "Lightest secondary purple"),
        ("secondary-100", "#F3E8FF", "Very light secondary purple"),
        ("secondary-200", "#E9D5FF", "Light secondary purple"),
        ("secondary-300", "#D8B4FE", "Medium light secondary purple"),
        ("secondary-400", "#C084FC", "Medium secondary purple"),
        ("secondary-500", "#A855F7", "Base secondary purple"),
        ("secondary-600", "#9333EA", "Medium dark secondary purple"),
        ("secondary-700", "#7E22CE", "Dark secondary purple"),
        ("secondary-800", "#6B21A8", "Very dark secondary purple"),
        ("secondary-900", "#581C87", "Darkest secondary purple"),
    ]
    NEUTRAL_COLORS = [
        ("neutral-50", "#F9FAFB", "Lightest gray"),
        ("neutral-100", "#F3F4F6", "Very light gray"),
        ("neutral-200", "#E5E7EB", "Light gray"),
        ("neutral-300", "#D1D5DB", "Medium light gray"),
        ("neutral-400", "#9CA3AF", "Medium gray"),
        ("neutral-500", "#6B7280", "Base gray"),
        ("neutral-600", "#4B5563", "Medium dark gray"),
        ("neutral-700", "#374151", "Dark gray"),
        ("neutral-800", "#1F2937", "Very dark gray"),
        ("neutral-900", "#111827", "Darkest gray"),
        ("neutral-white", "#FFFFFF", "Pure white"),
        ("neutral-black", "#000000", "Pure black"),
    ]
    SEMANTIC_COLORS = [
        ("success", "#10B981", "Success green"),
        ("success-light", "#D1FAE5", "Light success background"),
        ("success-dark", "#065F46", "Dark success text"),
        ("warning", "#F59E0B", "Warning orange"),
        ("warning-light", "#FEF3C7", "Light warning background"),
        ("warning-dark", "#92400E", "Dark warning text"),
        ("error", "#EF4444", "Error red"),
        ("error-light", "#FEE2E2", "Light error background"),
        ("error-dark", "#991B1B", "Dark error text"),
        ("info", "#3B82F6", "Info blue"),
        ("info-light", "#DBEAFE", "Light info background"),
        ("info-dark", "#1E40AF", "Dark info text"),
    ]
    FONT_FAMILIES = [
        (
            "font-sans",
            'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            "System sans-serif stack",
        ),
        (
            "font-serif",
            'ui-serif, Georgia, Cambria, "Times New Roman", Times, serif',
            "System serif stack",
        ),
        (
            "font-mono",
            'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace',
            "System monospace stack",
        ),
    ]
    FONT_SIZES = [
        ("text-xs", "0.75rem", "Extra small text (12px)"),
        ("text-sm", "0.875rem", "Small text (14px)"),
        ("text-base", "1rem", "Base text size (16px)"),
        ("text-lg", "1.125rem", "Large text (18px)"),
        ("text-xl", "1.25rem", "Extra large text (20px)"),
        ("text-2xl", "1.5rem", "2X large text (24px)"),
        ("text-3xl", "1.875rem", "3X large text (30px)"),
        ("text-4xl", "2.25rem", "4X large text (36px)"),
        ("text-5xl", "3rem", "5X large text (48px)"),
        ("text-6xl", "3.75rem", "6X large text (60px)"),
    ]
    FONT_WEIGHTS = [
        ("font-thin", "100", "Thin font weight"),
        ("font-light", "300", "Light font weight"),
        ("font-normal", "400", "Normal font weight"),
        ("font-medium", "500", "Medium font weight"),
        ("font-semibold", "600", "Semibold font weight"),
        ("font-bold", "700", "Bold font weight"),
        ("font-extrabold", "800", "Extra bold font weight"),
    ]
    SPACING = [
        ("spacing-0", "0rem", "No spacing (0px)"),
        ("spacing-px", "1px", "1 pixel"),
        ("spacing-0-5", "0.125rem", "0.5 spacing unit (2px)"),
        ("spacing-1", "0.25rem", "1 spacing unit (4px)"),
        ("spacing-1-5", "0.375rem", "1.5 spacing units (6px)"),
        ("spacing-2", "0.5rem", "2 spacing units (8px)"),
        ("spacing-2-5", "0.625rem", "2.5 spacing units (10px)"),
        ("spacing-3", "0.75rem", "3 spacing units (12px)"),
        ("spacing-3-5", "0.875rem", "3.5 spacing units (14px)"),
        ("spacing-4", "1rem", "4 spacing units (16px)"),
        ("spacing-5", "1.25rem", "5 spacing units (20px)"),
        ("spacing-6", "1.5rem", "6 spacing units (24px)"),
        ("spacing-7", "1.75rem", "7 spacing units (28px)"),
        ("spacing-8", "2rem", "8 spacing units (32px)"),
        ("spacing-9", "2.25rem", "9 spacing units (36px)"),
        ("spacing-10", "2.5rem", "10 spacing units (40px)"),
        ("spacing-11", "2.75rem", "11 spacing units (44px)"),
        ("spacing-12", "3rem", "12 spacing units (48px)"),
        ("spacing-14", "3.5rem", "14 spacing units (56px)"),
        ("spacing-16", "4rem", "16 spacing units (64px)"),
        ("spacing-20", "5rem", "20 spacing units (80px)"),
        ("spacing-24", "6rem", "24 spacing units (96px)"),
    ]
    BORDER_RADIUS = [
        ("rounded-none", "0px", "No border radius"),
        ("rounded-sm", "0.125rem", "Small border radius (2px)"),
        ("rounded", "0.25rem", "Default border radius (4px)"),
        ("rounded-md", "0.375rem", "Medium border radius (6px)"),
        ("rounded-lg", "0.5rem", "Large border radius (8px)"),
        ("rounded-xl", "0.75rem", "Extra large border radius (12px)"),
        ("rounded-2xl", "1rem", "2X large border radius (16px)"),
        ("rounded-3xl", "1.5rem", "3X large border radius (24px)"),
        ("rounded-full", "9999px", "Fully rounded (circular)"),
    ]
    BORDER_WIDTHS = [
        ("border-0", "0px", "No border"),
        ("border", "1px", "Default border (1px)"),
        ("border-2", "2px", "2px border"),
        ("border-4", "4px", "4px border"),
        ("border-8", "8px", "8px border"),
    ]
    SHADOWS = [
        ("shadow-none", "none", "No shadow"),
        ("shadow-sm", "0 1px 2px 0 rgb(0 0 0 / 0.05)", "Small shadow"),
        (
            "shadow",
            "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
            "Default shadow",
        ),
        (
            "shadow-md",
            "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
            "Medium shadow",
        ),
        (
            "shadow-lg",
            "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
            "Large shadow",
        ),
        (
            "shadow-xl",
            "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
            "Extra large shadow",
        ),
        ("shadow-2xl", "0 25px 50px -12px rgb(0 0 0 / 0.25)", "2X large shadow"),
        ("shadow-inner", "inset 0 2px 4px 0 rgb(0 0 0 / 0.05)", "Inner shadow"),
    ]
    BREAKPOINTS = [
        ("breakpoint-sm", "640px", "Small screen breakpoint"),
        ("breakpoint-md", "768px", "Medium screen breakpoint"),
        ("breakpoint-lg", "1024px", "Large screen breakpoint"),
        ("breakpoint-xl", "1280px", "Extra large screen breakpoint"),
        ("breakpoint-2xl", "1536px", "2X large screen breakpoint"),
    ]

    TOKEN_GROUPS = [
        ("color", PRIMARY_COLORS + SECONDARY_COLORS + NEUTRAL_COLORS + SEMANTIC_COLORS),
        ("font", FONT_FAMILIES + FONT_SIZES + FONT_WEIGHTS),
        ("spacing", SPACING),
        ("border", BORDER_RADIUS + BORDER_WIDTHS),
        ("shadow", SHADOWS),
        ("breakpoint", BREAKPOINTS),
    ]

    def seed(self) -> int:
        from design.models import DesignToken

        count = 0
        for token_type, tokens in self.TOKEN_GROUPS:
            for name, value, description in tokens:
                _, created = DesignToken.objects.update_or_create(
                    name=name,
                    source="system",
                    defaults={
                        "token_type": token_type,
                        "value": value,
                        "description": description,
                        "priority_level": 4,
                        "tier_restriction": [],
                        "is_active": True,
                    },
                )
                if created:
                    count += 1
        return count
