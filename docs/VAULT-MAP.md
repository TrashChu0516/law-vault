# Vault map

Folder-level view of the private vault. File titles are withheld; the shape is not.

```
contract-law-notes/
├── AGENTS.md                       operating rules for every agent session
├── .opencode/skills/               15 skill folders
├── cases/                          237 Markdown notes + 23 judgment PDFs
│   ├── CASE_INDEX.md               Dataview index over every case
│   ├── CL1_Contract/               175 notes · wk_1, 2, 3, 4, 7, 9, 10
│   ├── CRL_Criminal/               57 notes · wk_1, 3, 5, 6, 7, 9, 11
│   ├── LRW1/                       3 notes
│   └── SLS/LAW108_Week2_Readings
├── modules/
│   ├── CL1_Contract/
│   │   ├── Statutes/               4 statute banks (CPFTA, UCTA, ETA, Evidence Act)
│   │   └── Summaries/              8 exam summaries (tracked)
│   ├── CRL_Criminal/
│   │   ├── Summaries/              5 exam summaries (tracked)
│   │   └── Interpretations/
│   │   ├── Criminal Procedure Code 2010
│   │   ├── Misuse of Drugs Act
│   │   └── Penal Code 1871
│   ├── LRW/
│   └── SLS/Statutes/
├── Notes/                          Contract · Crim · LRW · SLS
├── Textbook/                       private, git-ignored
│   ├── CL1_Contract_Law/Phang/     chapter PDFs only
│   ├── CL1_Contract_Law/case_book/
│   ├── CRL_Criminal_Law/
│   └── LRW1/
├── Slides/                         private · Contract1 · Crim
├── _course_outlines/               private · CL1 · CRL · SLS
├── Grill/
│   ├── CL1_Contract/               rubric, trigger bank, error ledger, attempts
│   ├── CRL_Criminal/               rubric, checklist, mastery ledger, attempts
│   └── _shared/                    The ELEMENTS of STYLE (cross-module)
├── _templates/                     6 note schemas
├── _tools/                         15 converters, verifiers and system docs
├── _integrity/                     3 guides (citation, verification, plagiarism)
└── _research/                      2 docs (research hub, case-finding pipeline)
```

## Scale by module

| Module | Week folders | Case notes | Statute banks |
|---|---|---|---|
| Contract Law (CL1) | 7 | 175 | 4 |
| Criminal Law (CRL) | 7 | 57 | 3 (Interpretations) |
| Legal Research & Writing (LRW) | 1 | 3 | — |
| Singapore Legal System (SLS) | 1 | — | 1 |

The week folders track the course, not the doctrine. The tag layer is what makes cross-cutting queries possible; see [DATA-MODEL.md](DATA-MODEL.md) §5.

## Where the leverage is

- **`cases/`** — the retrieval corpus. 235 case notes are the reason the agent can cite instead of recall.
- **`modules/*/Summaries/`** — the generated summaries: one mini-textbook per chapter, the highest-value output of the system.
- **`Grill/`** — the performance layer. Notes are input; this is where they become marks.
