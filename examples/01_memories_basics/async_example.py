#!/usr/bin/env python3
"""
Memories Basics - Asynchronous Version

Demonstrates async memory operations including:
1. Async CRUD operations
2. Concurrent bulk operations
3. Async pagination with iter()

Run: python async_example.py
"""

import asyncio

from trix import AsyncTrix
from trix.types import MemoryCreate


async def main() -> None:
    """Demonstrate async memory operations."""

    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC MEMORY BASICS")
        print("=" * 60)

        # ======================================================================
        # CREATE - Concurrent memory creation
        # ======================================================================
        print("\n1. Creating memories concurrently...")

        create_tasks = [
            client.memories.create(
                content=f"Async memory {i}: Learning about {topic}",
                tags=["async", topic.lower()],
            )
            for i, topic in enumerate(["Python", "Async", "Concurrency"])
        ]

        memories = await asyncio.gather(*create_tasks)
        print(f"   ✓ Created {len(memories)} memories concurrently")

        # ======================================================================
        # READ - Concurrent fetch
        # ======================================================================
        print("\n2. Fetching memories concurrently...")

        fetch_tasks = [client.memories.get(m.id) for m in memories]
        fetched = await asyncio.gather(*fetch_tasks)

        for mem in fetched:
            print(f"   - {mem.content[:40]}...")

        # ======================================================================
        # UPDATE - Concurrent updates
        # ======================================================================
        print("\n3. Updating memories concurrently...")

        update_tasks = [client.memories.update(m.id, tags=m.tags + ["updated"]) for m in memories]

        updated = await asyncio.gather(*update_tasks)
        print(f"   ✓ Updated {len(updated)} memories")

        # ======================================================================
        # BULK CREATE - Async bulk operation
        # ======================================================================
        print("\n4. Async bulk create...")

        bulk_result = await client.memories.bulk_create(
            [
                MemoryCreate(content="Async bulk item 1", tags=["bulk"]),
                MemoryCreate(content="Async bulk item 2", tags=["bulk"]),
                MemoryCreate(content="Async bulk item 3", tags=["bulk"]),
            ]
        )
        print(f"   ✓ Bulk created {bulk_result.success} memories")

        # ======================================================================
        # ITER - Async pagination iterator
        # ======================================================================
        print("\n5. Async pagination...")

        count = 0
        async for mem in client.memories.iter(page_size=5, max_items=10):
            count += 1
            print(f"   {count}. {mem.content[:35]}...")
        print(f"   ✓ Iterated through {count} memories")

        # ======================================================================
        # STATS AND CONFIG - Concurrent fetch
        # ======================================================================
        print("\n6. Fetching stats and config concurrently...")

        stats, config = await asyncio.gather(
            client.memories.get_stats(), client.memories.get_config()
        )

        print(f"   Total memories: {stats.total}")
        print(f"   Max content length: {config.max_content_length}")

        # ======================================================================
        # CLEANUP - Concurrent deletion
        # ======================================================================
        print("\n7. Cleaning up...")

        all_ids = [m.id for m in memories]
        await client.memories.bulk_delete(all_ids)

        print("   ✓ All memories deleted")
        print("\n" + "=" * 60)
        print("🎉 Async memory basics complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
