import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { FaUser, FaEnvelope, FaCalendar, FaSignOutAlt, FaEdit, FaBook, FaTrophy } from 'react-icons/fa';
import styles from './auth.module.css';

const ProfilePage: React.FC = () => {
  const { user, loading, logout } = useAuth();

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.spinner}></div>
        <p>Loading profile...</p>
      </div>
    );
  }

  if (!user) {
    window.location.href = '/login';
    return null;
  }

  return (
    <div className={styles.profileContainer}>
      <div className={styles.profileWrapper}>
        {/* Profile Header */}
        <div className={styles.profileHeader}>
          <div className={styles.profileAvatar}>
            <FaUser />
          </div>
          <div className={styles.profileInfo}>
            <h1>{user.name || 'Student'}</h1>
            <p className={styles.profileEmail}>
              <FaEnvelope className={styles.inlineIcon} />
              {user.email}
            </p>
            <p className={styles.profileDate}>
              <FaCalendar className={styles.inlineIcon} />
              Member since {new Date().getFullYear()}
            </p>
          </div>
          <button onClick={logout} className={styles.logoutButton}>
            <FaSignOutAlt />
            <span>Logout</span>
          </button>
        </div>

        {/* Profile Content */}
        <div className={styles.profileContent}>
          {/* Stats Cards */}
          <div className={styles.statsGrid}>
            <div className={styles.statCard}>
              <div className={styles.statIcon}>
                <FaBook />
              </div>
              <div className={styles.statInfo}>
                <h3>5</h3>
                <p>Modules Completed</p>
              </div>
            </div>

            <div className={styles.statCard}>
              <div className={styles.statIcon}>
                <FaTrophy />
              </div>
              <div className={styles.statInfo}>
                <h3>12</h3>
                <p>Achievements</p>
              </div>
            </div>

            <div className={styles.statCard}>
              <div className={styles.statIcon}>
                <FaUser />
              </div>
              <div className={styles.statInfo}>
                <h3>85%</h3>
                <p>Progress</p>
              </div>
            </div>
          </div>

          {/* Account Information */}
          <div className={styles.profileSection}>
            <div className={styles.sectionHeader}>
              <h2>Account Information</h2>
              <button className={styles.editButton}>
                <FaEdit />
                <span>Edit Profile</span>
              </button>
            </div>

            <div className={styles.infoGrid}>
              <div className={styles.infoItem}>
                <label>Full Name</label>
                <p>{user.name || 'Not provided'}</p>
              </div>

              <div className={styles.infoItem}>
                <label>Email Address</label>
                <p>{user.email}</p>
              </div>

              <div className={styles.infoItem}>
                <label>Account Type</label>
                <p>Student</p>
              </div>

              <div className={styles.infoItem}>
                <label>Status</label>
                <p className={styles.statusActive}>Active</p>
              </div>
            </div>
          </div>

          {/* Learning Progress */}
          <div className={styles.profileSection}>
            <h2>Learning Progress</h2>
            <div className={styles.progressList}>
              <div className={styles.progressItem}>
                <div className={styles.progressInfo}>
                  <span className={styles.progressTitle}>ROS 2 Fundamentals</span>
                  <span className={styles.progressPercent}>100%</span>
                </div>
                <div className={styles.progressBar}>
                  <div className={styles.progressFill} style={{ width: '100%' }}></div>
                </div>
              </div>

              <div className={styles.progressItem}>
                <div className={styles.progressInfo}>
                  <span className={styles.progressTitle}>Gazebo Simulation</span>
                  <span className={styles.progressPercent}>75%</span>
                </div>
                <div className={styles.progressBar}>
                  <div className={styles.progressFill} style={{ width: '75%' }}></div>
                </div>
              </div>

              <div className={styles.progressItem}>
                <div className={styles.progressInfo}>
                  <span className={styles.progressTitle}>Isaac Sim Basics</span>
                  <span className={styles.progressPercent}>50%</span>
                </div>
                <div className={styles.progressBar}>
                  <div className={styles.progressFill} style={{ width: '50%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
