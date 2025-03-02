import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { GOOGLE_CLIENT_ID, ROUTES } from './constants';
import theme from './theme';
import Layout from './components/Layout';
import Login from './pages/Login';
import Profile from './pages/Profile';
import PrivateRoute from './components/PrivateRoute';
import { AuthProvider } from './store/AuthContext';

const App = () => {
  return (
    <AuthProvider>
      <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Router>
            <Layout>
              <Routes>
                <Route path={ROUTES.LOGIN} element={<Login />} />
                <Route
                  path={ROUTES.PROFILE}
                  element={
                    <PrivateRoute>
                      <Profile />
                    </PrivateRoute>
                  }
                />
                <Route path={ROUTES.HOME} element={<Navigate to={ROUTES.PROFILE} replace />} />
              </Routes>
            </Layout>
          </Router>
          <ToastContainer 
            position="bottom-right"
            autoClose={5000}
            hideProgressBar={false}
            newestOnTop
            closeOnClick
            pauseOnFocusLoss
            draggable
            pauseOnHover
          />
        </ThemeProvider>
      </GoogleOAuthProvider>
    </AuthProvider>
  );
};

export default App; 