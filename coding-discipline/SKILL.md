---
name: coding-discipline
description: Use when writing or modifying code, especially in agentic flows — before composing diffs, generating new modules, or applying suggested fixes
---

# Coding Discipline

**If you can name the failure mode you're about to commit, you usually won't commit it.**

Five failure modes most commonly observed when LLMs write code, with the counter-move for each.

## The Five Failure Modes

| Failure mode | What it looks like | Counter |
|--------------|--------------------|---------|
| **Silent assumption** | Picking one reading of an ambiguous ask and proceeding | Surface it: state the assumption, or ask |
| **Scope creep** | Touching adjacent code because "it's right there" | Stay surgical: every changed line traces to the request |
| **Speculative complexity** | Adding config, abstraction, or error paths nobody asked for | Build the smallest thing that solves the stated problem |
| **Hallucination** | Writing code that references symbols, APIs, or paths that don't exist | Verify before writing: read, run, or look it up |
| **Drift** | Losing the original goal across long sessions or hand-offs | Stop when the verifiable check passes, not before |

## 1. Silent Assumption → Surface It

Before any non-trivial change, name the load-bearing assumption. If two reasonable readings exist, present both.

```
Bad:  <writes code>
Good: "Reading 'cache user lookups' as in-process LRU rather than
       a shared cache — flag if you meant the latter."
```

**Smell test:** If you can't name your assumption in one sentence, you don't know what you're building.

## 2. Scope Creep → Stay Surgical

A diff answers one question: *what did the user ask for?* Every other line is contraband.

- **Allowed:** orphans your own change created (unused imports, dead branches you rewrote).
- **Not allowed:** "while I'm here" reformatting, renaming, dead-code removal, style sweeps. Mention them in your reply; don't commit them.

**Smell test:** If your diff has two unrelated chunks, split it.

## 3. Speculative Complexity → Build Less

Optionality is not free. Every config flag, base class, or wrapper is a maintenance cost paid for a request that hasn't been made yet.

Disallowed reflexes:
- "I'll make this configurable in case…"
- "Let me extract a base class so future implementations…"
- "I'll handle this edge case even though it's structurally impossible."
- "I'll add a wrapper for a hypothetical caller."

**The falsifiable test:** "Does a second caller exist *right now* that needs a different value?" No → don't add the parameter. "Real flexibility" and "speculation" feel different from inside; this question collapses the distinction.

**Smell test:** If the simplest version is half the size, write that one.

## 4. Hallucination → Verify Before Writing

Code that references things that don't exist — an import path, a method signature, a config key.

- **Look it up first.** Prefer [serena MCP](https://github.com/oraios/serena) symbolic tools (`find_symbol`, `get_symbols_overview`, `find_referencing_symbols`) over `Read`/`Grep`; [context7 MCP](https://github.com/upstash/context7) for external library docs; `grep`/`Read` otherwise.
- **Run it before saying it's done.** *"It should work"* ≠ *"I ran it and it works."*
- **Mark uncertainty.** *"I think it's `obj.foo()` but haven't confirmed"* lets the user catch a guess.

**Smell test:** Writing a function call from memory rather than from a file you just read = guessing. Look it up.

## 5. Drift → Anchor on a Verifiable Goal

A vague goal ("make it work") guarantees rework. Restate the request as one of:
- A failing test you'll make pass
- A specific output you'll produce
- A specific behavior you'll observe

For multi-step work: state a 2–4 step plan, each paired with its check. Step done when its check passes — not before.

**Smell test:** If you can't name the check that proves it's done, you're not done.

## Pre-Commit Self-Check

Before sending a diff:

1. **Assumption** — stated, or "n/a"?
2. **Scope** — every changed line traces to the request?
3. **Simplicity** — could a senior cut this in half?
4. **Verification** — confirmed referenced symbols/APIs exist? Ran the code, not just wrote it?
5. **Goal** — can you name the check that proves this is done?

A "no" on any line: stop and revise, don't ship and explain.

## Red Flags

| Inner thought | What it actually means |
|---------------|------------------------|
| "I'll just guess what they meant" | You haven't surfaced the assumption |
| "While I'm here, let me also…" | Scope creep starting now |
| "Let me add a flag for flexibility" | Speculative complexity — no second caller exists |
| "That's real flexibility, not speculation" | Same thing. Does a current caller need that value? If not, remove the parameter. |
| "I'll handle every conceivable error" | Many of those errors are structurally impossible |
| "I'm pretty sure that method exists" | You haven't verified — look it up |
| "It should work" (without running it) | "Should work" ≠ "I ran it and it works" |
| "Tests can come after" | You haven't named the verification |
| "I lost track of what they wanted" | Drift — restate the goal before continuing |

## Tradeoff

This skill biases toward caution and under-doing. For trivial tasks (typo fix, one-line rename), use judgment.
