#!/usr/bin/env python3
"""Add the experiment entry after the original portfolio archive layers.

The original page bodies, scripts, metadata, and media URLs remain byte-for-byte
unchanged. The two marked additions are deliberately idempotent.
"""
from pathlib import Path
import argparse
import re

PAGES = (
    "index.html", "work-tibet.html", "work-wugui.html", "work-houtu.html",
    "work-moving-worlds.html", "work-nobody-says-no.html", "work-ruyue.html",
    "work-quiet-days.html",
)
LINK = '<a class="experiments-nav" href="/experiments/">实验交互</a>'
STYLE = '''<style id="experiments-navigation">
header nav .experiments-nav{white-space:nowrap;font-size:11px;letter-spacing:1px;padding:8px 0;color:var(--dim);text-decoration:none}
header nav .experiments-nav:hover{color:var(--paper)}
header nav .experiments-nav:focus-visible{outline:1px solid currentColor;outline-offset:5px;text-decoration:underline}
@media(max-width:900px){header nav .experiments-nav{font-size:12px}}
@media(max-width:480px){header nav{flex-wrap:wrap}header nav .experiments-nav{font-size:11px;letter-spacing:0}}
@media(max-width:420px){header nav{justify-content:flex-end;gap:8px 18px}header .category-nav{flex-basis:100%;justify-content:space-between;gap:10px}header .nav-divider{display:none}.intro{top:max(185px,22%)}}
</style>'''
APP_FILES = (
    "experiments/index.html", "experiments/experiments.css",
    "experiments/tidal-echoes-cover.png", "experiments/tidal-echoes/index.html",
    "experiments/tidal-echoes/app.js", "experiments/tidal-echoes/style.css",
)


def patch_page(original: str, name: str) -> str:
    """Fail closed if the portfolio layout changes; never silently corrupt it."""
    navs = re.findall(r'<nav\b[^>]*aria-label="主导航"[^>]*>.*?</nav>', original, re.S)
    if len(navs) != 1 or original.count("</head>") != 1:
        raise ValueError(f"{name}: expected one main navigation and head")
    nav = navs[0]
    if 'class="experiments-nav"' in original:
        if nav.count(LINK) != 1 or original.count(STYLE) != 1:
            raise ValueError(f"{name}: partial or changed experiment navigation")
        return original
    if 'id="experiments-navigation"' in original:
        raise ValueError(f"{name}: experiment style exists without its link")
    marker = '<button id="index-open"'
    if nav.count(marker) != 1:
        raise ValueError(f"{name}: original portfolio index button not found")
    return original.replace(nav, nav.replace(marker, LINK + marker, 1), 1).replace(
        "</head>", STYLE + "\n</head>", 1
    )


def install(site: Path) -> list[str]:
    missing = [p for p in (*PAGES, *APP_FILES) if not (site / p).is_file()]
    if missing:
        raise ValueError("Incomplete website; refusing publication: " + ", ".join(missing))
    # Validate every page before writing any page.
    changes = []
    for name in PAGES:
        path = site / name
        original = path.read_text(encoding="utf-8")
        patched = patch_page(original, name)
        if patched != original:
            changes.append((path, patched))
    for path, patched in changes:
        path.write_text(patched, encoding="utf-8")
    return [path.name for path, _ in changes]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", nargs="?", default="_site", type=Path)
    args = parser.parse_args()
    try:
        changed = install(args.site)
    except ValueError as error:
        parser.exit(1, str(error) + "\n")
    print(f"Experiment entry validated; {len(changed)} portfolio pages updated.")
