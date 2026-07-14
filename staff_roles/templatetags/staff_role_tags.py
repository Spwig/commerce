"""
Template tags for role-based permission checks in templates.
"""

from django import template

from staff_roles.services import can_access_admin, get_user_roles, has_category_access

register = template.Library()


@register.simple_tag
def has_category(user, category_key, level="view"):
    """
    Check if a user has access to a permission category.

    Usage:
        {% load staff_role_tags %}
        {% has_category user 'catalog' as can_view_catalog %}
        {% if can_view_catalog %}...{% endif %}

        {% has_category user 'catalog' 'full' as can_edit_catalog %}
    """
    if not user or not user.is_authenticated:
        return False
    return has_category_access(user, category_key, level)


@register.simple_tag
def user_roles(user):
    """
    Get all StaffRole objects for a user.

    Usage:
        {% user_roles user as roles %}
        {% for role in roles %}{{ role.display_name }}{% endfor %}
    """
    if not user or not user.is_authenticated:
        return []
    return get_user_roles(user)


@register.inclusion_tag("staff_roles/role_badge.html")
def role_badge(role):
    """
    Render a colored badge for a role.

    Usage:
        {% role_badge role %}
    """
    return {"role": role}


@register.simple_tag
def user_can_access_admin(user):
    """
    Check if a user can access the admin panel.

    Usage:
        {% user_can_access_admin user as can_admin %}
    """
    if not user or not user.is_authenticated:
        return False
    return can_access_admin(user)
