# research

A front-door skill for **answer-seeking** work: you have a question and need a
sourced, cited answer — not a conversation that asks *you* questions.

It covers two flavours of question, picking the source by where the truth lives:

- **About your own system** (the common case) — "do we have an endpoint for X?",
  "what's the payload of event X?", "what happens when X?", "how do I run X?".
  Answered from the **code** (via serena) and the **KB**, which are
  authoritative for internal questions.
- **About the wider world** — "what's the best-practice approach for X?",
  comparing libraries, fact-checking a claim. Answered from **official docs**
  (context7) and **web search**.

Effort scales to the question: a one-line lookup gets a direct cited answer with
no ceremony; a deep trace or a library evaluation gets explicit confidence
levels, conflict reporting, and a stopping criterion.

## Why it exists

`brainstorm` and `research` both sit at the fuzzy front-end of a task, but they
point in opposite directions:

| | brainstorm | research |
|---|---|---|
| Who asks the questions | Agent asks **you** | **You** ask the agent |
| What it resolves | Ambiguity about **intent** (what do you want?) | Ambiguity about **knowledge** (how is this done? what's true?) |
| You need to supply | Answers / opinions | Just the question |
| Output | A sharpened spec | Sourced findings + confidence + gaps |

Without a dedicated front door, "I don't know how to do X — find me the right
approach" requests get misrouted to `brainstorm`, which then interrogates a user
who explicitly has no answers. This skill is the missing door.

They often **chain**: research first (learn what's possible), then brainstorm
(decide what *we* want, now that the intent questions are answerable).

## Relationship to using-software-specialists

The *how* of good research (source hierarchy, confidence, conflict reporting,
stopping criterion) lives in the `deep-research-agent` specialist inside
[using-software-specialists](../using-software-specialists/). This skill is the
discoverable, top-level entry point that applies that mindset — reach for it on
reflex the way you reach for `brainstorm`.

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Routing vs. brainstorm, the research method, scoping-question rule, handoff |
