#!/usr/bin/env python3
"""
Knowledge Graph - Asynchronous Version

Run: python async_example.py
"""

import asyncio
from trix import AsyncTrix


async def main() -> None:
    """Demonstrate async knowledge graph operations."""
    
    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC KNOWLEDGE GRAPH")
        print("=" * 60)
        
        # ======================================================================
        # SETUP
        # ======================================================================
        print("\n1. Creating graph nodes...")
        
        memories = await client.memories.bulk_create([
            {"content": "Python is a programming language.", "tags": ["python"]},
            {"content": "Django is a Python web framework.", "tags": ["django"]},
            {"content": "PostgreSQL is a database.", "tags": ["postgres"]},
            {"content": "Redis is an in-memory cache.", "tags": ["redis"]},
        ])
        
        python, django, postgres, redis = memories
        print(f"   ✓ Created {len(memories)} nodes")
        
        # Create edges concurrently
        print("\n2. Creating edges concurrently...")
        
        edge_tasks = [
            client.relationships.create(
                source_id=django.id, target_id=python.id,
                relationship_type="related_to", weight=0.95
            ),
            client.relationships.create(
                source_id=django.id, target_id=postgres.id,
                relationship_type="related_to", weight=0.8
            ),
            client.relationships.create(
                source_id=django.id, target_id=redis.id,
                relationship_type="related_to", weight=0.7
            ),
        ]
        
        relationships = await asyncio.gather(*edge_tasks)
        print(f"   ✓ Created {len(relationships)} edges")
        
        # ======================================================================
        # PARALLEL GRAPH QUERIES
        # ======================================================================
        print("\n3. Parallel graph queries...")
        
        traversal, neighbors, stats = await asyncio.gather(
            client.graph.traverse(start_id=django.id, max_depth=2),
            client.graph.neighbors(memory_id=django.id, direction="both"),
            client.graph.get_stats(),
        )
        
        print(f"   Traversal: {len(traversal.nodes)} nodes")
        print(f"   Neighbors: {len(neighbors.neighbors)} neighbors")
        print(f"   Graph stats: {stats.total_nodes} nodes, {stats.total_edges} edges")
        
        # ======================================================================
        # SHORTEST PATH
        # ======================================================================
        print("\n4. Finding shortest path: Python → PostgreSQL...")
        
        path = await client.graph.shortest_path(
            source_id=python.id,
            target_id=postgres.id,
            max_depth=5
        )
        
        print(f"   Path length: {len(path.path)} hops")
        
        # ======================================================================
        # EXPAND FROM MULTIPLE NODES
        # ======================================================================
        print("\n5. Expanding from multiple nodes...")
        
        expanded = await client.graph.expand(
            memory_ids=[postgres.id, redis.id],
            depth=2,
            limit=20
        )
        
        print(f"   Expanded to {len(expanded.memories)} memories")
        
        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n6. Cleaning up...")
        
        await asyncio.gather(*[client.relationships.delete(r.id) for r in relationships])
        await client.memories.bulk_delete([m.id for m in memories])
        
        print("   ✓ Cleaned up")
        print("\n" + "=" * 60)
        print("🎉 Async knowledge graph complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

