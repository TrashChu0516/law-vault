---
type: system
area: tools
created: 2026-08-26
---

# Tag Taxonomy — Controlled Vocabulary

> **The single source of truth for every legal tag in this vault.**
> **Rule: tag only from this list.** A new tag requires a new outline reference — never invent one.
> Maintained by **Clawclaw** (organizational tags). **Steven** owns ratio/obiter tagging.

## How the system works (3 layers, 2 owners)

| Layer          | Where it lives                                                                    | Owner    |
| -------------- | --------------------------------------------------------------------------------- | -------- |
| Properties     | frontmatter: `module` · `week` · `jurisdiction` · `court` · `citation` · `status` | Clawclaw |
| Doctrine tags  | frontmatter `tags:` array (nested)                                                | Clawclaw |
| Ratio / obiter | inline bullets: `… #key-principle/…` and `… #obiter`                              | Steven   |
|                |                                                                                   |          |

## Tag convention

- Nested with `/` — module first, then **area**, then outline **section**.
- **Every case carries its area tag + its most-specific outline-section tag.** A landmark case cited across seminars carries **multiple** tags.
- `topic` (coarse) mirrors the area; `tags` (fine) is authoritative for filtering.
- The "quality check" (`_tools/librarian.md`) flags any tag not in this list, or any case with no tags.

---

## CL1 — Contract Law 1

Source: Week 1 – Week 4 seminar outlines.

### Area `cl1/formation` — Week 1 (formation)

| Tag | Outline section |
|-----|-----------------|
| `cl1/formation` | (area) |
| `cl1/formation/objective-approach` | §2 The Objective Approach |
| `cl1/formation/offer` | §3 Offer and Acceptance (battle of the forms) |
| `cl1/formation/acceptance` | §3 Offer and Acceptance (general) |
| `cl1/formation/acceptance/knowledge` | §3 Knowledge of the offer |
| `cl1/formation/acceptance/silence` | §3 Method of acceptance |
| `cl1/formation/acceptance/unilateral` | §3 Acceptance and unilateral contracts |
| `cl1/formation/acceptance/conduct` | §3 Subsequent conduct |
| `cl1/formation/acceptance/postal-rule` | §3 Postal acceptance |
| `cl1/formation/acceptance/instantaneous` | §3 Instantaneous communications |
| `cl1/formation/acceptance/electronic` | §3 Contracts and electronic communications |
| `cl1/formation/tenders-auctions` | §3 Special cases: tenders and auctions |

### Area `cl1/certainty` — Week 2 (certainty & completeness)

| Tag | Outline section |
|-----|-----------------|
| `cl1/certainty` | (area) |
| `cl1/certainty/good-faith` | §B Agreements to negotiate in good faith |
| `cl1/certainty/subject-to-contract` | §C Agreements "subject to contract" |
| `cl1/certainty/curing` | §D Curing uncertainty and incompleteness |
| `cl1/certainty/restitution` | §E What can the court do if there is no contract |

### Area `cl1/intention` — Week 2 (intention to create legal relations)

| Tag | Outline section |
|-----|-----------------|
| `cl1/intention` | (area) |
| `cl1/intention/family` | §B Family and social arrangements |
| `cl1/intention/commercial` | §C Commercial arrangements |
| `cl1/intention/letters-of-comfort` | §D Letters of comfort and intent |

### Area `cl1/consideration` — Week 3 (consideration)

| Tag | Outline section |
|-----|-----------------|
| `cl1/consideration` | (area) |
| `cl1/consideration/past` | §1 Past consideration |
| `cl1/consideration/move` | §1 Consideration must "move" from the promisee |
| `cl1/consideration/sufficiency` | §1 Sufficiency and adequacy of consideration |
| `cl1/consideration/pre-existing-duty` | §1 Pre-existing duties |
| `cl1/consideration/variation` | §1 Variation of contracts (increasing pacts) |
| `cl1/consideration/decreasing-pact` | §1 Variation — decreasing pacts |

### Area `cl1/promissory-estoppel` — Week 3 (promissory estoppel)

| Tag | Outline section |
|-----|-----------------|
| `cl1/promissory-estoppel` | (area) |
| `cl1/promissory-estoppel/origin` | §2 Meaning and origin |
| `cl1/promissory-estoppel/promise` | §2 Elements — clear and unequivocal promise |
| `cl1/promissory-estoppel/reliance` | §2 Elements — reliance |
| `cl1/promissory-estoppel/detriment` | §2 Elements — detriment and inequitability |
| `cl1/promissory-estoppel/effect` | §2 Effect — suspend or extinguish rights |
| `cl1/promissory-estoppel/no-cause` | §2 Cannot found a new cause of action |

### Area `cl1/privity` — Week 3 (privity overview)

| Tag | Outline section |
|-----|-----------------|
| `cl1/privity` | §3 Privity (overview — detailed in Term 2) |

### Area `cl1/terms` — Week 4 (express terms)

| Tag | Outline section |
|-----|-----------------|
| `cl1/terms` | (area) §1 Express terms |
| `cl1/terms/representation` | §1 Distinguishing express terms from misrepresentations |
| `cl1/terms/incorporation` | §1 Incorporation of express terms |
| `cl1/terms/incorporation/signature` | §1 Incorporation by signature |
| `cl1/terms/incorporation/notice` | §1 Incorporation by notice |
| `cl1/terms/incorporation/course-of-dealing` | §1 Previous course of dealing |
| `cl1/terms/entire-agreement` | §1 Preventing incorporation — entire agreement clauses |
| `cl1/terms/parol-evidence` | §1 Issues of proof — the parol evidence rule (common law + Evidence Act ss 93–94) |
| `cl1/terms/interpretation` | §1 The interpretation of express terms |
| `cl1/terms/interpretation/contextual` | §1 Taking a contextual approach (Evidence Act s 94 proviso (f), ss 95–100) |
| `cl1/terms/interpretation/post-contract` | §1 Post-contractual behaviour |
| `cl1/terms/interpretation/canons` | §1 Canons of interpretation |

### Area `cl1/implied-terms` — Week 4 (implied terms)

| Tag | Outline section |
|-----|-----------------|
| `cl1/implied-terms` | (area) §2 Implied terms |
| `cl1/implied-terms/fact` | §2 Terms implied in fact |
| `cl1/implied-terms/law` | §2 Terms implied in law |
| `cl1/implied-terms/custom` | §2 Terms implied by custom and usage |
| `cl1/implied-terms/statute` | §2 Terms implied by statute (e.g. Sale of Goods Act ss 12–14) |

### Area `cl1/nom-clauses` — Week 4 (no oral modification)

| Tag | Outline section |
|-----|-----------------|
| `cl1/nom-clauses` | §3 Agreements not to orally modify contract terms |

### Area `cl1/terms/exception-clauses` — Week 7 (exception clauses, common law)

Source: Week 7 seminar outline — "Terms of the contract (ii): the regulation of terms".

| Tag | Outline section |
|-----|-----------------|
| `cl1/terms/exception-clauses` | § the common law approach to exception clauses — exclusion vs limitation, nature and purpose |
| `cl1/terms/exception-clauses/incorporation` | § incorporation (signature; notice; course of dealing) |
| `cl1/terms/exception-clauses/interpretation` | § interpretation, including *contra proferentem* and the *Canada Steamship* approach |
| `cl1/terms/exception-clauses/collateral-contracts` | § inconsistent terms and collateral contracts |
| `cl1/terms/exception-clauses/fundamental-breach` | § fundamental breach — "rule of law" vs "rule of construction" |

### Area `cl1/ucta` — Week 7 (Unfair Contract Terms Act 1977)

| Tag | Outline section |
|-----|-----------------|
| `cl1/ucta` | § UCTA overview — the triggers for application and the consequences |
| `cl1/ucta/applicability` | § applicability; "business liability" (ss 1(3), 14) |
| `cl1/ucta/negligence-pi-death` | § exclusions relating to negligence, personal injury and death (ss 1, 2, 14) |
| `cl1/ucta/s3` | § exclusions of other liability arising in contract (s 3) |
| `cl1/ucta/consumer` | § dealing as a "consumer" |
| `cl1/ucta/standard-form` | § written standard terms of business |
| `cl1/ucta/reasonableness` | § the test of reasonableness (s 11, Sch 2) — burden of proof, judicial approaches, relative bargaining power, negotiations or protest, availability of a reasonable alternative, public policy |

### Area `cl1/cpfta` — Week 7 (Consumer Protection (Fair Trading) Act)

| Tag | Outline section |
|-----|-----------------|
| `cl1/cpfta` | § CPFTA overview — who may seek relief, against whom, the prescribed limit, "consumer" |
| `cl1/cpfta/unfair-practices` | § unfair practices (s 4; Sch 2 "specific unfair practices") |
| `cl1/cpfta/remedies` | § remedies (ss 6, 8) — damages and other relief |
| `cl1/cpfta/s9-injunction` | § s 9 — injunction against a supplier (CCCS enforcement) |

### Area `cl1/performance` — Week 9 (discharge by performance)

Added 2026-10-13 with the Week 9 outline and slides. Sections follow the seminar
outline's own headings; the fine children follow the *issues* the slides work
through, because that is what a problem question turns on.

| Tag | Outline / slide section |
|-----|-------------------------|
| `cl1/performance` | (area) |
| `cl1/performance/standard` | § Discharge by performance: starting-point — full and precise compliance; strict vs relative compliance |
| `cl1/performance/de-minimis` | § *de minimis* breach (*Arcos v EA Ronaasen*) |
| `cl1/performance/personal-performance` | § Who can perform? — must the promisor perform personally? |
| `cl1/performance/tender` | § Defence of tender — tender of performance (*Startup v MacDonald*) |
| `cl1/performance/independent` | § Independent obligations |
| `cl1/performance/interdependent` | § Interdependent obligations — conditions precedent / subsequent |
| `cl1/performance/concurrent-terms` | § Concurrent terms — Sale of Goods Act 1979, s 28 |
| `cl1/performance/entire-obligations` | § Entire and divisible obligations — entire obligations (*Cutter v Powell*, *Sumpter v Hedges*) |
| `cl1/performance/divisible-obligations` | § Entire and divisible obligations — divisible obligations (*Tong Aik*) |
| `cl1/performance/substantial-performance` | § Substantial performance (*Hoenig v Isaacs*, *Bolton v Mahadeva*, *San International*) |
| `cl1/performance/quantum-meruit` | § Responses to entire obligations — new collateral contract / *quantum meruit* (*Eng Chiet Shoong*, *Tong Aik*) |

> **Why `substantial-performance` is its own tag rather than folding into
> `entire-obligations`.** The slides treat "is this obligation entire?" and "has
> there been substantial performance?" as two *separate* questions — the first a
> matter of construction, the second a question of fact about proportionality and
> purpose (*Bolton v Mahadeva*) or overall effect (*San International*). A problem
> answer can turn on either, so they are tagged apart.

---

### Area `cl1/frustration` — Week 9 (the triggers for frustration)

Added 2026-10-13 with `week 9 Reading List - Triggers for Frustration`. Fine
children follow **the reading list's own headings**, because the triggers are
taught as a list of categories.

| Tag | Reading-list section |
|-----|----------------------|
| `cl1/frustration` | (area) |
| `cl1/frustration/nature` | § the nature of frustration — the construction/radical-difference approach |
| `cl1/frustration/force-majeure` | § frustration **vs** a force majeure clause — whether the clause excludes the doctrine |
| `cl1/frustration/supervening-illegality` | § supervening illegality (*Metropolitan Water Board v Dick Kerr*) |
| `cl1/frustration/impossibility` | § supervening impossibility (Part C) |
| `cl1/frustration/destruction-of-subject-matter` | § destruction of subject-matter (*Taylor v Caldwell*) |
| `cl1/frustration/unavailability` | § unavailability of subject-matter (19.037–19.038) |
| `cl1/frustration/failure-of-supply` | § failure of supply (*Alliance Concrete*, [47]–[57]) |
| `cl1/frustration/impossible-method` | § impossible method of performance (*Tsakiroglou*, *Holcim* [63]) |
| `cl1/frustration/death-incapacity` | § death or incapacity (19.035–19.036) |
| `cl1/frustration/delay` | § temporary delay (*Metropolitan Water Board v Dick Kerr*) |
| `cl1/frustration/impracticability` | § supervening impracticability (*Davis Contractors*, *Glahe* [42]) |
| `cl1/frustration/purpose` | § frustration of purpose (*Krell v Henry*, *Herne Bay*, *Shenyin Wangou* [14]–[15]) |
| `cl1/frustration/obstacles` | § obstacles to frustration (Part E) — foreseeability |
| `cl1/frustration/self-induced` | § self-induced frustration (*Maritime National Fish*, *The Super Servant Two*) |
| `cl1/frustration/consequences` | § **consequences** at common law — prospective discharge, total failure of consideration (*Chandler*, *Fibrosa*, *Appleby*, *Whincup*) — ch 19 Part D §1 |
| `cl1/frustration/statutory-adjustment` | § the **Frustrated Contracts Act 1959** — s 2(2)–(3) money, s 2(4) valuable benefit (*Lim Kim Som*, *Gamerco*, *BP v Hunt*) — ch 19 Part D §2 |

### `cl1/agreement` — discharge by agreement (Week 10 §2.2)

| Tag | Maps to |
|---|---|
| `cl1/agreement` | (area) |
| `cl1/agreement/subsequent-agreement` | § discharge or variation of a prior agreement by a later one — consideration for the second agreement; Evidence Act s 94(d); Civil Law Act s 6 |

> **Why `nature` and `force-majeure` are separate.** The Singapore cases on this
> list reach frustration mostly through a **force majeure clause** rather than the
> doctrine (*RDC Concrete*, *Holcim*, *Glahe*), so the first question in a problem
> is usually whether the clause displaces the doctrine at all. That is a distinct
> analytical step from the "radical difference" test, hence a distinct tag.

---

## CRL — Criminal Law

Source: LAW103 course outline, **weekly lesson plan**. ⚠️ This prof gives **no weekly seminar outlines**, so tags derive from the course outline's weekly *topics* (and will gain fine children as each week's cases land).

| Area tag | Week | Topics |
|----------|------|--------|
| `crl/foundations` | 1 | Overview, criminal justice system, jurisdiction/territoriality, IRAC |
| `crl/punishment` | 2 | Aims of punishment, prosecutorial discretion, sentencing |
| `crl/elements` | 3–4 | Anatomy of a crime: actus reus, mens rea, strict liability, causation, omissions |
| `crl/property-offences` | 5 | Theft (s 378), misappropriation, CBT, forgery, cheating |
| `crl/sexual-offences` | 6 | Outrage of modesty, sexual assault by penetration, rape |
| `crl/defences` | 7 | Mistake of fact, accident, unsound mind, intoxication, consent, necessity, duress, private defence |
| `crl/homicide` | 9–10 | Murder, culpable homicide, causing death by rash/negligent act, dangerous driving |
| `crl/parties` | 11–12 | Common intention, abetment, conspiracy, attempts |

### CRL fine children (confirmed as each week's cases land)

- `crl/elements/actus-reus` · `crl/elements/mens-rea` · `crl/elements/strict-liability` · `crl/elements/causation` · `crl/elements/omissions`
- **Week 5** — `crl/property-offences/theft` · `crl/property-offences/misappropriation` · `crl/property-offences/cbt` · `crl/property-offences/forgery` · `crl/property-offences/cheating` · `crl/property-offences/criminal-intimidation` · `crl/property-offences/robbery` *(added with Kho Jabing / Daniel Vijay, Weeks 10–11 — robbery as the ulterior offence a common intention attaches to)*
- **Week 6** — `crl/sexual-offences/outrage-of-modesty` · `crl/sexual-offences/sexual-assault` · `crl/sexual-offences/rape`
- **Week 7** — `crl/defences/mistake-of-fact` · `crl/defences/accident` · `crl/defences/unsound-mind` · `crl/defences/intoxication` · `crl/defences/consent` · `crl/defences/necessity` · `crl/defences/duress` · `crl/defences/private-defence`
- **Weeks 9–10 (homicide)** — `crl/homicide/murder` · `crl/homicide/culpable-homicide` · `crl/homicide/rash-negligent` · `crl/homicide/s300c`
  - `crl/homicide/s300c` is the **s 300(c) limb** (intention to cause bodily injury sufficient in the ordinary course of nature to cause death). It recurs across the homicide set (Mohammed Ali, Lim Poh Lye, Sundarti, Tan Joo Cheng, Daniel Vijay, Azlin) and the courts treat its interpretation as its own question — hence its own tag rather than folding into `murder`.
  - The three **partial defences / s 300 exceptions** carry their own tags because they are pleaded *independently* of the general defences and each has its own test: `crl/defences/provocation` (Exception 1) · `crl/defences/sudden-fight` (Exception 4) · `crl/defences/diminished-responsibility` (Exception 7) · `crl/defences/exceeding-private-defence` (Exception 2, ss 98–99).
- **Weeks 10–11 (parties)** — `crl/parties/abetment` · `crl/parties/common-intention` · `crl/parties/conspiracy` · `crl/parties/attempts`


---

## Future modules (reserve the namespace, add when the outline exists)

- `tort/…` — Tort Law
- `sls/…` — Singapore Legal System
- `lrw/…` — Legal Research & Writing
