import React from 'react';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { Box, Typography, Paper } from '@mui/material';
import { useAuth } from '../hooks/useAuth';
import { toast } from 'react-toastify';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSuccess = async (credentialResponse) => {
    try {
      console.log('Google OAuth response:', credentialResponse);
      const response = await fetch('http://localhost:8000/auth/google', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          credential: credentialResponse.credential,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Login error:', errorData);
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      console.log('Login success:', data);
      login(data.token, data.user);
      toast.success('Successfully logged in!');
      navigate('/profile');
    } catch (error) {
      console.error('Login error:', error);
      toast.error(error.message || 'Login failed. Please try again.');
    }
  };

  const handleError = () => {
    console.error('Google OAuth error');
    toast.error('Login failed. Please try again.');
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '80vh',
      }}
    >
      <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h5" component="h1" gutterBottom>
          Welcome to User Management
        </Typography>
        <Typography variant="body1" gutterBottom sx={{ mb: 3 }}>
          Please sign in with your Google account
        </Typography>
        <GoogleLogin
          onSuccess={handleSuccess}
          onError={handleError}
          useOneTap
          flow="implicit"
          auto_select={false}
        />
      </Paper>
    </Box>
  );
};

export default Login; 