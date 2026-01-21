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
        memories = client.memories.bulk_create([
            {"content": "React is a JavaScript UI library.", "tags": ["react"]},
            {"content": "Next.js is built on React.", "tags": ["nextjs"]},
            {"content": "Vercel created Next.js.", "tags": ["vercel"]},
            {"content": "JavaScript is a programming language.", "tags": ["javascript"]},
            {"content": "TypeScript extends JavaScript.", "tags": ["typescript"]},
        ])
        
        react, nextjs, vercel, javascript, typescript = memories
        print(f"   ✓ Created {len(memories)} nodes")
        
        # Create relationships (edges)
        print("\n2. Creating graph edges (relationships)...")
        
        edges = [
            (nextjs.id, react.id, "built_with"),
            (react.id, javascript.id, "uses"),
            (typescript.id, javascript.id, "extends"),
            (nextjs.id, typescript.id, "supports"),
            (vercel.id, nextjs.id, "created"),
        ]
        
        relationships = []
        for source, target, rel_type in edges:
            rel = client.relationships.create(
                source_id=source,
                target_id=target,
                relationship_type="related_to",
                weight=0.9,
                metadata={"edge_type": rel_type}
            )
            relationships.append(rel)
        
        print(f"   ✓ Created {len(relationships)} edges")
        
        # ======================================================================
        # GRAPH TRAVERSAL
        # ======================================================================
        print("\n3. Traversing graph from Next.js...")
        
        traversal = client.graph.traverse(
            start_id=nextjs.id,
            max_depth=2,
            direction="both",
            limit=10
        )
        
        print(f"   Found {len(traversal.nodes)} nodes in traversal:")
        for node in traversal.nodes:
            print(f"      - {node.content[:40]}... (depth: {node.depth})")
        
        # ======================================================================
        # SHORTEST PATH
        # ======================================================================
        print("\n4. Finding shortest path: Vercel → JavaScript...")
        
        path = client.graph.shortest_path(
            source_id=vercel.id,
            target_id=javascript.id,
            max_depth=5
        )
        
        print(f"   Path length: {len(path.path)} hops")
        print("   Path:")
        for i, node in enumerate(path.path):
            prefix = "   └──" if i == len(path.path) - 1 else "   ├──"
            print(f"   {prefix} {node.content[:40]}...")
        
        # ======================================================================
        # NEIGHBORS
        # ======================================================================
        print("\n5. Finding neighbors of React...")
        
        neighbors = client.graph.neighbors(
            memory_id=react.id,
            direction="both",
            limit=10
        )
        
        print(f"   React has {len(neighbors.neighbors)} neighbors:")
        for neighbor in neighbors.neighbors:
            print(f"      - {neighbor.memory.content[:40]}...")
        
        # ======================================================================
        # EXPAND
        # ======================================================================
        print("\n6. Expanding from TypeScript...")
        
        expanded = client.graph.expand(
            memory_ids=[typescript.id],
            depth=2,
            limit=20
        )
        
        print(f"   Expanded to {len(expanded.memories)} memories")
        
        # ======================================================================
        # GRAPH STATISTICS
        # ======================================================================
        print("\n7. Getting graph statistics...")
        
        stats = client.graph.get_stats()
        print(f"   Total nodes: {stats.total_nodes}")
        print(f"   Total edges: {stats.total_edges}")
        print(f"   Average degree: {stats.average_degree:.2f}")
        
        # ======================================================================
        # GET CONTEXT
        # ======================================================================
        print("\n8. Getting graph context for a query...")
        
        context = client.graph.get_context(
            query="web development frameworks",
            start_ids=[react.id, nextjs.id],
            max_depth=2,
            limit=10
        )
        
        print(f"   Context has {len(context.memories)} relevant memories")
        
        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n9. Cleaning up...")
        
        for rel in relationships:
            client.relationships.delete(rel.id)
        client.memories.bulk_delete([m.id for m in memories])
        
        print("   ✓ Cleaned up")
        print("\n" + "=" * 60)
        print("🎉 Knowledge graph complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()

