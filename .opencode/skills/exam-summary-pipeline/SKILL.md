---
name: exam-summary-pipeline
description: "Build exam-ready mini-textbook summaries for CL1 Contract Law weeks — condensed on the Phang (SAL Textbook) chapter, with copy-paste I/R/A pre-writes, every seminar-outline question answered, hypothetical answer skeletons, and a case ledger. Use when the user asks for an exam summary / cheatsheet / week summary for contract law, to continue the exam-summary series (Week 7 done; Weeks 1–4 to do), or to produce revision notes for a contract chapter. Extensible to criminal law later."
metadata:
  copilot-enabled-agents: claude, codex, opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
argument-hint: "[week number or chapter, e.g. 'Week 3' or 'Chapter 4']"
---

# Exam-Summary Pipeline — agent-facing spec

You are producing a **weekly exam summary** ("mini-textbook / cheatsheet") for the user's CL1 Contract Law course. This spec is written for you, the agent. Follow it in full. The user's overriding statement of purpose: *"everyone can write long, but only the good ones know what is necessary for the exam — the goal is to score marks."* Optimise for marks, not for completeness.

## 0. Cardinal rules (non-negotiable)

1. **Never fabricate.** No citation, pinpoint, section number, textbook paragraph, quote or case fact may be produced from memory or inference. Read the source, or mark `[CHECK]` and flag it in your reply. Law is semantic: one reversed rule, wrong party, wrong test, or wrong section number can fail the user's paper. Fidelity beats fluency.
2. **Start from what we already have.** The vault is the primary source: the Phang textbook PDFs, the seminar outlines, the user's own notes, the case notes (many with full briefs), and the verified statutes saved in `modules/CL1_Contract/Statutes/`. Exhaust these before anything else.
3. **Outside sources only when the vault falls short.** In order of preference: **LawNet** (lawnet.com — full Singapore judgments with pinpoints and note-up), **Singapore Statutes Online** (sso.agc.gov.sg — statutes), **Lexis Advance** (commentary). Anything taken from outside must be verified at its source and cited like everything else.
4. **Verify, verify, verify; cite everything.** Every legal proposition carries a citation — case `[n]`, textbook `0X.YYY`, or statutory section. A claim without a citation is not allowed in the output.
5. **Ask, don't guess, for missing materials.** If a needed textbook chapter, statute, or case text is absent from the vault and cannot be verified online, stop and ask the user. Never reconstruct from memory.
6. **Self-contained output.** The summary must work standalone — a reader with the Week 7 exemplar plus the case notes needs nothing else, and no prior chat context.

## 1. Activation

Trigger phrases from the user: "Week N exam summary", "exam summary for Week N", "cheatsheet for [chapter]", "continue the exam summary series", "mini-textbook for [chapter]", "retro-do Week N". Also run this spec if the user references this skill by name.

Before writing anything: read this entire skill, then the current-week materials (below). If resuming in a fresh session, do **not** assume context from previous chats — rebuild it from the vault.

## 2. Deliverable

One markdown file per week/chapter, saved to `modules/CL1_Contract/Summaries/` named like the chapter: `Chapter N <Title> — Exam Summary.md`. (Week 7's is the exemplar: `Chapter 7 Regulation of Terms — Exam Summary.md`.) Optionally, if the user asks, produce the print-ready PDF via the pipeline in §11.3 and update `cases/CL1_Contract/CL1_MOC.md` cross-links.

## 3. Materials map (check what exists before scoping)

| Source | Location | Notes |
|---|---|---|
| SAL Textbook (Phang) chapters | `Textbook/CL1_Contract_Law/Phang/` | **Present: Ch 3 (Offer & Acceptance), Ch 4 (Consideration), Ch 6 (Express & Implied Terms), Ch 7 (Regulation of Terms).** Missing chapters → ask the user for the PDF. PDFs must be text-extracted (§11.1). |
| Casebooks (Burrows / McKendrick) | `Textbook/CL1_Contract_Law/case_book/` | For English "casebook placeholder" cases (no full text in vault). Cite such cases by name only (no paragraph pinpoints). |
| Seminar outlines | `_course_outlines/CL1_Contract_Law/` | Week 01, 2, 3, 4, 7 present. These define the examinable scope AND contain the professor's questions. **Weeks 5–6 are presentation weeks — skip if asked.** |
| Case notes | `cases/CL1_Contract/wk_N/` | wk_1 (30 files), wk_2 (22), wk_3 (31), wk_4 (40), wk_7 (14, fully briefed). See §9 for the house brief format; wk_1–4 are mostly raw judgments, some with eLitigation artifacts. |
| User's own notes | `Notes/Contract/ContN.md` | Read the relevant week. Capture the professor's emphasis and the user's framing; flag conflicts rather than silently overriding. (Cont7 is a stub; Cont4 is rich.) |
| Verified statutes | `modules/CL1_Contract/Statutes/` | UCTA (Cap 396, 2020 Rev Ed), CPFTA (2020 Rev Ed), Electronic Transactions Act 2010. Root also has `Sales of Goods Act 1979.md`. For other statutes (e.g., Evidence Act ss 93–100), fetch from SSO and **save a verified copy here** (§11.2). |
| Conventions | `_tools/TAG_TAXONOMY.md`, `cases/CL1_Contract/CL1_MOC.md`, `_templates/` | Tags and cross-linking. |
| The exemplar | `modules/CL1_Contract/Summaries/Chapter 7 Regulation of Terms — Exam Summary.md` | The standard to match. Know its anatomy (§4). |

## 4. The exemplar's anatomy (match this structure)

- **Frontmatter** — `type: summary`, module/week/topic, `sources:` string listing exactly what was used, tags from the taxonomy.
- **Intro block** — what this is; citation conventions; companion materials.
- **§0 The three-step method** — the analytical flow for every answer + an opening pre-write.
- **Parts A–D** — the condensed textbook skeleton (mirroring Phang's chapter structure, with `07.xxx`-style paragraph refs), each doctrine followed by **pre-writes**.
- **Part D** — answers to *every* question in the week's seminar outline, numbered to match the outline.
- **Part E** — condensed answer skeletons for each hypothetical in the outline (issue → rule → application → conclusion, ~120–180 words each).
- **Appendix** — case ledger table (one line per case + importance stars) + an exam-day checklist.

**Pre-write syntax** (the core value — sentences the user can paste into IRAC as I/R/A):

> **R — \<doctrine\> (pre-write):** "\<one or two sentences of rule, in exam register\>" (citations)
>
> **A — \<hook\>:** "\<how to deploy it on facts\>" (citations)

Every pre-write ends with citations: case `[n]` pinpoints, `Phang 0X.YYY`, statutory sections. Keep each ≤ 60 words.

## 5. Length control (do not exceed)

Target **5,500–7,000 words** (≈ 9–12 printed pages A4 at 10 pt). Hard cap ~7,500 words. Budget:

| Section | Budget |
|---|---|
| Intro + method | ~200 words |
| Parts A–C (skeleton + pre-writes) | ~3,500 words total |
| Part D (seminar Q&A) | ~800 words (1–3 sentences per question, each cited) |
| Part E (hypotheticals) | ~600 words total |
| Appendix (ledger + checklist) | ~500 words |

Trim rules: prefer tables over prose for comparisons; if a point repeats between the skeleton and the Q&A, state it once and cross-reference; cut anything that would not earn marks.

## 6. Workflow (run in order)

1. **Scope.** Read the week's seminar outline + the relevant ContN note. Build a scoping table: topic → prescribed cases → textbook paragraph span → statutes. Confirm every required chapter/case/statute is available; **ask the user about anything missing.**
2. **Textbook pass.** Extract and read the chapter (§11.1). Note paragraph numbers as you go; never cite an unread paragraph; when quoting, keep honesty (`…` for omissions, `[sic]` where needed).
3. **Case pass.** For each prescribed case:
   - If the case note is **briefed** (Exam version + Case brief + Pro Max): harvest the pre-writes and verified pinpoints; spot-check 2–3 pinpoints against the Judgment text.
   - If **raw** (most wk_1–4 files): read the judgment text; derive the exam-relevant ratio; record exact `[n]` pinpoints. Beware eLitigation abridgements/artifacts (e.g., `[num ]` strings).
   - If **casebook-only**: read the extract in the casebook PDF; cite by case name only.
4. **Statute pass.** Verify every provision you will cite against the saved text (or fetch + save). Build an **old → new numbering map** where the cases were decided under a prior edition (e.g., CPFTA: old s 12B = now s 14; old s 13 = now s 35). Cite current numbering, with the old number noted.
5. **Notes pass.** Read ContN; align terminology with the user's framing; flag conflicts explicitly rather than silently choosing.
6. **Draft** per §4 format with §5 budgets.
7. **Answer every seminar question** (§4 Part D) — do not skip or merge questions; number to match the outline.
8. **Hypotheticals** (§4 Part E) — full issue-spotting but condensed.
9. **Verification protocol** (§7) — mandatory gate. Do not present the file as finished until it passes.
10. **Output + close-out.** Save the file; if asked, generate the print PDF (§11.3) and/or update the MOC. Report: what was produced, length, sources used, and any `[CHECK]` items.

## 7. Verification protocol (mandatory final gate)

**Scripted checks:**
- Grep the draft: every pre-write contains ≥ 1 citation (`[`, `Phang`, `s ` scenario-dependent); no orphan claims.
- Count words; enforce §5.
- Random-sample **5 pinpoints** and trace each to the source text (grep the case file for the exact `[n]` and read it; or the statute text). If one fails, audit all.
- Statute cross-check: every section number you cited appears in the saved statute text with matching content.
- Numbering check: any case decided under an old edition — is the old→new mapping stated?

**Red-team questions (ask for every rule):**
- Direction: who bears the burden? Which test passes/fails? Does "cover" mean include or exclude? Who is liable to whom?
- Parties: consumer or business? Inter-party or third party? Supplier or principal?
- Effect: void, ineffective-for-that-liability, or subject to reasonableness? Severable?
- Register: is this ratio or obiter? Holding or dictum?
- Would the professor's model answer include this? Would it be wrong in any particular?

**If any check fails or remains uncertain:** fix from source; if unresolvable, mark `[CHECK]` inline and list it in your reply. Never bury uncertainty.

## 8. Pitfalls ledger (real mistakes from the Week 7 build — learn from these)

1. **"Cover" in the Canada Steamship test 2** = the words are wide enough to *catch within the exemption* (i.e., exclude), NOT that the clause creates liability. Getting this backwards inverts the whole analysis.
2. **Wilful-misconduct carve-out direction:** "not liable unless wilful misconduct" means liability is preserved ONLY above that line; everything below (negligence, even gross) is exempted. The carve-out's height tells you what the exemption catches.
3. **Exemption vs indemnity:** exemption = shield between the contracting parties ("don't sue me"); indemnity = third-party claims pass-through ("if you're sued, send me the bill"). An exemption clause cannot be confined to third-party claims (no privity); an indemnity is prima facie third-party oriented.
4. **Cumulative tests:** UCTA s 12(1)(a) and (b) are cumulative; a party can fail (a) or (b) independently. State which limb fails and why.
5. **UCTA s 6(4):** s 6 is NOT limited to business liability; s 7 IS (Phang 07.135). Don't over-generalise.
6. **CPFTA numbering drift:** cases cite old editions. Map every provision. Watch s 13(5) CPFTA (Part 4 provisions do not apply to Part 3) — verify against the printed Act when the reasoning depends on it.
7. **CPFTA "consumer" differs by Part:** Part 2 = an *individual* (s 2(1)); Part 3 = the UCTA "deals as consumer" test (s 13(2)).
8. **Prescribed limit changes:** $10k → $20k → **$30k** over time. Cite the current figure and note the case-era figure when discussing older cases.
9. **Schedule renumbering:** e.g., the price-benefit unfair practice cited in Freely as Sch 2 para 7 is now para 9. Verify against the printed Schedule; don't assert mappings you haven't checked.
10. **Pinpoint discipline:** a fact or quote must be grepped in the judgment text before you write its `[n]`. (In the Week 7 build, a Freely pinpoint was wrong on first draft — caught and fixed only by this check.)
11. **NOM clauses are evidential, not contractual** in Singapore: rebuttable presumption + estoppel; they do not cover rescission (Charles Lim [29]–[31], [56]–[58]).
12. **Entire agreement clauses:** don't say they block contextual interpretation (they don't) or that UCTA always applies to them (only if in substance exclusionary — Ng Giap Hon [32]).
13. **"Void" vs "ineffective":** UCTA failure = the liability cannot be excluded/restricted by that term (not automatic wholesale voiding); severance/whole-term reasonableness rules apply.
14. **Quotes:** never silently edit. Use `…` and keep the original words; italics/bold inside quotes only if in the source.
15. **eLitigation artifacts:** wk_1–4 files may include abridgements, `[num ]` strings, or missing paragraphs. Cross-check anything load-bearing.

## 9. Case-brief house format (for weeks 1–4, where briefs are absent)

If you also brief cases (recommended when a summary relies on a raw case), follow the established format: frontmatter (`importance: 1–5`, tags from the taxonomy, `note_up` where known) → importance callout after the Note-up line → **Exam version** (a: one paragraph; b: when to reach for it; c: analogy table) → **Case brief** (citation/coram; facts; issues; result; numbered ratio with `[n]`; obiter; authorities) → **Pro Max** (numbered deep-dive sections + quick-recall card) → **Judgment** (preserve source text untouched). Match the depth of the Week 7 briefs; scale by importance.

## 10. Citation conventions

- Case pinpoints: `[n]` referring to the judgment as reproduced in the case note. Case short-name in italics; full name on first mention.
- Textbook: `Phang 07.034` / `06.037` / `04.076` (chapter.paragraph).
- Statutes: `s X` with the Act named at least once per section of your document; state the edition when the distinction matters.
- Old vs new: `s 14 (formerly s 12B)` — always give both when the reader may hold the other numbering.
- Ratio vs obiter: label it when it matters.
- Every paragraph of the output that states law must trace to at least one of the above.

## 11. Toolkit (verified techniques)

### 11.1 Extract text from the Phang PDFs (macOS)
`pdftotext` is not installed. Use PDFKit via Swift:

```swift
// extract.swift — run: swift extract.swift "file.pdf" > out.txt
import Foundation
import PDFKit
let url = URL(fileURLWithPath: CommandLine.arguments[1])
let doc = PDFDocument(url: url)!
print("PAGECOUNT:\(doc.pageCount)")
for i in 0..<doc.pageCount {
  if let s = doc.page(at: i)?.string { print("\n=== PAGE \(i+1) ===\n" + s) }
}
```

Extraction artifacts: spaced-out title letters ("T h e L a w"), body/footnote interleaving, occasional `\x00`. Clean with a small Python pass (strip nulls/control chars; join single-letter runs). Cross-check any load-bearing quote against the page context.

### 11.2 Fetch statutes from SSO (sso.agc.gov.sg)
- `curl` is blocked (CloudFront 403); plain `webfetch` returns only the shell/TOC (content lazy-loads).
- Use the **ego-browser** skill: `taskSpace(...)` → `page.goto("https://sso.agc.gov.sg/Act/<ID>")` → `page.click('text="Whole Document"')` → wait ~8–9 s → `page.evaluate(() => document.body.innerText)` → save. Verify by grepping for distinctive phrases of the sections you need.
- Save the verified text into `modules/CL1_Contract/Statutes/<Act name>.md` with frontmatter (type: statute, retrieved date, source URL, note to re-verify). Future sessions must prefer the saved copy and re-verify only if the user's edition may differ.

### 11.3 Print-ready PDF (optional, on request)
Pipeline: md → styled HTML (Python converter) → Chrome headless print-to-pdf.
- Converter gotchas: drop YAML frontmatter; escape HTML first, then convert; wikilink regex must handle inner brackets — `\[\[(.*?)\]\]` then `rsplit("|", 1)` for the alias; unescape `\|` inside table cells before parsing rows; group `>` blocks as blockquotes; page-break before each `# PART` heading; A4 `@page` margins ~15 mm.
- Chrome: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=10000 --user-data-dir=<temp> --print-to-pdf="<out.pdf>" "file://<html>"`. **Chrome may not exit** — run it backgrounded with a watchdog loop that polls for a stable PDF size, then `pkill -f "<profile>"`. Output to `$VAULT/for printing/` and include a copy of the source `.md`.
- Verify the PDF by extracting its text (same Swift tool) and grepping for key strings; check page count.

## 12. Roadmap & continuity

- **Contract summaries: COMPLETE** (Wks 1–4 + 7 written; Wks 5–6 were presentation weeks). The summary phase is done — exam practice now runs through the sibling skill **`.opencode/skills/exam-grill-pipeline/SKILL.md`** (timed attempts · marking against `Grill/CL1_Contract/IRAC Rubrics.md` · drills + error ledger). Load it for any practice, marking or drill work; the old chapter mapping (Wk1→Ch3, Wk2→Ch3 Part E, Wk3→Ch4, Wk4→Ch6 + Ch4 paras 04.073–076) is all built out.
- **Weeks 5–6:** presentation weeks — skip unless the user asks.
- **Criminal law (started Sep 2026):** the CRL pipeline now lives in its own sibling skill — `.opencode/skills/crl-exam-summary-pipeline/SKILL.md` (Woon spine → statutes → R·M·A pre-writes → drill loop; LawNet source discipline; statutory-currentness discipline). Load it for any CRL summary work; its §10 carries the criminal build state.
- **Continuity script for a fresh chat:** *Contract:* "This continues the exam-summary series. Load the `exam-summary-pipeline` skill, then generate the Week N summary." *Criminal:* "This continues the criminal law exam-summary series. Load the `crl-exam-summary-pipeline` skill, then build the Week N summary." (If the skills list is unavailable, read the skill file under `.opencode/skills/` directly.)
