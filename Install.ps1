param([string]$Python = 'python', [switch]$Development)
$ErrorActionPreference = 'Stop'
$projectDir = $PSScriptRoot
$venvPython = Join-Path $projectDir '.venv\Scripts\python.exe'
if (!(Test-Path -LiteralPath $venvPython)) {
    & $Python -m venv (Join-Path $projectDir '.venv')
    if ($LASTEXITCODE) { throw 'Python 3.11 or newer is required. Install Python and retry.' }
}
# Python's bundled pip may predate archive-extraction security fixes.
# Upgrade only this project's environment, never the user's global Python.
& $venvPython -m pip --disable-pip-version-check install --upgrade 'pip>=26.2,<27'
if ($LASTEXITCODE) { throw 'Could not update the isolated package installer.' }
if ($Development) {
    Push-Location -LiteralPath $projectDir
    try { & $venvPython -m pip --disable-pip-version-check install -e '.[test]' }
    finally { Pop-Location }
} else {
    & $venvPython -m pip --disable-pip-version-check install $projectDir
}
if ($LASTEXITCODE) { throw 'Dependency installation failed. Read the error above.' }
Write-Output 'Firestorm MCP installed. No viewer or agent configuration was changed.'
Write-Output 'Start-FirestormMCP.cmd starts the viewer with LEAP when you are ready.'
Write-Output 'Check-FirestormMCP.cmd checks the connection without launching the viewer.'
Write-Output 'MCP server command:'
Write-Output $venvPython
Write-Output 'Arguments: -m firestorm_mcp.server --tool-profile compact'
