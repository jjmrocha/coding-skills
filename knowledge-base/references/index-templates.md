# Index Templates

Templates for the three special files that aren't content pages: `wiki/index.md`, each repo's `wiki/<repo>/index.md`, and `plans/index.md`. Use [page-template.md](page-template.md) for everything else.

There is no KB-root `index.md` — `wiki/index.md` and `plans/index.md` are parallel entry points.

---

## `wiki/index.md`

Lists every repo under `wiki/`. Updated when a new repo folder is created. Active plans are NOT listed here — they live in `plans/index.md`.

```markdown
# Wiki

## Repos
- [[wiki/order-service]] — Order placement, cancellation, fulfillment lifecycle.
- [[wiki/user-service]] — User accounts, authentication, profiles.
- [[wiki/email-service]] — Outbound email via SendGrid.
```

---

## Per-repo `wiki/<repo>/index.md`

Lists every page in the repo, grouped by subfolder. Updated whenever a page is created, renamed, or removed in this repo.

```markdown
# <repo-name>

<One-paragraph description of what this repo is responsible for.>

## Entities
- [[wiki/<repo>/entities/<name>]] — <one-line summary from the page's frontmatter>

## Interfaces
- [[wiki/<repo>/interfaces/<name>]] — <method + path>

## Jobs
- [[wiki/<repo>/jobs/<name>]] — <schedule + purpose>

## Dependencies
- [[wiki/<repo>/dependencies/<name>]] — <external service name + purpose>

## Events
- [[wiki/<repo>/events/<name>]] — producer | consumer | producer+consumer

## Business rules
- [[wiki/<repo>/rules/<name>]] — <one-line summary>

## Helpers
- [[wiki/<repo>/helpers/<category>]] — <one-line summary of what's in this category>

## Patterns
- [[wiki/<repo>/patterns/<name>]] *(convention | recipe | template)* — <one-line summary>
```

Omit empty sections — if the repo has no jobs, drop the `## Jobs` heading entirely. Same applies to `## Helpers` and `## Patterns`.

In the `## Patterns` list, render the `*(kind)*` marker using the page's `kind:` frontmatter value, so the agent can scan by intent without opening each page.

---

## `plans/index.md`

Status table for every plan, regardless of repo. Sort by status (Active first), then by date descending.

```markdown
# Plans

| Plan | Date | Status | Repos | Goal |
|------|------|--------|-------|------|
| [[plans/proj-1234]] | 2026-05-22 | Active | order-service, email-service | Order cancellation flow. |
| [[plans/feature-search]] | 2026-05-10 | Active | search-service | Full-text product search. |
| [[plans/feature-jwt-auth]] | 2026-04-12 | Done | user-service | Migrate to JWT auth. |
| [[plans/feature-newsletter]] | 2026-02-03 | Abandoned | email-service | Newsletter system (deferred Q3). |
```

**Status values:** `Draft` | `Active` | `Done` | `Abandoned`.
