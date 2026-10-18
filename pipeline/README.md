# ⚙️ pipeline/ — the `gallery` CLI

The Python package (`plot_gallery`) that turns `content/` into `generated/`: it validates the content, renders each plot in a sandbox, runs the notebooks and compiles the catalog and the bundles.

```text
pipeline/
├── plot_gallery/   the package (entry point: cli.py)
├── templates/      starting files used by `gallery new`
└── tests/          pytest suite (uses tests/fixtures, never real content)
```

| Command | Purpose |
|---------|---------|
| `uv run gallery update [ids…]` | sync → render → execute → build (the everyday command) |
| `uv run gallery check` | every validation and drift check, without writing (what CI runs) |
| `uv run gallery --help` | all commands |
| `uv run pytest` | run the pipeline tests |

Edit this folder only when changing the rules or the tooling. Specs: [02 — Technical Architecture](../docs/specs/02-technical-architecture.md#5-the-pipeline).
