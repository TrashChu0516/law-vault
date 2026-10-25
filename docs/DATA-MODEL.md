# Data model

## 1. Principles

1. **One file, one entity.** One case, one statute, one topic, one answer. Identity is the filename.
2. **The filename is the citation.** Case notes are named `Party v Party [Year] SGHC 123.md`, so a wikilink resolves to the right case and sorts chronologically.
3. **YAML frontmatter is the schema.** Everything a query needs lives above the first `---`. Prose lives below it.
4. **Links, not copies.** A case is referenced as `[[Case Name]]`, never retyped. The graph is the index.
5. **Tags are a controlled vocabulary.** New tags require a new outline section; they are not invented per note.

## 2. Case notes

### Schema

| Field | Type | Required | Purpose |
|---|---|---|---|
| `case_name` | string | ✔ | Display name; mirrors the filename |
| `citation` | string | ✔ | Neutral citation, e.g. `[2014] SGHC 71` |
| `reported` | string | | Law report citation, e.g. `[2014] 2 SLR 1398` |
| `court` | string | ✔ | Court and level |
| `module` | string | ✔ | `CL1`, `CRL`, `LRW`, `SLS` |
| `week` | number | ✔ | Teaching week — drives folder placement and seminar queries |
| `jurisdiction` | string | ✔ | `SG`, `UK`, … |
| `decision_date` | date | ✔ | Date of judgment |
| `coram` | string | ✔ | Judge(s) |
| `topic` | list | ✔ | Coarse doctrine area |
| `tags` | list | ✔ | Fine-grained doctrine tags (see §5) |
| `note_up` | string | | Followed / distinguished / overruled counts |
| `importance` | number | | 1–5, drives revision priority |
| `source` | URL | ✔ | Where the text came from |
| `status` | enum | ✔ | `fulltext`, `summary`, `stub` |
| `type` | string | ✔ | Always `case` |

### Example

```yaml
---
case_name: "Speedo Motoring Pte Ltd v Ong Gek Sing"
citation: "[2014] SGHC 71"
reported: "[2014] 2 SLR 1398"
court: "High Court"
module: "CL1"
week: 7
jurisdiction: "SG"
decision_date: "14 April 2014"
coram: "George Wei JC"
topic: ["terms"]
tags: ["cl1/cpfta", "cl1/cpfta/remedies"]
note_up: "0 followed · 0 distinguished · 0 overruled · 0 not followed · 1 referred"
importance: 4
source: "https://www.lawnet.com/research"
type: case
status: fulltext
---
```

### Body structure

```markdown
## In this note          ← navigation
## Exam version          ← one IRAC-ready paragraph, written last
## Key principles        ← ratio bank; bullets tagged #key-principle/<doctrine>
## Case brief            ← headnote / ratio / facts / reasoning / obiter
## Pro Max               ← the deep dive; reading this ≈ reading the case
## Judgment              ← source text, unmodified
```

The `## Judgment` section is immutable. `verify_brief.py` checks it byte-for-byte, so a brief can only be added above it.

## 3. Statute notes

| Field | Purpose |
|---|---|
| `statute` | Full title and revision, e.g. `Unfair Contract Terms Act 1977 (Cap 396, 2020 Rev Ed)` |
| `module` | Owning module |
| `jurisdiction` | `SG` |
| `retrieved` | Date pulled from SSO |
| `source` | Exact SSO URL |
| `note` | Verification caveat and known corrections |
| `tags` | `[cl1/ucta]` |

```yaml
---
type: statute
module: CL1
jurisdiction: SG
statute: "Unfair Contract Terms Act 1977 (Cap 396, 2020 Rev Ed)"
retrieved: "2026-09-28"
source: "https://sso.agc.gov.sg/Act/UCTA1977 (current version as at 28 Sep 2026)"
note: "Extracted from SSO during the Week 7 build. Re-verify before relying on it for assessed work."
tags: [cl1/ucta]
---
```

The `note` field is not decoration. If an earlier transcription mislabelled a section, the correction is recorded there so the error is not silently reintroduced.

## 4. Other note types

| Template | Type | Key fields |
|---|---|---|
| `t-topic-note.md` | `topic` | `module`, `topic`, `source`, `status` |
| `t-lego-block.md` | `block` | `block_id`, `module`, `topic`, `type` (rule/test/framework/definition/exception/distinction), `authority_type`, `primary_authority` |
| `t-irac-answer.md` | `irac-answer` | `module`, `question`, `word_limit`, `date`, `status` |
| `t-essay-outline.md` | `essay-outline` | `module`, `question`, `word_limit`, `date`, `status` |

The LEGO block is the atomic unit: a rule, its authority, and a ready-to-type IRAC insert. Exam summaries are assembled from blocks; grill drills rehearse them.

## 5. Tag taxonomy

Three layers, two owners:

| Layer | Where | Example | Owner |
|---|---|---|---|
| Properties | Frontmatter | `module: CL1`, `week: 7`, `court: High Court` | Mechanical |
| Doctrine tags | Frontmatter `tags:` | `cl1/ucta/s3`, `cl1/formation/objective-approach` | Controlled vocabulary |
| Ratio / obiter | Inline bullet suffix | `#key-principle/ucta/s3`, `#obiter` | Human judgment |

Rules:

- Nested with `/`: module → area → outline section.
- Every case carries its area tag **and** its most specific outline-section tag.
- A landmark case cited across seminars carries multiple tags.
- Inline `#key-principle/...` tags feed the Master Legal Index automatically; `#obiter` feeds a separate table.
- Unknown tags are surfaced by the librarian query, not silently accepted.

## 6. The query layer

There is no database. Dataview queries over frontmatter are the database.

**Master index — every ratio, rolled up by doctrine:**

```dataview
TABLE WITHOUT ID
  file.link AS "Case",
  replace(join(L.tags, ", "), "key-principle/", "") AS "Doctrine",
  L.text AS "Ratio"
FROM "cases"
FLATTEN file.lists AS L
WHERE contains(join(L.tags, " "), "key-principle")
SORT file.name ASC
```

**Librarian — anything that slipped through:**

```dataview
TABLE WITHOUT ID file.link AS "Case"
FROM "cases"
WHERE type = "case" AND (!tags OR length(tags) = 0)
```

The same pattern answers "all Court of Appeal cases on formation, newest first", "all cases not cited in any summary", and "all statute notes not verified this month". Adding a field to the schema adds a query; no migration required.

## 7. Schema evolution

- **Additive by default.** New optional fields do not break old notes.
- **Rename with a script.** When a field is renamed, `case_note_tools.py fixmeta` repairs the batch; the change is one commit.
- **Record corrections in the note.** A wrong section number is corrected in place, and the correction is logged in the `note` field — the audit trail matters more than a clean-looking file.
- **No silent edits to judgments.** The `## Judgment` section is source text. Corrections go in the brief, above it.
