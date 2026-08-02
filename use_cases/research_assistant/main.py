#!/usr/bin/env python3
"""
Research Assistant - Synchronous Version

A research assistant demonstrating the real, read-mostly knowledge API:
1. Document ingestion (memories) scoped to a project space
2. Knowledge extraction via ENRICHMENT (entities + facts, async server-side)
3. Semantic search across documents
4. Entity lookup and fact retrieval (read-only)

Note: entities and facts are NOT created by hand — they are extracted from
the documents you ingest. This assistant stores documents and reads back the
knowledge the server derives from them.

Run: python main.py
"""

from trix import EnrichmentOperation, Trix
from trix.exceptions import NotFoundError


class ResearchAssistant:
    """Builds a project knowledge base from ingested documents."""

    def __init__(self, client: Trix, project_name: str) -> None:
        self.client = client
        self.space_id: str | None = None
        self._setup_project(project_name)

    def _setup_project(self, name: str) -> None:
        """Create (or reuse) a space for this research project."""
        slug = name.lower().replace(" ", "-")
        try:
            space = self.client.spaces.get_by_slug(slug)
        except NotFoundError:
            space = self.client.spaces.create(
                name=name, slug=slug, description=f"Research project: {name}"
            )
        self.space_id = space.id

    def ingest_document(self, content: str, source: str) -> dict:
        """Store a document and trigger knowledge extraction (enrichment)."""
        memory = self.client.memories.create(
            content=content,
            space_id=self.space_id,
            tags=["document"],
            metadata={"source": source, "type": "document"},
        )
        # Entities + facts are extracted asynchronously by enrichment.
        enrichment = self.client.enrichments.enrich(
            memory.id,
            operations=[EnrichmentOperation.ENTITIES, EnrichmentOperation.TOPICS],
        )
        return {"memory_id": memory.id, "enrichment_status": enrichment.status}

    def search_documents(self, query: str, limit: int = 5) -> list[dict]:
        """Search documents in the project space."""
        results = self.client.search.query(
            query=query, space_id=self.space_id, tags=["document"], limit=limit
        )
        return [
            {
                "content": r.memory.content[:200],
                "score": r.score,
                "source": r.memory.metadata.get("source"),
            }
            for r in results.data
        ]

    def find_entity(self, name: str) -> dict | None:
        """Find an extracted entity by name or alias (client-side match)."""
        # For large accounts you would paginate; entities.list is read-only.
        entities = self.client.entities.list(limit=100)
        needle = name.lower()
        for entity in entities.data:
            candidates = [entity.name.lower(), *(a.lower() for a in entity.aliases)]
            if needle in candidates:
                return {"id": entity.id, "name": entity.name, "type": entity.type}
        return None

    def get_facts_about(self, entity_name: str) -> list[dict]:
        """Get facts that mention an entity (entities.get_facts)."""
        entity = self.find_entity(entity_name)
        if not entity:
            return []
        result = self.client.entities.get_facts(entity["id"])
        return [{"predicate": f.predicate, "object": f.object} for f in result.facts]

    def answer_question(self, question: str) -> dict:
        """Answer a question using documents plus related facts."""
        docs = self.search_documents(question, limit=3)
        related_facts = self.client.facts.list(limit=5)
        return {
            "relevant_documents": docs,
            "related_facts_count": len(related_facts.data),
        }


def _ingest_corpus(assistant: ResearchAssistant) -> list[dict]:
    """Ingest a small demo corpus and return the ingest results."""
    documents = [
        ("Python was created by Guido van Rossum in 1991.", "wikipedia"),
        ("Python supports procedural and object-oriented paradigms.", "docs.python.org"),
        ("Django is a high-level Python web framework.", "djangoproject.com"),
    ]
    results = []
    for content, source in documents:
        results.append(assistant.ingest_document(content, source))
        print(f"   Ingested from {source}")
    return results


def main() -> None:
    """Demonstrate the research assistant."""
    print("=" * 60)
    print("RESEARCH ASSISTANT")
    print("=" * 60)

    with Trix.from_env() as client:
        assistant = ResearchAssistant(client, "Python Research")

        print("\n1. Ingesting documents (extraction runs via enrichment)...")
        doc_results = _ingest_corpus(assistant)

        print("\n2. Searching documents...")
        for r in assistant.search_documents("Python web framework"):
            print(f"   - {r['source']}: {r['content'][:50]}...")

        print("\n3. Finding an entity...")
        entity = assistant.find_entity("Python")
        print(f"   {entity['name']} ({entity['type']})" if entity else "   (not extracted yet)")

        print("\n4. Getting facts about Python...")
        print(f"   Found {len(assistant.get_facts_about('Python'))} fact(s)")

        print("\n5. Answering a question...")
        answer = assistant.answer_question("Who created Python?")
        print(f"   {len(answer['relevant_documents'])} docs, {answer['related_facts_count']} facts")

        print("\n6. Cleaning up...")
        for result in doc_results:
            client.memories.delete(result["memory_id"])
        if assistant.space_id:
            client.spaces.delete(assistant.space_id)
        print("   Cleaned up")

    print("\n" + "=" * 60)
    print("Research assistant complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
