"""Identity stitch binds an anonymous touch stream to a customer."""

import pytest
from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory

from attribution.models import TouchPoint, VisitorThread
from attribution.services import identity
from attribution.signals import bind_touch_stream_on_login

pytestmark = pytest.mark.django_db

User = get_user_model()


def _touch(visitor_key, channel="email"):
    return TouchPoint.objects.create(visitor_key=visitor_key, channel=channel, medium=channel)


def test_ensure_visitor_key_mints_and_stashes():
    req = RequestFactory().get("/")
    req.session = SessionStore()
    req.session.create()
    key, is_new = identity.ensure_visitor_key(req)
    assert key and is_new
    assert req.attribution_visitor_key == key
    assert req.session[identity.SESSION_STASH_KEY] == key
    assert getattr(req, "_attribution_new_visitor_key", False) is True


def test_ensure_visitor_key_reuses_cookie():
    req = RequestFactory().get("/")
    req.session = SessionStore()
    req.session.create()
    req.COOKIES[identity.VISITOR_COOKIE] = "existing-key-123"
    key, is_new = identity.ensure_visitor_key(req)
    assert key == "existing-key-123"
    assert is_new is False


def test_bind_customer_backfills_touch_stream():
    user = User.objects.create_user(username="buyer", email="b@example.com", password="x")
    vk = "vk-bind-1"
    _touch(vk)
    _touch(vk, channel="organic_search")

    n = identity.bind_customer(vk, user)

    assert n == 2
    assert TouchPoint.objects.filter(visitor_key=vk, customer=user).count() == 2
    thread = VisitorThread.objects.get(visitor_key=vk)
    assert thread.customer_id == user.id


def test_bind_customer_is_idempotent():
    user = User.objects.create_user(username="buyer2", email="b2@example.com", password="x")
    vk = "vk-bind-2"
    _touch(vk)
    identity.bind_customer(vk, user)
    # Second run backfills nothing new (already bound).
    assert identity.bind_customer(vk, user) == 0


def test_login_signal_stitches_from_cookie():
    user = User.objects.create_user(username="buyer3", email="b3@example.com", password="x")
    vk = "vk-login-1"
    _touch(vk)

    req = RequestFactory().get("/")
    req.session = SessionStore()
    req.session.create()
    req.COOKIES[identity.VISITOR_COOKIE] = vk

    bind_touch_stream_on_login(sender=None, request=req, user=user)

    assert TouchPoint.objects.get(visitor_key=vk).customer_id == user.id
