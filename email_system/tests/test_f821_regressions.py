"""Regression tests for email_system F821 bugs.

- email_system/admin.py EmailAccountAdmin.get_queryset used Q(...) without
  importing it. Any search query on the changelist raised NameError.
- email_system/views/wizard.py test-send POST (ProviderWizardStep5View)
  referenced `component_id` before it was assigned.
- email_system/views/wizard.py completion GET (ProviderWizardStep6View)
  rendered a context dict with `is_builtin` which was never defined in
  the method.

The wizard checks are done via AST inspection so they remain green as the
code around them is refactored — the invariant we care about is
"undefined name is not referenced before assignment", not a specific
line-by-line ordering."""

import ast
import inspect

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from email_system.admin import EmailAccountAdmin
from email_system.models import EmailAccount
from email_system.views import wizard as wizard_module

User = get_user_model()


def _find_class_method(module, class_name, method_name):
    """Return the ast.FunctionDef for module.ClassName.method_name."""
    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if (
                    isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and child.name == method_name
                ):
                    return child
    raise AssertionError(f"Could not locate {class_name}.{method_name} in {module.__name__}")


def _first_line_using(fn_node, name):
    """Return the first ast node line that reads `name` as a Load."""
    for sub in ast.walk(fn_node):
        if isinstance(sub, ast.Name) and sub.id == name and isinstance(sub.ctx, ast.Load):
            return sub.lineno
    return None


def _first_line_assigning(fn_node, name):
    """Return the first line that assigns to `name`."""
    for sub in ast.walk(fn_node):
        if isinstance(sub, ast.Assign):
            for target in sub.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return sub.lineno
    return None


class EmailAccountAdminSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="email_admin_regression",
            email="ear@example.com",
            password="pw",
        )
        self.admin = EmailAccountAdmin(EmailAccount, AdminSite())

    def test_search_query_does_not_raise(self):
        request = RequestFactory().get(
            "/en/admin/email_system/emailaccount/", {"q": "test@example.com"}
        )
        request.user = self.user
        qs = self.admin.get_queryset(request)
        list(qs)


class WizardComponentIdScopeTest(TestCase):
    """component_id must be assigned before any reference inside
    ProviderWizardStep5View.post — the original F821 bug crashed on
    the very first `if component_id == 'builtin_smtp':` line."""

    def test_component_id_assigned_before_first_use(self):
        post = _find_class_method(wizard_module, "ProviderWizardStep5View", "post")
        assign_line = _first_line_assigning(post, "component_id")
        use_line = _first_line_using(post, "component_id")

        self.assertIsNotNone(assign_line, "component_id is never assigned inside post()")
        self.assertIsNotNone(use_line, "component_id is never read inside post()")
        self.assertLess(
            assign_line,
            use_line,
            "component_id must be assigned before it is read (F821 regression)",
        )


class WizardIsBuiltinAssignedTest(TestCase):
    """is_builtin must be assigned before it is used inside
    ProviderWizardStep6View.get (the completion step) so that the
    context dict does not reference an undefined name."""

    def test_is_builtin_assigned_before_first_use(self):
        get = _find_class_method(wizard_module, "ProviderWizardStep6View", "get")
        assign_line = _first_line_assigning(get, "is_builtin")
        use_line = _first_line_using(get, "is_builtin")

        self.assertIsNotNone(assign_line, "is_builtin is never assigned inside get()")
        self.assertIsNotNone(use_line, "is_builtin is never read inside get()")
        self.assertLess(
            assign_line,
            use_line,
            "is_builtin must be assigned before it is read (F821 regression)",
        )
