@echo off
setlocal
cd /d "%~dp0"
echo This installation keeps user data in assets/, projects/, output/, inbox/.
echo Future update packages should replace app/ and root batch files only.
echo User data folders are not part of app updates.
pause
