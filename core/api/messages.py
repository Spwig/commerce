"""
Customer Messages API

Public and authenticated API endpoints for customer messages/support.
Allows customers to submit contact forms and view their message history.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import serializers
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q

from admin_api.models import CustomerMessage, MessageReply
from core.api.authentication import HeadlessAPIMixin


# Throttling for contact form
class ContactFormThrottle(AnonRateThrottle):
    """Rate limit for anonymous contact form submissions"""
    rate = '5/hour'


class AuthenticatedContactThrottle(UserRateThrottle):
    """Rate limit for authenticated message submissions"""
    rate = '20/hour'


# Serializers
class ContactSubjectSerializer(serializers.Serializer):
    """Available contact form subjects/types"""
    value = serializers.CharField()
    label = serializers.CharField()


class MessageSubmitSerializer(serializers.Serializer):
    """Serializer for submitting a new message"""
    name = serializers.CharField(max_length=200, required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    subject = serializers.CharField(max_length=300, required=True)
    message = serializers.CharField(required=True)
    message_type = serializers.ChoiceField(
        choices=['general', 'support', 'order', 'product', 'other'],
        default='general'
    )
    order_number = serializers.CharField(required=False, allow_blank=True)


class MessageListSerializer(serializers.ModelSerializer):
    """Serializer for listing messages"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    has_reply = serializers.SerializerMethodField()

    class Meta:
        model = CustomerMessage
        fields = [
            'id',
            'subject',
            'message_type',
            'type_display',
            'status',
            'status_display',
            'has_reply',
            'reply_count',
            'last_reply_at',
            'created_at',
            'replied_at',
        ]
        read_only_fields = fields

    def get_has_reply(self, obj) -> bool:
        return obj.reply_count > 0


class CustomerThreadReplySerializer(serializers.ModelSerializer):
    """Serializer for individual replies in a thread (customer-facing)."""
    sender_name = serializers.CharField(read_only=True)

    class Meta:
        model = MessageReply
        fields = [
            'id',
            'sender_type',
            'sender_name',
            'content',
            'created_at',
        ]
        read_only_fields = fields


class MessageDetailSerializer(serializers.ModelSerializer):
    """Serializer for message details with full thread history."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    order_number = serializers.SerializerMethodField()
    replies = CustomerThreadReplySerializer(many=True, read_only=True)

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
            'status',
            'status_display',
            'order_number',
            'reply_text',
            'replied_at',
            'reply_count',
            'replies',
            'created_at',
        ]
        read_only_fields = fields

    def get_order_number(self, obj) -> str | None:
        if obj.order:
            return obj.order.order_number
        return None


class MessageReplySerializer(serializers.Serializer):
    """Serializer for customer follow-up messages"""
    message = serializers.CharField(required=True)


# Views
@extend_schema(
    tags=['Messages'],
    summary=_("Get contact form subjects"),
    description=_("Get available subjects/categories for the contact form."),
    responses={200: ContactSubjectSerializer(many=True)}
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def get_contact_subjects(request):
    """
    Get available contact form subjects.
    """
    subjects = [
        {'value': 'general', 'label': str(_('General Inquiry'))},
        {'value': 'support', 'label': str(_('Support Request'))},
        {'value': 'order', 'label': str(_('Order Related'))},
        {'value': 'product', 'label': str(_('Product Question'))},
        {'value': 'other', 'label': str(_('Other'))},
    ]

    return Response({
        'success': True,
        'data': subjects
    })


@extend_schema(
    tags=['Messages'],
    summary=_("Submit contact form"),
    description=_("Submit a new message through the contact form. Rate limited to 5/hour for anonymous users."),
    request=MessageSubmitSerializer,
    responses={
        201: OpenApiResponse(description=_("Message submitted successfully")),
        400: OpenApiResponse(description=_("Validation error")),
        429: OpenApiResponse(description=_("Rate limit exceeded")),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def submit_contact_form(request):
    """
    Submit a contact form message.

    This endpoint is public and rate-limited to prevent abuse.
    """
    serializer = MessageSubmitSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    # Check for order if order_number provided
    order = None
    if data.get('order_number'):
        from orders.models import Order
        try:
            order = Order.objects.get(order_number=data['order_number'])
        except Order.DoesNotExist:
            pass  # Order not found - proceed without linking

    # Create the message
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    ip_address = forwarded_for.split(',')[0].strip() if forwarded_for else request.META.get('REMOTE_ADDR', '')

    create_kwargs = {
        'name': data['name'],
        'email': data['email'],
        'phone': data.get('phone', ''),
        'subject': data['subject'],
        'message': data['message'],
        'message_type': data.get('message_type', 'general'),
        'order': order,
        'status': 'unread',
        'ip_address': ip_address or None,
        'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500],
    }
    # Link to user account if authenticated
    if request.user and request.user.is_authenticated:
        create_kwargs['user'] = request.user

    message = CustomerMessage.objects.create(**create_kwargs)

    return Response({
        'success': True,
        'message': _('Your message has been submitted. We will respond shortly.'),
        'data': {
            'id': message.id,
            'subject': message.subject,
            'created_at': message.created_at.isoformat()
        }
    }, status=status.HTTP_201_CREATED)


@extend_schema_view(
    list=extend_schema(
        tags=['Messages'],
        summary=_("List customer messages"),
        description=_("List all messages submitted by the authenticated customer."),
        parameters=[
            OpenApiParameter('status', str, description=_('Filter by status: unread, read, replied, archived')),
            OpenApiParameter('type', str, description=_('Filter by type: general, support, order, product, other')),
        ],
        responses={200: MessageListSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=['Messages'],
        summary=_("Get message details"),
        description=_("Get details of a specific message including any staff reply."),
        responses={200: MessageDetailSerializer}
    ),
)
class CustomerMessageViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    Customer Messages ViewSet

    Provides authenticated customers access to their message history.

    Endpoints:
    - GET /api/messages/ - List customer's messages
    - GET /api/messages/{id}/ - Get message details with full thread
    - POST /api/messages/{id}/follow-up/ - Send follow-up message in thread
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MessageDetailSerializer
        return MessageListSerializer

    def get_queryset(self):
        """Get messages for the authenticated user (by user FK or email fallback)"""
        user = self.request.user
        queryset = CustomerMessage.objects.filter(
            Q(user=user) | Q(email=user.email, user__isnull=True)
        ).order_by('-created_at')

        # Prefetch replies for detail view
        if self.action == 'retrieve':
            from django.db.models import Prefetch
            queryset = queryset.prefetch_related(
                Prefetch('replies', queryset=MessageReply.objects.select_related('sender_user'))
            )

        # Filter by status
        msg_status = self.request.query_params.get('status')
        if msg_status and msg_status in ['unread', 'read', 'replied', 'archived']:
            queryset = queryset.filter(status=msg_status)

        # Filter by type
        msg_type = self.request.query_params.get('type')
        if msg_type and msg_type in ['general', 'support', 'order', 'product', 'other']:
            queryset = queryset.filter(message_type=msg_type)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'count': queryset.count(),
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Messages'],
        summary=_("Send follow-up message"),
        description=_("Send a follow-up message in an existing conversation thread."),
        request=MessageReplySerializer,
        responses={
            201: OpenApiResponse(description=_("Follow-up sent")),
            400: OpenApiResponse(description=_("Validation error")),
        }
    )
    @action(detail=True, methods=['post'], url_path='follow-up')
    def follow_up(self, request, pk=None):
        """
        Send a follow-up message in the thread.

        Creates a MessageReply on the original message rather than a
        standalone message, keeping the full conversation in one thread.
        Resets the message status to 'unread' so merchants see it.
        """
        original_message = self.get_object()

        serializer = MessageReplySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create reply in the existing thread
        reply = original_message.add_reply(
            sender_type='customer',
            content=serializer.validated_data['message'],
            sender_user=request.user,
        )

        return Response({
            'success': True,
            'message': _('Follow-up message sent.'),
            'data': {
                'id': reply.id,
                'content': reply.content,
                'created_at': reply.created_at.isoformat()
            }
        }, status=status.HTTP_201_CREATED)
