---
name: knowledge-base
description: Use when reading from or writing to a configured knowledge base (KB / wiki) — looking up system surfaces (entities, tables, REST endpoints, Kafka events, cron jobs, external dependencies, business rules), reusable helpers, canonical patterns (conventions / recipes / templates), or implementation plans by ticket/branch; ingesting docs; updating the KB after a code change touched a tracked surface; before brainstorming, analyzing code, or producing code in a project with a configured kb_path; or auditing the KB for staleness.
---

# Knowledge Base

A user-curated, agent-maintained **knowledge base (KB)** for your project workspace. The KB is the root container; it holds two kinds of content with different lifecycles and different trust semantics:

- **Wiki** (`wiki/`) — per-repo system documentation: entities, interfaces, jobs, dependencies, events, business rules. Pages point at the code that implements each surface and carry the *why* the code can't express on its own. Answers *"what exists?"* — wiki claims describe current state, so they must be backed by code (see Core Principles).
- **Plans** (`plans/`) — implementation plans for features and tickets, often spanning repos, with their own lifecycle (Draft / Active / Done / Abandoned). Answers *"what's intended?"* — plans describe intent, not current state, so the code-citation rule binds them less strictly (still read code before reporting *current* facts even when a plan describes them).

Queryable on its own; consulted by `brainstorm` and `analyze-code` when a `kb_path` is configured.

## Core Principles

1. **Code is the source of truth. The wiki is a finding aid.** Wiki pages tell you where things live and why they exist; the code tells you what they actually do. Reading the wiki is never a substitute for reading the code it cites. Every wiki claim that ends up in your reply to the user must be backed by code you read *this turn* — not by the wiki page alone.
2. **Writes are autonomous; deletes are not.** Wrong writes self-correct when readers follow the pointer to code. Deletes are invisible to future readers, so they need approval — with one autonomous exception: non-plan pages whose `sources:` are all truly dead (no rename detected). See the [Delete protocol](#delete-protocol) for the full conditions.

## Wiki's Role

**The wiki helps you find and contextualize code, not answer from.**

Three things it does well:

- **Find code faster.** Every page cites the files it describes in `sources:` — those paths are the entry point for any real answer.
- **Carry context the code can't.** Why a job runs at 3 AM, which team owns refunds, what the legal driver was for a rule — the wiki holds the *why* the code can't express on its own.
- **Connect surfaces.** Producer→consumer links, rule→endpoint links — the wiki is a map of the system, not its dictionary.

Three things it isn't:

- A cache of the code's current state. It will drift; assume it has.
- A trusted source for facts the user will act on. Re-read the cited code first.
- A replacement for reading the implementation when answering *"what does X do?"*, *"what values can Y take?"*, *"when does Z fire?"*.

No *"quick lookup"* exemption — the same drift that produces consequential bugs produces casual misinformation, and you can rarely tell from the question alone which one the user is about to act on.

## When NOT to Use

- No `kb_path` configured in CLAUDE.md → the skill refuses to act; do not invent a default location.
- The question is about code structure currently visible in the working directory → read the code directly; the wiki is a finding aid, not the source.
- Personal memory across sessions (preferences, project state, deadlines) → use Claude Code's `~/.claude` memory system; the KB is for *system* knowledge.

## Configuration

One key in the project's CLAUDE.md (or a global CLAUDE.md if one KB serves many related repos):

```yaml
kb_path: /Users/you/.kb/work    # required — absolute path. No default.
```

**Repo name resolution** (used for writes; auto-detected, no config key):

1. `git config --get remote.origin.url` → extract `<org>/<repo>.git` → use `<repo>`.
2. Fallback: basename of `git rev-parse --show-toplevel`.
3. If both fail, ask the user once.

**First-use bootstrap.** When `kb_path` exists but is empty (or no folder exists for the current repo under `wiki/`), ask authorization before creating anything:

- *"`<kb_path>` doesn't exist. Create it with the canonical layout (`wiki/index.md`, `plans/index.md`)? Initialize it as a git repo for change history (recommended)?"*
- *"No folder for `<repo-name>` under `wiki/`. Create the canonical layout (`wiki/<repo>/index.md` + the eight default subfolders `entities/`, `interfaces/`, `jobs/`, `dependencies/`, `events/`, `rules/`, `helpers/`, `patterns/`)?"*

All eight default subfolders are created at bootstrap (empty if no content yet) — including `helpers/` and `patterns/` — so downstream skills (`brainstorm`, `analyze-code`, `using-software-specialists`) always find the expected layout. The repo's `index.md` always renders the `## Helpers` and `## Patterns` headings (with an explicit *"(none yet)"* placeholder when empty) so consulting agents can distinguish *"none documented yet"* from *"forgot to look."*

If the user declines `git init`, there's no per-write audit trail — changes are visible only in `last_updated` frontmatter and the agent's post-write summary in the current session.

## Folder Structure

```
<kb_path>/                            the knowledge base (KB)
  plans/                              one bucket — plans (often span repos)
    index.md                          plans TOC
    <ticket-or-branch>.md             proj-1234.md, feature-add-search.md, or YYYY-MM-DD-slug.md
  wiki/                               another bucket — per-repo system docs
    index.md                          wiki TOC: lists every repo
    <repo-name>/                      one per repo
      index.md                        repo TOC: pages grouped by subfolder
      entities/                       tables, models
      interfaces/                     REST/GraphQL/gRPC endpoints
      jobs/                           cron / scheduled tasks
      dependencies/                   external services this repo calls
      events/                         topics this repo produces or consumes
      rules/                          business rules (domain invariants, policies)
      helpers/                        reusable functions, grouped by category
      patterns/                       canonical shapes for recurring problems
```

The six system subfolders (`entities`, `interfaces`, `jobs`, `dependencies`, `events`, `rules`) plus `helpers/` and `patterns/` are the **defaults** — eight in total. Use them. Add another only if content genuinely doesn't fit; justify it in the repo's `index.md`.

The KB root has exactly two children today: `wiki/` and `plans/`. Other top-level buckets (e.g., `decisions/` for ADRs, `glossary/`, `runbooks/`) can be added later without conflicting with repo names.

### `helpers/` and `patterns/` — internal-knowledge subfolders

These two subfolders capture *internal* knowledge that the six system subfolders don't: what reusable functions live in the repo, and what canonical shapes the team uses for recurring problems. They follow the same `sources:` / `last_updated:` discipline as every other page.

**`helpers/` — catalog of reusable functions.**

- **Granularity:** one file per category. A category is a topic cluster (e.g., `helpers/dates.md`), not a module path. Every cross-cutting date helper lives in `dates.md` regardless of which source file holds it.
- **Escape hatch:** a single large or non-trivial helper can have its own page (`helpers/<name>.md`). The category page links to it.
- **Inclusion bar:** a function appears in `helpers/` if and only if (a) it is reusable across the repo — not specific to a single feature's internal use — and (b) it is not private (Python: not prefixed with `_`; analogous for other languages). Domain-specific helpers (e.g., `build_dcf_inputs` in a finance app) stay with their feature.
- **`sources:`** lists the file(s) where the listed helpers are defined; usually one file per category.
- **Page shape:** see [references/page-template.md](references/page-template.md).

**`patterns/` — canonical shapes for recurring problems.**

- **Granularity:** one file per pattern.
- **Kinds:** every pattern page declares `kind:` in frontmatter, one of:
  - `convention` — a standing decision about how to do something (e.g., "we use offset pagination, never cursor"). Carries the *rule* and the *why*.
  - `recipe` — a step-by-step how-to for a recurring task (e.g., "how to add a new CLI command"). References the files touched.
  - `template` — a canonical code snippet (e.g., "unit-test shape with fixtures"). Snippet ~30 lines max — beyond that, point to the exemplar.
- **`sources:`** cites canonical exemplar file(s) — the place(s) the team treats as "the way."
- **Page shape:** see [references/page-template.md](references/page-template.md).
- **Creation channel:** pattern pages are created *only* via the **Ingest** or **Update** workflow. They are **not** created autonomously by a specialist mid-implementation. Modifying an existing pattern page (e.g., the exemplar's signature changed) is a normal autonomous Update.

## Operating Modes

Mode is determined by the user's verb. Four modes:

| Mode | Trigger phrases | Discipline |
|------|----------------|------------|
| **Query** | *"what's the orders schema"*, *"what events does X publish"*, *"is there a plan for PROJ-1234"*, *"what business rules apply to refunds"* | Read-only. |
| **Ingest** | *"read this doc and store what's relevant"*, *"ingest the schema from `<path/url>`"*, *"add what we just discussed to the wiki"* | Write directly; ask only when the source is ambiguous; summarize after. |
| **Update** | *"update the wiki with what we just changed"*, *"we added the order.cancelled event, update the KB"* | Write directly; summarize after. Deletes follow the [Delete protocol](#delete-protocol). |
| **Lint** | *"lint the wiki"*, *"audit the KB"*, *"check for stale wiki pages"* | Flag-only, **except** auto-deletes non-plan pages whose in-tree `sources:` are all dead. |

### Query workflow

1. Read the appropriate index for the question: `wiki/index.md` (for system/architecture questions) or `plans/index.md` (for project/feature questions). The KB has no overarching root index — these two are parallel entry points.
2. Read the relevant pages to find which code files describe the answer (their `sources:` frontmatter).
3. **Open the cited code and read it.** The wiki page is the index entry; the code is the answer. If `sources:` lists multiple files, read the ones relevant to the question. No *"the wiki is recent enough"* shortcut — `last_updated` records when the wiki was edited, not when the code was.
4. Synthesize the answer **from the code**, using the wiki for surrounding context (rationale, ownership, related surfaces, history).
5. **Cite both** in your reply: the code file(s) you read this turn (`src/orders.py`) and the wiki page that pointed you there (`wiki/order-service/entities/orders.md`). This is response-side citation — distinct from how wiki pages themselves record provenance (see Citation rules below).
6. If the code disagrees with the wiki — even in a minor detail — **surface the disagreement explicitly**, give the code's answer as the truth, and flag the page as a candidate for `/knowledge-base update`. Never silently prefer one over the other.
7. If neither the wiki nor the code has the answer, say so explicitly. Offer to add it once the user clarifies.

### Ingest workflow

1. **Enumerate the full source set, then read every file in it.** The "source" is whatever the user named — a file, a URL, pasted text, a directory, a codebase, a doc tree. If it resolves to *more than one file*, list **every** file in scope first (e.g., `git ls-files`, `find <dir> -type f`, archive listing), then read each one. **No sampling, no representative-files shortcut, no "the README covers it."** Skipping files = missing surfaces. The only files you may exclude are ones the user explicitly named as out of scope, or boilerplate that contains no system surface (lockfiles, generated code, vendored deps, binary assets) — and even then, *announce* the exclusion in the summary so the user can correct you.
2. Identify which repo and which subfolder(s) the content belongs to (under `wiki/<repo>/`), or whether it's a plan (`plans/`). One source file may touch multiple pages; one page may aggregate facts from many source files. **Ask the user only when the source is genuinely ambiguous** — contradictory, partial, or unclear which repo it belongs to. Don't ask "which subfolder?" for clean sources; pick the best fit and surface the choice in the summary.
3. For each page: create or update; add `[[wiki-links]]` to related pages; set `sources:` (listing **every** source file that contributed, not just the first) and `last_updated:` in frontmatter.
4. Update the repo's `wiki/<repo>/index.md` and the wiki's `wiki/index.md` if a new repo or new top-level page was added.
5. Summarize what was written — one line per page, scannable, and lead with the **coverage line** so the user can spot under-ingestion at a glance:
   ```
   Ingested 17/17 files from docs/architecture/ (0 excluded).
   Wrote:
     + wiki/order-service/dependencies/sendgrid.md   email provider, REST API, owner: comms team
     + wiki/order-service/events/order-created.md    schema, producers, consumers
     ~ wiki/order-service/index.md                   linked new pages
   ```
   If you excluded files, list them and the reason: `Excluded: docs/architecture/legacy-2018.md (user said "current docs only")`.

**Coverage rule (load-bearing).** Before writing the summary, cross-check: does the number of source files you read match the number of files in scope? If not, you ingested partially — go back to step 1 and read the rest. Reporting "Wrote N pages" without "Ingested M/M files" is incomplete and forbidden; the user can't tell whether you covered the source or skipped half of it.

### Update workflow

1. Identify pages affected by the change the user is describing.
2. Write the changes directly. Add `[[wiki-links]]` to related pages; set `last_updated:` in frontmatter.
3. Update the repo's `wiki/<repo>/index.md` and the `wiki/index.md` as needed.
4. Summarize what was written — one line per page, scannable:
   ```
   Wrote:
     ~ wiki/order-service/entities/orders.md                 added 'cancelled' to status enum
     + wiki/order-service/interfaces/post-orders-cancel.md   new page
     + wiki/order-service/events/order-cancelled.md          new page (producer)
     ~ wiki/order-service/index.md                           linked new pages
   ```
5. If the change requires **deleting** a page, follow the [Delete protocol](#delete-protocol) instead — most deletes need explicit approval.

### Lint workflow

Run the lint script from inside the current repo's working tree:

```bash
uv run scripts/lint.py <kb_path> --json
```

The script walks the KB (both `wiki/` and `plans/`), parses frontmatter, runs all seven checks, and emits a structured report. **Do not load pages into context to run lint manually** — the script's whole purpose is to keep the per-page bodies out of your context. Read the report (small) and act on the findings. The seven checks:

1. **Broken `sources:` paths** — frontmatter source points to a file that no longer exists. Script flags renames (with the new path) and dead files separately; it does **not** auto-fix paths.
2. **Aging pages** — `last_updated` older than 90 days. Flag as *"needs review"*, not *"definitely stale"*.
3. **Orphan pages** — no inbound `[[wiki-link]]` from any other page.
4. **Concept-gap candidates** — regex heuristic; expect false positives. The script emits candidates; you triage by reading the flagged pages.
5. **`[needs source]` markers** — claims still missing citations.
6. **All-dead in-tree sources** — every `sources:` path is in the current working tree AND every one is truly dead (no surviving file, no rename detected). Non-plan pages in this state are **auto-delete candidates** per the [Delete protocol](#delete-protocol); plans are flagged, never deleted. Pages where sources were *renamed* are NOT auto-delete candidates — they show up under check 1 so you can update the source path.
7. **Pattern `kind:` validity** — pages under `patterns/` must declare `kind:` in frontmatter, set to one of `convention | recipe | template`. Flag pages missing the field or using an unknown value.

After running: surface findings 1, 2, 3, 5, 7 to the user; triage check 4 by reading flagged pages; for check 6 candidates, verify each with `scripts/check-sources.py` before deleting (the Delete protocol details what each verdict means).

### Delete protocol

Before deciding to delete a page, run the source-check script:

```bash
uv run scripts/check-sources.py <page-path>
```

The script returns a verdict. Act according to this table:

| Verdict | Action |
|---|---|
| `safe-to-delete` | All in-tree sources are truly dead (no renames), no externals, not a plan. Delete autonomously. |
| `partial` | Some sources alive, some dead/renamed. Drop the dead/renamed entries from `sources:`; flag for review. Don't delete. |
| `flag` (reason: renames present) | All paths gone but rename targets found. **Update** the source paths instead of deleting. |
| `flag` (reason: external sources) | URL or `[[wiki-link]]` sources present — can't fully verify. Flag for user. |
| `flag` (reason: cross-repo) | Page belongs to a different repo than CWD; the script can't verify. Flag for user. |
| `flag` (reason: plan) | Page is under `plans/` — never auto-deleted. Flag for user. |
| `all-alive` | Nothing to do. |
| `no-sources` | Page has no `sources:` field. Don't delete based on source-liveness; flag for user. |

The auto-delete conditions in plain English: **all** of these must hold for `safe-to-delete`:

- Every `sources:` path resolves into the current working tree (no cross-repo sources — the agent can't verify code in repos it isn't in).
- Every in-tree `sources:` path is truly dead — file doesn't exist at the path AND no rename detected. Renamed sources mean "update the path," not "delete the page."
- No external (URL or `[[wiki-link]]`) sources mixed in.
- The page is **not** under `plans/`.

All other deletions — page obsolete for reasons unrelated to `sources:` liveness, merging two pages, restructuring — require explicit user approval. Before deleting, show what's about to be deleted and which inbound `[[wiki-links]]` will break.

After any delete (autonomous or approved): remove the entry from the repo's `index.md` and the master `index.md`. Include the delete in the post-action summary:

```
Deleted:
  - wiki/order-service/jobs/legacy-cleanup.md   all sources gone (file removed in commit a1b2c3d)
```

## Page Format

YAML frontmatter + Markdown body. Required frontmatter fields: `summary`, `sources` (list, ≥1 entry), `last_updated` (YYYY-MM-DD). Full template and per-subfolder body shape: [references/page-template.md](references/page-template.md).

### `[[wiki-link]]` syntax

Path from the **KB root**, no extension.

- ✅ `[[wiki/order-service/entities/orders]]` — page inside a repo.
- ✅ `[[wiki/order-service]]` — shorthand for the repo's `wiki/<repo>/index.md`.
- ✅ `[[plans/proj-1234]]` — a plan.
- ✅ `[[wiki]]` — shorthand for `wiki/index.md`.
- ❌ `[[order-service/entities/orders]]` — missing the `wiki/` prefix (pre-migration form; agents reading older content will see this — flag for update).

Wiki-links must resolve to existing files. Lint mode flags broken links.

**Exception for `wiki/index.md`'s repo list.** The `## Repos` section in `wiki/index.md` uses **standard markdown links with an explicit `index.md` target** — `[order-service](order-service/index.md)`, not `[[wiki/order-service]]`. Reason: `wiki/index.md` is the wiki's entry point, browsed by humans in plain markdown viewers where `[[wiki-link]]` text is not clickable. Everywhere else (body cross-references, related-pages lists, producer/consumer links), keep the `[[wiki-link]]` form. See [references/index-templates.md](references/index-templates.md) for the template.

### Citation rules

Wiki pages cite their provenance in the `sources:` frontmatter list — never inline in the body. Source values are free-form strings (live code file, external URL, session note, or another wiki page); see [references/page-template.md](references/page-template.md) for formats. If a claim can't be sourced, mark it `[needs source]` inline in the body. Lint mode counts these.

### Special pages

Three files use templates distinct from regular content pages:

| File | Purpose |
|------|---------|
| `wiki/index.md` | Wiki TOC: lists every repo under `wiki/`. |
| `wiki/<repo>/index.md` | Per-repo TOC: lists every page in the repo, grouped by subfolder. |
| `plans/index.md` | Status table for every plan, regardless of repo. |

There is no KB-root `index.md` — the two sub-indexes (`wiki/index.md` and `plans/index.md`) are parallel entry points. Templates: [references/index-templates.md](references/index-templates.md).

## Integration with Other Skills

The skill is read by `brainstorm` and `analyze-code`. Both integrations are **gated on `kb_path` being configured** — when no KB exists, the existing skills behave exactly as before.

| Skill | When it fires | What it does |
|-------|---------------|--------------|
| `brainstorm` | Step 1 (Explore context) | Reads the current repo's `wiki/<repo>/index.md` — which now lists `Helpers` and `Patterns` alongside the existing sections — plus relevant `wiki/<repo>/rules/` pages before the first Socratic question. Drills into specific helper/pattern pages on demand as the design conversation reveals what's relevant. |
| `brainstorm` | Step 9 (Save plan) | Default plan path becomes `<kb_path>/plans/<ticket-or-branch>.md`. Frontmatter records `repos: [...]` so cross-repo plans are findable from any participating repo. |
| `analyze-code` | Step 1 (Frame) | Reads this repo's `wiki/<repo>/dependencies/`, `events/`, `rules/`, and the plan at `<kb_path>/plans/<current-branch>.md` if one exists. Reads the `Helpers` and `Patterns` sections of `wiki/<repo>/index.md`; drills into specific pages on demand when the code under review suggests overlap. May follow cross-repo `[[wiki-links]]` if relevant. Wiki↔code disagreements become findings — including **"reinvents existing helper"** and **"violates documented pattern"**. |
| `using-software-specialists` | Implementation phase | **Phase A (consult, mandatory before producing code):** specialist reads `wiki/<repo>/index.md` including the `Helpers` and `Patterns` sections, then drills into relevant pages. Uses existing helpers and follows canonical patterns instead of inventing divergent shapes. **Phase B (post-write, before declaring completion):** if any new function meets the helpers inclusion bar (reusable, non-private), the specialist updates `helpers/<category>.md` autonomously (existing Update workflow). Pattern *creation* is **not** in scope for the specialist — patterns are added only via Ingest. |

### Cross-references between pages (load-bearing for the integrations)

Three link types the skill maintains:

- **Entity ↔ plan.** A plan's frontmatter lists touched entities; each entity page's *"Related plans"* section links back to plans that modified it.
- **Event producer ↔ consumer.** Each event page lists `producer:` and `consumers:` as `[[wiki-links]]`. Both sides have the link, so following either direction works.
- **Rule ↔ entity/endpoint.** A business rule like *"orders cancellable within 30 min"* links to the entity and endpoint where it's enforced. `analyze-code` can trace rule → enforcement points and flag missing enforcement as a finding.

## Wiki ↔ code disagreements

Three failure modes you'll encounter while honoring Core Principle #1. The middle row is the most valuable — a disagreement is often a *bug*, not just stale docs.

| Failure mode | Example | Skill response |
|---|---|---|
| **Wiki silent on a real thing** | Code has a `refunds` table; wiki has no `wiki/<repo>/entities/refunds.md`. | Lint flags it; `analyze-code` may suggest `/knowledge-base update`. |
| **Wiki claims something code doesn't reflect** | Wiki says `orders.status` includes `cancelled`; code has only `pending\|paid`. | **Surfaced as a finding** — often signals a bug (intent vs. implementation drift), not just stale docs. Answer the user from the code; flag the page for update. The user decides which side to fix. |
| **Wiki agrees but is incomplete** | Wiki has `orders.total` is decimal; code confirms — but the implicit `>= 0` rule isn't documented. | Background context, no action required. User may invoke `/knowledge-base update` with the missing detail. |
| **Reinvents an existing helper** | Code defines `parse_timestamp(s)` doing the same job as `parse_iso` in [[wiki/<repo>/helpers/dates]]. | **Finding.** Suggest replacing the new function with the existing helper. Severity at least Medium — parallel implementations of an existing utility drift. |
| **Violates a documented pattern** | Code adds a list endpoint with cursor pagination; `patterns/pagination.md` is a `convention` for offset-based. | **Finding.** Surface the convention and the divergence; leave the decision to the user. Severity depends on the kind: violating a `convention` is usually Medium; diverging from a `template` is usually Low; missing steps in a `recipe` is Medium if it skips a safety step. |

## What the Skill Does Not Do

- **No autonomous deletes** except the one case in the [Delete protocol](#delete-protocol): non-plan pages whose `sources:` are all dead in-tree. All other deletes — restructures, merges, "this is obsolete" — require explicit approval.
- **No drift detection.** The skill does not scan the codebase to find wiki-vs-code diffs proactively. Disagreements surface only when a reader (`analyze-code`, or any query workflow) opens both during normal work — which the query workflow now requires for every reply.
- **No auto-fix of broken source paths.** Lint flags broken `sources:` (including renames); the user fixes. Auto-fix of paths is distinct from auto-delete of all-dead-source pages and is not supported.
- **No body-inline timestamps.** `last_updated` lives in frontmatter only. Inline *"as of YYYY-MM-DD"* notes rot independently and are forbidden.
- **No content for `~/.claude` memory's job.** User preferences, session state, deadlines, in-flight project state — those live in Claude Code's auto-memory, not the wiki.

## Rules

- **Bootstrap requires approval** (creating `<kb_path>` or a new repo folder under `wiki/`). Ingest and Update write directly.
- **Deletes require approval** except the one autonomous case in the [Delete protocol](#delete-protocol). Plan pages are never auto-deleted.
- Always update the affected `index.md` files after any change (create, update, or delete).
- Always summarize writes and deletes after acting — one line per page, scannable.
- File names: lowercase with hyphens (`user-account.md`, not `UserAccount.md`).
- Every factual claim cites a source in the page's `sources:` list. Unsourced claims get `[needs source]` inline.
- If two sources disagree, note the contradiction explicitly in the body.
- When uncertain how to categorize a piece of information, write to the best-fit subfolder and surface the choice in the post-write summary. Ask the user only when the source is genuinely ambiguous (e.g., spans repos in an unclear way).

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Inventing a `kb_path` default | The skill refuses if unconfigured — say so, ask the user to set it in CLAUDE.md |
| Leaving a frontmatter string value unquoted when it contains anything beyond letters, digits, spaces, hyphens, underscores, or dots | **Wrap it in double quotes.** That's the universal fix — `summary: "Path: foo"`, `summary: "parse_iso (in helpers/dates.md)"`, `summary: "yes — the cancellable window"`. Unquoted, YAML treats reserved indicators (`:` followed by space, `::`, leading `#`, `&`, `*`, `!`, `|`, `>`, `{` `}` `[` `]`, `,`, `?`, `%`, `@`, `` ` ``) as syntax — frontmatter breaks. Worse, unquoted bareword values that look like booleans or numbers get **silently coerced** (`summary: no` → boolean `false`; `summary: 1.0` → float `1.0`), which lint won't catch because the YAML is "valid," just wrong. **Default: quote any non-trivial string.** Filenames are different — they're not YAML, but they ride the same risk surface in shells and tools; stick to lowercase letters, digits, and hyphens, never `:` / `::` / other punctuation. Also avoid programming-language shorthands like `path::symbol` (Rust/C++) — say it in English: *"`parse_iso` in `helpers/dates.md`"*. |
| Ingesting from a multi-file source by reading only a sample (the README, a few "representative" files, the top of the tree) | Multi-file sources must be enumerated and read **in full**. List every file first, then read each. Skipping = missing surfaces. The Ingest summary's coverage line (`Ingested M/M files`) is mandatory; partial coverage must be reported as such, not hidden. |
| Listing only the first file under `sources:` when a page aggregates facts from several files | `sources:` must list **every** file that contributed to the page. One-source-per-page is a rule of thumb for *content* pages, not a cap — pages that legitimately span files (helpers categories, rules with multiple enforcement points) need every contributing file cited. |
| Answering a *"quick lookup"* from the wiki without opening the cited code | There is no quick-lookup exemption. The wiki is a finding aid; the answer comes from code. Read the `sources:` files before replying. |
| Treating a wiki page as authoritative because `last_updated` is recent | `last_updated` records when the wiki was edited, not when the code was. The code can have moved the same day. Open the cited files. |
| Citing only the wiki in your reply (*"source: orders.md"*) when you didn't read the code | Cite the code file you read this turn alongside the wiki page that pointed you there. If you didn't read the code, don't reply yet — go read it. |
| Putting `(source: ...)` citations inside wiki page bodies instead of in the `sources:` frontmatter list | Body is content; provenance belongs in frontmatter so lint can audit it. The `(source: ...)` form is only for agent-to-user replies, not for the wiki content itself. |
| Following every cross-repo `[[wiki-link]]` during `analyze-code` | The cross-repo lookup is soft — follow only when judged relevant to the audit |
| Treating a wiki ↔ code disagreement as just "stale docs" | It's a finding. Surface it. Often it's a bug. |
| Auto-fixing a renamed `sources:` path during lint | Lint flags path issues; the user fixes. Auto-*delete* of all-dead-source pages is allowed; auto-*fix* of paths is not. |
| Asking for diff approval before every write | Write directly; summarize after. The wiki self-corrects when readers follow its pointers; approval theater rubber-stamps at scale and is worse than no approval. |
| Auto-deleting a page when only *some* `sources:` entries are dead | Delete only when **all** in-tree sources are dead. Otherwise drop the dead entry and flag the page for review. |
| Auto-deleting a plan page | Plans are never auto-deleted, even when their sources are dead. Flag only; the user decides. |
| Trying to delete a page with cross-repo sources | The agent can't verify code in repos it isn't in. Flag, never auto-delete. |
| Putting personal memory in the wiki | User preferences, session state, deadlines → `~/.claude` memory; not the wiki |
| Listing a private or feature-internal function in `helpers/` | The bar is *reusable across the repo, non-private*. Feature-internal helpers stay with their feature. Private functions (Python `_`-prefixed, etc.) never appear. |
| Creating a `patterns/<name>.md` page autonomously during implementation | Pattern *pages* are Ingest-only. The user decides what's canonical. Updating an *existing* pattern page when its exemplar drifts is fine — that's a normal Update. |
| Writing a `patterns/` page without `kind:` in frontmatter, or using a value outside `convention` \| `recipe` \| `template` | `kind:` is required (lint check 7). Choose the right one or don't write the page. |
