"""Tests for Clustering example."""

import pytest
import respx
from httpx import Response

from trix import Trix, AsyncTrix


@pytest.fixture
def mock_cluster():
    return {
        "id": "cluster_123",
        "name": "Python Cluster",
        "description": "Python memories",
        "memory_count": 5,
        "metadata": {"topic": "programming"},
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
    }


@pytest.fixture
def mock_cluster_list(mock_cluster):
    return {
        "data": [mock_cluster],
        "cursor": None,
    }


@pytest.fixture
def mock_memory_list():
    return {
        "data": [
            {"id": "mem_1", "content": "Memory 1", "tags": [], "metadata": {}},
            {"id": "mem_2", "content": "Memory 2", "tags": [], "metadata": {}},
        ],
        "total": 2,
        "limit": 10,
        "offset": 0,
    }


@pytest.fixture
def mock_incremental_result():
    return {
        "job_id": "job_123",
        "status": "completed",
        "estimated_memories": 5,
    }


@pytest.fixture
def mock_expansion():
    return {
        "suggestions": [
            {"id": "mem_3", "content": "Similar memory", "score": 0.85},
        ],
    }


# =============================================================================
# Synchronous Tests
# =============================================================================

@respx.mock
def test_create_cluster_sync(mock_cluster):
    """Test creating a cluster synchronously."""
    respx.post("https://api.trixdb.com/clusters").mock(
        return_value=Response(200, json=mock_cluster)
    )
    
    with Trix(api_key="test") as client:
        cluster = client.clusters.create(
            name="Python Cluster",
            description="Python memories",
        )
        
        assert cluster.id == "cluster_123"
        assert cluster.name == "Python Cluster"


@respx.mock
def test_get_cluster_sync(mock_cluster):
    """Test getting a cluster synchronously."""
    respx.get("https://api.trixdb.com/clusters/cluster_123").mock(
        return_value=Response(200, json=mock_cluster)
    )
    
    with Trix(api_key="test") as client:
        cluster = client.clusters.get("cluster_123")
        
        assert cluster.memory_count == 5


@respx.mock
def test_list_clusters_sync(mock_cluster_list):
    """Test listing clusters synchronously."""
    respx.get("https://api.trixdb.com/clusters").mock(
        return_value=Response(200, json=mock_cluster_list)
    )
    
    with Trix(api_key="test") as client:
        clusters = client.clusters.list()
        
        assert len(clusters.data) == 1


@pytest.fixture
def mock_membership():
    return {
        "cluster_id": "cluster_123",
        "memory_id": "mem_1",
        "confidence": 1.0,
        "added_at": "2026-01-21T00:00:00Z",
    }


@respx.mock
def test_add_memory_to_cluster_sync(mock_membership):
    """Test adding memory to cluster synchronously."""
    respx.post("https://api.trixdb.com/clusters/cluster_123/memories/mem_1").mock(
        return_value=Response(200, json=mock_membership)
    )

    with Trix(api_key="test") as client:
        result = client.clusters.add_memory("cluster_123", "mem_1")
        assert result.cluster_id == "cluster_123"


@respx.mock
def test_expand_cluster_sync(mock_expansion):
    """Test cluster expansion synchronously."""
    respx.post("https://api.trixdb.com/clusters/cluster_123/expand").mock(
        return_value=Response(200, json=mock_expansion)
    )

    with Trix(api_key="test") as client:
        result = client.clusters.expand("cluster_123", limit=5)

        assert len(result) == 1


# =============================================================================
# Asynchronous Tests
# =============================================================================

@respx.mock
@pytest.mark.asyncio
async def test_create_cluster_async(mock_cluster):
    """Test creating a cluster asynchronously."""
    respx.post("https://api.trixdb.com/clusters").mock(
        return_value=Response(200, json=mock_cluster)
    )
    
    async with AsyncTrix(api_key="test") as client:
        cluster = await client.clusters.create(name="Python Cluster")
        
        assert cluster.id == "cluster_123"


@respx.mock
@pytest.mark.asyncio
async def test_list_clusters_async(mock_cluster_list):
    """Test listing clusters asynchronously."""
    respx.get("https://api.trixdb.com/clusters").mock(
        return_value=Response(200, json=mock_cluster_list)
    )
    
    async with AsyncTrix(api_key="test") as client:
        clusters = await client.clusters.list()
        
        assert len(clusters.data) == 1

