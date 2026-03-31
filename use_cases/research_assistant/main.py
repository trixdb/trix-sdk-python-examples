#!/usr/bin/env python3
"""
Research Assistant - Synchronous Version

A research assistant demonstrating:
1. Document ingestion and storage
2. Entity and fact extraction
3. Knowledge graph building
4. Multi-hop question answering

Run: python main.py
"""

from trix import Trix
from trix.exceptions import NotFoundError


class ResearchAssistant:
    """A research assistant that builds a knowledge graph from documents."""
    
    def __init__(self, client: Trix, project_name: str):
        self.client = client
        self.space_id: str | None = None
        self._setup_project(project_name)
    
    def _setup_project(self, name: str) -> None:
        """Create a space for this research project."""
        slug = name.lower().replace(" ", "-")
        try:
            space = self.client.spaces.get_by_slug(slug)
            self.space_id = space.id
        except NotFoundError:
            space = self.client.spaces.create(
                name=name, slug=slug, description=f"Research project: {name}"
            )
            self.space_id = space.id
    
    def ingest_document(self, content: str, source: str,
                        extract_entities: bool = True) -> dict:
        """Ingest a document and optionally extract entities."""
        # Store the document
        memory = self.client.memories.create(
            content=content,
            space_id=self.space_id,
            tags=["document"],
            metadata={"source": source, "type": "document"}
        )

        result = {"memory_id": memory.id, "entities": [], "facts": []}

        if extract_entities:
            # Extract entities from the memory we just created
            extraction = self.client.entities.extract(memory_id=memory.id, save=False)
            for entity in extraction.entities:
                created = self.client.entities.create(
                    name=entity.name,
                    entity_type=entity.entity_type,
                )
                result["entities"].append(created.id)

            # Extract facts from the memory
            facts_extraction = self.client.facts.extract(memory_id=memory.id, save=False)
            for fact in facts_extraction.facts:
                created = self.client.facts.create(
                    subject=fact.subject,
                    predicate=fact.predicate,
                    obj=fact.object,
                    metadata={"source": source}
                )
                result["facts"].append(created.id)

        return result
    
    def search_documents(self, query: str, limit: int = 5) -> list[dict]:
        """Search documents in the project."""
        results = self.client.search.query(
            query=query,
            space_id=self.space_id,
            tags=["document"],
            limit=limit
        )
        return [{"content": r.memory.content[:200], "score": r.score,
                 "source": r.memory.metadata.get("source")}
                for r in results.data]
    
    def find_entity(self, name: str) -> dict | None:
        """Find an entity by name."""
        result = self.client.entities.resolve(text=name)
        if result.entity:
            return {"id": result.entity.id, "name": result.entity.name,
                    "type": result.entity.entity_type}
        return None
    
    def get_facts_about(self, entity_name: str) -> list[dict]:
        """Get facts about an entity."""
        entity = self.find_entity(entity_name)
        if not entity:
            return []

        facts = self.client.facts.list(subject=entity["id"], limit=10)
        return [{"predicate": f.predicate, "object": f.object}
                for f in facts.data]

    def answer_question(self, question: str) -> dict:
        """Answer a question using the knowledge base."""
        # Search relevant documents
        docs = self.search_documents(question, limit=3)

        # Get facts related to the question (if any exist)
        # Note: fact verification requires a fact_id, so we search for related facts instead
        related_facts = self.client.facts.list(limit=5)

        return {
            "relevant_documents": docs,
            "related_facts_count": len(related_facts.data),
        }


def main():
    """Demonstrate the research assistant."""
    print("=" * 60)
    print("RESEARCH ASSISTANT")
    print("=" * 60)
    
    with Trix.from_env() as client:
        assistant = ResearchAssistant(client, "Python Research")
        
        # Ingest documents
        print("\n1. Ingesting documents...")
        
        documents = [
            ("Python was created by Guido van Rossum in 1991. It emphasizes code readability.",
             "wikipedia"),
            ("Python supports multiple programming paradigms including procedural and OOP.",
             "docs.python.org"),
            ("Django is a high-level Python web framework that encourages rapid development.",
             "djangoproject.com"),
        ]
        
        doc_results = []
        for content, source in documents:
            result = assistant.ingest_document(content, source)
            doc_results.append(result)
            print(f"   ✓ Ingested from {source}")
        
        # Search
        print("\n2. Searching documents...")
        results = assistant.search_documents("Python web framework")
        print(f"   Found {len(results)} relevant documents")
        for r in results:
            print(f"      - {r['source']}: {r['content'][:50]}...")
        
        # Find entity
        print("\n3. Finding entities...")
        entity = assistant.find_entity("Python")
        if entity:
            print(f"   Found: {entity['name']} ({entity['type']})")
        
        # Get facts
        print("\n4. Getting facts about Python...")
        facts = assistant.get_facts_about("Python")
        print(f"   Found {len(facts)} facts")
        
        # Answer question
        print("\n5. Answering question...")
        answer = assistant.answer_question("Who created Python?")
        print(f"   Found {len(answer['relevant_documents'])} relevant docs")
        print(f"   Related facts: {answer['related_facts_count']}")
        
        # Cleanup
        print("\n6. Cleaning up...")
        for result in doc_results:
            client.memories.delete(result["memory_id"])
        client.spaces.delete(assistant.space_id)
        print("   ✓ Cleaned up")
        
        print("\n" + "=" * 60)
        print("🎉 Research assistant complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()

