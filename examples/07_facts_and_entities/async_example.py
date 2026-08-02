#!/usr/bin/env python3
"""
Facts and Entities - Asynchronous Version

Run: python async_example.py
"""

import asyncio

from trix import AsyncTrix


async def main() -> None:
    """Demonstrate async facts and entities operations."""

    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC FACTS AND ENTITIES")
        print("=" * 60)

        # ======================================================================
        # CREATE ENTITIES CONCURRENTLY
        # ======================================================================
        print("\n1. Creating entities concurrently...")

        entity_tasks = [
            client.entities.create(
                name="JavaScript",
                entity_type="programming_language",
                properties={"paradigm": "multi-paradigm"},
            ),
            client.entities.create(
                name="Brendan Eich",
                entity_type="person",
                properties={"role": "Creator of JavaScript"},
            ),
            client.entities.create(
                name="Netscape",
                entity_type="organization",
            ),
        ]

        js, brendan, netscape = await asyncio.gather(*entity_tasks)
        print(f"   ✓ Created {3} entities concurrently")

        # ======================================================================
        # CREATE FACTS CONCURRENTLY
        # ======================================================================
        print("\n2. Creating facts concurrently...")

        fact_tasks = [
            client.facts.create(
                subject=brendan.id,
                predicate="created",
                obj=js.id,
                confidence=1.0,
            ),
            client.facts.create(
                subject=brendan.id,
                predicate="worked_at",
                obj=netscape.id,
            ),
            client.facts.create(
                subject=js.id,
                predicate="developed_at",
                obj=netscape.id,
            ),
        ]

        facts = await asyncio.gather(*fact_tasks)
        print(f"   ✓ Created {len(facts)} facts concurrently")

        # ======================================================================
        # CREATE A MEMORY AND EXTRACT IN PARALLEL
        # ======================================================================
        print("\n3. Creating memory and parallel extraction...")

        text = "Brendan Eich created JavaScript at Netscape in 1995."

        # First create a memory to extract from
        extraction_memory = await client.memories.create(
            content=text, metadata={"type": "extraction_demo"}
        )

        # Now extract entities and facts in parallel
        entity_extract, fact_extract = await asyncio.gather(
            client.entities.extract(memory_id=extraction_memory.id, save=False),
            client.facts.extract(memory_id=extraction_memory.id, save=False),
        )

        print(f"   Entities: {len(entity_extract.entities)}")
        print(f"   Facts: {len(fact_extract.facts)}")

        # ======================================================================
        # PARALLEL QUERIES
        # ======================================================================
        print("\n4. Parallel queries...")

        js_facts, created_facts, search_results = await asyncio.gather(
            client.facts.list(subject=js.id),
            client.facts.list(predicate="created"),
            client.entities.search(query="programming"),
        )

        print(f"   JS facts: {len(js_facts.data)}")
        print(f"   'created' facts: {len(created_facts.data)}")
        print(f"   Search results: {len(search_results.entities)}")

        # ======================================================================
        # VERIFY FACT
        # ======================================================================
        print("\n5. Verifying fact...")

        # Verify the first fact we created
        verification = await client.facts.verify(fact_id=facts[0].id)
        print(f"   Verified: {verification.is_verified}")

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n6. Cleaning up...")

        await asyncio.gather(*[client.facts.delete(f.id) for f in facts])
        await client.memories.delete(extraction_memory.id)
        await asyncio.gather(
            *[
                client.entities.delete(js.id),
                client.entities.delete(brendan.id),
                client.entities.delete(netscape.id),
            ]
        )

        print("   ✓ Cleaned up")
        print("\n" + "=" * 60)
        print("🎉 Async facts and entities complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
