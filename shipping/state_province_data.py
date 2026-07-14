"""
State/Province/Region Data for Zone Wizard

Hybrid approach:
- Curated high-quality data for major countries (manually maintained)
- Automatic fallback to pycountry library for global coverage (~250 countries)

Our curated data provides better translations and common names for high-traffic countries.
All other countries automatically use ISO 3166-2 subdivision data from pycountry.

Format: {
    'COUNTRY_CODE': {
        'STATE_CODE': 'State Name',
        ...
    }
}
"""

from django.utils.translation import gettext_lazy as _

try:
    import pycountry

    PYCOUNTRY_AVAILABLE = True
except ImportError:
    PYCOUNTRY_AVAILABLE = False

# ==============================================================================
# CURATED STATE/PROVINCE DATA
# High-quality, manually maintained data for major countries with good translations
# ==============================================================================

STATES_BY_COUNTRY = {
    "US": {  # United States
        "AL": _("Alabama"),
        "AK": _("Alaska"),
        "AZ": _("Arizona"),
        "AR": _("Arkansas"),
        "CA": _("California"),
        "CO": _("Colorado"),
        "CT": _("Connecticut"),
        "DE": _("Delaware"),
        "FL": _("Florida"),
        "GA": _("Georgia"),
        "HI": _("Hawaii"),
        "ID": _("Idaho"),
        "IL": _("Illinois"),
        "IN": _("Indiana"),
        "IA": _("Iowa"),
        "KS": _("Kansas"),
        "KY": _("Kentucky"),
        "LA": _("Louisiana"),
        "ME": _("Maine"),
        "MD": _("Maryland"),
        "MA": _("Massachusetts"),
        "MI": _("Michigan"),
        "MN": _("Minnesota"),
        "MS": _("Mississippi"),
        "MO": _("Missouri"),
        "MT": _("Montana"),
        "NE": _("Nebraska"),
        "NV": _("Nevada"),
        "NH": _("New Hampshire"),
        "NJ": _("New Jersey"),
        "NM": _("New Mexico"),
        "NY": _("New York"),
        "NC": _("North Carolina"),
        "ND": _("North Dakota"),
        "OH": _("Ohio"),
        "OK": _("Oklahoma"),
        "OR": _("Oregon"),
        "PA": _("Pennsylvania"),
        "RI": _("Rhode Island"),
        "SC": _("South Carolina"),
        "SD": _("South Dakota"),
        "TN": _("Tennessee"),
        "TX": _("Texas"),
        "UT": _("Utah"),
        "VT": _("Vermont"),
        "VA": _("Virginia"),
        "WA": _("Washington"),
        "WV": _("West Virginia"),
        "WI": _("Wisconsin"),
        "WY": _("Wyoming"),
        "DC": _("District of Columbia"),
        "AS": _("American Samoa"),
        "GU": _("Guam"),
        "MP": _("Northern Mariana Islands"),
        "PR": _("Puerto Rico"),
        "VI": _("U.S. Virgin Islands"),
    },
    "CA": {  # Canada
        "AB": _("Alberta"),
        "BC": _("British Columbia"),
        "MB": _("Manitoba"),
        "NB": _("New Brunswick"),
        "NL": _("Newfoundland and Labrador"),
        "NS": _("Nova Scotia"),
        "ON": _("Ontario"),
        "PE": _("Prince Edward Island"),
        "QC": _("Quebec"),
        "SK": _("Saskatchewan"),
        "NT": _("Northwest Territories"),
        "NU": _("Nunavut"),
        "YT": _("Yukon"),
    },
    "AU": {  # Australia
        "ACT": _("Australian Capital Territory"),
        "NSW": _("New South Wales"),
        "NT": _("Northern Territory"),
        "QLD": _("Queensland"),
        "SA": _("South Australia"),
        "TAS": _("Tasmania"),
        "VIC": _("Victoria"),
        "WA": _("Western Australia"),
    },
    "GB": {  # United Kingdom
        "ENG": _("England"),
        "SCT": _("Scotland"),
        "WLS": _("Wales"),
        "NIR": _("Northern Ireland"),
    },
    "DE": {  # Germany
        "BW": _("Baden-Württemberg"),
        "BY": _("Bavaria"),
        "BE": _("Berlin"),
        "BB": _("Brandenburg"),
        "HB": _("Bremen"),
        "HH": _("Hamburg"),
        "HE": _("Hesse"),
        "MV": _("Mecklenburg-Vorpommern"),
        "NI": _("Lower Saxony"),
        "NW": _("North Rhine-Westphalia"),
        "RP": _("Rhineland-Palatinate"),
        "SL": _("Saarland"),
        "SN": _("Saxony"),
        "ST": _("Saxony-Anhalt"),
        "SH": _("Schleswig-Holstein"),
        "TH": _("Thuringia"),
    },
    "FR": {  # France
        "ARA": _("Auvergne-Rhône-Alpes"),
        "BFC": _("Bourgogne-Franche-Comté"),
        "BRE": _("Brittany"),
        "CVL": _("Centre-Val de Loire"),
        "COR": _("Corsica"),
        "GES": _("Grand Est"),
        "HDF": _("Hauts-de-France"),
        "IDF": _("Île-de-France"),
        "NOR": _("Normandy"),
        "NAQ": _("Nouvelle-Aquitaine"),
        "OCC": _("Occitanie"),
        "PDL": _("Pays de la Loire"),
        "PAC": _("Provence-Alpes-Côte d'Azur"),
    },
    "IT": {  # Italy
        "ABR": _("Abruzzo"),
        "BAS": _("Basilicata"),
        "CAL": _("Calabria"),
        "CAM": _("Campania"),
        "EMR": _("Emilia-Romagna"),
        "FVG": _("Friuli-Venezia Giulia"),
        "LAZ": _("Lazio"),
        "LIG": _("Liguria"),
        "LOM": _("Lombardy"),
        "MAR": _("Marche"),
        "MOL": _("Molise"),
        "PMN": _("Piedmont"),
        "PUG": _("Apulia"),
        "SAR": _("Sardinia"),
        "SIC": _("Sicily"),
        "TOS": _("Tuscany"),
        "TAA": _("Trentino-South Tyrol"),
        "UMB": _("Umbria"),
        "VDA": _("Aosta Valley"),
        "VEN": _("Veneto"),
    },
    "ES": {  # Spain
        "AN": _("Andalusia"),
        "AR": _("Aragon"),
        "AS": _("Asturias"),
        "IB": _("Balearic Islands"),
        "CN": _("Canary Islands"),
        "CB": _("Cantabria"),
        "CL": _("Castile and León"),
        "CM": _("Castile-La Mancha"),
        "CT": _("Catalonia"),
        "EX": _("Extremadura"),
        "GA": _("Galicia"),
        "MD": _("Madrid"),
        "MC": _("Murcia"),
        "NC": _("Navarre"),
        "PV": _("Basque Country"),
        "RI": _("La Rioja"),
        "VC": _("Valencia"),
    },
    "IN": {  # India
        "AN": _("Andaman and Nicobar Islands"),
        "AP": _("Andhra Pradesh"),
        "AR": _("Arunachal Pradesh"),
        "AS": _("Assam"),
        "BR": _("Bihar"),
        "CH": _("Chandigarh"),
        "CT": _("Chhattisgarh"),
        "DN": _("Dadra and Nagar Haveli and Daman and Diu"),
        "DL": _("Delhi"),
        "GA": _("Goa"),
        "GJ": _("Gujarat"),
        "HR": _("Haryana"),
        "HP": _("Himachal Pradesh"),
        "JK": _("Jammu and Kashmir"),
        "JH": _("Jharkhand"),
        "KA": _("Karnataka"),
        "KL": _("Kerala"),
        "LA": _("Ladakh"),
        "LD": _("Lakshadweep"),
        "MP": _("Madhya Pradesh"),
        "MH": _("Maharashtra"),
        "MN": _("Manipur"),
        "ML": _("Meghalaya"),
        "MZ": _("Mizoram"),
        "NL": _("Nagaland"),
        "OR": _("Odisha"),
        "PY": _("Puducherry"),
        "PB": _("Punjab"),
        "RJ": _("Rajasthan"),
        "SK": _("Sikkim"),
        "TN": _("Tamil Nadu"),
        "TG": _("Telangana"),
        "TR": _("Tripura"),
        "UP": _("Uttar Pradesh"),
        "UT": _("Uttarakhand"),
        "WB": _("West Bengal"),
    },
    "CN": {  # China
        "AH": _("Anhui"),
        "BJ": _("Beijing"),
        "CQ": _("Chongqing"),
        "FJ": _("Fujian"),
        "GS": _("Gansu"),
        "GD": _("Guangdong"),
        "GX": _("Guangxi"),
        "GZ": _("Guizhou"),
        "HI": _("Hainan"),
        "HE": _("Hebei"),
        "HL": _("Heilongjiang"),
        "HA": _("Henan"),
        "HB": _("Hubei"),
        "HN": _("Hunan"),
        "JS": _("Jiangsu"),
        "JX": _("Jiangxi"),
        "JL": _("Jilin"),
        "LN": _("Liaoning"),
        "NM": _("Inner Mongolia"),
        "NX": _("Ningxia"),
        "QH": _("Qinghai"),
        "SN": _("Shaanxi"),
        "SD": _("Shandong"),
        "SH": _("Shanghai"),
        "SX": _("Shanxi"),
        "SC": _("Sichuan"),
        "TJ": _("Tianjin"),
        "XJ": _("Xinjiang"),
        "XZ": _("Tibet"),
        "YN": _("Yunnan"),
        "ZJ": _("Zhejiang"),
    },
    "JP": {  # Japan
        "HOKKAIDO": _("Hokkaido"),
        "AOMORI": _("Aomori"),
        "IWATE": _("Iwate"),
        "MIYAGI": _("Miyagi"),
        "AKITA": _("Akita"),
        "YAMAGATA": _("Yamagata"),
        "FUKUSHIMA": _("Fukushima"),
        "IBARAKI": _("Ibaraki"),
        "TOCHIGI": _("Tochigi"),
        "GUNMA": _("Gunma"),
        "SAITAMA": _("Saitama"),
        "CHIBA": _("Chiba"),
        "TOKYO": _("Tokyo"),
        "KANAGAWA": _("Kanagawa"),
        "NIIGATA": _("Niigata"),
        "TOYAMA": _("Toyama"),
        "ISHIKAWA": _("Ishikawa"),
        "FUKUI": _("Fukui"),
        "YAMANASHI": _("Yamanashi"),
        "NAGANO": _("Nagano"),
        "GIFU": _("Gifu"),
        "SHIZUOKA": _("Shizuoka"),
        "AICHI": _("Aichi"),
        "MIE": _("Mie"),
        "SHIGA": _("Shiga"),
        "KYOTO": _("Kyoto"),
        "OSAKA": _("Osaka"),
        "HYOGO": _("Hyogo"),
        "NARA": _("Nara"),
        "WAKAYAMA": _("Wakayama"),
        "TOTTORI": _("Tottori"),
        "SHIMANE": _("Shimane"),
        "OKAYAMA": _("Okayama"),
        "HIROSHIMA": _("Hiroshima"),
        "YAMAGUCHI": _("Yamaguchi"),
        "TOKUSHIMA": _("Tokushima"),
        "KAGAWA": _("Kagawa"),
        "EHIME": _("Ehime"),
        "KOCHI": _("Kochi"),
        "FUKUOKA": _("Fukuoka"),
        "SAGA": _("Saga"),
        "NAGASAKI": _("Nagasaki"),
        "KUMAMOTO": _("Kumamoto"),
        "OITA": _("Oita"),
        "MIYAZAKI": _("Miyazaki"),
        "KAGOSHIMA": _("Kagoshima"),
        "OKINAWA": _("Okinawa"),
    },
    "MX": {  # Mexico
        "AGU": _("Aguascalientes"),
        "BCN": _("Baja California"),
        "BCS": _("Baja California Sur"),
        "CAM": _("Campeche"),
        "CHP": _("Chiapas"),
        "CHH": _("Chihuahua"),
        "COA": _("Coahuila"),
        "COL": _("Colima"),
        "DIF": _("Mexico City"),
        "DUR": _("Durango"),
        "GUA": _("Guanajuato"),
        "GRO": _("Guerrero"),
        "HID": _("Hidalgo"),
        "JAL": _("Jalisco"),
        "MEX": _("México"),
        "MIC": _("Michoacán"),
        "MOR": _("Morelos"),
        "NAY": _("Nayarit"),
        "NLE": _("Nuevo León"),
        "OAX": _("Oaxaca"),
        "PUE": _("Puebla"),
        "QUE": _("Querétaro"),
        "ROO": _("Quintana Roo"),
        "SLP": _("San Luis Potosí"),
        "SIN": _("Sinaloa"),
        "SON": _("Sonora"),
        "TAB": _("Tabasco"),
        "TAM": _("Tamaulipas"),
        "TLA": _("Tlaxcala"),
        "VER": _("Veracruz"),
        "YUC": _("Yucatán"),
        "ZAC": _("Zacatecas"),
    },
    "BR": {  # Brazil
        "AC": _("Acre"),
        "AL": _("Alagoas"),
        "AP": _("Amapá"),
        "AM": _("Amazonas"),
        "BA": _("Bahia"),
        "CE": _("Ceará"),
        "DF": _("Federal District"),
        "ES": _("Espírito Santo"),
        "GO": _("Goiás"),
        "MA": _("Maranhão"),
        "MT": _("Mato Grosso"),
        "MS": _("Mato Grosso do Sul"),
        "MG": _("Minas Gerais"),
        "PA": _("Pará"),
        "PB": _("Paraíba"),
        "PR": _("Paraná"),
        "PE": _("Pernambuco"),
        "PI": _("Piauí"),
        "RJ": _("Rio de Janeiro"),
        "RN": _("Rio Grande do Norte"),
        "RS": _("Rio Grande do Sul"),
        "RO": _("Rondônia"),
        "RR": _("Roraima"),
        "SC": _("Santa Catarina"),
        "SP": _("São Paulo"),
        "SE": _("Sergipe"),
        "TO": _("Tocantins"),
    },
}


def get_states_for_country(country_code):
    """
    Get list of states/provinces for a country.

    Uses hybrid approach:
    1. First checks our curated STATES_BY_COUNTRY for high-quality data
    2. Falls back to pycountry for global ISO 3166-2 subdivision data
    3. Returns empty dict if no data available

    Args:
        country_code: ISO 3166-1 alpha-2 country code (e.g., 'US', 'CA')

    Returns:
        dict: Dictionary of {code: name} for states/provinces
              Empty dict if country has no subdivisions
    """
    country_code = country_code.upper()

    # First check our curated data
    if country_code in STATES_BY_COUNTRY:
        return STATES_BY_COUNTRY[country_code]

    # Fall back to pycountry for global coverage
    if PYCOUNTRY_AVAILABLE:
        try:
            country = pycountry.countries.get(alpha_2=country_code)
            if country:
                subdivisions = pycountry.subdivisions.get(country_code=country_code)
                if subdivisions:
                    # Convert pycountry subdivisions to our format
                    # pycountry uses full codes like 'US-CA', we want just 'CA'
                    states = {}
                    for subdivision in subdivisions:
                        # Get the subdivision code without country prefix
                        # e.g., 'US-CA' -> 'CA'
                        code = subdivision.code.split("-")[-1]
                        states[code] = subdivision.name
                    return states
        except (AttributeError, LookupError):
            pass

    return {}


def get_states_for_countries(country_codes):
    """
    Get states/provinces for multiple countries.

    Uses hybrid approach via get_states_for_country():
    - Curated data for high-traffic countries
    - pycountry fallback for global coverage

    Args:
        country_codes: List of ISO 3166-1 alpha-2 country codes

    Returns:
        dict: Dictionary mapping country codes to their states
              Format: {'US': {'CA': 'California', 'NY': 'New York'}, ...}
              Only includes countries that have subdivision data
    """
    result = {}
    for country_code in country_codes:
        states = get_states_for_country(country_code)
        if states:
            result[country_code.upper()] = states
    return result


def has_states(country_code):
    """
    Check if a country has state/province data.

    Uses hybrid approach - checks both curated data and pycountry.

    Args:
        country_code: ISO 3166-1 alpha-2 country code

    Returns:
        bool: True if country has subdivision data
    """
    states = get_states_for_country(country_code)
    return bool(states)
