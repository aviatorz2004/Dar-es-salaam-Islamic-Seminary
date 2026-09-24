# Dar es Salaam Islamic Seminary — Gallery

A static recreation of the school's gallery: the album index plus the four photo
albums, built with the site's paper-and-ink design system.

```
/                                 → redirects to /gallery/
/gallery/                         → album index ("Choose an album.")
/gallery/campus-courtyard/        → Campus & courtyard      (3 photographs)
/gallery/study-classroom/         → Study & classroom       (2 photographs)
/gallery/assembly-ceremony/       → Assembly & ceremony     (2 photographs)
/gallery/around-the-school/       → Around the school       (3 photographs)
```

## Run it

Any static file server works — the site has no build step and no dependencies:

```bash
python3 -m http.server 8080
# then open http://localhost:8080/gallery/
```

## Layout

```
index.html                      redirect to the gallery
gallery/index.html              album index
gallery/<album>/index.html      one page per album
assets/css/site.css             design system (tokens, components, motion)
assets/js/site.js               scroll reveals + photo lightbox
assets/img/                     photography + favicon
```

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
`.label-caps`, dividers use `.lattice-rule`, and entrance motion uses
`.reveal` / `.rule-draw` — all reduced-motion aware, with a `<noscript>`
fallback so content is never stuck hidden.

## Notes

- **Photography.** The five files in `assets/img/` are AI-generated stand-ins that
  match the original captions (courtyard, carved door, gate, study hall,
  assembly). Replace them with the school's own photographs, keeping the same
  filenames, and every page updates.
- **Content.** Album titles, descriptions, photo captions and the footer credit
  line follow the original gallery.
- **Fonts.** If you need the site to work fully offline, self-host the Fraunces
  and Archivo `.woff2` files and drop the Google Fonts `<link>` tags.
