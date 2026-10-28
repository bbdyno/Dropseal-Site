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
<link rel="icon" href="{up}icon.png" type="image/png">
<link rel="apple-touch-icon" href="{up}icon.png">
<link rel="stylesheet" href="{up}style.css">
<script src="{up}site.js" defer></script>
</head>
<body class="page-{page}"><main>
<header class="top">
<a class="brand" href="{page_file('index')}"><img src="{up}icon.png" alt="">Dropseal</a>
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


UNITS = {"en": ["steps", "kcal", "min", "km"], "ko": ["걸음", "kcal", "분", "km"], "ja": ["歩", "kcal", "分", "km"],
         "zh-Hans": ["步", "千卡", "分钟", "公里"], "zh-Hant": ["步", "大卡", "分鐘", "公里"]}
GOALS = [50000, 3000, 300, 100]


def index(lang):
    t = TEXT[lang]
    up = "" if lang == "en" else "../"
    media = f"{up}media/{lang}"
    steps = "\n".join(
        f'<article class="story-step"><span class="n">{i}</span><h3>{title}</h3><p>{body}</p></article>'
        for i, (title, body) in enumerate(t["steps"], start=1))
    alt = t["screen_alt"]
    screens = "\n".join([
        f'<img class="screen" src="{media}/5-compose.jpg" alt="{alt[0]}" loading="lazy">',
        f'<video class="screen" src="{media}/sealing.mp4" poster="{media}/sealing.jpg" muted playsinline preload="metadata" aria-label="{alt[1]}"></video>',
        f'<img class="screen" src="{media}/2-sealed.jpg" alt="{alt[2]}" loading="lazy">',
        f'<video class="screen" src="{media}/unsealing.mp4" poster="{media}/unsealing.jpg" muted playsinline preload="metadata" aria-label="{alt[3]}"></video>',
    ])
    glyphs = ["sneaker-move", "flame", "timer", "path"]
    metrics = "\n".join(
        f'<div>{icon(g)}<strong>{name}</strong><p class="figure"><span data-count="{goal}">{goal:,}</span> {unit}</p><span>{note}</span></div>'
        for g, (name, note), goal, unit in zip(glyphs, t["metrics"], GOALS, UNITS[lang]))
    local = t["local_text"].replace("{privacy}", f'<a href="privacy.html">{t["privacy_link"]}</a>')
    return f"""</main>
<section class="hero">
<div class="hero-stage">
<div class="hero-copy">
<h1>{t['h1']}</h1>
<p class="lede">{t['lede']}</p>
<p class="hint">{t['scroll_hint']} <span aria-hidden="true">↓</span></p>
</div>
<figure class="hero-figure">
<svg class="hero-seal" role="img" aria-label="Dropseal"></svg>
<p class="hero-meter"><span class="hero-count" data-goal="50000">0</span><span class="of"> / 50,000 {t['unit']}</span></p>
<blockquote class="hero-letter">{t['letter_line']}</blockquote>
</figure>
</div>
</section>

<section class="story">
<div class="wrap">
<h2 class="reveal">{t['how']}</h2>
<div class="story-grid">
<div class="story-steps">
{steps}
</div>
<div class="phone-col">
<div class="phone">
{screens}
</div>
<button class="sound-toggle" type="button" aria-pressed="false" data-on="{t['sound_on']}" data-off="{t['sound_off']}">{t['sound_on']}</button>
</div>
</div>
</div>
</section>

<main>
<section class="reveal">
<h2>{t['goals']}</h2>
<div class="metrics">
{metrics}
</div>
</section>

<section class="reveal">
<h2>{t['local']}</h2>
<p class="muted big">{local}</p>
</section>

<section class="price reveal">
<svg class="seal-static" data-progress="0.12" aria-hidden="true"></svg>
<div>
<h2>{t['price_title']}</h2>
<p class="muted">{t['soon']}</p>
<p class="note">{t['store_note']}</p>
</div>
</section>
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
