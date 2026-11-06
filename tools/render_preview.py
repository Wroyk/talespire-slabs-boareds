#!/usr/bin/env python3
"""Render the generated layout: as an overlay on a plan image (if given) or standalone."""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import build_grasshopper as bg  # noqa: E402


def render(out_png, plan_png=None, X0=117.0, Y0=164.0, P=59.1):
    floor, diag, edges, diag_walls, ring, tier, round_cells = bg.main(os.path.join(os.path.dirname(__file__), "..", "grasshopper"))
    if plan_png:
        im = Image.open(plan_png).convert("RGBA")
    else:
        X0, Y0, P = 20, 20, 24
        im = Image.new("RGBA", (int(X0 * 2 + P * bg.NCOLS), int(Y0 * 2 + P * bg.NROWS)), "white")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    def px(c, r):
        return (X0 + P * c, Y0 + P * r)

    for (c, r) in ring:
        d.rectangle([px(c, r), px(c + 1, r + 1)], fill=(90, 90, 90, 120))
    for (c, r) in floor - bg.HOLE_CELLS:
        d.rectangle([px(c, r), px(c + 1, r + 1)], fill=(0, 160, 255, 70))
    for (c, r) in bg.HOLE_CELLS:
        d.rectangle([px(c, r), px(c + 1, r + 1)], fill=(0, 0, 0, 255))
    for (c, r) in diag:
        d.rectangle([px(c, r), px(c + 1, r + 1)], fill=(255, 200, 0, 90))
    colors = {"wall": (220, 0, 0, 230), "door": (0, 170, 0, 230), "door2": (0, 170, 0, 230), "hatch": (170, 0, 170, 230)}
    for (c, r), rot in round_cells.items():
        cx, cy = {0: (c, r + 1), 90: (c, r), 180: (c + 1, r), 270: (c + 1, r + 1)}[rot]
        start = {0: 270, 90: 0, 180: 90, 270: 180}[rot]
        x0, y0 = px(cx - 1, cy - 1)
        x1, y1 = px(cx + 1, cy + 1)
        d.arc([x0, y0, x1, y1], start=start, end=start + 90, fill=(220, 0, 0, 230), width=6)
    for (axis, c, r), kind in edges.items():
        if kind == "none":
            continue
        col = colors[kind]
        w = 6 if kind == "wall" else 10
        if axis == "h":
            d.line([px(c, r), px(c + 1, r)], fill=col, width=w)
        else:
            d.line([px(c, r), px(c, r + 1)], fill=col, width=w)
    for seg in diag_walls:
        (c0, r0), (c1, r1) = seg[0], seg[1]
        col = (0, 170, 0, 230) if len(seg) > 2 else (220, 0, 0, 230)
        d.line([px(c0, r0), px(c1, r1)], fill=col, width=6)
    for (c, r) in tier:
        for (dc, dr, a, b) in ((0, -1, (c, r), (c + 1, r)), (0, 1, (c, r + 1), (c + 1, r + 1)),
                               (-1, 0, (c, r), (c, r + 1)), (1, 0, (c + 1, r), (c + 1, r + 1))):
            if (c + dc, r + dr) not in tier:
                d.line([px(*a), px(*b)], fill=(255, 120, 0, 255), width=4)
    for key, x, ry, rot in bg.P:
        cx, cy = px(x, ry)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=(0, 0, 0, 255), fill=(255, 255, 255, 200), width=2)
        d.text((cx + 10, cy - 6), key, fill=(0, 0, 200, 255))
    for key, x, ry, rot, y in bg.X:
        cx, cy = px(x, ry)
        col = (255, 120, 0, 255) if y >= bg.ROOF_Y else (0, 120, 0, 255)
        d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], outline=col, fill=(255, 255, 255, 180), width=2)
        d.text((cx + 8, cy - 6), key, fill=col)
    if not plan_png:
        for name, cells in bg.ROOMS.items():
            cx = sum(c for c, r in cells) / len(cells) + 0.5
            cy = sum(r for c, r in cells) / len(cells) + 0.5
            d.text((px(cx, cy)[0] - 4 * len(name) / 2, px(cx, cy)[1] + 12), name, fill=(120, 0, 0, 255))
        for c in range(0, bg.NCOLS + 1, 5):
            d.text((px(c, 0)[0] + 2, 2), str(c), fill=(0, 0, 0, 255))
        for r in range(0, bg.NROWS + 1, 5):
            d.text((2, px(0, r)[1] + 2), str(r), fill=(0, 0, 0, 255))
        for c in range(bg.NCOLS + 1):
            d.line([px(c, 0), px(c, bg.NROWS)], fill=(200, 200, 200, 255), width=1)
        for r in range(bg.NROWS + 1):
            d.line([px(0, r), px(bg.NCOLS, r)], fill=(200, 200, 200, 255), width=1)
    im = Image.alpha_composite(im, ov).convert("RGB")
    im.save(out_png)
    print("wrote", out_png)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
