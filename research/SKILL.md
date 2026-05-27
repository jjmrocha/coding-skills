---
name: research
description: Use when you have a question and need a sourced answer instead of a back-and-forth — about THIS codebase ("do we have an endpoint/example for X?", "what's the payload of event X?", "what happens when X?", "how do I run X?") or about the wider world ("what's the best-practice approach for X?", comparing libraries, fact-checking a claim). You have questions, not answers.
---

# Research

**Core principle:** You bring a sourced answer *to* the user. You don't interrogate them for answers they don't have, and you don't answer from memory — you go find the truth in the most authoritative source and cite it.

This is the inverse of **brainstorm**. Route by who holds the answers:

| You have... | Use |
|---|---|
| A question, and need to *find* the answer ("do we have X?", "what happens when X?", "what's best practice?") | **research** (this skill) |
| A goal, and opinions to give about what to build ("I want to build X") | **brainstorm** |

## Where the answer lives

Pick the source by where the truth actually is. Most questions are *internal* — about your own system:

| Question is about... | Primary source | How to read it |
|---|---|---|
| This codebase — endpoints, handlers, event payloads, examples, "what happens when X?" | The code (authoritative) | **serena** (`find_symbol`, `get_symbols_overview`, `find_referencing_symbols`), then grep/Read |
| How we operate — running imports, scripts, jobs | Repo scripts / Makefile / README, then the KB | grep + `knowledge-base` |
| Decisions or patterns we've documented | The KB | `knowledge-base` (when `kb_path` set) |
| The wider world — best practice, library choice, "is X true?" | Official docs > blogs | **context7** first, then web search |

For internal questions the code is authoritative over docs when they disagree — read the source, then report any drift.

## Match effort to the question

- **Direct lookup** ("do we have an endpoint for X?", "what's the payload of event X?") → find it, answer, cite the `file:line`. No ceremony.
- **Tracing or evaluation** ("what happens when X?", "which library?") → apply the **deep-research-agent** discipline (in `using-software-specialists`): explicit confidence per finding, report conflicts instead of silently picking a winner, decide the stopping criterion upfront.

## When a scoping question IS allowed

Default to investigating. Ask the user at most **one** round of scoping questions, and only when the answer materially changes *where you look* **and** the user plausibly knows it. Never ask them what they'd need the research to tell them.

## Output and handoff

Deliver the answer with its source cited (a `file:line`, a doc, a KB entry) and — for non-trivial findings — a confidence level and named gaps. Then hand off: to **brainstorm** to decide what *we* want, or to **using-software-specialists** to plan and implement.

## Red Flags

| Thought | Reality |
|---------|---------|
| "Let me ask what they're trying to build" | They came with a question, not a goal. Answer it first. |
| "I'm pretty sure we have an endpoint for that" | Don't answer the codebase from memory. Read it with serena and cite the `file:line`. |
| "This blog post agrees with me" | Check the primary source. Secondary ≠ authoritative. |
| "Sources agree, so it's settled" | Agreement ≠ correctness. State confidence anyway. |
| "Let me research more to be thorough" | Know your stopping criterion. Good-enough beats never-finished. |
| "I'll pick the best option for them" | Report the tradeoffs with evidence; deciding is brainstorm's job. |
