"""
SVG Sanitizer - Remove potentially malicious content from SVG files

Strips out JavaScript, event handlers, and external references while preserving
the visual appearance of the SVG for use as logos, icons, etc.
"""
import re
from lxml import etree
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

# Dangerous SVG elements that can execute scripts
DANGEROUS_ELEMENTS = {
    'script',
    'foreignObject',
    'iframe',
    'embed',
    'object',
    'animate',  # Can be used for timing attacks
    'animateMotion',
    'animateTransform',
    'set',
}

# Event handler attributes (onclick, onload, etc.)
EVENT_HANDLERS = [
    'onload', 'onclick', 'onmouseover', 'onmouseout', 'onmousemove',
    'onmousedown', 'onmouseup', 'onfocus', 'onblur', 'onchange',
    'onsubmit', 'onreset', 'onselect', 'onkeydown', 'onkeyup',
    'onkeypress', 'onerror', 'onabort', 'ondblclick', 'ondrag',
    'ondragend', 'ondragenter', 'ondragleave', 'ondragover',
    'ondragstart', 'ondrop', 'onscroll', 'onwheel', 'ontouchstart',
    'ontouchend', 'ontouchmove', 'ontouchcancel'
]


def sanitize_svg(svg_content: bytes) -> bytes:
    """
    Sanitize SVG content by removing potentially malicious elements and attributes.

    Args:
        svg_content: Raw SVG file content as bytes

    Returns:
        Sanitized SVG content as bytes

    Raises:
        ValueError: If SVG cannot be parsed or sanitized
    """
    try:
        # Parse SVG as XML
        parser = etree.XMLParser(
            remove_blank_text=True,
            remove_comments=True,
            resolve_entities=False,  # Prevent XXE attacks
            no_network=True,  # Prevent external entity fetching
        )
        
        tree = etree.parse(BytesIO(svg_content), parser)
        root = tree.getroot()

        # Remove dangerous elements (iterate through all elements)
        elements_to_remove = []
        for element in root.iter():
            # Get tag name without namespace
            tag_name = element.tag.split('}')[-1] if '}' in element.tag else element.tag

            if tag_name.lower() in DANGEROUS_ELEMENTS:
                logger.warning(f"Removing dangerous SVG element: {tag_name}")
                elements_to_remove.append(element)

        # Remove elements (do this after iteration to avoid modifying tree while iterating)
        for element in elements_to_remove:
            parent = element.getparent()
            if parent is not None:
                parent.remove(element)

        # Remove event handler attributes and javascript: URLs from all elements
        for element in root.iter():
            # Remove event handlers
            for attr in EVENT_HANDLERS:
                if attr in element.attrib:
                    logger.warning(f"Removing event handler: {attr}")
                    del element.attrib[attr]

            # Check for javascript: in href and xlink:href
            for attr in ['href', '{http://www.w3.org/1999/xlink}href']:
                if attr in element.attrib:
                    value = element.attrib[attr]
                    if value.strip().lower().startswith('javascript:'):
                        logger.warning(f"Removing javascript: URL from {attr}")
                        del element.attrib[attr]
                    # Also block data: URIs with script content
                    elif value.strip().lower().startswith('data:') and 'script' in value.lower():
                        logger.warning(f"Removing suspicious data: URI from {attr}")
                        del element.attrib[attr]

            # Remove any remaining script-like content in attributes
            for attr, value in list(element.attrib.items()):
                # Check for inline scripts in style attributes
                if attr == 'style' and 'expression(' in value.lower():
                    logger.warning(f"Removing expression() from style attribute")
                    del element.attrib[attr]

        # Convert back to bytes
        sanitized_svg = etree.tostring(
            tree,
            encoding='utf-8',
            xml_declaration=True,
            pretty_print=False
        )

        logger.info("SVG sanitized successfully")
        return sanitized_svg

    except etree.XMLSyntaxError as e:
        raise ValueError(f"Invalid SVG file: {e}")
    except Exception as e:
        raise ValueError(f"Failed to sanitize SVG: {e}")


def is_svg_safe(svg_content: bytes) -> tuple[bool, str]:
    """
    Quick check if SVG contains obviously malicious content.

    Args:
        svg_content: Raw SVG file content as bytes

    Returns:
        Tuple of (is_safe, reason)
    """
    content_lower = svg_content.lower()

    # Check for script tags
    if b'<script' in content_lower:
        return False, "Contains <script> tags"

    # Check for javascript: URLs
    if b'javascript:' in content_lower:
        return False, "Contains javascript: URLs"

    # Check for event handlers
    for handler in EVENT_HANDLERS:
        if f' {handler}='.encode().lower() in content_lower:
            return False, f"Contains {handler} event handler"

    return True, "No obvious threats detected"
