@echo off
REM Activate virtual environment
call .\.venv\Scripts\activate.bat

REM Run the main script
python main.py

REM Deactivate virtual environment
deactivate
pause
