from flask import render_template, request, session, redirect, url_for, flash, jsonify
from app import app
from extensions import db
from models import Conversation, UserSession, Suggestion
from ai_service import get_ai_response
from sentiment_analyzer import analyze_sentiment, get_emotion_emoji
from suggestion_engine import suggestion_engine
import uuid
import json
from datetime import datetime
import logging

import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed
    engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)  # Usually female at index 1
    engine.say(text)
    engine.runAndWait()


@app.route('/')
def index():
    """Landing page with introduction to the mental health companion"""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """Main chat interface with enhanced features"""
    # Create or get session ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        
        # Create user session record
        user_session = UserSession(session_id=session['session_id'])
        db.session.add(user_session)
        db.session.commit()
    
    # Update last active time
    user_session = UserSession.query.filter_by(session_id=session['session_id']).first()
    if user_session:
        user_session.last_active = datetime.utcnow()
        db.session.commit()
    
    # Get conversation history
    conversations = Conversation.query.filter_by(
        session_id=session['session_id']
    ).order_by(Conversation.timestamp).all()
    
    # Get recent suggestions
    recent_suggestions = suggestion_engine.get_recent_suggestions(session['session_id'], limit=3)
    
    return render_template('chat.html', conversations=conversations, recent_suggestions=recent_suggestions)

@app.route('/send_message', methods=['POST'])
def send_message():
    """Process user message with enhanced emotion detection and suggestions"""
    if 'session_id' not in session:
        return redirect(url_for('chat'))
    
    user_message = request.form.get('message', '').strip()
    
    if not user_message:
        flash('Please enter a message.', 'warning')
        return redirect(url_for('chat'))
    
    try:
        logging.info(f"Processing message: {user_message[:50]}... for session: {session['session_id']}")
        
        # Get enhanced AI response with emotion detection
        ai_response, detected_emotions, primary_emotion, sentiment_score = get_ai_response(user_message, session['session_id'])
        logging.info(f"Detected emotions: {detected_emotions}, Primary: {primary_emotion}")
        
        # Generate personalized suggestions
        suggestions = suggestion_engine.get_suggestions(session['session_id'], detected_emotions)
        logging.info(f"Generated {len(suggestions)} suggestions")
        
        # Save conversation with enhanced emotion data
        conversation = Conversation(
            session_id=session['session_id'],
            user_message=user_message,
            ai_response=ai_response,
            emotions=json.dumps(detected_emotions),
            primary_emotion=primary_emotion,
            sentiment_score=sentiment_score
        )
        db.session.add(conversation)
        db.session.commit()
        
        logging.info(f"Conversation saved successfully: ID {conversation.id}")
        flash('Message sent successfully!', 'success')
        
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        import traceback
        logging.error(f"Full traceback: {traceback.format_exc()}")
        flash('Sorry, I encountered an error. Please try again.', 'error')
    
    return redirect(url_for('chat'))

@app.route('/voice_message', methods=['POST'])
def voice_message():
    """Process voice message (same as text message but from voice input)"""
    if 'session_id' not in session:
        return jsonify({'error': 'No session found'}), 400
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        logging.info(f"Processing voice message: {user_message[:50]}... for session: {session['session_id']}")
        
        # Get enhanced AI response
        ai_response, detected_emotions, primary_emotion, sentiment_score = get_ai_response(user_message, session['session_id'])
        
        # Generate suggestions
        suggestions = suggestion_engine.get_suggestions(session['session_id'], detected_emotions)
        
        # Save conversation
        conversation = Conversation(
            session_id=session['session_id'],
            user_message=user_message,
            ai_response=ai_response,
            emotions=json.dumps(detected_emotions),
            primary_emotion=primary_emotion,
            sentiment_score=sentiment_score
        )
        db.session.add(conversation)
        db.session.commit()
        
        # Format response for JSON
        response_data = {
            'ai_response': ai_response,
            'emotions': detected_emotions,
            'primary_emotion': primary_emotion,
            'emotion_emoji': get_emotion_emoji(primary_emotion),
            'suggestions': [
                {
                    'type': s.suggestion_type,
                    'content': s.content,
                    'title': s.title,
                    'url': s.url,
                    'emotion': s.emotion
                } for s in suggestions
            ],
            'timestamp': conversation.timestamp.strftime('%I:%M %p')
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logging.error(f"Error processing voice message: {str(e)}")
        return jsonify({'error': 'Failed to process voice message'}), 500

@app.route('/resources')
def resources():
    """Crisis resources and mental health information"""
    return render_template('resources.html')

@app.route('/new_session')
def new_session():
    """Start a new chat session"""
    session.pop('session_id', None)
    return redirect(url_for('chat'))

@app.route('/play_audio')
def play_audio():
    """Audio player test page"""
    return render_template('audio_test.html')

@app.template_filter('emotion_emoji')
def emotion_emoji_filter(emotion):
    """Template filter to get emotion emoji"""
    return get_emotion_emoji(emotion)

@app.template_filter('parse_emotions')
def parse_emotions_filter(emotions_json):
    """Template filter to parse emotions JSON"""
    try:
        return json.loads(emotions_json) if emotions_json else []
    except:
        return []