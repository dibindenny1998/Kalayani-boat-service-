"""Generate the Kalyani Boat Service website into site/.

Edit the details below (contacts, tours, prices), then run:
    python3 build/build.py
and upload the contents of site/ to public_html on Hostinger.
Needs Python 3.8+ and Pillow (for image sizes): pip install pillow
"""
import json
from html import escape
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"

# ---------------------------------------------------------------- business details
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
         "Snake Boat Race finishing point", "Vembanad Lake", "SAI (Sports Authority of India) centre", "C Block"]
END = ["Vilakkumaram", "Back to Rajiv Boat Jetty"]
VILLAGES = ["Kainakary", "Chavara Bhavan", "Vattakayal", "Pallathurthi"]
FARMS = ["Narrow canals", "Paddy fields farmed below sea level", "Temples", "Duck farming", "Fish hatchery"]
ROUTES = {
    "base": (START + END, []),
    "half": (START + VILLAGES + END, VILLAGES),
    "full": (START + FARMS + VILLAGES + END, FARMS + VILLAGES),
}

# ---------------------------------------------------------------- tours
# start/end are hours (15.5 = 3:30 pm); price is for two guests; extra is per extra guest per hour.
TOURS = [
    dict(slug="sunrise-cruise", name="Sunrise Cruise", start=6, end=9, hours=3, price=1500, extra=100,
         sky="pulari", img="deck-front", route="base",
         includes=["Morning tea or coffee"],
         lead="Leave Rajiv Boat Jetty at 6 am and watch the sun come up over Vembanad Lake, past the Snake Boat Race track and the quiet village banks.",
         title="Sunrise Shikara Cruise in Alleppey"),
    dict(slug="half-day-tour", name="Half Day Tour with Breakfast", start=8, end=12, hours=4, price=2300, extra=150,
         sky="pakal", img="shikara-kalyani", route="half",
         includes=["Kerala breakfast", "Tea or coffee"],
         lead="Four hours on the backwaters with a Kerala breakfast on board, going further out to Kainakary, Chavara Bhavan, Vattakayal and Pallathurthi.",
         title="Half Day Shikara Tour with Breakfast"),
    dict(slug="full-day-tour", name="Full Day Tour with Breakfast & Lunch", start=8, end=16, hours=8, price=4600, extra=150,
         sky="pakal", img="chairs-pink", route="full",
         includes=["Kerala breakfast", "Lunch, veg or non-veg", "Tea or coffee"],
         lead="A full day through narrow canals, paddy fields below sea level, temples, duck farms and village life, with breakfast and lunch on board.",
         title="Full Day Shikara Tour with Breakfast & Lunch"),
    dict(slug="breakfast-cruise", name="Breakfast Cruise", start=9, end=12, hours=3, price=1800, extra=100,
         sky="pakal", img="deck-sofa", route="base",
         includes=["Kerala breakfast", "Tea or coffee"],
         lead="A relaxed morning cruise from 9 am to noon with a Kerala breakfast served on the shikara deck.",
         title="Breakfast Shikara Cruise in Alleppey"),
    dict(slug="lunch-cruise", name="Lunch Cruise", start=13, end=16, hours=3, price=1800, extra=100,
         sky="pakal", img="chairs-green", route="base",
         includes=["Tea or coffee"],
         lead="An afternoon cruise from 1 pm to 4 pm across Vembanad Lake and past the Snake Boat Race track.",
         title="Afternoon Lunch Cruise by Shikara"),
    dict(slug="sunset-cruise", name="Sunset Cruise", start=15.5, end=18.5, hours=3, price=1600, extra=100,
         sky="anthi", img="shikara-sunset-bow", route="base",
         includes=["Tea or coffee with snacks"],
         lead="Set out at 3:30 pm and watch the sun go down over Vembanad Lake, with evening tea and snacks on board.",
         title="Sunset Shikara Cruise on Vembanad Lake"),
    dict(slug="regular-cruise", name="Regular Cruise", start=None, end=None, hours=3, price=1500, extra=100,
         sky="kayal", img="guests-bow", route="base",
         includes=["Tea or coffee with snacks"],
         lead="Pick any three hours that suit you. Same route as our classic cruise, at the time you choose.",
         title="3-Hour Shikara Cruise at Your Own Time"),
]


def clock(h):
    hh, mm = int(h), int(round((h - int(h)) * 60))
    ap = "am" if hh < 12 else "pm"
    return f"{(hh - 1) % 12 + 1}:{mm:02d} {ap}"


for t in TOURS:
    t["time"] = f"{clock(t['start'])} – {clock(t['end'])}" if t["start"] is not None else "Any 3 hours"
    t["hhmm"] = f"{int(t['start']):02d}:{int(round((t['start'] % 1) * 60)):02d}" if t["start"] is not None else "Any"
TOUR = {t["slug"]: t for t in TOURS}


def inr(v):
    s = str(v)
    return "₹" + (s[:-3] + "," + s[-3:] if len(s) > 3 else s)


# ---------------------------------------------------------------- photos
CAPTIONS = {
    "shikara-sunset-bow": "Sunset through the bow of a Kalyani shikara",
    "shikara-kalyani": "The Kalyani shikara moored at the jetty",
    "deck-sofa": "Cushioned front deck under the coir canopy",
    "deck-front": "Looking out from the shikara deck onto the backwater",
    "deck-yellow": "The open front deck, ready for guests",
    "chairs-green": "Cane chairs under the canopy",
    "guests-bow": "Guests relaxing on the front deck",
    "deck-pink": "The shikara deck and canopy",
    "chairs-pink": "Seating for groups on board",
    "kayak-rainbow": "Kayaking under a rainbow",
    "kayak-sunset-solo": "Sunset kayaking on Vembanad Lake",
    "kayak-canal": "Paddling into the village canals",
    "kayak-sunrise-group": "A group of kayakers at sunrise",
    "kayak-sunset-group": "Kayaks heading into the sunset",
    "kayak-trees": "Kayaking under the trees in a narrow canal",
}
DIMS = {}
for f in (OUT / "assets/img").glob("*-lg.webp"):
    DIMS[f.name[:-8]] = Image.open(f).size


def img(name, alt=None, cls="", sizes="(max-width: 820px) 100vw, 50vw", eager=False, pos=None):
    w, h = DIMS[name]
    style = f' style="object-position:{pos}"' if pos else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="assets/img/{name}-lg.webp" srcset="assets/img/{name}-sm.webp 640w, assets/img/{name}-lg.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{escape(alt or CAPTIONS[name])}" {load}{style}>')


def fig(name, cls="", alt=None, sizes="(max-width: 820px) 100vw, 50vw", eager=False, pos=None):
    return f'<figure class="ph {cls}">{img(name, alt, sizes=sizes, eager=eager, pos=pos)}</figure>'


# ---------------------------------------------------------------- shared pieces
WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s1 2.6 1.1 2.7c.1.2 1.9 2.9 4.6 4 1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
WAVES = '<svg class="waves" viewBox="0 0 1200 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 50Q150 10 300 50T600 50T900 50T1200 50"/><path d="M0 90Q150 50 300 90T600 90T900 90T1200 90"/></svg>'
SKY_COLOR = {"pulari": "#FF7A59", "pakal": "#0FA3A3", "anthi": "#FF4E6A", "kayal": "#2FA35A"}

NAV = [("index.html", "Home"), ("shikara-tours.html", "Shikara tours"), ("kayaking.html", "Kayaking"),
       ("gallery.html", "Gallery"), ("about.html", "About"), ("contact.html", "Contact")]


def wa(msg, label="Book on WhatsApp", cls="btn btn--coral"):
    return f'<a class="{cls}" href="contact.html" data-wa="{escape(msg)}">{WA_ICON}{label}</a>'


def header(current):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == current else ""}>{n}</a>' for h, n in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
  <a class="logo" href="index.html" aria-label="Kalyani Boat Service, home">Kalyani <em>Boat Service</em></a>
  <button class="menu" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Main">{links}{wa("Hi Kalyani Boat Service! I'd like to book a shikara ride.", "Book a ride", "btn btn--dark btn--sm")}</nav>
</div></header>'''


def footer():
    tours = "".join(f'<li><a href="{t["slug"]}.html">{t["name"]}</a></li>' for t in TOURS)
    phones = "".join(f'<li><a href="tel:{p.replace(" ", "")}">{p}</a></li>' for p in SITE["phones"])
    return f'''<footer class="foot"><div class="wrap">
  <div class="big">Kalyani <em>on the water.</em></div>
  <div class="grid">
    <div style="display:grid;gap:16px;align-content:start">
      <p style="max-width:34ch">Shikara cruises and kayaking on the Alleppey backwaters, from sunrise to sunset. Every tour starts at {SITE["jetty"]}.</p>
      <div class="btns">{wa("Hi Kalyani Boat Service! I'd like to book a shikara ride.", "Chat on WhatsApp", "btn btn--mango btn--sm")}</div>
    </div>
    <div><h4>Shikara tours</h4><ul>{tours}</ul></div>
    <div><h4>Explore</h4><ul><li><a href="kayaking.html">Kayaking</a></li><li><a href="gallery.html">Gallery</a></li><li><a href="about.html">About us</a></li><li><a href="contact.html">Contact &amp; booking</a></li><li><a href="terms.html">Booking terms</a></li><li><a href="privacy.html">Privacy</a></li></ul></div>
    <div><h4>Contact</h4><ul>{phones}<li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li><li><a href="{SITE["maps"]}" target="_blank" rel="noopener">{SITE["jetty"]}</a></li></ul></div>
  </div>
  <div class="base"><span>© <span id="year">2026</span> Kalyani Boat Service, Alleppey</span><span lang="ml" class="ml">കല്യാണി</span></div>
</div></footer>
<a class="wa" href="contact.html" data-wa="Hi Kalyani Boat Service! I have a question about your boat tours.">{WA_ICON}<span>Chat on WhatsApp</span></a>'''


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
<meta name="theme-color" content="#0FA3A3">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Figtree:wght@400;500;600;700&family=Instrument+Serif:ital@1&family=Manjari:wght@400;700&display=swap">
<link rel="stylesheet" href="assets/css/style.css?v=2">
{ld}
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="assets/js/data.js?v=2"></script>
<script src="assets/js/main.js?v=2" defer></script>
{scripts}
</body>
</html>
'''


def chip(t):
    return f'<span class="tchip {t["sky"]}">{t["time"]} · {t["hours"]} hrs</span>'


def card(t):
    return f'''<a class="card rv" href="{t["slug"]}.html">
  {fig(t["img"], sizes="(max-width: 700px) 100vw, 400px")}
  <div class="body">{chip(t)}<h3>{t["name"]}</h3><p class="mut">{escape(t["lead"])}</p>
  <div class="row"><span><span class="amt">{inr(t["price"])}</span> <span class="per">for two</span></span><span class="go" aria-hidden="true">→</span></div></div>
</a>'''


def slots():
    out = ""
    for t in TOURS:
        out += f'''<a class="slot" href="{t["slug"]}.html" style="--sc:{SKY_COLOR[t["sky"]]}">
  {fig(t["img"], sizes="360px")}<span class="sky" style="background:var(--{t["sky"]})"></span>
  <time>{t["hhmm"]}</time><h3>{t["name"]}</h3><p>{t["time"]} · {escape(", ".join(t["includes"]))}</p>
  <p class="price"><b>{inr(t["price"])}</b> for two</p></a>'''
    return f'<div class="day__scroller"><div class="day__track" id="track">{out}</div></div>'


def route_list(t):
    stops, extra = ROUTES[t["route"]]
    lis = "".join(f'<li class="{"extra" if s in extra else ""}">{escape(s)}{"<small>Added on this tour</small>" if s in extra else ""}</li>' for s in stops)
    return f'<ol class="route">{lis}</ol>'


def enquiry(selected="sunrise-cruise", heading="Check the price and book"):
    opts = "".join(f'<option value="{t["slug"]}"{" selected" if t["slug"] == selected else ""}>{t["name"]} · {t["time"]}</option>' for t in TOURS)
    return f'''<form class="calc rv" data-calc data-email action="enquiry.php" method="post">
  <div><div class="eyebrow">Price &amp; booking</div><h3>{heading}</h3></div>
  <label class="field"><span>Tour</span><select name="tour">{opts}</select></label>
  <div class="fields">
    <label class="field"><span>Date</span><input type="date" name="date" required></label>
    <div class="field"><span id="g-label">Guests</span>
      <div class="step" role="group" aria-labelledby="g-label"><button type="button" data-step="-1" aria-label="Fewer guests">−</button><output aria-live="polite">2</output><button type="button" data-step="1" aria-label="More guests">+</button></div>
      <input type="hidden" name="guests" value="2">
    </div>
  </div>
  <div class="total"><span class="sum">{inr(TOUR[selected]["price"])}</span><p class="sumnote">Base price, covers up to two guests</p></div>
  <div class="fields">
    <label class="field"><span>Your name</span><input name="name" autocomplete="name" required></label>
    <label class="field"><span>Phone or WhatsApp</span><input name="phone" type="tel" autocomplete="tel" required></label>
  </div>
  <label class="field"><span>Email (optional)</span><input name="email" type="email" autocomplete="email"></label>
  <label class="field"><span>Preferred start time or a note (optional)</span><textarea name="message" placeholder="For the Regular Cruise, tell us the start time you'd like."></textarea></label>
  <label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>
  <input type="hidden" name="started" value="">
  <div class="btns"><button type="button" class="btn btn--coral" data-send="wa">{WA_ICON}Send on WhatsApp</button><button type="submit" class="btn btn--ghost">Send by email</button></div>
  <p class="status" role="status" hidden></p>
  <p class="per">We confirm every booking personally on WhatsApp or by phone.</p>
</form>'''


def glow(kind, h2, p, buttons, pics=None, extra=""):
    right = (f'<div class="pics">{fig(pics[0], "p1", sizes="420px")}{fig(pics[1], "p2", sizes="320px")}</div>' if pics else extra)
    return f'''<section class="glow glow--{kind} rv">{WAVES}<div class="wrap inner">
  <div style="display:grid;gap:22px;justify-items:start"><h2>{h2}</h2><p class="lead">{p}</p><div class="btns">{buttons}</div></div>
  {right}
</div></section>'''


def phero(img_name, crumbs, h1, lead, buttons="", top="", sticker="", pos=None):
    return f'''<section class="phero"><div class="stage">
  {img(img_name, sizes="100vw", eager=True, pos=pos)}<div class="stage__shade"></div>{sticker}
  <div class="txt wrap"><p class="crumbs">{crumbs}</p>{top}<h1>{h1}</h1><p class="lead">{lead}</p>{f'<div class="btns">{buttons}</div>' if buttons else ""}</div>
</div></section>'''


def final(h2, p, buttons, photo="shikara-sunset-bow"):
    return f'''<section class="final rv">{img(photo, sizes="100vw")}<div class="wrap"><h2>{h2}</h2><p class="lead" style="color:#fff">{p}</p><div class="btns">{buttons}</div></div></section>'''


BUSINESS = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "name": SITE["name"], "url": SITE["url"],
    "image": SITE["url"] + "/assets/img/og-image.jpg", "telephone": SITE["phones"][0], "email": SITE["email"],
    "priceRange": f"{inr(min(t['price'] for t in TOURS))} – {inr(max(t['price'] for t in TOURS))}",
    "address": {"@type": "PostalAddress", "streetAddress": "Rajiv Boat Jetty", "addressLocality": "Alappuzha",
                "addressRegion": "Kerala", "addressCountry": "IN"},
}
BOOK = "Hi Kalyani Boat Service! I'd like to book a shikara ride."


# ---------------------------------------------------------------- pages
def home():
    marquee = "".join(f"<span>{s}</span>" for s in ["Sunrise cruise", "Kerala breakfast on board", "Snake Boat Race track", "Vembanad Lake", "Village canals", "Kayaking", "Sunset cruise"] * 2)
    body = f'''<section class="hero" aria-label="Introduction">
  <div class="stage" id="stage">
    <canvas id="sky" aria-hidden="true"></canvas>
    <div class="stage__shade"></div>
    <div class="birds" aria-hidden="true"><svg class="bird b1" viewBox="0 0 40 16"><path d="M2 10 Q11 0 20 9 Q29 0 38 10"/></svg><svg class="bird b2" viewBox="0 0 40 16"><path d="M2 10 Q11 0 20 9 Q29 0 38 10"/></svg><svg class="bird b3" viewBox="0 0 40 16"><path d="M2 10 Q11 0 20 9 Q29 0 38 10"/></svg></div>
    <div class="hero__content wrap">
      <div class="hero__text">
        <div class="chip"><span class="dot"></span>Shikara · Kayaking · Rajiv Boat Jetty, Alleppey</div>
        <h1><span class="line">Alleppey from</span><span class="line">the water, <span class="rotator" id="rotator"><span>at sunrise</span></span></span><span class="line"><em class="serif">on a Kalyani shikara.</em></span></h1>
        <p class="hero__lead">Seven shikara tours from first light to sunset, across Vembanad Lake, past the Snake Boat Race track and into the village canals. From {inr(1500)} for two.</p>
        <div class="btns"><a class="btn btn--coral" href="shikara-tours.html">See shikara tours</a>{wa(BOOK, "Book on WhatsApp", "btn btn--light")}</div>
        <div class="player" id="player">
      <button type="button" id="playbtn" aria-label="Pause the day">❚❚</button>
      <span class="clock" id="clock">06:00</span>
      <span class="what" id="now">Sunrise Cruise on the water</span>
      <button type="button" class="live" id="livebtn">Now in Alleppey</button>
      <input type="range" id="hour" min="5" max="19.6" step="0.01" value="6" aria-label="Time of day on the water">
        </div>
      </div>
      <div class="hero__floats" aria-hidden="true">
        {fig("shikara-sunset-bow", "float float--a")}
        {fig("guests-bow", "float float--b")}
        <div class="badge"><b>From {inr(1500)}</b><span>for two, tea on board</span></div>
      </div>
    </div>
    <a class="spinner" href="#day" aria-label="See the tours of the day"><svg viewBox="0 0 120 120" aria-hidden="true"><defs><path id="circ" d="M60 60 m-46 0 a46 46 0 1 1 92 0 a46 46 0 1 1 -92 0"/></defs><text><textPath href="#circ">SHIKARA ✿ KAYAKING ✿ ALLEPPEY ✿ SUNRISE TO SUNSET ✿ </textPath></text></svg><span class="spinner__arrow">↓</span></a>
  </div>
  <div class="rates wrap">
    <a class="rate rate--coral" href="sunrise-cruise.html"><span>Sunrise cruise</span><b>{inr(1500)}</b><small>6:00 am · for two</small><i>→</i></a>
    <a class="rate rate--lagoon" href="full-day-tour.html"><span>Full day with lunch</span><b>{inr(4600)}</b><small>8 hours · for two</small><i>→</i></a>
    <a class="rate rate--mango" href="sunset-cruise.html"><span>Sunset cruise</span><b>{inr(1600)}</b><small>3:30 pm · for two</small><i>→</i></a>
  </div>
</section>

<div class="marquee-wrap" aria-hidden="true"><div class="marquee"><div class="marquee__track">{marquee}</div></div></div>

<section class="statement wrap" aria-label="About shikaras">
  <div class="eyebrow">Shikara: the small boat of the backwaters</div>
  <p id="scrub">A shikara sits low on the water and slips into village canals the big houseboats can't reach. You lie back on the deck and Alleppey drifts past.</p>
  <div class="story">
    <div>
      <p><b>Kalyani Boat Service</b> runs shikara cruises and kayaking from Rajiv Boat Jetty in Alappuzha. Our shikaras have a cushioned front deck, cane chairs and a woven coir canopy, and every tour passes the Snake Boat Race track before crossing Vembanad Lake.</p>
      <blockquote>“Pick your hour. The backwater looks different at every one.”</blockquote>
      <div class="btns" style="margin-top:22px"><a class="btn btn--ghost btn--sm" href="about.html">About Kalyani →</a></div>
    </div>
    <dl class="facts">
      <div class="fact fact--lagoon"><dt>Shikara tours a day</dt><dd>7</dd></div>
      <div class="fact fact--mango"><dt>First cruise leaves</dt><dd>6 am</dd></div>
      <div class="fact fact--coral"><dt>For two guests, from</dt><dd>{inr(1500)}</dd></div>
      <div class="fact fact--leaf"><dt>Boarding point</dt><dd>1 jetty</dd></div>
    </dl>
  </div>
</section>

<section class="day" id="day" aria-labelledby="day-title">
  <div class="day__intro wrap sec__head" style="margin-bottom:0"><div><div class="eyebrow">A day on the water</div><h2 id="day-title">From first light <em class="serif">to the last.</em></h2></div>
    <p>Seven tours through the day, each priced for two guests. Scroll along the day and pick your hour.</p></div>
  {slots()}
</section>

<section class="sec wrap" aria-labelledby="mo-title">
  <div class="sec__head"><div><div class="eyebrow">On board</div><h2 id="mo-title">Your seat <em class="serif">on the backwaters.</em></h2></div>
    <p>Real photos from Kalyani's shikaras and kayaking trips on Vembanad Lake.</p></div>
  <div class="mosaic">
    <figure class="ph m1 rv">{img("shikara-sunset-bow", sizes="(max-width:760px) 100vw, 50vw")}<span class="mtag">Sunset cruise</span></figure>
    <figure class="ph m2 rv">{img("chairs-green", sizes="50vw")}<span class="mtag">Cane chairs</span></figure>
    <figure class="ph m3 rv">{img("deck-sofa", sizes="33vw")}<span class="mtag">The front deck</span></figure>
    <figure class="ph m4 rv">{img("kayak-trees", sizes="17vw")}<span class="mtag">Canals</span></figure>
    <figure class="ph m5 rv">{img("kayak-sunset-group", sizes="50vw")}<span class="mtag">Kayaking</span></figure>
    <figure class="ph m6 rv">{img("guests-bow", sizes="50vw", pos="50% 35%")}<span class="mtag">Guests on board</span></figure>
  </div>
</section>

{glow("dusk", 'Snake Boat Race track <em class="serif">to Vembanad Lake.</em>', "Our classic three-hour route. The half-day and full-day tours go further, to Kainakary, Chavara Bhavan, Vattakayal, Pallathurthi and the paddy fields farmed below sea level.", '<a class="btn btn--mango" href="shikara-tours.html">Compare all tours</a>', extra=route_list(TOUR["sunrise-cruise"]))}

{glow("kayal", 'Kayaking <em class="serif">at sunrise &amp; sunset.</em>', "Small groups, single and double kayaks, guided through the canals. Message us for this week's timings and rates.", wa("Hi Kalyani Boat Service! I'd like to know about kayaking timings and rates.", "Ask about kayaking", "btn btn--light") + '<a class="btn btn--ghost" style="color:#fff" href="kayaking.html">See kayaking</a>', pics=["kayak-sunset-solo", "kayak-rainbow"])}

{final('Catch the sunset <em class="serif">on Vembanad Lake.</em>', f"The Sunset Cruise leaves Rajiv Boat Jetty at 3:30 pm with tea and snacks on board. {inr(1600)} for two.", wa("Hi Kalyani Boat Service! I'd like to book the Sunset Cruise.", "Book the Sunset Cruise", "btn btn--mango") + '<a class="btn btn--light" href="sunset-cruise.html">See details</a>')}
'''
    return page("index.html", "Kalyani Boat Service | Shikara Tours & Kayaking in Alleppey",
                "Shikara cruises and kayaking on the Alleppey backwaters, from ₹1,500 for two. Sunrise, sunset, breakfast, half-day and full-day tours from Rajiv Boat Jetty.",
                body, "index.html", '<script src="assets/js/hero.js?v=2" defer></script>', BUSINESS)


def shikara_tours():
    body = f'''{phero("shikara-kalyani", '<a href="index.html">Home</a> / Shikara tours', 'Seven ways to spend <em class="serif">a day on the water.</em>',
                 "From a 6 am sunrise to a 3:30 pm sunset cruise, every tour starts at Rajiv Boat Jetty and takes in the Snake Boat Race track and Vembanad Lake.",
                 wa("Hi Kalyani Boat Service! I'd like to book a shikara tour.") + '<a class="btn btn--light" href="#price">Check the price</a>',
                 sticker=f'<div class="sticker"><b>{inr(1500)}</b><span>from, for two</span></div>', pos="50% 62%")}

<section class="day" id="day" aria-labelledby="day-title">
  <div class="day__intro wrap sec__head" style="margin-bottom:0"><div><div class="eyebrow">Tours by time of day</div><h2 id="day-title">From first light <em class="serif">to sunset.</em></h2></div><p>Tap a tour for its route, what's included and the price for your group.</p></div>
  {slots()}
</section>

<section class="sec wrap">
  <div class="sec__head"><div><div class="eyebrow">All tours</div><h2>Choose <em class="serif">your cruise.</em></h2></div><p>Prices are for two guests. Extra guests pay ₹100 to ₹150 for each hour of the tour.</p></div>
  <div class="cards">{"".join(card(t) for t in TOURS)}</div>
</section>

<section class="sec band" id="price"><div class="wrap split">
  <div style="display:grid;gap:18px;align-content:start"><div class="eyebrow">How pricing works</div><h2>One price for two, <em class="serif">then per hour.</em></h2>
    <p class="lead">Each tour has a price for two guests. Every extra guest adds a fixed amount for each hour: ₹100 per hour on the three-hour cruises and ₹150 per hour on the half-day and full-day tours.</p>
    <p class="mut">Example: the Sunrise Cruise for four guests is {inr(1500)} + 2 × ₹100 × 3 hrs = <b>{inr(2100)}</b>.</p></div>
  {enquiry()}
</div></section>
'''
    schema = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f'{SITE["url"]}/{t["slug"]}.html', "name": t["name"]} for i, t in enumerate(TOURS)]}
    return page("shikara-tours.html", "Shikara Tours in Alleppey | Prices & Timings | Kalyani Boat Service",
                "All Kalyani shikara tours with timings and prices: Sunrise Cruise ₹1,500, Breakfast Cruise ₹1,800, Half Day ₹2,300, Full Day ₹4,600, Sunset Cruise ₹1,600 for two.",
                body, "shikara-tours.html", schema=schema)


def tour_page(t):
    others = [o for o in TOURS if o is not t][:3]
    inc = "".join(f"<li>{escape(i)}</li>" for i in t["includes"])
    when = (f"Starts at {clock(t['start'])} and returns at {clock(t['end'])}." if t["start"] is not None
            else "You choose the start time. Tell us your preferred time when you book.")
    faqs = [
        ("Where do we board the shikara?", f"All tours start and end at {SITE['jetty']}. We share the exact meeting point on WhatsApp when we confirm your booking."),
        ("How is the price worked out?", f"{inr(t['price'])} covers two guests. Each extra guest adds ₹{t['extra']} for each hour of the tour, so ₹{t['extra'] * t['hours']} per extra guest on this {t['hours']}-hour tour."),
        ("What time does the tour run?", when),
        ("How do I book?", "Send us your date and number of guests on WhatsApp or with the form on this page. We reply to confirm availability and the booking details."),
    ]
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    words = t["name"].split(" ")
    h1 = " ".join(words[:-1]) + f' <em class="serif">{words[-1]}</em>' if len(words) > 1 else t["name"]
    kind = {"pulari": "pulari", "pakal": "pakal", "anthi": "dusk", "kayal": "kayal"}[t["sky"]]
    body = f'''{phero(t["img"], f'<a href="index.html">Home</a> / <a href="shikara-tours.html">Shikara tours</a> / {t["name"]}', h1, escape(t["lead"]),
                 wa(f"Hi Kalyani Boat Service! I'd like to book the {t['name']} ({t['time']}).") + '<a class="btn btn--light" href="#price">Price for your group</a>',
                 top=chip(t), sticker=f'<div class="sticker"><b>{inr(t["price"])}</b><span>for two guests</span></div>')}

<section class="wrap"><dl class="kfacts">
  <div><dt>Time</dt><dd>{t["time"]}</dd></div><div><dt>Duration</dt><dd>{t["hours"]} hours</dd></div>
  <div><dt>Price for two</dt><dd>{inr(t["price"])}</dd></div><div><dt>Extra guest</dt><dd>₹{t["extra"]} / hr</dd></div>
</dl></section>

<section class="sec wrap split">
  <div class="rv" style="display:grid;gap:16px"><div class="eyebrow">Included</div><h2>On <em class="serif">board.</em></h2><ul class="ticks">{inc}<li>Pick up and drop at Rajiv Boat Jetty</li></ul>
    <div class="eyebrow" style="margin-top:26px">Good to know</div><ul class="ticks"><li>{when}</li><li>The price covers two guests. Extra guests are charged per hour.</li><li>Bring sunglasses, a hat and sunscreen for daytime tours.</li></ul></div>
  {fig(t["img"], "rv tilt-r", sizes="(max-width:860px) 100vw, 50vw")}
</section>

{glow(kind, 'Where <em class="serif">you\'ll go.</em>', "From Rajiv Boat Jetty and back again. Stops marked in colour are added on this tour.", wa(f"Hi Kalyani Boat Service! I'd like to book the {t['name']}.", "Book this tour", "btn btn--light"), extra=route_list(t))}

<section class="sec wrap split" id="price">
  <div style="display:grid;gap:16px;align-content:start"><div class="eyebrow">Questions</div><h2>Before <em class="serif">you go.</em></h2><div class="faq">{faq}</div></div>
  {enquiry(t["slug"], "Price for your group")}
</section>

<section class="sec band" style="padding-top:clamp(70px,9vw,120px)"><div class="wrap">
  <div class="sec__head"><div><div class="eyebrow">More tours</div><h2>You might <em class="serif">also like.</em></h2></div><a class="btn btn--ghost" href="shikara-tours.html">All shikara tours</a></div>
  <div class="cards">{"".join(card(o) for o in others)}</div>
</div></section>
'''
    schema = [
        {"@context": "https://schema.org", "@type": "TouristTrip", "name": t["name"], "description": t["lead"],
         "touristType": "Backwater cruise", "provider": {"@type": "LocalBusiness", "name": SITE["name"], "telephone": SITE["phones"][0]},
         "itinerary": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s} for i, s in enumerate(ROUTES[t["route"]][0])]},
         "offers": {"@type": "Offer", "price": t["price"], "priceCurrency": "INR", "description": "Price for two guests", "url": f'{SITE["url"]}/{t["slug"]}.html'}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    return page(f'{t["slug"]}.html', f'{t["title"]} | {inr(t["price"])} for two | Kalyani',
                f'{t["name"]} from Rajiv Boat Jetty, Alleppey: {t["time"]}, {t["hours"]} hours, {inr(t["price"])} for two. Includes {", ".join(t["includes"]).lower()}. Book on WhatsApp.',
                body, "shikara-tours.html", schema=schema)


def kayaking():
    photos = "".join(f'<figure>{fig(n, "rv", sizes="(max-width: 700px) 100vw, 400px")}<figcaption>{CAPTIONS[n]}</figcaption></figure>'
                     for n in ["kayak-trees", "kayak-sunset-solo", "kayak-rainbow", "kayak-canal", "kayak-sunrise-group"])
    body = f'''{phero("kayak-sunset-group", '<a href="index.html">Home</a> / Kayaking', 'Paddle where <em class="serif">big boats can\'t go.</em>',
                 "Kayak through the narrow village canals and out onto Vembanad Lake at sunrise or sunset. Message us for this week's timings and rates.",
                 wa("Hi Kalyani Boat Service! I'd like to know about kayaking timings and rates.", "Ask about kayaking") + '<a class="btn btn--light" href="shikara-tours.html">See shikara tours</a>',
                 sticker='<div class="sticker"><b>Sunrise</b><span>&amp; sunset sessions</span></div>')}

<section class="sec wrap">
  <div class="sec__head"><div><div class="eyebrow">On the water</div><h2>Canals, lakes <em class="serif">&amp; long light.</em></h2></div><p>Photos from Kalyani kayaking trips.</p></div>
  <div class="gal">{photos}</div>
</section>

{glow("kayal", 'Plan your <em class="serif">kayaking session.</em>', "Tell us your date, the time of day you prefer and how many people are coming. We'll reply with timings, rates and the meeting point.", wa("Hi Kalyani Boat Service! I'd like to book kayaking. Date: , People: ", "Ask on WhatsApp", "btn btn--light"), pics=["kayak-canal", "kayak-sunrise-group"])}
'''
    return page("kayaking.html", "Kayaking in Alleppey | Sunrise & Sunset Kayak Tours | Kalyani",
                "Sunrise and sunset kayaking through the Alleppey village canals and on Vembanad Lake with Kalyani Boat Service. Message us for timings and rates.",
                body, "kayaking.html", schema=BUSINESS)


def gallery():
    order = ["shikara-sunset-bow", "kayak-sunset-group", "guests-bow", "kayak-trees", "deck-sofa", "kayak-rainbow", "shikara-kalyani",
             "kayak-sunset-solo", "chairs-green", "deck-front", "kayak-canal", "deck-yellow", "chairs-pink", "kayak-sunrise-group", "deck-pink"]
    figs = "".join(f'<figure>{fig(n, "rv", sizes="(max-width: 700px) 100vw, 400px")}<figcaption>{CAPTIONS[n]}</figcaption></figure>' for n in order)
    body = f'''{phero("kayak-sunset-solo", '<a href="index.html">Home</a> / Gallery', 'Moments from <em class="serif">the backwater.</em>', "Our shikaras, our guests and the light on Vembanad Lake.", pos="50% 45%")}
<section class="sec wrap"><div class="gal">{figs}</div></section>'''
    return page("gallery.html", "Photo Gallery | Kalyani Boat Service, Alleppey",
                "Photos of Kalyani shikaras, sunset cruises and kayaking on the Alleppey backwaters and Vembanad Lake.", body, "gallery.html")


def about():
    body = f'''{phero("shikara-kalyani", '<a href="index.html">Home</a> / About', 'Kalyani <em class="serif">Boat Service.</em>',
                 "Shikara cruises and kayaking on the Alleppey backwaters, from Rajiv Boat Jetty in Alappuzha.", pos="50% 66%")}

<section class="sec wrap split">
  <div class="prose rv">
    <div class="eyebrow">Our shikaras</div><h2>Built for <em class="serif">slow afternoons.</em></h2>
    <p>A shikara is a small, covered Kerala boat built for slow cruising. Ours have a cushioned front deck for lying back and watching the water, cane chairs for groups and a woven coir canopy for shade. Life buoys are kept on board.</p>
    <h2 style="margin-top:20px">Our <em class="serif">tours.</em></h2>
    <p>We run seven shikara tours through the day, from a 6 am Sunrise Cruise to a 3:30 pm Sunset Cruise, plus kayaking on the lake and in the village canals. Every shikara tour passes the Snake Boat Race track and crosses Vembanad Lake. The longer tours go on to Kainakary, Chavara Bhavan, Vattakayal, Pallathurthi and the paddy fields farmed below sea level.</p>
    <div class="btns">{wa(BOOK)}<a class="btn btn--ghost" href="shikara-tours.html">See all tours</a></div>
  </div>
  <div class="mosaic" style="grid-template-columns:1fr 1fr;grid-auto-rows:200px">
    <figure class="ph rv" style="grid-row:span 2">{img("deck-sofa", sizes="300px")}</figure>
    <figure class="ph rv">{img("chairs-green", sizes="300px")}</figure>
    <figure class="ph rv">{img("deck-yellow", sizes="300px")}</figure>
  </div>
</section>
{final('Come aboard <em class="serif">the Kalyani.</em>', "Every tour leaves from Rajiv Boat Jetty, from 6 am to 3:30 pm.", wa(BOOK, "Book on WhatsApp", "btn btn--mango"), photo="guests-bow")}'''
    return page("about.html", "About Kalyani Boat Service | Shikara Tours from Rajiv Boat Jetty",
                "Kalyani Boat Service runs shikara cruises and kayaking on the Alleppey backwaters from Rajiv Boat Jetty, Alappuzha.", body, "about.html", schema=BUSINESS)


def contact():
    phones = "".join(f'<li><b>Phone / WhatsApp</b><a href="tel:{p.replace(" ", "")}">{p}</a></li>' for p in SITE["phones"])
    body = f'''{phero("deck-front", '<a href="index.html">Home</a> / Contact', 'Let\'s get you <em class="serif">on the water.</em>', "The quickest way to book is WhatsApp. Or fill in the form and we'll get back to you.", wa(BOOK, "Chat on WhatsApp"), pos="50% 55%")}
<section class="sec wrap split">
  <div style="display:grid;gap:22px;align-content:start"><div class="eyebrow">Contact &amp; booking</div><h2>Call, message <em class="serif">or email.</em></h2>
    <ul class="contact-list">{phones}
      <li><b>Email</b><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
      <li><b>Boarding point</b><a href="{SITE["maps"]}" target="_blank" rel="noopener">{SITE["jetty"]} ↗</a></li></ul></div>
  {enquiry(heading="Send an enquiry")}
</section>'''
    return page("contact.html", "Contact & Book | Kalyani Boat Service, Alleppey",
                "Book a shikara cruise or kayaking in Alleppey. WhatsApp +91 98473 86262 or +91 97477 98412, or send an enquiry online.",
                body, "contact.html", schema=BUSINESS)


def simple(path, title, desc, h1, html, noindex=False, base=False):
    body = f'''<section class="phero phero--plain"><div class="stage" style="--g:var(--kayal)"><div class="txt wrap"><p class="crumbs"><a href="index.html">Home</a> / {h1}</p><h1>{h1}</h1></div></div></section>
<section class="sec wrap"><div class="prose">{html}</div></section>'''
    return page(path, title, desc, body, noindex=noindex, base=base)


TERMS = f'''<p class="lead">Simple terms for booking a Kalyani shikara tour or kayaking session.</p>
<h2>Prices</h2><ul><li>Each shikara tour has a price for two guests.</li><li>Each extra guest is charged per hour: ₹100 per hour on three-hour cruises and ₹150 per hour on the half-day and full-day tours.</li><li>Prices on this website are in Indian Rupees.</li></ul>
<h2>Booking</h2><ul><li>A booking is confirmed only when we confirm it to you on WhatsApp or by phone.</li><li>Advance payment, payment methods and cancellation terms are shared with you when we confirm your booking.</li></ul>
<h2>On the day</h2><ul><li>All tours start and end at {SITE["jetty"]}. Please arrive 10 minutes before your start time.</li><li>Timings can change because of weather or water conditions. We will contact you if this happens.</li></ul>
<p>Questions? Call {SITE["phones"][0]} or WhatsApp us.</p>'''

PRIVACY = f'''<p class="lead">How we handle the details you send us.</p>
<h2>What we collect</h2><p>When you send an enquiry we receive your name, phone number, optional email, tour, date, number of guests and any note you add.</p>
<h2>How we use it</h2><p>Only to reply to your enquiry and arrange your booking. We do not sell or share your details. Enquiries sent by email arrive in our inbox at {SITE["email"]}. Messages sent on WhatsApp are handled by WhatsApp.</p>
<h2>Cookies</h2><p>This website does not use tracking or advertising cookies.</p>
<h2>Contact</h2><p>To ask about or remove your details, email {SITE["email"]}.</p>'''


def build():
    pages = {
        "index.html": home(), "shikara-tours.html": shikara_tours(), "kayaking.html": kayaking(),
        "gallery.html": gallery(), "about.html": about(), "contact.html": contact(),
        "terms.html": simple("terms.html", "Booking Terms | Kalyani Boat Service", "Booking terms for Kalyani Boat Service shikara tours in Alleppey.", "Booking terms", TERMS),
        "privacy.html": simple("privacy.html", "Privacy | Kalyani Boat Service", "How Kalyani Boat Service handles enquiry details.", "Privacy", PRIVACY),
        "thank-you.html": simple("thank-you.html", "Thank you | Kalyani Boat Service", "Your enquiry has been sent.", "Thank you",
                                 f'<p class="lead">Your enquiry has been sent. We will reply on WhatsApp or by phone shortly.</p><div class="btns">{wa("Hi Kalyani Boat Service! I just sent an enquiry on your website.", "Message us on WhatsApp")}<a class="btn btn--ghost" href="index.html">Back to home</a></div>', noindex=True),
        "404.html": simple("404.html", "Page not found | Kalyani Boat Service", "This page could not be found.", "Page not found",
                           '<p class="lead">This page has drifted off. Try one of these instead.</p><div class="btns"><a class="btn btn--coral" href="shikara-tours.html">Shikara tours</a><a class="btn btn--ghost" href="index.html">Home</a></div>', noindex=True, base=True),
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


if __name__ == "__main__":
    build()
