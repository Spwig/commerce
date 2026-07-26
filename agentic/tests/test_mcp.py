"""
Storefront MCP server: JSON-RPC 2.0, gating, and the catalog tools.

The server projects the same catalog as the UCP REST binding, so these tests
focus on the MCP protocol envelope (initialize / tools/list / tools/call,
notifications, errors) and the off = 404 gate.
"""

import json

import pytest
from django.test import Client

from agentic.models import AgenticSettings
from tests.factories import ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]

MCP_URL = "/api/agentic/mcp"


@pytest.fixture
def client():
    return Client()


def _enable(**overrides):
    s = AgenticSettings.get_settings()
    s.is_enabled = True
    for k, v in overrides.items():
        setattr(s, k, v)
    s.save()


def _rpc(client, method, params=None, request_id=1):
    body = {"jsonrpc": "2.0", "method": method, "id": request_id}
    if params is not None:
        body["params"] = params
    resp = client.post(MCP_URL, data=json.dumps(body), content_type="application/json")
    return resp


class TestGating:
    def test_post_404_when_disabled(self, client):
        resp = client.post(
            MCP_URL,
            data=json.dumps({"jsonrpc": "2.0", "method": "ping", "id": 1}),
            content_type="application/json",
        )
        assert resp.status_code == 404

    def test_404_when_mcp_surface_off(self, client):
        _enable(mcp_storefront_enabled=False)
        resp = _rpc(client, "ping")
        assert resp.status_code == 404

    def test_get_is_405_when_enabled(self, client):
        _enable()
        assert client.get(MCP_URL).status_code == 405


class TestProtocol:
    def test_initialize(self, client):
        _enable()
        data = _rpc(client, "initialize").json()
        assert data["jsonrpc"] == "2.0"
        assert data["result"]["protocolVersion"] == "2025-11-25"
        assert data["result"]["capabilities"]["tools"] == {}
        assert data["result"]["serverInfo"]["name"] == "Spwig Storefront"

    def test_tools_list(self, client):
        _enable()
        tools = _rpc(client, "tools/list").json()["result"]["tools"]
        names = {t["name"] for t in tools}
        assert names == {"search_catalog", "get_product"}
        # Each tool advertises an input schema.
        assert all("inputSchema" in t for t in tools)

    def test_notification_gets_no_body(self, client):
        _enable()
        # No "id" → a notification; the server must not respond with a result.
        resp = client.post(
            MCP_URL,
            data=json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}),
            content_type="application/json",
        )
        assert resp.status_code == 202
        assert resp.content == b""

    def test_unknown_method(self, client):
        _enable()
        data = _rpc(client, "does/not/exist").json()
        assert data["error"]["code"] == -32601

    def test_invalid_json(self, client):
        _enable()
        resp = client.post(MCP_URL, data="{not json", content_type="application/json")
        assert resp.status_code == 400
        assert resp.json()["error"]["code"] == -32700

    def test_batch_rejected(self, client):
        _enable()
        resp = client.post(
            MCP_URL,
            data=json.dumps([{"jsonrpc": "2.0", "method": "ping", "id": 1}]),
            content_type="application/json",
        )
        assert resp.status_code == 400


class TestCatalogTools:
    def test_search_catalog(self, client):
        ProductFactory(name="Blue Widget", status="published")
        ProductFactory(name="Red Gadget", status="published")
        _enable()

        data = _rpc(
            client, "tools/call", {"name": "search_catalog", "arguments": {"query": "widget"}}
        ).json()
        result = data["result"]
        assert "structuredContent" in result
        payload = result["structuredContent"]
        assert payload["total"] == 1
        assert payload["products"][0]["title"] == "Blue Widget"
        # The text content mirrors the structured content as JSON.
        assert json.loads(result["content"][0]["text"])["total"] == 1

    def test_get_product(self, client):
        p = ProductFactory(name="Lookup Me", status="published")
        _enable()
        data = _rpc(
            client, "tools/call", {"name": "get_product", "arguments": {"id": str(p.id)}}
        ).json()
        assert data["result"]["structuredContent"]["title"] == "Lookup Me"

    def test_get_product_unknown_id_is_tool_error(self, client):
        _enable()
        data = _rpc(
            client, "tools/call", {"name": "get_product", "arguments": {"id": "999999"}}
        ).json()
        # Tool-level failure surfaces as isError in the result, not a protocol error.
        assert data["result"]["isError"] is True
        assert "error" not in data

    def test_unknown_tool(self, client):
        _enable()
        data = _rpc(client, "tools/call", {"name": "delete_everything", "arguments": {}}).json()
        assert data["error"]["code"] == -32601

    def test_get_product_respects_agent_visibility(self, client):
        hidden = ProductFactory(name="Hidden", status="published", agent_visible=False)
        _enable()
        data = _rpc(
            client, "tools/call", {"name": "get_product", "arguments": {"id": str(hidden.id)}}
        ).json()
        assert data["result"]["isError"] is True
