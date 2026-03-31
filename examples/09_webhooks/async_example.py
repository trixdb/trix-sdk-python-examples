#!/usr/bin/env python3
"""
Webhooks - Asynchronous Version

Run: python async_example.py
"""

import asyncio
from trix import AsyncTrix
from trix.types import WebhookEvent


async def main() -> None:
    """Demonstrate async webhook operations."""

    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC WEBHOOKS")
        print("=" * 60)

        # ======================================================================
        # GET EVENT TYPES
        # ======================================================================
        print("\n1. Getting event types...")

        event_types = await client.webhooks.get_event_types()
        print(f"   Available: {len(event_types)} event types")

        # ======================================================================
        # CREATE WEBHOOKS CONCURRENTLY
        # ======================================================================
        print("\n2. Creating webhooks concurrently...")

        create_tasks = [
            client.webhooks.create(
                name="Memory Events",
                url="https://example.com/webhooks/memories",
                events=[WebhookEvent.MEMORY_CREATED, WebhookEvent.MEMORY_UPDATED],
            ),
            client.webhooks.create(
                name="Relationship Events",
                url="https://example.com/webhooks/relationships",
                events=[WebhookEvent.RELATIONSHIP_CREATED],
            ),
        ]

        webhooks = await asyncio.gather(*create_tasks)
        print(f"   Created {len(webhooks)} webhooks concurrently")

        # ======================================================================
        # PARALLEL WEBHOOK QUERIES
        # ======================================================================
        print("\n3. Querying webhooks in parallel...")

        query_tasks = [
            client.webhooks.get(wh.id) for wh in webhooks
        ]

        details = await asyncio.gather(*query_tasks)

        for wh in details:
            print(f"      - {wh.name}: {wh.events}")

        # ======================================================================
        # TEST WEBHOOKS CONCURRENTLY
        # ======================================================================
        print("\n4. Testing webhooks concurrently...")

        test_tasks = [client.webhooks.test(wh.id) for wh in webhooks]

        test_results = await asyncio.gather(*test_tasks, return_exceptions=True)

        for wh, result in zip(webhooks, test_results):
            if isinstance(result, Exception):
                print(f"      - {wh.name}: Error")
            else:
                print(f"      - {wh.name}: status={result.get('status_code')}")

        # ======================================================================
        # PARALLEL DELIVERY QUERIES
        # ======================================================================
        print("\n5. Getting deliveries in parallel...")

        delivery_tasks = [
            client.webhooks.get_deliveries(wh.id, limit=5) for wh in webhooks
        ]

        delivery_results = await asyncio.gather(*delivery_tasks)

        for wh, deliveries in zip(webhooks, delivery_results):
            print(f"      - {wh.name}: {len(deliveries.data)} deliveries")

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n6. Deleting webhooks concurrently...")

        delete_tasks = [client.webhooks.delete(wh.id) for wh in webhooks]
        await asyncio.gather(*delete_tasks)

        print(f"   Deleted {len(webhooks)} webhooks")

        print("\n" + "=" * 60)
        print("Async webhooks complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
