#!/usr/bin/env python3
"""BAILII "plain <p>" judgment pages -> vault case note.

    python3 _tools/bailii_plain_to_md.py <in.html> <out.md> \
        --module CL1 --week 10 [--name "..."] --style lords|sections

A THIRD BAILII markup, distinct from the two `bailii_to_md.py` handles. Here
every paragraph is a bare `<p>` with no class, the law-report running heads are
repeated as ordinary paragraphs at every page break, and page numbers arrive as
their own paragraphs ("2 [2]", "[13] 2"). Neither `class="western"` nor
`class="jdg"` appears anywhere, so the older converter finds nothing and exits
with "no paragraphs found".

Two styles:

  lords    House of Lords pamphlet (Fibrosa [1942] UKHL 4). Speeches are headed
           by a bare name ("Lord Atkin") followed by "MY LORDS,". The running
           head — all seven names, then the case name — repeats at every page
           break and is indistinguishable from a speech heading *in isolation*,
           so it is dropped as a BLOCK: three or more consecutive name-only
           paragraphs. A lone name paragraph followed by "MY LORDS," is a real
           speech heading.
  sections first-instance transcript (Gamerco [1995] EWHC 1 (QB)). The judge's
           own headings are short bare paragraphs; they are promoted from an
           explicit whitelist rather than guessed, because short paragraphs in a
           transcript are otherwise usually fragments of quoted documents.

Neither judgment carries printed paragraph numbers, so this script emits none.
Citations must go by speech or by the judge's own heading.
"""
import argparse
import html as H
import re

TAG = re.compile(r'<[^>]+>')
# "[8]" · "2 [2]" · "[13] 2" · "3 [16]" · "- 10 -" — page furniture, never text.
PAGEMARK = re.compile(
    r'^\s*(?:'
    r'\d{1,3}\s*\[\s*\d{1,3}\s*\]|'      # "2 [2]"
    r'\[\s*\d{1,3}\s*\]\s*\d{1,3}|'      # "[13] 2"
    r'\[\s*\d{1,3}\s*\]|'                  # "[8]"
    r'-\s*\d{1,3}\s*-|'                      # "- 10 -"
    r'A\d{1,2}'                                # scan junk left by the OCR
    r')\s*$')
CHROME = re.compile(r'^\s*(\[\s*(Home|New search|Databases|Help|Feedback|DONATE)\s*\]|'
                    r'HTML VERSION OF JUDGMENT|Crown Copyright|JISCBAILII|Cite as:|'
                    r'URL:|You are here:)')

LORDS = ['Lord Chancellor', 'Lord Atkin', 'Lord Russell of Killowen',
         'Lord Macmillan', 'Lord Wright', 'Lord Roche', 'Lord Porter']

GAMERCO_HEADINGS = ['The issues', 'Formation of the contract',
                    'The construction of the contract', "The defendant's obligation",
                    'The law', 'Subsequent events', 'Recovery and expenses',
                    'The approach to the proviso', '2 . Equal Division',
                    '3. Broad Discretion', 'Merchandise']


def paragraphs(path):
    h = open(path, encoding='utf-8', errors='ignore').read()
    out = []
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', h, re.S):
        s = TAG.sub(' ', m.group(1))
        s = H.unescape(s).replace('\xa0', ' ')
        s = re.sub(r'\s+', ' ', s).strip()
        if s:
            out.append(s)
    return out


DICT = set()
try:
    with open('/usr/share/dict/web2', encoding='utf-8', errors='ignore') as fh:
        DICT = {w.strip().lower() for w in fh if w.strip()}
except OSError:
    pass


def dehyphenate(s):
    """Rejoin words the printed line broke with a hyphen ("con- tract").

    Only rejoin where the hyphenated form is NOT itself a dictionary word:
    that keeps "ship-building" hyphenated and repairs "con- tract". Without a
    dictionary the two cases are indistinguishable, so if none loads the text
    is left alone rather than silently corrupted.
    """
    if not DICT:
        return s

    def fix(m):
        a, b = m.group(1), m.group(2)
        if (a + '-' + b).lower() in DICT and (a + b).lower() not in DICT:
            return a + '-' + b
        return a + b
    return re.sub(r'\b([A-Za-z]{2,})- ([A-Za-z]{2,})\b', fix, s)


def is_lord_name(s):
    s = re.sub(r'[.:]+$', '', s).strip()
    s = re.sub(r'^The\s+', '', s)
    return s in LORDS


def build_lords(ps):
    """Fibrosa: drop running-head blocks, keep real speeches."""
    keep, i = [], 0
    while i < len(ps):
        s = ps[i]
        # a run of >=3 consecutive name-only paragraphs is a page's running head
        j = i
        while j < len(ps) and is_lord_name(ps[j]):
            j += 1
        run = j - i
        if run >= 3:
            i = j
            # the running head is followed by the case name and/or a page mark
            while i < len(ps) and (ps[i].startswith('FIBROSA') or PAGEMARK.match(ps[i])):
                i += 1
            continue
        # a single name followed by "MY LORDS," is a real speech heading
        if is_lord_name(s) and i + 1 < len(ps) and ps[i + 1].lower().startswith('my lords'):
            keep.append(('speaker', re.sub(r'[.:]$', '', s)))
            i += 1
            continue
        if s.startswith('FIBROSA SPOLKA AKCYJNA'):
            i += 1
            continue
        if PAGEMARK.match(s) or CHROME.match(s):
            i += 1
            continue
        keep.append(('body', s))
        i += 1
    # Everything before the first speech heading is the pamphlet cover
    # ("Die Lunae…", "Parliamentary Archives", the split case name). The
    # reading list's page pinpoints start at the first speech anyway.
    first = next((k for k, (kind, _) in enumerate(keep) if kind == 'speaker'), 0)
    return keep[first:]


def build_sections(ps, start_pat, headings, stop_pat=None):
    """Gamerco: start at the judge, promote an explicit heading whitelist."""
    start = next((i for i, s in enumerate(ps) if re.search(start_pat, s)), 0)
    keep = []
    for j, s in enumerate(ps[start:], start):
        # the stop marker is the judge speaking AGAIN, after the judgment proper,
        # so it must not be tested against the paragraph the judgment opens with
        if stop_pat and j > start and re.search(stop_pat, s):
            break
        if s in headings:
            keep.append(('heading', s))
        elif PAGEMARK.match(s) or CHROME.match(s) or re.fullmatch(r'\d{1,2}\.', s):
            continue
        else:
            keep.append(('body', s))
    return keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('out')
    ap.add_argument('--module', default='CL1')
    ap.add_argument('--week', default='10')
    ap.add_argument('--name', required=True)
    ap.add_argument('--court', required=True)
    ap.add_argument('--cite', required=True)
    ap.add_argument('--neutral', required=True)
    ap.add_argument('--date', required=True)
    ap.add_argument('--coram', required=True)
    ap.add_argument('--style', choices=['lords', 'sections'], required=True)
    ap.add_argument('--start', default='')
    ap.add_argument('--stop', default='')
    ap.add_argument('--citation-note', required=True)
    ap.add_argument('--dehyphenate', action='store_true',
                    help='rejoin words broken by a hyphen at a printed line end')
    a = ap.parse_args()

    ps = paragraphs(a.src)
    if a.dehyphenate:
        ps = [dehyphenate(x) for x in ps]
    if a.style == 'lords':
        rows = build_lords(ps)
    else:
        rows = build_sections(ps, a.start, GAMERCO_HEADINGS, a.stop or None)
    if len(rows) < 20:
        raise SystemExit('only %d blocks — parser did not engage' % len(rows))

    lines = []
    for kind, text in rows:
        if kind in ('speaker', 'heading'):
            lines += ['', '### ' + text, '']
        else:
            lines += [text, '']
    body = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()

    note = f'''---
case_name: "{a.name}"
citation: "{a.neutral}"
reported: "{a.cite}"
court: "{a.court}"
module: "{a.module}"
week: {a.week}
jurisdiction: "UK"
decision_date: "{a.date}"
coram: "{a.coram}"
topic: ["frustration"]
tags: []
source: "BAILII"
type: case
status: fulltext
---

# {a.name}
> {a.cite} · {a.neutral}

**Court:** {a.court} · **Decision Date:** {a.date} · **Coram:** {a.coram}

> **Source:** BAILII full text ({a.neutral}). Not an abridged reproduction.

## Citation note

> {a.citation_note}

## In this note
- [[#Exam version]] · [[#Case brief]] · [[#Pro Max]] · [[#Judgment]]

## Exam version
<!-- IRAC-ready recap. -->

## Case brief
<!-- Exam-venue version: ratio → facts → holding. -->

## Pro Max
<!-- The deep dive. Reading this ≈ reading the case. -->

## Judgment

{body}
'''
    open(a.out, 'w', encoding='utf-8').write(note)
    print('%s  ·  %d words  ·  %d blocks' % (a.out, len(body.split()), len(rows)))


if __name__ == '__main__':
    main()
