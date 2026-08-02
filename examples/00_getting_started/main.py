#!/usr/bin/env python3
"""
Getting Started with Trix SDK - Synchronous Version

This example demonstrates the basics of using the Trix Python SDK:
1. Creating a client instance
2. Using environment variables for configuration
3. Creating your first memory
4. Retrieving and searching memories

Run: python main.py
"""

from trix import Trix
from trix.exceptions import AuthenticationError, TrixError


def main() -> None:
    """Main entry point demonstrating basic Trix SDK usage."""

    # ==========================================================================
    # Method 1: Create client with explicit API key
    # ==========================================================================
    # Useful for testing or when you want explicit control
    # client = Trix(api_key="your_api_key_here")

    # ==========================================================================
    # Method 2: Create client from environment variables (recommended)
    # ==========================================================================
    # This reads TRIX_API_KEY from environment automatically
    # Best practice for production code
    try:
        client = Trix.from_env()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Make sure TRIX_API_KEY is set in your environment")
        return

    # ==========================================================================
    # Using context manager (recommended)
    # ==========================================================================
    # The context manager ensures proper cleanup of resources
    with client:
        try:
            # ------------------------------------------------------------------
            # Create your first memory
            # ------------------------------------------------------------------
            print("Creating your first memory...")

            memory = client.memories.create(
                content="The Trix SDK makes it easy to store and retrieve memories.",
                tags=["getting-started", "tutorial"],
                metadata={"source": "example", "importance": "high"},
            )

            print(f"✓ Created memory with ID: {memory.id}")
            print(f"  Content: {memory.content[:50]}...")
            print(f"  Tags: {memory.tags}")

            # ------------------------------------------------------------------
            # Retrieve the memory by ID
            # ------------------------------------------------------------------
            print("\nRetrieving memory by ID...")

            retrieved = client.memories.get(memory.id)
            print(f"✓ Retrieved: {retrieved.content}")

            # ------------------------------------------------------------------
            # Search for memories
            # ------------------------------------------------------------------
            print("\nSearching for memories...")

            results = client.search.query(query="How do I store memories?", limit=5)

            print(f"✓ Found {len(results.data)} matching memories:")
            for i, result in enumerate(results.data, 1):
                print(f"  {i}. {result.memory.content[:60]}... (score: {result.score:.3f})")

            # ------------------------------------------------------------------
            # Update a memory
            # ------------------------------------------------------------------
            print("\nUpdating memory...")

            updated = client.memories.update(
                memory.id,
                tags=["getting-started", "tutorial", "updated"],
                metadata={"source": "example", "importance": "high", "updated": True},
            )

            print(f"✓ Updated tags: {updated.tags}")

            # ------------------------------------------------------------------
            # Delete the memory (cleanup)
            # ------------------------------------------------------------------
            print("\nCleaning up...")

            client.memories.delete(memory.id)
            print("✓ Memory deleted")

            print("\n🎉 Getting started complete! You've learned the basics.")

        except AuthenticationError:
            print("❌ Authentication failed. Check your API key.")
        except TrixError as e:
            print(f"❌ API error: {e.message}")


if __name__ == "__main__":
    main()
