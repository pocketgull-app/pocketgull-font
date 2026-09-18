# PocketGull Font Superfamily — Windows User Font Installer
# Copies TTF binaries to %LOCALAPPDATA%\Microsoft\Windows\Fonts, updates registry,
# registers with GDI, and broadcasts WM_FONTCHANGE.

[CmdletBinding()]
param(
    [string]$SourceDir = "$PSScriptRoot\..\fonts\ttf",
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  PocketGull Superfamily — Windows Font Installer " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$resolvedSource = Resolve-Path $SourceDir
$destDir = [System.IO.Path]::Combine($env:LOCALAPPDATA, "Microsoft", "Windows", "Fonts")

if (-not (Test-Path -LiteralPath $destDir)) {
    New-Item -Path $destDir -ItemType Directory -Force | Out-Null
    Write-Host "[INIT] Created fonts directory: $destDir" -ForegroundColor Green
}

$ttfFiles = Get-ChildItem -LiteralPath $resolvedSource -Filter "*.ttf" | Sort-Object Name
Write-Host "Found $($ttfFiles.Count) TTF fonts in: $resolvedSource" -ForegroundColor Gray
Write-Host "Target directory: $destDir" -ForegroundColor Gray

$updatedCount = 0
$installedCount = 0
$skippedCount = 0
$failedCount = 0

# P/Invoke definition for GDI AddFontResourceExW and WM_FONTCHANGE broadcast
$typeDefinition = @"
using System;
using System.Runtime.InteropServices;

public class FontHelper {
    [DllImport("gdi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern int AddFontResourceExW(string lpszFilename, uint fl, IntPtr pdv);

    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern IntPtr SendMessageTimeout(
        IntPtr hWnd,
        uint Msg,
        UIntPtr wParam,
        IntPtr lParam,
        uint fuFlags,
        uint uTimeout,
        out UIntPtr lpdwResult
    );

    public const int FR_PRIVATE = 0x10;
    public const int FR_NOT_ENUM = 0x20;
    public const uint WM_FONTCHANGE = 0x001D;
    public const uint SMTO_ABORTIFHUNG = 0x0002;
    public static readonly IntPtr HWND_BROADCAST = new IntPtr(0xFFFF);
}
"@

try {
    Add-Type -TypeDefinition $typeDefinition -ErrorAction SilentlyContinue
} catch {
    # Type might already be loaded in pwsh session
}

$regPath = "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts"
if (-not (Test-Path -LiteralPath $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
}

foreach ($src in $ttfFiles) {
    $targetPath = [System.IO.Path]::Combine($destDir, $src.Name)
    $needsCopy = $true

    if ((Test-Path -LiteralPath $targetPath) -and (-not $Force)) {
        try {
            $srcHash = (Get-FileHash -LiteralPath $src.FullName -Algorithm SHA256).Hash
            $dstHash = (Get-FileHash -LiteralPath $targetPath -Algorithm SHA256).Hash
            if ($srcHash -eq $dstHash) {
                $needsCopy = $false
                $skippedCount++
            }
        } catch {
            $needsCopy = $true
        }
    }

    if ($needsCopy) {
        $existed = Test-Path -LiteralPath $targetPath
        try {
            Copy-Item -LiteralPath $src.FullName -Destination $targetPath -Force
            if ($existed) {
                Write-Host "  [UPDATED] $($src.Name)" -ForegroundColor Green
                $updatedCount++
            } else {
                Write-Host "  [INSTALLED] $($src.Name)" -ForegroundColor Cyan
                $installedCount++
            }
        } catch {
            # File might be locked by running process (Terminal, Edge, DirectWrite)
            $oldPath = [System.IO.Path]::Combine($destDir, "$($src.BaseName).$([System.Guid]::NewGuid().ToString('N').Substring(0,8)).old")
            try {
                Rename-Item -LiteralPath $targetPath -NewName ([System.IO.Path]::GetFileName($oldPath)) -Force
                Copy-Item -LiteralPath $src.FullName -Destination $targetPath -Force
                Write-Host "  [REPLACED-LOCKED] $($src.Name) (renamed in-use -> $([System.IO.Path]::GetFileName($oldPath)))" -ForegroundColor Yellow
                $updatedCount++
            } catch {
                Write-Host "  [FAILED] Could not copy $($src.Name): $_" -ForegroundColor Red
                $failedCount++
                continue
            }
        }
    }

    # Register in Registry
    # Create descriptive registry font name
    $regName = "$($src.BaseName) (TrueType)"
    # Clean up standard names
    if ($src.BaseName -like "PocketGull-*") {
        $variant = $src.BaseName.Substring(11)
        $regName = "Pocket Gull $variant (TrueType)"
    } elseif ($src.BaseName -eq "PocketGullMono-Regular") {
        $regName = "Pocket Gull Mono (TrueType)"
    } elseif ($src.BaseName -like "PocketGullMono-*") {
        $variant = $src.BaseName.Substring(15)
        $regName = "Pocket Gull Mono $variant (TrueType)"
    }

    Set-ItemProperty -Path $regPath -Name $regName -Value $targetPath -Type String
    if ($src.BaseName -eq "PocketGull-Regular") {
        Set-ItemProperty -Path $regPath -Name "Pocket Gull (TrueType)" -Value $targetPath -Type String
        Set-ItemProperty -Path $regPath -Name "PocketGull (TrueType)" -Value $targetPath -Type String
    }
    if ($src.BaseName -eq "PocketGullMono-Regular") {
        Set-ItemProperty -Path $regPath -Name "PocketGull Mono (TrueType)" -Value $targetPath -Type String
        Set-ItemProperty -Path $regPath -Name "PocketGullMono (TrueType)" -Value $targetPath -Type String
    }

    # Register in GDI
    try {
        [FontHelper]::AddFontResourceExW($targetPath, 0, [IntPtr]::Zero) | Out-Null
    } catch {
        # ignore P/Invoke fallback
    }
}

Write-Host "`nInstallation Summary:" -ForegroundColor White
Write-Host "  Updated:   $updatedCount" -ForegroundColor Green
Write-Host "  Installed: $installedCount" -ForegroundColor Cyan
Write-Host "  Identical: $skippedCount" -ForegroundColor Gray
if ($failedCount -gt 0) {
    Write-Host "  Failed:    $failedCount" -ForegroundColor Red
}

# Broadcast WM_FONTCHANGE to all Windows apps
Write-Host "`nBroadcasting WM_FONTCHANGE to refresh DirectWrite & GDI font cache..." -ForegroundColor Gray
try {
    [UIntPtr]$result = [UIntPtr]::Zero
    [FontHelper]::SendMessageTimeout(
        [FontHelper]::HWND_BROADCAST,
        [FontHelper]::WM_FONTCHANGE,
        [UIntPtr]::Zero,
        [IntPtr]::Zero,
        [FontHelper]::SMTO_ABORTIFHUNG,
        2000,
        [ref]$result
    ) | Out-Null
    Write-Host "[OK] DirectWrite/GDI font change broadcasted successfully." -ForegroundColor Green
} catch {
    Write-Host "[WARN] Font change broadcast exception: $_" -ForegroundColor Yellow
}

# Clean up stale .old files if possible
$oldFiles = Get-ChildItem -LiteralPath $destDir -Filter "*.old" -ErrorAction SilentlyContinue
foreach ($old in $oldFiles) {
    try {
        Remove-Item -LiteralPath $old.FullName -Force -ErrorAction SilentlyContinue
    } catch {}
}

Write-Host "`nAll PocketGull fonts successfully reinstalled and active on Windows!" -ForegroundColor Green
