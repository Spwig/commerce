"""
Customer Messages Integration Tests.

Tests the customer-facing message views in the accounts portal:
- message_list: Displays messages for the authenticated user
- message_detail: Shows single message thread with follow-up capability
- message_new: Allows customers to submit new messages
- dashboard: Includes unread_reply_count in context

Also tests CustomerMessageForm and FollowUpMessageForm validation.
"""
import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages

from admin_api.models import CustomerMessage
from accounts.forms import CustomerMessageForm, FollowUpMessageForm
from tests.factories import UserFactory, OrderFactory, CustomerMessageFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.messages]


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def other_user(db):
    """A second customer user for isolation tests."""
    return UserFactory(
        username='other_customer',
        email='other@test.spwig.com',
    )


@pytest.fixture
def anon_client():
    """Unauthenticated Django test client."""
    return Client()


@pytest.fixture
def customer_order(customer_user):
    """An order belonging to the customer_user."""
    return OrderFactory(user=customer_user)


@pytest.fixture
def other_user_order(other_user):
    """An order belonging to other_user (not customer_user)."""
    return OrderFactory(user=other_user)


@pytest.fixture
def customer_message(customer_user):
    """A basic unread message from customer_user."""
    return CustomerMessageFactory(user=customer_user)


@pytest.fixture
def replied_message(customer_user):
    """A message from customer_user that has been replied to."""
    return CustomerMessageFactory(user=customer_user, replied=True)


@pytest.fixture
def anonymous_message(customer_user):
    """An anonymous message matching customer_user's email (no user FK)."""
    return CustomerMessageFactory(
        anonymous=True,
        email=customer_user.email,
        name='Anonymous Customer',
    )


# ============================================================
# Views — message_list
# ============================================================

class TestMessageListView:

    def test_returns_200_for_authenticated_user(self, customer_client):
        """Message list returns 200 for an authenticated customer."""
        url = reverse('accounts:message_list')
        response = customer_client.get(url)
        assert response.status_code == 200

    def test_redirects_unauthenticated_user(self, anon_client):
        """Message list redirects unauthenticated users to login."""
        url = reverse('accounts:message_list')
        response = anon_client.get(url)
        assert response.status_code == 302
        assert '/account/login/' in response.url or '/accounts/login/' in response.url

    def test_shows_messages_belonging_to_user(self, customer_client, customer_user):
        """Message list shows messages where user FK matches."""
        msg = CustomerMessageFactory(user=customer_user, subject='My message')
        url = reverse('accounts:message_list')
        response = customer_client.get(url)
        assert response.status_code == 200
        messages_list = response.context['messages_list']
        assert msg in messages_list

    def test_shows_email_fallback_messages(self, customer_client, customer_user, anonymous_message):
        """Message list includes anonymous messages matching user's email."""
        url = reverse('accounts:message_list')
        response = customer_client.get(url)
        messages_list = response.context['messages_list']
        assert anonymous_message in messages_list

    def test_does_not_show_other_users_messages(self, customer_client, other_user):
        """Message list does not show messages belonging to other users."""
        other_msg = CustomerMessageFactory(
            user=other_user,
            subject='Not my message',
        )
        url = reverse('accounts:message_list')
        response = customer_client.get(url)
        messages_list = response.context['messages_list']
        assert other_msg not in messages_list

    def test_does_not_show_anonymous_messages_with_different_email(
        self, customer_client
    ):
        """Message list excludes anonymous messages with non-matching emails."""
        wrong_email_msg = CustomerMessageFactory(
            anonymous=True,
            email='stranger@example.com',
            name='Stranger',
        )
        url = reverse('accounts:message_list')
        response = customer_client.get(url)
        messages_list = response.context['messages_list']
        assert wrong_email_msg not in messages_list

    def test_context_uses_messages_list_key(self, customer_client):
        """Context variable is 'messages_list' (not 'messages' which collides with Django messages)."""
        url = reverse('accounts:message_list')
        response = customer_client.get(url)
        assert 'messages_list' in response.context

    def test_context_includes_total_count(self, customer_client, customer_user):
        """Context includes total_count of user's messages."""
        CustomerMessageFactory(user=customer_user)
        CustomerMessageFactory(user=customer_user)
        url = reverse('accounts:message_list')
        response = customer_client.get(url)
        assert response.context['total_count'] == 2

    def test_empty_state(self, customer_client):
        """Message list handles user with no messages gracefully."""
        url = reverse('accounts:message_list')
        response = customer_client.get(url)
        assert response.status_code == 200
        messages_list = response.context['messages_list']
        assert messages_list.count() == 0
        assert response.context['total_count'] == 0


# ============================================================
# Views — message_detail
# ============================================================

class TestMessageDetailView:

    def test_returns_200_for_message_owner(self, customer_client, customer_message):
        """Message detail returns 200 when accessed by the message owner."""
        url = reverse('accounts:message_detail', kwargs={'message_id': customer_message.pk})
        response = customer_client.get(url)
        assert response.status_code == 200

    def test_returns_404_for_non_owner(self, customer_client, other_user):
        """Message detail returns 404 when accessed by a different user."""
        other_msg = CustomerMessageFactory(user=other_user, subject='Private')
        url = reverse('accounts:message_detail', kwargs={'message_id': other_msg.pk})
        response = customer_client.get(url)
        assert response.status_code == 404

    def test_redirects_unauthenticated_user(self, anon_client, customer_message):
        """Message detail redirects unauthenticated users to login."""
        url = reverse('accounts:message_detail', kwargs={'message_id': customer_message.pk})
        response = anon_client.get(url)
        assert response.status_code == 302
        assert '/account/login/' in response.url or '/accounts/login/' in response.url

    def test_accessible_via_email_fallback(self, customer_client, anonymous_message):
        """Message detail allows access to anonymous messages matching user's email."""
        url = reverse('accounts:message_detail', kwargs={'message_id': anonymous_message.pk})
        response = customer_client.get(url)
        assert response.status_code == 200

    def test_context_contains_message_object(self, customer_client, customer_message):
        """Context includes 'msg' with the correct message object."""
        url = reverse('accounts:message_detail', kwargs={'message_id': customer_message.pk})
        response = customer_client.get(url)
        assert response.context['msg'] == customer_message

    def test_shows_follow_up_form_when_reply_exists(self, customer_client, replied_message):
        """Follow-up form is shown when the message has a reply_text."""
        url = reverse('accounts:message_detail', kwargs={'message_id': replied_message.pk})
        response = customer_client.get(url)
        assert response.context['follow_up_form'] is not None
        assert isinstance(response.context['follow_up_form'], FollowUpMessageForm)

    def test_no_follow_up_form_when_no_reply(self, customer_client, customer_message):
        """Follow-up form is None when the message has no reply."""
        url = reverse('accounts:message_detail', kwargs={'message_id': customer_message.pk})
        response = customer_client.get(url)
        assert response.context['follow_up_form'] is None

    def test_follow_up_post_creates_new_message(
        self, customer_client, customer_user, replied_message
    ):
        """POST follow-up creates a new CustomerMessage."""
        url = reverse('accounts:message_detail', kwargs={'message_id': replied_message.pk})
        initial_count = CustomerMessage.objects.count()

        customer_client.post(url, {
            'action': 'follow_up',
            'message': 'This is my follow-up response.',
        })

        assert CustomerMessage.objects.count() == initial_count + 1

    def test_follow_up_post_sets_re_prefix(
        self, customer_client, customer_user, replied_message
    ):
        """Follow-up message subject has 'Re:' prefix from original subject."""
        url = reverse('accounts:message_detail', kwargs={'message_id': replied_message.pk})
        customer_client.post(url, {
            'action': 'follow_up',
            'message': 'Follow-up text here.',
        })

        follow_up = CustomerMessage.objects.order_by('-created_at').first()
        assert follow_up.subject == f"Re: {replied_message.subject}"

    def test_follow_up_post_copies_message_type_and_order(
        self, customer_client, customer_user, customer_order
    ):
        """Follow-up copies message_type and order from the original message."""
        original = CustomerMessageFactory(
            user=customer_user,
            replied=True,
            message_type='order',
            order=customer_order,
        )
        url = reverse('accounts:message_detail', kwargs={'message_id': original.pk})
        customer_client.post(url, {
            'action': 'follow_up',
            'message': 'About my order again.',
        })

        follow_up = CustomerMessage.objects.order_by('-created_at').first()
        assert follow_up.message_type == 'order'
        assert follow_up.order == customer_order

    def test_follow_up_post_sets_user_fields(
        self, customer_client, customer_user, replied_message
    ):
        """Follow-up sets user FK, name, and email from request.user."""
        customer_user.first_name = 'Jane'
        customer_user.last_name = 'Doe'
        customer_user.save()

        url = reverse('accounts:message_detail', kwargs={'message_id': replied_message.pk})
        customer_client.post(url, {
            'action': 'follow_up',
            'message': 'Follow-up with user info.',
        })

        follow_up = CustomerMessage.objects.order_by('-created_at').first()
        assert follow_up.user == customer_user
        assert follow_up.name == 'Jane Doe'
        assert follow_up.email == customer_user.email

    def test_follow_up_post_sets_status_unread(
        self, customer_client, replied_message
    ):
        """Follow-up message status is set to 'unread'."""
        url = reverse('accounts:message_detail', kwargs={'message_id': replied_message.pk})
        customer_client.post(url, {
            'action': 'follow_up',
            'message': 'Another follow-up.',
        })

        follow_up = CustomerMessage.objects.order_by('-created_at').first()
        assert follow_up.status == 'unread'

    def test_follow_up_post_redirects_to_detail_page(
        self, customer_client, replied_message
    ):
        """Follow-up POST redirects back to the same detail page."""
        url = reverse('accounts:message_detail', kwargs={'message_id': replied_message.pk})
        response = customer_client.post(url, {
            'action': 'follow_up',
            'message': 'Redirect test.',
        })

        assert response.status_code == 302
        assert str(replied_message.pk) in response.url

    def test_follow_up_post_shows_success_message(
        self, customer_client, replied_message
    ):
        """Follow-up POST triggers a Django flash success message."""
        url = reverse('accounts:message_detail', kwargs={'message_id': replied_message.pk})
        response = customer_client.post(url, {
            'action': 'follow_up',
            'message': 'Flash message test.',
        }, follow=True)

        flash_messages = list(get_messages(response.wsgi_request))
        assert len(flash_messages) > 0
        assert 'follow-up' in str(flash_messages[0]).lower()

    def test_follow_up_post_with_empty_message_shows_errors(
        self, customer_client, replied_message
    ):
        """Follow-up POST with empty message does not create a message."""
        url = reverse('accounts:message_detail', kwargs={'message_id': replied_message.pk})
        initial_count = CustomerMessage.objects.count()

        response = customer_client.post(url, {
            'action': 'follow_up',
            'message': '',
        })

        # No new message should be created
        assert CustomerMessage.objects.count() == initial_count
        # Page should re-render (200) with form errors
        assert response.status_code == 200

    def test_follow_up_post_without_action_does_not_create(
        self, customer_client, replied_message
    ):
        """POST without action='follow_up' does not create a follow-up."""
        url = reverse('accounts:message_detail', kwargs={'message_id': replied_message.pk})
        initial_count = CustomerMessage.objects.count()

        customer_client.post(url, {
            'message': 'No action field.',
        })

        assert CustomerMessage.objects.count() == initial_count

    def test_follow_up_user_name_fallback_to_email(
        self, customer_client, customer_user, replied_message
    ):
        """Follow-up name falls back to email when first/last name are empty."""
        customer_user.first_name = ''
        customer_user.last_name = ''
        customer_user.save()

        url = reverse('accounts:message_detail', kwargs={'message_id': replied_message.pk})
        customer_client.post(url, {
            'action': 'follow_up',
            'message': 'Fallback name test.',
        })

        follow_up = CustomerMessage.objects.order_by('-created_at').first()
        assert follow_up.name == customer_user.email


# ============================================================
# Views — message_new
# ============================================================

class TestMessageNewView:

    def test_returns_200_for_authenticated_user(self, customer_client):
        """New message page returns 200 for authenticated customer."""
        url = reverse('accounts:message_new')
        response = customer_client.get(url)
        assert response.status_code == 200

    def test_redirects_unauthenticated_user(self, anon_client):
        """New message page redirects unauthenticated users to login."""
        url = reverse('accounts:message_new')
        response = anon_client.get(url)
        assert response.status_code == 302
        assert '/account/login/' in response.url or '/accounts/login/' in response.url

    def test_form_in_context(self, customer_client):
        """GET renders form in context."""
        url = reverse('accounts:message_new')
        response = customer_client.get(url)
        assert 'form' in response.context
        assert isinstance(response.context['form'], CustomerMessageForm)

    def test_order_queryset_filtered_to_user(
        self, customer_client, customer_order, other_user_order
    ):
        """GET renders form with order queryset filtered to user's orders only."""
        url = reverse('accounts:message_new')
        response = customer_client.get(url)
        form = response.context['form']
        order_qs = form.fields['order'].queryset
        assert customer_order in order_qs
        assert other_user_order not in order_qs

    def test_get_with_order_param_preselects(self, customer_client, customer_order):
        """GET with ?order=<id> pre-selects that order in the form."""
        url = reverse('accounts:message_new') + f'?order={customer_order.pk}'
        response = customer_client.get(url)
        form = response.context['form']
        assert form.initial.get('order') == customer_order

    def test_get_with_invalid_order_param_does_not_crash(self, customer_client):
        """GET with ?order=999 (nonexistent) does not crash."""
        url = reverse('accounts:message_new') + '?order=999999'
        response = customer_client.get(url)
        assert response.status_code == 200
        form = response.context['form']
        # No order pre-selected
        assert form.initial.get('order') is None

    def test_get_with_other_users_order_param_does_not_preselect(
        self, customer_client, other_user_order
    ):
        """GET with another user's order ID does not pre-select it."""
        url = reverse('accounts:message_new') + f'?order={other_user_order.pk}'
        response = customer_client.get(url)
        form = response.context['form']
        assert form.initial.get('order') is None

    def test_post_with_valid_data_creates_message(self, customer_client, customer_user):
        """POST with valid data creates a new CustomerMessage."""
        url = reverse('accounts:message_new')
        initial_count = CustomerMessage.objects.count()

        customer_client.post(url, {
            'subject': 'Test Subject',
            'message': 'Test message body content.',
            'message_type': 'general',
        })

        assert CustomerMessage.objects.count() == initial_count + 1
        msg = CustomerMessage.objects.order_by('-created_at').first()
        assert msg.subject == 'Test Subject'
        assert msg.message == 'Test message body content.'
        assert msg.message_type == 'general'

    def test_post_sets_user_and_metadata(self, customer_client, customer_user):
        """POST sets user FK, name, email, ip_address, user_agent."""
        customer_user.first_name = 'John'
        customer_user.last_name = 'Smith'
        customer_user.save()

        url = reverse('accounts:message_new')
        customer_client.post(
            url,
            {
                'subject': 'Metadata Test',
                'message': 'Checking metadata fields.',
                'message_type': 'support',
            },
            HTTP_USER_AGENT='TestBrowser/1.0',
        )

        msg = CustomerMessage.objects.order_by('-created_at').first()
        assert msg.user == customer_user
        assert msg.name == 'John Smith'
        assert msg.email == customer_user.email
        assert msg.ip_address is not None
        assert msg.user_agent == 'TestBrowser/1.0'

    def test_post_sets_status_unread(self, customer_client):
        """POST creates message with status 'unread'."""
        url = reverse('accounts:message_new')
        customer_client.post(url, {
            'subject': 'Status Test',
            'message': 'Check status is unread.',
            'message_type': 'general',
        })

        msg = CustomerMessage.objects.order_by('-created_at').first()
        assert msg.status == 'unread'

    def test_post_with_order_links_message(self, customer_client, customer_order):
        """POST with valid order ID links the message to that order."""
        url = reverse('accounts:message_new')
        customer_client.post(url, {
            'subject': 'Order Question',
            'message': 'Question about my order.',
            'message_type': 'order',
            'order': customer_order.pk,
        })

        msg = CustomerMessage.objects.order_by('-created_at').first()
        assert msg.order == customer_order

    def test_post_without_order_leaves_order_null(self, customer_client):
        """POST without order field leaves order as None."""
        url = reverse('accounts:message_new')
        customer_client.post(url, {
            'subject': 'General Question',
            'message': 'No order related.',
            'message_type': 'general',
        })

        msg = CustomerMessage.objects.order_by('-created_at').first()
        assert msg.order is None

    def test_post_redirects_to_detail_page(self, customer_client):
        """POST with valid data redirects to the detail page of the new message."""
        url = reverse('accounts:message_new')
        response = customer_client.post(url, {
            'subject': 'Redirect Test',
            'message': 'Should redirect to detail.',
            'message_type': 'general',
        })

        assert response.status_code == 302
        msg = CustomerMessage.objects.order_by('-created_at').first()
        expected_url = reverse('accounts:message_detail', kwargs={'message_id': msg.pk})
        assert expected_url in response.url

    def test_post_shows_success_flash_message(self, customer_client):
        """POST triggers a Django flash success message."""
        url = reverse('accounts:message_new')
        response = customer_client.post(url, {
            'subject': 'Flash Test',
            'message': 'Flash message check.',
            'message_type': 'general',
        }, follow=True)

        flash_messages = list(get_messages(response.wsgi_request))
        assert len(flash_messages) > 0
        assert 'submitted' in str(flash_messages[0]).lower() or 'sent' in str(flash_messages[0]).lower()

    def test_post_missing_subject_shows_errors(self, customer_client):
        """POST without required subject field shows form errors."""
        url = reverse('accounts:message_new')
        response = customer_client.post(url, {
            'message': 'No subject provided.',
            'message_type': 'general',
        })

        # Should re-render form (200), not redirect (302)
        assert response.status_code == 200
        form = response.context['form']
        assert 'subject' in form.errors

    def test_post_missing_message_shows_errors(self, customer_client):
        """POST without required message field shows form errors."""
        url = reverse('accounts:message_new')
        response = customer_client.post(url, {
            'subject': 'Missing Body',
            'message_type': 'general',
        })

        assert response.status_code == 200
        form = response.context['form']
        assert 'message' in form.errors

    def test_post_with_other_users_order_is_rejected(
        self, customer_client, other_user_order
    ):
        """POST with order ID belonging to another user is rejected by queryset filtering."""
        url = reverse('accounts:message_new')
        response = customer_client.post(url, {
            'subject': 'Sneaky Order',
            'message': 'Trying to link another user order.',
            'message_type': 'order',
            'order': other_user_order.pk,
        })

        # Form should show order validation error (invalid choice)
        assert response.status_code == 200
        form = response.context['form']
        assert 'order' in form.errors

    def test_post_user_name_fallback_to_email(self, customer_client, customer_user):
        """When user has no first/last name, name falls back to email."""
        customer_user.first_name = ''
        customer_user.last_name = ''
        customer_user.save()

        url = reverse('accounts:message_new')
        customer_client.post(url, {
            'subject': 'Name Fallback',
            'message': 'User without names.',
            'message_type': 'general',
        })

        msg = CustomerMessage.objects.order_by('-created_at').first()
        assert msg.name == customer_user.email


# ============================================================
# Views — dashboard unread_reply_count
# ============================================================

class TestDashboardUnreadReplyCount:

    def test_dashboard_context_includes_unread_reply_count(self, customer_client):
        """Dashboard context includes unread_reply_count key."""
        url = reverse('accounts:dashboard')
        response = customer_client.get(url)
        assert response.status_code == 200
        assert 'unread_reply_count' in response.context

    def test_count_reflects_replied_messages(self, customer_client, customer_user):
        """unread_reply_count counts messages with status='replied' for the user."""
        CustomerMessageFactory(user=customer_user, replied=True)
        CustomerMessageFactory(user=customer_user, replied=True)
        # This one is 'unread', should NOT be counted
        CustomerMessageFactory(user=customer_user, status='unread')

        url = reverse('accounts:dashboard')
        response = customer_client.get(url)
        assert response.context['unread_reply_count'] == 2

    def test_count_includes_email_fallback_messages(self, customer_client, customer_user):
        """unread_reply_count includes anonymous replied messages matching user email."""
        # Replied anonymous message matching customer email
        CustomerMessageFactory(
            anonymous=True,
            email=customer_user.email,
            name='Anon',
            replied=True,
        )
        # Replied message with user FK
        CustomerMessageFactory(user=customer_user, replied=True)

        url = reverse('accounts:dashboard')
        response = customer_client.get(url)
        assert response.context['unread_reply_count'] == 2

    def test_count_excludes_other_users_messages(self, customer_client, other_user):
        """unread_reply_count does not count messages belonging to other users."""
        CustomerMessageFactory(user=other_user, replied=True)

        url = reverse('accounts:dashboard')
        response = customer_client.get(url)
        assert response.context['unread_reply_count'] == 0

    def test_count_zero_when_no_replied_messages(self, customer_client, customer_user):
        """unread_reply_count is 0 when user has no replied messages."""
        # Only unread messages, no replied ones
        CustomerMessageFactory(user=customer_user, status='unread')
        CustomerMessageFactory(user=customer_user, status='read')

        url = reverse('accounts:dashboard')
        response = customer_client.get(url)
        assert response.context['unread_reply_count'] == 0


# ============================================================
# Forms — CustomerMessageForm
# ============================================================

class TestCustomerMessageForm:

    def test_valid_data_passes_validation(self, customer_user):
        """Form is valid with all required fields and valid order queryset."""
        from orders.models import Order
        form = CustomerMessageForm(data={
            'subject': 'Test Subject',
            'message': 'Test message body.',
            'message_type': 'general',
        })
        form.fields['order'].queryset = Order.objects.none()
        assert form.is_valid()

    def test_subject_required(self):
        """Form requires subject field."""
        from orders.models import Order
        form = CustomerMessageForm(data={
            'message': 'Body only.',
            'message_type': 'general',
        })
        form.fields['order'].queryset = Order.objects.none()
        assert not form.is_valid()
        assert 'subject' in form.errors

    def test_message_required(self):
        """Form requires message field."""
        from orders.models import Order
        form = CustomerMessageForm(data={
            'subject': 'Subject only.',
            'message_type': 'general',
        })
        form.fields['order'].queryset = Order.objects.none()
        assert not form.is_valid()
        assert 'message' in form.errors

    def test_subject_max_length_enforced(self):
        """Subject field enforces max_length=300."""
        from orders.models import Order
        form = CustomerMessageForm(data={
            'subject': 'x' * 301,
            'message': 'Body.',
            'message_type': 'general',
        })
        form.fields['order'].queryset = Order.objects.none()
        assert not form.is_valid()
        assert 'subject' in form.errors

    def test_subject_at_max_length_is_valid(self):
        """Subject field at exactly max_length=300 is valid."""
        from orders.models import Order
        form = CustomerMessageForm(data={
            'subject': 'x' * 300,
            'message': 'Body.',
            'message_type': 'general',
        })
        form.fields['order'].queryset = Order.objects.none()
        assert form.is_valid()

    def test_message_max_length_enforced(self):
        """Message field enforces max_length=5000."""
        from orders.models import Order
        form = CustomerMessageForm(data={
            'subject': 'Subject',
            'message': 'x' * 5001,
            'message_type': 'general',
        })
        form.fields['order'].queryset = Order.objects.none()
        assert not form.is_valid()
        assert 'message' in form.errors

    def test_order_is_optional(self, customer_user):
        """Order field is not required."""
        from orders.models import Order
        form = CustomerMessageForm(data={
            'subject': 'No Order',
            'message': 'Message without order.',
            'message_type': 'general',
        })
        form.fields['order'].queryset = Order.objects.none()
        assert form.is_valid()

    def test_message_type_defaults_to_general(self):
        """Message type initial value is 'general'."""
        from orders.models import Order
        form = CustomerMessageForm()
        form.fields['order'].queryset = Order.objects.none()
        assert form.fields['message_type'].initial == 'general'

    def test_valid_message_types_accepted(self):
        """All defined message types are accepted."""
        from orders.models import Order
        for type_value, _label in CustomerMessageForm.MESSAGE_TYPE_CHOICES:
            form = CustomerMessageForm(data={
                'subject': 'Type Test',
                'message': 'Body.',
                'message_type': type_value,
            })
            form.fields['order'].queryset = Order.objects.none()
            assert form.is_valid(), f"message_type '{type_value}' should be valid"

    def test_invalid_message_type_rejected(self):
        """Invalid message type is rejected."""
        from orders.models import Order
        form = CustomerMessageForm(data={
            'subject': 'Type Test',
            'message': 'Body.',
            'message_type': 'invalid_type',
        })
        form.fields['order'].queryset = Order.objects.none()
        assert not form.is_valid()
        assert 'message_type' in form.errors


# ============================================================
# Forms — FollowUpMessageForm
# ============================================================

class TestFollowUpMessageForm:

    def test_valid_data_passes_validation(self):
        """FollowUp form is valid with a non-empty message."""
        form = FollowUpMessageForm(data={
            'message': 'This is a follow-up.',
        })
        assert form.is_valid()

    def test_message_required(self):
        """FollowUp form requires message field."""
        form = FollowUpMessageForm(data={
            'message': '',
        })
        assert not form.is_valid()
        assert 'message' in form.errors

    def test_message_missing_key_fails(self):
        """FollowUp form fails when message key is absent."""
        form = FollowUpMessageForm(data={})
        assert not form.is_valid()
        assert 'message' in form.errors

    def test_message_max_length_enforced(self):
        """FollowUp form enforces max_length=5000 on message."""
        form = FollowUpMessageForm(data={
            'message': 'x' * 5001,
        })
        assert not form.is_valid()
        assert 'message' in form.errors

    def test_message_at_max_length_is_valid(self):
        """FollowUp form with message at exactly 5000 chars is valid."""
        form = FollowUpMessageForm(data={
            'message': 'x' * 5000,
        })
        assert form.is_valid()


# ============================================================
# Security
# ============================================================

class TestMessageSecurity:

    def test_all_message_endpoints_require_auth(self, anon_client, customer_message):
        """All message endpoints redirect unauthenticated users."""
        endpoints = [
            reverse('accounts:message_list'),
            reverse('accounts:message_new'),
            reverse('accounts:message_detail', kwargs={'message_id': customer_message.pk}),
        ]
        for url in endpoints:
            response = anon_client.get(url)
            assert response.status_code == 302, (
                f'GET {url} returned {response.status_code}, expected 302 redirect'
            )

    def test_user_cannot_access_other_users_message(self, customer_client, other_user):
        """Authenticated user cannot view messages belonging to other users."""
        other_msg = CustomerMessageFactory(user=other_user)
        url = reverse('accounts:message_detail', kwargs={'message_id': other_msg.pk})
        response = customer_client.get(url)
        assert response.status_code == 404

    def test_user_cannot_link_other_users_order_via_post(
        self, customer_client, other_user_order
    ):
        """User cannot associate another user's order with a new message."""
        url = reverse('accounts:message_new')
        response = customer_client.post(url, {
            'subject': 'Security Test',
            'message': 'Attempting to link foreign order.',
            'message_type': 'order',
            'order': other_user_order.pk,
        })

        # Should fail validation, not create
        assert response.status_code == 200
        form = response.context['form']
        assert 'order' in form.errors
        # No message should have been created with the foreign order
        assert not CustomerMessage.objects.filter(order=other_user_order).exists()

    def test_nonexistent_message_returns_404(self, customer_client):
        """Accessing a nonexistent message ID returns 404."""
        url = reverse('accounts:message_detail', kwargs={'message_id': 999999})
        response = customer_client.get(url)
        assert response.status_code == 404
