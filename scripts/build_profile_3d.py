#!/usr/bin/env python3
"""
Render every 3D panel the profile README shows.

    python3 scripts/build_profile_3d.py --theme azure     --out profile-3d
    python3 scripts/build_profile_3d.py --theme azure-dark --out profile-3d --suffix -dark

Content comes from profile.config.json; geometry and palette come from
isokit.py. Stdlib only.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import isokit as k  # noqa: E402

W = 1000


# ---------------------------------------------------------------------------
# hero
# ---------------------------------------------------------------------------

def panel_hero(cfg, t):
    H = 420
    s = ['<ellipse cx="700" cy="250" rx="420" ry="190" fill="url(#glow)"/>']

    # Text block, left.
    s.append('<text x="54" y="118" class="h1">%s</text>' % k.esc(cfg["name"]))
    s.append('<rect x="54" y="136" width="300" height="3" rx="2" '
             'fill="url(#rule)"/>')
    s.append('<text x="54" y="178" class="sub">%s &#183; %s</text>'
             % (k.esc(cfg["role"]), k.esc(cfg["location"])))

    # Intro, wrapped by hand so it never overflows the panel.
    words, line, lines = cfg["intro"].split(), "", []
    for word in words:
        trial = (line + " " + word).strip()
        if len(trial) > 52:
            lines.append(line)
            line = word
        else:
            line = trial
    lines.append(line)
    for i, ln in enumerate(lines[:4]):
        s.append('<text x="54" y="%d" class="body">%s</text>'
                 % (218 + i * 21, k.esc(ln)))

    # Tagline chips.
    x = 54
    for i, part in enumerate(cfg["tagline"].rstrip(".").split(". ")):
        fill = t["accent"] if i % 2 == 0 else t["accent2"]
        svg, w = k.chip(x, 318, part.upper(), t,
                        fill=k.mix(t["slab"], fill, 0.14), fg=fill)
        s.append(svg)
        x += w + 8

    # Isometric "control centre": a plate with a cluster of towers on it.
    ox, oy, tw, th = 700, 196, 58, 29
    s.append(k.platform(ox - 3 * tw / 2.0, oy, 5, 5, tw, th, t,
                        color=k.mix(t["ground"], t["accent"], 0.10)))

    towers = [
        (0, 0, 54, t["accent"]), (1, 0, 30, k.mix(t["accent"], t["bg1"], .35)),
        (2, 0, 72, t["accent2"]),
        (0, 1, 38, k.mix(t["accent"], t["bg1"], .2)), (1, 1, 92, t["accent"]),
        (2, 1, 46, k.mix(t["accent2"], t["bg1"], .3)),
        (0, 2, 66, t["accent2"]), (1, 2, 42, t["accent"]),
        (2, 2, 58, k.mix(t["accent"], t["accent2"], .5)),
        (3, 1, 26, k.mix(t["accent"], t["bg1"], .45)),
        (1, 3, 34, k.mix(t["accent2"], t["bg1"], .4)),
    ]
    towers.sort(key=lambda c: c[0] + c[1])
    base_x = ox - 3 * tw / 2.0
    for gx, gy, h, color in towers:
        px, py = k.project(gx + 0.5, gy + 0.5, base_x, oy, tw, th)
        s.append(k.ground_shadow(px, py, tw, th, t, 0.8))
        s.append(k.box(px, py, tw * 0.80, th * 0.80, h, color))

    s.append('<text x="54" y="%d" class="foot">@%s</text>'
             % (H - 26, k.esc(cfg["handle"])))
    return k.document(W, H, t, '<g class="rise">%s</g>' % "".join(s),
                      title="%s — %s" % (cfg["name"], cfg["role"]))


# ---------------------------------------------------------------------------
# technology stack
# ---------------------------------------------------------------------------

def panel_stack(cfg, t):
    items = cfg["stack"]
    cols = 6
    rows = (len(items) + cols - 1) // cols
    row_pitch = 168
    H = 150 + rows * row_pitch

    s = [k.section_heading(54, 56, "TECHNOLOGY STACK", t, 320)]
    s.append('<text x="54" y="88" class="body">Tower height tracks how much '
             'of the day-to-day actually runs on it.</text>')

    tw, th = 92, 46
    for i, item in enumerate(items):
        col, row = i % cols, i // cols
        cx = 112 + col * 156
        cy = 232 + row * row_pitch
        h = 26 + item["weight"] * 78
        s.append(k.ground_shadow(cx, cy, tw, th, t, 1.05))
        s.append(k.box(cx, cy, tw, th, h, item["color"]))
        # A thin band of the brand colour ties the label to its tower.
        s.append('<rect x="%g" y="%g" width="26" height="3" rx="2" '
                 'fill="%s"/>' % (cx - 13, cy + th / 2.0 + 16, item["color"]))
        s.append('<text x="%g" y="%g" text-anchor="middle" class="lblb">%s'
                 '</text>' % (cx, cy + th / 2.0 + 38, k.esc(item["name"])))

    return k.document(W, H, t, '<g class="rise">%s</g>' % "".join(s),
                      title="Technology stack")


# ---------------------------------------------------------------------------
# delivery pipeline
# ---------------------------------------------------------------------------

def panel_pipeline(cfg, t):
    stages = cfg["pipeline"]
    H = 430
    s = [k.section_heading(54, 56, "DELIVERY PIPELINE", t, 320)]
    s.append('<text x="54" y="88" class="body">Every commit walks this path '
             'before anything reaches a cluster.</text>')

    n = len(stages)
    span = W - 170
    step = span / float(n - 1)
    base_y = 268
    tw, th = 78, 39

    # Conveyor plate running under the whole run of stages.
    plate = []
    for i in range(n):
        cx = 85 + i * step
        plate.append((cx, base_y))
    s.append('<polygon points="%s" fill="%s" opacity="0.65"/>'
             % (" ".join("%g,%g" % (x, y + th / 2.0 + 4) for x, y in plate)
                + " " + " ".join("%g,%g" % (x, y - th / 2.0 - 4)
                                 for x, y in reversed(plate)),
                t["ground"]))

    # Connectors first so the solids paint over them.
    for i in range(n - 1):
        x1 = 85 + i * step
        x2 = 85 + (i + 1) * step
        s.append(k.beam(x1 + tw * 0.42, base_y - 14, x2 - tw * 0.42,
                        base_y - 14, t["accent"], 2.5, dash="1 7",
                        opacity="0.6"))

    for i, stage in enumerate(stages):
        cx = 85 + i * step
        h = 46 if i % 2 == 0 else 62
        s.append(k.ground_shadow(cx, base_y, tw, th, t))
        s.append(k.box(cx, base_y, tw, th, h, stage["color"]))
        s.append('<text x="%g" y="%g" text-anchor="middle" class="tile" '
                 'fill="%s">%d</text>'
                 % (cx, base_y - h + 4, k.readable_on(stage["color"]), i + 1))
        s.append('<text x="%g" y="%g" text-anchor="middle" class="lblb">%s'
                 '</text>' % (cx, base_y + th / 2.0 + 30,
                              k.esc(stage["stage"])))
        # Tool names can be long; split on the separator onto two lines.
        for j, piece in enumerate(stage["tool"].split(" · ")):
            s.append('<text x="%g" y="%g" text-anchor="middle" class="lbl">%s'
                     '</text>' % (cx, base_y + th / 2.0 + 50 + j * 16,
                                  k.esc(piece)))

    s.append('<text x="54" y="%d" class="foot">build &#8594; verify &#8594; '
             'sign &#8594; admit &#8594; watch</text>' % (H - 26))
    return k.document(W, H, t, '<g class="rise">%s</g>' % "".join(s),
                      title="Delivery pipeline")


# ---------------------------------------------------------------------------
# featured projects
# ---------------------------------------------------------------------------

def panel_projects(cfg, t):
    projects = cfg["projects"][:3]
    H = 470
    s = [k.section_heading(54, 56, "FEATURED ENGINEERING WORK", t, 320)]

    col_w = 288
    gap = 20
    x0 = 54
    for i, p in enumerate(projects):
        x = x0 + i * (col_w + gap)
        cy = 196

        # Pedestal the card sits on.
        px = x + col_w / 2.0
        s.append(k.ground_shadow(px, cy, 150, 75, t))
        s.append(k.box(px, cy, 150, 75, 34, p["color"]))
        s.append('<text x="%g" y="%g" text-anchor="middle" class="tile" '
                 'fill="%s">%02d</text>'
                 % (px, cy - 34 + 6, k.readable_on(p["color"]), i + 1))

        # Info card.
        card_y = cy + 56
        s.append(k.card(x, card_y, col_w, 196, t, accent=p["color"]))

        # Title, wrapped to two lines.
        words, line, lines = p["title"].split(), "", []
        for word in words:
            trial = (line + " " + word).strip()
            if len(trial) > 22:
                lines.append(line)
                line = word
            else:
                line = trial
        lines.append(line)
        for j, ln in enumerate(lines[:2]):
            s.append('<text x="%g" y="%g" class="lblb" '
                     'style="font-size:15px">%s</text>'
                     % (x + 20, card_y + 36 + j * 20, k.esc(ln)))

        # Blurb.
        words, line, blines = p["blurb"].split(), "", []
        for word in words:
            trial = (line + " " + word).strip()
            if len(trial) > 36:
                blines.append(line)
                line = word
            else:
                line = trial
        blines.append(line)
        top = card_y + 36 + len(lines[:2]) * 20 + 10
        for j, ln in enumerate(blines[:5]):
            s.append('<text x="%g" y="%g" class="body">%s</text>'
                     % (x + 20, top + j * 18, k.esc(ln)))

        # Tag chips.
        tx = x + 20
        for tag in p["tags"]:
            svg, tw_ = k.chip(tx, card_y + 160, tag, t,
                              fill=k.mix(t["slab"], p["color"], 0.12),
                              fg=p["color"])
            if tx + tw_ > x + col_w - 16:
                break
            s.append(svg)
            tx += tw_ + 6

    return k.document(W, H, t, '<g class="rise">%s</g>' % "".join(s),
                      title="Featured engineering work")


# ---------------------------------------------------------------------------
# current focus / footer
# ---------------------------------------------------------------------------

def panel_focus(cfg, t):
    items = cfg["focus"]
    H = 396
    s = [k.section_heading(54, 56, "CURRENT FOCUS", t, 320)]

    n = len(items)
    step = (W - 200) / float(n)
    base_y = 232
    tw, th = 88, 44

    for i, item in enumerate(items):
        cx = 100 + i * step + step / 2.0
        h = 34 + item["weight"] * 74
        s.append(k.ground_shadow(cx, base_y, tw, th, t))
        s.append(k.box(cx, base_y, tw, th, h, item["color"]))
        for j, piece in enumerate(item["name"].split(" / ")):
            s.append('<text x="%g" y="%g" text-anchor="middle" class="lbl">%s'
                     '</text>' % (cx, base_y + th / 2.0 + 28 + j * 16,
                                  k.esc(piece)))

    s.append('<rect x="%d" y="%d" width="340" height="2" rx="1" '
             'fill="url(#rule)" opacity="0.7"/>' % (W / 2 - 170, H - 76))
    s.append('<text x="%d" y="%d" text-anchor="middle" class="lblb" '
             'style="letter-spacing:3px">%s</text>'
             % (W / 2, H - 46, k.esc(cfg["tagline"].upper())))
    s.append('<text x="%d" y="%d" text-anchor="middle" class="foot">'
             'panels generated from profile.config.json &#183; refreshed '
             'daily</text>' % (W / 2, H - 24))

    return k.document(W, H, t, '<g class="rise">%s</g>' % "".join(s),
                      title="Current focus")


# ---------------------------------------------------------------------------

PANELS = {
    "hero": panel_hero,
    "stack": panel_stack,
    "pipeline": panel_pipeline,
    "projects": panel_projects,
    "focus": panel_focus,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="profile.config.json")
    ap.add_argument("--theme", default="azure")
    ap.add_argument("--out", default="profile-3d")
    ap.add_argument("--suffix", default="",
                    help='appended to each filename, e.g. "-dark"')
    ap.add_argument("--only", default="",
                    help="comma-separated panel names; default is all")
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as fh:
        cfg = json.load(fh)

    t = k.theme(args.theme)
    os.makedirs(args.out, exist_ok=True)

    wanted = [p.strip() for p in args.only.split(",") if p.strip()] or \
        list(PANELS)
    for name in wanted:
        if name not in PANELS:
            sys.exit("Unknown panel %r. Known: %s"
                     % (name, ", ".join(sorted(PANELS))))
        svg = PANELS[name](cfg, t)
        path = os.path.join(args.out, "%s%s.svg" % (name, args.suffix))
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        print("wrote %s (%.1f KB)" % (path, len(svg) / 1024.0))


if __name__ == "__main__":
    main()
