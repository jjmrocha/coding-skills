# addressing-findings

A Claude Code skill for working through a list of findings one at a time. The
list can be an `analyze-code` report, the review comments on a pull request,
or any other list of issues. For each finding it explains the problem,
proposes fix options, recommends one and asks you to choose. Nothing changes
until you approve.

## When to use

- Right after an `/analyze-code` report.
- When you address the review comments on a pull request.
- For any list of issues where each one needs a decision before the code
  changes.

## When not to use

- To produce the findings in the first place. Use `/analyze-code`.
- To diagnose a single bug. Use `/using-software-specialists` with the
  troubleshooter specialist.

## What it enforces

- Each message holds one finding. Under time pressure the messages get
  shorter, but never hold more than one finding. You can approve several
  findings by number.
- Every change traces to an option you approved, and nothing is edited on the
  side. Edits to docs, plans and the wiki count as changes.
- After each approved change, the project's lint and tests run and the result
  is reported.
- It never posts to the pull request. It gives you the reply text for each
  thread, and you post it. It never stages or commits.

## Usage

```
/addressing-findings
/addressing-findings go through the report
/addressing-findings address the comments on PR #42
```
