#!/usr/bin/env python3
"""
Testing and Mock Patterns

Patterns for testing code that uses the Trix SDK.
"""

import pytest
import respx
from httpx import Response

from trix import Trix, AsyncTrix


# =============================================================================
# 1. Basic Mocking with respx
# =============================================================================

@respx.mock
def test_create_memory():
    """Mock a simple API call."""
    # Set up mock
    respx.post("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(201, json={
            "id": "mem_123",
            "content": "Test content",
            "tags": [],
            "metadata": {},
            "created_at": "2024-01-01T00:00:00Z"
        })
    )
    
    # Test
    with Trix(api_key="test-key") as client:
        memory = client.memories.create(content="Test content")
        assert memory.id == "mem_123"


# =============================================================================
# 2. Mocking Multiple Endpoints
# =============================================================================

@respx.mock
def test_search_workflow():
    """Mock multiple API calls in a workflow."""
    # Mock memory creation
    respx.post("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(201, json={
            "id": "mem_123",
            "content": "Python programming",
            "tags": ["python"],
            "metadata": {},
            "created_at": "2024-01-01T00:00:00Z"
        })
    )
    
    # Mock search
    respx.get("https://api.trixdb.com/v1/search").mock(
        return_value=Response(200, json={
            "data": [{
                "memory": {
                    "id": "mem_123",
                    "content": "Python programming",
                    "tags": ["python"],
                    "metadata": {},
                    "created_at": "2024-01-01T00:00:00Z"
                },
                "score": 0.95
            }],
            "query": "Python"
        })
    )
    
    with Trix(api_key="test-key") as client:
        # Create
        memory = client.memories.create(content="Python programming", tags=["python"])
        
        # Search
        results = client.search.query(query="Python")
        
        assert len(results.data) == 1
        assert results.data[0].score == 0.95


# =============================================================================
# 3. Async Mocking
# =============================================================================

@pytest.mark.asyncio
@respx.mock
async def test_async_operations():
    """Mock async API calls."""
    respx.get("https://api.trixdb.com/v1/memories/mem_123").mock(
        return_value=Response(200, json={
            "id": "mem_123",
            "content": "Test",
            "tags": [],
            "metadata": {},
            "created_at": "2024-01-01T00:00:00Z"
        })
    )
    
    async with AsyncTrix(api_key="test-key") as client:
        memory = await client.memories.get("mem_123")
        assert memory.id == "mem_123"


# =============================================================================
# 4. Mocking Errors
# =============================================================================

@respx.mock
def test_not_found_error():
    """Mock error responses."""
    respx.get("https://api.trixdb.com/v1/memories/nonexistent").mock(
        return_value=Response(404, json={
            "error": {"code": "not_found", "message": "Memory not found"}
        })
    )
    
    with Trix(api_key="test-key") as client:
        from trix.exceptions import NotFoundError
        
        with pytest.raises(NotFoundError):
            client.memories.get("nonexistent")


@respx.mock
def test_rate_limit_error():
    """Mock rate limit responses."""
    respx.post("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(429, json={
            "error": {"code": "rate_limited", "message": "Too many requests"}
        }, headers={"Retry-After": "60"})
    )
    
    with Trix(api_key="test-key") as client:
        from trix.exceptions import RateLimitError
        
        with pytest.raises(RateLimitError):
            client.memories.create(content="Test")


# =============================================================================
# 5. Mocking Pagination
# =============================================================================

@respx.mock
def test_pagination():
    """Mock paginated responses."""
    # First page
    respx.get("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(200, json={
            "data": [
                {"id": "mem_1", "content": "First", "tags": [], "metadata": {}, "created_at": "2024-01-01T00:00:00Z"},
                {"id": "mem_2", "content": "Second", "tags": [], "metadata": {}, "created_at": "2024-01-01T00:00:00Z"},
            ],
            "total": 3,
            "limit": 2,
            "offset": 0,
        })
    )

    with Trix(api_key="test-key") as client:
        result = client.memories.list(limit=2)
        assert len(result.data) == 2
        assert result.total == 3


# =============================================================================
# 6. Fixtures for Reusable Mocks
# =============================================================================

@pytest.fixture
def mock_trix_api():
    """Reusable fixture for common mocks."""
    with respx.mock:
        # Set up common mocks
        respx.post("https://api.trixdb.com/v1/memories").mock(
            return_value=Response(201, json={
                "id": "mem_fixture",
                "content": "Fixture content",
                "tags": [],
                "metadata": {},
                "created_at": "2024-01-01T00:00:00Z"
            })
        )
        yield


def test_with_fixture(mock_trix_api):
    """Use the fixture."""
    with Trix(api_key="test-key") as client:
        memory = client.memories.create(content="Test")
        assert memory.id == "mem_fixture"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

