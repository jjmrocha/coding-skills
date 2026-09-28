# addressing-findings

A Claude Code skill for working through a list of findings one at a time —
an `analyze-code` report, a PR's review comments, or any list of issues. For
each finding it explains the problem, proposes fix options, recommends one,
and asks. Nothing changes until you approve.

## When to Use

* Right after an `/analyze-code` report
* Addressing review comments on a PR
* Any list of issues where each needs a decision before code changes

**When NOT to use:**

* Producing the findings in the first place → `/analyze-code`
* Diagnosing a single bug → `/using-software-specialists` with the
  `troubleshooter` specialist

## What It Enforces

* **One finding per message.** Under time pressure, each message gets
  shorter; it never holds more than one finding. You can approve several by
  number.
* **Approval per finding.** Every change traces to an option you approved —
  no "while I'm here" edits. Docs, plan, and wiki edits count as changes.
* **Verified after each fix.** The project's lint and tests run after each
  approved change, and the outcome is reported.
* **Never posts to the PR.** It hands you the reply text for each thread;
  you post it. It never stages or commits.

## Usage

```
/addressing-findings
/addressing-findings go through the report
/addressing-findings address the comments on PR #42
```
