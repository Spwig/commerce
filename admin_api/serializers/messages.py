"""
Message Serializers for Admin API

Serializers for customer messages management in the merchant mobile app.

Supports two message sources:
- contact_form: CustomerMessage model (standalone contact form submissions)
- order_note: OrderNote model (customer notes attached to orders)
"""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from admin_api.models import CustomerMessage, MessageReply


class ReadBySerializer(serializers.Serializer):
    """Serializer for staff read receipt entries."""
    name = serializers.CharField(help_text=_('Staff member name'))
    read_at = serializers.DateTimeField(help_text=_('When they read the message'))


class ThreadReplySerializer(serializers.Serializer):
    """Serializer for individual replies in a message thread."""
    id = serializers.IntegerField()
    sender_type = serializers.CharField(help_text=_('customer or staff'))
    sender_name = serializers.CharField(help_text=_('Display name of the sender'))
    content = serializers.CharField(help_text=_('Reply content'))
    email_sent = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class CustomerMessageListSerializer(serializers.ModelSerializer):
    """Compact serializer for message list view."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    preview = serializers.SerializerMethodField()

    class Meta:
        model = CustomerMessage
        fields = [
            'id',
            'name',
            'email',
            'subject',
            'preview',
            'message_type',
            'type_display',
            'status',
            'status_display',
            'created_at',
        ]

    def get_preview(self, obj):
        """Get first 100 characters of message."""
        if len(obj.message) <= 100:
            return obj.message
        return obj.message[:100] + '...'


class CustomerMessageDetailSerializer(serializers.ModelSerializer):
    """Full serializer for message detail view."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    read_by_name = serializers.SerializerMethodField()
    order_number = serializers.CharField(source='order.order_number', read_only=True, allow_null=True)

    class Meta:
        model = CustomerMessage
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'subject',
            'message',
            'message_type',
            'type_display',
            'order_id',
            'order_number',
            'status',
            'status_display',
            'read_at',
            'read_by_name',
            'created_at',
            'updated_at',
        ]

    def get_read_by_name(self, obj):
        if obj.read_by:
            return obj.read_by.get_full_name() or obj.read_by.email
        return None


class UnifiedMessageListSerializer(serializers.Serializer):
    """
    Unified serializer for messages from all sources.

    Deep linking:
    - source='contact_form' → use message_id to link to /messages/{id}/
    - source='order_note' → use order_number to link to /orders/{order_number}/
    """
    id = serializers.IntegerField(help_text=_('Unique ID within the source'))
    source = serializers.CharField(help_text=_('Message source: contact_form or order_note'))
    name = serializers.CharField(help_text=_('Sender name'))
    email = serializers.EmailField(help_text=_('Sender email'), allow_null=True)
    subject = serializers.CharField(help_text=_('Message subject or context'))
    preview = serializers.CharField(help_text=_('First 100 chars of message'))
    status = serializers.CharField(help_text=_('unread, read, replied, or archived'))
    status_display = serializers.CharField(help_text=_('Human-readable status'))
    created_at = serializers.DateTimeField()

    # Thread info
    reply_count = serializers.IntegerField(
        default=0,
        help_text=_('Number of replies in this thread')
    )
    last_reply_at = serializers.DateTimeField(
        allow_null=True,
        help_text=_('Timestamp of last reply')
    )

    # Per-user read tracking
    is_read_by_me = serializers.BooleanField(
        help_text=_('Whether the current user has read this message')
    )
    read_by = ReadBySerializer(
        many=True,
        help_text=_('List of staff members who have read this message')
    )
    last_activity_at = serializers.DateTimeField(
        help_text=_('Timestamp of most recent activity (reply or creation)')
    )

    # Deep linking fields - one of these will be populated based on source
    message_id = serializers.IntegerField(
        allow_null=True,
        help_text=_('CustomerMessage ID (for contact_form source)')
    )
    order_id = serializers.IntegerField(
        allow_null=True,
        help_text=_('Order ID (for order_note source)')
    )
    order_number = serializers.CharField(
        allow_null=True,
        help_text=_('Order number (for order_note source)')
    )


class UnifiedMessageDetailSerializer(serializers.Serializer):
    """
    Unified serializer for message detail from all sources.

    Deep linking:
    - source='contact_form' → use message_id
    - source='order_note' → use order_number to link to order
    """
    id = serializers.IntegerField(help_text=_('Unique ID within the source'))
    source = serializers.CharField(help_text=_('Message source: contact_form or order_note'))
    name = serializers.CharField(help_text=_('Sender name'))
    email = serializers.EmailField(help_text=_('Sender email'), allow_null=True)
    phone = serializers.CharField(help_text=_('Sender phone'), allow_null=True, allow_blank=True)
    subject = serializers.CharField(help_text=_('Message subject or context'))
    message = serializers.CharField(help_text=_('Full message content'))
    message_type = serializers.CharField(help_text=_('Message type (general, support, order, product, other)'))
    type_display = serializers.CharField(help_text=_('Human-readable message type'))
    status = serializers.CharField(help_text=_('unread, read, replied, or archived'))
    status_display = serializers.CharField(help_text=_('Human-readable status'))
    read_at = serializers.DateTimeField(allow_null=True)
    read_by_name = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    # Legacy reply fields (backward compat — latest staff reply)
    reply_text = serializers.CharField(
        allow_null=True, allow_blank=True,
        help_text=_('Latest staff reply text (backward compat)')
    )
    replied_at = serializers.DateTimeField(
        allow_null=True,
        help_text=_('When the latest staff reply was sent')
    )
    replied_by_name = serializers.CharField(
        allow_null=True,
        help_text=_('Name of staff member who last replied')
    )

    # Thread replies (full conversation history)
    replies = ThreadReplySerializer(
        many=True,
        help_text=_('All replies in this thread, chronologically ordered')
    )
    reply_count = serializers.IntegerField(
        default=0,
        help_text=_('Number of replies in this thread')
    )

    # Per-user read tracking
    is_read_by_me = serializers.BooleanField(
        help_text=_('Whether the current user has read this message')
    )
    read_by = ReadBySerializer(
        many=True,
        help_text=_('List of staff members who have read this message')
    )
    last_activity_at = serializers.DateTimeField(
        help_text=_('Timestamp of most recent activity (reply or creation)')
    )

    # Deep linking fields
    message_id = serializers.IntegerField(
        allow_null=True,
        help_text=_('CustomerMessage ID (for contact_form source)')
    )
    order_id = serializers.IntegerField(
        allow_null=True,
        help_text=_('Order ID (for order_note source)')
    )
    order_number = serializers.CharField(
        allow_null=True,
        help_text=_('Order number (for order_note source)')
    )


class MessageStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating message status."""
    status = serializers.ChoiceField(
        choices=[
            ('read', 'Mark as Read'),
            ('replied', 'Mark as Replied'),
            ('archived', 'Archive'),
        ]
    )


class MessageReplyInputSerializer(serializers.Serializer):
    """Serializer for replying to a customer message."""
    reply_text = serializers.CharField(
        max_length=5000,
        help_text=_('Reply message content')
    )
    send_email = serializers.BooleanField(
        default=True,
        help_text=_('Whether to send the reply via email to the customer')
    )
    subject = serializers.CharField(
        max_length=300,
        required=False,
        help_text=_('Email subject (defaults to "Re: {original_subject}")')
    )


class MessageReplyResponseSerializer(serializers.Serializer):
    """Response serializer for message reply."""
    id = serializers.IntegerField()
    reply_text = serializers.CharField()
    replied_at = serializers.DateTimeField()
    replied_by_name = serializers.CharField()
    email_sent = serializers.BooleanField()
    status = serializers.CharField()
    status_display = serializers.CharField()


class MessageFilterSerializer(serializers.Serializer):
    """Serializer for message list filters."""
    source = serializers.ChoiceField(
        choices=[
            ('all', 'All Sources'),
            ('contact_form', 'Contact Form'),
            ('order_note', 'Order Notes'),
        ],
        required=False,
        default='all',
        help_text=_('Filter by message source')
    )
    status = serializers.ChoiceField(
        choices=[
            ('all', 'All'),
            ('unread', 'Unread'),
            ('read', 'Read'),
            ('replied', 'Replied'),
            ('archived', 'Archived'),
        ],
        required=False,
        default='all'
    )
    search = serializers.CharField(required=False, allow_blank=True)
    sort = serializers.ChoiceField(
        choices=[
            ('-activity', 'Latest Activity'),
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
            ('status', 'Group by Status'),
        ],
        required=False,
        default='-activity',
        help_text=_('Sort order. -activity sorts by most recent reply or creation time.')
    )
    page = serializers.IntegerField(required=False, default=1, min_value=1)
    page_size = serializers.IntegerField(required=False, default=20, min_value=1, max_value=100)
