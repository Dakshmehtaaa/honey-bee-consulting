"""Draws the website illustrations. scripts/build-pages.py writes them into the pages.

Each entry in PIECES returns one SVG (or a small block of markup). Class names inside the art
(.bloom, .cell, .rise, .lit, .fly-in…) are the hooks story.css animates. Gradients live once per
page in the "defs" piece, so the pictures can share them."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from bees import bee_solid, front_bee

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'dist')


def svg_el(vb, inner, cls, label=None):
    a = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    return f'<svg class="{cls}" viewBox="{vb}" xmlns="http://www.w3.org/2000/svg"{a} focusable="false">{inner}</svg>'


def shared_defs():
    """Gradients every picture on the page refers to. Kept out of display:none so they paint."""
    return (f'<svg class="svg-defs" width="0" height="0" aria-hidden="true" focusable="false">'
            f'{defs()}{comb_defs()}</svg>')


def bloom(i, x, y, inner):
    """Wraps a flower so it can grow from its base (x, y)."""
    return f'<g class="bloom" style="--i:{i};transform-origin:{x}px {y}px">{inner}</g>'


def bee_g(x, y, s, angle, prop=None, hat=None, flip=False, cls="bee-svg"):
    inner = fly(bee(prop=prop, hat=hat), angle=angle)
    return f'<g class="{cls}" transform="translate({x},{y}) scale({-s if flip else s},{s}) translate(-100,-92)">{inner}</g>'


# ---------- hero: the meadow feeds the comb ----------
def hero():
    W, H = 640, 560
    s = [f'<circle cx="430" cy="236" r="232" fill="#FBF1D3"/>', glow(440, 230, 300)]
    # the branch the comb hangs from
    s.append(branch("M246,92 C330,80 430,76 520,80 S610,70 650,60", sw=3,
                    leaves=((300, 84, -150, 46), (352, 80, -32, 40), (566, 76, -160, 42), (612, 66, -20, 38))))
    # wax where the comb is glued to the twig
    s.append(f'<path d="M352,92 C380,74 470,72 496,90 L484,104 H364 Z" fill="url(#g-wax)" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    cells = [(0, 0, "capped"), (1, 0, "honey"), (-1, 1, "honey"), (0, 1, "honey"), (1, 1, "capped"),
             (-1, 2, "honey"), (0, 2, "empty"), (1, 2, "honey"), (0, 3, "honey"), (-1, 3, "capped")]
    s.append(f'<g class="hero-comb">{comb(396, 136, 44, cells, sw=3.4)}</g>')
    s.append(drip(434, 375, 52, w=10))
    # ground and meadow
    s.append(hill(f"M0,{H} V476 C120,452 250,462 340,486 C420,508 520,500 640,486 V{H} Z", "url(#g-hill-b)"))
    s.append(hill(f"M0,{H} V512 C140,496 300,506 420,526 C500,538 580,536 640,530 V{H} Z", "url(#g-hill-c)"))
    s.append(bloom(0, 48, 520, stem(48, 530, 44, 384, bend=14, leaves=((.4, 1), (.6, -1)), leaf=24, sw=2.6) + petal_flower(44, 382, 32, n=11, rot=12, sw=2.6)))
    s.append(bloom(1, 150, 520, stem(152, 520, 146, 318, bend=-18, leaves=((.42, 1), (.62, -1)), leaf=30, sw=3) + petal_flower(146, 318, 58, n=12, rot=6, sw=3.2)))
    s.append(bloom(2, 262, 528, stem(262, 528, 268, 392, bend=18, leaves=((.5, -1),), leaf=26, sw=3) + cup_flower(268, 386, 36, sw=3)))
    s.append(bloom(3, 86, 524, stem(86, 524, 80, 430, bend=10, leaves=((.55, 1),), leaf=20, sw=2.6) + petal_flower(80, 428, 30, n=10, rot=18, sw=2.6)))
    s.append(bloom(4, 336, 536, stem(336, 536, 342, 466, bend=-8, leaves=(), sw=2.4) + petal_flower(342, 464, 20, n=9, sw=2.4)))
    s.append(grass(206, 540, 40, 6, sw=2.4) + grass(30, 548, 30, 5, sw=2.4) + grass(380, 548, 30, 5, sw=2.4) + grass(560, 540, 26, 4, sw=2.4))
    # the trail from the daisy to the comb, with pollen in the air
    s.append(f'<path class="trail" d="M178,296 C200,212 250,176 300,170 S346,172 352,196" fill="none" stroke="{FOREST}" '
             f'stroke-width="3" stroke-dasharray=".1 11" stroke-linecap="round" opacity=".8"/>')
    s.append(sparkles([(206, 240), (232, 206), (268, 186), (192, 268)], 3))
    # a second bee, further back, already at the comb
    s.append(f'<g class="hero-bee-back">{bee_g(566, 318, .3, 14, prop="pollen", flip=True)}</g>')
    return svg_el(f"0 0 {W} {H}", "".join(s), "hero-svg")


# ---------- the market: many hives, one is chosen ----------
COMPETE_GOLD = (742, 108, 3)
COMPETE_HIVES = [(80, 64, 1), (196, 78, 2), (318, 66, 1), (440, 84, 2), (580, 72, 1), COMPETE_GOLD, (900, 80, 2), (1020, 66, 1), (1132, 78, 2)]


def compete():
    W, H, g = 1200, 420, 372
    s = [hill(f"M0,{H} V342 C200,322 420,330 600,340 C800,350 1000,326 {W},334 V{H} Z", "url(#g-hill-a)"),
         hill(f"M0,{H} V386 C240,370 480,378 700,390 C900,400 1060,384 {W},388 V{H} Z", "url(#g-hill-b)")]
    gx, gw, gb = COMPETE_GOLD
    s.append(f'<g class="lit">{glow(gx + 10, g - 150, 230)}</g>')
    for i, (x, w, boxes) in enumerate(COMPETE_HIVES):
        s.append(f'<g class="rise" style="--i:{i}">{shadow(x + w * .15, g + 2, w * .8, w * .09)}{box_hive(x, g, w, boxes, sw=2.6)}</g>')
    # the chosen hive: drawn again in gold over its muted twin, with flowers growing round it
    s.append(f'<g class="lit">{trail("M20,96 C200,40 430,60 560,150 S716,300 728,334", sw=2.6, gap=12)}'
             f'{trail("M1180,90 C1040,44 900,96 830,176 S760,300 756,334", sw=2.6, gap=12)}</g>')
    s.append(f'<g class="lit">{box_hive(gx, g, gw, gb, gold=True, sw=3)}</g>')
    for i, (x, r, kind) in enumerate([(660, 20, "d"), (688, 15, "c"), (812, 18, "d"), (842, 13, "d"), (628, 12, "d")]):
        head = petal_flower(x, g - 8 - r * 1.6, r, n=10, sw=2) if kind == "d" else cup_flower(x, g - 8 - r * 1.6, r, sw=2)
        s.append(f'<g class="lit">{bloom(i, x, g + 6, stem(x, g + 8, x, g - 8 - r * 1.6, bend=4, leaves=((.45, 1),), leaf=r * .8, sw=2) + head)}</g>')
    # buyers and consumers converge on it (their trails are drawn behind the hive, above)
    for i, (x, y, sc, a, flip) in enumerate([(286, 62, .3, -6, False), (548, 140, .32, 18, False), (1010, 70, .3, -6, True), (846, 160, .32, 18, True)]):
        s.append(f'<g class="fly-in" style="--i:{i}">{bee_g(x, y, sc, a, prop="pollen", flip=flip)}</g>')
    return svg_el(f"0 0 {W} {H}", "".join(s), "compete-svg")


# ---------- compliance only vs. contributing ----------
def value_a():
    """Compliant only: the report is filed, the hive stays as it was."""
    W, H, g = 520, 380, 320
    s = [hill(f"M0,{H} V318 C160,306 360,312 {W},318 V{H} Z", "#E7E7DD"),
         shadow(272, g + 2, 84, 10), box_hive(260, g, 110, 2, sw=3)]
    # a clipboard with a tick, leaning on the hive
    s.append(f'<g transform="rotate(-8 132 270)" stroke="{MUTE_DARK}" stroke-width="3" stroke-linejoin="round">'
             f'<rect x="104" y="226" width="60" height="78" rx="6" fill="{MUTE_TOP}"/>'
             f'<rect x="120" y="218" width="28" height="14" rx="4" fill="{MUTE_SIDE}"/>'
             f'<path d="M116,252 H150 M116,266 H150 M116,280 H140" stroke-width="3" stroke-linecap="round"/>'
             f'<path d="M134,288 L142,296 L158,276" fill="none" stroke-width="4" stroke-linecap="round"/></g>')
    return svg_el(f"0 0 {W} {H}", "".join(s), "value-svg value-a")


def value_b():
    """Compliant and contributing: environment and society feed the hive."""
    W, H, g = 520, 380, 320
    s = [glow(268, 190, 200),
         hill(f"M0,{H} V312 C160,298 360,304 {W},312 V{H} Z", "url(#g-hill-b)"),
         shadow(272, g + 2, 84, 10)]
    s.append(trail("M70,190 C120,110 200,96 236,150 S250,262 254,286", sw=2.4, gap=11))
    s.append(trail("M450,190 C400,110 320,96 290,150 S276,262 270,286", sw=2.4, gap=11))
    s.append(box_hive(260, g, 110, 3, gold=True, sw=3))
    # environment on the left, society on the right
    for i, (x, h, r) in enumerate([(54, 140, 26), (100, 110, 20), (24, 96, 16)]):
        s.append(bloom(i, x, H - 30, stem(x, H - 22, x - 2, H - 30 - h, bend=8, leaves=((.45, 1),), leaf=r * .8, sw=2.4) + petal_flower(x - 2, H - 32 - h, r, n=11, sw=2.4)))
    for i, (x, h, r) in enumerate([(466, 140, 24), (420, 108, 19), (500, 92, 15)]):
        s.append(bloom(i + 3, x, H - 30, stem(x, H - 22, x + 2, H - 30 - h, bend=-8, leaves=((.45, -1),), leaf=r * .8, sw=2.4) + cup_flower(x + 2, H - 30 - h, r, sw=2.4)))
    s.append(f'<g class="fly-in" style="--i:0">{bee_g(170, 104, .3, -10, prop="pollen")}</g>')
    s.append(f'<g class="fly-in" style="--i:1">{bee_g(352, 104, .3, -10, prop="pollen", flip=True)}</g>')
    return svg_el(f"0 0 {W} {H}", "".join(s), "value-svg value-b")


# ---------- bees used as standalone pictures ----------
def bee_svg(inner, cls="bee-svg"):
    return f'<svg class="{cls}" viewBox="0 0 200 200" aria-hidden="true" focusable="false">{inner}</svg>'


CREW = {"inspector": dict(prop="medal", hat="peaked", angle=-16),
        "engineer": dict(prop="cog", hat="backwards", angle=-20),
        "storyteller": dict(prop="report", hat="beret", angle=-14)}


def crew(name):
    c = CREW[name]
    return lambda: bee_svg(fly(bee(prop=c["prop"], hat=c["hat"]), angle=c["angle"]))


def guide():
    return bee_svg(fly(bee(prop="goggles", halo=IVORY)))


def swarm():
    """Contact: the crew flanks the Messenger, who looks straight at the visitor."""
    side = [("s1", "inspector"), ("s2", "engineer")], [("s3", "storyteller"), ("s4", None)]
    def one(cls, name):
        inner = fly(bee(prop="goggles", halo=IVORY)) if name is None else fly(bee(prop=CREW[name]["prop"], hat=CREW[name]["hat"], halo=IVORY), angle=CREW[name]["angle"])
        return f'<div class="swarm-bee {cls}">{bee_svg(inner)}</div>'
    return ('<div class="swarm" aria-hidden="true">' + "".join(one(c, n) for c, n in side[0])
            + f'<div class="swarm-messenger">{bee_svg(front_bee(halo=IVORY), "bee-svg messenger-svg")}</div>'
            + "".join(one(c, n) for c, n in side[1]) + '</div>')


def letter():
    return bee_svg(fly(bee(prop="letter", halo=IVORY), angle=-14))


def messenger():
    return bee_svg(front_bee(), "bee-svg messenger-svg")


def scout():
    """Resources: the Scout with its lens over an open guide."""
    W, H = 340, 280
    s = [glow(170, 150, 150),
         shadow(170, 252, 120, 12),
         f'<g stroke="{INK}" stroke-width="3" stroke-linejoin="round">'
         f'<path d="M170,246 C140,232 96,228 52,236 L56,150 C100,142 142,146 170,162 Z" fill="{PETAL_1}"/>'
         f'<path d="M170,246 C200,232 244,228 288,236 L284,150 C240,142 198,146 170,162 Z" fill="{PETAL_2}"/>'
         f'<path d="M170,162 V246" fill="none"/>'
         f'<path d="M76,170 C100,166 126,168 150,176 M76,188 C100,184 126,186 150,194 M76,206 C96,203 116,204 134,208" fill="none" stroke="{MUTE_LINE}" stroke-width="3" stroke-linecap="round"/>'
         f'</g>',
         honey_cell(222, 196, 26, "honey", sw=2.6),
         f'<g class="bee-svg">{bee_g(176, 82, .62, -14, prop="lens", flip=False, cls="scout-bee")}</g>']
    return svg_el(f"0 0 {W} {H}", "".join(s), "scout-svg")


PIECES = {"defs": shared_defs, "hero": hero, "compete": compete, "value-a": value_a, "value-b": value_b,
          "crew-inspector": crew("inspector"), "crew-engineer": crew("engineer"), "crew-storyteller": crew("storyteller"),
          "guide": guide, "swarm": swarm, "letter": letter, "messenger": messenger, "scout": scout}
