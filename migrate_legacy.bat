@echo off
setlocal
cd /d "%~dp0"
echo Mongi Renderer legacy data migration
set /p OLD=Old MongiRenderer folder path: 
python app\migrate_legacy.py "%OLD%"
pause
