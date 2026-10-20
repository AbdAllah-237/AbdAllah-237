"""Generates the SVG components used in the profile README.

Run from the repo root:  python3 scripts/build_cards.py
Edit the DATA section below, re-run, commit the files in assets/.
"""
import base64, io, os
from xml.sax.saxutils import escape as esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")

# ───────────────────────── design tokens ─────────────────────────
BG = "#0B1020"
CARD = "#111833"
CARD2 = "#0E1530"
LINE = "#1F2A4D"
TEXT = "#E6EDF7"
MUTED = "#94A3B8"
CYAN = "#22D3EE"
VIOLET = "#A78BFA"
PINK = "#F472B6"
FONT = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace"

# ───────────────────────────── DATA ──────────────────────────────
NAME = "AbdAllah Elmarakby"
ROLE = "AI Automation Engineer · Founder @ Courlix"
TAGLINE = ["I build end-to-end systems that combine intelligent",
           "automation, APIs and scalable backend logic."]
CHIPS = ["n8n · LLM Agents", "Python & APIs", "ML & Data", "Egypt"]

PROJECTS = [
    dict(slug="courlix", icon="🌐", title="Courlix", kicker="E-LEARNING PLATFORM",
         desc="A full e-learning platform I designed, built and launched from scratch — architecture, backend, API integrations and automation.",
         tags=["Python", "n8n", "OpenAI", "REST APIs"], accent=CYAN),
    dict(slug="outreach", icon="📧", title="AI Outreach System", kicker="N8N · AUTOMATION",
         desc="Reads a prospect's website, writes a personalized message with AI, runs the outreach flow and tracks responses automatically.",
         tags=["n8n", "OpenAI", "Gemini", "Gmail", "Sheets"], accent=VIOLET),
    dict(slug="leads", icon="🎯", title="AI Lead Management", kicker="N8N · AI AGENT",
         desc="End-to-end AI system that qualifies leads, stores them as structured data and sends personalized email replies.",
         tags=["n8n", "OpenAI API", "Automation"], accent=PINK),
    dict(slug="greenhouse", icon="🌱", title="Smart Greenhouse", kicker="IOT · GRADUATION PROJECT",
         desc="Solar-powered greenhouse with automated irrigation, heating and environmental monitoring, controlled from a mobile app.",
         tags=["IoT", "Arduino", "Raspberry Pi", "Solar"], accent="#34D399"),
    dict(slug="score", icon="📈", title="Student Score Prediction", kicker="MACHINE LEARNING",
         desc="Supervised ML models that predict students' academic performance using a structured ML pipeline.",
         tags=["Python", "scikit-learn", "Regression"], accent="#FBBF24"),
    dict(slug="segmentation", icon="🧩", title="Customer Segmentation", kicker="MACHINE LEARNING",
         desc="Clustering customers into meaningful groups to extract actionable business insights.",
         tags=["Python", "Clustering", "Pandas"], accent="#60A5FA"),
]

EXPERIENCE = [
    ("2025 — NOW", "Founder & Automation Engineer", "Courlix.com",
     "Designed, built and launched a full e-learning platform. Own the architecture, backend, API integrations and automation workflows.", CYAN),
    ("2025", "Machine Learning Intern", "Elevvo Pathways",
     "Shipped ML projects with structured pipelines: score prediction, customer segmentation, forest-cover classification.", VIOLET),
    ("2024 — 2025", "Administrative Assistant & Records", "Confidential Department",
     "Managed a high volume of critical operations and records under pressure.", PINK),
    ("2023", "Data Analyst Intern", "MeriSkill",
     "Cleaned, analyzed and visualized HR & healthcare data; delivered insights through reports and dashboards.", "#34D399"),
]

STACK = [
    ("AI & AUTOMATION", [("n8n", "#EA4B71"), ("Make", "#A855F7"), ("OpenAI API", "#10A37F"),
                         ("Gemini", "#8E75B2"), ("LLM Agents", PINK), ("Web Scraping", "#34D399")]),
    ("BACKEND & APIS", [("Python", "#3776AB"), ("REST APIs", "#14B8A6"), ("Webhooks", CYAN),
                        ("Google Sheets", "#34A853"), ("Gmail API", "#EA4335"), ("Git", "#F05032")]),
    ("DATA & ML", [("Pandas", "#818CF8"), ("NumPy", "#4DABCF"), ("scikit-learn", "#F7931E"),
                   ("Matplotlib", "#60A5FA"), ("Jupyter", "#F37626")]),
    ("IOT & HARDWARE", [("Arduino", "#00979D"), ("Raspberry Pi", "#C51A4A")]),
]

CERTS = [
    ("Mastering Agentic AI with n8n", "Udemy", "🤖"),
    ("AI Sales Automation using n8n", "Udemy · Workshop", "💼"),
    ("Scientific Computing with Python", "freeCodeCamp · 300+ hrs", "🐍"),
    ("Google Project Management", "Coursera", "📋"),
    ("Foundations of Digital Marketing", "Google", "📣"),
]

SECTIONS = {"about": ("01", "About"), "experience": ("02", "Experience"),
            "projects": ("03", "Featured Projects"), "stack": ("04", "Tech Stack"),
            "certs": ("05", "Certificates"), "stats": ("06", "GitHub Activity")}


# ──────────────────────────── helpers ────────────────────────────
def wrap(text, size, width, weight="regular"):
    lines, cur = [], ""
    for w in text.split():
        nxt = f"{cur} {w}".strip()
        if cur and tw(nxt, size, weight) > width:
            lines.append(cur); cur = w
        else:
            cur = nxt
    if cur: lines.append(cur)
    return lines


_FONTS = {"regular": "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
          "semibold": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
          "bold": "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
          "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"}


def tw(text, size, weight="regular"):
    """Text width in px (measured with Inter when available, +6% safety)."""
    if weight is True: weight = "bold"
    if weight is False: weight = "regular"
    try:
        from PIL import ImageFont
        f = ImageFont.truetype(_FONTS[weight], 100)
        return f.getlength(text) * size / 100 * 1.06
    except Exception:
        return len(text) * size * (0.62 if weight == "mono" else 0.58)


def defs_common():
    return f"""
  <linearGradient id="grad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/>
  </linearGradient>
  <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CYAN}" stop-opacity=".55"/>
    <stop offset=".5" stop-color="{LINE}"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity=".55"/>
  </linearGradient>"""


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


# ───────────────────────────── hero ──────────────────────────────
def hero():
    from PIL import Image
    im = Image.open(os.path.join(OUT, "avatar.png"))
    im.thumbnail((300, 340), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    pw, ph = im.size
    W, H = 1200, 420
    px, py = W - pw - 90, H - ph

    chips, x = [], 60
    for c in CHIPS:
        w = tw(c, 14) + 42
        chips.append(f'<g transform="translate({x},318)"><rect width="{w:.0f}" height="34" rx="17" fill="{CARD}" stroke="{LINE}"/>'
                     f'<circle cx="17" cy="17" r="4" fill="url(#grad)"/>'
                     f'<text x="28" y="22" font-size="14" fill="{TEXT}">{esc(c)}</text></g>')
        x += w + 10

    tag = "".join(f'<text x="60" y="{252 + i*26}" font-size="18" fill="{MUTED}">{esc(l)}</text>' for i, l in enumerate(TAGLINE))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>{defs_common()}
  <radialGradient id="orb1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".35"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <radialGradient id="orb2"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".40"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.2" fill="#ffffff" opacity=".06"/></pattern>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="28"/></clipPath>
  <style>
    .o1{{animation:f1 9s ease-in-out infinite}} .o2{{animation:f2 11s ease-in-out infinite}}
    @keyframes f1{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(60px,30px)}}}}
    @keyframes f2{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-50px,-25px)}}}}
    .pulse{{animation:p 2s ease-out infinite;transform-origin:center;transform-box:fill-box}}
    @keyframes p{{0%{{opacity:.8;transform:scale(1)}}100%{{opacity:0;transform:scale(2.6)}}}}
    .ring{{animation:r 6s linear infinite;transform-origin:{px + pw/2}px {H - 150}px}}
    @keyframes r{{to{{transform:rotate(360deg)}}}}
    .fade{{animation:fi 1s ease-out both}} @keyframes fi{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1}}}}
  </style>
</defs>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
  <circle class="o1" cx="{px + pw/2}" cy="200" r="260" fill="url(#orb2)"/>
  <circle class="o2" cx="180" cy="40" r="240" fill="url(#orb1)"/>
  <circle class="ring" cx="{px + pw/2}" cy="{H - 150}" r="150" fill="none" stroke="url(#grad)" stroke-width="2" stroke-dasharray="6 14" opacity=".7"/>
  <circle cx="{px + pw/2}" cy="{H - 150}" r="128" fill="{CARD}" opacity=".9"/>
  <image x="{px}" y="{py}" width="{pw}" height="{ph}" xlink:href="data:image/png;base64,{b64}"/>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="27" fill="none" stroke="url(#border)" stroke-width="2"/>

<g class="fade">
  <g transform="translate(60,62)">
    <rect width="232" height="32" rx="16" fill="#0F2A2E" stroke="#155E63"/>
    <circle class="pulse" cx="18" cy="16" r="5" fill="#34D399"/><circle cx="18" cy="16" r="5" fill="#34D399"/>
    <text x="32" y="21" font-size="13.5" fill="#A7F3D0" font-weight="600">Open to collaborations</text>
  </g>
  <text x="58" y="160" font-size="58" font-weight="800" fill="url(#grad)" letter-spacing="-1">{esc(NAME)}</text>
  <text x="60" y="204" font-size="22" font-weight="600" fill="{TEXT}">{esc(ROLE)}</text>
  {tag}
  {''.join(chips)}
</g>
</svg>"""


# ───────────────────────── section header ─────────────────────────
def section(num, title):
    W, H = 1200, 64
    t_w = tw(title, 28, "bold")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>{defs_common()}
  <linearGradient id="fadeLine" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".8"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>
</defs>
<text x="0" y="42" font-family="{MONO}" font-size="16" font-weight="700" fill="{CYAN}">{num}</text>
<text x="40" y="44" font-size="28" font-weight="800" fill="url(#grad)">{esc(title)}</text>
<rect x="{58 + t_w:.0f}" y="34" width="{W - 58 - t_w:.0f}" height="2" rx="1" fill="url(#fadeLine)"/>
</svg>"""


# ───────────────────────── project card ──────────────────────────
def project(p):
    W, H = 590, 280
    a = p["accent"]
    desc = "".join(f'<text x="32" y="{142 + i*24}" font-size="15.5" fill="{MUTED}">{esc(l)}</text>'
                   for i, l in enumerate(wrap(p["desc"], 15.5, W - 64)[:4]))
    tags, x = [], 32
    for t in p["tags"]:
        w = tw(t, 12.5, "mono") + 24
        tags.append(f'<g transform="translate({x},{H-56})"><rect width="{w:.0f}" height="28" rx="8" fill="{CARD2}" stroke="{LINE}"/>'
                    f'<text x="{w/2:.0f}" y="19" font-family="{MONO}" font-size="12.5" fill="{TEXT}" text-anchor="middle">{esc(t)}</text></g>')
        x += w + 8
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>{defs_common()}
  <radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{a}" stop-opacity=".28"/><stop offset=".6" stop-color="{a}" stop-opacity="0"/></radialGradient>
  <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="22"/></clipPath>
  <style>.s{{animation:sh 4s ease-in-out infinite}}@keyframes sh{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}</style>
</defs>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{CARD}"/>
  <rect class="s" width="{W}" height="{H}" fill="url(#glow)"/>
  <rect width="{W}" height="4" fill="url(#bar)"/>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="21" fill="none" stroke="{LINE}" stroke-width="1.5"/>
<rect x="32" y="32" width="52" height="52" rx="14" fill="{CARD2}" stroke="{a}" stroke-opacity=".5"/>
<text x="58" y="67" font-size="26" text-anchor="middle">{p["icon"]}</text>
<text x="100" y="52" font-family="{MONO}" font-size="12" font-weight="700" fill="{a}" letter-spacing="1.5">{esc(p["kicker"])}</text>
<text x="100" y="80" font-size="24" font-weight="800" fill="{TEXT}">{esc(p["title"])}</text>
<g transform="translate({W-62},32)"><rect width="30" height="30" rx="9" fill="{CARD2}" stroke="{LINE}"/>
<path d="M10 20 L20 10 M12 10 H20 V18" stroke="{TEXT}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
{desc}
{''.join(tags)}
</svg>"""


# ─────────────────────────── timeline ────────────────────────────
def timeline():
    W, ROW, TOP = 1200, 132, 20
    H = TOP + ROW * len(EXPERIENCE) + 10
    rows = []
    for i, (date, role, org, desc, c) in enumerate(EXPERIENCE):
        y = TOP + i * ROW
        d = "".join(f'<text x="244" y="{y + 84 + j*22}" font-size="15" fill="{MUTED}">{esc(l)}</text>'
                    for j, l in enumerate(wrap(desc, 15, W - 290)[:2]))
        cur = i == 0
        rows.append(f"""
<g>
  <rect x="0" y="{y+8}" width="{tw(date,13,'mono')+28:.0f}" height="30" rx="15" fill="{CARD}" stroke="{c}" stroke-opacity=".6"/>
  <text x="14" y="{y+28}" font-family="{MONO}" font-size="13" font-weight="700" fill="{c}">{esc(date)}</text>
  {'<circle class="pulse" cx="190" cy="'+str(y+24)+'" r="9" fill="'+c+'"/>' if cur else ''}
  <circle cx="190" cy="{y+24}" r="9" fill="{BG}" stroke="{c}" stroke-width="3"/>
  <circle cx="190" cy="{y+24}" r="3.5" fill="{c}"/>
  <rect x="220" y="{y}" width="{W-220}" height="{ROW-16}" rx="18" fill="{CARD}" stroke="{LINE}"/>
  <text x="244" y="{y+34}" font-size="21" font-weight="800" fill="{TEXT}">{esc(role)}</text>
  <text x="244" y="{y+58}" font-size="15" font-weight="600" fill="{c}">{esc(org)}</text>
  {d}
</g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>{defs_common()}
  <linearGradient id="vline" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity=".1"/></linearGradient>
  <style>.pulse{{animation:p 2s ease-out infinite;transform-box:fill-box;transform-origin:center}}
  @keyframes p{{0%{{opacity:.7;transform:scale(1)}}100%{{opacity:0;transform:scale(2.4)}}}}</style>
</defs>
<rect x="189" y="{TOP+24}" width="2" height="{H-TOP-60}" fill="url(#vline)"/>
{''.join(rows)}
</svg>"""


# ─────────────────────────── tech stack ──────────────────────────
def stack():
    W, ROW = 1200, 66
    H = ROW * len(STACK) + 50
    out = []
    for i, (label, items) in enumerate(STACK):
        y = 32 + i * ROW
        out.append(f'<text x="40" y="{y+25}" font-family="{MONO}" font-size="13" font-weight="700" fill="{MUTED}" letter-spacing="1.5">{esc(label)}</text>')
        x = 250
        for name, col in items:
            w = tw(name, 15, "semibold") + 50
            out.append(f'<g transform="translate({x},{y})"><rect width="{w:.0f}" height="40" rx="12" fill="{CARD2}" stroke="{col}" stroke-opacity=".45"/>'
                       f'<circle cx="20" cy="20" r="5" fill="{col}"/>'
                       f'<text x="34" y="26" font-size="15" font-weight="600" fill="{TEXT}">{esc(name)}</text></g>')
            x += w + 10
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>{defs_common()}</defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22" fill="{CARD}" stroke="url(#border)" stroke-width="1.5"/>
{''.join(out)}
</svg>"""


# ────────────────────────── certificates ─────────────────────────
def certs():
    W, COLS, GAP, CH = 1200, 3, 16, 96
    cw = (W - GAP * (COLS - 1)) / COLS
    rows = (len(CERTS) + COLS - 1) // COLS
    H = rows * CH + (rows - 1) * GAP
    out = []
    for i, (t, issuer, ic) in enumerate(CERTS):
        r, c = divmod(i, COLS)
        in_row = min(COLS, len(CERTS) - r * COLS)
        offset = (W - (in_row * cw + (in_row - 1) * GAP)) / 2
        x, y = offset + c * (cw + GAP), r * (CH + GAP)
        lines = wrap(t, 16.5, cw - 100)[:2]
        ty = y + (38 if len(lines) == 1 else 30)
        txt = "".join(f'<text x="{x+84}" y="{ty + j*21}" font-size="16.5" font-weight="700" fill="{TEXT}">{esc(l)}</text>' for j, l in enumerate(lines))
        out.append(f"""<g>
  <rect x="{x+1}" y="{y+1}" width="{cw-2:.0f}" height="{CH-2}" rx="18" fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/>
  <rect x="{x+20}" y="{y+22}" width="50" height="50" rx="14" fill="{CARD2}" stroke="url(#border)"/>
  <text x="{x+45}" y="{y+56}" font-size="24" text-anchor="middle">{ic}</text>
  {txt}
  <text x="{x+84}" y="{ty + len(lines)*21 + 6}" font-family="{MONO}" font-size="12.5" fill="{CYAN}">{esc(issuer)}</text>
</g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>{defs_common()}</defs>
{''.join(out)}
</svg>"""


# ─────────────────────────── about card ──────────────────────────
def about():
    W, H = 1200, 300
    code = [
        [("class ", VIOLET), ("AbdAllah", CYAN), (":", TEXT)],
        [("    title     ", TEXT), ("= ", MUTED), ('"AI Automation Engineer"', "#A5D6A7")],
        [("    building  ", TEXT), ("= ", MUTED), ('"Courlix.com — e-learning platform, built from zero"', "#A5D6A7")],
        [("    focus     ", TEXT), ("= ", MUTED), ("[", TEXT), ('"Agentic AI"', "#A5D6A7"), (", ", TEXT), ('"n8n"', "#A5D6A7"), (", ", TEXT), ('"LLMs"', "#A5D6A7"), (", ", TEXT), ('"APIs"', "#A5D6A7"), ("]", TEXT)],
        [("    education ", TEXT), ("= ", MUTED), ('"B.Sc. Electrical & Computer Eng. — Minufiya Univ."', "#A5D6A7")],
        [("    motto     ", TEXT), ("= ", MUTED), ('"Do it twice → automate it the third time ⚡"', "#FBBF24")],
    ]
    lines = []
    for i, segs in enumerate(code):
        spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in segs)
        lines.append(f'<text x="70" y="{100 + i*30}" font-family="{MONO}" font-size="16" xml:space="preserve">{spans}</text>'
                     f'<text x="40" y="{100 + i*30}" font-family="{MONO}" font-size="14" fill="#3B4A72" text-anchor="end">{i+1}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>{defs_common()}
  <style>.cur{{animation:b 1s steps(1) infinite}}@keyframes b{{50%{{opacity:0}}}}</style>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{CARD}"/><rect width="{W}" height="48" fill="{CARD2}"/></g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="21" fill="none" stroke="url(#border)" stroke-width="1.5"/>
<circle cx="28" cy="24" r="6.5" fill="#FF5F57"/><circle cx="50" cy="24" r="6.5" fill="#FEBC2E"/><circle cx="72" cy="24" r="6.5" fill="#28C840"/>
<text x="{W/2}" y="29" font-family="{MONO}" font-size="13" fill="{MUTED}" text-anchor="middle">about_me.py</text>
{''.join(lines)}
<rect class="cur" x="70" y="{100 + len(code)*30 - 16}" width="10" height="20" fill="{CYAN}"/>
</svg>"""


if __name__ == "__main__":
    save("hero.svg", hero())
    save("about.svg", about())
    save("timeline.svg", timeline())
    save("stack.svg", stack())
    save("certs.svg", certs())
    for key, (n, t) in SECTIONS.items():
        save(f"h-{key}.svg", section(n, t))
    for p in PROJECTS:
        save(f"p-{p['slug']}.svg", project(p))
    print("done")
