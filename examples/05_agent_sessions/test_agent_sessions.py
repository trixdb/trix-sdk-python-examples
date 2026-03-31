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
            {
                "id": "smem_1",
                "session_id": "sess_123",
                "content": "Message 1",
                "role": "user",
                "created_at": "2026-01-21T00:00:00Z",
            },
        ],
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
            query="What was discussed?",
            session_id="sess_123",
        )

        assert len(context.memories) == 1


@respx.mock
def test_end_session_sync(mock_session):
    """Test ending a session synchronously."""
    ended = {**mock_session, "ended_at": "2026-01-21T01:00:00Z", "summary": "Test summary"}
    respx.post("https://api.trixdb.com/agent/sessions/sess_123/end").mock(
        return_value=Response(200, json=ended)
    )

    with Trix(api_key="test") as client:
        session = client.agent.end_session(
            session_id="sess_123",
            summary="Test summary",
            key_insights=["Insight 1"],
        )

        assert session.summary == "Test summary"


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
async def test_end_session_async(mock_session):
    """Test ending a session asynchronously."""
    ended = {**mock_session, "ended_at": "2026-01-21T01:00:00Z"}
    respx.post("https://api.trixdb.com/agent/sessions/sess_123/end").mock(
        return_value=Response(200, json=ended)
    )

    async with AsyncTrix(api_key="test") as client:
        session = await client.agent.end_session(
            session_id="sess_123",
            summary="Discussion summary",
        )

        assert session.session_id == "sess_123"
