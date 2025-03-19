import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import './LoginPage.css';

const LoginPage = ({ onGuestLogin }) => {
  const { loginWithRedirect } = useAuth0();
  
  // Function to handle login with specific parameters
  const handleLogin = () => {
    loginWithRedirect({
      prompt: 'login', // Skip the signup option
      screen_hint: 'login' // Hint to Auth0 that this is a login, not signup
    });
  };
  
  // Function for new users signup
  const handleSignup = () => {
    loginWithRedirect({
      screen_hint: 'signup' // Hint to Auth0 to show the signup form
    });
  };

  // Function to handle guest login
  const handleGuestLogin = () => {
    // Call the guest login function passed from the parent component
    onGuestLogin();
  };
  
  return (
    <div className="login-page">
      <div className="left-panel">
        <h1>Welcome to Catchat</h1>
        <p>Your gateway to quantum intelligence. Catchat makes accessing quantum computers as easy as chatting with AI</p>
        <div className="features">
          <div className="feature">
            <div className="feature-icon">🔒</div>
            <span>Access powerful quantum computers</span>
          </div>
          <div className="feature">
            <div className="feature-icon">🧠</div>
            <span>Run real quantum applications</span>
          </div>
          <div className="feature">
            <div className="feature-icon">⚡</div>
            <span>Lightning-fast responses</span>
          </div>
        </div>
      </div>
      <div className="right-panel">
        <div className="login-form">
          <img
            src="https://i.postimg.cc/tTJdgpLM/DALL-E-2025-03-02-13-50-37-A-minimalist-professional-logo-for-Cat-Chat-on-a-clean-white-backgrou.webp"
            alt="Catchat Logo"
            className="logo"
          />
          <h2>Sign up to Schrödinger's Chat</h2>
          <p>Catchat is your AI-powered interface for quantum computing. Connect instantly and start running real quantum applications.</p>
          <button className="login-btn signup" onClick={handleSignup}>
            Sign Up
          </button>
          <button className="login-btn login" onClick={handleLogin}>
            Log In
          </button>
          <button className="login-btn guest" onClick={handleGuestLogin}>
            Continue as Guest
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
