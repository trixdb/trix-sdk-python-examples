"""Tests for the Facts and Entities example.

These mock the REAL, read-mostly API surface:
  - facts.{list, list_for_memory, create_for_memory}
  - entities.{list, get, find_by_type, get_facts, merge}
  - enrichments.enrich

All paths are the live /v1 routes (knowledge facts/entities + memory-scoped
facts/enrichments).
"""

import pytest
import respx
from httpx import Response
from trix import AsyncTrix, Trix

BASE = "https://api.trixdb.com/v1"


@pytest.fixture
def mock_fact():
    return {
        "id": "fact_123",
        "subject": "Guido van Rossum",
        "predicate": "created",
        "object": "Python",
        "confidence": 1.0,
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
    }


@pytest.fixture
def mock_entity():
    return {
        "id": "ent_123",
        "name": "Guido van Rossum",
        "type": "person",
        "aliases": ["Guido", "BDFL"],
        "created_at": "2026-01-21T00:00:00Z",
        "updated_at": "2026-01-21T00:00:00Z",
    }


# =============================================================================
# Facts — synchronous
# =============================================================================


@respx.mock
def test_create_fact_for_memory(mock_fact):
    """facts.create_for_memory posts to /memories/:id/facts."""
    route = respx.post(f"{BASE}/memories/mem_123/facts").mock(
        return_value=Response(200, json=mock_fact)
    )

    with Trix(api_key="test") as client:
        fact = client.facts.create_for_memory(
            "mem_123", content="Guido created Python", importance=8
        )

    assert route.called
    assert fact.id == "fact_123"
    assert fact.predicate == "created"


@respx.mock
def test_list_facts_for_memory(mock_fact):
    """facts.list_for_memory reads /memories/:id/facts."""
    respx.get(f"{BASE}/memories/mem_123/facts").mock(
        return_value=Response(200, json={"memory_id": "mem_123", "facts": [mock_fact], "total": 1})
    )

    with Trix(api_key="test") as client:
        result = client.facts.list_for_memory("mem_123")

    assert result.memory_id == "mem_123"
    assert result.total == 1
    assert result.facts[0].subject == "Guido van Rossum"


@respx.mock
def test_list_facts_filtered(mock_fact):
    """facts.list queries /knowledge/facts with filters."""
    route = respx.get(f"{BASE}/knowledge/facts").mock(
        return_value=Response(200, json={"data": [mock_fact], "total": 1, "limit": 10, "offset": 0})
    )

    with Trix(api_key="test") as client:
        facts = client.facts.list(predicate="created", min_confidence=0.5, limit=10)

    assert route.called
    assert len(facts.data) == 1
    assert facts.data[0].object == "Python"


# =============================================================================
# Entities — synchronous
# =============================================================================


@respx.mock
def test_list_entities(mock_entity):
    """entities.list reads /knowledge/entities."""
    respx.get(f"{BASE}/knowledge/entities").mock(
        return_value=Response(
            200, json={"data": [mock_entity], "total": 1, "limit": 10, "offset": 0}
        )
    )

    with Trix(api_key="test") as client:
        entities = client.entities.list(entity_type="person")

    assert len(entities.data) == 1
    assert entities.data[0].type == "person"


@respx.mock
def test_get_entity(mock_entity):
    """entities.get reads /knowledge/entities/:id."""
    respx.get(f"{BASE}/knowledge/entities/ent_123").mock(
        return_value=Response(200, json=mock_entity)
    )

    with Trix(api_key="test") as client:
        entity = client.entities.get("ent_123")

    assert entity.name == "Guido van Rossum"
    assert "BDFL" in entity.aliases


@respx.mock
def test_get_entity_facts(mock_fact):
    """entities.get_facts reads /knowledge/entities/:id/facts."""
    respx.get(f"{BASE}/knowledge/entities/ent_123/facts").mock(
        return_value=Response(200, json={"entity_id": "ent_123", "facts": [mock_fact]})
    )

    with Trix(api_key="test") as client:
        result = client.entities.get_facts("ent_123")

    assert result.entity_id == "ent_123"
    assert len(result.facts) == 1


@respx.mock
def test_merge_entities(mock_entity):
    """entities.merge posts both ids to /knowledge/entities/merge."""
    route = respx.post(f"{BASE}/knowledge/entities/merge").mock(
        return_value=Response(200, json={"merged_entity": mock_entity, "deleted_id": "ent_456"})
    )

    with Trix(api_key="test") as client:
        result = client.entities.merge(target_id="ent_123", source_id="ent_456")

    assert route.called
    assert result.merged_entity.id == "ent_123"
    assert result.deleted_id == "ent_456"


# =============================================================================
# Enrichment — synchronous
# =============================================================================


@respx.mock
def test_trigger_enrichment():
    """enrichments.enrich posts operations to /memories/:id/enrichments."""
    route = respx.post(f"{BASE}/memories/mem_123/enrichments").mock(
        return_value=Response(
            200,
            json={"memory_id": "mem_123", "triggered": ["entities", "topics"], "status": "queued"},
        )
    )

    from trix import EnrichmentOperation

    with Trix(api_key="test") as client:
        result = client.enrichments.enrich(
            "mem_123", operations=[EnrichmentOperation.ENTITIES, EnrichmentOperation.TOPICS]
        )

    assert route.called
    assert result.status == "queued"
    assert "entities" in result.triggered


# =============================================================================
# Asynchronous
# =============================================================================


@respx.mock
@pytest.mark.asyncio
async def test_create_fact_for_memory_async(mock_fact):
    """Async facts.create_for_memory posts to /memories/:id/facts."""
    respx.post(f"{BASE}/memories/mem_123/facts").mock(return_value=Response(200, json=mock_fact))

    async with AsyncTrix(api_key="test") as client:
        fact = await client.facts.create_for_memory("mem_123", content="x", importance=5)

    assert fact.id == "fact_123"


@respx.mock
@pytest.mark.asyncio
async def test_find_entities_by_type_async(mock_entity):
    """Async entities.find_by_type filters /knowledge/entities by type."""
    respx.get(f"{BASE}/knowledge/entities").mock(
        return_value=Response(
            200, json={"data": [mock_entity], "total": 1, "limit": 5, "offset": 0}
        )
    )

    async with AsyncTrix(api_key="test") as client:
        entities = await client.entities.find_by_type("person", limit=5)

    assert len(entities.data) == 1
    assert entities.data[0].type == "person"
