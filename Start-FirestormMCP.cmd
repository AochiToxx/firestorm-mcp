@echo off
"%~dp0.venv\Scripts\python.exe" -m firestorm_mcp.launcher %*
set "launch_exit=%errorlevel%"
if not "%launch_exit%"=="0" pause
exit /b %launch_exit%
