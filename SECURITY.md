# Security Policy

At **PocketGull**, security, cryptographic determinism, and typography asset integrity are foundational. We adhere to **OpenSSF (Open Source Security Foundation)** standards and treat font binary compilation, glyph parsing safety, and supply chain provenance as safety-critical engineering disciplines.

## Supported Versions (Semantic Versioning 2.0.0)

We follow strict Semantic Versioning (`MAJOR.MINOR.PATCH`). Active production releases receive full security and typographic maintenance updates.

| Version | Supported          | Status |
| :--- | :---: | :--- |
| **3.0.x** | :white_check_mark: | **Active Production Superfamily Release (Google Fonts Option 5 Standard)** |
| 2.0.x | :white_check_mark: | Maintenance & LTS security updates |
| 1.0.x | :x: | Deprecated / End-of-Life |

---

## Reporting a Vulnerability

If you discover a security vulnerability, memory corruption risk, buffer handling flaw, or malicious font binary condition within PocketGull Font, please do **not** disclose it publicly.

Please report vulnerabilities through our coordinated private disclosure channels:

1. **GitHub Private Vulnerability Reporting (Preferred)**:
   [Submit a Private Advisory via GitHub Security](https://github.com/pocketgull-app/pocketgull-font/security/advisories/new)
2. **Security & Data Protection Officer**:
   PocketGull LLC, 101 SW Madison St #1664, Portland, Oregon 97207 USA  
   Email: **dpo@pocketgull.app** or **philgear@gmail.com**.

### Response Timeline
* **Initial Acknowledgement**: Within **24–48 hours**.
* **Triage & Reproduction**: Within **3 business days**.
* **Remediation & Patch Release**: Within **7 business days**, accompanied by a cryptographically signed GitHub Release with SHA-256 binary manifests.

---

## OpenSSF Supply Chain & Font Binary Security Standards

1. **W3C OpenType Sanitizer (OTS) Pre-Flight Hardening**:
   All font binaries (`.ttf`, `.woff2`) MUST achieve 100% pass rates across W3C OTS validation prior to release, ensuring zero buffer overruns or malformed table boundaries in client browsers.
2. **Strict 2-Byte Word-Boundary Alignment**:
   All TrueType `.glyf` records are padded to strict 2-byte word boundaries (`loca[i] % 2 == 0`) and table checksum adjustments are cryptographically recomputed (`0xB1B0AFBA - fontChecksum`).
3. **Zero Executable Code Injection (Names & Postscript Tables)**:
   Font name tables (`nameID 0–25`) and PostScript strings are sanitized of non-printable control characters, zero-width Unicode vectors, and script execution triggers.
4. **Deterministic OpenType Compilation**:
   Binaries are compiled with deterministic timestamps (`SOURCE_DATE_EPOCH=1700000000`) to guarantee reproducible builds and verifiable artifact digests.
5. **Zero Secret & Zero Telemetry Invariant**:
   Font binaries and the interactive web specimen contain zero analytics scripts, zero tracking pixels, and zero outbound network egress.

---

## 🏥 HIPAA & COPPA Statutory Compliance

### 1. HIPAA Safe Harbor & BAA Exemption (45 CFR Parts 160 & 164)
* **Zero ePHI Ingestion or Storage**: The PocketGull font software (`.ttf`, `.woff2`) is passive typographical rendering software. It possesses no networking stack, maintains no disk or database caches of rendered glyph strings, and establishes zero outbound sockets.
* **No Business Associate Agreement (BAA) Required**: Under 45 CFR § 164.502(e) and § 164.103, software that does not create, receive, maintain, or transmit electronic Protected Health Information (ePHI) on behalf of a Covered Entity is exempt from BAA execution.
* **100% Client-Side Safe Harbor**: All browser-based specimen testers, variable font axes, and Doc Drill interfaces execute 100% in local client memory (`window.localStorage` strictly for theme preferences). Clinical text pasted into testers never leaves the browser tab.
* **ISMP / FDA Error Reduction**: Character disambiguation features (slashed zero `cv08`, curved `l` `cv05`, serifed `I` `ss02`) directly reinforce HIPAA Security Rule data integrity standards (§ 164.312(c)(1)) by preventing human misinterpretation of medical orders.

### 2. COPPA Statutory Exemption (15 U.S.C. § 6501–6506; 16 CFR Part 312)
* **Zero Personal Information (PI) Collection**: PocketGull does not collect, log, store, or transmit names, email addresses, physical addresses, persistent device identifiers (no tracking cookies, no canvas fingerprinting), geolocation, or multimedia from any user.
* **No User Accounts or Authentication**: The specimen website operates entirely unauthenticated without registration forms, paywalls, or profiling algorithms.
* **Pediatric Healthcare & K-12 Educational Safety**: PocketGull is fully cleared for deployment across pediatric hospital wards, children's emergency clinics, and K-12 tribal language immersion schools (e.g. Inuktitut, Cherokee, Chinuk Wawa literacy programs) with zero parental consent obligations under COPPA.

---

## ⚖️ FDA Regulatory Classification & Medical Software Liability Disclaimer

### 1. Non-Device Clinical Decision Support (21 U.S.C. § 360j(o))
* **Statutory Classification**: PocketGull Font Superfamily is typographical rendering software and visual communication infrastructure. Under **Section 3060 of the 21st Century Cures Act** (amending the Federal Food, Drug, and Cosmetic Act at 21 U.S.C. § 360j(o)) and the **FDA Final Guidance on Clinical Decision Support Software (September 2022)**, typographical display libraries are explicitly classified as non-device software functions.
* **No Autonomous Diagnostic Function**: PocketGull does not analyze, process, interpret, or calculate patient physiological parameters, diagnostic conclusions, or therapeutic regimens. It serves solely as an optical presentation layer for human clinical review.
* **CDRH Human Factors Alignment**: While exempt from 510(k) premarket notification and 21 CFR Part 820 Quality System Regulations (QSR), PocketGull's stroke geometry, Louise Sloan 5:1 optotypes, and character disambiguation strictly adhere to **FDA CDRH Human Factors Engineering guidelines (ANSI/AAMI HE75:2009/(R)2018)**.

### 2. SIL Open Font License 1.1 Warranty Disclaimer & Tort Immunity
* Under **Section 6 of the SIL Open Font License 1.1**, the font software is provided *"AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED*.
* In no event shall the copyright holders or contributors be liable for any claim, damages, or other liability arising from the use or inability to use the font software in clinical EHR, telemetry, or diagnostic environments (*Mracek v. Bryn Mawr Hospital* distinction between products liability and clinical software infrastructure).

---

## 🔐 Cryptographic Provenance & NIST SP 800-218 (SSDF) Alignment

To satisfy **Executive Order 14028** and **NIST SP 800-218 Secure Software Development Framework (SSDF)** requirements for hospital and Health IT enterprise deployments:

1. **Deterministic Release Digests**:
   Every production release includes an authoritative `fonts/SHA256SUMS` manifest containing cryptographic SHA-256 digests for all TrueType (`.ttf`) and Web Open Font Format (`.woff2`) binaries.
   ```bash
   # Verify release binary integrity
   sha256sum -c fonts/SHA256SUMS
   ```
2. **Subresource Integrity (SRI) Manifest**:
   All webfont deliverables include pre-computed W3C Subresource Integrity (`sha384-...`) hashes in `fonts/sri-hashes.json` for CDN deployment, preventing tampering and cross-site font injection.
   ```html
   <link rel="preload" href="https://font.pocketgull.app/fonts/woff2/PocketGull-Bold.woff2" 
         as="font" type="font/woff2" crossorigin 
         integrity="sha384-c0eHz2vKk8U9h/L97q09eWw6b5A2b4c1d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6">
   ```
3. **Reproducible Compilation Pipeline**:
   TrueType binaries are compiled using deterministic SFNT builders with static timestamps, guaranteeing bit-for-bit reproducibility across independent audit environments.

