# 🤖 generated/ — what the machine writes

> **Do not edit anything in this folder.** Regenerate it with `uv run gallery update`.

Everything here is produced by the pipeline from `content/` and committed, so the website can be built without Python. CI regenerates these files on every pull request and fails if they differ from what was committed.

```text
generated/
├── catalog.json           the only file the website reads
├── schemas/               JSON Schemas (YAML autocompletion, TypeScript types)
└── plots/<plot-id>/       plot.png · plot-800.webp · plot-1600.webp · <plot-id>.zip
```

Specs: [03 — Data Model](../docs/specs/03-data-model.md#7-generated-outputs-per-plot-generatedplotsplot-id).
