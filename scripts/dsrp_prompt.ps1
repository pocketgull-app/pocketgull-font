## Project Ataxia & PocketGull Systems Thinking DSRP Prompt Script
# Implements the Cabrera Research Lab (Cornell University) DSRP 4x2 loop for terminal sessions.
# Runs 100% offline using local files, rendering native PocketGull Systems Thinking glyphs (U+E9E0-U+E9E3).

param(
    [switch]$NonInteractive
)

$ConfigPath = Join-Path $PSScriptRoot 'dsrp_config.json'

function Get-DSRPConfig {
    if (Test-Path $ConfigPath) {
        $json = Get-Content $ConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
    } else {
        Write-Error "DSRP config not found at $ConfigPath"
        return $null
    }
    return $json
}

function Show-DSRPPrompt {
    param([switch]$NoWait)
    $cfg = Get-DSRPConfig
    if (-not $cfg) { return }
    $d = $cfg.D | Get-Random
    $s = $cfg.S | Get-Random
    $r = $cfg.R | Get-Random
    $p = $cfg.P | Get-Random

    $glyphD = [char]0xE9E0
    $glyphS = [char]0xE9E1
    $glyphR = [char]0xE9E2
    $glyphP = [char]0xE9E3

    Write-Host "`n  ══════════════════════════════════════════════════════════════════════════" -ForegroundColor DarkCyan
    Write-Host "   POCKETGULL SYSTEMS THINKING & DSRP COGNITIVE LOOP (600 UPM)" -ForegroundColor Cyan
    Write-Host "  ══════════════════════════════════════════════════════════════════════════" -ForegroundColor DarkCyan
    Write-Host "`n  🟦 $glyphD  D (Distinctions)  — $d" -ForegroundColor Cyan
    Write-Host "  🟩 $glyphS  S (Systems)       — $s" -ForegroundColor Green
    Write-Host "  🟥 $glyphR  R (Relationships) — $r" -ForegroundColor Red
    Write-Host "  🟪 $glyphP  P (Perspectives)  — $p`n" -ForegroundColor Magenta

    if ($cfg.metadata) {
        Write-Host "  🎙️  Podcast : $($cfg.metadata.podcast)" -ForegroundColor Gray
        Write-Host "  🎓  Cornell : $($cfg.metadata.cornell_course)" -ForegroundColor Gray
        Write-Host "  🧭  STSI    : $($cfg.metadata.stsi_institute)`n" -ForegroundColor Gray
    }

    if (-not $NoWait -and -not $NonInteractive) {
        Write-Host "  (Reflect on each pattern in your terminal or journal. Press ENTER to continue…)" -ForegroundColor Yellow
        [void](Read-Host)
    }
}

function Invoke-DSRP {
    Show-DSRPPrompt -NoWait:$NonInteractive
}

if ($MyInvocation.InvocationName -ne '.') {
    Show-DSRPPrompt -NoWait:$NonInteractive
}

