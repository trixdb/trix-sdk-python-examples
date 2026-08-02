#!/usr/bin/env python3
"""
Facts and Entities - Asynchronous Version

Same read-mostly workflow as main.py (create memory -> attach fact ->
enrich -> read/query/merge), but using AsyncTrix so the independent reads
run concurrently with asyncio.gather.

Run: python async_example.py
"""

import asyncio

from trix import AsyncTrix
from trix.types import EnrichmentOperation


async def read_knowledge(client: AsyncTrix, memory_id: str) -> None:
    """Fetch memory facts, account facts, and person entities concurrently."""
    memory_facts, created_facts, people = await asyncio.gather(
        client.facts.list_for_memory(memory_id),
        client.facts.list(predicate="created", limit=10),
        client.entities.find_by_type("person", limit=5),
    )
    print(f"   Memory facts: {memory_facts.total}")
    print(f"   Account 'created' facts: {created_facts.total}")
    print(f"   Person entities: {people.total}")

    if people.data:
        entity = people.data[0]
        entity_facts = await client.entities.get_facts(entity.id)
        print(f"   {len(entity_facts.facts)} fact(s) mention {entity.name}")


async def main() -> None:
    """Demonstrate the async facts and entities workflow."""
    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC FACTS AND ENTITIES")
        print("=" * 60)

        print("\n1. Creating a source memory...")
        memory = await client.memories.create(
            content="Brendan Eich created JavaScript at Netscape in 1995.",
            tags=["knowledge", "programming"],
        )
        print(f"   Created memory {memory.id}")

        print("\n2. Attaching an explicit fact...")
        fact = await client.facts.create_for_memory(
            memory.id,
            content="Brendan Eich created JavaScript.",
            importance=8,
        )
        print(f"   Attached fact {fact.id}")

        print("\n3. Triggering extraction (enrichment)...")
        result = await client.enrichments.enrich(
            memory.id,
            operations=[EnrichmentOperation.ENTITIES, EnrichmentOperation.TOPICS],
        )
        print(f"   Enrichment status={result.status}")

        print("\n4. Reading knowledge concurrently...")
        await read_knowledge(client, memory.id)

        print("\n5. Cleaning up...")
        await client.memories.delete(memory.id)
        print("   Deleted source memory")

        print("\n" + "=" * 60)
        print("Async facts and entities complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
