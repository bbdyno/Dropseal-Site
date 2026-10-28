"""Builds docs/ from src/content.py. Run: python3 src/build.py

English pages sit at the site root; every other language gets its own folder (docs/ko/ …)
with the same three pages, linked to each other with hreflang.
"""
from pathlib import Path
import re

from content import CONTACT, LANGUAGES, NAMES, TEXT

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
ICONS = ROOT / "src" / "icons"
BASE_URL = "https://bbdyno.github.io/Dropseal-Site/"
PAGES = ["index", "privacy", "support"]


def icon(name):
    return (ICONS / f"{name}.svg").read_text().strip()


def folder(lang):
    return "" if lang == "en" else f"{lang}/"


def page_file(page):
    return "./" if page == "index" else f"{page}.html"


def url(lang, page):
    return BASE_URL + folder(lang) + ("" if page == "index" else f"{page}.html")


def mail():
    return f'<a href="mailto:{CONTACT}">{CONTACT}</a>'


def head(lang, page, title, desc):
    up = "" if lang == "en" else "../"
    alternates = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{url(l, page)}">' for l in LANGUAGES)
    t = TEXT[lang]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
{alternates}
<link rel="alternate" hreflang="x-default" href="{url('en', page)}">
<link rel="icon" href="{up}seal.svg" type="image/svg+xml">
<link rel="stylesheet" href="{up}style.css">
</head>
<body><main>
<header class="top">
<a class="brand" href="{page_file('index')}">{icon('seal-fill')}Dropseal</a>
<nav><a href="privacy.html">{t['nav_privacy']}</a><a href="support.html">{t['nav_support']}</a><a href="#languages">{NAMES[lang]}</a></nav>
</header>
"""


def foot(lang, page):
    up = "" if lang == "en" else "../"
    links = []
    for other in LANGUAGES:
        href = up + folder(other) + ("" if page == "index" else f"{page}.html") or "./"
        current = ' aria-current="page"' if other == lang else ""
        links.append(f'<a href="{href}" hreflang="{other}" lang="{other}"{current}>{NAMES[other]}</a>')
    return f"""<footer>
<nav id="languages" class="langs" aria-label="{TEXT[lang]['language']}">{''.join(links)}</nav>
<p>© 2026 Taein Kim · {mail()}</p>
</footer>
</main></body>
</html>
"""


def index(lang):
    t = TEXT[lang]
    steps = "\n".join(
        f'<li><span class="n">{i}</span><div><h3>{title}</h3><p>{body}</p></div></li>'
        for i, (title, body) in enumerate(t["steps"], start=1))
    glyphs = ["sneaker-move", "flame", "timer", "path"]
    metrics = "\n".join(
        f"<div>{icon(g)}<strong>{name}</strong><span>{note}</span></div>"
        for g, (name, note) in zip(glyphs, t["metrics"]))
    local = t["local_text"].replace("{privacy}", f'<a href="privacy.html">{t["privacy_link"]}</a>')
    return f"""<h1>{t['h1']}</h1>
<p class="lede">{t['lede']}</p>

<h2>{t['how']}</h2>
<ol class="steps">
{steps}
</ol>

<h2>{t['goals']}</h2>
<div class="metrics">
{metrics}
</div>

<h2>{t['local']}</h2>
<p class="muted">{local}</p>
<p class="note">{t['soon']}</p>
"""


def privacy(lang):
    t = TEXT[lang]
    points = "\n".join(f"<li>{p}</li>" for p in t["privacy_points"])
    sections = "\n".join(f"<h2>{h}</h2>\n<p>{p.replace('{mail}', mail())}</p>" for h, p in t["privacy_sections"])
    return f"""<div class="prose">
<h1 class="page-title">{t['privacy_h1']}</h1>
<p class="muted">{t['updated']}</p>
<ul>
{points}
</ul>
{sections}
</div>
"""


def support(lang):
    t = TEXT[lang]
    faq = "\n".join(f"<h2>{q}</h2>\n<p>{a}</p>" for q, a in t["faq"])
    return f"""<div class="prose">
<h1 class="page-title">{t['support_h1']}</h1>
<p>{t['support_contact'].replace('{mail}', mail())}</p>
{faq}
</div>
"""


BODIES = {"index": index, "privacy": privacy, "support": support}
META = {"index": ("index_title", "index_desc"), "privacy": ("privacy_title", "privacy_desc"),
        "support": ("support_title", "support_desc")}


def main():
    for lang in LANGUAGES:
        out = DOCS / folder(lang)
        out.mkdir(parents=True, exist_ok=True)
        for page in PAGES:
            title_key, desc_key = META[page]
            html = head(lang, page, TEXT[lang][title_key], TEXT[lang][desc_key]) + BODIES[page](lang) + foot(lang, page)
            assert "{" not in re.sub(r"<svg.*?</svg>", "", html, flags=re.S), f"unfilled placeholder in {lang}/{page}"
            (out / f"{page}.html").write_text(html)
    print("built", len(LANGUAGES) * len(PAGES), "pages")


if __name__ == "__main__":
    main()
