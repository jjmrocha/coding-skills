# research

A skill for **answering questions about your own system** — you have a question
and need a sourced, cited answer, not a conversation that asks *you* questions.

It answers questions about:

- **The code** — "do we have an endpoint for X?", "what's the payload of event
  X?", "what happens when X?". Read with **serena**'s symbol tools
  (`get_symbols_overview` → `find_symbol` → `find_referencing_symbols`) so the
  agent loads only the relevant symbol and cites it — never answering from
  memory, and reading far fewer tokens than opening whole files.
- **What we've documented** — system surfaces, patterns, decisions, plans, how
  we run things. Read from the **KB** (`knowledge-base`), then validated against
  the code.

**Code is ground truth.** When the KB and the code disagree, the code wins —
report the drift and fix the KB.

Effort scales to the question: a one-line lookup gets a direct cited answer with
no ceremony; a deeper trace gets explicit confidence levels, conflict reporting,
and a stopping criterion set upfront.

## What it does NOT do

**External / wider-world research** — best-practice approaches, comparing
libraries, fact-checking a claim against official docs or the web — is not this
skill's job. That work belongs to the `deep-research-agent` specialist inside
[using-software-specialists](../using-software-specialists/), which owns the
source hierarchy, confidence, and conflict-reporting discipline for outside
sources. `research` hands those questions off rather than answering them from
memory.

## Usage

```
/research do we have an endpoint for password reset?
/research what happens when an order is cancelled?
/research is there a plan for PROJ-1234?
```
