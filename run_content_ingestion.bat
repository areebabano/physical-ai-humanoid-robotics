@echo off
setlocal

echo Starting content ingestion pipeline for Physical AI Humanoid Robotics book...

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run the content ingestion script
python backend\content_ingestion.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Content ingestion completed successfully!
) else (
    echo.
    echo Content ingestion failed with error level %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

pause