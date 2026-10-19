# Google Markdown Style Guide — Formatting

Source: https://google.github.io/styleguide/docguide/style.html

## Headings

- Use **ATX-style headings** (`#`, `##`, `###`) — **never** Setext-style underlines (`===` or `---`).
- Exactly **one H1** per document (the title), ideally the same or nearly the same as the file name. All other headings are H2 or deeper.
- Space after `#`, and a blank line **before and after** every heading.
- Heading names: **unique and fully descriptive** within the document, even for sub-sections (`### Foo summary`, not a second `### Summary`), because anchors are built from them.
- Capitalization: follow the Google Developer Documentation Style Guide (sentence case for titles and headings).
- **Preserve the original capitalization** of product, tool, and binary names everywhere (`Markdown`, `gRPC`, `iOS`, `npm`).

```markdown
# Document Title

## Section Heading

### Subsection Heading

Wrong — Setext style:
Title
=====

Section
-------
```

---

## Document Layout

Recommended layout:
1. `# Title`
2. Author (optional)
3. Short introduction: 1–3 sentences
4. `[TOC]` (only where the hosting supports it)
5. Content sections, starting at `## H2`
6. `## See also` (optional final section with further links)

### Table of Contents
- `[TOC]` is a directive of hosting such as Gitiles. GitHub and most other renderers do not support it. **Do not report a missing `[TOC]`** unless the project uses such hosting.
- Where used: place it after the introduction and before the first H2. Omit it when all content is visible without scrolling on a laptop.

---

## Line Length

- **80-character limit** for prose.
- Exceptions (may exceed 80 chars): links, tables, headings, code blocks. Text before and after a long link is still wrapped.

---

## Trailing Whitespace

- **Prohibited.** Do not use two trailing spaces for a line break.
- For a hard line break, use a trailing backslash `\`, sparingly. Better: avoid the need and start a new paragraph with a blank line.

---

## Lists

### Markers and Spacing
- The guide sets **no rule** between `*` and `-` for bullets. Its examples use `*`. Report only mixed markers within one list, as Low.
- Use a **4-space indent** for wrapped text and nested lists, for both numbered and bulleted lists:
  - Numbered: 2 spaces after `1.`, so the text starts at column 4.
  - Bulleted: 3 spaces after `*`, so the text starts at column 4.
  - Wrapped text in a nested list: 8-space indent.
- Small, non-nested, single-line lists may use one space after the marker.

```markdown
1.  Use 2 spaces after the item number, so the text itself is indented 4 spaces.
    Use a 4-space indent for wrapped text.
2.  Use 2 spaces again for the next item.

*   Use 3 spaces after a bullet, so the text itself is indented 4 spaces.
    1.  Nested numbered item.
        Wrapped text in a nested list needs an 8-space indent.

* Foo
* Bar
```

### Numbering
- Use **lazy numbering** (all `1.`) for long lists that may change, especially nested ones.
- Use full sequential numbering (`1.`, `2.`, `3.`) for short, stable lists.

---

## Code

### Inline Code
- Use **backticks** for short code quotations, field names, commands, and file types in a generic sense (`README.md`).
- Use a code span to stop Markdown processing, for example a fake path or example URL that would autolink: `` `https://www.google.com/search?q=$TERM` ``.

### Code Blocks
- Use **fenced blocks** (triple backticks) for any code longer than one line.
- **Declare the language** on the fence (` ```python `).
- Fenced blocks are strongly recommended over indented (4-space) code blocks, which cannot declare a language and have ambiguous boundaries.
- Escape newlines with a trailing backslash `\` in command-line snippets meant to be copied into a terminal.

```markdown
    ```shell
    $ bazel run :target -- --flag --foo=longlonglonglonglongvalue \
      --bar=anotherlonglonglonglonglonglonglonglongvalue
    ```
```

### Code Blocks in Lists
- Indent a fenced block to the list item's text indentation so it does not break the list.
- An indented code block inside a list is indented 4 additional spaces from the list indentation.

```markdown
*   Bullet.
    ```c++
    int foo;
    ```
*   Next bullet.
```

---

## Links

- **Shorten links** wherever possible.
- **Informative link text**: wrap the most fitting phrase. Never "here", "link", or the bare URL as text.
- Links to other Markdown pages: use the **explicit path** (`/path/to/page.md`), not the full qualified URL.
- Relative paths are fine within the same directory. **Avoid `../`** relative paths.

### Reference Links
- Use reference links (`[text][ref]`) **only when the URL is long enough to hurt readability** inline. For a short URL, inline it.
- Use them more often in tables, to keep cells short, and to avoid repeating the same URL.
- Define a reference just before the next heading, at the end of the section where it is first used. A reference used in several sections goes at the end of the document.

```markdown
<!-- Good -->
See the [configuration guide](/docs/config.md).
The [style guide] says not to use reference links unless you have to.

[style guide]: https://docs.google.com/document/d/13HQBxfhCwx8lVRuN2Wf6poqvAfVeEXmFVcawP5I6B3c/edit

## Next section

<!-- Avoid — non-descriptive text -->
See [here](https://example.com/docs).
<!-- Avoid — reference link for a short URL -->
The [style guide][style_guide] says so.

[style_guide]: https://google.com/Markdown-style
```

---

## Blank Lines

- **One blank line** before and after headings.
- **One blank line** between paragraphs.

---

## Tables

- Use for **tabular data** with fairly uniform distribution across two dimensions, or many parallel items with distinct attributes, that needs quick scanning.
- **Avoid** for data that fits a list: poor distribution (many empty or identical cells), few rows relative to columns, or long prose in cells.
- Use reference links inside table cells to keep them short.

---

## HTML

- **Strongly prefer Markdown over HTML.** Avoid HTML hacks; reconsider whether you need the effect. Big tables are the main exception.
- HTML reduces portability (Gitiles does not render HTML).

---

## Images

- Use sparingly; prefer simple screenshots. Use them when it is easier to show than to describe (UI navigation).
- Always include **descriptive alt text**.

---

## Documentation Philosophy

- Maintain a **small set of fresh and accurate docs**, not sprawling, outdated documentation. Delete cruft in small batches.
- **Better/Best Rule**: accept iterative improvements over perfectionism to keep authors productive.
