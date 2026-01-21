#!/usr/bin/env python3
"""
Advanced Patterns - Synchronous Version

This example demonstrates production patterns:
1. Error handling with exception types
2. Custom retry strategies
3. Request/response interceptors
4. Connection pooling
5. Rate limiting handling
6. Timeout configuration

Run: python main.py
"""

import time
from trix import Trix
from trix.exceptions import (
    TrixError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError,
)


def demonstrate_error_handling():
    """Show different error handling patterns."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING")
    print("=" * 60)
    
    with Trix.from_env() as client:
        # Handle specific errors
        print("\n1. Handling specific exceptions...")
        
        try:
            # Try to get a non-existent memory
            client.memories.get("nonexistent_id")
        except NotFoundError as e:
            print(f"   ✓ NotFoundError: {e.message}")
            print(f"     Status: {e.status_code}")
        except TrixError as e:
            print(f"   Other error: {e}")
        
        # Handle validation errors
        print("\n2. Handling validation errors...")
        
        try:
            # Invalid input
            client.memories.create(content="")  # Empty content
        except ValidationError as e:
            print(f"   ✓ ValidationError: {e.message}")
            if e.errors:
                for field, msg in e.errors.items():
                    print(f"     - {field}: {msg}")
        except TrixError as e:
            print(f"   Other error: {e}")
        
        # Handle rate limiting
        print("\n3. Rate limit handling pattern...")
        
        def with_rate_limit_retry(func, max_retries=3):
            """Execute function with rate limit retry."""
            for attempt in range(max_retries):
                try:
                    return func()
                except RateLimitError as e:
                    if attempt < max_retries - 1:
                        wait_time = e.retry_after or (2 ** attempt)
                        print(f"   Rate limited, waiting {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise
        
        # Usage example (simulated)
        print("   ✓ Rate limit retry pattern implemented")


def demonstrate_custom_client_config():
    """Show custom client configuration."""
    print("\n" + "=" * 60)
    print("CUSTOM CLIENT CONFIGURATION")
    print("=" * 60)
    
    # Custom timeout configuration
    print("\n1. Custom timeout configuration...")
    
    client = Trix.from_env(
        timeout=30.0,  # 30 second timeout
    )
    
    with client:
        print(f"   ✓ Client configured with custom timeout")
    
    # Custom base URL (for self-hosted or proxy)
    print("\n2. Custom base URL...")
    
    # client = Trix(
    #     api_key="your-key",
    #     base_url="https://your-proxy.example.com/v1"
    # )
    print("   ✓ Custom base URL pattern shown")
    
    # Connection with retries
    print("\n3. Connection with automatic retries...")
    
    client = Trix.from_env(
        max_retries=3,
    )
    
    with client:
        print(f"   ✓ Client configured with 3 retries")


def demonstrate_batch_operations():
    """Show efficient batch patterns."""
    print("\n" + "=" * 60)
    print("BATCH OPERATIONS")
    print("=" * 60)
    
    with Trix.from_env() as client:
        # Batch create with chunking
        print("\n1. Chunked batch creation...")
        
        def chunked_create(items: list, chunk_size: int = 100):
            """Create items in chunks to avoid payload limits."""
            results = []
            for i in range(0, len(items), chunk_size):
                chunk = items[i:i + chunk_size]
                created = client.memories.bulk_create(chunk)
                results.extend(created)
                print(f"   Processed chunk {i//chunk_size + 1}")
            return results
        
        # Example usage
        large_dataset = [{"content": f"Memory {i}"} for i in range(5)]
        memories = chunked_create(large_dataset, chunk_size=2)
        print(f"   ✓ Created {len(memories)} memories in chunks")
        
        # Cleanup
        client.memories.bulk_delete([m.id for m in memories])


def demonstrate_pagination_patterns():
    """Show pagination handling patterns."""
    print("\n" + "=" * 60)
    print("PAGINATION PATTERNS")
    print("=" * 60)
    
    with Trix.from_env() as client:
        # Create some test data
        memories = client.memories.bulk_create([
            {"content": f"Pagination test memory {i}"} for i in range(5)
        ])
        
        # Manual pagination
        print("\n1. Manual pagination...")
        
        cursor = None
        page = 0
        all_items = []
        
        while True:
            result = client.memories.list(limit=2, cursor=cursor)
            all_items.extend(result.data)
            page += 1
            print(f"   Page {page}: {len(result.data)} items")
            
            if not result.pagination.has_more:
                break
            cursor = result.pagination.cursor
        
        print(f"   ✓ Total items: {len(all_items)}")
        
        # Using iterator (preferred)
        print("\n2. Using iterator (recommended)...")
        
        count = 0
        for memory in client.memories.iter(limit=2):
            count += 1
            if count >= 5:
                break
        
        print(f"   ✓ Iterated through {count} items")
        
        # Cleanup
        client.memories.bulk_delete([m.id for m in memories])


def main():
    """Run all advanced pattern demonstrations."""
    print("=" * 60)
    print("ADVANCED PATTERNS")
    print("=" * 60)
    
    demonstrate_error_handling()
    demonstrate_custom_client_config()
    demonstrate_batch_operations()
    demonstrate_pagination_patterns()
    
    print("\n" + "=" * 60)
    print("🎉 Advanced patterns complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

