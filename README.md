# Trix Python SDK Examples

Official examples repository for the [Trix Python SDK](https://github.com/trixdb/trix-sdk-python).

## Quick Start

```bash
# Clone the repository
git clone https://github.com/trixdb/trix-sdk-python-examples.git
cd trix-sdk-python-examples

# Install dependencies
pip install -e .

# Set up environment
cp .env.example .env
# Edit .env with your API key

# Run an example
python examples/00_getting_started/main.py
```

## Prerequisites

- Python 3.11+
- Trix API key (get one at [trixdb.com](https://trixdb.com))

## Examples

| # | Example | Description |
|---|---------|-------------|
| 00 | [Getting Started](examples/00_getting_started/) | Client setup, first memory, basic operations |
| 01 | [Memories Basics](examples/01_memories_basics/) | CRUD, bulk operations, metadata, tags |
| 02 | [Search & Retrieval](examples/02_search_and_retrieval/) | Semantic search, similar, by_topic, filters |
| 03 | [Relationships](examples/03_relationships/) | Link memories, get_related, reinforce/weaken |
| 04 | [Spaces & Multitenancy](examples/04_spaces_multitenancy/) | Multi-tenant isolation with spaces |
| 05 | [Agent Sessions](examples/05_agent_sessions/) | Sessions, core memory, context retrieval |
| 06 | [Knowledge Graph](examples/06_knowledge_graph/) | Traverse, shortest_path, neighbors, expand |
| 07 | [Facts & Entities](examples/07_facts_and_entities/) | Extract, verify facts; resolve entities |
| 08 | [Clustering](examples/08_clustering/) | Automatic memory organization |
| 09 | [Webhooks](examples/09_webhooks/) | Event subscriptions and handling |
| 10 | [Advanced Patterns](examples/10_advanced_patterns/) | Error handling, retries, interceptors |
| 11 | [Pipeline Presets](examples/11_pipeline_presets/) | 3-tier preset resolver, account/space defaults |

Each example includes:
- `main.py` - Synchronous version
- `async_example.py` - Asynchronous version
- `test_example.py` - Tests with mocks
- `README.md` - Tutorial documentation

## Use Cases

Real-world implementations combining multiple SDK features:

| Use Case | Description |
|----------|-------------|
| [Chat Bot](use_cases/chat_bot/) | Memory-augmented conversational AI |
| [Personal Knowledge Base](use_cases/personal_knowledge_base/) | Note storage and retrieval system |
| [AI Agent Memory](use_cases/ai_agent_memory/) | Working + long-term memory for agents |
| [Research Assistant](use_cases/research_assistant/) | Document ingestion and Q&A |

## Recipes

Quick patterns for common tasks:

- [Error Handling](recipes/error_handling.py) - Exception handling patterns
- [Pagination](recipes/pagination.py) - Efficient iteration
- [Retry Strategies](recipes/retry_strategies.py) - Handling transient failures
- [Testing Patterns](recipes/testing_mock_patterns.py) - Mocking with respx

## Environment Variables

```bash
TRIX_API_KEY=your_api_key_here
TRIX_BASE_URL=https://api.trixdb.com  # Optional
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific example tests
pytest examples/00_getting_started/

# Run with coverage
pytest --cov=examples
```

## Sync vs Async

All examples support both synchronous and asynchronous usage:

**Synchronous:**
```python
from trix import Trix

with Trix.from_env() as client:
    memory = client.memories.create(content="Hello, Trix!")
```

**Asynchronous:**
```python
from trix import AsyncTrix

async with AsyncTrix.from_env() as client:
    memory = await client.memories.create(content="Hello, Trix!")
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

