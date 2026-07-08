from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import Max
from functools import wraps
from pathlib import Path
import json
import logging
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .models import Page, Element, PageVersion, PagePublishHistory, RuleGroup, VisibilityRule, RuleGroupMember
logger = logging.getLogger(__name__)

def staff_required_api(view_func):
    """Custom decorator for API views that require staff access"""
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': _('Authentication required')}, status=401)
        if not request.user.is_staff:
            return JsonResponse({'error': _('Staff access required')}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapped_view


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(staff_required_api, name='dispatch')
class PageBuilderAPIView(View):
    """Base API view for page builder operations"""
    
    def get_json_data(self, request):
        """Helper to parse JSON data from request"""
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return None


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(staff_required_api, name='dispatch')
# SectionAPIView removed - sections no longer used
class RemovedSectionAPIView(PageBuilderAPIView):
    """API endpoints for managing page sections"""
    
    def post(self, request):
        """Create a new section"""
        data = self.get_json_data(request)
        if not data:
            return JsonResponse({'error': _('Invalid JSON data')}, status=400)
        
        try:
            page_id = data.get('page_id')
            order = data.get('order', 0)
            
            if not page_id:
                return JsonResponse({'error': _('page_id is required')}, status=400)
            
            page = get_object_or_404(Page, id=page_id)
            
            # Create new generic section
            section_name = data.get('name', _('New Section'))
            section = PageSection.objects.create(
                page=page,
                name=section_name,
                order=order,
                is_active=True
            )

            # Auto-create the default container for this section
            default_container = section.get_default_container()

            return JsonResponse({
                'success': True,
                'section': {
                    'id': section.id,
                    'name': section.name,
                    'order': section.order,
                    'container_id': default_container.id,
                    'html': self.render_section_html(section)
                }
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def put(self, request, section_id):
        return self.patch(request, section_id)
    
    def patch(self, request, section_id):
        """Update an existing section"""
        data = self.get_json_data(request)
        if not data:
            return JsonResponse({'error': _('Invalid JSON data')}, status=400)
        
        try:
            section = get_object_or_404(PageSection, id=section_id)
            
            # Update section fields
            if 'order' in data:
                section.order = data['order']
            if 'is_active' in data:
                section.is_active = data['is_active']
            
            section.save()
            
            return JsonResponse({
                'success': True,
                'section': {
                    'id': section.id,
                    'name': section.name,
                    'order': section.order,
                    'html': self.render_section_html(section)
                }
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def delete(self, request, section_id):
        """Delete a section"""
        try:
            section = get_object_or_404(PageSection, id=section_id)
            section.delete()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def render_section_html(self, section):
        """Helper to render section HTML"""
        try:
            from django.template.loader import render_to_string
            return render_to_string('page_builder/sections/generic.html', {
                'section': section,
                'elements': section.get_elements_ordered()
            })
        except:
            return f'<div class="section-placeholder">Section: {section.name}</div>'


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(staff_required_api, name='dispatch')
class ElementAPIView(PageBuilderAPIView):
    """API endpoints for managing section elements"""
    
    def post(self, request):
        """Create a new element"""
        data = self.get_json_data(request)
        if not data:
            return JsonResponse({'error': _('Invalid JSON data')}, status=400)
        
        try:
            # section_id = data.get('section_id')  # Sections removed
            page_id = data.get('page_id')
            parent_element_id = data.get('parent_element_id')
            element_type = data.get('element_type')
            order = data.get('order', 0)

            if not element_type:
                return JsonResponse({'error': _('element_type is required')}, status=400)

            # Need either page_id or parent_element_id
            if not page_id and not parent_element_id:
                return JsonResponse({'error': _('Either page_id or parent_element_id is required')}, status=400)

            # Get the page and parent element if provided
            page = None
            parent_element = None

            if parent_element_id:
                parent_element = get_object_or_404(Element, id=parent_element_id)
                # Use parent's page
                page = parent_element.page
            elif page_id:
                page = get_object_or_404(Page, id=page_id)
            
            # Create new element with only valid model fields
            element_data = {
                'page': page,
                'parent_element': parent_element,
                'element_type': element_type,
                'order': order,
                'is_active': True,
                'content': data.get('content', {}),
                'name': data.get('name', _('{} Element').format(element_type.title())),
            }

            # Merge config defaults into content (config defaults as base, provided content overrides)
            from .element_registry import get_registry
            registry = get_registry()
            element_config = registry.get_element(element_type)
            if element_config:
                config_defaults = element_config.config_data.get('defaults', {}) if hasattr(element_config, 'config_data') else {}
                if config_defaults:
                    merged_content = {**config_defaults, **element_data['content']}
                    element_data['content'] = merged_content

            # Filter out any invalid fields that might have been passed
            valid_fields = {field.name for field in Element._meta.get_fields()}
            filtered_data = {k: v for k, v in element_data.items() if k in valid_fields}
            
            element = Element.objects.create(**filtered_data)

            # Auto-create draft version after element creation
            page = element.page or (element.parent_element.page if element.parent_element else None)
            if page:
                draft = page.get_draft_version()
                if not draft:
                    # Create new draft if none exists
                    draft = page.create_draft_version(
                        user=request.user if request.user.is_authenticated else None,
                        description="Auto-save after element creation"
                    )
                else:
                    # Update existing draft snapshot
                    draft.create_snapshot()

            return JsonResponse({
                'success': True,
                'element': {
                    'id': element.id,
                    'element_type': element.element_type,
                    'order': element.order,
                    'content': element.content,
                    'name': element.name,
                    'html': self.render_element_html(element, request)
                },
                'draft_saved': True if page else False
            })

        except Exception as e:
            import traceback
            print(f"ElementAPIView POST Error: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            print(f"Request data: {data}")
            return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)
    
    def get(self, request, element_id):
        """Get element data"""
        try:
            element = Element.objects.get(id=element_id)
        except Element.DoesNotExist:
            return JsonResponse({'error': f'Element with id {element_id} does not exist'}, status=404)

        try:
            return JsonResponse({
                'id': element.id,
                'element_type': element.element_type,
                'name': element.name,
                'content': element.content,
                'order': element.order,
                'is_active': element.is_active,
                # 'section_id': None,  # Sections removed
                'page_id': element.page.id if element.page else None,
                'parent_element_id': element.parent_element.id if element.parent_element else None
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def put(self, request, element_id):
        return self.patch(request, element_id)
    
    def patch(self, request, element_id):
        """Update an existing element"""
        data = self.get_json_data(request)
        if not data:
            return JsonResponse({'error': _('Invalid JSON data')}, status=400)

        try:
            # Try to get the element
            try:
                element = Element.objects.get(id=element_id)
            except Element.DoesNotExist:
                # Log more details for debugging
                all_elements = list(Element.objects.values_list('id', 'element_type', 'name'))
                print(f"[ERROR] Element with id {element_id} not found")
                print(f"Available elements in DB: {all_elements}")

                # Return a more helpful error message
                return JsonResponse({
                    'error': f'Element with id {element_id} not found. This usually means the element was not properly saved when created. Please refresh the page and try again.',
                    'element_id': element_id,
                    'available_ids': [e[0] for e in all_elements]
                }, status=404)
            
            # Update element fields
            if 'order' in data:
                element.order = data['order']
            if 'content' in data:
                element.content.update(data['content'])
            if 'name' in data:
                element.name = data['name']
            if 'is_active' in data:
                element.is_active = data['is_active']
            
            element.save()

            # Auto-create draft version after element update
            page = element.page or (element.parent_element.page if element.parent_element else None)
            if page:
                draft = page.get_draft_version()
                if not draft:
                    # Create new draft if none exists
                    draft = page.create_draft_version(
                        user=request.user if request.user.is_authenticated else None,
                        description="Auto-save after element update"
                    )
                else:
                    # Update existing draft snapshot
                    draft.create_snapshot()

            return JsonResponse({
                'success': True,
                'element': {
                    'id': element.id,
                    'element_type': element.element_type,
                    'order': element.order,
                    'content': element.content,
                    'name': element.name,
                    'html': self.render_element_html(element, request)
                },
                'draft_saved': True if page else False
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, element_id):
        """Delete an element"""
        try:
            element = get_object_or_404(Element, id=element_id)
            element.delete()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def render_element_html(self, element, request=None):
        """Helper to render element HTML with wrapper"""
        try:
            from django.template.loader import render_to_string
            from .element_registry import get_registry
            from .context_providers import get_element_context, ELEMENT_CONTEXT_PROVIDERS

            registry = get_registry()
            element_config = registry.get_element(element.element_type)

            # Get dynamic context from context providers (for elements like navigation_menu)
            content = element.content or {}
            dynamic_context = {}
            if content.get('data_source') == 'dynamic' or element.element_type in ELEMENT_CONTEXT_PROVIDERS:
                dynamic_context = get_element_context(element.element_type, content, request)

            context = {
                'element': element,
                'element_config': element_config,
                'element_context': dynamic_context,
                'is_visual_builder': True,
            }

            # Use modular template if available, fallback to old template
            if element_config:
                template_path = f'page_builder/elements/{element.element_type}/template.html'
            else:
                template_path = f'page_builder/elements/{element.element_type}.html'

            # Pass request so Django creates a RequestContext and runs all
            # context processors (currency, site_settings, auth, static, etc.)
            element_inner_html = render_to_string(template_path, context, request=request)

            # Wrap the element HTML in the proper wrapper structure
            wrapped_html = f'''
            <div class="element-wrapper" data-element-id="{element.id}" data-element-type="{element.element_type}">
                <div class="element-controls">
                    <button class="control-btn edit-btn" data-action="edit-element" data-element-id="{element.id}">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="control-btn delete-btn" data-action="delete-element" data-element-id="{element.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="element-content">
                    {element_inner_html}
                </div>
            </div>
            '''

            return wrapped_html
        except Exception as e:
            return f'<div class="element-placeholder">Element: {element.element_type} (Error: {str(e)})</div>'


# Section reordering removed - sections no longer exist
# @csrf_exempt
# @staff_required_api
# @require_http_methods(["POST"])
# def reorder_sections(request):
#     pass


@extend_schema(
    tags=['Page Builder'],
    summary=_('Reorder page elements'),
    description=_('''Reorders elements within a container or moves an element to a new parent.

    **Authentication:** Staff only

    **Request body:**
    - element_orders: Array of {id, order} pairs to update
    - element_id (optional): Element being moved
    - new_parent_id (optional): Target container ID
    - new_parent_type (optional): Type of parent (always container)'''),
    responses={
        200: OpenApiResponse(description=_('Elements reordered successfully')),
        401: OpenApiResponse(description=_('Authentication required')),
        403: OpenApiResponse(description=_('Staff access required')),
        500: OpenApiResponse(description=_('Server error')),
    }
)
@csrf_exempt
@staff_required_api
@require_http_methods(["POST"])
def reorder_elements(request):
    """API endpoint to reorder elements within a section or container"""
    try:
        data = json.loads(request.body)
        element_orders = data.get('element_orders', [])

        # Check if this is also a parent change operation
        element_id = data.get('element_id')
        new_parent_id = data.get('new_parent_id')
        new_parent_type = data.get('new_parent_type')

        print(f"Reorder request - Element: {element_id}, New parent: {new_parent_type} {new_parent_id}")

        # Handle parent change if specified - now always container to container
        if element_id and new_parent_id:
            element = Element.objects.get(id=element_id)

            # Always moving to a container
            parent_element = Element.objects.get(id=new_parent_id)
            element.parent_element = parent_element
            element.save()

        # Update orders for all elements in the container
        for item in element_orders:
            elem_id = item.get('id')
            order = item.get('order')

            # Debug logging for order 0
            if order == 0:
                logger.info(f"🎯 Updating element {elem_id} with order 0")

            if elem_id and order is not None:
                Element.objects.filter(id=elem_id).update(order=order)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@extend_schema(
    tags=['Page Builder'],
    summary=_('Get page data for visual builder'),
    description=_('''Returns complete page data including all elements for the visual builder.

    **Authentication:** Staff only

    **Response includes:**
    - Page metadata (title, slug, type, status)
    - All top-level elements with their content and order'''),
    responses={
        200: OpenApiResponse(description=_('Page data retrieved successfully')),
        401: OpenApiResponse(description=_('Authentication required')),
        403: OpenApiResponse(description=_('Staff access required')),
        404: OpenApiResponse(description=_('Page not found')),
    }
)
@staff_required_api
def get_page_data(request, page_id):
    """Get complete page data for the visual builder"""
    try:
        page = get_object_or_404(
            Page.objects.select_related('theme').prefetch_related('elements'),
            id=page_id
        )

        elements_data = []
        for element in page.elements.filter(parent_element__isnull=True).order_by('order'):
            elements_data.append({
                'id': element.id,
                'element_type': element.element_type,
                'order': element.order,
                'content': element.content,
                'name': element.name,
                'is_active': element.is_active
            })

        return JsonResponse({
            'success': True,
            'page': {
                'id': page.id,
                'title': page.title,
                'slug': page.slug,
                'page_type': page.page_type,
                'status': page.status,
                'elements': elements_data
            }
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def _get_dynamic_options_for_source(source_name):
    """
    Fetch dynamic options for a given source name.
    Returns a list of {value, label} options.
    """
    if source_name == 'menus':
        from design.header_footer_models import Menu
        menus = Menu.objects.filter(is_active=True).values('id', 'name')
        options = [{'value': '', 'label': _('-- Select a menu --')}]
        options.extend([{'value': str(m['id']), 'label': m['name']} for m in menus])
        return options
    # Add other dynamic sources as needed
    return []


def _inject_dynamic_options(config_data):
    """
    Recursively scan config for dynamic_options_source and inject options.
    """
    import copy
    config = copy.deepcopy(config_data)

    def process_properties(properties):
        if not properties or not isinstance(properties, dict):
            return
        for key, prop in properties.items():
            if isinstance(prop, dict):
                # Check for dynamic_options_source
                if 'dynamic_options_source' in prop:
                    source = prop['dynamic_options_source']
                    prop['options'] = _get_dynamic_options_for_source(source)
                    del prop['dynamic_options_source']
                # Recurse into nested properties (for property_groups)
                if 'properties' in prop:
                    process_properties(prop['properties'])

    # Process tabs
    if 'tabs' in config:
        for tab_key, tab in config['tabs'].items():
            if 'properties' in tab:
                process_properties(tab['properties'])

    # Process top-level properties
    if 'properties' in config:
        process_properties(config['properties'])

    return config


@extend_schema(
    tags=['Page Builder'],
    summary=_('Get element type configuration'),
    description=_('''Returns the configuration schema for a specific element type, used to
    render the properties panel in the visual builder.

    **Authentication:** Staff only

    **Response includes:**
    - Element tabs and properties configuration
    - Dynamic options (e.g., available menus for navigation elements)
    - Default values and validation rules'''),
    parameters=[
        OpenApiParameter(
            name='element_type',
            type=str,
            location=OpenApiParameter.PATH,
            description=_('Element type identifier (e.g., hero, text, container)')
        )
    ],
    responses={
        200: OpenApiResponse(description=_('Element configuration schema')),
        401: OpenApiResponse(description=_('Authentication required')),
        403: OpenApiResponse(description=_('Staff access required')),
        404: OpenApiResponse(description=_('Element type not found')),
    }
)
@staff_required_api
@require_http_methods(["GET"])
def get_element_config(request, element_type):
    """
    Get the configuration for a specific element type.
    Uses the element registry to get merged config with base property inheritance.
    Injects dynamic options for fields like menu selectors.
    """
    from .element_registry import get_registry

    registry = get_registry()
    element = registry.get_element(element_type)

    if not element:
        return JsonResponse({'error': 'Element type not found'}, status=404)

    try:
        # Get the merged config data and inject dynamic options
        config_data = _inject_dynamic_options(element.config_data)
        return JsonResponse(config_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# Page Settings API Endpoints
# ============================================================================

@staff_required_api
@require_http_methods(["GET"])
def get_page_settings_config(request, page_id):
    """
    Get page settings configuration with dynamic options for the visual builder.

    Returns the page_config.json schema along with:
    - Current page data
    - Dynamic options for header/footer template selects
    - Theme options
    - Layout preset options from theme
    """
    from design.header_footer_models import HeaderTemplate, FooterTemplate
    from design.theme_models import Theme
    from design.models import DesignToken

    try:
        page = get_object_or_404(
            Page.objects.select_related('theme', 'header_template', 'footer_template'),
            id=page_id
        )

        # Load page_config.json
        config_path = Path(__file__).parent / 'templates/page_builder/page_config.json'
        with open(config_path, encoding='utf-8') as f:
            config = json.load(f)

        # Build dynamic options for header templates
        headers = list(HeaderTemplate.objects.filter(is_active=True).values('id', 'name'))
        header_options = [{'value': '', 'label': _('Site Default')}]
        header_options.extend([{'value': str(h['id']), 'label': h['name']} for h in headers])

        # Build dynamic options for footer templates
        footers = list(FooterTemplate.objects.filter(is_active=True).values('id', 'name'))
        footer_options = [{'value': '', 'label': _('Site Default')}]
        footer_options.extend([{'value': str(f['id']), 'label': f['name']} for f in footers])

        # Build dynamic options for themes
        themes = list(Theme.objects.filter(is_active=True).values('id', 'name'))
        theme_options = [{'value': '', 'label': _('Site Default')}]
        theme_options.extend([{'value': str(t['id']), 'label': t['name']} for t in themes])

        # Build layout preset options (theme-based + standard)
        layout_preset_options = [
            {'value': 'theme-default', 'label': _('Theme Default')},
        ]

        # Check for theme-specific width tokens
        active_theme = page.effective_theme
        if active_theme:
            theme_tokens = DesignToken.objects.filter(
                theme=active_theme,
                token_type='spacing',
                name__icontains='container'
            ).values('name', 'value')

            for token in theme_tokens:
                if 'narrow' in token['name'].lower():
                    layout_preset_options.append({
                        'value': 'theme-narrow',
                        'label': _('Theme Narrow ({})').format(token['value'])
                    })
                elif 'wide' in token['name'].lower():
                    layout_preset_options.append({
                        'value': 'theme-wide',
                        'label': _('Theme Wide ({})').format(token['value'])
                    })

        # Add standard presets
        layout_preset_options.extend([
            {'value': 'narrow', 'label': _('Narrow (800px)')},
            {'value': 'standard', 'label': _('Standard (1200px)')},
            {'value': 'wide', 'label': _('Wide (1400px)')},
            {'value': 'full', 'label': _('Full Width')},
            {'value': 'custom', 'label': _('Custom')},
        ])

        # Attach dynamic options to config
        config['dynamic_options'] = {
            'header_templates': header_options,
            'footer_templates': footer_options,
            'themes': theme_options,
            'layout_presets': layout_preset_options,
        }

        # Build current page data
        page_data = {
            'id': page.id,
            'title': page.title,
            'slug': page.slug,
            'status': page.status,
            'page_type': page.page_type,
            'is_default_for_type': page.is_default_for_type,
            'is_system_page': page.is_system_page,
            # SEO
            'meta_title': page.meta_title,
            'meta_description': page.meta_description,
            'meta_keywords': page.meta_keywords,
            'og_image_id': page.og_image_id,
            'seo_auto_generated': page.seo_auto_generated,
            # Header/Footer
            'hide_header': page.hide_header,
            'hide_footer': page.hide_footer,
            'header_template_id': str(page.header_template_id) if page.header_template_id else '',
            'footer_template_id': str(page.footer_template_id) if page.footer_template_id else '',
            # Design
            'page_design_config': page.page_design_config or {},
            'layout_preset': (page.page_design_config or {}).get('layout_preset', 'theme-default'),
            'custom_width': (page.page_design_config or {}).get('custom_width', ''),
            'background': (page.page_design_config or {}).get('background', ''),
            'typography': (page.page_design_config or {}).get('typography', ''),
            'text_color': (page.page_design_config or {}).get('text_color', ''),
            # Advanced
            'requires_auth': page.requires_auth,
            'cache_timeout': page.cache_timeout,
            'theme_id': str(page.theme_id) if page.theme_id else '',
            # Translations
            'translations': page.translations or {},
        }

        return JsonResponse({
            'success': True,
            'config': config,
            'page_data': page_data
        })

    except Exception as e:
        logger.error(f"Error fetching page settings config: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@staff_required_api
@require_http_methods(["PATCH", "PUT"])
def update_page_settings(request, page_id):
    """
    Update page settings from the visual builder.

    Accepts partial updates - only fields provided will be updated.
    Handles both top-level page fields and nested page_design_config.
    """
    try:
        data = json.loads(request.body)
        page = get_object_or_404(Page, id=page_id)

        # Fields that map directly to Page model
        direct_fields = [
            'title', 'slug', 'status', 'page_type', 'is_default_for_type',
            'meta_title', 'meta_description', 'meta_keywords',
            'seo_auto_generated', 'requires_auth', 'cache_timeout',
            'hide_header', 'hide_footer',
        ]

        for field in direct_fields:
            if field in data:
                value = data[field]
                # Handle empty string to None for optional fields
                if value == '' and field in ['slug']:
                    value = None
                setattr(page, field, value)

        # Handle ForeignKey fields (convert '' to None)
        fk_fields = ['header_template_id', 'footer_template_id', 'theme_id', 'og_image_id']
        for field in fk_fields:
            if field in data:
                value = data[field]
                setattr(page, field, int(value) if value else None)

        # Handle page_design_config (nested JSON)
        design_config_fields = ['layout_preset', 'custom_width', 'background', 'typography', 'text_color']
        if any(f in data for f in design_config_fields):
            if not page.page_design_config:
                page.page_design_config = {}

            for field in design_config_fields:
                if field in data:
                    page.page_design_config[field] = data[field]

        # Handle full page_design_config if provided as object
        if 'page_design_config' in data and isinstance(data['page_design_config'], dict):
            if not page.page_design_config:
                page.page_design_config = {}
            page.page_design_config.update(data['page_design_config'])

        # Handle translations if provided
        if 'translations' in data and isinstance(data['translations'], dict):
            if not page.translations:
                page.translations = {}
            page.translations.update(data['translations'])

        page.save()

        # Update draft version
        draft = page.get_draft_version()
        if draft:
            draft.create_snapshot()
        else:
            page.create_draft_version(
                user=request.user if request.user.is_authenticated else None,
                description="Page settings updated"
            )

        return JsonResponse({
            'success': True,
            'page_id': page.id,
            'message': _('Page settings saved successfully')
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': _('Invalid JSON data')}, status=400)
    except Exception as e:
        logger.error(f"Error updating page settings: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# Versioning API endpoints
@extend_schema(
    tags=['Page Builder'],
    summary=_('Save page draft'),
    description=_('''Creates a new draft version of the page with the current element state.

    **Authentication:** Staff only

    **Request body (optional):**
    - description: Change description for this draft'''),
    responses={
        200: OpenApiResponse(description=_('Draft saved with version ID and number')),
        401: OpenApiResponse(description=_('Authentication required')),
        403: OpenApiResponse(description=_('Staff access required')),
        404: OpenApiResponse(description=_('Page not found')),
    }
)
@staff_required_api
@require_http_methods(["POST"])
def save_page_draft(request, page_id):
    """Save current page state as a draft version"""
    try:
        page = get_object_or_404(Page, id=page_id)

        # Get optional description from request
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        description = data.get('description', 'Draft saved')

        # Create a new draft version
        version = page.create_draft_version(
            user=request.user,
            description=description
        )

        return JsonResponse({
            'success': True,
            'version_id': version.id,
            'version_number': version.version_number,
            'message': 'Draft saved successfully'
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@extend_schema(
    tags=['Page Builder'],
    summary=_('Publish page'),
    description=_('''Publishes the current draft version of a page, making it live.

    **Authentication:** Staff only

    **Request body (optional):**
    - notes: Publish notes for the history log'''),
    responses={
        200: OpenApiResponse(description=_('Page published with version details')),
        401: OpenApiResponse(description=_('Authentication required')),
        403: OpenApiResponse(description=_('Staff access required')),
        404: OpenApiResponse(description=_('Page not found')),
    }
)
@staff_required_api
@require_http_methods(["POST"])
def publish_page(request, page_id):
    """Publish the current draft of a page"""
    try:
        page = get_object_or_404(Page, id=page_id)

        # Get optional notes from request
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        notes = data.get('notes', '')

        # Publish the draft
        published_version = page.publish_current_draft(
            user=request.user,
            notes=notes
        )

        return JsonResponse({
            'success': True,
            'version_id': published_version.id,
            'version_number': published_version.version_number,
            'published_at': published_version.created_at.isoformat(),
            'message': 'Page published successfully'
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@extend_schema(
    tags=['Page Builder'],
    summary=_('Get page versions'),
    description=_('''Returns all versions of a page for the version history panel.

    **Authentication:** Staff only'''),
    responses={
        200: OpenApiResponse(description=_('List of page versions with metadata')),
        401: OpenApiResponse(description=_('Authentication required')),
        403: OpenApiResponse(description=_('Staff access required')),
        404: OpenApiResponse(description=_('Page not found')),
    }
)
@staff_required_api
@require_http_methods(["GET"])
def get_page_versions(request, page_id):
    """Get all versions of a page"""
    try:
        page = get_object_or_404(Page, id=page_id)

        versions = []
        for version in page.versions.all():
            versions.append({
                'id': version.id,
                'version_number': version.version_number,
                'is_published': version.is_published,
                'is_current_draft': version.is_current_draft,
                'created_at': version.created_at.isoformat(),
                'created_by': version.created_by.username if version.created_by else None,
                'description': version.change_description
            })

        return JsonResponse({
            'page_id': page.id,
            'page_title': page.title,
            'current_status': page.status,
            'versions': versions
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_required_api
@require_http_methods(["POST"])
def revert_to_version(request, page_id, version_id):
    """Revert a page to a specific version"""
    try:
        page = get_object_or_404(Page, id=page_id)

        # Revert to the specified version
        new_draft = page.revert_to_version(
            version_id=version_id,
            user=request.user
        )

        return JsonResponse({
            'success': True,
            'new_draft_id': new_draft.id,
            'new_draft_number': new_draft.version_number,
            'message': f'Page reverted to version {version_id}'
        })

    except PageVersion.DoesNotExist:
        return JsonResponse({'error': 'Version not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_required_api
@require_http_methods(["GET"])
def preview_version(request, page_id, version_id):
    """Preview a specific version of a page without restoring it"""
    try:
        page = get_object_or_404(Page, id=page_id)
        version = get_object_or_404(PageVersion, id=version_id, page=page)

        # Return the version's content snapshot
        return JsonResponse({
            'version_id': version.id,
            'version_number': version.version_number,
            'content': version.content_snapshot,
            'created_at': version.created_at.isoformat(),
            'is_published': version.is_published,
            'is_current_draft': version.is_current_draft
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_required_api
@require_http_methods(["GET"])
def get_publish_history(request, page_id):
    """Get the publish history for a page"""
    try:
        page = get_object_or_404(Page, id=page_id)

        history = []
        for record in page.publish_history.all()[:20]:  # Last 20 publishes
            history.append({
                'id': record.id,
                'published_at': record.published_at.isoformat(),
                'published_by': record.published_by.username if record.published_by else None,
                'version_number': record.published_version.version_number if record.published_version else None,
                'notes': record.publish_notes,
                'rolled_back': record.rolled_back_at is not None
            })

        return JsonResponse({
            'page_id': page.id,
            'page_title': page.title,
            'history': history
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# Public Pages API (Headless Frontend)
# ============================================================================

@extend_schema(
    tags=['Page Builder'],
    summary=_("Get published page by slug"),
    description=_("Get published page content by slug. Public endpoint for headless frontends. Only returns published pages. Includes SEO metadata and page elements."),
    parameters=[
        OpenApiParameter(
            name='slug',
            type=str,
            location=OpenApiParameter.PATH,
            description=_('The page slug (URL-friendly identifier)')
        ),
    ],
    responses={
        200: OpenApiResponse(description=_("Page content retrieved successfully")),
        401: OpenApiResponse(description=_("Authentication required for this page")),
        404: OpenApiResponse(description=_("Page not found")),
    }
)
@require_http_methods(["GET"])
def get_public_page(request, slug):
    """
    Get published page content by slug.

    Public endpoint for headless frontends to fetch page content.
    Only returns published pages. Includes SEO metadata.

    GET /api/page-builder/public/{slug}/
    """
    try:
        page = Page.objects.filter(
            slug=slug,
            status='published'
        ).select_related('theme').prefetch_related('elements').first()

        if not page:
            return JsonResponse({
                'success': False,
                'error': _('Page not found')
            }, status=404)

        # Check if page requires authentication
        if page.requires_auth and not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': _('Authentication required')
            }, status=401)

        # Build elements tree
        elements_data = []
        for element in page.elements.filter(parent_element__isnull=True).order_by('order'):
            elements_data.append(_build_element_tree(element))

        return JsonResponse({
            'success': True,
            'data': {
                'id': page.id,
                'title': page.title,
                'slug': page.slug,
                'page_type': page.page_type,
                'seo': {
                    'meta_title': page.meta_title or page.title,
                    'meta_description': page.meta_description,
                    'meta_keywords': page.meta_keywords,
                    'og_image': request.build_absolute_uri(page.og_image.url) if page.og_image else None,
                },
                'elements': elements_data,
                'theme': {
                    'id': page.theme.id if page.theme else None,
                    'name': page.theme.name if page.theme else None,
                } if page.theme else None,
                'published_at': page.published_at.isoformat() if page.published_at else None,
            }
        })

    except Exception as e:
        logger.error(f"Error fetching public page: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def _build_element_tree(element):
    """Recursively build element tree for public page response"""
    children = []
    for child in element.children.all().order_by('order'):
        children.append(_build_element_tree(child))

    return {
        'id': element.id,
        'element_type': element.element_type,
        'name': element.name,
        'content': element.content,
        'order': element.order,
        'css_classes': element.css_classes,
        'style_overrides': element.style_overrides,
        'responsive_config': element.responsive_config,
        'visibility_config': element.visibility_config,
        'children': children if children else None,
    }


@extend_schema(
    tags=['Page Builder'],
    summary=_("Get legal/policy pages"),
    description=_("Get all legal and policy pages for footer navigation. Returns published pages like Terms of Service, Privacy Policy, About Us, Contact, FAQ, Refund Policy, and Shipping Policy. Useful for building site footers in headless frontends."),
    responses={
        200: OpenApiResponse(description=_("List of legal/policy pages")),
    }
)
@require_http_methods(["GET"])
def get_legal_pages(request):
    """
    Get all legal/policy pages.

    Returns pages commonly needed for footers: Terms, Privacy, About, etc.
    Only returns published pages of relevant types.

    GET /api/page-builder/public/legal/
    """
    try:
        # Get common legal/info page types
        legal_page_types = ['about', 'contact', 'custom']

        pages = Page.objects.filter(
            status='published',
            page_type__in=legal_page_types
        ).values('id', 'title', 'slug', 'page_type', 'meta_description')

        # Also get any pages with common legal slugs
        legal_slugs = [
            'terms', 'terms-of-service', 'terms-and-conditions',
            'privacy', 'privacy-policy',
            'refund', 'refund-policy', 'returns',
            'shipping', 'shipping-policy',
            'faq', 'faqs',
            'about', 'about-us',
            'contact', 'contact-us',
        ]

        slug_pages = Page.objects.filter(
            status='published',
            slug__in=legal_slugs
        ).values('id', 'title', 'slug', 'page_type', 'meta_description')

        # Combine and deduplicate
        all_pages = list(pages) + list(slug_pages)
        seen_ids = set()
        unique_pages = []
        for page in all_pages:
            if page['id'] not in seen_ids:
                seen_ids.add(page['id'])
                unique_pages.append(page)

        return JsonResponse({
            'success': True,
            'data': {
                'pages': unique_pages,
                'count': len(unique_pages)
            }
        })

    except Exception as e:
        logger.error(f"Error fetching legal pages: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@extend_schema(
    tags=['Page Builder'],
    summary=_("Get default page by type"),
    description=_("Get the default page for a specific page type. Useful for headless frontends to get the configured home page, category page template, cart page, checkout page, etc. Returns the page marked as default for the type, or the first published page of that type."),
    parameters=[
        OpenApiParameter(
            name='page_type',
            type=str,
            location=OpenApiParameter.PATH,
            description=_('Page type: home, category, product, cart, checkout, about, contact, or custom')
        ),
    ],
    responses={
        200: OpenApiResponse(description=_("Page content retrieved successfully")),
        400: OpenApiResponse(description=_("Invalid page type")),
        404: OpenApiResponse(description=_("No page found for this type")),
    }
)
@require_http_methods(["GET"])
def get_page_by_type(request, page_type):
    """
    Get the default page for a specific page type.

    Useful for headless frontends to get the configured home page,
    category page template, etc.

    GET /api/page-builder/public/type/{page_type}/
    """
    try:
        # Validate page type
        valid_types = [pt[0] for pt in Page.PAGE_TYPES]
        if page_type not in valid_types:
            return JsonResponse({
                'success': False,
                'error': _('Invalid page type')
            }, status=400)

        # Get default page for this type, or first published page
        page = Page.objects.filter(
            page_type=page_type,
            status='published',
            is_default_for_type=True
        ).select_related('theme').first()

        if not page:
            # Fall back to first published page of this type
            page = Page.objects.filter(
                page_type=page_type,
                status='published'
            ).select_related('theme').first()

        if not page:
            return JsonResponse({
                'success': False,
                'error': _('No page found for this type')
            }, status=404)

        # Build elements tree
        elements_data = []
        for element in page.elements.filter(parent_element__isnull=True).order_by('order'):
            elements_data.append(_build_element_tree(element))

        return JsonResponse({
            'success': True,
            'data': {
                'id': page.id,
                'title': page.title,
                'slug': page.slug,
                'page_type': page.page_type,
                'is_default': page.is_default_for_type,
                'seo': {
                    'meta_title': page.meta_title or page.title,
                    'meta_description': page.meta_description,
                    'meta_keywords': page.meta_keywords,
                    'og_image': request.build_absolute_uri(page.og_image.url) if page.og_image else None,
                },
                'elements': elements_data,
                'theme': {
                    'id': page.theme.id if page.theme else None,
                    'name': page.theme.name if page.theme else None,
                } if page.theme else None,
            }
        })

    except Exception as e:
        logger.error(f"Error fetching page by type: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@extend_schema(
    tags=['Page Builder'],
    summary=_("List visibility rule groups"),
    description=_("""Get all active visibility rule groups for the visibility rules editor.

    This endpoint returns saved rule groups that can be applied to page elements
    for advanced visibility conditions (e.g., show to US mobile users only,
    hide during business hours, show to VIP customers).

    **Authentication:** Staff only (requires login with staff privileges).

    **Use cases:**
    - Populate saved rule groups dropdown in visibility rules editor
    - Allow staff to reuse pre-configured visibility conditions"""),
    responses={
        200: OpenApiResponse(
            description=_("List of active visibility rule groups"),
        ),
        401: OpenApiResponse(description=_("Authentication required")),
        403: OpenApiResponse(description=_("Staff access required")),
        500: OpenApiResponse(description=_("Server error")),
    }
)
@staff_required_api
@require_http_methods(["GET"])
def get_visibility_rule_groups(request):
    """
    Get all available visibility rule groups for the visibility rules editor.

    Returns:
        {
            "success": True,
            "rule_groups": [
                {
                    "id": 1,
                    "name": "US Mobile Users",
                    "description": "Show to US visitors on mobile",
                    "logic_operator": "AND",
                    "rules_count": 2,
                    "rules_summary": "geo_country = US, device_type = mobile"
                },
                ...
            ]
        }
    """
    try:
        rule_groups = RuleGroup.objects.filter(is_active=True).prefetch_related('rules').order_by('name')

        data = []
        for group in rule_groups:
            # Get rule summaries
            rules = group.rules.all()
            rules_summary = ', '.join([
                f"{r.rule_type} {r.operator} {r.value[:20]}..." if len(str(r.value)) > 20 else f"{r.rule_type} {r.operator} {r.value}"
                for r in rules[:3]
            ])
            if rules.count() > 3:
                rules_summary += f" (+{rules.count() - 3} more)"

            data.append({
                'id': group.id,
                'name': group.name,
                'description': group.description,
                'logic_operator': group.logic_operator,
                'rules_count': rules.count(),
                'rules_summary': rules_summary,
            })

        return JsonResponse({
            'success': True,
            'rule_groups': data
        })

    except Exception as e:
        logger.error(f"Error fetching visibility rule groups: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================================================
# Visibility Rule Builder API Endpoints
# ============================================================================

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(staff_required_api, name='dispatch')
class RuleGroupAPIView(PageBuilderAPIView):
    """API endpoints for managing rule groups"""

    def get(self, request, group_id=None):
        """Get rule group(s) - list all or get single with full structure"""
        try:
            if group_id:
                # Get single group with full structure
                group = get_object_or_404(
                    RuleGroup.objects.prefetch_related('rules', 'child_groups'),
                    id=group_id
                )
                return JsonResponse({
                    'success': True,
                    'group': self._build_group_data(group, include_rules=True)
                })
            else:
                # List all groups
                groups = RuleGroup.objects.filter(
                    parent_group__isnull=True
                ).prefetch_related('rules', 'child_groups').order_by('name')

                return JsonResponse({
                    'success': True,
                    'groups': [self._build_group_data(g) for g in groups]
                })

        except Exception as e:
            logger.error(f"Error fetching rule groups: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    def post(self, request):
        """Create a new rule group"""
        data = self.get_json_data(request)
        if not data:
            return JsonResponse({'error': _('Invalid JSON data')}, status=400)

        try:
            name = data.get('name', '').strip()
            if not name:
                return JsonResponse({'error': _('Name is required')}, status=400)

            group = RuleGroup.objects.create(
                name=name,
                description=data.get('description', ''),
                logic_operator=data.get('logic_operator', 'AND'),
                is_active=data.get('is_active', True),
                priority=data.get('priority', 5)
            )

            # Handle parent group
            parent_id = data.get('parent_group_id')
            if parent_id:
                try:
                    parent = RuleGroup.objects.get(id=parent_id)
                    group.parent_group = parent
                    group.save()
                except RuleGroup.DoesNotExist:
                    pass

            return JsonResponse({
                'success': True,
                'group': self._build_group_data(group)
            })

        except Exception as e:
            logger.error(f"Error creating rule group: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, group_id):
        """Update an existing rule group"""
        return self.patch(request, group_id)

    def patch(self, request, group_id):
        """Update an existing rule group"""
        data = self.get_json_data(request)
        if not data:
            return JsonResponse({'error': _('Invalid JSON data')}, status=400)

        try:
            group = get_object_or_404(RuleGroup, id=group_id)

            if 'name' in data:
                group.name = data['name']
            if 'description' in data:
                group.description = data['description']
            if 'logic_operator' in data:
                group.logic_operator = data['logic_operator']
            if 'is_active' in data:
                group.is_active = data['is_active']
            if 'priority' in data:
                group.priority = data['priority']
            if 'parent_group_id' in data:
                parent_id = data['parent_group_id']
                if parent_id:
                    group.parent_group = RuleGroup.objects.get(id=parent_id)
                else:
                    group.parent_group = None

            group.save()

            return JsonResponse({
                'success': True,
                'group': self._build_group_data(group)
            })

        except Exception as e:
            logger.error(f"Error updating rule group: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, group_id):
        """Delete a rule group"""
        try:
            group = get_object_or_404(RuleGroup, id=group_id)
            group_name = group.name
            group.delete()

            return JsonResponse({
                'success': True,
                'message': f'Rule group "{group_name}" deleted successfully'
            })

        except Exception as e:
            logger.error(f"Error deleting rule group: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    def _build_group_data(self, group, include_rules=False):
        """Build group data dictionary"""
        data = {
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'logic_operator': group.logic_operator,
            'is_active': group.is_active,
            'priority': group.priority,
            'parent_group_id': group.parent_group_id,
            'rules_count': group.rules.count(),
        }

        if include_rules:
            # Get rules with order from through table
            members = RuleGroupMember.objects.filter(
                group=group
            ).select_related('rule').order_by('order')

            data['rules'] = [{
                'id': m.rule.id,
                'name': m.rule.name,
                'description': m.rule.description,
                'rule_type': m.rule.rule_type,
                'operator': m.rule.operator,
                'value': m.rule.value,
                'is_active': m.rule.is_active,
                'priority': m.rule.priority,
                'order': m.order,
            } for m in members]

            # Get nested child groups
            data['child_groups'] = [
                self._build_group_data(child, include_rules=True)
                for child in group.child_groups.all().order_by('priority', 'name')
            ]

        return data


@csrf_exempt
@staff_required_api
@require_http_methods(["PUT", "POST"])
def save_rule_group_structure(request, group_id):
    """
    Save the full structure of a rule group including rules and nested groups.

    This endpoint handles bulk updates from the rule builder, including:
    - Reordering rules within the group
    - Adding/removing rules
    - Updating nested groups
    """
    try:
        data = json.loads(request.body)
        group = get_object_or_404(RuleGroup, id=group_id)

        # Update group properties
        if 'name' in data:
            group.name = data['name']
        if 'description' in data:
            group.description = data['description']
        if 'logic_operator' in data:
            group.logic_operator = data['logic_operator']
        if 'is_active' in data:
            group.is_active = data['is_active']
        if 'priority' in data:
            group.priority = data['priority']

        group.save()

        # Update rules membership and order
        if 'rules' in data:
            rules_data = data['rules']

            # Get current rule IDs in this group
            current_rule_ids = set(group.rules.values_list('id', flat=True))
            new_rule_ids = set()

            for idx, rule_data in enumerate(rules_data):
                rule_id = rule_data.get('id')
                if rule_id:
                    new_rule_ids.add(rule_id)

                    # Update or create membership
                    member, created = RuleGroupMember.objects.update_or_create(
                        group=group,
                        rule_id=rule_id,
                        defaults={'order': idx}
                    )

            # Remove rules that are no longer in the group
            removed_ids = current_rule_ids - new_rule_ids
            if removed_ids:
                RuleGroupMember.objects.filter(
                    group=group,
                    rule_id__in=removed_ids
                ).delete()

        # Handle nested groups
        if 'child_groups' in data:
            _save_nested_groups(group, data['child_groups'])

        return JsonResponse({
            'success': True,
            'message': f'Rule group "{group.name}" saved successfully'
        })

    except Exception as e:
        logger.error(f"Error saving rule group structure: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def _save_nested_groups(parent_group, child_groups_data):
    """Recursively save nested child groups"""
    existing_child_ids = set(parent_group.child_groups.values_list('id', flat=True))
    processed_ids = set()

    for child_data in child_groups_data:
        child_id = child_data.get('id')

        if child_id:
            # Update existing child group
            try:
                child = RuleGroup.objects.get(id=child_id)
                child.name = child_data.get('name', child.name)
                child.description = child_data.get('description', child.description)
                child.logic_operator = child_data.get('logic_operator', child.logic_operator)
                child.is_active = child_data.get('is_active', child.is_active)
                child.priority = child_data.get('priority', child.priority)
                child.parent_group = parent_group
                child.save()
                processed_ids.add(child_id)

                # Handle rules for this child
                if 'rules' in child_data:
                    _update_group_rules(child, child_data['rules'])

                # Recursively handle nested groups
                if 'child_groups' in child_data:
                    _save_nested_groups(child, child_data['child_groups'])

            except RuleGroup.DoesNotExist:
                pass
        else:
            # Create new child group
            child = RuleGroup.objects.create(
                name=child_data.get('name', _('New Group')),
                description=child_data.get('description', ''),
                logic_operator=child_data.get('logic_operator', 'AND'),
                is_active=child_data.get('is_active', True),
                priority=child_data.get('priority', 5),
                parent_group=parent_group
            )

            # Handle rules for new child
            if 'rules' in child_data:
                _update_group_rules(child, child_data['rules'])

            # Recursively handle nested groups
            if 'child_groups' in child_data:
                _save_nested_groups(child, child_data['child_groups'])

    # Remove child groups that are no longer present
    removed_ids = existing_child_ids - processed_ids
    if removed_ids:
        RuleGroup.objects.filter(id__in=removed_ids).delete()


def _update_group_rules(group, rules_data):
    """Update rules membership for a group"""
    # Clear existing memberships
    RuleGroupMember.objects.filter(group=group).delete()

    for idx, rule_data in enumerate(rules_data):
        rule_id = rule_data.get('id')
        if rule_id:
            RuleGroupMember.objects.create(
                group=group,
                rule_id=rule_id,
                order=idx
            )


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(staff_required_api, name='dispatch')
class VisibilityRuleAPIView(PageBuilderAPIView):
    """API endpoints for managing individual visibility rules"""

    def get(self, request, rule_id=None):
        """Get rule(s) - list all or get single"""
        try:
            if rule_id:
                # Get single rule
                rule = get_object_or_404(VisibilityRule, id=rule_id)
                return JsonResponse({
                    'success': True,
                    'rule': self._build_rule_data(rule)
                })
            else:
                # List all rules, optionally filtered
                rules = VisibilityRule.objects.all().order_by('name')

                # Filter by active status if specified
                active = request.GET.get('active')
                if active == 'true':
                    rules = rules.filter(is_active=True)
                elif active == 'false':
                    rules = rules.filter(is_active=False)

                # Filter by rule type category
                category = request.GET.get('category')
                if category:
                    category_mappings = {
                        'geo': ['geo_country', 'geo_region', 'geo_city', 'geo_timezone'],
                        'user': ['user_logged_in', 'user_group', 'user_segment', 'user_lifetime_value', 'user_order_count'],
                        'device': ['device_type', 'browser', 'operating_system', 'screen_size', 'connection_speed'],
                        'time': ['date_range', 'time_range', 'day_of_week', 'business_hours'],
                        'behavioral': ['first_visit', 'visit_count', 'page_views', 'time_on_site', 'referrer', 'utm_campaign'],
                        'ecommerce': ['cart_value', 'cart_items', 'has_purchased', 'abandoned_cart', 'wishlist_items'],
                        'language': ['browser_language', 'selected_language', 'selected_currency'],
                    }
                    if category in category_mappings:
                        rules = rules.filter(rule_type__in=category_mappings[category])

                return JsonResponse({
                    'success': True,
                    'rules': [self._build_rule_data(r) for r in rules]
                })

        except Exception as e:
            logger.error(f"Error fetching visibility rules: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    def post(self, request):
        """Create a new visibility rule"""
        data = self.get_json_data(request)
        if not data:
            return JsonResponse({'error': _('Invalid JSON data')}, status=400)

        try:
            rule_type = data.get('rule_type', '').strip()
            if not rule_type:
                return JsonResponse({'error': _('Rule type is required')}, status=400)

            # Validate rule type
            valid_types = [rt[0] for rt in VisibilityRule.RULE_TYPES]
            if rule_type not in valid_types:
                return JsonResponse({'error': _('Invalid rule type')}, status=400)

            rule = VisibilityRule.objects.create(
                name=data.get('name', f'{rule_type} Rule'),
                description=data.get('description', ''),
                rule_type=rule_type,
                operator=data.get('operator', 'equals'),
                value=data.get('value', ''),
                is_active=data.get('is_active', True),
                priority=data.get('priority', 5),
            )

            # Optionally add to a group
            group_id = data.get('group_id')
            if group_id:
                try:
                    group = RuleGroup.objects.get(id=group_id)
                    # Get max order
                    max_order = RuleGroupMember.objects.filter(group=group).aggregate(
                        max_order=Max('order')
                    )['max_order'] or -1
                    RuleGroupMember.objects.create(
                        group=group,
                        rule=rule,
                        order=max_order + 1
                    )
                except RuleGroup.DoesNotExist:
                    pass

            return JsonResponse({
                'success': True,
                'rule': self._build_rule_data(rule)
            })

        except Exception as e:
            logger.error(f"Error creating visibility rule: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, rule_id):
        """Update an existing visibility rule"""
        return self.patch(request, rule_id)

    def patch(self, request, rule_id):
        """Update an existing visibility rule"""
        data = self.get_json_data(request)
        if not data:
            return JsonResponse({'error': _('Invalid JSON data')}, status=400)

        try:
            rule = get_object_or_404(VisibilityRule, id=rule_id)

            if 'name' in data:
                rule.name = data['name']
            if 'description' in data:
                rule.description = data['description']
            if 'rule_type' in data:
                # Validate rule type
                valid_types = [rt[0] for rt in VisibilityRule.RULE_TYPES]
                if data['rule_type'] in valid_types:
                    rule.rule_type = data['rule_type']
            if 'operator' in data:
                rule.operator = data['operator']
            if 'value' in data:
                rule.value = data['value']
            if 'is_active' in data:
                rule.is_active = data['is_active']
            if 'priority' in data:
                rule.priority = data['priority']

            rule.save()

            return JsonResponse({
                'success': True,
                'rule': self._build_rule_data(rule)
            })

        except Exception as e:
            logger.error(f"Error updating visibility rule: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, rule_id):
        """Delete a visibility rule"""
        try:
            rule = get_object_or_404(VisibilityRule, id=rule_id)
            rule_name = rule.name
            rule.delete()

            return JsonResponse({
                'success': True,
                'message': f'Rule "{rule_name}" deleted successfully'
            })

        except Exception as e:
            logger.error(f"Error deleting visibility rule: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    def _build_rule_data(self, rule):
        """Build rule data dictionary"""
        return {
            'id': rule.id,
            'name': rule.name,
            'description': rule.description,
            'rule_type': rule.rule_type,
            'operator': rule.operator,
            'value': rule.value,
            'is_active': rule.is_active,
            'priority': rule.priority,
        }


@extend_schema(
    tags=['Page Builder'],
    summary=_('Get visibility rule types configuration'),
    description=_('''Returns configuration for all visibility rule types including operators
    and value input configurations. Used by the rule builder to dynamically
    render the rule editor.

    **Authentication:** Staff only

    **Response includes:**
    - Rule types organized by category (geo, user, device, time, etc.)
    - Operators with compatibility information
    - Value type configurations'''),
    responses={
        200: OpenApiResponse(description=_('Rule types and operators configuration')),
        401: OpenApiResponse(description=_('Authentication required')),
        403: OpenApiResponse(description=_('Staff access required')),
    }
)
@staff_required_api
@require_http_methods(["GET"])
def get_rule_types_config(request):
    """
    Get configuration for all rule types including operators and value configurations.
    Used by the rule builder to configure the properties panel dynamically.
    """
    try:
        # Rule types organized by category
        rule_types_by_category = {
            'geo': {
                'label': _('Geographic'),
                'icon': 'fas fa-globe',
                'types': [
                    {'id': 'geo_country', 'label': _('Country'), 'value_type': 'country_select'},
                    {'id': 'geo_region', 'label': _('Region/State'), 'value_type': 'text'},
                    {'id': 'geo_city', 'label': _('City'), 'value_type': 'text'},
                    {'id': 'geo_timezone', 'label': _('Timezone'), 'value_type': 'timezone_select'},
                ]
            },
            'user': {
                'label': _('User'),
                'icon': 'fas fa-user',
                'types': [
                    {'id': 'user_logged_in', 'label': _('User Logged In'), 'value_type': 'boolean'},
                    {'id': 'user_group', 'label': _('User Group'), 'value_type': 'user_group_select'},
                    {'id': 'user_segment', 'label': _('Customer Segment'), 'value_type': 'segment_select'},
                    {'id': 'user_lifetime_value', 'label': _('Lifetime Value'), 'value_type': 'number'},
                    {'id': 'user_order_count', 'label': _('Order Count'), 'value_type': 'number'},
                ]
            },
            'device': {
                'label': _('Device'),
                'icon': 'fas fa-mobile-alt',
                'types': [
                    {'id': 'device_type', 'label': _('Device Type'), 'value_type': 'device_select'},
                    {'id': 'browser', 'label': _('Browser'), 'value_type': 'browser_select'},
                    {'id': 'operating_system', 'label': _('Operating System'), 'value_type': 'os_select'},
                    {'id': 'screen_size', 'label': _('Screen Size'), 'value_type': 'screen_size_select'},
                    {'id': 'connection_speed', 'label': _('Connection Speed'), 'value_type': 'connection_select'},
                ]
            },
            'time': {
                'label': _('Time'),
                'icon': 'fas fa-clock',
                'types': [
                    {'id': 'date_range', 'label': _('Date Range'), 'value_type': 'date_range'},
                    {'id': 'time_range', 'label': _('Time Range'), 'value_type': 'time_range'},
                    {'id': 'day_of_week', 'label': _('Day of Week'), 'value_type': 'day_select'},
                    {'id': 'business_hours', 'label': _('Business Hours'), 'value_type': 'boolean'},
                ]
            },
            'behavioral': {
                'label': _('Behavioral'),
                'icon': 'fas fa-chart-line',
                'types': [
                    {'id': 'first_visit', 'label': _('First Visit'), 'value_type': 'boolean'},
                    {'id': 'visit_count', 'label': _('Visit Count'), 'value_type': 'number'},
                    {'id': 'page_views', 'label': _('Page Views'), 'value_type': 'number'},
                    {'id': 'time_on_site', 'label': _('Time on Site'), 'value_type': 'duration'},
                    {'id': 'referrer', 'label': _('Referrer'), 'value_type': 'text'},
                    {'id': 'utm_campaign', 'label': _('UTM Campaign'), 'value_type': 'text'},
                ]
            },
            'ecommerce': {
                'label': _('E-commerce'),
                'icon': 'fas fa-shopping-cart',
                'types': [
                    {'id': 'cart_value', 'label': _('Cart Value'), 'value_type': 'currency'},
                    {'id': 'cart_items', 'label': _('Cart Items Count'), 'value_type': 'number'},
                    {'id': 'has_purchased', 'label': _('Has Purchased'), 'value_type': 'boolean'},
                    {'id': 'abandoned_cart', 'label': _('Abandoned Cart'), 'value_type': 'boolean'},
                    {'id': 'wishlist_items', 'label': _('Wishlist Items'), 'value_type': 'number'},
                ]
            },
            'language': {
                'label': _('Language'),
                'icon': 'fas fa-language',
                'types': [
                    {'id': 'browser_language', 'label': _('Browser Language'), 'value_type': 'language_select'},
                    {'id': 'selected_language', 'label': _('Selected Language'), 'value_type': 'language_select'},
                    {'id': 'selected_currency', 'label': _('Selected Currency'), 'value_type': 'currency_select'},
                ]
            },
        }

        # Operators with their compatible value types
        operators = {
            'equals': {'label': _('Equals'), 'symbol': '=', 'compatible': ['all']},
            'not_equals': {'label': _('Not Equals'), 'symbol': '≠', 'compatible': ['all']},
            'contains': {'label': _('Contains'), 'symbol': '⊃', 'compatible': ['text', 'list']},
            'not_contains': {'label': _('Not Contains'), 'symbol': '⊅', 'compatible': ['text', 'list']},
            'greater_than': {'label': _('Greater Than'), 'symbol': '>', 'compatible': ['number', 'currency', 'duration']},
            'less_than': {'label': _('Less Than'), 'symbol': '<', 'compatible': ['number', 'currency', 'duration']},
            'greater_or_equal': {'label': _('Greater or Equal'), 'symbol': '≥', 'compatible': ['number', 'currency', 'duration']},
            'less_or_equal': {'label': _('Less or Equal'), 'symbol': '≤', 'compatible': ['number', 'currency', 'duration']},
            'in_list': {'label': _('In List'), 'symbol': '∈', 'compatible': ['select', 'multi_select']},
            'not_in_list': {'label': _('Not in List'), 'symbol': '∉', 'compatible': ['select', 'multi_select']},
            'between': {'label': _('Between'), 'symbol': '↔', 'compatible': ['number', 'date_range', 'time_range']},
            'is_true': {'label': _('Is True'), 'symbol': '✓', 'compatible': ['boolean']},
            'is_false': {'label': _('Is False'), 'symbol': '✗', 'compatible': ['boolean']},
        }

        return JsonResponse({
            'success': True,
            'rule_types': rule_types_by_category,
            'operators': operators,
        })

    except Exception as e:
        logger.error(f"Error fetching rule types config: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@extend_schema(
    tags=['Page Builder'],
    summary=_('Get internal link sources'),
    description=_('''Returns searchable internal content for link selector widgets.

    **Authentication:** Staff only

    **Query parameters:**
    - type: Filter by content type (all, product, page, category, blog)
    - search: Search term to filter results
    - limit: Max results per type (default: 10, max: 50)

    **Response includes:**
    - Products, Pages, Categories, Blog Posts with URLs and thumbnails
    - URLs without language prefix for dynamic i18n'''),
    parameters=[
        OpenApiParameter(name='type', type=str, description=_('Content type filter')),
        OpenApiParameter(name='search', type=str, description=_('Search term')),
        OpenApiParameter(name='limit', type=int, description=_('Max results per type')),
    ],
    responses={
        200: OpenApiResponse(description=_('Link sources by content type')),
        401: OpenApiResponse(description=_('Authentication required')),
        403: OpenApiResponse(description=_('Staff access required')),
    }
)
@csrf_exempt
@staff_required_api
@require_http_methods(["GET"])
def get_link_sources(request):
    """
    Get available link sources for the link selector widget.

    Query parameters:
    - type: 'all' | 'product' | 'page' | 'category' | 'blog' (default: 'all')
    - search: Search term to filter results
    - limit: Max results per type (default: 10, max: 50)

    Returns searchable internal content (Products, Pages, Categories, Blog Posts)
    for use in link selector widgets in the page builder.

    URLs are returned WITHOUT language prefix so they work dynamically with
    the visitor's preferred language when rendered on the frontend.
    """
    from django.db.models import Q

    source_type = request.GET.get('type', 'all')
    search = request.GET.get('search', '').strip()
    limit = min(int(request.GET.get('limit', 10)), 50)

    result = {}

    # Products
    if source_type in ('all', 'product'):
        try:
            from catalog.models import Product
            # Product uses status='published', not is_active
            products_qs = Product.objects.filter(status='published')
            if search:
                products_qs = products_qs.filter(
                    Q(name__icontains=search) | Q(sku__icontains=search)
                )

            products = []
            for p in products_qs[:limit]:
                thumbnail = None
                if hasattr(p, 'images') and p.images.exists():
                    first_img = p.images.first()
                    # ProductImage uses media_asset field, not image
                    if first_img and hasattr(first_img, 'media_asset') and first_img.media_asset:
                        try:
                            thumbnail = first_img.thumbnail_small
                        except Exception:
                            thumbnail = None

                # URL without language prefix (frontend handles i18n dynamically)
                products.append({
                    'id': p.id,
                    'name': str(p.name),
                    'slug': p.slug,
                    'url': p.get_absolute_url() if hasattr(p, 'get_absolute_url') else f'/product/{p.slug}/',
                    'thumbnail': thumbnail,
                    'sku': p.sku if hasattr(p, 'sku') else None,
                })
            result['products'] = products
        except ImportError:
            result['products'] = []

    # Pages
    if source_type in ('all', 'page'):
        pages_qs = Page.objects.filter(status='published')
        if search:
            pages_qs = pages_qs.filter(
                Q(title__icontains=search) | Q(slug__icontains=search)
            )

        pages = []
        for page in pages_qs[:limit]:
            # URL without language prefix (frontend handles i18n dynamically)
            pages.append({
                'id': page.id,
                'title': str(page.title),
                'name': str(page.title),  # Alias for consistent API
                'slug': page.slug,
                'url': page.get_absolute_url() if hasattr(page, 'get_absolute_url') else f'/page/{page.slug}/',
                'page_type': page.page_type if hasattr(page, 'page_type') else None,
            })
        result['pages'] = pages

    # Categories
    if source_type in ('all', 'category'):
        try:
            from catalog.models import Category
            categories_qs = Category.objects.filter(is_active=True)
            if search:
                categories_qs = categories_qs.filter(
                    Q(name__icontains=search) | Q(slug__icontains=search)
                )

            categories = []
            for cat in categories_qs[:limit]:
                thumbnail = None
                # Category uses image_asset field (MediaAsset FK)
                if hasattr(cat, 'image_asset') and cat.image_asset:
                    try:
                        thumbnail = cat.image_asset.get_thumbnail('small')
                    except Exception:
                        thumbnail = None

                # URL without language prefix (frontend handles i18n dynamically)
                categories.append({
                    'id': cat.id,
                    'name': str(cat.name),
                    'slug': cat.slug,
                    'url': cat.get_absolute_url() if hasattr(cat, 'get_absolute_url') else f'/category/{cat.slug}/',
                    'thumbnail': thumbnail,
                    'parent_id': cat.parent_id if hasattr(cat, 'parent_id') else None,
                })
            result['categories'] = categories
        except ImportError:
            result['categories'] = []

    # Blog posts
    if source_type in ('all', 'blog'):
        try:
            from blog.models import BlogPost
            posts_qs = BlogPost.objects.filter(status='published')
            if search:
                posts_qs = posts_qs.filter(
                    Q(title__icontains=search) | Q(slug__icontains=search)
                )

            blog_posts = []
            for post in posts_qs[:limit]:
                thumbnail = None
                # Blog Post uses featured_image as MediaAsset FK
                if hasattr(post, 'featured_image') and post.featured_image:
                    try:
                        thumbnail = post.featured_image.get_thumbnail('small')
                    except Exception:
                        thumbnail = None

                # URL without language prefix (frontend handles i18n dynamically)
                blog_posts.append({
                    'id': post.id,
                    'title': str(post.title),
                    'name': str(post.title),  # Alias for consistent API
                    'slug': post.slug,
                    'url': post.get_absolute_url() if hasattr(post, 'get_absolute_url') else f'/blog/{post.slug}/',
                    'thumbnail': thumbnail,
                })
            result['blog_posts'] = blog_posts
        except ImportError:
            result['blog_posts'] = []

    return JsonResponse(result)


@csrf_exempt
@staff_required_api
@require_http_methods(["GET"])
def product_search(request):
    """
    Enriched product search for the product picker widget.

    Query parameters:
    - search: Search term (name or SKU)
    - ids: Comma-separated product IDs to look up (for displaying current selections)
    - limit: Max results (default: 20, max: 50)

    Returns product data enriched with thumbnail, formatted prices, sale status, etc.
    """
    from catalog.models import Product

    search = request.GET.get('search', '').strip()
    ids_param = request.GET.get('ids', '').strip()
    limit = min(int(request.GET.get('limit', 20)), 50)

    products_qs = Product.objects.filter(
        status='published', hide_from_storefront=False
    ).exclude(
        sales_channel='pos_only'
    ).select_related('category').prefetch_related('images')

    if ids_param:
        # Look up specific products by ID (for displaying current selections)
        try:
            product_ids = [int(pid) for pid in ids_param.split(',') if pid.strip()]
        except ValueError:
            return JsonResponse({'error': 'Invalid product IDs'}, status=400)
        products_qs = products_qs.filter(id__in=product_ids)
        # Preserve the requested order using CASE WHEN
        if product_ids:
            from django.db.models import Case, When
            preserved_order = Case(
                *[When(pk=pk, then=pos) for pos, pk in enumerate(product_ids)]
            )
            products_qs = products_qs.order_by(preserved_order)
    elif search:
        from django.db.models import Q
        products_qs = products_qs.filter(
            Q(name__icontains=search) | Q(sku__icontains=search)
        )[:limit]
    else:
        # No search or IDs - return recent products
        products_qs = products_qs.order_by('-created_at')[:limit]

    products = []
    for p in products_qs:
        thumbnail = None
        if hasattr(p, 'primary_image_url'):
            thumbnail = p.primary_image_url

        products.append({
            'id': p.id,
            'name': str(p.name),
            'slug': p.slug,
            'sku': p.sku or '',
            'url': p.get_absolute_url(),
            'thumbnail': thumbnail,
            'price': p.formatted_price,
            'compare_price': p.formatted_compare_price if p.is_on_sale else None,
            'is_on_sale': p.is_on_sale,
            'in_stock': p.is_in_stock,
            'category': str(p.category.name) if p.category else '',
            'product_type': p.product_type,
        })

    return JsonResponse({'products': products})


@staff_required_api
@require_http_methods(["POST"])
def capture_page_thumbnail(request, page_id):
    """Save a client-captured screenshot as the page preview thumbnail."""
    import base64
    from io import BytesIO
    from PIL import Image, ImageOps
    from django.core.files.base import ContentFile
    from django.utils import timezone

    page = get_object_or_404(Page, id=page_id)

    # Rate limit: 1 capture per 3 seconds per user
    from django.core.cache import cache as _cache
    rate_key = f'thumb_capture_{request.user.pk}'
    if _cache.get(rate_key):
        return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
    _cache.set(rate_key, 1, timeout=3)

    try:
        data = json.loads(request.body)
        image_data = data.get('image_data')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not image_data:
        return JsonResponse({'error': 'image_data required'}, status=400)

    # Limit base64 payload to ~5MB decoded
    if len(image_data) > 7 * 1024 * 1024:
        return JsonResponse({'error': 'Image data too large'}, status=400)

    try:
        # Strip data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',', 1)[1]

        image_bytes = base64.b64decode(image_data)

        # Guard against decompression bombs
        Image.MAX_IMAGE_PIXELS = 25_000_000  # ~5000x5000

        img = Image.open(BytesIO(image_bytes))

        # Validate image format
        if img.format not in ('PNG', 'JPEG', 'WEBP', 'GIF', 'BMP'):
            return JsonResponse({'error': 'Unsupported image format'}, status=400)

        img.load()

        # Resize to 400x300 cover crop
        img = ImageOps.fit(img, (400, 300), Image.Resampling.LANCZOS)

        # Convert to RGB for WebP (drop alpha channel)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode in ('RGBA', 'LA'):
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background

        # Save as WebP for smaller file size
        output = BytesIO()
        img.save(output, format='WEBP', quality=82, method=4)
        output.seek(0)

        # Delete old thumbnail file if it exists
        if page.preview_thumbnail:
            try:
                page.preview_thumbnail.delete(save=False)
            except Exception:
                pass

        filename = f'page_preview_{page_id}.webp'
        page.preview_thumbnail.save(filename, ContentFile(output.read()), save=False)
        page.preview_thumbnail_updated_at = timezone.now()
        page.save(update_fields=['preview_thumbnail', 'preview_thumbnail_updated_at'])

        return JsonResponse({
            'success': True,
            'thumbnail_url': page.preview_thumbnail.url,
        })

    except Exception as e:
        logger.error("Error capturing page thumbnail: %s", e, exc_info=True)
        return JsonResponse({'error': 'Failed to process thumbnail'}, status=500)