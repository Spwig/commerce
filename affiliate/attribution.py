"""
Affiliate Attribution Engine
Handles conversion tracking and commission calculation for affiliate sales
"""

from decimal import Decimal
from django.utils import timezone
from django.db import transaction
import logging

from .models import Click, Commission, Link, Program

logger = logging.getLogger(__name__)


class AttributionEngine:
    """
    Attribution engine for tracking affiliate conversions and creating commissions.
    Currently implements last-click attribution model.
    """

    def __init__(self, order):
        """
        Initialize attribution engine for an order.

        Args:
            order: The order instance to attribute
        """
        self.order = order
        self.session = getattr(order, 'session', None)
        self.request = getattr(order, 'request', None)

    def process_order(self):
        """
        Process order for affiliate attribution and create commissions.

        Returns:
            list: List of Commission objects created
        """
        # Find applicable affiliate clicks
        clicks = self._find_applicable_clicks()

        if not clicks:
            logger.info(f"No affiliate clicks found for order {self.order.id}")
            return []

        # Create commissions for all applicable clicks
        commissions = []
        for click in clicks:
            commission = self._create_commission(click)
            if commission:
                commissions.append(commission)

        if commissions:
            logger.info(
                f"Created {len(commissions)} commission(s) for order {self.order.id}"
            )

        return commissions

    def _find_applicable_clicks(self):
        """
        Find affiliate clicks that should receive credit for this order.
        Currently uses last-click attribution model.

        Returns:
            QuerySet: Click objects that should receive credit
        """
        clicks = []

        # Method 1: Check for affiliate cookies in session/request
        if self.request:
            clicks_from_cookies = self._find_clicks_from_cookies()
            if clicks_from_cookies:
                clicks.extend(clicks_from_cookies)

        # Method 2: Check for affiliate parameter in session
        if self.session:
            affiliate_code = self.session.get('affiliate_code')
            if affiliate_code:
                click = self._find_click_by_code(affiliate_code)
                if click:
                    clicks.append(click)

        # Method 3: Check user's recent clicks (fallback)
        if not clicks and hasattr(self.order, 'user') and self.order.user:
            click = self._find_click_by_user(self.order.user)
            if click:
                clicks.append(click)

        # Deduplicate and return most recent valid click per program
        return self._deduplicate_clicks(clicks)

    def _find_clicks_from_cookies(self):
        """
        Find clicks from affiliate cookies in the request.

        Returns:
            list: List of Click objects found from cookies
        """
        clicks = []

        if not self.request:
            return clicks

        # Check for affiliate cookies (format: aff_{program_id})
        for cookie_name, cookie_value in self.request.COOKIES.items():
            if cookie_name.startswith('aff_'):
                try:
                    # Extract program ID from cookie name
                    program_id = int(cookie_name.split('_')[1])

                    # Find click by cookie value and program
                    click = Click.objects.select_related(
                        'link', 'link__affiliate', 'link__program'
                    ).filter(
                        cookie_value=cookie_value,
                        link__program_id=program_id,
                        link__is_active=True,
                        link__program__status='active'
                    ).first()

                    if click and self._is_click_valid(click):
                        clicks.append(click)
                        logger.debug(
                            f"Found valid click from cookie: {cookie_name} "
                            f"for program {program_id}"
                        )

                except (ValueError, IndexError) as e:
                    logger.warning(f"Invalid affiliate cookie format: {cookie_name}")
                    continue

        return clicks

    def _find_click_by_code(self, affiliate_code):
        """
        Find most recent valid click by affiliate code.

        Args:
            affiliate_code: The affiliate code from session

        Returns:
            Click or None: Most recent valid click
        """
        click = Click.objects.select_related(
            'link', 'link__affiliate', 'link__program'
        ).filter(
            link__affiliate__affiliate_code=affiliate_code,
            link__is_active=True,
            link__program__status='active'
        ).order_by('-clicked_at').first()

        if click and self._is_click_valid(click):
            return click

        return None

    def _find_click_by_user(self, user):
        """
        Find most recent valid click by user (if logged in).

        Args:
            user: The user who placed the order

        Returns:
            Click or None: Most recent valid click
        """
        # Get most recent click within cookie lifetime
        # This is a fallback method if no cookies/session data available
        click = Click.objects.select_related(
            'link', 'link__affiliate', 'link__program'
        ).filter(
            link__is_active=True,
            link__program__status='active'
        ).order_by('-clicked_at').first()

        if click and self._is_click_valid(click):
            # Additional check: click should be recent enough
            max_age_days = click.link.program.cookie_lifetime_days
            age = timezone.now() - click.clicked_at
            if age.days <= max_age_days:
                return click

        return None

    def _is_click_valid(self, click):
        """
        Check if a click is still valid for attribution.

        Args:
            click: Click instance to validate

        Returns:
            bool: True if click is valid
        """
        # Check if click is within cookie lifetime
        age = timezone.now() - click.clicked_at
        max_age = click.link.program.cookie_lifetime_days

        if age.days > max_age:
            logger.debug(
                f"Click {click.id} is too old ({age.days} days, "
                f"max {max_age} days)"
            )
            return False

        # Check if link and program are active
        if not click.link.is_active:
            logger.debug(f"Click {click.id} has inactive link")
            return False

        if click.link.program.status != 'active':
            logger.debug(f"Click {click.id} has inactive program")
            return False

        # Check if affiliate is active
        if click.link.affiliate.status != 'active':
            logger.debug(f"Click {click.id} has inactive affiliate")
            return False

        return True

    def _deduplicate_clicks(self, clicks):
        """
        Deduplicate clicks, keeping the most recent per program.

        Args:
            clicks: List of Click objects

        Returns:
            list: Deduplicated list of Click objects
        """
        if not clicks:
            return []

        # Group by program, keep most recent
        program_clicks = {}
        for click in clicks:
            program_id = click.link.program_id
            if program_id not in program_clicks or \
               click.clicked_at > program_clicks[program_id].clicked_at:
                program_clicks[program_id] = click

        return list(program_clicks.values())

    @transaction.atomic
    def _create_commission(self, click):
        """
        Create a commission record for a click.

        Args:
            click: Click instance that should receive credit

        Returns:
            Commission or None: Created commission instance
        """
        try:
            # Check if commission already exists for this order/click
            existing = Commission.objects.filter(
                order=self.order,
                click=click
            ).exists()

            if existing:
                logger.warning(
                    f"Commission already exists for order {self.order.id} "
                    f"and click {click.id}"
                )
                return None

            # Calculate commission amount
            amount = self._calculate_commission_amount(
                click.link.program,
                self.order
            )

            # Determine currency and base-currency equivalent
            from core.models import SiteSettings
            settings = SiteSettings.get_settings()
            order_currency = self.order.customer_currency or str(self.order.total_amount.currency) if hasattr(self.order.total_amount, 'currency') else settings.default_currency
            base_currency = settings.default_currency
            commission_exchange_rate = self.order.exchange_rate_used

            if order_currency and order_currency != base_currency and commission_exchange_rate:
                amount_base = (amount / commission_exchange_rate).quantize(Decimal('0.01'))
            else:
                amount_base = amount

            # Create commission
            commission = Commission.objects.create(
                affiliate=click.link.affiliate,
                program=click.link.program,
                order=self.order,
                click=click,
                amount=amount,
                currency=order_currency or base_currency,
                amount_base=amount_base,
                base_currency=base_currency,
                exchange_rate_used=commission_exchange_rate,
                status='pending',  # Requires approval
                notes=f"Auto-generated from order {self.order.id}"
            )

            logger.info(
                f"Created commission {commission.id} for {commission.currency} {amount} "
                f"(base: {base_currency} {amount_base}, "
                f"order {self.order.id}, affiliate {click.link.affiliate.affiliate_code})"
            )

            return commission

        except Exception as e:
            logger.error(
                f"Error creating commission for order {self.order.id}: {str(e)}"
            )
            return None

    def _calculate_commission_amount(self, program, order):
        """
        Calculate commission amount based on program settings.

        Args:
            program: Program instance
            order: Order instance

        Returns:
            Decimal: Commission amount
        """
        if program.commission_type == 'percentage':
            # Calculate percentage of order total
            order_total = getattr(order, 'total', Decimal('0'))
            percentage = program.commission_value / Decimal('100')
            amount = order_total * percentage

        else:  # fixed
            # Fixed amount per order
            amount = program.commission_value

        # Round to 2 decimal places
        return amount.quantize(Decimal('0.01'))


class CommissionCalculator:
    """
    Helper class for calculating commission amounts and forecasts.
    """

    @staticmethod
    def calculate_for_order(program, order_total):
        """
        Calculate commission for an order given program and order total.

        Args:
            program: Program instance
            order_total: Decimal order total amount

        Returns:
            Decimal: Commission amount
        """
        if program.commission_type == 'percentage':
            percentage = program.commission_value / Decimal('100')
            amount = order_total * percentage
        else:
            amount = program.commission_value

        return amount.quantize(Decimal('0.01'))

    @staticmethod
    def forecast_earnings(program, estimated_sales, estimated_order_value):
        """
        Forecast potential earnings for a program.

        Args:
            program: Program instance
            estimated_sales: Number of estimated sales
            estimated_order_value: Average order value

        Returns:
            dict: Forecast data
        """
        commission_per_order = CommissionCalculator.calculate_for_order(
            program,
            Decimal(str(estimated_order_value))
        )

        total_commissions = commission_per_order * Decimal(str(estimated_sales))

        return {
            'commission_per_order': float(commission_per_order),
            'estimated_sales': estimated_sales,
            'total_commissions': float(total_commissions),
            'commission_type': program.get_commission_type_display(),
            'commission_value': float(program.commission_value)
        }


# Utility function for easy integration
def attribute_order_to_affiliate(order):
    """
    Convenience function to attribute an order to affiliates.

    Usage:
        from affiliate.attribution import attribute_order_to_affiliate

        # In your order completion handler:
        commissions = attribute_order_to_affiliate(order)

    Args:
        order: Order instance

    Returns:
        list: List of Commission objects created
    """
    engine = AttributionEngine(order)
    return engine.process_order()
