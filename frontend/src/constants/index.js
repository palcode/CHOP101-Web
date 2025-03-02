export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID;

export const AUTH_TOKEN_KEY = 'token';
export const USER_DATA_KEY = 'user';

export const API_ENDPOINTS = {
  GOOGLE_AUTH: '/auth/google',
  USER_PROFILE: '/users/me',
  USER_PROFILE_UPDATE: '/users/me/profile',
};

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  PROFILE: '/profile',
}; 