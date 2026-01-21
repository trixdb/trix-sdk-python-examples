#!/usr/bin/env python3
"""
Retry Strategies

Patterns for handling transient failures with retries.
"""

import time
import random
import asyncio
from functools import wraps
from typing import TypeVar, Callable

from trix import Trix, AsyncTrix
from trix.exceptions import TrixError, RateLimitError, ServerError

T = TypeVar("T")


# =============================================================================
# 1. Simple Retry with Exponential Backoff
# =============================================================================

def retry_with_backoff(
    func: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> T:
    """Retry a function with exponential backoff."""
    for attempt in range(max_retries + 1):
        try:
            return func()
        except (RateLimitError, ServerError) as e:
            if attempt == max_retries:
                raise
            
            delay = base_delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
            time.sleep(delay)
    
    raise RuntimeError("Should not reach here")


# Usage example
def example_simple_retry():
    with Trix.from_env() as client:
        memory = retry_with_backoff(
            lambda: client.memories.create(content="Test")
        )
        print(f"Created: {memory.id}")


# =============================================================================
# 2. Retry Decorator
# =============================================================================

def with_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    jitter: bool = True,
):
    """Decorator for automatic retries."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (RateLimitError, ServerError):
                    if attempt == max_retries:
                        raise
                    
                    delay = base_delay * (2 ** attempt)
                    if jitter:
                        delay += random.uniform(0, delay * 0.1)
                    
                    time.sleep(delay)
            
            raise RuntimeError("Should not reach here")
        return wrapper
    return decorator


# Usage example
@with_retry(max_retries=3)
def create_memory_with_retry(client: Trix, content: str):
    return client.memories.create(content=content)


# =============================================================================
# 3. Async Retry
# =============================================================================

async def async_retry_with_backoff(
    coro_func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> T:
    """Async retry with exponential backoff."""
    for attempt in range(max_retries + 1):
        try:
            return await coro_func()
        except (RateLimitError, ServerError):
            if attempt == max_retries:
                raise
            
            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)
    
    raise RuntimeError("Should not reach here")


# Usage example
async def example_async_retry():
    async with AsyncTrix.from_env() as client:
        memory = await async_retry_with_backoff(
            lambda: client.memories.create(content="Test")
        )
        print(f"Created: {memory.id}")


# =============================================================================
# 4. Rate Limit Aware Retry
# =============================================================================

def rate_limit_aware_retry(func: Callable[[], T], max_retries: int = 3) -> T:
    """Retry that respects rate limit headers."""
    for attempt in range(max_retries + 1):
        try:
            return func()
        except RateLimitError as e:
            if attempt == max_retries:
                raise
            
            # Use retry_after from the error if available
            delay = getattr(e, "retry_after", 1.0) or 1.0
            print(f"Rate limited, waiting {delay}s...")
            time.sleep(delay)
        except ServerError:
            if attempt == max_retries:
                raise
            time.sleep(2 ** attempt)
    
    raise RuntimeError("Should not reach here")


# =============================================================================
# 5. Circuit Breaker Pattern
# =============================================================================

class CircuitBreaker:
    """Circuit breaker to prevent cascading failures."""
    
    def __init__(self, failure_threshold: int = 5, reset_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time: float | None = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func: Callable[[], T]) -> T:
        """Execute function with circuit breaker protection."""
        if self.state == "open":
            if time.time() - (self.last_failure_time or 0) > self.reset_timeout:
                self.state = "half-open"
            else:
                raise RuntimeError("Circuit breaker is open")
        
        try:
            result = func()
            self._on_success()
            return result
        except TrixError:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failures = 0
        self.state = "closed"
    
    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"


# Usage example
def example_circuit_breaker():
    breaker = CircuitBreaker(failure_threshold=3)
    
    with Trix.from_env() as client:
        try:
            memory = breaker.call(lambda: client.memories.create(content="Test"))
            print(f"Created: {memory.id}")
        except RuntimeError as e:
            print(f"Circuit breaker open: {e}")


if __name__ == "__main__":
    example_simple_retry()

