# Kalyani Boat Service website

Website for **Kalyani Boat Service**, which runs shikara cruises and kayaking from Rajiv Boat Jetty, Alleppey.
Domain: **alleppeyshikaratours.com** (registered on Hostinger).

It's a static site (HTML, CSS, JavaScript) plus one small PHP file for the enquiry form, so it runs on any Hostinger plan.

## What's in it

Modern, minimal design on a light base, using the four time-of-day gradients (dawn, day, dusk, backwater) as accents. All text comes from the client's price sheet and contact details; nothing unconfirmed is on the site.

| Page | File |
|---|---|
| Home: hero that plays the day (photo and colour follow the hour), tours with time filters, sunrise/sunset compare, route, on-board photos, kayaking, price and booking | `site/index.html` |
| Tours list | `site/tours.html` |
| One page per tour (7) | `site/sunrise-cruise.html`, `half-day-tour.html`, `full-day-tour.html`, `breakfast-cruise.html`, `lunch-cruise.html`, `sunset-cruise.html`, `regular-cruise.html` |
| Kayaking, Gallery, Contact | `site/kayaking.html`, `site/gallery.html`, `site/contact.html` |
| Booking terms, Privacy, Thank you, 404 | `site/terms.html`, `privacy.html`, `thank-you.html`, `404.html` |

Review copy (temporary domain): https://mediumseagreen-monkey-262172.hostingersite.com

Bookings work two ways:
- **WhatsApp:** every Book button opens WhatsApp with a ready-made message. The enquiry form's **Send on WhatsApp** button adds the tour, date, guests and estimated price.
- **Email:** the form's **Send by email** button posts to `site/enquiry.php`, which emails the enquiry to the business.

## Upload to Hostinger

1. In hPanel, open **Websites → alleppeyshikaratours.com → File Manager → public_html**.
2. Delete Hostinger's default `default.php` / placeholder files if present.
3. Upload **everything inside `site/`** (not the `site` folder itself), including the hidden `.htaccess` file. `index.html` must be directly inside `public_html`.
4. In hPanel, open **Security → SSL** and make sure SSL is active, so `.htaccess` can send everyone to `https://`.
5. In hPanel, open **Emails** and create `noreply@alleppeyshikaratours.com`. `enquiry.php` sends from that address; without it, Gmail may reject the enquiry emails.
6. Send a test booking from the Book page and check that it arrives in `alleppeyshikaratours@gmail.com`, including the spam folder.
7. Add the site to Google Search Console and submit `https://alleppeyshikaratours.com/sitemap.xml`.

## Changing prices, times or contact details

All tour data, prices, routes and contact numbers live at the top of `build/build.py`.

```bash
pip install pillow
python3 build/build.py      # regenerates every page in site/
```

Then upload the changed files again. Don't edit the generated HTML pages by hand; the next build overwrites them.
The CSS (`site/assets/css/style.css`), scripts (`site/assets/js/main.js`, `hero.js`), `enquiry.php` and `.htaccess` are edited directly.

The enquiry email address is set in two places: `SITE["email"]` in `build/build.py`, and `$to` at the top of `site/enquiry.php`.

### Photos

The photos in `site/assets/img/` were made from the client's WhatsApp photos by `build/images.py`. To use new or full-size originals, put them in a folder, update the `PHOTOS` list in that script, and run:

```bash
python3 build/images.py /path/to/photos
python3 build/build.py
```

## Still to confirm with the client

The site uses the client's printed price sheet as it stands. These points are unclear on the sheet:

- [ ] **Full Day Tour timing:** the sheet says "08:00 am – 12:00 noon (8 hrs)". The site shows 8:00 am – 4:00 pm.
- [ ] **Sunset Cruise:** the sheet says "03:30 am". The site shows 3:30 pm – 6:30 pm.
- [ ] **Lunch Cruise:** the sheet lists only "Morning Tea/Coffee". Is lunch included?
- [ ] **Sunrise Cruise length:** the sheet says 3 hours (6–9 am). Earlier we were told 2 hours.
- [ ] **Kayaking:** tour names, timings, rates, meeting point and any rules (age, swimming). The page currently says "rates on request".
- [ ] **Advance payment and cancellation policy**, for the Booking terms page.
- [ ] **Full-size original photos.** The current ones are WhatsApp-compressed and look soft on large screens.
- [ ] **Google reviews or guest quotes**, to add a reviews section. None are on the site, because none have been supplied.
- [ ] **Which number is the WhatsApp number.** The site uses +91 98473 86262.
- [ ] **Instagram / Facebook links**, if any.

Photos left out on purpose: the blue kayak printed "GoKayakingClub" (it may belong to another company) and the wooden canoe with a houseboat behind it (it looks like a stock or AI image).
