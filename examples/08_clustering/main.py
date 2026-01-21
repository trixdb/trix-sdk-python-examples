#!/usr/bin/env python3
"""
Clustering - Synchronous Version

This example demonstrates automatic memory organization:
1. Creating and managing clusters
2. Adding memories to clusters
3. Automatic clustering
4. Incremental clustering
5. Cluster expansion

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
        
        memories = client.memories.bulk_create([
            # Programming topic
            {"content": "Python list comprehensions are powerful.", "tags": ["python"]},
            {"content": "Python dictionaries use hash tables.", "tags": ["python"]},
            {"content": "Python supports multiple inheritance.", "tags": ["python"]},
            # Database topic
            {"content": "PostgreSQL supports JSONB columns.", "tags": ["database"]},
            {"content": "SQL indexes improve query performance.", "tags": ["database"]},
            {"content": "Database normalization reduces redundancy.", "tags": ["database"]},
            # Web topic
            {"content": "REST APIs use HTTP methods.", "tags": ["web"]},
            {"content": "GraphQL provides flexible queries.", "tags": ["web"]},
        ])
        
        print(f"   ✓ Created {len(memories)} memories")
        
        # ======================================================================
        # CREATE CLUSTER MANUALLY
        # ======================================================================
        print("\n2. Creating a manual cluster...")
        
        python_cluster = client.clusters.create(
            name="Python Programming",
            description="Cluster for Python-related memories",
            metadata={"topic": "programming", "language": "python"}
        )
        
        print(f"   ✓ Created cluster: {python_cluster.name} ({python_cluster.id})")
        
        # ======================================================================
        # ADD MEMORIES TO CLUSTER
        # ======================================================================
        print("\n3. Adding memories to cluster...")
        
        # Add first 3 memories (Python-related)
        for mem in memories[:3]:
            client.clusters.add_memory(
                cluster_id=python_cluster.id,
                memory_id=mem.id
            )
        
        print(f"   ✓ Added 3 memories to Python cluster")
        
        # ======================================================================
        # GET CLUSTER
        # ======================================================================
        print("\n4. Getting cluster details...")
        
        cluster = client.clusters.get(python_cluster.id)
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
        # GET CLUSTER MEMORIES
        # ======================================================================
        print("\n6. Getting memories in cluster...")
        
        cluster_memories = client.clusters.get_memories(
            cluster_id=python_cluster.id,
            limit=10
        )
        
        print(f"   Memories in '{python_cluster.name}':")
        for mem in cluster_memories.data:
            print(f"      - {mem.content[:40]}...")
        
        # ======================================================================
        # INCREMENTAL CLUSTERING
        # ======================================================================
        print("\n7. Running incremental clustering...")
        
        # This assigns unclustered memories to existing or new clusters
        result = client.clusters.incremental_clustering(
            memory_ids=[m.id for m in memories[3:]],  # Unclustered memories
            min_cluster_size=2,
            similarity_threshold=0.7
        )
        
        print(f"   ✓ Created {result.clusters_created} new clusters")
        print(f"   ✓ Assigned {result.memories_assigned} memories")
        
        # ======================================================================
        # EXPAND CLUSTER
        # ======================================================================
        print("\n8. Expanding cluster (finding similar memories)...")
        
        expansion = client.clusters.expand(
            cluster_id=python_cluster.id,
            limit=5,
            similarity_threshold=0.6
        )
        
        print(f"   Found {len(expansion.suggestions)} candidate memories:")
        for suggestion in expansion.suggestions:
            print(f"      - {suggestion.memory.content[:40]}... (score: {suggestion.score:.2f})")
        
        # ======================================================================
        # UPDATE CLUSTER
        # ======================================================================
        print("\n9. Updating cluster...")
        
        updated = client.clusters.update(
            python_cluster.id,
            name="Python Programming Concepts",
            description="Updated description"
        )
        print(f"   ✓ Updated cluster name to: {updated.name}")
        
        # ======================================================================
        # REMOVE MEMORY FROM CLUSTER
        # ======================================================================
        print("\n10. Removing memory from cluster...")
        
        client.clusters.remove_memory(
            cluster_id=python_cluster.id,
            memory_id=memories[0].id
        )
        print(f"   ✓ Removed one memory from cluster")
        
        # Verify count
        updated_cluster = client.clusters.get(python_cluster.id)
        print(f"   New memory count: {updated_cluster.memory_count}")
        
        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n11. Cleaning up...")
        
        # Delete clusters first
        for c in client.clusters.list().data:
            client.clusters.delete(c.id)
        
        # Then delete memories
        client.memories.bulk_delete([m.id for m in memories])
        
        print("   ✓ Cleaned up")
        print("\n" + "=" * 60)
        print("🎉 Clustering complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()

