import React, { createContext, useState, useEffect } from 'react';
import { AUTH_TOKEN_KEY, USER_DATA_KEY } from '../constants';
import { getCurrentUser } from '../services/api';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem(AUTH_TOKEN_KEY));
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem(USER_DATA_KEY);
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      if (token) {
        try {
          const userData = await getCurrentUser();
          updateUserData(userData);
        } catch (error) {
          console.error('Failed to fetch user data:', error);
          // If we can't fetch user data, token might be invalid
          localStorage.removeItem(AUTH_TOKEN_KEY);
          localStorage.removeItem(USER_DATA_KEY);
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, [token]);

  const updateUserData = (userData) => {
    if (userData) {
      localStorage.setItem(USER_DATA_KEY, JSON.stringify(userData));
      setUser(userData);
    }
  };

  const value = {
    token,
    user,
    setToken,
    setUser: updateUserData,
    loading,
  };

  if (loading) {
    return null; // or a loading spinner component
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 