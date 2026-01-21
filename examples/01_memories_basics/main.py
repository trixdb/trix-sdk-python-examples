#!/usr/bin/env python3
"""
Memories Basics - Synchronous Version

This example covers comprehensive memory management:
1. CRUD operations (Create, Read, Update, Delete)
2. Bulk operations for efficiency
3. Pagination with iter()
4. Memory statistics and configuration

Run: python main.py
"""

from trix import Trix
from trix.types import MemoryType


def main() -> None:
    """Demonstrate comprehensive memory operations."""
    
    with Trix.from_env() as client:
        print("=" * 60)
        print("MEMORY BASICS - CRUD OPERATIONS")
        print("=" * 60)
        
        # ======================================================================
        # CREATE - Single Memory
        # ======================================================================
        print("\n1. Creating a single memory...")
        
        memory = client.memories.create(
            content="Python is a versatile programming language used for web development, data science, and AI.",
            type=MemoryType.TEXT,
            tags=["programming", "python", "languages"],
            metadata={
                "source": "tutorial",
                "category": "technology",
                "difficulty": "beginner"
            }
        )
        print(f"   ✓ Created: {memory.id}")
        
        # ======================================================================
        # READ - Get by ID
        # ======================================================================
        print("\n2. Reading memory by ID...")
        
        retrieved = client.memories.get(memory.id)
        print(f"   Content: {retrieved.content[:60]}...")
        print(f"   Type: {retrieved.type}")
        print(f"   Tags: {retrieved.tags}")
        
        # ======================================================================
        # UPDATE - Modify existing memory
        # ======================================================================
        print("\n3. Updating memory...")
        
        updated = client.memories.update(
            memory.id,
            content="Python is a versatile, high-level programming language.",
            tags=["programming", "python", "languages", "updated"],
            metadata={"source": "tutorial", "version": 2}
        )
        print(f"   ✓ Updated tags: {updated.tags}")
        
        # ======================================================================
        # BULK CREATE - Multiple memories at once
        # ======================================================================
        print("\n4. Bulk creating memories...")
        
        bulk_memories = client.memories.bulk_create([
            {"content": "JavaScript powers interactive web pages.", "tags": ["javascript", "web"]},
            {"content": "Rust provides memory safety without garbage collection.", "tags": ["rust", "systems"]},
            {"content": "Go is designed for simplicity and concurrency.", "tags": ["go", "backend"]},
        ])
        print(f"   ✓ Created {len(bulk_memories)} memories")
        
        # ======================================================================
        # LIST - With filtering and pagination
        # ======================================================================
        print("\n5. Listing memories with pagination...")
        
        page = client.memories.list(limit=10)
        print(f"   Found {page.pagination.total} total memories")
        print(f"   This page has {len(page.data)} items")
        
        # ======================================================================
        # ITER - Automatic pagination iterator
        # ======================================================================
        print("\n6. Iterating through all memories...")
        
        count = 0
        for mem in client.memories.iter(page_size=5, max_items=20):
            count += 1
            print(f"   {count}. {mem.content[:40]}...")
        print(f"   ✓ Iterated through {count} memories")
        
        # ======================================================================
        # STATS - Get memory statistics
        # ======================================================================
        print("\n7. Getting memory statistics...")
        
        stats = client.memories.get_stats()
        print(f"   Total memories: {stats.total_memories}")
        print(f"   Total size: {stats.total_size_bytes} bytes")
        
        # ======================================================================
        # CONFIG - Get memory configuration
        # ======================================================================
        print("\n8. Getting memory configuration...")
        
        config = client.memories.get_config()
        print(f"   Max content length: {config.max_content_length}")
        print(f"   Supported types: {config.supported_types}")
        
        # ======================================================================
        # BULK UPDATE
        # ======================================================================
        print("\n9. Bulk updating memories...")
        
        updates = [{"id": m.id, "tags": m.tags + ["bulk-updated"]} for m in bulk_memories[:2]]
        updated_memories = client.memories.bulk_update(updates)
        print(f"   ✓ Updated {len(updated_memories)} memories")
        
        # ======================================================================
        # CLEANUP - Delete all created memories
        # ======================================================================
        print("\n10. Cleaning up...")
        
        # Delete single memory
        client.memories.delete(memory.id)
        
        # Bulk delete
        ids_to_delete = [m.id for m in bulk_memories]
        client.memories.bulk_delete(ids_to_delete)
        
        print("   ✓ All memories deleted")
        print("\n" + "=" * 60)
        print("🎉 Memory basics complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()

