#!/usr/bin/env python3
"""
PocketGull Typefoundry: Dieter Rams Minimalist Social Preview Updater
=====================================================================
Surgically updates the Dieter Rams minimalist social preview SVGs and PNGs:
  1. Replaces '6TH GRADE FRIENDLY' with 'LOUISE SLOAN 5:1' while preserving
     the original Dieter Rams Minimalist layout, device photo, and copy.
  2. Eliminates Braille tofu (.notdef boxes) across all SVGs
     (social_github_preview.svg, social_twitter_card.svg,
      social_instagram_square.svg, social_instagram_portrait.svg,
      print_gallery_exhibition.svg) by converting <text class="font-braille">
     into pure ISO/TR 11548 vector <circle> geometry and embedding
     PocketGull WOFF2 fonts in <defs><style>.
  3. Rasterizes crisp, authentic PocketGull v4.0 PNGs for:
     - .github/social_github_preview.png (Washi Dieter Rams)
     - documentation/images/social_github_preview.png (Washi Dieter Rams 2x)
     - article/social_github_preview.png (Dark Dieter Rams)
     - article/social_twitter_card.png (Dark Dieter Rams Twitter Card)
"""

import base64
import io
import re
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
FONTS_TTF_DIR = ROOT_DIR / "fonts" / "ttf"
FONTS_WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
ARTICLE_DIR = ROOT_DIR / "article"
DOC_IMG_DIR = ROOT_DIR / "documentation" / "images"
GITHUB_DIR = ROOT_DIR / ".github"


def get_font(stem: str, size: int) -> ImageFont.FreeTypeFont:
    p = FONTS_TTF_DIR / f"{stem}.ttf"
    if not p.exists():
        p = FONTS_TTF_DIR / "PocketGull-Regular.ttf"
    return ImageFont.truetype(str(p), size)


def braille_to_svg_group(
    text: str,
    x: float,
    y_baseline: float,
    font_size: float,
    fill: str,
    anchor: str = "start",
) -> str:
    """
    Converts a Unicode Braille string (U+2800..U+28FF) into pure SVG <circle>
    elements so it never renders as tofu (.notdef) in any SVG viewer.
    """
    dot_r = font_size * 0.125
    col_gap = font_size * 0.40
    row_gap = font_size * 0.36
    cell_adv = font_size * 0.96
    y_top = y_baseline - font_size * 0.78

    total_w = len(text) * cell_adv - (cell_adv - col_gap - dot_r * 2)
    start_x = x
    if anchor == "middle":
        start_x = x - total_w / 2.0
    elif anchor == "end":
        start_x = x - total_w

    dot_bits = [
        (0x01, 0, 0),
        (0x02, 0, 1),
        (0x04, 0, 2),
        (0x08, 1, 0),
        (0x10, 1, 1),
        (0x20, 1, 2),
        (0x40, 0, 3),
        (0x80, 1, 3),
    ]

    elems: list[str] = []
    cur_x = start_x
    for ch in text:
        cp = ord(ch)
        if 0x2800 <= cp <= 0x28FF:
            mask = cp - 0x2800
            for bit, col, row in dot_bits:
                if mask & bit:
                    cx = cur_x + col * col_gap + dot_r
                    cy = y_top + row * row_gap + dot_r
                    elems.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{dot_r:.2f}" fill="{fill}"/>')
        elif ch in ("—", "-"):
            cy = y_top + row_gap * 1.0
            elems.append(
                f'<line x1="{cur_x:.2f}" y1="{cy:.2f}" x2="{cur_x + col_gap * 1.2:.2f}" y2="{cy:.2f}" stroke="{fill}" stroke-width="{max(1.5, dot_r * 0.9):.2f}" stroke-linecap="round"/>'
            )
        cur_x += cell_adv

    return f'<g class="braille-vector" aria-label="Braille">{"".join(elems)}</g>'


def draw_braille_pil(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: float,
    y_baseline: float,
    font_size: float,
    fill: tuple[int, int, int, int],
    anchor: str = "start",
) -> None:
    """Draws tactile Braille cells onto a PIL ImageDraw matching the original Dieter Rams dot styling."""
    dot_r = font_size * 0.125
    col_gap = font_size * 0.40
    row_gap = font_size * 0.36
    cell_adv = font_size * 0.96
    y_top = y_baseline - font_size * 0.78

    total_w = len(text) * cell_adv - (cell_adv - col_gap - dot_r * 2)
    start_x = x
    if anchor == "middle":
        start_x = x - total_w / 2.0
    elif anchor == "end":
        start_x = x - total_w

    dot_bits = [
        (0x01, 0, 0),
        (0x02, 0, 1),
        (0x04, 0, 2),
        (0x08, 1, 0),
        (0x10, 1, 1),
        (0x20, 1, 2),
        (0x40, 0, 3),
        (0x80, 1, 3),
    ]

    cur_x = start_x
    for ch in text:
        cp = ord(ch)
        if 0x2800 <= cp <= 0x28FF:
            mask = cp - 0x2800
            for bit, col, row in dot_bits:
                if mask & bit:
                    cx = cur_x + col * col_gap + dot_r
                    cy = y_top + row * row_gap + dot_r
                    draw.ellipse((cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r), fill=fill)
        elif ch in ("—", "-"):
            cy = y_top + row_gap * 1.0
            draw.line(
                (cur_x, cy, cur_x + col_gap * 1.2, cy),
                fill=fill,
                width=max(2, int(dot_r * 0.95)),
            )
        cur_x += cell_adv


def build_embedded_font_css() -> str:
    """Builds @font-face declarations with embedded Base64 WOFF2 for zero-tofu SVG rendering."""
    declarations: list[str] = []
    fonts = [
        ("PocketGull", "PocketGull-Fineliner-Core.woff2", "normal", "400"),
        ("PocketGull", "PocketGull-Bold-Core.woff2", "normal", "bold"),
        ("PocketGull Mono", "PocketGullMono-Regular-Core.woff2", "normal", "400"),
    ]
    for fam, fname, fstyle, fweight in fonts:
        fpath = FONTS_WOFF2_DIR / fname
        if fpath.exists():
            b64 = base64.b64encode(fpath.read_bytes()).decode("ascii")
            declarations.append(
                f'    @font-face {{ font-family: "{fam}"; src: local("{fam}"), url("data:font/woff2;base64,{b64}") format("woff2"); font-style: {fstyle}; font-weight: {fweight}; }}'
            )
    declarations.extend(
        [
            '    .font-title { font-family: "PocketGull", -apple-system, sans-serif; font-weight: bold; }',
            '    .font-mono { font-family: "PocketGull Mono", "Courier New", monospace; }',
            '    .font-braille { font-family: "PocketGull", "Segoe UI Symbol", sans-serif; letter-spacing: 0.22em; font-weight: bold; }',
            '    .font-body { font-family: "PocketGull", -apple-system, sans-serif; }',
        ]
    )
    return "\n".join(declarations)


def upgrade_svg_file(svg_path: Path, embed_woff2: bool = True) -> None:
    """
    Surgically updates an SVG file:
      1. Replaces any <text ... class="font-braille" ...>...</text> with pure vector
         Braille <circle> dots so tofu can never appear.
      2. Replaces '6TH GRADE FRIENDLY' with 'LOUISE SLOAN 5:1' and restores
         Dieter Rams Minimalist terminology.
      3. Embeds PocketGull Core WOFF2 fonts into <style> so all text renders in
         authentic PocketGull in any SVG viewer.
    """
    if not svg_path.exists():
        return
    content = svg_path.read_text(encoding="utf-8")

    # 1. Replace <text ... class="font-braille" ...>...</text> with vector circles
    pattern = re.compile(
        r'<text\s+([^>]*class="font-braille"[^>]*)>([^<]+)</text>'
    )

    def _replace_braille(match: re.Match) -> str:
        attrs = match.group(1)
        inner_text = match.group(2)

        def _attr(name: str, default: str = "") -> str:
            m = re.search(rf'\b{name}="([^"]+)"', attrs)
            return m.group(1) if m else default

        x = float(_attr("x", "0"))
        y = float(_attr("y", "0"))
        fsize = float(_attr("font-size", "14"))
        fill = _attr("fill", "#0D9488")
        anchor = _attr("text-anchor", "start")
        return braille_to_svg_group(inner_text, x, y, fsize, fill, anchor)

    content = pattern.sub(_replace_braille, content)

    # 2. Replace '6TH GRADE FRIENDLY' & enforce Libre Functionalist wording (Google Fonts trademark-clean)
    content = content.replace("6TH GRADE FRIENDLY", "LOUISE SLOAN 5:1")
    content = content.replace("GRADE 6 READING LEVEL", "LOUISE SLOAN 5:1")
    content = content.replace(
        "<!-- Right Side: COPPA-Safe, 6th-Grade Content -->",
        "<!-- Right Side: Libre Functionalist & Clinical Content -->",
    )
    content = content.replace(
        "<!-- Right Side: Dieter Rams Minimalist & Clinical Content -->",
        "<!-- Right Side: Libre Functionalist & Clinical Content -->",
    )
    content = content.replace(
        "<!-- 6th Grade Plain Language Description -->",
        "<!-- Libre Functionalist Plain Language Description -->",
    )
    content = content.replace(
        "<!-- Dieter Rams Plain Language Description -->",
        "<!-- Libre Functionalist Plain Language Description -->",
    )
    content = content.replace(
        "<!-- 6th Grade Explanation -->",
        "<!-- Humanist Optotype Explanation -->",
    )
    content = content.replace(
        "<!-- Bottom Plain-Language Guide (6th Grade Reading Level) -->",
        "<!-- Bottom Libre Functionalist Guide -->",
    )
    content = content.replace(
        "<!-- Bottom Dieter Rams Functionalist Guide -->",
        "<!-- Bottom Libre Functionalist Guide -->",
    )
    content = content.replace(
        "<!-- 3 Big Lessons in Good Design (6th Grade Reading Level) -->",
        "<!-- 3 Principles of Libre Functionalist & Optotypic Design -->",
    )
    content = content.replace(
        "<!-- 3 Principles of Dieter Rams & Optotypic Design -->",
        "<!-- 3 Principles of Libre Functionalist & Optotypic Design -->",
    )
    content = content.replace(
        "MODEL PG-01 // DIETER RAMS MINIMAL DESIGN",
        "MODEL PG-01 // LIBRE FUNCTIONALIST DESIGN",
    )
    content = content.replace(
        'Dieter Rams: "Less, but better."',
        'Libre Functionalism: "Less, but better."',
    )
    content = content.replace(
        'Dieter Rams taught us: "Less, but better."',
        'Libre Functionalism: "Less, but better."',
    )
    content = content.replace(
        'Libre Functionalism said: "Less, but better."',
        'Libre Functionalism: "Less, but better."',
    )
    content = content.replace(
        "DESIGN THAT CARES // DIETER RAMS 10 PRINCIPLES",
        "DESIGN THAT CARES // LIBRE FUNCTIONALIST PRINCIPLES",
    )
    content = content.replace(
        "DESIGN THAT CARES // Libre Functionalism PRINCIPLES",
        "DESIGN THAT CARES // LIBRE FUNCTIONALIST PRINCIPLES",
    )
    content = content.replace(
        "COPPA SAFE • FAMILY FRIENDLY",
        "COPPA SAFE • LOUISE SLOAN 5:1",
    )
    content = content.replace(
        "Designed by Phil Gear // pocketgull.app // github.com/pocketgull-app",
        "Designed by Phil Gear // font.pocketgull.app // font.pocketgull.com // github.com/pocketgull-app",
    )

    # 3. Embed PocketGull WOFF2 in <style> if requested
    if embed_woff2:
        style_pattern = re.compile(r"<style>.*?</style>", re.DOTALL)
        embedded_css = f"<style>\n{build_embedded_font_css()}\n  </style>"
        content = style_pattern.sub(lambda _: embedded_css, content, count=1)

    svg_path.write_text(content, encoding="utf-8")
    print(f"  [SVG Updated] {svg_path.relative_to(ROOT_DIR)}")


def extract_device_photo_from_svg(svg_path: Path) -> Image.Image:
    """Extracts the embedded JPEG device photo from an SVG."""
    text = svg_path.read_text(encoding="utf-8")
    m = re.search(r'href="data:image/jpeg;base64,([^"]+)"', text)
    if not m:
        raise RuntimeError(f"Could not find embedded JPEG in {svg_path}")
    raw = base64.b64decode(m.group(1))
    return Image.open(io.BytesIO(raw)).convert("RGBA")


def patch_instagram_pngs() -> None:
    """
    Patches the two legacy 'Dieter Rams' text regions inside
    article/social_instagram_square.png and article/social_instagram_portrait.png
    to 'LIBRE FUNCTIONALIST PRINCIPLES' and 'Libre Functionalism: \"Less, but better.\"'
    using authentic PocketGull Mono.
    """
    sq_path = ARTICLE_DIR / "social_instagram_square.png"
    if sq_path.exists():
        sq = Image.open(sq_path).convert("RGBA")
        draw = ImageDraw.Draw(sq)
        # 1. Header subtitle (x=280..680, y=82..112)
        draw.rectangle((280, 82, 700, 112), fill=(9, 14, 23, 255))
        draw.text(
            (288, 88),
            "DESIGN THAT CARES // LIBRE FUNCTIONALIST PRINCIPLES",
            fill=(148, 163, 184, 255),
            font=get_font("PocketGullMono-Bold", 13),
        )
        # 2. Card 1 footer (x=74..350, y=795..830)
        draw.rectangle((74, 795, 380, 830), fill=(11, 19, 43, 255))
        draw.text(
            (80, 804),
            'Libre Functionalism: "Less, but better."',
            fill=(56, 189, 248, 255),
            font=get_font("PocketGullMono-Regular", 11),
        )
        sq.convert("RGB").save(sq_path, format="PNG", optimize=True)
        print(f"  [PNG Updated] {sq_path.relative_to(ROOT_DIR)} (Libre Functionalist patched)")

    pt_path = ARTICLE_DIR / "social_instagram_portrait.png"
    if pt_path.exists():
        pt = Image.open(pt_path).convert("RGBA")
        draw = ImageDraw.Draw(pt)
        # Replace 'GRADE 6 READING LEVEL' at top-right (x=780..1025, y=90..122)
        draw.rectangle((780, 90, 1025, 122), fill=(9, 14, 23, 255))
        draw.text(
            (1020, 98),
            "LOUISE SLOAN 5:1",
            fill=(45, 212, 191, 255),
            font=get_font("PocketGullMono-Regular", 12),
            anchor="ra",
        )
        draw.rectangle((78, 1094, 995, 1122), fill=(13, 22, 40, 255))
        draw.text(
            (84, 1096),
            'Libre Functionalism: "Less, but better." When we strip away clutter, what remains is pure, honest help.',
            fill=(226, 232, 240, 255),
            font=get_font("PocketGull-Regular", 15),
        )
        pt.convert("RGB").save(pt_path, format="PNG", optimize=True)
        print(f"  [PNG Updated] {pt_path.relative_to(ROOT_DIR)} (Libre Functionalist + Louise Sloan 5:1 patched)")


def render_dieter_rams_github_preview(device_photo: Image.Image, dark_mode: bool = False, scale: int = 2) -> Image.Image:
    """
    Renders the Dieter Rams Minimalist GitHub Social Preview (1280x640 * scale)
    using authentic PocketGull v4.0 fonts and zero-tofu Braille geometry.
    """
    W, H = 1280 * scale, 640 * scale
    s = scale

    img = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(img)

    if not dark_mode:
        # Warm Washi Light gradient (#FFFFFF -> #FAF8F5 -> #F4EFE6)
        for y in range(H):
            t = y / H
            r = int(255 - t * 11)
            g = int(255 - t * 16)
            b = int(255 - t * 25)
            draw.line((0, y, W, y), fill=(r, g, b, 255))
        grid_col = (231, 226, 214, 255)
        eyebrow_col = (13, 148, 136, 255)
        title_col = (31, 27, 22, 255)
        accent_teal = (13, 148, 136, 255)
        body_col = (87, 83, 78, 255)
        meta_col = (31, 27, 22, 255)
        pipe_col = (168, 162, 158, 255)
        star_col = (246, 177, 43, 255)
        quote_col = (120, 113, 108, 255)
        photo_stroke = (45, 212, 191, 140)
        photo_label = (45, 212, 191, 255)
        braille_col = (13, 148, 136, 255)
    else:
        # Dark Dieter Rams Obsidian gradient (#070A10 -> #0F172A)
        for y in range(H):
            t = y / H
            r = int(7 + t * 8)
            g = int(10 + t * 13)
            b = int(16 + t * 26)
            draw.line((0, y, W, y), fill=(r, g, b, 255))
        grid_col = (40, 53, 75, 255)
        eyebrow_col = (56, 189, 248, 255)
        title_col = (248, 250, 252, 255)
        accent_teal = (45, 212, 191, 255)
        body_col = (203, 213, 225, 255)
        meta_col = (226, 232, 240, 255)
        pipe_col = (100, 116, 139, 255)
        star_col = (245, 158, 11, 255)
        quote_col = (148, 163, 184, 255)
        photo_stroke = (45, 212, 191, 130)
        photo_label = (45, 212, 191, 255)
        braille_col = (56, 189, 248, 255)

    # Top & Bottom Subtle Grid Lines
    draw.line((60 * s, 60 * s, 1220 * s, 60 * s), fill=grid_col, width=max(1, int(1 * s)))
    draw.line((60 * s, 580 * s, 1220 * s, 580 * s), fill=grid_col, width=max(1, int(1 * s)))

    # Left Side: Dieter Rams Device Photo (x=60, y=60, w=500, h=520)
    pw, ph = 500 * s, 520 * s
    px, py = 60 * s, 60 * s

    # Center-crop device_photo to 500:520 aspect ratio
    src_w, src_h = device_photo.size
    target_ratio = 500.0 / 520.0
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        cropped = device_photo.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        cropped = device_photo.crop((0, top, src_w, top + new_h))

    photo_resized = cropped.resize((pw, ph), Image.Resampling.LANCZOS)
    corner_r = (14 if dark_mode else 6) * s
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, ph), radius=corner_r, fill=255)
    img.paste(photo_resized, (px, py), mask)
    draw.rounded_rectangle((px, py, px + pw, py + ph), radius=corner_r, outline=photo_stroke, width=max(1, int(1.5 * s)))

    # Photo caption: MODEL PG-01 // LIBRE FUNCTIONALIST DESIGN
    f_photo_cap = get_font("PocketGullMono-Bold", 11 * s)
    draw.text(
        (px + 20 * s, py + 494 * s),
        "MODEL PG-01 // LIBRE FUNCTIONALIST DESIGN",
        fill=photo_label,
        font=f_photo_cap,
    )

    # Right Side (x=600, y=75)
    rx, ry = 600 * s, 75 * s

    f_eyebrow = get_font("PocketGullMono-Bold", 13 * s)
    f_title = get_font("PocketGull-Bold", 46 * s)
    f_body = get_font("PocketGull-Regular", 18 * s)
    f_mono_spec = get_font("PocketGullMono-Regular", 12 * s)
    f_mono_bold = get_font("PocketGullMono-Bold", 12 * s)
    f_quote = get_font("PocketGull-Italic", 14 * s)
    f_footer = get_font("PocketGullMono-Regular", 12 * s)

    if not dark_mode:
        # Pure Typographic Eyebrow
        draw.text((rx, ry + 6 * s), "CLINICAL TYPEFACE SUPERFAMILY", fill=eyebrow_col, font=f_eyebrow)
    else:
        # Dark mode pill eyebrow
        draw.rounded_rectangle((rx, ry, rx + 270 * s, ry + 30 * s), radius=15 * s, fill=(13, 25, 43, 255), outline=(45, 212, 191, 140), width=max(1, s))
        draw.ellipse((rx + 12 * s, ry + 10 * s, rx + 22 * s, ry + 20 * s), fill=star_col)
        draw.text((rx + 32 * s, ry + 8 * s), "POCKETGULL TYPEFOUNDRY", fill=eyebrow_col, font=get_font("PocketGullMono-Regular", 11 * s))

    # Main Title
    draw.text((rx, ry + 42 * s), "Letters Made for", fill=title_col, font=f_title)
    draw.text((rx, ry + 96 * s), "Healthy Eyes.", fill=accent_teal, font=f_title)

    # Description
    draw.text((rx, ry + 165 * s), "Good design is simple and kind. PocketGull is a clean,", fill=body_col, font=f_body)
    draw.text((rx, ry + 195 * s), "friendly typeface designed to help everyone read with ease.", fill=body_col, font=f_body)
    draw.text((rx, ry + 225 * s), "No tired eyes. No confusing numbers. Just pure clarity.", fill=body_col, font=f_body)

    # Meta Specifications (✓ COPPA SAFE | ✓ LOUISE SLOAN 5:1 | ★ SIL OFL 1.1 OPEN SOURCE)
    my = ry + 275 * s
    if not dark_mode:
        draw.line((rx, my, rx + 620 * s, my), fill=grid_col, width=max(1, s))
        ty = my + 12 * s
        cx = rx
        draw.text((cx, ty), "✓ ", fill=accent_teal, font=f_mono_bold)
        cx += int(18 * s)
        draw.text((cx, ty), "COPPA SAFE", fill=meta_col, font=f_mono_spec)
        cx += int(112 * s)
        draw.text((cx, ty), "|", fill=pipe_col, font=f_mono_spec)
        cx += int(36 * s)
        draw.text((cx, ty), "✓ ", fill=accent_teal, font=f_mono_bold)
        cx += int(18 * s)
        draw.text((cx, ty), "LOUISE SLOAN 5:1", fill=meta_col, font=f_mono_spec)
        cx += int(156 * s)
        draw.text((cx, ty), "|", fill=pipe_col, font=f_mono_spec)
        cx += int(36 * s)
        draw.text((cx, ty), "✓ ", fill=star_col, font=f_mono_bold)
        cx += int(18 * s)
        draw.text((cx, ty), "SIL OFL 1.1 OPEN SOURCE", fill=meta_col, font=f_mono_spec)
        draw.line((rx, my + 38 * s, rx + 620 * s, my + 38 * s), fill=grid_col, width=max(1, s))
    else:
        # 3 Dark Pill Boxes
        pills = [
            ("✓ COPPA SAFE", meta_col, 180 * s),
            ("✓ LOUISE SLOAN 5:1", meta_col, 220 * s),
            ("✓ SIL OFL 1.1 FREE", star_col, 180 * s),
        ]
        px_cur = rx
        for lbl, col, pw_box in pills:
            draw.rounded_rectangle((px_cur, my, px_cur + pw_box, my + 38 * s), radius=6 * s, fill=(24, 34, 53, 255))
            draw.text((px_cur + 16 * s, my + 12 * s), lbl, fill=col, font=f_mono_spec)
            px_cur += pw_box + 16 * s

    # Braille & Dieter Rams Rule
    draw.line((rx, (ry + 345 * s), rx + 620 * s, (ry + 345 * s)), fill=grid_col, width=max(1, s))
    draw_braille_pil(
        draw,
        "⠏⠕⠉⠅⠑⠞⠛⠥⠇⠇ ⠺⠑⠝⠊⠛⠑⠗⠀⠁⠃⠑⠗⠀⠃⠑⠎⠎⠑⠗",
        rx,
        ry + 382 * s,
        14 * s,
        fill=braille_col,
        anchor="start",
    )
    draw.text(
        (rx, ry + 402 * s),
        "“Weniger, aber besser” — Less, but better. Honest, gentle, and useful.",
        fill=quote_col,
        font=f_quote,
    )
    draw.text(
        (rx, ry + 434 * s),
        "Designed by Phil Gear // font.pocketgull.app // font.pocketgull.com // github.com/pocketgull-app",
        fill=quote_col,
        font=get_font("PocketGullMono-Regular", 11 * s),
    )

    return img


def render_twitter_card_pil(device_photo: Image.Image) -> Image.Image:
    """Renders article/social_twitter_card.png (1200x675) with zero-tofu Braille."""
    W, H = 1200, 675
    s = 2
    img = Image.new("RGBA", (W * s, H * s))
    draw = ImageDraw.Draw(img)

    for y in range(H * s):
        t = y / (H * s)
        r = int(6 + t * 5)
        g = int(9 + t * 10)
        b = int(17 + t * 26)
        draw.line((0, y, W * s, y), fill=(r, g, b, 255))

    # Left: Device Photo (x=60, y=70, w=470, h=535)
    pw, ph = 470 * s, 535 * s
    px, py = 60 * s, 70 * s
    src_w, src_h = device_photo.size
    target_ratio = 470.0 / 535.0
    new_w = int(src_h * target_ratio)
    left = (src_w - new_w) // 2
    cropped = device_photo.crop((left, 0, left + new_w, src_h)).resize((pw, ph), Image.Resampling.LANCZOS)
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, ph), radius=14 * s, fill=255)
    img.paste(cropped, (px, py), mask)
    draw.rounded_rectangle((px, py, px + pw, py + ph), radius=14 * s, outline=(45, 212, 191, 128), width=2 * s)

    draw.rounded_rectangle((px + 15 * s, py + 485 * s, px + 455 * s, py + 520 * s), radius=6 * s, fill=(3, 7, 18, 215))
    draw.text(
        (px + 30 * s, py + 497 * s),
        "LESS, BUT BETTER • LIBRE SYSTEM 01",
        fill=(45, 212, 191, 255),
        font=get_font("PocketGullMono-Bold", 11 * s),
    )

    # Right Side (x=570, y=70)
    rx, ry = 570 * s, 70 * s
    draw.text((rx, ry + 18 * s), "● THE GENTLE HEALER // PHIL GEAR", fill=(245, 158, 11, 255), font=get_font("PocketGullMono-Bold", 12 * s))
    draw.text((rx, ry + 42 * s), "A Story of Kind Ink", fill=(248, 250, 252, 255), font=get_font("PocketGull-Bold", 34 * s))

    # Limerick Box
    draw.rounded_rectangle((rx, ry + 95 * s, rx + 570 * s, ry + 325 * s), radius=12 * s, fill=(14, 23, 42, 255), outline=(51, 65, 85, 255), width=2)
    f_lim = get_font("PocketGull-Italic", 20 * s)
    f_lim_b = get_font("PocketGull-BoldItalic", 21 * s)
    draw.text((rx + 30 * s, ry + 122 * s), "In a circle where empathy grows,", fill=(203, 213, 225, 255), font=f_lim)
    draw.text((rx + 30 * s, ry + 157 * s), "And care like a mountain stream flows,", fill=(203, 213, 225, 255), font=f_lim)
    draw.text((rx + 30 * s, ry + 192 * s), "He drew with kind ink", fill=(56, 189, 248, 255), font=f_lim)
    draw.text((rx + 30 * s, ry + 227 * s), "To help everyone think,", fill=(56, 189, 248, 255), font=f_lim)
    draw.text((rx + 30 * s, ry + 267 * s), "And soothe tired eyes from their woes!", fill=(45, 212, 191, 255), font=f_lim_b)

    # Explanation
    ey = ry + 355 * s
    f_exp = get_font("PocketGull-Regular", 15 * s)
    draw.text((rx, ey + 6 * s), "When you read books or look at a screen, your eyes work hard.", fill=(226, 232, 240, 255), font=f_exp)
    draw.text((rx, ey + 30 * s), "PocketGull was drawn with friendly shapes and open spaces so", fill=(226, 232, 240, 255), font=f_exp)
    draw.text((rx, ey + 54 * s), "reading feels like a gentle breeze. Safe, clear, and kind for all.", fill=(226, 232, 240, 255), font=f_exp)

    draw.line((rx, ey + 95 * s, rx + 570 * s, ey + 95 * s), fill=(51, 65, 85, 255), width=2)
    draw_braille_pil(
        draw,
        "⠏⠕⠉⠅⠑⠞⠛⠥⠇⠇ — ⠉⠁⠗⠑⠀⠁⠝⠙⠀⠅⠊⠝⠙⠝⠑⠎⠎",
        rx,
        ey + 125 * s,
        13 * s,
        fill=(56, 189, 248, 255),
        anchor="start",
    )
    draw.text(
        (rx + 570 * s, ey + 113 * s),
        "COPPA SAFE • LOUISE SLOAN 5:1",
        fill=(100, 116, 139, 255),
        font=get_font("PocketGullMono-Regular", 11 * s),
        anchor="ra",
    )

    return img.resize((W, H), Image.Resampling.LANCZOS)


def main() -> None:
    print("1. Extracting embedded Dieter Rams device photo...")
    device_photo = extract_device_photo_from_svg(ARTICLE_DIR / "social_github_preview.svg")

    print("2. Surgically upgrading SVG files (Zero Tofu vector Braille + Louise Sloan 5:1)...")
    svg_targets = [
        (ARTICLE_DIR / "social_github_preview.svg", True),
        (ARTICLE_DIR / "social_twitter_card.svg", True),
        (ARTICLE_DIR / "social_instagram_square.svg", True),
        (ARTICLE_DIR / "social_instagram_portrait.svg", True),
        (ARTICLE_DIR / "print_gallery_exhibition.svg", False),
    ]
    for path, embed in svg_targets:
        upgrade_svg_file(path, embed_woff2=embed)

    print("3. Rendering Dieter Rams Washi & Dark GitHub Social Preview PNGs...")
    washi_2x = render_dieter_rams_github_preview(device_photo, dark_mode=False, scale=2)
    washi_1x = washi_2x.resize((1280, 640), Image.Resampling.LANCZOS)

    dark_2x = render_dieter_rams_github_preview(device_photo, dark_mode=True, scale=2)
    dark_1x = dark_2x.resize((1280, 640), Image.Resampling.LANCZOS)

    # Save 2560x1280 Washi Retina to documentation/images/social_github_preview.png
    doc_png = DOC_IMG_DIR / "social_github_preview.png"
    washi_2x.convert("RGB").save(doc_png, format="PNG", optimize=True)
    print(f"  [PNG Updated] {doc_png.relative_to(ROOT_DIR)} ({doc_png.stat().st_size:,} bytes)")

    # Save 1280x640 Washi to .github/social_github_preview.png
    gh_png = GITHUB_DIR / "social_github_preview.png"
    washi_1x.convert("RGB").save(gh_png, format="PNG", optimize=True)
    print(f"  [PNG Updated] {gh_png.relative_to(ROOT_DIR)} ({gh_png.stat().st_size:,} bytes)")

    # Save 1280x640 Dark Dieter Rams to article/social_github_preview.png
    art_png = ARTICLE_DIR / "social_github_preview.png"
    dark_1x.convert("RGB").save(art_png, format="PNG", optimize=True)
    print(f"  [PNG Updated] {art_png.relative_to(ROOT_DIR)} ({art_png.stat().st_size:,} bytes)")

    # Save 1200x675 Twitter Card to article/social_twitter_card.png
    tw_png = ARTICLE_DIR / "social_twitter_card.png"
    render_twitter_card_pil(device_photo).convert("RGB").save(tw_png, format="PNG", optimize=True)
    print(f"  [PNG Updated] {tw_png.relative_to(ROOT_DIR)} ({tw_png.stat().st_size:,} bytes)")

    # Patch Instagram PNGs to Libre Functionalist terminology
    patch_instagram_pngs()


if __name__ == "__main__":
    main()
