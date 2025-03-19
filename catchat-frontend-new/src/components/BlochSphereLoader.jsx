// BlochSphereLoader.jsx
import React from 'react';
import '../App.css';

const BlochSphereLoader = () => {
  return (
    <div className="loading-overlay">
      <div className="quantum-measurement">
        <div className="bloch-sphere">
          <div className="sphere sphere-outer"></div>
          <div className="sphere sphere-inner"></div>
          <div className="qubit-state"></div>
        </div>
      </div>
    </div>
  );
};

export default BlochSphereLoader;
