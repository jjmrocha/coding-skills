# designing-top-down

A Claude Code skill that sets the order in which code is written, so the top
function reads like an explanation of the problem. Loaded by
`using-software-specialists` in the Implementation phase.

The core rule: **write the top function first, as real code that calls
functions that do not exist yet.** Then do the same for each of those
functions, one at a time, until every function can be written without calling
a new unsolved one.

## When to use

Implementing a feature, tool, or function that needs more than a few lines of
code, before writing that code. This includes cases where the whole solution
already seems obvious.

## What it asks for

1. The goal, stated as you would explain it to someone.
2. A template: the top function in real code, with each unsolved step written
   as a stub. The template is right when the code would solve the problem if
   every stub worked as its signature says.
3. Each signature based only on what the caller needs.
4. One stub at a time, finished completely before the next.
5. Going back up and changing a template when a lower function shows it is
   wrong, even if finished work must be redone.

## Why it exists

Without guidance, agents write a whole module in one step. The top function
then mixes layers: it parses arguments, reads files, sorts, filters and formats
output inline, so it no longer reads like the problem it solves.

## Provenance

Written test-first with headless Claude Code on three small command-line tasks.
Without the skill, 1 of 15 runs produced a top function that only called named
steps, and none wrote a template first. With the skill, 15 of 15 top functions
only called named steps, and 9 of 15 runs wrote the template with stubs before
anything else. Agents mostly did not fill the stubs one at a time; that step is
kept because it is part of the method, not because the tests enforced it.

The method is the author's own way of solving coding problems: turn one
unsolved problem into a few smaller unsolved problems, and repeat.
