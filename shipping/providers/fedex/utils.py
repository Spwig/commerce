"""
FedEx Provider Utility Functions

Unit conversions, service code mappings, and helper functions.
"""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# FedEx Service Codes to Human-Readable Names
FEDEX_SERVICE_CODES = {
    # Domestic Ground
    'FEDEX_GROUND': _('FedEx Ground'),
    'GROUND_HOME_DELIVERY': _('FedEx Home Delivery'),
    
    # Domestic Express
    'FEDEX_EXPRESS_SAVER': _('FedEx Express Saver'),
    'FEDEX_2_DAY': _('FedEx 2Day'),
    'FEDEX_2_DAY_AM': _('FedEx 2Day AM'),
    'STANDARD_OVERNIGHT': _('FedEx Standard Overnight'),
    'PRIORITY_OVERNIGHT': _('FedEx Priority Overnight'),
    'FIRST_OVERNIGHT': _('FedEx First Overnight'),
    
    # International
    'INTERNATIONAL_ECONOMY': _('FedEx International Economy'),
    'INTERNATIONAL_PRIORITY': _('FedEx International Priority'),
    'INTERNATIONAL_FIRST': _('FedEx International First'),
    'INTERNATIONAL_GROUND': _('FedEx International Ground'),
    'EUROPE_FIRST_INTERNATIONAL_PRIORITY': _('FedEx Europe First'),
    
    # SmartPost
    'SMART_POST': _('FedEx SmartPost'),
    
    # Freight (not supported in v1.0 but included for completeness)
    'FEDEX_FREIGHT_ECONOMY': _('FedEx Freight Economy'),
    'FEDEX_FREIGHT_PRIORITY': _('FedEx Freight Priority'),
    'FEDEX_1_DAY_FREIGHT': _('FedEx 1Day Freight'),
    'FEDEX_2_DAY_FREIGHT': _('FedEx 2Day Freight'),
    'FEDEX_3_DAY_FREIGHT': _('FedEx 3Day Freight'),
}


# Typical transit times (for reference, actual times come from API)
TYPICAL_TRANSIT_DAYS = {
    'FEDEX_GROUND': (1, 5),
    'FEDEX_EXPRESS_SAVER': 3,
    'FEDEX_2_DAY': 2,
    'FEDEX_2_DAY_AM': 2,
    'STANDARD_OVERNIGHT': 1,
    'PRIORITY_OVERNIGHT': 1,
    'FIRST_OVERNIGHT': 1,
    'INTERNATIONAL_ECONOMY': (4, 7),
    'INTERNATIONAL_PRIORITY': (1, 3),
    'INTERNATIONAL_FIRST': (1, 2),
}


def grams_to_pounds(grams: float) -> float:
    """
    Convert weight from grams to pounds.
    
    Args:
        grams: Weight in grams
        
    Returns:
        Weight in pounds (rounded to 2 decimals)
        
    Example:
        >>> grams_to_pounds(1000)
        2.20
    """
    pounds = grams * 0.00220462
    return round(pounds, 2)


def pounds_to_grams(pounds: float) -> float:
    """
    Convert weight from pounds to grams.
    
    Args:
        pounds: Weight in pounds
        
    Returns:
        Weight in grams (rounded to nearest gram)
        
    Example:
        >>> pounds_to_grams(2.20)
        998
    """
    grams = pounds / 0.00220462
    return round(grams)


def cm_to_inches(cm: float) -> float:
    """
    Convert length from centimeters to inches.
    
    Args:
        cm: Length in centimeters
        
    Returns:
        Length in inches (rounded to 2 decimals)
        
    Example:
        >>> cm_to_inches(10)
        3.94
    """
    inches = cm * 0.393701
    return round(inches, 2)


def inches_to_cm(inches: float) -> float:
    """
    Convert length from inches to centimeters.
    
    Args:
        inches: Length in inches
        
    Returns:
        Length in centimeters (rounded to 2 decimals)
        
    Example:
        >>> inches_to_cm(3.94)
        10.01
    """
    cm = inches / 0.393701
    return round(cm, 2)


def get_service_name(service_code: str) -> str:
    """
    Get human-readable service name from FedEx service code.
    
    Args:
        service_code: FedEx service type code
        
    Returns:
        Translated service name or the code if unknown
        
    Example:
        >>> get_service_name('FEDEX_GROUND')
        'FedEx Ground'
    """
    return str(FEDEX_SERVICE_CODES.get(service_code, service_code))


def parse_fedex_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    Parse FedEx date string to datetime object.
    
    FedEx uses various date formats:
    - ISO 8601: "2025-10-23T14:30:00"
    - Date only: "2025-10-23"
    
    Args:
        date_str: Date string from FedEx API
        
    Returns:
        Datetime object or None if parsing fails
        
    Example:
        >>> parse_fedex_date('2025-10-23')
        datetime(2025, 10, 23, 0, 0, 0)
    """
    if not date_str:
        return None
    
    try:
        # Try ISO 8601 format with time
        if 'T' in date_str:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        
        # Try date only format
        return datetime.strptime(date_str, '%Y-%m-%d')
    
    except (ValueError, AttributeError):
        return None


def calculate_delivery_days(commit_data: Optional[Dict[str, Any]]) -> Optional[int]:
    """
    Calculate delivery days from FedEx commit data.
    
    Args:
        commit_data: FedEx commit data from rate response
        
    Returns:
        Number of delivery days or None
        
    Example:
        >>> calculate_delivery_days({'transitDays': '3'})
        3
    """
    if not commit_data:
        return None
    
    # FedEx provides transitDays directly
    transit_days = commit_data.get('transitDays')
    if transit_days:
        try:
            return int(transit_days)
        except (ValueError, TypeError):
            pass
    
    # Fallback: Calculate from dates
    delivery_date_str = commit_data.get('dateDetail', {}).get('dayFormat')
    if delivery_date_str:
        delivery_date = parse_fedex_date(delivery_date_str)
        if delivery_date:
            days = (delivery_date.date() - timezone.now().date()).days
            return max(0, days)
    
    return None


def parse_money(money_obj: Optional[Any]) -> Optional[Decimal]:
    """
    Parse FedEx Money value to Decimal.

    FedEx API returns money in two formats:
    1. Object format: {'amount': 12.50, 'currency': 'USD'}
    2. Plain number: 12.50

    Args:
        money_obj: FedEx Money object or plain number

    Returns:
        Decimal amount or None

    Example:
        >>> parse_money({'amount': 12.50, 'currency': 'USD'})
        Decimal('12.50')
        >>> parse_money(12.50)
        Decimal('12.50')
    """
    if money_obj is None:
        return None

    # Handle plain number format
    if isinstance(money_obj, (int, float)):
        try:
            return Decimal(str(money_obj))
        except (ValueError, TypeError):
            return None

    # Handle object format with 'amount' key
    if isinstance(money_obj, dict):
        amount = money_obj.get('amount')
        if amount is not None:
            try:
                return Decimal(str(amount))
            except (ValueError, TypeError):
                return None

    return None


def get_currency(money_obj: Optional[Any], fallback: str = 'USD') -> str:
    """
    Get currency code from FedEx Money object or use fallback.

    Args:
        money_obj: FedEx Money object or plain number
        fallback: Fallback currency code (default: 'USD')

    Returns:
        Currency code

    Example:
        >>> get_currency({'amount': 12.50, 'currency': 'USD'})
        'USD'
        >>> get_currency(12.50, 'CAD')
        'CAD'
    """
    if isinstance(money_obj, dict):
        return money_obj.get('currency', fallback)

    return fallback


def format_fedex_date(dt: datetime) -> str:
    """
    Format datetime for FedEx API requests.
    
    Args:
        dt: Datetime object
        
    Returns:
        Date string in YYYY-MM-DD format
        
    Example:
        >>> format_fedex_date(datetime(2025, 10, 23))
        '2025-10-23'
    """
    return dt.strftime('%Y-%m-%d')


def redact_account_number(account_number: str) -> str:
    """
    Redact FedEx account number for logging.
    
    Args:
        account_number: 9-digit account number
        
    Returns:
        Redacted account number (*****1234)
        
    Example:
        >>> redact_account_number('123456789')
        '*****6789'
    """
    if not account_number or len(account_number) < 4:
        return '***'
    
    return f"*****{account_number[-4:]}"
