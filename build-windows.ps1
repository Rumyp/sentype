$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Python312 = Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"
if (-not (Test-Path $Python312)) {
  throw "Python 3.12 is required for the Windows Nuitka build. Install it with: winget install --id Python.Python.3.12 --exact"
}

if (-not (Test-Path "$Root\.venv312\Scripts\python.exe")) {
  & $Python312 -m venv "$Root\.venv312"
}

$BuildPython = "$Root\.venv312\Scripts\python.exe"
& $BuildPython -m pip install --upgrade pip
& $BuildPython -m pip install -r requirements-build.txt

& $BuildPython -m nuitka `
  --onefile `
  --standalone `
  --assume-yes-for-downloads `
  --mingw64 `
  --windows-console-mode=force `
  --output-filename=sentype.exe `
  --include-data-files=sentences_easy.txt=sentences_easy.txt `
  --include-data-files=sentences_medium.txt=sentences_medium.txt `
  --include-data-files=sentences_hard.txt=sentences_hard.txt `
  --include-data-files=words.txt=words.txt `
  game.py

New-Item -ItemType Directory -Force -Path "$Root\release" | Out-Null
$ReleaseExe = "$Root\release\sentype-0.2.1-windows-x64.exe"
for ($Attempt = 1; $Attempt -le 10; $Attempt++) {
  try {
    Copy-Item "$Root\sentype.exe" $ReleaseExe -Force
    break
  } catch {
    if ($Attempt -eq 10) {
      throw
    }
    Start-Sleep -Seconds 2
  }
}
Get-FileHash "$Root\release\sentype-0.2.1-windows-x64.exe" -Algorithm SHA256 |
  Format-List Path, Hash
