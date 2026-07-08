"""
Template tags for affiliate functionality
"""
from django import template
from affiliate.models import Affiliate

register = template.Library()


@register.simple_tag
def get_active_affiliates():
    """
    Get all active affiliates for dropdown selection
    """
    return Affiliate.objects.filter(status='active').select_related('user').order_by('user__first_name', 'user__last_name')
