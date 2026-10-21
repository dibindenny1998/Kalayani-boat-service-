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
BOAT = '<svg class="boat" viewBox="0 0 64 32" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h44q8 0 10-12 3 2 2 8-2 12-14 12H16Q7 28 4 20z"/><path d="M12 19v-7q14-8 28 0v7"/></svg>'
ARR = '<span class="arr" aria-hidden="true">→</span>'
WAVE = '<svg class="wave" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true"><path class="fill" d="M0 60V30Q180 0 360 30T720 30T1080 30T1440 30V60z"/><path class="line" d="M0 30Q180 0 360 30T720 30T1080 30T1440 30"/></svg>'
WAVE_DOWN = WAVE.replace('class="wave"', 'class="wave down"')
FILM = ["shikara-sunset-bow", "kayak-rainbow", "deck-sofa", "kayak-trees", "guests-bow", "kayak-sunset-group", "shikara-kalyani", "chairs-pink", "kayak-sunset-solo", "deck-front", "kayak-canal", "deck-yellow"]


def film():
    frames = "".join(f"<figure>{img(n, sizes='300px')}<figcaption>{CAPTIONS[n]}</figcaption></figure>" for n in FILM)
    copy = frames.replace("<figure>", '<figure aria-hidden="true">')
    return f'<div class="film" aria-label="Photos from Kalyani boats"><div class="film__track">{frames}{copy}</div></div>'


BOOK = "Hi Kalyani Boat Service! I'd like to book a shikara ride."

NAV = [("hours.html", "Hours"), ("index.html#route", "Route"), ("the-boat.html", "On deck"), ("kayak.html", "Kayak"), ("gallery.html", "Gallery")]


def wa(msg, label="Book on WhatsApp", cls="ticket ticket--red"):
    return f'<a class="{cls}" href="book.html" data-wa="{escape(msg)}">{WA_ICON}{label}</a>'


def header(current):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == current else ""}>{n}</a>' for h, n in NAV)
    book_cur = cur if current == "book.html" else ""
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="sky" id="pagesky" aria-hidden="true"></div><div class="grain" aria-hidden="true"></div>
<header class="top"><div class="wrap">
  <a class="logo" href="index.html" aria-label="Kalyani Boat Service, home"><span class="script">Kalyani</span><small>Boat service<br>Alleppey</small></a>
  <button class="menu" aria-label="Menu" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav" aria-label="Main">{links}<a class="ticket ticket--sm" href="book.html"{book_cur}>Book a pass {ARR}</a></nav>
</div></header>'''


def footer():
    tours = "".join(f'<li><a href="{t["slug"]}.html">{t["hhmm"]} · {t["name"]}</a></li>' for t in TOURS)
    phones = "".join(f'<li><a href="tel:{p.replace(" ", "")}">{p}</a></li>' for p in SITE["phones"])
    return f'''<footer class="foot"><div class="scallop"></div><div class="wrap">
  <div class="big" aria-hidden="true">Kalyani</div>
  <div class="grid">
    <div style="display:grid;gap:16px;align-content:start"><p style="color:var(--dim);max-width:36ch">Shikara and kayak hours on the Alleppey backwater. Every departure leaves from {SITE["jetty"]}.</p>
      <div class="acts">{wa(BOOK, "WhatsApp us", "ticket ticket--sm")}</div></div>
    <div><h4>Departures</h4><ul>{tours}</ul></div>
    <div><h4>More</h4><ul><li><a href="hours.html">All hours &amp; fares</a></li><li><a href="the-boat.html">On deck</a></li><li><a href="kayak.html">Kayak hour</a></li><li><a href="gallery.html">Gallery</a></li><li><a href="book.html">Book a pass</a></li><li><a href="terms.html">Booking terms</a></li><li><a href="privacy.html">Privacy</a></li></ul></div>
    <div><h4>Jetty desk</h4><ul>{phones}<li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li><li><a href="{SITE["maps"]}" target="_blank" rel="noopener">{SITE["jetty"]} ↗</a></li></ul></div>
  </div>
  <div class="base"><span>© <span id="year">2026</span> Kalyani Boat Service</span><span>09°29′N 76°20′E · Alappuzha</span></div>
</div></footer>
<a class="wa" href="book.html" data-wa="Hi Kalyani Boat Service! I have a question about your boat tours." aria-label="Chat on WhatsApp">{WA_ICON}</a>'''


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
<meta name="theme-color" content="#11163A">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=DM+Mono:wght@400;500&family=Hanken+Grotesk:wght@400;500;600;700&family=Yellowtail&family=Manjari:wght@400;700&display=swap">
<link rel="stylesheet" href="assets/css/style.css?v=6">
{ld}
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/data.js?v=6"></script>
<script src="assets/js/main.js?v=6" defer></script>
{scripts}
</body>
</html>
'''


def rise(*lines):
    return "".join(f'<span class="ln"><span>{l}</span></span>' for l in lines)


def board(title="Departures · Rajiv Boat Jetty"):
    rows = ""
    for t in TOURS:
        rows += f"""<a class="row" href="{t["slug"]}.html" data-img="assets/img/{t["img"]}-sm.webp" data-start="{t["start"] if t["start"] is not None else ""}" data-end="{t["end"] if t["end"] is not None else ""}">
  <span class="flip" data-text="{t["hhmm"].upper()}">{t["hhmm"].upper()}</span>
  <span class="th">{img(t["img"], sizes="64px")}</span>
  <span class="nm">{t["name"]}<small>{escape(", ".join(t["includes"]))}</small></span>
  <span class="du">{t["hours"]} HRS</span><span class="fa"><b>{inr(t["price"])}</b> / 2</span>
  <span class="st">{"On request" if t["start"] is None else "Scheduled"}</span><span class="go" aria-hidden="true">→</span></a>"""
    return f"""<div class="board rv"><div class="board__top"><span class="tag">{title}</span><span class="board__clock" aria-label="Time in Alleppey">--:--</span></div>
  <div class="rows">{rows}</div>
  <p class="board__foot">Fares are for two guests · each extra guest ₹100–₹150 per hour · times in IST</p><img class="peek" alt="" aria-hidden="true"></div>"""


def stops(t):
    lst, extra = ROUTES[t["route"]]
    lis = "".join(f'<li class="{"x" if s in extra else ""}"><span>{escape(s)}{"<small>Added on this route</small>" if s in extra else ""}</span></li>' for s in lst)
    return f'<ol class="stops">{lis}</ol>'


ROUTE_PHOTOS = ["deck-front", "shikara-kalyani", "deck-sofa", "guests-bow", "shikara-sunset-bow", "chairs-green", "deck-yellow", "chairs-pink", "kayak-sunset-group"]


def journey(t, heading, lede, photo="shikara-sunset-bow"):
    swaps = "".join(f'<img src="assets/img/{n}-sm.webp" alt="" loading="lazy" data-k="{i}"' + (' class="on"' if i == 0 else "") + ">" for i, n in enumerate(ROUTE_PHOTOS))
    return f"""{WAVE}<section class="sec lite day" id="route"><div class="wrap journey">
  <div class="stick"><span class="tag">The route</span><h2 class="rise">{heading}</h2><p class="lede">{lede}</p>
    <figure class="port swap" aria-hidden="true">{swaps}</figure><p class="cap">Seen from on board</p></div>
  {stops(t)}
</div></section>{WAVE_DOWN}"""


def chat(qas):
    items = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for i, (q, a) in enumerate(qas))
    return f'<div class="chat">{items}</div>'


def bookpass(selected="sunrise-cruise", heading="Book a boarding pass"):
    opts = "".join(f'<option value="{t["slug"]}"{" selected" if t["slug"] == selected else ""}>{t["hhmm"]} · {t["name"]}</option>' for t in TOURS)
    t = TOUR[selected]
    return f'''<form class="pass rv" data-calc data-email action="enquiry.php" method="post">
  <div class="pass__main">
    <div class="ptop"><span class="script">Kalyani</span><span class="tag">{heading}</span></div>
    <label class="field"><span>Departure</span><select name="tour">{opts}</select></label>
    <div class="fields">
      <label class="field"><span>Date</span><input type="date" name="date" required></label>
      <div class="field"><span id="g-label">Guests</span>
        <div class="step" role="group" aria-labelledby="g-label"><button type="button" data-step="-1" aria-label="Fewer guests">−</button><output aria-live="polite">2</output><button type="button" data-step="1" aria-label="More guests">+</button></div>
        <input type="hidden" name="guests" value="2"></div>
      <label class="field"><span>Name on the pass</span><input name="name" autocomplete="name" required></label>
      <label class="field"><span>Phone / WhatsApp</span><input name="phone" type="tel" autocomplete="tel" required></label>
      <label class="field"><span>Email (optional)</span><input name="email" type="email" autocomplete="email"></label>
      <label class="field"><span>Start time or a note</span><input name="message" placeholder="Needed for the Regular Cruise"></label>
    </div>
    <label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>
    <input type="hidden" name="started" value="">
    <div class="acts"><button type="button" class="ticket ticket--red" data-send="wa">{WA_ICON}Send pass on WhatsApp</button><button type="submit" class="ticket ticket--line">Email it to us</button></div>
    <p class="status" role="status" hidden></p>
  </div>
  <aside class="pass__stub" aria-live="polite">
    <span class="tag">Fare for your group</span>
    <span class="stub-total sum">{inr(t["price"])}</span>
    <div class="stubline"><span>Departure <b class="s-tour">{t["name"]}</b></span><span>Time <b class="s-time">{t["time"]}</b></span><span>Date <b class="s-date">Choose a date</b></span><span>Guests <b class="s-guests">2</b></span></div>
    <p class="sumnote" style="font:500 11px var(--mono);color:var(--ink-soft)">Fare covers two guests</p>
    <div class="code" aria-hidden="true"></div>
    <span class="tag" style="font-size:10px">Gate · Rajiv Boat Jetty</span>
  </aside>
</form>'''


def pcard(t):
    return f'''<a class="pcard rv" href="{t["slug"]}.html">
  <div class="m"><span class="tag">{t["time"]} · {t["hours"]} hrs</span><h3>{t["name"]}</h3><p>{escape(t["lead"])}</p><div class="pp">{img(t["img"], sizes="80px")}</div></div>
  <div class="s sky-{t["sky"]}"><small>Fare / 2</small><b>{t["hhmm"]}</b><span class="fare">{inr(t["price"])}</span></div>
</a>'''


BUSINESS = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "name": SITE["name"], "url": SITE["url"],
    "image": SITE["url"] + "/assets/img/og-image.jpg", "telephone": SITE["phones"][0], "email": SITE["email"],
    "priceRange": f"{inr(min(t['price'] for t in TOURS))} – {inr(max(t['price'] for t in TOURS))}",
    "address": {"@type": "PostalAddress", "streetAddress": "Rajiv Boat Jetty", "addressLocality": "Alappuzha", "addressRegion": "Kerala", "addressCountry": "IN"},
}

# photos shown by the home page dial, by hour
DIAL_PHOTOS = [("kayak-sunrise-group", 0, 7.5, "50% 62%"), ("deck-front", 7.5, 10, "50% 55%"), ("shikara-kalyani", 10, 13, "50% 62%"),
               ("chairs-green", 13, 15.5, "50% 50%"), ("shikara-sunset-bow", 15.5, 18.6, "50% 55%"), ("kayak-sunset-group", 18.6, 24, "50% 60%")]
DECK = [("Coir canopy", "A woven coconut-fibre roof keeps the deck shaded through the day.", "30%", "10%"),
        ("Life buoys", "Rings hang under the canopy, within reach of every seat.", "47%", "14%"),
        ("Cane chairs", "Covered cane chairs for groups, facing the water on both sides.", "38%", "64%"),
        ("Turned teak pillars", "Carved wooden pillars hold up the canopy along the length of the boat.", "80%", "40%"),
        ("Open water", "Low rails, so the backwater is at eye level from your seat.", "10%", "38%")]


# ---------------------------------------------------------------- pages
def home():
    pics = "".join(f'<img src="assets/img/{n}-lg.webp" alt="" data-from="{a}" data-to="{b}" style="object-position:{p}"{" class=\"on\"" if i == 0 else ""} {"fetchpriority=\"high\"" if i == 0 else "loading=\"lazy\""}>' for i, (n, a, b, p) in enumerate(DIAL_PHOTOS))
    sunrise = TOUR["sunrise-cruise"]
    body = f'''<section class="hour" id="hour" aria-label="Pick your hour">
  <div class="pics" aria-hidden="true">{pics}</div><div class="tint" aria-hidden="true"></div><div class="shade" aria-hidden="true"></div>
  <div class="copy wrap">
    <div class="coords"><span>Alleppey · Kerala</span><span>09°29′N 76°20′E</span><span>Rajiv Boat Jetty</span></div>
    <h1 class="rise">{rise('Pick your', 'hour<span class="script">on the backwater</span>')}</h1>
    <p class="lede">Shikara rides and kayaking from Rajiv Boat Jetty. First boat at six in the morning, last one out at half past three for the sunset.</p>
  </div>
  <svg class="xboat" viewBox="0 0 160 60" aria-hidden="true"><path d="M8 40h104q18 0 24-26 6 3 4 16-4 24-30 24H38Q16 54 8 40z" fill="#0A0D24"/><path d="M26 39V27q36-18 72 0v12" fill="none" stroke="#0A0D24" stroke-width="5"/><path d="M118 38q8-10 10-24" fill="none" stroke="#E8B54A" stroke-width="3"/></svg>
  <div class="birds" aria-hidden="true"><svg viewBox="0 0 40 16"><path d="M2 10 Q11 0 20 9 Q29 0 38 10"/></svg><svg viewBox="0 0 40 16"><path d="M2 10 Q11 0 20 9 Q29 0 38 10"/></svg><svg viewBox="0 0 40 16"><path d="M2 10 Q11 0 20 9 Q29 0 38 10"/></svg></div>
  <a class="cue" href="#departures" aria-label="Scroll to departures"><span></span>Scroll</a>
  <div class="dialbox">
    <svg class="dial" id="dial" viewBox="0 0 1000 300" role="slider" aria-label="Hour of the day" aria-valuemin="5" aria-valuemax="20" aria-valuenow="6" tabindex="0">
      <line class="hz" x1="0" y1="290" x2="1000" y2="290"/>
      <path class="arc" d="M60 290 A440 260 0 0 1 940 290"/>
      <path class="done" id="dialdone" d="M60 290 A440 260 0 0 1 60 290"/>
      <g id="ticks"></g><circle class="halo" id="halo" r="30"/><circle class="sun" id="sun" r="16"/>
    </svg>
    <div class="readout">
      <span class="t" id="rt">06:00</span>
      <a class="n" id="rn" href="{sunrise["slug"]}.html">{sunrise["name"]}</a>
      <span class="f" id="rf">{inr(sunrise["price"])} for two · drag the sun</span>
      <div class="ctl"><button type="button" id="rplay">Pause</button><button type="button" id="rnow">Now in Alleppey</button></div>
    </div>
  </div>
</section>

<section class="sec lite dawn" id="departures"><div class="wrap">
  <div class="head"><div><span class="tag">Today at the jetty</span><h2 class="rise">{rise("Seven", 'departures<span class="script" style="font-size:.5em"> a day</span>')}</h2></div>
    <p class="lede">Every shikara ride leaves from Rajiv Boat Jetty and comes back there. The board shows what is on the water right now in Alleppey. Hover a departure to see the boat.</p></div>
  {board()}
  <div class="acts" style="margin-top:28px"><a class="ticket ticket--red" href="hours.html">All hours &amp; fares {ARR}</a></div>
</div></section>

{film()}

<section class="sec wrap" id="light">
  <div class="head"><div><span class="tag">Same lake, two hours</span><h2 class="rise">{rise("Sunrise", 'or <span class="script">sunset?</span>')}</h2></div>
    <p class="lede">Drag across the photo. Mornings are cool, still and pink. Evenings turn the whole lake gold.</p></div>
  <div class="compare rv" id="compare">
    {img("kayak-sunrise-group", sizes="(max-width:1480px) 100vw, 1400px", pos="50% 62%")}
    <div class="compare__top">{img("shikara-sunset-bow", sizes="(max-width:1480px) 100vw, 1400px", pos="50% 55%")}</div>
    <span class="compare__line" aria-hidden="true"><i>⇆</i></span>
    <span class="compare__lab l">Sunrise · on the lake</span><span class="compare__lab r">Sunset · from the shikara</span>
    <input type="range" min="0" max="100" value="50" aria-label="Compare sunrise and sunset">
  </div>
  <div class="acts" style="margin-top:24px;justify-content:center"><a class="ticket" href="sunrise-cruise.html">Sunrise · {inr(1500)} {ARR}</a><a class="ticket ticket--red" href="sunset-cruise.html">Sunset · {inr(1600)} {ARR}</a></div>
</section>

{journey(TOUR["sunrise-cruise"], rise("Jetty to", "lake and back"), "The classic three-hour loop: out past the Snake Boat Race course, across Vembanad Lake and home through Vilakkumaram. Longer tours add villages, canals and paddy fields.")}

<section class="sec paper lite"><div class="wrap">
  <div class="head"><div><span class="tag">On deck</span><h2 class="rise">{rise("Your seat", 'for <span class="script">three hours</span>')}</h2></div>
    <p class="lede">Tap the gold markers to look around a Kalyani shikara.</p></div>
  <div class="deckgrid">
    <div class="deck rv" data-deck>{img("chairs-green", sizes="(max-width:900px) 100vw, 900px")}
      {"".join(f'<button class="spot" type="button" style="--x:{x};--y:{y}" aria-expanded="false" data-i="{i}">{i + 1}</button>' for i, (n, d, x, y) in enumerate(DECK))}
    </div>
    <div class="deckside">
      <figure class="frame rv tilt">{img("deck-sofa", sizes="400px")}</figure>
      <figure class="frame rv tilt">{img("guests-bow", sizes="400px", pos="50% 30%")}</figure>
    </div>
  </div>
  <div class="acts" style="margin-top:28px"><a class="ticket ticket--line" href="the-boat.html">Walk the whole boat {ARR}</a></div>
</div></section>

<section class="sec kayak"><div class="wrap grid">
  <div style="display:grid;gap:22px;justify-items:start"><span class="tag" style="color:#FFE27A">Kayak hour</span><h2 class="rise">{rise("Paddle the", 'canals <span class="script">yourself</span>')}</h2>
    <p class="lede">Swap the cushions for a paddle. Kayak sessions go into the narrow village canals and out onto the lake at sunrise and at sunset.</p>
    <div class="acts">{wa("Hi Kalyani Boat Service! I'd like to know kayaking timings and rates.", "Ask for kayak times", "ticket ticket--cream")}<a class="ticket ticket--line" href="kayak.html">Kayak hour {ARR}</a></div></div>
  <div class="ports" aria-hidden="true"><figure class="port k1 tilt">{img("kayak-sunset-solo", sizes="320px")}</figure><figure class="port k2 tilt">{img("kayak-trees", sizes="240px")}</figure><figure class="port k3 tilt">{img("kayak-rainbow", sizes="220px")}</figure>
    <svg class="paddle" viewBox="0 0 40 160" fill="currentColor"><rect x="18" y="20" width="4" height="120" rx="2"/><ellipse cx="20" cy="14" rx="10" ry="16"/><ellipse cx="20" cy="146" rx="10" ry="16"/></svg></div>
</div></section>

<section class="sec lite dawn2"><div class="wrap boatman">
  <div><div class="head" style="grid-template-columns:1fr"><div><span class="tag">Ask the boatman</span><h2 class="rise">{rise("Questions", 'from the <span class="script">jetty</span>')}</h2></div><p class="lede">What people ask us most before they step on board.</p></div>
  {chat(HOME_QA)}</div>
  <figure class="boatpic rv">{img("shikara-kalyani", sizes="(max-width:900px) 100vw, 520px", pos="50% 62%")}<figcaption><span class="script">Kalyani</span> waiting at the jetty</figcaption></figure>
</div></section>

<section class="sec dusk" id="book"><div class="wrap">
  <div class="head"><div><span class="tag">Book</span><h2 class="rise">{rise("Print your", '<span class="script">boarding pass</span>')}</h2></div><p class="lede">Pick a departure, a date and how many of you are coming. The fare updates as you go, and the pass goes to us on WhatsApp.</p></div>
  {bookpass()}
</div></section>
'''
    return page("index.html", "Kalyani Boat Service | Shikara Rides & Kayaking by the Hour, Alleppey",
                "Pick your hour on the Alleppey backwater: shikara rides from Rajiv Boat Jetty at 6 am, 8 am, 9 am, 1 pm and 3:30 pm, from ₹1,500 for two. Kayaking at sunrise and sunset.",
                body, "index.html", '<script src="assets/js/hero.js?v=6" defer></script>', BUSINESS)


HOME_QA = [
    ("Where do we get on the boat?", f"At {SITE['jetty']}. Every departure starts and ends there. We send the exact spot on WhatsApp when we confirm."),
    ("Which hour should we pick?", "For soft light and a quiet lake, the 6:00 Sunrise Cruise. For food on board, a breakfast departure or the full day. For colour in the sky, the 3:30 Sunset Cruise."),
    ("How does the fare work?", "Each fare covers two people. Every extra guest adds ₹100 an hour on the three-hour rides and ₹150 an hour on the half day and full day."),
    ("Can we go at our own time?", "Yes. The Regular Cruise is any three hours you like, at the same fare as the sunrise ride. Tell us your start time when you book."),
    ("How do we book?", "Fill in the boarding pass on this page and send it on WhatsApp, or call the jetty desk. We reply to confirm the slot."),
]


def hours():
    body = f'''<section class="phero">{img("shikara-sunset-bow", sizes="100vw", eager=True)}<div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> / Hours</p><span class="tag">The timetable</span>
  <h1 class="rise">{rise("Hours", 'on the <span class="script">water</span>')}</h1>
  <p class="lede">Six fixed departures and one you time yourself. All from Rajiv Boat Jetty, all priced for two.</p>
  <div class="acts"><a class="ticket ticket--red" href="#book">Book a pass {ARR}</a><a class="ticket ticket--line" href="#passes">See every pass</a></div>
</div></section>

<section class="sec wrap">{board("Live departures · IST")}</section>

<section class="sec wrap" id="passes" style="padding-top:0">
  <div class="head"><div><span class="tag">Boarding passes</span><h2 class="rise">{rise("Choose a", 'departure')}</h2></div><p class="lede">Open a pass for the route, what is served on board and the fare for your group.</p></div>
  <div class="passes">{"".join(pcard(t) for t in TOURS)}</div>
</section>

<section class="sec wrap" style="padding-top:0">
  <div class="head"><div><span class="tag">Fares</span><h2 class="rise">{rise("Two aboard,", 'then by the hour')}</h2></div>
    <p class="lede">The fare covers two people. Each extra guest pays per hour of the ride: ₹100 on the three-hour departures, ₹150 on the half day and full day. Four people on the Sunrise Cruise: {inr(1500)} + 2 × ₹100 × 3 = {inr(2100)}.</p></div>
</section>

<section class="sec wrap" id="book" style="padding-top:0">{bookpass()}</section>'''
    schema = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f'{SITE["url"]}/{t["slug"]}.html', "name": t["name"]} for i, t in enumerate(TOURS)]}
    return page("hours.html", "Shikara Timings & Fares in Alleppey | Kalyani Boat Service",
                "Kalyani shikara departures from Rajiv Boat Jetty: Sunrise 6 am ₹1,500, Half Day 8 am ₹2,300, Full Day 8 am ₹4,600, Breakfast 9 am ₹1,800, Lunch 1 pm ₹1,800, Sunset 3:30 pm ₹1,600, for two.",
                body, "hours.html", schema=schema)


def tour_page(t):
    end_stop = "Vembanad Lake" if t["route"] == "base" else ("Pallathurthi" if t["route"] == "half" else "Kainakary")
    when = (f"Boarding at {clock(t['start'])}, back at {clock(t['end'])}." if t["start"] is not None
            else "You pick the start time. Tell us when you book.")
    qas = [
        ("What is included in the fare?", f"{', '.join(t['includes'])}, and the boat for {t['hours']} hours with our crew. The fare of {inr(t['price'])} covers two guests."),
        ("What if we are more than two?", f"Each extra guest adds ₹{t['extra']} for every hour, so ₹{t['extra'] * t['hours']} per person on this {t['hours']}-hour ride."),
        ("What time should we reach the jetty?", f"{when} Please be at Rajiv Boat Jetty ten minutes early."),
        ("What should we bring?", "Sunglasses, a hat and sunscreen for daytime rides, and a light layer for the early morning."),
    ]
    other = [o for o in TOURS if o is not t][:3]
    inc = "".join(f"<li>{escape(i)}</li>" for i in t["includes"])
    body = f'''<section class="phero">{img(t["img"], sizes="100vw", eager=True)}<div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> / <a href="hours.html">Hours</a> / {t["name"]}</p><span class="tag">Departure {t["hhmm"]} · {t["hours"]} hours</span>
  <h1 class="rise">{rise(*t["name"].split(" with ")) if " with " in t["name"] else rise(t["name"])}</h1>
  <p class="lede">{escape(t["lead"])}</p>
</div></section>

<section class="wrap tourpass">
  <div class="pass rv">
    <div class="pass__main"><div class="ptop"><span class="script">Kalyani</span><span class="tag">Boarding pass · {t["name"]}</span></div>
      <div class="fromto"><div><small>From</small><b>Rajiv Jetty</b></div>{BOAT}<div style="text-align:right"><small>Out to</small><b>{end_stop}</b></div></div>
      <dl class="kv"><div><dt>Departs</dt><dd>{t["hhmm"]}</dd></div><div><dt>Duration</dt><dd>{t["hours"]} hrs</dd></div><div><dt>Fare for two</dt><dd class="money">{inr(t["price"])}</dd></div><div><dt>Extra guest</dt><dd>₹{t["extra"]}/hr</dd></div><div><dt>Gate</dt><dd>Rajiv Jetty</dd></div></dl></div>
    <aside class="pass__stub"><span class="tag">Admit two</span><span class="stub-total">{inr(t["price"])}</span><div class="stubline"><span>Time <b>{t["time"]}</b></span><span>On board <b>{escape(", ".join(t["includes"]))}</b></span></div>
      <div class="code" aria-hidden="true"></div>{wa(f"Hi Kalyani Boat Service! I'd like to book the {t['name']} ({t['time']}).", "Book this pass", "ticket ticket--red ticket--sm")}</aside>
  </div>
</section>

{journey(t, rise("The", "route"), "From the jetty and back. Stops in red are added on this departure.", photo=t["img"])}

<div class="scallop"></div>
<section class="sec paper"><div class="wrap head" style="margin-bottom:0">
  <div><span class="tag">On board</span><h2 class="rise">{rise("In the", '<span class="script">fare</span>')}</h2></div>
  <ul class="ticks">{inc}<li>The shikara and crew for {t["hours"]} hours</li><li>Boarding at Rajiv Boat Jetty</li></ul>
</div></section>
<div class="scallop" style="transform:scaleY(-1)"></div>

<section class="sec wrap">
  <div class="head"><div><span class="tag">Ask the boatman</span><h2 class="rise">{rise("Before", "you board")}</h2></div></div>
  {chat(qas)}
</section>

<section class="sec wrap" id="book" style="padding-top:0">{bookpass(t["slug"], "Your pass for this ride")}</section>

<section class="sec wrap" style="padding-top:0">
  <div class="head"><div><span class="tag">Other departures</span><h2 class="rise">{rise("Another", "hour?")}</h2></div><a class="ticket ticket--line" href="hours.html">Full timetable {ARR}</a></div>
  <div class="passes">{"".join(pcard(o) for o in other)}</div>
</section>'''
    schema = [
        {"@context": "https://schema.org", "@type": "TouristTrip", "name": t["name"], "description": t["lead"], "touristType": "Backwater cruise",
         "provider": {"@type": "LocalBusiness", "name": SITE["name"], "telephone": SITE["phones"][0]},
         "itinerary": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s} for i, s in enumerate(ROUTES[t["route"]][0])]},
         "offers": {"@type": "Offer", "price": t["price"], "priceCurrency": "INR", "description": "Fare for two guests", "url": f'{SITE["url"]}/{t["slug"]}.html'}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]},
    ]
    return page(f'{t["slug"]}.html', f'{t["title"]} | {t["hhmm"]} · {inr(t["price"])} for two | Kalyani',
                f'{t["name"]} from Rajiv Boat Jetty, Alleppey. Departs {t["time"]}, {t["hours"]} hours, {inr(t["price"])} for two. {", ".join(t["includes"])} on board.',
                body, "hours.html", schema=schema)


def kayak():
    ports = "".join(f'<figure class="rv"><div class="port" style="width:min(100%,340px);margin-inline:auto">{img(n, sizes="340px")}</div><p class="cap" style="text-align:center">{CAPTIONS[n]}</p></figure>'
                    for n in ["kayak-trees", "kayak-sunrise-group", "kayak-canal", "kayak-rainbow", "kayak-sunset-solo", "kayak-sunset-group"])
    qas = [("When do kayak sessions run?", "At sunrise and at sunset, when the water is calm and the light is soft. Message us for this week's times."),
           ("Where do we start?", "We share the meeting point when we confirm your session."),
           ("How much does it cost?", "Rates depend on the session and group size. Send us your date and number of people and we reply with the rate."),
           ("Single or double kayaks?", "Tell us who is coming and we suggest the right boats for your group.")]
    body = f'''<section class="phero">{img("kayak-sunset-group", sizes="100vw", eager=True)}<div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> / Kayak</p><span class="tag">Kayak hour</span>
  <h1 class="rise">{rise("Paddle", 'your <span class="script">own way</span>')}</h1>
  <p class="lede">Kayak through the narrow village canals and out onto Vembanad Lake, at sunrise or at sunset.</p>
  <div class="acts">{wa("Hi Kalyani Boat Service! I'd like to know kayaking timings and rates.", "Ask for kayak times")}<a class="ticket ticket--line" href="hours.html">Shikara hours</a></div>
</div></section>
<section class="sec wrap"><div class="head"><div><span class="tag">Through the porthole</span><h2 class="rise">{rise("Canals,", "lake, light")}</h2></div><p class="lede">From our kayak trips.</p></div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:40px 30px">{ports}</div></section>
<section class="sec kayak"><div class="wrap"><div class="head"><div><span class="tag" style="color:#FFE27A">Ask the boatman</span><h2 class="rise">{rise("Kayak", "questions")}</h2></div></div>{chat(qas)}</div></section>'''
    return page("kayak.html", "Kayaking in Alleppey at Sunrise & Sunset | Kalyani Boat Service",
                "Kayak the Alleppey village canals and Vembanad Lake at sunrise or sunset with Kalyani Boat Service. Message us for times and rates.", body, "kayak.html", schema=BUSINESS)


def the_boat():
    lst = "".join(f'<li data-n="{i + 1:02d}"><div><b>{n}</b><span>{d}</span></div></li>' for i, (n, d, x, y) in enumerate(DECK))
    body = f'''<section class="phero">{img("shikara-kalyani", sizes="100vw", eager=True, pos="50% 62%")}<div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> / On deck</p><span class="tag">The boat</span>
  <h1 class="rise">{rise("On deck", 'of the <span class="script">Kalyani</span>')}</h1>
  <p class="lede">A shikara is the small covered boat of Kerala's backwater: low in the water, shaded, built for sitting back and watching the banks go by.</p>
</div></section>
<section class="sec wrap"><div class="head"><div><span class="tag">Look around</span><h2 class="rise">{rise("Tap the", "markers")}</h2></div></div>
  <div class="deck rv" data-deck>{img("chairs-green", sizes="(max-width:1480px) 100vw, 1400px")}
    {"".join(f'<button class="spot" type="button" style="--x:{x};--y:{y}" aria-expanded="false" data-i="{i}">{i + 1}</button>' for i, (n, d, x, y) in enumerate(DECK))}</div>
  <ul class="decklist" style="margin-top:40px">{lst}</ul></section>
<section class="sec wrap" style="padding-top:0"><div class="head"><div><span class="tag">The front deck</span><h2 class="rise">{rise("Lie back,", 'look <span class="script">up</span>')}</h2></div>
  <p class="lede">At the bow, a cushioned platform under the canopy. Most guests end up here.</p></div>
  <div class="gal">{"".join(f'<figure class="rv"><div class="frame">{img(n, sizes="(max-width:700px) 100vw, 460px")}</div><p class="cap">{CAPTIONS[n]}</p></figure>' for n in ["deck-sofa", "guests-bow", "deck-yellow", "deck-pink", "chairs-pink", "deck-front"])}</div></section>
<section class="sec wrap" style="padding-top:0">{bookpass()}</section>'''
    return page("the-boat.html", "On Deck: Inside a Kalyani Shikara | Alleppey", "Look around a Kalyani shikara: cushioned front deck, cane chairs, coir canopy and life buoys on board.", body, "the-boat.html", schema=BUSINESS)


def gallery():
    order = ["shikara-sunset-bow", "kayak-sunset-group", "guests-bow", "kayak-trees", "deck-sofa", "kayak-rainbow", "shikara-kalyani",
             "kayak-sunset-solo", "chairs-green", "deck-front", "kayak-canal", "deck-yellow", "chairs-pink", "kayak-sunrise-group", "deck-pink"]
    figs = "".join(f'<figure class="rv"><div class="frame">{img(n, sizes="(max-width:700px) 100vw, 460px")}</div><p class="cap">{i + 1:02d} · {CAPTIONS[n]}</p></figure>' for i, n in enumerate(order))
    body = f'''<section class="phero phero--plain"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / Gallery</p><span class="tag">Logbook</span>
  <h1 class="rise">{rise("From the", '<span class="script">logbook</span>')}</h1><p class="lede">Photos from the boats, the lake and the people who came aboard.</p></div></section>
<section class="sec wrap" style="padding-top:40px"><div class="gal">{figs}</div></section>'''
    return page("gallery.html", "Photos | Kalyani Boat Service, Alleppey", "Photos of Kalyani shikaras, sunset rides and kayaking on Vembanad Lake, Alleppey.", body, "gallery.html")


def book():
    phones = "".join(f'<li><b>Phone / WhatsApp</b><a href="tel:{p.replace(" ", "")}">{p}</a></li>' for p in SITE["phones"])
    body = f'''<section class="phero phero--plain"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / Book</p><span class="tag">Jetty desk</span>
  <h1 class="rise">{rise("Book a", '<span class="script">pass</span>')}</h1><p class="lede">Fill in the pass and send it on WhatsApp, or call the jetty desk. We confirm every booking ourselves.</p></div></section>
<section class="sec wrap" style="padding-top:40px">{bookpass(heading="Booking request")}</section>
<section class="sec wrap" style="padding-top:0"><div class="head"><div><span class="tag">Reach us</span><h2 class="rise">{rise("Jetty", "desk")}</h2></div></div>
  <ul class="lines">{phones}<li><b>Email</b><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li><li><b>Boarding</b><a href="{SITE["maps"]}" target="_blank" rel="noopener">Rajiv Boat Jetty ↗</a></li></ul></section>'''
    return page("book.html", "Book a Shikara Ride | Kalyani Boat Service, Alleppey",
                "Book a Kalyani shikara ride or kayak session in Alleppey. WhatsApp +91 98473 86262 or +91 97477 98412.", body, "book.html", schema=BUSINESS)


def simple(path, title, desc, h1, html, noindex=False, base=False):
    body = f'''<section class="phero phero--plain"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / {h1}</p><h1>{h1}</h1></div></section>
<section class="sec wrap" style="padding-top:40px"><div class="prose">{html}</div></section>'''
    return page(path, title, desc, body, noindex=noindex, base=base)


TERMS = f'''<p class="lede">Simple terms for booking a Kalyani shikara tour or kayaking session.</p>
<h2>Prices</h2><ul><li>Each shikara tour has a price for two guests.</li><li>Each extra guest is charged per hour: ₹100 per hour on three-hour cruises and ₹150 per hour on the half-day and full-day tours.</li><li>Prices on this website are in Indian Rupees.</li></ul>
<h2>Booking</h2><ul><li>A booking is confirmed only when we confirm it to you on WhatsApp or by phone.</li><li>Advance payment, payment methods and cancellation terms are shared with you when we confirm your booking.</li></ul>
<h2>On the day</h2><ul><li>All tours start and end at {SITE["jetty"]}. Please arrive 10 minutes before your start time.</li><li>Timings can change because of weather or water conditions. We will contact you if this happens.</li></ul>
<p>Questions? Call {SITE["phones"][0]} or WhatsApp us.</p>'''

PRIVACY = f'''<p class="lede">How we handle the details you send us.</p>
<h2>What we collect</h2><p>When you send an enquiry we receive your name, phone number, optional email, tour, date, number of guests and any note you add.</p>
<h2>How we use it</h2><p>Only to reply to your enquiry and arrange your booking. We do not sell or share your details. Enquiries sent by email arrive in our inbox at {SITE["email"]}. Messages sent on WhatsApp are handled by WhatsApp.</p>
<h2>Cookies</h2><p>This website does not use tracking or advertising cookies.</p>
<h2>Contact</h2><p>To ask about or remove your details, email {SITE["email"]}.</p>'''


def build():
    pages = {
        "index.html": home(), "hours.html": hours(), "kayak.html": kayak(), "the-boat.html": the_boat(),
        "gallery.html": gallery(), "book.html": book(),
        "terms.html": simple("terms.html", "Booking Terms | Kalyani Boat Service", "Booking terms for Kalyani Boat Service shikara rides in Alleppey.", "Booking terms", TERMS),
        "privacy.html": simple("privacy.html", "Privacy | Kalyani Boat Service", "How Kalyani Boat Service handles booking details.", "Privacy", PRIVACY),
        "thank-you.html": simple("thank-you.html", "Pass received | Kalyani Boat Service", "Your booking request has been sent.", "Pass received",
                                 f'<p class="lede">Your booking request reached the jetty desk. We will confirm on WhatsApp or by phone shortly.</p><div class="acts">{wa("Hi Kalyani Boat Service! I just sent a booking request on your website.", "Message us on WhatsApp")}<a class="ticket ticket--line" href="index.html">Back to the jetty</a></div>', noindex=True),
        "404.html": simple("404.html", "Page not found | Kalyani Boat Service", "This page could not be found.", "Off the map",
                           '<p class="lede">This page has drifted off the route.</p><div class="acts"><a class="ticket ticket--red" href="hours.html">See today\'s departures</a><a class="ticket ticket--line" href="index.html">Home</a></div>', noindex=True, base=True),
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
