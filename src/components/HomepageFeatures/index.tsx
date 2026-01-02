import React from 'react';
import Heading from '@theme/Heading';
import {
  FaBook,
  FaRobot,
  FaLock,
  FaFlask,
  FaCog,
  FaDesktop,
  FaEye,
  FaChartLine,
  FaGlobe
} from 'react-icons/fa';

type FeatureItem = {
  title: string;
  Icon: React.ComponentType;
  description: React.ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Comprehensive Textbook',
    Icon: FaBook,
    description: (
      <>
        A complete guide covering all aspects of physical AI and humanoid robotics.
        From fundamentals to advanced concepts, with practical examples and hands-on exercises.
      </>
    ),
  },
  {
    title: 'AI-Powered Chatbot',
    Icon: FaRobot,
    description: (
      <>
        Get instant help with our intelligent RAG-powered chatbot that understands
        the textbook content and provides contextual answers to your questions.
      </>
    ),
  },
  {
    title: 'Secure Authentication',
    Icon: FaLock,
    description: (
      <>
        Personalized learning experience with secure user accounts, progress tracking,
        and customized content recommendations based on your learning journey.
      </>
    ),
  },
  {
    title: 'Hands-On Labs',
    Icon: FaFlask,
    description: (
      <>
        Practice what you learn with interactive labs, simulation exercises,
        and real-world robotics projects using ROS 2, Gazebo, and Isaac Sim.
      </>
    ),
  },
  {
    title: 'ROS 2 Mastery',
    Icon: FaCog,
    description: (
      <>
        Master Robot Operating System 2 (ROS 2) with in-depth tutorials,
        best practices, and production-ready code examples for building robotic applications.
      </>
    ),
  },
  {
    title: 'Simulation Environments',
    Icon: FaDesktop,
    description: (
      <>
        Learn to work with industry-standard simulation tools including Gazebo Classic,
        Gazebo Fortress, and NVIDIA Isaac Sim for virtual robot development and testing.
      </>
    ),
  },
  {
    title: 'Vision-Language-Action Models',
    Icon: FaEye,
    description: (
      <>
        Explore cutting-edge VLA models that enable robots to understand visual scenes,
        process natural language commands, and execute complex manipulation tasks.
      </>
    ),
  },
  {
    title: 'Progressive Learning Path',
    Icon: FaChartLine,
    description: (
      <>
        Structured curriculum from beginner to advanced topics, with clear learning objectives,
        assessments, and capstone projects to solidify your robotics expertise.
      </>
    ),
  },
  {
    title: 'Real-World Applications',
    Icon: FaGlobe,
    description: (
      <>
        Learn by building real applications: autonomous navigation, manipulation tasks,
        human-robot interaction, and complete humanoid control systems.
      </>
    ),
  },
];

function Feature({title, Icon, description}: FeatureItem) {
  return (
    <div className="feature-card">
      <div className="feature-icon">
        <Icon />
      </div>
      <Heading as="h3" className="feature-title">
        {title}
      </Heading>
      <p className="feature-description">{description}</p>
    </div>
  );
}

export default function HomepageFeatures(): React.ReactElement {
  return (
    <section className="features-section">
      <div className="container">
        <div className="features-header">
          <h2 className="features-main-title">
            Why Choose This Course?
          </h2>
          <p className="features-subtitle">
            A comprehensive, hands-on approach to mastering physical AI and humanoid robotics
          </p>
          <div className="features-divider"></div>
        </div>
        <div className="features-grid">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
