import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import ChatbotWidget from '../components/ChatbotWidget';

// Default theme root component with AuthProvider wrapper
const Root = ({children}) => {
  return (
    <AuthProvider>
      {children}
      <ChatbotWidget />
    </AuthProvider>
  );
};

export default Root;