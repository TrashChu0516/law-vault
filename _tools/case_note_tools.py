#!/usr/bin/env python3
"""case_note_tools.py — housekeeping for case notes in the vault.

Two jobs, both idempotent:

  scaffold <file.md> ...   Insert the standard brief sections above the judgment
                           body and demote the body's `##` headings to `###` so
                           they nest under `## Judgment`.  Existing prose in the
                           sections is never overwritten.

  fixmeta  <file.md> ...   Repair `case_name` / `aliases` / the `# H1` line by
                           deriving them from the file name.  Build-time bug left
                           several notes titled `[1997] SGHC 258` instead of the
                           case name; the file name always holds the true name.

Usage:
  python3 _tools/case_note_tools.py fixmeta cases/CRL_Criminal/wk_5/*.md
  python3 _tools/case_note_tools.py scaffold cases/CRL_Criminal/wk_5/*.md

The section skeleton inserted by `scaffold`:

    ## In this note     (TOC)
    ## Exam version
    ## Case brief
    ## Pro Max
    ## Judgment         (the source text follows)

`## Key principles` is deliberately NOT inserted — that bank belongs to Steven
(see _tools/TAG_TAXONOMY.md); the ratio lives under `## Pro Max`.
"""
import os
import re
import sys

SECTIONS = ["Exam version", "Case brief", "Pro Max", "Judgment"]

HEADER_MARK = re.compile(
    r'^\*\*(Case Number|Decision Date|Tribunal/Court|Coram|Counsel Name|Parties|'
    r'Court|Judge|Prosecution|Defence|Charge|Outcome)\b')

CITE_TAIL = re.compile(r'\s*\[\d{4}\]\s+[A-Z][A-Za-z()]{1,12}\s+\d+\s*$')


def split_frontmatter(txt):
    m = re.match(r'^---\n(.*?\n)---\n(.*)$', txt, re.S)
    if not m:
        return None, txt
    return m.group(1), m.group(2)


def true_name(path):
    """Case name = file name minus the trailing ' [CITATION]'."""
    base = os.path.splitext(os.path.basename(path))[0]
    return CITE_TAIL.sub('', base).strip()


def fixmeta(path):
    name = true_name(path)
    txt = open(path, encoding='utf-8').read()
    fm, rest = split_frontmatter(txt)
    if fm is None:
        print(f'!! no frontmatter: {path}')
        return
    # --- frontmatter: case_name + aliases ---
    fm2 = re.sub(r'^case_name: .*$', 'case_name: "%s"' % name.replace('"', '\\"'),
                 fm, count=1, flags=re.M)
    if re.search(r'^aliases: ', fm2, re.M):
        alias_line = 'aliases: ["%s"]' % name.replace('"', '\\"')
        # keep a hand-added second alias (e.g. the s/o ↔ s:o variant)
        old = re.search(r'^aliases: \[(.*)\]$', fm2, re.M)
        if old and old.group(1).count('"') > 2:
            extras = [a.strip() for a in old.group(1).split('","')[1:]]
            alias_line = 'aliases: ["%s", %s]' % (name, ', '.join(extras))
        fm2 = re.sub(r'^aliases: .*$', alias_line, fm2, count=1, flags=re.M)
    # --- H1 line ---
    cite = ''
    cm = re.search(r'^citation: "(.*)"', fm2, re.M)
    if cm:
        cite = cm.group(1)
    if re.search(r'^# .*$', rest, re.M):
        rest = re.sub(r'^# .*$', '# %s' % name, rest, count=1, flags=re.M)
    else:
        rest = '# %s\n> %s\n\n' % (name, cite) + rest
    open(path, 'w', encoding='utf-8').write('---\n%s---\n%s' % (fm2, rest))
    print(f'fixmeta  {os.path.basename(path)}  -> {name}')


def find_body_start(rest):
    """First line that belongs to the judgment body."""
    lines = rest.split('\n')
    for i, l in enumerate(lines):
        if re.match(r'^\*\*\[\d+\]\*\*', l):
            return i
        if re.match(r'^#{2,3} ', l) and l.strip('# ').strip() not in SECTIONS:
            return i
        if HEADER_MARK.match(l):
            continue
    # nothing matched -> after the leading title/quote/metadata block
    for i, l in enumerate(lines):
        s = l.strip()
        if s and not s.startswith('#') and not s.startswith('>') and not HEADER_MARK.match(l):
            return i
    return len(lines)


def scaffold(path, force=False):
    txt = open(path, encoding='utf-8').read()
    fm, rest = split_frontmatter(txt)
    if fm is None:
        print(f'!! no frontmatter: {path}')
        return
    if '## In this note' in rest and not force:
        print(f'skip     {os.path.basename(path)}  (already scaffolded)')
        return

    lines = rest.split('\n')
    b = find_body_start(rest)
    head, body = '\n'.join(lines[:b]).rstrip(), '\n'.join(lines[b:])

    # demote body headings one level so they nest under `## Judgment`
    body = re.sub(r'^(#{2,4}) ', lambda m: '#' * (len(m.group(1)) + 1) + ' ', body, flags=re.M)

    stub = (
        '## In this note\n'
        '- [[#Exam version]] · [[#Case brief]] · [[#Pro Max]] · [[#Judgment]]\n\n'
        '## Exam version\n'
        '<!-- IRAC-ready recap. -->\n\n'
        '## Case brief\n'
        '<!-- Exam-venue version: ratio → facts → holding. -->\n\n'
        '## Pro Max\n'
        '<!-- The deep dive. Reading this ≈ reading the case. -->\n\n'
        '## Judgment\n'
    )
    out = '---\n%s---\n%s\n\n%s\n%s' % (fm, head, stub, body)
    open(path, 'w', encoding='utf-8').write(out)
    print(f'scaffold {os.path.basename(path)}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd, paths = sys.argv[1], sys.argv[2:]
    for p in paths:
        if cmd == 'fixmeta':
            fixmeta(p)
        elif cmd == 'scaffold':
            scaffold(p)
        else:
            print('unknown command', cmd)
            sys.exit(1)
