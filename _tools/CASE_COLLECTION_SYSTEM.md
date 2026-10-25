---
type: system
area: case-collection
created: 2026-08-16
status: live
---

# Case Collection System — Architecture & Pipeline

> **How we turn "hundreds of PDFs" into a searchable, wiki-linked, database-backed case library.**

---

## 1. The Architecture Decision: ONE vault, not two

**Decision: cases live in the SAME vault, under `cases/<module>/`.**

| Option | Verdict | Why |
|--------|---------|-----|
| Separate case vault | ❌ Rejected | Breaks `[[wikilinks]]` (cross-vault linking needs absolute paths/plugins); fragments the graph; a case can't cleanly link to its doctrine block, statute, and outline. |
| **Same vault, `cases/<module>/`** | ✅ **Chosen** | Single source of truth. A case → links to its LEGO block → links to the statute → links to the outline, all in one graph. Dataview queries span *all* modules. |

**Folder layout:**
```
cases/
├── CASE_INDEX.md          ← Dataview-powered master index (database-like)
├── CL1_Contract/          ← Contract Law 1 cases
├── CRL_Criminal/
├── LRW/
└── SLS/
```

**Why this gives a material advantage over Google Docs:** every case note has structured YAML frontmatter (citation, court, topic, module, decision date, coram). Dataview then turns the whole collection into a *queryable database* — "show me every Court of Appeal case on formation, sorted by date" — which is impossible in Google Docs.

---

## 2. Naming Convention (critical for wikilinks + sorting)

```
Case Name v Case Name [Year] SGHC 123.md
```
Examples:
- `Chwee Kin Keong v Digilandmall.com Pte Ltd [2004] SGHC 71.md`
- `Gay Choon Ing v Loh Sze Ti Terence Peter [2009] SGCA 45.md`

Rules:
- Full party names (so `[[wikilink]]` from the outline resolves unambiguously).
- Neutral citation in square brackets (stable identifier).
- One case = one file.

---

## 3. The Conversion Pipeline (faithful, not summarised)

| Jurisdiction | Source | Method | Status |
|--------------|--------|--------|--------|
| **Singapore** | [elitigation.sg](https://www.elitigation.sg) (official, Government of Singapore) | `_tools/elitigation_to_md.py <url> <out.md>` — raw HTML → faithful MD (headings, numbered paragraphs `[n]`, quotes, metadata) | ✅ **Working** |
| **UK / Commonwealth** | BAILII | bot-protected for scripted download; fetch per-case | ⚠️ needs workaround |
| **Australia** | AustLII | 403 on scripted download | ⚠️ needs workaround |
| **Pre-1890 cases** | Old law reports (scanned only) | No free full text → **preserve original PDF/scan** | ⚠️ archive-only |

**The integrity rule:** the MD must be a faithful rendering of the authentic judgment — headings, paragraphs, footnotes, and citations preserved. If a source is a low-quality scan, we keep the **original file** and link to it, rather than transcribe a degraded copy.

---

## 4. Plugin Evaluation (install only what earns its place)

| Plugin | Verdict | Why |
|--------|---------|-----|
| **Dataview** | ✅ **Install (essential)** | Database-like queries over every note's frontmatter. Turns the case folder into "quick as a database". E.g. `TABLE decision_date, coram FROM "cases/CL1_Contract" WHERE topic = "formation" SORT decision_date ASC`. |
| **Templater** | ✅ **Install (essential)** | Auto-insert the case-brief / block / statute templates when you create a note. Kills tedious boilerplate. |
| **Obsidian Git** | ✅ **Install (recommended)** | Automatic version history + backup of the vault. Protects your work; aligns with the integrity theme. |
| Advanced Tables | 🟡 Optional | Nicer table editing (you'll have many tables). |
| Linter | 🟡 Optional | Enforces consistent formatting across notes. |
| Footnotes Shortcut | 🟡 Optional | Faster footnote insertion (case briefs use footnotes). |

**Install steps** (in Obsidian): Settings → Community plugins → Browse → search "Dataview" / "Templater" / "Obsidian Git" → Install → Enable. (I'll write the Dataview/Templater config once you've enabled them.)

---

## 5. The Source Map (case → authentic source)

### Singapore (elitigation.sg — converting now)
| Case | Neutral citation | URL |
|------|------------------|-----|
| Chwee Kin Keong v Digilandmall.com | [2004] SGHC 71 | ✅ converted |
| Chwee Kin Keong v Digilandmall.com (CA) | [2005] SGCA 2 | elitigation.sg/gd/s/2005_SGCA_2 |
| Gay Choon Ing v Loh Sze Ti | [2009] SGCA (verify #) | to locate |
| Tribune Investment v Soosan Trading | [2000] (verify #) | to locate |
| Jiangsu Overseas v Concord Energy | [2016] SGCA (verify #) | to locate |
| Aircharter World v Kontena Nasional | [1999] SGCA (verify #) | to locate |
| Midlink Development v Stansfield | [2004] (verify #) | to locate |
| 1L30G v EQ Insurance | [2017] SGHC (verify #) | to locate |

### UK / Commonwealth (BAILII)
Smith v Hughes (1871) · Centrovincial Estates [1983] · Hartog v Colin & Shields [1939] · Felthouse v Bindley (1862) · Errington v Errington [1952] · Daulia Ltd [1978] · Soulsbury v Soulsbury [2007] · Holwell Securities v Hughes [1974] · Entores v Miles Far East [1955] · Brinkibon v Stahag Stahl [1983] · Blackpool & Fylde [1990] · Harvela Investments [1985] · Barry v Davies [2000] · Solle v Butcher [1950] · The Hannah Blumenthal [1983] · DAZN v Coupang [2025]

### Australia (AustLII)
R v Clarke (1927) 40 CLR 227

### Pre-1890 — no free full text (preserve original scans)
Tinn v Hoffman (1873) · Gibbons v Proctor (1891) · Williams v Carwardine (1833)

---

## 6. Status & Next Steps

- ✅ Pipeline built and proven (Chwee Kin Keong HC converted).
- ⏳ Remaining Singapore cases: locate neutral citations → batch-convert.
- ⏳ UK cases: solve BAILII fetch (per-case WebFetch or manual download → run through a BAILII converter).
- ⏳ Pre-1890 cases: source scanned originals from the library → store as PDF in `_course_outlines` or `cases/_originals/`.

---

*← [[000_HOME|Home]] · [[_research/RESEARCH_HUB|Research Hub]]*
