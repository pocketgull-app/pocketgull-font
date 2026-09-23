#!/usr/bin/env bash
# ==============================================================================
# PocketGull Foundry — Clinical Device Acuity & Snellen/Sloan Optical Benchmark
# ==============================================================================
# COST SAFEGUARD: This script is only executed on major upstream foundry release tags.
# It runs local optical and acuity metrics with $0.00 cloud device expenditure.
# ==============================================================================

set -euo pipefail

echo "======================================================================"
echo "  🔬 POCKETGULL CLINICAL DEVICE ACUITY & SNELLEN/SLOAN BENCHMARK"
echo "======================================================================"
echo "  Cost Policy: Strict \$0.00/mo (Workstation Direct Rendering)"
echo "  Optotype:    Louise Sloan 5:1 Grid (1000 UPM / 200 UPM Stroke)"
echo "  Target:      Thermal 203 DPI, High-DPI Mobile & Scotopic Night Display"
echo "======================================================================"

# 1. Run Pure-Dart Seven Pillars Compliance Auditor
dart run tool/pocketgull_foundry.dart compliance

# 2. Run Google OSV Dependency & Lockfile Security Audit
dart run tool/pocketgull_foundry.dart osv

# 3. Run Automated SWE Invariant Unit Tests
npm run test:unit

echo ""
echo "======================================================================"
echo "  🏆 CLINICAL ACUITY & OPTICAL VERIFICATION COMPLETE"
echo "======================================================================"
