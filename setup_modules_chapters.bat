@echo off
REM --------------------------------------------
REM Setup 4 Modules with Chapters for Physical AI & Humanoid Robotics
REM --------------------------------------------

REM Create main folders if not exist
if not exist docs mkdir docs
if not exist prompts mkdir prompts

REM ------------------------
REM Module 1: ROS 2 Fundamentals
REM ------------------------
set module=module_1
if not exist docs\%module% mkdir docs\%module%
REM Chapter prompts
echo "Write Module 1 Chapter 1: ROS 2 Fundamentals including overview, nodes, topics, services, URDF, Python integration, examples, exercises. Format in Docusaurus Markdown." > prompts\%module%_1.txt
echo "Write Module 1 Chapter 2: ROS 2 Packages including package creation, launch files, parameters, Python examples, best practices. Format in Docusaurus Markdown." > prompts\%module%_2.txt
echo "Write Module 1 Chapter 3: ROS 2 Action ^& Services including action servers, clients, request-response patterns. Format in Docusaurus Markdown." > prompts\%module%_3.txt
echo "Write Module 1 Chapter 4: URDF Robot Modeling including links, joints, visuals, collisions, inertial. Format in Docusaurus Markdown." > prompts\%module%_4.txt
echo "Write Module 1 Chapter 5: rclpy Advanced including timers, callbacks, parameters, error handling. Format in Docusaurus Markdown." > prompts\%module%_5.txt
echo "Write Module 1 Chapter 6: Integration ^& Applications combining nodes, topics, services, URDF, Python. Format in Docusaurus Markdown." > prompts\%module%_6.txt

for %%i in (1 2 3 4 5 6) do (
    type nul > docs\%module%\%%i.md
)

REM ------------------------
REM Module 2: Digital Twin (Gazebo & Unity)
REM ------------------------
set module=module_2
if not exist docs\%module% mkdir docs\%module%
echo "Write Module 2 Chapter 1: Gazebo Simulation including physics, gravity, collisions, LiDAR, Depth Camera, IMU. Format in Docusaurus Markdown." > prompts\%module%_1.txt
echo "Write Module 2 Chapter 2: Unity Visualization including high-fidelity rendering, human-robot interaction. Format in Docusaurus Markdown." > prompts\%module%_2.txt

for %%i in (1 2) do (
    type nul > docs\%module%\%%i.md
)

REM ------------------------
REM Module 3: AI-Robot Brain (NVIDIA Isaac)
REM ------------------------
set module=module_3
if not exist docs\%module% mkdir docs\%module%
echo "Write Module 3 Chapter 1: Isaac Sim Basics including simulation, VSLAM, Nav2. Format in Docusaurus Markdown." > prompts\%module%_1.txt
echo "Write Module 3 Chapter 2: AI Perception ^& RL including reinforcement learning, sim-to-real transfer. Format in Docusaurus Markdown." > prompts\%module%_2.txt

for %%i in (1 2) do (
    type nul > docs\%module%\%%i.md
)

REM ------------------------
REM Module 4: Vision-Language-Action (VLA)
REM ------------------------
set module=module_4
if not exist docs\%module% mkdir docs\%module%
echo "Write Module 4 Chapter 1: Voice-to-Action including natural language mapping to ROS2 actions. Format in Docusaurus Markdown." > prompts\%module%_1.txt
echo "Write Module 4 Chapter 2: Capstone Autonomous Humanoid integrating modules 1-4, GPT-driven cognitive planning, simulation exercises. Format in Docusaurus Markdown." > prompts\%module%_2.txt

for %%i in (1 2) do (
    type nul > docs\%module%\%%i.md
)

REM ------------------------
REM Create generate_chapters.bat
REM ------------------------
(
echo @echo off
echo REM --------------------------------------------
echo REM Generate all chapters using Claude CLI
echo REM --------------------------------------------
for %%M in (module_1 module_2 module_3 module_4) do (
    for /f "tokens=*" %%C in ('dir /b prompts\%%M_*.txt') do (
        echo claude code write "docs\%%M\%%~nC.md" --print ^< "prompts\%%~nxC"
    )
)
echo.
echo echo All chapters prompts sent to Claude CLI.
echo pause
) > generate_chapters.bat

echo ✅ All modules, chapter files, prompts, and generate_chapters.bat are ready!
pause
