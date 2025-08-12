from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from evolancewebapp.backend import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME
from evolancewebapp.backend.server import EmotionLog
import logging

# Configure logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class LogService:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self._connect_to_mongodb()

    def _connect_to_mongodb(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.client.admin.command('ping')
            self.db = self.client[MONGO_DB_NAME]
            self.db = self.db[MONGO_COLLECTION_NAME]
            logging.info("Successfully connected to MongoDB")

        except ConnectionFailure as e:
             logging.error(f"An unexpected error during MongoDB connection: {e}")   
             self.client = None
             self.db = None
             self.collection = None

    def insert_log_entry(self, log_entry: EmotionLog):
        if not self.collection:
            logging.error("MongoDB collection not initialized. Cannot insert log entry.")
            return False
        try:
            result = self.collection.insert_one(log_entry.model_dump(exclude_none=True, by_alias=True))
            logging.info(f"Log entry inserted with ID:{result.inserted_id}")
            return True
        
        except Exception as e:
            logging.error(f"Failed to insert log entry: {e}")
            return False

    def get_all_log_entries(self):
        if not self.connection:
            logging.error("MongoDB collection not initialized. Cannot retrieve log entries")
            return[]
        try:
            logs = list(self.collection.find({}).sort("timestamp", -1))
            # Convert ObjectId to string for JSON serialization if needed for API

            for log in logs:
                if '_id' in log:
                    log['_id'] = str(log['_id'])
            logging.info(f"Retrieved {len(logs)} log entries")        
            return logs
        except Exception as e:
            logging.error(f"Failed to retrieve log entries: {e}")
            return []
        
# Global instance of LogService to avoid reloading model on every request
log_service = LogService()    





