# Dar es Salaam Islamic Seminary — website

The full public website: home, about, leadership, academics and the five
departments, admissions, news, the events calendar, the gallery, the FAQ and
the contact page — built as plain HTML, CSS and JavaScript with no build step
and no dependencies.

```
/                                 home
/about/                           about the seminary, values, history
/leadership/                      headmaster, administrator, heads of department
/academics/                       four programmes + five departments
/departments/<slug>/              sciences · mathematics-ict · languages
                                   islamic-studies-arabic · history-civics-geography
/admissions/                      the five-step process, requirements, fees 2027
/news/                            article index
/news/<slug>/                     three articles
/events/                          upcoming + archive
/events/<slug>/                   five events
/gallery/                         album index
/gallery/<album>/                 campus-courtyard · study-classroom
                                   assembly-ceremony · around-the-school
/faq/                             questions grouped by topic
/contact/                         channels, message form, location
/404.html                         not found
```

## Run it

Any static file server works:

```bash
python3 -m http.server 8080
# then open http://localhost:8080/
```

## Download

`dis-website.zip` contains the whole site in a single `dis-website/` folder —
unzip it and open `index.html`, or serve the folder with any static host
(GitHub Pages, Netlify, nginx, Apache). It is regenerated with:

```bash
python3 build.py --zip
```

## Layout

```
build.py                        generates every page from the content below
index.html, about/, news/, …    the generated site
assets/css/site.css             design system (tokens, components, motion)
assets/js/site.js               scroll reveals, mobile menu, lightbox, form
assets/img/                     photography + favicon
```

`build.py` is the single source of truth: it holds the navigation, the page
templates and all the copy, so a change to the header, footer or a fee is made
once and applies everywhere. Edit the content blocks in that file and re-run it.

## Design system

| Token | Value | Used for |
| --- | --- | --- |
| `--paper` | `#f3ede2` | page background |
| `--paper-2` | `#e9e1d3` | image placeholders, quiet panels |
| `--ink` | `#0e2e33` | body text |
| `--ink-deep` | `#0a1f23` | hero scrims, lightbox backdrop |
| `--jade` | `#146b5c` | links / hover accents |
| `--brass` | `#c08a2e` | section numerals, lattice rule, focus rings |
| `--sand` | `#6e6558` | captions, secondary copy |

Type is **Fraunces** (display, with the `SOFT`/`WONK`/`opsz` axes) and **Archivo**
(text), loaded from Google Fonts with a local fallback stack. Section labels use
`.label-caps`, dividers use `.lattice-rule`, and entrance motion uses `.reveal`
and `.rule-draw` — all reduced-motion aware, with a `<noscript>` fallback so
content is never stuck hidden.

## Notes

- **Photography.** The five files in `assets/img/` are AI-generated stand-ins that
  match the original captions (courtyard, carved door, gate, study hall,
  assembly). Replace them with the school's own photographs, keeping the same
  filenames, and every page updates.
- **Contact form.** The site is static, so the form hands the message to the
  visitor's mail client addressed to `info@dis.ac.tz` (with a honeypot field for
  bots). Point it at a form endpoint if you would rather it post somewhere.
- **Map.** The location panel is a styled placeholder with a "Get directions"
  link instead of an embedded map that would need an API key.
- **Content.** Programme, department, staff, admissions, fee, news, event, FAQ
  and contact copy follows the original site.
- **Fonts.** To work fully offline, self-host the Fraunces and Archivo `.woff2`
  files and drop the Google Fonts `<link>` tags.
