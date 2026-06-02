# knowledge-base

A Claude Code skill for a user-curated, agent-maintained project knowledge
base (KB). The KB holds two kinds of content: a **wiki** of per-repo system
surfaces (entities, interfaces, jobs, dependencies, events, business rules)
plus internal-knowledge subfolders (`helpers/`, `patterns/`), and **plans**
for implementation work (often spanning repos). Queryable on
its own; consulted by `brainstorm`, `using-software-specialists`, and
`analyze-code` when a `kb_path` is configured.

**The wiki is a finding aid, not a source of truth.** Pages exist to point
an agent at the code that implements a surface and to carry the *why*
(rationale, ownership, history) the code can't express. Every wiki claim
used in an answer is cross-checked against the cited code before being
reported — there is no "quick lookup" exemption.

## When to Use

* Asking about the system: entities, REST endpoints, Kafka events, cron
  jobs, external services, business rules
* Looking up an implementation plan by ticket or feature branch
* Recording what was learned during a session (system docs, ADR-style
  decisions, business rules)
* Updating the wiki after a code change introduced or modified a tracked
  surface
* Auditing the KB for staleness, orphans, or unsourced claims

**When NOT to use:**

* No `kb_path` configured in CLAUDE.md → skill refuses; do not invent a
  default location
* The question is about code visible in the working directory → read the
  code directly
* User preferences, session state, deadlines → use Claude Code's
  `~/.claude` memory, not the KB

## Configuration

One key in the project's CLAUDE.md (or in a global CLAUDE.md if one KB
serves many related repos):

```yaml
kb_path: /Users/you/.kb/work    # required — absolute path. No default.
```

Multiple related repos (e.g., a microservices workspace) can share one KB
by pointing to the same path.

## How It Works

Four operating modes, each chosen by the user's verb:

| Mode | Trigger phrase example | Discipline |
|------|------------------------|------------|
| **Query** | *"what events does the Order Service publish?"* | Read-only |
| **Ingest** | *"read this doc and store what's relevant"* | Write directly; ask only when source is ambiguous; summarize after |
| **Update** | *"we added the order.cancelled event, update the KB"* | Write directly; summarize after. Deletes need approval |
| **Lint** | *"audit the KB for stale pages"* | Flag-only, except auto-deletes non-plan pages with all-dead in-tree sources |

**Code is the source of truth. The wiki is a finding aid.** The wiki points
at the code and carries surrounding context; the code answers the question.
The query workflow always reads the cited code before replying, and
discrepancies are surfaced explicitly. Writes happen directly (wrong writes
self-correct when readers follow the pointer), but deletes require approval
— except the one autonomous case where a non-plan page's `sources:` are all
dead in-tree.

## Storage Layout

```
<kb_path>/                            the knowledge base (KB)
  plans/                              one bucket — plans (often span repos)
    index.md                          plans TOC
    <ticket-or-branch>.md             e.g., proj-1234.md, feature-add-search.md
  wiki/                               another bucket — per-repo system docs
    index.md                          wiki TOC: lists every repo
    <repo-name>/                      one per repo, name auto-detected from git
      index.md                        repo TOC
      entities/ interfaces/ jobs/ dependencies/ events/ rules/
      helpers/ patterns/              internal-knowledge subfolders
```

There is no KB-root `index.md` — `wiki/index.md` and `plans/index.md` are
parallel entry points. The two-bucket layout leaves room for future
top-level categories (`decisions/`, `glossary/`, `runbooks/`) without
colliding with repo names.

## Usage

```
/knowledge-base what's the orders schema?
/knowledge-base ingest the API spec from docs/openapi.yaml
/knowledge-base update the KB with the order.cancelled event we just added
/knowledge-base lint the KB
```

## Credit

Inspired by Andrej Karpathy's
[LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
