"""Generate the profile README SVGs: hero banner, plus light/dark tech stack, experience and project cards."""
import sys
from html import escape
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets"

SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
MONO_CW = 7.0  # approx char width of 12px mono

BG_DEFS = """
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0B1020"/>
      <stop offset="0.55" stop-color="#121A33"/>
      <stop offset="1" stop-color="#1B1240"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#22D3EE"/>
      <stop offset="1" stop-color="#A78BFA"/>
    </linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="#FFFFFF" stroke-opacity="0.04"/>
    </pattern>"""

BASE_CSS = f"""
      .h1{{font:700 52px {SANS};fill:#F8FAFC}}
      .h2{{font:600 22px {SANS};fill:url(#accent)}}
      .h3{{font:500 17px {SANS};fill:#CBD5E1}}
      .title{{font:700 19px {SANS};fill:#F8FAFC}}
      .org{{font:600 14px {SANS};fill:#CBD5E1}}
      .body{{font:400 14px {SANS};fill:#94A3B8}}
      .small{{font:400 13px {SANS};fill:#94A3B8}}
      .mono{{font:600 12px {MONO}}}
      .chip{{font:600 12px {MONO};fill:#E2E8F0}}"""


def svg(w, h, title, desc, defs, css, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
  <title id="t">{escape(title)}</title>
  <desc id="d">{escape(desc)}</desc>
  <defs>{BG_DEFS}{defs}
    <style>{BASE_CSS}{css}
    </style>
  </defs>
  <rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" rx="18" fill="url(#grid)"/>
{body}
</svg>
"""


def chips(x, y, labels, color, max_w):
    """Lay chips left to right, wrapping to a new row past max_w."""
    out, cx, cy = [], x, y
    for lab in labels:
        w = len(lab) * MONO_CW + 22
        if cx + w > x + max_w:
            cx, cy = x, cy + 34
        out.append(
            f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="26" rx="13" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.45"/>'
            f'<text x="{cx + w / 2:.0f}" y="{cy + 17}" text-anchor="middle" class="chip">{escape(lab)}</text>'
        )
        cx += w + 8
    return "\n".join(out)


def lines(x, y, rows, cls, dy):
    return "\n".join(
        f'<text x="{x}" y="{y + i * dy}" class="{cls}">{escape(r)}</text>' for i, r in enumerate(rows)
    )


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1200, 336
    css = """
      .flow{stroke:url(#accent);stroke-width:2;stroke-dasharray:6 10;animation:dash 2.4s linear infinite}
      .node{fill:#0F172A;stroke-width:2}
      .lbl{font:600 13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#CBD5E1}
      .wave{animation:slide 6s linear infinite}
      @keyframes dash{to{stroke-dashoffset:-32}}
      @keyframes slide{to{transform:translateX(-240px)}}"""
    defs = """
    <clipPath id="waveclip"><rect x="680" y="236" width="480" height="56" rx="10"/></clipPath>"""
    tags = ["Python", "SQL", "PyTorch", "TensorFlow", "Time series", "ETL"]
    tag_svg, tx = [], 66
    for t in tags:
        w = len(t) * 7.8 + 26
        tag_svg.append(
            f'<rect x="{tx:.0f}" y="288" width="{w:.0f}" height="28" rx="14" fill="#1E293B" stroke="#334155"/>'
            f'<text x="{tx + w / 2:.0f}" y="307" text-anchor="middle" class="lbl">{t}</text>'
        )
        tx += w + 10

    phd_svg, px = [], 66
    for t in ["Reinforcement Learning", "Industrial Cyber-Physical Systems"]:
        w = len(t) * 7.8 + 28
        phd_svg.append(
            f'<rect x="{px:.0f}" y="180" width="{w:.0f}" height="30" rx="15" fill="#A78BFA" fill-opacity="0.16" stroke="#A78BFA" stroke-opacity="0.7"/>'
            f'<text x="{px + w / 2:.0f}" y="200" text-anchor="middle" class="lbl" style="fill:#E9D5FF">{t}</text>'
        )
        px += w + 10

    # Pipeline nodes: data -> ETL -> model -> eval
    xs = [680, 808, 936, 1064]
    colors = ["#22D3EE", "#38BDF8", "#A78BFA", "#34D399"]
    names = ["data", "ETL", "model", "eval"]
    y0, nh, nw = 70, 120, 96
    nodes = []
    for x, c, n in zip(xs, colors, names):
        nodes.append(f'<rect x="{x}" y="{y0}" width="{nw}" height="{nh}" rx="14" class="node" stroke="{c}"/>')
        nodes.append(f'<text x="{x + nw / 2}" y="{y0 + nh - 16}" text-anchor="middle" class="lbl">{n}</text>')
    cx = [x + nw / 2 for x in xs]
    icons = f"""
  <!-- data: cylinder -->
  <ellipse cx="{cx[0]}" cy="102" rx="24" ry="8" fill="none" stroke="#22D3EE" stroke-width="2"/>
  <path d="M{cx[0]-24} 102 V136 A24 8 0 0 0 {cx[0]+24} 136 V102" fill="none" stroke="#22D3EE" stroke-width="2"/>
  <path d="M{cx[0]-24} 119 A24 8 0 0 0 {cx[0]+24} 119" fill="none" stroke="#22D3EE" stroke-width="2" stroke-opacity=".6"/>
  <!-- ETL: funnel -->
  <path d="M{cx[1]-26} 96 H{cx[1]+26} L{cx[1]+8} 120 V140 L{cx[1]-8} 148 V120 Z" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linejoin="round"/>
  <!-- model: tiny network -->
  {"".join(f'<line x1="{cx[2]-22}" y1="{a}" x2="{cx[2]}" y2="{b}" stroke="#A78BFA" stroke-opacity=".5"/>' for a in (98,120,142) for b in (106,134))}
  {"".join(f'<line x1="{cx[2]}" y1="{a}" x2="{cx[2]+22}" y2="120" stroke="#A78BFA" stroke-opacity=".5"/>' for a in (106,134))}
  {"".join(f'<circle cx="{cx[2]-22}" cy="{a}" r="5" fill="#0F172A" stroke="#A78BFA" stroke-width="2"/>' for a in (98,120,142))}
  {"".join(f'<circle cx="{cx[2]}" cy="{a}" r="5" fill="#0F172A" stroke="#A78BFA" stroke-width="2"/>' for a in (106,134))}
  <circle cx="{cx[2]+22}" cy="120" r="5" fill="#A78BFA"/>
  <!-- eval: animated bars -->
  {"".join(f'''<rect x="{cx[3]-26 + i*14}" y="{150-h}" width="10" height="{h}" rx="2" fill="#34D399" fill-opacity="{0.55 + i*0.15}">
    <animate attributeName="height" values="{h};{h2};{h}" dur="3s" begin="{i*0.4}s" repeatCount="indefinite"/>
    <animate attributeName="y" values="{150-h};{150-h2};{150-h}" dur="3s" begin="{i*0.4}s" repeatCount="indefinite"/>
  </rect>''' for i, (h, h2) in enumerate([(18, 30), (30, 22), (26, 44), (40, 50)]))}"""
    links = []
    for i in range(3):
        x1, x2 = xs[i] + nw, xs[i + 1]
        links.append(f'<line x1="{x1}" y1="130" x2="{x2}" y2="130" stroke="#334155" stroke-width="2"/>')
        links.append(f'<line x1="{x1}" y1="130" x2="{x2}" y2="130" class="flow"/>')
        links.append(f'<path id="l{i}" d="M{x1} 130 H{x2}" fill="none"/>')
        links.append(
            f'<circle r="4" fill="{colors[i + 1]}"><animateMotion dur="1.6s" begin="{i * 0.5}s" repeatCount="indefinite"><mpath href="#l{i}"/></animateMotion></circle>'
        )

    # Scrolling signal (time-series) under the pipeline
    pts = []
    import math
    for k in range(0, 961, 6):
        v = 264 + 10 * math.sin(k / 19) + 6 * math.sin(k / 7.3) * (1 if (k // 120) % 2 else 0.4)
        pts.append(f"{680 + k},{v:.1f}")
    wave = f"""
  <rect x="680" y="236" width="480" height="56" rx="10" fill="#0F172A" stroke="#334155"/>
  <g clip-path="url(#waveclip)">
    <polyline class="wave" points="{' '.join(pts)}" fill="none" stroke="url(#accent)" stroke-width="2"/>
  </g>
  <text x="692" y="252" class="lbl" style="font-size:11px;fill:#64748B">signal</text>"""

    body = f"""
  <text x="64" y="92" class="h1">Ichrak Hamdi</text>
  <text x="66" y="132" class="h2">Machine Learning Engineer · Data Scientist</text>
  <text x="66" y="166" class="h3">PhD Researcher in Computer Science, Université Laval</text>
  {chr(10).join(phd_svg)}
  <text x="66" y="246" class="body" style="font-size:16px">End-to-end Python ML pipelines for real-world data:</text>
  <text x="66" y="268" class="body" style="font-size:16px">ETL, time series, signal processing and deep learning.</text>
  {chr(10).join(tag_svg)}
  <g transform="translate(0 8)">
  {chr(10).join(links)}
  {chr(10).join(nodes)}
  {icons}
  {wave}
  </g>"""
    return svg(W, H, "Ichrak Hamdi: Machine Learning Engineer and Data Scientist",
               "Banner with name, title, PhD research areas (reinforcement learning, industrial cyber-physical systems), and an animated data pipeline from raw data through ETL and a model to evaluation, above a scrolling signal.",
               defs, css, body)


# ---------------------------------------------------------------- themed sections
# Everything below has a transparent background and is generated twice
# (name-light.svg / name-dark.svg) so the README can pick one with <picture>.
THEMES = {
    "light": {
        "text": "#1F2328", "muted": "#59636E", "faint": "#818B98", "line": "#D0D7DE", "tile": "#F6F8FA",
        "cyan": "#0E7490", "violet": "#6D28D9", "pink": "#BE185D", "amber": "#B45309", "green": "#047857", "blue": "#1D4ED8",
    },
    "dark": {
        "text": "#E6EDF3", "muted": "#9198A1", "faint": "#6E7681", "line": "#30363D", "tile": "#F6F8FA",
        "cyan": "#22D3EE", "violet": "#A78BFA", "pink": "#F472B6", "amber": "#FBBF24", "green": "#34D399", "blue": "#60A5FA",
    },
}


def plain_svg(w, h, title, desc, css, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
  <title id="t">{escape(title)}</title>
  <desc id="d">{escape(desc)}</desc>
  <style>{css}
  </style>
{body}
</svg>
"""


def write_themed(name, fn):
    for theme, t in THEMES.items():
        (OUT / f"{name}-{theme}.svg").write_text(fn(t))


# ---------------------------------------------------------------- tech stack
ICONS = Path(__file__).resolve().parent / "icons"  # devicon logos (MIT)


def logo(name):
    import base64
    data = base64.b64encode((ICONS / f"{name}.svg").read_bytes()).decode()
    return f"data:image/svg+xml;base64,{data}"


def stack(t):
    # One row per area; logos sit on light tiles so dark marks (Kafka) stay visible in dark mode.
    W, m, label_w, tile, step = 1200, 8, 260, 76, 110
    rows = [
        ("Languages", [("python", "Python"), ("cplusplus", "C++"), ("java", "Java"),
                       ("javascript", "JavaScript"), ("matlab", "MATLAB")]),
        ("Machine Learning", [("pytorch", "PyTorch"), ("tensorflow", "TensorFlow"), ("scikitlearn", "scikit-learn"),
                              ("opencv", "OpenCV"), ("jupyter", "Jupyter")]),
        ("Data Science", [("pandas", "pandas"), ("numpy", "NumPy"), ("matplotlib", "Matplotlib")]),
        ("Data & Cloud", [("mysql", "MySQL"), ("azure", "Azure"), ("apachekafka", "Kafka"),
                          ("hadoop", "Hadoop"), ("docker", "Docker"), ("git", "Git")]),
    ]
    rh = tile + 56
    H = m + len(rows) * rh
    css = f"""
    .row{{font:700 24px {SANS};fill:{t['text']}}}
    .name{{font:500 17px {SANS};fill:{t['muted']}}}"""
    parts = []
    for r, (label, items) in enumerate(rows):
        y = m + r * rh
        parts.append(f'<text x="{m}" y="{y + tile / 2 + 9}" class="row">{escape(label)}</text>')
        for i, (icon_name, name) in enumerate(items):
            x = m + label_w + i * step
            parts.append(f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="16" fill="{t["tile"]}" stroke="{t["line"]}"/>')
            parts.append(f'<image x="{x + 15}" y="{y + 15}" width="{tile - 30}" height="{tile - 30}" href="{logo(icon_name)}"/>')
            parts.append(f'<text x="{x + tile / 2}" y="{y + tile + 26}" text-anchor="middle" class="name">{escape(name)}</text>')
    return plain_svg(W, H, "Tech stack",
                     "Languages: Python, C++, Java, JavaScript, MATLAB. Machine learning: PyTorch, TensorFlow, scikit-learn, OpenCV, Jupyter. "
                     "Data science: pandas, NumPy, Matplotlib. Data and cloud: MySQL, Azure, Kafka, Hadoop, Docker, Git.",
                     css, "\n".join(parts))


# ---------------------------------------------------------------- experience
EXPERIENCE = [
    # (dates, role, org, description, accent)
    ("2025 – present", "PhD in Computer Science", "Université Laval · Québec",
     "Autonomous AI agents for the cyberdefense of industrial cyber-physical systems.", "violet"),
    ("2025 – 2026", "Course Lecturer & Teaching Assistant", "Université Laval · Québec",
     "Taught 2 algorithms courses; TA for IoT Security and Advanced C++ (code review, grading).", "green"),
    ("2024", "Machine Learning Research Engineer", "Knowlepsy · Remote",
     "End-to-end ML pipelines for epilepsy health data: time series, signals, ETL on Azure.", "cyan"),
    ("2023", "AI Research Intern", "UQAT · Rouyn-Noranda",
     "Optimization algorithms for planning sidewalk snow-removal operations.", "amber"),
    ("2022", "AI Intern", "Talan Tunisie · Tunis",
     "Distributed architectures for a metaverse project and motion detection algorithms.", "pink"),
]


def experience(t):
    W, rh, top = 1200, 118, 14
    H = top + rh * len(EXPERIENCE) - 18
    lx = 236  # timeline x
    css = f"""
    .date{{font:600 18px {MONO};fill:{t['muted']}}}
    .role{{font:700 24px {SANS};fill:{t['text']}}}
    .org{{font:600 18px {SANS}}}
    .desc{{font:400 19px {SANS};fill:{t['muted']}}}"""
    parts = [f'<line x1="{lx}" y1="{top + 12}" x2="{lx}" y2="{H - 30}" stroke="{t["line"]}" stroke-width="2"/>']
    for i, (dates, role, org, desc, accent) in enumerate(EXPERIENCE):
        y = top + i * rh
        c = t[accent]
        parts.append(f'<text x="{lx - 28}" y="{y + 20}" text-anchor="end" class="date">{escape(dates)}</text>')
        parts.append(f'<circle cx="{lx}" cy="{y + 13}" r="8" fill="{c}"/>')
        if i == 0:
            parts.append(f'<circle cx="{lx}" cy="{y + 13}" r="8" fill="none" stroke="{c}" stroke-width="2">'
                         '<animate attributeName="r" values="8;16;8" dur="2.4s" repeatCount="indefinite"/>'
                         '<animate attributeName="opacity" values="1;0;1" dur="2.4s" repeatCount="indefinite"/></circle>')
        parts.append(f'<text x="{lx + 32}" y="{y + 22}" class="role">{escape(role)}</text>')
        parts.append(f'<text x="{lx + 32}" y="{y + 50}" class="org" fill="{c}">{escape(org)}</text>')
        parts.append(f'<text x="{lx + 32}" y="{y + 78}" class="desc">{escape(desc)}</text>')
    return plain_svg(W, H, "Experience",
                     "; ".join(f"{d}: {r}, {o}. {ds}" for d, r, o, ds, _ in EXPERIENCE), css, "\n".join(parts))


# ---------------------------------------------------------------- projects
PROJECTS = {
    "project-traffic": ("Network Traffic Classification", "Deep learning · Security", "cyan",
        ["Detects cyberattacks in network traffic and", "compares LSTM and Transformer models."],
        ["TensorFlow", "LSTM", "Transformers"], None),
    "project-mammogram": ("Mammogram Segmentation", "Computer vision · Health", "pink",
        ["U-Net vs Fuzzy C-Means vs EM for breast-", "cancer screening, served in a Django app."],
        ["U-Net", "Django", "Python"], "Best poster"),
    "project-emotion": ("Facial Emotion Detection", "Computer vision · Real time", "violet",
        ["Real-time facial expression recognition", "with convolutional neural networks."],
        ["TensorFlow", "OpenCV", "CNN"], None),
    "project-mario": ("Super Mario RL Agent", "Reinforcement learning", "green",
        ["A Double-DQN agent that learns to play", "Super Mario Bros from raw pixels."],
        ["TensorFlow", "DQN", "Gym"], None),
}


def project(t, title, kicker, accent, desc, tags, award):
    W, H, p = 580, 260, 30
    c = t[accent]
    css = f"""
    .k{{font:700 15px {MONO};fill:{c}}}
    .ti{{font:700 28px {SANS};fill:{t['text']}}}
    .d{{font:400 20px {SANS};fill:{t['muted']}}}
    .chip{{font:600 15px {MONO};fill:{t['text']}}}
    .go{{font:600 16px {SANS};fill:{t['faint']}}}"""
    parts = [
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>',
        f'<rect x="{p}" y="0" width="64" height="4" rx="2" fill="{c}"/>',
        f'<text x="{p}" y="46" class="k">{escape(kicker.upper())}</text>',
        f'<text x="{W - p}" y="46" text-anchor="end" class="go">View repo →</text>',
        f'<text x="{p}" y="88" class="ti">{escape(title)}</text>',
        lines(p, 126, desc, "d", 28),
    ]
    cx = p
    for lab in tags + ([award] if award else []):
        is_award = lab == award
        col = t["amber"] if is_award else c
        w = len(lab) * 9.3 + 28
        parts.append(f'<rect x="{cx:.0f}" y="{H - 64}" width="{w:.0f}" height="34" rx="17" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".55"/>')
        parts.append(f'<text x="{cx + w / 2:.0f}" y="{H - 41}" text-anchor="middle" class="chip">{escape(lab)}</text>')
        cx += w + 10
    return plain_svg(W, H, title, f"{kicker}. {' '.join(desc)}", css, "\n".join(parts))


(OUT / "hero.svg").write_text(hero())
write_themed("stack", stack)
write_themed("experience", experience)
for name, args in PROJECTS.items():
    write_themed(name, lambda t, a=args: project(t, *a))
print("ok")
