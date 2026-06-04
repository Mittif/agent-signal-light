@echo off
setlocal

cd /d "%~dp0"

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if %ERRORLEVEL%==0 (
        py -3 install.py %*
        exit /b %ERRORLEVEL%
    )
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
    python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if %ERRORLEVEL%==0 (
        python install.py %*
        exit /b %ERRORLEVEL%
    )
)

where python3 >nul 2>nul
if %ERRORLEVEL%==0 (
    python3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if %ERRORLEVEL%==0 (
        python3 install.py %*
        exit /b %ERRORLEVEL%
    )
)

echo Could not find Python 3.10 or newer.
echo Install Python from https://www.python.org/downloads/windows/
echo During setup, enable "Add python.exe to PATH", then rerun install.cmd.
exit /b 1
