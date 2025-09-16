#!/usr/bin/env python3
"""
Check MongoDB Atlas users and database info
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def check_mongodb_info():
    """Check MongoDB Atlas connection and user info"""
    
    uri = "mongodb+srv://waitlist:unumau@evolance-waitlist.oy1zgcg.mongodb.net/?retryWrites=true&w=majority&appName=evolance-waitlist"
    
    print("🔍 Checking MongoDB Atlas connection...")
    print(f"Username: waitlist")
    print(f"Password: unumau")
    print()
    
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Try to ping
        client.admin.command('ping')
        print("✅ Connection successful!")
        
        # List all databases
        print("\n📊 Available databases:")
        for db_name in client.list_database_names():
            print(f"   - {db_name}")
        
        # Check evolance_webapp database
        if 'evolance_webapp' in client.list_database_names():
            db = client['evolance_webapp']
            print(f"\n📁 Collections in evolance_webapp:")
            for collection in db.list_collection_names():
                print(f"   - {collection}")
                
            # Check if there are any users
            if 'users' in db.list_collection_names():
                users_count = db.users.count_documents({})
                print(f"\n👥 Users in database: {users_count}")
                
                # Show all users
                if users_count > 0:
                    print("\n📋 All users:")
                    for user in db.users.find():
                        print(f"   - {user.get('email', 'No email')} ({user.get('full_name', 'No name')}) - ID: {user.get('id', 'No ID')}")
        else:
            print("\n❌ evolance_webapp database not found")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Possible solutions:")
        print("1. Check if username 'evolance-waitlist' exists")
        print("2. Check if password 'unumau' is correct")
        print("3. Check if IP is whitelisted in MongoDB Atlas")
        print("4. Check if database user has proper permissions")

if __name__ == "__main__":
    check_mongodb_info() 