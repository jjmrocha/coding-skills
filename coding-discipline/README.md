# coding-discipline

A Claude Code skill that names the six most common failure modes of code
written by language models, and the counter for each. It is loaded on every
coding turn.

## When to use

Any non-trivial task that writes or changes code: a feature, a bug fix, a
refactor, applying a suggested edit or generating a new module. Skip it for
trivial changes such as a typo fix.

## Credit

Failure modes 1 to 3 and 5 (silent assumption, scope creep, speculative
complexity and drift) are catalogued by Andrej Karpathy in his
[January 2026 tweet on LLM coding pitfalls](https://x.com/karpathy/status/2015883857489522876).

Failure mode 4 (hallucination, countered by verifying before writing) and
failure mode 6 (parallel solution) are this skill's own. So are the
failure-mode table, the falsifiable tests and the pre-commit self-check.
