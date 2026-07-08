"""
Visibility Rule Evaluation Engine
Handles the evaluation of visibility rules against context data
"""

import re
import json
from datetime import datetime, time, date
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth.models import Group
from typing import Dict, Any, Optional, List
import logging

from core.utils import get_default_currency

logger = logging.getLogger(__name__)


class ContextCollector:
    """
    Collects all relevant context data for rule evaluation
    """

    def collect_context(self, request) -> Dict[str, Any]:
        """
        Gather all available context data from the request
        """
        context = {
            'request': request,
            'user': self._get_user_context(request),
            'geo': self._get_geo_context(request),
            'device': self._get_device_context(request),
            'time': self._get_time_context(),
            'behavior': self._get_behavior_context(request),
            'ecommerce': self._get_ecommerce_context(request),
            'language': self._get_language_context(request),
        }

        # Add UTM parameters if present
        context['utm'] = self._get_utm_context(request)

        return context

    def _get_user_context(self, request) -> Dict[str, Any]:
        """Extract user-related context"""
        user = request.user
        context = {
            'is_authenticated': user.is_authenticated,
            'is_staff': user.is_staff if user.is_authenticated else False,
            'is_superuser': user.is_superuser if user.is_authenticated else False,
            'username': user.username if user.is_authenticated else None,
            'email': user.email if user.is_authenticated else None,
            'groups': [],
            'segment': None,
            'lifetime_value': 0,
            'order_count': 0,
        }

        if user.is_authenticated:
            # Get user groups
            context['groups'] = list(user.groups.values_list('name', flat=True))

            # Get customer metrics if available
            try:
                from customers.models import CustomerMetrics, CustomerSegment
                metrics = CustomerMetrics.objects.filter(user=user).first()
                if metrics:
                    context['lifetime_value'] = float(metrics.lifetime_value.amount) if metrics.lifetime_value else 0
                    context['order_count'] = metrics.completed_orders

                # Get customer segment
                segment = CustomerSegment.determine_segment_for_user(user)
                if segment:
                    context['segment'] = segment.name
            except Exception as e:
                logger.debug(f"Could not load customer metrics: {e}")

        return context

    def _get_geo_context(self, request) -> Dict[str, Any]:
        """Extract geographic context using GeoIP"""
        context = {
            'country_code': None,
            'country_name': None,
            'region': None,
            'city': None,
            'timezone': None,
            'is_vpn': False,
            'is_proxy': False,
            'is_tor': False,
        }

        try:
            from geoip.models import GeoLocation
            from geoip.utils import get_client_ip

            ip = get_client_ip(request)
            if ip:
                # Try to get cached location
                geo = GeoLocation.objects.filter(ip_address=ip, is_expired=False).first()
                if geo:
                    context.update({
                        'country_code': geo.country_code,
                        'country_name': geo.country_name,
                        'region': geo.region_name,
                        'city': geo.city_name,
                        'is_vpn': geo.is_vpn,
                        'is_proxy': geo.is_proxy,
                        'is_tor': geo.is_tor,
                    })
        except Exception as e:
            logger.debug(f"Could not load GeoIP data: {e}")

        # Get timezone from request or geo data
        context['timezone'] = request.session.get('django_timezone', timezone.get_current_timezone_name())

        return context

    def _get_device_context(self, request) -> Dict[str, Any]:
        """Extract device and browser context"""
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        context = {
            'user_agent': user_agent,
            'device_type': self._detect_device_type(user_agent),
            'browser': self._detect_browser(user_agent),
            'operating_system': self._detect_os(user_agent),
            'is_mobile': self._is_mobile(user_agent),
            'is_tablet': self._is_tablet(user_agent),
            'is_desktop': self._is_desktop(user_agent),
        }

        # Get screen size from cookie if available (set by JavaScript)
        if 'screen_size' in request.COOKIES:
            try:
                screen_data = json.loads(request.COOKIES.get('screen_size', '{}'))
                context['screen_width'] = screen_data.get('width')
                context['screen_height'] = screen_data.get('height')
            except:
                pass

        return context

    def _get_time_context(self) -> Dict[str, Any]:
        """Extract time-related context"""
        now = timezone.now()
        local_now = timezone.localtime(now)

        context = {
            'current_datetime': now,
            'local_datetime': local_now,
            'date': local_now.date(),
            'time': local_now.time(),
            'hour': local_now.hour,
            'day_of_week': local_now.weekday(),  # 0=Monday, 6=Sunday
            'day_name': local_now.strftime('%A'),
            'is_weekend': local_now.weekday() >= 5,
            'is_business_hours': self._is_business_hours(local_now),
        }

        return context

    def _get_behavior_context(self, request) -> Dict[str, Any]:
        """Extract behavioral context from session"""
        session = request.session
        context = {
            'is_first_visit': session.get('first_visit', True),
            'visit_count': session.get('visit_count', 1),
            'page_views': session.get('page_views', 0),
            'time_on_site': 0,  # Would need JavaScript tracking
            'referrer': request.META.get('HTTP_REFERER', ''),
            'landing_page': session.get('landing_page', request.path),
        }

        # Track first visit
        if 'first_visit' not in session:
            session['first_visit'] = True
            session['visit_count'] = 1
        else:
            session['first_visit'] = False

        return context

    def _get_ecommerce_context(self, request) -> Dict[str, Any]:
        """Extract e-commerce context"""
        context = {
            'cart_value': 0,
            'cart_items': 0,
            'has_purchased': False,
            'has_abandoned_cart': False,
            'wishlist_items': 0,
        }

        if request.user.is_authenticated:
            try:
                from cart.models import Cart, Wishlist
                from orders.models import Order
                from customers.models import AbandonedCart

                # Get current cart
                cart = Cart.objects.filter(user=request.user, is_active=True).first()
                if cart:
                    context['cart_value'] = float(cart.get_total())
                    context['cart_items'] = cart.items.count()

                # Check purchase history
                context['has_purchased'] = Order.objects.filter(
                    user=request.user,
                    status='completed'
                ).exists()

                # Check abandoned carts
                context['has_abandoned_cart'] = AbandonedCart.objects.filter(
                    user=request.user,
                    recovered=False
                ).exists()

                # Get wishlist count
                wishlist = Wishlist.objects.filter(user=request.user).first()
                if wishlist:
                    context['wishlist_items'] = wishlist.items.count()

            except Exception as e:
                logger.debug(f"Could not load e-commerce data: {e}")

        return context

    def _get_language_context(self, request) -> Dict[str, Any]:
        """Extract language and localization context"""
        from django.utils import translation

        context = {
            'browser_language': request.META.get('HTTP_ACCEPT_LANGUAGE', '').split(',')[0].strip(),
            'selected_language': translation.get_language(),
            'selected_currency': request.session.get('currency', get_default_currency()),
        }

        return context

    def _get_utm_context(self, request) -> Dict[str, Any]:
        """Extract UTM parameters from request"""
        context = {}
        for param in ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']:
            context[param] = request.GET.get(param, '')
        return context

    def _detect_device_type(self, user_agent: str) -> str:
        """Detect device type from user agent"""
        if self._is_mobile(user_agent):
            return 'mobile'
        elif self._is_tablet(user_agent):
            return 'tablet'
        else:
            return 'desktop'

    def _is_mobile(self, user_agent: str) -> bool:
        """Check if user agent is mobile"""
        mobile_patterns = ['mobile', 'android', 'iphone', 'ipod', 'blackberry', 'windows phone']
        return any(pattern in user_agent for pattern in mobile_patterns) and 'ipad' not in user_agent

    def _is_tablet(self, user_agent: str) -> bool:
        """Check if user agent is tablet"""
        tablet_patterns = ['ipad', 'tablet', 'kindle', 'silk']
        return any(pattern in user_agent for pattern in tablet_patterns) or \
               ('android' in user_agent and 'mobile' not in user_agent)

    def _is_desktop(self, user_agent: str) -> bool:
        """Check if user agent is desktop"""
        return not self._is_mobile(user_agent) and not self._is_tablet(user_agent)

    def _detect_browser(self, user_agent: str) -> str:
        """Detect browser from user agent"""
        browsers = {
            'chrome': 'chrome',
            'safari': 'safari',
            'firefox': 'firefox',
            'edge': 'edge',
            'opera': 'opera',
            'ie': 'msie|trident',
        }

        for name, pattern in browsers.items():
            if re.search(pattern, user_agent):
                return name

        return 'unknown'

    def _detect_os(self, user_agent: str) -> str:
        """Detect operating system from user agent"""
        os_patterns = {
            'windows': 'windows',
            'macos': 'mac os|macintosh',
            'linux': 'linux',
            'android': 'android',
            'ios': 'iphone|ipad|ipod',
        }

        for name, pattern in os_patterns.items():
            if re.search(pattern, user_agent):
                return name

        return 'unknown'

    def _is_business_hours(self, dt: datetime) -> bool:
        """Check if current time is within business hours (9 AM - 5 PM weekdays)"""
        if dt.weekday() >= 5:  # Weekend
            return False
        return 9 <= dt.hour < 17


class RuleEvaluator:
    """
    Evaluates visibility rules against context
    """

    def evaluate_single_rule(self, rule, context: Dict[str, Any]) -> bool:
        """
        Evaluate a single visibility rule
        """
        if not rule.is_active:
            return False

        # Get cache key for this rule and context
        cache_key = self._get_cache_key(rule, context)

        # Check cache
        if rule.cache_duration > 0:
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

        # Evaluate based on rule type
        try:
            result = self._evaluate_rule_type(rule, context)

            # Cache result
            if rule.cache_duration > 0:
                cache.set(cache_key, result, rule.cache_duration)

            return result

        except Exception as e:
            logger.error(f"Error evaluating rule {rule.name}: {e}")
            return False

    def evaluate_rule_group(self, group, context: Dict[str, Any]) -> bool:
        """
        Evaluate a group of rules with logic operator
        """
        if not group.is_active:
            return False

        # Get all active rules in the group
        rules = group.rules.filter(is_active=True).order_by('rulegroupmember__order')

        if not rules.exists():
            return True  # No rules means no restrictions

        # Evaluate child groups first
        child_groups = group.child_groups.filter(is_active=True)
        group_results = [self.evaluate_rule_group(child, context) for child in child_groups]

        # Evaluate individual rules
        rule_results = [self.evaluate_single_rule(rule, context) for rule in rules]

        # Combine results
        all_results = group_results + rule_results

        if group.logic_operator == 'AND':
            return all(all_results)
        else:  # OR
            return any(all_results)

    def _evaluate_rule_type(self, rule, context: Dict[str, Any]) -> bool:
        """
        Evaluate specific rule type
        """
        rule_type = rule.rule_type
        operator = rule.operator
        rule_value = rule.value

        # Geographic rules
        if rule_type == 'geo_country':
            return self._compare(context['geo']['country_code'], operator, rule_value)
        elif rule_type == 'geo_region':
            return self._compare(context['geo']['region'], operator, rule_value)
        elif rule_type == 'geo_city':
            return self._compare(context['geo']['city'], operator, rule_value)
        elif rule_type == 'geo_timezone':
            return self._compare(context['geo']['timezone'], operator, rule_value)

        # User rules
        elif rule_type == 'user_logged_in':
            return self._compare(context['user']['is_authenticated'], operator, rule_value)
        elif rule_type == 'user_group':
            return self._compare_list(context['user']['groups'], operator, rule_value)
        elif rule_type == 'user_segment':
            return self._compare(context['user']['segment'], operator, rule_value)
        elif rule_type == 'user_lifetime_value':
            return self._compare_numeric(context['user']['lifetime_value'], operator, rule_value)
        elif rule_type == 'user_order_count':
            return self._compare_numeric(context['user']['order_count'], operator, rule_value)

        # Device rules
        elif rule_type == 'device_type':
            return self._compare(context['device']['device_type'], operator, rule_value)
        elif rule_type == 'browser':
            return self._compare(context['device']['browser'], operator, rule_value)
        elif rule_type == 'operating_system':
            return self._compare(context['device']['operating_system'], operator, rule_value)
        elif rule_type == 'screen_size':
            width = context['device'].get('screen_width', 0)
            return self._compare_numeric(width, operator, rule_value)

        # Time rules
        elif rule_type == 'date_range':
            return self._compare_date_range(context['time']['date'], rule_value)
        elif rule_type == 'time_range':
            return self._compare_time_range(context['time']['time'], rule_value)
        elif rule_type == 'day_of_week':
            return self._compare_list([context['time']['day_name']], operator, rule_value)
        elif rule_type == 'business_hours':
            return self._compare(context['time']['is_business_hours'], operator, rule_value)

        # Behavioral rules
        elif rule_type == 'first_visit':
            return self._compare(context['behavior']['is_first_visit'], operator, rule_value)
        elif rule_type == 'visit_count':
            return self._compare_numeric(context['behavior']['visit_count'], operator, rule_value)
        elif rule_type == 'page_views':
            return self._compare_numeric(context['behavior']['page_views'], operator, rule_value)
        elif rule_type == 'referrer':
            return self._compare(context['behavior']['referrer'], operator, rule_value)
        elif rule_type == 'utm_campaign':
            return self._compare(context['utm'].get('utm_campaign', ''), operator, rule_value)

        # E-commerce rules
        elif rule_type == 'cart_value':
            return self._compare_numeric(context['ecommerce']['cart_value'], operator, rule_value)
        elif rule_type == 'cart_items':
            return self._compare_numeric(context['ecommerce']['cart_items'], operator, rule_value)
        elif rule_type == 'has_purchased':
            return self._compare(context['ecommerce']['has_purchased'], operator, rule_value)
        elif rule_type == 'abandoned_cart':
            return self._compare(context['ecommerce']['has_abandoned_cart'], operator, rule_value)
        elif rule_type == 'wishlist_items':
            return self._compare_numeric(context['ecommerce']['wishlist_items'], operator, rule_value)

        # Language rules
        elif rule_type == 'browser_language':
            return self._compare(context['language']['browser_language'], operator, rule_value)
        elif rule_type == 'selected_language':
            return self._compare(context['language']['selected_language'], operator, rule_value)
        elif rule_type == 'selected_currency':
            return self._compare(context['language']['selected_currency'], operator, rule_value)

        else:
            logger.warning(f"Unknown rule type: {rule_type}")
            return False

    def _compare(self, actual_value, operator: str, expected_value) -> bool:
        """Generic comparison based on operator"""
        if operator == 'equals':
            return str(actual_value).lower() == str(expected_value).lower()
        elif operator == 'not_equals':
            return str(actual_value).lower() != str(expected_value).lower()
        elif operator == 'contains':
            return str(expected_value).lower() in str(actual_value).lower()
        elif operator == 'not_contains':
            return str(expected_value).lower() not in str(actual_value).lower()
        elif operator == 'is_true':
            return bool(actual_value)
        elif operator == 'is_false':
            return not bool(actual_value)
        elif operator == 'regex':
            return bool(re.search(str(expected_value), str(actual_value), re.IGNORECASE))
        else:
            return False

    def _compare_numeric(self, actual_value, operator: str, expected_value) -> bool:
        """Numeric comparison"""
        try:
            actual = float(actual_value) if actual_value is not None else 0
            expected = float(expected_value) if isinstance(expected_value, (int, float, str)) else 0

            if operator == 'equals':
                return actual == expected
            elif operator == 'not_equals':
                return actual != expected
            elif operator == 'greater_than':
                return actual > expected
            elif operator == 'less_than':
                return actual < expected
            elif operator == 'between':
                if isinstance(expected_value, dict):
                    min_val = float(expected_value.get('min', 0))
                    max_val = float(expected_value.get('max', 0))
                    return min_val <= actual <= max_val
            return False
        except (ValueError, TypeError):
            return False

    def _compare_list(self, actual_list: List, operator: str, expected_value) -> bool:
        """List comparison"""
        if not isinstance(actual_list, list):
            actual_list = [actual_list]

        expected_list = expected_value if isinstance(expected_value, list) else [expected_value]
        expected_list = [str(v).lower() for v in expected_list]
        actual_list = [str(v).lower() for v in actual_list]

        if operator == 'in_list':
            return any(item in expected_list for item in actual_list)
        elif operator == 'not_in_list':
            return not any(item in expected_list for item in actual_list)
        else:
            return self._compare(','.join(actual_list), operator, ','.join(expected_list))

    def _compare_date_range(self, current_date, date_range_value) -> bool:
        """Compare date against date range"""
        if isinstance(date_range_value, dict):
            start_date = date_range_value.get('start')
            end_date = date_range_value.get('end')

            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if current_date < start_date:
                    return False

            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                if current_date > end_date:
                    return False

            return True
        return False

    def _compare_time_range(self, current_time, time_range_value) -> bool:
        """Compare time against time range"""
        if isinstance(time_range_value, dict):
            start_time = time_range_value.get('start')
            end_time = time_range_value.get('end')

            if start_time:
                start_time = datetime.strptime(start_time, '%H:%M').time()
                if current_time < start_time:
                    return False

            if end_time:
                end_time = datetime.strptime(end_time, '%H:%M').time()
                if current_time > end_time:
                    return False

            return True
        return False

    def _get_cache_key(self, rule, context: Dict[str, Any]) -> str:
        """Generate cache key for rule evaluation"""
        # Create a simplified context hash for caching
        context_parts = []

        if 'user' in context:
            context_parts.append(f"user_{context['user'].get('username', 'anon')}")
        if 'geo' in context:
            context_parts.append(f"geo_{context['geo'].get('country_code', 'unknown')}")
        if 'device' in context:
            context_parts.append(f"device_{context['device'].get('device_type', 'unknown')}")

        context_hash = '_'.join(context_parts)
        return f"visibility_rule_{rule.id}_{context_hash}"