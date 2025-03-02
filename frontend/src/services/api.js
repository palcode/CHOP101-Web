import axios from 'axios';
import { toast } from 'react-toastify';
import { API_BASE_URL, API_ENDPOINTS, AUTH_TOKEN_KEY } from '../constants';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    if (error.response) {
      console.error('Response data:', error.response.data);
      switch (error.response.status) {
        case 401:
          localStorage.removeItem(AUTH_TOKEN_KEY);
          window.location.href = '/login';
          toast.error('Session expired. Please login again.');
          break;
        case 403:
          toast.error('Access denied.');
          break;
        case 404:
          toast.error('Resource not found.');
          break;
        case 429:
          toast.error('Too many requests. Please try again later.');
          break;
        default:
          toast.error(error.response.data?.detail || 'An error occurred.');
      }
    } else if (error.request) {
      console.error('Request error:', error.request);
      toast.error('Network error. Please check your connection.');
    } else {
      console.error('Error:', error.message);
      toast.error('An unexpected error occurred.');
    }
    return Promise.reject(error);
  }
);

export const googleAuth = async (credential) => {
  try {
    console.log('Sending Google auth request...');
    const response = await api.post(API_ENDPOINTS.GOOGLE_AUTH, { credential });
    console.log('Google auth response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Google auth error:', error);
    throw error;
  }
};

export const getCurrentUser = async () => {
  try {
    console.log('Fetching current user data...');
    const response = await api.get(API_ENDPOINTS.USER_PROFILE);
    console.log('Current user data:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching user data:', error);
    throw error;
  }
};

export const updateProfile = async (profileData) => {
  try {
    console.log('Updating profile with data:', profileData);
    const response = await api.put(API_ENDPOINTS.USER_PROFILE_UPDATE, profileData);
    console.log('Profile update response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error updating profile:', error);
    throw error;
  }
};

export const getUserProfile = async () => {
  try {
    console.log('Fetching user profile...');
    const response = await api.get(API_ENDPOINTS.USER_PROFILE);
    console.log('User profile data:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

export default api; 