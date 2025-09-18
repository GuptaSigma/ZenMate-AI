// Enhanced MindfulChat Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initializeChatInterface();
    initializeSuggestions();
    initializeKeyboardShortcuts();
    initializeAccessibility();
    initializeAnimations();
    
    console.log('Enhanced MindfulChat initialized');
});

function initializeChatInterface() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    
    if (!chatForm || !messageInput) return;
    
    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
    
    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        const message = messageInput.value.trim();
        if (!message) {
            e.preventDefault();
            return;
        }
        
        // Add loading state
        sendButton.classList.add('loading');
        sendButton.disabled = true;
        
        // The form will submit normally, but we show loading state
        setTimeout(() => {
            if (sendButton) {
                sendButton.classList.remove('loading');
                sendButton.disabled = false;
            }
        }, 1000);
    });
    
    // Handle keyboard shortcuts
    messageInput.addEventListener('keydown', function(e) {
        // Shift + Enter for new line, Enter to send
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.requestSubmit();
        }
    });
    
    // Auto-scroll to bottom
    if (chatMessages) {
        scrollToBottom();
    }
    
    // Initialize suggestion buttons
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const message = this.getAttribute('data-message');
            if (message && messageInput) {
                messageInput.value = message;
                messageInput.focus();
                // Auto-resize
                messageInput.style.height = 'auto';
                messageInput.style.height = messageInput.scrollHeight + 'px';
            }
        });
    });
    
    // Initialize speak buttons
    const speakBtns = document.querySelectorAll('.speak-btn');
    speakBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const text = this.getAttribute('data-text');
            if (text && 'speechSynthesis' in window) {
                speakText(text, btn);
            } else {
                showNotification('Text-to-speech not supported in your browser', 'warning');
            }
        });
    });
}

function initializeSuggestions() {
    // Handle suggestion card interactions
    const suggestionCards = document.querySelectorAll('.suggestion-card');
    suggestionCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking on a link
            if (e.target.tagName === 'A') return;
            
            // Add some visual feedback
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
    
    // Smooth scrolling for suggestion panel
    const suggestionsScroll = document.querySelector('.suggestions-scroll');
    if (suggestionsScroll) {
        suggestionsScroll.addEventListener('wheel', function(e) {
            e.preventDefault();
            this.scrollLeft += e.deltaY;
        });
    }
}

function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Alt + M to focus message input
        if (e.altKey && e.key === 'm') {
            e.preventDefault();
            const messageInput = document.getElementById('messageInput');
            if (messageInput) {
                messageInput.focus();
            }
        }
        
        // Alt + V for voice toggle
        if (e.altKey && e.key === 'v') {
            e.preventDefault();
            const voiceBtn = document.getElementById('voiceBtn');
            if (voiceBtn && !voiceBtn.disabled) {
                voiceBtn.click();
            }
        }
        
        // Escape to stop voice
        if (e.key === 'Escape') {
            const stopVoice = document.getElementById('stopVoice');
            if (stopVoice && !stopVoice.classList.contains('d-none')) {
                stopVoice.click();
            }
        }
    });
}

function initializeAccessibility() {
    // Add ARIA labels for dynamic content
    const emotionTags = document.querySelectorAll('.emotion-tag');
    emotionTags.forEach(tag => {
        if (!tag.getAttribute('aria-label')) {
            const title = tag.getAttribute('title');
            if (title) {
                tag.setAttribute('aria-label', `Emotion detected: ${title}`);
            }
        }
    });
    
    // Announce new messages to screen readers
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === Node.ELEMENT_NODE && 
                        node.classList && node.classList.contains('message-group')) {
                        // Announce new message
                        announceToScreenReader('New message received');
                    }
                });
            }
        });
    });
    
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        observer.observe(chatMessages, { childList: true });
    }
}

function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe message groups
    const messageGroups = document.querySelectorAll('.message-group');
    messageGroups.forEach(group => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        group.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(group);
    });
}

function speakText(text, button) {
    if (!('speechSynthesis' in window)) {
        showNotification('Text-to-speech not supported', 'warning');
        return;
    }
    
    // Stop any ongoing speech
    speechSynthesis.cancel();
    
    // Create utterance
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Configure speech
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 0.8;
    
    // Update button state
    const originalIcon = button.querySelector('i');
    const originalText = button.querySelector('.btn').textContent || button.textContent;
    
    button.disabled = true;
    button.innerHTML = '<i data-feather="square" class="me-1"></i>Stop';
    feather.replace();
    
    // Handle speech events
    utterance.onstart = function() {
        console.log('Speech started');
    };
    
    utterance.onend = function() {
        button.disabled = false;
        button.innerHTML = '<i data-feather="volume-2" class="me-1"></i>Listen';
        feather.replace();
    };
    
    utterance.onerror = function(event) {
        console.error('Speech error:', event.error);
        button.disabled = false;
        button.innerHTML = '<i data-feather="volume-2" class="me-1"></i>Listen';
        feather.replace();
        showNotification('Speech synthesis failed', 'error');
    };
    
    // Start speaking
    speechSynthesis.speak(utterance);
    
    // Add click handler to stop speech
    const stopHandler = function() {
        speechSynthesis.cancel();
        button.removeEventListener('click', stopHandler);
    };
    button.addEventListener('click', stopHandler);
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.style.cssText = `
        position: absolute;
        left: -10000px;
        width: 1px;
        height: 1px;
        overflow: hidden;
    `;
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// Utility function to format timestamps
function formatTimestamp(date) {
    return new Intl.DateTimeFormat('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    }).format(date);
}

// Utility function to detect emotion from text (client-side backup)
function detectBasicEmotion(text) {
    const emotionKeywords = {
        happy: ['happy', 'joy', 'great', 'wonderful', 'amazing', 'fantastic'],
        sad: ['sad', 'down', 'depressed', 'blue', 'unhappy'],
        angry: ['angry', 'mad', 'furious', 'annoyed', 'frustrated'],
        anxious: ['anxious', 'worried', 'nervous', 'scared', 'afraid'],
        excited: ['excited', 'thrilled', 'pumped', 'energetic']
    };
    
    const lowerText = text.toLowerCase();
    const detectedEmotions = [];
    
    for (const [emotion, keywords] of Object.entries(emotionKeywords)) {
        for (const keyword of keywords) {
            if (lowerText.includes(keyword)) {
                detectedEmotions.push(emotion);
                break;
            }
        }
    }
    
    return detectedEmotions.length > 0 ? detectedEmotions : ['neutral'];
}

// Export functions for voice.js
window.MindfulChat = {
    scrollToBottom,
    showNotification,
    announceToScreenReader,
    formatTimestamp,
    detectBasicEmotion,
    speakText
};
