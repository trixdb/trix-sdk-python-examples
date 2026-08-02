#!/usr/bin/env python3
"""
Personal Knowledge Base - Synchronous Version

A personal knowledge management system demonstrating:
1. Memory organization with tags and metadata
2. Full-text and semantic search
3. Relationship-based knowledge linking
4. Clustering for automatic organization

Run: python main.py
"""

from trix import Trix
from trix.exceptions import NotFoundError
from trix.types import RelationshipType


class PersonalKnowledgeBase:
    """A personal knowledge base using Trix."""

    def __init__(self, client: Trix, space_slug: str = "personal-kb"):
        self.client = client
        self.space_id: str | None = None
        self._setup_space(space_slug)

    def _setup_space(self, slug: str) -> None:
        """Create or get the knowledge base space."""
        try:
            space = self.client.spaces.get_by_slug(slug)
            self.space_id = space.id
        except NotFoundError:
            space = self.client.spaces.create(
                name="Personal Knowledge Base",
                slug=slug,
                description="My personal knowledge repository",
            )
            self.space_id = space.id

    def add_note(
        self, content: str, tags: list[str] | None = None, source: str | None = None
    ) -> str:
        """Add a note to the knowledge base."""
        memory = self.client.memories.create(
            content=content,
            tags=tags or [],
            space_id=self.space_id,
            metadata={"type": "note", "source": source} if source else {"type": "note"},
        )
        return memory.id

    def link_notes(self, source_id: str, target_id: str, relationship: str = "related") -> str:
        """Create a link between two notes."""
        rel = self.client.relationships.create(
            source_id=source_id,
            target_id=target_id,
            relationship_type=RelationshipType.RELATED_TO,
            description=relationship,
        )
        return rel.id

    def search(self, query: str, limit: int = 10) -> list[dict]:
        """Search the knowledge base."""
        results = self.client.search.query(query=query, space_id=self.space_id, limit=limit)
        return [
            {"id": r.memory.id, "content": r.memory.content, "score": r.score} for r in results.data
        ]

    def find_related(self, note_id: str) -> list[dict]:
        """Find notes related to a given note."""
        related = self.client.relationships.get_related(note_id)
        return [
            {"id": m.memory.id, "content": m.memory.content, "score": m.score}
            for m in related.related
        ]

    def get_by_tag(self, tag: str, limit: int = 20) -> list[dict]:
        """Get all notes with a specific tag."""
        results = self.client.memories.list(tags=[tag], space_id=self.space_id, limit=limit)
        return [{"id": m.id, "content": m.content} for m in results.data]

    def auto_organize(self) -> dict:
        """Automatically organize notes into clusters."""
        # Get all notes
        notes = list(self.client.memories.iter(space_id=self.space_id, page_size=100))

        if len(notes) < 3:
            return {"clusters_created": 0, "notes_organized": 0}

        # Create a cluster and add notes
        cluster = self.client.clusters.create(
            name="Auto-organized", description="Automatically organized notes"
        )
        for note in notes:
            self.client.clusters.add_memory(cluster.id, note.id)

        return {"clusters_created": 1, "notes_organized": len(notes)}


def main():
    """Demonstrate the personal knowledge base."""
    print("=" * 60)
    print("PERSONAL KNOWLEDGE BASE")
    print("=" * 60)

    with Trix.from_env() as client:
        kb = PersonalKnowledgeBase(client)

        # Add some notes
        print("\n1. Adding notes...")

        notes = [
            ("Python decorators modify function behavior.", ["python", "programming"]),
            ("FastAPI uses Python type hints for validation.", ["python", "fastapi", "web"]),
            ("SQLAlchemy is an ORM for Python.", ["python", "database"]),
            ("PostgreSQL supports JSON columns natively.", ["database", "postgres"]),
            ("REST APIs typically use JSON for data exchange.", ["web", "api"]),
        ]

        note_ids = []
        for content, tags in notes:
            note_id = kb.add_note(content, tags=tags)
            note_ids.append(note_id)
            print(f"   ✓ Added: {content[:40]}...")

        # Link related notes
        print("\n2. Linking related notes...")
        kb.link_notes(note_ids[0], note_ids[1], "related")  # decorators -> fastapi
        kb.link_notes(note_ids[1], note_ids[2], "uses")  # fastapi -> sqlalchemy
        print("   ✓ Created links")

        # Search
        print("\n3. Searching...")
        results = kb.search("Python web framework")
        print(f"   Found {len(results)} results:")
        for r in results[:3]:
            print(f"      - {r['content'][:40]}... (score: {r['score']:.2f})")

        # Find by tag
        print("\n4. Finding by tag 'python'...")
        python_notes = kb.get_by_tag("python")
        print(f"   Found {len(python_notes)} notes with 'python' tag")

        # Find related
        print("\n5. Finding related notes...")
        related = kb.find_related(note_ids[0])
        print(f"   Notes related to first note: {len(related)}")

        # Auto-organize
        print("\n6. Auto-organizing with clustering...")
        org_result = kb.auto_organize()
        print(f"   Created {org_result['clusters_created']} clusters")

        # Cleanup
        print("\n7. Cleaning up...")
        client.memories.bulk_delete(note_ids)
        client.spaces.delete(kb.space_id)
        print("   ✓ Cleaned up")

        print("\n" + "=" * 60)
        print("🎉 Personal knowledge base complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
