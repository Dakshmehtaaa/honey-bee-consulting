"""Render SVG files to PNG with Chromium (Playwright).

Usage: python3 scripts/brand/render.py <file.svg> <out.png> [scale]"""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

src, out = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2]
scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1
svg = src.read_text()
w, h = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg = b.new_page(viewport={"width": int(w), "height": int(h)}, device_scale_factor=scale)
    pg.set_content(f'<style>html,body{{margin:0}}svg{{display:block;width:{w}px;height:{h}px}}</style>{svg}')
    pg.screenshot(path=out, omit_background=False)
    b.close()
print(out)
