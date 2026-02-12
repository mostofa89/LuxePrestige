from backends.models import Membership

try:
    m = Membership.objects.create(
        name="Test Membership",
        tier="bronze",
        price=9.99,
        description="Test description",
        benefits="Test benefit 1\nTest benefit 2",
        discount_percentage=5.00,
        is_active=True,
        is_featured=False
    )
    print(f"✓ Created membership ID {m.id}")
    print(f"  Name: {m.name}")
    print(f"  Tier: {m.tier}")
    print(f"  Price: {m.price}")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
