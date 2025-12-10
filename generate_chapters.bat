@echo off
REM --------------------------------------------
REM Generate all chapters using Claude CLI (space-friendly filenames)
REM --------------------------------------------

REM ------------------------
REM Module 1: ROS 2 Fundamentals
REM ------------------------
claude code write "docs\module_1\module 1 1.md" --print < "prompts\module 1 1.txt"
claude code write "docs\module_1\module 1 2.md" --print < "prompts\module 1 2.txt"
claude code write "docs\module_1\module 1 3.md" --print < "prompts\module 1 3.txt"
claude code write "docs\module_1\module 1 4.md" --print < "prompts\module 1 4.txt"
claude code write "docs\module_1\module 1 5.md" --print < "prompts\module 1 5.txt"
claude code write "docs\module_1\module 1 6.md" --print < "prompts\module 1 6.txt"

REM ------------------------
REM Module 2: Digital Twin (Gazebo & Unity)
REM ------------------------
claude code write "docs\module_2\module 2 1.md" --print < "prompts\module 2 1.txt"
claude code write "docs\module_2\module 2 2.md" --print < "prompts\module 2 2.txt"

REM ------------------------
REM Module 3: AI-Robot Brain (NVIDIA Isaac)
REM ------------------------
claude code write "docs\module_3\module 3 1.md" --print < "prompts\module 3 1.txt"
claude code write "docs\module_3\module 3 2.md" --print < "prompts\module 3 2.txt"

REM ------------------------
REM Module 4: Vision-Language-Action (VLA)
REM ------------------------
claude code write "docs\module_4\module 4 1.md" --print < "prompts\module 4 1.txt"
claude code write "docs\module_4\module 4 2.md" --print < "prompts\module 4 2.txt"

echo All chapters prompts sent to Claude CLI.
pause

