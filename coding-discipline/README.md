# coding-discipline

A Claude Code skill that names the six most common LLM coding failure modes
and the counter-move for each. Loaded on every coding turn.

## When to Use

Any non-trivial code-writing or code-modifying task — feature, bug fix,
refactor, applying a suggested edit, generating a new module. Skip for
typo-fix-class trivialities.

## Attribution & Provenance

**Failure modes #1–3 and #5** (Silent Assumption, Scope Creep, Speculative
Complexity, Drift) are catalogued by Andrej Karpathy in his
[January 2026 tweet on LLM coding pitfalls](https://x.com/karpathy/status/2015883857489522876).

**Failure mode #4** (Hallucination → Verify Before Writing) and **#6**
(Parallel Solution), the failure-mode-table framing, the smell tests, and the
Pre-Commit Self-Check are this skill's own.
