---
name: brainstorm
description: "Use when user presents a vague idea, unclear requirements, or wants to explore possibilities before building. Triggers on 'I want to build X', ambiguous feature requests, concept validation, or any time implementation should not start without first understanding what is being built."
---

# Brainstorm — Socratic Requirements Discovery

Turn ambiguous ideas into concrete, validated designs through guided Socratic dialogue. Shared clarity before any implementation.

**Hard rule:** Do NOT suggest implementation, write code, or scaffold anything until a design has been presented and the user has explicitly approved it. Applies to every project regardless of perceived simplicity.

## Steps

1. **Explore context & conventions** — read existing architecture and prior decisions. For any capability that overlaps with what's already in the repo (pagination, auth, validation, error handling, persistence, logging, config), identify the libraries, patterns, and file/module layout in use. The design aligns with what exists unless divergence is explicitly stated and justified. **If the change modifies an existing module, run `analyze-code` on the affected files first** — inherited debt, coupling, and security smells in that module are design inputs, not post-implementation surprises. **If `wiki_path` is configured in CLAUDE.md, also load `knowledge-base` and read the current repo's `index.md` plus relevant `rules/` pages** — entities, events, and business rules captured there are real constraints that should shape the design.
2. **Assess scope** — if the idea spans multiple independent systems, decompose first; each sub-project gets its own spec → plan → implementation cycle.
3. **Ask clarifying questions** — one per message, Socratic style (see below).
4. **Propose 2-3 approaches** — with trade-offs; lead with your recommendation and reasoning. For cross-domain work, load specialists from `using-software-specialists` (architect for system shape, security for trust boundaries, requirements-analyst for hidden assumptions) so trade-offs cover more than the happy path.
5. **Present design section-by-section** — confirm each section before moving on; cover architecture, components, data flow, error handling, testing.
6. **Probe non-functional requirements** — explicitly ask about performance targets, scalability, security posture, compliance, accessibility. NFRs skipped here become rework later.
7. **Validate the design** — before the final summary, check: placeholders/TBDs (fix them), internal contradictions (architecture vs feature descriptions), scope creep beyond a single plan, ambiguous requirements (pick one interpretation and make it explicit), and conformance with existing repo conventions (any new pattern for an already-solved problem class needs explicit justification).
8. **Final summary & approval** — present the validated design; revise until the user explicitly approves.
9. **Spec only if asked** — do NOT write a spec file automatically. Save to disk only when the user explicitly requests it; then use [references/spec-template.md](references/spec-template.md). **If `wiki_path` is configured in CLAUDE.md, the default location becomes `<wiki_path>/plans/<ticket-or-branch>.md`** (e.g., `proj-1234.md`, `feature-add-search.md`, or `YYYY-MM-DD-slug.md` if neither ticket nor branch applies) — the plan's frontmatter records `repos: [...]` so cross-repo plans are findable from any participating repo. Otherwise default to `docs/specs/YYYY-MM-DD-<topic>.md` or per project convention; **for cross-repo work without a wiki, save to a path outside the repo provided by the user** (e.g., `~/plans/YYYY-MM-DD-<topic>.md`). If the user names a directory but not a filename, ask.
10. **Hand off to planning** — pass the approved design to the `project-planner` specialist. Brainstorm ends at an approved design; planning begins after.

## Socratic Questioning

One question per message. Prefer multiple-choice when the options are known. Let each answer shape the next question. Ask "why" when the stated need and the real need might differ.

Progression template:
- Purpose: *"What problem does this solve?"*
- Goal: *"Why does this matter right now?"*
- Constraints: *"What configuration, integrations, or existing systems should I know about?"*
- Success: *"What does a successful outcome look like — what would it allow users to do?"*
- Validate: *"So the core need is X — is that right?"*

## Design Presentation

Scale each section to its complexity (2-3 sentences if simple, up to 300 words if nuanced). Confirm each section before writing the next. Design for isolation: components with one clear purpose; internals can change without breaking consumers.

## Example

```yaml
User: "I want a tool that tracks my reading habits."

# Step 1 — no existing project found. Step 2 — single system.
# Step 3 — Socratic Q&A:
Q: "What problem does this solve — finishing more books, or remembering what you've read?"
A: "Remembering what I read and my notes on it."
Q: "Goodreads integration, or standalone?"
A: "Standalone."

# Step 4 — Approaches:
#   A) CLI + local markdown (recommended — simple, portable)
#   B) Local web app + SQLite
#   C) Notion/Obsidian plugin

# Step 5 — Design (one section at a time):
Q: "Architecture: CLI appends entries to a local JSON file, search by title/tag. Fit?"
# → Approved → handoff to project-planner.
```

## Revision Mode

When invoked with an existing plan file (e.g., *"here's our plan at ~/plans/X.md, the auth section needs to change to OAuth"*), do NOT re-run the full Socratic loop from step 3. Instead:

1. **Read the existing plan** before asking anything.
2. **Identify the delta** — which sections does the requested change affect, and which are untouched?
3. **Ask only about the deltas** — confirm the new intent, surface contradictions with untouched sections, probe NFRs only for the changed surface.
4. **Re-validate the changed sections** (step 7 applies to the deltas), then update the plan file in place once the user approves.

The skill's hard rule (no implementation before approval) still applies. The Socratic loop is a discovery tool, not a ritual — when the design exists, diff it; don't rediscover it.

## MCP Enhancements (optional)

- `sequential-thinking` — for trade-off comparison across proposed approaches; reduces locking onto the first idea.
- `serena` — for context exploration. Prefer `get_symbols_overview`/`find_symbol` over full-file `Read`, and `find_referencing_symbols` over repo-wide `Grep`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Jumping to implementation before clarity | Ask "what problem does this solve?" first; the hard rule at the top is absolute |
| Asking multiple questions at once | One per message — let each answer shape the next |
| Accepting the first vague answer | Follow up: "Tell me more about that" |
| Writing the full spec then asking for feedback | Section-by-section confirmation (step 5) |
| Skipping the scope check on large ideas | Decompose first, brainstorm the first sub-project |
| Designing in a vacuum, ignoring existing patterns | Step 1 isn't optional — align with how the codebase already solves overlapping problems |
| Writing a spec to disk without being asked | Step 9 — only when the user explicitly requests it |
| Skipping NFRs because the user didn't volunteer them | Step 6 — probe explicitly; NFRs skipped here become rework |
