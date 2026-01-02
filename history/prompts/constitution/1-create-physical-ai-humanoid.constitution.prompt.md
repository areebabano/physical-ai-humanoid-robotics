---
id: 1
title: Create Physical AI Humanoid Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: claude
command: /sp.constitution
labels: ["constitution", "project-setup", "governance"]
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
    Create a complete AI-native textbook to teach Physical AI and Humanoid Robotics,
    including ROS 2, Gazebo, NVIDIA Isaac, VLA integration, and simulated humanoid robotics.
    The textbook will include interactive RAG chatbot support, user personalization, and
    optional Urdu translation features. Deploy via Docusaurus to GitHub Pages.

# Phase 1: Specify
specify:
  goals:
    - Write a unified textbook for Physical AI & Humanoid Robotics course.
    - Integrate interactive RAG chatbot within the book.
    - Enable user signup/signin with Better-Auth and personalization of content.
    - Enable Urdu translation at chapter start.
    - Deploy to GitHub Pages or Vercel.
  success_criteria:
    - Book is fully published and accessible.
    - Chatbot answers user questions correctly from the book content.
    - Users can personalize content based on their background.
    - Users can translate chapters into Urdu on demand.
    - Demo video < 90 seconds is ready.
    - GitHub repository and published book links submitted.

# Phase 2: Clarify
clarify:
  audience:
    - Students learning Physical AI & Humanoid Robotics
    - Researchers and hobbyists interested in embodied AI
  core_content_modules:
    - name: "Module 1: Robotic Nervous System (ROS 2)"
      topics:
        - ROS 2 Nodes, Topics, and Services
        - URDF (Unified Robot Description Format)
        - Python integration using rclpy
        - ROS 2 package development
    - name: "Module 2: Digital Twin (Gazebo & Unity)"
      topics:
        - Physics simulation, gravity, collisions
        - Gazebo environment setup and sensors simulation
        - Unity visualization and high-fidelity rendering
        - LiDAR, Depth Cameras, and IMU integration
    - name: "Module 3: AI-Robot Brain (NVIDIA Isaac)"
      topics:
        - NVIDIA Isaac Sim & Isaac ROS
        - AI perception pipelines and VSLAM
        - Nav2 path planning for bipedal humanoid movement
        - Sim-to-Real transfer techniques
        - Reinforcement Learning for robot control
    - name: "Module 4: Vision-Language-Action (VLA)"
      topics:
        - Voice-to-Action using OpenAI Whisper
        - Cognitive Planning using LLMs
        - Capstone: Autonomous Humanoid Robot
  hardware_requirements:
    - High-performance workstation with RTX GPU, 64GB RAM
    - Jetson Orin Nano/NX for edge AI
    - Intel RealSense Camera D435i/D455
    - Unitree Go2 or proxy robot
  software_requirements:
    - ROS 2 Humble/Iron
    - Gazebo Simulator
    - Unity for visualization
    - NVIDIA Isaac Sim & Isaac ROS
    - OpenAI Whisper, GPT models integration
  optional_features:
    - User signup/signin with Better-Auth
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
    - Setup project folder using Docusaurus
    - Use Claude Code to generate chapter outlines, explanations, examples, and exercises
    - Write textbook chapters for each module
    - Develop RAG chatbot and integrate it in the book
    - Add optional user personalization and Urdu translation
    - Deploy the textbook to GitHub Pages or Vercel
    - Record demo video < 90 seconds
    - Submit GitHub repo and published book links

# Phase 4: Tasks
tasks:
  - task: "Initialize Docusaurus Project"
    priority: 1
    details:
      - npx create-docusaurus@latest physical-ai-book classic
      - Setup GitHub repository
      - Configure deployment to GitHub Pages
  - task: "Chapter Writing"
    priority: 2
    dependencies: ["Initialize Docusaurus Project"]
    details:
      - Module 1: ROS 2 fundamentals, URDF, Python integration
      - Module 2: Gazebo simulation, Unity visualization, sensors
      - Module 3: NVIDIA Isaac Sim, AI perception, VSLAM, Nav2
      - Module 4: VLA, voice-to-action, GPT integration
      - Capstone project: Autonomous humanoid simulation
  - task: "RAG Chatbot Integration"
    priority: 3
    dependencies: ["Chapter Writing"]
    details:
      - Use OpenAI Agents/ChatKit SDK
      - FastAPI backend
      - Neon serverless Postgres DB for content indexing
      - Qdrant Cloud Free Tier for vector search
      - Embed chatbot into Docusaurus book pages
  - task: "Optional Features"
    priority: 4
    dependencies: ["Chapter Writing"]
    details:
      - Better-Auth signup/signin
      - Ask user software/hardware background at signup
      - Personalization button at chapter start
      - Urdu translation button at chapter start
  - task: "Deployment"
    priority: 5
    dependencies: ["RAG Chatbot Integration", "Optional Features"]
    details:
      - Publish book to GitHub Pages or Vercel
      - Test chatbot and optional features
      - Verify links and UI functionality
  - task: "Demo Video"
    priority: 6
    dependencies: ["Deployment"]
    details:
      - Record <90 secon
```

## Response snapshot

Created the project constitution for the Physical AI & Humanoid Robotics Textbook with the following key elements:

1. Six core principles established:
   - Educational Excellence
   - Interactive Learning Experience
   - Test-First (NON-NEGOTIABLE)
   - Modular Architecture
   - Accessibility and Internationalization
   - Open Source and Reproducible

2. Additional constraints section covering:
   - Technology stack requirements
   - Performance standards
   - Security requirements

3. Development workflow section with:
   - Content creation process
   - Quality gates
   - Review process

4. Governance section establishing the constitution's authority

The constitution file was written to `.specify/memory/constitution.md` with version 1.0.0, ratified on 2025-12-07.

## Outcome

- ✅ Impact: Created foundational project constitution with governance structure
- 🧪 Tests: No tests required for constitution creation
- 📁 Files: Created .specify/memory/constitution.md
- 🔁 Next prompts: Continue with project setup and implementation planning
- 🧠 Reflection: The constitution effectively captures the project's educational focus and technical requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin with Docusaurus project initialization