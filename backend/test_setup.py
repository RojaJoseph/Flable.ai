"""
Quick test script to verify setup works
Run this BEFORE pushing to Render
"""
import sys

def test_imports():
    """Test if all imports work"""
    print("Testing imports...")
    try:
        import fastapi
        import sqlalchemy
        import pydantic
        import argon2
        from jose import jwt
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_password_hash():
    """Test if password hashing works"""
    print("\nTesting password hashing...")
    try:
        from argon2 import PasswordHasher
        ph = PasswordHasher()
        
        # Test hash
        password = "test123"
        hashed = ph.hash(password)
        print(f"✅ Hash created: {hashed[:40]}...")
        
        # Test verify
        ph.verify(hashed, password)
        print("✅ Password verification works!")
        return True
    except Exception as e:
        print(f"❌ Password hashing failed: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\nTesting database...")
    try:
        from database.connection import engine, Base
        from database.models import User
        
        # Try to create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created!")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    print("=" * 60)
    print("  FLABLE.AI - PRE-DEPLOYMENT TEST")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Password Hashing", test_password_hash()))
    results.append(("Database", test_database()))
    
    # Summary
    print("\n" + "=" * 60)
    print("  TEST RESULTS")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:.<40} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Ready to deploy to Render!")
        print("\nNext steps:")
        print("  git add .")
        print("  git commit -m 'Switch to Argon2 - complete fix'")
        print("  git push")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Fix the errors above before deploying.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
