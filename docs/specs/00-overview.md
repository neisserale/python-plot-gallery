# 00 — The System at a Glance

> Status: Approved v1.0 · Last updated: 2026-10-18 · Index: [README](README.md)

This document explains the whole product **with pictures first**. Each diagram has a short caption, and the details live in documents 01–06.

> **Viewing the diagrams:** GitHub renders Mermaid natively. In VS Code or Cursor, install *Markdown Preview Mermaid Support* (`bierner.markdown-mermaid`) and open the Markdown preview (`Ctrl+Shift+V`).

---

## 1. What we are building, in one sentence

> A website where every Python plot comes with **the code, the data and a notebook** that reproduce it exactly, and where a robot checks that promise on every change.

---

## 2. The services, end to end

Who does what, from the author's keyboard to the visitor's screen.

```mermaid
flowchart LR
  subgraph LOCAL["💻 Author's computer"]
    direction TB
    IDE["VS Code / Cursor<br/>+ Claude Code"]
    UV["uv<br/>Python 3.12 environment"]
    CLI["gallery CLI<br/>validate · render · build"]
    DEV["npm run dev<br/>local preview of the site"]
    IDE --> CLI
    UV --> CLI
    CLI --> DEV
  end

  subgraph GITHUB["🐙 GitHub"]
    direction TB
    PR["Pull request"]
    REPO[("Repository<br/>main branch")]
  end

  subgraph ACTIONS["⚙️ GitHub Actions — the safety net"]
    direction TB
    CI1["content.yml<br/>Python + reproducibility checks"]
    CI2["web.yml<br/>site build + tests"]
  end

  subgraph VERCEL["▲ Vercel"]
    direction TB
    BUILD["Build<br/>next build → static files"]
    CDN["Global CDN<br/>production + PR previews"]
    BUILD --> CDN
  end

  subgraph EXTERNAL["🌍 External services"]
    direction TB
    PYPI["PyPI<br/>Python packages"]
    COLAB["Google Colab<br/>runs notebooks online"]
    RAW["raw.githubusercontent.com<br/>dataset files"]
  end

  VISITOR["🧑‍💻 Visitor's browser"]

  PYPI -.->|"uv installs"| UV
  IDE -->|"git push"| PR
  PR --> CI1 & CI2
  CI1 & CI2 -->|"✅ all green"| REPO
  PR -->|"preview deploy"| BUILD
  REPO -->|"merge to main"| BUILD
  CDN -->|"HTML · images · CSV · zip"| VISITOR
  VISITOR -->|"View notebook"| REPO
  VISITOR -->|"Open in Colab"| COLAB
  COLAB -->|"downloads CSV"| RAW
```

| Service | Role | What runs there | Cost |
|---------|------|-----------------|------|
| **Author's computer** | Create and preview content | `uv`, the `gallery` CLI, Jupyter, `npm run dev` | — |
| **GitHub** | Source of truth; notebook rendering | git, PRs, notebook viewer | Free (public repo) |
| **GitHub Actions** | Prove every plot is still reproducible | Python checks, image comparison, notebook execution, site build, E2E tests | Free (public repo) |
| **Vercel** | Build and serve the site | `next build` (Node only, **no Python**), CDN | Free (Hobby) |
| **PyPI** | Package index | Used by `uv` locally, in CI, and for visitors running `uv run plot.py` | Free |
| **Google Colab** | Zero-install notebook execution for visitors | The plot's notebook | Free |

**Key idea:** Python only runs on the author's machine and in GitHub Actions. Visitors receive plain static files, which makes the site fast, cheap and safe.

---

## 3. The repository in four worlds

Each top-level folder has **one role**. If you know which world you are in, you know whether you should edit a file.

```mermaid
flowchart LR
  C["✍️ <b>content/</b><br/>what humans write<br/><i>datasets · plots · notebooks</i>"]
  P["⚙️ <b>pipeline/</b><br/>the gallery CLI<br/><i>validates · renders · compiles</i>"]
  G["🤖 <b>generated/</b><br/>what the machine writes<br/><i>catalog · images · bundles · schemas</i>"]
  W["🌐 <b>web/</b><br/>the website<br/><i>reads the catalog and shows it</i>"]

  C -->|"input"| P
  P -->|"output"| G
  G -->|"read at build time"| W
  C -.->|"plot.py and CSV copied as downloads"| W

  classDef human fill:#FDF6D8,stroke:#B8A44A,color:#16181D
  classDef machine fill:#E3F2F1,stroke:#1A7F7A,color:#16181D
  classDef site fill:#ECEAF6,stroke:#5B4F9A,color:#16181D
  class C human
  class P,G machine
  class W site
```

| World | Who writes it | Edit by hand? | Committed? |
|-------|---------------|---------------|------------|
| ✍️ `content/` | Authors | **Yes**, this is where content is created | Yes |
| ⚙️ `pipeline/` | Maintainers (tooling code) | Yes, when changing the tooling | Yes |
| 🤖 `generated/` | `uv run gallery update` | **Never** | Yes, and CI rejects any drift |
| 🌐 `web/` | Maintainers (frontend code) | Yes, when changing the site | Yes (except `public/assets/`, which is copied at build time) |
| 📘 `docs/` | Everyone | Yes | Yes |

The full tree is in [05 — Project Structure](05-project-structure.md).

---

## 4. Anatomy of a plot

Three files you write, plus one shared dataset, become one detail page.

```mermaid
flowchart LR
  subgraph AUTHORED["✍️ content/plots/scatter-penguin-bill-dimensions/"]
    direction TB
    Y["📄 plot.yaml<br/>title · description · categories<br/>dataset · alt text"]
    PY["🐍 plot.py<br/>the code that draws the figure"]
    NB["📓 notebook.ipynb<br/>the 6-step explanation"]
  end

  DS["✍️ content/datasets/palmer-penguins/<br/>📄 dataset.yaml + 📊 palmer-penguins.csv"]

  subgraph GEN["🤖 generated/plots/scatter-penguin-bill-dimensions/"]
    direction TB
    IMG["🖼️ plot.png + .webp"]
    ZIP["📦 bundle .zip<br/>plot.py + CSV + notebook + README"]
  end

  subgraph PAGE["🌐 /plots/scatter-penguin-bill-dimensions"]
    direction TB
    A["A · Visualization"]
    B["B · Description"]
    CC["C · Dataset"]
    D["D · Python code"]
    E["E · Notebook"]
    R["⭐ Reproduce this plot<br/>(3 steps)"]
  end

  PY -->|"rendered"| IMG --> A
  Y --> B
  Y -->|"dataset.id"| DS --> CC
  PY -->|"shown byte for byte"| D
  NB -->|"GitHub + Colab links"| E
  PY & DS & NB --> ZIP --> R
```

| You write | It becomes |
|-----------|------------|
| `plot.yaml` | The card, the title, the description and the filters |
| `plot.py` | The image (rendered by CI), the code block, the download and the notebook's final cell |
| `notebook.ipynb` (steps 1–5) | The step-by-step lesson on GitHub and Colab |
| `dataset.yaml` + CSV (once, shared) | The dataset section, the preview table and the download |

---

## 5. The pipeline: from sources to site

`uv run gallery update` runs four steps in order. `uv run gallery check` runs the same logic **without writing anything** and fails on any difference. That is what CI runs.

```mermaid
flowchart LR
  subgraph IN["✍️ Sources"]
    LOCK["uv.lock"]
    PY["plot.py"]
    NB["notebook.ipynb"]
    YML["plot.yaml<br/>dataset.yaml"]
    CSV["dataset CSV"]
  end

  S1["① sync<br/>pin versions in plot.py<br/>copy plot.py → notebook final cell"]
  S2["② render<br/>run plot.py in an empty sandbox<br/>save PNG + WebP"]
  S3["③ execute<br/>run the notebook top to bottom<br/>store outputs"]
  S4["④ build<br/>validate everything<br/>compile catalog + zip bundles"]

  subgraph OUT["🤖 Results"]
    IMG["generated/plots/{id}/<br/>images + bundle"]
    CAT["generated/catalog.json"]
    SCH["generated/schemas/"]
    NBO["notebook outputs"]
  end

  LOCK --> S1
  PY --> S1 --> S2 --> S3 --> S4
  CSV --> S2 & S3 & S4
  NB --> S1
  YML --> S4
  S2 --> IMG
  S3 --> NBO
  S4 --> CAT & SCH & IMG
```

The **sandbox** is a temporary empty folder that contains only `plot.py` and its CSV. If the code secretly depends on anything else (another file, the internet, your personal matplotlib settings), it fails there instead of failing for a visitor.

---

## 6. The life of a plot: from idea to production

```mermaid
sequenceDiagram
  autonumber
  actor A as ✍️ Author
  participant CLI as ⚙️ gallery CLI
  participant GH as 🐙 GitHub
  participant CI as ✅ GitHub Actions
  participant V as ▲ Vercel
  actor U as 🧑‍💻 Visitor

  A->>CLI: gallery new box-penguin-body-mass
  CLI-->>A: folder with plot.yaml, plot.py, notebook.ipynb (templates)
  A->>A: write metadata, code, notebook steps 1–5
  A->>CLI: gallery update box-penguin-body-mass
  CLI-->>A: images, notebook outputs, catalog, bundle
  A->>A: npm run dev → check the page locally
  A->>GH: push branch + open pull request
  GH->>CI: run content.yml + web.yml
  GH->>V: build preview
  V-->>A: preview URL
  CI-->>GH: ✅ reproducible, valid, builds
  A->>GH: merge to main
  GH->>V: production build
  V-->>U: new plot is live
```

---

## 7. The safety net: what CI guarantees

Every pull request has to pass every gate. A ❌ blocks the merge, so broken content never reaches visitors.

```mermaid
flowchart TD
  START(["Pull request opened"]) --> Q1{"Metadata valid?<br/>schemas · ids · columns"}
  Q1 -->|no| X1["❌ field-level error report"]
  Q1 -->|yes| Q2{"Dataset intact?<br/>checksum · columns · types"}
  Q2 -->|no| X2["❌ dataset changed or invalid"]
  Q2 -->|yes| Q3{"Code in sync?<br/>version pins · notebook final cell"}
  Q3 -->|no| X3["❌ run gallery update"]
  Q3 -->|yes| Q4{"Image reproducible?<br/>re-render ≈ committed image"}
  Q4 -->|no| X4["❌ diff image attached to the run"]
  Q4 -->|yes| Q5{"Notebook runs<br/>top to bottom?"}
  Q5 -->|no| X5["❌ failing cell reported"]
  Q5 -->|yes| Q6{"Catalog, bundles and<br/>types up to date?"}
  Q6 -->|no| X6["❌ generated/ is stale"]
  Q6 -->|yes| Q7{"Site builds, tests pass,<br/>no accessibility errors?"}
  Q7 -->|no| X7["❌ build / test / axe report"]
  Q7 -->|yes| OK(["✅ Ready to merge → auto-deploy"])

  classDef fail fill:#FDE8E6,stroke:#B42318,color:#16181D
  classDef pass fill:#E3F2F1,stroke:#1A7F7A,color:#16181D
  class X1,X2,X3,X4,X5,X6,X7 fail
  class OK pass
```

---

## 8. The visitor's journey

The UX has a single goal: **go from "I need a chart" to "I have it running" in as few steps as possible.**

```mermaid
flowchart TD
  A(["Arrive at the gallery"]) --> B{"Do I know<br/>what I want?"}
  B -->|"yes"| C["🔍 Search<br/><i>'histogram', 'seaborn'…</i>"]
  B -->|"not yet"| D["🏷️ Filter<br/>by category or library"]
  C & D --> E["Open a plot card"]
  E --> F["👀 See the figure<br/>📖 read when to use it"]
  F --> G{"How do I want<br/>to reproduce it?"}
  G -->|"fastest"| H["⧉ Copy the code"]
  G -->|"on my machine"| I["📦 Download bundle<br/>→ unzip → uv run plot.py"]
  G -->|"no install"| J["▶ Open in Colab"]
  G -->|"learn step by step"| K["📓 Read the notebook"]
  H & I & J & K --> L(["✅ Same figure, reproduced"])
```

---

## 9. Pages at a glance

```mermaid
flowchart LR
  HOME["🏠 /<br/>Gallery<br/>search · filters · cards"]
  DETAIL["📈 /plots/{id}<br/>Plot detail<br/>figure · reproduce · 5 sections"]
  ABOUT["ℹ️ /about<br/>Mission · how it works<br/>contribute"]
  NF["🚫 404"]
  EXT["🐙 GitHub notebook<br/>▶ Colab"]

  HOME -->|"card"| DETAIL
  DETAIL -->|"breadcrumb / back (filters kept)"| HOME
  DETAIL -->|"related plots"| DETAIL
  DETAIL --> EXT
  HOME <--> ABOUT
```

Wireframes and the visual system are in [04 — UI/UX](04-ui-ux-spec.md).

---

## 10. The build plan

```mermaid
flowchart LR
  P1["P1<br/>Foundation"] --> P2["P2<br/>Pipeline"]
  P1 --> P4["P4<br/>Gallery page"]
  P2 --> P3["P3<br/>First 3 plots"]
  P2 -.->|"catalog schema"| P4
  P3 & P4 --> P5["P5<br/>Detail page"]
  P5 --> P6["P6<br/>Quality"]
  P6 --> P7["P7<br/>Launch 🚀"]
```

Details, tasks and exit criteria are in [06 — Implementation Plan](06-implementation-plan.md).

---

## 11. Where to read more

| If you want to know… | Read |
|----------------------|------|
| Why the product exists, user stories, acceptance criteria | [01 — Product Requirements](01-product-requirements.md) |
| How the system works and why it was designed that way | [02 — Technical Architecture](02-technical-architecture.md) |
| What every file contains and how it is validated | [03 — Data Model](03-data-model.md) |
| How it looks and behaves | [04 — UI/UX Specification](04-ui-ux-spec.md) |
| Where each file lives | [05 — Project Structure](05-project-structure.md) |
| In what order we build it | [06 — Implementation Plan](06-implementation-plan.md) |
