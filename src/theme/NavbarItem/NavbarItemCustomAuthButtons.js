import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import Link from '@docusaurus/Link';

const NavbarItemCustomAuthButtons = (props) => {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="navbar__auth-buttons" {...props}>
      {user ? (
        <div className="dropdown dropdown--hoverable dropdown--right">
          <span className="navbar__item navbar__link" style={{ cursor: 'pointer' }}>
            {user.name || user.email}
          </span>
          <ul className="dropdown__menu" style={{ position: 'absolute', right: 0, backgroundColor: 'white', border: '1px solid #ddd', borderRadius: '4px', listStyle: 'none', padding: 0, margin: '5px 0 0 0', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <li>
              <Link className="dropdown__link" to="/user/profile" style={{ display: 'block', padding: '8px 16px', textDecoration: 'none', color: '#222' }}>
                Profile
              </Link>
            </li>
            <li>
              <button
                className="dropdown__link dropdown__logout-btn"
                onClick={handleLogout}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  padding: '8px 16px',
                  display: 'block',
                  color: '#222',
                  fontSize: 'inherit',
                  fontFamily: 'inherit'
                }}
              >
                Logout
              </button>
            </li>
          </ul>
        </div>
      ) : (
        <div className="navbar__auth-links" style={{ display: 'flex', gap: '8px' }}>
          <Link
            className="button button--secondary button--sm"
            to="/login"
            style={{ textDecoration: 'none' }}
          >
            Log in
          </Link>
          <Link
            className="button button--primary button--sm"
            to="/register"
            style={{ textDecoration: 'none' }}
          >
            Sign up
          </Link>
        </div>
      )}
    </div>
  );
};

export default NavbarItemCustomAuthButtons;