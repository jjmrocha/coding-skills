# research

A skill for **answering questions about your own system**. You have a question
and need an answer with cited sources, and the skill brings that answer to you
instead of asking you questions.

It answers two kinds of question:

- Questions about the code, such as "do we have an endpoint for X?", "what is
  the payload of event X?" or "what happens when X?". It reads the code with
  **serena**'s symbol tools (`get_symbols_overview`, then `find_symbol`, then
  `find_referencing_symbols`), so the agent loads only the relevant symbol and
  cites it. It never answers from memory, and it reads far fewer tokens than
  it would by opening whole files.
- Questions about what the team has documented: system surfaces, patterns,
  decisions, plans and how things are run. It reads these from the knowledge
  base (`knowledge-base`) and then checks them against the code.

**Code is ground truth.** When the knowledge base and the code disagree, the
code wins. The skill reports the drift and fixes the knowledge base.

The effort matches the question. A one-line lookup gets a direct answer with a
citation and nothing more. A deeper trace gets a confidence level for each
finding, a report of any conflicts, and a stopping criterion set at the start.

## What it does not do

It does not research the wider world: best practices, library comparisons, or
checking a claim against official docs or the web. That work belongs to the
`deep-research-agent` specialist in
[using-software-specialists](../using-software-specialists/), which ranks
outside sources, rates confidence and reports conflicts between them.
`research` hands those questions off instead of answering them from memory.

## Usage

```
/research do we have an endpoint for password reset?
/research what happens when an order is cancelled?
/research is there a plan for PROJ-1234?
```
