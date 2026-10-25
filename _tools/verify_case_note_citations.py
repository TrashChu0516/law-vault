#!/usr/bin/env python3
"""verify_case_note_citations.py — check a case note's brief against its own judgment.

For each note in cases/CRL_Criminal/wk_5/:
  1. Every `**[n]**` paragraph citation appearing ABOVE `## Judgment` must
     correspond to a paragraph marker that actually exists in the judgment text.
     (A citation range like `[12]–[15]` is checked endpoint by endpoint.)
  2. Every blockquote line (`> ...`) in the brief, and every inline quoted span
     of 6+ words, must be found verbatim in the judgment text, after normalising
     the eLitigation artefact that renders apostrophes as backticks.

Run:  python3 _tools/verify_case_note_citations.py
"""
import glob
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER = (sys.argv[1] if len(sys.argv) > 1
          else os.path.join(VAULT, 'cases', 'CRL_Criminal', 'wk_5'))


def norm(s):
    """Normalise punctuation that the sources vary on."""
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('`', "'")
    s = s.replace('\u201c', '"').replace('\u201d', '"')
    s = s.replace('\u2014', '-').replace('\u2013', '-').replace('\u2212', '-')
    s = re.sub(r'[*_>#\[\]]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()


def check(path):
    txt = open(path, encoding='utf-8').read()
    cut = txt.find('## Judgment')
    if cut < 0:
        return [('ERROR', 'no ## Judgment section')]
    brief, body = txt[:cut], txt[cut:]
    nb = norm(body)

    issues = []

    # ---- 1. paragraph citations ------------------------------------------
    have = {int(m.group(1)) for m in re.finditer(r'^\*\*\[(\d{1,3})\]\*\*', body, re.M)}
    cited = set()
    for m in re.finditer(r'\[(\d{1,3})\](?:\s*[–\-]\s*\[?(\d{1,3})\]?)?', brief):
        a = int(m.group(1))
        cited.add(a)
        if m.group(2):
            b = int(m.group(2))
            for n in range(min(a, b), max(a, b) + 1):
                cited.add(n)
    missing = sorted(n for n in cited if n not in have)
    if missing:
        issues.append(('PARA', f'cites paragraphs that do not exist: {missing}'))

    # ---- 2. quotations ----------------------------------------------------
    quotes = []
    for line in brief.split('\n'):
        s = line.strip()
        if s.startswith('> '):
            quotes.append(('blockquote', s[2:].strip()))
    for m in re.finditer(r'"([^"\n]{40,400})"', brief):
        quotes.append(('inline', m.group(1)))

    bad = []
    for kind, q in quotes:
        # a blockquote may carry a leading cite marker and inline ellipses
        q2 = re.sub(r'^\*\*\[[\d,\s–\-]+\]\*\*\s*', '', q)
        parts = [p for p in re.split(r'…|\.\.\.', norm(q2)) if len(p.split()) >= 6]
        for p in parts:
            if p and p not in nb:
                bad.append((kind, p[:100]))
    if bad:
        for kind, p in bad:
            issues.append(('QUOTE', f'{kind} not found verbatim: "{p}…"'))
    return issues


def main():
    total = 0
    for path in sorted(glob.glob(os.path.join(FOLDER, '*.md'))):
        name = os.path.basename(path)
        if name.startswith('_'):
            continue
        issues = check(path)
        total += len(issues)
        if issues:
            print(f'\n=== {name}')
            for kind, msg in issues:
                print(f'   [{kind}] {msg}')
        else:
            print(f'OK   {name}')
    print(f'\n{total} issue(s)')
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
