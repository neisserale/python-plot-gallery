# 01 — Product Requirements

> Status: Approved v1.0 · Last updated: 2026-10-18 · Index: [README](README.md) · Visual summary: [00](00-overview.md)

## 1. Vision

**Plot Gallery is an open catalog of Python data visualizations where every plot can be reproduced.** Each entry shows the final figure, explains what it is for, and publishes the exact code, the dataset and a step-by-step notebook needed to recreate it.

Existing galleries (Matplotlib Gallery, Seaborn Examples, Python Graph Gallery) are great for discovering plots. Their weak points are the ones this project targets:

| Gap in existing galleries | Plot Gallery's answer |
|---------------------------|-----------------------|
| Examples use synthetic data or hidden loaders | Every plot uses a real, downloadable, versioned dataset |
| The published code is not guaranteed to produce the image shown | CI re-renders every image from the published code on each change |
| Dependency versions are not stated | Exact pinned versions, runnable with `uv run plot.py` |
| Code is shown, but how it was built is not | Each plot comes with a progressive notebook (six fixed steps) |
| The design feels like documentation | A modern, focused interface built for browsing and learning |

## 2. Problem and goals

### 2.1 Problem

Data practitioners and students copy plotting code that often does not run as-is. Datasets are missing, versions don't match, or there is hidden preprocessing. Educators have no curated, trustworthy, reproducible set of examples to point students to.

### 2.2 Goals

| ID | Goal | Measure of success (MVP) |
|----|------|--------------------------|
| G-1 | **Reproducibility.** Every published plot can be regenerated from public resources. | 100% of plots pass the CI reproducibility check on `main` |
| G-2 | **Learning.** Users understand how a plot is built, not just its final form. | Every plot has a notebook following the 6-step structure |
| G-3 | **Discoverability.** Users find a suitable plot quickly. | Any plot reachable in ≤ 2 interactions (search or filter) from the gallery |
| G-4 | **Quality.** The site looks professional and is fast and accessible. | Lighthouse ≥ 90 (mobile) in Performance, Accessibility, Best Practices and SEO |
| G-5 | **Low maintenance.** Adding a plot is cheap and safe. | A new plot needs only 3 authored files and one CLI command |

### 2.3 Non-goals (MVP)

- Running user-provided code in the browser or on a server.
- User accounts, comments, ratings, authentication, payments, a database.
- Interactive (Plotly) charts. They are planned, see D-06.
- A CMS or web-based authoring. Content is authored in git.
- Internationalization. The site is in English only.

## 3. Target users

| Persona | Context | Main need | Key features |
|---------|---------|-----------|--------------|
| **Dana — Data Scientist** | Building a report and needs a specific chart quickly | Copy working code and adapt it | Search, copy code, pinned dependencies |
| **Alex — Data Analyst** | Knows pandas and is moving from Excel charts to Python | Pick the right chart for the question | Categories, "when to use" guidance |
| **Sam — Python developer** | Not a dataviz specialist | Runnable, idiomatic code | `uv run plot.py`, clean modular code |
| **Lee — Student** | Learning data visualization | Understand step by step | Notebook, Colab link, dataset preview |
| **Prof. Kim — Educator** | Prepares course material | Trustworthy, citable, reusable examples | Dataset license and citation, stable URLs, Colab |

## 4. User stories

Priority: **M** = Must (MVP), **S** = Should (MVP if time allows), **C** = Could (post-MVP).

### Browse and discover

| ID | Story | Priority |
|----|-------|----------|
| US-01 | As a user, I want to see all plots as a visual grid of cards so that I can browse by appearance. | M |
| US-02 | As a user, I want to search plots by name, description, tags, library or dataset so that I find a plot quickly. | M |
| US-03 | As a user, I want to filter by category and by library so that I narrow the catalog to what I need. | M |
| US-04 | As a user, I want the search and filters reflected in the URL so that I can share or bookmark a filtered view. | S |
| US-05 | As a user, I want a clear empty state when nothing matches, with a way to reset the filters. | M |

### Understand a plot

| ID | Story | Priority |
|----|-------|----------|
| US-10 | As a user, I want to see the final plot at high quality and enlarge it so that I can inspect the details. | M |
| US-11 | As an analyst, I want to read what the plot represents, when to use it and its common applications so that I choose the right chart. | M |
| US-12 | As a user, I want to see which libraries (and versions) the plot uses. | M |
| US-13 | As a user, I want links to related plots so that I can explore alternatives. | S |

### Reproduce a plot

| ID | Story | Priority |
|----|-------|----------|
| US-20 | As a data scientist, I want to view the complete Python code with syntax highlighting and copy it with one click. | M |
| US-21 | As a user, I want to see the dataset's name, description, source, license, columns (highlighting the ones the plot needs) and a preview of its rows. | M |
| US-22 | As a user, I want to download the dataset as CSV. | M |
| US-23 | As a user, I want to download **one bundle** (code + dataset + notebook), unzip it and run `uv run plot.py` to get the same figure. | M |
| US-24 | As a student, I want to open the plot's notebook on GitHub to follow the construction step by step. | M |
| US-25 | As a student, I want to open the notebook in Google Colab and run it without any local setup. | S |
| US-26 | As a user, I want to download `plot.py` as a file. | S |

### Experience

| ID | Story | Priority |
|----|-------|----------|
| US-30 | As a user, I want light and dark mode, defaulting to my system preference, so that reading is comfortable. | M |
| US-31 | As a mobile user, I want every page to work well on a phone. | M |
| US-32 | As a keyboard or screen-reader user, I want to use every feature, and I want each plot to have a meaningful text alternative. | M |
| US-33 | As a visitor, I want an About page explaining the project, the reproducibility guarantee and how to contribute. | S |

### Contributor (maintainer)

| ID | Story | Priority |
|----|-------|----------|
| US-40 | As a maintainer, I want to scaffold a new plot with one command so that its structure is always correct. | S |
| US-41 | As a maintainer, I want one command that validates, renders, executes and compiles all content locally. | M |
| US-42 | As a maintainer, I want CI to block a merge when a notebook fails, metadata is invalid, or the published code no longer matches the published image. | M |
| US-43 | As a maintainer, I want every merge to `main` deployed automatically, with preview deployments for pull requests. | M |

## 5. Functional requirements

### 5.1 Gallery

| ID | Requirement |
|----|-------------|
| FR-01 | The home page lists every published plot as a card with a thumbnail, title, summary, categories, primary library and a link to its detail page. |
| FR-02 | A search box filters the cards as the user types. Matching ignores case and accents and covers title, summary, tags, categories, libraries, chart type and dataset name. Multi-word queries match cards containing **all** words. |
| FR-03 | Filters: categories (multi-select) and libraries (multi-select). Options in the same group combine with **OR**; different groups and the search combine with **AND**. |
| FR-04 | Each filter option shows how many plots it would match given the other active filters. |
| FR-05 | The current search and filters are stored in the URL (`?q=&category=&library=`) and restored when the page loads. |
| FR-06 | A "Clear filters" action and a result count ("3 plots") are always visible while filters are active. |
| FR-07 | Default order: featured plots first, then by title. |

### 5.2 Plot detail page (`/plots/<plot-id>`)

| ID | Requirement |
|----|-------------|
| FR-10 | **Header:** breadcrumb, chart type, title, summary, category badges (with icons), library badges, difficulty. |
| FR-11 | **Visualization:** the rendered figure at high resolution (responsive `srcset`), with alt text, that can be enlarged in a dialog. |
| FR-12 | **Description:** what the plot represents, when to use it (list), common applications (list) and, optionally, caveats. |
| FR-13 | **Dataset:** name, description, source with link, license, citation, row and column counts, file size, a column table (name, type, description, unit, *required by this plot* marker), a preview of the first 10 rows and a CSV download button. |
| FR-14 | **Python code:** the full `plot.py` with syntax highlighting, line numbers, a copy-to-clipboard button with visible and screen-reader feedback, a download button and a list of pinned dependencies. |
| FR-15 | **Notebook:** a link to the `.ipynb` on GitHub, an "Open in Colab" link, and the six-step outline of the notebook. |
| FR-16 | **Related plots:** up to 3 cards. The related plots declared in metadata come first; the rest is filled with plots sharing a category. |
| FR-17 | **"Reproduce this plot" card:** three numbered steps (① download the bundle `<plot-id>.zip`, ② unzip and open a terminal in the folder, ③ run `uv run plot.py`, with a copy button), a link to install uv, the alternatives "Copy code" and "Open in Colab", and key facts (primary library, dataset, license, last updated). It is sticky on desktop and placed right after the figure on mobile. |
| FR-18 | An unknown `plot-id` returns a styled 404 page. |
| FR-19 | A sticky horizontal **section bar** (Visualization · Description · Dataset · Code · Notebook) highlights the current section and scrolls to a section when clicked, with the same pattern on all screen sizes. |

### 5.3 Global

| ID | Requirement |
|----|-------------|
| FR-20 | Theme toggle with three modes: System (default), Light and Dark. The choice persists and the page never flashes the wrong theme. |
| FR-21 | Header with logo, navigation (Gallery, About), GitHub link and theme toggle. Footer with license, repository link and credits. |
| FR-22 | Per-page SEO metadata (title, description, canonical URL, Open Graph image = the plot thumbnail), plus `sitemap.xml` and `robots.txt`. |
| FR-23 | About page: mission, the reproducibility guarantee, local usage, how to contribute, licenses (Should). |

### 5.4 Content pipeline (maintainer-facing)

| ID | Requirement |
|----|-------------|
| FR-30 | `gallery check` validates all metadata against the schemas and checks referential integrity (dataset ids, related plot ids, required columns present in the dataset). |
| FR-31 | `gallery render` executes each `plot.py` in an isolated directory that contains only that file and its dataset, then writes the full-size PNG and WebP thumbnails. |
| FR-32 | `gallery check` re-renders every plot and compares the result against the committed image within a tolerance. A mismatch fails the check. |
| FR-33 | `gallery execute` runs every notebook top to bottom in an isolated directory. Any error fails the check. |
| FR-34 | `gallery sync` writes the pinned dependencies (from `uv.lock`) into each `plot.py` header and copies `plot.py` into the notebook's final cell. `gallery check` fails if either is out of date. |
| FR-35 | `gallery build` compiles `catalog.json`. `gallery check` fails if the committed catalog differs from a fresh build. |
| FR-36 | Datasets are checked against their declared SHA-256 checksum and declared columns. |
| FR-37 | `gallery new <plot-id>` scaffolds a plot folder from templates (Should). |
| FR-38 | `gallery build` produces a deterministic bundle `<plot-id>.zip` per plot containing `plot.py`, the dataset CSV, `notebook.ipynb` and a generated `README.md` with run instructions, license and citation. |

## 6. Non-functional requirements

| ID | Area | Requirement |
|----|------|-------------|
| NFR-01 | Reproducibility | Each plot regenerates within tolerance on CI (Ubuntu) and on a contributor machine (Windows/macOS/Linux) using `uv sync` + `gallery render`. |
| NFR-02 | Reproducibility | A user who downloads `plot.py` and its CSV into an empty folder and runs `uv run plot.py` gets the published figure. |
| NFR-03 | Performance | Lighthouse mobile ≥ 90 in all four categories; LCP ≤ 2.5 s and CLS ≤ 0.1 on simulated 4G. |
| NFR-04 | Performance | No Python and no server-side computation per request. Every page is static HTML. |
| NFR-05 | Performance | Thumbnails ≤ 80 KB (WebP, 800 px). Only the content visible on load is loaded eagerly. |
| NFR-06 | Accessibility | WCAG 2.2 AA: contrast, keyboard operability, visible focus, semantic landmarks, alt text required by the schema, `prefers-reduced-motion` respected. |
| NFR-07 | Accessibility | Plots in the MVP use colorblind-safe palettes (authoring guideline, checked in review). |
| NFR-08 | Responsiveness | Fully usable from 360 px to 1920 px wide, with no horizontal page scroll. Wide tables and code scroll inside their own containers. |
| NFR-09 | Maintainability | Adding a plot touches only `content/`. No frontend code changes. |
| NFR-10 | Maintainability | One Python environment (`uv.lock`) and one Node lockfile, both pinned. Lint and format run in CI. |
| NFR-11 | Security | A static site with no user input processed server-side. Security headers set (CSP, `X-Content-Type-Options`, `Referrer-Policy`). Dependencies updated through Dependabot (post-MVP). |
| NFR-12 | Size | Each dataset ≤ 5 MB, enforced by the validator. |
| NFR-13 | Browser support | The last 2 versions of Chrome, Edge, Firefox and Safari (desktop and mobile). |
| NFR-14 | Licensing | Every dataset declares its license and source. Only datasets that may be redistributed are accepted. |

## 7. MVP scope

### In scope

- Gallery page with search, category and library filters, and URL state.
- Detail page with all five sections (Visualization, Description, Dataset, Python Code, Jupyter Notebook), the "Reproduce this plot" card with its downloadable bundle, and related plots.
- Light and dark mode, responsive layout, accessibility baseline.
- About page (Should).
- Three plots, all from the **Palmer Penguins** dataset (CC0-1.0) (D-08):

| plot-id | Chart | Category | Primary library | Question it answers |
|---------|-------|----------|-----------------|---------------------|
| `scatter-penguin-bill-dimensions` | Scatter plot | Relationship | Seaborn | How do bill length and depth relate across species? |
| `box-penguin-body-mass` | Box plot | Distribution, Comparison | Seaborn | How does body mass differ by species and sex? |
| `histogram-penguin-flipper-length` | Histogram | Distribution | Matplotlib (+ NumPy) | What does the distribution of flipper length look like? |

- Python content pipeline (validate, sync, render, execute, build, check) and CI.
- Vercel production deploys from `main` and preview deploys for pull requests.

### Out of scope (MVP)

Plotly/interactive charts, user accounts, comments, a database, a CMS, i18n, analytics (optional later), category landing pages (filtering via query parameters covers them), dark variants of images, a code playground.

### Category taxonomy

`distribution`, `comparison`, `relationship`, `composition`, `time-series`, `statistical`, `machine-learning`.
A plot has 1–3 categories. The list is a closed enum ([03 §3](03-data-model.md#3-plot-metadata-plotyaml)).

## 8. Acceptance criteria (MVP)

The MVP is accepted when all of the following hold.

**Gallery**

- AC-01 — *Given* the home page, *then* three cards are shown, each with a thumbnail, title, summary, categories and primary library, linking to `/plots/<plot-id>`.
- AC-02 — *Given* the query `flipper`, *then* only `histogram-penguin-flipper-length` is shown and the URL contains `?q=flipper`.
- AC-03 — *Given* the filters Category = Distribution and Library = Seaborn, *then* only `box-penguin-body-mass` is shown.
- AC-04 — *Given* a filter combination with no matches, *then* an empty state with a "Clear filters" button is shown, and clicking it restores all three plots.
- AC-05 — *Given* a URL with filters, *when* it is opened in a new tab, *then* the same filtered view is shown.

**Detail page**

- AC-10 — Each detail page shows the five sections in order, and each is reachable through the section bar.
- AC-11 — The code shown equals the committed `plot.py` byte for byte, and "Copy" puts that exact text on the clipboard and announces "Copied".
- AC-12 — "Download dataset" downloads a CSV whose SHA-256 matches `dataset.yaml`.
- AC-13 — Downloading the bundle, unzipping it and running `uv run plot.py` inside the folder opens a figure that matches the published image (manual check on Windows and one Unix OS).
- AC-14 — The GitHub notebook link opens the `.ipynb` with rendered outputs, and the Colab link opens a notebook that runs top to bottom without manual steps.
- AC-15 — The required columns are highlighted in the dataset section, and the preview shows 10 rows.
- AC-16 — `/plots/does-not-exist` shows the 404 page.

**Quality**

- AC-20 — CI on `main` is green: lint, unit tests, `gallery check` (schemas, checksums, sync, render comparison, notebook execution, catalog drift), type-check, frontend build, E2E smoke + axe (D-11).
- AC-21 — Deliberately changing a color in a `plot.py` without re-rendering makes CI fail on the image comparison.
- AC-22 — Lighthouse mobile ≥ 90 on `/` and on one detail page, in all four categories.
- AC-23 — Every page works with the keyboard alone, and axe reports no serious or critical violations.
- AC-24 — The theme follows the system by default, the toggle persists across reloads, and there is no flash of the wrong theme.
- AC-25 — Layout verified at 360, 768, 1280 and 1920 px with no horizontal page scroll.
- AC-26 — The production URL serves the site, and every pull request gets a preview URL.
