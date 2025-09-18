import random
import logging
import re
import json
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from models import Conversation

# Enhanced mental health response patterns and templates
class LocalAIService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.response_patterns = self._load_response_patterns()
        self.coping_strategies = self._load_coping_strategies()
        self.crisis_keywords = ['suicide', 'kill myself', 'end it all', 'want to die', 'hurt myself', 'self harm', 'no point living']
        self.emotion_keywords = self._load_emotion_keywords()
        
    def _load_emotion_keywords(self):
        """Enhanced emotion detection keywords"""
        return {
            'anxiety': ['anxious', 'anxiety', 'worried', 'nervous', 'panic', 'overwhelmed', 'scared', 'fearful', 'restless', 'tense'],
            'depression': ['depressed', 'depression', 'sad', 'hopeless', 'empty', 'worthless', 'down', 'low', 'blue', 'miserable'],
            'stress': ['stress', 'stressed', 'pressure', 'overwhelmed', 'busy', 'exhausted', 'burned out', 'frazzled'],
            'anger': ['angry', 'mad', 'furious', 'frustrated', 'irritated', 'annoyed', 'rage', 'livid', 'upset'],
            'loneliness': ['lonely', 'alone', 'isolated', 'disconnected', 'abandoned', 'left out', 'solitary'],
            'fear': ['afraid', 'scared', 'fearful', 'terrified', 'frightened', 'worried', 'apprehensive'],
            'sadness': ['sad', 'sorrow', 'grief', 'melancholy', 'dejected', 'downhearted', 'mournful'],
            'happiness': ['happy', 'joy', 'joyful', 'elated', 'cheerful', 'delighted', 'pleased', 'content'],
            'excitement': ['excited', 'thrilled', 'enthusiastic', 'energetic', 'pumped', 'eager'],
            'calm': ['calm', 'peaceful', 'serene', 'tranquil', 'relaxed', 'at ease', 'centered'],
            'confusion': ['confused', 'lost', 'uncertain', 'unclear', 'bewildered', 'puzzled'],
            'guilt': ['guilty', 'ashamed', 'regretful', 'remorseful', 'sorry', 'blame myself'],
            'gratitude': ['grateful', 'thankful', 'appreciative', 'blessed', 'fortunate']
        }
        
    def _load_response_patterns(self):
        """Enhanced response patterns for multiple emotions"""
        return {
            'anxiety': [
                "I understand that anxiety can feel overwhelming. It's completely normal to feel this way sometimes.",
                "Anxiety is your mind's way of trying to protect you. Let's work through this together.",
                "Take a deep breath with me. You're safe right now, and these feelings will pass.",
                "I hear that you're feeling anxious. Would you like to try a grounding technique?",
                "Anxiety can make everything feel urgent, but you have the strength to handle this step by step."
            ],
            'depression': [
                "I hear the pain in your words, and I want you to know that your feelings are valid.",
                "Depression can make everything feel heavy. You're not alone in this struggle.",
                "It takes courage to reach out when you're feeling low. I'm glad you're here.",
                "Even small steps forward matter. You don't have to carry this burden alone.",
                "Your feelings are real and important. There is hope, even when it's hard to see."
            ],
            'stress': [
                "Stress can feel like too much to handle sometimes. Let's break this down together.",
                "I understand you're feeling overwhelmed. What's the most pressing thing on your mind?",
                "Stress is your body's response to challenges. You've handled difficult times before.",
                "It sounds like you have a lot on your plate. Let's think about what you can control.",
                "Taking care of yourself during stressful times isn't selfish - it's necessary."
            ],
            'anger': [
                "I can sense your frustration. Anger often comes from feeling unheard or hurt.",
                "It's okay to feel angry. These emotions are telling you something important.",
                "Anger can be powerful energy. Let's think about healthy ways to channel it.",
                "I hear that something has really upset you. Your feelings are completely valid.",
                "Sometimes anger protects us from deeper pain. What's underneath these feelings?"
            ],
            'loneliness': [
                "Feeling lonely can be one of the hardest emotions to sit with. I'm here with you now.",
                "Loneliness doesn't mean you're alone in the universe. You matter, and your feelings matter.",
                "I understand that loneliness can feel endless, but connection is always possible.",
                "Even though you feel isolated, there are people who care about you, including me right now.",
                "Loneliness is a signal that you need connection. That's a very human need."
            ],
            'fear': [
                "Fear is a natural response when we feel threatened or uncertain. You're safe here.",
                "I acknowledge your fear. It takes courage to face what scares us.",
                "Fear often protects us, but sometimes it can hold us back. Let's explore this together.",
                "Your fears are valid. Would you like to talk about what's frightening you?"
            ],
            'sadness': [
                "Sadness is a deep and meaningful emotion. It's okay to sit with these feelings.",
                "I see your sadness, and it's completely valid to feel this way.",
                "Sometimes we need to honor our sadness before we can move through it.",
                "Your tears and sorrow are expressions of your humanity. You don't have to hide them."
            ],
            'happiness': [
                "It's wonderful to hear something positive from you! Tell me more about what's going well.",
                "I can sense the joy in your message. It's great to celebrate these moments.",
                "Your happiness is contagious! What's contributing to these good feelings?",
                "It's beautiful to witness your joy. These moments of happiness are important to acknowledge."
            ],
            'excitement': [
                "Your excitement is infectious! I love hearing about what's energizing you.",
                "It's fantastic that you're feeling so enthusiastic. What's got you so excited?",
                "This energy you're feeling is wonderful. How can we channel it positively?"
            ],
            'calm': [
                "I can sense the peace in your words. It's beautiful when we find moments of calm.",
                "Your sense of tranquility is inspiring. What's helping you feel so centered?",
                "This calm energy you're experiencing is precious. How are you nurturing it?"
            ],
            'confusion': [
                "Feeling confused is completely normal when we're processing complex situations.",
                "It's okay not to have all the answers right now. Let's explore this uncertainty together.",
                "Confusion often comes before clarity. What specific areas feel unclear to you?"
            ],
            'guilt': [
                "Guilt can be a heavy burden to carry. Let's examine these feelings with compassion.",
                "Feeling guilty shows that you care, but remember that you're human and deserve forgiveness.",
                "These feelings of guilt are real, but they don't define your worth as a person."
            ],
            'gratitude': [
                "Gratitude is such a powerful emotion. It's wonderful that you're feeling thankful.",
                "Your appreciation for life's gifts is beautiful. What are you feeling most grateful for?",
                "This sense of gratitude can be a source of strength and joy."
            ],
            'neutral': [
                "I'm here to listen to whatever you'd like to share. How has your day been?",
                "Thank you for reaching out. What's on your mind today?",
                "I'm glad you're here. Is there something specific you'd like to talk about?",
                "How are you feeling right now? I'm here to support you through whatever you're experiencing."
            ]
        }
    
    def _load_coping_strategies(self):
        """Enhanced coping strategies for different emotions"""
        return {
            'breathing': [
                "Try the 4-7-8 breathing technique: Breathe in for 4, hold for 7, exhale for 8.",
                "Focus on your breath. Breathe in slowly through your nose, out through your mouth.",
                "Try box breathing: In for 4, hold for 4, out for 4, hold for 4."
            ],
            'grounding': [
                "Try the 5-4-3-2-1 technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
                "Feel your feet on the ground. Notice the temperature of the air on your skin.",
                "Hold an object and focus on its texture, weight, and temperature."
            ],
            'self_care': [
                "Remember to be gentle with yourself. Self-compassion is not selfish.",
                "Have you eaten or had water recently? Sometimes basic needs affect our mood.",
                "Consider doing something small that brings you comfort - a warm drink, soft music, or a brief walk."
            ],
            'movement': [
                "Sometimes gentle movement can help release tension. Try stretching or a short walk.",
                "Physical activity can help process emotions. Even 5 minutes of movement can make a difference.",
                "Consider dancing to your favorite song or doing some light yoga."
            ],
            'mindfulness': [
                "Try to observe your thoughts without judgment, like clouds passing in the sky.",
                "Practice mindful awareness: notice what you're thinking and feeling without trying to change it.",
                "Ground yourself in the present moment. What do you notice around you right now?"
            ]
        }
    
    def detect_emotions(self, text):
        """Detect multiple emotions in text using enhanced keyword matching"""
        text_lower = text.lower()
        detected_emotions = []
        emotion_scores = {}
        
        # Check for each emotion
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Give higher weight to exact matches
                    if f" {keyword} " in f" {text_lower} ":
                        score += 2
                    else:
                        score += 1
            
            if score > 0:
                emotion_scores[emotion] = score
                detected_emotions.append(emotion)
        
        # Sort emotions by score (highest first)
        if emotion_scores:
            sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
            return [emotion for emotion, score in sorted_emotions]
        
        return ['neutral']
    
    def _analyze_text_sentiment(self, text):
        """Analyze text using TextBlob for additional sentiment context"""
        try:
            blob = TextBlob(text)
            polarity = getattr(blob.sentiment, 'polarity', 0.0)
            
            if polarity > 0.3:
                return 'happiness'
            elif polarity < -0.3:
                return 'sadness'
            elif polarity < -0.1:
                return 'depression'
            else:
                return 'neutral'
        except Exception as e:
            logging.error(f"Error in sentiment analysis: {e}")
            return 'neutral'
    
    def _check_crisis_indicators(self, text):
        """Check for crisis-related keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.crisis_keywords)
    
    def _get_crisis_response(self):
        """Return appropriate crisis response"""
        return """I'm very concerned about what you've shared. Your life has value and meaning. Please reach out for immediate help:

• Call 988 (Suicide & Crisis Lifeline) - available 24/7
• Text HOME to 741741 (Crisis Text Line)
• Call 911 if you're in immediate danger

You don't have to go through this alone. There are people who want to help you, including professional counselors who are trained to support you through this difficult time."""

    def generate_response(self, user_message, session_id):
        """Generate AI response using enhanced emotion detection and memory"""
        try:
            # Check for crisis indicators first
            if self._check_crisis_indicators(user_message):
                return self._get_crisis_response(), ['crisis'], 'crisis', -1.0
            
            # Get conversation context for better memory
            context = self._get_conversation_context(session_id, limit=5)
            
            # Detect multiple emotions
            detected_emotions = self.detect_emotions(user_message)
            
            # Get sentiment analysis as backup
            sentiment_emotion = self._analyze_text_sentiment(user_message)
            
            # Combine emotion detection with sentiment
            if sentiment_emotion not in detected_emotions and sentiment_emotion != 'neutral':
                detected_emotions.append(sentiment_emotion)
            
            # Choose primary emotion
            primary_emotion = detected_emotions[0] if detected_emotions else 'neutral'
            
            # Get appropriate response pattern
            if primary_emotion in self.response_patterns:
                responses = self.response_patterns[primary_emotion]
            else:
                responses = self.response_patterns['neutral']
            
            base_response = random.choice(responses)
            
            # Add personalization based on conversation history
            if context and len(context) > 2:
                personalization = self._add_context_personalization(context, user_message, detected_emotions)
                if personalization:
                    base_response += f" {personalization}"
            
            # Add coping strategy if appropriate
            if primary_emotion in ['anxiety', 'stress', 'depression', 'anger', 'fear', 'sadness']:
                coping_category = self._get_coping_category(primary_emotion)
                if coping_category and random.random() < 0.6:  # 60% chance
                    coping_suggestion = random.choice(self.coping_strategies[coping_category])
                    base_response += f"\n\n{coping_suggestion}"
            
            # Add encouraging follow-up for difficult emotions
            if primary_emotion in ['depression', 'loneliness', 'anxiety', 'sadness', 'fear', 'guilt']:
                encouragements = [
                    "Remember, it's okay to take things one moment at a time.",
                    "You're showing strength by reaching out and talking about this.",
                    "Your feelings are valid, and so are you.",
                    "It's okay to not be okay sometimes. Healing isn't linear.",
                    "You're not alone in this journey."
                ]
                base_response += f"\n\n{random.choice(encouragements)}"
            
            # Calculate overall sentiment score
            sentiment_score = self._calculate_sentiment_score(detected_emotions)
            
            return base_response, detected_emotions, primary_emotion, sentiment_score
            
        except Exception as e:
            logging.error(f"Error generating local AI response: {e}")
            return ("I want you to know that I'm here for you, even though I'm having some technical difficulties right now. "
                   "Your feelings and experiences matter. If you're in crisis, please don't hesitate to reach out to a mental health professional or call 988 for the Suicide & Crisis Lifeline."), ['neutral'], 'neutral', 0.0
    
    def _get_conversation_context(self, session_id, limit=5):
        """Get recent conversation history for enhanced context"""
        try:
            recent_conversations = Conversation.query.filter_by(
                session_id=session_id
            ).order_by(Conversation.timestamp.desc()).limit(limit).all()
            
            context = []
            for conv in reversed(recent_conversations):
                context.append({
                    "role": "user", 
                    "content": conv.user_message,
                    "emotions": json.loads(conv.emotions) if conv.emotions else [],
                    "primary_emotion": conv.primary_emotion
                })
                context.append({"role": "assistant", "content": conv.ai_response})
            
            return context
        except Exception as e:
            logging.error(f"Error getting conversation context: {e}")
            return []
    
    def _add_context_personalization(self, context, current_message, current_emotions):
        """Add personalization based on conversation history and emotion patterns"""
        try:
            # Analyze emotion patterns over time
            user_messages = [msg for msg in context if msg["role"] == "user"]
            
            if len(user_messages) < 2:
                return ""
            
            # Check for recurring emotions
            all_emotions = []
            for msg in user_messages:
                if "emotions" in msg and msg["emotions"]:
                    all_emotions.extend(msg["emotions"])
            
            # Check for recurring themes
            all_text = " ".join([msg["content"] for msg in user_messages] + [current_message])
            
            # Pattern matching for recurring concerns
            if 'anxiety' in all_emotions and 'anxiety' in current_emotions:
                return "I notice anxiety has been a recurring theme in our conversations. You're not alone in this struggle."
            
            if 'stress' in all_emotions and any(emotion in current_emotions for emotion in ['stress', 'overwhelmed']):
                return "It seems like stress has been weighing on you lately. Let's work on finding some relief."
            
            if 'work' in all_text.lower() and 'stress' in all_emotions:
                return "Work stress seems to be a consistent challenge for you."
            
            if 'sleep' in all_text.lower() or 'tired' in all_text.lower():
                return "I've noticed sleep and rest have come up in our conversations. Quality rest is so important for mental health."
            
            return ""
            
        except Exception as e:
            logging.error(f"Error adding context personalization: {e}")
            return ""
    
    def _get_coping_category(self, emotion):
        """Map emotions to appropriate coping strategies"""
        emotion_to_coping = {
            'anxiety': 'breathing',
            'stress': 'breathing', 
            'anger': 'movement',
            'depression': 'self_care',
            'sadness': 'self_care',
            'fear': 'grounding',
            'confusion': 'mindfulness',
            'loneliness': 'self_care'
        }
        return emotion_to_coping.get(emotion)
    
    def _calculate_sentiment_score(self, emotions):
        """Calculate overall sentiment score based on detected emotions"""
        positive_emotions = ['happiness', 'excitement', 'calm', 'gratitude']
        negative_emotions = ['depression', 'anxiety', 'anger', 'sadness', 'fear', 'loneliness', 'guilt']
        
        positive_count = sum(1 for emotion in emotions if emotion in positive_emotions)
        negative_count = sum(1 for emotion in emotions if emotion in negative_emotions)
        
        if positive_count > negative_count:
            return min(0.8, positive_count * 0.3)
        elif negative_count > positive_count:
            return max(-0.8, -negative_count * 0.3)
        else:
            return 0.0


# Global instance
ai_service = LocalAIService()

def get_ai_response(user_message, session_id):
    """Main function to get AI response with enhanced features"""
    return ai_service.generate_response(user_message, session_id)
