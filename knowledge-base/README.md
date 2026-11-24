# knowledge-base

A Claude Code skill for a project knowledge base (KB) that you curate and the
agent maintains. The KB holds three kinds of content:

- A **wiki** of each repository's system surfaces (entities, interfaces, jobs,
  dependencies, events and business rules), plus internal-knowledge folders
  for `helpers/` and `patterns/`.
- **Plans** for implementation work, which often span several repositories.
- **Manuals** that explain the system in plain language to operators without
  a technical background.

You can query the KB on its own. When `kb_path` is configured, `brainstorm`,
`using-software-specialists` and `analyze-code` also read the wiki and the
plans.

**The wiki is a finding aid, not a source of truth.** A page points the agent
at the code that implements a surface, and it carries the reasons, ownership
and history that the code cannot express. Every wiki claim used in an answer
is checked against the cited code before it is reported, including quick
lookups.

## When to use

- Asking about the system: entities, REST endpoints, Kafka events, cron jobs,
  external services and business rules.
- Looking up an implementation plan by ticket or feature branch.
- Asking for a manual that explains part of the system to operators in plain
  language.
- Recording what was learned during a session, such as system docs, decisions
  in the style of an ADR, or business rules.
- Updating the wiki after a code change added or changed a tracked surface.
- Auditing the KB for stale pages, orphan pages or claims without a source.

## When not to use

- When no `kb_path` is configured. The skill refuses and does not invent a
  default location.
- When the question is about code in the working directory. Read the code
  directly.
- For user preferences, session state or deadlines. Use Claude Code's memory
  in `~/.claude`, not the KB.

## Configuration

The skill reads one key from the agent instructions. A global instruction
file works when one KB serves many related repositories:

```yaml
kb_path: /Users/you/.kb/work    # required, absolute path, no default
```

Several related repositories, such as the services of one workspace, can
share one KB by pointing to the same path.

## How it works

The verb in your request chooses one of four modes:

| Mode | Example request | Discipline |
|------|-----------------|------------|
| **Query** | *"what events does the Order Service publish?"* | Read-only. |
| **Ingest** | *"read this doc and store what's relevant"* | Writes directly, asks only when the source is ambiguous, and summarizes after. |
| **Update** | *"we added the order.cancelled event, update the KB"* | Writes directly and summarizes after. Deletes need approval. |
| **Lint** | *"audit the KB for stale pages"* | Only flags problems, with one exception: it deletes unprotected pages whose in-tree sources are all gone. |

A query always reads the cited code before it replies, and it reports any
difference between the wiki and the code. Writes happen directly, because a
wrong write gets corrected the next time a reader follows its pointer to the
code. Deletes need your approval, with one exception: a page whose `sources:`
are all gone from the tree, and which is neither a plan nor a manual, is
deleted without asking.

Manuals follow the same sourcing rules in plainer language. They are created
only when you ask for one, refreshed automatically when a source file
changes, and never deleted without approval.

## Storage layout

```
<kb_path>/                            the knowledge base (KB)
  plans/                              one bucket: plans (often span repos)
    index.md                          plans TOC
    <ticket-or-branch>.md             e.g., proj-1234.md, feature-add-search.md
  manuals/                            one bucket: operator-facing docs
    index.md                          manuals TOC
    <topic-slug>.md                   e.g., running-a-valuation.md
  wiki/                               another bucket: per-repo system docs
    index.md                          wiki TOC: lists every repo
    <repo-name>/                      one per repo, name auto-detected from git
      index.md                        repo TOC
      entities/ interfaces/ jobs/ dependencies/ events/ rules/
      helpers/ patterns/              internal-knowledge subfolders
```

There is no `index.md` at the root of the KB. `wiki/index.md`,
`plans/index.md` and `manuals/index.md` are three separate entry points.
`manuals/` is flat like `plans/`, because a manual can cover the whole system
instead of one repository. The bucket layout leaves room for new top-level
categories later, such as `decisions/` or `glossary/`, without clashing with
repository names.

## Usage

```
/knowledge-base what's the orders schema?
/knowledge-base ingest the API spec from docs/openapi.yaml
/knowledge-base update the KB with the order.cancelled event we just added
/knowledge-base lint the KB
/knowledge-base write a manual explaining how to run a valuation
```

## Credit

Inspired by Andrej Karpathy's
[LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
