#!/usr/bin/env python3
"""add_headnote.py — splice the editorial headnote (catchwords / Facts / Held)
from a note's committed copy into its `## Judgment` section.

The case notes built from eLitigation carry the judgment text but not the
editorial headnote, because eLitigation renders the catchwords in a container of
their own (`class="catchwords text-left"`) and the Facts/Held headnote is not on
the page at all.  Where an earlier copy of the note in git does carry the
headnote, this puts it back — clearly labelled, above the judgment text.

    python3 _tools/add_headnote.py "cases/CRL_Criminal/wk_5/<file>.md"

Idempotent: does nothing if the headnote is already present.
"""
import os
import re
import subprocess
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADNOTE_MARK = '**Editorial headnote**'


def sect(lines, start, end):
    s = next((i for i, l in enumerate(lines) if l.strip() == start), None)
    if s is None:
        return []
    e = next((i for i in range(s + 1, len(lines)) if lines[i].strip() == end), len(lines))
    return [l.strip() for l in lines[s + 1:e] if l.strip()]


def split_welded(text):
    """The source stripped line breaks, welding catchwords together."""
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' · ', text)


def build_headnote(rel):
    raw = subprocess.run(['git', 'show', f'HEAD:{rel}'], cwd=VAULT,
                         capture_output=True, text=True, check=True).stdout
    lines = raw.split('\n')
    if not any(l.strip() == 'Catchwords' for l in lines):
        return None
    cw = [split_welded(l) for l in sect(lines, 'Catchwords', 'Facts')]
    fa = sect(lines, 'Facts', 'Holdings')
    hd = sect(lines, 'Holdings', 'Judgments')
    if not (cw or fa or hd):
        return None
    out = ['> ' + HEADNOTE_MARK + ' (from the reported version; not part of the judgment text).', '']
    if cw:
        out += ['**Catchwords**', ''] + ['- ' + l for l in cw] + ['']
    if fa:
        out += ['**Facts**', '', re.sub(r'\s+', ' ', ' '.join(fa)).strip(), '']
    if hd:
        out += ['**Held**', '', re.sub(r'\s+', ' ', ' '.join(hd)).strip(), '']
    out += ['---', '']
    return '\n'.join(out)


def main():
    for rel in sys.argv[1:]:
        path = os.path.join(VAULT, rel)
        txt = open(path, encoding='utf-8').read()
        if HEADNOTE_MARK in txt:
            print(f'skip     {os.path.basename(path)}  (headnote already present)')
            continue
        hn = build_headnote(rel)
        if hn is None:
            print(f'no headnote in committed copy: {os.path.basename(path)}')
            continue
        # insert directly after the `## Judgment` heading
        txt = re.sub(r'(## Judgment\n\n)', r'\1' + hn.replace('\\', '\\\\') + '\n', txt, count=1)
        open(path, 'w', encoding='utf-8').write(txt)
        print(f'headnote {os.path.basename(path)}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main()
