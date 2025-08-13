#!/usr/bin/env python3
"""
Test database functionality independently
"""

from database import Database
import hashlib

def test_database():
    print("Testing Database Functionality...")
    print("=" * 40)
    
    # Create database instance
    db = Database()
    
    # Initialize database
    print("Initializing database...")
    db.initialize_database()
    
    # Test user creation
    print("\nTesting user creation...")
    test_name = "Test User"
    test_email = "test@example.com"
    test_password = "testpass123"
    test_role = "student"
    
    # Hash password
    hashed_password = hashlib.sha256(test_password.encode()).hexdigest()
    print(f"Original password: {test_password}")
    print(f"Hashed password: {hashed_password}")
    
    try:
        # Create user
        user_id = db.create_user(test_name, test_email, hashed_password, test_role)
        print(f"✓ User created successfully with ID: {user_id}")
        
        # Try to retrieve user
        user = db.get_user_by_email(test_email)
        if user:
            print(f"✓ User retrieved successfully:")
            print(f"  ID: {user['id']}")
            print(f"  Name: {user['name']}")
            print(f"  Email: {user['email']}")
            print(f"  Role: {user['role']}")
            print(f"  Stored password hash: {user['password']}")
            print(f"  Password match: {user['password'] == hashed_password}")
        else:
            print("✗ Failed to retrieve user")
            
        # Test login simulation
        print(f"\nTesting login simulation...")
        login_password = "testpass123"
        login_hash = hashlib.sha256(login_password.encode()).hexdigest()
        print(f"Login password: {login_password}")
        print(f"Login hash: {login_hash}")
        print(f"Hash match: {login_hash == hashed_password}")
        
        if login_hash == hashed_password:
            print("✓ Login would succeed!")
        else:
            print("✗ Login would fail!")
            
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Show all users
    print(f"\nAll users in database:")
    users = db.get_all_users()
    for user in users:
        print(f"  - {user['name']} ({user['email']}) - {user['role']}")
    
    print(f"\nTotal users: {db.get_total_users()}")

if __name__ == "__main__":
    test_database()
