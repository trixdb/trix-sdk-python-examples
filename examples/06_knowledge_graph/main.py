#!/usr/bin/env python3
"""
Knowledge Graph - Synchronous Version

This example demonstrates graph operations:
1. Graph traversal from a starting node
2. Finding shortest paths between memories
3. Discovering neighbors
4. Expanding graph context
5. Graph statistics

Run: python main.py
"""

from trix import Trix
from trix.types import RelationshipType


def main() -> None:
    """Demonstrate knowledge graph operations."""

    with Trix.from_env() as client:
        print("=" * 60)
        print("KNOWLEDGE GRAPH")
        print("=" * 60)

        # ======================================================================
        # SETUP - Create connected memories
        # ======================================================================
        print("\n1. Creating knowledge graph nodes...")

        # Create a small knowledge graph about a tech stack
        react = client.memories.create(
            content="React is a JavaScript UI library.", tags=["react"]
        )
        nextjs = client.memories.create(
            content="Next.js is built on React.", tags=["nextjs"]
        )
        vercel = client.memories.create(
            content="Vercel created Next.js.", tags=["vercel"]
        )
        javascript = client.memories.create(
            content="JavaScript is a programming language.", tags=["javascript"]
        )
        typescript = client.memories.create(
            content="TypeScript extends JavaScript.", tags=["typescript"]
        )

        memories = [react, nextjs, vercel, javascript, typescript]
        print(f"   Created {len(memories)} nodes")

        # Create relationships (edges)
        print("\n2. Creating graph edges (relationships)...")

        edges = [
            (nextjs.id, react.id),
            (react.id, javascript.id),
            (typescript.id, javascript.id),
            (nextjs.id, typescript.id),
            (vercel.id, nextjs.id),
        ]

        relationships = []
        for source, target in edges:
            rel = client.relationships.create(
                source_id=source,
                target_id=target,
                relationship_type=RelationshipType.RELATED_TO,
                weight=0.9,
            )
            relationships.append(rel)

        print(f"   Created {len(relationships)} edges")

        # ======================================================================
        # GRAPH TRAVERSAL
        # ======================================================================
        print("\n3. Traversing graph from Next.js...")

        traversal = client.graph.traverse(
            start_ids=[nextjs.id],
            depth=2,
        )

        print(f"   Found {len(traversal.nodes)} nodes in traversal:")
        for node in traversal.nodes:
            print(f"      - {node.memory.content[:40]}... (depth: {node.depth})")

        # ======================================================================
        # SHORTEST PATH
        # ======================================================================
        print("\n4. Finding shortest path: Vercel -> JavaScript...")

        path = client.graph.shortest_path(
            source_id=vercel.id,
            target_id=javascript.id,
            max_hops=5
        )

        if path:
            print(f"   Path length: {len(path.path)} hops")
            print("   Path:")
            for i, node in enumerate(path.path):
                prefix = "   ---" if i == len(path.path) - 1 else "   |--"
                print(f"   {prefix} {node}")

        # ======================================================================
        # NEIGHBORS
        # ======================================================================
        print("\n5. Finding neighbors of React...")

        neighbors = client.graph.neighbors(node_id=react.id)

        print(f"   React has {len(neighbors.incoming)} incoming, "
              f"{len(neighbors.outgoing)} outgoing connections")

        # ======================================================================
        # EXPAND
        # ======================================================================
        print("\n6. Expanding from TypeScript...")

        expanded = client.graph.expand(
            seed_memory_ids=[typescript.id],
            max_hops=2,
        )

        print(f"   Expanded to {expanded.stats.expanded_count} memories")

        # ======================================================================
        # GRAPH STATISTICS
        # ======================================================================
        print("\n7. Getting graph statistics...")

        stats = client.graph.get_stats()
        print(f"   Total nodes: {stats.total_nodes}")
        print(f"   Total edges: {stats.total_edges}")

        # ======================================================================
        # GET CONTEXT
        # ======================================================================
        print("\n8. Getting graph context for a query...")

        context = client.graph.get_context(
            query="web development frameworks",
            depth=2,
            semantic_limit=10
        )

        print(f"   Context has {len(context.memories)} relevant memories")

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n9. Cleaning up...")

        for rel in relationships:
            client.relationships.delete(rel.id)
        client.memories.bulk_delete([m.id for m in memories])

        print("   Cleaned up")
        print("\n" + "=" * 60)
        print("Knowledge graph complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
