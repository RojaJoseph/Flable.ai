"""
Seed user script - Creates demo user with proper password hashing
"""

from database.connection import SessionLocal
from database.models import User
from utils.auth_utils import hash_password

def seed_user():
    """Create demo user"""
    db = SessionLocal()
    
    try:
        # Check if user exists
        existing_user = db.query(User).filter(User.email == "demo@flable.ai").first()
        
        if existing_user:
            print(f"✓ User already exists: {existing_user.email}")
            print(f"  ID: {existing_user.id}")
            print(f"  Username: {existing_user.username}")
            print(f"  Active: {existing_user.is_active}")
            
            # Update password to ensure it's properly hashed
            print("\n  Updating password to ensure proper hash...")
            existing_user.hashed_password = hash_password("demo123")
            db.commit()
            print("  ✓ Password updated!")
            return
        
        # Create new user
        print("Creating new demo user...")
        user = User(
            email="demo@flable.ai",
            username="demo_user",
            hashed_password=hash_password("demo123"),
            full_name="Demo User",
            company_name="Demo Company",
            is_active=True,
            is_verified=True
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"\n✓ User created successfully!")
        print(f"  Email: {user.email}")
        print(f"  Username: {user.username}")
        print(f"  Password: demo123")
        print(f"  ID: {user.id}")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  FLABLE.AI - User Seed Script")
    print("=" * 60)
    print()
    
    seed_user()
    
    print()
    print("=" * 60)
    print("  Done! You can now login with:")
    print("  Email: demo@flable.ai")
    print("  Password: demo123")
    print("=" * 60)
