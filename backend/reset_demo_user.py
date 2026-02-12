"""
Reset Demo User - Creates or updates demo user with proper password hash
"""
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import User
from utils.auth_utils import hash_password
import sys

def reset_demo_user():
    """Reset or create demo user with proper password hash"""
    print("Resetting demo user...")
    db = SessionLocal()
    
    try:
        # Check if user exists
        existing_user = db.query(User).filter(User.email == "demo@flable.ai").first()
        
        if existing_user:
            print(f"Found existing user: {existing_user.email}")
            # Update password
            existing_user.hashed_password = hash_password("demo123")
            db.commit()
            print("✓ Password updated successfully!")
        else:
            print("Creating new demo user...")
            # Create user
            user = User(
                email="demo@flable.ai",
                username="demo_user",
                hashed_password=hash_password("demo123"),
                full_name="Demo User",
                role="admin",
                is_active=True,
                is_verified=True
            )
            db.add(user)
            db.commit()
            print("✓ User created successfully!")
        
        print("\nLogin Credentials:")
        print("Email: demo@flable.ai")
        print("Password: demo123")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    reset_demo_user()
