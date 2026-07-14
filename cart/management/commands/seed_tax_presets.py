from decimal import Decimal

from core.management.commands._seed_base import SeedCommand

PRESET_GROUPS = [
    {
        "key": "eu_vat",
        "name": "EU VAT Rates",
        "description": "Standard VAT rates for all 27 EU member states. Updated Feb 2026.",
        "icon": "fas fa-euro-sign",
        "tax_type": "vat",
        "region": "europe",
    },
    {
        "key": "europe_other_vat",
        "name": "Other European VAT",
        "description": "VAT rates for non-EU European countries including Norway, Switzerland, UK, Turkey, and others.",
        "icon": "fas fa-globe-europe",
        "tax_type": "vat",
        "region": "europe",
    },
    {
        "key": "us_sales_tax",
        "name": "US State Sales Tax",
        "description": "Base state sales tax rates for all 50 US states plus DC. Note: local/city taxes may apply on top.",
        "icon": "fas fa-flag-usa",
        "tax_type": "sales_tax",
        "region": "north_america",
    },
    {
        "key": "ca_gst_hst",
        "name": "Canadian GST/HST",
        "description": "Combined federal and provincial tax rates for all Canadian provinces and territories.",
        "icon": "fas fa-leaf",
        "tax_type": "gst",
        "region": "north_america",
    },
    {
        "key": "asia_pacific",
        "name": "Asia-Pacific VAT/GST",
        "description": "Standard VAT, GST, and consumption tax rates for Asia-Pacific countries.",
        "icon": "fas fa-globe-asia",
        "tax_type": "vat",
        "region": "asia_pacific",
    },
    {
        "key": "middle_east",
        "name": "Middle East VAT",
        "description": "VAT rates for Middle Eastern countries including GCC states.",
        "icon": "fas fa-mosque",
        "tax_type": "vat",
        "region": "middle_east",
    },
    {
        "key": "africa_vat",
        "name": "Africa VAT",
        "description": "Standard VAT rates for African countries.",
        "icon": "fas fa-globe-africa",
        "tax_type": "vat",
        "region": "africa",
    },
    {
        "key": "latin_america",
        "name": "Latin America VAT",
        "description": "Standard VAT/IVA rates for Latin American and Caribbean countries.",
        "icon": "fas fa-globe-americas",
        "tax_type": "vat",
        "region": "latin_america",
    },
    {
        "key": "oceania",
        "name": "Oceania GST/VAT",
        "description": "GST and VAT rates for Oceania including Australia, New Zealand, and Pacific Islands.",
        "icon": "fas fa-water",
        "tax_type": "gst",
        "region": "oceania",
    },
    {
        "key": "central_asia",
        "name": "Central Asia VAT",
        "description": "VAT rates for Central Asian countries.",
        "icon": "fas fa-mountain",
        "tax_type": "vat",
        "region": "asia_pacific",
    },
    # From migration 0016
    {
        "key": "uk_vat",
        "name": "UK VAT",
        "description": "Standard VAT rate for the United Kingdom (20%).",
        "icon": "fas fa-sterling-sign",
        "tax_type": "vat",
        "region": "europe",
    },
]


# Format: (country_code, country_name, state_code, state_name, rate, tax_type, notes)
PRESET_RATES = {
    # ==========================================
    # EU VAT RATES (27 countries)
    # ==========================================
    "eu_vat": [
        ("AT", "Austria", "", "", Decimal("0.2000"), "vat", ""),
        ("BE", "Belgium", "", "", Decimal("0.2100"), "vat", ""),
        ("BG", "Bulgaria", "", "", Decimal("0.2000"), "vat", ""),
        ("HR", "Croatia", "", "", Decimal("0.2500"), "vat", ""),
        ("CY", "Cyprus", "", "", Decimal("0.1900"), "vat", ""),
        ("CZ", "Czech Republic", "", "", Decimal("0.2100"), "vat", ""),
        ("DK", "Denmark", "", "", Decimal("0.2500"), "vat", ""),
        ("EE", "Estonia", "", "", Decimal("0.2400"), "vat", "Raised from 22% in July 2025"),
        ("FI", "Finland", "", "", Decimal("0.2550"), "vat", "Raised from 24% in September 2024"),
        ("FR", "France", "", "", Decimal("0.2000"), "vat", ""),
        ("DE", "Germany", "", "", Decimal("0.1900"), "vat", ""),
        ("GR", "Greece", "", "", Decimal("0.2400"), "vat", ""),
        ("HU", "Hungary", "", "", Decimal("0.2700"), "vat", "Highest standard VAT in the world"),
        ("IE", "Ireland", "", "", Decimal("0.2300"), "vat", ""),
        ("IT", "Italy", "", "", Decimal("0.2200"), "vat", ""),
        ("LV", "Latvia", "", "", Decimal("0.2100"), "vat", ""),
        ("LT", "Lithuania", "", "", Decimal("0.2100"), "vat", ""),
        ("LU", "Luxembourg", "", "", Decimal("0.1700"), "vat", ""),
        ("MT", "Malta", "", "", Decimal("0.1800"), "vat", ""),
        ("NL", "Netherlands", "", "", Decimal("0.2100"), "vat", ""),
        ("PL", "Poland", "", "", Decimal("0.2300"), "vat", ""),
        ("PT", "Portugal", "", "", Decimal("0.2300"), "vat", ""),
        ("RO", "Romania", "", "", Decimal("0.2100"), "vat", "Raised from 19% in August 2025"),
        ("SK", "Slovakia", "", "", Decimal("0.2300"), "vat", "Raised from 20% in January 2025"),
        ("SI", "Slovenia", "", "", Decimal("0.2200"), "vat", ""),
        ("ES", "Spain", "", "", Decimal("0.2100"), "vat", ""),
        ("SE", "Sweden", "", "", Decimal("0.2500"), "vat", ""),
    ],
    # ==========================================
    # OTHER EUROPEAN VAT (non-EU)
    # ==========================================
    "europe_other_vat": [
        ("GB", "United Kingdom", "", "", Decimal("0.2000"), "vat", ""),
        ("NO", "Norway", "", "", Decimal("0.2500"), "vat", ""),
        ("CH", "Switzerland", "", "", Decimal("0.0810"), "vat", "Lowest in Europe"),
        ("LI", "Liechtenstein", "", "", Decimal("0.0810"), "vat", "Same rate as Switzerland"),
        ("IS", "Iceland", "", "", Decimal("0.2400"), "vat", ""),
        ("TR", "Turkey", "", "", Decimal("0.2000"), "vat", ""),
        ("RS", "Serbia", "", "", Decimal("0.2000"), "vat", ""),
        ("UA", "Ukraine", "", "", Decimal("0.2000"), "vat", ""),
        ("RU", "Russia", "", "", Decimal("0.2200"), "vat", "Raised from 20% in January 2026"),
        ("BY", "Belarus", "", "", Decimal("0.2000"), "vat", ""),
        ("GE", "Georgia", "", "", Decimal("0.1800"), "vat", ""),
        ("AM", "Armenia", "", "", Decimal("0.2000"), "vat", ""),
        ("AZ", "Azerbaijan", "", "", Decimal("0.1800"), "vat", ""),
        ("MD", "Moldova", "", "", Decimal("0.2000"), "vat", ""),
        ("MK", "North Macedonia", "", "", Decimal("0.1800"), "vat", ""),
        ("AL", "Albania", "", "", Decimal("0.2000"), "vat", ""),
        ("BA", "Bosnia & Herzegovina", "", "", Decimal("0.1700"), "vat", ""),
        ("ME", "Montenegro", "", "", Decimal("0.2100"), "vat", ""),
        ("XK", "Kosovo", "", "", Decimal("0.1800"), "vat", ""),
        ("AD", "Andorra", "", "", Decimal("0.0450"), "vat", "Lowest VAT in the world"),
        ("FO", "Faroe Islands", "", "", Decimal("0.2500"), "vat", ""),
    ],
    # ==========================================
    # US STATE SALES TAX (50 states + DC)
    # ==========================================
    "us_sales_tax": [
        ("US", "United States", "AL", "Alabama", Decimal("0.0400"), "sales_tax", ""),
        (
            "US",
            "United States",
            "AK",
            "Alaska",
            Decimal("0.0000"),
            "sales_tax",
            "No state sales tax; local taxes may apply",
        ),
        ("US", "United States", "AZ", "Arizona", Decimal("0.0560"), "sales_tax", ""),
        ("US", "United States", "AR", "Arkansas", Decimal("0.0650"), "sales_tax", ""),
        ("US", "United States", "CA", "California", Decimal("0.0725"), "sales_tax", ""),
        ("US", "United States", "CO", "Colorado", Decimal("0.0290"), "sales_tax", ""),
        ("US", "United States", "CT", "Connecticut", Decimal("0.0635"), "sales_tax", ""),
        (
            "US",
            "United States",
            "DE",
            "Delaware",
            Decimal("0.0000"),
            "sales_tax",
            "No state sales tax",
        ),
        ("US", "United States", "DC", "District of Columbia", Decimal("0.0600"), "sales_tax", ""),
        ("US", "United States", "FL", "Florida", Decimal("0.0600"), "sales_tax", ""),
        ("US", "United States", "GA", "Georgia", Decimal("0.0400"), "sales_tax", ""),
        (
            "US",
            "United States",
            "HI",
            "Hawaii",
            Decimal("0.0400"),
            "sales_tax",
            "General Excise Tax",
        ),
        ("US", "United States", "ID", "Idaho", Decimal("0.0600"), "sales_tax", ""),
        ("US", "United States", "IL", "Illinois", Decimal("0.0625"), "sales_tax", ""),
        ("US", "United States", "IN", "Indiana", Decimal("0.0700"), "sales_tax", ""),
        ("US", "United States", "IA", "Iowa", Decimal("0.0600"), "sales_tax", ""),
        ("US", "United States", "KS", "Kansas", Decimal("0.0650"), "sales_tax", ""),
        ("US", "United States", "KY", "Kentucky", Decimal("0.0600"), "sales_tax", ""),
        (
            "US",
            "United States",
            "LA",
            "Louisiana",
            Decimal("0.0500"),
            "sales_tax",
            "Raised from 4.45% in January 2025",
        ),
        ("US", "United States", "ME", "Maine", Decimal("0.0550"), "sales_tax", ""),
        ("US", "United States", "MD", "Maryland", Decimal("0.0600"), "sales_tax", ""),
        ("US", "United States", "MA", "Massachusetts", Decimal("0.0625"), "sales_tax", ""),
        ("US", "United States", "MI", "Michigan", Decimal("0.0600"), "sales_tax", ""),
        ("US", "United States", "MN", "Minnesota", Decimal("0.06875"), "sales_tax", ""),
        ("US", "United States", "MS", "Mississippi", Decimal("0.0700"), "sales_tax", ""),
        ("US", "United States", "MO", "Missouri", Decimal("0.04225"), "sales_tax", ""),
        (
            "US",
            "United States",
            "MT",
            "Montana",
            Decimal("0.0000"),
            "sales_tax",
            "No state sales tax",
        ),
        ("US", "United States", "NE", "Nebraska", Decimal("0.0550"), "sales_tax", ""),
        ("US", "United States", "NV", "Nevada", Decimal("0.0460"), "sales_tax", ""),
        (
            "US",
            "United States",
            "NH",
            "New Hampshire",
            Decimal("0.0000"),
            "sales_tax",
            "No state sales tax",
        ),
        ("US", "United States", "NJ", "New Jersey", Decimal("0.06625"), "sales_tax", ""),
        ("US", "United States", "NM", "New Mexico", Decimal("0.05125"), "sales_tax", ""),
        ("US", "United States", "NY", "New York", Decimal("0.0400"), "sales_tax", ""),
        ("US", "United States", "NC", "North Carolina", Decimal("0.0475"), "sales_tax", ""),
        ("US", "United States", "ND", "North Dakota", Decimal("0.0500"), "sales_tax", ""),
        ("US", "United States", "OH", "Ohio", Decimal("0.0575"), "sales_tax", ""),
        ("US", "United States", "OK", "Oklahoma", Decimal("0.0450"), "sales_tax", ""),
        (
            "US",
            "United States",
            "OR",
            "Oregon",
            Decimal("0.0000"),
            "sales_tax",
            "No state sales tax",
        ),
        ("US", "United States", "PA", "Pennsylvania", Decimal("0.0600"), "sales_tax", ""),
        ("US", "United States", "RI", "Rhode Island", Decimal("0.0700"), "sales_tax", ""),
        ("US", "United States", "SC", "South Carolina", Decimal("0.0600"), "sales_tax", ""),
        ("US", "United States", "SD", "South Dakota", Decimal("0.0450"), "sales_tax", ""),
        ("US", "United States", "TN", "Tennessee", Decimal("0.0700"), "sales_tax", ""),
        ("US", "United States", "TX", "Texas", Decimal("0.0625"), "sales_tax", ""),
        ("US", "United States", "UT", "Utah", Decimal("0.0470"), "sales_tax", ""),
        ("US", "United States", "VT", "Vermont", Decimal("0.0600"), "sales_tax", ""),
        ("US", "United States", "VA", "Virginia", Decimal("0.0430"), "sales_tax", ""),
        ("US", "United States", "WA", "Washington", Decimal("0.0650"), "sales_tax", ""),
        ("US", "United States", "WV", "West Virginia", Decimal("0.0600"), "sales_tax", ""),
        ("US", "United States", "WI", "Wisconsin", Decimal("0.0500"), "sales_tax", ""),
        ("US", "United States", "WY", "Wyoming", Decimal("0.0400"), "sales_tax", ""),
    ],
    # ==========================================
    # CANADIAN GST/HST (13 provinces/territories)
    # ==========================================
    "ca_gst_hst": [
        ("CA", "Canada", "AB", "Alberta", Decimal("0.0500"), "gst", "GST only"),
        ("CA", "Canada", "BC", "British Columbia", Decimal("0.1200"), "gst", "GST 5% + PST 7%"),
        ("CA", "Canada", "MB", "Manitoba", Decimal("0.1300"), "gst", "GST 5% + RST 8%"),
        ("CA", "Canada", "NB", "New Brunswick", Decimal("0.1500"), "gst", "HST"),
        ("CA", "Canada", "NL", "Newfoundland & Labrador", Decimal("0.1500"), "gst", "HST"),
        (
            "CA",
            "Canada",
            "NS",
            "Nova Scotia",
            Decimal("0.1400"),
            "gst",
            "HST - Reduced from 15% in April 2025",
        ),
        ("CA", "Canada", "NT", "Northwest Territories", Decimal("0.0500"), "gst", "GST only"),
        ("CA", "Canada", "NU", "Nunavut", Decimal("0.0500"), "gst", "GST only"),
        ("CA", "Canada", "ON", "Ontario", Decimal("0.1300"), "gst", "HST"),
        ("CA", "Canada", "PE", "Prince Edward Island", Decimal("0.1500"), "gst", "HST"),
        ("CA", "Canada", "QC", "Quebec", Decimal("0.14975"), "gst", "GST 5% + QST 9.975%"),
        ("CA", "Canada", "SK", "Saskatchewan", Decimal("0.1100"), "gst", "GST 5% + PST 6%"),
        ("CA", "Canada", "YT", "Yukon", Decimal("0.0500"), "gst", "GST only"),
    ],
    # ==========================================
    # ASIA-PACIFIC (24 countries)
    # ==========================================
    "asia_pacific": [
        (
            "JP",
            "Japan",
            "",
            "",
            Decimal("0.1000"),
            "vat",
            "Consumption tax; 8% reduced rate on food",
        ),
        ("KR", "South Korea", "", "", Decimal("0.1000"), "vat", ""),
        ("CN", "China", "", "", Decimal("0.1300"), "vat", "Standard rate; also 9% and 6% reduced"),
        ("IN", "India", "", "", Decimal("0.1800"), "gst", "Standard rate; also 5%, 12%, 28% slabs"),
        ("AU", "Australia", "", "", Decimal("0.1000"), "gst", ""),
        ("NZ", "New Zealand", "", "", Decimal("0.1500"), "gst", ""),
        ("SG", "Singapore", "", "", Decimal("0.0900"), "gst", "Raised from 8% in January 2024"),
        ("MY", "Malaysia", "", "", Decimal("0.1000"), "sales_tax", "SST; service tax 6-8%"),
        ("TH", "Thailand", "", "", Decimal("0.0700"), "vat", "Legal rate 10%, temporarily reduced"),
        ("PH", "Philippines", "", "", Decimal("0.1200"), "vat", ""),
        ("ID", "Indonesia", "", "", Decimal("0.1100"), "vat", "12% on luxury goods from Jan 2025"),
        ("VN", "Vietnam", "", "", Decimal("0.1000"), "vat", "Also 5% reduced rate"),
        ("TW", "Taiwan", "", "", Decimal("0.0500"), "vat", ""),
        ("HK", "Hong Kong", "", "", Decimal("0.0000"), "vat", "No VAT/GST/sales tax"),
        ("KH", "Cambodia", "", "", Decimal("0.1000"), "vat", ""),
        ("LA", "Laos", "", "", Decimal("0.1000"), "vat", ""),
        ("MM", "Myanmar", "", "", Decimal("0.0500"), "vat", "Commercial tax"),
        ("MN", "Mongolia", "", "", Decimal("0.1000"), "vat", ""),
        ("BD", "Bangladesh", "", "", Decimal("0.1500"), "vat", ""),
        ("PK", "Pakistan", "", "", Decimal("0.1800"), "gst", ""),
        ("LK", "Sri Lanka", "", "", Decimal("0.1800"), "vat", ""),
        ("NP", "Nepal", "", "", Decimal("0.1300"), "vat", ""),
        ("MV", "Maldives", "", "", Decimal("0.0800"), "gst", ""),
        ("BT", "Bhutan", "", "", Decimal("0.0700"), "vat", "Introduced January 2026"),
    ],
    # ==========================================
    # MIDDLE EAST (9 countries)
    # ==========================================
    "middle_east": [
        ("AE", "United Arab Emirates", "", "", Decimal("0.0500"), "vat", "Introduced 2018"),
        ("SA", "Saudi Arabia", "", "", Decimal("0.1500"), "vat", "Raised from 5% in July 2020"),
        ("BH", "Bahrain", "", "", Decimal("0.1000"), "vat", "Raised from 5% in January 2022"),
        ("OM", "Oman", "", "", Decimal("0.0500"), "vat", "Introduced April 2021"),
        ("QA", "Qatar", "", "", Decimal("0.0000"), "vat", "No VAT (excise tax only)"),
        ("KW", "Kuwait", "", "", Decimal("0.0000"), "vat", "No VAT yet"),
        ("JO", "Jordan", "", "", Decimal("0.1600"), "gst", ""),
        ("IL", "Israel", "", "", Decimal("0.1700"), "vat", ""),
        ("LB", "Lebanon", "", "", Decimal("0.1100"), "vat", ""),
    ],
    # ==========================================
    # AFRICA (25 countries)
    # ==========================================
    "africa_vat": [
        ("ZA", "South Africa", "", "", Decimal("0.1500"), "vat", ""),
        ("KE", "Kenya", "", "", Decimal("0.1600"), "vat", ""),
        ("NG", "Nigeria", "", "", Decimal("0.0750"), "vat", ""),
        ("EG", "Egypt", "", "", Decimal("0.1400"), "vat", ""),
        ("MA", "Morocco", "", "", Decimal("0.2000"), "vat", ""),
        ("GH", "Ghana", "", "", Decimal("0.1500"), "vat", ""),
        ("TZ", "Tanzania", "", "", Decimal("0.1800"), "vat", ""),
        ("UG", "Uganda", "", "", Decimal("0.1800"), "vat", ""),
        ("RW", "Rwanda", "", "", Decimal("0.1800"), "vat", ""),
        ("ET", "Ethiopia", "", "", Decimal("0.1500"), "vat", ""),
        ("BW", "Botswana", "", "", Decimal("0.1400"), "vat", ""),
        ("ZM", "Zambia", "", "", Decimal("0.1600"), "vat", ""),
        ("MZ", "Mozambique", "", "", Decimal("0.1600"), "vat", ""),
        ("AO", "Angola", "", "", Decimal("0.1400"), "vat", ""),
        ("CM", "Cameroon", "", "", Decimal("0.1925"), "vat", ""),
        ("DZ", "Algeria", "", "", Decimal("0.1900"), "vat", ""),
        ("TN", "Tunisia", "", "", Decimal("0.1900"), "vat", ""),
        ("SN", "Senegal", "", "", Decimal("0.1800"), "vat", ""),
        ("CI", "Ivory Coast", "", "", Decimal("0.1800"), "vat", ""),
        ("CD", "DR Congo", "", "", Decimal("0.1600"), "vat", ""),
        ("MU", "Mauritius", "", "", Decimal("0.1500"), "vat", ""),
        ("NA", "Namibia", "", "", Decimal("0.1500"), "vat", ""),
        ("ZW", "Zimbabwe", "", "", Decimal("0.1500"), "vat", ""),
        ("MW", "Malawi", "", "", Decimal("0.1650"), "vat", ""),
        ("MG", "Madagascar", "", "", Decimal("0.2000"), "vat", ""),
    ],
    # ==========================================
    # LATIN AMERICA (22 countries)
    # ==========================================
    "latin_america": [
        ("BR", "Brazil", "", "", Decimal("0.1700"), "vat", "ICMS varies 17-20% by state"),
        ("MX", "Mexico", "", "", Decimal("0.1600"), "vat", "IVA"),
        ("AR", "Argentina", "", "", Decimal("0.2100"), "vat", "IVA"),
        ("CO", "Colombia", "", "", Decimal("0.1900"), "vat", "IVA"),
        ("CL", "Chile", "", "", Decimal("0.1900"), "vat", "IVA"),
        ("PE", "Peru", "", "", Decimal("0.1800"), "vat", "IGV (16% + 2% municipal)"),
        ("UY", "Uruguay", "", "", Decimal("0.2200"), "vat", "IVA - highest in Latin America"),
        ("EC", "Ecuador", "", "", Decimal("0.1200"), "vat", "IVA"),
        ("BO", "Bolivia", "", "", Decimal("0.1300"), "vat", "IVA"),
        ("PY", "Paraguay", "", "", Decimal("0.1000"), "vat", "IVA"),
        ("VE", "Venezuela", "", "", Decimal("0.1600"), "vat", "IVA"),
        ("GT", "Guatemala", "", "", Decimal("0.1200"), "vat", "IVA"),
        ("CR", "Costa Rica", "", "", Decimal("0.1300"), "vat", "IVA"),
        ("PA", "Panama", "", "", Decimal("0.0700"), "vat", "ITBMS"),
        ("DO", "Dominican Republic", "", "", Decimal("0.1800"), "vat", "ITBIS"),
        ("SV", "El Salvador", "", "", Decimal("0.1300"), "vat", "IVA"),
        ("HN", "Honduras", "", "", Decimal("0.1500"), "vat", "ISV"),
        ("NI", "Nicaragua", "", "", Decimal("0.1500"), "vat", "IVA"),
        ("JM", "Jamaica", "", "", Decimal("0.1500"), "gst", "General Consumption Tax"),
        ("TT", "Trinidad & Tobago", "", "", Decimal("0.1250"), "vat", ""),
        ("BB", "Barbados", "", "", Decimal("0.1750"), "vat", ""),
        ("LC", "Saint Lucia", "", "", Decimal("0.1250"), "vat", ""),
    ],
    # ==========================================
    # OCEANIA (5 countries)
    # ==========================================
    "oceania": [
        ("AU", "Australia", "", "", Decimal("0.1000"), "gst", "Basic food exempt"),
        ("NZ", "New Zealand", "", "", Decimal("0.1500"), "gst", ""),
        ("PG", "Papua New Guinea", "", "", Decimal("0.1000"), "gst", ""),
        ("FJ", "Fiji", "", "", Decimal("0.1500"), "vat", ""),
        ("VU", "Vanuatu", "", "", Decimal("0.1500"), "vat", ""),
    ],
    # ==========================================
    # CENTRAL ASIA (6 countries)
    # ==========================================
    "central_asia": [
        ("KZ", "Kazakhstan", "", "", Decimal("0.1200"), "vat", ""),
        ("UZ", "Uzbekistan", "", "", Decimal("0.1200"), "vat", ""),
        ("KG", "Kyrgyzstan", "", "", Decimal("0.1200"), "vat", ""),
        ("TJ", "Tajikistan", "", "", Decimal("0.1400"), "vat", ""),
        ("TM", "Turkmenistan", "", "", Decimal("0.1500"), "vat", ""),
        ("PR", "Puerto Rico", "", "", Decimal("0.1150"), "sales_tax", "US territory"),
    ],
    # ==========================================
    # UK VAT (from migration 0016)
    # ==========================================
    "uk_vat": [
        ("GB", "United Kingdom", "", "", Decimal("0.2000"), "vat", ""),
    ],
}


class Command(SeedCommand):
    seed_name = "tax_presets"
    seed_version = 1
    help = "Seed tax preset groups and rates for all major regions"

    def seed(self) -> int:
        from cart.models import TaxPresetGroup, TaxPresetRate

        created_count = 0

        for group_data in PRESET_GROUPS:
            group_key = group_data["key"]
            group, group_created = TaxPresetGroup.objects.get_or_create(
                key=group_key,
                defaults={
                    "name": group_data["name"],
                    "description": group_data["description"],
                    "icon": group_data["icon"],
                    "tax_type": group_data["tax_type"],
                    "region": group_data["region"],
                },
            )
            if group_created:
                created_count += 1

            rates = PRESET_RATES.get(group_key, [])
            for country_code, country_name, state_code, state_name, rate, tax_type, notes in rates:
                _, rate_created = TaxPresetRate.objects.get_or_create(
                    group=group,
                    country=country_code,
                    state=state_code,
                    defaults={
                        "country_name": country_name,
                        "state_name": state_name,
                        "rate": rate,
                        "tax_type": tax_type,
                        "notes": notes,
                    },
                )
                if rate_created:
                    created_count += 1

        return created_count
