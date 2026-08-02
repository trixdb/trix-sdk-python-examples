#!/usr/bin/env python3
"""
Facts and Entities - Synchronous Version

Facts and entities in Trix are READ-MOSTLY. You do not create them
standalone — they are derived from your memories:

    1. Create a Memory (the source of truth).
    2. Optionally attach an explicit fact to it (facts.create_for_memory).
    3. Let ENRICHMENT extract entities + facts from the content.
    4. Read / query / merge the resulting knowledge.

There is no facts.create / entities.create / extract / verify on the live
API — those endpoints do not exist. This example demonstrates the real
surface: facts.{list, list_for_memory, create_for_memory} and
entities.{list, get, find_by_type, get_facts, merge}, plus enrichment.

Run: python main.py
"""

from trix import Trix
from trix.types import EnrichmentOperation, Memory


def create_source_memory(client: Trix) -> Memory:
    """Create the memory that facts and entities are derived from."""
    memory = client.memories.create(
        content="Guido van Rossum created Python in 1991. Python is used by Google and Netflix.",
        tags=["knowledge", "programming"],
    )
    print(f"   Created memory {memory.id}")
    return memory


def attach_fact(client: Trix, memory_id: str) -> None:
    """Attach an explicit fact to a memory (POST /memories/:id/facts)."""
    fact = client.facts.create_for_memory(
        memory_id,
        content="Python was created by Guido van Rossum.",
        importance=8,
        category="history",
    )
    print(f"   Attached fact {fact.id}: {fact.subject} {fact.predicate} {fact.object}")


def trigger_extraction(client: Trix, memory_id: str) -> None:
    """Ask enrichment to extract entities + facts from the memory content."""
    result = client.enrichments.enrich(
        memory_id,
        operations=[EnrichmentOperation.ENTITIES, EnrichmentOperation.TOPICS],
    )
    print(f"   Enrichment status={result.status}; triggered: {', '.join(result.triggered)}")
    print("   (entities and facts are extracted asynchronously by the server)")


def read_memory_facts(client: Trix, memory_id: str) -> None:
    """Read the facts attached to / extracted for a single memory."""
    result = client.facts.list_for_memory(memory_id)
    print(f"   Memory {result.memory_id} has {result.total} fact(s):")
    for fact in result.facts:
        print(f"      - {fact.subject} {fact.predicate} {fact.object} (conf={fact.confidence})")


def query_account_facts(client: Trix) -> None:
    """Query facts across the whole account with server-side filters."""
    facts = client.facts.list(predicate="created", min_confidence=0.5, limit=10)
    print(f"   Found {facts.total} fact(s) with predicate 'created':")
    for fact in facts.data:
        print(f"      - {fact.subject} -> {fact.object}")


def explore_entities(client: Trix) -> None:
    """List entities, read one, and read the facts about it."""
    people = client.entities.find_by_type("person", limit=5)
    print(f"   Found {people.total} person entit(y/ies)")
    if not people.data:
        return
    entity = client.entities.get(people.data[0].id)
    print(f"   Entity: {entity.name} ({entity.type}), aliases={entity.aliases}")
    entity_facts = client.entities.get_facts(entity.id)
    print(f"   {len(entity_facts.facts)} fact(s) mention {entity.name}")


def merge_duplicates(client: Trix) -> None:
    """Merge two entities of the same type to deduplicate them."""
    people = client.entities.list(entity_type="person", limit=2)
    if len(people.data) < 2:
        print("   Need 2+ entities to merge; skipping")
        return
    target, source = people.data[0], people.data[1]
    merged = client.entities.merge(target_id=target.id, source_id=source.id)
    print(f"   Merged {merged.deleted_id} into {merged.merged_entity.id}")


def main() -> None:
    """Demonstrate the read-mostly facts and entities workflow."""
    with Trix.from_env() as client:
        print("=" * 60)
        print("FACTS AND ENTITIES (read-mostly, memory-derived)")
        print("=" * 60)

        print("\n1. Creating a source memory...")
        memory = create_source_memory(client)

        print("\n2. Attaching an explicit fact to the memory...")
        attach_fact(client, memory.id)

        print("\n3. Triggering entity/fact extraction (enrichment)...")
        trigger_extraction(client, memory.id)

        print("\n4. Reading facts for the memory...")
        read_memory_facts(client, memory.id)

        print("\n5. Querying account-wide facts...")
        query_account_facts(client)

        print("\n6. Exploring extracted entities...")
        explore_entities(client)

        print("\n7. Merging duplicate entities...")
        merge_duplicates(client)

        print("\n8. Cleaning up...")
        client.memories.delete(memory.id)
        print("   Deleted source memory")

        print("\n" + "=" * 60)
        print("Facts and entities complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
