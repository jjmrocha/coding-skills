# Google JSON Style Guide — Naming & Values

Source: https://google.github.io/styleguide/jsoncguide.html

The Google JSON guide covers **JSON APIs**: request and response payloads, and data files a project defines (examples, fixtures, data documents). It sets **no formatting rules** — no indentation, line length, or key order beyond the reserved properties below. Do not report formatting.

## Scope

- **Check**: API request/response examples, fixtures, data files, and other JSON whose keys the project chooses.
- **Skip**: configuration files whose keys are defined by a tool — `package.json`, `package-lock.json`, `tsconfig*.json`, `jsconfig.json`, `.eslintrc.json`, `composer.json`, `.vscode/*.json`, `renovate.json`, `*.schema.json` keywords, lock files, and similar. Their authors cannot rename the keys. `tsconfig.json` and `.jsonc` files allow comments.

---

## General

- **No comments** in JSON.
- **Double quotes** around every property name and every string value. Booleans, numbers, and `null` are **not** quoted: `"isGift": "true"` and `"quantity": "3"` are wrong.
- Flatten data; use a nested object only when it is semantically one structure (such as an address).

---

## Property Names

- **lowerCamelCase ASCII**: `apiVersion`, `createdAt`, `unitPrice`. `snake_case`, `kebab-case`, and `PascalCase` are wrong.
- First character: a letter, `_`, or `$`. Then letters, digits, `_`, or `$`. So `_links` and `$schemaRef` are allowed.
- Avoid JavaScript reserved words.
- **Map keys are exempt**: when an object is used as a map, keys may be any Unicode string (`"72"`, `"en-US"`). Do not report them.
- **Arrays have plural names; everything else is singular.** `"item": [...]` and `"tags": "fragile"` are wrong. Numeric totals such as `totalItems` are fine.
- Avoid reserved property names (below) for anything other than their defined meaning. Resolve naming conflicts with a new name or a new API version.

---

## Property Values

- Values are booleans, numbers, strings, objects, arrays, or `null` — never JavaScript expressions.
- **Empty or `null` optional values: consider removing the property**, unless the value has meaning (`"balance": 0`). Report as Low.
- **Enum values are strings**: `"color": "WHITE"`, not a numeric code.
- **Dates**: RFC 3339 strings: `"2007-11-06T16:34:41.000Z"`. `"03/11/2026 14:05"` is wrong.
- **Durations**: ISO 8601 strings: `"P3Y6M4DT12H30M5S"`, `"PT90M"`. `"90 minutes"` is wrong.
- **Latitude/longitude**: one ISO 6709 string, preferably `±DD.DDDD±DDD.DDDD`: `"+40.6894-074.0447"`. An object `{ "lat": ..., "lng": ... }` is wrong.

---

## Reserved Structure

A response has a few top-level properties and then **either a `data` object or an `error` object, never both**. Reserved properties are optional; when a service needs the concept, use the reserved name.

- **Top level**: `apiVersion` (should always be present), `context`, `id`, `method`, `params`, `data`, `error`.
- **In `data`**: `kind`, `fields`, `etag`, `id`, `lang`, `updated` (RFC 3339), `deleted`, `items`, and the paging properties `currentItemCount`, `itemsPerPage`, `startIndex`, `totalItems`, `pageIndex`, `totalPages`, `pageLinkTemplate`, `next`/`nextLink`, `previous`/`previousLink`, `self`/`selfLink`, `edit`/`editLink`.
- **In `error`**: `code`, `message`, `errors` (array of objects with `domain`, `reason`, `message`, `location`, `locationType`, `extendedHelp`, `sendReport`).

### Property Order
- `kind`, when present, is the **first** property of its object.
- `items` is the **last** property of `data`.

```json
{
  "apiVersion": "2.0",
  "data": {
    "kind": "album",
    "id": "1",
    "updated": "2010-01-07T19:58:42.949Z",
    "totalItems": 2,
    "items": [
      { "kind": "photo", "title": "Lisa" },
      { "kind": "photo", "title": "Bart" }
    ]
  }
}
```
