#!/usr/bin/env python3
"""
PocketGull Typefoundry: Windows OS Font Installer & Cache Synchronizer
======================================================================
Installs all production TTF binaries into the Windows User Font Store:
- Destination: %LOCALAPPDATA%\Microsoft\Windows\Fonts
- Registry: HKCU\Software\Microsoft\Windows NT\CurrentVersion\Fonts
- GDI / DirectWrite Registration: AddFontResourceW
- System-Wide Broadcast: WM_FONTCHANGE via SendMessageTimeoutW
"""

import os
import sys
import shutil
import winreg
import ctypes
from pathlib import Path
from fontTools.ttLib import TTFont

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
USER_FONTS_DIR = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts"

def get_font_names(font_path: Path):
    font = TTFont(str(font_path))
    names = font["name"]
    full_name = None
    family = None
    subfamily = None

    for record in names.names:
        # Prefer Windows platform (3, 1) or Unicode (0, 3)
        if record.platformID in (3, 0):
            try:
                text = record.toUnicode()
            except Exception:
                continue
            if record.nameID == 4 and not full_name:
                full_name = text
            elif record.nameID == 1 and not family:
                family = text
            elif record.nameID == 2 and not subfamily:
                subfamily = text

    font.close()
    if not full_name and family and subfamily:
        full_name = f"{family} {subfamily}"
    return full_name or font_path.stem

def install_all():
    print("======================================================================")
    print("  POCKETGULL FOUNDRY: WINDOWS OS FONT INSTALLER (OCTOBER 2026)")
    print("======================================================================\n")

    USER_FONTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Target Directory: {USER_FONTS_DIR}")

    reg_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)

    installed = 0
    ttf_files = sorted(TTF_DIR.glob("*.ttf"))

    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    for src in ttf_files:
        full_name = get_font_names(src)
        reg_name = f"{full_name} (TrueType)"
        primary_dst = USER_FONTS_DIR / src.name
        versioned_dst = USER_FONTS_DIR / f"{src.stem}-v31.ttf"

        target_dst = None
        # First attempt: Try primary file
        try:
            # Attempt to unload existing resource first if present
            gdi32.RemoveFontResourceW(str(primary_dst))
            shutil.copy2(str(src), str(primary_dst))
            target_dst = primary_dst
        except PermissionError:
            # File is locked by fontdrvhost: use versioned destination
            try:
                gdi32.RemoveFontResourceW(str(versioned_dst))
                shutil.copy2(str(src), str(versioned_dst))
                target_dst = versioned_dst
            except Exception as e:
                print(f"  [FAIL] Could not copy {src.name} or {versioned_dst.name}: {e}")
                continue
        except Exception as e:
            print(f"  [WARN] Unexpected error for {src.name}: {e}")
            continue

        if not target_dst:
            continue

        # Register in HKCU Fonts
        try:
            winreg.SetValueEx(reg_key, reg_name, 0, winreg.REG_SZ, str(target_dst))
        except Exception as e:
            print(f"  [WARN] Registry write failed for {reg_name}: {e}")

        # Register dynamically in current session
        gdi32.AddFontResourceW(str(target_dst))
        print(f"  • Installed: {reg_name} -> {target_dst.name}")
        installed += 1

    winreg.CloseKey(reg_key)

    # Broadcast WM_FONTCHANGE to all top-level windows
    print("\nBroadcasting WM_FONTCHANGE across Windows desktop & DirectWrite...")
    HWND_BROADCAST = 0xFFFF
    WM_FONTCHANGE = 0x001D
    SMTO_ABORTIFHUNG = 0x0002
    result = ctypes.c_ulong()
    user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_FONTCHANGE,
        0,
        0,
        SMTO_ABORTIFHUNG,
        2000,
        ctypes.byref(result)
    )

    print(f"\n[SUCCESS] Successfully installed and activated {installed} fonts in Windows OS!\n")

if __name__ == "__main__":
    install_all()
