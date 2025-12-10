"""
Utility script to initialize the database with textbook content
"""
import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.src.database import engine, async_session
from backend.src.models.textbook_module_db import TextbookModule
from backend.src.models.chapter_db import Chapter
from backend.src.models.user_db import Base
from backend.src.services.textbook_module_service import textbook_module_service
from backend.src.services.chapter_service import chapter_service


async def initialize_database_content():
    """
    Initialize the database with textbook content
    """
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

    # Add sample content
    async with async_session() as session:
        # Create textbook modules based on the content we created
        modules_data = [
            {
                "title": "Robotic Nervous System (ROS 2)",
                "description": "Learn about ROS 2, the middleware framework for robotics communication",
                "module_number": 1,
                "weeks_duration": 4,
                "programming_language": "Python"
            },
            {
                "title": "Digital Twin (Gazebo & Unity)",
                "description": "Simulation environments for robotics development and testing",
                "module_number": 2,
                "weeks_duration": 3,
                "programming_language": "Python"
            },
            {
                "title": "AI-Robot Brain (NVIDIA Isaac)",
                "description": "AI perception and control systems for robots using NVIDIA Isaac",
                "module_number": 3,
                "weeks_duration": 4,
                "programming_language": "Python"
            },
            {
                "title": "Vision-Language-Action (VLA)",
                "description": "Natural language interaction and multimodal AI for robotics",
                "module_number": 4,
                "weeks_duration": 3,
                "programming_language": "Python"
            },
            {
                "title": "Capstone: Autonomous Humanoid Robot",
                "description": "Integrate all concepts in a complete autonomous humanoid robot system",
                "module_number": 5,
                "weeks_duration": 5,
                "programming_language": "Python"
            }
        ]

        created_modules = []
        for module_data in modules_data:
            module = await textbook_module_service.create_module(
                session,
                title=module_data["title"],
                description=module_data["description"],
                module_number=module_data["module_number"],
                weeks_duration=module_data["weeks_duration"],
                programming_language=module_data["programming_language"]
            )
            created_modules.append(module)
            print(f"Created module: {module.title}")

        # Create chapters for each module
        # Module 1 chapters
        module1_chapters = [
            {"title": "Introduction to ROS 2", "chapter_number": 1, "slug": "introduction-to-ros2"},
            {"title": "ROS 2 Architecture", "chapter_number": 2, "slug": "ros2-architecture"},
            {"title": "Nodes, Topics, and Services", "chapter_number": 3, "slug": "nodes-topics-services"},
            {"title": "ROS 2 Tools", "chapter_number": 4, "slug": "ros2-tools"},
        ]

        for i, chapter_data in enumerate(module1_chapters, 1):
            chapter = await chapter_service.create_chapter(
                session,
                title=chapter_data["title"],
                content=f"Content for {chapter_data['title']} - This chapter covers the fundamentals of ROS 2 including installation, basic concepts, and practical examples.",
                module_id=created_modules[0].id,
                chapter_number=chapter_data["chapter_number"],
                slug=chapter_data["slug"],
                learning_objectives=f"Understand the basics of {chapter_data['title']}"
            )
            print(f"  Created chapter: {chapter.title}")

        # Module 2 chapters
        module2_chapters = [
            {"title": "Introduction to Digital Twins", "chapter_number": 1, "slug": "introduction-to-digital-twins"},
            {"title": "Gazebo Simulation Environment", "chapter_number": 2, "slug": "gazebo-simulation"},
            {"title": "Unity Integration", "chapter_number": 3, "slug": "unity-integration"},
            {"title": "Robot Modeling", "chapter_number": 4, "slug": "robot-modeling"},
        ]

        for i, chapter_data in enumerate(module2_chapters, 1):
            chapter = await chapter_service.create_chapter(
                session,
                title=chapter_data["title"],
                content=f"Content for {chapter_data['title']} - This chapter covers digital twin concepts, Gazebo simulation, and Unity integration for robotics.",
                module_id=created_modules[1].id,
                chapter_number=chapter_data["chapter_number"],
                slug=chapter_data["slug"],
                learning_objectives=f"Understand the concepts of {chapter_data['title']}"
            )
            print(f"  Created chapter: {chapter.title}")

        # Module 3 chapters
        module3_chapters = [
            {"title": "Introduction to NVIDIA Isaac", "chapter_number": 1, "slug": "introduction-to-nvidia-isaac"},
            {"title": "Isaac Sim Setup", "chapter_number": 2, "slug": "isaac-sim-setup"},
            {"title": "AI Perception Systems", "chapter_number": 3, "slug": "ai-perception-systems"},
            {"title": "SLAM and Navigation", "chapter_number": 4, "slug": "slam-navigation"},
        ]

        for i, chapter_data in enumerate(module3_chapters, 1):
            chapter = await chapter_service.create_chapter(
                session,
                title=chapter_data["title"],
                content=f"Content for {chapter_data['title']} - This chapter covers NVIDIA Isaac platform, AI perception, and navigation systems.",
                module_id=created_modules[2].id,
                chapter_number=chapter_data["chapter_number"],
                slug=chapter_data["slug"],
                learning_objectives=f"Understand the concepts of {chapter_data['title']}"
            )
            print(f"  Created chapter: {chapter.title}")

        # Module 4 chapters
        module4_chapters = [
            {"title": "Introduction to VLA Models", "chapter_number": 1, "slug": "introduction-to-vla-models"},
            {"title": "Architecture of VLA Systems", "chapter_number": 2, "slug": "vla-architecture"},
            {"title": "GPT Integration for Robot Control", "chapter_number": 3, "slug": "gpt-integration"},
            {"title": "Voice Command Processing", "chapter_number": 4, "slug": "voice-command-processing"},
        ]

        for i, chapter_data in enumerate(module4_chapters, 1):
            chapter = await chapter_service.create_chapter(
                session,
                title=chapter_data["title"],
                content=f"Content for {chapter_data['title']} - This chapter covers Vision-Language-Action models and their integration with robotics.",
                module_id=created_modules[3].id,
                chapter_number=chapter_data["chapter_number"],
                slug=chapter_data["slug"],
                learning_objectives=f"Understand the concepts of {chapter_data['title']}"
            )
            print(f"  Created chapter: {chapter.title}")

        # Module 5 chapters
        module5_chapters = [
            {"title": "Project Overview", "chapter_number": 1, "slug": "capstone-project-overview"},
            {"title": "System Architecture", "chapter_number": 2, "slug": "system-architecture"},
            {"title": "Integration Challenges", "chapter_number": 3, "slug": "integration-challenges"},
            {"title": "Testing and Validation", "chapter_number": 4, "slug": "testing-validation"},
        ]

        for i, chapter_data in enumerate(module5_chapters, 1):
            chapter = await chapter_service.create_chapter(
                session,
                title=chapter_data["title"],
                content=f"Content for {chapter_data['title']} - This chapter covers the capstone project integrating all concepts learned.",
                module_id=created_modules[4].id,
                chapter_number=chapter_data["chapter_number"],
                slug=chapter_data["slug"],
                learning_objectives=f"Understand the concepts of {chapter_data['title']}"
            )
            print(f"  Created chapter: {chapter.title}")

        await session.commit()
        print("Database initialized with textbook content successfully!")


if __name__ == "__main__":
    asyncio.run(initialize_database_content())