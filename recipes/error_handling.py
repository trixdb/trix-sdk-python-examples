#!/usr/bin/env python3
"""
Error Handling Recipes

Common patterns for handling errors with the Trix SDK.
"""

from trix import Trix
from trix.exceptions import (
    TrixError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError,
)


# =============================================================================
# 1. Basic Error Handling
# =============================================================================

def basic_error_handling():
    """Handle errors with a try/except block."""
    with Trix.from_env() as client:
        try:
            memory = client.memories.get("nonexistent-id")
        except NotFoundError:
            print("Memory not found")
        except AuthenticationError:
            print("Invalid API key")
        except TrixError as e:
            print(f"Trix error: {e}")


# =============================================================================
# 2. Comprehensive Error Handling
# =============================================================================

def comprehensive_error_handling():
    """Handle all error types with appropriate responses."""
    with Trix.from_env() as client:
        try:
            memory = client.memories.create(content="Test")
            print(f"Created: {memory.id}")
            
        except AuthenticationError:
            # API key is invalid or expired
            print("Please check your TRIX_API_KEY environment variable")
            raise SystemExit(1)
            
        except RateLimitError as e:
            # Too many requests - wait and retry
            print(f"Rate limited. Retry after: {e.retry_after} seconds")
            
        except ValidationError as e:
            # Request validation failed
            print(f"Invalid request: {e.message}")
            
        except NotFoundError:
            # Resource doesn't exist
            print("Resource not found")
            
        except ServerError:
            # Server-side error (5xx)
            print("Server error - please try again later")
            
        except TrixError as e:
            # Catch-all for other Trix errors
            print(f"Unexpected error: {e}")


# =============================================================================
# 3. Graceful Degradation
# =============================================================================

def graceful_degradation(query: str) -> list[str]:
    """Return partial results when some operations fail."""
    results = []
    
    with Trix.from_env() as client:
        # Try semantic search first
        try:
            search_results = client.search.query(query=query, limit=5)
            results.extend([r.memory.content for r in search_results.results])
        except TrixError:
            pass  # Fall through to alternatives
        
        # Try similar search as backup
        if not results:
            try:
                similar = client.search.similar(text=query, limit=5)
                results.extend([r.memory.content for r in similar.results])
            except TrixError:
                pass
        
        # Return whatever we got
        return results


# =============================================================================
# 4. Error Context Preservation
# =============================================================================

class MemoryOperationError(Exception):
    """Custom exception with context."""
    
    def __init__(self, operation: str, memory_id: str, cause: Exception):
        self.operation = operation
        self.memory_id = memory_id
        self.cause = cause
        super().__init__(f"{operation} failed for {memory_id}: {cause}")


def operation_with_context(memory_id: str):
    """Preserve error context for debugging."""
    with Trix.from_env() as client:
        try:
            return client.memories.get(memory_id)
        except TrixError as e:
            raise MemoryOperationError("get", memory_id, e) from e


# =============================================================================
# 5. Bulk Operation Error Handling
# =============================================================================

def bulk_with_partial_failure(contents: list[str]) -> dict:
    """Handle partial failures in bulk operations."""
    results = {"succeeded": [], "failed": []}
    
    with Trix.from_env() as client:
        for content in contents:
            try:
                memory = client.memories.create(content=content)
                results["succeeded"].append(memory.id)
            except TrixError as e:
                results["failed"].append({"content": content[:50], "error": str(e)})
    
    return results


if __name__ == "__main__":
    basic_error_handling()

