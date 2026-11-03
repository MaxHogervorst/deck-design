# Auckland deck — build guide and builder brief

Technical reference for the owner and builder:

- **Plans:** framing opens first, with 16 numbered joist lines, three dashed continuation candidates, bearer/pile positions and a coordinate table. Dimensions and side profile are separate views.
- **Materials:** specifications, planning quantities and outstanding decisions in one table.
- **Build steps:** seven short phases, open by default.
- **Builder checks:** a table for the in-person discussion. No online forms or feedback workflow.

Live site: **https://maxhogervorst.github.io/deck-design/**

The design remains **preliminary, not construction drawings**. Confirmed owner choices are distinguished from provisional structural details and checks still requiring verification.

## Current brief

- Main deck: **6600 × 2600 mm**; rebuilt section: **900 × 1970 mm**.
- Main + rebuilt area: **18.933 m²**, excluding tread.
- **Deck → one full-width tread → garden**. Tread: **6600 × 400 mm**, selected surface **250 mm above the garden**, beneath a deck about **500 mm high**. The vertical access detail is not verified.
- **38 mm-thick pine decking**; 138 mm board width remains provisional until the actual product is selected.
- Freestanding from the house. Double 140×45 bearers and 140×45 joists remain structural concepts.

## Build and view

Requires Node.js 22 or newer. No dependency installation is needed.

```sh
npm run build
npm start
```

The server uses port 3000 by default; set `PORT` to change it. `npm run dev` builds and starts the server in one command. Rebuild after editing website sources or project Markdown, then refresh the browser. There is no automatic file watcher.

The build creates two self-contained HTML variants:

| Output | Contents |
|---|---|
| `docs/index.html` | Public Pages website: drawings, materials, owner build guide, builder discussion brief and page-sharing controls. Working Markdown downloads are excluded. |
| `dist/index.html` | Portable website with the same guide and brief, plus embedded working Markdown documents and source downloads. Share this fuller bundle with the intended recipients. |

No remote fonts, analytics, APIs, accounts or external assets are required. The HTML can be opened directly in a modern browser.

## Using the website

The framing view is the default. J01–J03 fit within the 900 mm rebuilt strip at 427.5 mm centres; the remaining 13 bays are approximately 438.46 mm. Dashed continuations remain provisional. Open the joist coordinate table for centre positions, or enlarge the drawing. No displayed coordinate is an approved cut length.

The owner build guide covers design/pre-work, set-out, footings, bearers/bracing, joists and the rebuilt-section junction, decking, and the garden tread/completion. It explains the order of work without treating unresolved structural choices as approved construction details.

The builder-checks table lists six topics: layout/house interface, the rebuilt section and retained bearer, framing/bracing/connections, footings/ground, deck-to-tread-to-garden access, and the exact decking/purchase plan. Use these during the in-person discussion. Agreed changes belong in the project record rather than an on-site review form.

## Share and publish

Share the live link, or use **Share design → Download website** to send an HTML attachment. Some email clients do not preview active HTML; recipients can download the attachment and open it in a browser.

GitHub Pages serves the generated **`docs/`** folder on the **`main`** branch. The site supports the `/deck-design/` subpath without asset-path configuration. `npm run build` refreshes `docs/index.html` and `docs/.nojekyll` alongside `dist/index.html`; commit the refreshed `docs/` output when publishing website changes.

Public Pages output excludes the embedded working Markdown documents and their download section. Those source files remain in the repository and in the fuller `dist/` bundle. This does not imply that the repository itself is private. The build does not change hosting/domain settings or publish the cloud environment.

## Website sources

| File | Purpose |
|---|---|
| `site/index.html` | Page content and accessible structure |
| `site/styles.css` | Responsive layout, diagram controls and print styling |
| `site/diagrams.js` | Proportional plan, provisional framing and one-tread side profile |
| `site/build-guide.js` | Seven-phase owner build guide |
| `site/app.js` | Drawing selection, in-person discussion topics, source downloads and page sharing |
| `scripts/build.mjs` | Creates self-contained HTML and the public variant without working-note downloads |
| `scripts/serve.mjs` | Minimal local static server |

## Project sources

The Markdown files remain the working design record. After changing dimensions, materials or construction details, update the affected notes and website content together, then rebuild. The portable build embeds current source documents; illustrated plans and summaries are curated rather than automatically inferred from prose.

- [PROJECT.md](PROJECT.md): requirements and latest owner choices
- [DESIGN.md](DESIGN.md): coordinates, framing concepts and access geometry
- [MATERIALS.md](MATERIALS.md): conditional quantity scenarios and historical prices
- [OPEN_ISSUES.md](OPEN_ISSUES.md): outstanding checks and required evidence
- [SITE_MEASUREMENTS.md](SITE_MEASUREMENTS.md): confirmed and missing site facts
- [BUILD_STEPS.md](BUILD_STEPS.md): draft construction sequence and hold points
- [REFERENCES.md](REFERENCES.md): primary-source research leads and verification history
- [DECISIONS.md](DECISIONS.md): decision history
- [AGENTS.md](AGENTS.md): repository guidance

## Validation after changes

Run `npm run build` and check both HTML variants in a browser on desktop and mobile. Exercise plan selection by mouse/keyboard, drawing tabs, the single-tread profile, the seven build phases, the six in-person discussion topics, source downloads in the fuller bundle and the share controls. Confirm that the public variant contains no embedded working notes, and that review forms, feedback exports and reviewer-note storage are absent.

These checks validate website behaviour, not structural design or compliance. No current NZ structural or regulatory requirement has been independently verified by this website work.
