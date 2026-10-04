# Solvardis — non-WordPress recreation

The working site is in `dist/`. It is static HTML, CSS and browser JavaScript. There is no PHP, WordPress installation, database or build dependency. The original Bridge/Qode and LayerSlider frontend code is retained to preserve the site's appearance and animations.

## Run locally

With Node.js 20 or later:

```sh
node serve.mjs
```

Open `http://127.0.0.1:4173`. Alternatively, `python3 -m http.server 4173 --directory dist` serves the same website. Open through a web server, rather than double-clicking HTML files.

## Deploy

Deploy the contents of `dist/` to any static host that supports directory `index.html` files. No build command is needed. Keep asset paths rooted at the domain. The included `vercel.json` publishes `dist/` directly, without a build or install step, and preserves directory routes. Vercel deploys automatically from `main`.

## What was preserved

- Original page markup, copy, seven-item navigation, logos, colours, typography, spacing, footer and responsive breakpoints.
- Original three-slide LayerSlider imagery, six-second slide settings, fades, responsive scaling and original hidden control settings.
- Bridge page transitions, mobile navigation, gallery lightboxes, portfolio layout, progress bars and other exported theme elements.
- All published exported page routes, ten industry details, and linked pagination routes.
- Local images, icon fonts, Google Fonts and the 33 linked technical data PDFs.

`asset-map.json` maps the 606 exported attachment IDs to their original and local files. `page-map.json` maps original page IDs, routes and shortcode names. `capture-report.json` records capture results and unavailable legacy dependencies. The downloadable complete archive contains `data/export.json`, the parsed WordPress export for maintenance; this large archival file is excluded from the deployment repository and is unnecessary to run the site. Restore it from the archive before using the recapture command below. All media files were drawn from the supplied ZIP where available; theme resources and rendered shortcode content were recovered from the original local site.

The ten original industry permalinks returned 404, so their original rendered pages were recovered through alternate WordPress URLs. The Icons demo was recovered through WordPress's rendered-content API and composed into the preserved theme shell. The legacy Shop export is empty and its source route returns 500; the static Shop route preserves the empty content. There is no checkout, user-account, comment-posting or commerce backend. These legacy theme demo routes were never part of the active seven-item Solvardis navigation.

The contact page retains the original Google Maps settings. During verification, the original public browser key reported that geocoding billing is disabled; the map therefore shows the theme's default location rather than resolving the office address. This also affects the original site. The site owner needs to enable billing or supply a replacement Maps key to restore office geocoding. Google Maps remains an external service. The live original site does not contain a contact submission form; its email links are preserved.

Likes, where present in theme demonstrations, are stored locally in the visitor's browser rather than sent to WordPress. Empty Home breadcrumb links were repaired. WordPress discovery/feed/emoji/administration and unused contact-submit wiring were removed. Original third-party library files and notices remain intact.

## Check and recapture

```sh
node validate.mjs
python3 capture.py --export data/export.json --uploads /path/to/solvardis-uploads.zip
```

Recapture requires network access to `http://pi2.local:8082`. Normal use of the delivered site does not. The captures and original desktop/mobile comparison screenshots are supplied alongside this project. Representative visual QA used 1440×1000 desktop and 390×844 mobile viewports; it included the homepage, About, Services, Industries, an industry detail, data sheets, mobile menu and contact map. Not every legacy theme demonstration page was manually inspected.
