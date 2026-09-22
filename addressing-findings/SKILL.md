---
name: addressing-findings
description: Use when the user wants to work through review findings, audit results, or a list of issues one at a time, deciding on each before anything changes — "address each finding one by one", "go through the findings", "let's fix these one at a time", or right after a code review or analysis report.
---

# Addressing Findings

Walk a findings list one item at a time: explain, propose, stop. The user decides each one; nothing changes until they do.

Alway use the SKILL using-software-specialists.

## Before the first finding

- **Source the list**: the most recent review or report in the conversation, or the one the user names. None exists → ask for it.
- **Re-check current state**: code may have changed since the report. Drop findings already resolved and say so in one line.
- **Load the specialist** for the finding's domain when a routing skill (e.g. `using-software-specialists`) is available, and name it.

## Per finding

One finding per message, in this shape:

1. **`## Finding N of M: <plain-language title>`**
2. **Issue** — what is wrong, quoting the line(s) with `file:line`. Say what it affects and when it bites. If an earlier claim about it was wrong, correct it here.
3. **Fix options** — usually two, each with its cost. Include "keep it and document why" when that is a real option.
4. **Recommendation** — one option, one sentence why.
5. **One question** in plain text, ending the message: "Apply A?" No option pickers, no second question.

Then stop. Never begin the next finding in the same message as a question.

## On the user's answer

| Answer | Do |
|---|---|
| Approve ("go ahead", "go with A") | Apply exactly that. Run the verification the project requires (lint, tests, migration checks). Report the outcome in 1–3 lines with the results, then present the next finding. |
| Skip ("next", "later", "leave it") | Don't re-pitch. Record it as skipped; present the next finding. |
| Confusion ("explain", "I didn't understand") | Re-explain the same finding with more detail, with concrete before/after snippets and no new options. Repeat the question. |
| Pushback on the premise | Accept the correction; drop or narrow the finding. Save the correction to memory if it should outlive the session. |
| "I made changes, check them" | Report-only: build, lint, tests, what is now resolved, what is still open. No edits. |

## Rules

- Every change traces to an approved option — no "while I'm here" edits.
- Docs, plan, and wiki edits are changes too: approve first.
- Never stage or commit.
- A finding made moot by an earlier fix: one line saying so, then move on.

## Closing

After the last finding: a table `# | Finding | Outcome` (fixed / documented / skipped / resolved by user), the current verification status, and what is left uncommitted.
