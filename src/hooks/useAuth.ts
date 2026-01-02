import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

export const useLogin = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { login } = useAuth();

  const executeLogin = async (email: string, password: string) => {
    setLoading(true);
    setError(null);

    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return { loading, error, executeLogin };
};

export const useRegister = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { register } = useAuth();

  const executeRegister = async (email: string, password: string, name: string) => {
    setLoading(true);
    setError(null);

    try {
      await register(email, password, name);
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return { loading, error, executeRegister };
};

export const useLogout = () => {
  const { logout } = useAuth();

  return { logout };
};

// Hook to protect routes - for Docusaurus we'll use a different approach
export const useAuthStatus = () => {
  const { user, loading } = useAuth();

  return { user, loading };
};