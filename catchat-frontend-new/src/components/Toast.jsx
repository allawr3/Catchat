import React from 'react';

function Toast({ message, show }) {
  return (
    <div className={`toast ${show ? 'show' : ''}`}>
      <span>{message}</span>
    </div>
  );
}

export default Toast;
