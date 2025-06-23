@echo off
cd /d "%~dp0"

REM Check for Python 3.12
python --version 2>NUL | findstr /C:"3.12" >NUL
if errorlevel 1 (
    echo Python 3.12 not found. Downloading installer...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -OutFile python-3.12.3-amd64.exe"
    echo Please install Python 3.12, then restart this script.
    start python-3.12.3-amd64.exe
    pause
    exit /b
)

if exist requirements.txt (
    echo Installing required libraries...
    pip install -r requirements.txt
)
streamlit run streamlitVersion.py
pause