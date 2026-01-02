import React from 'react';
import { FaGithub, FaTwitter, FaLinkedin, FaYoutube, FaDiscord, FaEnvelope } from 'react-icons/fa';
import styles from './styles.module.css';

export default function Footer(): JSX.Element {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerContainer}>
        {/* Top Section */}
        <div className={styles.footerTop}>
          <div className={styles.footerBrand}>
            <h3 className={styles.brandTitle}>PHYSICAL AI & ROBOTICS</h3>
            <p className={styles.brandDescription}>
              Master the future of robotics with hands-on training in ROS 2,
              Gazebo, Isaac Sim, and cutting-edge AI integration.
            </p>
          </div>

          <div className={styles.footerLinks}>
            <div className={styles.linkColumn}>
              <h4 className={styles.linkTitle}>Quick Links</h4>
              <ul className={styles.linkList}>
                <li><a href="/module_0/module_0_overview">Get Started</a></li>
                <li><a href="/docs/module_1/module_1_0">Modules</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/contact">Contact</a></li>
              </ul>
            </div>

            <div className={styles.linkColumn}>
              <h4 className={styles.linkTitle}>Resources</h4>
              <ul className={styles.linkList}>
                <li><a href="/documentation">Documentation</a></li>
                <li><a href="/tutorials">Tutorials</a></li>
                <li><a href="/community">Community</a></li>
                <li><a href="/faq">FAQ</a></li>
              </ul>
            </div>

            <div className={styles.linkColumn}>
              <h4 className={styles.linkTitle}>Connect</h4>
              <div className={styles.socialIcons}>
                <a href="https://github.com" target="_blank" rel="noopener noreferrer" className={styles.socialIcon}>
                  <FaGithub />
                </a>
                <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className={styles.socialIcon}>
                  <FaTwitter />
                </a>
                <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className={styles.socialIcon}>
                  <FaLinkedin />
                </a>
                <a href="https://youtube.com" target="_blank" rel="noopener noreferrer" className={styles.socialIcon}>
                  <FaYoutube />
                </a>
                <a href="https://discord.com" target="_blank" rel="noopener noreferrer" className={styles.socialIcon}>
                  <FaDiscord />
                </a>
                <a href="mailto:contact@example.com" className={styles.socialIcon}>
                  <FaEnvelope />
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className={styles.divider}></div>

        {/* Bottom Section */}
        <div className={styles.footerBottom}>
          <p className={styles.copyright}>
            © {new Date().getFullYear()} Physical AI & Humanoid Robotics. All rights reserved.
          </p>
          <div className={styles.bottomLinks}>
            <a href="/privacy">Privacy Policy</a>
            <span className={styles.separator}>•</span>
            <a href="/terms">Terms of Service</a>
            <span className={styles.separator}>•</span>
            <a href="/cookies">Cookie Policy</a>
          </div>
        </div>
      </div>

      {/* Animated Background */}
      <div className={styles.footerBackground}></div>
    </footer>
  );
}
