#!/usr/bin/env python3
"""
Relationships - Asynchronous Version

Demonstrates async relationship operations:
1. Concurrent relationship creation
2. Async relationship traversal

Run: python async_example.py
"""

import asyncio

from trix import AsyncTrix
from trix.types import RelationshipType


async def main() -> None:
    """Demonstrate async relationship operations."""

    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC RELATIONSHIPS")
        print("=" * 60)

        # ======================================================================
        # SETUP
        # ======================================================================
        print("\n1. Creating memories...")

        memories = await asyncio.gather(
            client.memories.create(content="Machine Learning basics", tags=["ml"]),
            client.memories.create(content="Deep Learning neural networks", tags=["dl"]),
            client.memories.create(content="Natural Language Processing", tags=["nlp"]),
            client.memories.create(content="Computer Vision techniques", tags=["cv"]),
        )
        print(f"   ✓ Created {len(memories)} memories")

        ml, dl, nlp, cv = memories

        # ======================================================================
        # CONCURRENT RELATIONSHIP CREATION
        # ======================================================================
        print("\n2. Creating relationships concurrently...")

        rel_tasks = [
            client.relationships.create(
                source_id=dl.id,
                target_id=ml.id,
                relationship_type=RelationshipType.RELATED_TO,
                weight=0.95,
            ),
            client.relationships.create(
                source_id=nlp.id,
                target_id=ml.id,
                relationship_type=RelationshipType.RELATED_TO,
                weight=0.9,
            ),
            client.relationships.create(
                source_id=cv.id,
                target_id=ml.id,
                relationship_type=RelationshipType.RELATED_TO,
                weight=0.9,
            ),
            client.relationships.create(
                source_id=nlp.id,
                target_id=dl.id,
                relationship_type=RelationshipType.SIMILAR_TO,
                weight=0.8,
            ),
        ]

        relationships = await asyncio.gather(*rel_tasks)
        print(f"   ✓ Created {len(relationships)} relationships concurrently")

        # ======================================================================
        # PARALLEL QUERIES
        # ======================================================================
        print("\n3. Querying relationships in parallel...")

        incoming, outgoing, related = await asyncio.gather(
            client.relationships.get_incoming(ml.id),
            client.relationships.get_outgoing(dl.id),
            client.relationships.get_related(ml.id),
        )

        print(f"   ML incoming: {len(incoming.data)}")
        print(f"   DL outgoing: {len(outgoing.data)}")
        print(f"   ML related: {len(related.related)}")

        # ======================================================================
        # CONCURRENT REINFORCEMENT
        # ======================================================================
        print("\n4. Reinforcing relationships concurrently...")

        reinforce_tasks = [
            client.relationships.reinforce(rel.id, boost=0.05) for rel in relationships[:2]
        ]

        reinforced = await asyncio.gather(*reinforce_tasks)
        print(f"   ✓ Reinforced {len(reinforced)} relationships")

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n5. Cleaning up...")

        delete_tasks = [client.relationships.delete(r.id) for r in relationships]
        await asyncio.gather(*delete_tasks)
        await client.memories.bulk_delete([m.id for m in memories])

        print("   ✓ Cleaned up")
        print("\n" + "=" * 60)
        print("🎉 Async relationships complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
