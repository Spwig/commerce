"""
Template tags for visibility rules
"""

from django import template
from django.utils.safestring import mark_safe
from ..visibility_evaluator import ContextCollector
import json

register = template.Library()


@register.simple_tag(takes_context=True)
def check_element_visibility(context, element):
    """
    Check if an element should be visible based on its visibility rules

    Usage:
        {% load visibility_tags %}
        {% check_element_visibility element as is_visible %}
        {% if is_visible %}
            <!-- Render element -->
        {% endif %}
    """
    request = context.get('request')
    if not request:
        return True  # Default to visible if no request context

    return element.check_visibility(request)


@register.inclusion_tag('page_builder/element_wrapper.html', takes_context=True)
def render_element_with_visibility(context, element, extra_classes=""):
    """
    Render an element with visibility checking

    Usage:
        {% load visibility_tags %}
        {% render_element_with_visibility element %}
    """
    request = context.get('request')
    is_visible = element.check_visibility(request) if request else True

    return {
        'element': element,
        'is_visible': is_visible,
        'extra_classes': extra_classes,
        'request': request,
    }


@register.filter
def is_visible(element, request):
    """
    Filter to check element visibility

    Usage:
        {% if element|is_visible:request %}
            <!-- Render element -->
        {% endif %}
    """
    return element.check_visibility(request)


@register.simple_tag(takes_context=True)
def visibility_debug(context, element):
    """
    Debug tag to show why an element is visible/hidden
    Only works when DEBUG is True

    Usage:
        {% load visibility_tags %}
        {% visibility_debug element %}
    """
    from django.conf import settings

    if not settings.DEBUG:
        return ""

    request = context.get('request')
    if not request:
        return mark_safe('<div class="visibility-debug">No request context</div>')

    # Collect context
    collector = ContextCollector()
    eval_context = collector.collect_context(request)

    # Check basic visibility
    result = {
        'is_active': element.is_active,
        'show_on_mobile': element.show_on_mobile,
        'show_on_tablet': element.show_on_tablet,
        'show_on_desktop': element.show_on_desktop,
        'has_rules': element.visibility_rules.exists(),
    }

    # Check each rule group
    if element.visibility_rules.exists():
        rule_results = []
        for rule_group in element.visibility_rules.filter(is_active=True):
            group_result = {
                'name': rule_group.name,
                'logic': rule_group.logic_operator,
                'result': rule_group.evaluate(eval_context),
                'rules': []
            }

            # Check individual rules
            for rule in rule_group.rules.filter(is_active=True):
                rule_result = {
                    'name': rule.name,
                    'type': rule.get_rule_type_display(),
                    'operator': rule.operator,
                    'value': rule.value,
                    'result': rule.evaluate(eval_context)
                }
                group_result['rules'].append(rule_result)

            rule_results.append(group_result)

        result['rule_groups'] = rule_results

    # Determine final visibility
    result['final_visibility'] = element.check_visibility(request)

    # Format as HTML
    html = '<div class="visibility-debug" style="'
    html += 'background: #f8f9fa; border: 2px solid #007bff; '
    html += 'padding: 10px; margin: 10px 0; border-radius: 5px; '
    html += 'font-size: 12px; font-family: monospace;">'
    html += f'<h4 style="margin: 0 0 10px 0; color: #007bff;">Visibility Debug: {element.name}</h4>'
    html += f'<pre style="margin: 0; white-space: pre-wrap;">{json.dumps(result, indent=2)}</pre>'
    html += '</div>'

    return mark_safe(html)


@register.simple_tag
def visibility_context_info(request):
    """
    Display current context information for debugging

    Usage:
        {% load visibility_tags %}
        {% visibility_context_info request %}
    """
    from django.conf import settings

    if not settings.DEBUG:
        return ""

    collector = ContextCollector()
    context = collector.collect_context(request)

    # Remove sensitive data
    if 'user' in context:
        context['user'] = {
            'is_authenticated': context['user']['is_authenticated'],
            'groups': context['user']['groups'],
            'segment': context['user'].get('segment'),
        }

    html = '<div class="context-debug" style="'
    html += 'background: #e8f4fd; border: 2px solid #17a2b8; '
    html += 'padding: 10px; margin: 10px 0; border-radius: 5px; '
    html += 'font-size: 11px; font-family: monospace;">'
    html += '<h4 style="margin: 0 0 10px 0; color: #17a2b8;">Current Context</h4>'
    html += '<pre style="margin: 0; white-space: pre-wrap; max-height: 300px; overflow-y: auto;">'
    html += json.dumps(context, indent=2, default=str)
    html += '</pre></div>'

    return mark_safe(html)


@register.inclusion_tag('page_builder/visibility_rules_summary.html')
def visibility_rules_summary(element):
    """
    Display a summary of visibility rules for an element

    Usage:
        {% load visibility_tags %}
        {% visibility_rules_summary element %}
    """
    rules_summary = []

    for rule_group in element.visibility_rules.filter(is_active=True):
        group_info = {
            'name': rule_group.name,
            'logic': rule_group.get_logic_operator_display(),
            'rules': []
        }

        for rule in rule_group.rules.filter(is_active=True).order_by('rulegroupmember__order'):
            rule_info = {
                'name': rule.name,
                'type': rule.get_rule_type_display(),
                'operator': rule.get_operator_display() if hasattr(rule, 'get_operator_display') else rule.operator,
                'value': rule.value,
            }
            group_info['rules'].append(rule_info)

        rules_summary.append(group_info)

    return {
        'element': element,
        'rules_summary': rules_summary,
        'has_rules': len(rules_summary) > 0,
    }