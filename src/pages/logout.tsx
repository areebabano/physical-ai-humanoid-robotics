import React, { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Layout from '@theme/Layout';

const LogoutPage = () => {
  const { logout } = useAuth();

  useEffect(() => {
    // Perform logout when this page loads
    logout();
  }, [logout]);

  return (
    <Layout title="Logging Out" description="Logging out from your account">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div className="auth-form">
              <h1>Logging Out</h1>
              <p>You are being logged out. Redirecting...</p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default LogoutPage;