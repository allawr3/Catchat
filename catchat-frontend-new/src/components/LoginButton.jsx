// ~/catchat-frontend-new/src/components/LoginButton.jsx
import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const LoginButton = () => {
  const { loginWithRedirect, isAuthenticated } = useAuth0();

  return (
    !isAuthenticated && (
      <button 
        onClick={() => loginWithRedirect()}
        className="login-button"
      >
        Log In
      </button>
    )
  );
};

export default LoginButton;
