"""
Admin API Models

Models for the Spwig Merchant mobile app Admin API:
- MobileAuthToken: Access and refresh tokens with device tracking
- AdminAPIAuditLog: Audit trail for admin operations
- DeviceRegistration: Push notification device registration
"""

import secrets

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class MobileAuthToken(models.Model):
    """
    Token for mobile app authentication with refresh capability.

    Supports access tokens (short-lived), refresh tokens (long-lived),
    and 2FA pending tokens (very short-lived, for completing 2FA flow)
    with device tracking for multi-device support.
    """

    TOKEN_TYPE_CHOICES = [
        ("access", _("Access Token")),
        ("refresh", _("Refresh Token")),
        ("2fa_pending", _("2FA Pending Token")),
    ]

    # 2FA pending token lifetime in minutes (default 5 minutes)
    TWO_FA_PENDING_LIFETIME_MINUTES = 5

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mobile_tokens",
        verbose_name=_("User"),
    )
    token = models.CharField(_("Token"), max_length=64, unique=True, db_index=True)
    token_type = models.CharField(_("Token Type"), max_length=12, choices=TOKEN_TYPE_CHOICES)
    device_id = models.CharField(
        _("Device ID"), max_length=255, help_text=_("Unique identifier for the device")
    )
    device_name = models.CharField(
        _("Device Name"),
        max_length=255,
        blank=True,
        help_text=_('Human-readable device name (e.g., "iPhone 15 Pro")'),
    )

    # Timestamps
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    expires_at = models.DateTimeField(_("Expires At"))
    last_used_at = models.DateTimeField(_("Last Used At"), null=True, blank=True)
    last_used_ip = models.GenericIPAddressField(_("Last Used IP"), null=True, blank=True)

    # Revocation
    is_revoked = models.BooleanField(_("Is Revoked"), default=False)
    revoked_at = models.DateTimeField(_("Revoked At"), null=True, blank=True)
    revoked_reason = models.CharField(_("Revocation Reason"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Mobile Auth Token")
        verbose_name_plural = _("Mobile Auth Tokens")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["token", "token_type"]),
            models.Index(fields=["user", "device_id"]),
            models.Index(fields=["user", "token_type", "is_revoked"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.token_type} ({self.device_name or self.device_id[:8]})"

    @property
    def is_expired(self):
        """Check if the token has expired."""
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        """Check if the token is valid (not expired and not revoked)."""
        return not self.is_expired and not self.is_revoked

    def revoke(self, reason=""):
        """Revoke this token."""
        self.is_revoked = True
        self.revoked_at = timezone.now()
        self.revoked_reason = reason
        self.save(update_fields=["is_revoked", "revoked_at", "revoked_reason"])

    def update_last_used(self, ip_address=None):
        """Update last used timestamp and IP."""
        self.last_used_at = timezone.now()
        if ip_address:
            self.last_used_ip = ip_address
        self.save(update_fields=["last_used_at", "last_used_ip"])

    @classmethod
    def generate_token(cls):
        """Generate a cryptographically secure token."""
        return secrets.token_urlsafe(48)

    @classmethod
    def create_token_pair(cls, user, device_id, device_name=""):
        """
        Create an access/refresh token pair for a user and device.

        Returns:
            tuple: (access_token, refresh_token)
        """
        from django.conf import settings

        mobile_settings = getattr(settings, "MOBILE_API_SETTINGS", {})
        access_lifetime = mobile_settings.get("ACCESS_TOKEN_LIFETIME_MINUTES", 30)
        refresh_lifetime = mobile_settings.get("REFRESH_TOKEN_LIFETIME_DAYS", 14)

        now = timezone.now()

        # Create access token
        access_token = cls.objects.create(
            user=user,
            token=cls.generate_token(),
            token_type="access",
            device_id=device_id,
            device_name=device_name,
            expires_at=now + timezone.timedelta(minutes=access_lifetime),
        )

        # Create refresh token
        refresh_token = cls.objects.create(
            user=user,
            token=cls.generate_token(),
            token_type="refresh",
            device_id=device_id,
            device_name=device_name,
            expires_at=now + timezone.timedelta(days=refresh_lifetime),
        )

        return access_token, refresh_token

    @classmethod
    def create_2fa_pending_token(cls, user, device_id, device_name=""):
        """
        Create a short-lived 2FA pending token.

        This token is issued after password verification but before 2FA completion.
        It's used to identify the authentication session during 2FA verification.

        Args:
            user: The user who passed password verification
            device_id: Device identifier
            device_name: Human-readable device name

        Returns:
            MobileAuthToken: The 2FA pending token
        """
        now = timezone.now()

        # Revoke any existing 2FA pending tokens for this device
        cls.objects.filter(
            user=user, device_id=device_id, token_type="2fa_pending", is_revoked=False
        ).update(is_revoked=True, revoked_at=now, revoked_reason="New 2FA challenge")

        # Create new 2FA pending token (short-lived)
        pending_token = cls.objects.create(
            user=user,
            token=cls.generate_token(),
            token_type="2fa_pending",
            device_id=device_id,
            device_name=device_name,
            expires_at=now + timezone.timedelta(minutes=cls.TWO_FA_PENDING_LIFETIME_MINUTES),
        )

        return pending_token

    @classmethod
    def revoke_all_for_user(cls, user, reason="Logout from all devices"):
        """Revoke all tokens for a user."""
        cls.objects.filter(user=user, is_revoked=False).update(
            is_revoked=True, revoked_at=timezone.now(), revoked_reason=reason
        )

    @classmethod
    def revoke_all_for_device(cls, user, device_id, reason="Device logout"):
        """Revoke all tokens for a specific device."""
        cls.objects.filter(user=user, device_id=device_id, is_revoked=False).update(
            is_revoked=True, revoked_at=timezone.now(), revoked_reason=reason
        )

    @classmethod
    def cleanup_expired_tokens(cls):
        """Delete expired tokens older than 30 days."""
        cutoff = timezone.now() - timezone.timedelta(days=30)
        return cls.objects.filter(expires_at__lt=cutoff).delete()


class AdminAPIAuditLog(models.Model):
    """
    Audit trail for admin API operations.

    Tracks who made what changes, when, with old and new values.
    Used for accountability and debugging.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="admin_api_audit_logs",
        verbose_name=_("User"),
    )
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True, db_index=True)

    # Action details
    action = models.CharField(
        _("Action"),
        max_length=100,
        db_index=True,
        help_text=_('Action performed (e.g., "order.update_status")'),
    )
    resource_type = models.CharField(
        _("Resource Type"),
        max_length=50,
        help_text=_('Type of resource (e.g., "order", "product")'),
    )
    resource_id = models.CharField(
        _("Resource ID"), max_length=100, help_text=_("ID of the affected resource")
    )

    # Change tracking
    old_value = models.JSONField(
        _("Old Value"), default=dict, blank=True, help_text=_("Previous state before the change")
    )
    new_value = models.JSONField(
        _("New Value"), default=dict, blank=True, help_text=_("New state after the change")
    )

    # Request context
    ip_address = models.GenericIPAddressField(_("IP Address"), null=True, blank=True)
    device_id = models.CharField(_("Device ID"), max_length=255, blank=True)
    user_agent = models.CharField(_("User Agent"), max_length=500, blank=True)

    # Additional context
    success = models.BooleanField(
        _("Success"), default=True, help_text=_("Whether the operation succeeded")
    )
    error_message = models.TextField(
        _("Error Message"), blank=True, help_text=_("Error details if the operation failed")
    )

    class Meta:
        verbose_name = _("Admin API Audit Log")
        verbose_name_plural = _("Admin API Audit Logs")
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "-timestamp"]),
            models.Index(fields=["action", "-timestamp"]),
            models.Index(fields=["resource_type", "resource_id"]),
            models.Index(fields=["-timestamp"]),
        ]

    def __str__(self):
        user_str = self.user.email if self.user else "Unknown"
        return f"{user_str} - {self.action} - {self.resource_type}:{self.resource_id}"

    @classmethod
    def cleanup_old_logs(cls, days=90):
        """Delete audit logs older than specified days."""
        cutoff = timezone.now() - timezone.timedelta(days=days)
        return cls.objects.filter(timestamp__lt=cutoff).delete()


class DeviceRegistration(models.Model):
    """
    Device registration for push notifications.

    Stores push notification tokens and notification preferences
    for each registered device.
    """

    PLATFORM_CHOICES = [
        ("ios", _("iOS")),
        ("android", _("Android")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registered_devices",
        verbose_name=_("User"),
    )
    device_id = models.CharField(
        _("Device ID"), max_length=255, help_text=_("Unique identifier for the device")
    )
    push_token = models.CharField(
        _("Push Token"), max_length=500, help_text=_("APNs/FCM token for push notifications")
    )
    platform = models.CharField(_("Platform"), max_length=10, choices=PLATFORM_CHOICES)

    # Notification preferences
    notify_new_orders = models.BooleanField(
        _("Notify New Orders"), default=True, help_text=_("Receive notifications for new orders")
    )
    notify_low_stock = models.BooleanField(
        _("Notify Low Stock"),
        default=True,
        help_text=_("Receive notifications for low stock alerts"),
    )
    notify_customer_messages = models.BooleanField(
        _("Notify Customer Messages"),
        default=True,
        help_text=_("Receive notifications for customer messages"),
    )

    # Status
    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_("Whether this device should receive notifications"),
    )
    last_notification_at = models.DateTimeField(_("Last Notification At"), null=True, blank=True)
    failed_attempts = models.PositiveIntegerField(
        _("Failed Attempts"), default=0, help_text=_("Number of consecutive failed push attempts")
    )

    # Timestamps
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Device Registration")
        verbose_name_plural = _("Device Registrations")
        ordering = ["-updated_at"]
        unique_together = [["user", "device_id"]]
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["platform", "is_active"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.platform} ({self.device_id[:8]})"

    def mark_notification_sent(self):
        """Mark that a notification was successfully sent."""
        self.last_notification_at = timezone.now()
        self.failed_attempts = 0
        self.save(update_fields=["last_notification_at", "failed_attempts"])

    def mark_notification_failed(self):
        """Mark that a notification failed to send."""
        self.failed_attempts += 1
        # Deactivate after 5 consecutive failures
        if self.failed_attempts >= 5:
            self.is_active = False
        self.save(update_fields=["failed_attempts", "is_active"])

    @classmethod
    def get_devices_for_notification(cls, notification_type, exclude_user=None):
        """
        Get all active devices that should receive a specific notification type.

        Args:
            notification_type: One of 'new_order', 'low_stock', 'customer_message'
            exclude_user: Optional user to exclude from notifications

        Returns:
            QuerySet of DeviceRegistration objects
        """
        queryset = cls.objects.filter(is_active=True)

        if notification_type == "new_order":
            queryset = queryset.filter(notify_new_orders=True)
        elif notification_type == "low_stock":
            queryset = queryset.filter(notify_low_stock=True)
        elif notification_type == "customer_message":
            queryset = queryset.filter(notify_customer_messages=True)

        if exclude_user:
            queryset = queryset.exclude(user=exclude_user)

        return queryset.select_related("user")


class StaffInvitation(models.Model):
    """
    Staff invitation for onboarding new team members.

    When a store owner or admin invites a new staff member, this model
    stores the invitation details until accepted.
    """

    email = models.EmailField(_("Email"), help_text=_("Email address of the invited staff member"))
    first_name = models.CharField(
        _("First Name"),
        max_length=150,
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=150,
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_invitations",
        verbose_name=_("Invited By"),
    )
    token = models.CharField(_("Invitation Token"), max_length=64, unique=True, db_index=True)
    group_ids = models.JSONField(
        _("Role IDs"), default=list, help_text=_("List of StaffRole IDs to assign upon acceptance")
    )

    # Status
    is_accepted = models.BooleanField(_("Accepted"), default=False)
    accepted_at = models.DateTimeField(_("Accepted At"), null=True, blank=True)
    expires_at = models.DateTimeField(_("Expires At"))

    # Timestamps
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Staff Invitation")
        verbose_name_plural = _("Staff Invitations")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email", "is_accepted"]),
            models.Index(fields=["token"]),
        ]

    def __str__(self):
        return f"Invitation for {self.email} by {self.invited_by}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        return not self.is_expired and not self.is_accepted

    @classmethod
    def generate_token(cls):
        return secrets.token_urlsafe(48)


class CustomerMessage(models.Model):
    """
    Customer messages from contact forms or inquiries.

    Stores messages submitted through the store's contact form
    for staff to review and respond via email.
    """

    STATUS_CHOICES = [
        ("unread", _("Unread")),
        ("read", _("Read")),
        ("replied", _("Replied")),
        ("archived", _("Archived")),
    ]

    TYPE_CHOICES = [
        ("general", _("General Inquiry")),
        ("support", _("Support Request")),
        ("order", _("Order Related")),
        ("product", _("Product Question")),
        ("other", _("Other")),
    ]

    # Sender information
    name = models.CharField(_("Name"), max_length=200, help_text=_("Sender's name"))
    email = models.EmailField(_("Email"), help_text=_("Sender's email address"))
    phone = models.CharField(
        _("Phone"), max_length=30, blank=True, help_text=_("Sender's phone number (optional)")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_messages",
        verbose_name=_("User"),
        help_text=_("Linked customer account (set when submitted while logged in)"),
    )

    # Message details
    subject = models.CharField(_("Subject"), max_length=300, help_text=_("Message subject"))
    message = models.TextField(_("Message"), help_text=_("Message content"))
    message_type = models.CharField(
        _("Type"), max_length=20, choices=TYPE_CHOICES, default="general"
    )

    # Related entities (optional)
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_messages",
        help_text=_("Related order (if applicable)"),
    )

    # Status tracking
    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default="unread", db_index=True
    )
    read_at = models.DateTimeField(_("Read At"), null=True, blank=True)
    read_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="read_customer_messages",
        verbose_name=_("Read By"),
    )

    # Reply tracking
    reply_text = models.TextField(
        _("Reply Text"), blank=True, help_text=_("Staff reply to the customer")
    )
    replied_at = models.DateTimeField(_("Replied At"), null=True, blank=True)
    replied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replied_customer_messages",
        verbose_name=_("Replied By"),
    )

    # Thread tracking (denormalized for efficient list queries)
    reply_count = models.PositiveIntegerField(
        _("Reply Count"), default=0, help_text=_("Total number of replies in this thread")
    )
    last_reply_at = models.DateTimeField(
        _("Last Reply At"), null=True, blank=True, help_text=_("Timestamp of the most recent reply")
    )
    LAST_REPLY_BY_CHOICES = [
        ("customer", _("Customer")),
        ("staff", _("Staff")),
    ]
    last_reply_by = models.CharField(
        _("Last Reply By"),
        max_length=10,
        choices=LAST_REPLY_BY_CHOICES,
        blank=True,
        help_text=_("Who sent the last reply in this thread"),
    )

    # Timestamps
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    # Metadata
    ip_address = models.GenericIPAddressField(_("IP Address"), null=True, blank=True)
    user_agent = models.CharField(_("User Agent"), max_length=500, blank=True)

    class Meta:
        verbose_name = _("Customer Message")
        verbose_name_plural = _("Customer Messages")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["email", "-created_at"]),
            models.Index(fields=["user", "-created_at"], name="idx_customermsg_user_created"),
        ]

    def __str__(self):
        return f"{self.name} - {self.subject[:50]}"

    def mark_as_read(self, user):
        """Mark message as read by a staff member."""
        if self.status == "unread":
            self.status = "read"
            self.read_at = timezone.now()
            self.read_by = user
            self.save(update_fields=["status", "read_at", "read_by", "updated_at"])

    def mark_as_replied(self, user=None, reply_text=""):
        """Mark message as replied with optional reply text."""
        self.status = "replied"
        self.replied_at = timezone.now()
        if user:
            self.replied_by = user
        if reply_text:
            self.reply_text = reply_text
        self.save(update_fields=["status", "replied_at", "replied_by", "reply_text", "updated_at"])

    def archive(self):
        """Archive the message."""
        self.status = "archived"
        self.save(update_fields=["status", "updated_at"])

    def add_reply(self, sender_type, content, sender_user=None, email_sent=False):
        """
        Add a reply to this message thread.

        Creates a MessageReply, updates denormalized thread fields, and
        (for staff replies) also updates legacy reply_text/replied_at/replied_by
        for backward compatibility with older app versions.

        Returns the created MessageReply instance.
        """
        reply = MessageReply.objects.create(
            message=self,
            sender_type=sender_type,
            sender_user=sender_user,
            content=content,
            email_sent=email_sent,
            email_sent_at=timezone.now() if email_sent else None,
        )

        # Update denormalized fields
        self.reply_count = self.replies.count()
        self.last_reply_at = reply.created_at
        self.last_reply_by = sender_type
        update_fields = ["reply_count", "last_reply_at", "last_reply_by", "updated_at"]

        # For staff replies, also update legacy single-reply fields
        if sender_type == "staff":
            self.status = "replied"
            self.reply_text = content
            self.replied_at = reply.created_at
            self.replied_by = sender_user
            update_fields += ["status", "reply_text", "replied_at", "replied_by"]
        elif sender_type == "customer":
            # Customer follow-up resets to unread so merchants see it
            self.status = "unread"
            update_fields += ["status"]

        self.save(update_fields=update_fields)
        return reply

    @classmethod
    def get_unread_count(cls):
        """Get count of unread messages."""
        return cls.objects.filter(status="unread").count()


class MessageReadReceipt(models.Model):
    """
    Per-user read tracking for customer messages.

    Tracks which staff members have read a message, supporting multi-staff
    stores where multiple team members may handle customer communications.
    Works for both CustomerMessage and OrderNote sources.
    """

    SOURCE_CHOICES = [
        ("contact_form", _("Contact Form")),
        ("order_note", _("Order Note")),
    ]

    source = models.CharField(
        _("Source"),
        max_length=20,
        choices=SOURCE_CHOICES,
    )
    object_id = models.PositiveIntegerField(
        _("Object ID"),
        help_text=_("ID of the CustomerMessage or OrderNote"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="message_read_receipts",
        verbose_name=_("Read By"),
    )
    read_at = models.DateTimeField(_("Read At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Message Read Receipt")
        verbose_name_plural = _("Message Read Receipts")
        unique_together = [("source", "object_id", "user")]
        indexes = [
            models.Index(fields=["source", "object_id"]),
            models.Index(fields=["user", "source"]),
        ]

    def __str__(self):
        return f"{self.user} read {self.source}#{self.object_id} at {self.read_at}"


class MessageReply(models.Model):
    """
    Individual reply in a customer message thread.

    Supports multi-turn conversations between customers and staff.
    Each reply belongs to a CustomerMessage and is ordered chronologically.
    """

    SENDER_CHOICES = [
        ("customer", _("Customer")),
        ("staff", _("Staff")),
    ]

    message = models.ForeignKey(
        "CustomerMessage",
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name=_("Message"),
    )
    sender_type = models.CharField(_("Sender Type"), max_length=10, choices=SENDER_CHOICES)
    sender_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="message_replies",
        verbose_name=_("Sender"),
        help_text=_("Staff user or customer user who sent this reply"),
    )
    content = models.TextField(_("Content"), help_text=_("Reply message content"))

    # Email tracking (for staff replies sent via email)
    email_sent = models.BooleanField(
        _("Email Sent"),
        default=False,
        help_text=_("Whether this reply was sent to the customer via email"),
    )
    email_sent_at = models.DateTimeField(_("Email Sent At"), null=True, blank=True)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Message Reply")
        verbose_name_plural = _("Message Replies")
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["message", "created_at"]),
        ]

    def __str__(self):
        return f"{self.get_sender_type_display()} reply on #{self.message_id} at {self.created_at}"

    @property
    def sender_name(self):
        """Get display name for the sender."""
        if self.sender_user:
            return self.sender_user.get_full_name() or self.sender_user.email
        if self.sender_type == "customer":
            return self.message.name
        return "Staff"
