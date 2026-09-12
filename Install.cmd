@echo off
python "%~dp0install.py" %*
set "setup_exit=%errorlevel%"
pause
exit /b %setup_exit%
