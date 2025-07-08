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
import openai
from openai import OpenAI

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
