import React, { useEffect, useRef } from 'react';
import './ChatDisplay.css';

function ChatDisplay({ messages }) {
  const messagesEndRef = useRef(null);
  const chatDisplayRef = useRef(null);
  
  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className="chat-display" ref={chatDisplayRef}>
      {messages.length === 0 ? (
        <div className="empty-chat"></div>
      ) : (
        messages.map((message, index) => (
          <div
            key={index}
            className={`message-container ${message.type === 'user' ? 'user-container' : 'bot-container'}`}
          >
            <div className={`message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}>
              {/* Render message content as string, with line breaks preserved */}
              <div style={{ whiteSpace: 'pre-wrap' }}>
                {String(message.content || '')}
              </div>
            </div>
          </div>
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}

export default ChatDisplay;
