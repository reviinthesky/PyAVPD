@echo off
setlocal enabledelayedexpansion

set PROJECT_DIR=%1
set PYTHON_DIR=%2
set PIP_PACKAGES=%3

echo project directory: %PROJECT_DIR%
echo python directory: %PYTHON_DIR%/python.exe
echo pip packages directory: %PIP_PACKAGES%

cd "%PROJECT_DIR%"
echo current directory %CD%
"%PYTHON_DIR%/python.exe" -m venv venv
call venv\Scripts\activate.bat
echo made a venv
if not "%PIP_PACKAGES%" == "" (
    echo requirements.txt path exists, installing packages...
    python -m pip install --upgrade pip
    python -m pip install -r "%PIP_PACKAGES%"
    echo pip installed
) else (
    echo no packages passed, skipping...
)
echo All configs files created successfully
echo Setup completed. 
timeout /t 10
start "" "%PROJECT_DIR%"
call venv\Scripts\deactivate.bat