"""Scene pieces for the honeybees illustrations: meadow, box hives, flowers, flight trails.

The bees themselves come from bees.py. Everything here returns SVG fragments; ids are unique per
call so several pieces can share one document. Style: ink outlines on the pieces that matter,
soft gradients for depth, muted outlines for everything in the background.
Usage from another script: `from art import *` with scripts/brand on sys.path."""
import math
from bees import bee, front_bee, fly, uid, text_path, IVORY, POLLEN, INK, FOREST, WING, CLAY

HONEY_L, HONEY_D, AMBER = "#F6D77C", "#C99418", "#A8700F"
SAGE_0, SAGE_1, SAGE_2, GRASS, LEAF, LEAF_D = "#EEF1E4", "#E2E9D4", "#CFDDBD", "#A8C58A", "#7FA563", "#4F7A45"
MUTE, MUTE_SIDE, MUTE_TOP, MUTE_LINE, MUTE_DARK = "#EAE9DF", "#D9D9CC", "#F4F3EA", "#A7AD9D", "#8E9585"
PETAL_1, PETAL_2 = "#FFFFFA", "#E9EDDC"


def defs():
    """Shared gradients. Include once per document."""
    return f'''<defs>
<linearGradient id="g-petal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PETAL_1}"/><stop offset="1" stop-color="{PETAL_2}"/></linearGradient>
<radialGradient id="g-pollen" cx=".38" cy=".34" r=".75"><stop offset="0" stop-color="{HONEY_L}"/><stop offset=".7" stop-color="{POLLEN}"/><stop offset="1" stop-color="{HONEY_D}"/></radialGradient>
<linearGradient id="g-leaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GRASS}"/><stop offset="1" stop-color="{LEAF_D}"/></linearGradient>
<linearGradient id="g-front" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3CB55"/><stop offset="1" stop-color="{POLLEN}"/></linearGradient>
<linearGradient id="g-side" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9A429"/><stop offset="1" stop-color="{HONEY_D}"/></linearGradient>
<linearGradient id="g-mute" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0EFE6"/><stop offset="1" stop-color="{MUTE}"/></linearGradient>
<radialGradient id="g-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{POLLEN}" stop-opacity=".55"/><stop offset=".55" stop-color="{POLLEN}" stop-opacity=".18"/><stop offset="1" stop-color="{POLLEN}" stop-opacity="0"/></radialGradient>
<radialGradient id="g-shadow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{INK}" stop-opacity=".22"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient>
<linearGradient id="g-hill-a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SAGE_1}"/><stop offset="1" stop-color="{SAGE_0}"/></linearGradient>
<linearGradient id="g-hill-b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SAGE_2}"/><stop offset="1" stop-color="{SAGE_1}"/></linearGradient>
<linearGradient id="g-hill-c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GRASS}"/><stop offset="1" stop-color="#BCD3A2"/></linearGradient>
</defs>'''


def shadow(cx, cy, rx, ry):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#g-shadow)"/>'


def glow(cx, cy, r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g-glow)"/>'


def box_hive(cx, ground, w, boxes=2, gold=False, sw=2.4, door=True):
    """A Langstroth hive in oblique view: stand, landing board, stacked boxes, telescoping lid.
    cx is the centre of the front face, ground the y the legs stand on. Muted unless gold."""
    dx, dy = w * 0.24, w * 0.16                       # depth of the oblique side
    bh, lid, stand, board = w * 0.42, w * 0.17, w * 0.16, w * 0.07
    x0, x1 = cx - w / 2, cx + w / 2
    line = INK if gold else MUTE_LINE
    front, side, top = ("url(#g-front)", "url(#g-side)", HONEY_L) if gold else ("url(#g-mute)", MUTE_SIDE, MUTE_TOP)
    slot = INK if gold else MUTE_DARK
    s = [f'<g stroke="{line}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">']
    # stand: two legs under the front, one at the back
    y = ground - stand
    s.append(f'<path d="M{x0+w*.12},{ground} V{y} M{x1-w*.12},{ground} V{y} M{x1+dx-w*.1},{ground-dy*.55} V{y-dy*.6}" fill="none"/>')
    # bottom board with a landing ramp in front
    s.append(f'<path d="M{x0-w*.04},{y} H{x1+w*.04} L{x1+w*.04+dx},{y-dy} V{y-dy-board} L{x1+w*.04},{y-board} Z" fill="{side}"/>')
    s.append(f'<path d="M{x0-w*.04},{y} H{x1+w*.04} V{y-board} H{x0-w*.04} Z" fill="{front}"/>')
    s.append(f'<path d="M{cx-w*.22},{y} L{cx-w*.3},{y+w*.08} H{cx+w*.3} L{cx+w*.22},{y} Z" fill="{side}"/>')
    y -= board
    # boxes, bottom up
    for i in range(boxes):
        yt = y - bh
        s.append(f'<path d="M{x1},{y} L{x1+dx},{y-dy} V{yt-dy} L{x1},{yt} Z" fill="{side}"/>')
        s.append(f'<rect x="{x0}" y="{yt}" width="{w}" height="{bh}" fill="{front}"/>')
        s.append(f'<rect x="{cx-w*.13}" y="{yt+bh*.26}" width="{w*.26}" height="{bh*.13}" rx="{bh*.065}" fill="{slot}" stroke="none" opacity="{.9 if gold else .55}"/>')
        if i == 0 and door:
            s.append(f'<rect x="{cx-w*.24}" y="{y-bh*.12}" width="{w*.48}" height="{bh*.12}" fill="{slot}" stroke="none"/>')
        y = yt
    # lid: overhangs a little, with a lit top face
    lx0, lx1 = x0 - w * .06, x1 + w * .06
    yt = y - lid
    s.append(f'<path d="M{lx1},{y} L{lx1+dx},{y-dy} V{yt-dy} L{lx1},{yt} Z" fill="{side}"/>')
    s.append(f'<rect x="{lx0}" y="{yt}" width="{lx1-lx0}" height="{lid}" fill="{front}"/>')
    s.append(f'<path d="M{lx0},{yt} L{lx0+dx},{yt-dy} H{lx1+dx} L{lx1},{yt} Z" fill="{top}"/>')
    if gold:   # a honey drip from the lid edge and a highlight along the top
        hx = lx0 + (lx1 - lx0) * .28
        s.append(f'<path d="M{hx-w*.08},{y} C{hx-w*.08},{y+bh*.18} {hx-w*.03},{y+bh*.3} {hx},{y+bh*.3} '
                 f'C{hx+w*.04},{y+bh*.3} {hx+w*.04},{y+bh*.14} {hx+w*.08},{y} Z" fill="{POLLEN}" stroke-width="{sw*.8}"/>')
        s.append(f'<path d="M{lx0+w*.06},{yt+lid*.32} H{lx1-w*.2}" stroke="#FFF3C4" stroke-width="{sw}" opacity=".8"/>')
    s.append('</g>')
    return "".join(s)


def skep(cx, top, halves, rh, gold=False, sw=2.4, door=None, step=None, cls=""):
    """A straw skep: stacked rounded rings. halves are the half-widths from the top ring down, so
    the same drawing hangs from a branch (narrow top and bottom) or stands as a dome (wide bottom).
    Rings are drawn top first so each lower ring overlaps the one above. door = (x, y, rx, ry)."""
    step = step or rh * .9
    line = INK if gold else MUTE_LINE
    fill = "url(#g-front)" if gold else "url(#g-mute)"
    hi = "#FFF3C4" if gold else "#FFFFFA"
    s = [f'<g stroke="{line}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">']
    for i, a in enumerate(halves):
        y = top + i * step
        g = f' class="{cls}" style="--i:{i}"' if cls else ""
        s.append(f'<g{g}><rect x="{cx-a:.1f}" y="{y:.1f}" width="{2*a:.1f}" height="{rh:.1f}" rx="{rh/2:.1f}" fill="{fill}"/>'
                 f'<path d="M{cx-a*.62:.1f},{y+rh*.32:.1f} Q{cx-a*.4:.1f},{y+rh*.18:.1f} {cx-a*.12:.1f},{y+rh*.24:.1f}" fill="none" stroke="{hi}" stroke-width="{sw*1.1:.1f}" opacity=".9"/></g>')
    if door:
        x, y, rx, ry = door
        if gold:
            s.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx*1.22:.1f}" ry="{ry*1.2:.1f}" fill="{AMBER}"/>')
        s.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{INK if gold else MUTE_DARK}"/>')
    s.append('</g>')
    return "".join(s)


def petal_flower(cx, cy, r, n=11, rot=0, sw=1.8, centre=True, line=INK):
    """A daisy head seen slightly from above: long soft petals, a domed pollen centre."""
    s = [f'<g stroke="{line}" stroke-width="{sw}" stroke-linejoin="round">']
    for k in range(n):
        a = rot + 360 * k / n
        s.append(f'<path d="M{cx},{cy} C{cx-r*.34},{cy-r*.32} {cx-r*.3},{cy-r*.98} {cx},{cy-r} '
                 f'C{cx+r*.3},{cy-r*.98} {cx+r*.34},{cy-r*.32} {cx},{cy} Z" fill="url(#g-petal)" '
                 f'transform="translate({cx} {cy}) scale(1 .78) rotate({a:.1f}) translate({-cx} {-cy})"/>')
    if centre:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*.32}" fill="url(#g-pollen)"/>')
        for k in range(7):
            a = k * 2.4
            rr = r * .17 * math.sqrt((k + .5) / 7)
            s.append(f'<circle cx="{cx+rr*math.cos(a):.1f}" cy="{cy+rr*math.sin(a):.1f}" r="{r*.035:.2f}" fill="{AMBER}" stroke="none"/>')
    s.append('</g>')
    return "".join(s)


def cup_flower(cx, cy, r, fill=CLAY, sw=1.8):
    """A tulip-like cup: three petals, the middle one in front."""
    l = f'M{cx},{cy+r*.55} C{cx-r*.9},{cy+r*.4} {cx-r*.95},{cy-r*.5} {cx-r*.55},{cy-r*.95} C{cx-r*.35},{cy-r*.45} {cx-r*.05},{cy-r*.2} {cx},{cy+r*.55} Z'
    rt = f'M{cx},{cy+r*.55} C{cx+r*.9},{cy+r*.4} {cx+r*.95},{cy-r*.5} {cx+r*.55},{cy-r*.95} C{cx+r*.35},{cy-r*.45} {cx+r*.05},{cy-r*.2} {cx},{cy+r*.55} Z'
    m = f'M{cx},{cy+r*.6} C{cx-r*.55},{cy+r*.4} {cx-r*.5},{cy-r*.6} {cx},{cy-r*1.05} C{cx+r*.5},{cy-r*.6} {cx+r*.55},{cy+r*.4} {cx},{cy+r*.6} Z'
    return (f'<g stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"><path d="{l}" fill="{fill}" opacity=".85"/>'
            f'<path d="{rt}" fill="{fill}" opacity=".85"/><path d="{m}" fill="{fill}"/>'
            f'<path d="M{cx-r*.18},{cy-r*.5} C{cx-r*.22},{cy-r*.1} {cx-r*.16},{cy+r*.2} {cx-r*.06},{cy+r*.4}" fill="none" stroke="#FFFFFF" stroke-opacity=".45" stroke-width="{sw*1.2}" stroke-linecap="round"/></g>')


def stem(x0, y0, x1, y1, bend=0.0, sw=1.8, leaves=((.45, 1), (.7, -1)), leaf=14):
    """A curved stem from the ground (x0,y0) to the head (x1,y1) with optional leaves."""
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    s = [f'<g stroke="{INK}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
         f'<path d="M{x0},{y0} Q{mx},{my} {x1},{y1}" fill="none" stroke="{LEAF_D}" stroke-width="{sw*1.5}"/>']
    for t, side in leaves:
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
        L = leaf
        s.append(f'<path d="M{px:.1f},{py:.1f} C{px+side*L*.3:.1f},{py-L*.55:.1f} {px+side*L*.9:.1f},{py-L*.7:.1f} {px+side*L*1.25:.1f},{py-L*.55:.1f} '
                 f'C{px+side*L*.95:.1f},{py-L*.05:.1f} {px+side*L*.45:.1f},{py+L*.08:.1f} {px:.1f},{py:.1f} Z" fill="url(#g-leaf)"/>')
        s.append(f'<path d="M{px:.1f},{py:.1f} Q{px+side*L*.6:.1f},{py-L*.35:.1f} {px+side*L*1.1:.1f},{py-L*.52:.1f}" fill="none" stroke="#FFFFFF" stroke-opacity=".4" stroke-width="{sw*.6}"/>')
    s.append('</g>')
    return "".join(s)


def grass(x, y, h, n=5, spread=10, sw=1.4, colour=LEAF):
    """A tuft of blades fanning out of one point."""
    s = []
    for k in range(n):
        t = k / max(1, n - 1) - .5
        tx, th = x + t * spread * 2.2, h * (1 - abs(t) * .7)
        s.append(f'<path d="M{x+t*spread*.4:.1f},{y} Q{x+t*spread:.1f},{y-th*.6:.1f} {tx:.1f},{y-th:.1f}" fill="none"/>')
    return f'<g stroke="{colour}" stroke-width="{sw}" stroke-linecap="round">' + "".join(s) + '</g>'


def trail(d, sw=2, colour=FOREST, gap=9, opacity=.75):
    """A dotted flight path."""
    return f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{sw}" stroke-dasharray=".1 {gap}" stroke-linecap="round" opacity="{opacity}"/>'


def hill(d, fill):
    return f'<path d="{d}" fill="{fill}"/>'


def flying_bee(x, y, s=.3, angle=-18, prop=None, flip=False, sw=6):
    """A brand bee centred near (x, y). s scales the 200-unit bee; flip faces it left."""
    inner = fly(bee(prop=prop, sw=sw), angle=angle)
    t = f"translate({x},{y}) scale({-s if flip else s},{s}) translate(-100,-92)"
    return f'<g transform="{t}">{inner}</g>'


def words(txt, font, size, x, y, fill, tracking=0.0, anchor="start"):
    return f'<path fill="{fill}" d="{text_path(txt, font, size, x, y, tracking, anchor)}"/>'


# ---------- honeycomb ----------
WAX, WAX_D, CAP, CAP_D = "#F5DC8C", "#E2BE5C", "#FBF0CC", "#EBD9A0"


def comb_defs():
    return f'''<defs>
<radialGradient id="g-honey" cx=".42" cy=".38" r=".7"><stop offset="0" stop-color="#FAD46A"/><stop offset=".55" stop-color="{POLLEN}"/><stop offset="1" stop-color="#C98A12"/></radialGradient>
<radialGradient id="g-well" cx=".5" cy=".62" r=".7"><stop offset="0" stop-color="#F3DFA6"/><stop offset="1" stop-color="#D9B55C"/></radialGradient>
<linearGradient id="g-cap" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF8DE"/><stop offset="1" stop-color="{CAP_D}"/></linearGradient>
<linearGradient id="g-wax" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F8E39F"/><stop offset="1" stop-color="{WAX_D}"/></linearGradient>
</defs>'''


def hex_path(cx, cy, r):
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in (-90, -30, 30, 90, 150, 210)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def honey_cell(cx, cy, r, state="honey", sw=3, i=0):
    """One comb cell: a wax wall, then a well that is full of honey, capped with wax, or empty."""
    s = [f'<g class="cell cell-{state}" style="--i:{i}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round">',
         f'<path d="{hex_path(cx, cy, r)}" fill="url(#g-wax)"/>']
    inner = hex_path(cx, cy + r * .03, r * .72)
    if state == "honey":
        s.append(f'<path d="{inner}" fill="url(#g-well)" stroke-width="{sw*.6}"/>')
        s.append(f'<path class="honey-fill" d="{inner}" fill="url(#g-honey)" stroke="none"/>')
        s.append(f'<path d="M{cx-r*.38:.1f},{cy-r*.2:.1f} Q{cx-r*.3:.1f},{cy-r*.42:.1f} {cx-r*.06:.1f},{cy-r*.46:.1f}" fill="none" stroke="#FFFBEA" stroke-width="{sw*1.1}" stroke-linecap="round" opacity=".85"/>')
    elif state == "capped":
        s.append(f'<path d="{inner}" fill="url(#g-cap)" stroke-width="{sw*.6}"/>')
        s.append(f'<path d="M{cx-r*.3:.1f},{cy+r*.1:.1f} Q{cx:.1f},{cy-r*.22:.1f} {cx+r*.3:.1f},{cy+r*.1:.1f}" fill="none" stroke="{CAP_D}" stroke-width="{sw*.8}" stroke-linecap="round"/>')
    else:
        s.append(f'<path d="{inner}" fill="url(#g-well)" stroke-width="{sw*.6}"/>')
        s.append(f'<path d="{hex_path(cx, cy + r * .12, r * .46)}" fill="#D2AB52" stroke="none" opacity=".55"/>')
    s.append('</g>')
    return "".join(s)


def comb(cx, cy, r, cells, sw=3):
    """cells: list of (col, row, state). Pointy-top layout, odd rows shifted right."""
    w, h = math.sqrt(3) * r, 1.5 * r
    out = []
    for i, (c, rw, state) in enumerate(cells):
        x = cx + c * w + (w / 2 if rw % 2 else 0)
        y = cy + rw * h
        out.append(honey_cell(round(x, 1), round(y, 1), r, state, sw, i))
    return "".join(out)


def drip(x, y, length, w=10, sw=2.4):
    """A honey drop hanging from (x, y): a thin neck swelling into a round bead."""
    n, L = w * .38, length
    return (f'<path class="drip" d="M{x-n:.1f},{y} C{x-n:.1f},{y+L*.42:.1f} {x-w:.1f},{y+L*.56:.1f} {x-w:.1f},{y+L-w:.1f} '
            f'A{w},{w} 0 0 0 {x+w:.1f},{y+L-w:.1f} C{x+w:.1f},{y+L*.56:.1f} {x+n:.1f},{y+L*.42:.1f} {x+n:.1f},{y} Z" '
            f'fill="url(#g-honey)" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<circle cx="{x-w*.38:.1f}" cy="{y+L-w*1.2:.1f}" r="{w*.24:.1f}" fill="#FFFBEA" opacity=".85"/>')


def branch(d, sw=3, leaves=()):
    """A twig the comb hangs from, with leaves at (x, y, angle, size)."""
    s = [f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sw*2.6}" stroke-linecap="round"/>',
         f'<path d="{d}" fill="none" stroke="#8A6A45" stroke-width="{sw*1.4}" stroke-linecap="round"/>']
    for x, y, a, L in leaves:
        s.append(f'<g transform="translate({x} {y}) rotate({a})"><path d="M0,0 C{L*.25},{-L*.32} {L*.7},{-L*.36} {L},0 C{L*.7},{L*.36} {L*.25},{L*.32} 0,0 Z" '
                 f'fill="url(#g-leaf)" stroke="{INK}" stroke-width="{sw*.7}" stroke-linejoin="round"/>'
                 f'<path d="M{L*.08},0 L{L*.8},0" stroke="#FFFFFF" stroke-opacity=".45" stroke-width="{sw*.5}" stroke-linecap="round"/></g>')
    return "".join(s)


def mimosa(x, y, h, sw=1.6):
    """A spray of round yellow blossoms on a bending stalk."""
    s = [f'<path d="M{x},{y} C{x+h*.05},{y-h*.5} {x+h*.2},{y-h*.8} {x+h*.32},{y-h}" fill="none" stroke="{LEAF_D}" stroke-width="{sw*1.4}" stroke-linecap="round"/>']
    for k in range(9):
        t = .32 + k * .085
        px = x + h * .32 * t ** 1.6
        py = y - h * t
        side = -1 if k % 2 else 1
        s.append(f'<circle cx="{px + side*h*.06:.1f}" cy="{py:.1f}" r="{h*.045:.1f}" fill="url(#g-pollen)" stroke="{INK}" stroke-width="{sw}"/>')
    return "".join(s)


def sparkles(points, r=2.2):
    return "".join(f'<circle class="spark" style="--i:{i}" cx="{x}" cy="{y}" r="{r}" fill="{POLLEN}"/>' for i, (x, y) in enumerate(points))
