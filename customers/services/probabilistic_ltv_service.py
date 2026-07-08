"""
Probabilistic LTV calculation service using BG/NBD and Gamma-Gamma models
Statistical approach for predicting customer lifetime value
"""

import logging
from datetime import datetime, timedelta
from decimal import Decimal

import pandas as pd
from django.db.models import Count, Sum, Min, Max, F
from django.utils import timezone
from djmoney.money import Money

from customers.models import CustomerMetrics, LTVSettings
from orders.models import Order
from core.utils import get_default_currency

logger = logging.getLogger(__name__)


class ProbabilisticLTVService:
    """Service for calculating LTV using BG/NBD and Gamma-Gamma models"""

    def __init__(self):
        self.bgf_model = None  # BetaGeoFitter model
        self.ggf_model = None  # GammaGammaFitter model
        self.last_fitted = None

    @classmethod
    def check_data_quality(cls):
        """
        Check if there's enough data for probabilistic modeling
        Returns: dict with quality metrics and recommendation
        """
        # Count customers with repeat purchases
        repeat_customers = CustomerMetrics.objects.filter(
            completed_orders__gte=2
        ).count()

        # Count total customers with orders
        total_customers = CustomerMetrics.objects.filter(
            completed_orders__gte=1
        ).count()

        # Check data span (earliest to latest order)
        order_span = Order.objects.filter(
            status='delivered'
        ).aggregate(
            earliest=Min('created_at'),
            latest=Max('created_at')
        )

        data_span_days = 0
        if order_span['earliest'] and order_span['latest']:
            data_span_days = (order_span['latest'] - order_span['earliest']).days

        # Get settings
        settings = LTVSettings.get_settings()
        min_threshold = settings.min_data_quality_threshold

        # Determine if we can use probabilistic
        can_use = (
            repeat_customers >= min_threshold and
            data_span_days >= 180  # At least 6 months of data
        )

        recommendation = 'good'
        if repeat_customers < min_threshold:
            recommendation = 'insufficient_customers'
        elif data_span_days < 180:
            recommendation = 'insufficient_history'
        elif data_span_days < 365:
            recommendation = 'marginal'

        return {
            'repeat_customers': repeat_customers,
            'total_customers': total_customers,
            'data_span_days': data_span_days,
            'min_threshold': min_threshold,
            'can_use_probabilistic': can_use,
            'recommendation': recommendation,
            'quality_score': min(1.0, repeat_customers / max(min_threshold, 1) *
                                  min(1.0, data_span_days / 365))
        }

    @classmethod
    def prepare_transaction_data(cls):
        """
        Prepare transaction data in RFM format for lifetimes library
        Returns: pandas DataFrame with columns: customer_id, frequency, recency, T, monetary_value
        """
        # Get all customers with at least one order
        customers_with_orders = CustomerMetrics.objects.filter(
            completed_orders__gte=1,
            first_purchase_date__isnull=False
        ).select_related('user')

        data = []
        now = timezone.now()

        for metrics in customers_with_orders:
            # Get all completed orders for this customer
            orders = Order.objects.filter(
                user=metrics.user,
                status='delivered'
            ).order_by('created_at')

            if orders.count() < 1:
                continue

            first_order = orders.first()
            last_order = orders.last()

            # Calculate RFM values
            # Frequency: number of repeat purchases (total purchases - 1)
            frequency = orders.count() - 1

            # Recency: time between first and last purchase (in days)
            if frequency > 0:
                recency = (last_order.created_at - first_order.created_at).days
            else:
                recency = 0

            # T: Age of customer (time since first purchase in days)
            T = (now - first_order.created_at).days

            # Monetary value: average order value (excluding first purchase for Gamma-Gamma)
            if frequency > 0:
                repeat_orders = orders.exclude(id=first_order.id)
                monetary_value = float(
                    repeat_orders.aggregate(avg=Sum('total_amount'))['avg'] / frequency
                )
            else:
                # For customers with only one purchase, use that value
                monetary_value = float(first_order.total_amount.amount)

            # Skip if invalid data
            if T <= 0 or monetary_value <= 0:
                continue

            data.append({
                'customer_id': metrics.user.id,
                'frequency': frequency,
                'recency': recency,
                'T': T,
                'monetary_value': monetary_value
            })

        if not data:
            return None

        return pd.DataFrame(data)

    def fit_models(self):
        """
        Fit BG/NBD and Gamma-Gamma models on current customer data
        Returns: dict with fit statistics
        """
        try:
            from lifetimes import BetaGeoFitter, GammaGammaFitter
        except ImportError:
            logger.error("lifetimes library not installed. Run: pip install lifetimes")
            return {
                'success': False,
                'error': 'lifetimes library not installed'
            }

        # Prepare data
        df = self.prepare_transaction_data()

        if df is None or len(df) < 10:
            return {
                'success': False,
                'error': 'Insufficient data for model fitting',
                'customers': 0 if df is None else len(df)
            }

        try:
            # Fit BG/NBD model (predicts future purchase count)
            self.bgf_model = BetaGeoFitter(penalizer_coef=0.01)
            self.bgf_model.fit(
                df['frequency'],
                df['recency'],
                df['T']
            )

            # Fit Gamma-Gamma model (predicts order value)
            # Only use customers with at least one repeat purchase
            repeat_customers = df[df['frequency'] > 0].copy()

            if len(repeat_customers) >= 10:
                self.ggf_model = GammaGammaFitter(penalizer_coef=0.01)
                self.ggf_model.fit(
                    repeat_customers['frequency'],
                    repeat_customers['monetary_value']
                )
            else:
                self.ggf_model = None

            self.last_fitted = timezone.now()

            return {
                'success': True,
                'customers_used': len(df),
                'repeat_customers': len(repeat_customers) if self.ggf_model else 0,
                'fitted_at': self.last_fitted,
                'bgf_params': {
                    'r': float(self.bgf_model.params_['r']),
                    'alpha': float(self.bgf_model.params_['alpha']),
                    'a': float(self.bgf_model.params_['a']),
                    'b': float(self.bgf_model.params_['b'])
                }
            }

        except Exception as e:
            logger.error(f"Error fitting probabilistic models: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def predict_customer_ltv(self, user, time_horizon_days=365):
        """
        Predict LTV for a specific customer
        Args:
            user: User object
            time_horizon_days: Prediction horizon (default 12 months)
        Returns: dict with LTV prediction and metadata
        """
        if not self.bgf_model:
            return {
                'success': False,
                'error': 'Models not fitted. Call fit_models() first.'
            }

        try:
            metrics = CustomerMetrics.objects.get(user=user)
        except CustomerMetrics.DoesNotExist:
            return {
                'success': False,
                'error': 'Customer metrics not found'
            }

        if not metrics.first_purchase_date or metrics.completed_orders < 1:
            return {
                'success': False,
                'error': 'Customer has no completed orders'
            }

        # Get customer's RFM values
        orders = Order.objects.filter(
            user=user,
            status='delivered'
        ).order_by('created_at')

        first_order = orders.first()
        last_order = orders.last()

        frequency = orders.count() - 1
        recency = (last_order.created_at - first_order.created_at).days if frequency > 0 else 0
        T = (timezone.now() - first_order.created_at).days

        if T <= 0:
            return {
                'success': False,
                'error': 'Invalid customer age'
            }

        # Predict probability alive
        probability_alive = float(
            self.bgf_model.conditional_probability_alive(frequency, recency, T)
        )

        # Predict future purchases
        predicted_purchases = float(
            self.bgf_model.conditional_expected_number_of_purchases_up_to_time(
                time_horizon_days,
                frequency,
                recency,
                T
            )
        )

        # Predict average order value
        if self.ggf_model and frequency > 0:
            # Use Gamma-Gamma model
            repeat_orders = orders.exclude(id=first_order.id)
            monetary_value = float(
                repeat_orders.aggregate(avg=Sum('total_amount'))['avg'] / frequency
            )
            predicted_avg_value = float(
                self.ggf_model.conditional_expected_average_profit(frequency, monetary_value)
            )
        else:
            # Fallback to historical average
            predicted_avg_value = float(metrics.average_order_value.amount)

        # Calculate LTV
        predicted_ltv = predicted_purchases * predicted_avg_value

        # Add historical spend
        total_ltv = float(metrics.total_spent.amount) + predicted_ltv

        # Calculate confidence based on customer data
        confidence = self._calculate_confidence(frequency, T, probability_alive)

        return {
            'success': True,
            'ltv': total_ltv,
            'predicted_future_value': predicted_ltv,
            'historical_value': float(metrics.total_spent.amount),
            'probability_alive': probability_alive,
            'predicted_purchases': predicted_purchases,
            'predicted_avg_value': predicted_avg_value,
            'confidence': confidence,
            'time_horizon_days': time_horizon_days
        }

    def _calculate_confidence(self, frequency, T, probability_alive):
        """Calculate confidence score for LTV prediction"""
        # Base confidence on purchase history
        history_confidence = min(1.0, frequency / 10)  # Max at 10 purchases

        # Age confidence (more reliable after 6 months)
        age_confidence = min(1.0, T / 180)

        # Probability alive factor
        alive_confidence = probability_alive

        # Combined confidence
        confidence = (history_confidence * 0.4 + age_confidence * 0.3 + alive_confidence * 0.3)

        return round(confidence, 3)

    def update_all_customer_ltv(self):
        """
        Update LTV for all customers using probabilistic models
        Returns: dict with update statistics
        """
        # First, fit the models
        fit_result = self.fit_models()

        if not fit_result['success']:
            return fit_result

        default_currency = get_default_currency()
        customers_updated = 0
        customers_failed = 0

        # Get all customers with orders
        customers = CustomerMetrics.objects.filter(
            completed_orders__gte=1
        ).select_related('user')

        for metrics in customers:
            # Predict LTV for 12 months
            result = self.predict_customer_ltv(metrics.user, time_horizon_days=365)

            if result['success']:
                # Update customer metrics
                metrics.lifetime_value = Money(result['ltv'], default_currency)
                metrics.probability_alive = result['probability_alive']
                metrics.predicted_purchases_12m = result['predicted_purchases']

                # Also calculate 24-month prediction
                result_24m = self.predict_customer_ltv(metrics.user, time_horizon_days=730)
                if result_24m['success']:
                    metrics.predicted_purchases_24m = result_24m['predicted_purchases']

                metrics.ltv_confidence_score = result['confidence']
                metrics.ltv_calculation_method = 'probabilistic'
                metrics.ltv_last_calculated = timezone.now()

                metrics.save(update_fields=[
                    'lifetime_value',
                    'probability_alive',
                    'predicted_purchases_12m',
                    'predicted_purchases_24m',
                    'ltv_confidence_score',
                    'ltv_calculation_method',
                    'ltv_last_calculated'
                ])
                customers_updated += 1
            else:
                customers_failed += 1

        # Update settings
        settings = LTVSettings.get_settings()
        settings.last_calculation_run = timezone.now()
        settings.save(update_fields=['last_calculation_run'])

        return {
            'success': True,
            'customers_updated': customers_updated,
            'customers_failed': customers_failed,
            'model_fit': fit_result
        }

    @classmethod
    def get_customer_predictions(cls, user):
        """
        Get detailed predictions for a specific customer
        Includes charts data and explanations
        """
        try:
            metrics = CustomerMetrics.objects.get(user=user)
        except CustomerMetrics.DoesNotExist:
            return None

        if metrics.ltv_calculation_method != 'probabilistic':
            return None

        # Get historical order timeline
        orders = Order.objects.filter(
            user=user,
            status='delivered'
        ).order_by('created_at').values('created_at', 'total_amount')

        order_timeline = [
            {
                'date': order['created_at'].strftime('%Y-%m-%d'),
                'amount': float(order['total_amount'])
            }
            for order in orders
        ]

        return {
            'probability_alive': round(metrics.probability_alive * 100, 1),
            'predicted_purchases_12m': round(metrics.predicted_purchases_12m, 1),
            'predicted_purchases_24m': round(metrics.predicted_purchases_24m, 1),
            'confidence_score': round(metrics.ltv_confidence_score * 100, 1),
            'confidence_level': (
                'High' if metrics.ltv_confidence_score >= 0.7
                else 'Medium' if metrics.ltv_confidence_score >= 0.4
                else 'Low'
            ),
            'ltv': float(metrics.lifetime_value.amount),
            'historical_value': float(metrics.total_spent.amount),
            'predicted_future_value': float(metrics.lifetime_value.amount) - float(metrics.total_spent.amount),
            'order_timeline': order_timeline,
            'last_calculated': metrics.ltv_last_calculated
        }
