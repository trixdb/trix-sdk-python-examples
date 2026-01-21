# Personal Knowledge Base Use Case

A personal knowledge management system for storing, organizing, and retrieving information.

## Features

- **Note Storage**: Store notes with tags and metadata
- **Search**: Full-text and semantic search
- **Linking**: Connect related notes
- **Auto-organization**: Automatic clustering
- **Tag-based Retrieval**: Find notes by topic

## Usage

```python
from trix import Trix

with Trix.from_env() as client:
    kb = PersonalKnowledgeBase(client)
    
    # Add notes
    note_id = kb.add_note(
        content="Python list comprehensions are powerful",
        tags=["python", "tips"],
        source="documentation"
    )
    
    # Search
    results = kb.search("Python syntax")
    
    # Link related notes
    kb.link_notes(note_id_1, note_id_2, relationship="extends")
    
    # Auto-organize
    kb.auto_organize()
```

## Running

```bash
python main.py
```

