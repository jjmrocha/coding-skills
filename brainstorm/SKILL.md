---
name: brainstorm
description: "Use when user presents a vague idea, unclear requirements, or wants to explore possibilities before building. Triggers on 'I want to build X', ambiguous feature requests, concept validation, or any time implementation should not start without understanding what is being built."
---

# Brainstorm — Socratic Requirements Discovery

Turn ambiguous ideas into concrete, validated designs through Socratic dialogue. Shared clarity before any implementation.

**Hard rule:** Do NOT suggest implementation, write code, or scaffold anything until a design is presented and the user explicitly approves it. Applies regardless of perceived simplicity.

**If the conversation was compacted, re-invoke this skill before continuing.**

## When NOT to Use

| Don't load when... | Instead... |
|---|---|
| User already approved a written plan | Skip to `using-software-specialists` |
| Bug fix or one-line change with clear scope | Skip to `using-software-specialists` |
| User is asking a question, not requesting a build | Answer directly |
| Changing an existing plan file (scope, split, or a sub-task's plan) | Jump to Revision Mode below |
| Feature plan exists with `pending` or `in progress` sub-tasks | Jump to Sub-task Mode — step 4 if one is `in progress`, else step 3 |

## Steps

1. **Explore context & conventions** — read existing architecture and prior decisions. For any capability overlapping what's already in the repo, identify the libraries, patterns, and file/module layout in use. The design aligns with what exists unless divergence is explicitly stated and justified. **If `kb_path` is configured, load `knowledge-base` first** — it owns wiki/plan/helper/pattern reads.
2. **Agree scope** — ask clarifying questions (see Socratic Questioning) until what's in and out of scope is agreed. A question belongs here only if its answer moves something in or out of scope. Design choices (tax treatment, ordering, edge cases, naming, where code lives) are not scope: they wait for the sub-task that needs them.
3. **Split** — always switch to **Sub-task Mode**. Size is never a reason to skip it. Steps 4–8 then run once per sub-task.
4. **Propose 2-3 approaches** — with trade-offs; lead with your recommendation and reasoning. For cross-domain work, load specialists from `using-software-specialists` (architect for system shape, security for trust boundaries, requirements-analyst for hidden assumptions) so trade-offs cover more than the happy path.
5. **Present design section-by-section** — confirm each section before moving on; cover architecture, components, data flow, error handling, testing. Scale each section to its complexity (a couple sentences if simple, longer if nuanced); design for isolation — each component one clear purpose, internals changeable without breaking consumers.
6. **Probe non-functional requirements** — explicitly ask about performance targets, scalability, security posture, compliance, accessibility. NFRs skipped here become rework later.
7. **Validate the design** — before the final summary, check: placeholders/TBDs (fix them), internal contradictions (architecture vs feature descriptions), scope creep beyond a single plan, ambiguous requirements (pick one interpretation and make it explicit), and conformance with existing repo conventions (any new pattern for an already-solved problem class needs explicit justification).
8. **Final summary & approval** — present the validated design — the **spec**, structured with [references/spec-template.md](references/spec-template.md) — and revise until the user explicitly approves. The spec is the approval artifact: it lives in the conversation. Brainstorm does NOT write it to a file — the durable artifact is the plan produced in the next step.
9. **Hand off to planning** — once the design is approved and the user signals to create the plan, load the **Project Planner** specialist from `using-software-specialists`. Convert the approved design (the spec) into an execution **plan** — this plan produced by the Project Planner (not the spec) is what gets saved to the KB under `<kb_path>/plans/` (see `knowledge-base`; if `kb_path` isn't configured, save to `docs/specs/` or the project's convention). Your role stops with the plan — do NOT start coding. This step runs once per sub-task, through Sub-task Mode steps 3–4.

## Sub-task Mode

### How to split

- A sub-task is a step of behavior, not a piece of code. When it is done, the code works, its tests pass, and the user can review it alone. "Add the constants" is not a sub-task. "Compute the surcharge for one order, with tests" is.
- The first sub-task is the smallest part of the feature that works alone. Each later one adds one behavior on top of the previous ones.
- Give every open design question to the first sub-task that needs its answer. Do not ask it earlier.
- Propose at least two sub-tasks. The user may merge them. You may not.

| Thought | Reality |
|---|---|
| "The feature is small" | Size is not a criterion. A small feature splits into smaller steps. |
| "The parts can't work on their own" | You are splitting by pieces of code. Split by behavior. |
| "Splitting only adds overhead" | Small parts are easier to review, and a change of direction costs less. |
| "I'll settle all the questions now" | Questions for later sub-tasks wait for those sub-tasks. Their answers may change after the earlier parts are built. |

### Steps

1. **Propose the split** — ordered list of sub-tasks (see How to split), one line each: what it delivers, what it depends on. Revise until approved.
2. **Save the feature plan** — load **Project Planner** from `using-software-specialists`; write one plan file to the same location as Step 9 with the agreed scope and the sub-task list, each `pending`. No sub-task detail yet.
3. **Next sub-task** — take the first `pending` sub-task and run Steps 4–8 scoped to it alone. On approval, Project Planner adds its detailed plan to the same file and marks it `in progress`. Hand off to `using-software-specialists` for implementation; brainstorm writes no code.
4. **After implementation** — ask the user if they're ready to start the next sub-task. On yes, mark the current one `done` and return to step 3. Stop when none remain.

Design one sub-task at a time. Later sub-tasks stay one-liners until their turn. If a sub-task's design needs to change an earlier sub-task's design, say so and agree the change before continuing; record it in the feature plan and include the rework in the current sub-task's plan.

## Socratic Questioning

One question per message. Ask in plain text — no option-picker tools. When the options are known, name them inside the question. Let each answer shape the next question. Ask "why" when the stated need and the real need might differ.

**Settle from the code before asking.** Before any question about how or where to do something, find the closest existing case in the code or KB (the same kind of thing, in the same module) and follow it. When existing cases disagree, follow the closest one and name it. An answer that the request states or the code shows is a decision you make, not a question.

**Message shape.** While agreeing scope or designing a sub-task, each message has two parts, in this order:
1. **Decided** — what you settled from the request or the code, one line each, with its source (a file, or the user's words). The user corrects any that are wrong.
2. **Question** — at most one, about something neither the request nor the code settles. Lead with your recommended answer and the reason: *"I'd default to X because Y — does that fit?"*

If nothing is open, end with the next step instead of a question.

Progression template:
- Purpose: *"What problem does this solve?"*
- Goal: *"Why does this matter right now?"*
- Constraints: *"What configuration, integrations, or existing systems should I know about?"*
- Success: *"What does a successful outcome look like — what would it allow users to do?"*
- Validate: *"So the core need is X — is that right?"*

## Revision Mode

Invoked with an existing plan file? Read it, identify the delta, ask only about deltas, re-validate changed sections (Step 7), update in place after approval. Hard rule still applies.
