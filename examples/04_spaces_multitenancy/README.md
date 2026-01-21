# Spaces and Multi-tenancy

## Goal

Learn to use spaces for data isolation in multi-tenant applications.

## Prerequisites

- Completed [03_relationships](../03_relationships/)

## Concepts Covered

### 1. What are Spaces?

Spaces provide logical isolation for memories:
- Each tenant gets their own space
- Memories in one space are isolated from others
- Searches can be scoped to specific spaces

### 2. Creating Spaces

```python
space = client.spaces.create(
    name="Customer Corp",
    slug="customer-corp",  # URL-friendly identifier
    description="Space for Customer Corp data",
    metadata={"plan": "enterprise", "region": "us-east"}
)
```

### 3. Space-Scoped Operations

All major operations support `space_id`:

```python
# Create memory in a specific space
memory = client.memories.create(
    content="Tenant-specific data",
    space_id=space.id
)

# Search within a space
results = client.search.query(
    query="find something",
    space_id=space.id  # Only searches this tenant's data
)
```

### 4. Multi-tenant Pattern

```python
def get_client_for_tenant(tenant_slug: str) -> tuple[Trix, Space]:
    """Get client and space for a tenant."""
    client = Trix.from_env()
    space = client.spaces.get_by_slug(tenant_slug)
    return client, space

def create_memory_for_tenant(tenant_slug: str, content: str):
    client, space = get_client_for_tenant(tenant_slug)
    with client:
        return client.memories.create(
            content=content,
            space_id=space.id
        )
```

## Walkthrough

### Sync Version (`main.py`)

1. Creates two tenant spaces with metadata
2. Lists all spaces
3. Gets a space by its slug (URL-friendly name)
4. Creates memories isolated to each space
5. Performs space-scoped searches
6. Updates space metadata
7. Cleans up

### Async Version (`async_example.py`)

Same concepts with concurrent operations:
- Creates multiple spaces in parallel
- Creates memories in different spaces concurrently
- Runs parallel space-scoped searches

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [05_agent_sessions](../05_agent_sessions/) - Build conversational agents

