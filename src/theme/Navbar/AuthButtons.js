import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import Link from '@docusaurus/Link';

const AuthButtons = () => {
  const { user, logout, loading } = useAuth();

  if (loading) {
    return (
      <div style={{
        color: 'var(--color-primary-300)',
        fontSize: '14px',
        padding: '8px 16px'
      }}>
        Loading...
      </div>
    );
  }

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="navbar__auth-container">
      {user ? (
        // User is authenticated - show profile dropdown
        <div className="dropdown dropdown--hoverable dropdown--right">
          <span>
            {user.name || user.email}
          </span>
          <ul className="dropdown__menu">
            <li>
              <Link className="dropdown__link" to="/user/profile">
                Profile
              </Link>
            </li>
            <li>
              <button
                className="dropdown__link dropdown__logout-btn"
                onClick={handleLogout}
              >
                Logout
              </button>
            </li>
          </ul>
        </div>
      ) : (
        // User is not authenticated - show login/register buttons
        <div className="navbar__auth-links">
          <Link className="navbar-login-btn" to="/login">
            Login
          </Link>
          <Link className="navbar-signup-btn" to="/register">
            Sign Up
          </Link>
        </div>
      )}
    </div>
  );
};

export default AuthButtons;