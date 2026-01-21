"""Tests for Search and Retrieval example."""

import pytest
import respx
from httpx import Response

from trix import Trix, AsyncTrix


@pytest.fixture
def mock_memory():
    return {
        "id": "mem_123",
        "content": "Machine learning models predict outcomes.",
        "type": "text",
        "tags": ["sample"],
        "metadata": {},
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
        "access_count": 0,
    }


@pytest.fixture
def mock_search_results(mock_memory):
    return {
        "data": [
            {"memory": mock_memory, "score": 0.92},
            {"memory": mock_memory, "score": 0.85},
        ],
        "query": "test query",
    }


@pytest.fixture
def mock_embedding():
    return {
        "embeddings": [[0.1, 0.2, 0.3, 0.4, 0.5] * 100],  # 500 dims
        "memory_ids": ["mem_123"],
    }


@pytest.fixture
def mock_embed_all():
    return {
        "total_processed": 2,
        "batch_size": 100,
        "status": "completed",
    }


@pytest.fixture
def mock_search_config():
    return {
        "default_limit": 10,
        "max_limit": 100,
        "min_similarity_threshold": 0.5,
    }


# =============================================================================
# Synchronous Tests
# =============================================================================

@respx.mock
def test_query_search_sync(mock_memory):
    """Test semantic query search synchronously."""
    mock_list = {
        "data": [mock_memory, mock_memory],
        "total": 2,
        "limit": 5,
        "offset": 0,
    }
    respx.get("https://api.trixdb.com/memories").mock(
        return_value=Response(200, json=mock_list)
    )

    with Trix(api_key="test") as client:
        results = client.memories.list(q="machine learning", limit=5)

        assert len(results.data) == 2


@respx.mock
def test_similar_search_sync(mock_search_results):
    """Test similar memories search synchronously."""
    respx.get("https://api.trixdb.com/search/similar/mem_123").mock(
        return_value=Response(200, json=mock_search_results)
    )

    with Trix(api_key="test") as client:
        results = client.search.similar(memory_id="mem_123", limit=3)

        assert len(results.data) == 2


@respx.mock
def test_embed_sync(mock_embedding):
    """Test embedding generation synchronously."""
    respx.post("https://api.trixdb.com/search/embed").mock(
        return_value=Response(200, json=mock_embedding)
    )

    with Trix(api_key="test") as client:
        result = client.search.embed(memory_ids=["mem_123"])

        assert len(result.embeddings) == 1


@respx.mock
def test_embed_all_sync(mock_embed_all):
    """Test batch embedding synchronously."""
    respx.post("https://api.trixdb.com/search/embed-all").mock(
        return_value=Response(200, json=mock_embed_all)
    )

    with Trix(api_key="test") as client:
        result = client.search.embed_all(batch_size=100)

        assert result.total_processed == 2


# =============================================================================
# Asynchronous Tests
# =============================================================================

@respx.mock
@pytest.mark.asyncio
async def test_query_search_async(mock_memory):
    """Test semantic query search asynchronously."""
    mock_list = {
        "data": [mock_memory, mock_memory],
        "total": 2,
        "limit": 5,
        "offset": 0,
    }
    respx.get("https://api.trixdb.com/memories").mock(
        return_value=Response(200, json=mock_list)
    )

    async with AsyncTrix(api_key="test") as client:
        results = await client.memories.list(q="machine learning", limit=5)

        assert len(results.data) == 2


@respx.mock
@pytest.mark.asyncio
async def test_embed_async(mock_embedding):
    """Test embedding generation asynchronously."""
    respx.post("https://api.trixdb.com/search/embed").mock(
        return_value=Response(200, json=mock_embedding)
    )

    async with AsyncTrix(api_key="test") as client:
        result = await client.search.embed(memory_ids=["mem_123"])

        assert len(result.embeddings) == 1

