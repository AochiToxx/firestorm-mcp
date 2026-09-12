@echo off
"%~dp0.venv\Scripts\python.exe" -m firestorm_mcp.probe %*
set "check_exit=%errorlevel%"
pause
exit /b %check_exit%
