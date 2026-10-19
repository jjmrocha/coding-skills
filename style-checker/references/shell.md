# Google Shell Style Guide — Formatting & Naming

Source: https://google.github.io/styleguide/shellguide.html

## Naming Conventions

| Identifier | Style | Example |
|-----------|-------|---------|
| Function | `lowercase_with_underscores` | `my_function` |
| Packaged function (with namespace) | `package::function_name` | `mypackage::my_func` |
| Variable (local) | `lowercase_with_underscores` | `my_variable` |
| Constant / environment variable | `UPPERCASE_WITH_UNDERSCORES` | `MY_CONSTANT`, `PATH` |
| Source file (library) | lowercase, underscores optional, `.sh` | `my_lib.sh`, `mylib.sh` |
| Source file (executable) | lowercase, underscores optional, `.sh` or no extension | `make_template`, `maketemplate.sh` |

### Naming Rules
- **No camelCase or PascalCase** in shell scripts. **No dashes** in file names (`make-template` is wrong).
- **Libraries must have `.sh` extension** and should not be executable.
- Executables: `.sh` or no extension. Prefer no extension when installed directly on the user's `PATH`, and `.sh` when a build rule renames the file.
- Loop variables are named after what is looped over: `for zone in "${zones[@]}"`.
- Constants and exported variables: declared at the **top of the file**. `readonly` and `export` are recommended over the equivalent `declare` forms. A constant set at runtime or in a conditional is made `readonly` immediately afterwards.
- Namespaced function names (`pkg::func`) do not work well in interactive contexts such as auto-completion; avoid them there.
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

- **2 spaces** per level. **No tabs.** (Exception: `<<-` here-document bodies may use tabs.) In existing files, keep the existing indentation.
- Blank lines between blocks improve readability.
- **80 characters** maximum line length.
- Long literal strings: use here-documents or embedded newlines.
- Words longer than 80 characters that cannot be split (file paths, URLs) are allowed, preferably on their own line or in a variable. The rest of such a line is still wrapped normally.

---

## Shell and Shebang

- **Bash is the only shell** permitted for executables, unless the environment forces plain Bourne shell. POSIX compatibility is not a goal.
- **Executables must start with** `#!/bin/bash` and minimal flags. Set shell options with `set` in the script, so `bash script_name` still works.
- Shell is for small utilities and wrappers. A script over 100 lines, or with complex control flow, should be rewritten in a structured language. Report this as Low.
- SUID and SGID are forbidden on shell scripts.
- All error messages go to `STDERR`.

```bash
#!/bin/bash
#
# Description of script.
```

---

## Pipelines

- Keep on **one line** if it fits.
- Multi-line: one segment per line, pipe symbol at the start of the **new line**, 2-space continuation indent, and `\` used consistently for continuation.
- The same applies to chains joined with `||` and `&&`.
- A comment goes before the whole pipeline.

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
- This applies to `if`, `for`, `while`, `until`, and `select`.
- `else` on its **own line**.
- Closing `fi`, `done`: on their own line, vertically aligned with the opening statement.
- Recommended: include `in "$@"` explicitly in for loops over arguments.
- Inside a function, declare the loop variable `local`.

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
- Patterns are not preceded by an open parenthesis (`(a)` is wrong) and usually need no quotes.
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
- **No space** between function name and `()`. Parentheses are required.
- **Function location**: all functions together near the top, just below constants. Only includes, `set` statements, and constants may come before them. No executable code between functions.
- A `main` function is **required** once a script has at least one other function. It is the bottom-most function, and `main "$@"` is the last non-comment line. Short linear scripts need no `main`.

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
- **Always quote** strings containing variables, command substitutions (even when an integer is expected), spaces, or shell meta-characters, unless careful unquoted expansion is required.
- Quoting the integer specials `$?`, `$#`, `$$`, `$!` is optional. Never quote literal integers (`value=32`). Prefer quoting words (`readonly USE_INTEGER='true'`).
- Prefer `"${var}"` over `"$var"` (explicit braces). Braces are not quoting: double quotes are still needed.
- Single quotes: for literal strings with no substitution.
- Use `"$@"` (not `"$*"`) for passing arguments. `$*` is fine for joining arguments into a message.

### Variable Expansion Precedence

These are strongly recommended, not mandatory. Report violations as Low unless the variable is unquoted.

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
- For **empty strings**: use `-z` and `-n` rather than filler characters like `x`, and rather than `[[ "${var}" ]]` alone.
- `<` and `>` inside `[[ ... ]]` compare **lexicographically**. For numbers use `(( ... ))` (preferred) or `-lt` / `-gt`.
- Do not quote the right-hand side of `=~` when it is a regex pattern.

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

- **File header**: required at top — brief overview of the file's contents. Copyright and author are optional.
- **Function comments**: required for any function that is not both obvious and short, and for **every** function in a library. They contain:
  - A description of the function
  - Globals: used and modified
  - Arguments
  - Outputs (stdout/stderr)
  - Returns: values other than the exit status of the last command
- Comment tricky, non-obvious, or important parts.
- `TODO` format: `# TODO(username): description` — the name, e-mail, or other identifier of the person with the best context.

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
- Use the `PIPESTATUS` array to check exit codes of individual pipeline stages. Copy it to another variable immediately if you need it later.

### Builtins over External Commands

- Prefer shell builtins and parameter expansion over external processes: `"${string/#foo/bar}"` over `echo | sed`, `$(( X + Y ))` over `expr`, `=~` with `BASH_REMATCH` over `sed` extraction.

### Arithmetic

- Inside `$(( ... ))`, omit `$` and braces on variables (recommended).
- Be careful with `(( ... ))` as a standalone statement under `set -e`: an expression that evaluates to zero exits the shell (`(( i++ ))` with `i=0`).

### Tools

- Running ShellCheck is recommended for all scripts.

---

## Prohibited Patterns

| Prohibited | Use instead |
|-----------|-------------|
| Backticks `` `cmd` `` | `$(cmd)` |
| `expr` for arithmetic | `$(( expression ))` |
| `let` for arithmetic | `$(( expression ))` |
| `$[ expression ]` for arithmetic | `$(( expression ))` |
| `eval` (avoid in general) | Direct assignment, arrays |
| A single string holding several command arguments | An array expanded as `"${flags[@]}"` |
| Unquoted `$(cmd)` in an array assignment (`files=($(ls))`) | `readarray -t files < <(cmd)` |
| `for x in $(cmd)` when output may contain spaces | `while read` or `readarray` |
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
