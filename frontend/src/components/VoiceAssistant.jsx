import React, { useState, useRef } from 'react';

const VoiceAssistant = () => {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [aiResponse, setAiResponse] = useState('');
    const recognitionRef = useRef(null);

    const startListening = () => {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new window.webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            
            recognition.onstart = () => {
                setIsListening(true);
            };
            
            recognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0])
                    .map(result => result.transcript)
                    .join('');
                setTranscript(transcript);
            };
            
            recognition.onend = () => {
                setIsListening(false);
                processVoiceCommand(transcript);
            };
            
            recognition.start();
            recognitionRef.current = recognition;
        } else {
            alert('Speech recognition not supported in this browser.');
        }
    };

    const stopListening = () => {
        if (recognitionRef.current) {
            recognitionRef.current.stop();
        }
    };

    const processVoiceCommand = async (command) => {
        try {
            const response = await fetch('http://localhost:8000/api/v1/ask-question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: command,
                    context: 'cooking assistance'
                })
            });
            
            const data = await response.json();
            setAiResponse(data.answer);
            
            // Speak the response
            speakText(data.answer);
            
        } catch (error) {
            console.error('Error processing voice command:', error);
        }
    };

    const speakText = (text) => {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.8;
            utterance.pitch = 1;
            window.speechSynthesis.speak(utterance);
        }
    };

    return (
        <div className="voice-assistant">
            <h3>Voice Assistant</h3>
            <button 
                onClick={isListening ? stopListening : startListening}
                className={`listen-btn ${isListening ? 'listening' : ''}`}
            >
                {isListening ? 'Stop Listening' : 'Start Voice Command'}
            </button>
            
            {transcript && (
                <div className="transcript">
                    <strong>You said:</strong> {transcript}
                </div>
            )}
            
            {aiResponse && (
                <div className="ai-response">
                    <strong>Assistant:</strong> {aiResponse}
                </div>
            )}
        </div>
    );
};

export default VoiceAssistant;