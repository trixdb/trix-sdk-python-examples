#!/usr/bin/env python3
"""
Advanced Patterns - Asynchronous Version

Run: python async_example.py
"""

import asyncio
from trix import AsyncTrix
from trix.exceptions import TrixError, RateLimitError, NotFoundError
from trix.types import MemoryCreate


async def demonstrate_error_handling():
    """Show async error handling patterns."""
    print("\n" + "=" * 60)
    print("ASYNC ERROR HANDLING")
    print("=" * 60)
    
    async with AsyncTrix.from_env() as client:
        print("\n1. Handling errors with context...")
        
        try:
            await client.memories.get("nonexistent")
        except NotFoundError as e:
            print(f"   ✓ NotFoundError caught: {e.message}")
        except TrixError as e:
            print(f"   Other error: {e}")


async def demonstrate_concurrent_with_semaphore():
    """Show concurrency control with semaphore."""
    print("\n" + "=" * 60)
    print("CONCURRENCY CONTROL")
    print("=" * 60)
    
    async with AsyncTrix.from_env() as client:
        # Create test data
        memories = await asyncio.gather(*[
            client.memories.create(content=f"Concurrent test {i}")
            for i in range(10)
        ])
        
        # Limit concurrent operations
        print("\n1. Using semaphore for rate limiting...")
        
        semaphore = asyncio.Semaphore(3)  # Max 3 concurrent operations
        
        async def limited_operation(memory_id: str):
            async with semaphore:
                mem = await client.memories.get(memory_id)
                return mem
        
        tasks = [limited_operation(m.id) for m in memories]
        results = await asyncio.gather(*tasks)
        
        print(f"   ✓ Processed {len(results)} items with max 3 concurrent")
        
        # Cleanup
        await client.memories.bulk_delete([m.id for m in memories])


async def demonstrate_async_iteration():
    """Show async iteration patterns."""
    print("\n" + "=" * 60)
    print("ASYNC ITERATION")
    print("=" * 60)
    
    async with AsyncTrix.from_env() as client:
        # Create test data
        memories = await asyncio.gather(*[
            client.memories.create(content=f"Async iter test {i}")
            for i in range(5)
        ])
        
        # Async iteration
        print("\n1. Async iteration...")
        
        count = 0
        async for memory in await client.memories.iter(page_size=2):
            count += 1
            print(f"   - {memory.content[:30]}...")
            if count >= 5:
                break
        
        print(f"   ✓ Iterated through {count} items")
        
        # Cleanup
        await client.memories.bulk_delete([m.id for m in memories])


async def demonstrate_timeout_handling():
    """Show timeout handling."""
    print("\n" + "=" * 60)
    print("TIMEOUT HANDLING")
    print("=" * 60)
    
    print("\n1. Using asyncio.timeout (Python 3.11+)...")
    
    async with AsyncTrix.from_env() as client:
        try:
            async with asyncio.timeout(5.0):  # 5 second timeout
                result = await client.memories.list(limit=1)
                print(f"   ✓ Request completed within timeout")
        except asyncio.TimeoutError:
            print("   ✗ Request timed out")


async def demonstrate_gather_with_exceptions():
    """Show error handling with asyncio.gather."""
    print("\n" + "=" * 60)
    print("GATHER WITH ERROR HANDLING")
    print("=" * 60)
    
    async with AsyncTrix.from_env() as client:
        # Create test data
        memories = await asyncio.gather(*[
            client.memories.create(content=f"Gather test {i}")
            for i in range(3)
        ])
        
        print("\n1. Gather with return_exceptions...")
        
        # Mix valid and invalid IDs
        ids = [m.id for m in memories] + ["invalid_id"]
        
        tasks = [client.memories.get(id) for id in ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successes = sum(1 for r in results if not isinstance(r, Exception))
        failures = sum(1 for r in results if isinstance(r, Exception))
        
        print(f"   ✓ Successes: {successes}, Failures: {failures}")
        
        # Cleanup
        await client.memories.bulk_delete([m.id for m in memories])


async def main():
    """Run all async advanced pattern demonstrations."""
    print("=" * 60)
    print("ASYNC ADVANCED PATTERNS")
    print("=" * 60)
    
    await demonstrate_error_handling()
    await demonstrate_concurrent_with_semaphore()
    await demonstrate_async_iteration()
    await demonstrate_timeout_handling()
    await demonstrate_gather_with_exceptions()
    
    print("\n" + "=" * 60)
    print("🎉 Async advanced patterns complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

