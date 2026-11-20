---
name: designing-top-down
description: Use when implementing a feature, tool, or function that needs more than a few lines of code — before writing that code, including when the whole solution already seems obvious.
---

# Designing Top-Down

**Write the top function first, as real code that calls functions that do not exist yet. Then do the same for each of those functions, one at a time, until every function can be written without calling a new unsolved one.**

## Steps

1. **State the goal as you would explain it to someone.** Say what goes in and what comes out, in a few sentences. When something in the goal is unclear, ask the person who gave you the task. If the unclear part changes the top function, stop until you have the answer. If it only touches one lower function, leave that function for later and work on another.

2. **Write the template.** Write the top function in real code. Call a new function for each step you have not solved yet, and give it the signature you think it needs. Write each unsolved function as a stub, so the file runs:

   ```python
   def find_files_by_mask(mask):
       raise NotImplementedError
   ```

   The template is right when this is true: if every stub worked as its signature says, this code would solve the problem.

3. **Base each signature only on what the caller needs at that point.** How the function will be built is a question for the next step, not this one.

4. **Pick one stub and repeat step 2 for it.** Finish that function completely, including the functions it calls, before you start the next stub.

5. **A function is finished when its body calls no new unsolved function.** Write it directly.

6. **When a lower function shows that a template above it is wrong, change the template.** Then fix everything that depended on it, including functions you already finished. The goal is a working solution, not keeping finished work.

## Example

Goal: "Given a file-name mask and a regular expression, print the files under the current directory whose name matches the mask and whose contents match the expression."

First template, before anything else is written:

```python
def main(mask, pattern):
    matching_files = [path for path in find_files_by_mask(mask)
                      if file_contains(path, pattern)]
    print_results(matching_files)


def find_files_by_mask(mask):
    raise NotImplementedError


def file_contains(path, pattern):
    raise NotImplementedError


def print_results(paths):
    raise NotImplementedError
```

Then `find_files_by_mask` gets the same treatment, and is finished before `file_contains` starts.

## Check before you finish

Read the top function out loud. It should sound like the explanation from step 1. If it also parses, sorts, filters, or formats inline, those are steps that were never split out. Move each into its own function.

## Other skills

`writing-unit-tests` writes the tests once the code works. This skill decides the order in which functions are written and how the code is split.
