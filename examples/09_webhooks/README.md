# Webhooks

## Goal

Learn to set up webhooks for real-time event notifications.

## Prerequisites

- Completed [08_clustering](../08_clustering/)
- A publicly accessible URL to receive webhooks

## Concepts Covered

### 1. Creating Webhooks

```python
webhook = client.webhooks.create(
    url="https://your-server.com/webhooks/trix",
    events=["memory.created", "memory.updated", "memory.deleted"],
    description="Memory change notifications",
    secret="your-secret-for-verification"
)
```

### 2. Available Event Types

```python
event_types = client.webhooks.get_event_types()
for event in event_types.types:
    print(f"{event.name}: {event.description}")
```

Common events:
- `memory.created`, `memory.updated`, `memory.deleted`
- `relationship.created`, `relationship.deleted`
- `cluster.created`, `cluster.updated`
- `session.created`, `session.ended`

### 3. Testing Webhooks

```python
result = client.webhooks.test(webhook.id)
print(f"Success: {result.success}")
print(f"Response time: {result.response_time_ms}ms")
```

### 4. Checking Deliveries

```python
deliveries = client.webhooks.get_deliveries(webhook.id, limit=20)
for delivery in deliveries.data:
    print(f"{delivery.event_type}: {delivery.status_code}")
```

### 5. Webhook Management

```python
# Update events
client.webhooks.update(
    webhook.id,
    events=["memory.created", "relationship.created"]
)

# Disable/enable
client.webhooks.update(webhook.id, status="disabled")
client.webhooks.update(webhook.id, status="active")

# Rotate secret
client.webhooks.rotate_secret(webhook.id)

# Delete
client.webhooks.delete(webhook.id)
```

### 6. Verifying Webhook Signatures

On your server, verify the signature:

```python
import hmac
import hashlib

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## Walkthrough

### Sync Version (`main.py`)

1. Lists available event types
2. Creates a webhook for memory events
3. Lists all configured webhooks
4. Tests webhook delivery
5. Checks delivery history
6. Enables/disables webhook
7. Rotates webhook secret
8. Cleans up

### Async Version (`async_example.py`)

Parallel operations:
- Creates multiple webhooks concurrently
- Tests webhooks in parallel
- Parallel delivery queries

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [10_advanced_patterns](../10_advanced_patterns/) - Error handling, retries, interceptors

