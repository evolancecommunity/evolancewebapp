#!/usr/bin/env python3
"""
Create admin user in MongoDB Atlas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import get_password_hash, db
import asyncio

async def create_admin_user():
    """Create admin user in the database"""
    
    print("👤 Creating admin user...")
    
    # Check if admin user already exists
    existing_admin = await db.users.find_one({"email": "admin@evolance.com"})
    
    if existing_admin:
        print("⚠️ Admin user already exists!")
        return
    
    # Create admin user
    admin_user = {
        "id": "admin-001",
        "email": "admin@evolance.com",
        "full_name": "Admin User",
        "hashed_password": get_password_hash("admin123"),
        "is_active": True,
        "personality_test_completed": True,
        "spiritual_level": 100,
        "created_at": "2024-01-01T00:00:00Z"
    }
    
    try:
        result = await db.users.insert_one(admin_user)
        print(f"✅ Admin user created successfully!")
        print(f"   Email: admin@evolance.com")
        print(f"   Password: admin123")
        print(f"   User ID: {result.inserted_id}")
        
        # Verify the user was created
        created_user = await db.users.find_one({"email": "admin@evolance.com"})
        if created_user:
            print(f"✅ User verified in database")
        else:
            print(f"❌ User not found in database")
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == "__main__":
    asyncio.run(create_admin_user()) 