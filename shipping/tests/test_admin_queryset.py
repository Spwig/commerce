"""Regression tests for CarrierPresetAdmin.get_queryset.

Previously the get_queryset method used Q(...) without importing Q, so
any changelist visit with the country=NONE param or a search query
raised NameError.
"""

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from shipping.admin import CarrierPresetAdmin
from shipping.models import CarrierPreset

User = get_user_model()


class CarrierPresetAdminQuerysetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin_regression",
            email="admin_regression@example.com",
            password="pw",
        )
        self.admin = CarrierPresetAdmin(CarrierPreset, AdminSite())

    def _request(self, **params):
        rf = RequestFactory()
        request = rf.get("/en/admin/shipping/carrierpreset/", params)
        request.user = self.user
        return request

    def test_get_queryset_with_country_none_does_not_raise(self):
        qs = self.admin.get_queryset(self._request(country="NONE"))
        list(qs)  # force evaluation — would NameError without Q import

    def test_get_queryset_with_search_query_does_not_raise(self):
        qs = self.admin.get_queryset(self._request(q="ups"))
        list(qs)
