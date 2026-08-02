"""
Tests for the Getting Started example.

These tests use respx to mock HTTP requests, allowing testing without a real API.
"""

import pytest
import respx
from httpx import Response
from trix import AsyncTrix, Trix

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_memory():
    """Sample memory response data."""
    return {
        "id": "mem_test123",
        "content": "The Trix SDK makes it easy to store and retrieve memories.",
        "type": "text",
        "tags": ["getting-started", "tutorial"],
        "metadata": {"source": "example", "importance": "high"},
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
        "access_count": 0,
    }


# =============================================================================
# Synchronous Tests
# =============================================================================


@respx.mock
def test_create_memory_sync(mock_memory):
    """Test creating a memory synchronously."""
    # Setup mock
    respx.post("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(200, json=mock_memory)
    )

    with Trix(api_key="test_key") as client:
        memory = client.memories.create(
            content="The Trix SDK makes it easy to store and retrieve memories.",
            tags=["getting-started", "tutorial"],
        )

        assert memory.id == "mem_test123"
        assert "getting-started" in memory.tags


@respx.mock
def test_search_memories_sync(mock_memory):
    """Test searching memories synchronously."""
    mock_list = {
        "data": [mock_memory],
        "total": 1,
        "limit": 5,
        "offset": 0,
    }
    respx.get("https://api.trixdb.com/v1/memories").mock(return_value=Response(200, json=mock_list))

    with Trix(api_key="test_key") as client:
        results = client.memories.list(q="How do I store memories?", limit=5)

        assert len(results.data) == 1
        assert results.data[0].id == "mem_test123"


# =============================================================================
# Asynchronous Tests
# =============================================================================


@respx.mock
@pytest.mark.asyncio
async def test_create_memory_async(mock_memory):
    """Test creating a memory asynchronously."""
    respx.post("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(200, json=mock_memory)
    )

    async with AsyncTrix(api_key="test_key") as client:
        memory = await client.memories.create(
            content="The Trix SDK makes it easy to store and retrieve memories.",
            tags=["getting-started", "tutorial"],
        )

        assert memory.id == "mem_test123"
        assert "getting-started" in memory.tags


@respx.mock
@pytest.mark.asyncio
async def test_search_memories_async(mock_memory):
    """Test searching memories asynchronously."""
    mock_list = {
        "data": [mock_memory],
        "total": 1,
        "limit": 5,
        "offset": 0,
    }
    respx.get("https://api.trixdb.com/v1/memories").mock(return_value=Response(200, json=mock_list))

    async with AsyncTrix(api_key="test_key") as client:
        results = await client.memories.list(q="How do I store memories?", limit=5)

        assert len(results.data) == 1
        assert results.data[0].id == "mem_test123"
