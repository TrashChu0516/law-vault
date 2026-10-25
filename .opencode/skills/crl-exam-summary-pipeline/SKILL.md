---
name: crl-exam-summary-pipeline
description: Criminal law (CRL) exam-summary pipeline — build exam-ready mini-textbook summaries anchored on Woon's Essential Criminal Law (the spine), statutes from the Interpretations bank, R·M·A case pre-writes, and typing-drill packs for timed exam output. Use when the user asks for a criminal law exam summary / cheatsheet / week summary, says "continue the criminal series", or references CRL weeks, cases/CRL_Criminal, or Woon.
---

# SKILL — CRL exam-summary pipeline (agent-facing spec)

You are producing the **criminal law** exam summaries for the user — the same series as the contract (CL1) summaries, adapted for a statute-first, case-heavy module. This skill is the criminal adaptation of `exam-summary-pipeline` (contract, sibling folder `.opencode/skills/exam-summary-pipeline/SKILL.md`): **load that skill too** — its §11 toolkit (Swift PDF extraction, SSO fetch via ego-browser, print-to-PDF) and §7 verification carry over unchanged. This file records what differs for criminal law and what the user has said the summaries must achieve.

## 0. Mission — the user's words (governs every decision)

> "WHATEVER NOT WRITTEN IS NOT COMMUNICATED AT ALL. My biggest nightmare is to be stuck in that 3 hour final THINKING WHAT AND HOW to write."
> "The summaries are supposed to be our biggest solution."

The deltas the user has named for criminal:

1. **Input ≠ output.** Reading and understanding are not exam performance; the pipeline converts learning into *surgical exam output* — pre-written blocks the user can type non-stop under timed pressure.
2. **Fit the cases into the spine.** Woon's *Essential Criminal Law* is the skeletal spine (less long-winded than Phang; flags common caveats); cases must attach to statutory elements via R·M·A blocks — "otherwise it becomes an interpretation exam, not a law exam." Cases illuminate the abstract statutes and sit closer to exam questions.
3. **Volume vs page limit.** The cheatsheet page limit conflicts with how voluminous the subject is → tiering (§6).
4. **"I think I understand" ≠ an A+ written answer.** Under pressure the difference is pre-writes + drill.
5. **Typing speed.** The user types slowly relative to thinking speed ("fingers can't catch brain") → summaries must be drillable word-for-word (§7 drill packs), so the exam response is *typed, not composed*.

## 1. Cardinal rules

1. **Never fabricate** (vault rule). In criminal law this bites hardest: never write a section number, element, holding or pinpoint from memory. Read the bank file / source, or mark `[CHECK]`.
2. **Statute-first currentness.** Criminal law is statutory. Every provision is cited to the **current Revised Edition** with amendment history where it matters (the bank's convention: amendment tags inline, e.g. `[15/2019]`). Verify every new section on **SSO** before saving; statute currentness is this module's highest-risk area (the Penal Code is frequently amended).
3. **Source discipline (from the Case Reading List).** Singapore judgments come from **LawNet, not eLitigation** (some eLitigation reproductions are silently abridged — the List flags the known ones; their notes carry provisional banners). UK cases via BAILII through a headed browser. Read the List's own *Source discipline* and due-diligence notes before fetching anything.
4. **Start from the vault** — §3 materials map — before going outside. Outside sources only when the vault falls short, then verify at source (AGENTS.md).
5. **Stop and ask when material is missing.** Never reconstruct a chapter, holding, or section. ("This list is deliberately incomplete.")
6. **Statute-verbatim blocks.** Elements are quoted from the saved Interpretations bank (or SSO, then saved); the user types them as-is in the exam.

## 2. Deliverable & naming

- **Summaries** → save to `modules/CRL_Criminal/Summaries/`:
  `CRL Week N — <Topic> — Exam Summary.md` (e.g. `CRL Week 5 — Property Offences — Exam Summary.md`; multi-week: `CRL Weeks 10–11 — <Topic> — Exam Summary.md`).
- Frontmatter: `type: summary`, `module: CRL`, `week`, `topic`, `sources`, `tags` (follow the CRL tag namespace already used in case notes, e.g. `crl/sexual-offences/rape`, plus a summary tag), `status`.
- Structure standard: the CL1 exemplar `modules/CL1_Contract/Summaries/Chapter 7 Regulation of Terms — Exam Summary.md`; anatomy adapted per §4.
- **Case-note standard** (when upgrading briefs): the wk_6 house format — see `cases/CRL_Criminal/wk_6/John Benjamin Cadawanaltharayil v Public Prosecutor [1995] SGHC 241.md`: frontmatter → "In this note" → **Exam version** (one-paragraph recap + *when to reach for this case* + analogy/distinction table) → **Case brief** → **Pro Max** → **Judgment**.

## 3. Materials map (verified paths, Sep 2026)

- **Spine:** `Textbook/CRL_Criminal_Law/Essential Criminal Law.pdf` (Walter Woon). Extract with the Swift tool + null-strip (contract skill §11.1). Woon = the element skeleton + "common caveats" — harvest both; do not drown the summary in his prose.
- **Extension:** the other PDF in the same folder — *Criminal Law in Singapore* (Yeo, Morgan & Chan, LexisNexis 2022). Use only to fill gaps, or when a week's outline prescribes it.
- **Case Reading List:** `_course_outlines/CRL_Criminal_Law/Criminal Law Case Reading List.md` — authoritative week topics + cases + status key (✅ full text / 📖 placeholder / ⬜ not collected) + source-discipline and due-diligence notes. **Read it first, every build.** Its wikilinks resolve each entry to the vault note. (Week 5's warning is superseded by its master outline: the faulty reproductions were repaired; two residual notes remain — Asok Kumar ends at [79]; Wong Tian Jun tables partly missing.)
- **Course outline:** `_course_outlines/CRL_Criminal_Law/G4 Crim Course Outline.pdf` — weekly scope + seminar questions. Extract the week's portion when building.
- **Slides:** `Slides/Crim/` — **Wks 1–6 in the vault** (as at 2 Oct 2026). Wk 1 carries the professor's **written model answers** (four versions of Case Studies 1–2 + his statutory-interpretation checklist — calibrate pre-write register against these); Wks 2–6 carry his **question sets** (hypotheticals) with no written answers. Wks 7+ not yet in vault — ask the user as they appear. Slides pass (§8 step 5): his emphasis guides Tier 1.
- **Cases:** `cases/CRL_Criminal/wk_N/` (+ `CRL_MOC.md`). **Wks 5, 6, 7, 9, 11 are fully briefed** (house format; wk_6 = the format model). Wk_5 also holds `_Week 5 — Property Offences (Master Outline).md` — doctrine end-to-end (the condensation source for that build). Wks 1 & 3 remain raw (wk_1 = PDFs only). wk_6 contains `CFE v Public Prosecutor [2026] SGCA 35` as an unprocessed **PDF** — confirm placement with the user before relying on it.
- **User's notes:** `Notes/Crim/Crim1.md`–`Crim7` + `Crim7 Defences.md` — align terminology, fill gaps, keep their vocabulary.
- **Statutes bank:** `modules/CRL_Criminal/Interpretations/<Act>/<Section>.md` — format = verbatim section text + inline amendment tags `[15/2019]` + `#statute` + occasional user annotations. Holdings include Penal Code ss 22–26E, 94, 191, 378, 403, 415; MDA ss 17–18; CPC ss 11, 123. **New (2 Oct 2026):** the **full Penal Code PDF** sits at `modules/CRL_Criminal/Penal Code 1871.pdf` (LRC informal consolidation, 320 pp, version in force **15/9/2026**) — extract sections from it first; still save each new section into the bank, and SSO-verify where currentness is live.
- **Course materials (new, 2 Oct 2026):** `_course_outlines/CRL_Criminal_Law/G4 Crim Course Outline.pdf` (weekly topics: Wk 5 property, Wk 6 sexual, Wk 7 defences, Wks 9–10 homicide, Wk 11 parties/abetment, Wk 12 conspiracy/attempts); `Grill/CL1_Contract/IRAC Rubrics.md` (the course's written-work criteria — issues · exposition/application · structure/analysis · authority · completeness — the marking scheme for the drill loop).
- **Sibling skill:** `.opencode/skills/exam-summary-pipeline/SKILL.md` (contract) — shared toolkit & verification.
- **Weekly seminar outlines:** when the professor's weekly outlines appear (they "pinpoint the chapters", as with CL1), archive them to `_course_outlines/CRL_Criminal_Law/` and follow them for scope.

## 4. Anatomy of a CRL summary (deltas from the CL1 exemplar)

- **Caveats panel** near the top: Woon's common caveats harvested for the week + source warnings (provisional reproductions etc.).
- **§0 Method** — the offence-analysis pipeline, written in typing order: (1) identify the offence(s) & parties; (2) elements checklist per offence (actus reus → mens rea), each element paired with (a) its statutory definition section (e.g. "intentionally" = Penal Code s 26C) and (b) its R·M·A blocks (§5); (3) defences filter (which defences plausibly arise); (4) conclusion shells; (5) offence-specific checklist items (e.g. property: "belongs to another"; homicide: the causation chain — verify each against the spine).
- **Parts = offences/topics** mirroring Woon + the week's outline; sub-parts = elements. Every element carries: statute-verbatim quote → R·M·A blocks → application hooks ("if the facts show X, type Y").
- **Seminar Q&A** — every question from the week's outline answered in 1–3 sentences (same as CL1).
- **Hypothetical skeletons** — IRAC shells for the week's likely fact patterns; blank party names so they are reusable; excluded from the word budget (standing rule).
- **Appendix** — case ledger (case → the statutory element it illuminates → its **UNIQUE contribution**, one line each — cf. the contract Week 4 build) + statutory map (section → one-line gist → cases that animate it) + exam-day trigger sheet (§7).

## 5. R·M·A — the case-block format (criminal edition)

Every case in the body appears in exactly one element's R·M·A block (cross-ref if it supports two), and in the ledger. Shape (from the saved bank, Penal Code ss 26A–26E):

- **R = Rule as a type-ready sentence:** statutory element (section + current Rev Ed) + case authority (LawNet citation + pinpoint). Quote the statutory words verbatim.
- **M = Material facts of the authority** — telegraphic fragments, pre-compressed to the one sentence that matters.
- **A = Analogise / distinguish hook** — the fact-pattern cue that pulls the case in or pushes it out (use the wk_6 analogy-table style when it helps).
- **⚠ = Caveat line (optional but characteristic of this module):** Woon's warning, an amendment risk, or a contrary authority.

Worked shape (s 26C example, abridged from the bank file `Interpretations/Penal Code 1871/26C Intentionally.md` — full text there; re-verify currency before reuse):

- **R:** "Intentionally" — s 26C(1)–(2): a person causes an effect intentionally if (a) it is his purpose, or (b) he knows it would be virtually certain to result. s 26C(3)–(4): a result being a natural and probable consequence does **not** by itself make it intended, but foresight may ground an *inference* of intention.
- **M/A (use):** when the facts give "purpose or virtual certainty" → type limb (a)/(b); when the prosecution only has "natural and probable consequence" → rely on (3)+(4) as an *inference* argument, and watch the trap of equating them with intention.

## 6. Condensation & the page limit

- **Tiering:** Tier 1 = §0 Method + element checklists + pre-writes (never cut). Tier 2 = R·M·A blocks, condensed to one line per limb. Tier 3 = appendix/ledger (one line per case; full briefs stay in `cases/`).
- One case = one line in the ledger; one R·M·A block in the body **max**.
- Target: obey the user's stated cheatsheet page limit for the module — **ask per build if unstated**; default body ≤ ~7,500 words unless told otherwise; hypotheticals excluded from the budget (standing rule).

## 7. Drill loop (anti-stuck machinery)

Each summary ends with a **typing-drill pack**:

1. 10–15 pre-write sentences formatted for blind typing (the exact sentences from the body).
2. 2–3 from-scratch issue shells (elements blanked; user fills under timer).
3. Suggested timers (e.g. 90 s per element block; a full issue in 6–8 min).

Grill mode runs as a **separate folder + separate chat** (user's standing instruction, as for CL1): hypos first (cross-element / cross-defence hybrids), then marked written answers against the course's written-work criteria (issues · exposition/application · structure/analysis · authority · completeness). Maintain an **error ledger**; re-drill weak blocks. Drills are built *from* the summary — they never create new content.

## 8. Workflow (per week)

1. **Scope:** read the Reading List entries for the week (topics, cases, status, warnings); resolve cases via its wikilinks; ask the user for the course instructor's slides if not in the vault.
2. **Spine pass:** extract Woon's chapter(s) (Swift tool; strip nulls; clean spaced-letter artifacts). Build the **element skeleton only** — no prose yet. Harvest caveats. **[CHECK] Woon's pinpoint scheme on first use** — do not assume a numbering format (e.g. Phang-style `0X.YYY`) before seeing it.
3. **Statute pass:** pull each needed section from the Interpretations bank; for missing ones, fetch SSO (ego-browser; whole-document click; save into the bank with amendment tags). Build the statutory map.
4. **Case pass:** read `cases/CRL_Criminal/wk_N/`; check completeness (eLitigation caveat); write R·M·A blocks + pinpoints; match the wk_6 format when upgrading raw notes.
5. **Slides pass** (when slides exist): fold the professor's emphasis into §0 + Q&A + Tier decisions.
6. **Notes pass:** reconcile with `Notes/Crim/CrimN.md`.
7. **Draft:** chunked writes (3–4 chunks; very large single writes fail — keep each ≤ ~20 KB).
8. **Verify** (§9), save, add the drill pack, update build state (§10).

## 9. Verification protocol (criminal edition)

- **Statute cross-check first:** every quoted section matches the bank/SSO text verbatim; current Rev Ed; amendment history noted where the element changed.
- Citation grep + **sample 5 pinpoints** traced back to source (`cases/` notes or the judgment).
- LawNet-completeness check on any newly fetched judgment (watch eLitigation abridgments).
- No orphan pre-writes: every R needs an authority; every authority needs a pinpoint.
- Red-team per element: correct mens rea term (intention / knowledge / rashness / negligence — ss 26A–26E)? statutory presumption flipping the burden (e.g. MDA ss 17–18)? defence statutory (Exceptions) or common law? case genuinely on all fours?
- Word count; link integrity (contract skill's perl check, with `cases/CRL_Criminal/wk_*` in scope); artifact scan.

## 10. Build state & continuity (update as builds complete)

*State as at 22 Oct 2026.*

- **Cases:** wks 5, 6, 7, 9, 11 fully briefed. wk_5 master outline present; source caveats resolved except the two residual notes (Asok [79] end; Wong tables). wk_1/wk_3 raw. **CFE v PP [2026] SGCA 35 processed (Wk 6)** — no longer pending. wk_7 briefs carry their own per-case pre-writes and analogise tables (mined in the Wk 7 summary).
- **Slides:** wks 1–**7, 9–10** in `Slides/Crim/`. Written model answers: Wk 1 (four versions) + Wk 4 (the professor's full John/s 304A rash-act model answer, reproduced in the Foundations summary). **Wk 7 deck (added 2 Oct) folded into the Wk 7 summary** — questions answered in Part L; the deck uses the **current** private-defence numbering (confirming the renumbering map; the Crim7 note's old numbers are the outlier); it supplies the ***R v Wilson*** facts (vault report still a placeholder); and its "s 94" label for slight harm is a **typo for s 95** (flagged). **Wk 9–10 Homicide deck (added 17 Oct) folded into the Wk 9–10 summary** — all questions answered in Part F; **deck errors flagged:** "Punishment for murder — S 304" is a typo for **s 302**, and "Type 3: up to 20 years" is wrong (**s 304(b) is 15 years**). Wks 8/11/12 pending.
- **Statutes:** full Penal Code PDF in vault (`modules/CRL_Criminal/Penal Code 1871.pdf`, in force 15/9/2026). **Bank now ~99 files** — Wks 5, 6 and (2 Oct) Wks 7 + 1–4 batches added: ss 22A, 26F–H, 43, 76–78, 80–86, 88–89, 91–93, 96–106A, 320, plus the earlier 4B, 26A–26D, 29/29B, 95, 379–382, 404–409, 416–420A, 424A/B, 463–471, 477A, 44, 71 [repealed], 79, 79A, 87, 90, 170, 349–354A, 375–377D. **Private-defence renumbering verified against the Act and bank filenames corrected** (current: 101 body start; 102 body death; 103 body non-death; 104 property start; 105 property death; 106 property non-death; 106A public servants). **Currentness catches:** s 71 repealed (Act 15/2010); s 376(1) deleted (Act 23/2021); s 382 caning wording `[Act 21/2025 wef 17/8/2026]`; **s 420(2) remote-communication cheating, mandatory caning ≥6 strokes `[Act 21/2025 wef 30/12/2025]`**. **Wk 9–10 batch (22 Oct):** ss 34, 44A, 111, 299–302, 304, 304A, 304B, 304C (bank = **110 files**). **Homicide currentness catches:** **s 304(b) is now 15 years** (slides say 20; *Govindasamy* [89] states the old 10-year maximum); **ss 304B/304C inserted by Act 15/2019, punishments amended by Act 21/2025 wef 17/8/2026**; **no s 303**; *Azlin* is [2022] SGCA 52 (Woon's footnote prints SGCA 67 — typo).
- **Summaries built: Weeks 1–4, 5, 6, 7 (2 Oct 2026); Weeks 9–10 (22 Oct 2026).**
  - **Wk 5 — Property Offences**: `modules/CRL_Criminal/Summaries/CRL Week 5 — Property Offences — Exam Summary.md` (~16.4k words; START HERE triage → §0 Method with the user's **Fit Rule** + objectivity map → Parts A–F per offence → slide Q&A → skeletons → ledger/statutory map/trigger sheet/drill pack). The §0 objectivity map (ss 24(a)/(b), 25, 26C, 26D, 26B, 95) is the seed of the cross-cutting Foundations layer.
  - **Wk 6 — Sexual Offences**: `modules/CRL_Criminal/Summaries/CRL Week 6 — Sexual Offences — Exam Summary.md` (~11.2k words; triage → §0 with the **LRW answer-craft distilled** + state-of-mind/burden map → Part A OoM → Part B ss 375/376 → Part C consent & mistake → Part D proof/evidence → 13 slide Qs answered → skeletons → ledger/statutory map/trigger sheet/drill pack).
  - **CFE v PP [2026] SGCA 35 PROCESSED and integrated** as the Wk 6 banner authority ([74]–[80], [89]–[94]: consent specificity; *Iryan* definition; *Barton* propositions; mistaken-consent two-limb test; continuing validity of consent; victim-blaming). The former "unprocessed PDF" pending item is resolved. **Bank extended by 19 sections** for Wk 6 (44, 71 [repealed — flagged], 79, 79A, 87, 90, 170, 349–351, 354, 354A, 375, 376, 376A, 377C, 377CA–D). **Currentness flags:** s 71 repealed (Act 15/2010); s 376(1) deleted (Act 23/2021) — old citations must be mapped.
  - **LRW advice distilled** into `Grill/CL1_Contract/IRAC Rubrics.md` (CREAC with conclusion up-front; issue-spotting sequence; rule-statement discipline; floor/ceiling calibration) — use it when marking grill papers.
  - **Wk 7 — General Defences**: `modules/CRL_Criminal/Summaries/CRL Week 7 — General Defences — Exam Summary.md` (~12.6k words; tiered per the user's steer — **mistake of fact, intoxication, private defence first**; PD current numbering + old→new renumbering map; *Muhammad Hamir* s 81 checklist; intoxication succeeds/fails pairs; the s 80 lawful-act trio + the four-condition formulation (*Tan Chor Jin* [30]); master alarm/trigger sheet; drill pack). **Slides pass complete (2 Oct):** Part K (s 95 slight harm) + Part L — 14 slide questions answered (accident hypos incl. George and *Kong Poh Ing*; necessity hypos incl. the transplant-theft; the two property-PD hypos; *Brown*/*Wilson* with slide-sourced facts; intoxication sub-types and *Teo*/*Tharema* takeaways; the slide's s 94/s 95 typo flagged); *Abdullah v R* added to the mistake section.
  - **Wks 1–4 — Foundations**: `modules/CRL_Criminal/Summaries/CRL Weeks 1–4 — Foundations — Exam Summary.md` (~7.4k words; master pipeline; fault-layer objectivity map; ss 26A–H; strict liability (*Gammon*); wilful blindness (*Adili* [51]); one-transaction (*Thabo Meli*/*Shaiful Edham* [84]); causation two-stage + the four Wk 4 hypos worked; Wk 1–2 layer (jurisdiction, IRAC + interpretation checklist, discretion, punishment); the professor's John/s 304A model answer; drill pack).
  - **Wks 9–10 — Homicide**: `modules/CRL_Criminal/Summaries/CRL Weeks 9–10 — Homicide — Exam Summary.md` (~13.4k words; START HERE homicide pipeline → §0 method/state-of-mind map/currentness panel → Part A s 299 + s 304 + s 301 → Part B s 300(a)–(d) (s 300(c) worked through *Virsa Singh*/*Lim Poh Lye*/*Tan Joo Cheng*/*Mohamed Ali*; s 300(d) through *Govindasamy*) → Part C Exceptions 1–7 (provocation → sudden fight → exceeding PD → DR first; consent/infanticide/public servant brief) → Part D s 304A + RTA + **ss 304B/304C** → Part E *Azlin* common-intention bridge → Part F all 14 slide Qs/hypos answered → Part G skeletons → ledger/statutory map/trigger sheet/drill pack). ***Govindasamy* verified from the eLitigation judgment** ([45], [52]–[63], [72]–[73]); all other pinpoints traced to the wk_9 briefs (plus *Tan Chor Jin* in wk_7).
  - **Source-accuracy fixes logged:** the wk_3 *Hue An Li* note banner says "not dichotomous" — **the judgment ([34]–[40]) and its SLR headnote say rashness and negligence ARE dichotomous** (the Foundations summary follows the judgment and flags the banner). s 71 repeal (Act 15/2010) flagged wherever old cases cite it (Zeng; Teo Heng Chye).
- **Next builds (user to give the go):** Wk 11 (Parties — wk_11 briefs already present) → Wk 12 (Inchoate). **Grill mode has now activated (19 Oct 2026):** the past papers are parsed (2019–2023 finals + 2021–2023 midterms; 2017-18/2018-19 are image-only and unavailable), and the CRL grill architecture is built in `Grill/CRL_Criminal/` under the skill **`crl-exam-grill-pipeline`**. The summaries remain the input; the grill consumes them. `archify` is installed — use it, if wanted, for a print-ready "which offence?" decision flowchart.
- **Pending:** the course instructor's Wks 8/11/12 slides; weekly CRL seminar outlines (archive under `_course_outlines/CRL_Criminal_Law/`); wk_1/wk_3 notes conversion; user review of the five built summaries; **the body-offences mini-block (ss 319–326)** flagged in `Grill/CRL_Criminal/Master Checklist` §7; **homicide cases not yet added to `Grill/CRL_Criminal/Case Mastery Ledger — CRL.md`**; first CRL grill session (E1).
- **Continuity script:** *"This continues the criminal law exam-summary series. Load the `crl-exam-summary-pipeline` skill, then build the Week N summary."*

## 11. Relationship to the other pipelines

- **Parent:** `exam-summary-pipeline` (contract CL1) — same R·M·A philosophy, extraction/fetch toolkit, chunked writes, verification, exemplar discipline. This skill adds the criminal deltas: statute-first currentness, Woon-as-spine, caveats panel, LawNet source discipline, drill loop.
- **Downstream:** `crl-exam-grill-pipeline` (criminal grill) — consumes these summaries and the case notes; case-first drills, D/I IRAC training, timed attempts, error ledger. Its files live in `Grill/CRL_Criminal/`.
- **Exemplars:** summary = the CL1 Week 7 file; criminal case note = the wk_6 files.
- **Do not duplicate** toolkit instructions here — read them from the parent skill when executing; keep this file focused on what differs.
