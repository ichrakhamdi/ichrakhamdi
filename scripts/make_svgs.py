"""Generate the profile README SVGs (hero, expertise cards, experience timeline)."""
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


# ---------------------------------------------------------------- expertise
def expertise():
    # Two columns, three rows, large type: the image is shown at ~830px on GitHub.
    W, m, rh = 1200, 56, 196
    H = m * 2 + rh * 3 - 40
    colx = [m, W // 2 + 28]
    items = [
        ("#22D3EE", "ML Engineering",
         ["Built and maintained ML pipelines for epilepsy", "health data at Knowlepsy, from raw data to model."],
         "Python · Pandas · NumPy · scikit-learn"),
        ("#A78BFA", "Time Series & Signals",
         ["Forecasting and signal processing on large,", "noisy sensor datasets."],
         "Forecasting · Signal processing · IoT"),
        ("#F472B6", "Deep Learning & Vision",
         ["Segmentation, emotion recognition and attack", "detection with CNNs, U-Net, LSTMs, Transformers."],
         "PyTorch · TensorFlow · OpenCV"),
        ("#FBBF24", "Data Engineering",
         ["ETL workflows and IoT data integration", "on Azure, from SQL to streaming."],
         "SQL · Azure · Kafka · Hadoop · Docker"),
        ("#34D399", "Code Review & Evaluation",
         ["Reviewing, debugging and grading code in", "5 university courses; evaluating AI agents."],
         "Debugging · Written feedback · Agent evaluation"),
        ("#60A5FA", "AI for Cybersecurity",
         ["PhD research on AI agents that defend", "industrial cyber-physical systems."],
         "Reinforcement learning · ICS / OT"),
    ]
    css = f"""
      .num{{font:600 17px {MONO}}}
      .t{{font:700 27px {SANS};fill:#F8FAFC}}
      .p{{font:400 19px {SANS};fill:#A8B3C4}}
      .tools{{font:500 15px {MONO};fill:#7C8BA1}}"""
    parts = [f'<line x1="{W // 2}" y1="{m}" x2="{W // 2}" y2="{H - m}" stroke="#1E293B" stroke-width="1.5"/>']
    for r in (1, 2):
        y = m + r * rh - 34
        parts.append(f'<line x1="{m}" y1="{y}" x2="{W - m}" y2="{y}" stroke="#1E293B" stroke-width="1.5"/>')
    for i, (c, title, desc, tools) in enumerate(items):
        x, y = colx[i % 2], m + (i // 2) * rh
        parts.append(f'<text x="{x}" y="{y + 20}" class="num" fill="{c}">{i + 1:02d}</text>')
        parts.append(f'<text x="{x + 40}" y="{y + 22}" class="t">{escape(title)}</text>')
        parts.append(lines(x + 40, y + 60, desc, "p", 27))
        parts.append(f'<text x="{x + 40}" y="{y + 126}" class="tools">{escape(tools)}</text>')
    return svg(W, H, "What I do",
               "Six areas: ML engineering, time series and signals, deep learning and vision, data engineering, code review and evaluation, and AI for cybersecurity.",
               "", css, "\n".join(parts))


# ---------------------------------------------------------------- experience
def experience():
    W, H = 1200, 440
    ty = 220  # timeline y
    x0, x1 = 60, 1140

    def yx(year, month=1):
        # 2022-01 -> 100, 250px per year
        return 100 + (year - 2022 + (month - 1) / 12) * 250

    css = """
      .card{fill:#0F172A;stroke:#1E293B;stroke-width:1.5}
      .now{animation:now 2s ease-in-out infinite;transform-origin:center;transform-box:fill-box}
      @keyframes now{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.8);opacity:.2}}"""
    entries = [
        # (start x, slot centre, above?, colour, dates, role, org, desc)
        (yx(2022, 7), 190, True, "#94A3B8", "JUL 2022 – AUG 2022", "AI Intern", "Talan Tunisie",
         ["Distributed architectures for a", "metaverse project; motion detection."]),
        (yx(2023, 3), 395, False, "#A78BFA", "MAR 2023 – AUG 2023", "AI Research Intern", "UQAT, Québec",
         ["Optimization algorithms for planning", "sidewalk snow-removal operations."]),
        (yx(2024, 1), 600, True, "#22D3EE", "JAN 2024 – DEC 2024", "ML Research Engineer", "Knowlepsy · Remote",
         ["ML pipelines on epilepsy health data:", "time series, signals, ETL on Azure."]),
        (yx(2025, 1), 805, False, "#F472B6", "JAN 2025 – PRESENT", "PhD in Computer Science", "Université Laval",
         ["AI agents for the cyberdefense of", "industrial cyber-physical systems."]),
        (yx(2025, 5), 1010, True, "#34D399", "MAY 2025 – MAY 2026", "Course Lecturer & TA", "Université Laval",
         ["Taught 2 algorithms courses; TA for", "IoT Security and Advanced C++."]),
    ]
    cw, chh = 330, 138
    parts = [
        f'<line x1="{x0}" y1="{ty}" x2="{x1}" y2="{ty}" stroke="#334155" stroke-width="2"/>',
        f'<line x1="{x0}" y1="{ty}" x2="{x1}" y2="{ty}" stroke="url(#accent)" stroke-width="2" stroke-dasharray="4 8" opacity=".6"/>',
    ]
    for yr in range(2022, 2027):
        x = yx(yr)
        parts.append(f'<line x1="{x}" y1="{ty - 6}" x2="{x}" y2="{ty + 6}" stroke="#475569" stroke-width="2"/>')
        parts.append(f'<text x="{x + 6}" y="{ty + 22}" class="mono" fill="#64748B">{yr}</text>')
    for sx, slot, above, c, dates, role, org, desc in entries:
        cx = slot - cw / 2
        cy = ty - 40 - chh if above else ty + 40
        ay = cy + chh if above else cy
        parts.append(f'<path d="M{slot} {ay} L{slot} {ty + (-22 if above else 22)} L{sx} {ty}" fill="none" stroke="{c}" stroke-opacity=".5" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{sx}" cy="{ty}" r="6" fill="#0B1020" stroke="{c}" stroke-width="2.5"/>')
        parts.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{chh}" rx="14" class="card"/>')
        parts.append(f'<rect x="{cx}" y="{cy + 18}" width="3" height="{chh - 36}" rx="1.5" fill="{c}"/>')
        parts.append(f'<text x="{cx + 22}" y="{cy + 28}" class="mono" fill="{c}">{dates}</text>')
        parts.append(f'<text x="{cx + 22}" y="{cy + 54}" class="title" style="font-size:18px">{escape(role)}</text>')
        parts.append(f'<text x="{cx + 22}" y="{cy + 76}" class="org">{escape(org)}</text>')
        parts.append(lines(cx + 22, cy + 102, desc, "small", 19))
    # pulsing "now" marker at the end of the line
    nx = yx(2026, 10)
    parts.append(f'<circle cx="{nx}" cy="{ty}" r="5" fill="#22D3EE" class="now"/>')
    parts.append(f'<circle cx="{nx}" cy="{ty}" r="5" fill="#22D3EE"/>')
    parts.append(f'<text x="{nx + 10}" y="{ty - 10}" class="mono" fill="#22D3EE">now</text>')
    return svg(W, H, "Experience timeline",
               "Timeline from 2022 to 2026: AI Intern at Talan Tunisie, AI Research Intern at UQAT, ML Research Engineer at Knowlepsy, PhD in Computer Science at Université Laval, and Course Lecturer and TA at Université Laval.",
               "", css, "\n".join(parts))


(OUT / "hero.svg").write_text(hero())
(OUT / "expertise.svg").write_text(expertise())
(OUT / "experience.svg").write_text(experience())
print("ok")


# ---------------------------------------------------------------- projects
def project(title, kicker, color, desc, tags, award=None):
    W, H = 580, 250
    css = """
      .card{fill:#0F172A;stroke:#1E293B;stroke-width:1.5}
      .link{font:600 13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#64748B}"""
    parts = [
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="{color}" stroke-opacity=".35"/>',
        f'<rect x="28" y="0" width="80" height="3" rx="1.5" fill="{color}"/>',
        f'<text x="28" y="44" class="mono" fill="{color}">{escape(kicker.upper())}</text>',
        f'<text x="28" y="76" class="title" style="font-size:22px">{escape(title)}</text>',
        lines(28, 108, desc, "body", 21),
        chips(28, H - 50, tags, color, W - 56),
        f'<text x="{W - 28}" y="44" text-anchor="end" class="link">view repo →</text>',
    ]
    if award:
        w = len(award) * 7.0 + 40
        parts.append(f'<rect x="{W - 28 - w:.0f}" y="{H - 50}" width="{w:.0f}" height="26" rx="13" fill="#FBBF24" fill-opacity=".15" stroke="#FBBF24" stroke-opacity=".6"/>')
        parts.append(f'<path d="M{W - 28 - w + 16:.0f} {H - 43} l3 6 6 1 -4.5 4 1 6 -5.5 -3 -5.5 3 1 -6 -4.5 -4 6 -1z" fill="#FBBF24"/>')
        parts.append(f'<text x="{W - 28 - w + 28:.0f}" y="{H - 33}" class="chip" style="fill:#FDE68A">{escape(award)}</text>')
    return svg(W, H, title, f"{kicker}: {' '.join(desc)}", "", css, "\n".join(parts))


PROJECTS = {
    "project-traffic": ("Network Traffic Classification", "Deep learning · Security", "#22D3EE",
        ["Detects and classifies cyberattacks in network traffic.", "Compares LSTM, Transformer, CNN-Transformer and",
         "FT-Transformer in one configurable pipeline."],
        ["TensorFlow", "LSTM", "Transformers", "scikit-learn"]),
    "project-mammogram": ("Mammogram Segmentation", "Computer vision · Health", "#F472B6",
        ["Django web app and comparative study of U-Net,", "Fuzzy C-Means and Expectation-Maximization for",
         "breast-cancer screening images."],
        ["U-Net", "Django", "Python"], "Best poster · DL Indaba"),
    "project-emotion": ("Facial Emotion Detection", "Computer vision · Real time", "#A78BFA",
        ["Real-time facial expression recognition with", "convolutional neural networks. Led the project",
         "team from objectives to delivery."],
        ["TensorFlow", "OpenCV", "CNN"]),
    "project-mario": ("Super Mario RL Agent", "Reinforcement learning", "#34D399",
        ["A Double-DQN agent with experience replay and a", "target network that learns to play Super Mario",
         "Bros from raw pixels."],
        ["TensorFlow", "DQN", "Gym"]),
}
for name, args in PROJECTS.items():
    (OUT / f"{name}.svg").write_text(project(*args))


# ---------------------------------------------------------------- highlights
def highlights():
    W, H, m, gap = 1200, 150, 20, 16
    tw = (W - 2 * m - 3 * gap) / 4
    tiles = [
        ("#22D3EE", "Industry ML", ["ML Research Engineer", "Knowlepsy · health data"]),
        ("#34D399", "5", ["university courses taught", "or assisted · Université Laval"]),
        ("#FBBF24", "Best poster", ["+ Ideathon winner", "Deep Learning Indaba"]),
        ("#F472B6", "Recognition", ["Departmental award for", "teaching · Université Laval"]),
    ]
    parts = []
    for i, (c, big, sub) in enumerate(tiles):
        x = m + i * (tw + gap)
        parts.append(f'<rect x="{x:.0f}" y="{m}" width="{tw:.0f}" height="{H - 2 * m}" rx="14" fill="#0F172A" stroke="#1E293B" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x + 22:.0f}" y="{m + 22}" width="3" height="{H - 2 * m - 44}" rx="1.5" fill="{c}"/>')
        parts.append(f'<text x="{x + 40:.0f}" y="{m + 50}" style="font:700 28px {SANS};fill:{c}">{escape(big)}</text>')
        parts.append(lines(int(x + 40), m + 76, sub, "small", 19))
    return svg(W, H, "Highlights", "Highlights: " + "; ".join(f"{b} {' '.join(s)}" for _, b, s in tiles), "", "", "\n".join(parts))


(OUT / "highlights.svg").write_text(highlights())
print("ok2")
