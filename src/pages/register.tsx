import React, { useState } from 'react';
import { useRegister } from '../hooks/useAuth';
import { FaEnvelope, FaLock, FaUser, FaArrowRight, FaRobot } from 'react-icons/fa';
import styles from './auth.module.css';

const RegisterPage: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const { loading, error, executeRegister } = useRegister();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }
    await executeRegister(email, password, name);
  };

  return (
    <div className={styles.authContainer}>
      {/* Left Side - Image */}
      <div className={styles.authLeft}>
        <div className={styles.authImageWrapper}>
          <div className={styles.authOverlay}>
            <div className={styles.authBrand}>
              <FaRobot className={styles.brandIcon} />
              <h2>Join Us Today</h2>
              <p>Start your journey into the future of robotics</p>
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
            <h1>Create Account</h1>
            <p>Start learning robotics today</p>
          </div>

          {error && (
            <div className={styles.errorMessage}>
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className={styles.authForm}>
            <div className={styles.formGroup}>
              <label htmlFor="name">
                <FaUser className={styles.labelIcon} />
                Full Name
              </label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                placeholder="John Doe"
                className={styles.formInput}
              />
            </div>

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

            <div className={styles.formGroup}>
              <label htmlFor="confirmPassword">
                <FaLock className={styles.labelIcon} />
                Confirm Password
              </label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                placeholder="••••••••"
                className={styles.formInput}
              />
            </div>

            <div className={styles.formOptions}>
              <label className={styles.checkboxLabel}>
                <input type="checkbox" required />
                <span>I agree to Terms & Conditions</span>
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className={styles.submitButton}
            >
              {loading ? (
                <>
                  <span className={styles.spinner}></span>
                  Creating account...
                </>
              ) : (
                <>
                  Create Account
                  <FaArrowRight className={styles.buttonIcon} />
                </>
              )}
            </button>
          </form>

          <div className={styles.authFooter}>
            <p>
              Already have an account?{' '}
              <a href="/login" className={styles.authLink}>
                Sign in here
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
