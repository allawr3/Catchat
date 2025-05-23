// ~/catchat-frontend-new/src/components/LogoutButton.jsx
import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const LogoutButton = () => {
  const { logout, isAuthenticated } = useAuth0();

  return (
    isAuthenticated && (
      <button 
        onClick={() => logout({ returnTo: window.location.origin })}
        className="logout-button"
      >
        Log Out
      </button>
    )
  );
};

export default LogoutButton;
