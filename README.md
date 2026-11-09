# Auckland deck

Website: https://maxhogervorst.github.io/deck-design/

[The build guide](CURRENT_DESIGN.md) · [Shopping CSV](docs/shopping-list.csv) · [Three drawings](docs/drawings/)

One owner-builder guide: deck on 16 timber piles, low step on six paver pads tied to the deck. The assumptions the owner would ideally have checked are listed at the end of the guide. Previous versions and research are in archive/.

Build: `OPENBLAS_NUM_THREADS=1 python scripts/check_revision.py`, `python scripts/render_plan.py`, `npm run build`. Node 22+ and Python/NumPy are required. Preview with `npm start`.
