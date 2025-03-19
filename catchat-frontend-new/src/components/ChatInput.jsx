import { useState, useRef, useEffect } from 'react';
import '../App.css';

function ChatInput({ onSubmit, isLoading }) {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);
  
  // Auto-resize text input with max height limit
  useEffect(() => {
    if (textareaRef.current) {
      // Reset height to auto to get the correct scrollHeight
      textareaRef.current.style.height = 'auto';
      // Set new height based on scrollHeight, with a max of 150px
      const newHeight = Math.min(textareaRef.current.scrollHeight, 150);
      textareaRef.current.style.height = `${newHeight}px`;
    }
  }, [input]);
  
  // Auto-focus the textarea on component mount
  useEffect(() => {
    textareaRef.current?.focus();
  }, []);
  
  const handleSubmit = () => {
    if (isLoading || !input.trim()) return;
    onSubmit(input);
    setInput('');
    // Reset textarea height
    setTimeout(() => {
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }, 0);
  };
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };
  
  return (
    <div className="input-container gold-trim">
      <div className="input-area">
        <textarea
          ref={textareaRef}
          className="text-input"
          placeholder="What do you want to know?"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          disabled={isLoading}
        />
      </div>
      <div className="input-toolbar">
        <div className="toolbar-left">
          {/* Left side is empty */}
        </div>
        <div className="toolbar-right">
          <button
            className={`send-button ${isLoading ? 'loading' : ''}`}
            aria-label="Submit"
            onClick={handleSubmit}
            disabled={isLoading || !input.trim()}
          >
            {isLoading ? (
              <div className="loading-indicator"></div>
            ) : (
              <span className="send-text">Send</span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatInput;
