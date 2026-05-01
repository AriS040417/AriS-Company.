$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
$pythonExe = Join-Path $scriptDir "tools/python/python.exe"
$pipelinePy = Join-Path $scriptDir "run_pipeline.py"

if (-not (Test-Path $pythonExe)) {
  throw "Portable Python not found. Run automation/setup_tools.ps1 first."
}

& $pythonExe $pipelinePy @args
