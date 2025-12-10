<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0 (added mobile responsiveness, coding standards, and implementation details)
- Modified principles: I, II, V, VI (updated to include mobile, coding standards, accessibility)
- Added sections: Technology Stack Requirements (expanded), Development Workflow (coding standards section)
- Templates requiring updates: ✅ All templates updated
- Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Educational Excellence and Mobile Responsiveness
Every feature and component must prioritize educational value and learning outcomes; Content must be accurate, well-structured, and accessible to students of varying backgrounds on all devices (desktop, tablet, mobile); Clear pedagogical purpose required for all additions - no features without educational justification; All UI components must be mobile-responsive and WCAG 2.1 compliant.

### II. Interactive Learning Experience
The textbook must provide interactive elements including RAG chatbot, personalization, and optional Urdu translation; All interactive components must be seamlessly integrated into the Docusaurus framework; User engagement metrics must be trackable and improvable; All interactive features must work across all device types and screen sizes.

### III. Test-First (NON-NEGOTIABLE)
All functionality must be thoroughly tested before implementation; Unit tests for all code components, integration tests for feature interactions, and end-to-end tests for user workflows; Red-Green-Refactor cycle strictly enforced for all development; Automated tests must pass before any code is merged.

### IV. Modular Architecture
Content modules must be independently developed and testable; Each module (ROS 2, Gazebo, NVIDIA Isaac, VLA) should be self-contained with clear interfaces; Clear separation between textbook content, interactive features, and deployment infrastructure; Modules must be designed for independent deployment and scaling.

### V. Accessibility, Internationalization, and Coding Standards
The textbook must support multiple languages with Urdu translation as a primary requirement; All UI components must be accessible (WCAG 2.1), mobile-responsive, and internationalization-ready; Content personalization based on user background must be configurable and user-controlled; All code (JS/TS, Python, YAML) must adhere to established coding standards (ESLint, Prettier, PEP8).

### VI. Open Source, Reproducible, and Secure
All code, content, and deployment configurations must be open source and reproducible; Deployment to GitHub Pages must be automated via CI/CD pipeline and documented; All dependencies and setup procedures must be clearly specified for community contribution; User data must be protected with secure authentication and privacy compliance.

## Additional Constraints

### Technology Stack Requirements
- Docusaurus for documentation framework and mobile-responsive deployment
- Better-Auth for user authentication and personalization
- OpenAI Agents/ChatKit SDK for RAG chatbot functionality
- FastAPI backend (Python) with Neon serverless Postgres for content indexing
- Qdrant Cloud Free Tier for vector search capabilities
- ROS 2 Humble/Iron, Gazebo, NVIDIA Isaac Sim for robotics content
- ESLint, Prettier for JS/TS code formatting and linting
- Python PEP8 conventions for Python code
- YAML linting for configuration files

### Performance Standards
- Page load times under 3 seconds for optimal user experience across all devices
- Chatbot response times under 5 seconds for interactive engagement
- Content indexing and search functionality must handle full textbook efficiently
- Mobile responsiveness tested on common screen sizes (320px, 768px, 1024px)

### Security Requirements
- User data protection and privacy compliance (GDPR, etc.)
- Secure authentication and session management
- Content integrity verification for educational materials
- API key security and environment variable management
- CI/CD pipeline security and branch protection

## Development Workflow

### Content Creation Process
- Chapter outlines must be written before detailed content
- Each module must have clear learning objectives and exercises
- Content must be reviewed by domain experts before publication
- All code examples must be tested and verified in relevant environments
- Mobile-responsive design must be validated during creation

### Quality Gates
- All content must pass technical accuracy review
- Interactive features must pass user experience testing
- Mobile responsiveness must be validated across devices
- Accessibility (WCAG 2.1) compliance must be verified
- Deployment must be verified on staging environment before production
- Code must pass linting and automated tests
- Demo video must showcase all key features effectively

### Coding Standards Enforcement
- All JavaScript/TypeScript code must pass ESLint validation
- All code must adhere to Prettier formatting standards
- Python code must follow PEP8 conventions
- YAML files must pass linting validation
- All code must include appropriate unit and integration tests

### Review Process
- Peer review required for all content additions
- Technical review for all code and integration features
- Educational review for pedagogical effectiveness
- Accessibility review for inclusive design compliance
- Mobile responsiveness review for cross-device compatibility

## Governance

This constitution supersedes all other development practices for the Physical AI & Humanoid Robotics Textbook project; All amendments to this constitution require explicit documentation, team approval, and migration plan for existing work; All pull requests and code reviews must verify compliance with these principles; Complexity must be justified by clear educational or technical benefits; Use this constitution for all development guidance and decision-making; All code must adhere to established coding standards and pass automated checks.

**Version**: 1.1.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07