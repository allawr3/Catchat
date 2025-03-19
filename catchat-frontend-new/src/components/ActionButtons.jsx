import React from 'react';

function ActionButtons({ isLoading, onGenerateQuantumThought, onAnalyzeBitcoinData, onGenerateCode }) {
  return (
    <div className="action-buttons">
      <button 
        className="action-button gold-action"
        onClick={onGenerateQuantumThought}
        disabled={isLoading}
      >
        <svg className="action-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span>Generate Quantum Thought</span>
      </button>
      
      <button 
        className="action-button gold-action"
        onClick={onAnalyzeBitcoinData}
        disabled={isLoading}
      >
        <svg className="action-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <span>Analyze Bitcoin Data</span>
      </button>
      
      <button 
        className="action-button gold-action"
        onClick={onGenerateCode}
        disabled={isLoading}
      >
        <svg className="action-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
        </svg>
        <span>Generate Code</span>
      </button>
    </div>
  );
}

export default ActionButtons;
