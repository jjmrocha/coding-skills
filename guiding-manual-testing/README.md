# guiding-manual-testing

A Claude Code skill for testing a change by hand against a real environment
with real data. The agent guides you one step at a time: it proposes a single
action, waits for the output, interprets it, and only then proposes the next
step.

## When to use

- Checking that a fix or feature behaves correctly on a local, testing or
  staging environment.
- Confirming that a change works against real data before you merge or
  release it.
- Testing a code path that only shows up with production-shaped data.

## When not to use

- Writing automated tests. Use `writing-unit-tests`.
- Auditing the code itself. Use `analyze-code`.
- Answering questions about how the code works. Use `research`.
- Production environments, which are not supported.

## What it enforces

- Each message holds one step. There are no multi-step plans and no
  branching instructions.
- A check passes only when both cases of a matched pair were observed: the
  case that must change and the case that must not.
- Data is produced through the real paths first, by running the job or using
  the UI. Changing the database directly is a fallback that must be justified.
- Before any direct change to data, the statement that restores it is
  captured. Data produced through the real paths stays in place. The blast
  radius of each trigger is stated before it runs.

## Output

A verification report in the conversation. It states what was under test, the
environment, the subject chosen and why, and each case with its predicted and
observed evidence. Unexpected observations are listed as separate findings.
When data was changed directly, the report confirms that the cleanup restored
it.

## Usage

```
/guiding-manual-testing help me test this on staging
/guiding-manual-testing verify the order cancellation fix on my local environment
```
