import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useLogout } from '../../hooks/useAuth';

const UserProfile: React.FC = () => {
  const { user, token, updateUser } = useAuth();
  const { logout } = useLogout();
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(user?.name || '');

  const handleUpdateProfile = async () => {
    if (user && token) {
      try {
        const response = await fetch(`/api/auth/me`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name }),
        });

        if (response.ok) {
          const updatedUser = await response.json();
          updateUser({ name: updatedUser.name });
          setIsEditing(false);
        } else {
          console.error('Failed to update profile');
        }
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    }
  };

  if (!user) {
    return <div>Please log in to view your profile.</div>;
  }

  return (
    <div className="user-profile">
      <h2>User Profile</h2>
      <div className="profile-info">
        <p><strong>Name:</strong> {isEditing ? (
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        ) : (
          user.name || 'Not provided'
        )}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Member since:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
        <p><strong>Status:</strong> {user.is_active ? 'Active' : 'Inactive'}</p>
      </div>
      <div className="profile-actions">
        {isEditing ? (
          <>
            <button onClick={handleUpdateProfile}>Save</button>
            <button onClick={() => { setIsEditing(false); setName(user.name || ''); }}>Cancel</button>
          </>
        ) : (
          <button onClick={() => setIsEditing(true)}>Edit Profile</button>
        )}
        <button onClick={logout}>Logout</button>
      </div>
    </div>
  );
};

export default UserProfile;