import { useContext } from 'react';
import { AuthContext } from '../store/AuthContext';
import { AUTH_TOKEN_KEY, USER_DATA_KEY } from '../constants';
import { getCurrentUser } from '../services/api';

export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  const { token, user, setToken, setUser, loading } = context;

  const login = (newToken, userData) => {
    localStorage.setItem(AUTH_TOKEN_KEY, newToken);
    localStorage.setItem(USER_DATA_KEY, JSON.stringify(userData));
    setToken(newToken);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(USER_DATA_KEY);
    setToken(null);
    setUser(null);
  };

  const updateProfile = async (profileData) => {
    if (user) {
      const updatedUser = {
        ...user,
        profile: {
          ...user.profile,
          ...profileData
        }
      };
      setUser(updatedUser);
      
      // Refresh user data from server to ensure we have the latest
      try {
        const freshUserData = await getCurrentUser();
        setUser(freshUserData);
      } catch (error) {
        console.error('Failed to refresh user data:', error);
      }
    }
  };

  const refreshUserData = async () => {
    try {
      const userData = await getCurrentUser();
      setUser(userData);
      return userData;
    } catch (error) {
      console.error('Failed to refresh user data:', error);
      return null;
    }
  };

  return {
    isAuthenticated: !!token,
    token,
    user,
    login,
    logout,
    updateProfile,
    refreshUserData,
    loading,
  };
}; 