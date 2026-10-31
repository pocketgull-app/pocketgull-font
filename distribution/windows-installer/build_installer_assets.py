"""
Build bespoke PocketGull brand assets and Inno Setup (.iss) script for Windows / WinGet.
Uses actual PocketGull TTF fonts and Origami Gull emblem to render:
  - wizard-banner.bmp (328x604 @ 200% DPI)
  - wizard-small.bmp  (110x110 @ 200% DPI)
  - pocketgull.ico    (Multi-size Windows Icon)
  - specimen-info.rtf (Styled RTF Clinical Specimen Proof)
  - PocketGullFont.iss (Inno Setup 6 script installing all superfamily TTFs)
"""

import os
import zipfile
from pathlib import Path
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
STAGE_TTF_DIR = OUT_DIR / "stage_ttf"
ASSETS_DIR = OUT_DIR / "assets"


def extract_release_ttfs() -> list[tuple[str, str]]:
    """Copy canonical TTFs from fonts/ttf/ (with patched ISMP glyphs) and deduplicate by nameID=4."""
    import shutil
    if STAGE_TTF_DIR.exists():
        shutil.rmtree(STAGE_TTF_DIR)
    STAGE_TTF_DIR.mkdir(parents=True, exist_ok=True)
    ttf_dir = ROOT / "fonts" / "ttf"
    font_entries: list[tuple[str, str]] = []
    seen_full_names: set[str] = set()

    # Skip redundant alias filenames that duplicate another TTF's exact nameID=4
    skip_files = {
        "PocketGullSerif[wght].ttf",
        "PocketGull-Soft.ttf",
        "PocketGull-Sign-VF.ttf",
    }

    for src_path in sorted(ttf_dir.glob("*.ttf")):
        filename = src_path.name
        if filename in skip_files:
            continue

        tt = TTFont(str(src_path))
        full_name = filename[:-4]
        for rec in tt["name"].names:
            if rec.nameID == 4 and rec.platformID in (3, 1):
                try:
                    decoded = rec.toUnicode().strip()
                    if decoded:
                        full_name = decoded
                        break
                except Exception:
                    pass

        if full_name in seen_full_names:
            continue
        seen_full_names.add(full_name)

        target_path = STAGE_TTF_DIR / filename
        shutil.copy2(src_path, target_path)
        font_entries.append((filename, full_name))

    return font_entries


def make_banner_specimen_font(base_bold_path: Path) -> str:
    """Create a temporary font where U+0030 ('0'), U+006C ('l'), and U+005A ('Z') map to their ISMP disambiguated glyphs."""
    tt = TTFont(str(base_bold_path))
    gsub = tt["GSUB"].table
    var_map = {}
    for frec in gsub.FeatureList.FeatureRecord:
        if frec.FeatureTag in ("zero", "cv08", "cv05", "cv11"):
            for lidx in frec.Feature.LookupListIndex:
                for st in gsub.LookupList.Lookup[lidx].SubTable:
                    var_map.update(getattr(st, "mapping", {}))

    for table in tt["cmap"].tables:
        if 0x0030 in table.cmap and "zero" in var_map:
            table.cmap[0x0030] = var_map["zero"]
        if 0x006C in table.cmap and "l" in var_map:
            table.cmap[0x006C] = var_map["l"]
        if 0x005A in table.cmap and "Z" in var_map:
            table.cmap[0x005A] = var_map["Z"]

    out_path = ASSETS_DIR / "_banner_ismp_bold.ttf"
    tt.save(str(out_path))
    return str(out_path)


def render_brand_assets() -> None:
    """Render PocketGull Washi & Clinical Sanctuary branded BMPs, ICO, and preview PNG."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    icon_src = Image.open(ASSETS_DIR / "origami-gull-512.png").convert("RGBA")

    # 1. Save multi-resolution Windows .ico
    ico_path = ASSETS_DIR / "pocketgull.ico"
    icon_src.save(
        ico_path,
        format="ICO",
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)],
    )

    # Load actual PocketGull fonts for authentic typography
    f_bold_path = str(STAGE_TTF_DIR / "PocketGull-Bold.ttf")
    f_ismp_bold_path = make_banner_specimen_font(STAGE_TTF_DIR / "PocketGull-Bold.ttf")
    f_serif_path = str(STAGE_TTF_DIR / "PocketGull-Serif-Regular.ttf")
    f_mono_path = str(STAGE_TTF_DIR / "PocketGullMono-Regular.ttf")

    font_title = ImageFont.truetype(f_bold_path, 30)
    font_sub = ImageFont.truetype(f_serif_path, 15)
    font_specimen_lg = ImageFont.truetype(f_ismp_bold_path, 22)
    font_mono = ImageFont.truetype(f_mono_path, 13)
    font_mono_sm = ImageFont.truetype(f_mono_path, 11)

    # 2. Render Wizard Sidebar Banner (328 x 604)
    W, H = 328, 604
    banner = Image.new("RGB", (W, H), (20, 25, 35))  # Deep Slate #141923
    draw = ImageDraw.Draw(banner)

    # Subtle vertical gradient + geometric grid
    for y in range(H):
        r = int(18 + (y / H) * 10)
        g = int(23 + (y / H) * 12)
        b = int(33 + (y / H) * 16)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    grid_color = (28, 36, 50)
    for gx in range(0, W, 24):
        draw.line([(gx, 0), (gx, H)], fill=grid_color, width=1)
    for gy in range(0, H, 24):
        draw.line([(0, gy), (W, gy)], fill=grid_color, width=1)

    # Top Washi Apricot & Clinical Teal Accent Bars
    draw.rectangle([0, 0, W, 6], fill=(254, 186, 148))   # #FEBA94 Origami Gull Apricot
    draw.rectangle([0, 6, W, 10], fill=(15, 118, 110))   # #0F766E Clinical Teal
    # Left architectural spine line
    draw.rectangle([24, 34, 27, H - 34], fill=(15, 118, 110))

    # Composite Origami Gull Emblem (116x116)
    emblem_size = 116
    emblem = icon_src.resize((emblem_size, emblem_size), Image.Resampling.LANCZOS)
    banner.paste(emblem, (44, 42), emblem)

    # Brand Title & Header
    draw.text((44, 178), "POCKETGULL", font=font_title, fill=(250, 248, 242))  # #FAF8F2 Washi Cream
    draw.text((44, 216), "Clinical & Scientific Typeface", font=font_sub, fill=(254, 186, 148))

    # Divider rule
    draw.line([(44, 252), (W - 28, 252)], fill=(55, 68, 88), width=1)

    # Specimen Card Box (Dark Slate Card)
    draw.rounded_rectangle(
        [44, 268, W - 24, 412],
        radius=10,
        fill=(14, 18, 26),
        outline=(45, 58, 76),
        width=1,
    )
    draw.text((58, 280), "CHARACTER DISAMBIGUATION", font=font_mono_sm, fill=(20, 184, 166))
    draw.text((58, 302), "0O  1lI  5S  8B  Z2", font=font_specimen_lg, fill=(250, 248, 242))
    draw.text((58, 336), "Aa Bb Cc Dd Ee Ff Gg", font=font_sub, fill=(229, 223, 211))
    draw.text((58, 363), "120/80 mmHg  |  500 mg", font=font_mono, fill=(254, 186, 148))
    draw.text((58, 386), "Open Counters  |  Clear Terminals", font=font_mono_sm, fill=(148, 163, 184))

    # Superfamily Families
    pillars = [
        "Sans, Serif, Slab & Rounded",
        "Fixed-Width Monospace",
        "Mathematics & Sciences",
        "Braille & Sign Language",
    ]
    py = 432
    for text in pillars:
        draw.ellipse([44, py + 6, 48, py + 10], fill=(20, 184, 166))
        draw.text((58, py), text, font=font_mono, fill=(229, 223, 211))
        py += 24

    # Footer Stamp & Version Badge
    draw.rounded_rectangle(
        [44, H - 64, 148, H - 36],
        radius=6,
        fill=(15, 118, 110),
    )
    draw.text((56, H - 57), "v3.1.0 OFL", font=font_mono, fill=(250, 248, 242))
    draw.text((158, H - 56), "font.pocketgull.app", font=font_mono_sm, fill=(148, 163, 184))

    banner_bmp = ASSETS_DIR / "wizard-banner.bmp"
    banner.save(banner_bmp, format="BMP")
    banner.save(ASSETS_DIR / "wizard-banner-preview.png", format="PNG")

    # 3. Render Wizard Small Header Stamp (110 x 110)
    SW, SH = 110, 110
    small = Image.new("RGB", (SW, SH), (250, 248, 242))  # Washi Cream #FAF8F2
    s_emblem = icon_src.resize((94, 94), Image.Resampling.LANCZOS)
    small.paste(s_emblem, (8, 8), s_emblem)
    small.save(ASSETS_DIR / "wizard-small.bmp", format="BMP")

    # 4. Render Horizontal 654 x 284 Banner (PNG & BMP)
    HW, HH = 654, 284
    hbanner = Image.new("RGB", (HW, HH), (20, 25, 35))
    hdraw = ImageDraw.Draw(hbanner)

    for y in range(HH):
        r = int(18 + (y / HH) * 10)
        g = int(23 + (y / HH) * 12)
        b = int(33 + (y / HH) * 16)
        hdraw.line([(0, y), (HW, y)], fill=(r, g, b))

    for gx in range(0, HW, 24):
        hdraw.line([(gx, 0), (gx, HH)], fill=grid_color, width=1)
    for gy in range(0, HH, 24):
        hdraw.line([(0, gy), (HW, gy)], fill=grid_color, width=1)

    # Top accent bars & left vertical spine
    hdraw.rectangle([0, 0, HW, 5], fill=(254, 186, 148))
    hdraw.rectangle([0, 5, HW, 8], fill=(15, 118, 110))
    hdraw.rectangle([20, 26, 23, HH - 22], fill=(15, 118, 110))

    # Left Column: Emblem + Title + Pillars + Version Stamp
    h_emblem = icon_src.resize((68, 68), Image.Resampling.LANCZOS)
    hbanner.paste(h_emblem, (38, 26), h_emblem)

    font_title_h = ImageFont.truetype(f_bold_path, 26)
    font_sub_h = ImageFont.truetype(f_serif_path, 14)
    font_spec_h = ImageFont.truetype(f_ismp_bold_path, 23)

    hdraw.text((118, 28), "POCKETGULL", font=font_title_h, fill=(250, 248, 242))
    hdraw.text((118, 62), "Clinical & Scientific Typeface", font=font_sub_h, fill=(254, 186, 148))

    hdraw.line([(38, 108), (314, 108)], fill=(55, 68, 88), width=1)

    hpy = 122
    for text in pillars:
        hdraw.ellipse([38, hpy + 6, 42, hpy + 10], fill=(20, 184, 166))
        hdraw.text((52, hpy), text, font=font_mono, fill=(229, 223, 211))
        hpy += 23

    hdraw.rounded_rectangle([38, HH - 50, 142, HH - 22], radius=6, fill=(15, 118, 110))
    hdraw.text((50, HH - 43), "v3.1.0 OFL", font=font_mono, fill=(250, 248, 242))
    hdraw.text((152, HH - 42), "font.pocketgull.app", font=font_mono_sm, fill=(148, 163, 184))

    # Right Column: Specimen Card Box
    hdraw.rounded_rectangle(
        [334, 26, HW - 20, HH - 22],
        radius=10,
        fill=(14, 18, 26),
        outline=(45, 58, 76),
        width=1,
    )
    hdraw.text((352, 40), "CHARACTER DISAMBIGUATION", font=font_mono_sm, fill=(20, 184, 166))
    hdraw.text((352, 64), "0O  1lI  5S  8B  Z2", font=font_spec_h, fill=(250, 248, 242))
    hdraw.text((352, 104), "Aa Bb Cc Dd Ee Ff Gg", font=font_sub, fill=(229, 223, 211))
    hdraw.text((352, 134), "120/80 mmHg  |  500 mg", font=font_mono, fill=(254, 186, 148))
    hdraw.line([(352, 166), (HW - 38, 166)], fill=(36, 46, 62), width=1)
    hdraw.text((352, 180), "b/d   p/q   n/u   m/w", font=font_mono, fill=(229, 223, 211))
    hdraw.text((352, 212), "Open Counters  |  Clear Terminals", font=font_mono_sm, fill=(148, 163, 184))

    hbanner.save(ASSETS_DIR / "pocketgull-banner-654x284.png", format="PNG")
    hbanner.save(ASSETS_DIR / "pocketgull-banner-654x284.bmp", format="BMP")

    # 5. Render NSIS MUI2 Welcome Sidebar (164 x 314) & Header (150 x 57) BMPs
    nsis_welcome = banner.resize((164, 314), Image.Resampling.LANCZOS)
    nsis_welcome.save(ASSETS_DIR / "nsis-welcome.bmp", format="BMP")

    NW, NH = 150, 57
    nsis_hdr = Image.new("RGB", (NW, NH), (20, 25, 35))
    nh_draw = ImageDraw.Draw(nsis_hdr)
    nh_draw.rectangle([0, 0, NW, 3], fill=(254, 186, 148))
    nh_draw.rectangle([0, 3, NW, 5], fill=(15, 118, 110))
    nh_emblem = icon_src.resize((40, 40), Image.Resampling.LANCZOS)
    nsis_hdr.paste(nh_emblem, (10, 11), nh_emblem)
    font_nh = ImageFont.truetype(f_bold_path, 13)
    font_nh_sub = ImageFont.truetype(f_mono_path, 9)
    nh_draw.text((56, 15), "POCKETGULL", font=font_nh, fill=(250, 248, 242))
    nh_draw.text((56, 33), "v3.1.0 OFL", font=font_nh_sub, fill=(20, 184, 166))
    nsis_hdr.save(ASSETS_DIR / "nsis-header.bmp", format="BMP")


def write_specimen_rtf(font_count: int) -> None:
    """Write a clean, restrained RTF overview sheet for interactive installations."""
    rtf = (
        r"{\rtf1\ansi\deff0"
        r"{\fonttbl{\f0\fswiss\fcharset0 Segoe UI;}{\f1\fmodern\fcharset0 Consolas;}}"
        r"{\colortbl;\red15\green118\blue110;\red24\green24\blue27;\red180\green83\blue9;}"
        r"\viewkind4\uc1\pard\cf1\b\f0\fs24 PocketGull Typeface Superfamily (v3.1.0)\par"
        r"\cf2\b0\fs18 Sans, Serif, Slab, Monospace, and Technical Fonts\par"
        r"\pard\sa120\sl276\slmult1\cf2\fs18\par"
        r"Designed by \b Phil Gear\b0  (\i The PocketGull Project Authors\i0 ). PocketGull is an open-source typeface "
        r"family engineered for clinical interfaces, scientific publishing, and high-legibility technical documentation, "
        r"with explicit character disambiguation (\b 0/O\b0 , \b 1/l/I\b0 , \b Z/2\b0 , \b b/d\b0 , \b p/q\b0 ).\par"
        r"\cf1\b Included in this package (" + str(font_count) + r" TrueType fonts):\b0\cf2\par"
        r"\f1\fs16  - PocketGull Sans (Regular, Italic, Bold, BoldItalic, Black, Condensed)\par"
        r" - PocketGull Display (Fineliner, Chiseltip, MarkerRaw, Halftone, Inline, Outline, Micro)\par"
        r" - PocketGull Serif, Slab & Soft (Regular, Bold, Variable Fonts)\par"
        r" - PocketGull Mono (Regular, Italic, Bold Fixed-Width Monospace)\par"
        r" - PocketGull Technical & Accessibility (Math, Chem, Lab, Genome, Algo, Music, Numerics, Learn, Sign, ASL)\par"
        r"\pard\sa120\sl276\slmult1\f0\fs18\par"
        r"\cf3\b License:\b0\cf2  SIL Open Font License 1.1 (OFL-1.1) \emdash  Free for commercial, clinical, academic, and personal use.\par"
        r"}"
    )
    (ASSETS_DIR / "specimen-info.rtf").write_text(rtf, encoding="ascii")


def write_inno_script(font_entries: list[tuple[str, str]]) -> Path:
    """Generate the Inno Setup 6 script (.iss)."""
    lines = [
        "; PocketGull Font Superfamily v3.1.0 — Official Windows & WinGet Installer",
        "[Setup]",
        "AppId={{8D692F2F-D44B-451D-A62F-E95528567C5F}",
        "AppName=PocketGull Font",
        "AppVersion=3.1.0",
        "AppVerName=PocketGull Font 3.1.0",
        "AppPublisher=The PocketGull Project Authors",
        "AppPublisherURL=https://font.pocketgull.app",
        "AppSupportURL=https://github.com/pocketgull-app/pocketgull-font/issues",
        "AppUpdatesURL=https://github.com/pocketgull-app/pocketgull-font/releases",
        "VersionInfoVersion=3.1.0.0",
        "VersionInfoCompany=The PocketGull Project Authors",
        "VersionInfoDescription=PocketGull Clinical & Scientific Typeface Installer",
        "VersionInfoCopyright=Copyright (c) 2026 The PocketGull Project Authors (OFL-1.1)",
        "DefaultDirName={autopf}\\PocketGull Font",
        "DisableDirPage=yes",
        "DisableProgramGroupPage=yes",
        "PrivilegesRequired=admin",
        "PrivilegesRequiredOverridesAllowed=dialog commandline",
        "OutputDir=dist",
        "OutputBaseFilename=PocketGull-Font-Setup-v3.1.0",
        "Compression=lzma2/ultra64",
        "SolidCompression=yes",
        "WizardStyle=modern",
        "WizardImageFile=assets\\wizard-banner.bmp",
        "WizardSmallImageFile=assets\\wizard-small.bmp",
        "SetupIconFile=assets\\pocketgull.ico",
        "UninstallDisplayIcon={app}\\pocketgull.ico",
        "UninstallDisplayName=PocketGull Font",
        "LicenseFile=..\\..\\OFL.txt",
        "InfoBeforeFile=assets\\specimen-info.rtf",
        "ArchitecturesInstallIn64BitMode=x64compatible",
        "",
        "[Languages]",
        'Name: "english"; MessagesFile: "compiler:Default.isl"',
        "",
        "[Files]",
        'Source: "assets\\pocketgull.ico"; DestDir: "{app}"; Flags: ignoreversion',
        'Source: "..\\..\\OFL.txt"; DestDir: "{app}"; Flags: ignoreversion',
        'Source: "..\\..\\README.md"; DestDir: "{app}"; Flags: ignoreversion',
    ]

    for filename, full_name in font_entries:
        lines.append(
            f'Source: "stage_ttf\\{filename}"; DestDir: "{{autofonts}}"; '
            f'FontInstall: "{full_name}"; Flags: ignoreversion restartreplace'
        )

    iss_path = OUT_DIR / "PocketGullFont.iss"
    iss_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return iss_path


def write_nsis_script(font_entries: list[tuple[str, str]]) -> Path:
    """Generate the open-source NSIS (Nullsoft) installer script (.nsi)."""
    DIST_DIR = OUT_DIR / "dist"
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    count = len(font_entries)

    lines = [
        "; PocketGull Font Superfamily v3.1.0 — Open-Source NSIS Installer (zlib/libpng license)",
        '!include "MUI2.nsh"',
        '!include "WinMessages.nsh"',
        "",
        'Name "PocketGull Font"',
        'OutFile "dist\\PocketGull-Font-Setup-v3.1.0.exe"',
        "Unicode True",
        "SetCompressor /SOLID lzma",
        'InstallDir "$PROGRAMFILES64\\PocketGull Font"',
        "RequestExecutionLevel admin",
        "BrandingText \"PocketGull Typeface v3.1.0 (SIL OFL-1.1)\"",
        "",
        'VIProductVersion "3.1.0.0"',
        'VIAddVersionKey "ProductName" "PocketGull Font"',
        'VIAddVersionKey "CompanyName" "The PocketGull Project Authors"',
        'VIAddVersionKey "FileDescription" "PocketGull Clinical & Scientific Typeface Installer"',
        'VIAddVersionKey "FileVersion" "3.1.0.0"',
        'VIAddVersionKey "ProductVersion" "3.1.0"',
        'VIAddVersionKey "LegalCopyright" "Copyright (c) 2026 The PocketGull Project Authors (OFL-1.1)"',
        "",
        '!define MUI_ICON "assets\\pocketgull.ico"',
        '!define MUI_UNICON "assets\\pocketgull.ico"',
        '!define MUI_WELCOMEFINISHPAGE_BITMAP "assets\\nsis-welcome.bmp"',
        '!define MUI_UNWELCOMEFINISHPAGE_BITMAP "assets\\nsis-welcome.bmp"',
        "!define MUI_HEADERIMAGE",
        '!define MUI_HEADERIMAGE_BITMAP "assets\\nsis-header.bmp"',
        "!define MUI_HEADERIMAGE_RIGHT",
        "",
        '!define MUI_WELCOMEPAGE_TITLE "PocketGull Typeface Superfamily (v3.1.0)"',
        (
            f'!define MUI_WELCOMEPAGE_TEXT "This package installs {count} PocketGull TrueType fonts '
            "(Sans, Serif, Slab, Rounded, Fixed-Width Monospace, Mathematics, Sciences, Braille, and Sign Language) "
            "to your Windows Fonts folder.$\\r$\\n$\\r$\\n"
            "Designed by Phil Gear (The PocketGull Project Authors) with explicit character disambiguation "
            "(0/O, 1/l/I, Z/2, b/d, p/q).$\\r$\\n$\\r$\\n"
            "License: SIL Open Font License 1.1 (OFL-1.1).$\\r$\\n$\\r$\\n"
            'Click Install to register the fonts on your system."'
        ),
        "!define MUI_PAGE_CUSTOMFUNCTION_SHOW WelcomeChangeNextToInstall",
        "!insertmacro MUI_PAGE_WELCOME",
        "!insertmacro MUI_PAGE_INSTFILES",
        "!insertmacro MUI_PAGE_FINISH",
        "",
        "!insertmacro MUI_UNPAGE_CONFIRM",
        "!insertmacro MUI_UNPAGE_INSTFILES",
        "",
        '!insertmacro MUI_LANGUAGE "English"',
        "",
        "Function WelcomeChangeNextToInstall",
        "  GetDlgItem $0 $HWNDPARENT 1",
        '  SendMessage $0 ${WM_SETTEXT} 0 "STR:&Install"',
        "FunctionEnd",
        "",
        'Section "Install" SecMain',
        "  SetRegView 64",
        '  SetOutPath "$INSTDIR"',
        "  SetOverwrite try",
        '  File "assets\\pocketgull.ico"',
        '  File "..\\..\\OFL.txt"',
        '  File "..\\..\\README.md"',
        "",
        '  SetOutPath "$FONTS"',
    ]

    for filename, full_name in font_entries:
        lines.extend([
            f'  File "stage_ttf\\{filename}"',
            f'  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" "{full_name} (TrueType)" "{filename}"',
        ])

    lines.extend([
        "",
        '  WriteUninstaller "$INSTDIR\\Uninstall.exe"',
        '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "DisplayName" "PocketGull Font"',
        '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "DisplayVersion" "3.1.0"',
        '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "Publisher" "The PocketGull Project Authors"',
        '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "URLInfoAbout" "https://font.pocketgull.app"',
        '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "DisplayIcon" "$INSTDIR\\pocketgull.ico"',
        '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "InstallLocation" "$INSTDIR"',
        '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "UninstallString" "$\\"$INSTDIR\\Uninstall.exe$\\""',
        '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "QuietUninstallString" "$\\"$INSTDIR\\Uninstall.exe$\\" /S"',
        '  WriteRegDWORD HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "NoModify" 1',
        '  WriteRegDWORD HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "NoRepair" 1',
        "  SetErrorLevel 0",
        "SectionEnd",
        "",
        'Section "Uninstall"',
        "  SetRegView 64",
    ])

    for filename, full_name in font_entries:
        lines.extend([
            f'  DeleteRegValue HKLM "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" "{full_name} (TrueType)"',
            f'  Delete /REBOOTOK "$FONTS\\{filename}"',
        ])

    lines.extend([
        '  Delete "$INSTDIR\\pocketgull.ico"',
        '  Delete "$INSTDIR\\OFL.txt"',
        '  Delete "$INSTDIR\\README.md"',
        '  Delete "$INSTDIR\\Uninstall.exe"',
        '  RMDir "$INSTDIR"',
        '  DeleteRegKey HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font"',
        "  SetErrorLevel 0",
        "SectionEnd",
    ])

    nsi_path = OUT_DIR / "PocketGullFont.nsi"
    nsi_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return nsi_path


if __name__ == "__main__":
    entries = extract_release_ttfs()
    render_brand_assets()
    write_specimen_rtf(len(entries))
    iss_file = write_inno_script(entries)
    nsi_file = write_nsis_script(entries)
    print(f"Prepared {len(entries)} TTF fonts, Inno script ({iss_file.name}), and NSIS script ({nsi_file.name})")
