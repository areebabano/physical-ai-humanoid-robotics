import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './index.module.css';
import { RiRobot2Line } from 'react-icons/ri';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className={styles.heroContainer}>
        <div className={styles.heroLeft}>
          <div className={styles.badge}>
            <span className={styles.badgeIcon}><RiRobot2Line /></span>
            <span className={styles.badgeText}>AI-Powered Learning</span>
          </div>
          <h1 className={styles.heroTitle}>
            <span className={styles.titleLine1}>Build The Future</span>
            <span className={styles.titleLine2}>With Humanoid Robots</span>
          </h1>
          <p className={styles.heroDescription}>
            Master cutting-edge robotics with hands-on training in ROS 2, Gazebo,
            Isaac Sim, and AI integration. Transform from beginner to expert in
            autonomous humanoid robotics.
          </p>
          <div className={styles.heroButtons}>
            <Link
              className={styles.primaryButton}
              to="module_0/module_0_overview"
              aria-label="Get started with the course">
              <span>Start Learning</span>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </Link>
            <Link
              className={styles.secondaryButton}
              to="module_1/module_1_0"
              aria-label="Explore the curriculum">
              <span>View Curriculum</span>
            </Link>
          </div>
          <div className={styles.statsBar}>
            <div className={styles.statItem}>
              <div className={styles.statNumber}>5+</div>
              <div className={styles.statLabel}>Modules</div>
            </div>
            <div className={styles.statDivider}></div>
            <div className={styles.statItem}>
              <div className={styles.statNumber}>100%</div>
              <div className={styles.statLabel}>Hands-On</div>
            </div>
            <div className={styles.statDivider}></div>
            <div className={styles.statItem}>
              <div className={styles.statNumber}>AI</div>
              <div className={styles.statLabel}>Powered</div>
            </div>
          </div>
        </div>
        <div className={styles.heroRight}>
          <div className={styles.imageWrapper}>
            <div className={styles.floatingCard1}></div>
            <div className={styles.floatingCard2}></div>
            <img
              src="/img/hero1.jpg"
              alt="Humanoid Robot"
              className={styles.heroImage}
              onError={(e) => {
                e.currentTarget.src = 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=800&fit=crop';
              }}
            />
            <div className={styles.imageGlow}></div>
          </div>
        </div>
      </div>
      <div className={styles.scrollIndicator}>
        <div className={styles.scrollMouse}></div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A Hands-On Guide to Humanoid Robotics, ROS 2, Simulation, and AI Integration">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}