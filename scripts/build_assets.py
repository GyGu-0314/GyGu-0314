"""Generate the light/dark SVG assets used by the profile README.

Run from the repo root:  python scripts/build_assets.py
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", fg="#1f2328", dim="#59636e",
                  acc="#800000", acc2="#b35c00", chip="#f3e8e8", chipfg="#800000", ok="#1a7f37", link="#0969da"),
    "dark":  dict(bg="#0d1117", card="#161b22", border="#30363d", fg="#e6edf3", dim="#9198a1",
                  acc="#ff7b72", acc2="#e3b341", chip="#3a1d1d", chipfg="#ffa198", ok="#3fb950", link="#58a6ff"),
}
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def t(x, y, s, size=14, fill="fg", weight=400, family=SANS, anchor="start", extra="", c=None):
    color = c[fill] if fill in c else fill
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}" {extra}>{s}</text>')


def chips(x, y, labels, c, size=11.5, mono=True, gap=6):
    out, cx = [], x
    for lab in labels:
        w = len(lab) * size * 0.62 + 16
        out.append(f'<rect x="{cx}" y="{y}" width="{w:.0f}" height="22" rx="11" fill="{c["chip"]}"/>')
        out.append(t(cx + w / 2, y + 15, escape(lab), size, "chipfg", 500, MONO if mono else SANS, "middle", c=c))
        cx += w + gap
    return "".join(out)


def svg(w, h, body, c, label, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}"><style>{style}</style>'
            f'<defs><clipPath id="r"><rect width="{w}" height="{h}" rx="12"/></clipPath></defs>'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="{c["bg"]}"/>'
            f'<g clip-path="url(#r)">{body}</g>'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="none" stroke="{c["border"]}"/></svg>')


# ---------------------------------------------------------------- hero banner
def hero(c):
    W, H = 900, 270
    anim = (".l{opacity:0;animation:in .35s ease forwards}@keyframes in{to{opacity:1}}"
            ".cur{animation:b 1s step-end infinite}@keyframes b{50%{opacity:0}}")
    b = [
        f'<rect x="0" y="0" width="6" height="{H}" fill="{c["acc"]}"/>',
        t(40, 62, "HI, I'M", 13, "dim", 600, extra='letter-spacing="3"', c=c),
        t(40, 108, "Gaoyuan Gu", 44, "fg", 700, c=c),
        t(40, 142, "Data Scientist · MS Applied Data Science @ UChicago", 16, "fg", 500, c=c),
        t(40, 166, "Finance &amp; business roots, now building pipelines and models", 14, "dim", c=c),
        t(40, 186, "and measuring how much to trust them.", 14, "dim", c=c),
        chips(40, 208, ["big-data ETL", "computer vision", "bayesian ML", "quant finance"], c),
    ]
    # terminal
    X, Y, TW, TH = 535, 28, 340, 214
    b += [f'<rect x="{X}" y="{Y}" width="{TW}" height="{TH}" rx="10" fill="{c["card"]}" stroke="{c["border"]}"/>',
          *[f'<circle cx="{X+18+i*16}" cy="{Y+16}" r="5" fill="{col}"/>' for i, col in enumerate(["#ff5f57", "#febc2e", "#28c840"])],
          t(X + TW - 14, Y + 20, "🍪 ccds", 11, "dim", family=MONO, anchor="end", c=c)]
    lines = [
        (f'<tspan fill="{c["ok"]}">$</tspan> make hire', None),
        (f'<tspan fill="{c["dim"]}">degree   </tspan> MS ADS · GPA 4.00', None),
        (f'<tspan fill="{c["dim"]}">capstone </tspan> Argonne Natl. Lab', None),
        (f'<tspan fill="{c["dim"]}">based in </tspan> Chicago · relocatable', None),
        (f'<tspan fill="{c["dim"]}">speaks   </tspan> 中文 · English', None),
        (f'<tspan fill="{c["dim"]}">available</tspan> <tspan fill="{c["acc"]}" font-weight="700">Jan 2027</tspan>', None),
        (f'<tspan fill="{c["ok"]}">✔ ready to ship</tspan>', None),
    ]
    for i, (s, _) in enumerate(lines):
        b.append(t(X + 18, Y + 54 + i * 22, s, 13, "fg", family=MONO,
                   extra=f'class="l" style="animation-delay:{0.3 + i * 0.3:.1f}s"', c=c))
    b.append(f'<rect class="cur" x="{X+18}" y="{Y+54+len(lines)*22-12}" width="8" height="15" fill="{c["acc"]}"/>')
    return svg(W, H, "".join(b), c, "Gaoyuan Gu, Data Scientist, MS Applied Data Science at UChicago, available January 2027", anim)


# ---------------------------------------------------------------- timeline
def timeline(c):
    W, H = 900, 190
    events = [
        ("2021", "NYU Shanghai", "BS Business &amp; Finance", "Minor Math · Dean's List", "dim"),
        ("2023", "CSC Financial", "IB Intern · Public REITs", "5 REIT cash-flow models", "dim"),
        ("2024", "AstraZeneca China", "Data Analyst Intern", "2,000+ reps · 2 wk → 3 d", "dim"),
        ("2025", "UChicago", "MS Applied Data Science", "GPA 4.00 / 4.00", "dim"),
        ("2026", "Argonne Natl. Lab", "CV Capstone", "edge vision · solar sites", "dim"),
        ("JAN 2027", "Your team?", "Full-time DS / ML", "Chicago or relocate", "acc"),
    ]
    x0, x1, ly = 92, 808, 58
    step = (x1 - x0) / (len(events) - 1)
    b = [f'<line x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="{c["border"]}" stroke-width="2"/>',
         f'<line x1="{x0+step*4}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="{c["acc"]}" stroke-width="2" stroke-dasharray="5 5"/>']
    for i, (yr, org, role, note, col) in enumerate(events):
        x = x0 + i * step
        last = i == len(events) - 1
        b.append(t(x, 34, yr, 12, "acc" if last else "dim", 700, MONO, "middle", c=c))
        b.append(f'<circle cx="{x}" cy="{ly}" r="{8 if last else 6}" fill="{c["acc"] if last else c["bg"]}" stroke="{c["acc"]}" stroke-width="2.5"/>')
        b.append(t(x, 92, org, 14, "acc" if last else "fg", 700, anchor="middle", c=c))
        b.append(t(x, 114, role, 12, "fg", anchor="middle", c=c))
        b.append(t(x, 134, note, 11.5, "dim", anchor="middle", c=c))
    b.append(t(W / 2, 170, "data/raw  →  data/external  →  data/processed  →  models/", 11.5, "dim", family=MONO, anchor="middle", c=c))
    return svg(W, H, "".join(b), c, "Timeline: NYU Shanghai 2021, CSC Financial 2023, AstraZeneca 2024, UChicago 2025, Argonne 2026, available January 2027")


# ---------------------------------------------------------------- project cards
PROJECTS = {
    "argonne": dict(kicker="CAPSTONE · IN PROGRESS", title="Bird-Collision Detection",
                    sub="Edge-computing vision at utility-scale solar sites",
                    m1=("Edge AI", "on-device vision system"), m2=("Argonne", "research-scientist partners"),
                    tags=["computer-vision", "edge", "detection"], foot="UChicago × Argonne · Mar 2026 – now"),
    "deepfake": dict(kicker="BAYESIAN DEEP LEARNING", title="Deepfake Detection + Uncertainty",
                     sub="A detector that also says how sure it is",
                     m1=("0.736", "test AUC"), m2=("2.4×", "uncertainty gap vs MC Dropout"),
                     tags=["pytorch", "variational-inference", "streamlit"], foot="4-person team · Jan – Mar 2026"),
    "egorecall": dict(kicker="MULTIMODAL RETRIEVAL", title="EgoRecall on Ego4D",
                      sub="“Where did I leave my keys?” over 667 GB of video",
                      m1=("205s→3s", "frame extraction / video"), m2=("27.9%", "strict Top-100 (vs 25.0%)"),
                      tags=["clip", "faiss", "gcs"], foot="4-person team · Mar – Jun 2026"),
    "edge": dict(kicker="MODEL TRADE-OFFS", title="ResNet-50 vs. MobileNetV3",
                 sub="How much accuracy does 4× speed cost?",
                 m1=("99.6%", "ResNet-50 · 2.91 ms"), m2=("94.0%", "MobileNetV3 · 0.72 ms"),
                 tags=["transfer-learning", "grad-cam", "latency"], foot="4-person team · Mar – Jun 2026"),
    "amazon": dict(kicker="BIG DATA · SOLO", title="64.7M Amazon Reviews",
                   sub="PySpark ETL on GCS + review-fraud analysis",
                   m1=("52.4 GiB", "nested Parquet, restartable"), m2=("9.5%→2.7%", "near-dupes after 2022"),
                   tags=["pyspark", "gcp", "minhash-lsh"], foot="Solo · Nov – Dec 2025"),
    "thesis": dict(kicker="QUANT RESEARCH · THESIS", title="SSE 50 ETF Options Efficiency",
                   sub="When and why does the market misprice options?",
                   m1=("20K+", "obs over 6 years"), m2=("ANOVA", "arbitrage windows found"),
                   tags=["options", "time-series", "statistics"], foot="NYU Shanghai · Mar – May 2025"),
}


def card(p, c):
    W, H = 440, 220
    b = [f'<rect x="0" y="0" width="{W}" height="4" fill="{c["acc"]}"/>',
         t(22, 34, p["kicker"], 11, "acc", 700, extra='letter-spacing="1.2"', c=c),
         t(22, 62, escape(p["title"]), 20, "fg", 700, c=c),
         t(22, 84, escape(p["sub"]), 13, "dim", c=c)]
    for i, (big, small) in enumerate([p["m1"], p["m2"]]):
        x = 22 + i * 205
        b.append(t(x, 128, escape(big), 26, "acc2", 700, c=c))
        b.append(t(x, 148, escape(small), 12, "dim", c=c))
    b.append(chips(22, 164, p["tags"], c, size=11))
    b.append(t(W - 22, 206, escape(p["foot"]), 11, "dim", anchor="end", c=c))
    return svg(W, H, "".join(b), c, f'{p["title"]}: {p["sub"]}')


# ---------------------------------------------------------------- fit section
def fit(c):
    W, H = 900, 230
    cols = [
        ("📊", "Analytics &amp; BI", "data analyst · BI · commercial ops",
         ["Sales-awards model for 10+ teams", "Payout disputes: 2 weeks → 3 days", "Power BI · Tableau · SQL · Excel/VBA"]),
        ("🧠", "ML &amp; Computer Vision", "data scientist · ML engineer",
         ["Argonne edge-vision capstone", "CLIP + FAISS retrieval on 667 GB", "PyTorch · Bayesian DL · PySpark"]),
        ("📈", "Quant &amp; Finance", "quant research · risk · fintech",
         ["Options-market efficiency thesis", "Cash-flow models for 5 public REITs", "Stats · time series · sensitivity"]),
    ]
    cw, gap, x0 = 272, 14, 22
    b = []
    for i, (ico, head, roles, pts) in enumerate(cols):
        x = x0 + i * (cw + gap)
        b.append(f'<rect x="{x}" y="22" width="{cw}" height="{H-44}" rx="10" fill="{c["card"]}" stroke="{c["border"]}"/>')
        b.append(t(x + 18, 58, ico, 22, "fg", c=c))
        b.append(t(x + 52, 56, head, 17, "fg", 700, c=c))
        b.append(t(x + 18, 84, roles, 12, "acc", 600, c=c))
        for j, pt in enumerate(pts):
            y = 116 + j * 28
            b.append(f'<circle cx="{x+22}" cy="{y-4}" r="3" fill="{c["acc2"]}"/>')
            b.append(t(x + 34, y, escape(pt).replace("&amp;amp;", "&amp;"), 12.5, "fg", c=c))
    return svg(W, H, "".join(b), c, "Where I fit: Analytics and BI, ML and Computer Vision, Quant and Finance")


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for name, c in THEMES.items():
        (OUT / f"hero-{name}.svg").write_text(hero(c))
        (OUT / f"timeline-{name}.svg").write_text(timeline(c))
        (OUT / f"fit-{name}.svg").write_text(fit(c))
        for key, p in PROJECTS.items():
            (OUT / f"card-{key}-{name}.svg").write_text(card(p, c))


if __name__ == "__main__":
    main()
