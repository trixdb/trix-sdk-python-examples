"""Tests for Facts and Entities example."""

import pytest
import respx
from httpx import Response

from trix import Trix, AsyncTrix


@pytest.fixture
def mock_entity():
    return {
        "id": "ent_123",
        "name": "Python",
        "type": "programming_language",
        "properties": {"paradigm": "multi-paradigm"},
        "aliases": ["Py"],
        "description": None,
        "mention_count": 1,
        "memory_ids": [],
        "metadata": {},
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
    }


@pytest.fixture
def mock_fact():
    return {
        "id": "fact_123",
        "subject": "ent_1",
        "predicate": "created",
        "object": "ent_2",
        "confidence": 1.0,
        "subject_type": "entity",
        "object_type": "entity",
        "source": None,
        "valid_from": None,
        "valid_to": None,
        "metadata": {},
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
    }


@pytest.fixture
def mock_fact_list(mock_fact):
    return {
        "data": [mock_fact],
        "total": 1,
        "limit": 10,
        "offset": 0,
    }


@pytest.fixture
def mock_entity_list(mock_entity):
    return {
        "data": [mock_entity],
        "total": 1,
        "limit": 10,
        "offset": 0,
    }


@pytest.fixture
def mock_entity_search(mock_entity):
    return {
        "data": [{**mock_entity, "score": 0.95}],
        "total": 1,
    }


# =============================================================================
# Synchronous Tests
# =============================================================================

@respx.mock
def test_create_entity_sync(mock_entity):
    """Test creating an entity synchronously."""
    respx.post("https://api.trixdb.com/v1/entities").mock(
        return_value=Response(200, json=mock_entity)
    )
    
    with Trix(api_key="test") as client:
        entity = client.entities.create(
            name="Python",
            entity_type="programming_language",
        )
        
        assert entity.id == "ent_123"
        assert entity.name == "Python"


@respx.mock
def test_create_fact_sync(mock_fact):
    """Test creating a fact synchronously."""
    respx.post("https://api.trixdb.com/v1/facts").mock(
        return_value=Response(200, json=mock_fact)
    )

    with Trix(api_key="test") as client:
        fact = client.facts.create(
            subject="ent_1",
            predicate="created",
            obj="ent_2",
        )

        assert fact.id == "fact_123"


@respx.mock
def test_list_facts_sync(mock_fact_list):
    """Test listing facts synchronously."""
    respx.get("https://api.trixdb.com/v1/facts").mock(
        return_value=Response(200, json=mock_fact_list)
    )

    with Trix(api_key="test") as client:
        facts = client.facts.list(subject="ent_1")

        assert len(facts.data) == 1


@respx.mock
def test_list_entities_sync(mock_entity_list):
    """Test listing entities synchronously."""
    respx.get("https://api.trixdb.com/v1/entities").mock(
        return_value=Response(200, json=mock_entity_list)
    )

    with Trix(api_key="test") as client:
        entities = client.entities.list()

        assert len(entities.data) == 1


# =============================================================================
# Asynchronous Tests
# =============================================================================

@respx.mock
@pytest.mark.asyncio
async def test_create_entity_async(mock_entity):
    """Test creating an entity asynchronously."""
    respx.post("https://api.trixdb.com/v1/entities").mock(
        return_value=Response(200, json=mock_entity)
    )
    
    async with AsyncTrix(api_key="test") as client:
        entity = await client.entities.create(
            name="Python",
            entity_type="programming_language",
        )
        
        assert entity.id == "ent_123"


@respx.mock
@pytest.mark.asyncio
async def test_search_entities_async(mock_entity_search):
    """Test searching entities asynchronously."""
    respx.post("https://api.trixdb.com/v1/entities/search").mock(
        return_value=Response(200, json=mock_entity_search)
    )

    async with AsyncTrix(api_key="test") as client:
        result = await client.entities.search(query="programming")

        assert len(result.data) == 1

