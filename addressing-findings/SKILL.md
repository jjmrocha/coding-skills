---
name: addressing-findings
description: Use when the user wants to work through review findings, PR review comments, audit results, or a list of issues, deciding on each before anything changes — "address the findings", "go through the report", "address the comments on PR #N", "let's fix these one at a time", or right after an analyze-code report or code review.
---

# Addressing Findings

Walk a findings list one item at a time: explain, propose, stop. The user decides each one; nothing changes until they do.

**One finding per message, always.** Time pressure and "batch the obvious ones" change how long each message is, not how many findings it holds. Deciding which findings are "obvious" is the user's call.

## Before the first finding

1. **Source the list.**
   - *analyze-code report* — use its findings in report order (already severity-ranked). Each finding's `Action: … → <specialist>` names its specialist.
   - *PR comments* — if not already provided, fetch them: `gh api repos/{owner}/{repo}/pulls/N/comments` (inline) and `gh pr view N --comments` (review bodies). Sort each comment:
     - requests a change → finding
     - asks a question → finding; one option is "answer only, no code change"
     - praise, acknowledgement, resolved thread → not a finding
     - Order: severity you assess, then `file:line`.
   - *Anything else* — the list the user names; none exists → ask for it.
   - Another list exists that the user didn't name (a report next to PR comments) → mention it in the orientation line; don't merge it.
2. **Re-check current state.** Code may have changed since the list was made. Drop findings already resolved.
3. **One line of orientation:** the source, M findings in the order you'll take them, what was dropped and why (resolved, praise). Then Finding 1.

## Per finding

Load the specialist the finding names; if it names none, pick one through `using-software-specialists`. Put `Using <specialist> specialist` directly above the finding header.

Full form:

1. **`## Finding N of M: <plain-language title>`** (PR comment: add `— <author>, #<comment id>`)
2. **Issue** — what is wrong, quoting the line(s) with `file:line`. What it affects and when it bites. If an earlier claim about it was wrong, correct it here.
3. **Fix options** — usually two, each with its cost and the tests it adds. Include "keep it and document why" when that is a real option. Steps only the user can do (rotate a key, change infra) are named as such.
4. **Recommendation** — one option, one sentence why.
5. **One question**, plain text, ending the message: "Apply A?" No option pickers, no second question.

Compact form — when the user signals time pressure ("move fast", "we're late", "batch these"): title, Issue in one line, recommended fix as a snippet with the tests it adds and any user-only step, "Apply?".

Then stop.

## On the user's answer

| Answer | Do |
|---|---|
| Approve ("go ahead", "go with A") | Apply exactly that. Run the project's verification (lint, tests). Report the outcome in 1–3 lines with the results — say so when the verification never exercises the changed code — then present the next finding. |
| Approve several by number ("apply 1, 3, 5") | Apply exactly those, verify once, report, present the next undecided finding. |
| Approve + extra scope ("and tidy it while you're there") | Apply the approved option only. Extra scope that overlaps a later finding waits for that finding; anything else becomes a new finding at the end of the list. |
| Skip ("next", "later", "leave it") | Don't re-pitch. Record as skipped; present the next finding. |
| Confusion ("explain", "I didn't understand") | Re-explain the same finding with before/after snippets and no new options. Repeat the question. |
| Pushback on the premise | Accept the correction; drop or narrow the finding. Save the correction to memory if it should outlive the session. |
| "I made changes, check them" | Report-only: build, lint, tests, what is now resolved, what is still open. No edits. |

## PR replies (never posted)

Never post to the PR — no replies, no resolved threads, no submitted reviews, even when asked to. The user posts; you write the text they can use.

After each decided PR finding, give the suggested reply for that thread: `#<comment id> (<author>): <text>`. Repeat them all in the closing.

## Rules

- Every change traces to an approved option — no "while I'm here" edits.
- Docs, plan, and wiki edits are changes too: approve first.
- Never stage or commit.
- A finding made moot by an earlier fix: one line saying so, then move on.

| Rationalization | Reality |
|---|---|
| "The user is in a hurry, a batch is faster" | Use the compact form. The user can approve several by number. |
| "These fixes are all in the same function" | Same function, separate decisions. Mention the overlap and present them one after another. |
| "They said address the comments — that's approval" | Approval is per finding. A request to address is a request to start the walk. |
| "They told me to reply to alice, so posting is fine" | You never post. Give them the reply text. |

## Closing

After the last finding: a table `# | Finding | Outcome` (fixed / documented / answered / skipped / resolved by user / needs user action), the current verification status, what is left uncommitted, and — for PR comments — the suggested reply text per thread, for the user to post.
