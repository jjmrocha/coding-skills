---
name: knowledge-base
description: Use when reading from or writing to a configured knowledge base (KB / wiki) — looking up system surfaces (entities, tables, REST endpoints, Kafka events, cron jobs, external dependencies, business rules), reusable helpers, canonical patterns (conventions / recipes / templates), or implementation plans by ticket/branch; ingesting docs; updating the KB after a code change touched a tracked surface; before brainstorming, analyzing code, or producing code in a project with a configured kb_path; or auditing the KB for staleness.
---

# Knowledge Base

A user-curated, agent-maintained KB. Two top-level buckets:

- **`wiki/`** — per-repo system docs (entities, interfaces, jobs, dependencies, events, rules, helpers, patterns). Answers *"what exists?"*
- **`plans/`** — implementation plans, often cross-repo. Answers *"what's intended?"*

## Core Principles (load-bearing)

1. **Code is truth. Wiki is a finding aid.** Every wiki claim that ends up in your reply must be backed by code you read **this turn** — not by the wiki page alone. No *"quick lookup"* exemption; no *"the wiki is recent enough"* exemption. `last_updated` records when the wiki was edited, not when the code was.
2. **Writes are autonomous; deletes require approval** — with one exception (see [Delete protocol](#delete-protocol)). Wrong writes self-correct when the next reader follows the pointer to code; deletes are invisible to future readers.
3. **Multi-file sources must be read in full.** No sampling, no "the README covers it." Skipping files = missing surfaces.

## When NOT to Use

- No `kb_path` configured in CLAUDE.md → refuse; **do not invent a default**.
- Question is about code visible in the working directory → read the code directly.
- Personal memory (preferences, project state) → `~/.claude` memory, not the KB.

## Configuration

```yaml
kb_path: /Users/you/.kb/work    # required — absolute path. No default.
```

**Repo name resolution** (for writes): `git remote.origin.url` → `<repo>`, fallback to `git rev-parse --show-toplevel` basename, else ask once.

**Bootstrap requires approval.** If `<kb_path>` doesn't exist, ask before creating the canonical layout (`wiki/index.md`, `plans/index.md`, optional `git init`). If `wiki/<repo>/` is missing, ask before creating it with the eight default subfolders: `entities/`, `interfaces/`, `jobs/`, `dependencies/`, `events/`, `rules/`, `helpers/`, `patterns/`. All eight are created at bootstrap (empty if no content) so downstream skills always find the expected layout.

## Folder Structure

```
<kb_path>/
  plans/       index.md + <ticket-or-branch>.md
  wiki/        index.md (lists repos)
    <repo>/    index.md (groups pages by subfolder)
      entities/ interfaces/ jobs/ dependencies/ events/ rules/ helpers/ patterns/
```

Two parallel entry points: `wiki/index.md` and `plans/index.md`. No KB-root index.

## Operating Modes

Mode is determined by the user's verb.

| Mode | Trigger phrases | Discipline |
|------|-----------------|------------|
| **Query** | *"what's the orders schema"*, *"is there a plan for PROJ-1234"* | Read-only. **Read cited code.** |
| **Ingest** | *"read this doc and store what's relevant"*, *"ingest the schema from `<path>`"* | Write directly; **report coverage**; summarize. |
| **Update** | *"update the wiki with what we just changed"* | Write directly; summarize. Deletes → protocol. |
| **Lint** | *"audit the KB"*, *"check for stale pages"* | Flag-only **except** auto-delete of non-plan pages with all-dead in-tree sources. |

### Write lock (Ingest, Update, autonomous Delete)

Multi-file writes aren't atomic. Take the advisory lock before writing; release after summary:

```bash
uv run scripts/kb-lock.py acquire <kb_path>   # exit 1 if blocked
# ... writes ...
uv run scripts/kb-lock.py release <kb_path>
```

If `acquire` exits non-zero, **stop**, surface the holder's PID and acquired-at to the user, don't write. Stale locks (>1h) reclaim automatically.

### Query workflow

1. Read `wiki/index.md` or `plans/index.md`.
2. Read the relevant page(s) to find `sources:` paths.
3. **Open the cited code and read it.** This step is non-negotiable. The wiki is the index entry; the code is the answer.
4. Synthesize the answer **from the code**, using the wiki only for surrounding context (rationale, ownership, related surfaces).
5. **Cite both** in your reply: the code file you read this turn AND the wiki page that pointed you there.
6. If code disagrees with wiki — even minor — **surface the disagreement explicitly**, give the code's answer as truth, flag the page for update. Never silently prefer one side.
7. If neither has the answer, say so. Offer to add it once clarified.

### Ingest workflow

Acquire the write lock; release on summary success.

1. **Enumerate the full source set, then read every file.** If the source resolves to more than one file, list every file first (`git ls-files`, `find <dir> -type f`, archive listing). Then read each. **No sampling.** The only allowed exclusions are files the user explicitly named out-of-scope, or boilerplate with no system surface (lockfiles, generated code, vendored deps, binary assets) — and you must announce any exclusion in the summary.
2. Identify the destination: which repo, which subfolder under `wiki/<repo>/`, or `plans/`. Ask only when the source is genuinely ambiguous; for clean sources, pick the best fit and surface the choice in the summary.
3. For each page: create or update; add `[[wiki-links]]`; set `sources:` (listing **every** contributing file) and `last_updated:`.
4. Update the affected `wiki/<repo>/index.md` and the top-level `wiki/index.md` if a new repo or top-level page was added.
5. **Summary is mandatory and leads with a coverage line:**
   ```
   Ingested 17/17 files from docs/architecture/ (0 excluded).
   Wrote:
     + wiki/order-svc/dependencies/sendgrid.md   email provider
     + wiki/order-svc/events/order-created.md    schema, producers, consumers
     ~ wiki/order-svc/index.md                   linked new pages
   ```
   Excluded files get a line each with the reason. **Coverage rule:** if read-count ≠ in-scope-count, you ingested partially — go back to step 1. Reporting "Wrote N pages" without "Ingested M/M files" is incomplete and forbidden.

### Update workflow

Acquire the write lock; release on summary success.

1. Identify pages affected by the change.
2. Write directly. Add `[[wiki-links]]`; set `last_updated:`.
3. Update the repo's `wiki/<repo>/index.md` and `wiki/index.md` as needed.
4. Summarize: one line per page, scannable (`+ new`, `~ updated`).
5. Deletes → [Delete protocol](#delete-protocol).

### Lint workflow

```bash
uv run scripts/lint.py <kb_path> --json
```

**Don't load pages into context to run lint manually** — the script keeps bodies out. Read the structured report. The seven checks:

1. **Broken `sources:` paths** — script flags renames vs dead files separately; doesn't auto-fix paths.
2. **Aging pages** — `last_updated` >90 days. Flag as *"needs review"*, not *"stale"*.
3. **Orphan pages** — no inbound `[[wiki-link]]`.
4. **Concept-gap candidates** — regex heuristic; triage by reading.
5. **`[needs source]` markers** — unsourced claims.
6. **All-dead in-tree sources** — non-plan pages with every `sources:` path truly dead (no rename) are **auto-delete candidates** per the [Delete protocol](#delete-protocol). Plans are flagged, never deleted. Renamed → not eligible (update path instead).
7. **Pattern `kind:` validity** — pages under `patterns/` must declare `kind:` set to `convention | recipe | template`.

Surface 1, 2, 3, 5, 7 to the user; triage 4 by reading; for 6 candidates, verify each with `check-sources.py` before deleting.

### Delete protocol

```bash
uv run scripts/check-sources.py <page-path>
```

| Verdict | Action |
|---|---|
| `safe-to-delete` | All in-tree sources dead, no externals, not a plan, current repo matches page repo. **Delete autonomously.** |
| `partial` | Drop dead/renamed entries from `sources:`; flag for review. Don't delete. |
| `flag (renames)` | Update source paths. Don't delete. |
| `flag (external / cross-repo / plan / no-sources)` | Surface to user. Don't delete. |
| `all-alive` | Nothing to do. |

**Autonomous delete = only `safe-to-delete`. Every other delete reason (page obsolete for non-source reasons, merging, restructuring, "user said delete") requires explicit approval.** Before approved deletes, show what's about to be deleted and which inbound `[[wiki-links]]` will break.

Autonomous deletes still take the [write lock](#write-lock-ingest-update-autonomous-delete) around the delete + index updates.

After any delete: remove the entry from the repo's `index.md` and `wiki/index.md`. Include the delete in the post-action summary.

## Page Format

YAML frontmatter (`summary`, `sources` ≥1 entry, `last_updated: YYYY-MM-DD`, `kind:` only on `patterns/`) + Markdown body. Wiki-links use **paths from the KB root, no extension**: `[[wiki/<repo>/entities/<name>]]`, `[[plans/<ticket>]]`. Citations live in `sources:`, never inline (use `[needs source]` for unsupported claims). Full template, per-subfolder body shape, and the special-case rule for `wiki/index.md` (uses standard markdown links): [references/page-template.md](references/page-template.md), [references/index-templates.md](references/index-templates.md).

`helpers/` and `patterns/` have a specific inclusion bar and creation channel — see [references/helpers-and-patterns.md](references/helpers-and-patterns.md).

## Integration with Other Skills

When `kb_path` is configured, `brainstorm`, `analyze-code`, and `using-software-specialists` consult the KB. They read the repo's `wiki/<repo>/index.md` — including the `Helpers` and `Patterns` sections — before producing code, then drill into specific pages on demand. `using-software-specialists` Phase B autonomously updates `helpers/<category>.md` when a new function meets the inclusion bar. Pattern *creation* is Ingest-only. Full integration matrix: [references/integrations.md](references/integrations.md).

## Wiki ↔ Code Disagreements

| Failure mode | Action |
|---|---|
| Wiki claims something code doesn't reflect | **Surface as a finding.** Often signals a bug, not just stale docs. Answer from code; flag the page. |
| Wiki silent on a real thing | Lint flags it; suggest `/knowledge-base update`. |
| Reinvents an existing helper | Finding. Suggest replacing with the documented helper. |
| Violates a documented `patterns/` convention | Finding. Surface convention + divergence; user decides. |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Inventing a `kb_path` default | Refuse; ask user to set it in CLAUDE.md. |
| Answering a *"quick lookup"* from the wiki without opening cited code | No exemption. Read `sources:` files before replying. |
| Citing only the wiki in your reply | Cite both: code file read this turn + wiki page that pointed you there. |
| Ingesting from a multi-file source by reading only a sample | Enumerate, then read every file. Coverage line (`Ingested M/M`) is mandatory. |
| Listing only the first contributing file under `sources:` | List **every** file that contributed. |
| Auto-deleting a page because user said *"delete"* | Only `safe-to-delete` verdict is autonomous. Merges, restructures, "obsolete" reasons need approval. |
| Auto-deleting when sources were renamed | Renames → update path, not delete. |
| Auto-deleting a plan page | Plans are never auto-deleted. |
| Inline `(source: ...)` in page body instead of `sources:` frontmatter | Provenance belongs in frontmatter so lint can audit it. |
| Unquoted YAML string with `:`, `#`, leading `&`/`*`/`!`/`>` etc. | Quote it: `summary: "..."`. Also quote bareword values that look like booleans (`yes`, `no`) or numbers — YAML coerces them silently. |
| Asking for diff approval before every write | Write directly; summarize after. Approval theater rubber-stamps at scale. |

More edge cases and the full YAML-pitfalls writeup: [references/common-pitfalls.md](references/common-pitfalls.md).
