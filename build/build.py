"""Generate the Kalyani Boat Service website into site/.

Edit the details below (contacts, tours, prices), then run:
    python3 build/build.py
and upload the contents of site/ to public_html on Hostinger.
Needs Python 3.8+ and Pillow (for image sizes): pip install pillow

Content rule: everything below comes from the client (price sheet, phone numbers, email, photos).
Anything not confirmed by the client is listed in README.md under "Still to confirm" and kept off the site.
"""
import json
from html import escape
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"

# ---------------------------------------------------------------- business details (from the client)
SITE = {
    "name": "Kalyani Boat Service",
    "url": "https://alleppeyshikaratours.com",
    "phones": ["+91 98473 86262", "+91 97477 98412"],
    "whatsapp": "919847386262",  # country code + number, no + or spaces
    "email": "alleppeyshikaratours@gmail.com",
    "jetty": "Rajiv Boat Jetty, Alappuzha",
    "maps": "https://www.google.com/maps/search/?api=1&query=Rajiv+Boat+Jetty+Alappuzha",
}

# ---------------------------------------------------------------- routes (from the client's price sheet)
START = ["Rajiv Boat Jetty", "Snake Boat Race starting point", "Snake Boat model",
         "Snake Boat Race finishing point", "Vembanad Lake", "SAI (Sports Authority of India)", "C Block"]
END = ["Vilakkumaram", "Back to Rajiv Boat Jetty"]
VILLAGES = ["Kainakary", "Chavara Bhavan", "Vattakayal", "Pallathurthi"]
FARMS = ["Narrow canals", "Paddy cultivation below sea level", "Temples", "Duck farming", "Fish hatchery"]
ROUTES = {
    "base": (START + END, []),
    "half": (START + VILLAGES + END, VILLAGES),
    "full": (START + FARMS + VILLAGES + END, FARMS + VILLAGES),
}

# ---------------------------------------------------------------- tours (from the client's price sheet)
# start/end are hours (15.5 = 3:30 pm); price is for a couple; extra is per extra person per hour.
TOURS = [
    dict(slug="sunrise-cruise", name="Sunrise Cruise", start=6, end=9, hours=3, price=1500, extra=100,
         sky="pulari", part="morning", img="deck-front", route="base", includes=["Morning tea or coffee"],
         lead="Sunrise on Vembanad Lake, past the Snake Boat Race track. Morning tea or coffee on board.",
         title="Sunrise Shikara Cruise in Alleppey"),
    dict(slug="half-day-tour", name="Half Day Tour", start=8, end=12, hours=4, price=2300, extra=150,
         sky="pakal", part="morning", img="shikara-kalyani", route="half", includes=["Kerala breakfast", "Tea or coffee"],
         lead="Four hours out to Kainakary, Chavara Bhavan, Vattakayal and Pallathurthi, with Kerala breakfast.",
         title="Half Day Shikara Tour with Breakfast"),
    dict(slug="full-day-tour", name="Full Day Tour", start=8, end=16, hours=8, price=4600, extra=150,
         sky="pakal", part="morning", img="chairs-pink", route="full", includes=["Kerala breakfast", "Lunch, veg or non-veg", "Tea or coffee"],
         time_label="From 8:00 am · 8 hours",
         lead="Eight hours through narrow canals, paddy fields below sea level, temples, duck farming and villages. Breakfast and lunch included.",
         title="Full Day Shikara Tour with Breakfast & Lunch"),
    dict(slug="breakfast-cruise", name="Breakfast Cruise", start=9, end=12, hours=3, price=1800, extra=100,
         sky="pakal", part="morning", img="deck-sofa", route="base", includes=["Kerala breakfast", "Tea or coffee"],
         lead="The classic route from 9 am to noon, with Kerala breakfast on board.",
         title="Breakfast Shikara Cruise in Alleppey"),
    dict(slug="lunch-cruise", name="Lunch Cruise", start=13, end=16, hours=3, price=1800, extra=100,
         sky="pakal", part="afternoon", img="chairs-green", route="base", includes=["Tea or coffee"],
         lead="The classic route from 1 pm to 4 pm across Vembanad Lake.",
         title="Afternoon Lunch Cruise by Shikara"),
    dict(slug="sunset-cruise", name="Sunset Cruise", start=15.5, end=18.5, hours=3, price=1600, extra=100,
         sky="anthi", part="evening", img="shikara-sunset-bow", route="base", includes=["Tea or coffee with snacks"],
         lead="Sunset over Vembanad Lake, with evening tea or coffee and snacks.",
         title="Sunset Shikara Cruise on Vembanad Lake"),
    dict(slug="regular-cruise", name="Regular Cruise", start=None, end=None, hours=3, price=1500, extra=100,
         sky="kayal", part="any", img="guests-bow", route="base", includes=["Tea or coffee with snacks"],
         lead="Any three hours you choose, on the classic route.",
         title="3-Hour Shikara Cruise at Your Own Time"),
]
PARTS = [("all", "All"), ("morning", "Morning"), ("afternoon", "Afternoon"), ("evening", "Evening"), ("any", "Any time")]


def clock(h):
    hh, mm = int(h), int(round((h - int(h)) * 60))
    ap = "am" if hh < 12 else "pm"
    return f"{(hh - 1) % 12 + 1}:{mm:02d} {ap}"


for t in TOURS:
    t["time"] = t.get("time_label") or (f"{clock(t['start'])} – {clock(t['end'])}" if t["start"] is not None else "Any 3 hours")
    t["hhmm"] = f"{int(t['start']):02d}:{int(round((t['start'] % 1) * 60)):02d}" if t["start"] is not None else "Any time"
TOUR = {t["slug"]: t for t in TOURS}


def inr(v):
    s = str(v)
    return "₹" + (s[:-3] + "," + s[-3:] if len(s) > 3 else s)


# ---------------------------------------------------------------- photos (the client's)
CAPTIONS = {
    "shikara-sunset-bow": "Sunset from the bow of a Kalyani shikara",
    "shikara-kalyani": "The Kalyani shikara at the jetty",
    "deck-sofa": "Front deck under the canopy",
    "deck-front": "Looking out from the shikara deck",
    "deck-yellow": "The front deck",
    "chairs-green": "Chairs under the canopy",
    "guests-bow": "Guests on the front deck",
    "deck-pink": "On board a Kalyani shikara",
    "chairs-pink": "Seating on board",
    "kayak-rainbow": "Kayaking",
    "kayak-sunset-solo": "Kayaking at sunset",
    "kayak-canal": "Kayaking",
    "kayak-sunrise-group": "Kayaking at sunrise",
    "kayak-sunset-group": "Kayaks at sunset",
    "kayak-trees": "Kayaking",
}
DIMS = {}
for f in (OUT / "assets/img").glob("*-lg.webp"):
    DIMS[f.name[:-8]] = Image.open(f).size


def img(name, alt=None, sizes="(max-width: 820px) 100vw, 50vw", eager=False, pos=None, cls=""):
    w, h = DIMS[name]
    style = f' style="object-position:{pos}"' if pos else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="assets/img/{name}-lg.webp" srcset="assets/img/{name}-sm.webp 640w, assets/img/{name}-lg.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{escape(alt if alt is not None else CAPTIONS[name])}" {load}{style}>')


# ---------------------------------------------------------------- shared pieces
WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s1 2.6 1.1 2.7c.1.2 1.9 2.9 4.6 4 1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BOOK = "Hi Kalyani Boat Service! I'd like to book a shikara ride."
NAV = [("tours.html", "Tours"), ("kayaking.html", "Kayaking"), ("gallery.html", "Gallery"), ("contact.html", "Contact")]


def wa(msg, label="Book on WhatsApp", cls="btn btn--coral"):
    return f'<a class="{cls}" href="contact.html" data-wa="{escape(msg)}">{WA_ICON}<span>{label}</span></a>'


def header(current):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == current else ""}>{n}</a>' for h, n in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar">
  <a class="logo" href="index.html" aria-label="Kalyani Boat Service, home"><span class="script">Kalyani</span><small>Boat Service</small></a>
  <nav class="nav" id="nav" aria-label="Main">{links}</nav>
  <div class="bar__end">{wa(BOOK, "Book", "btn btn--ink btn--sm")}<button class="menu" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button></div>
</div></header>'''


def footer():
    tours = "".join(f'<li><a href="{t["slug"]}.html">{t["name"]}</a></li>' for t in TOURS)
    phones = "".join(f'<li><a href="tel:{p.replace(" ", "")}">{p}</a></li>' for p in SITE["phones"])
    return f'''<footer class="foot"><div class="wrap">
  <div class="foot__cta"><h2>Ready when <span class="grad grad--anthi">you are.</span></h2>{wa(BOOK, "Book on WhatsApp", "btn btn--coral btn--lg")}</div>
  <div class="foot__grid">
    <div><a class="logo" href="index.html"><span class="script">Kalyani</span><small>Boat Service</small></a><p class="mut" style="margin-top:12px">Shikara tours and kayaking from {SITE["jetty"]}.</p></div>
    <div><h4>Tours</h4><ul>{tours}</ul></div>
    <div><h4>Contact</h4><ul>{phones}<li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li><li><a href="{SITE["maps"]}" target="_blank" rel="noopener">{SITE["jetty"]}</a></li></ul></div>
    <div><h4>More</h4><ul><li><a href="kayaking.html">Kayaking</a></li><li><a href="gallery.html">Gallery</a></li><li><a href="terms.html">Booking terms</a></li><li><a href="privacy.html">Privacy</a></li></ul></div>
  </div>
  <p class="foot__base">© <span id="year">2026</span> Kalyani Boat Service, Alleppey</p>
</div></footer>
<div class="dock" id="dock"><span><b>From {inr(1500)}</b> for two</span>{wa(BOOK, "Book", "btn btn--coral btn--sm")}</div>'''


def page(path, title, desc, body, current=None, scripts="", schema=None, og="og-image.jpg", noindex=False, base=False):
    url = SITE["url"] + "/" + ("" if path == "index.html" else path)
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.add("js")</script>
{'<base href="/">' if base else ""}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Kalyani Boat Service">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE["url"]}/assets/img/{og}">
<meta name="theme-color" content="#FFFDF7">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Yellowtail&display=swap">
<link rel="stylesheet" href="assets/css/style.css?v=13">
{ld}
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/data.js?v=13"></script>
<script src="assets/js/main.js?v=13" defer></script>
{scripts}
</body>
</html>
'''


def chip(t):
    return f'<span class="chip chip--{t["sky"]}">{t["time"]}</span>'


def card(t):
    return f'''<a class="card rv" href="{t["slug"]}.html" data-part="{t["part"]}">
  <div class="card__img">{img(t["img"], sizes="(max-width:700px) 85vw, 380px")}{chip(t)}</div>
  <div class="card__body"><h3>{t["name"]}</h3><p class="mut">{escape(t["lead"])}</p>
    <div class="card__foot"><span><b class="price">{inr(t["price"])}</b> <span class="mut">for two</span></span><span class="go" aria-hidden="true">{ARROW}</span></div></div>
</a>'''


def tours_rail():
    chips = "".join(f'<button type="button" class="filter{" on" if k == "all" else ""}" data-f="{k}">{n}</button>' for k, n in PARTS)
    return f'''<div class="filters" role="group" aria-label="Filter tours by time of day">{chips}</div>
<div class="rail" id="rail">{"".join(card(t) for t in TOURS)}</div>'''


def route_block(t):
    stops, extra = ROUTES[t["route"]]
    lis = "".join(f'<li class="{"x" if s in extra else ""}"><span class="n">{i + 1:02d}</span>{escape(s)}</li>' for i, s in enumerate(stops))
    return f'<ol class="route rv">{lis}</ol>'


def faq(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"


def booking(selected="sunrise-cruise", heading="Book your ride"):
    opts = "".join(f'<option value="{t["slug"]}"{" selected" if t["slug"] == selected else ""}>{t["name"]} · {t["time"]}</option>' for t in TOURS)
    t = TOUR[selected]
    return f'''<form class="book rv" data-calc data-email action="enquiry.php" method="post">
  <div class="book__main">
    <h3>{heading}</h3>
    <label class="field"><span>Tour</span><select name="tour">{opts}</select></label>
    <div class="fields">
      <label class="field"><span>Date</span><input type="date" name="date" required></label>
      <div class="field"><span id="g-label">Guests</span>
        <div class="step" role="group" aria-labelledby="g-label"><button type="button" data-step="-1" aria-label="Fewer guests">−</button><output aria-live="polite">2</output><button type="button" data-step="1" aria-label="More guests">+</button></div>
        <input type="hidden" name="guests" value="2"></div>
      <label class="field"><span>Name</span><input name="name" autocomplete="name" required></label>
      <label class="field"><span>Phone / WhatsApp</span><input name="phone" type="tel" autocomplete="tel" required></label>
    </div>
    <label class="field"><span>Email (optional)</span><input name="email" type="email" autocomplete="email"></label>
    <label class="field"><span>Start time or a note (optional)</span><input name="message" placeholder="For the Regular Cruise, tell us your start time"></label>
    <label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>
    <input type="hidden" name="started" value="">
    <p class="status" role="status" hidden></p>
  </div>
  <aside class="book__side">
    <span class="mut">Total</span>
    <span class="sum">{inr(t["price"])}</span>
    <p class="sumnote mut">Price for two guests</p>
    <div class="book__acts"><button type="button" class="btn btn--coral btn--block" data-send="wa">{WA_ICON}<span>Send on WhatsApp</span></button><button type="submit" class="btn btn--ghost btn--block">Send by email</button></div>
  </aside>
</form>'''


BUSINESS = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "name": SITE["name"], "url": SITE["url"],
    "image": SITE["url"] + "/assets/img/og-image.jpg", "telephone": SITE["phones"][0], "email": SITE["email"],
    "priceRange": f"{inr(min(t['price'] for t in TOURS))} – {inr(max(t['price'] for t in TOURS))}",
    "address": {"@type": "PostalAddress", "streetAddress": "Rajiv Boat Jetty", "addressLocality": "Alappuzha", "addressRegion": "Kerala", "addressCountry": "IN"},
}
PRICE_FAQ = [
    ("Where do we board?", f"All tours start and end at {SITE['jetty']}."),
    ("How is the price calculated?", "Each price is for two guests. Every extra guest adds ₹100 per hour on the three-hour tours and ₹150 per hour on the Half Day and Full Day tours."),
    ("Can we choose our own time?", f"Yes. The Regular Cruise runs for any three hours you choose, at {inr(1500)} for two."),
    ("How do we book?", "Send us your tour, date and number of guests on WhatsApp, by phone or with the booking form. We confirm availability."),
]

# hero photos, by hour of the day (hour from, hour to, focus)
HERO = [("kayak-sunrise-group", 0, 7.5, "50% 62%"), ("deck-front", 7.5, 10, "50% 55%"), ("shikara-kalyani", 10, 13, "50% 62%"),
        ("chairs-green", 13, 15.5, "50% 50%"), ("shikara-sunset-bow", 15.5, 18.6, "50% 55%"), ("kayak-sunset-group", 18.6, 24, "50% 60%")]


# ---------------------------------------------------------------- pages
def home(extra=""):
    pics = "".join(f'<img src="assets/img/{n}-lg.webp" alt="" data-from="{a}" data-to="{b}" style="object-position:{p}"' + (' class="on" fetchpriority="high"' if i == 0 else ' loading="lazy"') + ">" for i, (n, a, b, p) in enumerate(HERO))
    body = f'''<section class="hero" id="hero" aria-label="Kalyani Boat Service">
  <div class="hero__pics" aria-hidden="true">{pics}</div>
  <div class="hero__wash" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <div class="hero__text">
      <h1 class="rv">Alleppey <span class="grad grad--hero">by shikara.</span></h1>
      <p class="hero__sub rv">Seven tours from Rajiv Boat Jetty, sunrise to sunset. From {inr(1500)} for two.</p>
      <div class="hero__acts rv">{wa(BOOK, "Book on WhatsApp", "btn btn--coral btn--lg")}<a class="btn btn--glass btn--lg" href="#tours"><span>See tours</span>{ARROW}</a></div>
    </div>
    <div class="dial rv">
      <svg class="dial__svg" id="dial" viewBox="0 0 600 320" role="slider" tabindex="0" aria-label="Time of day: drag the sun" aria-valuemin="5" aria-valuemax="19.5" aria-valuenow="6">
        <defs><linearGradient id="pull" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFE7A8"/><stop offset=".6" stop-color="#FFC94A"/><stop offset="1" stop-color="#FFB320"/></linearGradient></defs>
        <line class="dial__hz" x1="10" y1="300" x2="590" y2="300"/>
        <path class="dial__arc" d="M30 300 A270 250 0 0 1 570 300"/>
        <path class="dial__pull" id="dpull" d="M30 300 A270 250 0 0 1 30 300"/>
        <g id="dticks"></g>
        <circle class="dial__halo" id="dhalo" r="24"/><circle class="dial__sun" id="dsun" r="13"/>
      </svg>
      <div class="dial__read">
        <button type="button" class="dial__play" id="dplay" aria-label="Pause">❚❚</button>
        <a class="dial__now" id="dnow" href="sunrise-cruise.html"><b id="dclock">06:00</b><span id="dname">Sunrise Cruise</span></a>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="tours"><div class="wrap">
  <div class="head"><h2 class="rv">Choose your <span class="grad grad--kayal">time.</span></h2><a class="link" href="tours.html">All tours {ARROW}</a></div>
  {tours_rail()}
</div></section>

<section class="sec band band--pakal"><div class="wrap split">
  <div class="rv"><h2>Same lake, <span class="grad grad--anthi">two moods.</span></h2><p class="lede">Drag to compare sunrise and sunset on Vembanad Lake.</p>
    <div class="acts"><a class="btn btn--white" href="sunrise-cruise.html"><span>Sunrise · {inr(1500)}</span></a><a class="btn btn--white" href="sunset-cruise.html"><span>Sunset · {inr(1600)}</span></a></div></div>
  <div class="compare rv" id="compare">
    {img("kayak-sunrise-group", alt="Sunrise on Vembanad Lake", sizes="(max-width:900px) 100vw, 640px", pos="50% 62%")}
    <div class="compare__top">{img("shikara-sunset-bow", alt="Sunset from a Kalyani shikara", sizes="(max-width:900px) 100vw, 640px")}</div>
    <span class="compare__line" aria-hidden="true"><i></i></span><span class="tag tag--l">Sunrise</span><span class="tag tag--r">Sunset</span>
    <input type="range" min="0" max="100" value="50" aria-label="Compare sunrise and sunset">
  </div>
</div></section>

<section class="sec"><div class="wrap split split--top">
  <div class="sticky rv"><h2>The <span class="grad grad--anthi">route.</span></h2>
    <p class="lede">Every tour starts and ends at Rajiv Boat Jetty. The Half Day and Full Day tours go further, to the villages, canals and paddy fields.</p>
    <div class="photo rv">{img("shikara-sunset-bow", sizes="(max-width:900px) 100vw, 560px")}</div></div>
  {route_block(TOUR["sunrise-cruise"])}
</div></section>

<section class="sec band band--soft"><div class="wrap">
  <div class="head"><h2 class="rv">On <span class="grad grad--kayal">board.</span></h2><a class="link" href="gallery.html">Gallery {ARROW}</a></div>
  <div class="bento">
    <figure class="b1 rv">{img("guests-bow", sizes="(max-width:760px) 100vw, 50vw", pos="50% 35%")}</figure>
    <figure class="b2 rv">{img("deck-sofa", sizes="(max-width:760px) 50vw, 25vw")}</figure>
    <figure class="b3 rv">{img("chairs-green", sizes="(max-width:760px) 50vw, 25vw")}</figure>
    <figure class="b4 rv">{img("shikara-kalyani", sizes="(max-width:760px) 50vw, 25vw", pos="50% 62%")}</figure>
    <figure class="b5 rv">{img("deck-yellow", sizes="(max-width:760px) 50vw, 25vw")}</figure>
  </div>
</div></section>

<section class="sec" id="kayaking"><div class="wrap">
  <div class="kayak rv">
    <div class="kayak__text"><h2>Kayaking <span class="grad grad--white">too.</span></h2><p>Message us for kayaking timings and rates.</p>
      <div class="acts">{wa("Hi Kalyani Boat Service! I'd like to know kayaking timings and rates.", "Ask about kayaking", "btn btn--white")}<a class="btn btn--glass" href="kayaking.html"><span>See photos</span>{ARROW}</a></div></div>
    <div class="kayak__pics">{img("kayak-sunset-solo", sizes="300px")}{img("kayak-trees", sizes="300px")}{img("kayak-rainbow", sizes="300px")}</div>
  </div>
</div></section>

<section class="sec band band--soft" id="book"><div class="wrap split split--top">
  <div class="rv"><h2>Price for <span class="grad grad--anthi">your group.</span></h2><p class="lede">Each price is for two guests. Extra guests pay per hour: ₹100 on three-hour tours, ₹150 on the Half Day and Full Day.</p>{faq(PRICE_FAQ)}</div>
  {booking()}
</div></section>
''' + extra
    return page("index.html", "Kalyani Boat Service | Shikara Tours & Kayaking in Alleppey",
                "Shikara tours from Rajiv Boat Jetty, Alleppey: Sunrise Cruise ₹1,500, Breakfast Cruise ₹1,800, Half Day ₹2,300, Full Day ₹4,600, Sunset Cruise ₹1,600, for two. Kayaking too.",
                body, "index.html", '<script src="assets/js/hero.js?v=13" defer></script>', BUSINESS)


def tours_page():
    rows = "".join(f'''<a class="trow rv" href="{t["slug"]}.html"><span class="trow__img">{img(t["img"], sizes="120px")}</span>
  <span class="trow__main"><b>{t["name"]}</b><span class="mut">{t["time"]} · {t["hours"]} hours · {escape(", ".join(t["includes"]))}</span></span>
  <span class="trow__price"><b>{inr(t["price"])}</b><span class="mut">for two</span></span><span class="go" aria-hidden="true">{ARROW}</span></a>''' for t in TOURS)
    body = f'''<section class="phead"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / Tours</p>
  <h1 class="rv">Shikara <span class="grad grad--kayal">tours.</span></h1><p class="lede rv">Seven tours from Rajiv Boat Jetty. Prices are for two guests.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="trows">{rows}</div></div></section>
<section class="sec band band--soft" id="book"><div class="wrap split split--top">
  <div class="rv"><h2>Price for <span class="grad grad--anthi">your group.</span></h2><p class="lede">Extra guests pay per hour: ₹100 on three-hour tours, ₹150 on the Half Day and Full Day.</p>{faq(PRICE_FAQ)}</div>
  {booking()}
</div></section>'''
    schema = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f'{SITE["url"]}/{t["slug"]}.html', "name": t["name"]} for i, t in enumerate(TOURS)]}
    return page("tours.html", "Shikara Tours, Timings & Prices | Kalyani Boat Service, Alleppey",
                "Kalyani shikara tours from Rajiv Boat Jetty with timings and prices for two: Sunrise ₹1,500, Half Day ₹2,300, Full Day ₹4,600, Breakfast ₹1,800, Lunch ₹1,800, Sunset ₹1,600, Regular ₹1,500.",
                body, "tours.html", schema=schema)


def tour_page(t):
    other = [o for o in TOURS if o is not t][:3]
    inc = "".join(f"<li>{escape(i)}</li>" for i in t["includes"])
    _, extra = ROUTES[t["route"]]
    route_note = "Highlighted stops are added on this tour." if extra else "The classic route, from Rajiv Boat Jetty and back."
    qas = [
        ("Where do we board?", f"At {SITE['jetty']}. The tour ends there too."),
        ("How much for more than two guests?", f"{inr(t['price'])} covers two guests. Each extra guest adds ₹{t['extra']} per hour, which is ₹{t['extra'] * t['hours']} per person on this {t['hours']}-hour tour."),
        ("How do we book?", "Send us your date and number of guests on WhatsApp, by phone or with the form below. We confirm availability."),
    ]
    body = f'''<section class="thero"><div class="wrap thero__grid">
  <div class="thero__text"><p class="crumbs"><a href="index.html">Home</a> / <a href="tours.html">Tours</a> / {t["name"]}</p>{chip(t)}
    <h1 class="rv">{t["name"]}</h1><p class="lede rv">{escape(t["lead"])}</p>
    <div class="facts rv"><div><span class="mut">Time</span><b>{t["time"]}</b></div><div><span class="mut">Duration</span><b>{t["hours"]} hours</b></div><div><span class="mut">Price for two</span><b class="price">{inr(t["price"])}</b></div><div><span class="mut">Extra guest</span><b>₹{t["extra"]} / hour</b></div></div>
    <div class="acts rv">{wa(f"Hi Kalyani Boat Service! I'd like to book the {t['name']} ({t['time']}).", "Book on WhatsApp", "btn btn--coral btn--lg")}<a class="btn btn--ghost btn--lg" href="#book"><span>Price for your group</span></a></div></div>
  <div class="thero__img rv">{img(t["img"], sizes="(max-width:900px) 100vw, 640px", eager=True)}</div>
</div></section>

<section class="sec"><div class="wrap split split--top">
  <div class="rv"><h2>The <span class="grad grad--anthi">route.</span></h2><p class="lede">{route_note}</p>
    <h3 style="margin-top:36px">Included</h3><ul class="ticks">{inc}</ul></div>
  {route_block(t)}
</div></section>

<section class="sec band band--soft" id="book"><div class="wrap split split--top">
  <div class="rv"><h2>Book this <span class="grad grad--anthi">tour.</span></h2>{faq(qas)}</div>
  {booking(t["slug"])}
</div></section>

<section class="sec"><div class="wrap">
  <div class="head"><h2 class="rv">More <span class="grad grad--kayal">tours.</span></h2><a class="link" href="tours.html">All tours {ARROW}</a></div>
  <div class="rail">{"".join(card(o) for o in other)}</div>
</div></section>'''
    schema = [
        {"@context": "https://schema.org", "@type": "TouristTrip", "name": t["name"], "description": t["lead"], "touristType": "Backwater cruise",
         "provider": {"@type": "LocalBusiness", "name": SITE["name"], "telephone": SITE["phones"][0]},
         "itinerary": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s} for i, s in enumerate(ROUTES[t["route"]][0])]},
         "offers": {"@type": "Offer", "price": t["price"], "priceCurrency": "INR", "description": "Price for two guests", "url": f'{SITE["url"]}/{t["slug"]}.html'}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]},
    ]
    return page(f'{t["slug"]}.html', f'{t["title"]} | {inr(t["price"])} for two | Kalyani',
                f'{t["name"]} from Rajiv Boat Jetty, Alleppey: {t["time"]}, {t["hours"]} hours, {inr(t["price"])} for two. {", ".join(t["includes"])}.',
                body, "tours.html", schema=schema)


def kayaking():
    photos = "".join(f'<figure class="rv">{img(n, sizes="(max-width:700px) 100vw, 420px")}</figure>' for n in ["kayak-sunset-group", "kayak-trees", "kayak-sunset-solo", "kayak-rainbow", "kayak-canal", "kayak-sunrise-group"])
    body = f'''<section class="phead"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / Kayaking</p>
  <h1 class="rv">Kayaking <span class="grad grad--kayal">in Alleppey.</span></h1><p class="lede rv">Message us for kayaking timings and rates.</p>
  <div class="acts rv">{wa("Hi Kalyani Boat Service! I'd like to know kayaking timings and rates.", "Ask on WhatsApp", "btn btn--coral btn--lg")}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="masonry">{photos}</div></div></section>'''
    return page("kayaking.html", "Kayaking in Alleppey | Kalyani Boat Service",
                "Kayaking with Kalyani Boat Service in Alleppey. Message us on WhatsApp for timings and rates.", body, "kayaking.html", schema=BUSINESS)


def gallery():
    order = ["shikara-sunset-bow", "kayak-sunset-group", "guests-bow", "kayak-trees", "deck-sofa", "kayak-rainbow", "shikara-kalyani",
             "kayak-sunset-solo", "chairs-green", "deck-front", "kayak-canal", "deck-yellow", "chairs-pink", "kayak-sunrise-group", "deck-pink"]
    figs = "".join(f'<figure class="rv">{img(n, sizes="(max-width:700px) 100vw, 420px")}</figure>' for n in order)
    body = f'''<section class="phead"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / Gallery</p>
  <h1 class="rv">Gallery<span class="grad grad--anthi">.</span></h1></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="masonry">{figs}</div></div></section>'''
    return page("gallery.html", "Gallery | Kalyani Boat Service, Alleppey", "Photos of Kalyani shikaras and kayaking in Alleppey.", body, "gallery.html")


def contact():
    phones = "".join(f'<a class="cline" href="tel:{p.replace(" ", "")}"><span class="mut">Phone / WhatsApp</span><b>{p}</b></a>' for p in SITE["phones"])
    body = f'''<section class="phead"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / Contact</p>
  <h1 class="rv">Get in <span class="grad grad--anthi">touch.</span></h1></div></section>
<section class="sec" style="padding-top:0"><div class="wrap split split--top">
  <div class="clines rv">{phones}<a class="cline" href="mailto:{SITE["email"]}"><span class="mut">Email</span><b>{SITE["email"]}</b></a><a class="cline" href="{SITE["maps"]}" target="_blank" rel="noopener"><span class="mut">Boarding point</span><b>{SITE["jetty"]}</b></a></div>
  {booking(heading="Send a booking request")}
</div></section>'''
    return page("contact.html", "Contact & Book | Kalyani Boat Service, Alleppey",
                "Book a shikara tour in Alleppey. Call or WhatsApp +91 98473 86262 or +91 97477 98412.", body, "contact.html", schema=BUSINESS)


def simple(path, title, desc, h1, html, noindex=False, base=False):
    body = f'''<section class="phead"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / {h1}</p><h1>{h1}</h1></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="prose">{html}</div></div></section>'''
    return page(path, title, desc, body, noindex=noindex, base=base)


TERMS = f'''<h2>Prices</h2><ul><li>Each tour price is for two guests.</li><li>Each extra guest is charged per hour: ₹100 per hour on three-hour tours and ₹150 per hour on the Half Day and Full Day tours.</li><li>Prices are in Indian Rupees.</li></ul>
<h2>Booking</h2><ul><li>A booking is confirmed when we confirm it to you on WhatsApp or by phone.</li><li>Payment and cancellation terms are shared when we confirm your booking.</li></ul>
<h2>Boarding</h2><ul><li>All tours start and end at {SITE["jetty"]}.</li></ul>
<p>Questions? Call {SITE["phones"][0]} or message us on WhatsApp.</p>'''

PRIVACY = f'''<h2>What we receive</h2><p>When you send a booking request we receive your name, phone number, optional email, tour, date, number of guests and any note you add.</p>
<h2>How we use it</h2><p>Only to reply to you and arrange your booking. Requests sent by email arrive at {SITE["email"]}. Messages sent on WhatsApp are handled by WhatsApp.</p>
<h2>Cookies</h2><p>This website does not use tracking or advertising cookies.</p>'''


def build():
    for old in ["hours.html", "the-boat.html", "kayak.html", "book.html", "shikara-tours.html", "about.html"]:
        (OUT / old).unlink(missing_ok=True)
    pages = {
        "index.html": home(), "tours.html": tours_page(), "kayaking.html": kayaking(), "gallery.html": gallery(), "contact.html": contact(),
        "terms.html": simple("terms.html", "Booking Terms | Kalyani Boat Service", "Booking terms for Kalyani Boat Service, Alleppey.", "Booking terms", TERMS),
        "privacy.html": simple("privacy.html", "Privacy | Kalyani Boat Service", "How Kalyani Boat Service handles booking details.", "Privacy", PRIVACY),
        "thank-you.html": simple("thank-you.html", "Request sent | Kalyani Boat Service", "Your booking request has been sent.", "Request sent",
                                 f'<p class="lede">We received your booking request and will confirm on WhatsApp or by phone.</p><div class="acts">{wa("Hi Kalyani Boat Service! I just sent a booking request on your website.", "Message us on WhatsApp")}<a class="btn btn--ghost" href="index.html"><span>Back to home</span></a></div>', noindex=True),
        "404.html": simple("404.html", "Page not found | Kalyani Boat Service", "This page could not be found.", "Page not found",
                           '<p class="lede">This page does not exist.</p><div class="acts"><a class="btn btn--coral" href="tours.html"><span>See tours</span></a><a class="btn btn--ghost" href="index.html"><span>Home</span></a></div>', noindex=True, base=True),
    }
    for t in TOURS:
        pages[f'{t["slug"]}.html'] = tour_page(t)
    for name, html in pages.items():
        (OUT / name).write_text(html, encoding="utf-8")

    data = {"whatsapp": SITE["whatsapp"], "tours": [{k: t[k] for k in ("slug", "name", "start", "end", "hours", "price", "extra", "time")} for t in TOURS]}
    (OUT / "assets/js/data.js").write_text("/* generated by build/build.py */\nwindow.KALYANI=" + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    (OUT / "assets/js/tours.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    urls = [p for p in pages if p not in ("404.html", "thank-you.html")]
    sm = "".join(f'<url><loc>{SITE["url"]}/{"" if p == "index.html" else p}</loc></url>' for p in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(pages)} pages into {OUT}")


# ---------------------------------------------------------------- single-page version (site-single/)
OUT_SINGLE = ROOT / "site-single"


def single_page():
    """The same homepage as one self-contained page: every link to another page becomes a jump within the page."""
    order = ["shikara-sunset-bow", "kayak-sunset-group", "guests-bow", "kayak-trees", "deck-sofa", "kayak-rainbow", "shikara-kalyani",
             "kayak-sunset-solo", "chairs-green", "deck-front", "kayak-canal", "deck-yellow", "chairs-pink", "kayak-sunrise-group", "deck-pink"]
    figs = "".join(f'<figure class="rv">{img(n, sizes="(max-width:700px) 100vw, 420px")}</figure>' for n in order[:9])
    phones = "".join(f'<a class="cline" href="tel:{p.replace(" ", "")}"><span class="mut">Phone / WhatsApp</span><b>{p}</b></a>' for p in SITE["phones"])
    extra = f"""
<section class="sec" id="gallery"><div class="wrap">
  <div class="head"><h2 class="rv">Gallery<span class="grad grad--anthi">.</span></h2></div>
  <div class="masonry">{figs}</div>
</div></section>

<section class="sec band band--soft" id="contact"><div class="wrap split split--top">
  <div class="rv"><h2>Get in <span class="grad grad--anthi">touch.</span></h2><p class="lede">Call or message us to book, or use the booking form above.</p></div>
  <div class="clines rv">{phones}<a class="cline" href="mailto:{SITE["email"]}"><span class="mut">Email</span><b>{SITE["email"]}</b></a><a class="cline" href="{SITE["maps"]}" target="_blank" rel="noopener"><span class="mut">Boarding point</span><b>{SITE["jetty"]}</b></a></div>
</div></section>

<section class="sec" id="legal" style="padding-top:0"><div class="wrap"><div class="faq">
  <details><summary>Booking terms</summary><div class="prose" style="margin-top:12px">{TERMS}</div></details>
  <details><summary>Privacy</summary><div class="prose" style="margin-top:12px">{PRIVACY}</div></details>
</div></div></section>
"""
    html = home(extra)
    html = html.replace('href="kayaking.html"><span>See photos', 'href="#gallery"><span>See photos')
    html = html.replace(f'<a class="link" href="tours.html">All tours {ARROW}</a>', "")
    for a, b in [('href="tours.html"', 'href="#tours"'), ('href="kayaking.html"', 'href="#kayaking"'), ('href="gallery.html"', 'href="#gallery"'),
                 ('href="contact.html"', 'href="#contact"'), ('href="terms.html"', 'href="#legal"'), ('href="privacy.html"', 'href="#legal"'),
                 ('href="index.html"', 'href="#main"'), ('assets/js/data.js?v=', 'assets/js/data-single.js?v=')]:
        html = html.replace(a, b)
    for t in TOURS:
        html = html.replace(f'href="{t["slug"]}.html"', f'href="#book" data-pick="{t["slug"]}"')
    return html


def build_single():
    import shutil
    if OUT_SINGLE.exists():
        shutil.rmtree(OUT_SINGLE)
    shutil.copytree(OUT / "assets", OUT_SINGLE / "assets")
    shutil.copy(OUT / "favicon.svg", OUT_SINGLE / "favicon.svg")
    (OUT_SINGLE / "index.html").write_text(single_page(), encoding="utf-8")
    data = {"single": True, "whatsapp": SITE["whatsapp"], "tours": [{k: t[k] for k in ("slug", "name", "start", "end", "hours", "price", "extra", "time")} for t in TOURS]}
    (OUT_SINGLE / "assets/js/data-single.js").write_text("/* generated by build/build.py */\nwindow.KALYANI=" + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    (OUT_SINGLE / "assets/js/data.js").unlink(missing_ok=True)
    php = (OUT / "enquiry.php").read_text(encoding="utf-8").replace("'thank-you.html'", "'index.html?sent=1#book'").replace("contact.html?error=1", "index.html?error=1#book").replace("Location: contact.html", "Location: index.html")
    (OUT_SINGLE / "enquiry.php").write_text(php, encoding="utf-8")
    ht = (OUT / ".htaccess").read_text(encoding="utf-8").replace("ErrorDocument 404 /404.html", "ErrorDocument 404 /index.html")
    (OUT_SINGLE / ".htaccess").write_text(ht, encoding="utf-8")
    (OUT_SINGLE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n", encoding="utf-8")
    print(f"Built single page into {OUT_SINGLE}")


if __name__ == "__main__":
    build()
    build_single()
