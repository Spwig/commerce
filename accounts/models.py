from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from custom_fields.mixins import CustomFieldsMixin
from design.models import DesignMixin

User = get_user_model()


class StaffMemberManager(UserManager):
    """Manager that only returns staff users."""

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)


class StaffMember(User):
    """Proxy model for staff-only admin views."""

    objects = StaffMemberManager()

    class Meta:
        proxy = True
        verbose_name = _('Staff Member')
        verbose_name_plural = _('Staff Members')


class CustomerProfile(CustomFieldsMixin, DesignMixin):
    """Extended customer profile with design preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Import tracking
    external_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text="Original customer ID from source platform (WooCommerce, Shopify, etc.)"
    )
    migration_job = models.ForeignKey(
        'migration.MigrationJob',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='imported_customers',
        help_text="Migration job that imported this customer"
    )

    # Personal information
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # B2B / Company Information
    company_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Company Name"),
        help_text=_("Business or company name for B2B customers")
    )

    tax_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Tax ID / VAT Number"),
        help_text=_("Business tax identification number or VAT registration number")
    )

    is_business_customer = models.BooleanField(
        default=False,
        verbose_name=_("Business Customer"),
        help_text=_("Check if this is a business/B2B customer account")
    )

    # Customer dashboard customization
    DASHBOARD_LAYOUTS = [
        ('default', 'Default Layout'),
        ('compact', 'Compact View'),
        ('detailed', 'Detailed View'),
        ('minimal', 'Minimal View'),
        ('cards', 'Card Layout'),
    ]
    
    dashboard_layout = models.CharField(
        max_length=20, 
        choices=DASHBOARD_LAYOUTS, 
        default='default',
        help_text="Customer dashboard layout preference"
    )
    
    # Display preferences
    show_order_history = models.BooleanField(default=True)
    show_wishlist = models.BooleanField(default=True)
    show_recent_products = models.BooleanField(default=True)
    show_recommendations = models.BooleanField(default=True)
    
    # Theme preferences
    preferred_theme = models.ForeignKey(
        'design.Theme',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Customer's preferred site theme"
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    @classmethod
    def get_or_create_for_user(cls, user):
        """Get or create profile for user"""
        profile, created = cls.objects.get_or_create(
            user=user,
            defaults={'user': user}
        )
        return profile
    
    # Customer Analytics Methods
    
    @property
    def customer_metrics(self):
        """Get or create customer metrics"""
        try:
            return self.user.customer_metrics
        except AttributeError:
            # CustomerMetrics model might not be available yet
            return None
    
    @property
    def lifetime_value(self):
        """Get customer lifetime value"""
        from decimal import Decimal, InvalidOperation
        metrics = self.customer_metrics
        if not metrics:
            return Decimal('0')
        try:
            return Decimal(str(metrics.lifetime_value)) if metrics.lifetime_value else Decimal('0')
        except (InvalidOperation, ValueError, TypeError):
            return Decimal('0')

    @property
    def total_spent(self):
        """Get total amount spent by customer"""
        from decimal import Decimal, InvalidOperation
        metrics = self.customer_metrics
        if not metrics:
            return Decimal('0')
        try:
            return Decimal(str(metrics.total_spent)) if metrics.total_spent else Decimal('0')
        except (InvalidOperation, ValueError, TypeError):
            return Decimal('0')
    
    @property
    def total_orders(self):
        """Get total number of orders"""
        return self.user.orders.count()
    
    @property
    def completed_orders_count(self):
        """Get number of completed orders"""
        return self.user.orders.filter(status='delivered').count()
    
    @property
    def average_order_value(self):
        """Calculate average order value"""
        from django.db.models import Avg
        from decimal import Decimal, InvalidOperation
        result = self.user.orders.filter(status='delivered').aggregate(
            avg=Avg('total_amount')
        )['avg']
        if not result:
            return Decimal('0')
        try:
            return Decimal(str(result))
        except (InvalidOperation, ValueError, TypeError):
            return Decimal('0')
    
    @property
    def is_guest_user(self):
        """Check if this is a guest user"""
        return self.user.username.startswith('guest_')

    @property
    def customer_segment(self):
        """Determine customer segment"""
        try:
            from customers.models import CustomerSegment
            return CustomerSegment.determine_segment_for_user(self.user)
        except ImportError:
            return None

    @property
    def days_since_last_order(self):
        """Days since last order"""
        from django.utils import timezone
        last_order = self.user.orders.filter(status='delivered').order_by('-created_at').first()
        if last_order:
            return (timezone.now() - last_order.created_at).days
        return None
    
    @property
    def is_vip_customer(self):
        """Check if customer qualifies as VIP"""
        segment = self.customer_segment
        return segment and segment.name in ['vip', 'high_value'] if segment else False
    
    @property
    def is_at_risk(self):
        """Check if customer is at risk of churning"""
        days_since_last = self.days_since_last_order
        if days_since_last is None:
            return False
        
        # Consider at risk if no purchase in last 90 days and has previous orders
        if days_since_last > 90 and self.completed_orders_count > 0:
            return True
            
        return False
    
    @property
    def purchase_frequency(self):
        """Calculate purchase frequency (orders per month)"""
        from django.utils import timezone
        from datetime import timedelta
        
        completed_orders = self.user.orders.filter(status='delivered')
        if completed_orders.count() < 2:
            return 0
        
        first_order = completed_orders.earliest('created_at')
        last_order = completed_orders.latest('created_at')
        
        days_active = (last_order.created_at - first_order.created_at).days
        if days_active > 0:
            orders_per_day = completed_orders.count() / days_active
            return orders_per_day * 30  # Convert to per month
        
        return 0
    
    @property
    def favorite_categories(self):
        """Get customer's most purchased categories"""
        from django.db.models import Count
        from orders.models import OrderItem
        
        categories = OrderItem.objects.filter(
            order__user=self.user,
            order__status='delivered'
        ).values(
            'product__category__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:3]
        
        return [cat['product__category__name'] for cat in categories if cat['product__category__name']]
    
    @property
    def abandoned_carts_count(self):
        """Get count of abandoned carts"""
        try:
            return self.user.abandoned_carts.count()
        except AttributeError:
            # Count carts that haven't been updated in 24+ hours and have items
            from cart.models import Cart
            from django.utils import timezone
            from datetime import timedelta
            
            return Cart.objects.filter(
                user=self.user,
                items__isnull=False,
                updated_at__lt=timezone.now() - timedelta(hours=24)
            ).distinct().count()
    
    @property
    def wishlist_items_count(self):
        """Get count of items in wishlist"""
        try:
            wishlist = self.user.wishlist_set.first()
            return wishlist.items.count() if wishlist else 0
        except:
            return 0
    
    def get_customer_summary(self):
        """Get comprehensive customer summary"""
        return {
            'profile': self,
            'total_spent': self.total_spent,
            'lifetime_value': self.lifetime_value,
            'total_orders': self.total_orders,
            'completed_orders': self.completed_orders_count,
            'average_order_value': self.average_order_value,
            'customer_segment': self.customer_segment,
            'days_since_last_order': self.days_since_last_order,
            'is_vip': self.is_vip_customer,
            'is_at_risk': self.is_at_risk,
            'purchase_frequency': self.purchase_frequency,
            'favorite_categories': self.favorite_categories,
            'abandoned_carts': self.abandoned_carts_count,
            'wishlist_items': self.wishlist_items_count,
        }
    
    def refresh_metrics(self):
        """Refresh cached customer metrics"""
        try:
            from customers.models import CustomerMetrics
            return CustomerMetrics.calculate_for_user(self.user)
        except ImportError:
            return None


class OAuthProviderSettings(models.Model):
    """Merchant-specific OAuth provider settings for social authentication"""

    PROVIDER_CHOICES = [
        ('google', 'Google'),
        ('apple', 'Apple'),
        ('microsoft', 'Microsoft'),
    ]

    provider = models.CharField(
        max_length=50,
        choices=PROVIDER_CHOICES,
        unique=True,
        help_text="OAuth provider type"
    )
    enabled = models.BooleanField(
        default=False,
        help_text="Enable this provider for customer authentication"
    )
    display_name = models.CharField(
        max_length=100,
        help_text="Display name shown on login button"
    )
    button_order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    custom_scopes = models.JSONField(
        default=list,
        blank=True,
        help_text="Additional OAuth scopes (JSON array)"
    )

    # Configuration status (auto-calculated)
    is_configured = models.BooleanField(
        default=False,
        editable=False,
        help_text="Whether OAuth credentials are configured"
    )
    configuration_notes = models.TextField(
        blank=True,
        help_text="Setup notes or troubleshooting information"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OAuth Provider Setting"
        verbose_name_plural = "OAuth Provider Settings"
        ordering = ['button_order', 'provider']

    def __str__(self):
        status = 'Enabled' if self.enabled else 'Disabled'
        configured = 'Configured' if self.is_configured else 'Not Configured'
        return f"{self.get_provider_display()} - {status} ({configured})"

    def save(self, *args, **kwargs):
        """Check if provider has credentials configured"""
        try:
            from allauth.socialaccount.models import SocialApp
            social_app = SocialApp.objects.filter(provider=self.provider).first()
            self.is_configured = bool(
                social_app and
                social_app.client_id and
                (social_app.secret or self.provider == 'apple')  # Apple uses key file
            )
        except Exception:
            self.is_configured = False

        # Set default display name if not provided
        if not self.display_name:
            self.display_name = self.get_provider_display()

        super().save(*args, **kwargs)


class CommunicationPreference(models.Model):
    """
    Customer communication preferences with GDPR compliance.

    Centralized preference management for email, SMS, and app-specific communications.
    Includes consent tracking, verification, and unsubscribe mechanisms.
    """

    # Core fields
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='communication_preferences',
        verbose_name=_("User")
    )

    # Master channel toggles
    email_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Email enabled"),
        help_text=_("Master toggle for all email communications")
    )
    sms_enabled = models.BooleanField(
        default=False,
        verbose_name=_("SMS enabled"),
        help_text=_("Master toggle for all SMS communications (opt-in required)")
    )

    # Category toggles (GDPR requires separate consent for marketing)
    email_transactional = models.BooleanField(
        default=True,
        verbose_name=_("Transactional emails"),
        help_text=_("Order confirmations, shipping updates, account security emails")
    )
    email_marketing = models.BooleanField(
        default=False,
        verbose_name=_("Marketing emails"),
        help_text=_("Newsletters, promotions, product recommendations (opt-in required)")
    )
    sms_transactional = models.BooleanField(
        default=False,
        verbose_name=_("Transactional SMS"),
        help_text=_("Order and shipping notifications via SMS (opt-in required)")
    )
    sms_marketing = models.BooleanField(
        default=False,
        verbose_name=_("Marketing SMS"),
        help_text=_("Marketing messages via SMS (opt-in required)")
    )

    # App-specific preferences (flexible JSON structure)
    app_preferences = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("App preferences"),
        help_text=_(
            "App-specific communication preferences stored as JSON. "
            "Example: {\"blog\": {\"enabled\": true, \"frequency\": \"weekly\"}, "
            "\"loyalty\": {\"points_earned\": true, \"tier_changes\": true}}"
        )
    )

    # Verification (double opt-in)
    email_verified = models.BooleanField(
        default=False,
        verbose_name=_("Email verified"),
        help_text=_("Whether marketing email address has been verified via double opt-in")
    )
    email_verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Email verified at"),
        help_text=_("Timestamp when email was verified")
    )
    sms_verified = models.BooleanField(
        default=False,
        verbose_name=_("SMS verified"),
        help_text=_("Whether SMS number has been verified")
    )
    sms_verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("SMS verified at"),
        help_text=_("Timestamp when SMS number was verified")
    )

    # SMS verification code (TCPA double opt-in)
    sms_verification_code = models.CharField(
        max_length=6,
        blank=True,
        default='',
        verbose_name=_("SMS verification code"),
        help_text=_("6-digit OTP code for SMS verification")
    )
    sms_verification_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("SMS verification sent at"),
        help_text=_("When the verification code was sent")
    )
    sms_verification_attempts = models.PositiveIntegerField(
        default=0,
        verbose_name=_("SMS verification attempts"),
        help_text=_("Number of failed verification attempts")
    )

    # Consent tracking (GDPR Article 7)
    CONSENT_SOURCE_CHOICES = [
        ('registration', _('Account Registration')),
        ('checkout', _('Checkout Process')),
        ('preference_center', _('Preference Center')),
        ('api', _('API')),
        ('admin', _('Admin Override')),
        ('migration', _('Data Migration')),
    ]

    consent_source = models.CharField(
        max_length=50,
        choices=CONSENT_SOURCE_CHOICES,
        default='registration',
        verbose_name=_("Consent source"),
        help_text=_("How the user's consent was obtained")
    )
    consent_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("Consent IP address"),
        help_text=_("IP address when consent was given (GDPR requirement)")
    )
    consent_user_agent = models.TextField(
        blank=True,
        verbose_name=_("Consent user agent"),
        help_text=_("Browser user agent when consent was given (GDPR requirement)")
    )
    consent_timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Consent timestamp"),
        help_text=_("When consent was originally given (GDPR requirement)")
    )

    # Unsubscribe tokens (one-click unsubscribe)
    unsubscribe_token = models.CharField(
        max_length=64,
        unique=True,
        blank=True,
        verbose_name=_("Unsubscribe token"),
        help_text=_("Unique token for one-click unsubscribe links")
    )

    # Language preference
    language_code = models.CharField(
        max_length=10,
        default='en',
        verbose_name=_("Language code"),
        help_text=_("Preferred language for communications (ISO 639-1)")
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )

    class Meta:
        verbose_name = _("Communication Preference")
        verbose_name_plural = _("Communication Preferences")
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['unsubscribe_token']),
            models.Index(fields=['email_verified', 'email_marketing']),
            models.Index(fields=['sms_verified', 'sms_marketing']),
        ]

    def __str__(self):
        return f"Preferences for {self.user.email}"

    def save(self, *args, **kwargs):
        """Generate unsubscribe token on creation"""
        if not self.unsubscribe_token:
            import secrets
            self.unsubscribe_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    @classmethod
    def get_default_app_preferences(cls):
        """Get default app preferences structure"""
        return {
            'blog': {
                'enabled': True,
                'frequency': 'weekly',  # immediate, weekly, monthly
                'categories': [],
            },
            'loyalty': {
                'enabled': True,
                'frequency': 'immediate',
                'points_earned': True,
                'tier_changes': True,
                'rewards_available': True,
                'points_expiring': True,
                'birthday_bonus': True,
                'campaign_offers': False,  # Opt-in required for campaigns
            },
            'referrals': {
                'enabled': True,
                'reward_issued': True,
                'referral_converted': True,
                'reward_expiring': True,
            },
            'affiliate': {
                'enabled': True,
                'commission_earned': True,
                'payout_processed': True,
                'monthly_report': True,
            },
        }

    @classmethod
    def get_or_create_for_user(cls, user):
        """
        Get or create preferences for user with defaults.

        Args:
            user: User instance

        Returns:
            Tuple of (CommunicationPreference, created)
        """
        from django.utils.translation import get_language
        prefs, created = cls.objects.get_or_create(
            user=user,
            defaults={
                'app_preferences': cls.get_default_app_preferences(),
                'consent_source': 'registration',
                'consent_timestamp': timezone.now(),
                'language_code': get_language() or 'en',
            }
        )

        # Ensure app_preferences has all default keys (for existing records)
        if created or not prefs.app_preferences:
            prefs.app_preferences = cls.get_default_app_preferences()
            prefs.save(update_fields=['app_preferences'])

        return prefs, created

    def should_send_email(self, message_type):
        """
        Check if user should receive email for given message type.

        Args:
            message_type: Email type key (e.g., 'order_confirmation', 'newsletter')

        Returns:
            bool: True if email should be sent
        """
        from .constants import get_message_type_category, is_locked_message_type

        # Check global email toggle
        if not self.email_enabled:
            return False

        # Locked messages (transactional) always send if email_transactional is enabled
        if is_locked_message_type(message_type):
            return self.email_transactional

        # Get message category
        category, app = get_message_type_category(message_type)

        # Marketing emails require verification
        if category == 'marketing':
            return self.email_marketing and self.email_verified

        # App-specific emails
        if category == 'app_specific' and app:
            # Requires marketing consent + app enabled
            if not (self.email_marketing and self.email_verified):
                return False

            app_prefs = self.app_preferences.get(app, {})
            if not app_prefs.get('enabled', False):
                return False

            # Check specific message type preference if it exists
            # Extract the preference key from message type (e.g., 'loyalty_points_earned' -> 'points_earned')
            pref_key = message_type.replace(f'{app}_', '')
            return app_prefs.get(pref_key, True)  # Default to True if not specified

        # Unknown category - default to requiring marketing consent
        return self.email_marketing and self.email_verified

    def should_send_sms(self, message_type):
        """
        Check if user should receive SMS for given message type.

        All SMS requires explicit opt-in (TCPA compliance).

        Args:
            message_type: SMS type key

        Returns:
            bool: True if SMS should be sent
        """
        from .constants import get_message_type_category

        # Check global SMS toggle
        if not self.sms_enabled:
            return False

        # SMS requires verification for ALL types (TCPA compliance)
        if not self.sms_verified:
            return False

        # Get message category
        category, _ = get_message_type_category(message_type)

        if category == 'transactional':
            return self.sms_transactional
        elif category == 'marketing':
            return self.sms_marketing

        # Unknown - default to False (safer for SMS)
        return False

    def get_app_preference(self, app, key, default=None):
        """
        Get a specific app preference value.

        Args:
            app: App name (e.g., 'blog', 'loyalty')
            key: Preference key (e.g., 'frequency', 'points_earned')
            default: Default value if not found

        Returns:
            Preference value or default
        """
        app_prefs = self.app_preferences.get(app, {})
        return app_prefs.get(key, default)

    def update_app_preference(self, app, updates):
        """
        Update app-specific preferences.

        Args:
            app: App name (e.g., 'blog', 'loyalty')
            updates: Dict of preference updates
        """
        if app not in self.app_preferences:
            self.app_preferences[app] = {}

        self.app_preferences[app].update(updates)
        self.save(update_fields=['app_preferences', 'updated_at'])


class PreferenceChangeLog(models.Model):
    """
    Audit trail for communication preference changes.

    Tracks every change to customer communication preferences for GDPR Article 7
    compliance (proof of consent) and customer transparency.
    """

    # Source choices for preference changes
    SOURCE_CHOICES = [
        ('user', _('User')),
        ('registration', _('Registration')),
        ('checkout', _('Checkout')),
        ('api', _('API')),
        ('admin', _('Admin')),
        ('verification', _('Email Verification')),
        ('unsubscribe', _('Unsubscribe Link')),
        ('system', _('System')),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='preference_changes',
        verbose_name=_('User'),
        help_text=_('User whose preference was changed')
    )

    preference = models.ForeignKey(
        CommunicationPreference,
        on_delete=models.CASCADE,
        related_name='change_logs',
        verbose_name=_('Preference'),
        help_text=_('Communication preference that was changed')
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Timestamp'),
        help_text=_('When the change occurred')
    )

    action = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_('Action'),
        help_text=_('Description of the change (e.g., "email_marketing.enable")')
    )

    old_value = models.JSONField(
        default=dict,
        verbose_name=_('Old Value'),
        help_text=_('Previous state before the change')
    )

    new_value = models.JSONField(
        default=dict,
        verbose_name=_('New Value'),
        help_text=_('New state after the change')
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('IP Address'),
        help_text=_('IP address from which the change was made')
    )

    user_agent = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name=_('User Agent'),
        help_text=_('Browser user agent string')
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        verbose_name=_('Source'),
        help_text=_('Where the change originated from')
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes'),
        help_text=_('Additional context or notes about the change')
    )

    class Meta:
        verbose_name = _('Preference Change Log')
        verbose_name_plural = _('Preference Change Logs')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp'], name='pref_log_user_time'),
            models.Index(fields=['action', '-timestamp'], name='pref_log_action_time'),
            models.Index(fields=['preference', '-timestamp'], name='pref_log_pref_time'),
            models.Index(fields=['-timestamp'], name='pref_log_time'),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.timestamp}"

    @property
    def change_summary(self):
        """Human-readable summary of what changed (old → new)."""
        if not self.old_value and not self.new_value:
            return ''
        if not self.old_value:
            parts = [f"{k}: {v}" for k, v in self.new_value.items()
                     if not k.startswith('_')]
            return ', '.join(parts[:5])
        if not self.new_value:
            return ''
        changes = []
        all_keys = set(list(self.old_value.keys()) + list(self.new_value.keys()))
        for key in sorted(all_keys):
            if key.startswith('_'):
                continue
            old_v = self.old_value.get(key)
            new_v = self.new_value.get(key)
            if old_v != new_v:
                old_display = str(old_v).lower() if isinstance(old_v, bool) else (
                    str(old_v) if old_v is not None else 'none')
                new_display = str(new_v).lower() if isinstance(new_v, bool) else (
                    str(new_v) if new_v is not None else 'none')
                changes.append(f"{key}: {old_display} \u2192 {new_display}")
        return ', '.join(changes[:5]) if changes else ''

    @classmethod
    def cleanup_old_logs(cls, days=90):
        """
        Delete preference change logs older than the specified number of days.

        Args:
            days: Number of days to retain logs (default: 90)

        Returns:
            int: Number of logs deleted
        """
        from django.utils import timezone
        from datetime import timedelta

        cutoff_date = timezone.now() - timedelta(days=days)
        deleted_count, _ = cls.objects.filter(timestamp__lt=cutoff_date).delete()

        return deleted_count