"""Tests for Knowledge Graph example."""

import pytest
import respx
from httpx import Response

from trix import Trix, AsyncTrix


@pytest.fixture
def mock_traversal():
    return {
        "nodes": [
            {
                "memory": {
                    "id": "mem_1",
                    "content": "Node 1",
                    "type": "text",
                    "tags": [],
                    "metadata": {},
                    "created_at": "2026-01-21T00:00:00Z",
                    "updated_at": "2026-01-21T00:00:00Z",
                    "access_count": 0,
                },
                "relationships": [],
                "depth": 0,
            },
            {
                "memory": {
                    "id": "mem_2",
                    "content": "Node 2",
                    "type": "text",
                    "tags": [],
                    "metadata": {},
                    "created_at": "2026-01-21T00:00:00Z",
                    "updated_at": "2026-01-21T00:00:00Z",
                    "access_count": 0,
                },
                "relationships": [],
                "depth": 1,
            },
        ],
        "total_nodes": 2,
    }


@pytest.fixture
def mock_path():
    return {
        "source_id": "mem_1",
        "target_id": "mem_3",
        "path": ["mem_1", "mem_2", "mem_3"],
        "relationships": [],
        "distance": 2,
    }


@pytest.fixture
def mock_neighbors():
    return {
        "node_id": "mem_1",
        "neighbors": [
            {
                "id": "mem_2",
                "type": "memory",
                "relationship": {
                    "id": "rel_1",
                    "source_id": "mem_2",
                    "target_id": "mem_1",
                    "relationship_type": "related_to",
                    "weight": 0.9,
                    "bidirectional": False,
                    "created_at": "2026-01-21T00:00:00Z",
                    "updated_at": "2026-01-21T00:00:00Z",
                    "reinforcement_count": 0,
                },
            }
        ],
    }


@pytest.fixture
def mock_expanded():
    return {
        "seed_memories": ["mem_1"],
        "expanded_memories": [
            {
                "id": "mem_1",
                "content": "Memory 1",
                "type": "text",
                "tags": [],
                "metadata": {},
                "created_at": "2026-01-21T00:00:00Z",
                "updated_at": "2026-01-21T00:00:00Z",
                "access_count": 0,
            },
            {
                "id": "mem_2",
                "content": "Memory 2",
                "type": "text",
                "tags": [],
                "metadata": {},
                "created_at": "2026-01-21T00:00:00Z",
                "updated_at": "2026-01-21T00:00:00Z",
                "access_count": 0,
            },
        ],
        "relationships": [],
        "stats": {"seed_count": 1, "expanded_count": 2, "final_count": 2},
    }


@pytest.fixture
def mock_stats():
    return {
        "node_count": 100,
        "edge_count": 250,
        "avg_degree": 2.5,
        "density": 0.05,
        "components": 3,
    }


@pytest.fixture
def mock_context():
    return {
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
        "relationships": [],
        "query": "test query",
    }


# =============================================================================
# Synchronous Tests
# =============================================================================

@respx.mock
def test_traverse_sync(mock_traversal):
    """Test graph traversal synchronously."""
    respx.post("https://api.trixdb.com/graph/traverse").mock(
        return_value=Response(200, json=mock_traversal)
    )

    with Trix(api_key="test") as client:
        result = client.graph.traverse(start_ids=["mem_1"], depth=2)

        assert len(result.nodes) == 2


@respx.mock
def test_shortest_path_sync(mock_path):
    """Test shortest path synchronously."""
    respx.post("https://api.trixdb.com/graph/shortest-path").mock(
        return_value=Response(200, json=mock_path)
    )
    
    with Trix(api_key="test") as client:
        result = client.graph.shortest_path(
            source_id="mem_1",
            target_id="mem_3",
        )
        
        assert len(result.path) == 3


@respx.mock
def test_neighbors_sync(mock_neighbors):
    """Test getting neighbors synchronously."""
    respx.get("https://api.trixdb.com/graph/neighbors/mem_1").mock(
        return_value=Response(200, json=mock_neighbors)
    )

    with Trix(api_key="test") as client:
        result = client.graph.neighbors(node_id="mem_1")

        assert len(result.neighbors) == 1


# =============================================================================
# Asynchronous Tests
# =============================================================================

@respx.mock
@pytest.mark.asyncio
async def test_traverse_async(mock_traversal):
    """Test graph traversal asynchronously."""
    respx.post("https://api.trixdb.com/graph/traverse").mock(
        return_value=Response(200, json=mock_traversal)
    )

    async with AsyncTrix(api_key="test") as client:
        result = await client.graph.traverse(start_ids=["mem_1"], depth=2)

        assert len(result.nodes) == 2


@respx.mock
@pytest.mark.asyncio
async def test_shortest_path_async(mock_path):
    """Test shortest path asynchronously."""
    respx.post("https://api.trixdb.com/graph/shortest-path").mock(
        return_value=Response(200, json=mock_path)
    )

    async with AsyncTrix(api_key="test") as client:
        result = await client.graph.shortest_path(source_id="mem_1", target_id="mem_3")

        assert len(result.path) == 3

