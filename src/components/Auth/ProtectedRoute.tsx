import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  fallback = <div>Please log in to access this content.</div>
}) => {
  const { user, loading } = useAuth();

  // Show loading while checking auth status
  if (loading) {
    return <div>Loading...</div>;
  }

  // If user is not authenticated, redirect to login
  if (!user) {
    // For Docusaurus, redirect to login page
    window.location.href = '/login';
    return null;
  }

  // If user is authenticated, render the children
  return <>{children}</>;
};

export default ProtectedRoute;