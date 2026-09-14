@echo off
setlocal
cd /d "%~dp0"
echo Mongi Renderer V1.6 - Windows Setup
where python >nul 2>nul
if errorlevel 1 (
  echo [!] Python not found.
  where winget >nul 2>nul || goto :manual_python
  winget install -e --id Python.Python.3.12
  echo Python installed. Reopen this file once PATH refreshes.
  pause
  exit /b 0
)
python -m pip install -r app\requirements.txt
if errorlevel 1 (
  echo [!] Python dependency install failed.
  pause
  exit /b 1
)
where ffmpeg >nul 2>nul
if errorlevel 1 (
  where winget >nul 2>nul || goto :manual_ffmpeg
  winget install -e --id Gyan.FFmpeg
  echo FFmpeg installed. Reopen this file once PATH refreshes.
  pause
  exit /b 0
)
where ffprobe >nul 2>nul
if errorlevel 1 goto :manual_ffmpeg
python app\bootstrap.py
if errorlevel 1 (
  echo [!] Setup verification failed.
  pause
  exit /b 1
)
echo.
echo Setup complete.
pause
exit /b 0
:manual_python
echo Install Python 3.10+ first, then rerun.
pause
exit /b 1
:manual_ffmpeg
echo Install FFmpeg including ffprobe and add it to PATH, then rerun.
pause
exit /b 1
