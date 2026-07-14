"""
Customer Messages API URL Configuration

Endpoints for customer messages and contact form.
Accessed via /api/messages/
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from . import messages

# Router for ViewSet
router = DefaultRouter()
router.register(r"", messages.CustomerMessageViewSet, basename="customer-message")

urlpatterns = [
    # Public contact form endpoints
    path("contact/", messages.submit_contact_form, name="contact-submit"),
    path("contact/subjects/", messages.get_contact_subjects, name="contact-subjects"),
]

# Add router URLs for authenticated message viewing
urlpatterns += router.urls
