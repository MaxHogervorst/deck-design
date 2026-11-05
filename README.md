# Auckland deck — build guide and builder brief

Technical reference for the owner and builder:

- **Plans:** framing opens first, with 19 numbered joist lines, four continuity candidates, two butt sisters, rebuilt cross-blocking, a trial tread frame and a coordinate table. Separate views explain rotated-board fixings, the tread frame, ground fixing, dimensions and side profile.
- **Materials:** specifications, planning quantities and outstanding decisions in one table.
- **Build steps:** one sequence for all three areas: levels, set-out, all foundations, all frames, boards, completion. Eleven assembly pictures have part IDs, tools and check dimensions. Previous/Next controls show one action at a time; printing includes all actions.
- **Builder plan review:** one in-person review before construction, with no during-build inspections planned. No online forms or feedback workflow.

Live site: **https://maxhogervorst.github.io/deck-design/**

The design remains **preliminary, not construction drawings**. Confirmed owner choices are distinguished from provisional structural details and checks still requiring verification.

## Current brief

- Main deck: **6600 × 2600 mm**; rebuilt section: **900 × 1970 mm**.
- Main + rebuilt area: **18.933 m²**, excluding tread.
- **Deck → one full-width tread → garden**. Tread: **6600 × 400 mm**, selected surface **250 mm above the garden**, retained by owner, beneath a deck about **500 mm high**. Access compliance is not verified; the owner requested structural work proceed at these levels.
- **32 mm-thick pine decking**; 80 mm width remains provisional. The rebuilt section is illustrated with boards turned 90° along its 1970 mm depth, interpreting the owner’s description.
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

The framing view is the default. J01–J04 fit within the900 mm strip at285 mm centres; the remaining15 bays are380 mm. Dashed continuations remain provisional. Open the joist coordinate table for centre positions, or enlarge the drawing. No displayed coordinate is an approved cut length.

The owner guide starts with the selected500/250 mm datums and uses one set-out for main deck, rebuilt section and tread. It builds all foundations together, completes both ground-supported structures and concealed connections, then lays all boards. Four coordinated inputs are missing: GP01 levels/tread, FP01 main foundations, AP01 structural spans/bracing/connections, DF01 boards/stock/fixings. The owner checks uncovered framing before any boards; no builder visit is implied.

The builder reviews the proposed joist continuity and rebuilt cross-blocks, main framing/bracing, footing plan, tread frame/access and the actual decking/fasteners once before construction. The owner builds from the agreed plan; no during-build builder inspections are planned. The requested site-clearance checklist is outside that review, and no handrails are proposed.

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
| `site/assembly-diagrams.js` | Labelled assembly pictures and the tread ground-connection cutaway |
| `site/build-guide.js` | Eleven-action owner assembly guide, part table, navigation and print mode |
| `site/app.js` | Drawing selection, in-person discussion topics, source downloads and page sharing |
| `scripts/build.mjs` | Creates self-contained HTML and the public variant without working-note downloads |
| `scripts/serve.mjs` | Minimal local static server |

## Project sources

The Markdown files remain the working design record. After changing dimensions, materials or construction details, update the affected notes and website content together, then rebuild. The portable build embeds current source documents; illustrated plans and summaries are curated rather than automatically inferred from prose.

- [PROJECT.md](PROJECT.md): requirements and latest owner choices
- [STRUCTURAL_REVIEW.md](STRUCTURAL_REVIEW.md): specific proposal, evidence, quantities and cutting scenario
- [DESIGN.md](DESIGN.md): coordinates, framing concepts and access geometry
- [MATERIALS.md](MATERIALS.md): conditional quantity scenarios and historical prices
- [OPEN_ISSUES.md](OPEN_ISSUES.md): outstanding checks and required evidence
- [SITE_MEASUREMENTS.md](SITE_MEASUREMENTS.md): confirmed and missing site facts
- [BUILD_STEPS.md](BUILD_STEPS.md): draft construction sequence and hold points
- [REFERENCES.md](REFERENCES.md): primary-source research leads and verification history
- [DECISIONS.md](DECISIONS.md): decision history
- [AGENTS.md](AGENTS.md): repository guidance

## Validation after changes

Run `npm run build` and check both HTML variants in a browser on desktop and mobile. Exercise plan selection by mouse/keyboard, all six drawing tabs, the single-tread profile, the eleven assembly actions, print-all behaviour, the six pre-build review topics, source downloads in the fuller bundle and the share controls. Confirm that the public variant contains no embedded working notes, and that review forms, feedback exports and reviewer-note storage are absent.

These checks validate website behaviour, not structural design or compliance. General BRANZ board-fixing guidance is recorded in REFERENCES.md. The full frame, foundations, connections and access geometry remain proposals for pre-build review, not independently verified construction details.

## Specific structural proposal

See [STRUCTURAL_REVIEW.md](STRUCTURAL_REVIEW.md) for calculations, published source comparisons, remaining limitations and the concrete/stock scenarios. Current framing is19 lines +2 butt sisters,4 long joists,36 main lateral blocks,18 rebuilt blocks and a900 mm intermediate bearer atY−800 on2 ordinary piles. Six main anchor positions and a conditional foundation schedule are shown; calculated concrete≈1.358 m³ before waste, with no retained replacement included. The tread proposal is SG8 H5 on six shared pads.

The site records32 mm thickness and around80 mm width, with80/88/90 mm quantity comparisons. At80 mm and5 mm illustrative gaps:31 main /11 rebuilt /5 tread rows,284.4 lm illustrative stock and1644 base fixing positions. Exact current-standard connections, the pad/anchor design, good-ground bearing and retained-support capacity remain unverified; this is a specific pre-build review proposal, not certified construction drawings.
