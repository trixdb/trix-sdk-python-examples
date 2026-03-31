#!/usr/bin/env python3
"""
Pagination Recipes

Efficient patterns for paginating through large result sets.
"""

import asyncio
from trix import Trix, AsyncTrix


# =============================================================================
# 1. Basic Iterator Pattern (Recommended)
# =============================================================================

def iterate_all_memories():
    """Use the built-in iterator for automatic pagination."""
    with Trix.from_env() as client:
        # iter() handles pagination automatically
        for memory in client.memories.iter(page_size=100):
            print(f"Memory: {memory.id}")
            # Process each memory...


# =============================================================================
# 2. Async Iterator Pattern
# =============================================================================

async def iterate_all_memories_async():
    """Async iteration with automatic pagination."""
    async with AsyncTrix.from_env() as client:
        async for memory in await client.memories.iter(page_size=100):
            print(f"Memory: {memory.id}")


# =============================================================================
# 3. Manual Pagination with Cursor
# =============================================================================

def manual_pagination():
    """Manual pagination when you need more control."""
    with Trix.from_env() as client:
        offset = 0
        total = 0

        while True:
            # Fetch a page
            page = client.memories.list(limit=50, offset=offset)

            # Process items
            for memory in page.data:
                total += 1
                print(f"Processing {memory.id}")

            # Check for more pages
            if len(page.data) < 50 or total >= page.total:
                break

            offset += 50

        print(f"Processed {total} memories")


# =============================================================================
# 4. Filtered Pagination
# =============================================================================

def paginate_with_filters(tag: str):
    """Paginate through filtered results."""
    with Trix.from_env() as client:
        # Filters work with iter() too
        for memory in client.memories.iter(tags=[tag], page_size=100):
            print(f"Tagged memory: {memory.content[:50]}")


# =============================================================================
# 5. Batch Processing with Pagination
# =============================================================================

def process_in_batches(batch_size: int = 50):
    """Process memories in batches for efficiency."""
    with Trix.from_env() as client:
        batch = []
        
        for memory in client.memories.iter(page_size=100):
            batch.append(memory)
            
            if len(batch) >= batch_size:
                # Process batch
                process_batch(batch)
                batch = []
        
        # Process remaining
        if batch:
            process_batch(batch)


def process_batch(memories):
    """Process a batch of memories."""
    print(f"Processing batch of {len(memories)} memories")


# =============================================================================
# 6. Parallel Pagination (Async)
# =============================================================================

async def parallel_pagination():
    """Fetch from multiple sources in parallel."""
    async with AsyncTrix.from_env() as client:
        # Start multiple paginated queries
        tasks = [
            collect_all(await client.memories.iter(tags=["important"])),
            collect_all(await client.memories.iter(tags=["recent"])),
            collect_all(await client.memories.iter(tags=["archived"])),
        ]
        
        important, recent, archived = await asyncio.gather(*tasks)
        
        print(f"Important: {len(important)}, Recent: {len(recent)}, Archived: {len(archived)}")


async def collect_all(async_iterator) -> list:
    """Collect all items from an async iterator."""
    items = []
    async for item in async_iterator:
        items.append(item)
    return items


# =============================================================================
# 7. Progress Tracking
# =============================================================================

def paginate_with_progress():
    """Track progress while paginating."""
    with Trix.from_env() as client:
        processed = 0
        
        for memory in client.memories.iter(page_size=100):
            processed += 1
            
            # Log progress every 100 items
            if processed % 100 == 0:
                print(f"Processed {processed} memories...")
            
            # Do work...
        
        print(f"Done! Processed {processed} total memories")


# =============================================================================
# 8. Early Termination
# =============================================================================

def paginate_until_found(target_content: str) -> str | None:
    """Stop pagination early when target is found."""
    with Trix.from_env() as client:
        for memory in client.memories.iter(page_size=100):
            if target_content in memory.content:
                return memory.id
        return None


if __name__ == "__main__":
    iterate_all_memories()

