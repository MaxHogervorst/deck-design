# Auckland deck — design review website

A portable website for reviewing a freestanding Auckland timber-deck concept. It includes interactive, dimensioned plan and framing views, a side profile, material assumptions, downloadable source notes and reviewer feedback exports.

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

The build creates **`dist/index.html`**, containing all styles, scripts, SVG drawing code and project source documents. No remote fonts, analytics, APIs, accounts or external assets are required. The finished HTML can be opened directly in a modern browser.

## Share with reviewers

Send `dist/index.html` as an attachment, or use **Share design → Download website** inside the page. Reviewers should download the HTML attachment and open it in a browser; some email clients do not preview active HTML attachments.

For a public URL, GitHub Pages can serve the generated **`docs/`** folder on the **`main`** branch. In repository **Settings → Pages**, choose **Deploy from a branch**, then **main /docs**, and save. The website supports the `/deck-design/` subpath without an asset-path configuration. The build refreshes `docs/index.html` and `docs/.nojekyll` alongside `dist/index.html`; commit the refreshed `docs/` output when publishing changes. The private source repository stays private. Pages availability for private repositories depends on the GitHub account plan. The build itself does not deploy or publish the cloud environment.

Reviewers enter optional names, assessments and notes. These stay in their browser when storage is available. They must use **Download review** or **Copy review** and send the result to the project owner; there is no shared database or automatic submission. A downloaded website excludes those personal review inputs. Downloaded reviews contain them intentionally. On browsers that block local storage, download the review before closing the page.

## Website sources

| File | Purpose |
|---|---|
| `site/index.html` | Page content and accessible structure |
| `site/styles.css` | Responsive layout, diagram controls and print styling |
| `site/diagrams.js` | Proportional plan, provisional framing and one-tread side profile |
| `site/app.js` | Drawing selection, review notes, source exports and sharing |
| `scripts/build.mjs` | Creates the self-contained HTML and embeds Markdown sources |
| `scripts/serve.mjs` | Minimal local static server |

## Project sources

The Markdown files remain the working design record. After changing dimensions or materials, update the affected source notes and website content together, then rebuild. The build embeds current source documents; the illustrated design and summaries are intentionally curated rather than automatically inferred from prose.

- [PROJECT.md](PROJECT.md): requirements and latest owner choices
- [DESIGN.md](DESIGN.md): coordinates, framing concepts and access geometry
- [MATERIALS.md](MATERIALS.md): conditional quantity scenarios and historical prices
- [OPEN_ISSUES.md](OPEN_ISSUES.md): outstanding checks and required evidence
- [SITE_MEASUREMENTS.md](SITE_MEASUREMENTS.md): confirmed and missing site facts
- [BUILD_STEPS.md](BUILD_STEPS.md): draft construction sequence and hold points
- [REFERENCES.md](REFERENCES.md): primary-source research leads and verification history
- [DECISIONS.md](DECISIONS.md): decision history
- [AGENTS.md](AGENTS.md): repository guidance

## Validation

The current build has been exercised in Chromium on desktop and at a 390 px mobile viewport: plan selection by mouse/keyboard, drawing tabs and framing pile count, single-tread profile, review persistence and export, source downloads, sharing controls and exclusion of private review notes from website downloads. Self-contained downloaded HTML is also tested with networking disabled. Direct `file://` navigation is blocked by this cloud browser's administrator policy; offline testing loads the HTML content into the browser instead.

This validates website behaviour, not structural design, compliance or fresh-host deployment. No current NZ structural or regulatory requirement has been independently verified by this website work.
