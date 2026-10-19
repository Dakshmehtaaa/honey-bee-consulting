"""The four service pictures on the homepage ("Four ways we help you win"): simple motion drawings, no bees.

Each picture is one SVG plus its own keyframes. The SVG's attributes are the finished frame, so calm
mode, reduced motion and no-JS show a complete picture; the animation only runs inside `.pv-play`
(a card that is hovered or focused, or the open service panel) under `.motion`.

Every animated element gets a class `pvN-k` and a timeline of (second, css) keys on one shared
8-second loop. build-pages.py writes the keyframes to dist/assets/pillars.css.
No ids anywhere, so a picture can be cloned into the panel without breaking the page's ids."""

LOOP = 8.0
INK, FOREST, POLLEN, CLAY, TEAL, PAPER, SAGE, LINE, MUTED = "#17291F", "#284F38", "#EABB35", "#C9693F", "#3F7F78", "#FFFFFB", "#E6ECDC", "#DEDDCF", "#8A968C"


class Pic:
    def __init__(self, n):
        self.n, self.k, self.css = n, 0, []

    def anim(self, keys, origin=None):
        """keys: [(second, css)]; holds the first value before and the last value after."""
        self.k += 1
        name = f"pv{self.n}-{self.k}"
        steps = [(0, keys[0][1])] + [(t / LOOP * 100, v) for t, v in keys] + [(100, keys[-1][1])]
        frames = "".join(f"{p:.2f}%{{{v}}}" for p, v in steps)
        o = f"transform-origin:{origin};" if origin else ""
        box = "transform-box:fill-box;" if origin and "px" not in origin else ""
        self.css.append(f"@keyframes {name}{{{frames}}}.motion .pv-play .{name}{{{box}{o}animation:{name} {LOOP}s linear infinite}}")
        return name

    # --- reusable timelines ---
    def draw(self, t0, t1, out=7.6):
        return self.anim([(t0, "stroke-dashoffset:1;opacity:0"), (t0 + .03, "stroke-dashoffset:.97;opacity:1"), (t1, "stroke-dashoffset:0"), (out, "stroke-dashoffset:0;opacity:1"), (LOOP, "stroke-dashoffset:0;opacity:0")])

    def pop(self, t0, t1=None, out=7.6, origin="50% 50%"):
        t1 = t1 or t0 + .45
        return self.anim([(t0, "opacity:0;transform:scale(.4)"), (t1 - .12, "opacity:1;transform:scale(1.08)"), (t1, "opacity:1;transform:scale(1)"),
                          (out, "opacity:1;transform:scale(1)"), (LOOP, "opacity:0;transform:scale(1)")], origin)

    def fade(self, t0, t1=None, out=7.6, dy=0, dx=0):
        t1 = t1 or t0 + .5
        return self.anim([(t0, f"opacity:0;transform:translate({dx}px,{dy}px)"), (t1, "opacity:1;transform:translate(0,0)"),
                          (out, "opacity:1;transform:translate(0,0)"), (LOOP, "opacity:0;transform:translate(0,0)")])

    def grow(self, t0, t1, origin="50% 100%", axis="Y", out=7.6):
        return self.anim([(t0, f"transform:scale{axis}(0)"), (t1, f"transform:scale{axis}(1)"), (out, f"transform:scale{axis}(1);opacity:1"), (LOOP, f"transform:scale{axis}(1);opacity:0")], origin)

    def svg(self, inner, label):
        return (f'<svg class="pv pv{self.n}" viewBox="0 0 480 360" role="img" aria-label="{label}" focusable="false">'
                f'<rect width="480" height="360" fill="none"/>{inner}</svg>')


def D(cls, d, stroke=INK, w=4, extra=""):
    """A stroke that can draw itself on (pathLength 1 + dasharray in CSS)."""
    return f'<path class="pv-draw {cls}" pathLength="1" d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'


# ---------------------------------------------------------------- 1 · ratings & certifications
def ratings():
    p = Pic(1)
    s = []
    # score card with a gauge
    s.append(f'<rect x="34" y="40" width="252" height="280" rx="22" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<rect x="34" y="40" width="252" height="46" rx="22" fill="{SAGE}"/><rect x="34" y="66" width="252" height="20" fill="{SAGE}"/>')
    s.append(f'<path d="M34 86H286" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<text x="58" y="70" font-family="DM Sans,Arial,sans-serif" font-size="17" font-weight="700" fill="{INK}" letter-spacing="1.5">CSR SCORE</text>')
    cx, cy, r = 160, 228, 78
    # gauge arcs (clay → amber → green), drawn left to right
    s.append(f'<path d="M{cx - r} {cy}A{r} {r} 0 0 1 {cx + r} {cy}" fill="none" stroke="{LINE}" stroke-width="22" stroke-linecap="round"/>')
    import math
    def arc(a0, a1, col, t0, t1):
        x0, y0 = cx - r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
        x1, y1 = cx - r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        return D(p.draw(t0, t1), f"M{x0:.1f} {y0:.1f}A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}", col, 22, ' stroke-linecap="butt"')
    s.append(arc(2, 62, CLAY, .2, .7) + arc(62, 118, POLLEN, .7, 1.2) + arc(118, 178, "#4F7A45", 1.2, 1.7))
    # needle sweeps from low to high
    needle = p.anim([(0, "transform:rotate(-78deg)"), (1.8, "transform:rotate(-78deg)"), (2.6, "transform:rotate(-30deg)"), (3.0, "transform:rotate(-36deg)"),
                     (3.8, "transform:rotate(38deg)"), (4.2, "transform:rotate(34deg)"), (7.6, "transform:rotate(34deg)"), (LOOP, "transform:rotate(-78deg)")], f"{cx}px {cy}px")
    s.append(f'<g class="{needle}" style="transform:rotate(34deg);transform-origin:{cx}px {cy}px"><path d="M{cx} {cy}V{cy - 62}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="13" fill="{INK}"/>')
    # the number swaps 42 → 61 → 78
    for val, t_in, t_out, col in (("42", 0, 2.6, CLAY), ("61", 2.6, 3.8, "#B08419"), ("78", 3.8, None, "#4F7A45")):
        keys = [(t_in, "opacity:1")] if t_in == 0 else [(t_in - .01, "opacity:0"), (t_in, "opacity:1")]
        if t_out:
            keys += [(t_out - .01, "opacity:1"), (t_out, "opacity:0")]
        else:
            keys += [(7.6, "opacity:1"), (LOOP, "opacity:0")]
        cls = p.anim(keys)
        s.append(f'<text class="{cls}" x="{cx}" y="{cy + 54}" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="44" font-weight="700" fill="{col}"'
                 f'{"" if val == "78" else " opacity=\"0\""}>{val}<tspan font-size="18" fill="{MUTED}">/100</tspan></text>')
    # medal tiers light up
    for i, (col, t) in enumerate(((CLAY, 2.2), ("#A9B3AA", 3.0), (POLLEN, 3.8))):
        x = 70 + i * 32
        s.append(f'<circle cx="{x}" cy="114" r="11" fill="{LINE}"/>')
        s.append(f'<circle class="{p.pop(t)}" cx="{x}" cy="114" r="11" fill="{col}" stroke="{INK}" stroke-width="2.5"/>')
    s.append(f'<text x="252" y="119" text-anchor="end" font-family="DM Sans,Arial,sans-serif" font-size="14" font-weight="700" fill="{MUTED}" letter-spacing="1">LEVEL</text>')
    # checklist card on the right, ticks draw one by one
    s.append(f'<rect x="306" y="40" width="146" height="196" rx="18" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    for i in range(4):
        y = 76 + i * 40
        s.append(f'<rect x="324" y="{y - 12}" width="24" height="24" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>')
        s.append(D(p.draw(.5 + i * .45, .8 + i * .45), f"M329 {y}l6 6 11 -12", FOREST, 4.5))
        s.append(f'<path d="M360 {y}H{430 - (i % 2) * 18}" stroke="{LINE}" stroke-width="7" stroke-linecap="round"/>')
    # the certificate seal stamps in
    seal = p.anim([(0, "opacity:0;transform:scale(1.9) rotate(-25deg)"), (4.6, "opacity:0;transform:scale(1.9) rotate(-25deg)"), (4.95, "opacity:1;transform:scale(.92) rotate(0)"),
                   (5.15, "opacity:1;transform:scale(1) rotate(0)"), (7.6, "opacity:1;transform:scale(1) rotate(0)"), (LOOP, "opacity:0;transform:scale(1) rotate(0)")], "50% 50%")
    pts = " ".join(f"{379 + (44 if k % 2 == 0 else 37) * math.cos(math.radians(k * 15)):.1f},{288 + (44 if k % 2 == 0 else 37) * math.sin(math.radians(k * 15)):.1f}" for k in range(24))
    s.append(f'<g class="{seal}"><path d="M356 316l-12 34 18-8 10 16 8-30z M402 316l12 34-18-8-10 16-8-30z" fill="{CLAY}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
             f'<polygon points="{pts}" fill="{POLLEN}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
             f'<circle cx="379" cy="288" r="27" fill="none" stroke="{INK}" stroke-width="2.5"/>'
             f'<path d="M366 289l9 9 17-19" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>')
    # little sparkles once the seal lands
    for i, (x, y) in enumerate(((326, 262), (436, 250), (440, 318))):
        s.append(f'<path class="{p.pop(5.1 + i * .12)}" d="M{x} {y - 9}v18M{x - 9} {y}h18" stroke="{POLLEN}" stroke-width="4" stroke-linecap="round"/>')
    return p.svg("".join(s), "A CSR score rises from 42 to 78 out of 100, checklist items get ticked and a certificate seal is awarded"), p.css


# ---------------------------------------------------------------- 2 · data, AI & automation
def data():
    p = Pic(2)
    s = []
    # three messy sources on the left
    srcs = ((70, 70, "XLS", FOREST), (70, 180, "PDF", CLAY), (70, 290, "@", TEAL))
    for i, (x, y, t, col) in enumerate(srcs):
        s.append(f'<g transform="translate({x} {y})"><path d="M-30 -38h40l20 20v56h-60z" fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                 f'<path d="M10 -38v20h20" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                 f'<rect x="-22" y="-6" width="44" height="20" rx="5" fill="{col}"/>'
                 f'<text x="0" y="9" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="14" font-weight="700" fill="{PAPER}">{t}</text>'
                 f'<path d="M-20 26h28" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/></g>')
    # pipes into the chip and out to the dashboard
    for y in (70, 180, 290):
        s.append(f'<path d="M106 {y}C150 {y} 160 180 196 180" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>')
    s.append(f'<path d="M284 180H322" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>')
    # the AI chip
    pulse = p.anim([(0, "opacity:0;transform:scale(1)"), (1.4, "opacity:.6;transform:scale(1)"), (2.2, "opacity:0;transform:scale(1.5)"),
                    (2.4, "opacity:0;transform:scale(1)"), (3.0, "opacity:.6;transform:scale(1)"), (3.8, "opacity:0;transform:scale(1.5)")], "240px 180px")
    s.append(f'<rect class="{pulse}" x="196" y="136" width="88" height="88" rx="20" fill="none" stroke="{POLLEN}" stroke-width="6" opacity="0"/>')
    for k in range(4):
        x, y = 210 + k * 20, 150 + k * 20
        s.append(f'<path d="M{x} 136v-12M{x} 224v12M196 {y}h-12M284 {y}h12" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    s.append(f'<rect x="196" y="136" width="88" height="88" rx="20" fill="{INK}"/>')
    s.append(f'<text x="240" y="194" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="34" font-weight="700" fill="{POLLEN}">AI</text>')
    spark = p.anim([(0, "transform:rotate(0) scale(1)"), (1.4, "transform:rotate(0) scale(1)"), (1.8, "transform:rotate(90deg) scale(1.3)"), (2.2, "transform:rotate(180deg) scale(1)"),
                    (3.0, "transform:rotate(180deg) scale(1)"), (3.4, "transform:rotate(270deg) scale(1.3)"), (3.8, "transform:rotate(360deg) scale(1)")], "50% 50%")
    s.append(f'<path class="{spark}" d="M272 128l3 8 8 3-8 3-3 8-3-8-8-3 8-3z" fill="{POLLEN}" stroke="{INK}" stroke-width="2"/>')
    # messy packets travel source → chip; clean rows travel chip → dashboard
    cols = (CLAY, TEAL, FOREST, POLLEN, CLAY, TEAL)
    for i in range(6):
        sy = (70, 180, 290)[i % 3]
        t0 = .2 + i * .32
        cls = p.anim([(t0, f"opacity:0;transform:translate(0px,0px) rotate({(i % 3 - 1) * 30}deg)"), (t0 + .1, f"opacity:1;transform:translate(0px,0px) rotate({(i % 3 - 1) * 30}deg)"),
                      (t0 + .9, f"opacity:1;transform:translate(110px,{180 - sy}px) rotate(0deg)"), (t0 + 1.0, f"opacity:0;transform:translate(118px,{180 - sy}px) rotate(0deg)")], "50% 50%")
        s.append(f'<rect class="{cls}" x="104" y="{sy - 7}" width="{12 + (i % 2) * 6}" height="14" rx="3" fill="{cols[i]}" stroke="{INK}" stroke-width="2" opacity="0"/>')
    for i in range(4):
        t0 = 1.6 + i * .4
        cls = p.anim([(t0, "opacity:0;transform:translateX(0px)"), (t0 + .1, "opacity:1;transform:translateX(0px)"), (t0 + .5, "opacity:1;transform:translateX(42px)"), (t0 + .6, "opacity:0;transform:translateX(48px)")])
        s.append(f'<rect class="{cls}" x="284" y="174" width="18" height="12" rx="3" fill="{FOREST}" opacity="0"/>')
    # the dashboard
    s.append(f'<rect x="326" y="74" width="132" height="212" rx="18" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<path d="M342 98h56" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><circle cx="440" cy="98" r="6" fill="#4F7A45"/>')
    for i, (h, col) in enumerate(((44, TEAL), (66, FOREST), (54, TEAL), (88, POLLEN))):
        x = 344 + i * 27
        s.append(f'<rect class="{p.grow(2.0 + i * .35, 2.5 + i * .35)}" x="{x}" y="{220 - h}" width="18" height="{h}" rx="4" fill="{col}"/>')
    s.append(f'<path d="M340 222H446" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    s.append(D(p.draw(3.6, 4.4), "M344 258c14-10 24 4 38-6s24-16 36-8 18-2 26-10", FOREST, 4))
    # validated badge
    s.append(f'<g class="{p.pop(4.6)}"><circle cx="452" cy="74" r="22" fill="#4F7A45" stroke="{INK}" stroke-width="3"/>'
             f'<path d="M441 74l8 8 14-15" fill="none" stroke="{PAPER}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>')
    # pills: time and cost saved
    s.append(f'<g class="{p.fade(5.0, 5.5, dy=10)}"><rect x="186" y="252" width="136" height="40" rx="20" fill="{POLLEN}" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="207" cy="272" r="10" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/><path d="M207 266v6l4 3.5" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
             f'<text x="224" y="278" font-family="DM Sans,Arial,sans-serif" font-size="17" font-weight="700" fill="{INK}">-70% time</text></g>')
    s.append(f'<g class="{p.fade(5.4, 5.9, dy=10)}"><rect x="186" y="300" width="136" height="40" rx="20" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="207" cy="320" r="10" fill="{POLLEN}" stroke="{INK}" stroke-width="2.5"/><text x="207" y="325" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="13" font-weight="700" fill="{INK}">€</text>'
             f'<text x="224" y="326" font-family="DM Sans,Arial,sans-serif" font-size="17" font-weight="700" fill="{INK}">-50% cost</text></g>')
    return p.svg("".join(s), "Spreadsheets, PDFs and emails flow into an AI chip and come out as a checked dashboard: 70% less time and 50% lower cost"), p.css


# ---------------------------------------------------------------- 3 · reporting & narrative
def reporting():
    p = Pic(3)
    s = []
    # the report builds itself
    s.append(f'<rect x="150" y="30" width="180" height="300" rx="16" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<rect class="{p.grow(.1, .5, "0% 50%", "X")}" x="170" y="52" width="140" height="28" rx="8" fill="{FOREST}"/>')
    s.append(f'<text class="{p.fade(.4, .7)}" x="182" y="72" font-family="DM Sans,Arial,sans-serif" font-size="15" font-weight="700" fill="{PAPER}" letter-spacing="1">ESG REPORT</text>')
    for i, (val, lab, col) in enumerate((("-32%", "CO₂", "#4F7A45"), ("94%", "TEAM", TEAL))):
        x = 170 + i * 74
        s.append(f'<g class="{p.pop(.8 + i * .3)}"><rect x="{x}" y="94" width="66" height="58" rx="10" fill="{SAGE}" stroke="{INK}" stroke-width="2.5"/>'
                 f'<text x="{x + 33}" y="123" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="21" font-weight="700" fill="{col}">{val}</text>'
                 f'<text x="{x + 33}" y="142" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="11" font-weight="700" fill="{MUTED}" letter-spacing="1">{lab}</text></g>')
    for i, h in enumerate((30, 44, 38, 60, 72)):
        s.append(f'<rect class="{p.grow(1.4 + i * .15, 1.8 + i * .15)}" x="{176 + i * 26}" y="{238 - h}" width="16" height="{h}" rx="3" fill="{POLLEN if i == 4 else TEAL}"/>')
    s.append(f'<path d="M168 240H312" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    for i, w in enumerate((130, 112, 124)):
        s.append(D(p.draw(2.2 + i * .2, 2.6 + i * .2), f"M172 {264 + i * 20}h{w}", LINE, 7))
    # it goes out to three audiences
    aud = ((70, 90, "clients"), (410, 90, "investors"), (410, 270, "teams"))
    links = ("M150 120C120 110 106 100 96 96", "M330 120C360 110 374 100 384 96", "M330 250C360 258 372 264 384 266")
    for i, ((x, y, who), d) in enumerate(zip(aud, links)):
        s.append(D(p.draw(3.0 + i * .5, 3.4 + i * .5), d, FOREST, 3, ' stroke-dasharray="1 1"'))
        g = p.pop(3.4 + i * .5)
        if who == "clients":
            icon = (f'<path d="M{x - 18} {y + 16}V{y - 6}l12-8v8l12-8v8l12-8v24z" fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                    f'<path d="M{x - 10} {y + 4}h4M{x + 2} {y + 4}h4M{x + 12} {y + 4}h2" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
        elif who == "investors":
            icon = (f'<path d="M{x - 18} {y + 14}l12-12 8 8 16-18" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
                    f'<path d="M{x + 8} {y - 8}h10v10" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            icon = "".join(f'<circle cx="{x + dx}" cy="{y - 8}" r="6" fill="{PAPER}" stroke="{INK}" stroke-width="3"/><path d="M{x + dx - 10} {y + 14}a10 10 0 0 1 20 0" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>' for dx in (-12, 12))
        bg = (POLLEN, SAGE, "#DCEDEA")[i]
        s.append(f'<g class="{g}"><circle cx="{x}" cy="{y}" r="38" fill="{bg}" stroke="{INK}" stroke-width="3"/>{icon}</g>')
    # a speech bubble: the story lands
    s.append(f'<g class="{p.fade(5.0, 5.5, dy=12)}"><path d="M30 214h96a12 12 0 0 1 12 12v40a12 12 0 0 1-12 12H70l-16 16v-16H30a12 12 0 0 1-12-12v-40a12 12 0 0 1 12-12z" fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
             f'<path d="M34 238h80M34 256h56" stroke="{FOREST}" stroke-width="6" stroke-linecap="round"/></g>')
    s.append(f'<path class="{p.pop(5.6)}" d="M116 256l3 7 7 3-7 3-3 7-3-7-7-3 7-3z" fill="{POLLEN}" stroke="{INK}" stroke-width="2"/>')
    return p.svg("".join(s), "An ESG report builds itself from numbers and charts, then reaches clients, investors and teams as a clear story"), p.css


# ---------------------------------------------------------------- 4 · environmental & social impact
def impact():
    p = Pic(4)
    s = []
    s.append(f'<circle class="{p.pop(.1, .6)}" cx="64" cy="64" r="26" fill="{POLLEN}" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<path d="M0 300H480" stroke="{INK}" stroke-width="3"/><rect x="0" y="301" width="480" height="59" fill="{SAGE}"/>')
    # the factory
    s.append(f'<path d="M40 300V206l44 -26v26l44-26v26l44-26V300z" fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    s.append(f'<rect x="140" y="118" width="22" height="70" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    for i in range(3):
        s.append(f'<rect x="{58 + i * 40}" y="238" width="22" height="22" rx="3" fill="{POLLEN}" stroke="{INK}" stroke-width="2.5"/>')
    # smoke: big puffs that fade away
    for i, (x, y, r) in enumerate(((152, 96, 16), (166, 68, 20), (186, 40, 22))):
        cls = p.anim([(0, "opacity:.9;transform:scale(1)"), (.6 + i * .2, "opacity:.9;transform:scale(1)"), (1.6 + i * .3, "opacity:0;transform:scale(.3)"),
                      (7.6, "opacity:0;transform:scale(.3)"), (LOOP, "opacity:.9;transform:scale(1)")], "50% 50%")
        s.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r}" fill="#A9B3AA" stroke="{INK}" stroke-width="2.5" opacity="0"/>')
    # solar panels land on the roof
    for i in range(3):
        cls = p.anim([(1.8 + i * .25, "opacity:0;transform:translateY(-40px)"), (2.2 + i * .25, "opacity:1;transform:translateY(0)"), (7.6, "opacity:1;transform:translateY(0)"), (LOOP, "opacity:0;transform:translateY(0)")])
        x = 46 + i * 44
        s.append(f'<g class="{cls}"><path d="M{x} {200 - i * 0}l30 -18v10l-30 18z" fill="{TEAL}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/></g>')
    # CO2 bars go down year by year
    s.append(f'<rect x="232" y="40" width="160" height="128" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<text x="248" y="64" font-family="DM Sans,Arial,sans-serif" font-size="14" font-weight="700" fill="{MUTED}" letter-spacing="1">CO₂ / YEAR</text>')
    for i, (h, col) in enumerate(((70, CLAY), (48, POLLEN), (28, "#4F7A45"))):
        s.append(f'<rect class="{p.grow(.6 + i * .5, 1.0 + i * .5)}" x="{256 + i * 40}" y="{152 - h}" width="26" height="{h}" rx="4" fill="{col}"/>')
    s.append(f'<path d="M248 154H376" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    s.append(f'<g class="{p.pop(2.3)}"><path d="M352 74l18 18M370 76v16h-16" fill="none" stroke="#4F7A45" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>')
    # trees grow
    for i, (x, h) in enumerate(((236, 58), (282, 82), (330, 66))):
        cls = p.grow(2.6 + i * .3, 3.2 + i * .3)
        s.append(f'<g class="{cls}"><path d="M{x} 300V{300 - h * .45}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                 f'<circle cx="{x}" cy="{300 - h * .7}" r="{h * .36:.0f}" fill="{"#4F7A45" if i != 1 else FOREST}" stroke="{INK}" stroke-width="3"/></g>')
    # people with a heart
    for i, x in enumerate((392, 436)):
        s.append(f'<g class="{p.fade(3.8 + i * .25, 4.3 + i * .25, dy=16)}"><circle cx="{x}" cy="246" r="11" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
                 f'<path d="M{x - 17} 300v-14a17 17 0 0 1 34 0v14" fill="{(POLLEN, TEAL)[i]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/></g>')
    s.append(f'<path class="{p.pop(4.7)}" d="M414 222c-10-8-16-13-16-20a8 8 0 0 1 16-3 8 8 0 0 1 16 3c0 7-6 12-16 20z" fill="{CLAY}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
    return p.svg("".join(s), "A factory's smoke clears, solar panels go up, CO2 bars fall year by year, trees grow and people get support"), p.css


PILLARS = {"ratings": ratings, "data": data, "reporting": reporting, "impact": impact}


def stylesheet():
    base = (".pv{width:100%;height:100%;display:block}\n.pv-draw{stroke-dasharray:1 1;stroke-dashoffset:0}\n"
            "/* generated by scripts/build-pages.py from scripts/brand/pillars.py: don't edit by hand */\n")
    return base + "\n".join(css for f in PILLARS.values() for css in f()[1]) + "\n"


# ---------------------------------------------------------------- the still card covers
# At rest each card shows one simple picture: its bee (from site_art.CREW) next to one big chart.
# Hover or focus cross-fades to the motion picture above.
F = 'font-family="DM Sans,Arial,sans-serif" font-weight="700"'


def _card(x, y, w, h):
    return f'<rect x="{x + 6}" y="{y + 8}" width="{w}" height="{h}" rx="22" fill="{INK}" opacity=".12"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'


def _chart(kind):
    if kind == "ratings":    # a score that climbs into the green
        return (_card(214, 52, 236, 248)
                + f'<text x="242" y="102" {F} font-size="16" fill="{MUTED}" letter-spacing="1.5">CSR SCORE</text>'
                + f'<text x="240" y="176" {F} font-size="76" fill="#4F7A45">78</text><text x="336" y="176" {F} font-size="24" fill="{MUTED}">/100</text>'
                + "".join(f'<rect x="{244 + i * 58}" y="{278 - h}" width="40" height="{h}" rx="7" fill="{c}" stroke="{INK}" stroke-width="3"/>' for i, (h, c) in enumerate(((34, CLAY), (58, POLLEN), (82, "#4F7A45"))))
                + f'<circle cx="420" cy="88" r="20" fill="#4F7A45" stroke="{INK}" stroke-width="3"/><path d="M410 88l7 7 13-14" fill="none" stroke="{PAPER}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "data":       # a dashboard that goes up
        bars = ((60, TEAL), (96, FOREST), (78, TEAL), (132, POLLEN))
        return (_card(214, 52, 236, 248)
                + f'<path d="M240 84h80" stroke="{INK}" stroke-width="8" stroke-linecap="round"/><circle cx="420" cy="84" r="9" fill="#4F7A45"/>'
                + "".join(f'<rect x="{242 + i * 50}" y="{270 - h}" width="34" height="{h}" rx="6" fill="{c}" stroke="{INK}" stroke-width="3"/>' for i, (h, c) in enumerate(bars))
                + f'<path d="M236 272H428" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
                + f'<path d="M259 196 309 160 359 178 409 120" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>' for x, y in ((259, 196), (309, 160), (359, 178), (409, 120))))
    if kind == "reporting":  # a report with a donut and a few lines, on the same size of paper as the others
        return (_card(214, 52, 236, 248)
                + f'<path d="M406 54l42 42h-30a12 12 0 0 1-12-12z" fill="{SAGE}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                + f'<rect x="240" y="76" width="104" height="20" rx="6" fill="{FOREST}"/>'
                + f'<circle cx="286" cy="158" r="36" fill="none" stroke="{LINE}" stroke-width="20"/>'
                + f'<path d="M286 122a36 36 0 1 1-34.2 47.1" fill="none" stroke="{TEAL}" stroke-width="20"/><path d="M251.8 169.1A36 36 0 0 1 286 122" fill="none" stroke="{POLLEN}" stroke-width="20"/>'
                + f'<text x="342" y="154" {F} font-size="26" fill="{TEAL}">-32%</text><text x="344" y="176" {F} font-size="13" fill="{MUTED}" letter-spacing="1">CO₂</text>'
                + "".join(f'<path d="M242 {226 + i * 22}h{w}" stroke="{LINE}" stroke-width="9" stroke-linecap="round"/>' for i, w in enumerate((176, 140, 160))))
    # impact: emissions come down year after year
    return (_card(214, 52, 236, 248)
            + f'<text x="240" y="98" {F} font-size="16" fill="{MUTED}" letter-spacing="1.5">CO₂ / YEAR</text>'
            + "".join(f'<rect x="{244 + i * 60}" y="{272 - h}" width="42" height="{h}" rx="7" fill="{c}" stroke="{INK}" stroke-width="3"/>' for i, (h, c) in enumerate(((140, CLAY), (96, POLLEN), (52, "#4F7A45"))))
            + f'<path d="M236 274H432" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
            + f'<path d="M378 92l40 40M420 100v34h-34" fill="none" stroke="#4F7A45" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')


def cover(kind):
    import site_art
    bee = site_art.crew({"ratings": "inspector", "data": "engineer", "reporting": "storyteller", "impact": "gardener"}[kind])()
    inner = bee[bee.index('>') + 1:bee.rindex('</svg>')]
    return (f'<svg class="pv-cover" viewBox="0 0 480 360" aria-hidden="true" focusable="false"><g transform="translate(-30 -26) scale(1.1)">{_chart(kind)}</g>'
            f'<svg x="-26" y="84" width="226" height="226" viewBox="0 0 200 200" overflow="visible">{inner}</svg></svg>')


COVERS = {k: (lambda k: lambda: cover(k))(k) for k in PILLARS}
