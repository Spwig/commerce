"""Element-side signals that invalidate cached visibility configuration.

A page's cached "has temporal visibility rules" flag also depends on element
state (activation/deactivation, moving an element between pages/parents) and on
the Element↔RuleGroup links. Those changes bump the shared version stamp defined
in ``visibility`` so a time-sensitive page can't be cached for its full timeout.
The rule/group/membership receivers live in ``visibility.signals``.
"""

from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from visibility.models import bump_visibility_config_version

from .models import Element


# Element activation/deactivation or moving an element between pages/parents
# changes which page a (possibly temporal) rule affects. Element edits happen at
# authoring time, so the extra invalidations are cheap.
@receiver(post_save, sender=Element)
@receiver(post_delete, sender=Element)
def _bump_on_element_change(sender, **kwargs):
    bump_visibility_config_version()


@receiver(m2m_changed, sender=Element.visibility_rules.through)
def _bump_on_element_rule_link_change(sender, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        bump_visibility_config_version()
