#!/usr/bin/env python3
"""
Getting Started with Trix SDK - Asynchronous Version

This example demonstrates async usage of the Trix Python SDK:
1. Creating an async client instance
2. Using async/await patterns
3. Managing memories asynchronously
4. Proper async context management

Run: python async_example.py
"""

import asyncio

from trix import AsyncTrix
from trix.exceptions import AuthenticationError, TrixError


async def main() -> None:
    """Main async entry point demonstrating async Trix SDK usage."""

    # ==========================================================================
    # Create async client from environment variables
    # ==========================================================================
    try:
        client = AsyncTrix.from_env()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Make sure TRIX_API_KEY is set in your environment")
        return

    # ==========================================================================
    # Using async context manager (recommended)
    # ==========================================================================
    async with client:
        try:
            # ------------------------------------------------------------------
            # Create memory asynchronously
            # ------------------------------------------------------------------
            print("Creating memory asynchronously...")

            memory = await client.memories.create(
                content="Async operations allow for non-blocking API calls.",
                tags=["async", "getting-started"],
                metadata={"source": "async_example"},
            )

            print(f"✓ Created memory: {memory.id}")

            # ------------------------------------------------------------------
            # Concurrent operations example
            # ------------------------------------------------------------------
            print("\nCreating multiple memories concurrently...")

            # Create multiple memories at once using gather
            tasks = [
                client.memories.create(
                    content=f"Concurrent memory #{i}",
                    tags=["concurrent", "batch"],
                )
                for i in range(3)
            ]

            memories = await asyncio.gather(*tasks)
            print(f"✓ Created {len(memories)} memories concurrently")

            # ------------------------------------------------------------------
            # Async search
            # ------------------------------------------------------------------
            print("\nSearching asynchronously...")

            results = await client.search.query(query="concurrent operations", limit=5)

            print(f"✓ Found {len(results.data)} results")

            # ------------------------------------------------------------------
            # Cleanup - delete all created memories
            # ------------------------------------------------------------------
            print("\nCleaning up...")

            delete_tasks = [client.memories.delete(m.id) for m in memories]
            delete_tasks.append(client.memories.delete(memory.id))
            await asyncio.gather(*delete_tasks)

            print("✓ All memories deleted")
            print("\n🎉 Async getting started complete!")

        except AuthenticationError:
            print("❌ Authentication failed. Check your API key.")
        except TrixError as e:
            print(f"❌ API error: {e.message}")


if __name__ == "__main__":
    asyncio.run(main())
