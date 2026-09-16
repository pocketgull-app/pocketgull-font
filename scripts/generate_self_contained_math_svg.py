#!/usr/bin/env python3
"""
PocketGull Typefoundry: Self-Contained SVG Embedder
====================================================
Embeds 'PocketGull-Math.woff2' directly into SVG files as a base64 Data URI.
Guarantees 100% visual fidelity on any client, browser, or markdown viewer
without requiring the user or operating system to have PocketGull installed.
"""

import os
import sys
import base64
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
WOFF2_PATH = os.path.join(ROOT_DIR, "fonts", "woff2", "PocketGull-Math.woff2")
TTF_PATH = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Math.ttf")

def get_font_base64():
    target = WOFF2_PATH if os.path.isfile(WOFF2_PATH) else TTF_PATH
    fmt = "woff2" if target.endswith(".woff2") else "truetype"
    if not os.path.isfile(target):
        raise FileNotFoundError(f"Neither {WOFF2_PATH} nor {TTF_PATH} found.")
    with open(target, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("ascii")
    return b64, fmt

def embed_font_in_svg(svg_content):
    b64, fmt = get_font_base64()
    font_face_rule = f"""
    @font-face {{
      font-family: 'PocketGull Math';
      src: url('data:font/{fmt};base64,{b64}') format('{fmt}');
      font-weight: 400;
      font-style: normal;
    }}
"""
    # If <defs> exists, insert into existing <style> or create one
    if "<style>" in svg_content:
        # Replace first <style> with <style> + font_face_rule
        svg_content = svg_content.replace("<style>", f"<style>{font_face_rule}", 1)
    elif "<defs>" in svg_content:
        svg_content = svg_content.replace("<defs>", f"<defs><style>{font_face_rule}</style>", 1)
    else:
        # Insert after <svg ...>
        svg_tag_end = svg_content.find(">")
        if svg_tag_end != -1:
            svg_content = (
                svg_content[:svg_tag_end + 1]
                + f"\n  <defs><style>{font_face_rule}</style></defs>"
                + svg_content[svg_tag_end + 1:]
            )
    return svg_content

def process_svg_file(input_path, output_path=None):
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_embedded{ext}"
    
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    embedded = embed_font_in_svg(content)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(embedded)
    
    in_sz = os.path.getsize(input_path)
    out_sz = os.path.getsize(output_path)
    print(f"[OK] Embedded font into: {output_path} ({in_sz:,} -> {out_sz:,} bytes)")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for p in sys.argv[1:]:
            process_svg_file(p)
    else:
        default_svg = os.path.join(ROOT_DIR, "documentation", "images", "pocketgull_math_telemetry_plate.svg")
        if os.path.isfile(default_svg):
            process_svg_file(default_svg)
        else:
            print(f"Usage: {sys.argv[0]} <path_to_svg>")
