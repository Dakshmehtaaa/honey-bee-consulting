"""Draws the honeybees logo family and bee characters as SVG.

Usage: python3 scripts/brand/bees.py <out-dir>   (needs fontTools; writes every SVG plus review.html)
The site copies: dist/assets/bee-mark.svg = mark-favicon, bee-mark-colour.svg = mark-colour,
honey-bee-logo.svg = lockup-sans. The homepage bees in index.html were pasted from bee()/front_bee()."""
import math, os, sys

IVORY, POLLEN, INK, FOREST, WING = "#F7F6EE", "#EABB35", "#17291F", "#284F38", "#F3F8EA"
LENS, CLAY = "#BFE0D8", "#C9693F"

# ---- base anatomy: drawn level, head to the right, ~ x 18..182, y 4..150 ----
ABD = "M18,114 C38,80 86,73 105,92 C117,104 115,124 101,134 C81,150 42,148 18,114 Z"
WING_B = "M112,90 C78,94 40,76 32,42 C72,32 108,56 112,90 Z"
WING_F = "M118,86 C96,62 94,26 120,4 C148,30 144,66 118,86 Z"
VEIN_B = "M102,82 C84,74 64,62 48,46"
VEIN_F = "M117,76 C112,58 113,38 120,20"
BODY = ("M96,104 C96,86 110,78 124,80 C130,72 140,70 150,72 C166,74 174,88 170,102 "
        "C166,114 154,120 142,116 C138,126 128,132 116,130 C104,128 96,118 96,104 Z")
ANT = "M152,74 C154,58 162,48 178,48"
ANT_HAT = "M163,57 C167,45 175,39 187,39"
LEGS = "M110,128 L106,142 L98,145 M130,126 L134,140 L143,142"
BANDS = ("M54,62 Q39,112 53,160 L67,160 Q53,112 68,62 Z "
         "M80,62 Q66,112 80,160 L94,160 Q80,112 94,62 Z")

_uid = [0]
def uid(p):
    _uid[0] += 1
    return f"{p}{_uid[0]}"

def bee(prop=None, sw=6, eye="dot", band=INK, body_fill=POLLEN, legs=True, halo=None, hat=None):
    """Full-colour bee in level coordinates. hat names an entry in HATS; the antenna then grows
    out of the crown instead of the head."""
    c = uid("abd")
    s = [f'<clipPath id="{c}"><path d="{ABD}"/></clipPath>']
    if halo:  # keyline so the ink head and outlines survive on a dark background
        s.append(f'<g fill="{halo}" stroke="{halo}" stroke-width="{sw+9}" stroke-linejoin="round" stroke-linecap="round">'
                 f'<path d="{WING_B}"/><path d="{WING_F}"/><path d="{ABD}"/><path d="{BODY}"/><path d="{ANT}" fill="none"/>'
                 + (f'<path d="{LEGS}" fill="none"/>' if legs else '') + '</g>')
    s += [f'<g stroke="{INK}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">',
         f'<g class="wing wing-b"><path d="{WING_B}" fill="{WING}"/><path d="{VEIN_B}" fill="none" stroke="{FOREST}" stroke-width="{sw*0.5}"/></g>',
         f'<g class="wing wing-f"><path d="{WING_F}" fill="{WING}"/><path d="{VEIN_F}" fill="none" stroke="{FOREST}" stroke-width="{sw*0.5}"/></g>']
    if legs:
        s.append(f'<path d="{LEGS}" fill="none"/>')
    if prop:
        s.append(PROPS[prop][0])
    s += [f'<path d="{ABD}" fill="{body_fill}" stroke="none"/>',
          f'<path d="{BANDS}" fill="{band}" stroke="none" clip-path="url(#{c})"/>',
          f'<path d="{ABD}" fill="none"/>',
          f'<path d="{BODY}" fill="{INK}"/>']
    if not hat:
        s.append(f'<path d="{ANT}" fill="none"/>')
    if eye == "dot":
        s.append(f'<circle cx="157" cy="90" r="4.2" fill="{IVORY}" stroke="none"/>')
    elif eye == "look":   # turned toward the viewer: bigger white, pupil forward-down
        s.append(f'<circle cx="156" cy="90" r="7" fill="{IVORY}" stroke="none"/>'
                 f'<circle cx="153.5" cy="92" r="3.6" fill="{INK}" stroke="none"/>')
    if prop:
        s.append(PROPS[prop][1])
    if hat:
        s.append(HATS[hat] + f'<path d="{ANT_HAT}" fill="none"/>')
    s.append('</g>')
    return "".join(s)

# props: (drawn behind body, drawn in front)
PROPS = {
    "goggles": ("",
        f'<path d="M147,86 C138,86 132,94 134,106" fill="none" stroke="{POLLEN}" stroke-width="5"/>'
        f'<rect x="147" y="79" width="27" height="19" rx="8" fill="{LENS}" stroke="{INK}" stroke-width="4"/>'
        f'<path d="M153,85 L163,85" stroke="{IVORY}" stroke-width="3"/>'),
    "pollen": (
        f'<circle cx="122" cy="150" r="13" fill="{POLLEN}"/>',
        f'<g fill="{INK}" stroke="none"><circle cx="117" cy="147" r="1.8"/><circle cx="126" cy="153" r="1.8"/><circle cx="124" cy="144" r="1.5"/></g>'),
    "hex": (
        f'<path d="M122,136 L136,144 L136,160 L122,168 L108,160 L108,144 Z" fill="{POLLEN}"/>'
        f'<path d="M122,143 L130,148 L130,157 L122,162 L114,157 L114,148 Z" fill="#F2D27A" stroke="none"/>', ""),
    "lens": (
        f'<path d="M134,160 L146,174" fill="none" stroke-width="7"/>'
        f'<circle cx="124" cy="148" r="13" fill="{LENS}"/>'
        f'<path d="M118,143 C120,140 124,139 127,140" fill="none" stroke="{IVORY}" stroke-width="3"/>', ""),
    "lens_held": ("",
        f'<path d="M136,124 C142,136 148,144 156,150" fill="none"/>'
        f'<path d="M154,148 L164,162" fill="none" stroke="{FOREST}" stroke-width="9"/>'
        f'<circle cx="174" cy="178" r="18" fill="{LENS}" fill-opacity=".85" stroke-width="6"/>'
        f'<path d="M165,172 C167,167 172,164 177,165" fill="none" stroke="{IVORY}" stroke-width="3.5"/>'
        f'<path d="M150,146 C154,144 158,146 158,150" fill="none" stroke-width="5"/>'),
    "sprout": (
        f'<path d="M120,166 C121,156 122,148 124,140" fill="none" stroke="{FOREST}" stroke-width="5"/>'
        f'<path d="M124,146 C132,136 144,138 146,144 C138,150 130,150 124,146 Z" fill="#8FB46A" stroke-width="4"/>'
        f'<path d="M122,152 C114,144 104,146 102,152 C110,158 116,157 122,152 Z" fill="#8FB46A" stroke-width="4"/>', ""),
}

# Headwear tells the crew apart at a glance; every hat is lighter than the ink head so it reads.
CREST, CAP_CLAY, CAP_CLAY_D, BERET, BERET_D = "#FFFFFA", CLAY, "#9E4E2C", "#6FB0A8", "#3F7F78"
STRAW, STRAW_D = "#F1D9A0", "#C9A45A"
_CROWN = "M127,82 C124,62 139,51 154,51 C169,51 178,62 175,80 C160,74 141,74 127,82 Z"
HATS = {
    # inspector's peaked cap: ivory crown, forest band and peak, gold badge
    "peaked": (f'<path d="M124,74 C116,64 128,50 151,47 C174,44 190,53 183,66 C180,71 175,72 172,71 C158,66 143,67 130,74 C128,75 126,75 124,74 Z" fill="{CREST}"/>'
               f'<path d="M130,83 C144,76 160,75 173,80 L172,70 C158,66 143,67 130,74 Z" fill="{FOREST}" stroke-width="4.5"/>'
               f'<path d="M167,79 C180,76 195,80 201,89 C189,94 176,92 165,86 Z" fill="{FOREST}"/>'
               f'<circle cx="158" cy="59" r="5.5" fill="{POLLEN}" stroke-width="3.5"/>'),
    # engineer's cap worn backwards: clay crown, peak pointing back
    "backwards": (f'<path d="M136,78 C120,74 102,76 92,86 C104,93 122,92 138,86 Z" fill="{CAP_CLAY_D}"/>'
                  f'<path d="{_CROWN}" fill="{CAP_CLAY}"/>'
                  f'<path d="M151,52 C147,60 146,70 148,76 M157,52 C164,59 167,68 166,75" fill="none" stroke="{CAP_CLAY_D}" stroke-width="3"/>'
                  f'<circle cx="154" cy="51" r="3.6" fill="{CAP_CLAY_D}" stroke-width="3"/>'),
    # gardener's straw sun hat: wide brim, forest band
    "sunhat": (f'<path d="M108,78 C114,66 146,58 190,64 C198,66 198,74 190,76 C162,72 134,76 116,86 C108,88 104,84 108,78 Z" fill="{STRAW}"/>'
               f'<path d="M128,72 C126,56 140,46 156,47 C172,48 180,58 178,68 C162,64 144,66 128,72 Z" fill="{STRAW}"/>'
               f'<path d="M129,70 C144,64 162,62 178,66 L178,60 C162,57 144,58 130,64 Z" fill="{FOREST}" stroke-width="3.5"/>'
               f'<path d="M122,80 C140,73 162,70 184,70" fill="none" stroke="{STRAW_D}" stroke-width="2.5"/>'),
    # storyteller's beret, tipped back over the head
    "beret": (f'<path d="M119,76 C112,62 132,50 155,51 C176,52 186,62 178,73 C163,82 132,85 119,76 Z" fill="{BERET}"/>'
              f'<path d="M126,70 C138,60 156,57 172,60" fill="none" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="3"/>'
              f'<path d="M150,51 L152,43" stroke-width="5"/>'),
}

def _cog(cx, cy, r, teeth=8):
    pts = []
    for k in range(teeth * 4):
        a = math.pi * 2 * k / (teeth * 4)
        rr = r if (k % 4) in (1, 2) else r * .74
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"

PROPS.update({
    "medal": (
        f'<path d="M114,152 L105,178 L114,174 L118,182 L125,156 Z" fill="{FOREST}" stroke-width="4"/>'
        f'<path d="M127,155 L132,182 L137,174 L146,177 L136,152 Z" fill="{CLAY}" stroke-width="4"/>'
        f'<circle cx="122" cy="148" r="15" fill="{POLLEN}"/>',
        f'<path d="M115,148 L120,154 L130,142" fill="none" stroke-width="4.5"/>'),
    "cog": (
        f'<path d="{_cog(124, 150, 17)}" fill="{IVORY}" stroke-width="4.5"/>'
        f'<circle cx="124" cy="150" r="5.5" fill="{POLLEN}" stroke-width="4"/>', ""),
    "letter": (
        f'<g transform="rotate(-10 124 152)"><rect x="104" y="138" width="40" height="28" rx="3" fill="{IVORY}" stroke-width="4.5"/>'
        f'<path d="M106,141 L124,155 L142,141" fill="none" stroke-width="3.5"/><circle cx="124" cy="160" r="3" fill="{CLAY}" stroke="none"/></g>', ""),
    "report": (
        f'<g transform="rotate(-8 122 152)"><rect x="106" y="133" width="32" height="40" rx="3" fill="{IVORY}" stroke-width="4.5"/>'
        f'<rect x="112" y="156" width="5" height="11" fill="{FOREST}" stroke="none"/><rect x="120" y="150" width="5" height="17" fill="{POLLEN}" stroke="none"/>'
        f'<rect x="128" y="144" width="5" height="23" fill="{CLAY}" stroke="none"/><path d="M112,140 H132" stroke-width="3"/></g>', ""),
})

def bee_solid(bg, fg=INK, gap=5, legs=True):
    """One-colour silhouette: parts separated by background-coloured gaps so it holds at 16-24px."""
    c = uid("abd")
    s = [f'<clipPath id="{c}"><path d="{ABD}"/></clipPath>',
         f'<g fill="{fg}" stroke="{bg}" stroke-width="{gap}" stroke-linejoin="round" stroke-linecap="round">',
         f'<path d="{WING_B}"/><path d="{WING_F}"/>']
    if legs:
        s.append(f'<path d="{LEGS}" fill="none" stroke="{fg}" stroke-width="8"/>')
    s += [f'<path d="{ABD}"/>',
          f'<path d="{BANDS}" fill="{bg}" stroke="none" clip-path="url(#{c})"/>',
          f'<path d="{BODY}" stroke-width="{gap+2}"/>',
          f'<path d="{ANT}" fill="none" stroke="{fg}" stroke-width="8"/>',
          f'<circle cx="157" cy="90" r="5" fill="{bg}" stroke="none"/>',
          '</g>']
    return "".join(s)

def fly(inner, angle=-28, s=1.0, tx=0, ty=0):
    return f'<g transform="translate({tx},{ty}) scale({s}) rotate({angle} 100 92)">{inner}</g>'

def front_bee(halo=None):
    """Messenger: faces the visitor (used at Contact)."""
    c = uid("fab")
    wl = "M94,106 C70,108 42,92 38,60 C66,56 90,78 94,106 Z"
    h = (f'<g fill="{halo}" stroke="{halo}" stroke-width="15" stroke-linejoin="round" stroke-linecap="round">'
         f'<path d="{wl}"/><path d="{wl}" transform="translate(200,0) scale(-1,1)"/><circle cx="100" cy="80" r="27"/>'
         f'<ellipse cx="100" cy="128" rx="30" ry="36"/><path d="M84,62 C80,46 70,38 60,38 M116,62 C120,46 130,38 140,38" fill="none"/></g>') if halo else ""
    return (h + f'<clipPath id="{c}"><ellipse cx="100" cy="128" rx="30" ry="36"/></clipPath>'
        f'<g stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">'
        f'<path class="wing wing-l" d="{wl}" fill="{WING}"/><g transform="translate(200,0) scale(-1,1)"><path class="wing wing-r" d="{wl}" fill="{WING}"/></g>'
        f'<path d="M84,62 C80,46 70,38 60,38 M116,62 C120,46 130,38 140,38" fill="none"/>'
        f'<ellipse cx="100" cy="128" rx="30" ry="36" fill="{POLLEN}" stroke="none"/>'
        f'<g clip-path="url(#{c})" fill="{INK}" stroke="none"><rect x="60" y="116" width="80" height="12"/><rect x="60" y="140" width="80" height="12"/></g>'
        f'<ellipse cx="100" cy="128" rx="30" ry="36" fill="none"/>'
        f'<circle cx="100" cy="80" r="27" fill="{INK}"/>'
        f'<circle cx="90" cy="80" r="8" fill="{IVORY}" stroke="none"/><circle cx="110" cy="80" r="8" fill="{IVORY}" stroke="none"/>'
        f'<g class="pupils"><circle cx="90" cy="82" r="4" fill="{INK}" stroke="none"/><circle cx="110" cy="82" r="4" fill="{INK}" stroke="none"/></g>'
        f'<g class="smile"><path d="M89,92 C94,100 106,100 111,92" fill="none" stroke="{IVORY}" stroke-width="4"/>'
        f'<circle cx="80" cy="92" r="4" fill="{CLAY}" stroke="none" opacity=".8"/><circle cx="120" cy="92" r="4" fill="{CLAY}" stroke="none" opacity=".8"/></g>'
        f'<path d="M78,128 L90,142 M122,128 L110,142" fill="none"/>'
        f'<rect x="80" y="136" width="40" height="28" rx="3" fill="{IVORY}" stroke-width="5"/>'
        f'<path d="M81,138 L100,152 L119,138" fill="none" stroke-width="4"/>'
        '</g>')

def svg(inner, vb, w=None, h=None, bg=None, rx=0):
    x, y, W, H = vb
    back = f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="{rx}" fill="{bg}"/>' if bg else ""
    wh = f' width="{w}" height="{h}"' if w else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {W} {H}"{wh}>{back}{inner}</svg>'

HEX = "M100,8 L180,54 L180,146 L100,192 L20,146 L20,54 Z"
SANS = "'DM Sans', Manrope, 'Helvetica Neue', Arial, sans-serif"
SERIF = "'Instrument Serif', Georgia, serif"

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'dist', 'assets', 'fonts')
_fonts = {}
def text_path(txt, font, size, x, y, tracking=0.0, anchor="start"):
    """Outline text so logo files never depend on an installed font."""
    if font not in _fonts:
        _fonts[font] = TTFont(os.path.join(FONT_DIR, font))
    f = _fonts[font]; gs = f.getGlyphSet(); cmap = f.getBestCmap(); k = size / f["head"].unitsPerEm
    names = [cmap[ord(c)] for c in txt]
    width = sum(gs[n].width * k for n in names) + tracking * (len(names) - 1)
    cur = x - (width / 2 if anchor == "middle" else 0)
    pen = SVGPathPen(gs)
    for n in names:
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, cur, y)))
        cur += gs[n].width * k + tracking
    return pen.getCommands()

def wordmark_sans(x, y, ink=INK, sub=FOREST):
    return (f'<path fill="{ink}" d="{text_path("honeybees", "font-3.ttf", 66, x, y, -2.6)}"/>'
            f'<rect x="{x+3}" y="{y+16}" width="28" height="5" rx="2.5" fill="{POLLEN}"/>'
            f'<path fill="{sub}" d="{text_path("CONSULTING", "font-2.ttf", 15.5, x+3, y+48, 7)}"/>')

def wordmark_serif(x, y, ink=INK, sub=FOREST):
    return (f'<path fill="{ink}" d="{text_path("honeybees", "font-5.ttf", 80, x, y, -1)}"/>'
            f'<path fill="{sub}" d="{text_path("CONSULTING", "font-2.ttf", 15.5, x+4, y+40, 7)}"/>')

# ---------- assets ----------
A = {}
A["mark-colour"] = svg(fly(bee(), s=1.0, tx=0, ty=8), (0, 0, 200, 200))
A["mark-solid"] = svg(fly(bee_solid(IVORY), tx=0, ty=8), (0, 0, 200, 200))
A["mark-favicon"] = svg(fly(bee_solid(IVORY, legs=False), s=1.08, tx=-8, ty=4), (0, 0, 200, 200))
A["mark-tile"] = svg(fly(bee_solid(FOREST, fg=IVORY, legs=False), s=0.82, tx=18, ty=24), (0, 0, 200, 200), bg=FOREST, rx=40)
A["mark-hex"] = svg(f'<path d="{HEX}" fill="{FOREST}" stroke="{FOREST}" stroke-width="10" stroke-linejoin="round"/>'
                    + fly(bee_solid(FOREST, fg=IVORY, legs=False), s=0.74, tx=26, ty=30), (0, 0, 200, 200))
A["mark-hex-colour"] = svg(f'<path d="{HEX}" fill="{IVORY}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
                    + fly(bee(), s=0.72, tx=28, ty=30), (0, 0, 200, 200))
A["lockup-sans"] = svg(fly(bee(), s=0.86, tx=-2, ty=6) + wordmark_sans(196, 100), (0, 0, 600, 180))
A["lockup-serif"] = svg(fly(bee(), s=0.86, tx=-2, ty=6) + wordmark_serif(196, 102), (0, 0, 600, 180))
A["lockup-sans-dark"] = svg(fly(bee(halo=IVORY), s=0.86, tx=-2, ty=6) + wordmark_sans(196, 100, ink=IVORY, sub="#C9D8C2"), (0, 0, 600, 180), bg=INK)
A["stacked"] = svg(fly(bee(), s=1.0, tx=100, ty=0)
                   + f'<path fill="{INK}" d="{text_path("honeybees", "font-3.ttf", 56, 200, 262, -2.2, "middle")}"/>'
                   + f'<path fill="{FOREST}" d="{text_path("CONSULTING", "font-2.ttf", 13.5, 203, 296, 6.5, "middle")}"/>',
                   (0, 0, 400, 320))

FLOWER = lambda cx, cy, r=14: (
    f'<g stroke="{INK}" stroke-width="5" stroke-linejoin="round">'
    + "".join(f'<ellipse cx="{cx}" cy="{cy-r}" rx="{r*0.62}" ry="{r}" fill="{IVORY}" transform="rotate({a} {cx} {cy})"/>' for a in range(0, 360, 72))
    + f'<circle cx="{cx}" cy="{cy}" r="{r*0.55}" fill="{POLLEN}"/></g>')
HIVE = lambda cx, cy: (f'<g stroke="{INK}" stroke-width="5" stroke-linejoin="round">'
    + "".join(f'<path d="M{cx+dx},{cy+dy-18} l15.6,9 v18 l-15.6,9 l-15.6,-9 v-18 Z" fill="{f}"/>'
              for dx, dy, f in [(0, 0, POLLEN), (31.2, 0, "#F2D27A"), (15.6, 27, POLLEN)]) + '</g>')
A["story-strip"] = svg(
    FLOWER(70, 120, 22)
    + f'<path d="M96,104 C160,30 250,40 290,90 S420,150 470,80" fill="none" stroke="{FOREST}" stroke-width="4" stroke-dasharray="2 12" stroke-linecap="round"/>'
    + fly(bee(prop="pollen"), angle=-12, s=0.62, tx=212, ty=26)
    + HIVE(510, 76),
    (0, 0, 600, 180))

CHAR = {
    "guide": ("The Guide", "Leads the scroll journey. Keeps A7's goggles, drops the cap so it stays grown-up.", fly(bee(prop="goggles"))),
    "forager": ("The Forager", "Carries pollen from nature to the hive: the value your CSR work creates.", fly(bee(prop="pollen"), angle=-18)),
    "scout": ("The Scout", "Measures first. Holds the lens for footprints, audits and data.", fly(bee(prop="lens", eye="look"), angle=-14)),
    "grower": ("The Grower", "Plants back. Social and environmental impact, the flower side of the story.", fly(bee(prop="sprout"), angle=-20)),
    "builder": ("The Builder", "Brings a honey cell to the hive: strategy and reporting that grow the business.", fly(bee(prop="hex"), angle=-22)),
    "messenger": ("The Messenger", "Turns to face the visitor at Contact.", front_bee()),
    "inspector": ("The Inspector", "Ratings and certifications. Peaked cap, gold medal.", fly(bee(prop="medal", hat="peaked"), angle=-16)),
    "engineer": ("The Engineer", "Data, AI and automation. Cap on backwards, a cog in hand.", fly(bee(prop="cog", hat="backwards"), angle=-20)),
    "gardener": ("The Gardener", "Impact projects. Straw sun hat, a seedling to plant.", fly(bee(prop="sprout", hat="sunhat"), angle=-16)),
    "storyteller": ("The Storyteller", "Reporting and narrative. Beret, and the report everyone reads.", fly(bee(prop="report", hat="beret"), angle=-14)),
}
for k, (_, _, g) in CHAR.items():
    A[f"bee-{k}"] = svg(g, (0, 0, 200, 200))


# ---------- review sheet ----------
def card(title, body, inner, cls=""):
    return f'<figure class="card {cls}"><div class="art">{inner}</div><figcaption><b>{title}</b><span>{body}</span></figcaption></figure>'

def review_html():
    sizes = "".join(f'<div class="sz"><div style="width:{p}px;height:{p}px">{A["mark-favicon"]}</div><small>{p}px</small></div>' for p in (16, 24, 32, 48))
    sizes_tile = "".join(f'<div class="sz"><div style="width:{p}px;height:{p}px">{A["mark-tile"]}</div><small>{p}px</small></div>' for p in (16, 24, 32, 48))
    chars = "".join(card(t, d, A[f"bee-{k}"], "char") for k, (t, d, _) in CHAR.items())

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>honeybees logo v1</title>
<style>
@font-face{{font-family:'DM Sans';font-weight:600;src:url(fonts/font-2.ttf)}}
@font-face{{font-family:'DM Sans';font-weight:700;src:url(fonts/font-3.ttf)}}
@font-face{{font-family:'Instrument Serif';src:url(fonts/font-5.ttf)}}
:root{{--bg:{IVORY};--card:#FFFFFB;--ink:{INK};--sub:#4D5F52;--line:#E4E2D6}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 'DM Sans',system-ui,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:40px 16px 64px}}
h1{{font:400 44px/1.1 'Instrument Serif',serif;margin:0 0 8px}}
h2{{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:{FOREST};margin:44px 0 6px}}
p.lead{{color:var(--sub);max-width:70ch;margin:0}}
p.note{{color:var(--sub);max-width:75ch;margin:0 0 16px}}
.grid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}}
.grid.wide{{grid-template-columns:repeat(auto-fill,minmax(420px,1fr))}}
.card{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden}}
.card .art{{padding:18px;display:flex;align-items:center;justify-content:center;min-height:200px}}
.card .art svg{{width:100%;height:auto;max-height:260px}}
.card.char .art svg{{max-width:190px}}
.card figcaption{{border-top:1px solid var(--line);padding:12px 16px;display:grid;gap:2px}}
.card figcaption span{{color:var(--sub);font-size:14px}}
.sizes{{display:flex;gap:28px;align-items:flex-end;flex-wrap:wrap;padding:18px}}
.sz{{display:grid;justify-items:center;gap:6px}} .sz small{{color:var(--sub)}}
.sz svg{{width:100%;height:100%;display:block}}
@media (max-width:480px){{.grid.wide{{grid-template-columns:1fr}} h1{{font-size:34px}}}}
</style></head><body><main>
<h1>honeybees · logo v1</h1>
<p class="lead">One primary bee, refined from the Leafwing line (A → A7 → the honeybees round), plus a family of characters for the website and slides. Same anatomy everywhere: leaf wings, one ink head-and-thorax, two bands, one antenna.</p>

<h2>1 · Primary logo</h2>
<p class="note">The bee climbs up and to the right (growth). Leaf-shaped wings carry the nature side of the story; the pollen body carries the honey. Pick a wordmark: the sans is the most legible, the serif matches the current site's headings.</p>
<div class="grid wide">
{card("A · Sans lockup", "DM Sans bold, lowercase, tracked CONSULTING, one pollen dash.", A["lockup-sans"])}
{card("B · Serif lockup", "Instrument Serif, warmer and more editorial.", A["lockup-serif"])}
{card("On dark", "The same lockup on ink, for slides and the footer.", A["lockup-sans-dark"])}
{card("Stacked", "For square spaces: social avatar, slide title, merch.", A["stacked"])}
</div>

<h2>2 · Marks and small sizes</h2>
<p class="note">The colour bee is for anything 48px and up. Below that, a solid silhouette with the bands and wing gaps cut out, legs dropped, so it still reads as a bee at favicon size.</p>
<div class="grid">
{card("Colour mark", "Default mark.", A["mark-colour"])}
{card("One colour", "Print, stamps, single-colour use.", A["mark-solid"])}
{card("App / avatar tile", "Forest tile, ivory bee.", A["mark-tile"])}
{card("Hive badge", "Bee in a honey cell: the hive is the business. Corner mark for slides.", A["mark-hex"])}
{card("Hive badge, colour", "Same badge, full colour.", A["mark-hex-colour"])}
</div>
<div class="grid wide" style="margin-top:16px">
<figure class="card"><div class="sizes">{sizes}</div><figcaption><b>Silhouette at real sizes</b><span>Favicon and browser tab.</span></figcaption></figure>
<figure class="card"><div class="sizes">{sizes_tile}</div><figcaption><b>Tile at real sizes</b><span>Home-screen icon and LinkedIn avatar.</span></figcaption></figure>
</div>

<h2>3 · The story in one line</h2>
<p class="note">Flower (nature and people) → bee (honeybees.consulting) → hive (the business). This is the spine of the scroll story and works as a slide divider.</p>
<div class="grid wide">{card("Story strip", "The flight path is the scroll path on the homepage.", A["story-strip"])}</div>

<h2>4 · The bee family</h2>
<p class="note">One body, told apart by a single prop and pose, never by costumes or faces, so it stays adult. Each bee owns a part of the story and a service. The Messenger is the only one that looks straight at you.</p>
<div class="grid">{chars}</div>
</main></body></html>"""

def main(out):
    os.makedirs(out, exist_ok=True)
    for k, v in A.items():
        with open(os.path.join(out, f"{k}.svg"), "w") as f:
            f.write(v)
    with open(os.path.join(out, "review.html"), "w") as f:
        f.write(review_html())
    print("ok", len(A), "svgs")

if __name__ == "__main__":
    main(sys.argv[1])
