"""Tests for Agent Sessions example."""

import pytest
import respx
from httpx import Response

from trix import Trix, AsyncTrix


@pytest.fixture
def mock_session():
    return {
        "session_id": "sess_123",
        "space_id": None,
        "metadata": {"channel": "web"},
        "created_at": "2026-01-21T00:00:00Z",
        "ended_at": None,
        "summary": None,
    }


@pytest.fixture
def mock_session_memory():
    return {
        "id": "smem_123",
        "session_id": "sess_123",
        "content": "Test message",
        "role": "user",
        "importance": None,
        "created_at": "2026-01-21T00:00:00Z",
    }


@pytest.fixture
def mock_context():
    return {
        "query": "What was discussed?",
        "memories": [
            {
                "id": "mem_1",
                "content": "Relevant memory",
                "type": "text",
                "tags": [],
                "metadata": {},
                "created_at": "2026-01-21T00:00:00Z",
                "updated_at": "2026-01-21T00:00:00Z",
                "access_count": 0,
            },
        ],
        "session_memories": [
            {"id": "smem_1", "session_id": "sess_123", "content": "Message 1", "role": "user", "created_at": "2026-01-21T00:00:00Z"},
        ],
    }


@pytest.fixture
def mock_core_memory():
    return {
        "blocks": [
            {"type": "persona", "content": "I am a helpful assistant.", "updated_at": "2026-01-21T00:00:00Z"},
        ],
        "updated_at": "2026-01-21T00:00:00Z",
    }


@pytest.fixture
def mock_block():
    return {
        "type": "persona",
        "content": "I am a helpful assistant.",
        "updated_at": "2026-01-21T00:00:00Z",
    }


@pytest.fixture
def mock_consolidation():
    return {
        "consolidated_count": 5,
        "new_memories": [],
        "removed_memory_ids": [],
        "relationships_created": 0,
        "dry_run": False,
    }


# =============================================================================
# Synchronous Tests
# =============================================================================

@respx.mock
def test_create_session_sync(mock_session):
    """Test creating a session synchronously."""
    respx.post("https://api.trixdb.com/agent/sessions").mock(
        return_value=Response(200, json=mock_session)
    )

    with Trix(api_key="test") as client:
        session = client.agent.create_session(
            session_id="sess_123",
            metadata={"channel": "web"},
        )

        assert session.session_id == "sess_123"


@respx.mock
def test_add_session_memory_sync(mock_session_memory):
    """Test adding a session memory synchronously."""
    respx.post("https://api.trixdb.com/agent/sessions/sess_123/memories").mock(
        return_value=Response(200, json=mock_session_memory)
    )
    
    with Trix(api_key="test") as client:
        mem = client.agent.add_session_memory(
            session_id="sess_123",
            content="Test message",
            role="user",
        )
        
        assert mem.id == "smem_123"


@respx.mock
def test_get_context_sync(mock_context):
    """Test getting context synchronously."""
    respx.post("https://api.trixdb.com/agent/context").mock(
        return_value=Response(200, json=mock_context)
    )

    with Trix(api_key="test") as client:
        context = client.agent.get_context(
            session_id="sess_123",
            query="What was discussed?",
        )

        assert len(context.memories) == 1


@respx.mock
def test_core_memory_blocks_sync(mock_core_memory, mock_block):
    """Test core memory operations synchronously."""
    respx.get("https://api.trixdb.com/agent/core-memory").mock(
        return_value=Response(200, json=mock_core_memory)
    )
    respx.put("https://api.trixdb.com/agent/memory/core/persona").mock(
        return_value=Response(200, json=mock_block)
    )

    with Trix(api_key="test") as client:
        core = client.agent.get_core_memory()
        assert len(core.blocks) == 1

        block = client.agent.update_block(
            block_type="persona",
            content="Updated content",
        )
        assert block.type == "persona"


# =============================================================================
# Asynchronous Tests
# =============================================================================

@respx.mock
@pytest.mark.asyncio
async def test_create_session_async(mock_session):
    """Test creating a session asynchronously."""
    respx.post("https://api.trixdb.com/agent/sessions").mock(
        return_value=Response(200, json=mock_session)
    )

    async with AsyncTrix(api_key="test") as client:
        session = await client.agent.create_session(
            session_id="sess_123",
            metadata={"channel": "web"},
        )

        assert session.session_id == "sess_123"


@respx.mock
@pytest.mark.asyncio
async def test_consolidate_async(mock_consolidation):
    """Test consolidation asynchronously."""
    respx.post("https://api.trixdb.com/agent/consolidate").mock(
        return_value=Response(200, json=mock_consolidation)
    )

    async with AsyncTrix(api_key="test") as client:
        from trix import ConsolidationStrategy
        result = await client.agent.consolidate(
            strategy=ConsolidationStrategy.SIMILARITY,
            threshold=0.8,
        )

        assert result.consolidated_count == 5

