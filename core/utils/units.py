"""
Unit conversion utilities for product measurements.
Uses Pint library for accurate conversions between different unit systems.
"""

from decimal import Decimal

from pint import UnitRegistry

# Initialize Pint unit registry
ureg = UnitRegistry()


class UnitConverter:
    """
    Handle unit conversions for product measurements.
    Supports weight, length, volume, area, and temperature conversions.
    Provides accurate conversions using the Pint library.
    """

    # Supported weight units
    WEIGHT_UNITS = {
        "g": "gram",
        "kg": "kilogram",
        "oz": "ounce",
        "lb": "pound",
    }

    # Supported length units
    LENGTH_UNITS = {
        "mm": "millimeter",
        "cm": "centimeter",
        "m": "meter",
        "in": "inch",
        "ft": "foot",
    }

    # Supported volume units
    VOLUME_UNITS = {
        "ml": "milliliter",
        "l": "liter",
        "cl": "centiliter",
        "dl": "deciliter",
        "fl_oz": "fluid_ounce",
        "cup": "cup",
        "pt": "pint",
        "qt": "quart",
        "gal": "gallon",
    }

    # Supported area units
    AREA_UNITS = {
        "sq_mm": "millimeter**2",
        "sq_cm": "centimeter**2",
        "sq_m": "meter**2",
        "sq_in": "inch**2",
        "sq_ft": "foot**2",
        "sq_yd": "yard**2",
    }

    # Supported temperature units
    TEMPERATURE_UNITS = {
        "c": "celsius",
        "f": "fahrenheit",
        "k": "kelvin",
    }

    @classmethod
    def convert_weight(cls, value: Decimal, from_unit: str, to_unit: str) -> Decimal | None:
        """
        Convert weight between units.

        Args:
            value: Weight value to convert
            from_unit: Source unit (g, kg, oz, lb)
            to_unit: Target unit (g, kg, oz, lb)

        Returns:
            Converted value as Decimal, or None if value is None

        Example:
            >>> UnitConverter.convert_weight(Decimal('100'), 'g', 'oz')
            Decimal('3.527')
        """
        if value is None or value == 0:
            return None

        # Get full unit names
        from_unit_name = cls.WEIGHT_UNITS.get(from_unit, from_unit)
        to_unit_name = cls.WEIGHT_UNITS.get(to_unit, to_unit)

        # Create quantity and convert
        quantity = ureg.Quantity(float(value), from_unit_name)
        converted = quantity.to(to_unit_name)

        # Return as Decimal with reasonable precision
        return Decimal(str(round(converted.magnitude, 3)))

    @classmethod
    def convert_length(cls, value: Decimal, from_unit: str, to_unit: str) -> Decimal | None:
        """
        Convert length between units.

        Args:
            value: Length value to convert
            from_unit: Source unit (mm, cm, m, in, ft)
            to_unit: Target unit (mm, cm, m, in, ft)

        Returns:
            Converted value as Decimal, or None if value is None

        Example:
            >>> UnitConverter.convert_length(Decimal('10'), 'cm', 'in')
            Decimal('3.937')
        """
        if value is None or value == 0:
            return None

        # Get full unit names
        from_unit_name = cls.LENGTH_UNITS.get(from_unit, from_unit)
        to_unit_name = cls.LENGTH_UNITS.get(to_unit, to_unit)

        # Create quantity and convert
        quantity = ureg.Quantity(float(value), from_unit_name)
        converted = quantity.to(to_unit_name)

        # Return as Decimal with reasonable precision
        return Decimal(str(round(converted.magnitude, 2)))

    @classmethod
    def format_weight(cls, value: Decimal, unit: str, precision: int = 2) -> str:
        """
        Format weight with unit label.

        Args:
            value: Weight value
            unit: Unit abbreviation (g, kg, oz, lb)
            precision: Number of decimal places

        Returns:
            Formatted string like "3.50 oz"

        Example:
            >>> UnitConverter.format_weight(Decimal('3.527'), 'oz', 2)
            '3.53 oz'
        """
        if value is None or value == 0:
            return ""

        return f"{float(value):.{precision}f} {unit}"

    @classmethod
    def format_length(cls, value: Decimal, unit: str, precision: int = 1) -> str:
        """
        Format length with unit label.

        Args:
            value: Length value
            unit: Unit abbreviation (mm, cm, m, in, ft)
            precision: Number of decimal places

        Returns:
            Formatted string like "10.5 cm"

        Example:
            >>> UnitConverter.format_length(Decimal('10.5'), 'cm', 1)
            '10.5 cm'
        """
        if value is None or value == 0:
            return ""

        return f"{float(value):.{precision}f} {unit}"

    @classmethod
    def get_country_preferred_weight_unit(cls, country_code: str) -> str:
        """
        Get preferred weight unit for a country.

        Args:
            country_code: ISO 2-letter country code

        Returns:
            Preferred weight unit ('lb' for imperial countries, 'kg' for metric)
        """
        # US, Liberia, Myanmar use imperial system
        imperial_countries = ["US", "LR", "MM"]

        if country_code and country_code.upper() in imperial_countries:
            return "lb"
        return "kg"

    @classmethod
    def get_country_preferred_length_unit(cls, country_code: str) -> str:
        """
        Get preferred length unit for a country.

        Args:
            country_code: ISO 2-letter country code

        Returns:
            Preferred length unit ('in' for imperial countries, 'cm' for metric)
        """
        # US, Liberia, Myanmar use imperial system
        imperial_countries = ["US", "LR", "MM"]

        if country_code and country_code.upper() in imperial_countries:
            return "in"
        return "cm"

    @classmethod
    def convert_volume(cls, value: Decimal, from_unit: str, to_unit: str) -> Decimal | None:
        """
        Convert volume between units.

        Args:
            value: Volume value to convert
            from_unit: Source unit (ml, l, cl, dl, fl_oz, cup, pt, qt, gal)
            to_unit: Target unit (ml, l, cl, dl, fl_oz, cup, pt, qt, gal)

        Returns:
            Converted value as Decimal, or None if value is None

        Example:
            >>> UnitConverter.convert_volume(Decimal('100'), 'ml', 'fl_oz')
            Decimal('3.381')
        """
        if value is None or value == 0:
            return None

        # Get full unit names
        from_unit_name = cls.VOLUME_UNITS.get(from_unit, from_unit)
        to_unit_name = cls.VOLUME_UNITS.get(to_unit, to_unit)

        # Create quantity and convert
        quantity = ureg.Quantity(float(value), from_unit_name)
        converted = quantity.to(to_unit_name)

        # Return as Decimal with reasonable precision
        return Decimal(str(round(converted.magnitude, 3)))

    @classmethod
    def convert_area(cls, value: Decimal, from_unit: str, to_unit: str) -> Decimal | None:
        """
        Convert area between units.

        Args:
            value: Area value to convert
            from_unit: Source unit (sq_mm, sq_cm, sq_m, sq_in, sq_ft, sq_yd)
            to_unit: Target unit (sq_mm, sq_cm, sq_m, sq_in, sq_ft, sq_yd)

        Returns:
            Converted value as Decimal, or None if value is None

        Example:
            >>> UnitConverter.convert_area(Decimal('1'), 'sq_m', 'sq_ft')
            Decimal('10.764')
        """
        if value is None or value == 0:
            return None

        # Get full unit names
        from_unit_name = cls.AREA_UNITS.get(from_unit, from_unit)
        to_unit_name = cls.AREA_UNITS.get(to_unit, to_unit)

        # Create quantity and convert
        quantity = ureg.Quantity(float(value), from_unit_name)
        converted = quantity.to(to_unit_name)

        # Return as Decimal with reasonable precision
        return Decimal(str(round(converted.magnitude, 3)))

    @classmethod
    def convert_temperature(cls, value: Decimal, from_unit: str, to_unit: str) -> Decimal | None:
        """
        Convert temperature between units.

        Args:
            value: Temperature value to convert
            from_unit: Source unit (c, f, k)
            to_unit: Target unit (c, f, k)

        Returns:
            Converted value as Decimal, or None if value is None

        Example:
            >>> UnitConverter.convert_temperature(Decimal('20'), 'c', 'f')
            Decimal('68.0')
        """
        if value is None:
            return None

        # Get full unit names
        from_unit_name = cls.TEMPERATURE_UNITS.get(from_unit, from_unit)
        to_unit_name = cls.TEMPERATURE_UNITS.get(to_unit, to_unit)

        # Create quantity and convert
        quantity = ureg.Quantity(float(value), from_unit_name)
        converted = quantity.to(to_unit_name)

        # Return as Decimal with reasonable precision (1 decimal for temperature)
        return Decimal(str(round(converted.magnitude, 1)))

    @classmethod
    def format_volume(cls, value: Decimal, unit: str, precision: int = 2) -> str:
        """
        Format volume with unit label.

        Args:
            value: Volume value
            unit: Unit abbreviation (ml, l, fl_oz, gal, etc.)
            precision: Number of decimal places

        Returns:
            Formatted string like "100.0 ml"
        """
        if value is None or value == 0:
            return ""

        return f"{float(value):.{precision}f} {unit}"

    @classmethod
    def format_area(cls, value: Decimal, unit: str, precision: int = 2) -> str:
        """
        Format area with unit label.

        Args:
            value: Area value
            unit: Unit abbreviation (sq_m, sq_ft, etc.)
            precision: Number of decimal places

        Returns:
            Formatted string like "10.5 sq ft"
        """
        if value is None or value == 0:
            return ""

        # Format unit display (replace underscore with space)
        unit_display = unit.replace("_", " ")
        return f"{float(value):.{precision}f} {unit_display}"

    @classmethod
    def format_temperature(cls, value: Decimal, unit: str, precision: int = 1) -> str:
        """
        Format temperature with unit label.

        Args:
            value: Temperature value
            unit: Unit abbreviation (c, f, k)
            precision: Number of decimal places

        Returns:
            Formatted string like "20.0°C"
        """
        if value is None:
            return ""

        # Map units to display symbols
        unit_symbols = {
            "c": "°C",
            "f": "°F",
            "k": "K",
        }

        symbol = unit_symbols.get(unit.lower(), unit.upper())
        return f"{float(value):.{precision}f}{symbol}"

    @classmethod
    def get_country_preferred_volume_unit(cls, country_code: str) -> str:
        """
        Get preferred volume unit for a country.

        Args:
            country_code: ISO 2-letter country code

        Returns:
            Preferred volume unit ('fl_oz' for imperial countries, 'ml' for metric)
        """
        # US, Liberia, Myanmar use imperial system
        imperial_countries = ["US", "LR", "MM"]

        if country_code and country_code.upper() in imperial_countries:
            return "fl_oz"
        return "ml"

    @classmethod
    def get_country_preferred_area_unit(cls, country_code: str) -> str:
        """
        Get preferred area unit for a country.

        Args:
            country_code: ISO 2-letter country code

        Returns:
            Preferred area unit ('sq_ft' for imperial countries, 'sq_m' for metric)
        """
        # US, Liberia, Myanmar use imperial system
        imperial_countries = ["US", "LR", "MM"]

        if country_code and country_code.upper() in imperial_countries:
            return "sq_ft"
        return "sq_m"

    @classmethod
    def get_country_preferred_temperature_unit(cls, country_code: str) -> str:
        """
        Get preferred temperature unit for a country.

        Args:
            country_code: ISO 2-letter country code

        Returns:
            Preferred temperature unit ('f' for Fahrenheit countries, 'c' for Celsius)
        """
        # US, Bahamas, Cayman Islands, Liberia, Palau use Fahrenheit
        fahrenheit_countries = ["US", "BS", "KY", "LR", "PW"]

        if country_code and country_code.upper() in fahrenheit_countries:
            return "f"
        return "c"
