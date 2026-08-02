#!/usr/bin/env python3
"""
Search and Retrieval - Synchronous Version

This example demonstrates search capabilities:
1. Semantic query search
2. Finding similar memories
3. Generating embeddings
4. Topic-based search

Run: python main.py
"""

from trix import Trix


def main() -> None:
    """Demonstrate search and retrieval operations."""

    with Trix.from_env() as client:
        print("=" * 60)
        print("SEARCH AND RETRIEVAL")
        print("=" * 60)

        # ======================================================================
        # SETUP - Create sample memories for searching
        # ======================================================================
        print("\n1. Setting up sample data...")

        sample_content = [
            "Machine learning models can predict outcomes based on historical data.",
            "Neural networks are inspired by the structure of the human brain.",
            "Deep learning excels at image and speech recognition tasks.",
            "Python is popular for data science and machine learning applications.",
            "The weather today is sunny with a high of 75 degrees.",
        ]

        # Create sample memories individually (bulk_create returns BulkResult, not a list)
        memories = []
        for c in sample_content:
            mem = client.memories.create(content=c, tags=["sample"])
            memories.append(mem)
        print(f"   ✓ Created {len(memories)} sample memories")

        # ======================================================================
        # QUERY - Semantic search
        # ======================================================================
        print("\n2. Semantic query search...")

        results = client.search.query(
            query="How do neural networks learn from data?",
            limit=3,
            threshold=0.5,  # Minimum similarity score
        )

        print("   Query: 'How do neural networks learn from data?'")
        print(f"   Found {len(results.data)} results:")
        for i, r in enumerate(results.data, 1):
            print(f"   {i}. (score: {r.score:.3f}) {r.memory.content[:50]}...")

        # ======================================================================
        # QUERY WITH FILTERS
        # ======================================================================
        print("\n3. Query with tag filters...")

        filtered_results = client.search.query(
            query="artificial intelligence",
            limit=5,
            tags=["sample"],  # Only search in memories with this tag
        )

        print(f"   Found {len(filtered_results.data)} results with 'sample' tag")

        # ======================================================================
        # SIMILAR - Find memories similar to a specific memory
        # ======================================================================
        print("\n4. Finding similar memories...")

        ml_memory = memories[0]  # The machine learning memory
        similar = client.search.similar(
            memory_id=ml_memory.id,
            limit=3,
        )

        print(f"   Finding memories similar to: '{ml_memory.content[:40]}...'")
        print(f"   Found {len(similar.data)} similar memories:")
        for i, r in enumerate(similar.data, 1):
            print(f"   {i}. (score: {r.score:.3f}) {r.memory.content[:50]}...")

        # ======================================================================
        # EMBED - Generate embeddings
        # ======================================================================
        print("\n5. Generating embeddings...")

        embedding = client.search.embed(memory_ids=[ml_memory.id])

        print(f"   Generated embeddings for {len(embedding.embeddings)} memories")

        # ======================================================================
        # EMBED ALL - Batch embedding generation
        # ======================================================================
        print("\n6. Batch embedding generation...")

        client.search.embed_all(batch_size=100)
        print("   Processed all memories in batches of 100")

        # ======================================================================
        # BY_TOPIC - Topic-based retrieval
        # ======================================================================
        print("\n7. Topic-based search...")

        topic_results = client.search.by_topic(topic="artificial intelligence", limit=5)

        print("   Topic: 'artificial intelligence'")
        print(f"   Found {len(topic_results.data)} memories on this topic:")
        for i, r in enumerate(topic_results.data, 1):
            print(f"   {i}. {r.memory.content[:50]}...")

        # ======================================================================
        # SEARCH CONFIG
        # ======================================================================
        print("\n8. Getting search configuration...")

        config = client.search.get_config()
        print(f"   Default limit: {config.default_limit}")
        print(f"   Max limit: {config.max_limit}")
        print(f"   Embedding dimensions: {config.embedding_dimensions}")

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n9. Cleaning up...")

        client.memories.bulk_delete([m.id for m in memories])
        print("   ✓ Sample memories deleted")

        print("\n" + "=" * 60)
        print("🎉 Search and retrieval complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
