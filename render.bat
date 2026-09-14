@echo off
setlocal
cd /d "%~dp0"
echo Mongi Renderer V1.6
python app\bootstrap.py
if errorlevel 1 (
  echo.
  echo Startup check failed.
  pause
  exit /b %errorlevel%
)
echo.
python app\run_inbox.py
if errorlevel 1 (
  echo.
  echo Render/import failed.
  pause
  exit /b %errorlevel%
)
echo.
echo DONE
pause
