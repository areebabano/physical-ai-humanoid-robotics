import React from 'react';
import ProtectedRoute from '../components/Auth/ProtectedRoute';
import UserProfile from '../components/Auth/UserProfile';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

const DashboardPage: React.FC = () => {
  return (
    <Layout title="Dashboard" description="Your dashboard">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <div className="dashboard-page">
              <h1>Dashboard</h1>
              <div className="dashboard-content">
                <div className="row">
                  <div className="col col--4">
                    <div className="card">
                      <div className="card__header">
                        <h3>Your Profile</h3>
                      </div>
                      <div className="card__body">
                        <UserProfile />
                      </div>
                    </div>
                  </div>
                  <div className="col col--8">
                    <div className="card">
                      <div className="card__header">
                        <h3>Welcome to Your Dashboard</h3>
                      </div>
                      <div className="card__body">
                        <p>This is your personal dashboard where you can manage your account and access personalized content.</p>
                        <ul>
                          <li>View and update your profile information</li>
                          <li>Access exclusive content</li>
                          <li>Track your learning progress</li>
                        </ul>
                        <div className="margin-top--md">
                          <Link to="/docs/module_0/module_0_overview" className="button button--primary">
                            Continue Learning
                          </Link>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default () => (
  <ProtectedRoute>
    <DashboardPage />
  </ProtectedRoute>
);