#!/usr/bin/env python3
"""
Hermetic Wheel & sdist builder for pocketgull-math
Produces standard PEP 427 .whl and sdist .tar.gz archives without external build dependencies.
"""

import os
import sys
import hashlib
import base64
import zipfile
import tarfile
import shutil

DIST_DIR = os.path.join("distribution", "python", "dist")
SRC_DIR = os.path.join("distribution", "python", "pocketgull_math")
PKG_NAME = "pocketgull_math"
VERSION = "3.1.0"
WHEEL_TAG = "py3-none-any"
WHEEL_NAME = f"{PKG_NAME}-{VERSION}-{WHEEL_TAG}.whl"
SDIST_NAME = f"{PKG_NAME}-{VERSION}.tar.gz"

os.makedirs(DIST_DIR, exist_ok=True)

def b64_digest(data):
    digest = hashlib.sha256(data).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")

def build_wheel():
    wheel_path = os.path.join(DIST_DIR, WHEEL_NAME)
    dist_info = f"{PKG_NAME}-{VERSION}.dist-info"
    
    metadata = f"""Metadata-Version: 2.1
Name: pocketgull-math
Version: {VERSION}
Summary: 1-Line Matplotlib & Scientific Visualization Integration for PocketGull Math
Home-page: https://font.pocketgull.app
Author: Phil Gear
License: OFL-1.1
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Science/Research
Classifier: Intended Audience :: Healthcare Industry
Classifier: Topic :: Scientific/Engineering :: Visualization
Classifier: Topic :: Scientific/Engineering :: Medical Science Apps.
Classifier: License :: OSI Approved :: SIL Open Font License 1.1 (OFL-1.1)
Classifier: Programming Language :: Python :: 3
Requires-Python: >=3.8
Requires-Dist: matplotlib>=3.5.0
Description-Content-Type: text/markdown

# PocketGull Math for Matplotlib & Python
1-Line scientific telemetry stylesheets and font integration.
"""

    wheel_info = f"""Wheel-Version: 1.0
Generator: pocketgull-builder ({VERSION})
Root-Is-Purelib: true
Tag: {WHEEL_TAG}
"""

    records = []

    with zipfile.ZipFile(wheel_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Package files
        for root, _, files in os.walk(SRC_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, os.path.dirname(SRC_DIR))
                with open(full_path, "rb") as f:
                    content = f.read()
                norm_path = rel_path.replace("\\", "/")
                zf.writestr(norm_path, content)
                records.append(f"{norm_path},sha256={b64_digest(content)},{len(content)}")

        # 2. Metadata
        meta_bytes = metadata.strip().encode("utf-8")
        zf.writestr(f"{dist_info}/METADATA", meta_bytes)
        records.append(f"{dist_info}/METADATA,sha256={b64_digest(meta_bytes)},{len(meta_bytes)}")

        wheel_bytes = wheel_info.strip().encode("utf-8")
        zf.writestr(f"{dist_info}/WHEEL", wheel_bytes)
        records.append(f"{dist_info}/WHEEL,sha256={b64_digest(wheel_bytes)},{len(wheel_bytes)}")

        # 3. RECORD
        records.append(f"{dist_info}/RECORD,,")
        record_content = "\n".join(records) + "\n"
        zf.writestr(f"{dist_info}/RECORD", record_content.encode("utf-8"))

    print(f"Created Wheel: {wheel_path} (Size: {os.path.getsize(wheel_path)} bytes)")

def build_sdist():
    sdist_path = os.path.join(DIST_DIR, SDIST_NAME)
    base_prefix = f"{PKG_NAME}-{VERSION}"
    
    with tarfile.open(sdist_path, "w:gz") as tar:
        # pyproject.toml
        tar.add("distribution/python/pyproject.toml", arcname=f"{base_prefix}/pyproject.toml")
        # README.md
        tar.add("distribution/python/README.md", arcname=f"{base_prefix}/README.md")
        # pocketgull_math/
        tar.add(SRC_DIR, arcname=f"{base_prefix}/pocketgull_math")
        
    print(f"Created sdist: {sdist_path} (Size: {os.path.getsize(sdist_path)} bytes)")

if __name__ == "__main__":
    build_wheel()
    build_sdist()
