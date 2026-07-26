"""Merge a guest's session cart into their account cart at login.

Django cycles the session key at login (session-fixation protection), which
orphans any cart keyed by the old session_key. The session DATA survives the
rotation, so CartViewSet.get_cart records the guest cart id there and this
receiver adopts that cart for the user. If the user already has a regular
cart, get_or_create_cart's duplicate-merge folds the two together on the
next fetch.

Accepted residual risk (security review 2026-07-21): classic pre-login
session fixation lets an attacker plant a guest cart that gets adopted at
the victim's login — a nuisance (attacker-chosen items appear in the cart),
not a disclosure; the key rotation cuts the attacker off at login and owned
carts (user set) are never adopted.
"""

import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Cart

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def merge_guest_cart_on_login(sender, request, user, **kwargs):
    cart_id = request.session.pop("guest_cart_id", None)
    if not cart_id:
        return
    cart = Cart.objects.filter(id=cart_id, user__isnull=True).first()
    if cart is None or not cart.items.exists():
        return
    cart.user = user
    cart.session_key = None
    cart.save(update_fields=["user", "session_key"])
    logger.info("Adopted guest cart %s for user %s at login", cart_id, user.pk)
