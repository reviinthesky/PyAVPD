@echo off

set PROJECT_DIR=%1
set PYTHON_DIR=%2
set PIP_PACKAGES=%3

color 5
echo project directory: %PROJECT_DIR%
echo python directory: %PYTHON_DIR%/python.exe
echo pip packages directory: %PIP_PACKAGES%

cd "%PROJECT_DIR%"
"%PYTHON_DIR%/python.exe" -m venv venv
call venv/Scripts/Activate
if not "%PIP_PACKAGES%" == ""(
    echo requirements.txt path exists, installing packages...
    python -m pip install -r "%PIP_PACKAGES%"
    color 2
    echo pip installed
) else (
    color 3
    echo no packages passed, skipping...
)
call deactivate

:process_configs
if "%4"=="" goto configs_done
if "%5"=="" goto invalid_args

set CONFIG_FILE=%4
set CONFIG_CONTENT=%5

echo Creating config file: %CONFIG_FILE%
echo %CONFIG_CONTENT% > %CONFIG_FILE%

shift
shift
goto process_configs

:invalid_args
color 4
echo ERROR: Invalid config args - missing content for file %CONFIG_FILE%
exit /b 1

:configs_done
color 2
echo All configs files created successfully
echo Setup completed. 
start "" "%PROJECT_DIR%"
exit /b 0


