from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import hashlib
import jwt
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create the main app without a prefix
app = FastAPI(title="TimeSoul API", description="API for TimeSoul - Evolance spiritual wellness app")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

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

# Token Model
class Token(BaseModel):
    access_token: str
    token_type: str

# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
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

# Initialize personality test questions
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

# Initialize sample stories
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

# Initialize sample videos
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

# Chat Routes
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
    
    # Generate AI response (mock implementation)
    ai_responses = [
        "I understand your feelings. Let's explore this together.",
        "That's a beautiful insight. How does this make you feel?",
        "You're on a wonderful journey of self-discovery.",
        "Remember, every step forward is progress, no matter how small.",
        "Your awareness is growing. Trust in your inner wisdom."
    ]
    
    ai_response_text = ai_responses[len(message) % len(ai_responses)]
    
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

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
