#!/usr/bin/env python3
"""lawnet_to_md.py — convert a raw LawNet judgment dump into a vault case note.

Input : the plain-text dump produced by ln_fetch.js (body.innerText of a LawNet
        judgment page).
Output: a Markdown note in this vault's house format — frontmatter, a metadata
        header, the editorial headnote (Catchwords / Facts / Held), and the
        judgment body with paragraph numbers normalised to `**[n]**`.

Usage:
    python3 _tools/lawnet_to_md.py <raw.txt> <out.md> [--module CRL] [--week 7]

Why LawNet and not eLitigation: eLitigation serves abridged text for a number of
judgments (paragraph numbers present, bodies empty) and nothing on the page says
so. LawNet gives the full text with pinpoints and the note-up status.
"""
import argparse
import os
import re
import sys

CITE_RE = re.compile(r'^\[\d{4}\]\s+\S')                    # "[2008] SGCA 32"
# The citation line carries one or more citations separated by "·"
# (e.g. "[2008] 4 SLR(R) 306 · [2008] SGCA 32"). A case reported only by its
# neutral citation has no separator at all, so match on the citation itself and
# take the case name from the line above.
NOTEUP_RE = re.compile(r'^(\d+)\s+(Followed|Distinguished|Overruled|Not Followed|Referred)$')
PARA_RE = re.compile(r'^(\d{1,3})\s+(\S.*)$')
KNOWN_LABELS = ['Decision Date', 'Court/Tribunal', 'Jurisdiction', 'Coram',
                'Judge', 'Counsel', 'Parties', 'Case Number']


def norm_ws(s):
    return re.sub(r'[ \t]+', ' ', s).strip()


def parse(raw):
    lines = [l.rstrip() for l in raw.split('\n')]

    # ---- locate the header: the citation line, name on the line above ------
    h = next((i for i, l in enumerate(lines)
              if CITE_RE.match(l.strip()) and i > 0 and lines[i - 1].strip()
              and not CITE_RE.match(lines[i - 1].strip())), None)
    if h is None:
        raise SystemExit('could not find the citation line — is this a judgment page?')
    d = {'case_name': norm_ws(lines[h - 1]), 'cite_line': norm_ws(lines[h])}

    i = h + 1
    # ---- note-up ----------------------------------------------------------
    counts = {}
    while i < len(lines) and NOTEUP_RE.match(lines[i].strip()):
        m = NOTEUP_RE.match(lines[i].strip())
        counts[m.group(2)] = int(m.group(1))
        i += 1
    d['note_up'] = counts

    # ---- Details block ----------------------------------------------------
    while i < len(lines) and lines[i].strip() != 'Details':
        i += 1
    i += 1
    meta = {}
    while i < len(lines):
        s = lines[i].strip()
        if s == 'Catchwords':
            break
        if s in KNOWN_LABELS and i + 1 < len(lines):
            v = norm_ws(lines[i + 1])
            # Coram and Counsel are multi-value lists LawNet welds together.
            if s in ('Coram', 'Counsel'):
                v = split_runon(v)
            meta[s] = v
            i += 2
            continue
        i += 1
    d['meta'] = meta

    # ---- Catchwords -------------------------------------------------------
    while i < len(lines) and lines[i].strip() != 'Catchwords':
        i += 1
    i += 1
    cw = []
    while i < len(lines) and lines[i].strip() not in ('Facts', 'Holdings', 'Judgments'):
        if lines[i].strip():
            cw.append(norm_ws(lines[i]))
        i += 1
    d['catchwords'] = clean_catchwords(cw)

    # ---- Facts (headnote) -------------------------------------------------
    facts = []
    j = next((k for k in range(h, len(lines)) if lines[k].strip() == 'Facts'), None)
    k2 = next((k for k in range(j + 1, len(lines)) if lines[k].strip() == 'Holdings'), len(lines)) if j is not None else None
    if j is not None:
        for l in lines[j + 1:k2]:
            if l.strip() and l.strip() != 'Facts':
                facts.append(norm_ws(l))
    d['facts'] = facts

    # ---- Holdings ---------------------------------------------------------
    # The judgment body begins at paragraph 1. Anchoring on that (rather than on
    # a "Judgments" heading, which some pages only show in the nav breadcrumb)
    # gives the holdings section a reliable end.
    j3 = next((k for k in range(max(j or h, h), len(lines)) if lines[k].strip() == 'Holdings'), None)
    p1 = next((k for k in range(j3 or h, len(lines)) if re.match(r'^1 \S', lines[k].strip())), None)
    held = []
    if j3 is not None:
        endh = p1 if p1 is not None else len(lines)
        for l in lines[j3 + 1:endh]:
            s = l.strip()
            if s and s != 'Holdings' and not s.startswith(('[Observation:', '[Editorial note:')):
                held.append(norm_ws(l))
    d['held'] = held

    # ---- the judgment body ------------------------------------------------
    if p1 is None:
        raise SystemExit('could not find paragraph 1 of the judgment')
    body = lines[p1:]
    jumps = [k for k, l in enumerate(body)
             if l.strip() == 'References' or l.strip().startswith('Reported by ')]
    if jumps:
        body = body[:min(jumps)]
    d['body'] = body

    # ---- note-up detail ---------------------------------------------------
    tail = lines[p1 + (min(jumps) if jumps else len(body)):]
    detail = {'referring': [], 'referred': [], 'legislation': []}
    labels = {'Later cases citing this case': 'referring',
              'Earlier cases cited by this case': 'referred'}
    cur = None
    for l in tail:
        s = l.strip()
        if s in labels:
            cur = labels[s]
            continue
        if s.startswith(('Referring (', 'Referred to (', 'Legislation (')):
            cur = 'legislation' if s.startswith('Legislation') else cur
            continue
        # any later "(n)" category header ends the legislation list; LawNet keeps
        # going with "Litigation (0)", "Other References (12)", book chapters…
        if re.match(r'^(Litigation|Other References|Journal Articles|Books|'
                    r'Practice Directions|Treaties)\b', s) or s.startswith('Chapter '):
            cur = None if cur == 'legislation' else cur
            continue
        if s in ('References', 'Info', 'View all', '') or s.startswith('Reported by '):
            continue
        if cur:
            detail[cur].append(s)
    d['detail'] = detail
    return d


def render_body(body):
    """Numbered paragraphs -> `**[n]**`; standalone short lines -> `###` headings.

    Paragraph numbers are accepted only in sequence. A judgment's own paragraphs
    run 1, 2, 3 … without jumping, so a line numbered far ahead of the expected
    value is not a paragraph of *this* judgment — it is a quotation of a
    paragraph of some other judgment (e.g. the court below), which LawNet renders
    oddly. Those are left as ordinary text instead of being given a false
    pinpoint. A tolerance of 2 absorbs an occasional paragraph that the page
    renders in a way the line pattern misses.
    """
    out, nums = [], []
    expected = 1
    date_re = re.compile(r'^\d{1,2}\s+(January|February|March|April|May|June|July|'
                         r'August|September|October|November|December)\b')
    for l in body:
        s = l.strip()
        if not s or s == '\t':
            out.append('')
            continue
        m = PARA_RE.match(s)
        is_para = False
        if m and not m.group(2).startswith(('...', '…')) and not date_re.match(s):
            n = int(m.group(1))
            # a paragraph may be very short ("2 In my judgment:") — accept the
            # expected number outright; allow a jump of 2 only for long lines,
            # which is what distinguishes a paragraph from a stray numbered item
            if n == expected or (expected < n <= expected + 2 and len(s) > 25):
                is_para = True
                expected = n + 1
                nums.append(n)
                out.append(f'**[{n}]** {m.group(2)}')
        if is_para:
            continue
        # a heading: short standalone line, not ending in sentence punctuation,
        # not itself a numbered paragraph
        if (len(s) < 90 and not s.endswith(('.', ';', ':', ',', '”'))
                and not re.match(r'^[\(\[]?\d', s)
                and len(s.split()) <= 12):
            out.append(f'### {s}')
            continue
        out.append(s)
    text = '\n'.join(out)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text, nums


def split_runon(s):
    """Break apart a run-on list LawNet renders without separators.

    LawNet puts each item of a multi-value field (Coram, Counsel) in its own
    element and the elements carry no whitespace between them, so innerText
    yields e.g. "Sundaresh Menon CJAndrew Phang Boon Leong JCAChao Hick Tin SJ"
    or "Foo Kim Thong SC (Foo & Co)Barry Tan (Barry LLP)".

    The seam is a judge's title token welded to the next name. The alternation
    MUST be atomic: without it the engine matches "JA", fails the lookahead
    because the next character is a space, then backtracks into the shorter "J"
    alternative and happily splits "JA" into "J · A".

    But atomicity has a cost, so the token list must be EXACT — a token that is
    a false prefix steals the seam and there is no backtracking to rescue it.
    "JT" was the culprit: in "… Lai Kew Chai J" + "Tay Yong Kwang J" the engine
    matched the bogus "JT", the lookahead failed on the "a" of "Tay", and with
    no backtrack the split was silently skipped. "JT" is not a Singapore
    judicial title and appears nowhere in the corpus, so it is removed. Any
    future addition to this list must be a real title.

    Residual limitation, by the same mechanism: a genuine "J" or "JA" title
    immediately followed by a name starting with the *same* letters (e.g. "JA" +
    "Andrew", which welds to "JAndrew") will be missed. Detect with:

        grep -rhoE "\\b(JCA|JAD|JA|JC|JJ|SJ|CJ|J)[A-Z][a-z]" cases/

    — a hit means a weld survived and needs fixing by hand.
    """
    if not s:
        return ''
    s = norm_ws(s)
    titles = r'(?>JCA|JAD|JA|JC|JJ|J|SJ|CJ)'
    s = re.sub(r'(?<![A-Z])' + titles + r'(?=[A-Z])', lambda m: m.group(0) + ' · ', s)
    s = re.sub(r'(?<=[A-Z]{2})(?=[A-Z][a-z])', ' · ', s)   # "... SC" + "Barry"
    s = re.sub(r'(?<=\))(?=[A-Z])', ' · ', s)              # "... (Firm)" + "Next"
    return s


def clean_catchwords(raw):
    """Tidy LawNet's catchword block.

    Two quirks: the headings are often welded together without spaces
    ("Criminal LawOffencesMurderGeneral Exceptions"), and the block carries
    LawNet-AI filler ("AI Summary", "Fact Score: …", a disclaimer) that is not
    part of the headnote. Split the welds on lower-to-upper boundaries and drop
    the filler.
    """
    skip = ('AI Summary', 'Catchwords', 'Disclaimer:')
    out = []
    for s in raw:
        s = norm_ws(s)
        if not s or s.startswith(skip) or s.startswith('Fact Score:'):
            continue
        if ' - ' not in s and '·' not in s and ' — ' not in s:
            s = re.sub(r'(?<=[a-z])(?=[A-Z])', ' · ', s)
        # LawNet also welds a headword to a following quoted phrase with no
        # whitespace: `... during robbery"Intention of causing bodily injury`.
        # Split BEFORE the opening quote, not after it — the quote belongs to
        # the phrase that follows. Requiring the quote to be glued to the
        # preceding character keeps a mid-sentence quotation intact
        # (`No reference to "beyond reasonable doubt" in judgment`).
        s = re.sub(r'(?<=\S)(?="[A-Z])', ' · ', s)
        out.append(s)
    return out


def group_citing(raw):
    """LawNet lists citing cases as date-line / name / citation / treatment."""
    recs, cur = [], []
    for s in raw:
        if '·' in s and re.match(r'^\d', s):
            if cur:
                recs.append(cur)
            cur = [s]
        elif cur is not None:
            cur.append(s)
    if cur:
        recs.append(cur)
    out = []
    for r in recs:
        date = r[0].split('·')[0].strip() if r else ''
        name = r[1] if len(r) > 1 else ''
        cite = r[2] if len(r) > 2 else ''
        how = r[3] if len(r) > 3 else ''
        out.append((name, cite, how, date))
    return out


def render_noteup(d, counts):
    lines = ['## Note-up', '']
    if counts:
        lines.append('**Counts:** ' + ' · '.join(f'{v} {k.lower()}' for k, v in counts.items()))
    else:
        lines.append('**Counts:** not shown')
    lines.append('')
    later = group_citing(d['detail'].get('referring', []))
    earlier = group_citing(d['detail'].get('referred', []))
    if later:
        lines += ['**Later cases citing this case**', '']
        lines += [f'- *{n}* {c} — {h} ({dt})' for n, c, h, dt in later]
        lines.append('')
    if earlier:
        lines += [f'**Earlier cases cited by this case:** {len(earlier)} recorded'
                  + (f' (e.g. *{earlier[0][0]}* {earlier[0][1]})' if earlier else ''), '']
    leg = [s for s in d['detail'].get('legislation', []) if s not in ('Singapore',)]
    if leg:
        lines += [f'**Legislation referred to:** {", ".join(dict.fromkeys(leg))[:220]}', '']
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('raw')
    ap.add_argument('out')
    ap.add_argument('--module', default='CRL')
    ap.add_argument('--week', default='')
    a = ap.parse_args()

    d = parse(open(a.raw, encoding='utf-8').read())
    body_md, nums = render_body(d['body'])
    gaps = [n for n in range(1, max(nums) + 1) if n not in nums] if nums else []

    cites = [c.strip() for c in d['cite_line'].split('·')]
    nu = d['note_up']
    nu_line = ' · '.join(f'{v} {k.lower()}' for k, v in nu.items()) if nu else ''

    fm = [
        '---',
        f'case_name: "{d["case_name"]}"',
        f'citation: "{cites[-1]}"',
    ]
    if len(cites) > 1:
        fm.append(f'reported: "{cites[0]}"')
    fm += [
        f'court: "{d["meta"].get("Court/Tribunal", "")}"',
        f'module: "{a.module}"',
        f'week: {a.week}' if a.week else 'week:',
        'jurisdiction: "SG"',
        f'decision_date: "{d["meta"].get("Decision Date", "")}"',
        f'coram: "{d["meta"].get("Coram", "")}"',
        'topic: []',
        'tags: []',
        f'note_up: "{nu_line}"',
        f'source: "https://www.lawnet.com/research"',
        'type: case',
        'status: fulltext',
        '---',
        '',
        f'# {d["case_name"]}',
        f'> {d["cite_line"]}',
        '',
        f'**Court:** {d["meta"].get("Court/Tribunal", "—")} · '
        f'**Decision Date:** {d["meta"].get("Decision Date", "—")} · '
        f'**Coram:** {d["meta"].get("Coram", "—")}',
        '',
        f'> **Note-up:** {nu_line or "not shown"}',
        '',
    ]
    fm += render_noteup(d, nu)
    fm += [
        '## In this note',
        '- [[#Exam version]] · [[#Case brief]] · [[#Pro Max]] · [[#Judgment]]',
        '',
        '## Exam version',
        '<!-- IRAC-ready recap. -->',
        '',
        '## Case brief',
        '<!-- Exam-venue version: ratio → facts → holding. -->',
        '',
        '## Pro Max',
        '<!-- The deep dive. Reading this ≈ reading the case. -->',
        '',
        '## Judgment',
        '',
        '> **Editorial headnote** (LawNet; not part of the judgment text).',
        '',
        '**Catchwords**',
        '',
    ]
    fm += ['- ' + c for c in d['catchwords']] if d['catchwords'] else ['*(none)*']
    fm += ['', '**Facts**', '', '\n\n'.join(d['facts']) if d['facts'] else '*(none)*']
    fm += ['', '**Held**', '', '\n\n'.join(d['held']) if d['held'] else '*(none)*']
    fm += ['', '---', '', body_md, '']

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, 'w', encoding='utf-8').write('\n'.join(fm))

    flag = '' if not gaps else f'  ⚠ gaps at {gaps[:12]}{"…" if len(gaps) > 12 else ""}'
    print(f'OK  {d["case_name"][:52]:54s} paras {len(nums):3d}  '
          f'(1–{max(nums) if nums else 0}){flag}')


if __name__ == '__main__':
    main()
