# build.ps1 — build DevVault.exe via PyInstaller

$ErrorActionPreference = "Stop"

Write-Host "=== DevVault build ===" -ForegroundColor Cyan

# Clean previous builds
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist")  { Remove-Item -Recurse -Force "dist" }

# Make sure PyInstaller is available
$py = "C:\Python314\python.exe"
& $py -m PyInstaller --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller not installed. Installing..." -ForegroundColor Yellow
    & $py -m pip install pyinstaller
}

# Build
Write-Host "Running PyInstaller..." -ForegroundColor Cyan
& $py -m PyInstaller DevVault.spec --noconfirm

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build FAILED." -ForegroundColor Red
    exit 1
}

$exe = "dist\DevVault\DevVault.exe"
if (-not (Test-Path $exe)) {
    Write-Host "Executable not found at $exe" -ForegroundColor Red
    exit 1
}

$size = (Get-ChildItem "dist\DevVault" -Recurse |
         Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host ""
Write-Host "Build OK" -ForegroundColor Green
Write-Host "  EXE:  $exe"
Write-Host "  Size: $([math]::Round($size, 1)) MB"
Write-Host ""
Write-Host "Run:  .\dist\DevVault\DevVault.exe"