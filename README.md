# Auckland deck and pine box tread

Current website: https://maxhogervorst.github.io/deck-design/

Main deck 6600 × 2600 mm, rebuilt strip 900 × 1970 mm, one 6600 × 400 mm pine tread. Selected surfaces approximately 500/250 mm above the garden. Main framing uses timber piles and doubled bearers; the single-layer tread box bears on low concrete supports. Continuous long plies remove planned bearer/rail splices.

See [CURRENT_DESIGN.md](CURRENT_DESIGN.md) for current dimensions, fresh cutting lists, source checks and the remaining pre-build details. Historical design notes are superseded where they conflict with that brief.

This is a working plan, not construction drawings. The complete low main-anchor/uplift connections and tread foundation/restraint assembly remain unfinished. Site ground/levels/drainage, actual supplied products and access compliance also require resolution before building. One pre-build discussion, then one owner build sequence; no builder inspections during construction assumed.

## Build locally

Requires Node.js 22 or newer; no dependencies.

```sh
npm run build
npm start
```

Open http://localhost:3000. The build generates identical standalone `docs/index.html` (GitHub Pages) and `dist/index.html` (local copy). Historical working documents are not embedded. GitHub Pages serves `docs/` from `main`.

Cut arithmetic can be reproduced with `python calculations/current_takeoff.py`; saved output is `calculations/current_takeoff.json`. These are quantity/geometry checks, not structural resistance calculations.
