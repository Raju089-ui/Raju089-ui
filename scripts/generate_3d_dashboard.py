#!/usr/bin/env python3
"""
Generate a custom 3D isometric GitHub profile dashboard as a single SVG.

Zero dependencies (stdlib only). Pulls data from the GitHub GraphQL API and
renders an isometric contribution city, language towers and stat slabs.

Usage:
    python3 generate_3d_dashboard.py --user Raju089-ui --theme dark \
        --out profile-3d/dashboard-dark.svg

    python3 generate_3d_dashboard.py --demo --out preview.svg   # no token needed
"""

import argparse
import datetime
import json
import os
import random
import sys
import urllib.error
import urllib.request

API_URL = "https://api.github.com/graphql"

QUERY = """
query($login: String!) {
  user(login: $login) {
    name
    login
    followers { totalCount }
    following { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false,
                 orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      nodes {
        name
        stargazerCount
        forkCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""

# --------------------------------------------------------------------------
# themes
# --------------------------------------------------------------------------

THEMES = {
    "dark": {
        "bg0": "#070b18",
        "bg1": "#0d1428",
        "grid": "#16203a",
        "text": "#e8edf7",
        "muted": "#7c8db5",
        "accent": "#5ad1ff",
        "accent2": "#c084fc",
        "empty": "#151c30",
        "levels": ["#1d2b4a", "#2763c9", "#19a7d4", "#5ad1ff", "#c084fc"],
        "slab": "#121a30",
        "slab_edge": "#1e2a47",
    },
    "light": {
        "bg0": "#f6f8fd",
        "bg1": "#e9eef9",
        "grid": "#d7e0f0",
        "text": "#16203a",
        "muted": "#5b6a8c",
        "accent": "#1668c4",
        "accent2": "#7c3aed",
        "empty": "#dde5f2",
        "levels": ["#b9cdf0", "#6f9fe8", "#2f7fd4", "#1668c4", "#7c3aed"],
        "slab": "#ffffff",
        "slab_edge": "#cfd9ec",
    },
    # Matches the Azure palette the rest of the profile README uses
    # (#0078d4 / #00b7c3 on #f5f9ff, body text #1a3a5c).
    "azure": {
        "bg0": "#f5f9ff",
        "bg1": "#e6f0fb",
        "grid": "#d7e4f3",
        "text": "#1a3a5c",
        "muted": "#5b7694",
        "accent": "#0078d4",
        "accent2": "#00b7c3",
        "empty": "#e1ebf8",
        "levels": ["#c3dcf4", "#86bde9", "#3f9ade", "#0078d4", "#00b7c3"],
        "slab": "#ffffff",
        "slab_edge": "#cfdceb",
    },
    "azure-dark": {
        "bg0": "#0a1628",
        "bg1": "#0f2038",
        "grid": "#17304f",
        "text": "#e6f0fa",
        "muted": "#7f9bbb",
        "accent": "#29a8ff",
        "accent2": "#00d4e0",
        "empty": "#13243c",
        "levels": ["#17304f", "#1c5fa8", "#0078d4", "#29a8ff", "#00d4e0"],
        "slab": "#10203a",
        "slab_edge": "#1d3350",
    },
}

# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------


def shade(hex_color, factor):
    """factor < 1 darkens, > 1 lightens."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    out = []
    for c in (r, g, b):
        v = int(c * factor)
        out.append(max(0, min(255, v)))
    return "#%02x%02x%02x" % tuple(out)


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


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------


def fetch_user(login, token):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": "bearer " + token,
            "Content-Type": "application/json",
            "User-Agent": "profile-3d-dashboard",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        sys.exit("GitHub API error %s: %s" % (exc.code, exc.read().decode()[:400]))

    if payload.get("errors"):
        sys.exit("GraphQL error: " + json.dumps(payload["errors"])[:400])
    if not payload.get("data", {}).get("user"):
        sys.exit("User '%s' not found (or token lacks read:user scope)." % login)
    return payload["data"]["user"]


def demo_user(login):
    """Synthetic data so the design can be previewed without a token."""
    random.seed(7)
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday() + 1 + 52 * 7)
    weeks = []
    for w in range(53):
        days = []
        for d in range(7):
            day = start + datetime.timedelta(days=w * 7 + d)
            if day > today:
                continue
            base = 0 if d in (0, 6) else 3
            burst = 9 if 18 <= w <= 27 else 0
            count = max(0, int(random.gauss(base + burst * 0.4, 3)))
            if random.random() < 0.18:
                count = 0
            days.append({"date": day.isoformat(), "contributionCount": count,
                         "weekday": d})
        weeks.append({"contributionDays": days})

    total = sum(d["contributionCount"] for w in weeks for d in w["contributionDays"])
    langs = [("Python", "#3572A5", 480000), ("Shell", "#89e051", 310000),
             ("HCL", "#844FBA", 265000), ("Go", "#00ADD8", 190000),
             ("JavaScript", "#f1e05a", 150000), ("Dockerfile", "#384d54", 90000)]
    nodes = []
    for name, color, size in langs:
        nodes.append({
            "name": name.lower() + "-lab",
            "stargazerCount": random.randint(3, 90),
            "forkCount": random.randint(0, 20),
            "languages": {"edges": [{"size": size,
                                     "node": {"name": name, "color": color}}]},
        })

    return {
        "name": "Raju Singh",
        "login": login,
        "followers": {"totalCount": 318},
        "following": {"totalCount": 104},
        "repositories": {"totalCount": 42, "nodes": nodes},
        "contributionsCollection": {
            "totalCommitContributions": int(total * 0.74),
            "totalPullRequestContributions": 128,
            "totalIssueContributions": 61,
            "contributionCalendar": {"totalContributions": total, "weeks": weeks},
        },
    }


def flatten_days(user):
    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = []
    for w in weeks:
        for d in w["contributionDays"]:
            days.append(d)
    days.sort(key=lambda d: d["date"])
    return days


def streaks(days):
    best = cur = run = 0
    for d in days:
        if d["contributionCount"] > 0:
            run += 1
            best = max(best, run)
        else:
            run = 0
    # current streak: walk backwards, today with 0 does not break it yet
    for i, d in enumerate(reversed(days)):
        if d["contributionCount"] > 0:
            cur += 1
        elif i == 0:
            continue
        else:
            break
    return cur, best


def top_languages(user, limit=6):
    totals = {}
    colors = {}
    for repo in user["repositories"]["nodes"] or []:
        for edge in (repo.get("languages") or {}).get("edges", []):
            name = edge["node"]["name"]
            totals[name] = totals.get(name, 0) + edge["size"]
            colors[name] = edge["node"].get("color") or "#8b949e"
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:limit]
    grand = sum(totals.values()) or 1
    return [(name, colors[name], size * 100.0 / grand) for name, size in ranked]


# --------------------------------------------------------------------------
# isometric drawing
# --------------------------------------------------------------------------


def iso_box(x, y, tw, th, h, top, right, left, extra=""):
    """One 3D cube drawn from the centre of its base diamond."""
    hw, hh = tw / 2.0, th / 2.0
    top_face = "%g,%g %g,%g %g,%g %g,%g" % (
        x, y - h, x + hw, y - h + hh, x, y - h + th, x - hw, y - h + hh)
    right_face = "%g,%g %g,%g %g,%g %g,%g" % (
        x + hw, y - h + hh, x, y - h + th, x, y + th, x + hw, y + hh)
    left_face = "%g,%g %g,%g %g,%g %g,%g" % (
        x - hw, y - h + hh, x, y - h + th, x, y + th, x - hw, y + hh)
    parts = []
    if h > 0.6:
        parts.append('<polygon points="%s" fill="%s"/>' % (left_face, left))
        parts.append('<polygon points="%s" fill="%s"/>' % (right_face, right))
    parts.append('<polygon points="%s" fill="%s"%s/>' % (top_face, top, extra))
    return "".join(parts)


def contribution_city(days, t, x0, y0, tw=24, th=11, max_h=52):
    """Isometric city: 53 week columns x 7 weekday rows."""
    by_cell = {}
    if not days:
        return "", 0
    first = datetime.date.fromisoformat(days[0]["date"])
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        col = (date - first).days // 7
        row = (date.weekday() + 1) % 7  # Sunday = 0, matches GitHub rows
        by_cell[(col, row)] = d["contributionCount"]

    counts = sorted(c for c in by_cell.values() if c > 0)
    if counts:
        cap = counts[int(len(counts) * 0.93)] or counts[-1]
    else:
        cap = 1
    cap = max(cap, 1)

    cells = sorted(by_cell.items(), key=lambda kv: (kv[0][0] + kv[0][1]))
    out = []
    for (col, row), count in cells:
        x = x0 + (col - row) * (tw / 2.0)
        y = y0 + (col + row) * (th / 2.0)
        if count == 0:
            out.append(iso_box(x, y, tw, th, 0, t["empty"],
                               t["empty"], t["empty"]))
            continue
        ratio = min(count / float(cap), 1.0)
        level = min(int(ratio * 4.999), 4)
        h = 4 + ratio * max_h
        base = t["levels"][level]
        extra = ' class="peak"' if level == 4 else ""
        out.append(iso_box(x, y, tw, th, h, base, shade(base, 0.74),
                           shade(base, 0.52), extra))
    return "".join(out), cap


def language_towers(langs, t, x0, y0, tw=40, th=18, gap=150):
    """Row of isometric towers, one per language, height = share of code."""
    out = []
    if not langs:
        return ""
    top_share = max(l[2] for l in langs) or 1
    for i, (name, color, share) in enumerate(langs):
        x = x0 + i * gap
        y = y0
        h = 18 + (share / top_share) * 60
        out.append(iso_box(x, y, tw, th, h, color, shade(color, 0.72),
                           shade(color, 0.5)))
        out.append(
            '<text x="%g" y="%g" text-anchor="middle" class="lbl">%s</text>'
            % (x, y + th + 22, esc(name)))
        out.append(
            '<text x="%g" y="%g" text-anchor="middle" class="lblv">%.1f%%</text>'
            % (x, y + th + 38, share))
    return "".join(out)


def stat_slab(x, y, w, value, label, t, accent):
    """Flat isometric plate with a number on it."""
    th = 14
    out = [
        '<polygon points="%g,%g %g,%g %g,%g %g,%g" fill="%s" opacity="0.55"/>'
        % (x, y + th, x + w / 2.0, y + th + th / 2.0, x, y + th + th,
           x - w / 2.0, y + th + th / 2.0, shade(accent, 0.35)),
        '<rect x="%g" y="%g" width="%g" height="%g" rx="10" fill="%s" '
        'stroke="%s" stroke-width="1"/>'
        % (x - w / 2.0, y - 46, w, 62, t["slab"], t["slab_edge"]),
        '<rect x="%g" y="%g" width="%g" height="3" rx="2" fill="%s"/>'
        % (x - w / 2.0 + 14, y - 46, w - 28, accent),
        '<text x="%g" y="%g" text-anchor="middle" class="stat">%s</text>'
        % (x, y - 14, esc(value)),
        '<text x="%g" y="%g" text-anchor="middle" class="lbl">%s</text>'
        % (x, y + 6, esc(label)),
    ]
    return "".join(out)


# --------------------------------------------------------------------------
# svg
# --------------------------------------------------------------------------


def build_svg(user, theme_name):
    t = THEMES[theme_name]
    days = flatten_days(user)
    cal = user["contributionsCollection"]["contributionCalendar"]
    cur_streak, best_streak = streaks(days)
    langs = top_languages(user)
    stars = sum(r["stargazerCount"] for r in (user["repositories"]["nodes"] or []))
    cc = user["contributionsCollection"]

    W, H = 1000, 916
    name = user.get("name") or user["login"]
    updated = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%d %b %Y, %H:%M UTC")

    city, cap = contribution_city(days, t, x0=224, y0=342)

    css = """
    .nm   { font: 700 34px 'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif; fill: %(text)s; }
    .sub  { font: 400 15px 'Segoe UI', Ubuntu, sans-serif; fill: %(muted)s; letter-spacing: .5px; }
    .sec  { font: 600 13px 'Segoe UI', Ubuntu, sans-serif; fill: %(muted)s; letter-spacing: 2.6px; }
    .stat { font: 700 25px 'Segoe UI', Ubuntu, sans-serif; fill: %(text)s; }
    .lbl  { font: 500 11px 'Segoe UI', Ubuntu, sans-serif; fill: %(muted)s; letter-spacing: .8px; }
    .lblv { font: 600 11px 'Segoe UI', Ubuntu, sans-serif; fill: %(text)s; }
    .foot { font: 400 11px 'Segoe UI', Ubuntu, sans-serif; fill: %(muted)s; }
    .peak { animation: pulse 3.6s ease-in-out infinite; }
    @keyframes pulse { 0%%,100%% { opacity: 1 } 50%% { opacity: .62 } }
    .rise { animation: rise 1.1s cubic-bezier(.2,.8,.3,1) both; }
    @keyframes rise { from { opacity: 0; transform: translateY(26px) }
                      to   { opacity: 1; transform: translateY(0) } }
    """ % t

    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
             'viewBox="0 0 %d %d" role="img">' % (W, H, W, H))
    s.append("<defs>")
    s.append('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0%%" stop-color="%s"/>'
             '<stop offset="100%%" stop-color="%s"/></linearGradient>'
             % (t["bg0"], t["bg1"]))
    s.append('<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0%%" stop-color="%s"/>'
             '<stop offset="100%%" stop-color="%s" stop-opacity="0"/></linearGradient>'
             % (t["accent"], t["accent2"]))
    s.append('<radialGradient id="glow" cx="50%%" cy="50%%">'
             '<stop offset="0%%" stop-color="%s" stop-opacity="0.26"/>'
             '<stop offset="100%%" stop-color="%s" stop-opacity="0"/></radialGradient>'
             % (t["accent"], t["accent"]))
    s.append("</defs>")
    s.append("<style>%s</style>" % css)

    s.append('<rect width="%d" height="%d" rx="18" fill="url(#bg)"/>' % (W, H))
    s.append('<ellipse cx="500" cy="420" rx="480" ry="220" fill="url(#glow)"/>')

    # header
    s.append('<text x="48" y="62" class="nm">%s</text>' % esc(name))
    s.append('<text x="48" y="88" class="sub">@%s &#183; %d contributions in the last year</text>'
             % (esc(user["login"]), cal["totalContributions"]))
    s.append('<rect x="48" y="104" width="420" height="3" rx="2" fill="url(#rule)"/>')

    # header mini stats (right)
    mini = [
        (human(stars), "STARS EARNED"),
        (human(user["followers"]["totalCount"]), "FOLLOWERS"),
        (human(user["repositories"]["totalCount"]), "REPOSITORIES"),
    ]
    for i, (val, lab) in enumerate(mini):
        x = 668 + i * 126
        s.append('<text x="%d" y="60" text-anchor="middle" class="stat">%s</text>'
                 % (x, esc(val)))
        s.append('<text x="%d" y="80" text-anchor="middle" class="lbl">%s</text>'
                 % (x, lab))

    # stat slabs (horizontal strip under the header)
    slabs = [
        (human(cal["totalContributions"]), "CONTRIBUTIONS", t["accent"]),
        (human(cc["totalCommitContributions"]), "COMMITS", t["accent2"]),
        (human(cc["totalPullRequestContributions"]), "PULL REQUESTS", t["accent"]),
        (str(cur_streak) + "d", "CURRENT STREAK", t["accent2"]),
        (str(best_streak) + "d", "LONGEST STREAK", t["accent"]),
    ]
    for i, (val, lab, accent) in enumerate(slabs):
        s.append(stat_slab(500 + (i - 2) * 186, 196, 168, val, lab, t, accent))

    # contribution city
    s.append('<text x="48" y="306" class="sec">CONTRIBUTION GRID &#183; 52 WEEKS</text>')
    s.append('<g class="rise">%s</g>' % city)

    # languages
    s.append('<text x="48" y="700" class="sec">LANGUAGE FOOTPRINT</text>')
    s.append('<g class="rise">%s</g>'
             % language_towers(langs, t, x0=135, y0=800))

    s.append('<text x="48" y="%d" class="foot">auto-generated &#183; last refresh %s</text>'
             % (H - 22, esc(updated)))
    s.append("</svg>")
    return "\n".join(s)


# --------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=os.environ.get("GITHUB_LOGIN", ""))
    ap.add_argument("--theme", default="dark", choices=sorted(THEMES))
    ap.add_argument("--out", default="profile-3d/dashboard.svg")
    ap.add_argument("--demo", action="store_true",
                    help="render with synthetic data, no API token needed")
    args = ap.parse_args()

    if args.demo:
        user = demo_user(args.user or "Raju089-ui")
    else:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("Set GH_TOKEN (or GITHUB_TOKEN) before running.")
        if not args.user:
            sys.exit("Pass --user <github-login>.")
        user = fetch_user(args.user, token)

    svg = build_svg(user, args.theme)
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("wrote %s (%.1f KB)" % (args.out, len(svg) / 1024.0))


if __name__ == "__main__":
    main()
