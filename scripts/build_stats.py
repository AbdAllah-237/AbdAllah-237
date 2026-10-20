"""Builds self-hosted GitHub stats cards (no third-party services).

Runs inside GitHub Actions:  python3 scripts/build_stats.py <out_dir>
Needs env GITHUB_TOKEN and GH_USER. With --demo it renders sample data locally.
"""
import datetime as dt
import json, os, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_cards import (BG, CARD, CARD2, LINE, TEXT, MUTED, CYAN, VIOLET, FONT, MONO,  # noqa: E402
                         esc, defs_common, tw)

USER = os.environ.get("GH_USER", "AbdAllah-237")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
EXCLUDE_LANGS = {"Jupyter Notebook"} if os.environ.get("EXCLUDE_NOTEBOOKS") else set()


def gql(query, variables=None):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json", "User-Agent": USER},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    if "errors" in out:
        raise RuntimeError(out["errors"])
    return out["data"]


def fetch():
    base = gql("""query($u:String!){ user(login:$u){
        name createdAt followers{totalCount}
        repositories(ownerAffiliations:OWNER, isFork:false, first:100){ totalCount nodes{
            stargazerCount
            languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name color } } } } }
        contributionsCollection{ totalCommitContributions totalPullRequestContributions
            totalIssueContributions restrictedContributionsCount } } }""", {"u": USER})["user"]

    days = {}
    start = dt.datetime.fromisoformat(base["createdAt"].replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    y = start
    while y < now:
        to = min(y + dt.timedelta(days=365), now)
        cal = gql("""query($u:String!,$f:DateTime!,$t:DateTime!){ user(login:$u){
            contributionsCollection(from:$f, to:$t){ contributionCalendar{ weeks{ contributionDays{ date contributionCount } } } } } }""",
                  {"u": USER, "f": y.isoformat(), "t": to.isoformat()})
        for w in cal["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
        y = to

    langs = {}
    for repo in base["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            n = e["node"]["name"]
            if n in EXCLUDE_LANGS:
                continue
            langs.setdefault(n, [0, e["node"]["color"] or "#8B949E"])
            langs[n][0] += e["size"]

    cc = base["contributionsCollection"]
    return dict(
        name=base["name"] or USER,
        stars=sum(r["stargazerCount"] for r in base["repositories"]["nodes"]),
        repos=base["repositories"]["totalCount"],
        followers=base["followers"]["totalCount"],
        commits=cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        prs=cc["totalPullRequestContributions"],
        issues=cc["totalIssueContributions"],
        days=dict(sorted(days.items())),
        langs=langs,
    )


def demo():
    import random
    random.seed(4)
    today = dt.date.today()
    days = {(today - dt.timedelta(days=i)).isoformat(): random.choice([0, 0, 0, 1, 2, 3, 5]) for i in range(500)}
    return dict(name="AbdAllah Elmarakby", stars=10, repos=11, followers=4, commits=67, prs=0, issues=0,
                days=dict(sorted(days.items())),
                langs={"Jupyter Notebook": [455, "#DA5B0B"], "TypeScript": [444, "#3178C6"], "PLpgSQL": [73, "#336790"],
                       "Python": [14, "#3572A5"], "CSS": [9, "#663399"], "HTML": [3, "#E34C26"]})


# ───────────────────────────── math ──────────────────────────────
def streaks(days):
    dates = sorted(days)
    total = sum(days.values())
    longest = cur = 0
    best = (None, None)
    run_start = None
    for d in dates:
        if days[d] > 0:
            cur += 1
            run_start = run_start or d
            if cur > longest:
                longest, best = cur, (run_start, d)
        else:
            cur, run_start = 0, None
    # current streak: today may still be 0 without breaking it
    current, i = 0, len(dates) - 1
    if i >= 0 and days[dates[i]] == 0:
        i -= 1
    while i >= 0 and days[dates[i]] > 0:
        current += 1; i -= 1
    first = next((d for d in dates if days[d] > 0), dates[0] if dates else None)
    return total, current, longest, best, first


def fmt_date(s):
    if not s: return "—"
    d = dt.date.fromisoformat(s)
    return d.strftime("%b %d, %Y").replace(" 0", " ")


def frame(W, H, body, extra_defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>{defs_common()}{extra_defs}
  <style>.fade{{animation:fi .9s ease-out both}}@keyframes fi{{from{{opacity:0}}to{{opacity:1}}}}</style>
</defs>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="20" fill="{CARD}" stroke="url(#border)" stroke-width="1.5"/>
{body}
</svg>"""


# ───────────────────────────── cards ─────────────────────────────
def stats_card(s):
    W, H = 590, 240
    items = [("★", "Stars earned", s["stars"]), ("◆", "Commits (this year)", s["commits"]),
             ("⑂", "Pull requests", s["prs"]), ("●", "Issues", s["issues"]),
             ("▣", "Public repos", s["repos"]), ("♥", "Followers", s["followers"])]
    cells = []
    cw, ch = (W - 64 - 24) / 3, 76
    for i, (ic, label, val) in enumerate(items):
        r, c = divmod(i, 3)
        x, y = 32 + c * (cw + 12), 64 + r * (ch + 12)
        cells.append(f"""<g class="fade" style="animation-delay:{i*.08:.2f}s">
  <rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="{ch}" rx="14" fill="{CARD2}" stroke="{LINE}"/>
  <text x="{x+16:.0f}" y="{y+40}" font-size="28" font-weight="800" fill="url(#grad)">{val}</text>
  <text x="{x+16:.0f}" y="{y+62}" font-size="12.5" fill="{MUTED}"><tspan fill="{VIOLET}">{ic}</tspan>  {esc(label)}</text>
</g>""")
    body = f"""<text x="32" y="42" font-size="18" font-weight="800" fill="{TEXT}">GitHub Stats</text>
<text x="{W-32}" y="42" font-family="{MONO}" font-size="12" fill="{CYAN}" text-anchor="end">@{esc(USER)}</text>
{''.join(cells)}"""
    return frame(W, H, body)


def langs_card(s):
    W, H = 590, 240
    total = sum(v[0] for v in s["langs"].values()) or 1
    top = sorted(s["langs"].items(), key=lambda kv: -kv[1][0])[:6]
    bar, x = [], 32
    bw = W - 64
    for name, (size, color) in top:
        w = bw * size / total
        bar.append(f'<rect x="{x:.1f}" y="62" width="{max(w,0):.1f}" height="12" fill="{color}"/>')
        x += w
    rows = []
    for i, (name, (size, color)) in enumerate(top):
        r, c = divmod(i, 2)
        X, Y = 32 + c * (bw / 2), 112 + r * 36
        rows.append(f"""<g class="fade" style="animation-delay:{i*.08:.2f}s">
  <circle cx="{X+6:.0f}" cy="{Y-5}" r="6" fill="{color}"/>
  <text x="{X+20:.0f}" y="{Y}" font-size="14.5" font-weight="600" fill="{TEXT}">{esc(name)}</text>
  <text x="{X + bw/2 - 24:.0f}" y="{Y}" font-family="{MONO}" font-size="13" fill="{MUTED}" text-anchor="end">{100*size/total:.1f}%</text>
</g>""")
    body = f"""<text x="32" y="42" font-size="18" font-weight="800" fill="{TEXT}">Most Used Languages</text>
<clipPath id="bar"><rect x="32" y="62" width="{bw}" height="12" rx="6"/></clipPath>
<rect x="32" y="62" width="{bw}" height="12" rx="6" fill="{CARD2}"/>
<g clip-path="url(#bar)">{''.join(bar)}</g>
{''.join(rows)}"""
    return frame(W, H, body)


def streak_card(s):
    W, H = 1200, 200
    total, current, longest, best, first = streaks(s["days"])
    col = (W - 64) / 3
    def block(i, big, label, sub, accent=False):
        cx = 32 + col * i + col / 2
        return f"""<g class="fade" style="animation-delay:{i*.1:.1f}s">
  <text x="{cx:.0f}" y="96" font-size="48" font-weight="800" fill="{'url(#grad)' if accent else TEXT}" text-anchor="middle">{big}</text>
  <text x="{cx:.0f}" y="132" font-size="16" font-weight="700" fill="{CYAN if accent else TEXT}" text-anchor="middle">{esc(label)}</text>
  <text x="{cx:.0f}" y="158" font-family="{MONO}" font-size="12.5" fill="{MUTED}" text-anchor="middle">{esc(sub)}</text>
</g>"""
    today = dt.date.today().strftime("%b %d").replace(" 0", " ")
    best_txt = f"{fmt_date(best[0])} → {fmt_date(best[1])}" if best[0] else "—"
    body = f"""
<rect x="{32+col:.0f}" y="36" width="1" height="128" fill="{LINE}"/>
<rect x="{32+2*col:.0f}" y="36" width="1" height="128" fill="{LINE}"/>
{block(0, total, "Total Contributions", f"{fmt_date(first)} → Present")}
{block(1, f"{current}🔥" if current else "0", "Current Streak", today, accent=True)}
{block(2, longest, "Longest Streak", best_txt)}"""
    return frame(W, H, body)


def activity_card(s):
    W, H = 1200, 300
    days = list(s["days"].items())[-31:]
    vals = [v for _, v in days] or [0]
    mx = max(max(vals), 1)
    L, R, T, B = 70, 40, 70, 56
    pw, ph = W - L - R, H - T - B
    step = pw / max(len(vals) - 1, 1)
    pts = [(L + i * step, T + ph - ph * v / mx) for i, v in enumerate(vals)]
    line = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(pts))
    area = f"{line} L{pts[-1][0]:.1f},{T+ph} L{pts[0][0]:.1f},{T+ph} Z"
    grid = []
    for k in range(5):
        y = T + ph * k / 4
        v = round(mx * (1 - k / 4))
        grid.append(f'<line x1="{L}" y1="{y:.0f}" x2="{W-R}" y2="{y:.0f}" stroke="{LINE}" stroke-dasharray="4 6"/>'
                    f'<text x="{L-14}" y="{y+4:.0f}" font-family="{MONO}" font-size="11.5" fill="{MUTED}" text-anchor="end">{v}</text>')
    labels = []
    for i, (d, _) in enumerate(days):
        if i % 5 == 0 or i == len(days) - 1:
            labels.append(f'<text x="{L + i*step:.0f}" y="{H-24}" font-family="{MONO}" font-size="11.5" fill="{MUTED}" text-anchor="middle">{dt.date.fromisoformat(d).day}</text>')
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4 if v else 2.5}" fill="{BG if v else LINE}" stroke="{VIOLET if v else LINE}" stroke-width="2"/>'
                   for (x, y), v in zip(pts, vals))
    plen = sum(((pts[i+1][0]-pts[i][0])**2 + (pts[i+1][1]-pts[i][1])**2) ** .5 for i in range(len(pts)-1)) + 10
    extra = f"""
  <linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".35"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
  <style>.draw{{stroke-dasharray:{plen:.0f};stroke-dashoffset:{plen:.0f};animation:dr 2s ease-out forwards}}@keyframes dr{{to{{stroke-dashoffset:0}}}}</style>"""
    rng = f"{fmt_date(days[0][0])} → {fmt_date(days[-1][0])}" if days else ""
    body = f"""<text x="32" y="42" font-size="18" font-weight="800" fill="{TEXT}">Contributions · last 31 days</text>
<text x="{W-32}" y="42" font-family="{MONO}" font-size="12" fill="{CYAN}" text-anchor="end">{esc(rng)}</text>
{''.join(grid)}
<path d="{area}" fill="url(#area)" class="fade"/>
<path d="{line}" fill="none" stroke="url(#grad)" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" class="draw"/>
<g class="fade">{dots}</g>
{''.join(labels)}"""
    return frame(W, H, body, extra)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "dist"
    os.makedirs(out, exist_ok=True)
    data = demo() if "--demo" in sys.argv else fetch()
    for name, fn in [("stats", stats_card), ("langs", langs_card), ("streak", streak_card), ("activity", activity_card)]:
        with open(os.path.join(out, f"{name}.svg"), "w", encoding="utf-8") as f:
            f.write(fn(data))
    print("stats built:", {k: data[k] for k in ("stars", "commits", "repos", "followers")})
