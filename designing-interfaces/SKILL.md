---
name: designing-interfaces
description: Use when writing or changing code other code will call — a new type, function, method, module, or package — before the implementation exists. Also when a caller needs data or behavior a module does not currently expose, when widening an existing interface, adding a getter, or deciding where new logic should live.
---

# Designing Interfaces

**A zero-line diff is not a zero-cost change.** The cheapest change to write is usually the one that moves complexity out to the callers, where no diff records it.

An **interface** here is everything a caller must know to use a module correctly: the signature, plus the types it drags along, the constants, the ordering rules, the error modes, and the invariants. Not just the type-level surface.

## The Contract

**REQUIRED: write this before the implementation. Put it in your reply, not in a comment.** Write it for a reader who has not seen this session: plain sentences, real code, no shorthand.

```
WHAT:       <what it does, in plain sentences>
WHERE:      <the module it lives in; why there, when that isn't obvious>
INTERFACE:  <each signature, as code; under it, each input and output in a plain
            sentence: what it means, including empty/nil/zero, and when it errors>
USE:        <the caller's code using it. When an existing call site changes, show
            it before and after>
```

Then check it against these principles. A design that breaks one is redesigned before any code is written.

1. **It does real work for the caller.** Broken when WHAT only says it returns or exposes something the module holds.
2. **It keeps complexity inside.** Broken when USE shows the caller filtering, rendering, ordering, or interpreting what the module could do itself.
3. **It follows the single responsibility principle.** Broken when WHAT joins unrelated jobs with "and". Steps of one job ("locks, renders, writes") are one job; the test is whether a caller could want one part without the other.
4. **It takes only the inputs it strictly needs.** Each input is something only the caller can decide. Broken by an input the module already has or could default, or by a whole object passed when one field is used.
5. **The function and its parameters are descriptive**, and follow the language's naming conventions (Go: `ActiveUsers`, not `GetActiveUsers`; Python: `retry_after`). If only vague names fit (`Manager`, `Helper`, `Data`, `Process`), the design is unclear: fix the design, not the name.
6. **It avoids error cases it could handle itself.** Broken when INTERFACE lists an error the function could define away, such as "not found" where an empty result would do.
7. **It is hard to use wrongly.** Broken by adjacent parameters of the same type that are easy to swap, or by a rule the caller must remember that the types could enforce.
8. **It hides its internal representation.** Broken when INTERFACE or USE exposes how the module stores its data.
9. **It is as small as possible.** Every added function or method is a permanent cost to every caller; see below.
10. **It receives its dependencies, not creates them.** I/O, clock, network, and randomness are passed in, so tests can replace them; see Seams.

**Thin by design.** A registration, adapter, or dispatcher is supposed to be thin. Its WHAT names the callee that does the work. If you cannot name the callee, it breaks principle 1.

### Worked example

A command needs to save the conversation transcript, which the core holds privately.

```
✗ WHAT:       Returns a copy of the conversation lines.
  WHERE:      core/core.go.
  INTERFACE:  func (c *Core) Lines() []Line
                returns  a snapshot copy of every line; Line has Kind (one of six
                         constants) and Text
  USE:        for _, l := range c.core.Lines() {
                  if l.Kind != core.KindSystem { b.WriteString(render(l)) }
              }
              os.WriteFile(path, []byte(b.String()), 0o644)
```

WHAT only returns state (principle 1). USE filters, renders, and writes (principle 2). `Line` and `Kind` expose the storage (principle 8). Redesign.

```
✓ WHAT:       Writes the whole conversation so far to a file and reports where it went.
  WHERE:      core/core.go. The core owns the lines and their lock.
  INTERFACE:  func (c *Core) SaveTranscript(path string) (resolved string, err error)
                path      where to write; empty means "pick a default filename"
                resolved  the path actually written
                err       set when the file can't be written; resolved is then empty
  USE:        resolved, err := c.core.SaveTranscript(path)
```

One job, done inside the module. The line format never escapes.

## Interface width is a cost

Adding a method to an interface is a cost **even when no implementation changes.** An
existing type that already satisfies the new method has not made the change free — it has
hidden the price. What you actually changed is the set of things every caller may now do
and every future implementer must provide.

Price it by asking what the *widest* caller can now reach, not how many lines you edited.

**Deletion test.** Delete the module. If complexity vanishes, it was a pass-through and should not exist. If it reappears in N callers, it earned its place.

## Seams

A **seam** is a place you can change behavior without editing in that place.

Introduce one only when something actually varies across it. **The test counts as the
second adapter when — and only when — the dependency is I/O, a clock, randomness, or the
network.** For those, "only one caller exists" is not a reason to skip the seam; the test
is the other caller, and without the seam the test reaches around the module instead of
through it.

For anything else — pure computation, in-process state — one caller means no seam. Call it
directly.

## Relationship to coding-discipline

`coding-discipline` minimizes **what you build**. This skill constrains **what you expose**.
They pull in opposite directions exactly once, and this is the case that matters:

> The shallow design is almost always the smaller diff.

When the two conflict, minimality applies to the implementation, never to the caller's
required knowledge. "Could a senior cut this in half?" is a question about the
implementation. A smaller diff that widens an interface is not the smaller change.

`coding-discipline`'s speculative-complexity test — *does a second caller exist right now?* —
governs parameters, flags, and configuration. It does not govern seams at I/O boundaries;
the Seams rule above does.

## Rationalizations

| Excuse | Reality |
|---|---|
| "The type already has this method, so the interface change is free" | You changed what every caller may do and every implementer must provide. Zero diff, real cost. |
| "The core still owns the state" | It owns the field. If callers read it directly, they own the representation, and you can never change it. |
| "It's still a narrow surface" | Look at USE. If the caller does the work there, it isn't narrow. |
| "I'll expose the state and let the caller decide policy" | Then policy lives in N callers. Name the second caller that wants a different policy — if there isn't one, the policy belongs inside. |
| "A type alias means nothing breaks" | Aliases hide dependency-direction changes. Which package owns the type now? |
| "One caller doesn't justify inventing an abstraction" | True for parameters. False for I/O, clocks, and randomness — the test is the second caller. |
| "It's technically breaking but the blast radius is nil" | Show the call sites that change in USE, before and after. |
| "The tests pass and the linter is clean" | Neither one can see interface width. That is why the contract exists. |
| "I'll just add a getter" | A getter does no work. WHAT says "returns". |
| "The names explain themselves" | Not to a reader who wasn't in this session. Write the sentence. |

## Red Flags

- Writing a method that only returns stored state to a caller outside the module
- Moving a type into another package so an interface will compile
- Reaching for a type alias to keep existing code building
- A test that calls an unexported function, or touches a real filesystem, clock, or network
- "…so it satisfies the interface with no new code"
- Formatting or rendering a module's private representation from outside that module
- Noting a cost in your summary and then proceeding anyway
- A WHAT with "and" between two jobs

**All of these mean: write the contract, and check it against the principles.**
