# Research Assistant Use Case

A research assistant that ingests documents, lets Trix extract knowledge from
them, and answers questions.

## How knowledge is built

Entities and facts are **not** created by hand. You ingest documents
(memories); the server extracts entities and facts from them asynchronously
via **enrichment**. The assistant then reads that derived knowledge back.

```
ingest_document(content)
   ├── memories.create(...)              # store the document
   └── enrichments.enrich(..., ENTITIES) # extract entities + facts (async)

find_entity(name)      → entities.list        (client-side name/alias match)
get_facts_about(name)  → entities.get_facts    (facts mentioning the entity)
answer_question(q)     → search.query + facts.list
```

## Features

- **Document Ingestion**: store documents in a project space
- **Knowledge Extraction**: entities/facts extracted via enrichment
- **Search**: semantic search across documents
- **Entity Lookup**: find extracted entities by name or alias
- **Question Answering**: combine document search with related facts

## Usage

```python
from trix import Trix

with Trix.from_env() as client:
    assistant = ResearchAssistant(client, "My Research Project")

    # Ingest documents (extraction happens server-side, asynchronously)
    assistant.ingest_document(
        content="Python was created by Guido van Rossum.",
        source="wikipedia",
    )

    # Search
    results = assistant.search_documents("Python creator")

    # Read extracted knowledge
    facts = assistant.get_facts_about("Python")

    # Answer questions
    answer = assistant.answer_question("Who created Python?")
```

## Running

```bash
python main.py
```
