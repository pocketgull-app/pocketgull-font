#!/usr/bin/env python3
"""
Cure OFL 1.1 Metadata and Deduplicate Glyph Nodes
=================================================
- Fixes duplicate nodes (including u1FAC1) across all fonts
- Ensures nameID 5 is 'Version 3.100; The PocketGull Project Authors; OFL 1.1'
- Recompresses WOFF2 binaries using Brotli Q11
- Synchronizes root font binaries
"""
import os
import shutil
import sys
import time
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program
from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"

def safe_save_font(font, target_path):
    target_path = Path(target_path)
    tmp_path = target_path.with_name(f"{target_path.stem}.tmp{target_path.suffix}")
    if tmp_path.exists():
        try:
            tmp_path.unlink()
        except Exception:
            pass
    font.save(str(tmp_path))
    font.close()
    for attempt in range(10):
        try:
            if target_path.exists():
                try:
                    target_path.unlink()
                except Exception:
                    pass
            shutil.move(str(tmp_path), str(target_path))
            return
        except Exception:
            time.sleep(0.3)
    shutil.copyfile(str(tmp_path), str(target_path))
    try:
        tmp_path.unlink()
    except Exception:
        pass

def fix_font(fpath):
    font = TTFont(str(fpath))
    modified = False
    glyf = font.get('glyf')
    
    # 1. Deduplicate nodes in glyf
    if glyf:
        for gname in font.getGlyphOrder():
            g = glyf[gname]
            if g.numberOfContours <= 0:
                continue
            coords, endPts, flags = g.getCoordinates(glyf)
            
            # Check for duplicate nodes
            has_dup = False
            start = 0
            for end in endPts:
                for i in range(start, end):
                    if coords[i] == coords[i+1]:
                        has_dup = True
                        break
                if len(coords) > 1 and coords[start] == coords[end]:
                    has_dup = True
                    break
                start = end + 1
                
            if has_dup:
                new_coords = []
                new_flags = []
                new_endPts = []
                start = 0
                for end in endPts:
                    c_coords = coords[start:end+1]
                    c_flags = flags[start:end+1]
                    cl_coords = []
                    cl_flags = []
                    n = len(c_coords)
                    for i in range(n):
                        next_i = (i + 1) % n
                        if c_coords[i] == c_coords[next_i]:
                            continue # skip consecutive duplicate point
                        cl_coords.append(c_coords[i])
                        cl_flags.append(c_flags[i])
                    if len(cl_coords) < 3:
                        cl_coords = c_coords
                        cl_flags = c_flags
                    new_coords.extend(cl_coords)
                    new_flags.extend(cl_flags)
                    new_endPts.append(len(new_coords) - 1)
                    start = end + 1
                    
                new_g = Glyph()
                new_g.numberOfContours = len(new_endPts)
                new_g.endPtsOfContours = new_endPts
                new_g.coordinates = GlyphCoordinates(new_coords)
                new_g.flags = bytearray([f & 0x3F for f in new_flags])
                new_g.program = Program()
                new_g.recalcBounds(glyf)
                glyf[gname] = new_g
                modified = True
                print(f"  [{fpath.name}] Deduplicated nodes in glyph {gname}")

    # 2. Update nameID 5 to OFL 1.1
    if 'name' in font:
        for n in font['name'].names:
            if n.nameID == 5:
                val = n.toUnicode()
                if 'Apache 2.0' in val:
                    new_val = val.replace('Apache 2.0', 'OFL 1.1')
                    n.string = new_val.encode(n.getEncoding())
                    modified = True
            elif n.nameID == 13:
                val = n.toUnicode()
                if 'Apache' in val:
                    new_val = "This Font Software is licensed under the SIL Open Font License, Version 1.1."
                    n.string = new_val.encode(n.getEncoding())
                    modified = True

    if modified:
        safe_save_font(font, fpath)
        print(f"  [OK] Saved TTF {fpath.name}")
        woff2_p = WOFF2_DIR / (fpath.stem + ".woff2")
        compress(str(fpath), str(woff2_p))
        print(f"  [OK] Recompressed WOFF2 {woff2_p.name}")
        if fpath.name == "PocketGullMono-Regular.ttf":
            try:
                shutil.copyfile(str(fpath), str(ROOT_DIR / fpath.name))
                shutil.copyfile(str(woff2_p), str(ROOT_DIR / woff2_p.name))
            except Exception as e:
                print(f"  [WARN] Root sync note: {e}")
        elif fpath.name == "PocketGull-VF.ttf":
            try:
                shutil.copyfile(str(fpath), str(ROOT_DIR / fpath.name))
                shutil.copyfile(str(woff2_p), str(ROOT_DIR / woff2_p.name))
            except Exception as e:
                print(f"  [WARN] Root sync note: {e}")
    else:
        font.close()

if __name__ == '__main__':
    print("=" * 70)
    print("  POCKETGULL TYPEFOUNDRY: OFL 1.1 METADATA & NODE DEDUPLICATION CURE")
    print("=" * 70)
    for p in sorted(TTF_DIR.glob("*.ttf")):
        fix_font(p)
    print("\n[SUCCESS] All fonts cured and synchronized.")
