#!/usr/bin/env python3
"""
Build the Dar es Salaam Islamic Seminary website.

Every page is generated from the content in this file plus the shared
templates below, so the header, footer, hero, section labels and motion stay
consistent across the whole site.

    python3 build.py            # write the site
    python3 build.py --zip      # also package it as dis-website.zip

The generated .html files are the site — open them with any static server:

    python3 -m http.server 8080
"""

import html
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_NAME = "Dar es Salaam Islamic Seminary"
FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wght@300..700&"
         "family=Fraunces:opsz,wght,SOFT,WONK@9..144,300..700,0..100,0..1&display=swap")


def esc(text):
    return html.escape(str(text), quote=True)


# --------------------------------------------------------------- icons -----
ICON_ARROW = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
              'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
ICON_BACK = ('<svg class="btn__arrow" viewBox="0 0 24 24" width="16" height="16" fill="none" '
             'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
             'aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>')
ICON_CLOSE = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" '
              'stroke-width="1.7" stroke-linecap="round" aria-hidden="true">'
              '<path d="M6 6l12 12M18 6L6 18"/></svg>')
ICON_PREV = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
             'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M15 6l-6 6 6 6"/></svg>')
ICON_NEXT = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
             'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M9 6l6 6-6 6"/></svg>')

# ----------------------------------------------------------------- nav -----
NAV = [
    ("/about/", "About"),
    ("/leadership/", "Leadership"),
    ("/academics/", "Academics"),
    ("/admissions/", "Admissions"),
    ("/news/", "News"),
    ("/events/", "Events"),
    ("/gallery/", "Gallery"),
    ("/contact/", "Contact"),
]

MOBILE_NAV = [
    ("/about/", "About"),
    ("/leadership/", "Leadership"),
    ("/academics/", "Academics"),
    ("/academics/#departments", "Departments"),
    ("/admissions/", "Admissions"),
    ("/news/", "News"),
    ("/events/", "Events"),
    ("/gallery/", "Gallery"),
    ("/faq/", "Questions & answers"),
    ("/contact/", "Contact"),
]

ADDRESS = "Mikocheni B, off Mwai Kibaki Road, P.O. Box 78314, Dar es Salaam, Tanzania"
PHONE = "+255 754 100 220"
EMAIL = "info@dis.ac.tz"
OFFICE_HOURS = "Monday – Friday, 07:30 – 16:30 · Saturday, 08:00 – 12:00 (admissions desk only)"


# ------------------------------------------------------------ templates ----
def document(title, description, active, body, og_image="/assets/img/courtyard.jpg",
             with_lightbox=False):
    """Wrap page content in the shared shell."""
    nav = "".join(
        '<a class="nav__link" href="%s"%s>%s</a>' % (
            href, ' aria-current="page"' if href == active else "", label)
        for href, label in NAV
    )
    mobile = "".join(
        '<a class="mobile-nav__link" href="%s"%s><span>%s</span>'
        '<span class="mobile-nav__num tnum">%02d</span></a>' % (
            href, ' aria-current="page"' if href == active else "", label, i + 1)
        for i, (href, label) in enumerate(MOBILE_NAV)
    )
    lightbox = LIGHTBOX if with_lightbox else ""

    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>%(title)s · DIS</title>
    <meta name="description" content="%(description)s">
    <meta name="theme-color" content="#f3ede2">
    <meta property="og:type" content="website">
    <meta property="og:title" content="%(title)s · DIS">
    <meta property="og:description" content="%(description)s">
    <meta property="og:image" content="%(og_image)s">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="%(fonts)s" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/site.css">
    <noscript><style>.reveal,.rule-draw{opacity:1 !important;transform:none !important}</style></noscript>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>

    <header class="site-header">
      <div class="site-header__inner shell">
        <a class="brand" href="/">
          <span class="brand__mark" aria-hidden="true">DIS</span>
          <span class="brand__text">
            <span class="brand__name">Dar es Salaam Islamic Seminary</span>
            <span class="label-caps brand__sub">Est. 1998 · Dar es Salaam</span>
          </span>
        </a>
        <nav class="nav" aria-label="Primary">%(nav)s</nav>
        <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false"
                aria-controls="mobile-nav" aria-label="Open menu">
          <span class="nav-toggle__bars" aria-hidden="true"><span></span><span></span><span></span></span>
        </button>
      </div>
    </header>

    <div class="mobile-nav" id="mobile-nav" data-mobile-nav hidden>
      <div class="shell">
        %(mobile)s
        <div class="mobile-nav__foot">
          <p class="label-caps">Office hours</p>
          <p>%(hours)s</p>
          <p><a class="footer-link" href="tel:%(phone_href)s">%(phone)s</a></p>
        </div>
      </div>
    </div>

    <main id="main">
%(body)s
    </main>

    <footer class="site-footer">
      <div class="shell">
        <div class="site-footer__grid">
          <div class="footer-col">
            <a class="brand" href="/">
              <span class="brand__mark" aria-hidden="true">DIS</span>
              <span class="brand__text">
                <span class="brand__name">Dar es Salaam Islamic Seminary</span>
                <span class="label-caps brand__sub">Knowledge, character and service since 1998</span>
              </span>
            </a>
            <p class="footer-about">
              A day and boarding school serving families across Dar es Salaam, Pwani and the
              Zanzibar archipelago. The national curriculum in full, taught inside a framework
              of adab.
            </p>
          </div>

          <div class="footer-col">
            <p class="label-caps footer-col__title">The school</p>
            <div class="footer-col__list">
              <a class="footer-link" href="/about/">About the seminary</a>
              <a class="footer-link" href="/leadership/">Leadership &amp; staff</a>
              <a class="footer-link" href="/academics/">Academic programmes</a>
              <a class="footer-link" href="/academics/#departments">Departments</a>
              <a class="footer-link" href="/gallery/">Gallery</a>
            </div>
          </div>

          <div class="footer-col">
            <p class="label-caps footer-col__title">Admissions &amp; news</p>
            <div class="footer-col__list">
              <a class="footer-link" href="/admissions/">How to apply</a>
              <a class="footer-link" href="/admissions/#fees">Fees 2027</a>
              <a class="footer-link" href="/news/">News</a>
              <a class="footer-link" href="/events/">Events calendar</a>
              <a class="footer-link" href="/faq/">Questions &amp; answers</a>
            </div>
          </div>

          <div class="footer-col">
            <p class="label-caps footer-col__title">Visit the office</p>
            <div class="footer-contact">
              <p class="footer-contact__row"><span class="label-caps footer-contact__key">Address</span>
                <span>%(address)s</span></p>
              <p class="footer-contact__row"><span class="label-caps footer-contact__key">Phone</span>
                <a class="footer-link" href="tel:%(phone_href)s">%(phone)s</a></p>
              <p class="footer-contact__row"><span class="label-caps footer-contact__key">Email</span>
                <a class="footer-link" href="mailto:%(email)s">%(email)s</a></p>
              <p class="footer-contact__row"><span class="label-caps footer-contact__key">Hours</span>
                <span>%(hours)s</span></p>
            </div>
          </div>
        </div>

        <div class="site-footer__bottom">
          <p>© %(year)s Dar es Salaam Islamic Seminary. All rights reserved.</p>
          <p class="site-footer__note">
            Photographs are the property of Dar es Salaam Islamic Seminary. To request a copy for
            publication, contact the office.
          </p>
        </div>
      </div>
    </footer>

%(lightbox)s
    <script src="/assets/js/site.js" defer></script>
  </body>
</html>
""" % {
        "title": esc(title), "description": esc(description), "og_image": esc(og_image),
        "fonts": FONTS, "nav": nav, "mobile": mobile, "lightbox": lightbox, "body": body,
        "address": esc(ADDRESS), "phone": esc(PHONE), "phone_href": esc(PHONE.replace(" ", "")),
        "email": esc(EMAIL), "hours": esc(OFFICE_HOURS), "year": "2026",
    }


LIGHTBOX = """    <div class="lightbox" data-lightbox-root role="dialog" aria-modal="true"
         aria-label="Photograph viewer" aria-hidden="true">
      <div class="lightbox__stage" data-lightbox-stage>
        <figure class="lightbox__figure">
          <img class="lightbox__img" data-lightbox-image alt="">
          <figcaption class="lightbox__caption" data-lightbox-caption></figcaption>
          <p class="lightbox__counter" data-lightbox-counter></p>
        </figure>
      </div>
      <button class="lightbox__close" type="button" data-lightbox-close aria-label="Close viewer">%s</button>
      <button class="lightbox__nav lightbox__nav--prev" type="button" data-lightbox-prev
              aria-label="Previous photograph">%s</button>
      <button class="lightbox__nav lightbox__nav--next" type="button" data-lightbox-next
              aria-label="Next photograph">%s</button>
    </div>""" % (ICON_CLOSE, ICON_PREV, ICON_NEXT)


# ----------------------------------------------------------- components ----
def eyebrow(num, label, rule=False):
    parts = ['<span class="eyebrow__num tnum">%s</span>' % esc(num),
             '<span class="label-caps eyebrow__label">%s</span>' % esc(label)]
    if rule:
        parts.append('<span class="lattice-rule rule-draw" aria-hidden="true"></span>')
    cls = "eyebrow eyebrow--rule reveal" if rule else "eyebrow reveal"
    return '<div class="%s">%s</div>' % (cls, "".join(parts))


def hero(num, label, title, lede, image=None, alt="", ctas=(), badge=None, variant=""):
    """Page hero. Pass image=None for the plain (no photograph) variant."""
    cls = "hero" + (" hero--plain" if image is None else "") + ((" " + variant) if variant else "")
    if image:
        media = ('<div class="hero__media"><img src="%s" alt="%s" fetchpriority="high" '
                 'decoding="async"></div><div class="hero__scrim" aria-hidden="true"></div>'
                 % (esc(image), esc(alt)))
    else:
        media = ""

    badge_html = ""
    if badge:
        text, past = badge
        badge_html = ('<p class="hero__badge%s reveal" style="--reveal-delay:0.05s">%s</p>'
                      % (" hero__badge--past" if past else "", esc(text)))

    cta_html = ""
    if ctas:
        links = []
        for cta_href, cta_label, cta_style in ctas:
            klass = "btn btn--onhero" + (" btn--back" if cta_style == "back" else "")
            icon = ICON_BACK if cta_style == "back" else ICON_ARROW
            links.append('<a class="%s" href="%s">%s%s</a>'
                         % (klass, esc(cta_href), esc(cta_label), icon))
        cta_html = ('<div class="hero__aside reveal" style="--reveal-delay:0.26s">%s</div>'
                    % "".join(links))

    return """      <section class="%(cls)s" aria-labelledby="hero-title">
%(media)s
        <div class="hero__inner shell">
          <div class="hero__brand reveal">
            <span class="hero__brand-mark" aria-hidden="true">DIS</span>
            <span class="label-caps hero__brand-name">%(site)s</span>
          </div>
          %(eyebrow)s
          <h1 class="hero__title reveal" id="hero-title" style="--reveal-delay:0.1s">%(title)s</h1>
          <p class="hero__lede reveal" style="--reveal-delay:0.18s">%(lede)s</p>
          %(badge)s
          %(cta)s
        </div>
      </section>""" % {
        "cls": cls, "media": media, "site": esc(SITE_NAME),
        "eyebrow": eyebrow(num, label), "title": esc(title), "lede": esc(lede),
        "badge": badge_html, "cta": cta_html,
    }


def section_head(num, label, title, lede=None):
    return '<header class="section-head">%s</header>' % section_head_inner(num, label, title, lede)


def section_head_inner(num, label, title, lede=None):
    """Section heading without the <header> wrapper, for nested use."""
    parts = [eyebrow(num, label, rule=True),
             '<h2 class="section-head__title reveal" style="--reveal-delay:0.08s">%s</h2>' % esc(title)]
    if lede:
        parts.append('<p class="section-head__lede reveal" style="--reveal-delay:0.14s">%s</p>' % esc(lede))
    return "".join(parts)


def section(inner, tight=False):
    cls = "section shell" + (" section--tight" if tight else "")
    return '      <section class="%s">%s</section>' % (cls, inner)


def stat(value, label):
    return ('<div class="stat reveal"><p class="stat__value tnum">%s</p>'
            '<p class="label-caps stat__label">%s</p></div>' % (esc(value), esc(label)))


def card(index, title, meta, text, href=None, link_label="View subjects", delay=0):
    body = ('<a class="card reveal" href="%s" style="--reveal-delay:%ss">'
            '<span class="card__index tnum">%s</span>'
            '<span class="card__title">%s</span>'
            '<span class="label-caps card__meta">%s</span>'
            '<span class="card__text">%s</span>'
            '<span class="card__foot">%s%s</span></a>'
            % (esc(href), delay, esc(index), esc(title), esc(meta), esc(text),
               esc(link_label), ICON_ARROW))
    if href:
        return body
    return ('<div class="card reveal" style="--reveal-delay:%ss">'
            '<span class="card__index tnum">%s</span>'
            '<h3 class="card__title">%s</h3>'
            '<p class="label-caps card__meta">%s</p>'
            '<p class="card__text">%s</p></div>'
            % (delay, esc(index), esc(title), esc(meta), esc(text)))


def step(num, title, meta, text, href=None, link_label="How to join", delay=0):
    link = ""
    if href:
        link = ('<p style="margin-top:0.9rem"><a class="card__foot" href="%s">%s%s</a></p>'
                % (esc(href), esc(link_label), ICON_ARROW))
    meta_html = ('<p class="label-caps card__meta" style="margin-top:0.4rem">%s</p>' % esc(meta)
                 if meta else "")
    return ('<div class="step reveal" style="--reveal-delay:%ss"><p class="step__num tnum">%s</p>'
            '<div><h3 class="step__title">%s</h3>%s<p class="step__text">%s</p>%s</div></div>'
            % (delay, esc(num), esc(title), meta_html, esc(text), link))


def value(num, title, text):
    return ('<div class="value reveal"><p class="value__num">%s</p>'
            '<h3 class="value__title">%s</h3><p class="value__text">%s</p></div>'
            % (esc(num), esc(title), esc(text)))


def staff_row(name, role, dept, bio):
    return ('<div class="staff__row reveal"><div><h3 class="staff__name">%s</h3>'
            '<p class="label-caps staff__role">%s</p><p class="label-caps staff__dept">%s</p></div>'
            '<p class="staff__bio">%s</p></div>'
            % (esc(name), esc(role), esc(dept), esc(bio)))


def news_card(item, delay=0):
    pin = '<span class="news-card__pin label-caps">Pinned</span>' if item.get("pinned") else ""
    tags = "".join('<li class="tag">%s</li>' % esc(t) for t in item.get("tags", []))
    return ('<a class="news-card reveal" href="/news/%s/" style="--reveal-delay:%ss">'
            '<span class="news-card__media"><img src="%s" alt="%s" loading="lazy" decoding="async"></span>'
            '<span class="news-card__meta label-caps"><span class="tnum">%s</span>'
            '<span>By %s</span>%s</span>'
            '<span class="news-card__title">%s</span>'
            '<span class="news-card__excerpt">%s</span>'
            '<ul class="news-card__tags">%s</ul></a>'
            % (esc(item["slug"]), delay, esc(item["image"]), esc(item["alt"]),
               esc(item["date"]), esc(item["author"]), pin, esc(item["title"]),
               esc(item["excerpt"]), tags))


def event_row(ev, delay=0):
    past = " event--past" if ev["status"] == "Past" else ""
    return ('<a class="event%s reveal" href="/events/%s/" style="--reveal-delay:%ss">'
            '<span class="event__date"><span class="event__date-day tnum">%s</span>'
            '<span class="label-caps event__date-month">%s</span>'
            '<span class="label-caps event__date-year tnum">%s</span></span>'
            '<span><span class="event__title">%s</span>'
            '<span class="label-caps event__when">%s</span>'
            '<span class="label-caps event__where">%s</span>'
            '<span class="event__text">%s</span></span>'
            '<span class="label-caps event__status">%s</span></a>'
            % (past, esc(ev["slug"]), delay, esc(ev["day"]), esc(ev["month"]), esc(ev["year"]),
               esc(ev["title"]), esc(ev["when"]), esc(ev["where"]), esc(ev["text"]),
               esc(ev["status"])))


def faq(question, answer):
    return ('<details class="faq reveal"><summary class="faq__summary">%s'
            '<span class="faq__icon" aria-hidden="true"></span></summary>'
            '<p class="faq__answer">%s</p></details>'
            % (esc(question), esc(answer)))


def channel(key, value_text, href=None, href_label=None):
    inner = ('<p class="label-caps channel__key">%s</p><p class="channel__value">%s</p>'
             % (esc(key), esc(value_text)))
    if href:
        return '<a class="channel reveal" href="%s">%s</a>' % (esc(href), inner)
    return '<div class="channel reveal">%s</div>' % inner


def kv_row(key, value_text, note=None):
    note_html = ' <span class="kv__note">%s</span>' % esc(note) if note else ""
    return ('<div class="kv__row reveal"><p class="kv__key">%s</p>'
            '<p class="kv__value tnum">%s%s</p></div>'
            % (esc(key), esc(value_text), note_html))


def cta(title, text, actions):
    links = []
    for href, label, style in actions:
        klass = "btn" + (" btn--dark" if style == "solid" else "")
        icon = ICON_ARROW
        links.append('<a class="%s" href="%s">%s%s</a>' % (klass, esc(href), esc(label), icon))
    return ('      <section class="cta"><div class="shell cta__inner">'
            '<div><h2 class="cta__title reveal">%s</h2><p class="cta__text reveal" '
            'style="--reveal-delay:0.08s">%s</p></div>'
            '<div class="cta__actions reveal" style="--reveal-delay:0.14s">%s</div>'
            '</div></section>' % (esc(title), esc(text), "".join(links)))


def album_row(album, delay=0):
    return ('<a class="album-row reveal" href="/gallery/%s/" style="--reveal-delay:%ss">'
            '<span class="album-row__thumb"><img src="%s" alt="%s" loading="lazy" decoding="async"></span>'
            '<span class="album-row__body"><span class="album-row__title">%s</span>'
            '<span class="album-row__desc">%s</span></span>'
            '<span class="album-row__meta"><span class="album-row__count tnum">%s</span>'
            '<span class="label-caps album-row__count-label">photos</span>'
            '<span class="album-row__arrow" aria-hidden="true">%s</span></span></a>'
            % (esc(album["slug"]), delay, esc(album["cover"]), esc(album["cover_alt"]),
               esc(album["title"]), esc(album["desc"]), esc(len(album["photos"])), ICON_ARROW))


def photo(photo_item, index, total, wide=False, delay=0):
    caption = photo_item["caption"]
    return ('<figure class="photo%s reveal" style="--reveal-delay:%ss">'
            '<button class="photo__frame" type="button" data-lightbox data-src="%s" '
            'data-caption="%s" aria-label="Open photograph %s of %s: %s">'
            '<img src="%s" alt="%s" loading="lazy" decoding="async">'
            '<span class="photo__hint" aria-hidden="true">View</span></button>'
            '<figcaption class="photo__caption"><span class="photo__index tnum">%02d</span>%s</figcaption>'
            '</figure>'
            % (" photo--wide" if wide else "", delay, esc(photo_item["src"]), esc(caption),
               index, total, esc(caption), esc(photo_item["src"]), esc(caption), index, esc(caption)))


# =====================================================================
#  CONTENT
# =====================================================================
PROGRAMMES = [
    ("01", "Primary School", "Primary · Standard 1 – 7",
     "Foundation literacy, numeracy and Qur'an, with class teachers who keep the same cohort "
     "through all seven years."),
    ("02", "O-Level (Form 1–4)", "Secondary · 4 years",
     "The full national curriculum toward CSEE, with streamed sciences, Kiswahili, Arabic and a "
     "compulsory study skills period."),
    ("03", "A-Level (Form 5–6)", "Advanced · 2 years",
     "PCM, PCM+ICT and arts combinations toward ACSEE, with a university mentoring tutorial each Friday."),
    ("04", "Hifz & Arabic Programme", "Complementary · Rolling",
     "Morning memorisation circle and Arabic conversation, open to all levels alongside the national "
     "curriculum."),
]

VALUES = [
    ("i", "Adab before achievement",
     "Manners are taught first. A learner who cannot greet a stranger respectfully has not finished "
     "their education, however high the marks."),
    ("ii", "Reason tested by practice",
     "Every science term carries practical hours, every language term carries a debate, and every "
     "claim in class is expected to carry evidence."),
    ("iii", "Service as a requirement",
     "Two afternoons a month are spent off campus — the clinic queue, the mosque compound, the ward "
     "at Temeke. Service is recorded, not optional."),
]

DEPARTMENTS = [
    {
        "slug": "sciences", "name": "Sciences", "count": "4 subjects",
        "text": "Chemistry, biology and physics with a practical block of three fitted laboratories "
                "and an afternoon science club.",
        "head": "Ms. Neema Shayo · Head of Sciences",
        "subjects": [("011", "Basic Mathematics"), ("031", "Physics"),
                     ("032", "Chemistry"), ("033", "Biology")],
    },
    {
        "slug": "mathematics-ict", "name": "Mathematics & ICT", "count": "3 subjects",
        "text": "Mathematics, additional mathematics and computer studies, including the Form 1–6 "
                "programming club.",
        "head": "Mr. Baraka Mushi · Head of Mathematics",
        "subjects": [("041", "Additional Mathematics"), ("072", "Computer Studies"),
                     ("073", "Statistics")],
    },
    {
        "slug": "languages", "name": "Languages", "count": "3 subjects",
        "text": "English, Kiswahili and French, with the debating society and the school newspaper "
                "run out of this department.",
        "head": "Ms. Zainabu Ally · Head of Languages",
        "subjects": [("021", "English Language"), ("022", "Kiswahili"), ("023", "French")],
    },
    {
        "slug": "islamic-studies-arabic", "name": "Islamic Studies & Arabic", "count": "4 subjects",
        "text": "Qur'an, hadith, fiqh, Arabic grammar and the morning hifz circle.",
        "head": "Ustadh Hamad Juma · Head of Islamic Studies",
        "subjects": [("101", "Qur'an & Tajwid"), ("102", "Arabic Grammar"),
                     ("103", "Hadith & Fiqh"), ("104", "Islamic History")],
    },
    {
        "slug": "history-civics-geography", "name": "Humanities", "count": "4 subjects",
        "text": "History, civics, geography and basic economics, including the Model UN delegation.",
        "head": "Mr. Joseph Kimaro · Head of Humanities",
        "subjects": [("022", "History"), ("024", "Civics"),
                     ("023", "Geography"), ("051", "Basic Economics")],
    },
]

STAFF = [
    ("Dr. Amina Mwinyi", "Headmaster", "Office of the Headmaster",
     "Twenty-two years in Tanzanian secondary education, four of them as a district school "
     "inspector. Leads the A-level tutorial programme and the alumni bursary fund."),
    ("Mr. Joseph Kimaro", "School Administrator", "Administration",
     "Runs the office, the admissions desk and the school calendar. The first person most families meet."),
    ("Ms. Neema Shayo", "Head of Sciences", "Sciences",
     "Physics teacher and science club patron; supervised the fit-out of the new laboratory block."),
    ("Ustadh Hamad Juma", "Head of Islamic Studies", "Islamic Studies & Arabic",
     "Leads the morning hifz circle and the school's Qur'an competition delegation."),
    ("Ms. Zainabu Ally", "Head of Languages", "Languages",
     "Kiswahili and English teacher; patron of the debating society and the school newspaper."),
    ("Mr. Baraka Mushi", "Head of Mathematics", "Mathematics & ICT",
     "Teaches additional mathematics and runs the Form 1–6 programming club."),
]

ADMISSION_STEPS = [
    ("01", "Collect or download the form",
     "Pick up the application form from the school office on Mwai Kibaki Road, or ask for it by "
     "email. The form is free of charge for the first issue."),
    ("02", "Complete and attach documents",
     "Fill in every field, attach the birth certificate, previous report card and two passport "
     "photographs. Incomplete forms are not assessed."),
    ("03", "Pay the assessment fee",
     "TZS 20,000 per candidate, paid at the bursar's office or by mobile money. Keep the receipt — "
     "it is your entry ticket to the test."),
    ("04", "Sit the entrance test and interview",
     "Tests run on the announced dates at 08:00. Report with the receipt, a pen and a ruler. "
     "Interviews follow the same morning for shortlisted candidates."),
    ("05", "Offer and enrolment",
     "Results are released within ten working days by SMS and at the office. Confirm the place "
     "within seven days by paying the first instalment to complete enrolment."),
]

FEES = [
    ("Primary", "TZS 900,000", "per year"),
    ("O-level (Form 1–4)", "TZS 1,350,000", "per year"),
    ("A-level (Form 5–6)", "TZS 1,650,000", "per year"),
    ("Boarding supplement", "TZS 780,000", "per year · hostel, two meals, evening prep"),
    ("One-off joining cost", "TZS 60,000", "uniform inspection, ID, orientation"),
]

NEWS = [
    {
        "slug": "dis-takes-second-place-regional-quran-competition",
        "title": "DIS takes second place at the Dar es Salaam regional Qur'an competition",
        "date": "19 September 2026", "author": "Super Administrator", "pinned": True,
        "image": "/assets/img/assembly.jpg",
        "alt": "Whole school gathered for morning assembly in the covered hall",
        "excerpt": "Twelve students represented the school at the regional tilawa and hifz "
                   "competition at the end of last month, returning with two individual medals "
                   "and second place overall.",
        "tags": ["students", "quran", "achievement"],
        "body": [
            "Twelve students represented the school at the regional tilawa and hifz competition, "
            "held this year at the Mnazi Mmoja grounds. Form 3 student Salma Ramadhani took second "
            "place in the 15-juz memorisation category; Form 5's Yusuf Mangi placed third in recitation.",
            "The delegation was accompanied by Ustadh Hamad Juma and Ms. Fatma Ally. “Preparation was "
            "ninety percent their own time,” Ms. Ally said. “They met at 04:30 for six weeks. What the "
            "school gave them was a quiet room and someone to hear them.”",
            "The school now qualifies for the national round in Dodoma in October.",
        ],
    },
    {
        "slug": "new-science-laboratory-block-opens",
        "title": "New science laboratory block opens for Form 5",
        "date": "19 September 2026", "author": "Super Administrator", "pinned": False,
        "image": "/assets/img/studyhall.jpg",
        "alt": "Students working at desks in the DIS study hall",
        "excerpt": "Three fitted laboratories — chemistry, biology and physics — came into use this "
                   "term, doubling the practical hours available to A-level science candidates.",
        "tags": ["sciences", "facilities", "A-level"],
        "body": [
            "Three fitted laboratories — chemistry, biology and physics — came into use this term, "
            "doubling the practical hours available to A-level science candidates. The block was "
            "funded over four years by alumni contributions in Mwanza and Dar es Salaam, with "
            "equipment supplied through the national textbook and apparatus scheme.",
            "Head of Sciences Ms. Neema Shayo says the difference is already visible: “Our candidates "
            "used to share one bench between four students. Now every pair has a bench, a fume "
            "cupboard for the chemistry sets, and enough titration work to stop treating practicals "
            "as a last-minute rehearsal.”",
            "The laboratory is supervised after hours by two technicians and is open to O-level "
            "students on Wednesday afternoons for club work.",
        ],
    },
    {
        "slug": "term-3-calendar-examinations-sports-day-parents-meeting",
        "title": "Term 3 calendar: examinations, sports day and the parents' meeting",
        "date": "12 September 2026", "author": "Super Administrator", "pinned": False,
        "image": "/assets/img/gate.jpg",
        "alt": "The open entrance gate of the campus at golden hour",
        "excerpt": "A summary of the dates families have asked about most: mock examinations, the "
                   "inter-house sports day, and the A-level parents' meeting.",
        "tags": ["calendar", "parents", "examinations"],
        "heading": "Dates for the diary",
        "list": [
            "<strong>Mock examinations</strong> — 6 to 17 October, morning sessions from 08:00. "
            "Candidates must be seated by 07:45.",
            "<strong>Inter-house sports day</strong> — 24 October at the school field. Houses: "
            "Mwanga, Uhuru, Amani and Tumaini. Parents are welcome from 08:30.",
            "<strong>A-level parents' meeting</strong> — 31 October, 10:00 in the library. Form 5 "
            "and 6 subject teachers will be present for individual ten-minute consultations.",
            "<strong>Fee instalment deadline</strong> — 15 October for the second instalment.",
        ],
        "body": [
            "The office will send the same dates by SMS to the number registered against each "
            "student. If your number has changed, tell the bursar's office before 10 October.",
        ],
    },
]

EVENTS = [
    {
        "slug": "inter-house-sports-day", "title": "Inter-house sports day",
        "day": "06", "month": "Oct", "year": "2026",
        "when": "6 October 2026 · 09:30", "where": "School field, Mwai Kibaki Road",
        "status": "Upcoming", "date_label": "Tuesday, 6 October 2026",
        "text": "Houses Mwanga, Uhuru, Amani and Tumaini compete in track and field. Parents welcome "
                "from 08:30; refreshments sold at the pavilion.",
        "calendar": "https://calendar.google.com/calendar/render?action=TEMPLATE&text=Inter-house%20sports%20day&dates=20261006T093000Z/20261006T160000Z&location=School%20field%2C%20Mwai%20Kibaki%20Road&details=Houses%20Mwanga%2C%20Uhuru%2C%20Amani%20and%20Tumaini%20compete%20in%20track%20and%20field.%20Parents%20welcome%20from%2008%3A30%3B%20refreshments%20sold%20at%20the%20pavilion.",
    },
    {
        "slug": "a-level-parents-meeting", "title": "A-level parents' meeting",
        "day": "15", "month": "Oct", "year": "2026",
        "when": "15 October 2026 · 10:00", "where": "School library",
        "status": "Upcoming", "date_label": "Thursday, 15 October 2026",
        "text": "Term progress, university guidance and individual consultations with Form 5 and 6 "
                "subject teachers in the library.",
        "calendar": "https://calendar.google.com/calendar/render?action=TEMPLATE&text=A-level%20parents%27%20meeting&dates=20261015T100000Z/20261015T130000Z&location=School%20library&details=Term%20progress%2C%20university%20guidance%20and%20individual%20consultations%20with%20Form%205%20and%206%20subject%20teachers%20in%20the%20library.",
    },
    {
        "slug": "open-day-prospective-form-1", "title": "Open day for prospective Form 1 families",
        "day": "26", "month": "Oct", "year": "2026",
        "when": "26 October 2026 · 08:00", "where": "Main courtyard",
        "status": "Upcoming", "date_label": "Monday, 26 October 2026",
        "text": "Tour the laboratories, meet the Headmaster and the boarding team, and collect the "
                "application form. No appointment needed.",
        "calendar": "https://calendar.google.com/calendar/render?action=TEMPLATE&text=Open%20day%20for%20prospective%20Form%201%20families&dates=20261026T080000Z/20261026T120000Z&location=Main%20courtyard&details=Tour%20the%20laboratories%2C%20meet%20the%20Headmaster%20and%20the%20boarding%20team%2C%20and%20collect%20the%20application%20form.%20No%20appointment%20needed.",
    },
    {
        "slug": "graduation-prize-giving", "title": "Graduation and prize giving",
        "day": "15", "month": "Aug", "year": "2026",
        "when": "15 August 2026 · 10:00", "where": "Covered assembly hall",
        "status": "Past", "date_label": "Saturday, 15 August 2026",
        "text": "The leaving cohort receives certificates, followed by prizes for academics, Qur'an "
                "recitation and service.",
        "calendar": "https://calendar.google.com/calendar/render?action=TEMPLATE&text=Graduation%20and%20prize%20giving&dates=20260815T100000Z/20260815T140000Z&location=Covered%20assembly%20hall&details=The%20leaving%20cohort%20receives%20certificates%2C%20followed%20by%20prizes%20for%20academics%2C%20Qur%27an%20recitation%20and%20service.",
    },
    {
        "slug": "science-club-exhibition", "title": "Science club exhibition",
        "day": "20", "month": "Jun", "year": "2026",
        "when": "20 June 2026 · 14:00", "where": "Science laboratory block",
        "status": "Past", "date_label": "Saturday, 20 June 2026",
        "text": "Form 3 and 4 present the term's projects — water testing, simple circuits and the "
                "school garden soil survey.",
        "calendar": "https://calendar.google.com/calendar/render?action=TEMPLATE&text=Science%20club%20exhibition&dates=20260620T140000Z/20260620T170000Z&location=Science%20laboratory%20block&details=Form%203%20and%204%20present%20the%20term%27s%20projects%20%E2%80%94%20water%20testing%2C%20simple%20circuits%20and%20the%20school%20garden%20soil%20survey.",
    },
]

ALBUMS = [
    {
        "slug": "campus-courtyard", "title": "Campus & courtyard",
        "desc": "The arcade, the yard and the everyday architecture of the school.",
        "cover": "/assets/img/courtyard.jpg", "cover_alt": "The school arcade at dawn",
        "photos": [
            {"src": "/assets/img/courtyard.jpg",
             "caption": "The school arcade at dawn, arches casting long shadows across the swept courtyard"},
            {"src": "/assets/img/carveddoor.jpg",
             "caption": "Carved lattice detail on a Swahili coast door"},
            {"src": "/assets/img/gate.jpg",
             "caption": "The open entrance gate of the campus at golden hour"},
        ],
    },
    {
        "slug": "study-classroom", "title": "Study & classroom",
        "desc": "Learners at work in classrooms, the library and evening prep.",
        "cover": "/assets/img/studyhall.jpg",
        "cover_alt": "Students at wooden desks in the study hall",
        "photos": [
            {"src": "/assets/img/studyhall.jpg",
             "caption": "Students at wooden desks in the study hall, morning light through louvered windows"},
            {"src": "/assets/img/assembly.jpg",
             "caption": "Whole school gathered for morning assembly in the covered hall"},
        ],
    },
    {
        "slug": "assembly-ceremony", "title": "Assembly & ceremony",
        "desc": "Morning assembly, prize giving and graduation days.",
        "cover": "/assets/img/assembly.jpg",
        "cover_alt": "Whole school gathered for morning assembly",
        "photos": [
            {"src": "/assets/img/assembly.jpg",
             "caption": "Whole school gathered for morning assembly in the covered hall"},
            {"src": "/assets/img/courtyard.jpg",
             "caption": "Students lining up in the courtyard before assembly"},
        ],
    },
    {
        "slug": "around-the-school", "title": "Around the school",
        "desc": "The gate, the grounds and details from around the compound.",
        "cover": "/assets/img/gate.jpg",
        "cover_alt": "The open entrance gate at golden hour",
        "photos": [
            {"src": "/assets/img/gate.jpg",
             "caption": "The campus gate at the end of the school day"},
            {"src": "/assets/img/studyhall.jpg",
             "caption": "Evening prep in the upper-form study hall"},
            {"src": "/assets/img/carveddoor.jpg",
             "caption": "Close detail of the carved door at the main office"},
        ],
    },
]

FAQ_GROUPS = [
    ("01", "Admissions", [
        ("When do applications open?",
         "Applications for the January intake open in March and are reviewed as they arrive until "
         "the closing date of 14 August. A rolling intake is possible when a place falls vacant — "
         "call the office to ask."),
        ("Is there an entrance examination?",
         "Yes. Form 1 and Form 5 candidates sit a written assessment in English, Kiswahili and "
         "Mathematics (plus sciences for A-level), followed by a short interview with the Headmaster."),
    ]),
    ("02", "Fees", [
        ("Can fees be paid in instalments?",
         "Fees are charged annually and payable in two instalments: 60 percent at the start of the "
         "year and 40 percent by 15 October. Mobile money and bank transfer are both accepted."),
        ("Are bursaries available?",
         "Twenty to thirty bursaries covering 25 to 100 percent of fees are awarded each March on "
         "merit and need. Collect the bursary form from the office in February."),
    ]),
    ("03", "Joining", [
        ("What uniform is required?",
         "Navy skirt or shorts, white shirt with the school crest, and the striped tie. Uniform can "
         "be bought at the bursar's office on orientation day."),
    ]),
    ("04", "School life", [
        ("Does the school offer boarding?",
         "Yes. Two hostels accommodate O-level and A-level boarders with evening prep supervised "
         "until 20:30. The boarding supplement is TZS 780,000 per year."),
        ("What languages are taught?",
         "English is the medium of instruction from Standard 4. Kiswahili, Arabic and French are "
         "taught as subjects; the hifz circle runs in Arabic."),
    ]),
    ("05", "Transport", [
        ("Is there a school bus?",
         "A minibus serves Mikocheni, Mbezi Beach, Tegeta, Kinondoni and Kariakoo on a published "
         "route. Places are allocated first-come, first-served each term."),
    ]),
]


# =====================================================================
#  PAGES
# =====================================================================
def page_home():
    body = [hero("01", "Welcome",
                 "Knowledge, character and service since 1998.",
                 "Dar es Salaam Islamic Seminary is a day and boarding school serving families "
                 "across Dar es Salaam, Pwani and the Zanzibar archipelago — the national "
                 "curriculum in full, taught inside a framework of adab.",
                 image="/assets/img/courtyard.jpg",
                 alt="The courtyard colonnade in early morning light",
                 ctas=[("/admissions/", "Apply for 2027", "solid"),
                       ("/gallery/", "See the gallery", "ghost")])]

    stats = "".join([
        stat("1998", "Founded in Mikocheni"),
        stat("≈900", "Learners today"),
        stat("14,000", "Volumes in the library"),
        stat("05", "Academic departments"),
    ])
    body.append('      <div class="stats">%s</div>' % stats)

    cards = "".join(card(num, title, meta, text, delay=i * 0.06)
                    for i, (num, title, meta, text) in enumerate(PROGRAMMES))
    body.append(section(section_head("02", "Programmes", "Where a learner joins us.")
                        + '        <div class="cards cards--3">%s</div>' % cards))

    values = "".join(value(num, title, text) for num, title, text in VALUES)
    body.append(section(section_head("03", "Values", "Rules written into the first prospectus.")
                        + '        <div class="values">%s</div>'
                          '        <p class="callout reveal" style="margin-top:clamp(2rem,4vw,3rem)">'
                          'Adab (character) before achievement. Knowledge is tested by practice. '
                          'Service is not optional. Discipline is a form of respect. Curiosity is '
                          'encouraged, never punished.</p>' % values))

    dept_cards = "".join(
        card("%02d" % (i + 1), d["name"], d["head"], d["text"],
             href="/departments/%s/" % d["slug"], delay=i * 0.06)
        for i, d in enumerate(DEPARTMENTS))
    body.append(section(section_head("04", "Departments",
                                     "Five departments, every subject accounted for.",
                                     "Each department lists its subjects and its head. DIS publishes "
                                     "these from the staff portal.")
                        + '        <div class="cards cards--3">%s</div>' % dept_cards))

    news_cards = "".join(news_card(item, delay=i * 0.06) for i, item in enumerate(NEWS))
    body.append(section(section_head("05", "News", "Latest first.")
                        + '        <div class="cards cards--3">%s</div>'
                          '        <p style="margin-top:2rem"><a class="btn" href="/news/">'
                          'All news%s</a></p>' % (news_cards, ICON_ARROW)))

    upcoming = [e for e in EVENTS if e["status"] == "Upcoming"]
    rows = "".join(event_row(ev, delay=i * 0.06) for i, ev in enumerate(upcoming))
    body.append(section(section_head("06", "Events", "Next on the calendar.")
                        + '        <div>%s</div>'
                          '        <p style="margin-top:2rem"><a class="btn" href="/events/">'
                          'Full calendar%s</a></p>' % (rows, ICON_ARROW)))

    albums = "".join(album_row(a, delay=i * 0.06) for i, a in enumerate(ALBUMS))
    body.append(section(section_head("07", "Gallery", "The school as it actually looks.")
                        + '        <div class="album-list">%s</div>' % albums))

    body.append(cta("Applications for the coming academic year close on 14 August 2026.",
                    "Forms are reviewed as they arrive. The admissions desk answers calls between "
                    "07:30 and 16:30 on weekdays — WhatsApp is the fastest way to reach us during "
                    "the intake season.",
                    [("/admissions/", "How to apply", "solid"),
                     ("/contact/", "Ask the office", "ghost")]))
    return document("Dar es Salaam Islamic Seminary",
                    "Dar es Salaam Islamic Seminary — a day and boarding school in Dar es Salaam "
                    "teaching the national curriculum in full inside a framework of adab. "
                    "Knowledge, character and service since 1998.",
                    "/", "\n".join(body))


def page_about():
    body = [hero("01", "About the seminary",
                 "Twenty-seven years of teaching between the coast road and the palm line.",
                 "Knowledge, character and service since 1998",
                 image="/assets/img/studyhall.jpg",
                 alt="Students studying in the DIS study hall in morning light")]

    prose = ('        <div class="dis-prose article__body reveal">'
             '<p>Dar es Salaam Islamic Seminary (DIS) is a day and boarding school serving families '
             'across Dar es Salaam, Pwani and the Zanzibar archipelago. We teach the national '
             'curriculum in full, and we teach it inside a framework of adab — manners, discipline '
             'and service — so that a DIS learner leaves able to argue a case, run an experiment '
             'and lead a community.</p>'
             '<p>Classes are kept below forty learners. Every form has a class teacher who knows '
             'each student by name, and the sixth-form tutorial programme pairs A-level students '
             'with a mentor from the university faculties in Dar es Salaam.</p></div>')
    body.append(section(section_head("02", "Who we are", "What a DIS education is for.") + prose))

    values = "".join(value(num, title, text) for num, title, text in VALUES)
    body.append(section(section_head("03", "Values", "Four rules written into the first prospectus.")
                        + '        <div class="values">%s</div>'
                          '        <p class="callout reveal" style="margin-top:clamp(2rem,4vw,3rem)">'
                          'Adab (character) before achievement. Knowledge is tested by practice. '
                          'Service is not optional. Discipline is a form of respect. Curiosity is '
                          'encouraged, never punished.</p>' % values))

    history = ('        <div class="split"><div class="dis-prose article__body reveal">'
               '<p><img src="/assets/img/gate.jpg" alt="The entrance gate of the DIS campus at '
               'golden hour" loading="lazy" decoding="async"></p>'
               '<p>The seminary opened in September 1998 in four rented rooms in Mikocheni with 46 '
               'pupils and three teachers. The founding committee — two teachers, a retired civil '
               'servant and the imam of the neighbouring mosque — wrote a single sentence into the '
               'first prospectus: <em>enter in knowledge, leave in service.</em></p>'
               '<p>The first Form Four cohort sat the CSEE in 2002 and passed at 91 percent. The '
               'A-level stream followed in 2006, and the science laboratory block — funded by alumni '
               'in Mwanza and Dar es Salaam — opened in 2011. Today DIS teaches just under nine '
               'hundred learners across primary, O-level and A-level, and has sent graduates to the '
               'University of Dar es Salaam, Muhimbili, Sokoine and universities in Egypt, Malaysia '
               'and the United Kingdom.</p>'
               '<p>The school moved to its present campus off Mwai Kibaki Road in 2009: eight '
               'classrooms, three laboratories, a library of 14,000 volumes, two hostels and the '
               'courtyard arcade that has become the school\'s signature.</p>'
               '<p class="cta__actions" style="margin-top:2rem">'
               '<a class="btn" href="/leadership/">Meet the leadership%s</a>'
               '<a class="btn" href="/academics/">Academic programmes%s</a></p>'
               '</div>'
               '<aside class="split__aside"><div class="panel reveal">'
               '<p class="label-caps footer-col__title">Milestones</p>'
               '<div class="kv">%s</div></div></aside></div>')
    milestones = "".join([
        kv_row("Founded", "September 1998", "four rented rooms, 46 pupils"),
        kv_row("First CSEE cohort", "2002", "91 percent pass rate"),
        kv_row("A-level stream", "2006"),
        kv_row("Science laboratory block", "2011"),
        kv_row("Present campus", "2009", "off Mwai Kibaki Road"),
    ])
    body.append(section(section_head("04", "History", "From four rented rooms in 1998.")
                        + history % (ICON_ARROW, ICON_ARROW, milestones)))
    return document("About DIS",
                    "Dar es Salaam Islamic Seminary is a day and boarding school serving families "
                    "across Dar es Salaam, Pwani and the Zanzibar archipelago, teaching the "
                    "national curriculum in full inside a framework of adab since 1998.",
                    "/about/", "\n".join(body))


def page_leadership():
    body = [hero("01", "Leadership", "The people who answer for this school.",
                 "Every name below teaches, supervises or keeps the office running. Doors are open "
                 "during office hours.",
                 image="/assets/img/courtyard.jpg",
                 alt="The DIS courtyard colonnade at dawn")]
    rows = "".join(staff_row(*s) for s in STAFF)
    body.append(section(section_head("02", "Staff", "Heads of department and office.",
                                     "Positions and departments are maintained by the staff "
                                     "themselves in the DIS portal, so this page is never out of date.")
                        + '        <div class="staff">%s</div>' % rows))
    body.append(cta("Need to reach a specific desk?",
                    "The office routes calls and messages to the right person during office hours.",
                    [("/contact/", "Contact the office", "solid"),
                     ("/academics/#departments", "Departments", "ghost")]))
    return document("Leadership",
                    "The headmaster, school administrator and heads of department at Dar es Salaam "
                    "Islamic Seminary.",
                    "/leadership/", "\n".join(body))


def page_academics():
    body = [hero("01", "Academics", "Four programmes, one standard.",
                 "The national curriculum in full, taught in classes under forty, with Arabic and "
                 "Qur'an living beside chemistry and mathematics.",
                 image="/assets/img/studyhall.jpg",
                 alt="Learners at desks in the DIS study hall")]

    steps = "".join(
        step(num, title, meta, text, href="/admissions/", link_label="How to join")
        for num, title, meta, text in PROGRAMMES)
    body.append(section(section_head("02", "Programmes", "Where a learner joins us.")
                        + '        <div class="steps">%s</div>' % steps))

    cards = "".join(
        card("%02d" % (i + 1), d["name"], d["head"], d["text"],
             href="/departments/%s/" % d["slug"], delay=i * 0.06)
        for i, d in enumerate(DEPARTMENTS))
    body.append(section(section_head("03", "Departments",
                                     "Five departments, every subject accounted for.",
                                     "Each department lists its subjects and its head. DIS publishes "
                                     "these from the staff portal.")
                        + '        <div class="cards cards--3" id="departments">%s</div>' % cards))
    body.append(cta("Applications for the coming academic year close on 14 August 2026.",
                    "Collect a form at the office on Mwai Kibaki Road, or ask the admissions desk "
                    "to send one by email.",
                    [("/admissions/", "How to apply", "solid"),
                     ("/faq/", "Admissions questions", "ghost")]))
    return document("Academic programmes",
                    "Primary, O-level, A-level and the hifz & Arabic programme at Dar es Salaam "
                    "Islamic Seminary, plus the five academic departments.",
                    "/academics/", "\n".join(body))


def page_department(dept, index):
    body = [hero("01", "Department", dept["name"], dept["text"],
                 image="/assets/img/carveddoor.jpg",
                 alt="Carved geometric lattice detail",
                 ctas=[("/academics/#departments", "All departments", "back")])]
    subjects = "".join(
        '<div class="kv__row reveal"><p class="kv__key">%s</p>'
        '<p class="kv__value">%s</p></div>' % (esc(code), esc(name))
        for code, name in dept["subjects"])
    body.append(section(section_head("02", "Subjects", "What is taught here.")
                        + '        <div class="kv">%s</div>'
                          '        <div class="split" style="margin-top:clamp(2rem,4vw,3rem)">'
                          '<div><p class="label-caps footer-col__title">Head of department</p>'
                          '<p class="callout" style="margin-top:0.75rem">%s</p></div>'
                          '<aside class="split__aside"><div class="panel reveal">'
                          '<p class="label-caps footer-col__title">Subjects offered</p>'
                          '<p class="stat__value tnum">%02d</p>'
                          '<p class="card__text">Subjects listed by the department in the DIS staff '
                          'portal.</p></div></aside></div>'
                        % (subjects, esc(dept["head"]), len(dept["subjects"]))))
    body.append(cta("Questions about a subject or a combination?",
                    "The office will put you in touch with the head of department.",
                    [("/contact/", "Ask the office", "solid"),
                     ("/academics/", "All programmes", "ghost")]))
    return document("%s department" % dept["name"],
                    "%s at Dar es Salaam Islamic Seminary: %s" % (dept["name"], dept["text"]),
                    "/academics/#departments", "\n".join(body),
                    og_image="/assets/img/carveddoor.jpg")


def page_admissions():
    body = [hero("01", "Admissions", "How to apply, in five steps.",
                 "Applications for the coming academic year close on 14 August 2026. Forms are "
                 "reviewed as they arrive.",
                 image="/assets/img/gate.jpg",
                 alt="The open campus gate at golden hour")]

    facts = ('        <div class="stats">'
             + stat("14 Aug 2026", "Application deadline")
             + stat("TZS 20,000", "Assessment fee")
             + stat("07:30–16:30", "Admissions desk, weekdays")
             + stat("+255 754 100 220", "Admissions telephone")
             + '</div>')
    body.append(facts)

    steps = "".join(step(num, title, "", text, delay=i * 0.05)
                    for i, (num, title, text) in enumerate(ADMISSION_STEPS))
    body.append(section(section_head("02", "The process", "From the form to the first day.",
                                     "The admissions desk answers calls between 07:30 and 16:30 on "
                                     "weekdays. WhatsApp is the fastest way to reach us during the "
                                     "intake season.")
                        + '        <div class="steps">%s</div>'
                          '        <p class="cta__actions" style="margin-top:2rem">'
                          '<a class="btn btn--dark" href="/contact/">Ask the admissions office%s</a>'
                          '<a class="btn" href="/faq/">Admissions questions%s</a></p>'
                        % (steps, ICON_ARROW, ICON_ARROW)))

    requirements = ('        <div class="split"><div class="dis-prose article__body reveal">'
                    '<h2>Entry requirements</h2><ul>'
                    '<li><strong>Primary (Standard 1–7):</strong> birth certificate and the previous '
                    'school report card.</li>'
                    '<li><strong>Form 1 (O-level):</strong> completed primary school with a strong '
                    'CSEE result; a written entrance test in English, Kiswahili and Mathematics.</li>'
                    '<li><strong>Form 5 (A-level):</strong> CSEE with a minimum of four passes '
                    'including Mathematics and English, plus an interview. Science combinations '
                    'require a pass in Basic Mathematics.</li>'
                    '<li><strong>Transfers:</strong> a leaving certificate from the previous school '
                    'and, for A-level, a subject-by-subject statement of results.</li></ul>'
                    '<p>All candidates sit an entrance assessment and, for O-level and A-level, an '
                    'interview with the Headmaster.</p>'
                    '<h2>Documents required</h2><ul>'
                    '<li>Birth certificate</li><li>Previous school report card</li>'
                    '<li>Leaving certificate (transfers)</li><li>Two passport photographs</li>'
                    '<li>National ID or NIN for A-level candidates</li>'
                    '<li>Medical record for boarding applicants</li></ul>'
                    '</div>'
                    '<aside class="split__aside"><div class="panel reveal">'
                    '<p class="label-caps footer-col__title">Message the office</p>'
                    '<p class="card__text">Send a WhatsApp message and the admissions desk will '
                    'reply with the form and the current intake dates.</p>'
                    '<a class="btn btn--dark" href="https://wa.me/255754100220">WhatsApp the office%s</a>'
                    '</div></aside></div>' % ICON_ARROW)
    body.append(section(section_head("03", "Requirements", "What each candidate needs.")
                        + requirements))

    fees = ('        <div id="fees"><div class="split"><div class="section-head">'
            + section_head_inner("03", "Fees 2027", "Two instalments a year.")
            + '        <p class="section-head__lede reveal" style="margin-bottom:1.5rem">Fees are '
              'payable in two instalments per academic year. Prices are in Tanzanian shillings.</p>'
            + '<div class="kv">%s</div>' % "".join(kv_row(k, v, n) for k, v, n in FEES)
            + '</div><aside class="split__aside"><div class="panel reveal">'
              '<p class="label-caps footer-col__title">Bursaries &amp; discounts</p>'
              '<p class="card__text">Sibling discount of 10 percent from the second child. Bursaries '
              'covering 25–100 percent of fees are awarded each March on academic merit and '
              'financial need; ask at the office for the bursary form.</p>'
              '<a class="btn" href="/faq/">Fee questions%s</a></div></aside></div></div>'
            % ICON_ARROW)
    body.append(section(fees))

    office = ('        <div class="split"><div class="dis-prose article__body reveal">'
              '<h2>Collect a form at the office on DIS</h2>'
              '<p>%s</p>'
              '<p>Bring the candidate\'s birth certificate if you would like the form checked '
              'before you leave. The office is open Monday to Friday, 07:30 – 16:30, and on '
              'Saturday mornings for admissions only.</p>'
              '<p><a class="btn" href="/contact/">Plan your visit%s</a></p></div>'
              '<aside class="split__aside"><div class="panel reveal">'
              '<p class="label-caps footer-col__title">Key dates</p><div class="kv">'
              '%s</div></div></aside></div>')
    key_dates = "".join([
        kv_row("Applications close", "14 August 2026"),
        kv_row("Second fee instalment", "15 October"),
        kv_row("Bursary forms available", "February"),
        kv_row("Bursaries awarded", "March"),
    ])
    body.append(section(section_head("04", "Visit", "Collect a form at the office.")
                        + office % (esc(ADDRESS), ICON_ARROW, key_dates)))
    return document("Admissions",
                    "How to apply to Dar es Salaam Islamic Seminary in five steps: the form, "
                    "documents, the assessment fee, the entrance test and interview, and enrolment. "
                    "Applications close 14 August 2026.",
                    "/admissions/", "\n".join(body), og_image="/assets/img/gate.jpg")


def page_news():
    body = [hero("01", "News", "Reports from the compound.",
                 "Results, buildings, competitions and the calendar — written by the staff who were "
                 "there.",
                 image="/assets/img/assembly.jpg",
                 alt="Morning assembly in the covered hall")]
    cards = "".join(news_card(item, delay=i * 0.06) for i, item in enumerate(NEWS))
    body.append(section(section_head("02", "All articles", "Latest first.")
                        + '        <div class="cards cards--3">%s</div>' % cards))
    return document("News",
                    "Reports from Dar es Salaam Islamic Seminary: results, buildings, competitions "
                    "and the school calendar.",
                    "/news/", "\n".join(body), og_image="/assets/img/assembly.jpg")


def page_article(item):
    paragraphs = "".join("<p>%s</p>" % p for p in item["body"])
    extra = ""
    if item.get("heading"):
        extra = ('<h2>%s</h2><ul>%s</ul>'
                 % (esc(item["heading"]),
                    "".join("<li>%s</li>" % li for li in item["list"])))
    tags = "".join('<li class="tag">%s</li>' % esc(t) for t in item.get("tags", []))
    body = [hero("01", "Article", item["title"], item["excerpt"],
                 image=item["image"], alt=item["alt"],
                 ctas=[("/news/", "All news", "back")])]
    body.append('      <section class="section shell">'
                '        <p class="article__meta label-caps reveal">'
                '<span class="tnum">%s</span><span>By %s</span></p>'
                '        <div class="dis-prose article__body reveal" style="margin-top:1.5rem">'
                '%s%s</div>'
                '        <ul class="news-card__tags reveal" style="margin-top:2.5rem">%s</ul>'
                '        <p style="margin-top:2.5rem"><a class="btn btn--back" href="/news/">'
                'All news%s</a></p>'
                '      </section>'
                % (esc(item["date"]), esc(item["author"]), paragraphs, extra, tags, ICON_ARROW))
    return document(item["title"],
                    item["excerpt"],
                    "/news/", "\n".join(body), og_image=item["image"])


def page_events():
    body = [hero("01", "Events", "The diary of the school.",
                 "Examinations, sports days, parents' meetings and the open day for families "
                 "considering DIS.",
                 image="/assets/img/assembly.jpg",
                 alt="Students gathered for assembly in the covered hall")]
    upcoming = [e for e in EVENTS if e["status"] == "Upcoming"]
    past = [e for e in EVENTS if e["status"] == "Past"]
    up_rows = "".join(event_row(ev, delay=i * 0.06) for i, ev in enumerate(upcoming))
    body.append(section(section_head("02", "Coming up", "Next on the calendar.")
                        + '        <p class="cta__actions reveal" style="margin-bottom:1.5rem">'
                          '<a class="btn btn--dark" href="/events/">Upcoming (%d)</a>'
                          '<a class="btn" href="#past">Past (%d)</a></p>'
                          '        <div>%s</div>'
                        % (len(upcoming), len(past), up_rows)))
    past_rows = "".join(event_row(ev, delay=i * 0.06) for i, ev in enumerate(past))
    body.append(section(section_head("03", "Archive", "Earlier this year.")
                        + '        <div id="past">%s</div>' % past_rows))
    body.append(cta("Planning around the school calendar?",
                    "The office confirms every date by SMS to the number registered against each "
                    "student.",
                    [("/contact/", "Ask about an event", "solid"),
                     ("/news/", "Read the news", "ghost")]))
    return document("Events",
                    "The DIS events calendar: inter-house sports day, the A-level parents' meeting, "
                    "the open day for prospective Form 1 families, graduation and the science club "
                    "exhibition.",
                    "/events/", "\n".join(body), og_image="/assets/img/assembly.jpg")


def page_event(ev):
    others = [e for e in EVENTS if e["slug"] != ev["slug"]][:3]
    rows = "".join(event_row(e, delay=i * 0.06) for i, e in enumerate(others))
    past = ev["status"] == "Past"
    body = [hero("01", "Event", ev["title"], ev["text"],
                 badge=("%s · %s" % (ev["status"], ev["date_label"]), past),
                 ctas=[(ev["calendar"], "Add to calendar", "solid"),
                       ("/contact/", "Ask about this event", "ghost")])]
    body.append(section(section_head("02", "Details", "When and where.")
                        + '        <div class="split"><div><div class="kv">%s</div></div>'
                          '<aside class="split__aside"><div class="panel reveal">'
                          '<p class="label-caps footer-col__title">All events</p>'
                          '<p class="card__text">Examinations, sports days, parents\' meetings and '
                          'open days are published on the school calendar.</p>'
                          '<a class="btn" href="/events/">Back to the calendar%s</a>'
                          '</div></aside></div>'
                        % ("".join([
                            kv_row("Date", ev["date_label"]),
                            kv_row("Time", ev["when"].split(" · ")[-1]),
                            kv_row("Venue", ev["where"]),
                            kv_row("Status", ev["status"]),
                        ]), ICON_ARROW)))
    body.append(section(section_head("03", "Other events", "Also on the calendar.")
                        + '        <div>%s</div>' % rows))
    return document(ev["title"],
                    "%s — %s at %s." % (ev["title"], ev["when"], ev["where"]),
                    "/events/", "\n".join(body))


def page_gallery():
    body = [hero("01", "Gallery", "The school as it actually looks.",
                 "Albums are uploaded by staff from the portal, so what you see here was "
                 "photographed this term.",
                 image="/assets/img/courtyard.jpg",
                 alt="The courtyard colonnade in early morning light")]
    rows = "".join(album_row(a, delay=i * 0.06) for i, a in enumerate(ALBUMS))
    body.append(section(section_head("02", "Albums", "Choose an album.")
                        + '        <div class="album-list">%s</div>' % rows))
    body.append(cta("Photographs are the property of the school.",
                    "To request a copy of any photograph for publication, contact the office.",
                    [("/contact/", "Contact the office", "solid"),
                     ("/", "Back to the home page", "ghost")]))
    return document("Gallery",
                    "Photographs of Dar es Salaam Islamic Seminary, uploaded by staff each term: "
                    "the campus and courtyard, study and classroom, assembly and ceremony, and the "
                    "grounds around the school.",
                    "/gallery/", "\n".join(body))


def page_album(album, index):
    photos = album["photos"]
    figures = "".join(
        photo(p, i + 1, len(photos), wide=(len(photos) == 3 and i == 0), delay=i * 0.06)
        for i, p in enumerate(photos))
    body = [hero("01", "Album", album["title"], album["desc"],
                 image="/assets/img/carveddoor.jpg",
                 alt="Carved geometric lattice detail",
                 ctas=[("/gallery/", "All albums", "back")])]
    body.append(section(section_head("02", "%d photographs" % len(photos),
                                     "Click any frame to open it.")
                        + '        <div class="photo-grid">%s</div>' % figures))
    return document(album["title"],
                    "%s — %d photographs from Dar es Salaam Islamic Seminary."
                    % (album["desc"], len(photos)),
                    "/gallery/", "\n".join(body), with_lightbox=True,
                    og_image=album["cover"])


def page_faq():
    body = [hero("01", "Questions & answers", "What families ask the office.",
                 "Grouped by topic. If your question is not here, the office answers calls between "
                 "07:30 and 16:30.",
                 image="/assets/img/studyhall.jpg",
                 alt="The study hall with morning light through louvered windows")]
    groups = []
    for num, topic, items in FAQ_GROUPS:
        block = ['<div class="reveal" style="margin-bottom:clamp(2rem,4vw,3rem)">',
                 '<p class="eyebrow" style="margin-bottom:1rem">'
                 '<span class="eyebrow__num tnum">%s</span>'
                 '<span class="label-caps eyebrow__label">%s</span></p>' % (esc(num), esc(topic))]
        block += [faq(q, a) for q, a in items]
        block.append('</div>')
        groups.append("".join(block))
    body.append(section(section_head("02", "Answers", "Asked often, answered plainly.",
                                     "Maintained by the DIS office — every answer here comes from "
                                     "the current school regulations.")
                        + "        " + "".join(groups)))
    body.append(cta("Question not answered here?",
                    "The office answers calls between 07:30 and 16:30 on weekdays and replies to "
                    "written messages within two working days.",
                    [("/contact/", "Write to the office", "solid"),
                     ("/admissions/", "How to apply", "ghost")]))
    return document("Questions & answers",
                    "What families ask the DIS office about admissions, fees, joining, school life "
                    "and transport.",
                    "/faq/", "\n".join(body), og_image="/assets/img/studyhall.jpg")


def page_contact():
    body = [hero("01", "Contact", "Come to the office, or write to it.",
                 OFFICE_HOURS,
                 image="/assets/img/courtyard.jpg",
                 alt="The school courtyard arcade at dawn")]
    channels = "".join([
        channel("Address", ADDRESS, href="https://www.google.com/maps/dir/?api=1&destination=-6.7708,39.2147"),
        channel("Telephone", PHONE, href="tel:+255754100220"),
        channel("WhatsApp", PHONE, href="https://wa.me/255754100220"),
        channel("Email", EMAIL, href="mailto:" + EMAIL),
        channel("Office hours", OFFICE_HOURS),
        channel("Written replies", "Within two working days"),
    ])
    body.append(section(section_head("02", "Channels", "Five ways to reach us.")
                        + '        <div class="channels">%s</div>' % channels))

    form = ('        <div class="split"><div>'
            '<h2 class="section-head__title reveal" style="margin-bottom:1.25rem">Write to the office</h2>'
            '<p class="section-head__lede reveal" style="margin-bottom:2rem">Messages land in the DIS '
            'office inbox and are answered in the order received.</p>'
            '<form class="form reveal" data-contact-form novalidate>'
            '<div class="form__row">'
            '<p class="field"><label class="label-caps field__label" for="f-name">Your name *</label>'
            '<input class="field__input" id="f-name" name="name" type="text" required '
            'autocomplete="name"></p>'
            '<p class="field"><label class="label-caps field__label" for="f-email">Email *</label>'
            '<input class="field__input" id="f-email" name="email" type="email" required '
            'autocomplete="email"></p></div>'
            '<div class="form__row">'
            '<p class="field"><label class="label-caps field__label" for="f-phone">Phone</label>'
            '<input class="field__input" id="f-phone" name="phone" type="tel" '
            'autocomplete="tel"></p>'
            '<p class="field"><label class="label-caps field__label" for="f-subject">Subject</label>'
            '<input class="field__input" id="f-subject" name="subject" type="text"></p></div>'
            '<p class="field"><label class="label-caps field__label" for="f-message">Message *</label>'
            '<textarea class="field__textarea" id="f-message" name="message" required></textarea></p>'
            '<p class="sr-only"><label for="f-website">Website</label>'
            '<input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></p>'
            '<p><button class="btn btn--dark" type="submit">Send message%s</button></p>'
            '<p class="form__note" data-form-status role="status">We reply within two working days. '
            'Your details are used only to answer you.</p>'
            '</form></div>'
            '<aside class="split__aside"><div class="panel reveal">'
            '<p class="label-caps footer-col__title">At the office</p>'
            '<div class="kv">%s</div></div></aside></div>')
    office_kv = "".join([
        kv_row("Admissions desk", "07:30 – 16:30"),
        kv_row("Bursar", "07:30 – 15:30"),
        kv_row("Headmaster", "By appointment"),
        kv_row("Saturday", "08:00 – 12:00"),
    ])
    body.append(section(form % (ICON_ARROW, office_kv)))

    location = ('        <div class="split"><div>'
                '<div class="map reveal"><div><div class="map__pin" aria-hidden="true"></div>'
                '<p class="map__label">Mikocheni B, off Mwai Kibaki Road</p>'
                '<p class="map__coords tnum">-6.7708, 39.2147</p></div></div>'
                '<p style="margin-top:1.5rem"><a class="btn btn--dark" '
                'href="https://www.google.com/maps/dir/?api=1&destination=-6.7708,39.2147">'
                'Get directions%s</a></p></div>'
                '<aside class="split__aside"><div class="panel reveal">'
                '<p class="label-caps footer-col__title">Getting here</p>'
                '<div class="dis-prose article__body"><ul>'
                '<li><strong>From the city centre:</strong> take the Mwai Kibaki Road corridor '
                'north-east, approximately 25 minutes outside rush hour.</li>'
                '<li><strong>By daladala:</strong> routes serving Mikocheni B stop at the mosque '
                'junction; the gate is a four-minute walk inland.</li>'
                '<li><strong>Parking:</strong> visitor parking is inside the main gate on the left, '
                'with space for twelve vehicles.</li></ul></div></div></aside></div>')
    body.append(section(section_head("03", "Location",
                                     "Off Mwai Kibaki Road, Mikocheni B.") + location % ICON_ARROW))
    return document("Contact",
                    "Come to the DIS office on Mwai Kibaki Road, or write to it. Address, telephone, "
                    "WhatsApp, email and office hours.",
                    "/contact/", "\n".join(body))


def page_404():
    body = ('      <section class="section shell notfound">'
            '<p class="notfound__code tnum reveal">404</p>'
            '<p class="label-caps footer-col__title reveal" style="margin-top:1.5rem">Not found</p>'
            '<h1 class="section-head__title reveal" style="margin:1rem auto 0;max-width:24ch">'
            'That page has been moved, or it never existed.</h1>'
            '<p class="section-head__lede reveal" style="margin:1.25rem auto 0">'
            'News articles and events keep their address only while they are published. '
            'Try the news index or the calendar.</p>'
            '<p class="cta__actions reveal" style="justify-content:center;margin-top:2rem">'
            '<a class="btn btn--dark" href="/">Go home%s</a>'
            '<a class="btn" href="/news/">Browse news%s</a></p></section>'
            % (ICON_ARROW, ICON_ARROW))
    return document("404 — not found",
                    "That page has been moved, or it never existed.",
                    None, body)


# =====================================================================
#  BUILD
# =====================================================================
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path


def build():
    written = []

    # home
    written.append(write("index.html", page_home()))
    written.append(write("404.html", page_404()))

    # simple pages
    written.append(write("about/index.html", page_about()))
    written.append(write("leadership/index.html", page_leadership()))
    written.append(write("academics/index.html", page_academics()))
    written.append(write("admissions/index.html", page_admissions()))
    written.append(write("faq/index.html", page_faq()))
    written.append(write("contact/index.html", page_contact()))

    # departments
    for i, dept in enumerate(DEPARTMENTS):
        written.append(write("departments/%s/index.html" % dept["slug"], page_department(dept, i)))

    # news
    written.append(write("news/index.html", page_news()))
    for item in NEWS:
        written.append(write("news/%s/index.html" % item["slug"], page_article(item)))

    # events
    written.append(write("events/index.html", page_events()))
    for ev in EVENTS:
        written.append(write("events/%s/index.html" % ev["slug"], page_event(ev)))

    # gallery
    written.append(write("gallery/index.html", page_gallery()))
    for i, album in enumerate(ALBUMS):
        written.append(write("gallery/%s/index.html" % album["slug"], page_album(album, i)))

    # robots
    written.append(write("robots.txt",
                         "User-Agent: *\nAllow: /\n"
                         "Disallow: /admin/\nDisallow: /staff/\nDisallow: /api/\n"
                         "Disallow: /login\nDisallow: /register\nDisallow: /reset-password\n"))

    return written


def package():
    """Zip everything the site needs into dis-website.zip."""
    target = os.path.join(ROOT, "dis-website.zip")
    if os.path.exists(target):
        os.remove(target)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for base, _dirs, files in os.walk(ROOT):
            _dirs[:] = [d for d in _dirs if d not in (".git", "__pycache__")]
            for name in files:
                if name.endswith((".pyc",)) or name == "dis-website.zip":
                    continue
                full = os.path.join(base, name)
                rel = os.path.relpath(full, ROOT)
                if rel.startswith(".git"):
                    continue
                zf.write(full, os.path.join("dis-website", rel))
    return target


if __name__ == "__main__":
    for path in build():
        print("built", path)
    if "--zip" in sys.argv:
        print("packaged", os.path.relpath(package(), ROOT))
    print("done — %d files" % len(build()))
