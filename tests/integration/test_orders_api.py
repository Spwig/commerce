"""
API integration tests for orders app ViewSets.

Tests REST API endpoints for:
- OrderViewSet
- AddressViewSet
- ReturnRequestViewSet
"""
import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from orders.models import Order, Address, OrderNote, ReturnRequest
from tests.factories import (
    UserFactory,
    ProductFactory,
    OrderFactory,
    OrderItemFactory,
    AddressFactory,
    OrderNoteFactory,
    ReturnRequestFactory,
)

User = get_user_model()


@pytest.mark.django_db
class TestOrderAPI:
    """API tests for OrderViewSet."""

    def setup_method(self):
        """Set up test client and user."""
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_list_orders_pagination(self):
        """Test listing orders with pagination."""
        # Create multiple orders
        for _ in range(15):
            OrderFactory(user=self.user)

        url = reverse('order-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'count' in response.data
        assert response.data['count'] == 15

    def test_retrieve_order_detail(self):
        """Test retrieving a single order's details."""
        order = OrderFactory(user=self.user)
        OrderItemFactory(order=order, quantity=2)
        OrderItemFactory(order=order, quantity=1)

        url = reverse('order-detail', kwargs={'pk': order.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == order.id
        assert response.data['order_number'] == order.order_number
        assert len(response.data['items']) == 2

    def test_cancel_order_endpoint(self):
        """Test cancelling an order via API."""
        order = OrderFactory(user=self.user, status='processing')

        url = reverse('order-cancel', kwargs={'pk': order.id})
        data = {'reason': 'Changed my mind'}
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK

        order.refresh_from_db()
        assert order.status == 'cancelled'

    def test_cancel_order_not_cancellable(self):
        """Test cancelling non-cancellable order returns error."""
        order = OrderFactory(user=self.user, status='delivered')

        url = reverse('order-cancel', kwargs={'pk': order.id})
        data = {'reason': 'Too late'}
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_reorder_endpoint(self):
        """Test reorder endpoint creates new cart from order."""
        order = OrderFactory(user=self.user)
        product1 = ProductFactory(price=Decimal('25.00'))
        product2 = ProductFactory(price=Decimal('35.00'))

        OrderItemFactory(order=order, product=product1, quantity=2)
        OrderItemFactory(order=order, product=product2, quantity=1)

        url = reverse('order-reorder', kwargs={'pk': order.id})
        response = self.client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'cart_id' in response.data

    def test_get_tracking_info(self):
        """Test getting tracking information for order."""
        order = OrderFactory(user=self.user, with_tracking=True)

        url = reverse('order-tracking', kwargs={'pk': order.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'tracking_number' in response.data
        assert response.data['tracking_number'] == order.tracking_number

    def test_get_order_statistics(self):
        """Test getting user's order statistics."""
        # Create multiple orders
        OrderFactory(user=self.user, status='delivered', total_amount=Decimal('100.00'), paid_order=True)
        OrderFactory(user=self.user, status='delivered', total_amount=Decimal('150.00'), paid_order=True)
        OrderFactory(user=self.user, status='cancelled', total_amount=Decimal('50.00'))

        url = reverse('order-statistics')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'total_orders' in response.data
        assert 'total_spent' in response.data
        assert response.data['total_orders'] == 3

    def test_add_order_note(self):
        """Test adding a note to an order."""
        order = OrderFactory(user=self.user)

        url = reverse('order-add-note', kwargs={'pk': order.id})
        data = {'note': 'Please deliver after 5 PM', 'is_customer_note': True}
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        # Verify note was created
        assert OrderNote.objects.filter(order=order, is_customer_note=True).exists()

    def test_generate_packing_slip(self):
        """Test generating packing slip for order."""
        order = OrderFactory(user=self.user)
        OrderItemFactory(order=order)

        url = reverse('order-packing-slip', kwargs={'pk': order.id})
        response = self.client.get(url)

        # Assuming packing slip returns PDF or HTML
        assert response.status_code == status.HTTP_200_OK

    def test_unauthorized_access_denied(self):
        """Test that unauthenticated users cannot access orders."""
        # Create unauthenticated client
        unauth_client = APIClient()

        order = OrderFactory(user=self.user)
        url = reverse('order-detail', kwargs={'pk': order.id})
        response = unauth_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_cannot_access_other_users_orders(self):
        """Test that users cannot access other users' orders."""
        other_user = UserFactory()
        other_order = OrderFactory(user=other_user)

        url = reverse('order-detail', kwargs={'pk': other_order.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestAddressAPI:
    """API tests for AddressViewSet."""

    def setup_method(self):
        """Set up test client and user."""
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_list_user_addresses(self):
        """Test listing user's addresses."""
        # Create addresses for user
        AddressFactory(user=self.user)
        AddressFactory(user=self.user)

        # Create address for different user (should not appear)
        other_user = UserFactory()
        AddressFactory(user=other_user)

        url = reverse('address-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_address(self):
        """Test creating a new address via API."""
        url = reverse('address-list')
        data = {
            'name': 'John Doe',
            'address1': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'postal_code': '10001',
            'country': 'US',
            'address_type': 'shipping',
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Address.objects.filter(user=self.user, address1='123 Main St').exists()

    def test_update_address(self):
        """Test updating an existing address."""
        address = AddressFactory(user=self.user, address1='123 Old St')

        url = reverse('address-detail', kwargs={'pk': address.id})
        data = {'address1': '456 New St'}
        response = self.client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK

        address.refresh_from_db()
        assert address.address1 == '456 New St'

    def test_delete_address(self):
        """Test deleting an address."""
        address = AddressFactory(user=self.user)

        url = reverse('address-detail', kwargs={'pk': address.id})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Address.objects.filter(id=address.id).exists()

    def test_delete_address_used_in_orders_prevented(self):
        """Test that addresses used in orders cannot be deleted."""
        address = AddressFactory(user=self.user)
        OrderFactory(user=self.user, shipping_address_ref=address)

        url = reverse('address-detail', kwargs={'pk': address.id})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Address.objects.filter(id=address.id).exists()

    def test_set_default_address(self):
        """Test setting an address as default."""
        address1 = AddressFactory(user=self.user, address_type='shipping', default_address=True)
        address2 = AddressFactory(user=self.user, address_type='shipping', is_default=False)

        url = reverse('address-set-default', kwargs={'pk': address2.id})
        response = self.client.post(url)

        assert response.status_code == status.HTTP_200_OK

        address1.refresh_from_db()
        address2.refresh_from_db()

        assert address1.is_default is False
        assert address2.is_default is True

    def test_filter_by_address_type(self):
        """Test filtering addresses by type."""
        AddressFactory(user=self.user, address_type='shipping')
        AddressFactory(user=self.user, address_type='shipping')
        AddressFactory(user=self.user, address_type='billing')

        url = reverse('address-list')
        response = self.client.get(url, {'address_type': 'shipping'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2


@pytest.mark.django_db
class TestReturnRequestAPI:
    """API tests for ReturnRequestViewSet."""

    def setup_method(self):
        """Set up test client and user."""
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_return_request(self):
        """Test creating a return request."""
        order = OrderFactory(user=self.user, delivered=True, paid_order=True)
        product = ProductFactory()
        order_item = OrderItemFactory(order=order, product=product, quantity=2)

        url = reverse('returnrequest-list')
        data = {
            'order': order.id,
            'reason': 'Product defective',
            'items_json': [
                {
                    'order_item_id': order_item.id,
                    'quantity': 1,
                    'reason': 'Defective',
                }
            ],
            'customer_notes': 'Item arrived damaged',
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert ReturnRequest.objects.filter(order=order).exists()

    def test_list_user_returns(self):
        """Test listing user's return requests."""
        order1 = OrderFactory(user=self.user)
        order2 = OrderFactory(user=self.user)

        ReturnRequestFactory(order=order1, user=self.user)
        ReturnRequestFactory(order=order2, user=self.user)

        # Create return for different user (should not appear)
        other_user = UserFactory()
        other_order = OrderFactory(user=other_user)
        ReturnRequestFactory(order=other_order, user=other_user)

        url = reverse('returnrequest-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2

    def test_retrieve_return_detail(self):
        """Test retrieving return request details."""
        order = OrderFactory(user=self.user)
        return_request = ReturnRequestFactory(order=order, user=self.user)

        url = reverse('returnrequest-detail', kwargs={'pk': return_request.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == return_request.id
        assert response.data['order'] == order.id

    def test_get_return_label(self):
        """Test getting return shipping label."""
        order = OrderFactory(user=self.user)
        return_request = ReturnRequestFactory(
            order=order,
            user=self.user,
            label_sent=True,
        )

        url = reverse('returnrequest-get-label', kwargs={'pk': return_request.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'label_url' in response.data or 'tracking_number' in response.data

    def test_user_cannot_create_return_for_other_users_order(self):
        """Test that users cannot create returns for other users' orders."""
        other_user = UserFactory()
        other_order = OrderFactory(user=other_user)

        url = reverse('returnrequest-list')
        data = {
            'order': other_order.id,
            'reason': 'Trying to return someone else order',
            'items_json': [],
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestOrderAPIPagination:
    """Test pagination and filtering for order list endpoint."""

    def setup_method(self):
        """Set up test client and user."""
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_pagination_default_page_size(self):
        """Test default pagination page size."""
        # Create 25 orders
        for _ in range(25):
            OrderFactory(user=self.user)

        url = reverse('order-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'next' in response.data
        assert response.data['count'] == 25

    def test_pagination_custom_page_size(self):
        """Test custom pagination page size."""
        for _ in range(25):
            OrderFactory(user=self.user)

        url = reverse('order-list')
        response = self.client.get(url, {'page_size': 5})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5

    def test_filter_by_status(self):
        """Test filtering orders by status."""
        OrderFactory(user=self.user, status='processing')
        OrderFactory(user=self.user, status='processing')
        OrderFactory(user=self.user, status='shipped')
        OrderFactory(user=self.user, status='delivered')

        url = reverse('order-list')
        response = self.client.get(url, {'status': 'processing'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2

    def test_filter_by_date_range(self):
        """Test filtering orders by date range."""
        from datetime import datetime, timedelta
        from django.utils import timezone

        # Create orders with different dates
        old_order = OrderFactory(user=self.user)
        old_order.created_at = timezone.now() - timedelta(days=60)
        old_order.save()

        recent_order = OrderFactory(user=self.user)

        url = reverse('order-list')
        start_date = (timezone.now() - timedelta(days=30)).isoformat()
        response = self.client.get(url, {'created_after': start_date})

        assert response.status_code == status.HTTP_200_OK
        # Should only include recent order


@pytest.mark.django_db
class TestOrderAPIPermissions:
    """Test permission and authorization for order API."""

    def test_staff_can_access_all_orders(self):
        """Test that staff users can access all orders."""
        staff_user = UserFactory(staff=True)
        client = APIClient()
        client.force_authenticate(user=staff_user)

        # Create orders for different users
        user1 = UserFactory()
        user2 = UserFactory()
        OrderFactory(user=user1)
        OrderFactory(user=user2)

        url = reverse('order-list')
        response = client.get(url)

        # Staff should see all orders (depending on permission implementation)
        assert response.status_code == status.HTTP_200_OK

    def test_guest_cannot_access_orders(self):
        """Test that unauthenticated users cannot access order endpoints."""
        client = APIClient()  # No authentication

        url = reverse('order-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
