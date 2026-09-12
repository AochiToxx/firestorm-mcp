param([string]$Python = 'python', [switch]$Development)
$ErrorActionPreference = 'Stop'
$setupArgs = @((Join-Path $PSScriptRoot 'install.py'))
if ($Development) { $setupArgs += '--development' }
& $Python @setupArgs
if ($LASTEXITCODE) { throw 'Installation failed. See the reason above.' }
