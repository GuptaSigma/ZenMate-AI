import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import logging

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    logging.info("Downloading NLTK vader_lexicon...")
    nltk.download('vader_lexicon', quiet=True)

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyze sentiment of text using NLTK's VADER sentiment analyzer
    Returns: (sentiment_score, sentiment_label)
    """
    try:
        scores = sia.polarity_scores(text)
        compound_score = scores['compound']
        
        # Determine sentiment label based on compound score
        if compound_score >= 0.05:
            label = 'positive'
        elif compound_score <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        
        return compound_score, label
        
    except Exception as e:
        logging.error(f"Error analyzing sentiment: {e}")
        return 0.0, 'neutral'

def get_sentiment_emoji(sentiment_label):
    """Get emoji representation of sentiment"""
    emoji_map = {
        'positive': '😊',
        'neutral': '😐',
        'negative': '😔'
    }
    return emoji_map.get(sentiment_label, '😐')

def get_emotion_emoji(emotion):
    """Get emoji representation of specific emotions"""
    emoji_map = {
        'happiness': '😊',
        'excitement': '🎉',
        'calm': '😌',
        'gratitude': '🙏',
        'anxiety': '😰',
        'depression': '😔',
        'stress': '😤',
        'anger': '😠',
        'fear': '😨',
        'sadness': '😢',
        'loneliness': '😞',
        'confusion': '😕',
        'guilt': '😣',
        'neutral': '😐'
    }
    return emoji_map.get(emotion, '😐')
