# Google HTML/CSS Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/htmlcssguide.html

Applies to HTML, CSS, Sass, and GSS source files. Generated, minified, or compiled output is exempt. Several rules are marked **(optional)** in the guide: report those only as Low, and never report their absence when the file is consistent.

## General (HTML and CSS)

- **Protocol**: use `https:` for images, media, style sheets, and scripts. Both `http:` and protocol-relative `//host/...` URLs are wrong (unless the resource is not available over HTTPS).
- **Indentation**: 2 spaces. No tabs, no mixed tabs and spaces.
- **Lowercase only**: element names, attributes, attribute values (except text/CDATA), CSS selectors, properties, and property values (except strings). `<A HREF="/">` and `color: #E5E5E5;` are wrong.
- **No trailing whitespace.**
- **Encoding**: UTF-8 without BOM. HTML documents declare `<meta charset="utf-8">`. Style sheets do **not** declare an encoding (no `@charset`, unless truly needed; then with double quotes).
- **Comments**: explain code where needed (optional).
- **Action items**: use the keyword `TODO` only, followed by a colon: `TODO: action item`. Other markers such as `@@` are wrong. The guide does **not** use the `TODO(name):` form for HTML/CSS.

```html
<!-- TODO: Remove optional tags. -->
```

---

## HTML Style Rules

- **Document type**: `<!doctype html>`. Legacy doctypes (HTML 4, XHTML) and a missing doctype are wrong.
- **Validity**: use valid HTML where possible.
- **Semantics**: use elements for their purpose — headings for headings, `p` for paragraphs, `a` for links. `<div onclick="...">` acting as a link or button is wrong.
- **Multimedia fallback**: images have meaningful `alt` text; video and audio have transcripts or captions where available. Decorative or redundant images use `alt=""` — that is correct, not a violation.
- **Separation of concerns**: keep structure, presentation, and behavior apart. Inline `style` attributes, presentational elements (`<center>`, `<font>`, `<u>` for styling), and inline event handlers (`onclick`) are wrong. Link as few style sheets and scripts as possible.
- **Entity references**: do not use them (`&mdash;`, `&rdquo;`, `&#x263a;`); write the character. Exceptions: characters with special meaning in HTML (`&lt;`, `&amp;`) and invisible characters (`&nbsp;`).
- **Optional tags (optional)**: the guide recommends **omitting** optional tags (`<html>`, `<head>`, `<body>`, `</li>`, `</p>`, `</td>`, ...), consistently. A document without them is correct. Do not report missing optional tags. Including them may be reported as Low at most.
- **`type` attributes**: omit `type` on style sheets (`type="text/css"`) and scripts (`type="text/javascript"`). Exception: JavaScript modules **must** use `type="module"`.
- **`id` attributes**: avoid unnecessary `id`s; prefer `class` for styling and `data-*` for scripting. A required `id` always contains a **hyphen**: `user-profile`, not `profile` or `userProfile`.

```html
<!doctype html>
<meta charset="utf-8">
<title>Saving money, saving bytes</title>
<p>Qed.
```

---

## HTML Formatting Rules

- **Every block, list, or table element on a new line**, and child elements indented. `<div><p>One</p><p>Two</p></div>` on one line is wrong. Exception: putting all `li` elements on one line to avoid whitespace issues is acceptable (Low at most).
- **Line wrapping (optional)**: there is no column limit for HTML. When wrapping attributes, indent continuation lines so they are distinguishable from child elements, consistently within a project.
- **Quotation marks**: attribute values use **double quotes**. `class='nav'` is wrong.

```html
<ul>
  <li>Moe
  <li>Larry
  <li>Curly
</ul>
```

---

## CSS Style Rules

- **Validity**: use valid CSS unless dealing with validator bugs or proprietary syntax.
- **Class names**: meaningful (`.gallery`, `.login`) or generic (`.aux`, `.alt`). Presentational (`.button-green`, `.clear`) and cryptic (`.yee-1901`) names are wrong.
- **Class name length**: as short as possible, as long as necessary: `.nav`, `.author` — not `.navigation`, `.atr`.
- **Delimiters**: separate words with **hyphens** only. `.demoimage`, `.error_status`, and `.navBar` are wrong.
- **Prefixes (optional)**: in large or embeddable projects, prefix classes with a short namespace and a dash: `.adw-help`.
- **Type selectors**: do not qualify classes with element names: `.error`, not `div.error` or `ul.example` (unless necessary).
- **ID selectors**: avoid them. `#example` is wrong; use a class.
- **Shorthand properties**: use them where possible, even when setting one value: `padding: 0 1em 2em;` instead of four `padding-*` declarations; `font: 100%/1.6 palatino, georgia, serif;`.
- **0 and units**: no unit after `0` unless required: `margin: 0;`. Correct exceptions: `flex: 0px;` and `flex: 1 1 0px;` (the flex-basis needs a unit). Do not report these.
- **Leading 0s**: always: `font-size: 0.8em;`, not `.8em`.
- **Hexadecimal**: 3-character notation where possible: `#ebc`, not `#eebbcc`; and lowercase.
- **`!important`**: avoid; use selector specificity.
- **Hacks**: avoid user-agent detection and CSS hacks; try another approach first.

---

## CSS Formatting Rules

- **Declaration order (optional)**: sort consistently within a project; in the absence of tooling, alphabetical order is suggested. Ignore vendor prefixes when sorting, but keep multiple prefixes for one property sorted (`-moz-` before `-webkit-`). Report unsorted declarations only as Low.
- **Block content indentation**: indent all block content — declarations and rules inside rules (such as inside `@media`).
- **Declaration stops**: a semicolon after **every** declaration, including the last.
- **Property name stops**: no space before the colon, one space after: `font-weight: bold;`.
- **Declaration block separation**: one space between the last selector and `{`, and `{` on the **same line** as the last selector. `.video{` and a `{` on the next line are both wrong.
- **Selector and declaration separation**: each selector and each declaration on its own line. `a:focus, a:active {` and `position: relative; top: 1px;` are wrong.
- **Rule separation**: a **blank line** between rules.
- **Quotation marks**: **single quotes** for attribute selectors and property values: `font-family: 'open sans', arial, sans-serif;`. **No quotes inside `url()`**: `@import url(https://www.google.com/css/maia.css);`. Exception: `@charset` requires double quotes.
- **Section comments (optional)**: group sections with comments, separated by new lines.

```css
@media screen, projection {
  html {
    background: #fff;
    color: #444;
  }
}

h1,
h2,
h3 {
  font-weight: normal;
  line-height: 1.2;
}
```

Note: older versions of the guide discouraged `@import`. The current guide has no such rule; do not report `@import` itself.
