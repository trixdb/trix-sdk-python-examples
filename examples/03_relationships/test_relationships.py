"""Tests for Relationships example."""

import pytest
import respx
from httpx import Response

from trix import Trix, AsyncTrix


@pytest.fixture
def mock_relationship():
    return {
        "id": "rel_123",
        "source_id": "mem_1",
        "target_id": "mem_2",
        "relationship_type": "related_to",
        "weight": 0.9,
        "bidirectional": False,
        "metadata": {},
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
        "reinforcement_count": 0,
    }


@pytest.fixture
def mock_relationship_list(mock_relationship):
    return {
        "data": [mock_relationship],
        "total": 1,
        "limit": 10,
        "offset": 0,
    }


@pytest.fixture
def mock_related_memories(mock_relationship):
    return {
        "memory_id": "mem_1",
        "related": [
            {
                "memory": {
                    "id": "mem_2",
                    "content": "Related content",
                    "type": "text",
                    "tags": [],
                    "metadata": {},
                    "created_at": "2026-01-21T00:00:00Z",
                    "updated_at": "2026-01-21T00:00:00Z",
                    "access_count": 0,
                },
                "relationship": mock_relationship,
                "score": 0.9,
            }
        ],
    }


@pytest.fixture
def mock_relationship_types():
    return {
        "types": [
            {"name": "related_to", "description": "General relationship"},
            {"name": "similar_to", "description": "Similar content"},
        ]
    }


# =============================================================================
# Synchronous Tests
# =============================================================================

@respx.mock
def test_create_relationship_sync(mock_relationship):
    """Test creating a relationship synchronously."""
    from trix.types import RelationshipType

    respx.post("https://api.trixdb.com/relationships/mem_1/create/mem_2").mock(
        return_value=Response(200, json=mock_relationship)
    )

    with Trix(api_key="test") as client:
        rel = client.relationships.create(
            source_id="mem_1",
            target_id="mem_2",
            relationship_type=RelationshipType.RELATED_TO,
        )

        assert rel.id == "rel_123"
        assert rel.weight == 0.9


@respx.mock
def test_get_incoming_sync(mock_relationship_list):
    """Test getting incoming relationships synchronously."""
    respx.get("https://api.trixdb.com/relationships/mem_1/incoming").mock(
        return_value=Response(200, json=mock_relationship_list)
    )

    with Trix(api_key="test") as client:
        incoming = client.relationships.get_incoming("mem_1")

        assert len(incoming.data) == 1


@respx.mock
def test_reinforce_sync(mock_relationship):
    """Test reinforcing a relationship synchronously."""
    reinforced = {**mock_relationship, "weight": 1.0, "reinforcement_count": 1}
    respx.post("https://api.trixdb.com/relationships/rel_123/reinforce").mock(
        return_value=Response(200, json=reinforced)
    )

    with Trix(api_key="test") as client:
        result = client.relationships.reinforce("rel_123", boost=0.1)

        assert result.weight == 1.0
        assert result.reinforcement_count == 1


@respx.mock
def test_get_related_sync(mock_related_memories):
    """Test getting related memories synchronously."""
    respx.get("https://api.trixdb.com/relationships/mem_1/related").mock(
        return_value=Response(200, json=mock_related_memories)
    )

    with Trix(api_key="test") as client:
        related = client.relationships.get_related("mem_1")

        assert len(related.related) == 1
        assert related.related[0].score == 0.9


# =============================================================================
# Asynchronous Tests
# =============================================================================

@respx.mock
@pytest.mark.asyncio
async def test_create_relationship_async(mock_relationship):
    """Test creating a relationship asynchronously."""
    from trix.types import RelationshipType

    respx.post("https://api.trixdb.com/relationships/mem_1/create/mem_2").mock(
        return_value=Response(200, json=mock_relationship)
    )

    async with AsyncTrix(api_key="test") as client:
        rel = await client.relationships.create(
            source_id="mem_1",
            target_id="mem_2",
            relationship_type=RelationshipType.RELATED_TO,
        )

        assert rel.id == "rel_123"


@respx.mock
@pytest.mark.asyncio
async def test_get_related_async(mock_related_memories):
    """Test getting related memories asynchronously."""
    respx.get("https://api.trixdb.com/relationships/mem_1/related").mock(
        return_value=Response(200, json=mock_related_memories)
    )

    async with AsyncTrix(api_key="test") as client:
        related = await client.relationships.get_related("mem_1")

        assert len(related.related) == 1

