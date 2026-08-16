"""Signals that invalidate cached visibility configuration.

A page's cached "has temporal visibility rules" flag is derived from rules, rule
groups and group membership. Any of those changing must drop the derived caches
immediately so a time-sensitive page can't be cached for its full timeout —
hence a single global version stamp bumped on every such change. These edits are
infrequent (rule configuration), so a coarse global bump is cheap and correct.

The element-side receivers (Element save/delete and the Element↔RuleGroup link)
live in ``page_builder.signals`` because Element belongs to that app; they import
``bump_visibility_config_version`` from here.
"""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (
    RuleGroup,
    RuleGroupMember,
    VisibilityRule,
    bump_visibility_config_version,
)


@receiver(post_save, sender=VisibilityRule)
@receiver(post_delete, sender=VisibilityRule)
@receiver(post_save, sender=RuleGroup)
@receiver(post_delete, sender=RuleGroup)
@receiver(post_save, sender=RuleGroupMember)
@receiver(post_delete, sender=RuleGroupMember)
def _bump_on_rule_change(sender, **kwargs):
    bump_visibility_config_version()
