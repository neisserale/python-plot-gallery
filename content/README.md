# ✍️ content/ — what humans write

Everything the gallery publishes starts here. **This is the only folder you edit to add or change a plot.**

```text
content/
├── datasets/<dataset-id>/   dataset.yaml + <dataset-id>.csv (written once, shared by plots)
└── plots/<plot-id>/         plot.yaml + plot.py + notebook.ipynb
```

| File | What it is |
|------|------------|
| `plot.yaml` | Metadata: title, description, categories, dataset, alt text |
| `plot.py` | The canonical code that draws the figure (its PEP 723 header is generated) |
| `notebook.ipynb` | The 6-step lesson (its `data` and `final` cells and its outputs are generated) |
| `dataset.yaml` | Source, license, columns and checksum of a dataset |

After editing, run `uv run gallery update <plot-id>` and commit the changes in `content/` and `generated/`.

Specs: [03 — Data Model](../docs/specs/03-data-model.md).
