---
type: research
area: case-finding-pipeline
source: "SMU 'How do I Locate Case Law?' — 'Which database to use?' + empirical findings"
source_url: "https://researchguides.smu.edu.sg/c.php?g=421855&p=2881184"
created: 2026-08-16
status: live
---

# Case-Finding Pipeline — the automated research spine

> **The school's routing logic, captured + automated.** Given a citation, this is the full path from "weird abbreviation" → "faithful MD in the vault."

---

## 0. The Routing Decision Tree (from SMU's guide)

```
CITATION  e.g. "Scruttons Ltd v Midland Silicones [1962] AC 446"
   │
   ▼
1. DECODE the abbreviation  →  Cardiff Index (legalabbrevs.cardiff.ac.uk)
   ("AC" = Law Reports, Appeal Cases, UK, from 1891)
   │
   ▼
2. IDENTIFY jurisdiction + time period
   │
   ├─ Singapore  ──────────────► LawNet (login) · elitigation.sg (free, 2000+) · Law Watch
   ├─ UK, post-1865  ─────────► BAILII (free) · LawNet/Westlaw/Lexis (login)
   ├─ UK, pre-1865  ──────────► HeinOnline "English Reports" (login) · CommonLII EngR (free)
   ├─ Australia  ─────────────► AustLII
   ├─ India  ─────────────────► Manupatra (login)
   ├─ China  ─────────────────► Chinalawinfo (login)
   ├─ Malaysia  ──────────────► CLJ Law (login)
   └─ US / Int'l ─────────────► Westlaw / HeinOnline / Oxford Reports
```

---

## 1. What I've already automated (no login needed)

| Jurisdiction | Source | Method | Status |
|--------------|--------|--------|--------|
| Singapore | elitigation.sg | `_tools/elitigation_to_md.py` (curl → MD) | ✅ 6 cases done |
| UK (modern + old) | BAILII | Playwright browser (`--headed`, Anubis bypass) → `[n]` paragraph markers | ✅ DAZN, Soulsbury done |

**Converter handles both elitigation formats**: `<p class="Judg-N">` (2004/2009) and `<div class="Judg-N">` (2016/2017). Pre-2000 SG judgments only exist as PDF → `pdftotext`.

---

## 2. BAILII old-case discovery (corrects earlier assumption)

BAILII **does** have pre-1996 English cases — under a different URL scheme (`J`-numbers):

| Case | BAILII URL |
|------|-----------|
| Felthouse v Bindley (1862) 11 CB(NS) 869 | `/ew/cases/EWHC/CP/1862/J35.html` |
| Adams v Lindsell (1818) 1 B & Ald 681 | `/ew/cases/EWHC/KB/1818/J59.html` |
| Entores v Miles Far East [1955] 2 QB 327 | `/ew/cases/EWCA/Civ/1955/3.html` |

> To find a case's BAILII URL reliably: **title search** (`search_by_title.html`) rather than guessing the path. `Smith v Hughes` (1871) returns only 4 *modern* "Smith-Hughes" cases → that one appears genuinely absent from BAILII.

**The likely gaps that DO need login / manual:**
- `Smith v Hughes` (1871) — not found on BAILII title search → Westlaw/Lexis/LawNet or casebook extract.
- Pre-1865 scanned reports → HeinOnline "English Reports, Full Reprint (1220–1865)".

---

## 3. What login unlocks (tell me what you'll share)

| Resource | Login | What it gets us |
|----------|-------|-----------------|
| **LawNet** (lawnet.com) | SMU account | SG cases pre-2000 (Aircharter 1999), UK Law Reports (ICLR), **note-up citator** (is a case still good law?) |
| **HeinOnline English Reports** | SMU account (libproxy) | Pre-1865 scanned reports (page images) |
| **Westlaw / Lexis Advance** | SMU account | UK cases not on BAILII (e.g. Smith v Hughes), KeyCite/Shepard's note-up |

> ⚠️ I won't store plaintext passwords in the vault. When you share SMU/SAL access, I'll use it per-session — ideally you authenticate once in the ego-browser/Playwright browser and I continue.

---

## 4. Firecrawl — evaluation

| Aspect | Verdict |
|--------|---------|
| What it is | "Context API" → URL/search → clean markdown/structured data for LLMs. Open-source (AGPL) + cloud (paid API). |
| Self-host | Docker + FoundationDB (heavy). |
| Cloud | Sign up at firecrawl.dev → API key → pay per use. |
| MCP | `npx -y firecrawl-mcp` with `FIRECRAWL_API_KEY`. |
| **Verdict for us** | **Redundant for now.** My Playwright CLI already turns BAILII/elitigation into faithful MD for free, no API key. Firecrawl would add value only at scale (hundreds of URLs) or for messy JS sites — and even then, Anubis's proof-of-work may still block its headless engine. Revisit if we ever crawl entire report series. |

---

## 5. The automation target (end state)

```
outline lists a case
   → decode citation (Cardiff Index)
   → route by jurisdiction+date (tree above)
   → fetch (elitigation curl / BAILII browser / LawNet login / HeinOnline scan)
   → convert to faithful MD (converter + paragraph markers)
   → add frontmatter (citation, court, topic, coram) + alias
   → link resolves in outline · Dataview indexes it · note-up status appended
```

Steps already automated: fetch (SG + BAILII) + convert + metadata + linking. **Remaining:** the login-gated sources + note-up citator.

---

*← [[_research/RESEARCH_HUB|Research Hub]] · [[_tools/BROWSER|Browser tooling]] · [[_tools/CASE_COLLECTION_SYSTEM|Case Collection System]]*
