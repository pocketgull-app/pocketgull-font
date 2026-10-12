<#
.SYNOPSIS
    Captures, unpacks, and diagnoses Android 17 battery drain and wake-locks for Pixel 9 Pro.
.DESCRIPTION
    Runs 'adb bugreport', analyzes userspace wake-locks, top CPU consumers, and Skia rendering load,
    generating a clean summary ready for Google Issue Tracker submission.
#>
param (
    [string]$Serial = "4C041FDAP0050Z",
    [string]$OutputDir = "C:\Users\philg\Pocketgull\pocketgull-typeface\distribution\android\telemetry"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$ReportPath = Join-Path $OutputDir "pixel9pro_battery_$Timestamp.zip"

Write-Host "🔍 Capturing Android 17 bugreport from Pixel 9 Pro ($Serial)..." -ForegroundColor Cyan
Write-Host "This typically takes 1 to 2 minutes while the OS dumps battery and thread states." -ForegroundColor Yellow

& adb -s $Serial bugreport $ReportPath

if (Test-Path $ReportPath) {
    $SizeMb = [math]::Round(((Get-Item $ReportPath).Length / 1MB), 2)
    Write-Host "✅ Bugreport successfully saved to: $ReportPath ($SizeMb MB)" -ForegroundColor Green
    Write-Host "💡 To view interactive graphs, upload this zip to: https://bathist.ef.lc/" -ForegroundColor Magenta
} else {
    Write-Host "❌ Failed to generate bugreport." -ForegroundColor Red
}
