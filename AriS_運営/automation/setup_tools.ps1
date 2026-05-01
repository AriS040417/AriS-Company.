$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$toolsDir = Join-Path $scriptDir "tools"
$pythonDir = Join-Path $toolsDir "python"
$ffmpegDir = Join-Path $toolsDir "ffmpeg"
$ffmpegBinDir = Join-Path $ffmpegDir "bin"

New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null

$pythonExe = Join-Path $pythonDir "python.exe"
if (-not (Test-Path $pythonExe)) {
  $pythonZip = Join-Path $toolsDir "python-embed.zip"
  Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip" -OutFile $pythonZip
  New-Item -ItemType Directory -Force -Path $pythonDir | Out-Null
  Expand-Archive -Path $pythonZip -DestinationPath $pythonDir -Force
}

$pthFile = Join-Path $pythonDir "python311._pth"
if (Test-Path $pthFile) {
  $pthText = Get-Content -Raw -Path $pthFile
  if ($pthText -match "#import site") {
    $pthText = $pthText -replace "#import site", "import site"
    Set-Content -Path $pthFile -Value $pthText -Encoding UTF8
  }
}

$getPip = Join-Path $pythonDir "get-pip.py"
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $getPip
& $pythonExe $getPip
& $pythonExe -m pip install -r (Join-Path $scriptDir "requirements.txt")

if (-not (Test-Path (Join-Path $ffmpegBinDir "ffmpeg.exe"))) {
  $ffmpegZip = Join-Path $toolsDir "ffmpeg.zip"
  Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile $ffmpegZip

  $extractRoot = Join-Path $ffmpegDir "raw"
  New-Item -ItemType Directory -Force -Path $extractRoot | Out-Null
  Expand-Archive -Path $ffmpegZip -DestinationPath $extractRoot -Force

  $foundBin = Get-ChildItem -Path $extractRoot -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1
  if (-not $foundBin) {
    throw "ffmpeg.exe not found after extraction"
  }
  $sourceBinDir = Split-Path -Parent $foundBin.FullName
  New-Item -ItemType Directory -Force -Path $ffmpegBinDir | Out-Null
  Copy-Item -Path (Join-Path $sourceBinDir "*.exe") -Destination $ffmpegBinDir -Force
}

Write-Output "setup complete"
Write-Output "python: $pythonExe"
Write-Output "ffmpeg: $(Join-Path $ffmpegBinDir 'ffmpeg.exe')"
