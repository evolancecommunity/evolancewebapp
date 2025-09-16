from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from backend.services.data_service import get_psychology_book_suggestions
from backend.services.data_service import get_meditation_book_suggestions
from backend.services.log_service import log_service
from backend.services.ai_response_generator import process_user_input_for_ai_response

import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any

import uuid
from datetime import datetime, timedelta, date
import hashlib
import jwt
from passlib.context import CryptContext
import openai
from openai import OpenAI
from bson import ObjectId

from evolancewebapp.backend.server import ALGORITHM


from bson import ObjectId


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]
customer_collection = db.get_collection("customers")
interaction_collection = db.get_collection("interactions")


# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Global variable for sentiment_pipeline
sentiment_pipeline = None


# Connect MongoDB and Hugging Face Transformers on startup

@api_router.on_event("startup")
async def connect_to_mongodb_and_load_models():

# Helper Function for MongoDB

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod


# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
# ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OpenAI setup
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if OPENAI_API_KEY and OPENAI_API_KEY != 'your-openai-api-key-here':
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create the main app without a prefix
app = FastAPI(title="TimeSoul API", description="API for TimeSoul - Evolance spiritual wellness app")




# User Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    full_name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    personality_test_completed: bool = False
    spiritual_level: int = 0
    profile_picture: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    personality_test_completed: bool
    spiritual_level: int
    profile_picture: Optional[str] = None

# Personality Test Models
class PersonalityQuestion(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    options: List[str]
    category: str

class PersonalityAnswer(BaseModel):
    question_id: str
    answer_index: int
    answer_text: str

class PersonalityTestSubmission(BaseModel):
    answers: List[PersonalityAnswer]

class PersonalityResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    answers: List[PersonalityAnswer]
    emotional_quotient_score: int
    personality_type: str
    spiritual_inclination: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Story Models
class Story(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    content: str
    category: str
    difficulty_level: int
    estimated_duration: str
    acceptance_threshold: int = 80
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserStoryProgress(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    story_id: str
    status: str = "not_started"  # not_started, in_progress, completed, revisited
    acceptance_level: int = 0
    ai_confirmed: bool = False
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)

# Chat Models
class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    message: str
    is_user: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    story_context: Optional[str] = None

# Video Models
class VideoLesson(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    mentor_name: str
    video_url: str
    thumbnail_url: str
    duration: str
    category: str
    difficulty_level: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

class VideoReview(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    video_id: str
    rating: int
    review_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class VideoReviewCreate(BaseModel):
    video_id: str
    rating: int
    review_text: str

# Todo Models
class Todo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    story_id: str
    title: str
    description: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class TodoCreate(BaseModel):
    story_id: str
    title: str
    description: str

# NEW: Consciousness Timeline Models
class SelfState(BaseModel):
    fulfillment_level: int  # 0-100
    happiness_level: int    # 0-100
    clarity_level: int      # 0-100
    confidence_level: int   # 0-100
    description: str
    key_characteristics: List[str]
    dominant_emotions: List[str]
    life_priorities: List[str]

class DecisionOption(BaseModel):
    title: str
    description: str
    potential_outcomes: List[str]
    confidence_score: int  # 0-100

class ConsciousnessDecision(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    decision_title: str
    decision_description: str
    decision_context: str
    decision_options: List[DecisionOption]
    past_self: SelfState
    present_self: SelfState
    future_self: SelfState
    overall_fulfillment_trend: str  # "ascending", "stable", "descending"
    decision_status: str = "contemplating"  # contemplating, decided, implemented
    chosen_option_index: Optional[int] = None
    ai_insights: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class DecisionCreate(BaseModel):
    decision_title: str
    decision_description: str
    decision_context: str
    decision_options: List[DecisionOption]

class FulfillmentEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    decision_id: Optional[str] = None
    fulfillment_level: int
    happiness_level: int
    clarity_level: int
    confidence_level: int
    notes: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class FulfillmentCreate(BaseModel):
    decision_id: Optional[str] = None
    fulfillment_level: int
    happiness_level: int
    clarity_level: int
    confidence_level: int
    notes: str

# Token Model
class Token(BaseModel):
    access_token: str
    token_type: str


class UserInput(BaseModel):
    user_id: str
    conversation_id: str
    turn_number: int
    message: str

class AIResponse(BaseModel):
    ai_response: str
    emojics: str
    detected_emotion: str
    reason_for_emotion: str
    suggested_psych_books: list
    suggested_meditation_books: list  
    message: str
    event_id: str
    timestamp: datetime

class ConversationLogEntry(BaseModel):
    user_id: str
    conversation_id: str
    turn_number: int
    user_message: str
    ai_full_response: AIResponse
    timestamp: datetime

class EmotionData(BaseModel):
    emotion: str
    score: float
    emojics: str
    reason: Optional[str] = None

class EmotionLog(BaseModel):
    user_id: str
    timestamp: datetime
    user_input: str
    detected_emotion: str
    ai_response: str
    suggested_psych_books: List[str]
    suggested_meditation_books: List[str]
    emojics: str
    reason_for_emotion: str

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat() + "z"
        }
# Button Model for emolytics

class ButtonClickEvent(BaseModel):
   """
   Pydantic model for the data received when a button is clicked.
   """    
   user_id: str
   button_name: str
   action_description: Optional[str]

class ButtonClickLog(BaseModel):
  """
  Pydantic model for the data stored in MongoDB.
  Includes a timestamp for when the event occurred.
  """   
  id: str 
  timestamp: datetime = Field(default_factory=datetime.date)
  user_id: str
  button_name: str
  action_description: Optional[str]

# Customer Model
class Customer(BaseModel):
   id: str = Field(default_factory=lambda: str(uuid.uuid4()))
   name: str = Field(..., example="Ramona Naidoo")
   email: str = Field(..., example="ramona.naidoo@example.com")
   phone: Optional[str] = Field(None, example="+27123456789")
   address: Optional[str] = Field(None, example="123 Main St, Cape Town, South Africa")
   time_zone: Optional[str] = Field(None, example="Central African Time")
   created_at: datetime = Field(default_factory=datetime.date)
   updated_at: datetime = Field(default_factory=datetime.date)

# Model for customer and evolance representation interaction
class Interaction(BaseModel):

   id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
   customer_message: str = Field(..., example="I am very satisfied with the service.")
   evolance_response: str = Field(..., example="We apologize for the inconvenience. How can we assist you further?")
   evolance_sentiment_label: str = Field(..., example="POSITIVE")
   evolance_sentiment_score: float = Field(..., example=0.98)
   customer_sentiment_label: str = Field(..., example="Negative")
   customer_sentiment_score: float = Field(..., example=0.99)
   timestamp: datetime = Field(default_factory=datetime.date)

# Create a new interaction
class InteractionCreate(BaseModel):
   customer_message: str = Field(..., example="How do I create an account or sign up?")
   evolance_response: str = Field(..., example="Welcome! You can create an account by providing a valid email address, a secure password, and your full name on the sign-up page. The system will create a new user ID for you, which will be the basis for all your data and progress in the app.")

# Sentiment analysis result
class SentimentResult(BaseModel):
   label: str = Field(..., example="POSITIVE")
   score: float = Field(..., example=0.98)

# Response after sentiment analysis
class AnalyzedInteractionResponse(BaseModel):
   id: str = Field(..., example="64f0c9e2b5e4c3a1d2f3e4b5")
   customer_message: str = Field(..., example="I am very satisfied with the service.")
   evolance_response: str = Field(..., example="We apologize for the inconvenience. How can we assist you further?")
   evolance_sentiment: SentimentResult
   customer_sentiment: SentimentResult
   timestamp: datetime = Field(..., example="2023-10-05T14:48:00.000Z")      

# configurations for interaction model between customer and evolance representative

class Config:
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}
    populated_by_name = True

# Configurations for Customer Model
class Config:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {
         datetime: lambda dt: dt.isoformat() + "z",
         ObjectId: str
        }
    schema_extra = {
        "example": {
            "name": "Ramona Naidoo",
            "email": "ramona.naidoo@example.com",
            "phone": "+27123456789",
            "address" : "123 Main St, Cape Town, South Africa",
            "company": "Evolance"
        }
    }


    if "description" in update_data:
        sentimental_result = sentiment_pipeline(update_data["description"])[0]
        update_data["sentiment"] = sentimental_result['label']
        update_data["sentiment_score"] = sentimental_result['score']

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_result = await support_tickets_collection.update_one({"_id": ObjectId(ticket_id)}, {"$set": update_data})

    if update_result.modified_count == 1:
        updated_ticket = await support_tickets_collection.find_one({"_id": ObjectId(ticket_id)})
        return SupportTicket(**updated_ticket)
    raise HTTPException(status_code=404, detail="Support ticket not found or no changes made")    

@api_router.delete("/tickets/{ticket_id}", summary="Delete a support ticket")
async def delete_support_ticket(ticket_id: str):
    """Deletes a support ticket from the system."""
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")

    delete_result = await support_tickets_collection.delete_one({"_id": ObjectId(ticket_id)})
    if delete_result.deleted_count == 1:
        return {"detail": "Support ticket deleted successfully"}
    raise HTTPException(status_code=404, detail="Support ticket not found")

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to the CRM Support API! Use /api/docs for documentation."}    

# FastAPI endpoints - Customer 

@api_router.post("/customers/", response_model=Customer, summary="Create a new customer")
async def create_customer(customer: Customer):
    """Create a new customer in the database."""
    customer_data = customer.model_dump()
    result = await customer_collection.insert_one(customer_data)
    new_customer = await customer_collection.find_one({"_id": result.inserted_id})
    return Customer(**new_customer)

@api_router.get("/customers/", response_model=List[Customer], summary="Get all customers")
async def get_customers():
    """Retrieve all customers from the database."""
    customers = []
    async for customer in customer_collection.find():
        customers.append(Customer(**customer))
    return customers

@api_router.get("/customers/{customer_id}", response_model=Customer, summary="Get a customer by ID")
async def get_customer(customer_id: str):
    """Retrieve a customer by their ID."""
    if not ObjectId.is_valid(customer_id):
        raise HTTPException(status_code=400, detail="Invalid customer ID format")
    customer = await customer_collection.find_one({"_id": ObjectId(customer_id)})
    if customer:
       return Customer(**customer)
    raise HTTPException(status_code=404, detail="Customer not found")

@api_router.put("/customers/{customer_id}", response_model=Customer, summary="Update a customer by ID")
async def update_customer(customer_id: str, customer: Customer):
    """Update a customer by their ID."""
    if not ObjectId.is_valid(customer_id):
        raise HTTPException(status_code=400, detail="Invalid customer ID format")
    updated_data = customer.model_dump(exclude_unset=True, by_alias=True)
    if not updated_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    updated_result = await customer_collection.update_one({"_id": ObjectId(customer_id)}, {"$set": updated_data})
    if updated_result.modified_count == 1:
        updated_customer = await customer_collection.find_one({"_id": ObjectId(customer_id)})
        return Customer(**updated_customer)
    raise HTTPException(status_code=404, detail="Customer not found")

@api_router.delete("/customers/{customer_id}", summary="Delete a customer by ID")
async def delete_customer(customer_id: str):
    """Delete a customer by their ID."""
    if not ObjectId.is_valid(customer_id):
        raise HTTPException(status_code=400, detail="Invalid customer ID format")
    delete_result = await customer_collection.delete_one({"_id": ObjectId(customer_id)})
    if delete_result.deleted_count == 1:
        await interaction_collection.delete_many({"customer_id": customer_id})
        return {"message": "Customer and interactions deleted"}
    raise HTTPException(status_code=404, detail="Customer not found")

# FastAPI endpoints - Interactions

@api_router.post("/interactions/", response_model=Interaction, summary="Create a new interaction")
async def create_interaction(interaction: Interaction):
    """Create a new interaction in the database."""
    if not ObjectId.is_valid(interaction.customer_id):
        raise HTTPException(status_code=400, detail="Invalid customer ID format")
    customer_exists = await customer_collection.find_one({"_id": ObjectId(interaction.customer_id)})
    if not customer_exists:
        raise HTTPException(status_code=404, detail="Customer not found")

@api_router.get("/interactions/{interaction_id}", response_model=Interaction, summary="Retrieve an interaction by ID")
async def get_interaction(interaction_id: str):
    """Retrieve an interaction by its ID."""
    interaction = get_interaction(interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    """Perform sentiment analysis on both customer message and evolance response"""
    sentiment_result = sentiment_pipeline(interaction.customer_message)[0]
    interaction["sentiment"] = sentiment_result['label']
    interaction["sentiment_score"] = sentiment_result['score']
    interaction_data = interaction.model_dump(by_alias=True, exclude_none=True)
    result = await interaction_collection.insert_one(interaction_data)
    new_interaction = await interaction_collection.find_one({"_id": result.inserted_id})
    return Interaction(**new_interaction)

@api_router.put("/interactions/{interaction_id}", response_model=Interaction, summary="Update an interaction by ID")
async def update_interaction(interaction_id: str, interaction: Interaction):
    """Update an interaction by its ID."""
    if not ObjectId.is_valid(interaction_id):
        raise HTTPException(status_code=400, detail="Invalid interaction ID format")
    update_data = interaction.model_dump(exclude_unset=True, by_alias=True)
    update_data.pop("_id", None)  # Remove id from update data
    update_data.pop("sentiment", None)  # Remove Sentiment from update data
    update_data.pop("sentiment_score", None)  # Remove Sentiment score from update data

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    updated_result = await interaction_collection.update_one({"_id": ObjectId(interaction_id)}, {"$set": update_data})
    if updated_result.modified_count == 1:
        updated_interaction = await interaction_collection.find_one({"_id": ObjectId(interaction_id)})
        return Interaction(**updated_interaction)
    raise HTTPException(status_code=404, detail="Interaction not found")

@api_router.delete("/interactions/{interaction_id}", summary="Delete an interaction by ID")
async def delete_interaction(interaction_id: str):
    """Delete an interaction by its ID."""
    if not ObjectId.is_valid(interaction_id):
        raise HTTPException(status_code=400, detail="Invalid interaction ID format")
    delete_result = await interaction_collection.delete_one({"_id": ObjectId(interaction_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Interaction deleted successfully"}
    raise HTTPException(status_code=404, detail="Interaction not found")

# FastAPI endpoints - Emolytics

@api_router.post("/chat", response_model=AIResponse,summary = "Process user input and generate AI response")
async def chat_with_emolytics(user_input: UserInput):
    """
    Main endpoint for conversational AI interaction.
    Processes user input, generates AI response with emotion detection,
    reasoning, emojics, and book suggestions, then logs the interaction.
    """
    try:
        # Process the user input to get the full AI response
        response= process_user_input_for_ai_response(user_input)


        # Create a log entry for the conversation turn
        conversation_log_entry = ConversationLogEntry(
            user_id=user_input.user_id,
            conversation_id=user_input.conversation_id,
            turn_number=user_input.turn_number,
            user_message=user_input.message,
            response=response
        )

        # Insert the log entry into MongoDB
        # Convert Pydantic model to a dictionary for MongoDB insertion
        log_data = conversation_log_entry.model_dump(exclude_none=True, by_alias=True)
        result = db.conversations_log_collection.insert_one(log_data)

        if not result.inserted_id:
            # Log this error internally, but still return the AI response to the user
            print(f"ERROR: Failed to log conversation turn for user {user_input.user_id}, conv {user_input.conversation_id}")

        return response

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred during chat processing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred: {str(e)}"
        )
    
# Log summary for the MongoDB    
@api_router.get("/logs", response_model=List[EmotionLog], summary ="Retrieve all interaction logs")    
async def get_logs():
    """Retrieves all stored interaction logs from MongoDB."""
    logs = log_service.get_all_log_entries()
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found.")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No logs found.")

    return logs

# You might want to add a health check endpoint
@api_router.get("/health", summary="Health check endpoint")
async def health_check():
    """Checks the health of the API and database connection"""
    if log_service.client.admin.command('ping'):
        try:
            log_service.client.admin.command('ping')
            return {"status": "healthy", "database_connection": "successful"}
        except ConnectionError:
            return {"status": "unhealthy", "database_connection": "unsuccessful"}
    else:
            return {"status": "unhealthy", "database_connection": "not_initialized"}


@api_router.get("/chat/history/{conversation_id}", response_model=List[ConversationLogEntry])
async def get_chat_history(conversation_id: str):
    """
    Retrieves the full chat history for a given conversation ID, including AI responses.
    """
    try:
        history_records = list(db.conversations_log_collection.find(
            {"conversation_id": conversation_id}
        ).sort("turn_number", 1))

        if not history_records:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No chat history found for this conversation ID.")

        return [ConversationLogEntry(**record) for record in history_records]

    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


 # FastAPI endpoints - Music suggestions

@api_router.post("/music/suggest", response_model=MusicPreference, summary="Get music suggestions based on mood or text")
async def suggest_music(request: MusicSuggestionRequest):
    """
    Suggests music tracks based on the user's mood or text input.
    """
    if not client:
        raise HTTPException(status_code=503, detail="Music service is not available")
    detected_mood = request.mood
    if request.text:
        if not sentiment_pipeline:
            raise HTTPException(status_code=503, detail="Sentiment analysis service is not available")
        try:
            # Use the hugging face model
            sentiment = sentiment_pipeline(request.text)[0]
            sentiment_label = sentiment['label']
            detected_mood = map_sentiment_to_mood(sentiment_label)
            print(f"Text: '{request.text}', Detected sentiment: {sentiment_label}, Detected Mood: {detected_mood}")
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {e}")
    elif not detected_mood:
        raise HTTPException(status_code=400, detail="Mood or text input is required for music suggestions")  
    # Get music suggestions based on the detected mood 
    suggestions = get_music_suggestions_by_mood(detected_mood)

    # Here you would implement the logic to suggest music tracks based on the detected mood
    # For now, let's return the received request as a placeholder
    return {"mood": detected_mood, "suggested_tracks": suggestions}

@api_router.post("/music/preference", response_model=MusicPreference, summary="Save user's music preferences")
async def save_music_preference(preference: MusicPreference):
    """
    Saves the user's music preferences.
    """
    if not client:
        raise HTTPException(status_code=503, detail="Music service is not available")
    try:
        result = await music_collection_name.insert_one(preference.model_dump(exclude_none=True, by_alias=True))
        return {"message": "Preference saved successfully", "preference_id": str(result.inserted_id)}
    except Exception as e:
        print(f"Error saving music preference: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving music preference: {e}")

@api_router.get("/music/preferences/{user_id}", response_model=List[MusicPreference], summary="Get user's music preferences")
async def get_music_preferences(user_id: str):
    """
    Retrieves the user's music preferences.
    """
    if not client:
        raise HTTPException(status_code=503, detail="Music service is not available")
    try:
        preferences = []
        async for doc in music_collection_name.find({"user_id": user_id}):
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            preferences.append(doc)
        return {"user_id": user_id, "preferences": preferences}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving music preferences: {e}")


# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.date.today() + expires_delta
    else:
        expire = datetime.date.today() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = await db.users.find_one({"email": email})
    if user is None:
        raise credentials_exception
    return User(**user)

async def get_ai_response(message: str, user_context: dict = None, story_context: str = None) -> str:
    """Get AI response using OpenAI GPT-4 or fallback to mock responses"""
    
    system_message = """You are Evolance, a wise and compassionate spiritual AI guide focused on inner transformation and consciousness expansion. You speak with warmth, depth, and gentle wisdom. You help users explore their inner landscape, make conscious decisions, and grow spiritually. 

Your responses should be:
- Spiritually insightful but accessible
- Compassionate and non-judgmental  
- Encouraging of self-reflection
- Focused on consciousness, mindfulness, and inner growth
- Personal and warm, not clinical

Always aim to guide users toward greater self-awareness, acceptance, and spiritual evolution."""

    if story_context:
        system_message += f"\n\nThe user is currently working on a spiritual story/journey: {story_context}. Tailor your response to support their journey."

    if openai_client and OPENAI_API_KEY != 'your-openai-api-key-here':
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Fall back to mock response
            pass
    
    # Fallback spiritual responses
    spiritual_responses = [
        "I sense deep wisdom in your words. Let's explore what your heart is truly saying about this situation. What feelings arise when you sit quietly with this?",
        "Your journey of self-discovery is beautiful to witness. Every question you ask brings you closer to your authentic truth. What would your highest self choose in this moment?",
        "There's profound growth happening within you. Sometimes the path isn't clear, but trust that your inner wisdom knows the way. What does your intuition whisper to you?",
        "I feel the sincerity of your seeking. Remember, every challenge is an invitation to expand your consciousness. How might this experience be serving your spiritual evolution?",
        "Your awareness is expanding beautifully. The fact that you're questioning and reflecting shows great spiritual maturity. What would love choose in this situation?",
        "I honor the courage it takes to look within. Your willingness to explore these depths is a gift to your soul's journey. What truth is emerging for you right now?",
        "The universe speaks through your experiences. Even in uncertainty, there's wisdom unfolding. What patterns do you notice in your spiritual growth?",
        "Your consciousness is awakening to new possibilities. Trust the process, even when it feels unclear. What would bring you the deepest sense of alignment?",
        "I witness the light of awareness growing within you. Every moment of mindfulness is a step toward liberation. How can you honor your inner voice today?",
        "The path of consciousness is one of gentle unfolding. Be patient with yourself as you navigate this journey. What brings you closer to your true essence?"
    ]
    
    # Select response based on message characteristics
    message_lower = message.lower()
    if any(word in message_lower for word in ['anxious', 'worried', 'fear', 'scared']):
        return "I feel the weight of your concerns, and I want you to know that what you're experiencing is part of the human journey. When anxiety arises, it often signals that our soul is asking us to trust more deeply. Take a gentle breath with me. What would it feel like to release this worry to the universe and trust in your inner strength?"
    elif any(word in message_lower for word in ['confused', 'lost', 'unclear', 'don\'t know']):
        return "In the sacred space of not knowing, wisdom often emerges. Your confusion is not a sign of weakness—it's your consciousness expanding beyond old limitations. Sometimes the soul needs to wander in the wilderness before finding its true path. What feels most authentic to you right now, even in the uncertainty?"
    elif any(word in message_lower for word in ['decision', 'choice', 'choose']):
        return "Decisions are spiritual crossroads where your future self is born. Before choosing with your mind, what does your heart know? Often our deepest wisdom comes not from analyzing but from feeling into what brings us alive. What choice would your most evolved self make?"
    else:
        return spiritual_responses[hash(message) % len(spiritual_responses)]

async def generate_consciousness_insights(decision: ConsciousnessDecision, user: User) -> List[str]:
    """Generate AI insights for consciousness timeline decisions"""
    
    if openai_client and OPENAI_API_KEY != 'your-openai-api-key-here':
        try:
            prompt = f"""As Evolance, a spiritual consciousness guide, provide 3-4 deep insights about this decision journey:

Decision: {decision.decision_title}
Context: {decision.decision_context}
Past fulfillment: {decision.past_self.fulfillment_level}/100
Present fulfillment: {decision.present_self.fulfillment_level}/100  
Future fulfillment: {decision.future_self.fulfillment_level}/100

Provide insights about:
1. The consciousness evolution pattern
2. What this decision reveals about their spiritual growth
3. How their fulfillment trajectory reflects their inner journey
4. Guidance for aligning with their highest path

Keep insights spiritual, profound but accessible, and encouraging."""

            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            
            insights_text = response.choices[0].message.content
            # Split into individual insights
            insights = [insight.strip() for insight in insights_text.split('\n') if insight.strip() and not insight.strip().startswith('#')]
            return insights[:4]  # Max 4 insights
            
        except Exception as e:
            logger.error(f"OpenAI API error for insights: {e}")
    
    # Fallback insights based on fulfillment patterns
    insights = []
    
    past_fulfillment = decision.past_self.fulfillment_level
    present_fulfillment = decision.present_self.fulfillment_level
    future_fulfillment = decision.future_self.fulfillment_level
    
    if future_fulfillment > present_fulfillment:
        insights.append("Your consciousness is expanding toward greater fulfillment. This decision represents a sacred opportunity to align with your soul's deeper calling.")
    elif future_fulfillment < present_fulfillment:
        insights.append("Sometimes the path of consciousness asks us to release what no longer serves us. Trust that any temporary decrease in fulfillment may be creating space for profound transformation.")
    else:
        insights.append("Your fulfillment levels suggest you're in a space of spiritual integration. This decision is an opportunity to deepen your current path rather than dramatically change direction.")
    
    if present_fulfillment > past_fulfillment + 20:
        insights.append("You've made remarkable progress in your spiritual evolution. The growth from your past self shows your commitment to conscious living.")
    elif present_fulfillment < past_fulfillment - 10:
        insights.append("Life's challenges have temporarily dimmed your fulfillment, but remember - even the dark night of the soul serves spiritual awakening. You have the wisdom to reclaim your inner light.")
    
    insights.append("Every decision is a vote for the future self you're becoming. Trust your inner wisdom to guide you toward choices that honor your spiritual growth.")
    insights.append("The fact that you're consciously examining this decision shows great spiritual maturity. Your awareness itself is transforming your reality.")
    
    return insights

# Initialize sample data functions
async def initialize_personality_questions():
    existing_questions = await db.personality_questions.count_documents({})
    if existing_questions == 0:
        questions = [
            {
                "id": str(uuid.uuid4()),
                "question": "How do you typically handle stress or overwhelming situations?",
                "options": [
                    "I take deep breaths and meditate to center myself",
                    "I talk to friends or family for support",
                    "I try to solve the problem immediately",
                    "I need some time alone to process my feelings"
                ],
                "category": "emotional_regulation"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "When making important decisions, what influences you most?",
                "options": [
                    "My intuition and inner voice",
                    "Logical analysis and facts",
                    "Advice from people I trust",
                    "How it will affect others around me"
                ],
                "category": "decision_making"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "How do you connect with your inner self?",
                "options": [
                    "Through meditation and mindfulness",
                    "Through creative expression",
                    "Through physical activities and nature",
                    "Through journaling and self-reflection"
                ],
                "category": "spiritual_connection"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "What brings you the most sense of fulfillment?",
                "options": [
                    "Helping others and making a difference",
                    "Personal growth and self-improvement",
                    "Achieving goals and recognition",
                    "Deep relationships and connections"
                ],
                "category": "life_purpose"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "How do you view challenges and setbacks?",
                "options": [
                    "As opportunities for growth and learning",
                    "As tests that make me stronger",
                    "As temporary obstacles to overcome",
                    "As signs to change direction"
                ],
                "category": "resilience"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "What is your relationship with emotions?",
                "options": [
                    "I embrace all emotions as part of the human experience",
                    "I try to understand what my emotions are telling me",
                    "I prefer to stay balanced and not get too emotional",
                    "I sometimes struggle to identify what I'm feeling"
                ],
                "category": "emotional_awareness"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "How do you prefer to spend your free time?",
                "options": [
                    "In quiet reflection or spiritual practices",
                    "Learning new things or exploring ideas",
                    "Socializing and connecting with others",
                    "Engaging in hobbies or creative activities"
                ],
                "category": "lifestyle_preference"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "What motivates you to keep going during difficult times?",
                "options": [
                    "Faith that everything happens for a reason",
                    "The support of loved ones",
                    "My personal goals and dreams",
                    "The belief that this too shall pass"
                ],
                "category": "motivation"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "How do you define success in life?",
                "options": [
                    "Living authentically and true to myself",
                    "Making positive impact on others",
                    "Achieving personal and professional goals",
                    "Finding peace and contentment"
                ],
                "category": "life_values"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "What role does spirituality play in your life?",
                "options": [
                    "It's central to everything I do",
                    "It provides guidance and comfort",
                    "I'm exploring and learning about it",
                    "I'm open but still questioning"
                ],
                "category": "spirituality"
            }
        ]
        await db.personality_questions.insert_many(questions)

# Psychology Multiple Choice Questions
async def psychology_multiple_choice_questions():
    psychology_questions = await db.multiple_choice_questions.count_documents({})
    if psychology_questions == 0:
        questions = [
            {
                "id": str(uuid.uuid4()),
                "question": "Which scientific framework asserts that each person has an own understanding of what reality is about and meaning of things?",
                "options": [
                    "Structuralism",
                    "Rationalism",
                    "Idealism",
                    "Relativism"
                ],
                "category": "introduction to psychology"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "____ opposed the idea of universal truths and suggests that psychology should focus on the experiences of people in their social and cultural contexts?",
                "options": [
                    "Humanism",
                    "Postmodernism",
                    "Psychodynamics",
                    "Positive_psychology"
                ],
                "category": "introduction_to_psychology"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "____ is the mostly used in the psychological approach with the aim of bringing unconscious context to the conscience",
                "options": [
                    "Taylorism",
                    "Introspection",
                    "Free association",
                    "Eidetic reduction"
                ],
                "category": "introduction_to_psychology"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Which part of the brain is important for an individual following a career as a mathematician?",
                "options": [
                    "Thalamus",
                    "Cerebellum",
                    "Left hemisphere",
                    "Right hemisphere"
                ],
                "category": "biological_features"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "One of the following ergonomics recommendations contribute to the proper design of work stations?",
                "options": [
                    "Seats with no arm rests",
                    "Minimal space for bodily movement",
                    "Inadequate access to the work station",
                    "Grips and handles that fit in the hand of the user"
                ],
                "category": "industrial psychology in the workplace"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Which of the following body areas is prone to repetitive-strain injuries",
                "options": [
                    "Ear",
                    "Eye",
                    "Neck",
                    "Ankle"
                ],
                "category": "industrial psychology in the workplace"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Which of the following domains in human development emphasise the roles of self-development and social influences in personality formation?",
                "options": [
                    "Critical periods",
                    "Cognitive development",
                    "Psychosocial development",
                    "Physical/biological development"
                ],
                "category": "social_psychology"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "____ attachment type would be the appropriate insecure attachment behaviour to describe a person who prefers to be alone and avoid committing themselves in a relationship?",
                "options": [
                    "Secure",
                    "Fixation",
                    "Avoidant",
                    "Ambivalent"
                ],
                "category": "attachment_theories"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Learning can be distinguised from performance in that____?",
                "options": [
                    "Learninig refers to behaviour",
                    "Learning will always change behaviour",
                    "One can always monitor learning directly",
                    "Learning refers to the potential change in behaviour"
                ],
                "category": "cognition"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "A type of perception where the perceiver uses too many personal attributes to make attributions or to explain causes of or reasons for behaviour in individuals or groups is referred to as the ____?",
                "options": [
                    "actor-observer effect",
                    "a top-down perceptual process",
                    "fundamental attribution error",
                    "self-serving bias"
                ],
                "category": "perception"
            }
        ]
        await db.multiple_choice_questions.insert_many(questions)

        
# Self evaluation - Psychologist
async def self_evaluation_questions():
    self_evaluation_questions = await db.self_evaluation_questions.count_documents({})
    if self_evaluation_questions == 0:
        questions = [
            {
                "id": str(uuid.uuid4()),
                "question": """A middle manager is feeling aggressive towards top management,but for various reasons he does not display his feelings towards them.
                 Instead he starts to interact aggressively with his subordinates. 
                 Subsequently his performance and that of his department deteriorates rapidly and influences the performance of the rest of the orgainisation. 
                 Top management calls on you as an Industrial psychologist to help them evaluate and study this problem and make the most appropriate intervention. 
                 What field of industrial psychology is at issue in this case?""",
                "options": [
                    "Ergonomics",
                    "Personal psychology",
                    "Research methodology",
                    "Consumer psychology",
                    "Orgainizational psychology"
                ],
                "category": "self_evaluation"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "You are an I/O psychologist in private practice. A person who suffered some impairment in terms of his physical and cognitive functions in a car accident asks you to refer him to a psychologist who could help him develop corrective actions that would address the brain injury. You refer him to a ____ ",
                "options": [
                    "Career counsellor",
                    "Neuropsychologist",
                    "Clinical psychology",
                    "Orgainisational psychology",
                    "Consumer psychology"
                ],
                "category": "self_evaluation"
            },
            {
                "id": str(uuid.uuid4()),
                "question": """Joe notices two men who seem to be having a heated exchange.
                 They are speaking loudly and one man is slapping the other one on the shoulder.
                 The same situation would have been interpreted differently had it occured in a subdued banking environment or at a large soccer gathering.
                 The difference in the intepretation of the behaviour would depend on ____""",
                "options": [
                    "The perceiver",
                    "The situation",
                    "The perceived target(s)",
                    "Subjective interpretation",
                    "the loudness of their voices"
                ],
                "category": "self_evaluation"
            },
            {
                "id": str(uuid.uuid4()),
                "question": """You are 20 years of age invited to a work party at which a new product is launched.
                 While observing the people socialising,
                 Which of the following strikes you as out of place in terms of your knowledge of affliliation behaviours?""",
                "options": [
                    "A older,smartly dressed woman in the company of a markedly younger man.",
                    "An attractive young woman in the company of a not-so-attractive older man, who is the sales director of the company.",
                    "Two attractive well known sports personalities together",
                    "A tall woman in her thirties, who is a senior manager in the marketing department accompanying a friend in his thirties who has just been appointed Marketing Director in the company.",
                    "The Chief Executive Officer of the company in the company of other Chief Executive Officers."
                ],
                "category": "self_evaluation"
            }
        ]
        await db.self_evaluation_questions.insert_many(questions)


# Learning Experience Questionaire

async def learning_experience_questionaire():
    learning_experience = await db.learning_experience_questionaire.count_documents({})
    if learning_experience == 0:
        questions = [
            {
                "id": str(uuid.uuid4()),
                "question": "I understand the content of the prescribed book better after doing the activities in the study guide",
                "options": [
                    "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user_research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "I shared my learning experiences with other people, and this enhanced my understanding",
                "options": [
                   "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user_research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "I think I am more sensitive now to my own and other people's/group's behaviours and habits",
                "options": [
                    "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user_research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "The learning experience improved my competencies to create opportunities to use in my studies and work",
                "options": [
                    "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user_research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "I believe that the discussion forums on the evolance portal help me understnd the portal better",
                "options": [
                    "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user_research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "I learnt certain competencies in decision making and problem-solving",
                "options": [
                    "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user_research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "The learning experience taught me to think more critically and creativity",
                "options": [
                    "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user_research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "By experiencing the learning methods as well the methods and applications of psychology, I think i am now more sensitive to people behaviours and the influence of environments on people",
                "options": [
                   "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user_research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "I learnt to study more effectively by using various methods of learning",
                "options": [
                    "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user_research"
            },
            
            {
                "id": str(uuid.uuid4()),
                "question": "Sometimes I had to cooperate with other persons or groups in order to learn",
                "options": [
                   "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "I think I have developed some basic research competencies such as reading, assessing and analysing information critically, and organising and presenting it logically and systematically",
                "options": [
                   "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "I had to take more personal responsibility for studying and learning, for instance by following my own pace and schedule and by probing in order to understand concepts and assumptions",
                "options": [
                   "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "The learning experience also taught me to write more economically, for instance, by summarising",
                "options": [
                   "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "The learning experience provided me with a bigger picture of events, for instance by helping me to understand people in more than one way, and to realise that we live together and are influenced by many factors",
                "options": [
                   "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user research"
            },
            {
                "id": str(uuid.uuid4()),
                "question": "In general I am very satisfied with my learning experience at evolance",
                "options": [
                   "Strongly Disagree",
                    "Disagree",
                    "Agree",
                    "Agree to some content",
                    "Strongly Agree"
                ],
                "category": "user research"
            }
        ]
        await db.learning_experience_questionaire.insert_many(questions)



async def initialize_sample_stories():
    existing_stories = await db.stories.count_documents({})
    if existing_stories == 0:
        stories = [
            {
                "id": str(uuid.uuid4()),
                "title": "The Journey of Self-Acceptance",
                "description": "Learn to embrace all aspects of yourself with compassion and understanding",
                "content": "This story guides you through the transformative process of self-acceptance...",
                "category": "self_love",
                "difficulty_level": 1,
                "estimated_duration": "2 weeks",
                "acceptance_threshold": 75
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Releasing Past Wounds",
                "description": "A healing journey to let go of past hurts and embrace forgiveness",
                "content": "Through gentle guidance and reflection, this story helps you release...",
                "category": "healing",
                "difficulty_level": 3,
                "estimated_duration": "4 weeks",
                "acceptance_threshold": 80
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Finding Your Inner Voice",
                "description": "Discover and trust your intuition and inner wisdom",
                "content": "This story takes you on a journey of deep listening...",
                "category": "intuition",
                "difficulty_level": 2,
                "estimated_duration": "3 weeks",
                "acceptance_threshold": 70
            }
        ]
        await db.stories.insert_many(stories)

async def initialize_sample_videos():
    existing_videos = await db.video_lessons.count_documents({})
    if existing_videos == 0:
        videos = [
            {
                "id": str(uuid.uuid4()),
                "title": "Introduction to Mindful Living",
                "description": "Learn the basics of incorporating mindfulness into your daily life",
                "mentor_name": "Dr. Sarah Chen",
                "video_url": "https://example.com/video1.mp4",
                "thumbnail_url": "https://example.com/thumb1.jpg",
                "duration": "15:30",
                "category": "mindfulness",
                "difficulty_level": 1
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Healing Through Meditation",
                "description": "Advanced meditation techniques for emotional healing",
                "mentor_name": "Master Liu Wei",
                "video_url": "https://example.com/video2.mp4",
                "thumbnail_url": "https://example.com/thumb2.jpg",
                "duration": "22:45",
                "category": "meditation",
                "difficulty_level": 3
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Building Emotional Resilience",
                "description": "Strategies to develop inner strength and emotional stability",
                "mentor_name": "Dr. Maria Santos",
                "video_url": "https://example.com/video3.mp4",
                "thumbnail_url": "https://example.com/thumb3.jpg",
                "duration": "18:20",
                "category": "resilience",
                "difficulty_level": 2
            }
        ]
        await db.video_lessons.insert_many(videos)

# Authentication Routes
@api_router.post("/auth/register", response_model=Token)
async def register(user: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    
    await db.users.insert_one(new_user.dict())
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.post("/auth/login", response_model=Token)
async def login(user: UserLogin):
    # Verify user
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse(**current_user.dict())

# Personality Test Routes
@api_router.get("/personality/questions", response_model=List[PersonalityQuestion])
async def get_personality_questions():
    questions = await db.personality_questions.find().to_list(1000)
    return [PersonalityQuestion(**q) for q in questions]

@api_router.post("/personality/submit", response_model=PersonalityResult)
async def submit_personality_test(
    submission: PersonalityTestSubmission,
    current_user: User = Depends(get_current_user)
):
    # Calculate emotional quotient score (simplified algorithm)
    eq_score = min(100, len(submission.answers) * 10)
    
    # Determine personality type based on answers (simplified)
    personality_types = ["Intuitive Seeker", "Analytical Achiever", "Compassionate Helper", "Creative Explorer"]
    personality_type = personality_types[eq_score % 4]
    
    # Determine spiritual inclination
    spiritual_inclinations = ["Deeply Spiritual", "Spiritually Curious", "Grounded Seeker", "Open Explorer"]
    spiritual_inclination = spiritual_inclinations[(eq_score + 1) % 4]
    
    result = PersonalityResult(
        user_id=current_user.id,
        answers=submission.answers,
        emotional_quotient_score=eq_score,
        personality_type=personality_type,
        spiritual_inclination=spiritual_inclination
    )
    
    await db.personality_results.insert_one(result.dict())
    
    # Update user's personality test status
    await db.users.update_one(
        {"id": current_user.id},
        {"$set": {"personality_test_completed": True, "spiritual_level": eq_score}}
    )
    
    return result

# Story Routes
@api_router.get("/stories", response_model=List[Story])
async def get_stories():
    stories = await db.stories.find().to_list(1000)
    return [Story(**story) for story in stories]

@api_router.get("/stories/progress", response_model=List[UserStoryProgress])
async def get_user_story_progress(current_user: User = Depends(get_current_user)):
    progress = await db.user_story_progress.find({"user_id": current_user.id}).to_list(1000)
    return [UserStoryProgress(**p) for p in progress]

@api_router.post("/stories/{story_id}/start")
async def start_story(story_id: str, current_user: User = Depends(get_current_user)):
    # Check if story exists
    story = await db.stories.find_one({"id": story_id})
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Check if user already has progress for this story
    existing_progress = await db.user_story_progress.find_one({
        "user_id": current_user.id,
        "story_id": story_id
    })
    
    if existing_progress:
        # Update existing progress
        await db.user_story_progress.update_one(
            {"user_id": current_user.id, "story_id": story_id},
            {"$set": {"status": "in_progress", "started_at": datetime.utcnow()}}
        )
    else:
        # Create new progress
        progress = UserStoryProgress(
            user_id=current_user.id,
            story_id=story_id,
            status="in_progress",
            started_at=datetime.utcnow()
        )
        await db.user_story_progress.insert_one(progress.dict())
    
    return {"message": "Story started successfully"}

@api_router.post("/stories/{story_id}/complete")
async def complete_story(
    story_id: str,
    acceptance_level: int,
    current_user: User = Depends(get_current_user)
):
    # Update story progress
    await db.user_story_progress.update_one(
        {"user_id": current_user.id, "story_id": story_id},
        {
            "$set": {
                "status": "completed",
                "acceptance_level": acceptance_level,
                "completed_at": datetime.utcnow(),
                "ai_confirmed": acceptance_level >= 80  # Auto-confirm if high acceptance
            }
        }
    )
    
    return {"message": "Story completed successfully"}

# Chat Routes with Enhanced AI
@api_router.post("/chat/message", response_model=ChatMessage)
async def send_chat_message(
    message: str,
    story_context: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    # Save user message
    user_message = ChatMessage(
        user_id=current_user.id,
        message=message,
        is_user=True,
        story_context=story_context
    )
    await db.chat_messages.insert_one(user_message.dict())
    
    # Get user context for AI
    user_context = {
        "name": current_user.full_name,
        "spiritual_level": current_user.spiritual_level
    }
    
    # Generate AI response
    ai_response_text = await get_ai_response(message, user_context, story_context)
    
    ai_message = ChatMessage(
        user_id=current_user.id,
        message=ai_response_text,
        is_user=False,
        story_context=story_context
    )
    await db.chat_messages.insert_one(ai_message.dict())
    
    return ai_message

@api_router.get("/chat/history", response_model=List[ChatMessage])
async def get_chat_history(
    limit: int = 50,
    story_context: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    query = {"user_id": current_user.id}
    if story_context:
        query["story_context"] = story_context
    
    messages = await db.chat_messages.find(query).sort("timestamp", -1).limit(limit).to_list(limit)
    return [ChatMessage(**msg) for msg in reversed(messages)]

# Video Routes
@api_router.get("/videos", response_model=List[VideoLesson])
async def get_video_lessons():
    videos = await db.video_lessons.find().to_list(1000)
    return [VideoLesson(**video) for video in videos]

@api_router.get("/videos/{video_id}/reviews", response_model=List[VideoReview])
async def get_video_reviews(video_id: str):
    reviews = await db.video_reviews.find({"video_id": video_id}).to_list(1000)
    return [VideoReview(**review) for review in reviews]

@api_router.post("/videos/review", response_model=VideoReview)
async def create_video_review(
    review: VideoReviewCreate,
    current_user: User = Depends(get_current_user)
):
    new_review = VideoReview(
        user_id=current_user.id,
        video_id=review.video_id,
        rating=review.rating,
        review_text=review.review_text
    )
    
    await db.video_reviews.insert_one(new_review.dict())
    return new_review

# Todo Routes
@api_router.get("/todos", response_model=List[Todo])
async def get_todos(
    story_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    query = {"user_id": current_user.id}
    if story_id:
        query["story_id"] = story_id
    
    todos = await db.todos.find(query).to_list(1000)
    return [Todo(**todo) for todo in todos]

@api_router.post("/todos", response_model=Todo)
async def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user)
):
    new_todo = Todo(
        user_id=current_user.id,
        story_id=todo.story_id,
        title=todo.title,
        description=todo.description
    )
    
    await db.todos.insert_one(new_todo.dict())
    return new_todo

@api_router.put("/todos/{todo_id}/complete")
async def complete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user)
):
    result = await db.todos.update_one(
        {"id": todo_id, "user_id": current_user.id},
        {"$set": {"completed": True, "completed_at": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {"message": "Todo completed successfully"}

# NEW: Consciousness Timeline Routes
@api_router.post("/consciousness/decision", response_model=ConsciousnessDecision)
async def create_consciousness_decision(
    decision_data: DecisionCreate,
    current_user: User = Depends(get_current_user)
):
    # Create default self states (user can update these)
    past_self = SelfState(
        fulfillment_level=50,
        happiness_level=50,
        clarity_level=40,
        confidence_level=45,
        description="My past self navigating earlier challenges",
        key_characteristics=["Learning", "Uncertain", "Growing"],
        dominant_emotions=["Curiosity", "Doubt", "Hope"],
        life_priorities=["Stability", "Learning", "Relationships"]
    )
    
    present_self = SelfState(
        fulfillment_level=65,
        happiness_level=60,
        clarity_level=55,
        confidence_level=60,
        description="My current self facing this decision",
        key_characteristics=["Aware", "Thoughtful", "Seeking"],
        dominant_emotions=["Contemplation", "Determination", "Mild anxiety"],
        life_priorities=["Growth", "Authenticity", "Purpose"]
    )
    
    future_self = SelfState(
        fulfillment_level=80,
        happiness_level=75,
        clarity_level=85,
        confidence_level=80,
        description="My future self having grown from this decision",
        key_characteristics=["Wise", "Confident", "Aligned"],
        dominant_emotions=["Peace", "Joy", "Gratitude"],
        life_priorities=["Service", "Wisdom", "Inner peace"]
    )
    
    decision = ConsciousnessDecision(
        user_id=current_user.id,
        decision_title=decision_data.decision_title,
        decision_description=decision_data.decision_description,
        decision_context=decision_data.decision_context,
        decision_options=decision_data.decision_options,
        past_self=past_self,
        present_self=present_self,
        future_self=future_self,
        overall_fulfillment_trend="ascending"
    )
    
    # Generate AI insights
    decision.ai_insights = await generate_consciousness_insights(decision, current_user)
    
    await db.consciousness_decisions.insert_one(decision.dict())
    return decision

@api_router.get("/consciousness/decisions", response_model=List[ConsciousnessDecision])
async def get_consciousness_decisions(current_user: User = Depends(get_current_user)):
    decisions = await db.consciousness_decisions.find({"user_id": current_user.id}).sort("created_at", -1).to_list(1000)
    return [ConsciousnessDecision(**decision) for decision in decisions]

@api_router.get("/consciousness/decision/{decision_id}", response_model=ConsciousnessDecision)
async def get_consciousness_decision(
    decision_id: str,
    current_user: User = Depends(get_current_user)
):
    decision = await db.consciousness_decisions.find_one({
        "id": decision_id,
        "user_id": current_user.id
    })
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return ConsciousnessDecision(**decision)

@api_router.put("/consciousness/decision/{decision_id}")
async def update_consciousness_decision(
    decision_id: str,
    updated_decision: ConsciousnessDecision,
    current_user: User = Depends(get_current_user)
):
    # Regenerate insights if self states changed significantly
    updated_decision.ai_insights = await generate_consciousness_insights(updated_decision, current_user)
    updated_decision.updated_at = datetime.utcnow()
    
    result = await db.consciousness_decisions.update_one(
        {"id": decision_id, "user_id": current_user.id},
        {"$set": updated_decision.dict()}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    return {"message": "Decision updated successfully"}

@api_router.post("/consciousness/decision/{decision_id}/choose")
async def make_consciousness_decision(
    decision_id: str,
    option_index: int,
    current_user: User = Depends(get_current_user)
):
    result = await db.consciousness_decisions.update_one(
        {"id": decision_id, "user_id": current_user.id},
        {
            "$set": {
                "chosen_option_index": option_index,
                "decision_status": "decided",
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    return {"message": "Decision choice recorded successfully"}

@api_router.post("/fulfillment/entry", response_model=FulfillmentEntry)
async def create_fulfillment_entry(
    entry_data: FulfillmentCreate,
    current_user: User = Depends(get_current_user)
):
    entry = FulfillmentEntry(
        user_id=current_user.id,
        decision_id=entry_data.decision_id,
        fulfillment_level=entry_data.fulfillment_level,
        happiness_level=entry_data.happiness_level,
        clarity_level=entry_data.clarity_level,
        confidence_level=entry_data.confidence_level,
        notes=entry_data.notes
    )
    
    await db.fulfillment_entries.insert_one(entry.dict())
    return entry

@api_router.get("/fulfillment/history", response_model=List[FulfillmentEntry])
async def get_fulfillment_history(
    decision_id: Optional[str] = None,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    query = {"user_id": current_user.id}
    if decision_id:
        query["decision_id"] = decision_id
    
    entries = await db.fulfillment_entries.find(query).sort("timestamp", -1).limit(limit).to_list(limit)
    return [FulfillmentEntry(**entry) for entry in entries]

@api_router.get("/fulfillment/analytics")
async def get_fulfillment_analytics(current_user: User = Depends(get_current_user)):
    # Get fulfillment entries from last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    entries = await db.fulfillment_entries.find({
        "user_id": current_user.id,
        "timestamp": {"$gte": thirty_days_ago}
    }).sort("timestamp", 1).to_list(1000)
    
    if not entries:
        return {
            "average_fulfillment": 0,
            "average_happiness": 0,
            "average_clarity": 0,
            "average_confidence": 0,
            "trend": "stable",
            "total_entries": 0
        }
    
    # Calculate averages
    avg_fulfillment = sum(e["fulfillment_level"] for e in entries) / len(entries)
    avg_happiness = sum(e["happiness_level"] for e in entries) / len(entries)
    avg_clarity = sum(e["clarity_level"] for e in entries) / len(entries)
    avg_confidence = sum(e["confidence_level"] for e in entries) / len(entries)
    
    # Calculate trend (compare first half vs second half)
    if len(entries) >= 4:
        mid_point = len(entries) // 2
        first_half_avg = sum(e["fulfillment_level"] for e in entries[:mid_point]) / mid_point
        second_half_avg = sum(e["fulfillment_level"] for e in entries[mid_point:]) / (len(entries) - mid_point)
        
        if second_half_avg > first_half_avg + 5:
            trend = "ascending"
        elif second_half_avg < first_half_avg - 5:
            trend = "descending"
        else:
            trend = "stable"
    else:
        trend = "stable"
    
    return {
        "average_fulfillment": round(avg_fulfillment, 1),
        "average_happiness": round(avg_happiness, 1),
        "average_clarity": round(avg_clarity, 1),
        "average_confidence": round(avg_confidence, 1),
        "trend": trend,
        "total_entries": len(entries)
    }

# Basic health check
@api_router.get("/")
async def root():
    return {"message": "TimeSoul API is running", "status": "healthy"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    await initialize_personality_questions()
    await initialize_sample_stories()
    await initialize_sample_videos()
    logger.info("TimeSoul API started successfully")
    if openai_client:
        logger.info("OpenAI integration enabled")
    else:
        logger.info("OpenAI integration disabled - using fallback responses")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
