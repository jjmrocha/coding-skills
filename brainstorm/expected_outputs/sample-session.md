# Sample Brainstorm Session

This is an example of a well-executed brainstorm session demonstrating the expected behavior.

---

**User:** I want to build something to help me track my expenses.

---

**Agent (Step 1 — Explore context):**
No existing project files found. Proceeding.

**Agent (Step 2 — Assess scope):**
Single-system scope. No decomposition needed.

**Agent (Step 3 — Clarifying questions, one at a time):**

> "What problem does this solve — is it about understanding where your money goes, staying within a budget, or something else?"

**User:** I keep overspending on dining out and I never realize it until my bank statement arrives.

---

> "Should this connect to your bank or credit card automatically, or are you comfortable logging expenses manually?"

**User:** Manual is fine — I don't want to deal with bank integrations.

---

> "What does a successful outcome look like — would you want a weekly summary, an alert when you're close to a limit, or just a way to review history?"

**User:** A weekly summary and an alert if I've already hit 80% of my dining budget for the month.

---

**Agent (Step 4 — Propose 2-3 approaches):**

Three options, all fitting manual entry and a budget alert:

**A) CLI tool with local CSV (recommended)** — simple, no dependencies, data is yours, easy to query. Weekly summary via a report command.

**B) Local web app with SQLite** — nicer UI, supports categories and charts. More setup required.

**C) Shared spreadsheet (Google Sheets/Notion)** — familiar UI, no code needed. Less automation for alerts.

I recommend **A** — it matches the scope and you can always migrate data later.

---

**User:** A sounds good.

---

**Agent (Step 5 — Design, section by section):**

> "**Architecture:** A single CLI script. Commands: `add <amount> <category> [note]`, `summary [--month]`, `budget set <category> <limit>`. Data stored in `~/.expenses/data.csv`. Does this structure look right?"

**User:** Yes, that works.

> "**Alert logic:** On each `add` command, if the category total for the current month exceeds 80% of its configured budget, print a warning. Does that match what you had in mind?"

**User:** Perfect.

---

**Agent (Step 6 — Write spec):**

Spec written to `docs/specs/2026-01-15-expense-tracker.md`.

---

**Agent (Step 7 — Self-review):**

Checked: no placeholders, architecture consistent with features, scope fits one implementation plan.

---

**Agent (Step 8 — User review gate):**

> "Spec committed. Please review `docs/specs/2026-01-15-expense-tracker.md` before we write the implementation plan."
