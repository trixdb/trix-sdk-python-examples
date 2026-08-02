"""Tests for Advanced Patterns example."""

import pytest
import respx
from httpx import Response

from trix import Trix, AsyncTrix
from trix.exceptions import (
    NotFoundError,
    ValidationError,
    RateLimitError,
    AuthenticationError,
)


# =============================================================================
# Error Handling Tests
# =============================================================================

@respx.mock
def test_not_found_error():
    """Test NotFoundError is raised correctly."""
    respx.get("https://api.trixdb.com/v1/memories/nonexistent").mock(
        return_value=Response(404, json={
            "error": {"message": "Memory not found", "code": "not_found"}
        })
    )
    
    with pytest.raises(NotFoundError) as exc_info:
        with Trix(api_key="test") as client:
            client.memories.get("nonexistent")
    
    assert exc_info.value.status_code == 404


@respx.mock
def test_validation_error():
    """Test ValidationError is raised correctly."""
    respx.post("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(422, json={
            "error": {
                "message": "Validation failed",
                "code": "validation_error",
                "errors": {"content": "Content is required"}
            }
        })
    )

    with pytest.raises(ValidationError) as exc_info:
        with Trix(api_key="test") as client:
            client.memories.create(content="")

    assert exc_info.value.status_code == 422


@respx.mock
def test_rate_limit_error():
    """Test RateLimitError is raised correctly."""
    respx.get("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(
            429,
            json={"error": {"message": "Rate limit exceeded"}},
            headers={"Retry-After": "5"}
        )
    )
    
    with pytest.raises(RateLimitError) as exc_info:
        with Trix(api_key="test") as client:
            client.memories.list()
    
    assert exc_info.value.status_code == 429
    assert exc_info.value.retry_after == 5


@respx.mock
def test_authentication_error():
    """Test AuthenticationError is raised correctly."""
    respx.get("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(401, json={
            "error": {"message": "Invalid API key"}
        })
    )
    
    with pytest.raises(AuthenticationError) as exc_info:
        with Trix(api_key="invalid") as client:
            client.memories.list()
    
    assert exc_info.value.status_code == 401


# =============================================================================
# Pagination Tests
# =============================================================================

@respx.mock
def test_manual_pagination():
    """Test manual pagination handling."""
    # First page
    respx.get("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(200, json={
            "data": [{
                "id": "mem_1",
                "content": "Memory 1",
                "type": "text",
                "tags": [],
                "metadata": {},
                "created_at": "2026-01-21T00:00:00Z",
                "updated_at": "2026-01-21T00:00:00Z",
                "access_count": 0,
            }],
            "total": 2,
            "limit": 1,
            "offset": 0,
        })
    )

    with Trix(api_key="test") as client:
        result = client.memories.list(limit=1)

        assert len(result.data) == 1
        assert result.total == 2
        assert result.limit == 1


# =============================================================================
# Async Tests
# =============================================================================

@respx.mock
@pytest.mark.asyncio
async def test_async_not_found_error():
    """Test NotFoundError in async context."""
    respx.get("https://api.trixdb.com/v1/memories/nonexistent").mock(
        return_value=Response(404, json={
            "error": {"message": "Memory not found"}
        })
    )
    
    with pytest.raises(NotFoundError):
        async with AsyncTrix(api_key="test") as client:
            await client.memories.get("nonexistent")


@respx.mock
@pytest.mark.asyncio
async def test_async_pagination():
    """Test async pagination."""
    respx.get("https://api.trixdb.com/v1/memories").mock(
        return_value=Response(200, json={
            "data": [{
                "id": "mem_1",
                "content": "Memory",
                "type": "text",
                "tags": [],
                "metadata": {},
                "created_at": "2026-01-21T00:00:00Z",
                "updated_at": "2026-01-21T00:00:00Z",
                "access_count": 0,
            }],
            "total": 1,
            "limit": 10,
            "offset": 0,
        })
    )

    async with AsyncTrix(api_key="test") as client:
        result = await client.memories.list(limit=10)

        assert len(result.data) == 1
        assert result.total == 1

