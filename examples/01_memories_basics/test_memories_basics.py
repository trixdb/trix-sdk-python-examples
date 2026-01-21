"""Tests for Memory Basics example."""

import pytest
import respx
from httpx import Response

from trix import Trix, AsyncTrix


@pytest.fixture
def mock_memory():
    return {
        "id": "mem_123",
        "content": "Test content",
        "type": "text",
        "tags": ["test"],
        "metadata": {},
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
        "access_count": 0,
    }


@pytest.fixture
def mock_memory_list(mock_memory):
    return {
        "data": [mock_memory],
        "total": 1,
        "limit": 10,
        "offset": 0,
    }


@pytest.fixture
def mock_stats():
    return {"total": 100, "total_size_bytes": 50000}


@pytest.fixture
def mock_config():
    return {
        "max_content_length": 10000,
        "supported_types": ["text", "image", "audio"],
        "embedding_model": "text-embedding-3-small",
        "embedding_dimensions": 1536,
    }


# =============================================================================
# Synchronous Tests
# =============================================================================

@respx.mock
def test_memory_crud_sync(mock_memory):
    """Test full CRUD cycle synchronously."""
    # Create
    respx.post("https://api.trixdb.com/memories").mock(
        return_value=Response(200, json=mock_memory)
    )
    # Get
    respx.get("https://api.trixdb.com/memories/mem_123").mock(
        return_value=Response(200, json=mock_memory)
    )
    # Update
    updated_memory = {**mock_memory, "tags": ["test", "updated"]}
    respx.patch("https://api.trixdb.com/memories/mem_123").mock(
        return_value=Response(200, json=updated_memory)
    )
    # Delete
    respx.delete("https://api.trixdb.com/memories/mem_123").mock(
        return_value=Response(204)
    )
    
    with Trix(api_key="test") as client:
        # Create
        created = client.memories.create(content="Test content")
        assert created.id == "mem_123"
        
        # Read
        retrieved = client.memories.get("mem_123")
        assert retrieved.content == "Test content"
        
        # Update
        updated = client.memories.update("mem_123", tags=["test", "updated"])
        assert "updated" in updated.tags
        
        # Delete
        client.memories.delete("mem_123")


@respx.mock
def test_bulk_operations_sync(mock_memory):
    """Test bulk create and delete synchronously."""
    from trix.types import MemoryCreate

    respx.post("https://api.trixdb.com/memories/bulk").mock(
        return_value=Response(200, json={"data": [mock_memory, mock_memory]})
    )
    respx.delete("https://api.trixdb.com/memories/bulk").mock(
        return_value=Response(204)
    )

    with Trix(api_key="test") as client:
        memories = client.memories.bulk_create([
            MemoryCreate(content="Memory 1"),
            MemoryCreate(content="Memory 2"),
        ])
        assert len(memories) == 2

        client.memories.bulk_delete(["mem_123", "mem_456"])


@respx.mock
def test_list_and_stats_sync(mock_memory_list, mock_stats, mock_config):
    """Test list, stats, and config synchronously."""
    respx.get("https://api.trixdb.com/memories").mock(
        return_value=Response(200, json=mock_memory_list)
    )
    respx.get("https://api.trixdb.com/memories/stats").mock(
        return_value=Response(200, json=mock_stats)
    )
    respx.get("https://api.trixdb.com/memories/config").mock(
        return_value=Response(200, json=mock_config)
    )
    
    with Trix(api_key="test") as client:
        page = client.memories.list(limit=10)
        assert len(page.data) == 1
        
        stats = client.memories.get_stats()
        assert stats.total == 100
        
        config = client.memories.get_config()
        assert config.max_content_length == 10000


# =============================================================================
# Asynchronous Tests
# =============================================================================

@respx.mock
@pytest.mark.asyncio
async def test_memory_crud_async(mock_memory):
    """Test full CRUD cycle asynchronously."""
    respx.post("https://api.trixdb.com/memories").mock(
        return_value=Response(200, json=mock_memory)
    )
    respx.get("https://api.trixdb.com/memories/mem_123").mock(
        return_value=Response(200, json=mock_memory)
    )
    respx.delete("https://api.trixdb.com/memories/mem_123").mock(
        return_value=Response(204)
    )
    
    async with AsyncTrix(api_key="test") as client:
        created = await client.memories.create(content="Test content")
        assert created.id == "mem_123"
        
        retrieved = await client.memories.get("mem_123")
        assert retrieved.content == "Test content"
        
        await client.memories.delete("mem_123")

