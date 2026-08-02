#!/usr/bin/env python3
"""
Clustering - Synchronous Version

This example demonstrates automatic memory organization:
1. Creating and managing clusters
2. Adding memories to clusters
3. Cluster expansion
4. Cluster quality and topics

Run: python main.py
"""

from trix import Trix


def main() -> None:
    """Demonstrate clustering operations."""

    with Trix.from_env() as client:
        print("=" * 60)
        print("CLUSTERING")
        print("=" * 60)

        # ======================================================================
        # SETUP - Create memories to cluster
        # ======================================================================
        print("\n1. Creating memories to cluster...")

        mem_data = [
            # Programming topic
            ("Python list comprehensions are powerful.", ["python"]),
            ("Python dictionaries use hash tables.", ["python"]),
            ("Python supports multiple inheritance.", ["python"]),
            # Database topic
            ("PostgreSQL supports JSONB columns.", ["database"]),
            ("SQL indexes improve query performance.", ["database"]),
            ("Database normalization reduces redundancy.", ["database"]),
            # Web topic
            ("REST APIs use HTTP methods.", ["web"]),
            ("GraphQL provides flexible queries.", ["web"]),
        ]

        memories = [client.memories.create(content=c, tags=t) for c, t in mem_data]

        print(f"   Created {len(memories)} memories")

        # ======================================================================
        # CREATE CLUSTER MANUALLY
        # ======================================================================
        print("\n2. Creating a manual cluster...")

        python_cluster = client.clusters.create(
            name="Python Programming",
            description="Cluster for Python-related memories",
            metadata={"topic": "programming", "language": "python"},
        )

        print(f"   Created cluster: {python_cluster.name} ({python_cluster.id})")

        # ======================================================================
        # ADD MEMORIES TO CLUSTER
        # ======================================================================
        print("\n3. Adding memories to cluster...")

        # Add first 3 memories (Python-related)
        for mem in memories[:3]:
            client.clusters.add_memory(cluster_id=python_cluster.id, memory_id=mem.id)

        print("   Added 3 memories to Python cluster")

        # ======================================================================
        # GET CLUSTER (with memories)
        # ======================================================================
        print("\n4. Getting cluster details...")

        cluster = client.clusters.get(python_cluster.id, include_memories=True)
        print(f"   Name: {cluster.name}")
        print(f"   Memory count: {cluster.memory_count}")
        print(f"   Metadata: {cluster.metadata}")

        # ======================================================================
        # LIST CLUSTERS
        # ======================================================================
        print("\n5. Listing all clusters...")

        clusters = client.clusters.list(limit=10)
        print(f"   Found {len(clusters.data)} clusters:")
        for c in clusters.data:
            print(f"      - {c.name}: {c.memory_count} memories")

        # ======================================================================
        # EXPAND CLUSTER
        # ======================================================================
        print("\n6. Expanding cluster (finding similar memories)...")

        suggestions = client.clusters.expand(cluster_id=python_cluster.id, limit=5, threshold=0.6)

        print(f"   Found {len(suggestions)} candidate memories")

        # ======================================================================
        # UPDATE CLUSTER
        # ======================================================================
        print("\n7. Updating cluster...")

        updated = client.clusters.update(
            python_cluster.id, name="Python Programming Concepts", description="Updated description"
        )
        print(f"   Updated cluster name to: {updated.name}")

        # ======================================================================
        # REMOVE MEMORY FROM CLUSTER
        # ======================================================================
        print("\n8. Removing memory from cluster...")

        client.clusters.remove_memory(cluster_id=python_cluster.id, memory_id=memories[0].id)
        print("   Removed one memory from cluster")

        # Verify count
        updated_cluster = client.clusters.get(python_cluster.id)
        print(f"   New memory count: {updated_cluster.memory_count}")

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n9. Cleaning up...")

        # Delete clusters first
        for c in client.clusters.list().data:
            client.clusters.delete(c.id)

        # Then delete memories
        client.memories.bulk_delete([m.id for m in memories])

        print("   Cleaned up")
        print("\n" + "=" * 60)
        print("Clustering complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
