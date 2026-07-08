from django.urls import path
from .api_views import ActiveAnnouncementsView, AnnouncementDetailView

urlpatterns = [
    path('active/', ActiveAnnouncementsView.as_view(), name='announcements_active'),
    path('<int:pk>/detail/', AnnouncementDetailView.as_view(), name='announcement_detail'),
]
