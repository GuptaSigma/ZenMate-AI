from extensions import db
from datetime import datetime
from sqlalchemy import Text

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    user_message = db.Column(Text, nullable=False)
    ai_response = db.Column(Text, nullable=False)
    emotions = db.Column(Text, nullable=True)  # JSON string of detected emotions
    primary_emotion = db.Column(db.String(50), nullable=True)
    sentiment_score = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, session_id, user_message, ai_response, emotions=None, primary_emotion=None, sentiment_score=None):
        self.session_id = session_id
        self.user_message = user_message
        self.ai_response = ai_response
        self.emotions = emotions
        self.primary_emotion = primary_emotion
        self.sentiment_score = sentiment_score
    
    def __repr__(self):
        return f'<Conversation {self.id}: {self.session_id}>'

class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, session_id):
        self.session_id = session_id
    
    def __repr__(self):
        return f'<UserSession {self.session_id}>'

class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    emotion = db.Column(db.String(50), nullable=False)
    suggestion_type = db.Column(db.String(50), nullable=False)  # quote, resource, article, technique
    content = db.Column(Text, nullable=False)
    title = db.Column(db.String(200), nullable=True)
    url = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, session_id, emotion, suggestion_type, content, title=None, url=None):
        self.session_id = session_id
        self.emotion = emotion
        self.suggestion_type = suggestion_type
        self.content = content
        self.title = title
        self.url = url
    
    def __repr__(self):
        return f'<Suggestion {self.id}: {self.emotion} - {self.suggestion_type}>'
