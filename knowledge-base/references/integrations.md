# Integration with Other Skills

All integrations are **gated on `kb_path` being configured** — when no KB exists, the other skills behave exactly as before.

| Skill | When it fires | What it does |
|-------|---------------|--------------|
| `brainstorm` | Step 1 (Explore context) | Reads the current repo's `wiki/<repo>/index.md` — which lists `Helpers` and `Patterns` alongside the existing sections — plus relevant `wiki/<repo>/rules/` pages before the first Socratic question. Drills into specific helper/pattern pages on demand as the design conversation reveals what's relevant. |
| `brainstorm` | Step 9 (Save plan) | Default plan path becomes `<kb_path>/plans/<ticket-or-branch>.md`. Frontmatter records `repos: [...]` so cross-repo plans are findable from any participating repo. |
| `analyze-code` | Step 1 (Frame) | Reads this repo's `wiki/<repo>/dependencies/`, `events/`, `rules/`, and the plan at `<kb_path>/plans/<current-branch>.md` if one exists. Reads the `Helpers` and `Patterns` sections of `wiki/<repo>/index.md`; drills into specific pages on demand when the code under review suggests overlap. May follow cross-repo `[[wiki-links]]` if relevant. Wiki↔code disagreements become findings — including **"reinvents existing helper"** and **"violates documented pattern"**. |
| `using-software-specialists` | Phase A (consult, mandatory before producing code) | Specialist reads `wiki/<repo>/index.md` including the `Helpers` and `Patterns` sections, then drills into relevant pages. Uses existing helpers and follows canonical patterns instead of inventing divergent shapes. |
| `using-software-specialists` | Phase B (post-write, before declaring completion) | If any new function meets the helpers inclusion bar (reusable, non-private), the specialist updates `helpers/<category>.md` autonomously via the Update workflow. Pattern *creation* is **not** in scope for the specialist — patterns are added only via Ingest. |

## Cross-references between pages (load-bearing for the integrations)

Three link types the skill maintains:

- **Entity ↔ plan.** A plan's frontmatter lists touched entities; each entity page's *"Related plans"* section links back to plans that modified it.
- **Event producer ↔ consumer.** Each event page lists `producer:` and `consumers:` as `[[wiki-links]]`. Both sides have the link, so following either direction works.
- **Rule ↔ entity/endpoint.** A business rule like *"orders cancellable within 30 min"* links to the entity and endpoint where it's enforced. `analyze-code` can trace rule → enforcement points and flag missing enforcement as a finding.
