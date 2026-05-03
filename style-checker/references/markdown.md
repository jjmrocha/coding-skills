# Google Markdown Style Guide — Formatting

Source: https://google.github.io/styleguide/docguide/style.html

## Headings

- Use **ATX-style headings** (`#`, `##`, `###`) — **never** Setext-style underlines (`===` or `---`).
- Exactly **one H1** per document (the title).
- Blank line **before and after** every heading.
- Space required after `#`.
- Heading names: **unique and fully descriptive** within the document.
- Capitalization: follow Google Developer Documentation Style Guide (sentence case for headings).

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

## Line Length

- **80-character limit** for prose.
- Exceptions (may exceed 80 chars): URLs, links, tables, headings, code blocks.
- Use reference-style links for long URLs that would break the 80-char limit.

---

## Lists

### Unordered Lists
- Use `*` for list markers (not `-` or `+`).
- Nested items: **4-space indent**.

```markdown
* First item
* Second item
    * Nested item
```

### Ordered Lists
- Use **lazy numbering** (all `1.`) for long or frequently changed lists.
- Use full sequential numbering (`1.`, `2.`, `3.`) for short, stable lists.
- Content alignment: 2 spaces after the number, 3 spaces after bullets (for 4-space total indent).

```markdown
1. First item
1. Second item
1. Third item

or:

1. First item
2. Second item
3. Third item
```

---

## Code Formatting

### Inline Code
- Use **backticks** for: field names, file names, file types, short code snippets, technical terms.

```markdown
Use `myVariable` and save to `config.json`.
```

### Code Blocks
- Use **fenced blocks** (triple backticks) with an explicit language tag.
- **Never** use indented code blocks (4-space indent interpreted as code).
- Use trailing backslash to escape newlines in command examples.

```markdown
    ```python
    def hello():
        print("hello")
    ```
```

Wrong (indented code block):
```markdown
    def hello():
        print("hello")
```

---

## Emphasis

- `**bold**` for strong emphasis.
- `*italic*` for light emphasis.
- Use emphasis **sparingly**.
- Prefer **backtick inline code** over emphasis for technical terms, file names, field names, and code references.

```markdown
<!-- Preferred for technical terms -->
Use the `--verbose` flag.

<!-- Not recommended -->
Use the *verbose* flag.
```

---

## Links

- Use **descriptive link text** — avoid "click here", "here", "link".
- Internal links: use **explicit paths** (`/path/to/file.md`), not full URLs.
- Relative paths: safe within same directory; avoid `../` constructions.
- **Reference-style links**: use for long URLs or repeated references to maintain 80-char limit.
- Define references just before the next heading in their section.

```markdown
<!-- Good -->
See the [configuration guide](docs/config.md).
Visit the [Google style guide][style-guide].

[style-guide]: https://google.github.io/styleguide/

<!-- Avoid — non-descriptive text -->
See [here](https://very-long-url.example.com).
[Click here](docs/config.md) for the guide.
```

---

## Blank Lines

- **One blank line** before and after headings.
- **One blank line** (empty line) between paragraphs.
- **No trailing spaces** for line breaks — use a blank line between paragraphs instead.

---

## Trailing Whitespace

- **Prohibited.** No trailing spaces at end of lines.
- Use trailing backslash `\` to escape newlines within code blocks if needed.

---

## HTML

- **Avoid inline HTML.** Prefer standard Markdown syntax.
- Use HTML only when Markdown cannot express the required formatting.

---

## Table of Contents

- Add `[TOC]` directive after the introduction, before the first H2 heading.
- Omit `[TOC]` only if all content is visible "above the fold" on a laptop screen.

---

## Document Structure

Recommended layout:
1. `# Title`
2. Author (optional)
3. Introduction paragraph(s)
4. `[TOC]`
5. Content sections (each `## H2`)
6. `## See also` (optional final section)

---

## File Naming

- Lowercase with underscores or dashes: `my_document.md`, `getting-started.md`.
- `README.md` is the conventional name for directory-level documentation.
