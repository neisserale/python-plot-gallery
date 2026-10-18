# Contributing to Plot Gallery

> **Draft.** The plot workflow below becomes available in Phase 2 (pipeline) and Phase 3 (first content). It is finalized in Phase 7.

## Set up

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and [Node.js 24+](https://nodejs.org/).
2. Clone the repository and run `uv sync` (add `--group notebooks` if you will edit notebooks).
3. For the website: `cd web && npm install`.

## Add a plot

```bash
uv run gallery new <plot-id>            # 1. scaffold content/plots/<plot-id>/
#                                         2. write plot.yaml, plot.py and notebook steps 1–5
uv run gallery update <plot-id>         # 3. sync, render, execute, build
cd web && npm run dev                   # 4. check the page locally
```

Then open a pull request with the changes in `content/` and `generated/`. Never edit `generated/` by hand.

Before opening the PR:

- [ ] `uv run gallery check` passes.
- [ ] The figure uses a colorblind-safe palette and has meaningful `image.alt` text.
- [ ] The bundle runs from an empty folder: unzip it, then `uv run plot.py`.
- [ ] The dataset's license allows redistribution.

The full rules are in [docs/specs/03-data-model.md](docs/specs/03-data-model.md).

## Conventions

- **Python:** English names and comments; single quotes for short strings, triple double quotes for docstrings. Ruff enforces both: run `uv run ruff check` and `uv run ruff format`.
- **TypeScript:** strict mode, Server Components by default, data only through `web/src/lib/catalog.ts`. Run `npm run lint` and `npm run typecheck`.
- **Branches:** `type/short-description`, for example `feat/box-plot` or `fix/copy-button`.
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/), for example `feat(content): add box plot of penguin body mass`.

The complete conventions are in [docs/specs/05-project-structure.md](docs/specs/05-project-structure.md).
