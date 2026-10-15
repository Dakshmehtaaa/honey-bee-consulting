"""Draws the website illustrations. scripts/build-pages.py writes them into the pages.

Each entry in PIECES returns one SVG (or a small block of markup). Class names inside the art
(.bloom, .cell, .rise, .lit, .fly-in…) are the hooks story.css animates. Gradients live once per
page in the "defs" piece, so the pictures can share them."""
import math, os, re, sys
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


# ---------- hero: a comb hanging from a branch that grows in from the right edge ----------
def hero():
    """The comb on its branch. The art is anchored to the right edge of the screen, so the branch
    runs off the right of the canvas; the meadow under it is a separate full-width strip (hero_land)."""
    W, H = 760, 700
    s = [f'<circle cx="470" cy="300" r="250" fill="#FBF1D3"/>', glow(470, 300, 330)]
    s.append(branch("M792,58 C700,62 600,86 500,100 S330,108 236,136",
                    sw=3.4, leaves=((300, 124, -150, 50), (372, 108, -28, 44), (640, 70, -150, 46), (712, 62, -24, 42), (540, 92, 18, 36))))
    s.append(f'<path d="M398,118 C430,96 540,92 566,114 L552,130 H412 Z" fill="url(#g-wax)" stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/>')
    cells = [(0, 0, "capped"), (1, 0, "honey"), (-1, 1, "honey"), (0, 1, "honey"), (1, 1, "capped"),
             (-1, 2, "honey"), (0, 2, "empty"), (1, 2, "honey"), (0, 3, "honey"), (-1, 3, "capped"), (1, 3, "honey")]
    s.append(f'<g class="hero-comb">{comb(442, 168, 50, cells, sw=3.6)}</g>')
    s.append(drip(486, 445, 60, w=11))
    s.append(drip(398, 432, 40, w=8))
    # big flowers rising out of the meadow strip (their stems run under it)
    s.append(bloom(0, 150, 700, stem(152, 720, 146, 418, bend=-20, leaves=((.36, 1), (.58, -1)), leaf=34, sw=3.2) + petal_flower(146, 416, 62, n=12, rot=6, sw=3.4)))
    s.append(bloom(1, 60, 700, stem(60, 720, 56, 500, bend=16, leaves=((.45, 1),), leaf=26, sw=2.8) + petal_flower(56, 498, 36, n=11, rot=12, sw=2.8)))
    s.append(bloom(2, 286, 700, stem(286, 720, 292, 520, bend=18, leaves=((.5, -1),), leaf=28, sw=3) + cup_flower(292, 512, 40, sw=3)))
    s.append(bloom(3, 620, 700, stem(620, 720, 626, 560, bend=-12, leaves=((.5, 1),), leaf=24, sw=2.8) + cup_flower(626, 554, 30, fill="#E39A62", sw=2.8)))
    s.append(bloom(4, 716, 700, stem(716, 720, 710, 520, bend=10, leaves=((.4, -1),), leaf=26, sw=2.8) + petal_flower(710, 518, 40, n=11, rot=20, sw=2.8)))
    s.append(f'<path class="trail" d="M184,390 C206,300 262,256 318,248 S386,252 392,276" fill="none" stroke="{FOREST}" '
             f'stroke-width="3" stroke-dasharray=".1 11" stroke-linecap="round" opacity=".8"/>')
    s.append(sparkles([(214, 328), (244, 290), (286, 266), (196, 360), (604, 220)], 3.2))
    s.append(f'<g class="hero-bee-back">{bee_g(640, 330, .34, 14, prop="pollen", flip=True)}</g>')
    return svg_el(f"0 0 {W} {H}", "".join(s), "hero-svg")


def hero_land():
    """The meadow under the hero, edge to edge. preserveAspectRatio slices from the middle, so the
    centre of the 2400-wide strip is what a phone sees."""
    W, H = 2400, 200
    s = [hill(f"M0,{H} V92 C300,60 620,70 900,96 C1180,120 1480,74 1800,82 C2060,88 2240,70 {W},78 V{H} Z", "url(#g-hill-a)"),
         hill(f"M0,{H} V128 C260,108 560,118 820,134 C1100,150 1400,118 1700,126 C1980,134 2200,116 {W},122 V{H} Z", "url(#g-hill-b)"),
         hill(f"M0,{H} V160 C320,148 640,156 960,166 C1260,174 1560,152 1900,160 C2120,166 2280,156 {W},158 V{H} Z", "url(#g-hill-c)")]
    for x in range(40, W, 130):
        s.append(grass(x + (x * 37) % 50, 168 - (x * 13) % 18, 22 + (x * 7) % 14, 5, sw=2.4))
    small = [(120, 0), (340, 1), (610, 0), (760, 1), (1010, 0), (1180, 1), (1370, 0), (1560, 1), (1760, 0), (1990, 1), (2210, 0)]
    for i, (x, kind) in enumerate(small):
        y = 150 - (x * 11) % 22
        h = 34 + (x * 7) % 26
        head = petal_flower(x, y - h, 12 + (x % 5), n=9, rot=x % 30, sw=2) if kind == 0 else cup_flower(x, y - h + 4, 11, fill="#E39A62", sw=2)
        s.append(bloom(i + 5, x, y, stem(x, y + 4, x + 2, y - h, bend=5, leaves=((.5, 1),), leaf=10, sw=2) + head))
    return (f'<svg class="hero-land-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">'
            + "".join(s) + '</svg>')


def goggles_ground():
    """The Guide's goggles lying in the grass, waiting to be picked up."""
    return (f'<svg class="goggles-svg" viewBox="0 0 80 44" aria-hidden="true" focusable="false"><g stroke="{INK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M14,26 C4,30 4,40 18,40 C34,40 48,38 62,34" fill="none" stroke="{POLLEN}" stroke-width="4.5"/>'
            f'<rect x="16" y="10" width="26" height="18" rx="8" fill="#BFE0D8" transform="rotate(-8 29 19)"/>'
            f'<rect x="44" y="8" width="26" height="18" rx="8" fill="#BFE0D8" transform="rotate(-8 57 17)"/>'
            f'<path d="M41,17 L45,16" fill="none"/>'
            f'<path d="M22,15 L32,13 M50,13 L60,11" stroke="{IVORY}" stroke-width="2.6"/></g></svg>')


# ---------- the market: many competitors, clients pick the best ESG ----------
COMPETE_GOLD = (742, 108, 3)
COMPETE_HIVES = [(80, 64, 1), (196, 78, 2), (318, 66, 1), (440, 84, 2), (580, 72, 1), COMPETE_GOLD, (900, 80, 2), (1020, 66, 1), (1132, 78, 2)]
GRADES = ["C", "D", "C", "B", "D", "A", "C", "D", "B"]


def grade(cx, cy, letter, gold=False):
    """An ESG rating badge. Gold for the leader; letters outlined so no font is needed."""
    r = 20 if gold else 15
    fill, line, ink = (POLLEN, INK, INK) if gold else ("#FFFFFA", MUTE_LINE, MUTE_DARK)
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{line}" stroke-width="{3 if gold else 2.4}"/>'
    s += words(letter, "font-3.ttf", 24 if gold else 17, cx, cy + (8.5 if gold else 6), ink, anchor="middle")
    if gold:
        s += f'<path d="M{cx+14},{cy-22} l3,7 7,1 -5,5 1,7 -6,-3 -6,3 1,-7 -5,-5 7,-1 Z" fill="#FFFFFA" stroke="{INK}" stroke-width="2"/>'
    return s


def compete():
    W, H, g = 1200, 420, 372
    s = [hill(f"M0,{H} V342 C200,322 420,330 600,340 C800,350 1000,326 {W},334 V{H} Z", "url(#g-hill-a)"),
         hill(f"M0,{H} V386 C240,370 480,378 700,390 C900,400 1060,384 {W},388 V{H} Z", "url(#g-hill-b)")]
    gx, gw, gb = COMPETE_GOLD
    s.append(f'<g class="lit">{glow(gx + 10, g - 150, 230)}</g>')
    tops = {}
    for i, (x, w, boxes) in enumerate(COMPETE_HIVES):
        top = g - w * (.16 + .07 + .42 * boxes + .17) - w * .16 - 14
        tops[i] = top
        badge = grade(x + w * .12, top - 4, GRADES[i]) if (x, w, boxes) != COMPETE_GOLD else ""
        s.append(f'<g class="rise" style="--i:{i}">{shadow(x + w * .15, g + 2, w * .8, w * .09)}{box_hive(x, g, w, boxes, sw=2.6)}{badge}</g>')
    s.append(f'<g class="lit">{trail("M20,96 C200,40 430,60 560,150 S716,300 728,334", sw=2.6, gap=12)}'
             f'{trail("M1180,90 C1040,44 900,96 830,176 S760,300 756,334", sw=2.6, gap=12)}</g>')
    s.append(f'<g class="lit">{box_hive(gx, g, gw, gb, gold=True, sw=3)}{grade(gx + gw * .12, tops[5] - 8, "A", gold=True)}</g>')
    for i, (x, r, kind) in enumerate([(660, 20, "d"), (688, 15, "c"), (812, 18, "d"), (842, 13, "d"), (628, 12, "d")]):
        head = petal_flower(x, g - 8 - r * 1.6, r, n=10, sw=2) if kind == "d" else cup_flower(x, g - 8 - r * 1.6, r, sw=2)
        s.append(f'<g class="lit">{bloom(i, x, g + 6, stem(x, g + 8, x, g - 8 - r * 1.6, bend=4, leaves=((.45, 1),), leaf=r * .8, sw=2) + head)}</g>')
    for i, (x, y, sc, a, flip) in enumerate([(286, 62, .3, -6, False), (548, 140, .32, 18, False), (1010, 70, .3, -6, True), (846, 160, .32, 18, True)]):
        s.append(f'<g class="fly-in" style="--i:{i}">{bee_g(x, y, sc, a, prop="pollen", flip=flip)}</g>')
    return svg_el(f"0 0 {W} {H}", "".join(s), "compete-svg")


# ---------- the ESG loop: act on both pillars, prove it, win clients ----------
LOOP_STAGES = ["env", "soc", "prove", "win"]
LOOP_ICONS = {
    "env": '<path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14z"/><path d="M5 19l8-8"/>',
    "soc": '<circle cx="9" cy="8" r="3"/><circle cx="16.5" cy="9.5" r="2.5"/><path d="M3.5 19c.5-3.5 2.8-5.5 5.5-5.5s5 2 5.5 5.5M14.5 14c2.8-.4 5 1.4 5.5 4.5"/>',
    "prove": '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "win": '<path d="M12 3l7.8 4.5v9L12 21l-7.8-4.5v-9z"/><path d="M8.5 12.5l2.4 2.4 4.6-5"/>',
}


def loop_ring():
    """The ring, its flowing dots, four chevrons, and a bee that flies round to the active stage."""
    c, r = 260, 190
    chev = "".join(f'<path class="loop-chev" d="M-5-7 3 0-5 7" transform="translate({c + r * math.cos(math.radians(a - 90)):.1f} {c + r * math.sin(math.radians(a - 90)):.1f}) rotate({a})"/>' for a in (45, 135, 225, 315))
    # the bee rests just behind the active stage, with a honey trail behind it, so the node never hides it
    lag = math.radians(-27)
    bx, by = c + r * math.sin(lag), c - r * math.cos(lag)
    t0 = math.radians(-82)
    tail = (f'<path class="loop-tail" d="M{c + r * math.sin(t0):.1f} {c - r * math.cos(t0):.1f}A{r} {r} 0 0 1 {bx:.1f} {by:.1f}"/>')
    bee = tail + f'<g class="loop-bee-fly">{bee_g(bx, by - 4, .24, -27, prop="pollen")}</g>'
    return (f'<svg class="loop-art" viewBox="0 0 520 520" aria-hidden="true" focusable="false">'
            f'<circle class="loop-halo" cx="{c}" cy="{c}" r="238"/><circle class="loop-halo loop-halo-2" cx="{c}" cy="{c}" r="150"/>'
            f'<circle class="loop-track" cx="{c}" cy="{c}" r="{r}"/>'
            f'<path class="loop-flow" pathLength="100" d="M{c} {c - r}a{r} {r} 0 1 1 0 {2 * r}a{r} {r} 0 1 1 0-{2 * r}"/>{chev}'
            f'<circle class="loop-core" cx="{c}" cy="{c}" r="124"/>'
            f'<g class="loop-comet">{bee}</g></svg>')


# ---------- bees used as standalone pictures ----------
def bee_svg(inner, cls="bee-svg"):
    return f'<svg class="{cls}" viewBox="0 0 200 200" aria-hidden="true" focusable="false">{inner}</svg>'


CREW = {"inspector": dict(prop="medal", hat="peaked", angle=-16),
        "engineer": dict(prop="cog", hat="backwards", angle=-20),
        "storyteller": dict(prop="report", hat="beret", angle=-14),
        "gardener": dict(prop="sprout", hat="sunhat", angle=-16)}


def crew(name):
    c = CREW[name]
    return lambda: bee_svg(fly(bee(prop=c["prop"], hat=c["hat"]), angle=c["angle"]))


def guide():
    """The Guide. Its goggles are a group of their own: it picks them up when the visitor scrolls."""
    from bees import PROPS
    inner = fly(bee(prop="goggles", halo=IVORY))
    g = PROPS["goggles"][1]
    return bee_svg(inner.replace(g, f'<g class="goggles">{g}</g>', 1))


def swarm():
    """Contact: the crew flanks the Messenger, who looks straight at the visitor."""
    side = [("s1", "inspector"), ("s2", "engineer")], [("s3", "storyteller"), ("s4", "gardener")]
    def one(cls, name):
        inner = fly(bee(prop=CREW[name]["prop"], hat=CREW[name]["hat"], halo=IVORY), angle=CREW[name]["angle"])
        return f'<div class="swarm-bee {cls}">{bee_svg(inner)}</div>'
    return ('<div class="swarm">' + "".join(one(c, n) for c, n in side[0])
            + f'<div class="swarm-messenger">{bee_svg(front_bee(halo=IVORY), "bee-svg messenger-svg")}</div>'
            + "".join(one(c, n) for c, n in side[1]) + '</div>')


def letter():
    """Newsletter: an envelope sealed with a honey hex, a sprig tucked under the flap."""
    W, H = 220, 170
    s = [glow(110, 92, 92),
         f'<g stroke="{INK}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" transform="rotate(-8 110 92)">'
         f'<path d="M30,52 L190,52 L190,148 L30,148 Z" fill="#FFFFFA"/>'
         f'<path d="M30,148 L94,98 M190,148 L126,98" fill="none" stroke="{MUTE_LINE}" stroke-width="3"/>'
         f'<path d="M30,52 L110,112 L190,52" fill="#F3F0E2"/>'
         f'<path d="M52,40 C60,24 76,20 88,30 C78,34 66,38 56,48" fill="url(#g-leaf)" stroke-width="3"/>'
         f'<path d="M48,50 C56,40 68,34 82,32" fill="none" stroke="{LEAF_D}" stroke-width="3"/>'
         f'<path d="{hex_path(110, 110, 18)}" fill="url(#g-honey)"/>'
         f'<path d="M104,110 L108,114 L117,104" fill="none" stroke-width="3.4"/></g>',
         sparkles([(196, 40), (206, 64), (184, 26)], 3)]
    return svg_el(f"0 0 {W} {H}", "".join(s), "letter-svg")


def messenger():
    return bee_svg(front_bee(), "bee-svg messenger-svg")


def scout():
    """Resources: the Scout holds its lens over an open field guide."""
    W, H = 360, 300
    s = [glow(180, 150, 160), shadow(180, 270, 140, 13),
         f'<g stroke="{INK}" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round">'
         # hard cover peeking out under the pages
         f'<path d="M180,266 C146,252 96,248 40,256 L36,158 C94,150 146,154 180,170 C214,154 266,150 324,158 L320,256 C264,248 214,252 180,266 Z" fill="{FOREST}"/>'
         # page block edges
         f'<path d="M180,258 C146,244 98,240 48,248 L46,154 C98,146 146,150 180,166 Z" fill="#F4F1E3"/>'
         f'<path d="M180,258 C214,244 262,240 312,248 L314,154 C262,146 214,150 180,166 Z" fill="#F4F1E3"/>'
         f'<path d="M180,252 C148,238 102,234 56,242 L54,148 C102,140 148,144 180,160 Z" fill="#FFFFFA"/>'
         f'<path d="M180,252 C212,238 258,234 304,242 L306,148 C258,140 212,144 180,160 Z" fill="#FBF8EC"/>'
         f'<path d="M180,160 V252" fill="none"/>'
         # left page: a small bar chart and a few lines
         f'<path d="M76,212 V198 M94,212 V188 M112,212 V178 M130,212 V170" fill="none" stroke-width="8" stroke="{LEAF}"/>'
         f'<path d="M130,212 V170" fill="none" stroke-width="8" stroke="{POLLEN}"/>'
         f'<path d="M70,214 H150" fill="none" stroke-width="2.6"/>'
         f'<path d="M72,168 C88,165 104,165 120,167" fill="none" stroke="{MUTE_LINE}" stroke-width="3"/>'
         f'<path d="M72,230 C96,226 126,227 156,233" fill="none" stroke="{MUTE_LINE}" stroke-width="3"/>'
         # right page: a checklist
         f'<path d="M206,180 l6,6 10,-12 M206,206 l6,6 10,-12" fill="none" stroke="{FOREST}" stroke-width="3.6"/>'
         f'<rect x="204" y="226" width="16" height="14" rx="3" fill="none" stroke="{MUTE_LINE}" stroke-width="3"/>'
         f'<path d="M232,180 C252,177 270,177 288,179 M232,206 C252,203 270,203 288,205 M232,232 C248,229 262,229 276,231" fill="none" stroke="{MUTE_LINE}" stroke-width="3"/>'
         # ribbon bookmark
         f'<path d="M262,146 L262,190 L270,182 L278,190 L278,145" fill="{CLAY}" stroke-width="2.6"/>'
         f'</g>',
         sparkles([(70, 120), (300, 110), (318, 132)], 3),
         f'<g class="scout-bee">{bee_g(150, 70, .62, -6, prop="lens_held")}</g>']
    return svg_el(f"0 0 {W} {H}", "".join(s), "scout-svg")


PIECES = {"defs": shared_defs, "hero": hero, "hero-land": hero_land, "goggles": goggles_ground, "compete": compete, "loop": loop_ring,
          "crew-inspector": crew("inspector"), "crew-engineer": crew("engineer"), "crew-storyteller": crew("storyteller"), "crew-gardener": crew("gardener"),
          "guide": guide, "swarm": swarm, "letter": letter, "messenger": messenger, "scout": scout}
