# Scope and exclusions

This repository is a **sanitised showcase**, not the working vault. It exists so the system can be reviewed without publishing material that is not mine to publish.

## What is included

| Category | Files | Why it is safe to publish |
|---|---|---|
| Agent skill specs | 15 `SKILL.md` files | My own prose and procedure. Private paths and third-party names removed. |
| Templates | 6 note schemas | My own design. |
| Tooling | 10 Python converters/verifiers + 5 architecture docs | My own code, MIT-licensed. |
| Rubrics and style standard | 3 documents | My own distillation of publicly described marking criteria. |
| Integrity guides | 3 documents | My own policy documents. |
| Sample case note | 1 note (*Speedo Motoring v Ong Gek Sing*) | The judgment is a public court document; the brief and structure are my own work. |
| Sample statute note | 1 note (UCTA 1977) | Singapore legislation is published on Singapore Statutes Online. |
| Skeleton folders | `cases/`, `modules/`, `Notes/`, `Textbook/`, `Slides/`, `_course_outlines/` | Structure only, with a README in each. |

## What is excluded, and why

| Excluded | Reason |
|---|---|
| **Textbook PDFs** (`Textbook/`) | Publisher copyright (SAL Textbook / Academy Publishing). They were never in git, even in the private repo — `.gitignore` keeps them out. |
| **Lecture slides and seminar outlines** (`Slides/`, `_course_outlines/`) | The professor's teaching material, not mine to redistribute. |
| **Past-year papers** | Circulated within the cohort; republishing them publicly is not appropriate. The skills describe the *method* for using them, not their contents. |
| **The full case library** (237 notes, 23 judgment PDFs) | Volume, plus editorial headnotes that may carry publisher rights. One sample note shows the schema and quality bar. |
| **Marked attempts and the error ledger** | Personal performance data. The *template* is included; the entries are not. |
| **AI chat data and API credentials** (`copilot/`, `.copilot/`, `.env`) | Secrets and private AI chat data. These were git-ignored from day one. |
| **Obsidian plugin state and caches** | Machine-specific noise; it would not help a reviewer. |

The private repository has tracked **text only** since its first commit. The split is enforced by `.gitignore`, not by remembering to exclude things:

```gitignore
Textbook/
Slides/
copilot/
.copilot/
copilot_skills/
.claude/
.opencode/
.agents/
.obsidian/plugins/copilot/
.smart-env/
.trash/
```

## Copyright notes

- **Singapore judgments** are public court documents, but the editorial headnotes and catchwords on commercial databases may attract separate rights. The sample note reproduces the judgment structure, not a proprietary headnote.
- **Textbook extracts** are quoted in the private summaries under fair-dealing-style limits (short quotations for study), not reproduced wholesale. No textbook text appears in this repo.
- **Statutes** are reproduced from Singapore Statutes Online with the retrieval date and URL recorded in the frontmatter.
- If you believe something here should not be public, contact me and I will remove it.

## Academic integrity

This is a study system, not an answer bank.

- The grill pipeline drills **past** papers; it does not produce answers to live assessments.
- Every output is checked against primary sources before it is relied on.
- The `_integrity/ANTI_PLAGIARISM_GUIDE.md` sets the boundary: the assistant may help with research, structure and critique; the submitted work must be mine.

## What a reviewer can and cannot verify here

**Can verify:** the skill format, the prompt/spec engineering, the Python converters, the schemas, the verification logic, the rubric design, and the writing standard.

**Cannot verify:** the size and quality of the private corpus, or the exam outcomes it produced. Those are demonstrated in a live walkthrough on request.

## How this public copy was produced

1. **Allowlist copy** — explicit file list, not `git clone` and delete. Nothing excluded can slip through.
2. **Fresh history** — `git init` and a single commit. The private repo's 142 commits are not mirrored, so no deleted file, old path or past secret can be recovered from history.
3. **Scrub pass** — absolute paths, personal names of third parties, and private corpus locations removed.
4. **Secret scan** — regex scan for API keys, tokens, emails and phone numbers before the first push.
5. **Review** — the diff is read before anything is pushed.

It is deliberately **not** a GitHub fork. A fork of a private repository cannot be made public, and a mirror would carry the history that the allowlist is designed to avoid.
