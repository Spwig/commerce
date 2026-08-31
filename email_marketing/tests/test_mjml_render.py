"""_render_mjml compiles MJML source to an HTML string.

Guards the mjml-python call convention: the package exposes ``mjml_to_html``
returning a dict-like whose HTML is on ``["html"]``. A regression here (e.g.
reverting to ``from mjml import mjml2html``, which binds the submodule) would
crash every campaign send at the render step.
"""

import unittest

from email_marketing.services.campaigns import _render_mjml

VALID_MJML = (
    "<mjml><mj-body><mj-section><mj-column>"
    "<mj-text>Hi {{ first_name }}</mj-text>"
    "</mj-column></mj-section></mj-body></mjml>"
)


class RenderMjmlTests(unittest.TestCase):
    def test_render_mjml_returns_compiled_html_string(self):
        result = _render_mjml(VALID_MJML)
        self.assertIsInstance(result, str)
        self.assertIn("<", result)
        # Merge tags survive compilation for per-recipient rendering downstream.
        self.assertIn("{{ first_name }}", result)
