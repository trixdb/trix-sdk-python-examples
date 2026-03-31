#!/usr/bin/env python3
"""
Webhooks - Synchronous Version

This example demonstrates webhook management:
1. Creating webhooks for events
2. Listing available event types
3. Testing webhook delivery
4. Checking webhook deliveries
5. Managing webhook lifecycle

Run: python main.py
"""

from trix import Trix
from trix.types import WebhookEvent


def main() -> None:
    """Demonstrate webhook operations."""

    with Trix.from_env() as client:
        print("=" * 60)
        print("WEBHOOKS")
        print("=" * 60)

        # ======================================================================
        # GET AVAILABLE EVENT TYPES
        # ======================================================================
        print("\n1. Getting available event types...")

        event_types = client.webhooks.get_event_types()

        print(f"   Available event types:")
        for event_type in event_types[:8]:
            print(f"      - {event_type.name}: {event_type.description}")

        # ======================================================================
        # CREATE WEBHOOK
        # ======================================================================
        print("\n2. Creating webhook...")

        webhook = client.webhooks.create(
            name="Memory Events",
            url="https://example.com/webhooks/trix",
            events=[WebhookEvent.MEMORY_CREATED, WebhookEvent.MEMORY_UPDATED],
        )

        print(f"   Created webhook: {webhook.id}")
        print(f"   URL: {webhook.url}")
        print(f"   Events: {webhook.events}")
        print(f"   Active: {webhook.active}")

        # ======================================================================
        # LIST WEBHOOKS
        # ======================================================================
        print("\n3. Listing all webhooks...")

        webhooks = client.webhooks.list()

        print(f"   Found {len(webhooks.data)} webhooks:")
        for wh in webhooks.data:
            print(f"      - {wh.id}: {wh.url} (active: {wh.active})")

        # ======================================================================
        # GET WEBHOOK
        # ======================================================================
        print("\n4. Getting webhook details...")

        retrieved = client.webhooks.get(webhook.id)
        print(f"   Webhook: {retrieved.id}")
        print(f"   URL: {retrieved.url}")
        print(f"   Events: {retrieved.events}")
        print(f"   Created: {retrieved.created_at}")

        # ======================================================================
        # UPDATE WEBHOOK
        # ======================================================================
        print("\n5. Updating webhook...")

        updated = client.webhooks.update(
            webhook.id,
            events=[
                WebhookEvent.MEMORY_CREATED,
                WebhookEvent.MEMORY_UPDATED,
                WebhookEvent.MEMORY_DELETED,
            ],
            name="All Memory Events"
        )

        print(f"   Updated events: {updated.events}")

        # ======================================================================
        # TEST WEBHOOK
        # ======================================================================
        print("\n6. Testing webhook delivery...")

        test_result = client.webhooks.test(webhook.id)

        print(f"   Test result:")
        print(f"      - Success: {test_result.get('success')}")
        print(f"      - Status code: {test_result.get('status_code')}")

        # ======================================================================
        # GET DELIVERIES
        # ======================================================================
        print("\n7. Getting webhook deliveries...")

        deliveries = client.webhooks.get_deliveries(
            webhook.id,
            limit=10
        )

        print(f"   Recent deliveries: {len(deliveries.data)}")
        for delivery in deliveries.data[:3]:
            print(f"      - {delivery.event_type} - {delivery.status_code}")

        # ======================================================================
        # ENABLE/DISABLE WEBHOOK
        # ======================================================================
        print("\n8. Disabling webhook...")

        disabled = client.webhooks.update(
            webhook.id,
            active=False
        )
        print(f"   Webhook active: {disabled.active}")

        print("\n9. Re-enabling webhook...")

        enabled = client.webhooks.update(
            webhook.id,
            active=True
        )
        print(f"   Webhook active: {enabled.active}")

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n10. Deleting webhook...")

        client.webhooks.delete(webhook.id)
        print(f"   Deleted webhook")

        print("\n" + "=" * 60)
        print("Webhooks complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
