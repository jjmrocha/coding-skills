---
name: brainstorm
description: "Use when user presents a vague idea, unclear requirements, or wants to explore possibilities before building. Triggers on 'I want to build X', ambiguous feature requests, concept validation, or any time implementation should not start without first understanding what is being built."
---

# Brainstorm — Socratic Requirements Discovery

Turn ambiguous ideas into concrete, validated designs through guided Socratic dialogue. The goal is shared clarity before any implementation begins.

**Hard rule:** Do NOT suggest implementation, write code, or scaffold anything until a design has been presented and the user has approved it. This applies to every project regardless of perceived simplicity.

**MCP enhancement (optional):** 
- `sequential-thinking` — use it when comparing trade-offs across 2-3 proposed approaches — multi-step reasoning reduces the chance of locking onto the first idea. If unavailable, reason step-by-step inline.
- `serena` — for code navigation. Prefer `get_symbols_overview` / `find_symbol` over full-file `Read`, and `find_referencing_symbols` over repo-wide `Grep`. Load symbol bodies only when a finding needs the detail.

## Steps

1. **Explore context** — check existing project architecture, related files, prior decisions
2. **Assess scope** — if the idea spans multiple independent systems, decompose before going deeper; each sub-project gets its own spec → plan → implementation cycle
3. **Ask clarifying questions** — one per message, Socratic style (see Questioning below)
4. **Propose 2-3 approaches** — with trade-offs; lead with your recommendation and reasoning. For cross-domain work, load the relevant specialists from `using-software-specialists` (architect for system shape, security for trust boundaries, requirements-analyst for hidden assumptions) so trade-offs cover more than the happy path.
5. **Present design** — section by section, confirm after each; cover architecture, components, data flow, error handling, testing
6. **Probe non-functional requirements** — before finalizing the design, explicitly ask about performance targets, scalability, security posture, compliance, and accessibility. NFRs omitted here become rework later.
7. **Write spec** — use `references/spec-template.md` as the starting structure; save to `docs/specs/YYYY-MM-DD-<topic>.md` or per project convention
8. **Self-review spec** — scan for placeholders, contradictions, scope creep, ambiguity; fix inline
9. **User reviews spec** — ask the user to review before handing off
10. **Hand off to planning** — pass the approved spec to the `project-planner` specialist to produce a verifiable execution plan. Brainstorm ends at an approved spec; planning begins after.

## Socratic Questioning

Ask questions that guide discovery rather than reveal the answer.

**Question progression:**
- Purpose: *"What problem does this solve?"*
- Goal: *"Why does this matter right now?"*
- Constraints: *"What configuration, integration points, or existing systems should I know about?"*
- Success: *"What does a successful outcome look like — what would it allow users to do?"*
- Validate: *"So the core need is X — is that right?"*

**Rules:**
- One question per message — multiple questions stall the conversation
- Prefer multiple-choice over open-ended when the options are known
- Follow each answer — let each response shape the next question
- Ask "why" when the stated need and the real need might differ

## Design Presentation

- Scale each section to its complexity: 2-3 sentences if simple, up to 300 words if nuanced
- Confirm each section before moving on — don't write the full spec then ask for feedback
- Design for isolation: break the system into components with one clear purpose each; changes to internals should not break consumers

## Spec Self-Review

Before asking the user to review:

1. **Placeholder scan** — any TBD, TODO, incomplete requirements? Fix them.
2. **Consistency** — does architecture match feature descriptions?
3. **Scope** — focused enough for a single implementation plan?
4. **Ambiguity** — can any requirement be read two ways? Pick one interpretation and make it explicit.

## Example:

```yaml
# Sample session — reading habit tracker idea

User: "I want a tool that tracks my reading habits."

# Step 1 — Context: No existing project found.
# Step 2 — Scope: Single system, proceed.

# Step 3 — Questions (one at a time):
Q: "What problem does this solve — finishing more books,
    or remembering what you've read?"
A: "Remembering what I read and my notes on it."

Q: "Should this integrate with Goodreads, or is a standalone tool fine?"
A: "Standalone is fine."

Q: "Who uses this — just you, or shared with others?"
A: "Just me."

# Step 4 — Propose 2-3 approaches:
#   A) CLI with local markdown files (recommended — simple, portable)
#   B) Local web app with SQLite
#   C) Notion/Obsidian plugin

# Step 5 — Design (architecture, one section at a time):
Q: "Architecture: a CLI that appends entries to a local JSON file,
    with a search command to retrieve by title or tag. Does that fit?"
```

Spec saved to `docs/specs/YYYY-MM-DD-reading-tracker.md` after design approval.

## Key Principles

| Principle | Why it matters |
|-----------|----------------|
| One question at a time | Multiple questions overwhelm and stall dialogue |
| Propose approaches before deciding | Avoids locking into the first idea |
| YAGNI — remove unused features | Scope creep starts during brainstorming |
| Incremental validation | Catch misunderstandings early, not after writing the spec |
| Design for isolation | Smaller, bounded units are easier to build and change |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Jumping to implementation before clarity | Ask "what problem does this solve?" first |
| Asking multiple questions at once | Pick the most important one |
| Accepting the first vague answer | Follow up: "Tell me more about that" |
| Writing a spec without section-by-section approval | Confirm each section before writing the next |
| Skipping scope check on large ideas | Decompose first, brainstorm the first sub-project |
