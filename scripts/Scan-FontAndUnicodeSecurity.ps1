<#
.SYNOPSIS
  PocketGull Windows Local Font & Repository Security Scanner (100% Offline)
.DESCRIPTION
  Helps developers, clinicians, and hardware engineers explore their local machine or Git repository for:
  1. Hidden Trojan Source BiDi overrides (CVE-2021-42574), Fake Spaces (U+3164), and Emoji Smuggling (U+E0100-U+E01EF).
  2. Legacy TrueType Bytecode Virtual Machine tables (fpgm, prep, cvt) and HarfBuzz WebAssembly shaper tables (Wasm, CVE-2026-113679 / CVE-2026-113680) in installed fonts.
  3. Unaligned 2-byte loca offsets or restrictive OS/2.fsType DRM locks.
.EXAMPLE
  pwsh scripts/Scan-FontAndUnicodeSecurity.ps1
  pwsh scripts/Scan-FontAndUnicodeSecurity.ps1 -IncludeSystemFonts
#>
param(
  [string]$TargetDir = (Resolve-Path "$PSScriptRoot\..").Path,
  [switch]$IncludeSystemFonts
)

$ErrorActionPreference = 'Stop'
$scriptPath = Join-Path $PSScriptRoot 'scan-font-security.mjs'

if ($IncludeSystemFonts) {
  node $scriptPath $TargetDir --system-fonts
} else {
  node $scriptPath $TargetDir
}
