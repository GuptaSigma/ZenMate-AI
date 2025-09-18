document.addEventListener('DOMContentLoaded', () => {
    // Check if the browser supports the Web Speech API
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        console.warn("Speech Recognition API not supported in this browser.");
        // Hide all voice-related buttons if not supported
        document.querySelectorAll('#voiceBtn, #voiceToggle, #voiceStartBtn').forEach(btn => btn.style.display = 'none');
        return;
    }

    // Get references to all the necessary HTML elements
    const voiceBtn = document.getElementById('voiceBtn');
    const messageInput = document.getElementById('messageInput');
    const chatForm = document.getElementById('chatForm');
    const voiceStatus = document.getElementById('voiceStatus');
    const voiceStatusText = document.getElementById('voiceStatusText');
    const stopVoiceBtn = document.getElementById('stopVoice');
    const voiceStartBtn = document.getElementById('voiceStartBtn'); // Button on the welcome screen

    // Initialize the Speech Recognition engine
    const recognition = new SpeechRecognition();
    recognition.continuous = false; // Stop listening after a pause
    recognition.lang = 'en-US';      // You can change this to your preferred language
    recognition.interimResults = true; // Show results as you speak

    let isListening = false;
    let final_transcript = '';

    // --- Event Handlers for the Recognition Process ---

    // When recognition starts
    recognition.onstart = () => {
        isListening = true;
        final_transcript = '';
        voiceStatus.classList.remove('d-none'); // Show the "Listening..." bar
        voiceStatusText.textContent = 'Listening...';
        voiceBtn.classList.add('active'); // Indicate the button is active
        console.log('Voice recognition started.');
    };

    // When recognition ends
    recognition.onend = () => {
        isListening = false;
        voiceStatus.classList.add('d-none'); // Hide the status bar
        voiceBtn.classList.remove('active');
        console.log('Voice recognition stopped.');
        
        // If there is a final transcript, submit the form
        if (final_transcript.trim()) {
            messageInput.value = final_transcript; // Ensure the final text is in the input
            chatForm.submit(); // Automatically send the message
        }
    };

    // When an error occurs
    recognition.onerror = (event) => {
        if (event.error === 'no-speech') {
            voiceStatusText.textContent = "Didn't catch that. Try again.";
        } else if (event.error === 'not-allowed') {
            voiceStatusText.textContent = 'Microphone access denied.';
            alert("You need to allow microphone access to use the voice feature.");
        } else {
            voiceStatusText.textContent = `Error: ${event.error}`;
        }
        console.error('Speech recognition error:', event.error);
    };

    // When speech is detected and transcribed
    recognition.onresult = (event) => {
        let interim_transcript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                final_transcript += event.results[i][0].transcript;
            } else {
                interim_transcript += event.results[i][0].transcript;
            }
        }
        // Update the text area with the live transcript
        messageInput.value = final_transcript + interim_transcript;
    };

    // --- Button Click Handlers ---

    // Main voice button in the input bar
    voiceBtn.addEventListener('click', () => {
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });
    
    // Stop button on the status bar
    stopVoiceBtn.addEventListener('click', () => {
        if (isListening) {
            recognition.stop();
        }
    });

    // "Try Voice Input" button on the welcome screen
    if(voiceStartBtn) {
        voiceStartBtn.addEventListener('click', () => {
             if (!isListening) {
                recognition.start();
            }
        });
    }
});