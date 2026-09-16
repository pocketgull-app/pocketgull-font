#!/usr/bin/env python3
"""
PocketGull Superfamily Master Release Packager
==============================================
Bundles the complete v3.1.0 release archive containing:
  - fonts/ttf/ (All 29 production TrueType binaries)
  - fonts/woff2/ (All 29 WOFF2 webfonts)
  - distribution/python/dist/ (Wheel & sdist)
  - distribution/latex/pocketgull-math.zip (CTAN package)
  - distribution/typst/ (Typst package + thumbnail.png)
  - distribution/matplotlib/ (4 stylesheets)
  - OFL.txt and README.md

Outputs:
  - pocketgull-typeface-v3.1.0.zip
  - PocketGull-v3.1.0-Superfamily.zip (symlink / copy)
  - Computes SHA256 for Homebrew and Winget
"""

import os
import sys
import hashlib
import zipfile
import shutil

VERSION = "3.1.0"
ZIP_NAME = f"pocketgull-font-v{VERSION}.zip"
SUPER_NAME = f"PocketGull-v{VERSION}-Superfamily.zip"

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def package():
    print(f"Creating {ZIP_NAME}...")
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
        # TTF Fonts
        for root, _, files in os.walk("fonts/ttf"):
            for f in files:
                if f.endswith(".ttf"):
                    p = os.path.join(root, f)
                    zf.write(p, p.replace("\\", "/"))
        
        # WOFF2 Fonts
        for root, _, files in os.walk("fonts/woff2"):
            for f in files:
                if f.endswith(".woff2"):
                    p = os.path.join(root, f)
                    zf.write(p, p.replace("\\", "/"))

        # Matplotlib Styles
        for root, _, files in os.walk("distribution/matplotlib"):
            for f in files:
                if f.endswith(".mplstyle"):
                    p = os.path.join(root, f)
                    zf.write(p, p.replace("\\", "/"))

        # Python Dist
        for root, _, files in os.walk("distribution/python/dist"):
            for f in files:
                p = os.path.join(root, f)
                zf.write(p, p.replace("\\", "/"))

        # LaTeX CTAN
        ctan_zip = "distribution/latex/pocketgull-math.zip"
        if os.path.exists(ctan_zip):
            zf.write(ctan_zip, ctan_zip.replace("\\", "/"))

        # Typst
        for root, _, files in os.walk("distribution/typst"):
            for f in files:
                p = os.path.join(root, f)
                zf.write(p, p.replace("\\", "/"))

        # Root licenses & docs
        if os.path.exists("OFL.txt"):
            zf.write("OFL.txt", "OFL.txt")
        if os.path.exists("README.md"):
            zf.write("README.md", "README.md")
        if os.path.exists("fonts.css"):
            zf.write("fonts.css", "fonts.css")

    # Copy to Superfamily alias
    shutil.copyfile(ZIP_NAME, SUPER_NAME)
    
    sha256 = get_sha256(ZIP_NAME)
    size_mb = os.path.getsize(ZIP_NAME) / (1024 * 1024)
    print(f"Successfully packaged {ZIP_NAME} ({size_mb:.2f} MB)")
    print(f"SHA256: {sha256}")
    print(f"Also created {SUPER_NAME}")
    return sha256

if __name__ == "__main__":
    package()
