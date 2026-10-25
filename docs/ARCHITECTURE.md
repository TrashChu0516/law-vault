# Architecture

## 1. The shape of the system

Four layers, each with one job:

| Layer | Job | Lives in | Is it generative? |
|---|---|---|---|
| **Source** | Authentic text: judgments, statutes, textbook chapters, outlines | Private corpus (PDF/HTML) | No |
| **Ingest** | Convert source into faithful, addressable Markdown | `_tools/*.py` | No — deterministic |
| **Vault** | Retrieve, link, query | `cases/`, `modules/`, `Notes/` | No |
| **Skills** | Decide what to write, how to mark, what to verify | `.opencode/skills/` | Yes — governed by spec |

The separation is deliberate. Anything that can be done deterministically is done outside the model, because models drift and scripts do not. The model is only trusted with judgment: synthesis, issue-spotting, application, marking.

## 2. Folder layout

```
contract-law-notes/
├── AGENTS.md                  ← constitution: sourcing + citation + verification rules
├── .opencode/skills/          ← 15 skill specs (one folder per skill)
├── cases/                     ← one note per case, grouped module/week
│   ├── CASE_INDEX.md          ← Dataview index over every case
│   └── CL1_Contract/wk_7/…
├── modules/                   ← module-level material
│   ├── CL1_Contract/Statutes/ ← verified statute banks (SSO)
│   └── */Summaries/           ← generated exam summaries (tracked)
├── Notes/                     ← personal topic notes, by module
├── Textbook/                  ← copyrighted PDFs only (private, ignored)
├── Slides/                    ← lecture slides (private)
├── _course_outlines/          ← seminar outlines (private)
├── Grill/                     ← CL1_Contract/ · CRL_Criminal/ · _shared/
├── _templates/                ← six note schemas
├── _tools/                    ← converters, verifiers, architecture docs
├── _integrity/                ← citation guide, verification checklist, plagiarism policy
└── _research/                 ← research hub, case-finding pipeline
```

`Textbook/`, `Slides/` and the AI chat data are git-ignored. The repository tracks text only.

## 3. Why one vault, not a database

The obvious alternative is a relational database or a SaaS notes app. I rejected both.

| Option | Verdict | Reason |
|---|---|---|
| Separate case database | Rejected | Breaks `[[wikilinks]]`. A case cannot link to its doctrine block, statute and outline in one graph. |
| SaaS notes (Notion, Roam) | Rejected | No local files, no real diffs, no agent-readable format, export is lossy. |
| **One Markdown vault** | **Chosen** | Single source of truth. Case → doctrine → statute → outline are one graph. Git gives history and review. Any agent can read it with `grep`. |

The cost is that Markdown has no foreign keys. The compensation is a strict frontmatter schema (see [DATA-MODEL.md](DATA-MODEL.md)) and Dataview as the query engine.

## 4. The graph

Every artefact is a node; every `[[wikilink]]` is an edge.

```
seminar outline ──► case note ──► doctrine block ──► exam summary
                        │                │
                        ▼                ▼
                   statute note ◄─── trigger bank
```

Practical consequences:

- A case note is written once and reused by the summary pipeline, the grill pipeline and the Master Legal Index.
- A statute note is cited by section, not by title, so an exam answer can link to `[[UCTA 1977#s 3]]`.
- The Master Legal Index (`_tools/Master_Legal_Index.md`) is a Dataview query, not a maintained list: any bullet tagged `#key-principle/<doctrine>` rolls up automatically.

## 5. Anatomy of a skill

A `SKILL.md` is a spec, not a prompt. The frontmatter is machine-readable; the body is a procedure a reviewer can audit.

```yaml
---
name: exam-summary-pipeline
description: "When to trigger this skill…"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
argument-hint: "[week number or chapter]"
---
```

The body follows the same sections every time:

1. **Activation** — the phrases that trigger it, and what to read first.
2. **Materials map** — which sources exist, where they are, what to do when one is missing.
3. **Procedure** — ordered steps, with the reasoning behind each.
4. **Output contract** — filename, structure, required sections.
5. **Verification** — the checks that must pass before the output is shown.
6. **Failure modes** — what to do instead of guessing.

That structure is what makes the system improvable: when an output is weak, the fix goes into the spec, not into a one-off chat.

## 6. The verification layer

Fabrication is the failure mode that matters in law. The system makes it detectable rather than trusting the model to avoid it:

| Control | Where | What it catches |
|---|---|---|
| Cardinal rules | `AGENTS.md` | Unsourced claims, guessing when material is missing |
| Case-note schema | `_templates/t-case-note.md` | Missing citation, court, date, coram |
| Citation verifier | `_tools/verify_case_note_citations.py` | Quoted passages that are not in the judgment; paragraph numbers that do not exist |
| Brief verifier | `_tools/verify_brief.py` | Brief propositions with no corresponding judgment paragraph |
| Librarian | `_tools/librarian.md` | Cases with no tags, no module, no citation — surfaced as a Dataview table |
| Integrity guides | `_integrity/` | Citation format, pre-submission checklist, plagiarism boundaries |

The rule is not "the model never makes mistakes". The rule is "a mistake should be findable before it reaches an exam answer".

## 7. Tradeoffs and what I would change

- **Markdown vs schema validation.** Frontmatter is conventional, not enforced. A JSON Schema check in CI would catch malformed notes earlier.
- **Per-week folders vs topic folders.** Weeks match the course and make seminar prep fast; they fight cross-cutting doctrine. The tag layer compensates, but a topic view is still a Dataview query rather than a folder.
- **One vault vs many.** One vault keeps the graph intact but couples modules. A shared `_templates/` and `_tools/` is the payoff; the cost is that a change to the schema touches every module.
- **Agent autonomy.** The skills can write files. In practice every write is reviewed, and the high-stakes outputs (exam summaries) are checked against the source before use. Tighter approval gates would be the next step if this were a team repo.
