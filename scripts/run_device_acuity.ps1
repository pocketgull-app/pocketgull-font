# ==============================================================================
# PocketGull Foundry — Clinical Device Acuity & Snellen/Sloan Optical Benchmark
# ==============================================================================
# COST SAFEGUARD: This script is only executed on major upstream foundry release tags.
# It runs local optical and acuity metrics with $0.00 cloud device expenditure.
# ==============================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  🔬 POCKETGULL CLINICAL DEVICE ACUITY & SNELLEN/SLOAN BENCHMARK" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Cost Policy: Strict `$0.00/mo (Workstation Direct Rendering)"
Write-Host "  Optotype:    Louise Sloan 5:1 Grid (1000 UPM / 200 UPM Stroke)"
Write-Host "  Target:      Thermal 203 DPI, High-DPI Mobile & Scotopic Night Display"
Write-Host "======================================================================`n"

# 1. Run Pure-Dart Seven Pillars Compliance Auditor
dart run tool/pocketgull_foundry.dart compliance
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 2. Run Google OSV Dependency & Lockfile Security Audit
dart run tool/pocketgull_foundry.dart osv
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 3. Run Automated SWE Invariant Unit Tests
npm run test:unit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n======================================================================" -ForegroundColor Green
Write-Host "  🏆 CLINICAL ACUITY & OPTICAL VERIFICATION COMPLETE" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
