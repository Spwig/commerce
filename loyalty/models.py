"""
Loyalty Program Models

Core data models for the Spwig loyalty and rewards system.
Implements a ledger-based points system with tiering, badges, and redemptions.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid

User = get_user_model()


class LoyaltyMember(models.Model):
    """
    Links a customer to the loyalty program.

    Each customer can only be enrolled once. Tracks enrollment date,
    current tier, and active status.
    """

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # External reference UUID for API use
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="External reference UUID for API access"
    )

    # Customer relationship
    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='loyalty_member',
        help_text="Customer enrolled in loyalty program"
    )

    # Enrollment tracking
    enrolled_at = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time of loyalty program enrollment"
    )

    # Current tier (set to null if no tiering system active)
    current_tier = models.ForeignKey(
        'LoyaltyTier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        help_text="Current tier membership"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether member is active in the program"
    )

    # Grace period tracking
    grace_period_started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When member first fell below tier threshold (for grace period tracking)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loyalty Member"
        verbose_name_plural = "Loyalty Members"
        indexes = [
            models.Index(fields=['customer', 'is_active']),
            models.Index(fields=['enrolled_at']),
            models.Index(fields=['current_tier']),
        ]

    def __str__(self):
        name = self.customer.get_full_name() or self.customer.username
        return f"{name} - Member #{self.id}"

    def __repr__(self):
        return f"<LoyaltyMember id={self.id} customer={self.customer.username} tier={self.current_tier}>"

    def get_next_tier(self):
        """Get the next tier this member can achieve."""
        if not self.current_tier:
            # No tier yet, return lowest rank tier
            return LoyaltyTier.objects.filter(is_active=True).order_by('rank').first()

        # Get next tier (lower rank number = higher tier)
        return LoyaltyTier.objects.filter(
            is_active=True,
            rank__lt=self.current_tier.rank
        ).order_by('-rank').first()


class LoyaltyBalance(models.Model):
    """
    Cached points balance for a loyalty member.

    This is a performance optimization - the authoritative source
    is the LoyaltyTransaction ledger. Balances are recalculated
    from the ledger periodically or on-demand.
    """

    # Member relationship (one-to-one)
    member = models.OneToOneField(
        LoyaltyMember,
        on_delete=models.CASCADE,
        related_name='balance',
        primary_key=True,
        help_text="Loyalty member this balance belongs to"
    )

    # Points balance
    available_points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Currently available points for redemption"
    )

    pending_points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Points earned but not yet available (pending refund window)"
    )

    lifetime_earned = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total points earned over lifetime (including expired/redeemed)"
    )

    lifetime_redeemed = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total points redeemed over lifetime"
    )

    lifetime_expired = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total points expired over lifetime"
    )

    # Timestamps
    last_earned_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last time points were earned"
    )

    last_redeemed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last time points were redeemed"
    )

    last_recalculated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time balance was recalculated from ledger"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loyalty Balance"
        verbose_name_plural = "Loyalty Balances"
        indexes = [
            models.Index(fields=['available_points']),
            models.Index(fields=['last_earned_at']),
        ]

    def __str__(self):
        return f"{self.member} - {self.available_points} points"

    def __repr__(self):
        return f"<LoyaltyBalance member={self.member.id} available={self.available_points}>"

    @property
    def total_points(self):
        """Total points including pending"""
        return self.available_points + self.pending_points


class LoyaltyTransaction(models.Model):
    """
    Immutable ledger of all point changes.

    This is the authoritative source for all points. Each transaction
    records a single point change with full audit trail. Transactions
    are never updated or deleted - only new compensating entries are added.
    """

    # Transaction types
    TYPE_EARN = 'earn'
    TYPE_REDEEM = 'redeem'
    TYPE_EXPIRE = 'expire'
    TYPE_REVOKE = 'revoke'
    TYPE_ADJUSTMENT = 'adjustment'
    TYPE_BONUS = 'bonus'

    TRANSACTION_TYPES = [
        (TYPE_EARN, 'Earned'),
        (TYPE_REDEEM, 'Redeemed'),
        (TYPE_EXPIRE, 'Expired'),
        (TYPE_REVOKE, 'Revoked'),
        (TYPE_ADJUSTMENT, 'Manual Adjustment'),
        (TYPE_BONUS, 'Bonus'),
    ]

    # Status choices
    STATUS_PENDING = 'pending'
    STATUS_AVAILABLE = 'available'
    STATUS_EXPIRED = 'expired'
    STATUS_REDEEMED = 'redeemed'
    STATUS_REVOKED = 'revoked'

    TRANSACTION_STATUSES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_EXPIRED, 'Expired'),
        (STATUS_REDEEMED, 'Redeemed'),
        (STATUS_REVOKED, 'Revoked'),
    ]

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # External reference UUID
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="External reference UUID for API access"
    )

    # Member relationship
    member = models.ForeignKey(
        LoyaltyMember,
        on_delete=models.PROTECT,  # Never delete transactions
        related_name='transactions',
        db_index=True,
        help_text="Loyalty member this transaction belongs to"
    )

    # Transaction details
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        db_index=True,
        help_text="Type of transaction"
    )

    points = models.IntegerField(
        help_text="Points amount (positive for earn/bonus, negative for redeem/expire)"
    )

    status = models.CharField(
        max_length=20,
        choices=TRANSACTION_STATUSES,
        default=STATUS_AVAILABLE,
        db_index=True,
        help_text="Current status of transaction"
    )

    # Context and metadata
    description = models.TextField(
        help_text="Human-readable description of transaction"
    )

    reason = models.CharField(
        max_length=255,
        blank=True,
        help_text="Brief reason for transaction (e.g., 'Order #1234', 'Birthday bonus')"
    )

    # Related objects (generic references)
    related_object_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Type of related object (e.g., 'order', 'redemption', 'campaign')"
    )

    related_object_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="ID of related object"
    )

    # Expiration tracking
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="When these points expire (null = never)"
    )

    # Reversal tracking
    reversal_of = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reversals',
        help_text="Original transaction being reversed (for revoke transactions)"
    )

    # Admin tracking
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loyalty_transactions_created',
        help_text="Admin user who created this transaction (for manual adjustments)"
    )

    admin_note = models.TextField(
        blank=True,
        help_text="Admin notes for manual adjustments"
    )

    # Timestamps (immutable - no updated_at)
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="When transaction was created"
    )

    class Meta:
        verbose_name = "Loyalty Transaction"
        verbose_name_plural = "Loyalty Transactions"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['member', 'transaction_type']),
            models.Index(fields=['member', 'status']),
            models.Index(fields=['member', 'created_at']),
            models.Index(fields=['transaction_type', 'created_at']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['related_object_type', 'related_object_id']),
        ]

    def __str__(self):
        return f"{self.member} - {self.transaction_type}: {self.points} points"

    def __repr__(self):
        return f"<LoyaltyTransaction id={self.id} member={self.member.id} type={self.transaction_type} points={self.points}>"

    def save(self, *args, **kwargs):
        """Override save to enforce immutability"""
        if self.pk is not None:
            raise ValueError("LoyaltyTransaction objects are immutable and cannot be updated")
        super().save(*args, **kwargs)


class LoyaltyTier(models.Model):
    """
    Defines tier levels and their associated benefits.

    Tiers provide status-based rewards and multipliers. Members progress
    through tiers based on spend, order count, or points earned.
    """

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # External reference UUID
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="External reference UUID for API access"
    )

    # Tier identification
    name = models.CharField(
        max_length=100,
        help_text="Tier name (e.g., 'Bronze', 'Silver', 'Gold', 'Platinum')"
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL-friendly identifier"
    )

    # Display
    description = models.TextField(
        blank=True,
        help_text="Description of tier benefits"
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome icon class (e.g., 'fa-medal', 'fa-crown')"
    )

    color = models.CharField(
        max_length=7,
        blank=True,
        help_text="Hex color code for tier badge (e.g., '#CD7F32' for bronze)"
    )

    # Tier ordering and requirements
    rank = models.IntegerField(
        unique=True,
        help_text="Tier order (lower rank = higher tier)"
    )

    # Entry criteria (one must be met)
    min_spend = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Minimum spend required to reach this tier"
    )

    min_orders = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Minimum order count required to reach this tier"
    )

    min_points_earned = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Minimum lifetime points earned to reach this tier"
    )

    # Tier benefits
    points_multiplier = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal('1.00'),
        validators=[MinValueValidator(Decimal('1.00'))],
        help_text="Points earning multiplier (e.g., 1.5 for 50% bonus)"
    )

    has_free_shipping = models.BooleanField(
        default=False,
        help_text="Whether tier includes free shipping"
    )

    has_early_access = models.BooleanField(
        default=False,
        help_text="Whether tier gets early access to sales/products"
    )

    # Grace period settings
    grace_period_days = models.IntegerField(
        default=30,
        validators=[MinValueValidator(0)],
        help_text="Days before demotion after falling below threshold"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether tier is active"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loyalty Tier"
        verbose_name_plural = "Loyalty Tiers"
        ordering = ['rank']
        indexes = [
            models.Index(fields=['rank', 'is_active']),
            models.Index(fields=['min_spend']),
            models.Index(fields=['min_orders']),
        ]

    def __str__(self):
        return f"{self.name} (Rank {self.rank})"

    def __repr__(self):
        return f"<LoyaltyTier id={self.id} name={self.name} rank={self.rank}>"


class LoyaltyBadge(models.Model):
    """
    Defines achievement badges that members can earn.

    Badges are awarded for specific actions, milestones, or achievements.
    They provide gamification and recognition elements to the loyalty program.
    """

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # External reference UUID
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="External reference UUID for API access"
    )

    # Badge identification
    name = models.CharField(
        max_length=100,
        help_text="Badge name (e.g., 'First Purchase', 'Social Sharer', 'VIP Customer')"
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL-friendly identifier"
    )

    # Display
    description = models.TextField(
        help_text="What this badge represents"
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome icon class (e.g., 'fa-star', 'fa-trophy')"
    )

    image = models.ForeignKey(
        'media_library.MediaAsset',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='badge_uses',
        help_text="Custom badge image from media library. If provided, this takes priority over icon."
    )

    # Badge criteria types
    CRITERIA_PROGRAM_JOIN = 'program_join'
    CRITERIA_FIRST_PURCHASE = 'first_purchase'
    CRITERIA_ORDER_COUNT = 'order_count'
    CRITERIA_TOTAL_SPEND = 'total_spend'
    CRITERIA_REVIEW_COUNT = 'review_count'
    CRITERIA_SOCIAL_SHARE = 'social_share'
    CRITERIA_MONTHLY_STREAK = 'monthly_streak'
    CRITERIA_REFERRALS = 'referrals'
    CRITERIA_BIRTHDAY_PURCHASE = 'birthday_purchase'
    CRITERIA_WISHLIST_ITEMS = 'wishlist_items'
    CRITERIA_EARLY_MORNING_ORDERS = 'early_morning_orders'
    CRITERIA_LATE_NIGHT_ORDERS = 'late_night_orders'
    CRITERIA_WEEKEND_ORDERS = 'weekend_orders'
    CRITERIA_QUICK_RETURN = 'quick_return'
    CRITERIA_SINGLE_ORDER_VALUE = 'single_order_value'
    CRITERIA_ITEMS_PER_ORDER = 'items_per_order'
    CRITERIA_ORDERS_PER_MONTH = 'orders_per_month'

    CRITERIA_TYPE_CHOICES = [
        (CRITERIA_PROGRAM_JOIN, _('Program Join - Member enrolled in loyalty program')),
        (CRITERIA_FIRST_PURCHASE, _('First Purchase - Made their first order')),
        (CRITERIA_ORDER_COUNT, _('Order Count - Placed specified number of orders')),
        (CRITERIA_TOTAL_SPEND, _('Total Spend - Reached total spend amount')),
        (CRITERIA_REVIEW_COUNT, _('Review Count - Submitted specified number of reviews')),
        (CRITERIA_SOCIAL_SHARE, _('Social Share - Shared on social media')),
        (CRITERIA_MONTHLY_STREAK, _('Monthly Streak - Purchased every month consecutively')),
        (CRITERIA_REFERRALS, _('Referrals - Referred specified number of customers')),
        (CRITERIA_BIRTHDAY_PURCHASE, _('Birthday Purchase - Made purchase on birthday')),
        (CRITERIA_WISHLIST_ITEMS, _('Wishlist Items - Added items to wishlist')),
        (CRITERIA_EARLY_MORNING_ORDERS, _('Early Morning Orders - Orders before 9 AM')),
        (CRITERIA_LATE_NIGHT_ORDERS, _('Late Night Orders - Orders after 9 PM')),
        (CRITERIA_WEEKEND_ORDERS, _('Weekend Orders - Orders on Saturday/Sunday')),
        (CRITERIA_QUICK_RETURN, _('Quick Return - Purchased within 24h of previous order')),
        (CRITERIA_SINGLE_ORDER_VALUE, _('Single Order Value - Placed high-value single order')),
        (CRITERIA_ITEMS_PER_ORDER, _('Items Per Order - Order with many items')),
        (CRITERIA_ORDERS_PER_MONTH, _('Orders Per Month - Multiple orders in one month')),
    ]

    # Badge criteria
    criteria_type = models.CharField(
        max_length=50,
        choices=CRITERIA_TYPE_CHOICES,
        help_text="Type of achievement that earns this badge"
    )

    criteria_value = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text=_(
            "Target value for achievement. Examples: "
            "5 for '5 orders', 100 for '$100 spent', "
            "3 for '3 consecutive months', etc."
        )
    )

    # Rewards
    points_reward = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Points awarded when badge is earned"
    )

    # Display settings
    is_visible = models.BooleanField(
        default=True,
        help_text="Whether badge is visible to members before earning"
    )

    display_order = models.IntegerField(
        default=0,
        help_text="Display order in badge gallery"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether badge can be earned"
    )

    # Awarding behavior
    auto_award = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether badge is automatically awarded when criteria is met. If False, badge can only be awarded through campaigns."
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loyalty Badge"
        verbose_name_plural = "Loyalty Badges"
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['criteria_type', 'is_active', 'auto_award']),
            models.Index(fields=['display_order']),
            models.Index(fields=['auto_award', 'is_active']),
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<LoyaltyBadge id={self.id} name={self.name} type={self.criteria_type}>"


class LoyaltyMemberBadge(models.Model):
    """
    Tracks badges earned by loyalty members.

    Maps members to badges they've achieved with timestamp tracking.
    """

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # Relationships
    member = models.ForeignKey(
        LoyaltyMember,
        on_delete=models.CASCADE,
        related_name='badges_earned',
        help_text="Member who earned the badge"
    )

    badge = models.ForeignKey(
        LoyaltyBadge,
        on_delete=models.CASCADE,
        related_name='earned_by',
        help_text="Badge that was earned"
    )

    # Tracking
    earned_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When badge was earned"
    )

    # Related transaction (if points were awarded)
    transaction = models.ForeignKey(
        LoyaltyTransaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='badge_awards',
        help_text="Associated points transaction"
    )

    class Meta:
        verbose_name = "Member Badge"
        verbose_name_plural = "Member Badges"
        unique_together = [['member', 'badge']]
        ordering = ['-earned_at']
        indexes = [
            models.Index(fields=['member', 'earned_at']),
            models.Index(fields=['badge', 'earned_at']),
        ]

    def __str__(self):
        return f"{self.member} - {self.badge.name}"

    def __repr__(self):
        return f"<LoyaltyMemberBadge member={self.member.id} badge={self.badge.id}>"


class LoyaltyRule(models.Model):
    """
    Defines rules for earning loyalty points.

    Rules determine when and how many points are awarded based on customer
    actions, purchases, or events. Supports spend-based, item-based, action-based,
    and event-based rules with various conditions and caps.
    """

    # Rule types
    TYPE_SPEND_BASED = 'spend_based'
    TYPE_ITEM_BASED = 'item_based'
    TYPE_ACTION_BASED = 'action_based'
    TYPE_EVENT_BASED = 'event_based'

    RULE_TYPES = [
        (TYPE_SPEND_BASED, 'Spend-Based'),
        (TYPE_ITEM_BASED, 'Item-Based'),
        (TYPE_ACTION_BASED, 'Action-Based'),
        (TYPE_EVENT_BASED, 'Event-Based'),
    ]

    # Action types (for action-based rules)
    ACTION_SIGNUP = 'signup'
    ACTION_REVIEW = 'review'
    ACTION_SOCIAL_SHARE = 'social_share'
    ACTION_BIRTHDAY = 'birthday'
    ACTION_REFERRAL = 'referral'

    ACTION_TYPES = [
        (ACTION_SIGNUP, 'Sign Up'),
        (ACTION_REVIEW, 'Write Review'),
        (ACTION_SOCIAL_SHARE, 'Social Share'),
        (ACTION_BIRTHDAY, 'Birthday'),
        (ACTION_REFERRAL, 'Referral'),
    ]

    # Event types (for event-based rules)
    EVENT_FIRST_PURCHASE = 'first_purchase'
    EVENT_NTH_PURCHASE = 'nth_purchase'
    EVENT_ANNIVERSARY = 'anniversary'

    EVENT_TYPES = [
        (EVENT_FIRST_PURCHASE, 'First Purchase'),
        (EVENT_NTH_PURCHASE, 'Nth Purchase'),
        (EVENT_ANNIVERSARY, 'Anniversary'),
    ]

    # Scope types
    SCOPE_ALL = 'all'
    SCOPE_CATEGORY = 'category'
    SCOPE_PRODUCT = 'product'
    SCOPE_BRAND = 'brand'

    SCOPE_TYPES = [
        (SCOPE_ALL, 'All Products'),
        (SCOPE_CATEGORY, 'Specific Category'),
        (SCOPE_PRODUCT, 'Specific Product'),
        (SCOPE_BRAND, 'Specific Brand'),
    ]

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # External reference UUID
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="External reference UUID for API access"
    )

    # Rule identification
    name = models.CharField(
        max_length=255,
        help_text="Rule name (e.g., 'Standard Purchase Points', 'Birthday Bonus')"
    )

    description = models.TextField(
        blank=True,
        help_text="Description of what this rule does"
    )

    # Rule type and configuration
    rule_type = models.CharField(
        max_length=50,
        choices=RULE_TYPES,
        db_index=True,
        help_text="Type of rule"
    )

    # For action-based rules
    action_type = models.CharField(
        max_length=50,
        choices=ACTION_TYPES,
        blank=True,
        help_text="Specific action type (for action-based rules)"
    )

    # For event-based rules
    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPES,
        blank=True,
        help_text="Specific event type (for event-based rules)"
    )

    # Scope configuration
    scope = models.CharField(
        max_length=50,
        choices=SCOPE_TYPES,
        default=SCOPE_ALL,
        help_text="What this rule applies to"
    )

    # Scope filters (JSON field for flexibility)
    scope_filters = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional scope filters (category IDs, product IDs, etc.)"
    )

    # Points calculation
    points_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('1.00'),
        help_text="Points per dollar spent (for spend-based) or fixed points (for others)"
    )

    # Minimum requirements
    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Minimum order amount to qualify"
    )

    # Caps and limits
    max_points_per_order = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Maximum points per order (null = no limit)"
    )

    max_points_per_day = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Maximum points per member per day (null = no limit)"
    )

    max_points_per_member = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Maximum points per member total (null = no limit)"
    )

    # Priority and exclusivity
    priority = models.IntegerField(
        default=100,
        help_text="Rule priority (lower = higher priority, evaluated first)"
    )

    is_exclusive = models.BooleanField(
        default=False,
        help_text="If true, no other rules apply when this one matches"
    )

    # Points availability
    points_pending_days = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Days before points become available (0 = immediate)"
    )

    # Expiration
    points_expire_days = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Days until earned points expire (null = never)"
    )

    # Tier restrictions
    allowed_tiers = models.ManyToManyField(
        LoyaltyTier,
        blank=True,
        related_name='applicable_rules',
        help_text="Tiers this rule applies to (empty = all tiers)"
    )

    # Date restrictions
    start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When rule becomes active (null = always active)"
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When rule expires (null = never expires)"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether rule is active"
    )

    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loyalty_rules_created',
        help_text="Admin user who created this rule"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loyalty Rule"
        verbose_name_plural = "Loyalty Rules"
        ordering = ['priority', '-created_at']
        indexes = [
            models.Index(fields=['rule_type', 'is_active']),
            models.Index(fields=['priority', 'is_active']),
            models.Index(fields=['scope', 'is_active']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_rule_type_display()})"

    def __repr__(self):
        return f"<LoyaltyRule id={self.id} type={self.rule_type} priority={self.priority}>"

    def is_currently_active(self):
        """Check if rule is active based on date restrictions"""
        if not self.is_active:
            return False

        now = timezone.now()

        if self.start_date and now < self.start_date:
            return False

        if self.end_date and now > self.end_date:
            return False

        return True

    def applies_to_tier(self, tier):
        """Check if rule applies to a specific tier"""
        if not self.allowed_tiers.exists():
            return True  # Applies to all tiers

        return self.allowed_tiers.filter(id=tier.id).exists()


class LoyaltyReward(models.Model):
    """
    Defines rewards that members can redeem with their points.

    Supports multiple reward types: discounts, products, free shipping, and experiences.
    Each reward has a points cost and availability constraints.
    """

    # Reward types
    TYPE_DISCOUNT = 'discount'
    TYPE_PRODUCT = 'product'
    TYPE_SHIPPING = 'shipping'
    TYPE_EXPERIENCE = 'experience'

    REWARD_TYPES = [
        (TYPE_DISCOUNT, 'Discount Code'),
        (TYPE_PRODUCT, 'Free Product'),
        (TYPE_SHIPPING, 'Free Shipping'),
        (TYPE_EXPERIENCE, 'Experience/Perk'),
    ]

    # Discount types (if reward type is discount)
    DISCOUNT_TYPE_PERCENTAGE = 'percentage'
    DISCOUNT_TYPE_FIXED = 'fixed'

    DISCOUNT_TYPES = [
        (DISCOUNT_TYPE_PERCENTAGE, 'Percentage Off'),
        (DISCOUNT_TYPE_FIXED, 'Fixed Amount Off'),
    ]

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # External reference UUID
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="External reference UUID for API access"
    )

    # Basic information
    name = models.CharField(
        max_length=200,
        help_text="Reward name (e.g., '$10 Off Your Next Order', 'Free Premium Mug')"
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        help_text="URL-safe identifier"
    )

    description = models.TextField(
        help_text="Detailed description of the reward"
    )

    # Reward type and configuration
    reward_type = models.CharField(
        max_length=20,
        choices=REWARD_TYPES,
        default=TYPE_DISCOUNT,
        db_index=True,
        help_text="Type of reward"
    )

    # Points cost
    points_cost = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Points required to redeem this reward"
    )

    # Discount configuration (if reward_type is 'discount')
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPES,
        null=True,
        blank=True,
        help_text="Type of discount (percentage or fixed amount)"
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Discount value (percentage or amount)"
    )

    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Minimum purchase amount to use discount"
    )

    # Product configuration (if reward_type is 'product')
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loyalty_rewards',
        help_text="Product to award (for product rewards)"
    )

    # Media
    image = models.ImageField(
        upload_to='loyalty/rewards/',
        null=True,
        blank=True,
        help_text="Reward image/thumbnail"
    )

    icon = models.CharField(
        max_length=50,
        default='fa-gift',
        help_text="Font Awesome icon class"
    )

    # Availability constraints
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether reward is currently available"
    )

    start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When reward becomes available"
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When reward expires"
    )

    quantity_total = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Total quantity available (null = unlimited)"
    )

    quantity_remaining = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Remaining quantity (updated on redemption)"
    )

    max_redemptions_per_member = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Maximum times a member can redeem this reward (null = unlimited)"
    )

    # Tier restrictions
    required_tier = models.ForeignKey(
        LoyaltyTier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='exclusive_rewards',
        help_text="Minimum tier required to redeem (null = all tiers)"
    )

    # Expiration settings
    redemption_expires_days = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Days until redeemed reward expires (null = no expiration)"
    )

    # Display settings
    featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Featured rewards appear prominently in UI"
    )

    display_order = models.IntegerField(
        default=0,
        db_index=True,
        help_text="Display order in reward catalog (lower = higher priority)"
    )

    # Terms and conditions
    terms = models.TextField(
        blank=True,
        help_text="Terms and conditions for this reward"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loyalty Reward"
        verbose_name_plural = "Loyalty Rewards"
        ordering = ['display_order', '-featured', 'name']
        indexes = [
            models.Index(fields=['reward_type', 'is_active']),
            models.Index(fields=['is_active', 'featured']),
            models.Index(fields=['points_cost']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['display_order']),
        ]

    def __str__(self):
        return f"{self.name} ({self.points_cost} pts)"

    def __repr__(self):
        return f"<LoyaltyReward id={self.id} name={self.name} type={self.reward_type}>"

    def clean(self):
        """Validate reward configuration based on reward type"""
        super().clean()

        # Validate discount rewards
        if self.reward_type == self.TYPE_DISCOUNT:
            if not self.discount_type:
                raise ValidationError({
                    'discount_type': _('Discount type is required for discount rewards.')
                })

            if not self.discount_value:
                raise ValidationError({
                    'discount_value': _('Discount value is required for discount rewards.')
                })

            # Additional validation for percentage discounts
            if self.discount_type == self.DISCOUNT_TYPE_PERCENTAGE:
                if self.discount_value > 100:
                    raise ValidationError({
                        'discount_value': _('Percentage discount cannot exceed 100%.')
                    })
                if self.discount_value <= 0:
                    raise ValidationError({
                        'discount_value': _('Discount value must be greater than 0.')
                    })

            # Additional validation for fixed amount discounts
            if self.discount_type == self.DISCOUNT_TYPE_FIXED:
                if self.discount_value <= 0:
                    raise ValidationError({
                        'discount_value': _('Discount value must be greater than 0.')
                    })

        # Validate product rewards
        if self.reward_type == self.TYPE_PRODUCT:
            if not self.product:
                raise ValidationError({
                    'product': _('Product selection is required for product rewards.')
                })

        # Ensure quantity_remaining doesn't exceed quantity_total
        if self.quantity_total is not None and self.quantity_remaining is not None:
            if self.quantity_remaining > self.quantity_total:
                raise ValidationError({
                    'quantity_remaining': _('Quantity remaining cannot exceed total quantity.')
                })

    def is_available(self):
        """Check if reward is currently available for redemption"""
        if not self.is_active:
            return False

        now = timezone.now()

        # Check date restrictions
        if self.start_date and now < self.start_date:
            return False

        if self.end_date and now > self.end_date:
            return False

        # Check quantity
        if self.quantity_remaining is not None and self.quantity_remaining <= 0:
            return False

        return True

    def can_member_redeem(self, member):
        """Check if a specific member can redeem this reward"""
        if not self.is_available():
            return False, "Reward is not currently available"

        # Check points balance
        try:
            if member.balance.available_points < self.points_cost:
                return False, f"Insufficient points (need {self.points_cost}, have {member.balance.available_points})"
        except LoyaltyBalance.DoesNotExist:
            return False, "Member has no balance record"

        # Check tier requirement
        if self.required_tier:
            if not member.current_tier or member.current_tier.rank < self.required_tier.rank:
                return False, f"Requires {self.required_tier.name} tier or higher"

        # Check redemption limit
        if self.max_redemptions_per_member:
            redemption_count = LoyaltyRedemption.objects.filter(
                member=member,
                reward=self,
                status__in=[LoyaltyRedemption.STATUS_PENDING, LoyaltyRedemption.STATUS_CONFIRMED]
            ).count()

            if redemption_count >= self.max_redemptions_per_member:
                return False, f"Maximum {self.max_redemptions_per_member} redemptions allowed per member"

        return True, "Eligible"


class LoyaltyRedemption(models.Model):
    """
    Tracks point redemptions for rewards.

    Implements a state machine for redemption lifecycle:
    pending -> confirmed -> fulfilled (or cancelled at any stage)
    """

    # Redemption statuses
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_FULFILLED = 'fulfilled'
    STATUS_CANCELLED = 'cancelled'
    STATUS_EXPIRED = 'expired'

    STATUSES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_FULFILLED, 'Fulfilled'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_EXPIRED, 'Expired'),
    ]

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # External reference UUID
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="External reference UUID for API access"
    )

    # Redemption code (unique identifier for customer)
    redemption_code = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        help_text="Unique redemption code (e.g., LOYALTY-XXXXX-XXXXX)"
    )

    # Relationships
    member = models.ForeignKey(
        LoyaltyMember,
        on_delete=models.PROTECT,
        related_name='redemptions',
        help_text="Member who redeemed the reward"
    )

    reward = models.ForeignKey(
        LoyaltyReward,
        on_delete=models.PROTECT,
        related_name='redemptions',
        help_text="Reward that was redeemed"
    )

    # Points tracking
    points_spent = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Points deducted for this redemption"
    )

    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default=STATUS_PENDING,
        db_index=True,
        help_text="Current redemption status"
    )

    # Linked transaction (points deduction)
    transaction = models.ForeignKey(
        LoyaltyTransaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='redemptions',
        help_text="Associated points transaction (deduction)"
    )

    # Order integration (if used in an order)
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loyalty_redemptions',
        help_text="Order where redemption was applied"
    )

    # Discount code (for discount rewards)
    voucher_code = models.ForeignKey(
        'vouchers.VoucherCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loyalty_redemptions',
        help_text="Generated voucher code (for discount rewards)"
    )

    # Expiration
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this redemption expires"
    )

    # State transition timestamps
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When redemption was confirmed"
    )

    fulfilled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When redemption was fulfilled"
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When redemption was cancelled"
    )

    # Cancellation details
    cancellation_reason = models.TextField(
        blank=True,
        help_text="Reason for cancellation"
    )

    # Admin notes
    admin_note = models.TextField(
        blank=True,
        help_text="Internal notes (not shown to customer)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loyalty Redemption"
        verbose_name_plural = "Loyalty Redemptions"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['member', 'status']),
            models.Index(fields=['reward', 'status']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['redemption_code']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"{self.member.customer.get_full_name()} - {self.reward.name} ({self.status})"

    def __repr__(self):
        return f"<LoyaltyRedemption id={self.id} code={self.redemption_code} status={self.status}>"

    def can_cancel(self):
        """Check if redemption can be cancelled"""
        return self.status in [self.STATUS_PENDING, self.STATUS_CONFIRMED]

    def is_expired(self):
        """Check if redemption has expired"""
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        return False


# ============================================================================
# CAMPAIGN & AUTOMATION MODELS
# ============================================================================


class LoyaltyCampaign(models.Model):
    """
    Campaign configuration for automated loyalty actions.

    Supports event-driven, scheduled, and behavioral campaigns with
    multi-step journeys, segmentation, and A/B testing.
    """

    # Campaign types
    TYPE_TRIGGER = 'trigger_based'
    TYPE_SCHEDULED = 'scheduled'
    TYPE_MANUAL = 'manual'
    TYPE_BEHAVIORAL = 'behavioral'

    CAMPAIGN_TYPES = [
        (TYPE_TRIGGER, 'Trigger-Based'),
        (TYPE_SCHEDULED, 'Scheduled'),
        (TYPE_MANUAL, 'Manual'),
        (TYPE_BEHAVIORAL, 'Behavioral'),
    ]

    # Trigger events
    EVENT_ORDER_PLACED = 'order_placed'
    EVENT_ORDER_REFUNDED = 'order_refunded'
    EVENT_ORDER_CANCELLED = 'order_cancelled'
    EVENT_CART_ABANDONED = 'cart_abandoned'
    EVENT_CUSTOMER_SIGNUP = 'customer_signup'
    EVENT_BIRTHDAY = 'birthday'
    EVENT_ANNIVERSARY = 'anniversary'
    EVENT_FIRST_PURCHASE = 'first_purchase'
    EVENT_NTH_PURCHASE = 'nth_purchase'
    EVENT_NO_PURCHASE_90D = 'no_purchase_90d'
    EVENT_POINTS_EXPIRING = 'points_expiring'
    EVENT_TIER_PROMOTED = 'tier_promoted'
    EVENT_TIER_DEMOTED = 'tier_demoted'
    EVENT_REVIEW_SUBMITTED = 'review_submitted'
    EVENT_REFERRAL_CONVERTED = 'referral_converted'

    TRIGGER_EVENTS = [
        (EVENT_ORDER_PLACED, 'Order Placed'),
        (EVENT_ORDER_REFUNDED, 'Order Refunded'),
        (EVENT_ORDER_CANCELLED, 'Order Cancelled'),
        (EVENT_CART_ABANDONED, 'Cart Abandoned'),
        (EVENT_CUSTOMER_SIGNUP, 'Customer Signup'),
        (EVENT_BIRTHDAY, 'Customer Birthday'),
        (EVENT_ANNIVERSARY, 'Membership Anniversary'),
        (EVENT_FIRST_PURCHASE, 'First Purchase'),
        (EVENT_NTH_PURCHASE, 'Nth Purchase'),
        (EVENT_NO_PURCHASE_90D, 'Inactive 90 Days'),
        (EVENT_POINTS_EXPIRING, 'Points Expiring Soon'),
        (EVENT_TIER_PROMOTED, 'Tier Promotion'),
        (EVENT_TIER_DEMOTED, 'Tier Demotion'),
        (EVENT_REVIEW_SUBMITTED, 'Review Submitted'),
        (EVENT_REFERRAL_CONVERTED, 'Referral Converted'),
    ]

    # Campaign status
    STATUS_DRAFT = 'draft'
    STATUS_ACTIVE = 'active'
    STATUS_PAUSED = 'paused'
    STATUS_ENDED = 'ended'
    STATUS_ARCHIVED = 'archived'

    STATUSES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_PAUSED, 'Paused'),
        (STATUS_ENDED, 'Ended'),
        (STATUS_ARCHIVED, 'Archived'),
    ]

    # Schedule types
    SCHEDULE_DAILY = 'daily'
    SCHEDULE_WEEKLY = 'weekly'
    SCHEDULE_MONTHLY = 'monthly'
    SCHEDULE_CUSTOM = 'custom_cron'

    SCHEDULE_TYPES = [
        (SCHEDULE_DAILY, 'Daily'),
        (SCHEDULE_WEEKLY, 'Weekly'),
        (SCHEDULE_MONTHLY, 'Monthly'),
        (SCHEDULE_CUSTOM, 'Custom Cron'),
    ]

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # External reference
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="External reference UUID for API access"
    )

    # Identification
    name = models.CharField(
        max_length=255,
        help_text="Campaign name (e.g., 'Birthday Bonus Points')"
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="URL-friendly identifier"
    )

    description = models.TextField(
        blank=True,
        help_text="Campaign purpose and details"
    )

    # Campaign type and trigger
    campaign_type = models.CharField(
        max_length=32,
        choices=CAMPAIGN_TYPES,
        default=TYPE_TRIGGER,
        help_text="Type of campaign automation"
    )

    trigger_event = models.CharField(
        max_length=64,
        choices=TRIGGER_EVENTS,
        blank=True,
        help_text="Event that triggers this campaign"
    )

    # Trigger conditions (JSONField for flexibility)
    trigger_conditions = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional filter criteria (e.g., min_order_amount, category_ids)"
    )

    # Actions configuration
    actions = models.JSONField(
        default=list,
        help_text="Array of actions to execute (award_points, send_email, etc.)"
    )

    # Journey configuration
    is_journey = models.BooleanField(
        default=False,
        help_text="Whether this is a multi-step campaign"
    )

    journey_steps = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of step configurations for multi-step journeys"
    )

    # Scheduling (for scheduled campaigns)
    schedule_type = models.CharField(
        max_length=32,
        choices=SCHEDULE_TYPES,
        blank=True,
        help_text="Schedule frequency"
    )

    schedule_config = models.JSONField(
        default=dict,
        blank=True,
        help_text="Schedule configuration (hour, minute, day_of_week, cron)"
    )

    # Segmentation
    target_segment = models.ForeignKey(
        'LoyaltySegment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='campaigns',
        help_text="Target customer segment"
    )

    target_tiers = models.ManyToManyField(
        'LoyaltyTier',
        blank=True,
        related_name='campaigns',
        help_text="Limit campaign to specific tiers"
    )

    target_all_members = models.BooleanField(
        default=True,
        help_text="Target all active members (ignores segment/tier)"
    )

    # Caps and limits
    max_triggers_per_member = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Maximum times this campaign can trigger for same member"
    )

    cooldown_days = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Days between campaign triggers for same member"
    )

    # A/B Testing
    is_ab_test = models.BooleanField(
        default=False,
        help_text="Whether this campaign is part of an A/B test"
    )

    ab_variant = models.CharField(
        max_length=10,
        blank=True,
        choices=[('A', 'Variant A'), ('B', 'Variant B'), ('control', 'Control')],
        help_text="A/B test variant"
    )

    ab_split_percentage = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of audience for this variant"
    )

    # Status and lifecycle
    status = models.CharField(
        max_length=32,
        choices=STATUSES,
        default=STATUS_DRAFT,
        db_index=True,
        help_text="Campaign status"
    )

    start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Campaign start date (null = starts immediately when activated)"
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Campaign end date (null = runs indefinitely)"
    )

    is_active = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether campaign is currently active"
    )

    # Statistics (cached)
    total_triggered = models.IntegerField(
        default=0,
        help_text="Total number of times campaign was triggered"
    )

    total_completed = models.IntegerField(
        default=0,
        help_text="Total number of successful executions"
    )

    total_failed = models.IntegerField(
        default=0,
        help_text="Total number of failed executions"
    )

    last_triggered_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last time campaign was triggered"
    )

    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_campaigns',
        help_text="User who created this campaign"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loyalty Campaign"
        verbose_name_plural = "Loyalty Campaigns"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['campaign_type', 'is_active']),
            models.Index(fields=['trigger_event']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def __repr__(self):
        return f"<LoyaltyCampaign id={self.id} name={self.name} status={self.status}>"

    def is_currently_active(self):
        """Check if campaign is currently active and within date range"""
        if not self.is_active or self.status != self.STATUS_ACTIVE:
            return False

        now = timezone.now()

        if self.start_date and now < self.start_date:
            return False

        if self.end_date and now > self.end_date:
            return False

        return True

    def can_trigger_for_member(self, member):
        """Check if campaign can trigger for specific member"""
        if not self.is_currently_active():
            return False

        # Check segment targeting
        if not self.target_all_members:
            if self.target_segment:
                from loyalty.services.segmentation import SegmentEvaluator
                evaluator = SegmentEvaluator()
                if not evaluator.evaluate_member(self.target_segment, member):
                    return False

            if self.target_tiers.exists():
                if not member.current_tier or member.current_tier not in self.target_tiers.all():
                    return False

        # Check max triggers
        if self.max_triggers_per_member:
            execution_count = self.executions.filter(member=member).count()
            if execution_count >= self.max_triggers_per_member:
                return False

        # Check cooldown
        if self.cooldown_days > 0:
            from datetime import timedelta
            cooldown_date = timezone.now() - timedelta(days=self.cooldown_days)
            recent_execution = self.executions.filter(
                member=member,
                triggered_at__gte=cooldown_date
            ).exists()
            if recent_execution:
                return False

        return True


class LoyaltyCampaignExecution(models.Model):
    """
    Tracks individual campaign executions for audit and analytics.

    Each execution represents a single campaign run for a specific member,
    with complete state tracking for multi-step journeys.
    """

    # Execution status
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'

    STATUSES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # External reference
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="External reference UUID for API access"
    )

    # Relationships
    campaign = models.ForeignKey(
        'LoyaltyCampaign',
        on_delete=models.CASCADE,
        related_name='executions',
        help_text="Campaign being executed"
    )

    member = models.ForeignKey(
        'LoyaltyMember',
        on_delete=models.CASCADE,
        related_name='campaign_executions',
        help_text="Member receiving campaign"
    )

    # Execution tracking
    triggered_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When campaign was triggered"
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When execution completed"
    )

    status = models.CharField(
        max_length=32,
        choices=STATUSES,
        default=STATUS_PENDING,
        db_index=True,
        help_text="Execution status"
    )

    # Journey tracking (for multi-step campaigns)
    current_step = models.IntegerField(
        default=1,
        help_text="Current step number in journey"
    )

    next_step_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="When next step should execute"
    )

    steps_completed = models.JSONField(
        default=list,
        help_text="List of completed step numbers"
    )

    # Results tracking
    actions_executed = models.JSONField(
        default=list,
        help_text="Log of executed actions with results"
    )

    points_awarded = models.IntegerField(
        default=0,
        help_text="Total points awarded in this execution"
    )

    rewards_issued = models.JSONField(
        default=list,
        help_text="List of reward IDs issued"
    )

    emails_sent = models.JSONField(
        default=list,
        help_text="List of email template types sent"
    )

    # Error tracking
    error_message = models.TextField(
        blank=True,
        help_text="Error message if execution failed"
    )

    retry_count = models.IntegerField(
        default=0,
        help_text="Number of retry attempts"
    )

    # A/B Testing
    ab_variant_assigned = models.CharField(
        max_length=10,
        blank=True,
        help_text="A/B test variant assigned to this execution"
    )

    # Context
    trigger_context = models.JSONField(
        default=dict,
        help_text="Data that triggered the campaign (order_id, etc.)"
    )

    class Meta:
        verbose_name = "Campaign Execution"
        verbose_name_plural = "Campaign Executions"
        ordering = ['-triggered_at']
        indexes = [
            models.Index(fields=['campaign', 'member']),
            models.Index(fields=['status', 'triggered_at']),
            models.Index(fields=['next_step_at']),
            models.Index(fields=['campaign', 'status']),
        ]

    def __str__(self):
        return f"{self.campaign.name} - {self.member.customer.get_full_name()} ({self.get_status_display()})"

    def __repr__(self):
        return f"<LoyaltyCampaignExecution id={self.id} campaign={self.campaign.id} status={self.status}>"

    def mark_completed(self):
        """Mark execution as completed"""
        self.status = self.STATUS_COMPLETED
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])

    def mark_failed(self, error_message):
        """Mark execution as failed"""
        self.status = self.STATUS_FAILED
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message'])

    def add_action_result(self, action_type, result):
        """Add action execution result to log"""
        self.actions_executed.append({
            'type': action_type,
            'timestamp': timezone.now().isoformat(),
            'result': result
        })
        self.save(update_fields=['actions_executed'])


class LoyaltySegment(models.Model):
    """
    Customer segmentation for targeted campaigns.

    Supports rule-based dynamic segments and manual segment assignments.
    """

    # Segment types
    TYPE_RULE_BASED = 'rule_based'
    TYPE_MANUAL = 'manual'
    TYPE_DYNAMIC = 'dynamic'

    SEGMENT_TYPES = [
        (TYPE_RULE_BASED, 'Rule-Based'),
        (TYPE_MANUAL, 'Manual Assignment'),
        (TYPE_DYNAMIC, 'Dynamic Calculation'),
    ]

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # External reference
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="External reference UUID for API access"
    )

    # Identification
    name = models.CharField(
        max_length=200,
        help_text="Segment name (e.g., 'High-Value Customers')"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="URL-friendly identifier"
    )

    description = models.TextField(
        blank=True,
        help_text="Segment description and criteria"
    )

    # Segment configuration
    criteria_type = models.CharField(
        max_length=32,
        choices=SEGMENT_TYPES,
        default=TYPE_DYNAMIC,
        help_text="How segment membership is determined"
    )

    criteria_config = models.JSONField(
        default=dict,
        help_text="Segment rules and filters configuration"
    )

    # Cache
    member_count = models.IntegerField(
        default=0,
        help_text="Cached count of segment members"
    )

    last_calculated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When member count was last calculated"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether segment is active"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loyalty Segment"
        verbose_name_plural = "Loyalty Segments"
        ordering = ['-member_count', 'name']
        indexes = [
            models.Index(fields=['criteria_type', 'is_active']),
            models.Index(fields=['last_calculated_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f"{self.name} ({self.member_count} members)"

    def __repr__(self):
        return f"<LoyaltySegment id={self.id} name={self.name} count={self.member_count}>"

    def refresh_member_count(self):
        """Refresh cached member count"""
        if self.criteria_type == self.TYPE_MANUAL:
            self.member_count = self.memberships.count()
        elif self.criteria_type == self.TYPE_DYNAMIC:
            from loyalty.services.segmentation import SegmentEvaluator
            evaluator = SegmentEvaluator()
            members = evaluator.get_segment_members(self)
            self.member_count = members.count()

        self.last_calculated_at = timezone.now()
        self.save(update_fields=['member_count', 'last_calculated_at'])


class LoyaltySegmentMembership(models.Model):
    """
    Tracks segment membership for manual/cached segments.

    For dynamic segments, membership is calculated on-the-fly.
    """

    # Primary key
    id = models.BigAutoField(primary_key=True)

    # Relationships
    segment = models.ForeignKey(
        'LoyaltySegment',
        on_delete=models.CASCADE,
        related_name='memberships',
        help_text="Segment this membership belongs to"
    )

    member = models.ForeignKey(
        'LoyaltyMember',
        on_delete=models.CASCADE,
        related_name='segment_memberships',
        help_text="Member in this segment"
    )

    # Tracking
    assigned_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When member was added to segment"
    )

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who manually assigned member (null for automated)"
    )

    class Meta:
        verbose_name = "Segment Membership"
        verbose_name_plural = "Segment Memberships"
        unique_together = [['segment', 'member']]
        ordering = ['-assigned_at']
        indexes = [
            models.Index(fields=['segment', 'assigned_at']),
            models.Index(fields=['member', 'assigned_at']),
        ]

    def __str__(self):
        return f"{self.member.customer.get_full_name()} in {self.segment.name}"

    def __repr__(self):
        return f"<LoyaltySegmentMembership segment={self.segment.id} member={self.member.id}>"
