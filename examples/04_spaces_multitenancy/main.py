#!/usr/bin/env python3
"""
Spaces and Multi-tenancy - Synchronous Version

This example demonstrates space management for multi-tenant applications:
1. Creating and managing spaces
2. Isolating memories per tenant
3. Space-scoped operations

Run: python main.py
"""

from trix import Trix


def main() -> None:
    """Demonstrate space management for multi-tenancy."""
    
    with Trix.from_env() as client:
        print("=" * 60)
        print("SPACES AND MULTI-TENANCY")
        print("=" * 60)
        
        # ======================================================================
        # CREATE SPACES
        # ======================================================================
        print("\n1. Creating tenant spaces...")
        
        # Create spaces for different tenants
        tenant_a = client.spaces.create(
            name="Tenant A",
            slug="tenant-a",
            description="Space for Tenant A's data",
            metadata={"plan": "enterprise", "region": "us-east"}
        )
        print(f"   ✓ Created: {tenant_a.name} ({tenant_a.slug})")
        
        tenant_b = client.spaces.create(
            name="Tenant B",
            slug="tenant-b",
            description="Space for Tenant B's data",
            metadata={"plan": "pro", "region": "eu-west"}
        )
        print(f"   ✓ Created: {tenant_b.name} ({tenant_b.slug})")
        
        # ======================================================================
        # LIST SPACES
        # ======================================================================
        print("\n2. Listing all spaces...")
        
        spaces = client.spaces.list()
        print(f"   Found {len(spaces.data)} spaces:")
        for space in spaces.data:
            print(f"      - {space.name} ({space.slug})")
        
        # ======================================================================
        # GET SPACE BY SLUG
        # ======================================================================
        print("\n3. Getting space by slug...")
        
        space = client.spaces.get_by_slug("tenant-a")
        print(f"   Found: {space.name}")
        print(f"   Metadata: {space.metadata}")
        
        # ======================================================================
        # CREATE MEMORIES IN SPECIFIC SPACES
        # ======================================================================
        print("\n4. Creating space-isolated memories...")
        
        # Create memory in Tenant A's space
        mem_a = client.memories.create(
            content="This data belongs to Tenant A.",
            space_id=tenant_a.id,
            tags=["tenant-a", "private"]
        )
        print(f"   ✓ Created memory in Tenant A: {mem_a.id}")
        
        # Create memory in Tenant B's space
        mem_b = client.memories.create(
            content="This data belongs to Tenant B.",
            space_id=tenant_b.id,
            tags=["tenant-b", "private"]
        )
        print(f"   ✓ Created memory in Tenant B: {mem_b.id}")
        
        # ======================================================================
        # SPACE-SCOPED SEARCH
        # ======================================================================
        print("\n5. Space-scoped search...")
        
        # Search only in Tenant A's space
        results_a = client.search.query(
            query="tenant data",
            space_id=tenant_a.id,
            limit=10
        )
        print(f"   Tenant A results: {len(results_a.results)}")
        
        # Search only in Tenant B's space
        results_b = client.search.query(
            query="tenant data",
            space_id=tenant_b.id,
            limit=10
        )
        print(f"   Tenant B results: {len(results_b.results)}")
        
        # ======================================================================
        # UPDATE SPACE
        # ======================================================================
        print("\n6. Updating space...")
        
        updated = client.spaces.update(
            tenant_a.id,
            description="Updated description for Tenant A",
            metadata={"plan": "enterprise", "region": "us-east", "upgraded": True}
        )
        print(f"   ✓ Updated: {updated.description}")
        
        # ======================================================================
        # GET SPACE BY ID
        # ======================================================================
        print("\n7. Getting space by ID...")
        
        retrieved = client.spaces.get(tenant_a.id)
        print(f"   Retrieved: {retrieved.name}")
        print(f"   Description: {retrieved.description}")
        
        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n8. Cleaning up...")
        
        # Delete memories first
        client.memories.delete(mem_a.id)
        client.memories.delete(mem_b.id)
        
        # Then delete spaces
        client.spaces.delete(tenant_a.id)
        client.spaces.delete(tenant_b.id)
        
        print("   ✓ Cleaned up all spaces and memories")
        
        print("\n" + "=" * 60)
        print("🎉 Spaces and multi-tenancy complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()

