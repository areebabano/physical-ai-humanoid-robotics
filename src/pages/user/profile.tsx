import React from 'react';
import ProtectedRoute from '../../components/Auth/ProtectedRoute';
import UserProfile from '../../components/Auth/UserProfile';
import Layout from '@theme/Layout';

const ProfilePage: React.FC = () => {
  return (
    <Layout title="User Profile" description="Your user profile">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <ProtectedRoute>
              <div className="profile-page">
                <h1>User Profile</h1>
                <UserProfile />
              </div>
            </ProtectedRoute>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ProfilePage;