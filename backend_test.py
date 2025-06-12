import requests
import sys
import time
import uuid
from datetime import datetime

class TimeSoulAPITester:
    def __init__(self, base_url="https://23e7a850-50e7-424b-a000-2c4f2cffb347.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        self.test_password = "Test123!"
        self.test_full_name = "Test User"
        self.story_id = None
        self.video_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"Response: {response.json()}")
                except:
                    print(f"Response: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_register(self):
        """Test user registration"""
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data={
                "email": self.test_email,
                "password": self.test_password,
                "full_name": self.test_full_name
            }
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            print(f"📝 Registered user: {self.test_email}")
            return True
        return False

    def test_login(self):
        """Test user login"""
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data={
                "email": self.test_email,
                "password": self.test_password
            }
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            print(f"🔑 Logged in as: {self.test_email}")
            return True
        return False

    def test_get_current_user(self):
        """Test getting current user info"""
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        if success and 'id' in response:
            self.user_id = response['id']
            print(f"👤 User ID: {self.user_id}")
            print(f"👤 User Name: {response['full_name']}")
            print(f"👤 Personality Test Completed: {response['personality_test_completed']}")
            return True
        return False

    def test_get_personality_questions(self):
        """Test getting personality questions"""
        success, response = self.run_test(
            "Get Personality Questions",
            "GET",
            "personality/questions",
            200
        )
        if success and isinstance(response, list):
            print(f"📋 Retrieved {len(response)} personality questions")
            return response
        return []

    def test_submit_personality_test(self, questions):
        """Test submitting personality test answers"""
        if not questions:
            print("❌ No questions available to submit answers")
            return False

        # Create mock answers for each question
        answers = []
        for question in questions:
            answer = {
                "question_id": question["id"],
                "answer_index": 0,  # Always select the first option
                "answer_text": question["options"][0]
            }
            answers.append(answer)

        success, response = self.run_test(
            "Submit Personality Test",
            "POST",
            "personality/submit",
            200,
            data={"answers": answers}
        )
        
        if success:
            print(f"📊 Personality Test Results:")
            print(f"   - EQ Score: {response['emotional_quotient_score']}")
            print(f"   - Personality Type: {response['personality_type']}")
            print(f"   - Spiritual Inclination: {response['spiritual_inclination']}")
            return True
        return False

    def test_get_stories(self):
        """Test getting stories"""
        success, response = self.run_test(
            "Get Stories",
            "GET",
            "stories",
            200
        )
        if success and isinstance(response, list) and len(response) > 0:
            self.story_id = response[0]["id"]
            print(f"📚 Retrieved {len(response)} stories")
            print(f"📖 First story: {response[0]['title']}")
            return True
        return False

    def test_start_story(self):
        """Test starting a story"""
        if not self.story_id:
            print("❌ No story ID available to start")
            return False

        success, _ = self.run_test(
            "Start Story",
            "POST",
            f"stories/{self.story_id}/start",
            200,
            data={}
        )
        return success

    def test_complete_story(self):
        """Test completing a story"""
        if not self.story_id:
            print("❌ No story ID available to complete")
            return False

        success, _ = self.run_test(
            "Complete Story",
            "POST",
            f"stories/{self.story_id}/complete?acceptance_level=85",
            200,
            data={}
        )
        return success

    def test_get_story_progress(self):
        """Test getting story progress"""
        success, response = self.run_test(
            "Get Story Progress",
            "GET",
            "stories/progress",
            200
        )
        if success and isinstance(response, list):
            print(f"📊 Retrieved progress for {len(response)} stories")
            if len(response) > 0:
                print(f"   - Story ID: {response[0]['story_id']}")
                print(f"   - Status: {response[0]['status']}")
                print(f"   - Acceptance Level: {response[0]['acceptance_level']}")
            return True
        return False

    def test_send_chat_message(self):
        """Test sending a chat message"""
        message = "Hello, I'm feeling anxious today."
        success, response = self.run_test(
            "Send Chat Message",
            "POST",
            f"chat/message?message={message}",
            200,
            data={}
        )
        if success:
            print(f"💬 AI Response: {response['message']}")
            return True
        return False

    def test_get_chat_history(self):
        """Test getting chat history"""
        success, response = self.run_test(
            "Get Chat History",
            "GET",
            "chat/history",
            200
        )
        if success and isinstance(response, list):
            print(f"💬 Retrieved {len(response)} chat messages")
            return True
        return False

    def test_get_videos(self):
        """Test getting video lessons"""
        success, response = self.run_test(
            "Get Video Lessons",
            "GET",
            "videos",
            200
        )
        if success and isinstance(response, list) and len(response) > 0:
            self.video_id = response[0]["id"]
            print(f"🎬 Retrieved {len(response)} video lessons")
            print(f"🎬 First video: {response[0]['title']}")
            return True
        return False

    def test_submit_video_review(self):
        """Test submitting a video review"""
        if not self.video_id:
            print("❌ No video ID available to review")
            return False

        success, response = self.run_test(
            "Submit Video Review",
            "POST",
            "videos/review",
            200,
            data={
                "video_id": self.video_id,
                "rating": 5,
                "review_text": "This video was very insightful and helped me understand mindfulness better."
            }
        )
        return success

    def test_get_video_reviews(self):
        """Test getting video reviews"""
        if not self.video_id:
            print("❌ No video ID available to get reviews")
            return False

        success, response = self.run_test(
            "Get Video Reviews",
            "GET",
            f"videos/{self.video_id}/reviews",
            200
        )
        if success and isinstance(response, list):
            print(f"⭐ Retrieved {len(response)} video reviews")
            return True
        return False

    def test_get_todos(self):
        """Test getting todos"""
        success, response = self.run_test(
            "Get Todos",
            "GET",
            "todos",
            200
        )
        if success and isinstance(response, list):
            print(f"📝 Retrieved {len(response)} todos")
            return True
        return False

    def run_all_tests(self):
        """Run all API tests in sequence"""
        print("🚀 Starting TimeSoul API Tests")
        print("=" * 50)
        
        # Authentication tests
        if not self.test_register():
            print("❌ Registration failed, stopping tests")
            return False
        
        if not self.test_get_current_user():
            print("❌ Getting user info failed, stopping tests")
            return False
        
        # Personality test
        questions = self.test_get_personality_questions()
        if not questions:
            print("❌ Getting personality questions failed, stopping tests")
            return False
        
        if not self.test_submit_personality_test(questions):
            print("❌ Submitting personality test failed, stopping tests")
            return False
        
        # Verify user info after personality test
        if not self.test_get_current_user():
            print("❌ Getting updated user info failed")
        
        # Stories tests
        if not self.test_get_stories():
            print("❌ Getting stories failed, continuing with other tests")
        
        if self.story_id:
            self.test_start_story()
            self.test_complete_story()
            self.test_get_story_progress()
        
        # Chat tests
        self.test_send_chat_message()
        self.test_get_chat_history()
        
        # Video tests
        if not self.test_get_videos():
            print("❌ Getting videos failed, continuing with other tests")
        
        if self.video_id:
            self.test_submit_video_review()
            self.test_get_video_reviews()
        
        # Todo tests
        self.test_get_todos()
        
        # Print results
        print("\n" + "=" * 50)
        print(f"📊 Tests passed: {self.tests_passed}/{self.tests_run} ({self.tests_passed/self.tests_run*100:.1f}%)")
        
        return self.tests_passed == self.tests_run

if __name__ == "__main__":
    tester = TimeSoulAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)