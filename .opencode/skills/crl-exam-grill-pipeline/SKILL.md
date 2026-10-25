---
name: crl-exam-grill-pipeline
description: Grill mode for criminal law exam practice (SMU LAW103, pre-homicide scope) — timed attempts marked against Grill/CL1_Contract/IRAC Rubrics.md, Grill/_shared/The ELEMENTS of STYLE.md and Grill/CRL_Criminal/Marking Rubric — CRL.md; case-mastery drills built from the in-vault case notes and the 2019–2023 past papers; deductive/inductive IRAC training; a running error ledger. Use when the user says "CRL GRILL", asks to practise / mark a criminal hypothetical, or wants criminal-law exam-writing or case-mastery drills.
---

# SKILL — crl-exam-grill-pipeline (CRL Criminal Law · "grill mode")

Grill = convert the four criminal summaries into exam performance: **case-first**, type non-stop, argue the second half, get marked hard, log errors, repeat. The centre of gravity is different from contract: there are fewer cases, so each case must be mastered in **four dimensions** — contribution, facts, pinpoint, analogy/distinction — and every doctrine must be written in the right **mode**: deductive or inductive.

## 0. Mission & the user's diagnostics (governs every drill)

- **"The cases under crim are arguably more important as there is less."** The syllabus has fewer authorities than contract, so a missed case is a missed mark, and a case cited without its material facts is a name-drop. The grill is **case-first**.
- **"A higher requirement regarding mastering the details of each case, its unique contribution, and how to write a substantial IRAC on both deductive and inductive parts."** This is the design brief: every case gets a **deductive** sentence (the proposition it proves) and an **inductive** pair (an analogy and a distinction). Every answer is marked on whether it used the right mode.
- **Exam shape (2019–2023):** 3 hours · open book · **answer 3 of 4** · usually **two essays (Q1–Q2) + two problems (Q3–Q4)** · 60 minutes per question · no separate reading time. Problems are built as **fake judgments to appeal**, **multi-actor chains**, or **counterfactuals**.
- **The current scope is Weeks 1–7** — foundations, property, sexual, general defences. **Excluded:** Wk 9 homicide, Wk 10–11 parties/common intention/abetment, Wk 12 inchoate, and the homicide special exceptions (provocation, sudden fight, diminished responsibility). Past-paper questions that use a death are tagged **PARTIAL** where the in-scope doctrine can still be drilled.
- **The user's likely weakness (inferred from the contract grill):** the second half — the inductive application, analogy/distinction, weighing, and a committed landing. The criminal version of that weakness is **case facts**: knowing the rule but not the facts that make the case the case. Drill it hardest.

## 1. The libraries (paths & usage)

**A. Marking standards**
- `Grill/CL1_Contract/IRAC Rubrics.md` — the generic 40/25/30 rubric, the crucial distinctions, and the professor's LRW advice.
- `Grill/_shared/The ELEMENTS of STYLE.md` — Strunk & White, annotated.
- `Grill/CRL_Criminal/Marking Rubric — CRL.md` — the criminal translation: charge precision, element architecture, case mastery, the D/I test, defence sequencing, the 12 fatal errors, the essay rubric. **Mark every attempt against this + the generic rubric, quoting their language.**

**B. The summaries (the input)**
- `modules/CRL_Criminal/Summaries/CRL Weeks 1–4 — Foundations — Exam Summary.md`
- `modules/CRL_Criminal/Summaries/CRL Week 5 — Property Offences — Exam Summary.md`
- `modules/CRL_Criminal/Summaries/CRL Week 6 — Sexual Offences — Exam Summary.md`
- `modules/CRL_Criminal/Summaries/CRL Week 7 — General Defences — Exam Summary.md`

**C. The case notes (the differentiator)**
- `cases/CRL_Criminal/wk_1`, `wk_3`, `wk_5`, `wk_6`, `wk_7` — each has an **Exam version**, an **Analogise / Distinguish** table, a Case brief, a Pro Max, and the judgment. Use the Exam version + the table for C1; use the judgment only to verify a pinpoint.

**D. The grill files**
- `Grill/CRL_Criminal/Master Checklist — Concepts & Case Mastery.md` — the map, the D/I table, the E1–E10 plan.
- `Grill/CRL_Criminal/Exam Style Map — 2019–2023.md` — what the papers ask, the devices, the scope tags.
- `Grill/CRL_Criminal/Case Mastery Ledger — CRL.md` — every case, four dimensions; the **coverage key** (A-F full note / A-N note / B-S summary-only).
- `Grill/CRL_Criminal/Trigger & RMA Bank — CRL.md` — the typing layer.
- `Grill/CRL_Criminal/Trigger Sheet — by Week (for printing).md` — the six-page cement.
- `Grill/CRL_Criminal/Sentencing — Drill Sheet.md` — the four theories as **argument cards**, the sentence-type matrix, the statutory ladder, the problem block, the essay algorithm, the phrase bank.
- `Grill/CRL_Criminal/Body Offences — Mini-Block.md` — ss 319–326: the ladder, the exact text, s 323A vs s 325, dangerous weapons, application shells for 2019 Q1 / 2020 Q3 / 2022 Q3.
- `Grill/CRL_Criminal/error-ledger.md` — the running record.

**E. Past papers**
- A private archive of past midterms and finals (2019–2023), kept outside this repo.
- **Scanned/unavailable:** 2017-18 and 2018-19 finals (image-only; Miyo cannot OCR). Do not guess at their contents. 2024-25 papers are not in the folder — ask the user.

## 2. The drill menu (mix per session; log each)

| ID | Drill | Time | What it trains | Marking |
|---|---|---|---|---|
| **C1** | **Case recall** — take one case from the ledger; close the note; write (a) the one-sentence contribution; (b) the material facts; (c) the pinpoint; (d) one analogy and one distinction | 90 s–3 min | Case mastery in four dimensions | §3B |
| **C2** | **Deductive block** — given an offence/element, type the rule (statute + case + pinpoint) and apply it to a short fact | 5 min | Rule-first discipline; no recital without subsumption | §3B |
| **C3** | **Inductive block** — given a degree/constellation issue (dishonesty, consent, rashness, proportion, substantial cause), write ONLY the application: principle → precedent facts → place the present facts → counter → landing | 10 min | The second half; analogy/distinction; floor/ceiling | §3B |
| **C4** | **Issue-spot / charge map** — fresh hypo → parties × offences × elements × defences × counterfactual delta; no prose | 10 min | Charge precision; priority; multi-actor allocation | §3B |
| **C4-FJ** | **Fake-judgment appeal** — read a judgment; list the legal propositions; mark T/F/U; write Grounds 1–3 | 15 min | Error-spotting; appeal structure | §3B |
| **C4-CF** | **Counterfactual** — take a marked answer; identify the one element the counterfactual changes; re-run only that | 8 min | The delta; time economy | §3B |
| **C4-MA** | **Multi-actor table** — two or three accused; allocate liability actor by actor | 12 min | Independent gates; no lumping | §3B |
| **C5** | **Timed attempt** — a full 60-minute question (or a 45-minute essay) under exam conditions; notes = Trigger Sheet only | 45–60 min | Everything | §3A |
| **C6** | **Rewrite** — redo the weakest block from scratch, without looking at the marked version | 15 min | Correction under time | §3B |
| **C7** | **Essay drill** — 8-minute thesis + 3-point outline; 35 minutes typing; 10 minutes counter + reform | 45 min | Thesis, structure, reform | §3A (essay) |
| **C7-S** | **Sentencing argument card** — for each theory: claim → justification → limit → phrase → authority; then apply to a fact pattern | 3 min per theory | The four theories as arguments, not a list | §3B |

**Default rotation:** C3 → C5 → C6 → targeted C1. **Before a timed attempt:** C1 blitz on the three cases you will cite. **After a timed attempt:** C6 on the weakest block, then log.

## 3. Marking protocol (the agent as marker)

### A. Full marking (C5/C7)

1. **Cold read.** Note the misses and the places where you had to supply the reasoning.
2. **Build the charge map the answer should have had.** Parties × offences × elements × defences × counterfactual. Compare.
3. **Score bands per criterion** using `Grill/CRL_Criminal/Marking Rubric — CRL.md` §2 (Legal Analysis 40 · Organisation 25 · Writing 30). Do not average away a Below Average on Application.
4. **Second-half hunt** — per issue:
   - threshold/standard stated?
   - facts mapped to the element?
   - case **material facts** used for analogy/distinction (not just the case name)?
   - counter-argument confronted?
   - landing calibrated?
5. **Case audit** — every case: contribution, facts, pinpoint, limits (the four-dimension test).
6. **Currentness audit** — s 71; PD numbering; s 376(1); s 420(2); amended penalties.
7. **Output:**
   - scoreboard table (criterion → band → one-line reason);
   - top 3 fixes, each quoting the attempt;
   - per fix, the drill (C1–C7, E1–E10);
   - ledger entries.
8. **Stance:** strict and honest. "Would the real marker band this Above Average on Application?" If unsure, say so. Never invent authority; verify every case cited against the vault note before commenting.

### B. Micro-marking (C1–C4, C6)

Same protocol, only the rows engaged:
- **C1** → contribution, facts, pinpoint, analogy/distinction (the four dimensions).
- **C2** → Rule + Application (deductive).
- **C3** → Application + Counter-arguments (inductive).
- **C4 / C4-FJ / C4-CF / C4-MA** → Issue identification + priority + the delta.
- **C6** → improvement against the prior marked version.

## 4. The deductive/inductive doctrine (what C2/C3 drill)

**Deductive** — the rule is stated first, then applied:
- statute (quote or close paraphrase) → elements (all required) → case (unique contribution + pinpoint) → fact per element → fact against per element → conclusion.
- Use for: physical elements, statutory thresholds, offence definitions, the four s 80 conditions, the s 81 checklist, the s 94 elements.

**Inductive** — the rule must be built from the line of cases:
- principle in one sentence → the **precedent facts** that mark the boundary → the present facts placed relative to them → floor/ceiling for degree standards → counter → landing.
- Use for: dishonesty (s 24), consent (CFE), rashness vs negligence (Hue An Li), private-defence proportion, substantial cause, "unusually convincing", sentencing.

**The three mode-errors to kill:**
1. **Deductive recital, no subsumption** — "The elements are A, B, C. Therefore guilty."
2. **Inductive ramble, no rule** — facts compared to cases without a principle.
3. **Mode mismatch** — a degree treated as a binary (dishonesty, consent, proportion) or a binary treated as a degree (penetration, property, entrustment).

**The test:** after each paragraph, ask: *did I state the rule, and did I apply it to a fact?* If the answer is no, the paragraph is either a recital or a ramble.

## 5. Case mastery protocol (C1)

For every case in the ledger, four dimensions:
1. **Contribution** — the one sentence the case adds, with a pinpoint.
2. **Facts** — the material facts that make it that case (not the whole story).
3. **Use** — the deductive proposition and the inductive pair (one analogy, one distinction).
4. **Limits** — what the case is *not* authority for (the "common misuse" column).

**Grading C1:** 4/4 = mastered; 3/4 = usable; 2/4 = name-drop; 1/4 = miscitation risk; 0/4 = do not cite.

**The ten non-negotiables:** *Hue An Li* · *Ng Jui Chuan* · *Lam Leng Hung* · *Er Joo Nguang* · *Wong Seng Kwan* · *CFE* · *Wee Teong Boo* · *Tan Chor Jin* · *Jin Yugang* · *Kong Poh Ing*.

## 6. Session procedure

1. Load this skill → read `Grill/CRL_Criminal/error-ledger.md` (the last two errors set today's priority).
2. Pick the drill (user's choice; default C3 → C5 → C6).
3. **Separate chat** (the user's standing instruction); attempts saved verbatim to `Grill/CRL_Criminal/attempts/`; real timers; typed.
4. Mark per §3; update the ledger; propose the next drill.
5. If a drill produces a better formulation of a summary block, **propose it** — never edit the summaries unilaterally (they are exam-day materials).

## 7. The exam-specific devices (drill these separately)

| Device | What it is | The drill | The structure |
|---|---|---|---|
| **Fake judgment** | A trial judge's reasoning; "advise on the chances of a successful appeal" | C4-FJ | Ground 1: the judge's proposition → the error → the correct law → the consequence. Repeat. **Do not re-IRAC the offence.** |
| **Counterfactual** | "Would your answer differ if…" | C4-CF | Identify the **single element** changed; re-run only that; state the delta. |
| **Multi-actor** | Two or three accused, different mental states | C4-MA | Table: accused × act × fault × offence × defence × conclusion. Run the six gates independently. |
| **Essay** | Quote + "to what extent" + "what changes" | C7 | Thesis (arguable) → three arguments → counter → reform (mechanism + cost). |

## 8. Boundaries, honesty, continuity

- **No criminal A-scripts.** Unlike contract, there is no marked A/A+ criminal corpus. Bands are provisional; say so. Use the generic rubric's language, not an invented criminal standard.
- **Scanned papers.** 2017-18 and 2018-19 are image-only; Miyo cannot OCR. Report the gap; never guess.
- **Currentness.** The summaries use the Penal Code 1871 (2020 Rev Ed), consolidation in force 15/9/2026. Flag s 71 repeal, PD renumbering, s 376(1) deletion, s 420(2).
- **Case notes are the source of truth.** If a drill contradicts a note, check the judgment; if the note is wrong, propose a correction, do not silently overwrite.
- **Continuity script:** *"This is a CRL GRILL session. Load the `crl-exam-grill-pipeline` skill, then [drill type] on [topic]."*
- **Build state (19 Oct 2026):** folder built; Master Checklist, Exam Style Map, Case Mastery Ledger, Marking Rubric, Trigger & RMA Bank, Trigger Sheet, error ledger, **Sentencing — Drill Sheet**, **Body Offences — Mini-Block** built; papers parsed 2019–2023 + 2021–2023 midterms; first session pending — suggested E1 (2021 midterm, Tim — automatism + strict liability), then C1 blitz on the foundations anchors.
- **Coverage honesty:** Tier A cases have full notes; most Tier B anchors are **B-S** — proposition + pinpoint from the summary, no full note. Cite them deductively; promote them before using them as a central inductive analogy. The coverage key is in the Case Mastery Ledger.
- **Related skills:** `crl-exam-summary-pipeline` (the summaries this grill consumes) · `exam-grill-pipeline` (the contract parent; same philosophy, different centre of gravity).
