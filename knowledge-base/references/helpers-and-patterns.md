# `helpers/` and `patterns/` — Internal-Knowledge Subfolders

Two subfolders under `wiki/<repo>/` capture *internal* knowledge the six system subfolders don't: reusable functions in the repo, and canonical shapes for recurring problems. Same `sources:` / `last_updated:` discipline as every other page.

## `helpers/` — catalog of reusable functions

- **Granularity:** one file per category. A category is a topic cluster (`helpers/dates.md`), not a module path. Every cross-cutting date helper lives in `dates.md` regardless of which source file holds it.
- **Escape hatch:** a single large or non-trivial helper can have its own page (`helpers/<name>.md`). The category page links to it.
- **Inclusion bar:** a function appears in `helpers/` if and only if:
  - **(a)** it is reusable across the repo — not specific to a single feature's internal use, AND
  - **(b)** it is not private (Python: not prefixed with `_`; analogous for other languages).
- **Excluded:** domain-specific helpers (e.g., `build_dcf_inputs` in a finance app) stay with their feature. Private functions never appear.
- **`sources:`** lists the file(s) where the listed helpers are defined; usually one file per category.
- **Page shape:** see [page-template.md](page-template.md) (the `helpers/` row).

## `patterns/` — canonical shapes for recurring problems

- **Granularity:** one file per pattern.
- **`kind:` (required frontmatter):** one of:
  - `convention` — a standing decision about how to do something (e.g., "we use offset pagination, never cursor"). Carries the *rule* and the *why*.
  - `recipe` — a step-by-step how-to for a recurring task (e.g., "how to add a new CLI command"). References the files touched.
  - `template` — a canonical code snippet (e.g., "unit-test shape with fixtures"). Snippet ~30 lines max — beyond that, point to the exemplar.
- **`sources:`** cites canonical exemplar file(s) — the place(s) the team treats as "the way."
- **Page shape:** see [page-template.md](page-template.md) (the `patterns/` row).
- **Creation channel (load-bearing):** pattern pages are created **only** via the Ingest or Update workflow. They are **not** created autonomously by a specialist mid-implementation. Updating an existing pattern page (e.g., the exemplar's signature changed) is a normal autonomous Update — that's fine.

## Why the per-repo index always renders these two headings

The repo's `index.md` always renders `## Helpers` and `## Patterns` — with an explicit `*(none yet)*` placeholder when empty — even though the six system sections are dropped when empty. Reason: `brainstorm`, `analyze-code`, and `using-software-specialists` consult these two sections by name before producing code. An absent heading is indistinguishable from "I forgot to look." See [index-templates.md](index-templates.md).
