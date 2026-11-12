# Auckland deck

Website: https://maxhogervorst.github.io/deck-design/

[The build guide](CURRENT_DESIGN.md) · [Shopping CSV](docs/shopping-list.csv) · [Sheets](docs/drawings/)

One owner-builder guide. The deck, the two steps and the shopping list are in [CURRENT_DESIGN.md](CURRENT_DESIGN.md). The site is the three sheets and that list.

Build: `OPENBLAS_NUM_THREADS=1 python scripts/check_revision.py`, `python scripts/render_plan.py`, `npm run build`. Node 22+ and Python/NumPy are required. Preview with `npm start`.
