from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from evolancewebapp.backend.server import ButtonClickEvent 
from evolancewebapp.backend.server import ButtonLog
import logging

# Configure logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ButtonLogService:
    def __init__(self):
        self.db = None

    async def initialize(self):
        """Initializes the service with the MongoDB database object."""
        self.db = await MongoDBManager().connect_to_mongo()
        self.collection = self.db["button_clicks"]
        logger.info("Button log service initialized with MongoDB connection.")

    async def insert_button_click(self, event_data: ButtonClickEvent) -> str:
        """
        Inserts a new button click log entry into MongoDB.
        Returns the ID of the inserted document.
        """    
        if not self.collection:
            logger.error("MongoDB collection not initialized. Cannot insert button click log entry.")
            raise ConnectionError("MongoDB connection not established.")
        
        # Create a ButtonClickLog instance to ensure all fields are present and typed correctly
        log_entry = ButtonClickEvent(
            user_id=event_data.user_id,
            button_name=event_data.button_name,
            action_description=event_data.action_description
        )

        try:
            result = await self.collection.insert_one(log_entry.model_dump(by_alias=True))
            logger.info(f"Button click log entry inserted with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to insert button click log entry: {e}")
            raise ConnectionError(f"Database error: {e}")
    async def get_all_button_clicks(self):
        if not self.collection:
            logger.error("MongoDB collection not initialized. Cannot retrieve button click log entries.")
            return[]
        try:
            clicks=[]
            async for doc in self.collection.find({}).sort("timestamp", -1):
                clicks.append(ButtonClickEvent(**doc))
            logger.info(f"Retrieved {len(clicks)} button click log entries from MongoDB.")    
            return clicks
        except Exception as e:
            logger.error(f"Failed to retrieve button click log entries: {e}")
            return []
        
        
button_log_service = ButtonLogService()        