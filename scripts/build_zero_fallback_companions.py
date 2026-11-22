#!/usr/bin/env python3
"""
Build the complete 52-script self-hosted, air-gapped, SIL OFL 1.1 zero-fallback
WOFF2 companion suite for PocketGull SMoE Experts.

Enforces PocketGull binary safety invariants:
  - Authentic GSUB/GPOS shaping tables preserved
  - TrueType bytecode VM stripped (fpgm, prep, cvt removed -> 0 bytes)
  - 2-byte word alignment (loca[i] % 2 == 0) via fontTools save
  - Brotli Q11 WOFF2 compression
  - Explicit SIL OFL 1.1 attribution preserved in name table
"""
import os
import sys
import urllib.request
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

UPSTREAM_DIR = "sources/clean_upstream"
OUT_DIR = "fonts/woff2/companions"
os.makedirs(UPSTREAM_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# Pinned immutable commit SHA on github.com/google/fonts (zero floating raw/main)
GF_COMMIT_SHA = "06bfe0d62a98375cb09c942fa18e68bd32cff057"
GF_OFL = f"https://github.com/google/fonts/raw/{GF_COMMIT_SHA}/ofl"

# Executable / VM / unsafe tables strictly stripped from every companion
BANNED_TABLES = ("fpgm", "prep", "cvt ", "Wasm", "Silf", "Glat", "Gloc", "Feat", "Sill", "DSIG", "meta")

# Non-shaping scripts where GSUB is stripped to prevent lookup-bomb DoS
NO_GSUB_SCRIPTS = {
    "PocketGull-Osage-Companion.woff2",
    "PocketGull-Ogham-Companion.woff2",
    "PocketGull-OldTurkic-Companion.woff2",
    "PocketGull-EgyptianHieroglyphs-Companion.woff2",
    "PocketGull-AnatolianHieroglyphs-Companion.woff2",
    "PocketGull-Armenian-Companion.woff2",
    "PocketGull-Georgian-Companion.woff2",
    "PocketGull-Coptic-Companion.woff2",
    "PocketGull-Runic-Companion.woff2",
    "PocketGull-Phoenician-Companion.woff2",
    "PocketGull-LinearB-Companion.woff2",
    "PocketGull-Gothic-Companion.woff2",
    "PocketGull-Glagolitic-Companion.woff2",
    "PocketGull-Deseret-Companion.woff2",
    "PocketGull-Lisu-Companion.woff2",
    "PocketGull-Yi-Companion.woff2",
    "PocketGull-Osmanya-Companion.woff2",
    "PocketGull-Korean-Companion.woff2",
}

# Each entry: (folder_or_None, local_filename_candidates, out_woff2, unicode_ranges)
COMPANIONS = [
    # --- Semitic & RTL ---
    ("notosansarabic", ["NotoSansArabic[wdth,wght].ttf"], "PocketGull-Arabic-Companion.woff2", "U+0600-06FF,U+0750-077F,U+08A0-08FF,U+FB50-FDFF,U+FE70-FEFF,U+200C-200F"),
    ("notosanshebrew", ["NotoSansHebrew[wdth,wght].ttf"], "PocketGull-Hebrew-Companion.woff2", "U+0590-05FF,U+FB1D-FB4F"),
    ("notosanssyriac", ["NotoSansSyriac-Regular.ttf", "NotoSansSyriac[wght].ttf"], "PocketGull-Syriac-Companion.woff2", "U+0700-074F"),
    ("notosansthaana", ["NotoSansThaana-Regular.ttf", "NotoSansThaana[wght].ttf"], "PocketGull-Thaana-Companion.woff2", "U+0780-07BF"),
    # --- National Scripts (Armenian, Georgian) ---
    ("notosansarmenian", ["NotoSansArmenian[wdth,wght].ttf", "NotoSansArmenian[wght].ttf", "NotoSansArmenian-Regular.ttf"], "PocketGull-Armenian-Companion.woff2", "U+0530-058F,U+FB13-FB17"),
    ("notosansgeorgian", ["NotoSansGeorgian[wdth,wght].ttf", "NotoSansGeorgian[wght].ttf", "NotoSansGeorgian-Regular.ttf"], "PocketGull-Georgian-Companion.woff2", "U+10A0-10FF,U+1C90-1CBF,U+2D00-2D2F"),
    # --- Deaf SignWriting ---
    ("notosanssignwriting", ["NotoSansSignWriting-Regular.ttf"], "PocketGull-SignWriting-Companion.woff2", "U+1D800-1DAAF"),
    # --- Indigenous & Sovereign Alphabets ---
    ("notosansosage", ["NotoSansOsage-Regular.ttf"], "PocketGull-Osage-Companion.woff2", "U+104B0-104FB,U+0300-036F"),
    ("notosansnko", ["NotoSansNKo-Regular.ttf"], "PocketGull-NKo-Companion.woff2", "U+07C0-07FF,U+200C-200F"),
    ("notosansbassavah", ["NotoSansBassaVah[wght].ttf", "NotoSansBassaVah-Regular.ttf"], "PocketGull-BassaVah-Companion.woff2", "U+16AD0-16AFF"),
    ("notosansmongolian", ["NotoSansMongolian-Regular.ttf"], "PocketGull-Mongolian-Companion.woff2", "U+1800-18AF,U+11660-1167F,U+200C-200F"),
    ("notosansogham", ["NotoSansOgham-Regular.ttf"], "PocketGull-Ogham-Companion.woff2", "U+1680-169F"),
    ("notosansoldturkic", ["NotoSansOldTurkic-Regular.ttf"], "PocketGull-OldTurkic-Companion.woff2", "U+10C00-10C4F"),
    # --- South Asian / Indic (10 scripts) ---
    ("notosansdevanagari", ["NotoSansDevanagari[wdth,wght].ttf"], "PocketGull-Devanagari-Companion.woff2", "U+0900-097F,U+A8E0-A8FF,U+200C-200D"),
    ("notosansbengali", ["NotoSansBengali[wdth,wght].ttf"], "PocketGull-Bengali-Companion.woff2", "U+0980-09FF,U+200C-200D"),
    ("notosansgurmukhi", ["NotoSansGurmukhi[wdth,wght].ttf"], "PocketGull-Gurmukhi-Companion.woff2", "U+0A00-0A7F,U+200C-200D"),
    ("notosansgujarati", ["NotoSansGujarati[wdth,wght].ttf"], "PocketGull-Gujarati-Companion.woff2", "U+0A80-0AFF,U+200C-200D"),
    ("notosansoriya", ["NotoSansOriya[wdth,wght].ttf"], "PocketGull-Oriya-Companion.woff2", "U+0B00-0B7F,U+200C-200D"),
    ("notosanstamil", ["NotoSansTamil[wdth,wght].ttf"], "PocketGull-Tamil-Companion.woff2", "U+0B80-0BFF,U+200C-200D"),
    ("notosanstelugu", ["NotoSansTelugu[wdth,wght].ttf"], "PocketGull-Telugu-Companion.woff2", "U+0C00-0C7F,U+200C-200D"),
    ("notosanskannada", ["NotoSansKannada[wdth,wght].ttf"], "PocketGull-Kannada-Companion.woff2", "U+0C80-0CFF,U+200C-200D"),
    ("notosansmalayalam", ["NotoSansMalayalam[wdth,wght].ttf"], "PocketGull-Malayalam-Companion.woff2", "U+0D00-0D7F,U+200C-200D"),
    ("notosanssinhala", ["NotoSansSinhala[wdth,wght].ttf"], "PocketGull-Sinhala-Companion.woff2", "U+0D80-0DFF,U+200C-200D"),
    # --- Southeast Asian & Tibetan (5 scripts) ---
    ("notosansthai", ["NotoSansThai[wdth,wght].ttf"], "PocketGull-Thai-Companion.woff2", "U+0E00-0E7F"),
    ("notosanslao", ["NotoSansLao[wdth,wght].ttf"], "PocketGull-Lao-Companion.woff2", "U+0E80-0EFF"),
    ("notoseriftibetan", ["NotoSerifTibetan[wght].ttf"], "PocketGull-Tibetan-Companion.woff2", "U+0F00-0FFF"),
    ("notosansmyanmar", ["NotoSansMyanmar[wdth,wght].ttf", "NotoSansMyanmar-Regular.ttf"], "PocketGull-Myanmar-Companion.woff2", "U+1000-109F,U+AA60-AA7F,U+200C-200D"),
    ("notosanskhmer", ["NotoSansKhmer[wdth,wght].ttf"], "PocketGull-Khmer-Companion.woff2", "U+1780-17FF,U+19E0-19FF,U+200C-200D"),
    # --- Living Regional & Indigenous (13 scripts) ---
    ("notosansjavanese", ["NotoSansJavanese[wght].ttf", "NotoSansJavanese-Regular.ttf"], "PocketGull-Javanese-Companion.woff2", "U+A980-A9DF,U+200C-200D"),
    ("notosansbalinese", ["NotoSansBalinese[wght].ttf", "NotoSansBalinese-Regular.ttf"], "PocketGull-Balinese-Companion.woff2", "U+1B00-1B7F,U+200C-200D"),
    ("notosanssundanese", ["NotoSansSundanese[wght].ttf", "NotoSansSundanese-Regular.ttf"], "PocketGull-Sundanese-Companion.woff2", "U+1B80-1BBF,U+1CC0-1CCF"),
    ("notosanstagalog", ["NotoSansTagalog-Regular.ttf"], "PocketGull-Tagalog-Companion.woff2", "U+1700-171F"),
    ("notosansolchiki", ["NotoSansOlChiki[wght].ttf", "NotoSansOlChiki-Regular.ttf"], "PocketGull-OlChiki-Companion.woff2", "U+1C50-1C7F"),
    ("notosansmeeteimayek", ["NotoSansMeeteiMayek[wght].ttf", "NotoSansMeeteiMayek-Regular.ttf"], "PocketGull-MeeteiMayek-Companion.woff2", "U+ABC0-ABFF,U+AAE0-AAFF"),
    ("notosanschakma", ["NotoSansChakma-Regular.ttf"], "PocketGull-Chakma-Companion.woff2", "U+11100-1114F,U+200C-200D"),
    ("notosanshanifirohingya", ["NotoSansHanifiRohingya[wght].ttf", "NotoSansHanifiRohingya-Regular.ttf"], "PocketGull-HanifiRohingya-Companion.woff2", "U+10D00-10D3F,U+200C-200F"),
    ("notosansyi", ["NotoSansYi-Regular.ttf"], "PocketGull-Yi-Companion.woff2", "U+A000-A4CF"),
    ("notosanslisu", ["NotoSansLisu[wght].ttf", "NotoSansLisu-Regular.ttf"], "PocketGull-Lisu-Companion.woff2", "U+A4D0-A4FF"),
    ("notosansmiao", ["NotoSansMiao-Regular.ttf"], "PocketGull-Miao-Companion.woff2", "U+16F00-16F9F"),
    ("notosansbamum", ["NotoSansBamum[wght].ttf", "NotoSansBamum-Regular.ttf"], "PocketGull-Bamum-Companion.woff2", "U+A6A0-A6FF"),
    ("notosansosmanya", ["NotoSansOsmanya-Regular.ttf"], "PocketGull-Osmanya-Companion.woff2", "U+10480-104AF"),
    # --- Ancient Medical & Epigraphic (9 scripts) ---
    ("notosansegyptianhieroglyphs", ["NotoSansEgyptianHieroglyphs-Regular.ttf"], "PocketGull-EgyptianHieroglyphs-Companion.woff2", "U+13000-1345F"),
    ("notosansanatolianhieroglyphs", ["NotoSansAnatolianHieroglyphs-Regular.ttf"], "PocketGull-AnatolianHieroglyphs-Companion.woff2", "U+14400-1467F"),
    ("notosanscoptic", ["NotoSansCoptic-Regular.ttf"], "PocketGull-Coptic-Companion.woff2", "U+2C80-2CFF,U+03E2-03EF"),
    ("notosansrunic", ["NotoSansRunic-Regular.ttf"], "PocketGull-Runic-Companion.woff2", "U+16A0-16FF"),
    ("notosansphoenician", ["NotoSansPhoenician-Regular.ttf"], "PocketGull-Phoenician-Companion.woff2", "U+10900-1091F"),
    ("notosanslinearb", ["NotoSansLinearB-Regular.ttf"], "PocketGull-LinearB-Companion.woff2", "U+10000-100FA"),
    ("notosansgothic", ["NotoSansGothic-Regular.ttf"], "PocketGull-Gothic-Companion.woff2", "U+10330-1034F"),
    ("notosansglagolitic", ["NotoSansGlagolitic-Regular.ttf"], "PocketGull-Glagolitic-Companion.woff2", "U+2C00-2C5F"),
    ("notosansdeseret", ["NotoSansDeseret-Regular.ttf"], "PocketGull-Deseret-Companion.woff2", "U+10400-1044F"),
]


def strip_bytecode_and_save_woff2(font: TTFont, out_path: str, strip_gsub: bool = False) -> None:
    if "glyf" not in font or "CFF " in font or "CFF2" in font:
        raise ValueError(f"Security gate rejected non-glyf/CFF outline in {out_path}")
    for tbl in BANNED_TABLES:
        if tbl in font:
            del font[tbl]
    if strip_gsub and "GSUB" in font:
        del font["GSUB"]
    # Enforce Pillar 2: 2-byte word alignment (loca[i] % 2 == 0) even for 32-bit long loca tables
    font["glyf"].padding = 2
    font.flavor = "woff2"
    font.save(out_path)


def fetch_first_available(folder: str, candidates: list[str]) -> str:
    for fname in candidates:
        local = os.path.join(UPSTREAM_DIR, fname)
        if os.path.exists(local):
            return local
    last_err = None
    for fname in candidates:
        local = os.path.join(UPSTREAM_DIR, fname)
        enc = fname.replace("[", "%5B").replace("]", "%5D").replace(",", "%2C")
        url = f"{GF_OFL}/{folder}/{enc}"
        try:
            urllib.request.urlretrieve(url, local)
            return local
        except Exception as e:
            last_err = e
    raise RuntimeError(f"Could not fetch any of {candidates} from {folder}: {last_err}")


def build_companion(folder: str, candidates: list[str], out_name: str, unicodes: str, force: bool = False) -> None:
    out_path = os.path.join(OUT_DIR, out_name)
    if os.path.exists(out_path) and not force:
        return
    src_path = fetch_first_available(folder, candidates)
    font = TTFont(src_path)
    opts = Options()
    opts.layout_features = ["*"]
    opts.hinting = False
    opts.desubroutinize = True
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    subsetter = Subsetter(options=opts)

    cps = set()
    for part in unicodes.split(","):
        part = part.strip().replace("U+", "")
        if "-" in part:
            lo, hi = part.split("-")
            cps.update(range(int(lo, 16), int(hi, 16) + 1))
        else:
            cps.add(int(part, 16))

    subsetter.populate(unicodes=cps)
    subsetter.subset(font)
    strip_bytecode_and_save_woff2(font, out_path, strip_gsub=(out_name in NO_GSUB_SCRIPTS))
    num_glyphs = font["maxp"].numGlyphs
    cmap_len = len(font.getBestCmap() or {})
    font.close()
    print(f"[OK] {out_name:48s} | glyphs={num_glyphs:4d} | cps={cmap_len:4d} | {os.path.getsize(out_path)/1024.0:6.1f} KB")


def build_korean_companion(force: bool = False) -> None:
    """
    Security-hardened Hangul companion:
      - Precomposed KS X 1001 Hangul Syllables (U+AC00-U+D7AF) ONLY
      - Pure TrueType glyf outlines (zero CFF/CFF2 CharStrings)
      - GSUB table stripped (zero ljmo/vjmo/tjmo dynamic Jamo composition)
      - Zero hinting bytecode / Wasm / Graphite tables
    """
    out_path = os.path.join(OUT_DIR, "PocketGull-Korean-Companion.woff2")
    if os.path.exists(out_path) and not force:
        return
    src_path = fetch_first_available("notosanskr", ["NotoSansKR[wght].ttf"])
    cps = set()
    for b1 in range(0xB0, 0xC9):
        for b2 in range(0xA1, 0xFF):
            try:
                ch = bytes([b1, b2]).decode("euc-kr")
                if 0xAC00 <= ord(ch) <= 0xD7AF:
                    cps.add(ord(ch))
            except UnicodeDecodeError:
                pass
    font = TTFont(src_path)
    opts = Options()
    opts.layout_features = []
    opts.hinting = False
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    subsetter = Subsetter(options=opts)
    subsetter.populate(unicodes=cps)
    subsetter.subset(font)
    strip_bytecode_and_save_woff2(font, out_path, strip_gsub=True)
    num_glyphs = font["maxp"].numGlyphs
    cmap_len = len(font.getBestCmap() or {})
    font.close()
    print(f"[OK] {'PocketGull-Korean-Companion.woff2':48s} | glyphs={num_glyphs:4d} | cps={cmap_len:4d} | {os.path.getsize(out_path)/1024.0:6.1f} KB")


def build_cjk_companion(force: bool = False) -> None:
    out_path = os.path.join(OUT_DIR, "PocketGull-CJK-Companion.woff2")
    if os.path.exists(out_path) and not force:
        return
    src_path = fetch_first_available("notosanssc", ["NotoSansSC[wght].ttf"])
    cps = set()
    cps.update(range(0x3000, 0x30FF + 1))
    cps.update(range(0x31F0, 0x31FF + 1))
    cps.update(range(0xFF00, 0xFF60 + 1))
    for b1 in range(0xB0, 0xD8):
        for b2 in range(0xA1, 0xFF):
            if b1 == 0xD7 and b2 > 0xF9:
                continue
            try:
                cps.add(ord(bytes([b1, b2]).decode("gb2312")))
            except UnicodeDecodeError:
                pass
    font = TTFont(src_path)
    opts = Options()
    opts.layout_features = ["*"]
    opts.hinting = False
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    subsetter = Subsetter(options=opts)
    subsetter.populate(unicodes=cps)
    subsetter.subset(font)
    strip_bytecode_and_save_woff2(font, out_path, strip_gsub=False)
    font.close()
    print(f"[OK] {'PocketGull-CJK-Companion.woff2':48s} | {os.path.getsize(out_path)/1024.0:6.1f} KB")


if __name__ == "__main__":
    force = "--force" in sys.argv
    for folder, cands, out_name, ur in COMPANIONS:
        build_companion(folder, cands, out_name, ur, force=force)
    build_korean_companion(force=force)
    build_cjk_companion(force=force)
    total = len([f for f in os.listdir(OUT_DIR) if f.endswith(".woff2")])
    print(f"[DONE] Total self-hosted OFL companions in {OUT_DIR}: {total}")
