#!/usr/bin/env python3
"""
Clustering - Asynchronous Version

Run: python async_example.py
"""

import asyncio
from trix import AsyncTrix


async def main() -> None:
    """Demonstrate async clustering operations."""

    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC CLUSTERING")
        print("=" * 60)

        # ======================================================================
        # SETUP
        # ======================================================================
        print("\n1. Creating memories...")

        memories = await asyncio.gather(
            client.memories.create(
                content="Machine learning models need training data.", tags=["ml"]
            ),
            client.memories.create(
                content="Neural networks have multiple layers.", tags=["ml"]
            ),
            client.memories.create(
                content="Deep learning is a subset of ML.", tags=["ml"]
            ),
            client.memories.create(
                content="Docker containers isolate applications.", tags=["devops"]
            ),
            client.memories.create(
                content="Kubernetes orchestrates containers.", tags=["devops"]
            ),
        )

        print(f"   Created {len(memories)} memories")

        # ======================================================================
        # CREATE CLUSTERS CONCURRENTLY
        # ======================================================================
        print("\n2. Creating clusters concurrently...")

        cluster_tasks = [
            client.clusters.create(name="Machine Learning", description="ML topics"),
            client.clusters.create(name="DevOps", description="DevOps topics"),
        ]

        ml_cluster, devops_cluster = await asyncio.gather(*cluster_tasks)
        print(f"   Created 2 clusters concurrently")

        # ======================================================================
        # ADD MEMORIES CONCURRENTLY
        # ======================================================================
        print("\n3. Adding memories to clusters...")

        add_tasks = [
            # ML memories to ML cluster
            *[client.clusters.add_memory(ml_cluster.id, m.id) for m in memories[:3]],
            # DevOps memories to DevOps cluster
            *[client.clusters.add_memory(devops_cluster.id, m.id) for m in memories[3:]],
        ]

        await asyncio.gather(*add_tasks)
        print(f"   Added all memories to clusters")

        # ======================================================================
        # PARALLEL CLUSTER QUERIES
        # ======================================================================
        print("\n4. Parallel cluster queries...")

        ml_details, devops_details, all_clusters = await asyncio.gather(
            client.clusters.get(ml_cluster.id),
            client.clusters.get(devops_cluster.id),
            client.clusters.list(),
        )

        print(f"   ML cluster: {ml_details.memory_count} memories")
        print(f"   DevOps cluster: {devops_details.memory_count} memories")
        print(f"   Total clusters: {len(all_clusters.data)}")

        # ======================================================================
        # PARALLEL EXPANSION
        # ======================================================================
        print("\n5. Expanding both clusters in parallel...")

        ml_expand, devops_expand = await asyncio.gather(
            client.clusters.expand(ml_cluster.id, limit=3),
            client.clusters.expand(devops_cluster.id, limit=3),
        )

        print(f"   ML expansion suggestions: {len(ml_expand)}")
        print(f"   DevOps expansion suggestions: {len(devops_expand)}")

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n6. Cleaning up...")

        await asyncio.gather(
            client.clusters.delete(ml_cluster.id),
            client.clusters.delete(devops_cluster.id),
        )
        await client.memories.bulk_delete([m.id for m in memories])

        print("   Cleaned up")
        print("\n" + "=" * 60)
        print("Async clustering complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
