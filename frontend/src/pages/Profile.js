import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Avatar,
  Grid,
  TextField,
  Button,
  CircularProgress,
  Divider,
} from '@mui/material';
import { useAuth } from '../hooks/useAuth';
import { updateProfile } from '../services/api';
import { toast } from 'react-toastify';

const Profile = () => {
  const { user, updateProfile: updateAuthProfile } = useAuth();
  const [loading, setLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    address: user?.profile?.address || '',
    phone: user?.profile?.phone || '',
    bio: user?.profile?.bio || '',
  });

  useEffect(() => {
    // Update form data when user profile changes
    if (user?.profile) {
      setFormData({
        address: user.profile.address || '',
        phone: user.profile.phone || '',
        bio: user.profile.bio || '',
      });
    }
  }, [user?.profile]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const updatedProfile = await updateProfile(formData);
      await updateAuthProfile(formData);
      setEditing(false);
      toast.success('Profile updated successfully');
    } catch (error) {
      console.error('Error updating profile:', error);
      toast.error('Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper sx={{ p: 4, mt: 4 }}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={4} sx={{ textAlign: 'center' }}>
          <Avatar
            src={user.picture}
            alt={user.name}
            sx={{ width: 150, height: 150, mx: 'auto', mb: 2 }}
          />
          <Typography variant="h5" gutterBottom>
            {user.name}
          </Typography>
          <Typography color="textSecondary" gutterBottom>
            {user.email}
          </Typography>
          <Divider sx={{ my: 2 }} />
          <Typography variant="body2" color="textSecondary">
            Member since: {user.profile && new Date(user.profile.created_at).toLocaleDateString()}
          </Typography>
        </Grid>
        <Grid item xs={12} md={8}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h6">Profile Information</Typography>
            <Button
              variant={editing ? "outlined" : "contained"}
              color={editing ? "error" : "primary"}
              onClick={() => setEditing(!editing)}
              disabled={loading}
            >
              {editing ? "Cancel" : "Edit Profile"}
            </Button>
          </Box>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Address"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  disabled={!editing || loading}
                  placeholder="Enter your address"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  disabled={!editing || loading}
                  placeholder="Enter your phone number"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Bio"
                  name="bio"
                  value={formData.bio}
                  onChange={handleInputChange}
                  multiline
                  rows={4}
                  disabled={!editing || loading}
                  placeholder="Tell us about yourself"
                />
              </Grid>
              {editing && (
                <Grid item xs={12}>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    fullWidth
                    disabled={loading}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Save Changes'}
                  </Button>
                </Grid>
              )}
            </Grid>
          </form>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default Profile; 