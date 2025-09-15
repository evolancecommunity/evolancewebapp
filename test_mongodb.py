#!/usr/bin/env python3
"""
Test MongoDB Atlas connection for Evolance app
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

def test_mongodb_connection():
    """Test connection to MongoDB Atlas"""
    
    # MongoDB Atlas connection string
    uri = "mongodb+srv://evolance-waitlist:unumau@evolance-waitlist.oy1zgcg.mongodb.net/?retryWrites=true&w=majority&appName=evolance-waitlist"
    
    print("🔌 Testing MongoDB Atlas connection...")
    print(f"URI: {uri}")
    print()
    
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # List databases
        print("\n📊 Available databases:")
        for db_name in client.list_database_names():
            print(f"   - {db_name}")
        
        # Test creating a collection
        db = client['evolance_db']
        collection = db['test_collection']
        
        # Insert a test document
        test_doc = {
            "test": True,
            "message": "MongoDB connection successful",
            "timestamp": "2024-01-01"
        }
        
        result = collection.insert_one(test_doc)
        print(f"\n✅ Test document inserted with ID: {result.inserted_id}")
        
        # Find the document
        found_doc = collection.find_one({"test": True})
        print(f"✅ Test document retrieved: {found_doc}")
        
        # Clean up - delete test document
        collection.delete_one({"test": True})
        print("✅ Test document cleaned up")
        
        # Close connection
        client.close()
        print("\n🔌 MongoDB connection test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    test_mongodb_connection() 