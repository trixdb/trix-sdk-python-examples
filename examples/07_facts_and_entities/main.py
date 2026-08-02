#!/usr/bin/env python3
"""
Facts and Entities - Synchronous Version

This example demonstrates structured knowledge extraction:
1. Creating and querying facts
2. Entity extraction and resolution
3. Fact verification
4. Entity merging

Run: python main.py
"""

from trix import Trix


def main() -> None:
    """Demonstrate facts and entities operations."""

    with Trix.from_env() as client:
        print("=" * 60)
        print("FACTS AND ENTITIES")
        print("=" * 60)

        # ======================================================================
        # CREATE ENTITIES
        # ======================================================================
        print("\n1. Creating entities...")

        # Create some entities
        python_entity = client.entities.create(
            name="Python",
            entity_type="programming_language",
            properties={"paradigm": "multi-paradigm", "typing": "dynamic"},
            aliases=["Python3", "Py"],
        )
        print(f"   ✓ Created entity: {python_entity.name} ({python_entity.id})")

        guido_entity = client.entities.create(
            name="Guido van Rossum",
            entity_type="person",
            properties={"role": "Creator of Python", "nationality": "Dutch"},
            aliases=["Guido", "BDFL"],
        )
        print(f"   ✓ Created entity: {guido_entity.name} ({guido_entity.id})")

        # ======================================================================
        # CREATE FACTS
        # ======================================================================
        print("\n2. Creating facts...")

        # Create facts linking entities
        fact1 = client.facts.create(
            subject=guido_entity.id,
            predicate="created",
            obj=python_entity.id,
            confidence=1.0,
            metadata={"year": 1991, "source": "Wikipedia"},
        )
        print(f"   ✓ Created fact: {guido_entity.name} created {python_entity.name}")

        fact2 = client.facts.create(
            subject=python_entity.id,
            predicate="has_feature",
            obj="dynamic typing",
            confidence=1.0,
        )
        print(f"   ✓ Created fact: {python_entity.name} has_feature dynamic typing")

        # ======================================================================
        # QUERY FACTS
        # ======================================================================
        print("\n3. Querying facts...")

        # Query facts about Python using list with filter
        facts = client.facts.list(subject=python_entity.id, limit=10)
        print(f"   Facts about {python_entity.name}:")
        for fact in facts.data:
            print(f"      - {fact.predicate}: {fact.object}")

        # Query by predicate
        created_facts = client.facts.list(predicate="created", limit=10)
        print(f"   Facts with predicate 'created': {len(created_facts.data)}")

        # ======================================================================
        # CREATE A MEMORY FOR EXTRACTION
        # ======================================================================
        print("\n4. Creating a memory for extraction...")

        text = "Guido van Rossum created Python in 1991. Python is used by Google and Netflix."

        # First create a memory to extract from
        extraction_memory = client.memories.create(
            content=text, metadata={"type": "extraction_demo"}
        )
        print(f"   ✓ Created memory: {extraction_memory.id}")

        # ======================================================================
        # EXTRACT ENTITIES FROM MEMORY
        # ======================================================================
        print("\n5. Extracting entities from memory...")

        extraction = client.entities.extract(memory_id=extraction_memory.id, save=False)

        print(f"   Extracted {len(extraction.entities)} entities:")
        for entity in extraction.entities:
            print(f"      - {entity.name} ({entity.entity_type})")

        # ======================================================================
        # EXTRACT FACTS FROM MEMORY
        # ======================================================================
        print("\n6. Extracting facts from memory...")

        fact_extraction = client.facts.extract(memory_id=extraction_memory.id, save=False)

        print(f"   Extracted {len(fact_extraction.facts)} facts:")
        for fact in fact_extraction.facts:
            print(f"      - {fact.subject} {fact.predicate} {fact.object}")

        # ======================================================================
        # SEARCH ENTITIES
        # ======================================================================
        print("\n7. Searching entities...")

        search_results = client.entities.search(
            query="programming language", entity_type="programming_language", limit=5
        )

        print(f"   Found {len(search_results.entities)} entities")

        # ======================================================================
        # RESOLVE ENTITY
        # ======================================================================
        print("\n8. Resolving entity references...")

        resolved = client.entities.resolve(text="Py")

        if resolved.entity:
            print(f"   'Py' resolved to: {resolved.entity.name}")

        # ======================================================================
        # VERIFY FACT
        # ======================================================================
        print("\n9. Verifying a fact...")

        # Verify the fact we created earlier
        verification = client.facts.verify(fact_id=fact1.id)

        print(f"   Verification result: {verification.is_verified}")
        print(f"   Confidence: {verification.confidence}")

        # ======================================================================
        # GET ENTITY
        # ======================================================================
        print("\n10. Getting entity details...")

        entity = client.entities.get(python_entity.id)
        print(f"   Entity: {entity.name}")
        print(f"   Type: {entity.entity_type}")
        print(f"   Properties: {entity.properties}")
        print(f"   Aliases: {entity.aliases}")

        # ======================================================================
        # UPDATE ENTITY
        # ======================================================================
        print("\n11. Updating entity...")

        updated = client.entities.update(
            python_entity.id,
            properties={"paradigm": "multi-paradigm", "typing": "dynamic", "version": "3.11"},
        )
        print(f"   ✓ Updated properties: {updated.properties}")

        # ======================================================================
        # MERGE ENTITIES
        # ======================================================================
        print("\n12. Merging duplicate entities...")

        # Create a duplicate
        dup_entity = client.entities.create(
            name="Python 3", entity_type="programming_language", properties={"version": "3.x"}
        )

        # Merge into primary (target_id absorbs source_id)
        merged = client.entities.merge(target_id=python_entity.id, source_id=dup_entity.id)
        print(f"   ✓ Merged entities: {merged.merged_count} aliases added")

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n13. Cleaning up...")

        client.facts.delete(fact1.id)
        client.facts.delete(fact2.id)
        client.memories.delete(extraction_memory.id)
        client.entities.delete(python_entity.id)
        client.entities.delete(guido_entity.id)

        print("   ✓ Cleaned up")
        print("\n" + "=" * 60)
        print("🎉 Facts and entities complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
