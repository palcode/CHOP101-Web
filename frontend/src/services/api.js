import axios from 'axios';
import { toast } from 'react-toastify';
import store from '../store';
import { logoutUser } from '../store/authSlice';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = store.getState().auth.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle 401 Unauthorized
      if (error.response.status === 401) {
        store.dispatch(logoutUser());
        toast.error('Session expired. Please login again.');
      }
      // Handle 403 Forbidden
      else if (error.response.status === 403) {
        toast.error('Access denied.');
      }
      // Handle 404 Not Found
      else if (error.response.status === 404) {
        toast.error('Resource not found.');
      }
      // Handle 429 Too Many Requests
      else if (error.response.status === 429) {
        toast.error('Too many requests. Please try again later.');
      }
      // Handle other errors
      else {
        toast.error(error.response.data.detail || 'An error occurred.');
      }
    } else if (error.request) {
      toast.error('Network error. Please check your connection.');
    } else {
      toast.error('An unexpected error occurred.');
    }
    return Promise.reject(error);
  }
);

export default api; 