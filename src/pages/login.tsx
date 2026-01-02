import React, { useState } from 'react';
import { useLogin } from '../hooks/useAuth';
import { FaEnvelope, FaLock, FaArrowRight, FaRobot } from 'react-icons/fa';
import styles from './auth.module.css';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { loading, error, executeLogin } = useLogin();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await executeLogin(email, password);
  };

  return (
    <div className={styles.authContainer}>
      {/* Left Side - Image */}
      <div className={styles.authLeft}>
        <div className={styles.authImageWrapper}>
          <div className={styles.authOverlay}>
            <div className={styles.authBrand}>
              <FaRobot className={styles.brandIcon} />
              <h2>Welcome Back</h2>
              <p>Continue your journey in Physical AI & Robotics</p>
            </div>
          </div>
          <img
            src="/img/hero1.jpg"
            alt="Physical AI"
            className={styles.authImage}
          />
        </div>
      </div>

      {/* Right Side - Form */}
      <div className={styles.authRight}>
        <div className={styles.authFormContainer}>
          <div className={styles.authHeader}>
            <h1>Sign In</h1>
            <p>Access your learning dashboard</p>
          </div>

          {error && (
            <div className={styles.errorMessage}>
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className={styles.authForm}>
            <div className={styles.formGroup}>
              <label htmlFor="email">
                <FaEnvelope className={styles.labelIcon} />
                Email Address
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="your@email.com"
                className={styles.formInput}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="password">
                <FaLock className={styles.labelIcon} />
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="••••••••"
                className={styles.formInput}
              />
            </div>

            <div className={styles.formOptions}>
              <label className={styles.checkboxLabel}>
                <input type="checkbox" />
                <span>Remember me</span>
              </label>
              <a href="/forgot-password" className={styles.forgotLink}>
                Forgot password?
              </a>
            </div>

            <button
              type="submit"
              disabled={loading}
              className={styles.submitButton}
            >
              {loading ? (
                <>
                  <span className={styles.spinner}></span>
                  Signing in...
                </>
              ) : (
                <>
                  Sign In
                  <FaArrowRight className={styles.buttonIcon} />
                </>
              )}
            </button>
          </form>

          <div className={styles.authFooter}>
            <p>
              Don't have an account?{' '}
              <a href="/register" className={styles.authLink}>
                Create one now
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
