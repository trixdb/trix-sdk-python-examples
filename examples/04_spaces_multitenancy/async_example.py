#!/usr/bin/env python3
"""
Spaces and Multi-tenancy - Asynchronous Version

Run: python async_example.py
"""

import asyncio
from trix import AsyncTrix


async def main() -> None:
    """Demonstrate async space management."""
    
    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC SPACES AND MULTI-TENANCY")
        print("=" * 60)
        
        # ======================================================================
        # CREATE SPACES CONCURRENTLY
        # ======================================================================
        print("\n1. Creating spaces concurrently...")
        
        space_tasks = [
            client.spaces.create(
                name=f"Async Tenant {i}",
                slug=f"async-tenant-{i}",
                description=f"Async space {i}",
            )
            for i in range(3)
        ]
        
        spaces = await asyncio.gather(*space_tasks)
        print(f"   ✓ Created {len(spaces)} spaces concurrently")
        
        # ======================================================================
        # CREATE MEMORIES IN SPACES CONCURRENTLY
        # ======================================================================
        print("\n2. Creating space-isolated memories...")
        
        mem_tasks = [
            client.memories.create(
                content=f"Data for {space.name}",
                space_id=space.id,
                tags=["async", space.slug],
            )
            for space in spaces
        ]
        
        memories = await asyncio.gather(*mem_tasks)
        print(f"   ✓ Created {len(memories)} memories in different spaces")
        
        # ======================================================================
        # PARALLEL SPACE-SCOPED SEARCHES
        # ======================================================================
        print("\n3. Parallel space-scoped searches...")
        
        search_tasks = [
            client.search.query(query="data", space_id=space.id, limit=5)
            for space in spaces
        ]
        
        search_results = await asyncio.gather(*search_tasks)
        
        for space, results in zip(spaces, search_results):
            print(f"   {space.name}: {len(results.results)} results")
        
        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n4. Cleaning up...")
        
        # Delete memories
        await asyncio.gather(*[client.memories.delete(m.id) for m in memories])
        
        # Delete spaces
        await asyncio.gather(*[client.spaces.delete(s.id) for s in spaces])
        
        print("   ✓ Cleaned up")
        print("\n" + "=" * 60)
        print("🎉 Async spaces complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

