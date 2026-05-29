---
name: brainstorm
description: "Use when user presents a vague idea, unclear requirements, or wants to explore possibilities before building. Triggers on 'I want to build X', ambiguous feature requests, concept validation, or any time implementation should not start without first understanding what is being built."
---

# Brainstorm — Socratic Requirements Discovery

Turn ambiguous ideas into concrete, validated designs through guided Socratic dialogue. Shared clarity before any implementation.

**Hard rule:** Do NOT suggest implementation, write code, or scaffold anything until a design has been presented and the user has explicitly approved it. Applies to every project regardless of perceived simplicity.

**If the conversation was compacted, re-invoke this skill before continuing.**

## When NOT to Use

| Don't load when... | Instead... |
|---|---|
| User already approved a written plan/spec | Skip to `using-software-specialists` |
| Bug fix or one-line change with clear scope | Skip to `using-software-specialists` |
| User is asking a question, not requesting a build | Answer directly |
| Revising an existing plan file | Jump to Revision Mode below |

## Steps

1. **Explore context & conventions** — read existing architecture and prior decisions. For any capability that overlaps with what's already in the repo (pagination, auth, validation, error handling, persistence, logging, config), identify the libraries, patterns, and file/module layout in use. The design aligns with what exists unless divergence is explicitly stated and justified. **If `kb_path` is configured, load `knowledge-base` first** — it owns wiki/plan/helper/pattern reads.
2. **Assess scope** — if the idea spans multiple independent systems, decompose first; each sub-project gets its own spec → plan → implementation cycle.
3. **Ask clarifying questions** — one per message, Socratic style (see below).
4. **Propose 2-3 approaches** — with trade-offs; lead with your recommendation and reasoning. For cross-domain work, load specialists from `using-software-specialists` (architect for system shape, security for trust boundaries, requirements-analyst for hidden assumptions) so trade-offs cover more than the happy path.
5. **Present design section-by-section** — confirm each section before moving on; cover architecture, components, data flow, error handling, testing.
6. **Probe non-functional requirements** — explicitly ask about performance targets, scalability, security posture, compliance, accessibility. NFRs skipped here become rework later.
7. **Validate the design** — before the final summary, check: placeholders/TBDs (fix them), internal contradictions (architecture vs feature descriptions), scope creep beyond a single plan, ambiguous requirements (pick one interpretation and make it explicit), and conformance with existing repo conventions (any new pattern for an already-solved problem class needs explicit justification).
8. **Final summary & approval** — present the validated design; revise until the user explicitly approves.
9. **Spec only if asked** — never write the spec file automatically. When asked, use [references/spec-template.md](references/spec-template.md). Default path: `<kb_path>/plans/<ticket-or-branch>.md` if `kb_path` is set (see `knowledge-base` for naming and `repos:` frontmatter); else `docs/specs/YYYY-MM-DD-<topic>.md` or the project's convention. If the user names a directory but not a filename, ask.
10. **Hand off to planning** — pass the approved design to the `project-planner` specialist. Brainstorm ends at an approved design; planning begins after.

## Socratic Questioning

One question per message. Prefer multiple-choice when the options are known. Let each answer shape the next question. Ask "why" when the stated need and the real need might differ.

**Recommend, don't interrogate.** For each question, lead with your recommended answer based on the context you've already gathered. Frame it as *"I'd default to X because Y — does that fit?"* rather than *"What should we do about X?"*. The user reacts; they don't have to generate. Switch to open-ended only when you genuinely have no basis to recommend.

**Check the repo before asking.** If a question can be answered from the codebase, KB, or git history, answer it yourself and state your finding — don't ask the user to recite what's discoverable. Only escalate to a question when the answer isn't in the artifacts you can read.

Progression template:
- Purpose: *"What problem does this solve?"*
- Goal: *"Why does this matter right now?"*
- Constraints: *"What configuration, integrations, or existing systems should I know about?"*
- Success: *"What does a successful outcome look like — what would it allow users to do?"*
- Validate: *"So the core need is X — is that right?"*

## Design Presentation

Scale each section to its complexity (2-3 sentences if simple, up to 300 words if nuanced). Confirm each section before writing the next. Design for isolation: components with one clear purpose; internals can change without breaking consumers.

## Example

```
User: "Tool to track my reading habits."
Q (Step 3): "Finishing more books, or remembering what you read?" → "Remembering."
Step 4 approaches: A) CLI + local markdown (rec.), B) Web + SQLite, C) Notion plugin.
Step 5: confirm architecture section → confirm data section → ... → Step 10 handoff.
```

## Revision Mode

Invoked with an existing plan file? Read it, identify the delta, ask only about deltas, re-validate changed sections (Step 7), update in place after approval. Hard rule still applies.
