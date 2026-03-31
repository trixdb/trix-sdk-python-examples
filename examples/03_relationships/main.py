#!/usr/bin/env python3
"""
Relationships - Synchronous Version

This example demonstrates relationship management:
1. Creating relationships between memories
2. Reinforcing and weakening relationships
3. Traversing relationship graphs
4. Finding related memories

Run: python main.py
"""

from trix import Trix
from trix.types import MemoryCreate, RelationshipType


def main() -> None:
    """Demonstrate relationship operations."""
    
    with Trix.from_env() as client:
        print("=" * 60)
        print("RELATIONSHIPS")
        print("=" * 60)
        
        # ======================================================================
        # SETUP - Create memories to link
        # ======================================================================
        print("\n1. Creating memories to connect...")
        
        mem_data = [
            ("Python is a programming language.", ["python"]),
            ("Django is a Python web framework.", ["django"]),
            ("Flask is another Python web framework.", ["flask"]),
            ("FastAPI is a modern Python API framework.", ["fastapi"]),
        ]
        memories = [client.memories.create(content=c, tags=t) for c, t in mem_data]

        python_mem = memories[0]
        django_mem = memories[1]
        flask_mem = memories[2]
        fastapi_mem = memories[3]
        
        print(f"   ✓ Created {len(memories)} memories")
        
        # ======================================================================
        # CREATE RELATIONSHIPS
        # ======================================================================
        print("\n2. Creating relationships...")
        
        # Django is built_with Python
        rel1 = client.relationships.create(
            source_id=django_mem.id,
            target_id=python_mem.id,
            relationship_type=RelationshipType.RELATED_TO,
            weight=0.9,
        )
        print(f"   ✓ Django -> Python: {rel1.id}")
        
        # Flask is built_with Python
        rel2 = client.relationships.create(
            source_id=flask_mem.id,
            target_id=python_mem.id,
            relationship_type=RelationshipType.RELATED_TO,
            weight=0.9,
        )
        print(f"   ✓ Flask -> Python: {rel2.id}")
        
        # FastAPI is built_with Python
        rel3 = client.relationships.create(
            source_id=fastapi_mem.id,
            target_id=python_mem.id,
            relationship_type=RelationshipType.RELATED_TO,
            weight=0.9,
        )
        print(f"   ✓ FastAPI -> Python: {rel3.id}")
        
        # Django and Flask are similar
        rel4 = client.relationships.create(
            source_id=django_mem.id,
            target_id=flask_mem.id,
            relationship_type=RelationshipType.SIMILAR_TO,
            bidirectional=True,
            weight=0.7,
        )
        print(f"   ✓ Django <-> Flask (bidirectional): {rel4.id}")
        
        # ======================================================================
        # GET RELATIONSHIPS
        # ======================================================================
        print("\n3. Getting relationships...")
        
        # Get outgoing relationships from Python
        outgoing = client.relationships.get_outgoing(python_mem.id)
        print(f"   Python has {len(outgoing.data)} outgoing relationships")
        
        # Get incoming relationships to Python
        incoming = client.relationships.get_incoming(python_mem.id)
        print(f"   Python has {len(incoming.data)} incoming relationships")
        for rel in incoming.data:
            print(f"      <- {rel.source_id} ({rel.relationship_type})")
        
        # ======================================================================
        # REINFORCE RELATIONSHIP
        # ======================================================================
        print("\n4. Reinforcing relationship...")
        
        reinforced = client.relationships.reinforce(
            rel1.id,
            boost=0.1  # Increase weight by 0.1
        )
        print(f"   New weight: {reinforced.weight} (was {rel1.weight})")
        
        # ======================================================================
        # WEAKEN RELATIONSHIP
        # ======================================================================
        print("\n5. Weakening relationship...")
        
        weakened = client.relationships.weaken(
            rel2.id,
            amount=0.2
        )
        print(f"   New weight: {weakened.weight}")
        
        # ======================================================================
        # GET RELATED MEMORIES
        # ======================================================================
        print("\n6. Finding related memories...")
        
        related = client.relationships.get_related(python_mem.id)

        print(f"   Memories related to Python:")
        for mem in related.related:
            print(f"      - {mem.memory.content[:40]}... (score: {mem.score:.2f})")
        
        # ======================================================================
        # GET RELATIONSHIP TYPES
        # ======================================================================
        print("\n7. Available relationship types...")
        
        types = client.relationships.get_types()
        print(f"   Available types:")
        for t in types[:5]:
            print(f"      - {t.name}: {t.description}")
        
        # ======================================================================
        # UPDATE RELATIONSHIP
        # ======================================================================
        print("\n8. Updating relationship...")
        
        updated = client.relationships.update(
            rel3.id,
            weight=1.0,
            description="Primary framework relationship"
        )
        print(f"   Updated weight to: {updated.weight}")
        
        # ======================================================================
        # REINFORCE GROUP
        # ======================================================================
        print("\n9. Reinforcing multiple relationships...")
        
        result = client.relationships.reinforce_group(
            relationship_ids=[rel1.id, rel2.id],
            amount=0.05
        )
        print(f"   Reinforced {result.updated_count} relationships")
        
        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n10. Cleaning up...")
        
        for rel in [rel1, rel2, rel3, rel4]:
            client.relationships.delete(rel.id)
        client.memories.bulk_delete([m.id for m in memories])
        
        print("   ✓ Cleaned up")
        print("\n" + "=" * 60)
        print("🎉 Relationships complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()

