import { useState, useEffect } from 'react';
import './App.css';
import LoginPage from './components/LoginPage';
import Toast from './components/Toast';
import ChatDisplay from './components/ChatDisplay';
import { useAuth0 } from '@auth0/auth0-react';
import ChatInput from './components/ChatInput';
import Footer from './components/Footer';
import BlochSphereLoader from './components/BlochSphereLoader';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [toast, setToast] = useState({ show: false, message: '' });
  const [isGuestMode, setIsGuestMode] = useState(false);

  // Auth0 hooks
  const { isAuthenticated, user, isLoading: auth0Loading, getAccessTokenSilently, logout } = useAuth0();

  // Check for guest mode in localStorage on initial load
  useEffect(() => {
    const storedGuestMode = localStorage.getItem('catchatGuestMode');
    if (storedGuestMode === 'true') {
      setIsGuestMode(true);
    }
  }, []);

  // Handle guest login
  const handleGuestLogin = () => {
    setIsGuestMode(true);
    localStorage.setItem('catchatGuestMode', 'true');
  };

  // Handle exiting guest mode
  const handleGuestLogout = () => {
    setIsGuestMode(false);
    localStorage.removeItem('catchatGuestMode');
  };

  // Show toast notification
  const showToast = (message, duration = 3000) => {
    setToast({ show: true, message });
    setTimeout(() => {
      setToast({ show: false, message: '' });
    }, duration);
  };

  const sendMessage = async (message) => {
    if (isLoading) return;
    // Don't send empty messages
    if (!message.trim()) {
      showToast('Please enter a message');
      return;
    }

    try {
      setIsLoading(true);
      // Add user message to the chat
      setMessages((prev) => [
        ...prev,
        {
          type: 'user',
          content: message,
        },
      ]);

      // Get the access token if the user is authenticated and not in guest mode
      let headers = { 'Content-Type': 'application/json' };
      if (isAuthenticated && !isGuestMode) {
        try {
          const token = await getAccessTokenSilently({
            authorizationParams: {
              audience: 'https://qcatchat.com/api', // Adjust this if needed
            },
          });
          headers['Authorization'] = `Bearer ${token}`;
          console.log("Successfully obtained auth token");
        } catch (tokenError) {
          console.error('Error getting access token:', tokenError);
          // Fall back to guest mode if there's an auth error
          console.log("Continuing without auth token due to error");
        }
      }

      // Call the API with the token
      const response = await fetch('https://qcatchat.com/chat', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          message: message,
          mode: 'standard',
          quantum_computer: "simulator",
          qubits: 5
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }

      const data = await response.json();
      console.log("API response:", data);

      let botContent;
      // Make sure we're always working with a string for content
      if (typeof data.response === 'object' && data.response !== null) {
        // Convert the object to a formatted string for safe rendering
        if (data.response.summary || data.response.details) {
          botContent = '';
          if (data.response.summary) {
            botContent += `Summary: ${data.response.summary}\n\n`;
          }
          if (data.response.details) {
            // Just include the details content without the "Details:" prefix
            botContent += `${data.response.details}`;
          }
        } else {
          // If it's some other object, stringify it
          botContent = JSON.stringify(data.response);
        }
      } else {
        // If it's already a string or other primitive
        botContent = String(data.response || '');
      }

      // Add bot response to the chat with string content
      setMessages((prev) => [
        ...prev,
        {
          type: 'bot',
          content: botContent, // This is now guaranteed to be a string
          mode: 'standard',
        },
      ]);
    } catch (error) {
      console.error('Error:', error);
      showToast('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Get time of day for greeting
  const getTimeOfDay = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'morning';
    if (hour < 18) return 'afternoon';
    return 'evening';
  };

  // Show loading indicator while Auth0 is initializing (unless in guest mode)
  if (auth0Loading && !isGuestMode) {
    return <div className="loading">Loading...</div>;
  }

  // Determine if user is authorized (authenticated or guest mode)
  const isAuthorized = isAuthenticated || isGuestMode;

  // Show login page if user is not authenticated or in guest mode
  if (!isAuthorized) {
    return <LoginPage onGuestLogin={handleGuestLogin} />;
  }

  // User is authenticated or in guest mode, show the chat interface
  return (
    <div className="app-container">
      {isLoading && <BlochSphereLoader />}
      <header className="app-header">
        <div className="user-info">
          {isGuestMode ? (
            <></>
          ) : (
            user?.name && <span>Welcome, {user.name}</span>
          )}
        </div>
        {isGuestMode ? (
          <button className="logout-button" onClick={handleGuestLogout}>
            Exit Guest Mode
          </button>
        ) : (
          <button className="logout-button" onClick={() => logout({ returnTo: window.location.origin })}>
            Log Out
          </button>
        )}
      </header>
      <main className="main-content">
        <div className="content-container">
          {/* Logo */}
          <div className="logo-container">
            <div className="logo-image-wrapper">
              <img
                src="https://i.postimg.cc/tTJdgpLM/DALL-E-2025-03-02-13-50-37-A-minimalist-professional-logo-for-Cat-Chat-on-a-clean-white-backgrou.webp"
                alt="CatChat Logo"
                className="logo-image"
              />
            </div>
          </div>
          {/* Welcome Message */}
          <h2 className="greeting">
            Good {getTimeOfDay()}, {isGuestMode ? 'Guest' : (user?.name || user?.email || 'Friend')}.
          </h2>
          <p className="subgreeting">How can I help you today?</p>
          {/* Chat Display */}
          {messages.length > 0 && <ChatDisplay messages={messages} />}
          {/* Input Box */}
          <ChatInput onSubmit={sendMessage} isLoading={isLoading} />
        </div>
      </main>
      {/* Toast Notification */}
      <Toast message={toast.message} show={toast.show} />
      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;
