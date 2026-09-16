import os
import sys
import shutil
import hashlib
import winreg
import ctypes
from ctypes import wintypes
from pathlib import Path
from fontTools.ttLib import TTFont

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SOURCE_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface\fonts\ttf")
DEST_DIR = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts"

user32 = ctypes.WinDLL('user32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

HWND_BROADCAST = 0xFFFF
WM_FONTCHANGE = 0x001D
SMTO_ABORTIFHUNG = 0x0002

def file_hash(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def install_all_fonts():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    ttf_files = sorted(SOURCE_DIR.glob("*.ttf"))
    print(f"Found {len(ttf_files)} TTF fonts in {SOURCE_DIR}")
    
    installed_count = 0
    updated_count = 0
    skipped_count = 0
    
    registry_entries = []
    
    for src in ttf_files:
        dst = DEST_DIR / src.name
        needs_copy = True
        
        if dst.exists():
            src_hash = file_hash(src)
            try:
                dst_hash = file_hash(dst)
                if src_hash == dst_hash:
                    needs_copy = False
                    skipped_count += 1
            except Exception:
                needs_copy = True
                
        if needs_copy:
            try:
                # Try direct copy
                shutil.copy2(src, dst)
                print(f"  [COPIED] {src.name} -> {dst.name}")
                if dst.exists():
                    updated_count += 1
                else:
                    installed_count += 1
            except PermissionError:
                # File is locked in Windows Terminal / font cache: rename & replace
                old_path = DEST_DIR / f"{src.stem}.old"
                if old_path.exists():
                    try:
                        old_path.unlink()
                    except Exception:
                        old_path = DEST_DIR / f"{src.stem}.{os.getpid()}.old"
                
                try:
                    os.rename(dst, old_path)
                    shutil.copy2(src, dst)
                    print(f"  [REPLACED-LOCKED] {src.name} (renamed old -> {old_path.name})")
                    updated_count += 1
                except Exception as ex:
                    print(f"  [ERROR] Failed to replace {src.name}: {ex}")
                    continue
        
        # Read font metadata for registry registration
        try:
            tt = TTFont(str(dst))
            name_table = tt['name']
            fam = name_table.getDebugName(1) or ""
            sub = name_table.getDebugName(2) or ""
            full = name_table.getDebugName(4) or ""
            ps = name_table.getDebugName(6) or ""
            
            # Primary registry name: "Full Name (TrueType)"
            reg_names = []
            if full:
                reg_names.append(f"{full} (TrueType)")
            if fam and sub and f"{fam} {sub} (TrueType)" not in reg_names:
                reg_names.append(f"{fam} {sub} (TrueType)")
            if fam and f"{fam} (TrueType)" not in reg_names:
                reg_names.append(f"{fam} (TrueType)")
                
            # Special case for Pocket Gull Mono variations
            if "Pocket Gull Mono" in fam or "PocketGull Mono" in fam or "PocketGullMono" in fam:
                for prefix in ["Pocket Gull Mono", "PocketGull Mono", "PocketGullMono"]:
                    alias = f"{prefix} {sub} (TrueType)".strip()
                    if alias not in reg_names:
                        reg_names.append(alias)
            
            for rname in reg_names:
                registry_entries.append((rname, str(dst)))
                
        except Exception as ex:
            print(f"  [WARN] Metadata read error for {dst.name}: {ex}")
            registry_entries.append((f"{src.stem} (TrueType)", str(dst)))
            
    print(f"\nSummary: {updated_count} updated, {installed_count} newly installed, {skipped_count} identical.")
    
    # Update HKCU Registry
    print("\nUpdating HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts...")
    reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Fonts")
    for name, path_val in registry_entries:
        winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, path_val)
    winreg.CloseKey(reg_key)
    print(f"Registered {len(registry_entries)} font name mappings in Windows Registry.")
    
    # Notify GDI & Windows system
    print("\nRegistering font resources via GDI AddFontResourceExW...")
    registered_resources = 0
    for src in ttf_files:
        dst = DEST_DIR / src.name
        if dst.exists():
            res = gdi32.AddFontResourceExW(str(dst), 0, 0)
            if res > 0:
                registered_resources += 1
    print(f"GDI registered {registered_resources} font resources.")
    
    # Broadcast WM_FONTCHANGE
    print("\nBroadcasting WM_FONTCHANGE to all Windows applications...")
    res_val = wintypes.DWORD()
    msg_res = user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_FONTCHANGE,
        0,
        0,
        SMTO_ABORTIFHUNG,
        2000,
        ctypes.byref(res_val)
    )
    print(f"WM_FONTCHANGE broadcast completed (result={msg_res}).")
    
    # Verify installed Mono font
    print("\n--- Verifying Installed PocketGullMono-Regular.ttf ---")
    mono_dst = DEST_DIR / "PocketGullMono-Regular.ttf"
    if mono_dst.exists():
        tt = TTFont(str(mono_dst))
        cmap = tt.getBestCmap()
        braille_sample = '⠠⠏⠕⠉⠅⠑⠞⠠⠛⠥⠇⠇'
        braille_missing = [f"U+{ord(c):04X}" for c in braille_sample if ord(c) not in cmap]
        print(f"Path: {mono_dst} ({mono_dst.stat().st_size:,} bytes)")
        print(f"Folder (U+1F4C1): {0x1F4C1 in cmap}")
        print(f"Stopwatch (U+23F1): {0x23F1 in cmap}")
        print(f"Git Branch (U+E0A0): {0xE0A0 in cmap}")
        print(f"Braille missing ({len(braille_missing)}): {braille_missing}")
        print(f"All Braille 256 present: {all(cp in cmap for cp in range(0x2800, 0x2900))}")

if __name__ == "__main__":
    install_all_fonts()
