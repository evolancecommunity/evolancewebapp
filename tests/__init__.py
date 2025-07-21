from nose import collector
import pytest
import requests
from evolancewebapp.backend.data_collection import FreeDataCollector
from evolancewebapp.backend.custom_ai_integration import CustomSpiritualAI

collector = FreeDataCollector()

# Test sacral tests collection
def test_collect_sacred_tests():
    texts = collector.collect_sacred_tests()
    assert isinstance(texts, list)
    assert len(texts) > 0
    assert "title" in texts[0]
    assert texts[0]["domain"] == "spiritual"

# Test psychology collection
def test_collect_psychology_resources():
    data = collector.collect_psychology_resources()    
    assert isinstance(data, list)
    assert "category" in data[0]
    assert data[0]["category"] == "psychology"

# Test mediation collection
def test_collect_spirituality_resources():
    guides = collector.collect_meditation_guides()
    assert isinstance(guides, list)
    assert guides[0]["domain"] == "Guided Meditation for Beginners"

# Test Spiritual AI integration
class TestCustomSpiritualAI:

    def setup_method(self):
        """Setup method to initialize the custom AI"""
        from evolancewebapp.backend.custom_ai_integration import CustomSpiritualAI
        self.ai = CustomSpiritualAI()

    def test_generate_response(self):
        """Test generating a response from the custom AI"""
        message = "I'm feeling anxious about my future"
        response = self.ai.generate_response(message)
        assert isinstance(response, str)
        assert len(response) > 0

    def test_fallback_response(self):
        """Test fallback responses when model is not available"""
        message = "I'm feeling lost and anxious"
        response = self.ai._fallback_response(message)
        assert isinstance(response, str)
        assert len(response) > 0


    def test_build_input_text_with_user_content(self):
        """Test building input text with user content"""
        ai = CustomSpiritualAI(model_path="./spiritual_ai_model")
        user_context = {
            "personality_type": "INFJ",
            "spiritual_level": "beginner",
            "current_emotional_state": "calm"
        }

        input_text = ai.build_input_text("What is spirituality?", user_context="user_context")
        expected_text = (
            "user: What is spirituality?\n"
            "assistant: [Personality Type: INFJ, Spiritual Level: beginner, Current Emotional State: calm]"
        )
        assert input_text == expected_text

    def test_build_input_with_story_context(self):
        """Test_build_input_text_with_story_context"""
        ai = CustomSpiritualAI(model_path="./spiritual_ai_model")
        story_context = "spiritual journey"
        input_text = ai.build_input_text("Tell me a story", story_context=story_context)
        expected_text = (
            "user: Tell me a story\n"
            "context: discussion about spiritual journey\n"
            "assistant: "
        )
        assert input_text == expected_text

    def test_build_input_text_with_all_contexts(self):
        """ Test building input text with all contexts"""
        ai = CustomSpiritualAI(model_path="./spiritual_ai_model")
        user_context = {
            "personality_type": "empath",
            "current_emotional_state": "calm"
        }
        story_context = "karma and reincarnation"

        input_text = ai.build_input_text(
            "Explain the concept of karma",
            user_context=user_context,
            story_context=story_context
        )
        expected_text = (
            "user: Explain the concept of karma\n"
            "context: user has empath personality\n"
            "context: current emotional state is calm\n"
            "context: discussion about karma and reincarnation\n"
            "assistant: "
        )
        assert input_text == expected_text
            
            



    def test_clean_response_adds_punctuation(self):
        """Test that clean_response adds punctuation"""
        ai = CustomSpiritualAI(model_path="./spiritual_ai_model")
        response = ai.clean_response("This is a response.")
        assert response == "This is a response."
        response = ai.clean_response("This is a question?")
        assert response == "This is a question?"
        response = ai.clean_response("This is an exclamation!")
        assert response == "This is an exclamation!"
        
    