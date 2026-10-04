"""
Shared isometric drawing kit for the profile panels.

Everything the README shows is drawn through this module so the panels read
as one system: same projection, same light direction, same palette.

Projection is 2:1 isometric. A tile at grid (gx, gy) lands at

    sx = ox + (gx - gy) * tw / 2
    sy = oy + (gx + gy) * th / 2

Light comes from the upper left, so for any solid:

    top face   = base colour
    right face = base * 0.72
    left face  = base * 0.50

Stdlib only, no dependencies.
"""

# ---------------------------------------------------------------------------
# palette
# ---------------------------------------------------------------------------

THEMES = {
    # Matches the Azure branding the profile already uses.
    "azure": {
        "bg0": "#f5f9ff",
        "bg1": "#e6f0fb",
        "grid": "#d7e4f3",
        "text": "#1a3a5c",
        "muted": "#5b7694",
        "faint": "#8ca4bd",
        "accent": "#0078d4",
        "accent2": "#00b7c3",
        "empty": "#d8e5f4",
        "levels": ["#c3dcf4", "#86bde9", "#3f9ade", "#0078d4", "#00b7c3"],
        "slab": "#ffffff",
        "slab_edge": "#cfdceb",
        "ground": "#dce8f6",
        "shadow": "#9fb6cf",
        "shadow_op": "0.30",
    },
    "azure-dark": {
        "bg0": "#0a1628",
        "bg1": "#0f2038",
        "grid": "#17304f",
        "text": "#e6f0fa",
        "muted": "#7f9bbb",
        "faint": "#5d7a9b",
        "accent": "#29a8ff",
        "accent2": "#00d4e0",
        "empty": "#17293f",
        "levels": ["#17304f", "#1c5fa8", "#0078d4", "#29a8ff", "#00d4e0"],
        "slab": "#10203a",
        "slab_edge": "#1d3350",
        "ground": "#12233c",
        "shadow": "#030911",
        "shadow_op": "0.55",
    },
}


def theme(name):
    try:
        return THEMES[name]
    except KeyError:
        raise SystemExit("Unknown theme %r. Known: %s"
                         % (name, ", ".join(sorted(THEMES))))


# ---------------------------------------------------------------------------
# colour helpers
# ---------------------------------------------------------------------------


def shade(hex_color, factor):
    """factor < 1 darkens, > 1 lightens, clamped to the byte range."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(
        max(0, min(255, int(c * factor))) for c in (r, g, b))


def mix(a, b, t):
    """Blend two hex colours; t=0 gives a, t=1 gives b."""
    a, b = a.lstrip("#"), b.lstrip("#")
    out = []
    for i in (0, 2, 4):
        ca, cb = int(a[i:i + 2], 16), int(b[i:i + 2], 16)
        out.append(int(round(ca + (cb - ca) * t)))
    return "#%02x%02x%02x" % tuple(out)


def readable_on(bg):
    """Pick near-black or near-white text for a given background."""
    h = bg.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    luma = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    return "#0d1b2a" if luma > 0.62 else "#ffffff"


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def human(n):
    n = int(n)
    if n >= 1000000:
        return "%.1fM" % (n / 1000000.0)
    if n >= 1000:
        return "%.1fk" % (n / 1000.0)
    return str(n)


# ---------------------------------------------------------------------------
# projection
# ---------------------------------------------------------------------------


def project(gx, gy, ox, oy, tw, th):
    """Grid coordinate to screen coordinate (centre of the tile's base)."""
    return ox + (gx - gy) * (tw / 2.0), oy + (gx + gy) * (th / 2.0)


# ---------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------


def diamond(x, y, tw, th, fill, opacity=None, extra=""):
    """Flat isometric tile centred on its left/right corners at (x, y)."""
    hw, hh = tw / 2.0, th / 2.0
    op = '' if opacity is None else ' opacity="%s"' % opacity
    return ('<polygon points="%g,%g %g,%g %g,%g %g,%g" fill="%s"%s%s/>'
            % (x, y - hh, x + hw, y, x, y + hh, x - hw, y, fill, op, extra))


def box(x, y, tw, th, h, color, extra="", top_extra=""):
    """
    A cube whose base diamond is centred at (x, y), rising h pixels.

    Returns left and right faces first so the top face paints over them.
    """
    hw, hh = tw / 2.0, th / 2.0
    top = color
    right = shade(color, 0.72)
    left = shade(color, 0.50)

    parts = []
    if h > 0.5:
        parts.append('<polygon points="%g,%g %g,%g %g,%g %g,%g" fill="%s"/>'
                     % (x - hw, y - h, x, y - h + hh, x, y + hh, x - hw, y,
                        left))
        parts.append('<polygon points="%g,%g %g,%g %g,%g %g,%g" fill="%s"/>'
                     % (x + hw, y - h, x, y - h + hh, x, y + hh, x + hw, y,
                        right))
    parts.append('<polygon points="%g,%g %g,%g %g,%g %g,%g" fill="%s"%s/>'
                 % (x, y - h - hh, x + hw, y - h, x, y - h + hh, x - hw, y - h,
                    top, top_extra))
    return "".join(parts) + extra


def slab(x, y, tw, th, h, color, t, label=None, value=None):
    """A wide low block, optionally with flat text sitting on top of it."""
    parts = [ground_shadow(x, y, tw * 1.12, th * 1.12, t),
             box(x, y, tw, th, h, color)]
    if value is not None:
        parts.append('<text x="%g" y="%g" text-anchor="middle" class="slabv">'
                     '%s</text>' % (x, y - h + th * 0.10, esc(value)))
    if label is not None:
        parts.append('<text x="%g" y="%g" text-anchor="middle" class="slabl">'
                     '%s</text>' % (x, y + th / 2.0 + 20, esc(label)))
    return "".join(parts)


def ground_shadow(x, y, tw, th, t, scale=1.0):
    """Soft contact shadow under a solid."""
    return ('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="%s" '
            'opacity="%s" filter="url(#soft)"/>'
            % (x, y + th * 0.10, tw * 0.52 * scale, th * 0.50 * scale,
               t["shadow"], t["shadow_op"]))


def platform(ox, oy, cols, rows, tw, th, t, color=None, rim=True):
    """
    A flat isometric plate spanning cols x rows tiles, used as the ground
    every other solid sits on.
    """
    color = color or t["ground"]
    # Corners in projection order: top, right, bottom, left.
    top_c, right_c, bottom_c, left_c = (
        project(gx, gy, ox, oy, tw, th)
        for gx, gy in ((0, 0), (cols, 0), (cols, rows), (0, rows)))
    top = " ".join("%g,%g" % p
                   for p in (top_c, right_c, bottom_c, left_c))

    parts = []
    if rim:
        depth = th * 0.55
        # Only the two front edges are visible: left->bottom, bottom->right.
        for (a, b), factor in (((left_c, bottom_c), 0.78),
                               ((bottom_c, right_c), 0.64)):
            parts.append(
                '<polygon points="%g,%g %g,%g %g,%g %g,%g" fill="%s"/>'
                % (a[0], a[1], b[0], b[1], b[0], b[1] + depth,
                   a[0], a[1] + depth, shade(color, factor)))
    parts.append('<polygon points="%s" fill="%s"/>' % (top, color))
    return "".join(parts)


def beam(x1, y1, x2, y2, color, width=3, dash=None, opacity="1"):
    """A connector between two points, drawn flat so it stays legible."""
    d = '' if dash is None else ' stroke-dasharray="%s"' % dash
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
            'stroke-width="%g" stroke-linecap="round" opacity="%s"%s/>'
            % (x1, y1, x2, y2, color, width, opacity, d))


def chip(x, y, text, t, fill=None, fg=None, pad=11, size=11):
    """A small rounded pill of text. Returns (svg, width)."""
    fill = fill or t["slab"]
    fg = fg or t["muted"]
    w = len(text) * size * 0.58 + pad * 2
    return ('<g><rect x="%g" y="%g" width="%g" height="22" rx="11" fill="%s" '
            'stroke="%s" stroke-width="1"/>'
            '<text x="%g" y="%g" text-anchor="middle" class="chip" '
            'fill="%s">%s</text></g>'
            % (x, y, w, fill, t["slab_edge"], x + w / 2.0, y + 15, fg,
               esc(text)), w)


def card(x, y, w, h, t, accent=None, radius=14):
    """A flat panel that floats above the isometric scene."""
    parts = ['<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" '
             'stroke="%s" stroke-width="1"/>'
             % (x, y, w, h, radius, t["slab"], t["slab_edge"])]
    if accent:
        parts.append('<rect x="%g" y="%g" width="%g" height="3" rx="2" '
                     'fill="%s"/>' % (x + 16, y, w - 32, accent))
    return "".join(parts)


# ---------------------------------------------------------------------------
# document
# ---------------------------------------------------------------------------

BASE_CSS = """
.h1    { font: 700 38px 'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif; fill: %(text)s; }
.h2    { font: 700 27px 'Segoe UI', Ubuntu, sans-serif; fill: %(text)s; }
.sub   { font: 400 16px 'Segoe UI', Ubuntu, sans-serif; fill: %(muted)s; }
.sec   { font: 600 13px 'Segoe UI', Ubuntu, sans-serif; fill: %(muted)s; letter-spacing: 2.6px; }
.lbl   { font: 500 12px 'Segoe UI', Ubuntu, sans-serif; fill: %(muted)s; letter-spacing: .8px; }
.lblb  { font: 700 13px 'Segoe UI', Ubuntu, sans-serif; fill: %(text)s; letter-spacing: .4px; }
.body  { font: 400 13px 'Segoe UI', Ubuntu, sans-serif; fill: %(muted)s; }
.stat  { font: 700 26px 'Segoe UI', Ubuntu, sans-serif; fill: %(text)s; }
.slabv { font: 700 15px 'Segoe UI', Ubuntu, sans-serif; fill: #ffffff; }
.slabl { font: 500 12px 'Segoe UI', Ubuntu, sans-serif; fill: %(muted)s; letter-spacing: .6px; }
.chip  { font: 500 11px 'Segoe UI', Ubuntu, sans-serif; letter-spacing: .4px; }
.foot  { font: 400 11px 'Segoe UI', Ubuntu, sans-serif; fill: %(faint)s; }
.tile  { font: 700 13px 'Segoe UI', Ubuntu, sans-serif; letter-spacing: .3px; }
.rise  { animation: rise 1s cubic-bezier(.2,.8,.3,1) both; }
@keyframes rise { from { opacity: 0; transform: translateY(20px) }
                  to   { opacity: 1; transform: translateY(0) } }
"""


def document(w, h, t, body, title=None, extra_defs="", extra_css=""):
    """Wrap panel content in a complete, self-contained SVG."""
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
           'viewBox="0 0 %d %d" role="img">' % (w, h, w, h)]
    if title:
        out.append("<title>%s</title>" % esc(title))

    out.append("<defs>")
    out.append('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
               '<stop offset="0%%" stop-color="%s"/>'
               '<stop offset="100%%" stop-color="%s"/></linearGradient>'
               % (t["bg0"], t["bg1"]))
    out.append('<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
               '<stop offset="0%%" stop-color="%s"/>'
               '<stop offset="100%%" stop-color="%s" stop-opacity="0"/>'
               '</linearGradient>' % (t["accent"], t["accent2"]))
    out.append('<radialGradient id="glow" cx="50%%" cy="50%%">'
               '<stop offset="0%%" stop-color="%s" stop-opacity="0.22"/>'
               '<stop offset="100%%" stop-color="%s" stop-opacity="0"/>'
               '</radialGradient>' % (t["accent"], t["accent"]))
    out.append('<filter id="soft" x="-60%" y="-60%" width="220%" '
               'height="220%"><feGaussianBlur stdDeviation="7"/></filter>')
    out.append(extra_defs)
    out.append("</defs>")

    out.append("<style>%s%s</style>" % (BASE_CSS % t, extra_css))
    out.append('<rect width="%d" height="%d" rx="18" fill="url(#bg)"/>'
               % (w, h))
    out.append(body)
    out.append("</svg>")
    return "\n".join(out)


def section_heading(x, y, text, t, rule_width=0):
    parts = ['<text x="%g" y="%g" class="sec">%s</text>'
             % (x, y, esc(text))]
    if rule_width:
        parts.append('<rect x="%g" y="%g" width="%g" height="2" rx="1" '
                     'fill="url(#rule)"/>' % (x, y + 10, rule_width))
    return "".join(parts)
