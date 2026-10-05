import os
import glob
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
import math

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

def get_glyph_contours(glyf, gname):
    g = glyf[gname]
    coords, end_pts, flags = g.getCoordinates(glyf)
    contours = []
    for i in range(len(end_pts)):
        start = 0 if i == 0 else end_pts[i-1] + 1
        end = end_pts[i] + 1
        pts = coords[start:end]
        y_min = min(y for x,y in pts)
        y_max = max(y for x,y in pts)
        x_min = min(x for x,y in pts)
        x_max = max(x for x,y in pts)
        contours.append({
            'idx': i,
            'start': start,
            'end': end,
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max,
            'pts': pts
        })
    return coords, end_pts, flags, contours

def calibrate_font(font_path):
    fname = font_path.name
    font = TTFont(str(font_path))
    glyf = font["glyf"]

    # 1. Determine Cap Height from 'H'
    cap_y = 714
    if 'H' in glyf:
        _, _, _, h_contours = get_glyph_contours(glyf, 'H')
        cap_y = max(c['y_max'] for c in h_contours)

    italic_angle = font["post"].italicAngle if "post" in font else 0
    tan_a = math.tan(math.radians(-italic_angle)) if italic_angle != 0 else 0

    is_bold = any(k in fname for k in ['Bold', 'Black', 'Chiseltip'])
    is_mono = 'Mono' in fname
    target_gap = 42 if is_bold else 48
    target_top = min(cap_y, 712) if not ('Marker' in fname or 'Mono-Bold' in fname) else min(cap_y, 725)

    print(f"\n--- Calibrating {fname} (Cap: {cap_y}, Target Top: {target_top}, Gap: {target_gap}) ---")

    # 2. Calibrate 'i'
    i_shift_info = None
    if 'i' in glyf and glyf['i'].numberOfContours == 2:
        coords, end_pts, flags, c_list = get_glyph_contours(glyf, 'i')
        # Identify stem vs dot
        if c_list[0]['y_min'] < c_list[1]['y_min']:
            stem_c, dot_c = c_list[0], c_list[1]
        else:
            dot_c, stem_c = c_list[0], c_list[1]

        stem_top = stem_c['y_max']
        dot_start = dot_c['start']
        dot_end = dot_c['end']
        cur_dot_h = dot_c['y_max'] - dot_c['y_min']
        cur_dot_mid_y = (dot_c['y_min'] + dot_c['y_max']) / 2.0
        cur_dot_mid_x = (dot_c['x_min'] + dot_c['x_max']) / 2.0

        target_bot = stem_top + target_gap
        avail_h = target_top - target_bot
        scale_f = avail_h / cur_dot_h if cur_dot_h > avail_h else 1.0

        # Transform dot coordinates
        new_coords = list(coords)
        for idx in range(dot_start, dot_end):
            ox, oy = new_coords[idx]
            # scale around center
            nx = cur_dot_mid_x + (ox - cur_dot_mid_x) * scale_f
            ny = cur_dot_mid_y + (oy - cur_dot_mid_y) * scale_f
            new_coords[idx] = (round(nx), round(ny))

        scaled_pts = new_coords[dot_start:dot_end]
        s_y_min = min(y for x,y in scaled_pts)
        s_y_max = max(y for x,y in scaled_pts)
        dy = target_bot - s_y_min
        dx = dy * tan_a

        final_coords = []
        for idx, (x, y) in enumerate(new_coords):
            if dot_start <= idx < dot_end:
                final_coords.append((int(round(x + dx)), int(round(y + dy))))
            else:
                final_coords.append((int(round(x)), int(round(y))))

        glyf['i'].coordinates = GlyphCoordinates(final_coords)
        glyf['i'].recalcBounds(glyf)

        final_dot = final_coords[dot_start:dot_end]
        f_y_min = min(y for x,y in final_dot)
        f_y_max = max(y for x,y in final_dot)
        print(f"  [i] Cured tittle: [{dot_c['y_min']}, {dot_c['y_max']}] -> [{f_y_min}, {f_y_max}] (gap={f_y_min - stem_top})")
        i_shift_info = (scale_f, dy, stem_top, target_gap, target_top)

    # 3. Calibrate 'j'
    if 'j' in glyf and glyf['j'].numberOfContours == 2 and i_shift_info:
        coords, end_pts, flags, c_list = get_glyph_contours(glyf, 'j')
        if c_list[0]['y_min'] < c_list[1]['y_min']:
            stem_c, dot_c = c_list[0], c_list[1]
        else:
            dot_c, stem_c = c_list[0], c_list[1]

        stem_top = stem_c['y_max']
        dot_start = dot_c['start']
        dot_end = dot_c['end']
        cur_dot_h = dot_c['y_max'] - dot_c['y_min']
        cur_dot_mid_y = (dot_c['y_min'] + dot_c['y_max']) / 2.0
        cur_dot_mid_x = (dot_c['x_min'] + dot_c['x_max']) / 2.0

        target_bot = stem_top + target_gap
        avail_h = target_top - target_bot
        scale_f = avail_h / cur_dot_h if cur_dot_h > avail_h else 1.0

        new_coords = list(coords)
        for idx in range(dot_start, dot_end):
            ox, oy = new_coords[idx]
            nx = cur_dot_mid_x + (ox - cur_dot_mid_x) * scale_f
            ny = cur_dot_mid_y + (oy - cur_dot_mid_y) * scale_f
            new_coords[idx] = (round(nx), round(ny))

        scaled_pts = new_coords[dot_start:dot_end]
        s_y_min = min(y for x,y in scaled_pts)
        dy = target_bot - s_y_min
        dx = dy * tan_a

        final_coords = []
        for idx, (x, y) in enumerate(new_coords):
            if dot_start <= idx < dot_end:
                final_coords.append((int(round(x + dx)), int(round(y + dy))))
            else:
                final_coords.append((int(round(x)), int(round(y))))

        glyf['j'].coordinates = GlyphCoordinates(final_coords)
        glyf['j'].recalcBounds(glyf)

        final_dot = final_coords[dot_start:dot_end]
        f_y_min = min(y for x,y in final_dot)
        f_y_max = max(y for x,y in final_dot)
        print(f"  [j] Cured tittle: [{dot_c['y_min']}, {dot_c['y_max']}] -> [{f_y_min}, {f_y_max}] (gap={f_y_min - stem_top})")

    # 4. Calibrate 'ij'
    if 'ij' in glyf and glyf['ij'].numberOfContours == 4 and i_shift_info:
        coords, end_pts, flags, c_list = get_glyph_contours(glyf, 'ij')
        # In ij, stems are lower, dots are higher
        dots = [c for c in c_list if c['y_min'] > 400]
        stems = [c for c in c_list if c['y_min'] <= 400]
        if len(dots) == 2 and len(stems) == 2:
            stem_top = max(s['y_max'] for s in stems)
            target_bot = stem_top + target_gap
            final_coords = list(coords)
            for d in dots:
                d_start = d['start']
                d_end = d['end']
                cur_h = d['y_max'] - d['y_min']
                avail_h = target_top - target_bot
                scale_f = avail_h / cur_h if cur_h > avail_h else 1.0
                mid_x = (d['x_min'] + d['x_max']) / 2.0
                mid_y = (d['y_min'] + d['y_max']) / 2.0
                
                # scale
                for idx in range(d_start, d_end):
                    ox, oy = final_coords[idx]
                    nx = mid_x + (ox - mid_x) * scale_f
                    ny = mid_y + (oy - mid_y) * scale_f
                    final_coords[idx] = (round(nx), round(ny))
                
                scaled_pts = final_coords[d_start:d_end]
                dy = target_bot - min(y for x,y in scaled_pts)
                dx = dy * tan_a
                for idx in range(d_start, d_end):
                    x, y = final_coords[idx]
                    final_coords[idx] = (int(round(x + dx)), int(round(y + dy)))

            glyf['ij'].coordinates = GlyphCoordinates(final_coords)
            glyf['ij'].recalcBounds(glyf)
            print("  [ij] Cured both tittles.")

    # 5. Calibrate 'i.heart' & 'j.heart'
    for hname in ['i.heart', 'j.heart']:
        if hname in glyf and glyf[hname].numberOfContours == 2 and i_shift_info:
            coords, end_pts, flags, c_list = get_glyph_contours(glyf, hname)
            if c_list[0]['y_min'] < c_list[1]['y_min']:
                stem_c, heart_c = c_list[0], c_list[1]
            else:
                heart_c, stem_c = c_list[0], c_list[1]

            stem_top = stem_c['y_max']
            h_start = heart_c['start']
            h_end = heart_c['end']
            cur_h = heart_c['y_max'] - heart_c['y_min']
            mid_x = (heart_c['x_min'] + heart_c['x_max']) / 2.0
            mid_y = (heart_c['y_min'] + heart_c['y_max']) / 2.0

            target_bot = stem_top + target_gap
            avail_h = target_top - target_bot
            scale_f = avail_h / cur_h if cur_h > avail_h else 1.0

            new_coords = list(coords)
            for idx in range(h_start, h_end):
                ox, oy = new_coords[idx]
                nx = mid_x + (ox - mid_x) * scale_f
                ny = mid_y + (oy - mid_y) * scale_f
                new_coords[idx] = (round(nx), round(ny))

            scaled_pts = new_coords[h_start:h_end]
            dy = target_bot - min(y for x,y in scaled_pts)
            dx = dy * tan_a

            final_coords = []
            for idx, (x, y) in enumerate(new_coords):
                if h_start <= idx < h_end:
                    final_coords.append((int(round(x + dx)), int(round(y + dy))))
                else:
                    final_coords.append((int(round(x)), int(round(y))))

            glyf[hname].coordinates = GlyphCoordinates(final_coords)
            glyf[hname].recalcBounds(glyf)
            f_heart = final_coords[h_start:h_end]
            f_y_min = min(y for x,y in f_heart)
            f_y_max = max(y for x,y in f_heart)
            print(f"  [{hname}] Cured heart tittle: [{heart_c['y_min']}, {heart_c['y_max']}] -> [{f_y_min}, {f_y_max}] (gap={f_y_min - stem_top})")

    font.save(str(font_path))
    print(f"  [SAVED] {fname}")

def main():
    print("=" * 80)
    print("  POCKETGULL FOUNDRY: MASTER TITTLE OPTICAL CALIBRATION (i, j, ij, hearts)")
    print("=" * 80)
    for font_path in sorted(TTF_DIR.glob("*.ttf")):
        calibrate_font(font_path)

if __name__ == "__main__":
    main()
