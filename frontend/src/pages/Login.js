import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useGoogleLogin } from '@react-oauth/google';
import { Box, Button, Container, Typography, Paper } from '@mui/material';
import { Google as GoogleIcon } from '@mui/icons-material';
import { toast } from 'react-toastify';
import { useDispatch } from 'react-redux';
import { loginUser } from '../store/authSlice';
import api from '../services/api';

const Login = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleGoogleLogin = useGoogleLogin({
    onSuccess: async (response) => {
      try {
        // Send the token to your backend
        const { data } = await api.post('/auth/google', {
          token: response.access_token,
        });

        // Store the token and user info
        dispatch(loginUser(data));
        toast.success('Successfully logged in!');
        navigate('/profile');
      } catch (error) {
        console.error('Login failed:', error);
        toast.error('Login failed. Please try again.');
      }
    },
    onError: () => {
      toast.error('Login failed. Please try again.');
    },
  });

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
          }}
        >
          <Typography component="h1" variant="h5" gutterBottom>
            Welcome to User Management
          </Typography>
          <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 3 }}>
            Please sign in with your Google account to continue
          </Typography>
          <Button
            variant="contained"
            startIcon={<GoogleIcon />}
            onClick={() => handleGoogleLogin()}
            size="large"
            sx={{ mt: 2 }}
          >
            Sign in with Google
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};

export default Login; 