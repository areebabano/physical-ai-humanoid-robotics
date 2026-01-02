---
id: 2
title: Update Constitution with Mobile and Coding Standards
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: claude
command: /sp.constitution
labels: ["constitution", "mobile", "coding-standards", "accessibility"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
# Physical AI & Humanoid Robotics Textbook Project Constitution
project:
  name: "Physical AI & Humanoid Robotics Textbook"
  description: |
    Create a fully AI-native, coding-compliant textbook to teach Physical AI and Humanoid Robotics.
    Includes ROS 2, Gazebo, NVIDIA Isaac, VLA integration, simulated humanoid robotics,
    RAG chatbot, personalization, Urdu translation, mobile responsiveness, and accessibility.

# Phase 1: Specify
specify:
  goals:
    - Unified textbook with modular chapters (Modules 1-4 + Capstone)
    - RAG chatbot integration
    - User signup/signin with Better-Auth + personalization
    - Urdu translation at chapter start
    - Fully mobile-responsive web deployment
    - Coding standards enforced for all files (JS/TS, Python, YAML)
    - Deploy to GitHub Pages or Vercel
  success_criteria:
    - Book accessible on desktop, tablet, and mobile
    - Chatbot correctly answers content-based questions
    - User personalization and Urdu translation functional
    - Code passes linting and tests
    - CI/CD deployment successful
    - Demo video < 90 seconds

# Phase 2: Clarify
clarify:
  audience:
    - Students learning Physical AI & Humanoid Robotics
    - Researchers and hobbyists interested in embodied AI
  core_content_modules:
    - name: "Module 1: Robotic Nervous System (ROS 2)"
      topics:
        - ROS 2 Nodes, Topics, Services
        - URDF (Unified Robot Description Format)
        - Python integration using rclpy
        - ROS 2 package development
    - name: "Module 2: Digital Twin (Gazebo & Unity)"
      topics:
        - Physics simulation, gravity, collisions
        - Gazebo environment setup & sensors simulation
        - Unity visualization, high-fidelity rendering
        - LiDAR, Depth Cameras, IMU integration
    - name: "Module 3: AI-Robot Brain (NVIDIA Isaac)"
      topics:
        - Isaac Sim & Isaac ROS
        - AI perception pipelines and VSLAM
        - Nav2 path planning for bipedal movement
        - Reinforcement learning & sim-to-real transfer
    - name: "Module 4: Vision-Language-Action (VLA)"
      topics:
        - Voice-to-Action using OpenAI Whisper
        - Cognitive Planning via GPT models
        - Capstone: Autonomous humanoid simulation
  hardware_requirements:
    - RTX GPU workstation (64GB RAM)
    - Jetson Orin Nano/NX edge AI
    - Intel RealSense Camera D435i/D455
    - Unitree Go2 or proxy robot
  software_requirements:
    - ROS 2 Humble/Iron
    - Gazebo Simulator
    - Unity for visualization
    - NVIDIA Isaac Sim & Isaac ROS
    - OpenAI Whisper, GPT models integration
  optional_features:
    - Better-Auth signup/signin
    - User personalization
    - Urdu translation
    - User profile fields:
        - Name
        - Email
        - Software background
        - Hardware background
        - Preferred language (English/Urdu)

# Phase 3: Plan
plan:
  steps:
    - Setup Docusaurus project with mobile-responsive theme
    - Integrate Claude Code for automated chapter content generation
    - Ensure code adheres to:
        - ESLint for JS/TS
        - Prettier formatting
        - Python PEP8 conventions
        - YAML linting
    - Write chapters for each module + capstone
    - Integrate RAG chatbot (secure, CI/CD ready)
    - Implement personalization & Urdu translation
    - Deploy with responsive design testing (mobile, tablet, desktop)
    - Test accessibility (WCAG 2.1)
    - Record demo video <90 seconds
    - Submit GitHub repo + published book link

# Phase 4: Tasks
tasks:
  - task: "Initialize Docusaurus Project"
    priority: 1
    details:
      - npx create-docusaurus@latest physical-ai-book classic
      - Setup GitHub repository with branch protection
      - Configure deployment to GitHub Pages
      - Apply responsive theme & accessibility defaults
      - Setup ESLint, Prettier, and CI/CD pipeline
  - task: "Chapter Writing"
    priority: 2
    dependencies: ["Initialize Docusaurus Project"]
    details:
      - Generate module content via Claude Code
      - Include code snippets, diagrams, and exercises
      - Ensure mobile-friendly markdown formatting
      - Adhere to coding standards
  - task: "RAG Chatbot Integration"
    priority: 3
    dependencies: ["Chapter Writing"]
    details:
      - OpenAI Agents/ChatKit SDK
      - FastAPI backend (Python)
      - Neon serverless Postgres DB for content indexing
      - Qdrant Cloud Free Tier vector search
      - Embed chatbot in responsive book pages
      - Secure user data and API keys
      - Write automated tests for chatbot responses
  - task: "Optional Features"
    priority: 4
    dependencies: ["Chapter Writing"]
    details:
      - Better-Auth signup/signin
      - Ask user software/hardware background at signup
      - Personalization button at chapter start
      - Urdu translation button at chapter start
      - Ensure mobile-friendly UI
  - task: "Deployment"
    priority: 5
    dependencies: ["RAG Chatbot Integration", "Optional Features"]
    details:
      - Deploy to GitHub Pages or Vercel
      - Test mobile responsiveness
      - Test accessibility (WCAG)
      - Run linting and automated tests
  - task: "Demo Video"
    priority: 6
    dependencies: ["Deployment"]
    details:
      - Record <90 second demo
      - Show RAG chatbot, personalization, Urdu translation
      - Highlight mobile responsiveness

# Phase 5: Implement
implement:
  execute_order:
    - "Initialize Docusaurus Project"
    - "Chapter Writing (Modules 1-4 + Capstone)"
    - "RAG Chatbot Integration"
    - "Optional Features (Better-Auth, Personalization, Urdu Translation)"
    - "Deployment to GitHub Pages/Vercel"
    - "Testing: Mobile + Accessibility + Linting + CI/CD"
    - "Demo Video Recording"
    - "Submission of GitHub repo and Book link"
  description: |
    Execute all tasks step by step using Claude Code + Spec-Kit Plus.
    Ensure chapters are coding-compliant, mobile responsive, accessible, and tested.
    Chatbot, personalization, and Urdu translation must work across devices.
```

## Response snapshot

Updated the project constitution to version 1.1.0, incorporating new requirements for mobile responsiveness, coding standards, and enhanced implementation details. Key changes include:

1. Updated Core Principles:
   - I. Educational Excellence renamed to "Educational Excellence and Mobile Responsiveness" - added mobile and accessibility requirements
   - II. Interactive Learning Experience - added cross-device functionality
   - V. Accessibility and Internationalization renamed to "Accessibility, Internationalization, and Coding Standards" - added coding standards
   - VI. Open Source and Reproducible renamed to "Open Source, Reproducible, and Secure" - added security requirements

2. Expanded Technology Stack Requirements to include ESLint, Prettier, PEP8, and YAML linting

3. Added Performance Standards for mobile responsiveness testing

4. Enhanced Security Requirements to include API key security and CI/CD pipeline security

5. Added new "Coding Standards Enforcement" section to Development Workflow

6. Updated Quality Gates to include code linting and mobile responsiveness validation

7. Updated Review Process to include mobile responsiveness review

The constitution now fully reflects the project's requirements for mobile responsiveness, coding standards compliance, and comprehensive implementation approach.

## Outcome

- ✅ Impact: Updated constitution to include mobile responsiveness, coding standards, and security requirements
- 🧪 Tests: No tests required for constitution update
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Continue with project implementation following updated constitution
- 🧠 Reflection: The updated constitution now comprehensively covers all project requirements including mobile, coding standards, and accessibility

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Docusaurus project initialization with mobile-responsive theme