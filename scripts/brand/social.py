"""LinkedIn and share images: the company-page logo, the company-page cover and a profile banner.

Usage: python3 scripts/brand/social.py <out-dir>   writes SVGs; render them to PNG with
scripts/brand/render.py (Chromium via Playwright)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *

HEAD_1, HEAD_2 = "Turn ESG into your", "competitive edge."
URL = "honeybees.consulting"


def doc(w, h, inner, bg=IVORY):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{defs()}'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{inner}</svg>')


def light(w, h, cx, cy, r):
    """Warm morning light behind the hives."""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g-glow)" opacity=".55"/>'


def logo_square(size=400, bg=FOREST):
    """Company-page logo: the colour bee with an ivory keyline on forest, small enough to stay
    inside the circle LinkedIn crops profile pictures to."""
    k = size / 200
    inner = (f'<g transform="scale({k})"><g transform="translate(101 103) scale(.72) translate(-100 -92)">'
             f'{fly(bee(halo=IVORY))}</g></g>')
    return doc(size, size, inner, bg=bg)


def market(ground, xs, gold_i, scale=1.0, sw=2.2):
    """A row of hives on the ground line; one of them is gold and lit."""
    out = []
    for i, (x, w, boxes) in enumerate(xs):
        if i == gold_i:
            out.append(glow(x + w * .1, ground - w * 1.2, w * 2.1))
        out.append(shadow(x + w * .15, ground + 1, w * .78, w * .09))
        out.append(box_hive(x, ground, w * scale, boxes, gold=(i == gold_i), sw=sw))
    return "".join(out)


def cover_company():
    """1128x191, LinkedIn company page. The page logo covers x 0..280 from y 60 down (checked on a
    live page), so that corner holds only meadow; words start at x 304, art sits to the right.
    A meadow runs along the whole bottom edge so the strip under the words is never bare."""
    W, H = 1128, 191
    g = 176
    s = [light(W, H, 990, 96, 250)]
    s.append(hill(f"M0,{H} V146 C120,136 240,142 340,152 C440,162 540,158 640,150 C760,140 900,130 1000,132 C1060,133 1100,130 {W},128 V{H} Z", "url(#g-hill-a)"))
    s.append(hill(f"M0,{H} V172 C140,164 300,166 460,170 C620,174 780,166 920,168 C1020,170 1080,164 {W},164 V{H} Z", "url(#g-hill-b)"))
    s.append(market(g, [(818, 40, 1), (892, 48, 2), (1002, 60, 3), (1076, 42, 2)], 2, sw=2.2))
    # the meadow the value comes from, between the words and the hives
    s.append(stem(716, H, 710, 88, bend=-10, leaves=((.42, 1), (.66, -1)), leaf=15, sw=2) + petal_flower(710, 88, 22, rot=8, sw=2))
    s.append(stem(758, H, 762, 122, bend=8, leaves=((.55, -1),), leaf=12, sw=2) + cup_flower(762, 120, 15, sw=2))
    s.append(stem(676, H, 672, 128, bend=6, leaves=((.55, 1),), leaf=11, sw=1.8) + petal_flower(672, 126, 13, n=9, rot=20, sw=1.8))
    s.append(stem(640, H, 638, 152, bend=-4, leaves=((.5, -1),), leaf=9, sw=1.6) + cup_flower(638, 150, 10, sw=1.6))
    # a low strip of grass and small flowers along the bottom, under the words too
    for x in (300, 352, 418, 470, 536, 598, 694, 742, 790, 860, 950, 1046, 1104):
        s.append(grass(x, H, 13 + (x * 7) % 9, 4, spread=7, sw=1.3))
    for x, y, r, kind in [(326, 180, 6.5, "d"), (392, 183, 5.5, "d"), (446, 178, 7, "c"), (508, 182, 6, "d"), (568, 179, 7, "d"),
                          (618, 183, 5.5, "d"), (850, 184, 6, "d"), (944, 185, 7, "d"), (1048, 185, 6, "d"), (1112, 181, 7, "d"), (270, 178, 7, "d")]:
        head = petal_flower(x - 1, y - 4, r, n=9, sw=1.3) if kind == "d" else cup_flower(x - 1, y - 4, r, sw=1.3)
        s.append(stem(x, H, x - 1, y - 2, leaves=(), sw=1.3) + head)
    # the flight path: from the daisy, over the muted hives, into the gold one
    s.append(trail("M724,76 C764,22 862,12 932,24 S1002,50 1006,72", sw=1.8, gap=8))
    s.append(flying_bee(792, 32, .2, angle=-8, prop="pollen"))
    s.append(flying_bee(924, 24, .22, angle=6, prop="goggles"))
    # words, centred in the band the logo leaves free
    s.append(words(URL, "font-2.ttf", 13, 306, 46, FOREST, 1.4))
    s.append(f'<rect x="306" y="54" width="22" height="3.5" rx="1.75" fill="{POLLEN}"/>')
    s.append(words(HEAD_1, "font-5.ttf", 44, 304, 102, INK, -.3))
    s.append(words(HEAD_2, "font-4.ttf", 44, 304, 148, FOREST, -.3))
    return doc(W, H, "".join(s))


def banner_profile():
    """1584x396, LinkedIn profile banner. The profile photo covers roughly x 0..380, y 220..396."""
    W, H = 1584, 396
    g = 360
    s = [light(W, H, 1330, 190, 420)]
    s.append(hill(f"M820,{H} C940,320 1100,300 1250,310 C1380,318 1480,290 {W},296 V{H} Z", "url(#g-hill-a)"))
    s.append(hill(f"M900,{H} C1020,352 1180,344 1300,350 C1420,356 1520,338 {W},342 V{H} Z", "url(#g-hill-b)"))
    s.append(market(g, [(1000, 70, 1), (1120, 80, 2), (1240, 72, 1), (1380, 96, 3), (1520, 76, 2)], 3, sw=3))
    # meadow on the left: the photo hides its lower half, so the flower heads stand tall
    s.append(hill(f"M0,{H} V300 C90,286 220,292 330,320 C370,332 390,360 400,{H} Z", "url(#g-hill-b)"))
    s.append(stem(150, H, 140, 96, bend=-14, leaves=((.5, 1), (.72, -1)), leaf=22, sw=2.4) + petal_flower(140, 96, 34, rot=8, sw=2.4))
    s.append(stem(262, H, 270, 150, bend=16, leaves=((.62, -1),), leaf=18, sw=2.4) + cup_flower(270, 146, 24, sw=2.4))
    s.append(stem(60, H, 54, 176, bend=10, leaves=((.6, 1),), leaf=15, sw=2.4) + petal_flower(54, 174, 22, n=9, rot=20, sw=2.4))
    s.append(stem(340, H, 344, 232, bend=-6, leaves=(), sw=2) + petal_flower(344, 230, 15, n=9, sw=2))
    s.append(grass(104, H, 34, 5, sw=2) + grass(206, H, 28, 4, sw=2) + grass(310, H, 22, 4, sw=2))
    for x, y, r in [(940, 370, 14), (1066, 378, 11), (1300, 376, 12), (1458, 380, 10), (1560, 372, 13)]:
        s.append(stem(x, H, x - 2, y - 2, leaves=(), sw=2) + petal_flower(x - 2, y - 4, r, n=9, sw=2))
    s.append(grass(1180, H, 22, 5, sw=2) + grass(1420, H, 20, 4, sw=2) + grass(980, H, 18, 4, sw=2))
    s.append(trail("M170,80 C300,10 560,20 760,60 S1160,80 1260,70 S1370,86 1392,170", sw=2.6, gap=12))
    s.append(flying_bee(560, 36, .3, angle=-4, prop="pollen"))
    s.append(flying_bee(980, 70, .32, angle=-8, prop="pollen"))
    s.append(flying_bee(1290, 76, .38, angle=12, prop="goggles"))
    s.append(words(URL, "font-2.ttf", 20, 424, 150, FOREST, 2))
    s.append(f'<rect x="424" y="162" width="34" height="5" rx="2.5" fill="{POLLEN}"/>')
    s.append(words(HEAD_1, "font-5.ttf", 62, 420, 230, INK, -.5))
    s.append(words(HEAD_2, "font-4.ttf", 62, 420, 290, FOREST, -.5))
    return doc(W, H, "".join(s))


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, svg_ in [("linkedin-logo", logo_square()), ("linkedin-cover-company", cover_company()),
                       ("linkedin-banner-profile", banner_profile())]:
        with open(os.path.join(out, name + ".svg"), "w") as f:
            f.write(svg_)
    print("ok")
