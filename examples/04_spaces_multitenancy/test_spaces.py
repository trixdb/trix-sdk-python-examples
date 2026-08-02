"""Tests for Spaces and Multi-tenancy example."""

import pytest
import respx
from httpx import Response
from trix import AsyncTrix, Trix


@pytest.fixture
def mock_space():
    return {
        "id": "space_123",
        "name": "Tenant A",
        "slug": "tenant-a",
        "description": "Test space",
        "metadata": {"plan": "enterprise"},
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
    }


@pytest.fixture
def mock_space_list(mock_space):
    return {
        "data": [mock_space],
    }


# =============================================================================
# Synchronous Tests
# =============================================================================


@respx.mock
def test_create_space_sync(mock_space):
    """Test creating a space synchronously."""
    respx.post("https://api.trixdb.com/v1/spaces").mock(return_value=Response(200, json=mock_space))

    with Trix(api_key="test") as client:
        space = client.spaces.create(
            name="Tenant A",
            description="Test space",
        )

        assert space.id == "space_123"
        assert space.slug == "tenant-a"


@respx.mock
def test_get_space_sync(mock_space):
    """Test getting a space by ID synchronously."""
    respx.get("https://api.trixdb.com/v1/spaces/space_123").mock(
        return_value=Response(200, json=mock_space)
    )

    with Trix(api_key="test") as client:
        space = client.spaces.get("space_123")

        assert space.name == "Tenant A"


@respx.mock
def test_list_spaces_sync(mock_space_list):
    """Test listing spaces synchronously."""
    respx.get("https://api.trixdb.com/v1/spaces").mock(
        return_value=Response(200, json=mock_space_list)
    )

    with Trix(api_key="test") as client:
        spaces = client.spaces.list()

        assert len(spaces.data) == 1


@respx.mock
def test_update_space_sync(mock_space):
    """Test updating a space synchronously."""
    updated = {**mock_space, "description": "Updated description"}
    respx.patch("https://api.trixdb.com/v1/spaces/space_123").mock(
        return_value=Response(200, json=updated)
    )

    with Trix(api_key="test") as client:
        space = client.spaces.update("space_123", description="Updated description")

        assert space.description == "Updated description"


# =============================================================================
# Asynchronous Tests
# =============================================================================


@respx.mock
@pytest.mark.asyncio
async def test_create_space_async(mock_space):
    """Test creating a space asynchronously."""
    respx.post("https://api.trixdb.com/v1/spaces").mock(return_value=Response(200, json=mock_space))

    async with AsyncTrix(api_key="test") as client:
        space = await client.spaces.create(
            name="Tenant A",
            description="Test space",
        )

        assert space.id == "space_123"


@respx.mock
@pytest.mark.asyncio
async def test_list_spaces_async(mock_space_list):
    """Test listing spaces asynchronously."""
    respx.get("https://api.trixdb.com/v1/spaces").mock(
        return_value=Response(200, json=mock_space_list)
    )

    async with AsyncTrix(api_key="test") as client:
        spaces = await client.spaces.list()

        assert len(spaces.data) == 1
