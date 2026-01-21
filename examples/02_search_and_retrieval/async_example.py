#!/usr/bin/env python3
"""
Search and Retrieval - Asynchronous Version

Demonstrates async search operations:
1. Concurrent search queries
2. Async embedding generation
3. Parallel search operations

Run: python async_example.py
"""

import asyncio
from trix import AsyncTrix


async def main() -> None:
    """Demonstrate async search operations."""
    
    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC SEARCH AND RETRIEVAL")
        print("=" * 60)
        
        # ======================================================================
        # SETUP
        # ======================================================================
        print("\n1. Setting up sample data...")
        
        memories = await client.memories.bulk_create([
            {"content": "Python is great for data analysis.", "tags": ["python"]},
            {"content": "JavaScript powers modern web apps.", "tags": ["javascript"]},
            {"content": "Machine learning automates predictions.", "tags": ["ml"]},
        ])
        print(f"   ✓ Created {len(memories)} memories")
        
        # ======================================================================
        # CONCURRENT SEARCHES
        # ======================================================================
        print("\n2. Running concurrent searches...")
        
        queries = [
            "programming languages",
            "web development",
            "artificial intelligence",
        ]
        
        search_tasks = [
            client.search.query(query=q, limit=3)
            for q in queries
        ]
        
        results = await asyncio.gather(*search_tasks)
        
        for query, result in zip(queries, results):
            print(f"   '{query}': {len(result.results)} results")
        
        # ======================================================================
        # CONCURRENT SIMILAR SEARCHES
        # ======================================================================
        print("\n3. Finding similar memories concurrently...")
        
        similar_tasks = [
            client.search.similar(memory_id=m.id, limit=2)
            for m in memories
        ]
        
        similar_results = await asyncio.gather(*similar_tasks)
        
        for mem, similar in zip(memories, similar_results):
            print(f"   Similar to '{mem.content[:25]}...': {len(similar.results)} found")
        
        # ======================================================================
        # ASYNC BATCH EMBEDDINGS
        # ======================================================================
        print("\n4. Generating embeddings...")
        
        embeddings = await client.search.embed_all(
            texts=["First text", "Second text", "Third text"]
        )
        print(f"   ✓ Generated {len(embeddings.embeddings)} embeddings")
        
        # ======================================================================
        # PARALLEL OPERATIONS
        # ======================================================================
        print("\n5. Running search and embed in parallel...")
        
        search_result, embedding = await asyncio.gather(
            client.search.query(query="programming", limit=5),
            client.search.embed(text="programming languages")
        )
        
        print(f"   Search found: {len(search_result.results)} results")
        print(f"   Embedding dims: {len(embedding.embedding)}")
        
        # ======================================================================
        # TOPIC SEARCH
        # ======================================================================
        print("\n6. Topic-based search...")
        
        topic_results = await client.search.by_topic(
            topic="software development",
            limit=5
        )
        print(f"   Found {len(topic_results.results)} memories on topic")
        
        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n7. Cleaning up...")
        
        await client.memories.bulk_delete([m.id for m in memories])
        print("   ✓ Cleaned up")
        
        print("\n" + "=" * 60)
        print("🎉 Async search complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

