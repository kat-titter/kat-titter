#!/usr/bin/env python3
"""Tab icon and share card for every page. build.sh runs `share.py --stamp`; plain `python3 share.py` also redraws the PNGs.

share/icon.svg is the one home of the icon (one action potential, in the page's ink): the tab icon is inlined from it
and the 180 px touch icon drawn from it. share/card.html is the 1200 x 630 share card's source; the PNGs need Chrome.
"""
import html, re, subprocess, sys, urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://kat-titter.github.io/kat-titter/"
ROLE = "Scientist-engineer and technical storyteller in neuroscience, imaging and AI."
PAGES = {  # page: (og:title, og:description, og:url path)
    "index.html": ("Katherine Titterton — Resume", ROLE, ""),
    "resume.html": ("Katherine Titterton — Resume", ROLE, "resume.html"),
    "cv.html": ("Katherine Titterton — Curriculum Vitae", ROLE + " Full CV with publications and talks.", "cv.html"),
}
ALT = "Katherine Titterton: scientist-engineer in neuroscience, imaging and AI. Resume and CV."
TOUCH_BG = "#1a1a1a"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def head(page):
    """The icon, touch-icon and share tags for one page's head."""
    title, desc, path = (html.escape(x) for x in PAGES[page])
    svg = (ROOT / "share/icon.svg").read_text().strip().replace('"', "'")
    icon = "data:image/svg+xml," + urllib.parse.quote(svg, safe=" ='/:;,.-()")
    card = SITE + "share/card.png"
    return "\n".join([
        f'<link rel="icon" href="{icon}">',
        '<link rel="apple-touch-icon" href="share/apple-touch-icon.png">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{SITE}{path}">',
        '<meta property="og:type" content="profile">',
        f'<meta property="og:image" content="{card}">',
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{ALT}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:image" content="{card}">',
    ])


def stamp():
    """Put head(page) between each page's <!-- share --> markers."""
    for page in PAGES:
        p = ROOT / page
        s, n = re.subn(r"<!-- share -->.*?<!-- /share -->",
                       lambda m: "<!-- share -->\n" + head(page) + "\n<!-- /share -->", p.read_text(), flags=re.S)
        assert n == 1, f"{page}: expected one <!-- share --> block"
        p.write_text(s)


def shot(page, png, w, h):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--virtual-time-budget=8000", f"--window-size={w},{h}", f"--screenshot={png}", page.as_uri()],
                   check=True, capture_output=True)


def render():
    """Redraw share/apple-touch-icon.png (180 px, opaque, iOS rounds the corners) and share/card.png."""
    tmp = ROOT / "share/.touch.html"
    tmp.write_text(f'<body style="margin:0;background:{TOUCH_BG}">{(ROOT / "share/icon.svg").read_text()}'
                   '<style>svg{display:block;width:180px;height:180px}</style>')
    try:
        shot(tmp, ROOT / "share/apple-touch-icon.png", 180, 180)
    finally:
        tmp.unlink()
    shot(ROOT / "share/card.html", ROOT / "share/card.png", 1200, 630)
    for p in ("apple-touch-icon.png", "card.png"):
        print(f"share/{p}: {(ROOT / 'share' / p).stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    stamp()
    if "--stamp" not in sys.argv:
        render()
