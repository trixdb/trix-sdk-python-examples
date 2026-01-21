"""Tests for Webhooks example."""

import pytest
import respx
from httpx import Response

from trix import Trix, AsyncTrix


@pytest.fixture
def mock_webhook():
    return {
        "id": "wh_123",
        "name": "Test Webhook",
        "url": "https://example.com/webhook",
        "events": ["memory.created", "memory.updated"],
        "space_id": None,
        "headers": {},
        "filters": None,
        "active": True,
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
    }


@pytest.fixture
def mock_webhook_list(mock_webhook):
    return {
        "data": [mock_webhook],
    }


@pytest.fixture
def mock_event_types():
    return {
        "event_types": [
            {"name": "memory.created", "description": "Memory created"},
            {"name": "memory.updated", "description": "Memory updated"},
            {"name": "memory.deleted", "description": "Memory deleted"},
        ]
    }


@pytest.fixture
def mock_test_result():
    return {
        "success": True,
        "status_code": 200,
    }


@pytest.fixture
def mock_deliveries():
    return {
        "data": [
            {
                "id": "del_1",
                "webhook_id": "wh_123",
                "event_type": "memory.created",
                "success": True,
                "status_code": 200,
                "payload": {},
                "error": None,
                "attempted_at": "2026-01-21T00:00:00Z",
            },
        ],
    }


# =============================================================================
# Synchronous Tests
# =============================================================================

@respx.mock
def test_create_webhook_sync(mock_webhook):
    """Test creating a webhook synchronously."""
    respx.post("https://api.trixdb.com/webhooks").mock(
        return_value=Response(200, json=mock_webhook)
    )

    with Trix(api_key="test") as client:
        from trix import WebhookEvent
        webhook = client.webhooks.create(
            name="Test Webhook",
            url="https://example.com/webhook",
            events=[WebhookEvent.MEMORY_CREATED],
        )

        assert webhook.id == "wh_123"
        assert webhook.active is True


@respx.mock
def test_list_webhooks_sync(mock_webhook_list):
    """Test listing webhooks synchronously."""
    respx.get("https://api.trixdb.com/webhooks").mock(
        return_value=Response(200, json=mock_webhook_list)
    )
    
    with Trix(api_key="test") as client:
        webhooks = client.webhooks.list()
        
        assert len(webhooks.data) == 1


@respx.mock
def test_get_event_types_sync(mock_event_types):
    """Test getting event types synchronously."""
    respx.get("https://api.trixdb.com/webhooks/event-types").mock(
        return_value=Response(200, json=mock_event_types)
    )

    with Trix(api_key="test") as client:
        types = client.webhooks.get_event_types()

        assert len(types) == 3


@respx.mock
def test_test_webhook_sync(mock_test_result):
    """Test testing a webhook synchronously."""
    respx.post("https://api.trixdb.com/webhooks/wh_123/test").mock(
        return_value=Response(200, json=mock_test_result)
    )

    with Trix(api_key="test") as client:
        result = client.webhooks.test("wh_123")

        assert result["success"] is True
        assert result["status_code"] == 200


@respx.mock
def test_get_deliveries_sync(mock_deliveries):
    """Test getting deliveries synchronously."""
    respx.get("https://api.trixdb.com/webhooks/wh_123/deliveries").mock(
        return_value=Response(200, json=mock_deliveries)
    )
    
    with Trix(api_key="test") as client:
        deliveries = client.webhooks.get_deliveries("wh_123")
        
        assert len(deliveries.data) == 1


# =============================================================================
# Asynchronous Tests
# =============================================================================

@respx.mock
@pytest.mark.asyncio
async def test_create_webhook_async(mock_webhook):
    """Test creating a webhook asynchronously."""
    respx.post("https://api.trixdb.com/webhooks").mock(
        return_value=Response(200, json=mock_webhook)
    )

    async with AsyncTrix(api_key="test") as client:
        from trix import WebhookEvent
        webhook = await client.webhooks.create(
            name="Test Webhook",
            url="https://example.com/webhook",
            events=[WebhookEvent.MEMORY_CREATED],
        )

        assert webhook.id == "wh_123"


@respx.mock
@pytest.mark.asyncio
async def test_list_webhooks_async(mock_webhook_list):
    """Test listing webhooks asynchronously."""
    respx.get("https://api.trixdb.com/webhooks").mock(
        return_value=Response(200, json=mock_webhook_list)
    )
    
    async with AsyncTrix(api_key="test") as client:
        webhooks = await client.webhooks.list()
        
        assert len(webhooks.data) == 1

