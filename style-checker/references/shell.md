# Google Shell Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/shellguide.html

## Naming Conventions

| Identifier | Style | Example |
|-----------|-------|---------|
| Function | `lowercase_with_underscores` | `my_function` |
| Packaged function (with namespace) | `package::function_name` | `mypackage::my_func` |
| Variable (local) | `lowercase_with_underscores` | `my_variable` |
| Constant / environment variable | `UPPERCASE_WITH_UNDERSCORES` | `MY_CONSTANT`, `PATH` |
| Source file (library) | `lowercase_with_underscores.sh` | `my_lib.sh` |
| Source file (executable) | `lowercase_with_underscores` (no extension) or `.sh` | `my_script`, `my_script.sh` |

### Naming Rules
- **No camelCase or PascalCase** in shell scripts.
- **Libraries must have `.sh` extension** and should not be executable.
- Executables: `.sh` extension optional; if it is a library sourced by others, must have `.sh`.
- Constants: declared with `readonly` or `declare -xr` at the **top of the file**.
- Local variables: always declare with `local` inside functions.
- **Separate declaration from command-substitution assignment** — `local var; var="$(cmd)"`. Combining them (`local var="$(cmd)"`) masks the command's exit code, since `local` becomes the command that sets `$?`.

```bash
# Correct
local my_var
my_var="$(my_command)"

# Wrong — exit code of my_command is lost
local my_var="$(my_command)"
```

```bash
# Correct
readonly MAX_RETRIES=3
declare -xr EXPORT_VAR="value"

my_function() {
  local my_var="local_value"
}

# Wrong
myFunction() { ... }          # camelCase
MY_FUNCTION() { ... }         # all-caps function
local MyVar="value"           # mixed case variable
```

---

## Indentation & Line Length

- **2 spaces** per level. **No tabs.** (Exception: `<<-` here-document bodies may use tabs.)
- **80 characters** maximum line length.
- Long literal strings: use here-documents or embedded newlines.
- Long file paths or URLs exceeding 80 chars: exempt if on their own line.

---

## Shebang

- **Executables must start with** `#!/bin/bash` and minimal flags.
- Use `#!/usr/bin/env bash` only when `bash` is not at `/bin/bash`.

```bash
#!/bin/bash
# Description of script.
```

---

## Pipelines

- Keep on **one line** if it fits.
- Multi-line: pipe symbol on a **new line**, 2-space continuation indent.

```bash
# One line — OK
command1 | command2 | command3

# Multi-line — OK
command1 \
  | command2 \
  | command3
```

---

## Control Flow

- **`; then`** and **`; do`** go on the **same line** as `if`/`for`/`while`.
- `else` on its **own line**.
- Closing `fi`, `done`: vertically aligned with opening statement.
- Always include `in "$@"` explicitly in for loops.

```bash
# Correct
if condition; then
  do_something
elif other; then
  do_other
else
  fallback
fi

for item in "${list[@]}"; do
  process "${item}"
done

# Wrong
if condition
then
  do_something
fi
```

---

## Case Statements

- Indent alternatives **2 spaces** from `case`.
- Indent actions **2 spaces** from pattern.
- One-line alternatives: space after pattern `)` and before `;;`.
- Multi-line: pattern, actions, and `;;` on separate lines.
- Avoid `;&` and `;;&` notations.

```bash
case "${expression}" in
  a)
    action_a
    ;;
  b) action_b ;;
  *) default_action ;;
esac
```

---

## Functions

- Opening brace on the **same line** as function name.
- `function` keyword is optional but must be **consistent throughout a project**.
- **No space** between function name and `()`.
- Use a `main` function as the bottom-most function; call it as the last non-comment line.

```bash
# Correct
my_function() {
  local var="value"
  echo "${var}"
}

# With function keyword (if project uses it consistently)
function my_function() {
  ...
}

# Wrong — Allman brace style
my_function()
{
  ...
}
```

### main Pattern

```bash
main() {
  # main logic here
}

main "$@"
```

---

## Quoting

- **Always quote** variables: `"${var}"` not `$var`.
- **Always quote** strings containing variables, command substitutions, spaces, or shell meta-characters.
- Prefer `"${var}"` over `"$var"` (explicit braces).
- Single quotes: for literal strings with no substitution.
- Use `"$@"` (not `"$*"`) for passing arguments.

### Variable Expansion Precedence
1. Stay **consistent** with existing code.
2. **Quote** variables (as above).
3. Prefer `"${var}"` over `"$var"`.
4. Single-character specials / positional parameters: **unbraced** unless needed (`$1`, `$?`, `$$`, `$!`).
5. All other variables: **use braces** (`"${some_var}"`).

```bash
# Correct
echo "${my_var}"
echo "Result: $(command)"

# Wrong
echo $my_var
echo "Result: `command`"
```

---

## Testing & Comparisons

- Prefer **`[[ ... ]]`** over `[ ... ]`, `test`, or `/usr/bin/[`.
- Use **`==`** for string equality inside `[[ ... ]]` (not `=`).
- Numeric comparisons: use **`(( ... ))`** or `-lt` / `-gt` inside `[[ ... ]]`.
- Inside `(( ... ))` / `$(( ... ))`: omit the `${}` braces on variables (use `var`, not `${var}`), and keep a space after `((` and before `))`.
- For **empty strings**: use `-z` and `-n` rather than filler characters like `x`.

```bash
# Correct
[[ "${file}" == "config.yml" ]]
(( retries > 3 ))

# Wrong
[ "${file}" = "config.yml" ]
[[ "${file}" = "config.yml" ]]  # = is allowed but == is preferred
```

---

## Comments

- **File header**: required at top — brief overview of script purpose.
- **Function comments**: required for any non-obvious function; document:
  - Globals read and modified
  - Arguments (positional)
  - Outputs (stdout/stderr)
  - Return values
- Comment tricky, non-obvious, or important parts.
- `TODO` format: `# TODO(username): description`

```bash
#!/bin/bash
# Backs up user data to remote storage.

# Connects to the backup server and uploads the given directory.
# Globals:
#   BACKUP_HOST
# Arguments:
#   $1 - Source directory path
# Outputs:
#   Writes status to stdout; errors to stderr
# Returns:
#   0 on success, 1 on connection failure
backup_directory() {
  local src_dir="$1"
  ...
}
```

---

## Advanced Patterns

### Error Output Function

```bash
# Write error messages to stderr
err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}
```

### Arrays for Safe Quoting

Use arrays to safely build command flags without complex quoting:

```bash
declare -a flags
flags=(--foo --bar='baz')
flags+=(--greeting="Hello ${name}")
mybinary "${flags[@]}"
```

### Return Value Checking

- Always check return values with `if` or by inspecting `$?`.
- Use the `PIPESTATUS` array to check exit codes of individual pipeline stages.

---

## Prohibited Patterns

| Prohibited | Use instead |
|-----------|-------------|
| Backticks `` `cmd` `` | `$(cmd)` |
| `expr` for arithmetic | `$(( expression ))` |
| `let` for arithmetic | `$(( expression ))` |
| `$[ expression ]` for arithmetic | `$(( expression ))` |
| `eval` for variable assignment | Direct assignment |
| Aliases in scripts | Functions |
| `[` (single bracket) for tests | `[[` (double bracket) |
| Unquoted variable expansion | `"${var}"` |
| `$*` for argument passing | `"$@"` |
| SUID/SGID on scripts | Use `sudo` or capabilities |
| `*` glob expansion (bare) | `./*` prefix to avoid `-` filenames |
| `command | while read` | Process substitution `< <(command)` or `readarray` |

```bash
# Wrong
result=`command`
val=`expr $a + $b`
[ -f "$file" ]

# Correct
result=$(command)
val=$(( a + b ))
[[ -f "${file}" ]]
```
