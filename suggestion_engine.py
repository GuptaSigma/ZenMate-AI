import random
import logging
from models import Suggestion, db

class SuggestionEngine:
    def __init__(self):
        self.suggestions_db = self._load_suggestions_database()
        
    def _load_suggestions_database(self):
        """Load comprehensive suggestions database for each emotion"""
        return {
            'anxiety': {
                'quotes': [
                    "You are braver than you believe, stronger than you seem, and smarter than you think. - A.A. Milne",
                    "Anxiety is the mark of spiritual insecurity. - Thomas Merton",
                    "The greatest weapon against stress is our ability to choose one thought over another. - William James",
                    "Nothing can bring you peace but yourself. - Ralph Waldo Emerson"
                ],
                'techniques': [
                    "Progressive Muscle Relaxation: Tense and release each muscle group for 5 seconds",
                    "Mindful Breathing: Focus on your breath for 2 minutes without judgment",
                    "Grounding Exercise: Name 5 things you can see, 4 you can hear, 3 you can touch",
                    "Journaling: Write down 3 things causing anxiety and 3 potential solutions"
                ],
                'resources': [
                    {
                        'title': 'Anxiety and Depression Association',
                        'description': 'Professional resources and support groups for anxiety',
                        'url': 'https://adaa.org'
                    },
                    {
                        'title': 'Calm App - Anxiety Programs',
                        'description': 'Guided meditations specifically for anxiety relief',
                        'url': 'https://calm.com'
                    }
                ]
            },
            'depression': {
                'quotes': [
                    "Even the darkest night will end and the sun will rise. - Victor Hugo",
                    "You are stronger than you know. More resilient than you think.",
                    "Depression is not a sign of weakness. It's a sign that you've been strong for too long.",
                    "Your current situation is not your final destination."
                ],
                'techniques': [
                    "Daily Gratitude Practice: Write down 3 things you're grateful for each day",
                    "Gentle Movement: Take a 10-minute walk outside or do light stretching",
                    "Connect with Nature: Spend time outdoors, even if just on a balcony",
                    "Reach Out: Send a message to one friend or family member today"
                ],
                'resources': [
                    {
                        'title': 'National Alliance on Mental Illness',
                        'description': 'Support groups and educational resources for depression',
                        'url': 'https://nami.org'
                    },
                    {
                        'title': 'Depression and Bipolar Support Alliance',
                        'description': 'Peer support and mental health resources',
                        'url': 'https://dbsalliance.org'
                    }
                ]
            },
            'stress': {
                'quotes': [
                    "You have been assigned this mountain to show others it can be moved.",
                    "Stress is caused by being 'here' but wanting to be 'there'. - Eckhart Tolle",
                    "Take time to make your soul happy.",
                    "The greatest weapon against stress is our ability to choose one thought over another."
                ],
                'techniques': [
                    "Time Management: List your tasks and prioritize the top 3 most important",
                    "Deep Breathing: Try 4-7-8 breathing (inhale 4, hold 7, exhale 8)",
                    "Boundary Setting: Practice saying 'no' to one non-essential commitment",
                    "Mini Breaks: Take 5-minute breaks every hour to reset your mind"
                ],
                'resources': [
                    {
                        'title': 'American Psychological Association - Stress',
                        'description': 'Evidence-based stress management techniques',
                        'url': 'https://apa.org/topics/stress'
                    },
                    {
                        'title': 'Headspace - Stress Relief',
                        'description': 'Guided meditations for stress management',
                        'url': 'https://headspace.com'
                    }
                ]
            },
            'anger': {
                'quotes': [
                    "Anger is an acid that can do more harm to the vessel in which it is stored than to anything on which it is poured. - Mark Twain",
                    "The best fighter is never angry. - Lao Tzu",
                    "Speak when you are angry and you will make the best speech you will ever regret. - Ambrose Bierce",
                    "Holding onto anger is like grasping a hot coal with the intent of throwing it at someone else."
                ],
                'techniques': [
                    "Count to 10: Take slow, deep breaths while counting to give yourself time",
                    "Physical Release: Do jumping jacks, push-ups, or punch a pillow",
                    "Identify Triggers: Write down what specifically made you angry",
                    "Perspective Check: Ask yourself if this will matter in 5 years"
                ],
                'resources': [
                    {
                        'title': 'American Psychological Association - Anger',
                        'description': 'Professional strategies for anger management',
                        'url': 'https://apa.org/topics/anger'
                    }
                ]
            },
            'sadness': {
                'quotes': [
                    "Tears are words that need to be written. - Paulo Coelho",
                    "The cure for anything is salt water: sweat, tears, or the sea. - Isak Dinesen",
                    "Sadness gives depth. Happiness gives height. Sadness gives roots. Happiness gives branches.",
                    "It's okay to not be okay. It's okay to cry. It's okay to feel sad."
                ],
                'techniques': [
                    "Allow the Feeling: Give yourself permission to feel sad without judgment",
                    "Creative Expression: Draw, write, or listen to music that matches your mood",
                    "Comfort Activities: Make tea, take a warm bath, or wrap yourself in a soft blanket",
                    "Memory Reflection: Look at photos or remember happy moments"
                ],
                'resources': [
                    {
                        'title': 'Mental Health America',
                        'description': 'Resources for understanding and coping with sadness',
                        'url': 'https://mhanational.org'
                    }
                ]
            },
            'happiness': {
                'quotes': [
                    "Happiness is not something ready-made. It comes from your own actions. - Dalai Lama",
                    "The secret of being happy is accepting where you are in life and making the most out of everyday.",
                    "Happiness is a choice, not a result. Nothing will make you happy until you choose to be happy.",
                    "Collect moments, not things."
                ],
                'techniques': [
                    "Gratitude Expansion: Share your happiness with someone who matters to you",
                    "Happiness Journal: Write about what's making you feel good right now",
                    "Pay It Forward: Do something kind for someone else to spread the joy",
                    "Savor the Moment: Take time to really appreciate this positive feeling"
                ],
                'resources': [
                    {
                        'title': 'Greater Good Science Center',
                        'description': 'Research-based practices for happiness and well-being',
                        'url': 'https://greatergood.berkeley.edu'
                    }
                ]
            },
            'loneliness': {
                'quotes': [
                    "The greatest thing in the world is to know how to belong to oneself. - Michel de Montaigne",
                    "You are never alone. You are eternally connected with everyone.",
                    "Loneliness is not lack of company, loneliness is lack of purpose. - Guillermo Maldonado",
                    "The eternal quest of the individual human being is to shatter his loneliness."
                ],
                'techniques': [
                    "Virtual Connection: Reach out to an old friend via text or call",
                    "Community Engagement: Join an online group or local activity",
                    "Self-Companionship: Practice being comfortable with yourself through meditation",
                    "Volunteer: Help others to create meaningful connections"
                ],
                'resources': [
                    {
                        'title': 'Campaign to End Loneliness',
                        'description': 'Resources and support for dealing with loneliness',
                        'url': 'https://campaigntoendloneliness.org'
                    }
                ]
            }
        }
    
    def get_suggestions(self, session_id, emotions, limit=3):
        """Get personalized suggestions based on detected emotions"""
        try:
            suggestions = []
            
            for emotion in emotions[:2]:  # Focus on top 2 emotions
                if emotion in self.suggestions_db:
                    emotion_suggestions = self.suggestions_db[emotion]
                    
                    # Add a quote
                    if 'quotes' in emotion_suggestions:
                        quote = random.choice(emotion_suggestions['quotes'])
                        suggestions.append(self._create_suggestion(
                            session_id, emotion, 'quote', quote, 'Inspirational Quote'
                        ))
                    
                    # Add a technique
                    if 'techniques' in emotion_suggestions:
                        technique = random.choice(emotion_suggestions['techniques'])
                        suggestions.append(self._create_suggestion(
                            session_id, emotion, 'technique', technique, 'Coping Technique'
                        ))
                    
                    # Add a resource
                    if 'resources' in emotion_suggestions and random.random() < 0.5:
                        resource = random.choice(emotion_suggestions['resources'])
                        suggestions.append(self._create_suggestion(
                            session_id, emotion, 'resource', 
                            resource['description'], resource['title'], resource['url']
                        ))
            
            # Limit number of suggestions
            return suggestions[:limit]
            
        except Exception as e:
            logging.error(f"Error getting suggestions: {e}")
            return []
    
    def _create_suggestion(self, session_id, emotion, suggestion_type, content, title=None, url=None):
        """Create and save a suggestion to the database"""
        suggestion = Suggestion(
            session_id=session_id,
            emotion=emotion,
            suggestion_type=suggestion_type,
            content=content,
            title=title,
            url=url
        )
        
        try:
            db.session.add(suggestion)
            db.session.commit()
        except Exception as e:
            logging.error(f"Error saving suggestion: {e}")
            db.session.rollback()
        
        return suggestion
    
    def get_recent_suggestions(self, session_id, limit=5):
        """Get recent suggestions for a session"""
        try:
            return Suggestion.query.filter_by(
                session_id=session_id
            ).order_by(Suggestion.timestamp.desc()).limit(limit).all()
        except Exception as e:
            logging.error(f"Error getting recent suggestions: {e}")
            return []

# Global instance
suggestion_engine = SuggestionEngine()
