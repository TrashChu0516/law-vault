---
name: exam-grill-pipeline
description: Grill mode for contract law exam practice — timed attempts marked against the in-vault rubric (Grill/CL1_Contract/IRAC Rubrics.md + Grill/_shared/The ELEMENTS of STYLE.md), drills built from the user's exam summaries and the 2007–2022 past-year papers, a senior-script language bank, and a running error ledger. Use when the user says "GRILL", asks to practise / mark a contract hypothetical, or wants exam-writing drills. Currently CL1 Contract; extensible to other modules.
---

# SKILL — exam-grill-pipeline (CL1 Contract Law · "grill mode")

Grill = convert the finished summaries into exam performance: type non-stop, argue the second half, get marked hard, log errors, repeat. This skill carries everything needed to run a grill session **without redoing the September–October 2026 recon** (seniors' scripts converted and sampled, 2007–2022 papers parsed, marker feedback distilled). The heavy reference material lives in `references/recon-notes.md` (same folder).

## 0. Mission & the user's diagnostics (governs every drill)

- "**Time/page limit is harsh.**" The exam: 3 hours, open-book, typed into a **single text box**, numbered parts, % weights. Every drill rehearses to fit.
- "**WHATEVER NOT WRITTEN IS NOT COMMUNICATED AT ALL.** My biggest nightmare is to be stuck in that 3 hour final THINKING WHAT AND HOW to write." → prewrites first, then practice typing them under time.
- The user's diagnosis of the senior scripts: strong at **rule assertions** (their phrasing is worth borrowing) but thin in **the later half of the application — "the inductive part with actual distinguish/analogise and weighing".** That second half is where marks are won; grill drills it hardest (§4).
- Earlier cohorts' advice (private material): finish prewrites early and **practise hypos with them**. The summaries are the input; grill is where they become performance.
- **Exam shapes:** **Midterm (current focus): 90 min · ONE scenario · ~5–6 subquestions · weights 10–20% each**. The professor's process: 10–15 min reading, then NO pausing — type from cement. **Math: ~75 min typing ÷ 100 marks ≈ 0.75 min/mark ≈ 18 words per 1% at ~24 wpm** (10% ≈ 180 · 20% ≈ 360 · 35% ≈ 630 — recalibrate from timed retypes). **Final (later): 3 h / 3 questions — separate math; do not conflate.**

## 1. The four libraries (paths & usage)

**A. Marking standards (in vault)**
- `Grill/CL1_Contract/IRAC Rubrics.md` — the grading rubric distilled: **Legal Analysis 40%** (Issue identification · Rule & Rule Explanation · Synthesis · Application · Counter-arguments/adverse authority) · **Organisation 25%** (IRAC · memo-structure elements · roadmap · headers · signposting) · **Writing 30%** (language · tone/audience · citation · proofreading); plus the "Crucial distinctions" (gateway vs factors; elements vs disjunctive requirements vs factors; tests vs guiding principles vs justifications; rule vs implication; threshold analysis; positive vs negative rule) and the "Professor's exam-writing advice (LRW)" distillations.
- `Grill/_shared/The ELEMENTS of STYLE.md` — Strunk & White, annotated by Steven (active voice; omit needless words; positive form with legal-nuance carve-outs; emphasis at end; that/which; etc.).
- **Mark every attempt against these two documents, quoting their criteria language.** They are the user's own standards — no invented criteria.
- Process standard: **the professor's exam-technique notes** (private) — 15 min reading/thinking max; gentle Q1 ≈ 6–7 min including all four elements + definitions; breadth over depth; 2-line counters "positive over the counter"; no pinpoints needed; **6-page trigger memory — cement, not encyclopaedia**; don't re-read what you wrote.

**B. The user's summaries (in vault)** — `modules/CL1_Contract/Summaries/`:
`Chapter 3 (Parts A–D) — Week 1 Exam Summary.md` · `Chapter 3 (Part E) & ICLR — Week 2 Exam Summary.md` · `Chapter 4 (Consideration & Promissory Estoppel) — Week 3 Exam Summary.md` · `Chapter 6 (Express & Implied Terms) — Week 4 Exam Summary.md` · `Chapter 7 Regulation of Terms — Exam Summary.md`.
These hold the pre-write banks + typing-drill packs. Drills type **from** these; in the real exam they are open-book material.

**C. Past-year papers** (private corpus — kept outside this repo; the parsed index and topic matrix live in `references/recon-notes.md`, also private)
- A private archive of past midterms and finals spanning 2007–2023, supplied by the user.
- **Exam constraints (verified from papers):** 3h · open-book · typed into ONE text box, parts prefaced "(1)a" etc. · single mega-question or 2–4 parts with % weights · recurring devices: "separate and independent scenarios", "how would your advice differ if…", "leave aside [SGA / tort / quantum / CPFTA]", fictitious jurisdiction ("Lion City = Singapore law").
- **Scans without a text layer** (Miyo cannot OCR — flag if the user wants them): several early papers are image-only. The pipeline flags them and never guesses at their contents.
- **Topic-scope caveat:** the 2016–2022 papers include discharge/remedies topics (frustration, repudiation, FM clauses) because historically LAW101 covered them. The user's summary series covers W1–4 + W7 only — **confirm scope with the user before drilling any discharge/frustration part.**

**D. Senior scripts** (private; insights, NOT binding — the user's professor is different, and the files themselves warn of errors)
- Used for two things only: **rule-assertion phrasing** and **marker-feedback calibration**.
- Every proposition borrowed from them is re-checked against the primary sources (case, statute, textbook) before it enters an answer.
- Treated as style evidence, never as authority.

**E. Trigger & RMA Bank** — `Grill/CL1_Contract/Trigger & RMA Bank.md`: the exam-condensed typing layer (TRIGGER → R·M·A per sub-topic, pinned to the summaries). Grows one installment per question; raw material for the exam-day 6-page trigger sheet and the backbone of D1/D2 drills.

## 2. Drill menu (mix per session; log each in the ledger)

- **D1 · Type-drill (10 min)** — blind-type one pre-write block from the summaries, verbatim, against a timer. Goal: stock parts cost zero thinking (WPM is a known weakness).
- **D2 · Issue-spot blitz (10–12 min)** — fresh hypo → produce ONLY the issue list + order + one-line rule tag each, no prose. Mark: missed issues, wrong priority, over-inclusion.
- **D3 · Second-half drill (25–35 min)** — given the rule (use a summary block) + facts → write ONLY the application: threshold, analogise/distinguish with ≥2 authorities, weigh, conclude. Mark: Application + Counter-arguments rows. **The core drill.**
- **D4 · Timed attempt** — a full question under exam time. Current target shape: **90 min / 5–6 subquestions** (≈15 min each after a 10–15 min read); for finals, 3 h / 3 essays. Typed; notes = summaries now → 6-page trigger sheet closer to exam day. Saved to `Grill/CL1_Contract/attempts/YYYY-MM-DD — <topic>.md`; gets the full marking (§3A).
- **D5 · Rewrite (15 min)** — immediately redo the weakest block from scratch, without looking at the marked version. Log the improvement.
- **D6 · Style pass (10 min)** — apply ELEMENTS rules sentence-by-sentence to a marked answer (active voice, omission, end-weight). Compare length before/after.

## 3. Marking protocol (the agent as marker)

**A. Full marking (D4):**
1. Read the attempt cold; note misses/flaws before consulting the rubric.
2. Score **band per criterion** (Below / Average / Above) using the exact band descriptors in `Grill/CL1_Contract/IRAC Rubrics.md`: Issue identification · Rule & explanation · Synthesis · Application · Counter-arguments · IRAC · roadmap/headers/signposting · language · tone · citation · proofreading.
3. **Second-half hunt (always):** per issue — (i) threshold/standard stated? (ii) facts mapped against floor/ceiling authorities? (iii) genuine analogies/distinctions with material facts, not name-drops? (iv) counter-argument confronted? (v) conclusion calibrated ("likely … because …")? Flag every conclusory leap.
4. Output: (a) scoreboard table (criterion → band → one-line reason); (b) top 3 fixes with quoted lines from the attempt; (c) per fix, the drill to run next; (d) ledger entries. Anchor quotes to the rubric's language ("unchallenged uncertainty", "case-by-case without synthesis", etc.).
5. Stance: strict and honest — "would the real marker band this Above Average on Analysis?" If unsure, say so. Never invent authority; verify any case cited in the attempt against the vault case notes before commenting; flag unverifiable cites as risks.

**B. Micro-marking (D2/D3):** same protocol, only the rows engaged (D3 → Application + Counter-arguments + Writing-lite; D2 → Issue + priority).

## 4. The second-half doctrine (what D3 drills)

Distilled from `Grill/CL1_Contract/IRAC Rubrics.md` + Prof Yeo's graded feedback (all quotes in `references/recon-notes.md` §2):

- **Threshold first** — state the standard ("deprive of substantially the whole benefit"; "de minimis"; "radical difference"; "legitimate interest") before applying it.
- **Floor/ceiling calibration** — for degree standards: the most serious case *below* the line vs the least serious case *above* it; compare material facts; place the present facts in the range. (Rubric: "the most severe case that falls below the threshold (the floor) + the least severe case that passed the threshold (the ceiling)").
- **Analogy/distinction plumbing** — principle → the precedent facts that matter → present facts → *why* they match or differ. Do not assert similarity; demonstrate it.
- **Complex R ↔ complex A** — contested rules get unpacked facts; clear-cut rules stay succinct.
- **Counter-arguments, fairly** — acknowledge adverse authority, then explain why it is distinguishable/limited/outweighed.
- **One landing per issue; no prevarication** — consider alternatives, then commit ("DON'T PREVARICATE… make sure there is only one point of contract formation… MUST SUFFICIENTLY CONSIDER ALTERNATIVE PERSPECTIVES").
- **Promise-by-promise / act-vs-promise** discipline in consideration ("Consideration MUST BE ANALYSED PROMISE BY PROMISE"; "DISTINGUISH CLEARLY BETWEEN ACT AND PROMISE").
- **Scope-of-promise framing for PE** (High Trees: the short answer was the *scope* of the promise — wartime conditions — not the elements).
- **No fruitless arguments, no repetition across parts, time economy** ("WHY WOULD THE EXAMINER ALLOCATE MARKS TO ISSUES YOU HAD ALREADY DISCUSSED IN OTHER PARTS?").
- **Judges' language standard** — "aspire to how judges use legal language"; where SG law is silent and an English case exists, reference it.

## 5. Language bank (fast, precise phrasing — full samples in `references/recon-notes.md` §4)

- **Issue:** "The issue is whether…" · "It must first be considered whether…"
- **Rule:** "The general rule is that…" · "As held in [case]…" · "s [X] of the [Act] provides that…" · "Following [case], …"
  - **Banned:** "Taking authority from [case]" — a marker explicitly flagged this; use "rely on the authority of", "following the decision of", "applying the reasoning in".
- **Application:** "On the facts, …" · "Applying [case], …" · "This is analogous to [case], where… / distinguishable from [case], where…" · "The present facts sit between [A] and [B]; they are closer to [B] because…"
- **Conclusion:** "Therefore, it is likely that…" · "[X] should be advised that…" · "The court will likely find…"
- **Calibration:** "It is arguable that… however…" — then commit. Avoid stacked, unjustified hedges.
- Polish senior stems when borrowing (e.g., "unlikely to be deemed de-minimis" → "is not plainly de minimis").

## 6. Session procedure

1. Load this skill → read `Grill/CL1_Contract/error-ledger.md` (recurring errors set today's priorities).
2. Pick the drill (user's choice; default rotation: D3 → D4 → targeted fixes → D6).
3. **Separate chat** (user's standing instruction) + attempts saved verbatim to `Grill/CL1_Contract/attempts/`; real timers; answers typed — that is the point.
4. Mark per §3; update the ledger; propose the next drill.
5. If practice produces a better formulation of a summary block, **propose it** — never edit the summaries unilaterally (exam-day materials).

### 6.1 Error ledger (`Grill/CL1_Contract/error-ledger.md`)
Columns: date · drill · topic · error · correct move · fix drill · status. Plus a "phrase upgrades" table. Terse. **Same error twice = stop and drill it to death.**

## 7. Toolkit (regenerate the parsed corpus — temp dirs are ephemeral)

- **docx → txt (macOS, local):** `find "<seniors dir>" -name "*.docx" ! -name "~\$*"` → `textutil -convert txt -output <out>.txt <file>`; flatten paths (`s|/|__|g`).
- **PDF → text (local only, via Miyo):** `sh .opencode/skills/miyo-parse/miyo-parse.sh "<file.pdf>" > out.txt`. No OCR — scanned papers return "no extractable text"; report, don't retry.
- Never send PDFs to cloud parsers (Miyo = the user's local-processing choice).

## 8. Boundaries, honesty, continuity

- Senior materials: different prof ⇒ **insights only**; phrasing transfers, substance must be checked against the user's summaries/Phang; the files themselves warn against treating them as a textbook.
- Do not redo the recon: the distillation lives in `references/recon-notes.md`; go to source files only for a specific deeper dive.
- **Continuity script:** *"This is a GRILL session. Load the `exam-grill-pipeline` skill, then [drill type] on [topic]."*
- **Build state (as at 12 Oct 2026):** summaries complete (Wks 1–4, 7); seniors corpus converted & sampled; papers parsed 2007–2022 (scans list §1C); ledger created (empty); first session pending — suggested opening: D2 + D3 on a recent paper, then D4 on AY2021-22 or AY2022-23 (subject to scope check).
- Related skills: `exam-summary-pipeline` (§12 links here) · `crl-exam-summary-pipeline` (criminal summaries) · **`crl-exam-grill-pipeline`** (criminal grill — the sibling of this skill; same philosophy, case-first centre of gravity).
