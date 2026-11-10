#!/usr/bin/env python3
"""
PocketGull Typefoundry — Z-Layered Anatomical ASL & Sign Language Font Compiler
===============================================================================
Compiles 'PocketGull-Sign.ttf', 'PocketGull-Sign.woff2', 'PocketGull-ASL.ttf', and 'PocketGull-ASL.woff2'.
"""

import math
import sys
from pathlib import Path

import numpy as np
from skimage.measure import approximate_polygon, find_contours
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"

SRC_MONO = TTF_DIR / "PocketGullMono-Regular.ttf"
OUT_SIGN_TTF = TTF_DIR / "PocketGull-Sign.ttf"
OUT_ASL_TTF = TTF_DIR / "PocketGull-ASL.ttf"

ADVANCE = 600  # Strict 600 UPM monospace grid

# -----------------------------------------------------------------------------
# ANALYTIC 2D SIGNED DISTANCE FIELD (SDF) & Z-OCCLUSION ENGINE
# -----------------------------------------------------------------------------
X_MIN, X_MAX = 0.0, 600.0
Y_MIN, Y_MAX = -60.0, 860.0
SCALE = 1.5

GRID_W = int((X_MAX - X_MIN) * SCALE)
GRID_H = int((Y_MAX - Y_MIN) * SCALE)
_xs = np.linspace(X_MIN, X_MAX, GRID_W, dtype=np.float32)
_ys = np.linspace(Y_MIN, Y_MAX, GRID_H, dtype=np.float32)
GX, GY = np.meshgrid(_xs, _ys)


def smin(a, b, k=16.0):
    if k <= 0.0:
        return np.minimum(a, b)
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.minimum(a, b) - h * h * k * 0.25


def sd_capsule(px, py, x0, y0, x1, y1, r0, r1=None):
    if r1 is None:
        r1 = r0
    vx = float(x1 - x0)
    vy = float(y1 - y0)
    l2 = vx * vx + vy * vy
    if l2 < 1e-4:
        return np.hypot(px - x0, py - y0) - r0
    wx = px - float(x0)
    wy = py - float(y0)
    t = np.clip((wx * vx + wy * vy) / l2, 0.0, 1.0)
    dx = wx - vx * t
    dy = wy - vy * t
    r = r0 + (r1 - r0) * t
    return np.hypot(dx, dy) - r


def sd_chain(pts, radii, k=8.0):
    d = sd_capsule(GX, GY, pts[0][0], pts[0][1], pts[1][0], pts[1][1], radii[0], radii[1])
    for i in range(1, len(pts) - 1):
        seg = sd_capsule(GX, GY, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], radii[i], radii[i + 1])
        d = smin(d, seg, k=k)
    return d


def sd_box_round(cx, cy, hx, hy, r):
    qx = np.abs(GX - float(cx)) - (float(hx) - float(r))
    qy = np.abs(GY - float(cy)) - (float(hy) - float(r))
    out = np.hypot(np.maximum(qx, 0.0), np.maximum(qy, 0.0))
    inn = np.minimum(np.maximum(qx, qy), 0.0)
    return out + inn - float(r)


def sd_palm_upright(cx=310, y_bot=65, y_top=380, w_bot=160, w_top=235, wrist=True):
    y_mid = 0.5 * (y_bot + y_top)
    d1 = sd_capsule(GX, GY, cx - w_top * 0.34, y_top - 42, cx + w_top * 0.34, y_top - 48, 58, 52)
    d2 = sd_capsule(GX, GY, cx - w_top * 0.32, y_mid + 15, cx - w_bot * 0.25, y_bot + 42, 60, 50)
    d3 = sd_capsule(GX, GY, cx + w_top * 0.32, y_mid + 10, cx + w_bot * 0.25, y_bot + 42, 56, 48)
    d4 = sd_capsule(GX, GY, cx, y_top - 45, cx, y_bot + 45, 80, 68)
    d = smin(smin(d1, d2, 26.0), smin(d3, d4, 26.0), 28.0)
    if wrist:
        dw = sd_box_round(cx, y_bot + 6, w_bot * 0.45, 34, 18)
        d = smin(d, dw, 20.0)
    return d


class ZCanvas:
    def __init__(self, stroke_w=24.0):
        self.stroke_w = stroke_w
        self.ink = np.zeros((GRID_H, GRID_W), dtype=np.float32)

    def add_layer(self, d, stroke_w=None):
        sw = self.stroke_w if stroke_w is None else stroke_w
        hw = sw * 0.5
        aa = 1.0 / SCALE
        bg_keep = np.clip((d - hw) / aa + 0.5, 0.0, 1.0)
        fg_stroke = np.clip((hw - np.abs(d)) / aa + 0.5, 0.0, 1.0)
        self.ink = np.maximum(self.ink * bg_keep, fg_stroke)

    def add_crease(self, pts, stroke_w=17.0, clip_inside=None):
        radii = [0.0] * len(pts)
        d = sd_chain(pts, radii, k=2.0)
        hw = stroke_w * 0.5
        aa = 1.0 / SCALE
        fg = np.clip((hw - d) / aa + 0.5, 0.0, 1.0)
        if clip_inside is not None:
            mask = np.clip((-clip_inside - 18.0) / aa + 0.5, 0.0, 1.0)
            fg = fg * mask
        self.ink = np.maximum(self.ink, fg)

    def add_arrow_head(self, tip_x, tip_y, dir_dx, dir_dy, length=52.0, wing=34.0, stroke_w=19.0):
        norm = math.hypot(dir_dx, dir_dy) or 1.0
        ux, uy = dir_dx / norm, dir_dy / norm
        nx, ny = -uy, ux
        bx = tip_x - ux * length
        by = tip_y - uy * length
        p_left = (bx + nx * wing, by + ny * wing)
        p_right = (bx - nx * wing, by - ny * wing)
        self.add_crease([p_left, (tip_x, tip_y), p_right], stroke_w=stroke_w)

    def to_tt_glyph(self, glyf_table):
        padded = np.pad(self.ink, 2, mode="constant", constant_values=0.0)
        raw_contours = find_contours(padded, level=0.5)

        pen = TTGlyphPen(glyf_table)
        for rc in raw_contours:
            ys = Y_MIN + (rc[:, 0] - 2.0) / SCALE
            xs = X_MIN + (rc[:, 1] - 2.0) / SCALE
            pts = np.column_stack([xs, ys])

            x_arr, y_arr = pts[:, 0], pts[:, 1]
            area = 0.5 * float(np.sum(x_arr * np.roll(y_arr, -1) - np.roll(x_arr, -1) * y_arr))
            if abs(area) < 160.0:
                continue

            simp = approximate_polygon(pts, tolerance=2.5)
            if len(simp) > 1 and np.hypot(*(simp[0] - simp[-1])) < 3.5:
                simp = simp[:-1]
            cleaned = []
            for p in simp:
                if not cleaned or math.hypot(p[0] - cleaned[-1][0], p[1] - cleaned[-1][1]) >= 4.5:
                    cleaned.append((float(p[0]), float(p[1])))
            if len(cleaned) > 1 and math.hypot(cleaned[0][0] - cleaned[-1][0], cleaned[0][1] - cleaned[-1][1]) < 4.5:
                cleaned.pop()
            if len(cleaned) < 4:
                continue

            cx_a = [p[0] for p in cleaned]
            cy_a = [p[1] for p in cleaned]
            s_area = 0.5 * sum(
                cx_a[i] * cy_a[(i + 1) % len(cleaned)] - cx_a[(i + 1) % len(cleaned)] * cy_a[i]
                for i in range(len(cleaned))
            )
            mx = 0.5 * (cleaned[0][0] + cleaned[1][0])
            my = 0.5 * (cleaned[0][1] + cleaned[1][1])
            edx = cleaned[1][0] - cleaned[0][0]
            edy = cleaned[1][1] - cleaned[0][1]
            elen = math.hypot(edx, edy) or 1.0
            sign_in = 1.0 if s_area > 0 else -1.0
            tx = mx + sign_in * (-edy / elen) * 3.0
            ty = my + sign_in * (edx / elen) * 3.0
            ix = int(np.clip(round((tx - X_MIN) * SCALE), 0, GRID_W - 1))
            iy = int(np.clip(round((ty - Y_MIN) * SCALE), 0, GRID_H - 1))
            is_outer_ink = self.ink[iy, ix] >= 0.5

            if (s_area < 0) != bool(is_outer_ink):
                cleaned.reverse()

            n = len(cleaned)
            q_pts = [(int(round(px)), int(round(py))) for px, py in cleaned]
            m_pts = [
                (int(round(0.5 * (q_pts[i][0] + q_pts[(i + 1) % n][0]))),
                 int(round(0.5 * (q_pts[i][1] + q_pts[(i + 1) % n][1]))))
                for i in range(n)
            ]

            pen.moveTo(m_pts[0])
            cur_on = m_pts[0]
            for i in range(1, n + 1):
                ctrl = q_pts[i % n]
                nxt_on = m_pts[i % n]
                if nxt_on == cur_on:
                    continue
                if ctrl == cur_on or ctrl == nxt_on:
                    pen.lineTo(nxt_on)
                else:
                    pen.qCurveTo(ctrl, nxt_on)
                cur_on = nxt_on
            pen.closePath()

        return pen.glyph()


def curled_finger_sdf(x, y_knuckle=485, y_tip=305, r_top=29, r_tip=26):
    return sd_capsule(GX, GY, x, y_knuckle, x, y_tip, r_top, r_tip)


def upright_finger_sdf(x0, y0, x1, y1, r_base=28, r_tip=23):
    xm, ym = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
    return sd_chain([(x0, y0), (xm, ym), (x1, y1)], [r_base, (r_base + r_tip) * 0.51, r_tip], k=6.0)


def add_palm_creases(cv, d_palm, cx=310, y_base=210):
    cv.add_crease([(cx - 55, y_base + 75), (cx - 10, y_base + 45), (cx + 35, y_base - 15)], stroke_w=15.0, clip_inside=d_palm)


# -----------------------------------------------------------------------------
# REFINED 36 CANONICAL ASL HANDSHAPES (A–Z, 0–9)
# -----------------------------------------------------------------------------
def draw_A(cv):
    """A: Fist with 4 tightly curled fingers and bold upright thumb rising proudly on radial left."""
    d_palm = sd_palm_upright(cx=340, y_bot=65, y_top=375, w_bot=160, w_top=230)
    # Fuse proud radial thumb mound + upright thumb on left rising to y=575 (well above 480 knuckles!)
    d_thumb = sd_chain([(215, 175), (162, 315), (168, 565)], [42, 35, 28], k=16.0)
    cv.add_layer(smin(d_palm, d_thumb, 22.0))
    # 4 compact curled fingers side-by-side at y=475..285
    for fx, yk, yt in [(248, 470, 285), (308, 482, 285), (368, 474, 290), (426, 456, 300)]:
        cv.add_layer(curled_finger_sdf(fx, yk, yt, r_top=28, r_tip=25))


def draw_B(cv):
    """B: Open flat hand, 4 straight upright fingers adducted together, thumb folded across palm."""
    d_palm = sd_palm_upright(cx=315, y_bot=65, y_top=400, w_bot=155, w_top=230)
    cv.add_layer(d_palm)
    for fx, yt, rb, rt in [(216, 745, 28, 24), (276, 795, 29, 25), (336, 760, 28, 24), (394, 685, 26, 22)]:
        cv.add_layer(upright_finger_sdf(fx, 385, fx, yt, rb, rt))
    d_thumb = sd_chain([(188, 225), (255, 295), (355, 315)], [36, 30, 25], k=14.0)
    cv.add_layer(d_thumb)


def draw_C(cv):
    """C: Smooth 3/4 lateral hand curving into an open C-arch facing right."""
    d_wrist = sd_box_round(215, 95, 68, 42, 20)
    d_arch = sd_chain(
        [(205, 130), (150, 285), (160, 500), (245, 660), (380, 680), (460, 605)],
        [46, 44, 44, 40, 34, 26],
        k=18.0,
    )
    d_thumb = sd_chain(
        [(215, 155), (280, 225), (385, 250), (450, 305)],
        [42, 35, 30, 25],
        k=16.0,
    )
    d_back_finger = sd_chain([(240, 675), (370, 718), (445, 655)], [26, 24, 20], k=12.0)
    cv.add_layer(d_back_finger)
    cv.add_layer(smin(d_wrist, smin(d_arch, d_thumb, 24.0), 22.0))


def draw_D(cv):
    """D: Tall upright index finger + generous round open circular loop formed by middle finger & thumb."""
    d_palm = sd_palm_upright(cx=275, y_bot=65, y_top=365, w_bot=150, w_top=200)
    d_idx = upright_finger_sdf(202, 355, 202, 800, 30, 25)
    cv.add_layer(smin(d_palm, d_idx, 18.0))
    # Back curled ring/pinky arc behind loop
    cv.add_layer(sd_chain([(315, 485), (415, 535), (455, 445)], [24, 23, 21], k=12.0))
    # Generous round D-loop (center ~340, 395, radius ~85 -> huge unmistakable circular hole!)
    d_mid = sd_chain([(265, 445), (355, 515), (438, 455), (428, 350)], [27, 26, 25, 23], k=14.0)
    d_thm = sd_chain([(215, 215), (305, 265), (412, 328)], [35, 29, 24], k=14.0)
    cv.add_layer(smin(d_mid, d_thm, 8.0))


def draw_E(cv):
    """E: 4 bent fingers perched cleanly above a horizontal tucked thumb with visible palmar gap."""
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=410, w_bot=160, w_top=235)
    cv.add_layer(d_palm)
    # Horizontal folded thumb lower across palm (y=245..265)
    d_thm = sd_chain([(185, 215), (275, 258), (405, 262)], [36, 30, 25], k=14.0)
    cv.add_layer(d_thm)
    # 4 short curled fingers higher up (y=535 down to y=355 -> crisp white gap/touch above thumb!)
    for fx, yk in [(216, 530), (278, 545), (340, 536), (400, 515)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 355, r_top=28, r_tip=25))


def draw_F(cv):
    """F: Index & thumb pinch a round front O-ring on left; middle, ring, pinky fan tall on right."""
    d_palm = sd_palm_upright(cx=315, y_bot=65, y_top=385, w_bot=155, w_top=225)
    f_mid = upright_finger_sdf(295, 380, 290, 795, 28, 24)
    f_rng = upright_finger_sdf(348, 375, 372, 765, 27, 23)
    f_pnk = upright_finger_sdf(398, 355, 448, 695, 25, 21)
    cv.add_layer(d_palm)
    cv.add_layer(f_pnk)
    cv.add_layer(f_rng)
    cv.add_layer(f_mid)
    d_idx = sd_chain([(240, 395), (172, 515), (138, 430), (192, 358)], [27, 25, 24, 22], k=10.0)
    d_thm = sd_chain([(215, 215), (155, 290), (190, 352)], [35, 29, 23], k=12.0)
    cv.add_layer(d_idx)
    cv.add_layer(d_thm)


def draw_G(cv):
    """G: Horizontal hand pointing right — index at top, parallel thumb below with generous open channel."""
    d_wrist = sd_box_round(105, 395, 42, 74, 18)
    d_hand = sd_capsule(GX, GY, 145, 405, 255, 425, 84, 78)
    d_idx = upright_finger_sdf(245, 505, 530, 505, 29, 24)
    cv.add_layer(smin(d_wrist, smin(d_hand, d_idx, 20.0), 18.0))
    # Curled middle/ring/pinky tucked cleanly at bottom-left
    for cy_k in [315, 260]:
        cv.add_layer(sd_capsule(GX, GY, 215, cy_k, 290, cy_k, 23, 21))
    # Parallel horizontal thumb at y=365 -> crisp 85-UPM open G channel between thumb (365) and index (505)!
    d_thm = sd_chain([(175, 330), (265, 365), (470, 365)], [35, 29, 24], k=14.0)
    cv.add_layer(d_thm)


def draw_H(cv):
    """H: Horizontal hand — index & middle extended right side-by-side together."""
    d_wrist = sd_box_round(105, 380, 42, 74, 18)
    d_hand = sd_capsule(GX, GY, 145, 395, 255, 415, 82, 76)
    cv.add_layer(smin(d_wrist, d_hand, 18.0))
    for cy_k in [320, 268]:
        cv.add_layer(sd_capsule(GX, GY, 230, cy_k, 305, cy_k, 23, 21))
    cv.add_layer(upright_finger_sdf(245, 488, 525, 488, 28, 23))
    cv.add_layer(upright_finger_sdf(245, 430, 535, 430, 28, 24))
    d_thm = sd_chain([(175, 305), (255, 355), (335, 365)], [34, 28, 23], k=12.0)
    cv.add_layer(d_thm)


def draw_I(cv, shift_x=0, shift_y=0, scale=1.0):
    """I: Pinky extended straight up on ulnar right; 3 curled fingers + thumb across front."""
    def sx(v): return int(round(300 + (v - 300) * scale + shift_x))
    def sy(v): return int(round(400 + (v - 400) * scale + shift_y))
    def sr(r): return r * scale

    d_palm = sd_palm_upright(cx=sx(295), y_bot=sy(65), y_top=sy(375), w_bot=sr(150), w_top=sr(220))
    d_pnk = upright_finger_sdf(sx(392), sy(355), sx(398), sy(765), sr(26), sr(22))
    cv.add_layer(smin(d_palm, d_pnk, sr(18.0)))
    for fx, yk in [(210, 475), (270, 490), (330, 480)]:
        cv.add_layer(curled_finger_sdf(sx(fx), sy(yk), sy(305), r_top=sr(28), r_tip=sr(25)))
    d_thm = sd_chain(
        [(sx(182), sy(235)), (sx(255), sy(295)), (sx(350), sy(315))],
        [sr(35), sr(29), sr(24)],
        k=sr(12.0),
    )
    cv.add_layer(d_thm)


def draw_J(cv):
    """J: Compact 'I' handshape + bold unobstructed J-swoop trajectory arrow in clean white space!"""
    draw_I(cv, shift_x=-68, shift_y=115, scale=0.82)
    # Clean sweeping J-curve descending on the right in open air and hooking left beneath the wrist with generous gap!
    j_pts = [(498, 635), (498, 235), (465, 98), (355, 52), (235, 88), (195, 165)]
    cv.add_crease(j_pts, stroke_w=20.0)
    cv.add_arrow_head(195, 165, -35, 75, length=46.0, wing=30.0, stroke_w=19.0)


def draw_K(cv):
    """K: Index straight up, middle angled up-right, thumb upright between them."""
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=380, w_bot=155, w_top=225)
    d_idx = upright_finger_sdf(228, 375, 222, 795, 29, 24)
    d_mid = upright_finger_sdf(288, 375, 365, 765, 29, 24)
    cv.add_layer(d_palm)
    cv.add_layer(d_idx)
    cv.add_layer(d_mid)
    for fx, yk in [(355, 455), (412, 435)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 295, r_top=27, r_tip=24))
    d_thm = sd_chain([(205, 215), (255, 345), (295, 505)], [36, 30, 24], k=12.0)
    cv.add_layer(d_thm)


def draw_L(cv):
    """L: Index straight up, thumb extended 90 degrees horizontally left, 3 fingers curled."""
    d_palm = sd_palm_upright(cx=335, y_bot=65, y_top=380, w_bot=150, w_top=215)
    d_idx = upright_finger_sdf(255, 375, 255, 795, 30, 25)
    d_thm = sd_chain([(255, 245), (175, 265), (78, 280)], [38, 32, 26], k=14.0)
    cv.add_layer(smin(smin(d_palm, d_idx, 18.0), d_thm, 22.0))
    for fx, yk in [(318, 470), (375, 460), (430, 440)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 295, r_top=27, r_tip=24))


def draw_M(cv):
    """M: 3 long fingers draped OVER thumb; thumb tip boldly poking out between 3rd (ring) & pinky!"""
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=385, w_bot=160, w_top=235)
    cv.add_layer(d_palm)
    # Pinky curled shorter on far right (x=442) leaving clear window for thumb tip at x=382!
    cv.add_layer(curled_finger_sdf(442, 445, 315, r_top=25, r_tip=22))
    # Thumb tucked underneath and poking its rounded tip UP-RIGHT at (384, 415)!
    d_thm = sd_chain([(182, 240), (285, 335), (384, 420)], [36, 30, 27], k=12.0)
    cv.add_layer(d_thm)
    # 3 long draped fingers (index, middle, ring) clearly crossing OVER the thumb!
    for fx, yk, yt in [(198, 515, 265), (256, 528, 260), (314, 515, 270)]:
        cv.add_layer(curled_finger_sdf(fx, yk, yt, r_top=27, r_tip=24))


def draw_N(cv):
    """N: 2 long fingers draped OVER thumb; thumb tip boldly poking out between 2nd (middle) & 3rd (ring)!"""
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=385, w_bot=160, w_top=235)
    cv.add_layer(d_palm)
    # Ring & pinky curled shorter on right (x=384, x=438) leaving clear window for thumb at x=322!
    cv.add_layer(curled_finger_sdf(384, 455, 310, r_top=26, r_tip=23))
    cv.add_layer(curled_finger_sdf(438, 435, 315, r_top=25, r_tip=22))
    # Thumb tucked under 2 fingers and poking its rounded tip UP at (322, 430)!
    d_thm = sd_chain([(182, 240), (265, 335), (322, 435)], [36, 30, 27], k=12.0)
    cv.add_layer(d_thm)
    # 2 long draped fingers (index, middle) crossing OVER the thumb!
    for fx, yk, yt in [(198, 515, 265), (256, 528, 262)]:
        cv.add_layer(curled_finger_sdf(fx, yk, yt, r_top=28, r_tip=24))


def draw_O(cv):
    """O: Smooth unified side-profile hand forming a generous clean O-aperture (zero wrist seam!)."""
    d_wrist = sd_box_round(235, 85, 68, 38, 18)
    # Subtle stacked background finger arc along upper dorsum for unmistakable hand anatomy
    d_back = sd_chain([(215, 595), (335, 668), (432, 565)], [25, 24, 21], k=12.0)
    cv.add_layer(d_back)
    # Unified top finger arch + bottom thumb arch meeting cleanly at (440, 400) around open oval hole!
    d_top = sd_chain(
        [(205, 120), (158, 295), (178, 510), (275, 620), (405, 575), (442, 435)],
        [45, 42, 40, 34, 29, 24],
        k=16.0,
    )
    d_bot = sd_chain(
        [(245, 120), (315, 210), (408, 265), (442, 385)],
        [42, 34, 29, 24],
        k=16.0,
    )
    cv.add_layer(smin(d_wrist, smin(d_top, d_bot, 10.0), 22.0))


def draw_P(cv):
    """P: Full-bodied downward K — wrist/palm at upper-right, index pointing left-down, middle down, thumb between."""
    d_wrist = sd_box_round(445, 715, 68, 44, 20)
    d_hand = sd_capsule(GX, GY, 415, 665, 315, 535, 84, 78)
    # Curled ring & pinky tucked under palm on right
    cv.add_layer(sd_capsule(GX, GY, 385, 455, 445, 395, 27, 24))
    cv.add_layer(sd_capsule(GX, GY, 420, 500, 470, 445, 26, 23))
    # Middle finger pointing boldly down
    d_mid = upright_finger_sdf(320, 505, 285, 135, 30, 25)
    cv.add_layer(d_mid)
    # Thumb nestled clearly between index & middle!
    d_thm = sd_chain([(375, 515), (295, 410), (235, 335)], [36, 30, 25], k=12.0)
    cv.add_layer(d_thm)
    # Index finger pointing forward-left above thumb
    d_idx = upright_finger_sdf(295, 565, 75, 465, 30, 25)
    cv.add_layer(smin(smin(d_wrist, d_hand, 22.0), d_idx, 18.0))


def draw_Q(cv):
    """Q: Full-bodied downward G — arched hand at top, index and thumb pointing straight down parallel with open gap."""
    d_wrist = sd_box_round(375, 720, 72, 44, 20)
    d_hand = sd_capsule(GX, GY, 345, 665, 285, 525, 86, 78)
    for cx_k, cy_k in [(365, 470), (402, 510)]:
        cv.add_layer(sd_capsule(GX, GY, cx_k, cy_k, cx_k + 48, cy_k - 48, 26, 23))
    # Index pointing straight down on left (x=205)
    d_idx = upright_finger_sdf(220, 535, 200, 140, 30, 25)
    cv.add_layer(smin(smin(d_wrist, d_hand, 22.0), d_idx, 18.0))
    # Thumb pointing down parallel on right (x=335 -> crisp 80-UPM open Q channel!)
    d_thm = sd_chain([(350, 515), (340, 385), (332, 205)], [36, 30, 25], k=14.0)
    cv.add_layer(d_thm)


def draw_R(cv):
    """R: Index & middle extended upright and CROSSED in Z-depth."""
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=380, w_bot=155, w_top=225)
    cv.add_layer(d_palm)
    d_mid = sd_chain([(305, 375), (278, 565), (232, 785)], [28, 26, 23], k=12.0)
    cv.add_layer(d_mid)
    d_idx = sd_chain([(240, 375), (272, 565), (310, 795)], [28, 26, 24], k=12.0)
    cv.add_layer(d_idx)
    for fx, yk in [(360, 455), (415, 435)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 295, r_top=26, r_tip=23))
    d_thm = sd_chain([(188, 235), (265, 295), (355, 315)], [35, 29, 24], k=12.0)
    cv.add_layer(d_thm)


def draw_S(cv):
    """S: Closed fist with thumb wrapped BOLDLY ACROSS THE FRONT of the 4 curled fingers."""
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=380, w_bot=160, w_top=235)
    cv.add_layer(d_palm)
    for fx, yk, yt in [(216, 495, 290), (278, 510, 290), (340, 500, 295), (398, 480, 305)]:
        cv.add_layer(curled_finger_sdf(fx, yk, yt, r_top=28, r_tip=25))
    d_thm = sd_chain([(175, 250), (248, 350), (378, 372)], [38, 32, 27], k=14.0)
    cv.add_layer(d_thm)


def draw_T(cv):
    """T: Fist with thumb poking BOLDLY UP BETWEEN 1st (index) and 2nd (middle) curled fingers!"""
    d_palm = sd_palm_upright(cx=315, y_bot=65, y_top=380, w_bot=160, w_top=235)
    cv.add_layer(d_palm)
    # Middle, ring, pinky curled on right starting at x=312
    for fx, yk, yt in [(312, 485, 295), (370, 475, 300), (425, 455, 310)]:
        cv.add_layer(curled_finger_sdf(fx, yk, yt, r_top=27, r_tip=24))
    # Thumb rising between index (192) & middle (312) and protruding cleanly up to y=555!
    d_thm = sd_chain([(188, 240), (245, 365), (254, 555)], [36, 31, 28], k=12.0)
    cv.add_layer(d_thm)
    # Index curled snugly on left of thumb (x=194)
    cv.add_layer(curled_finger_sdf(194, 480, 285, r_top=28, r_tip=25))


def draw_U(cv):
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=380, w_bot=155, w_top=225)
    cv.add_layer(d_palm)
    cv.add_layer(upright_finger_sdf(238, 375, 238, 785, 28, 24))
    cv.add_layer(upright_finger_sdf(296, 375, 296, 800, 28, 24))
    for fx, yk in [(356, 455), (412, 435)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 295, r_top=26, r_tip=23))
    d_thm = sd_chain([(188, 235), (265, 295), (355, 315)], [35, 29, 24], k=12.0)
    cv.add_layer(d_thm)


def draw_V(cv):
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=380, w_bot=155, w_top=225)
    cv.add_layer(d_palm)
    cv.add_layer(upright_finger_sdf(238, 375, 178, 785, 28, 24))
    cv.add_layer(upright_finger_sdf(298, 375, 358, 790, 28, 24))
    for fx, yk in [(360, 455), (415, 435)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 295, r_top=26, r_tip=23))
    d_thm = sd_chain([(188, 235), (265, 295), (355, 315)], [35, 29, 24], k=12.0)
    cv.add_layer(d_thm)


def draw_W(cv):
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=380, w_bot=155, w_top=230)
    cv.add_layer(d_palm)
    cv.add_layer(upright_finger_sdf(228, 375, 162, 775, 27, 23))
    cv.add_layer(upright_finger_sdf(292, 380, 292, 800, 28, 24))
    cv.add_layer(upright_finger_sdf(355, 375, 420, 775, 27, 23))
    cv.add_layer(curled_finger_sdf(415, 440, 295, r_top=25, r_tip=22))
    d_thm = sd_chain([(190, 225), (285, 290), (395, 315)], [35, 28, 23], k=12.0)
    cv.add_layer(d_thm)


def draw_X(cv):
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=375, w_bot=155, w_top=225)
    d_hook = sd_chain([(225, 375), (222, 595), (298, 655), (338, 545)], [29, 27, 25, 22], k=10.0)
    cv.add_layer(smin(d_palm, d_hook, 16.0))
    for fx, yk in [(295, 460), (352, 450), (408, 430)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 295, r_top=26, r_tip=23))
    d_thm = sd_chain([(188, 235), (265, 295), (345, 315)], [35, 29, 24], k=12.0)
    cv.add_layer(d_thm)


def draw_Y(cv):
    d_palm = sd_palm_upright(cx=305, y_bot=65, y_top=375, w_bot=150, w_top=215)
    d_thm = sd_chain([(215, 235), (145, 345), (82, 495)], [37, 31, 25], k=14.0)
    d_pnk = upright_finger_sdf(395, 355, 495, 655, 26, 21)
    cv.add_layer(smin(smin(d_palm, d_thm, 20.0), d_pnk, 18.0))
    for fx, yk in [(232, 475), (292, 488), (350, 475)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 295, r_top=27, r_tip=24))


def draw_Z(cv):
    d_palm = sd_palm_upright(cx=275, y_bot=55, y_top=335, w_bot=140, w_top=200)
    d_idx = upright_finger_sdf(210, 325, 210, 650, 27, 22)
    cv.add_layer(smin(d_palm, d_idx, 16.0))
    for fx, yk in [(268, 410), (320, 400), (370, 382)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 260, r_top=24, r_tip=21))
    d_thm = sd_chain([(168, 205), (235, 260), (315, 275)], [32, 27, 22], k=12.0)
    cv.add_layer(d_thm)
    z_pts = [(275, 790), (475, 790), (295, 605), (495, 605)]
    cv.add_crease(z_pts, stroke_w=19.0)
    cv.add_arrow_head(495, 605, 1.0, 0.0, length=42.0, wing=28.0, stroke_w=18.0)


def draw_0(cv): draw_O(cv)


def draw_1(cv):
    d_palm = sd_palm_upright(cx=315, y_bot=65, y_top=380, w_bot=155, w_top=220)
    d_idx = upright_finger_sdf(235, 375, 235, 795, 30, 25)
    cv.add_layer(smin(d_palm, d_idx, 18.0))
    for fx, yk in [(298, 465), (355, 455), (410, 435)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 295, r_top=26, r_tip=23))
    d_thm = sd_chain([(190, 235), (265, 295), (355, 315)], [35, 29, 24], k=12.0)
    cv.add_layer(d_thm)


def draw_2(cv): draw_V(cv)


def draw_3(cv):
    d_palm = sd_palm_upright(cx=320, y_bot=65, y_top=380, w_bot=155, w_top=220)
    d_thm = sd_chain([(220, 235), (150, 355), (92, 520)], [37, 31, 25], k=14.0)
    cv.add_layer(smin(d_palm, d_thm, 20.0))
    cv.add_layer(upright_finger_sdf(248, 375, 228, 785, 28, 24))
    cv.add_layer(upright_finger_sdf(312, 375, 332, 795, 28, 24))
    for fx, yk in [(372, 455), (425, 435)]:
        cv.add_layer(curled_finger_sdf(fx, yk, 295, r_top=26, r_tip=23))


def draw_4(cv):
    d_palm = sd_palm_upright(cx=310, y_bot=65, y_top=390, w_bot=155, w_top=230)
    cv.add_layer(d_palm)
    for x0, y0, x1, y1, rb, rt in [
        (215, 380, 148, 755, 27, 23),
        (275, 385, 255, 798, 28, 24),
        (335, 385, 362, 770, 27, 23),
        (392, 368, 458, 690, 25, 21),
    ]:
        cv.add_layer(upright_finger_sdf(x0, y0, x1, y1, rb, rt))
    d_thm = sd_chain([(188, 225), (265, 295), (365, 315)], [36, 30, 25], k=14.0)
    cv.add_layer(d_thm)


def draw_5(cv):
    d_palm = sd_palm_upright(cx=325, y_bot=65, y_top=390, w_bot=155, w_top=225)
    d_thm = sd_chain([(225, 235), (145, 345), (78, 495)], [37, 31, 25], k=14.0)
    cv.add_layer(smin(d_palm, d_thm, 20.0))
    for x0, y0, x1, y1, rb, rt in [
        (232, 380, 182, 760, 27, 23),
        (288, 385, 278, 800, 28, 24),
        (345, 382, 378, 770, 27, 23),
        (398, 365, 472, 690, 25, 21),
    ]:
        cv.add_layer(upright_finger_sdf(x0, y0, x1, y1, rb, rt))
    add_palm_creases(cv, d_palm, cx=325, y_base=210)


def draw_6(cv):
    d_palm = sd_palm_upright(cx=305, y_bot=65, y_top=385, w_bot=155, w_top=230)
    cv.add_layer(d_palm)
    cv.add_layer(upright_finger_sdf(208, 375, 168, 765, 27, 23))
    cv.add_layer(upright_finger_sdf(268, 380, 268, 800, 28, 24))
    cv.add_layer(upright_finger_sdf(328, 375, 365, 765, 27, 23))
    d_pnk = sd_chain([(402, 365), (425, 435), (362, 325)], [25, 23, 21], k=10.0)
    d_thm = sd_chain([(188, 225), (265, 275), (345, 312)], [35, 28, 23], k=12.0)
    cv.add_layer(d_pnk)
    cv.add_layer(d_thm)


def draw_7(cv):
    d_palm = sd_palm_upright(cx=305, y_bot=65, y_top=385, w_bot=155, w_top=230)
    cv.add_layer(d_palm)
    cv.add_layer(upright_finger_sdf(208, 375, 168, 765, 27, 23))
    cv.add_layer(upright_finger_sdf(268, 380, 262, 800, 28, 24))
    cv.add_layer(upright_finger_sdf(402, 365, 455, 705, 25, 21))
    d_rng = sd_chain([(338, 380), (355, 455), (322, 325)], [26, 24, 22], k=10.0)
    d_thm = sd_chain([(188, 225), (252, 275), (312, 312)], [35, 28, 23], k=12.0)
    cv.add_layer(d_rng)
    cv.add_layer(d_thm)


def draw_8(cv):
    d_palm = sd_palm_upright(cx=305, y_bot=65, y_top=385, w_bot=155, w_top=230)
    cv.add_layer(d_palm)
    cv.add_layer(upright_finger_sdf(208, 375, 165, 765, 27, 23))
    cv.add_layer(upright_finger_sdf(342, 375, 372, 765, 27, 23))
    cv.add_layer(upright_finger_sdf(402, 365, 458, 700, 25, 21))
    d_mid = sd_chain([(276, 385), (282, 465), (278, 325)], [27, 25, 22], k=10.0)
    d_thm = sd_chain([(188, 225), (235, 275), (274, 312)], [35, 28, 23], k=12.0)
    cv.add_layer(d_mid)
    cv.add_layer(d_thm)


def draw_9(cv): draw_F(cv)


BUILDERS = {
    "A": draw_A, "B": draw_B, "C": draw_C, "D": draw_D,
    "E": draw_E, "F": draw_F, "G": draw_G, "H": draw_H,
    "I": draw_I, "J": draw_J, "K": draw_K, "L": draw_L,
    "M": draw_M, "N": draw_N, "O": draw_O, "P": draw_P,
    "Q": draw_Q, "R": draw_R, "S": draw_S, "T": draw_T,
    "U": draw_U, "V": draw_V, "W": draw_W, "X": draw_X,
    "Y": draw_Y, "Z": draw_Z,
    "0": draw_0, "1": draw_1, "2": draw_2, "3": draw_3,
    "4": draw_4, "5": draw_5, "6": draw_6, "7": draw_7,
    "8": draw_8, "9": draw_9,
}


def set_clean_names(name_table, fam, sub, full, ps, version_str):
    records = {
        0: "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)",
        1: fam,
        2: sub,
        3: f"3.102;PGUL;{ps}",
        4: full,
        5: version_str,
        6: ps,
        13: "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
        14: "https://openfontlicense.org",
    }
    for nid, val in records.items():
        name_table.setName(val, nid, 3, 1, 0x0409)
        name_table.names = [
            r for r in name_table.names
            if not (r.nameID == nid and (r.platformID != 3 or r.platEncID != 1 or r.langID != 0x0409))
        ]


def compile_volumetric_font():
    print("=== POCKETGULL Z-LAYERED ANATOMICAL ASL & SIGN FONT COMPILER ===")
    if not SRC_MONO.is_file():
        print(f"[ERROR] Required base font missing: {SRC_MONO}")
        sys.exit(1)

    font = TTFont(str(SRC_MONO))
    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics
    cmap = font.getBestCmap()
    glyph_order = font.getGlyphOrder()

    for char, builder in BUILDERS.items():
        cv = ZCanvas(stroke_w=24.0)
        builder(cv)
        glyph = cv.to_tt_glyph(glyf)
        glyph.recalcBounds(glyf)

        cp = ord(char)
        gname = cmap.get(cp, char)
        if gname not in glyf:
            gname = f"uni{cp:04X}"
            if gname not in glyph_order:
                glyph_order.append(gname)
                font.setGlyphOrder(glyph_order)
        glyf[gname] = glyph
        hmtx[gname] = (ADVANCE, glyph.xMin if glyph.numberOfContours > 0 else 20)

    for sub in font["cmap"].tables:
        if sub.isUnicode():
            for lo, hi in zip("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                if ord(hi) in sub.cmap:
                    sub.cmap[ord(lo)] = sub.cmap[ord(hi)]

    xmin_all, ymin_all, xmax_all, ymax_all = 32767, 32767, -32768, -32768
    for gn in font.getGlyphOrder():
        g = glyf[gn]
        g.recalcBounds(glyf)
        if g.numberOfContours > 0:
            g.flags = bytearray([fl & 0x3F for fl in g.flags])
            xmin_all = min(xmin_all, g.xMin)
            ymin_all = min(ymin_all, g.yMin)
            xmax_all = max(xmax_all, g.xMax)
            ymax_all = max(ymax_all, g.yMax)

    head = font["head"]
    os2 = font["OS/2"]
    head.xMin, head.yMin, head.xMax, head.yMax = xmin_all, ymin_all, xmax_all, ymax_all
    head.fontRevision = 3.102
    os2.usWinAscent = max(os2.usWinAscent, max(0, ymax_all))
    os2.usWinDescent = max(os2.usWinDescent, max(0, -ymin_all))
    os2.fsType = 0
    os2.ulUnicodeRange2 |= (1 << 25)
    os2.fsSelection |= (1 << 7)

    ver = "Version 3.102; The PocketGull Project Authors; OFL 1.1"
    set_clean_names(font["name"], "PocketGull Sign", "Regular", "PocketGull Sign", "PocketGull-Sign", ver)
    font.save(str(OUT_SIGN_TTF))

    set_clean_names(font["name"], "PocketGull ASL", "Regular", "PocketGull ASL", "PocketGull-ASL", ver)
    font.save(str(OUT_ASL_TTF))
    font.close()
    print("Compiled refined PocketGull-Sign.ttf & PocketGull-ASL.ttf!")


if __name__ == "__main__":
    compile_volumetric_font()
