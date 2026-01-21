# Research Assistant Use Case

A research assistant that ingests documents, extracts knowledge, and answers questions.

## Features

- **Document Ingestion**: Store and index documents
- **Entity Extraction**: Automatically extract entities
- **Fact Extraction**: Extract structured facts
- **Search**: Semantic search across documents
- **Question Answering**: Answer questions from knowledge base

## Usage

```python
from trix import Trix

with Trix.from_env() as client:
    assistant = ResearchAssistant(client, "My Research Project")
    
    # Ingest documents
    assistant.ingest_document(
        content="Python was created by Guido van Rossum.",
        source="wikipedia",
        extract_entities=True
    )
    
    # Search
    results = assistant.search_documents("Python creator")
    
    # Get facts
    facts = assistant.get_facts_about("Python")
    
    # Answer questions
    answer = assistant.answer_question("Who created Python?")
```

## Running

```bash
python main.py
```

