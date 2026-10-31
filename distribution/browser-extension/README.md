# PocketGull Unicode & Font Leak Inspector (Browser Extension)

A 100% local, zero-egress **Manifest V3** developer extension for inspecting GitHub pull requests, web applications, and clinical interfaces for hidden Unicode spoofing (`CVE-2021-42574`), Emoji Smuggling (`VS17`–`VS256`), and webfont Subresource Integrity (SRI) leaks.

## Key Security & Privacy Guarantees
1. **Zero Background Execution & Zero Telemetry**: Uses `"activeTab"` only—never runs automatically in the background and makes zero network requests.
2. **Zero Multilingual False Positives**: Distinguishes dangerous BiDi overrides (`U+202E`) and fake spaces (`U+3164`) from legitimate script joiners (`U+200C` Persian `ZWNJ`, `U+200D` Emoji `ZWJ`, `U+FE0F` `VS16`).
3. **1-Click `[!]` Badge Reveal**: Temporarily replaces invisible Trojan Source / Variation Selector smuggling characters on the active page with visible `[!U+XXXX]` markers.

## How to Load Locally (Chrome / Edge / Brave)
1. Open `chrome://extensions` (or `edge://extensions`).
2. Enable **Developer mode** (top right toggle).
3. Click **Load unpacked** and select this folder: `distribution/browser-extension/`.
