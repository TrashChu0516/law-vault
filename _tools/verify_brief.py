#!/usr/bin/env python3
"""Verify a case note's brief against its own judgment text.

Three checks, all mechanical:

  1. `## Judgment` and everything below is byte-identical to the committed
     version — a brief must be added ABOVE the judgment, never inside it.
  2. Every paragraph number cited in the brief exists as a `**[n]**` marker in
     the judgment body.
  3. Every substantive blockquote in the brief appears VERBATIM in the judgment.
     Quotation drift is the failure mode that matters most: a paraphrase inside
     quotation marks is worse than no quotation, because it looks authoritative.

Usage:  python3 _tools/verify_brief.py <case-note.md> [more.md ...]
"""
import re
import subprocess
import sys


def committed(path):
    try:
        return subprocess.run(['git', 'show', f'HEAD:{path}'],
                              capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None


def norm(s):
    """Normalise for comparison: drop markers, collapse whitespace, unify quotes.

    Two conventions that are legitimate but would otherwise read as drift:
      * eLitigation writes a backtick where an apostrophe belongs; the briefs use
        a real apostrophe. Same character to a reader, so treat them as equal.
      * legal writing alters a quotation's initial capital with square brackets
        — "[W]here the Prosecution mounts…" quoting "…where the Prosecution
        mounts…". Unwrap those, or every properly-altered quotation is reported
        as a fabrication.

    Emphasis markup is stripped HERE, on both sides, rather than only from the
    quotation. Strip it from the quotation alone and it is stripped from one side
    of the comparison only: the judgment reads `limb (_b_)`, the brief quotes
    "limb (b)", and every quotation touching an italicised phrase is reported as
    drift. That produced ~90 false failures across six Week 5 notes before it was
    spotted — the checked-in text was correct throughout.
    """
    s = s.replace('\u2018', "'").replace('\u2019', "'").replace('`', "'")
    s = s.replace('\u201c', '"').replace('\u201d', '"')
    s = re.sub(r'\*\*\[\d+\]\*\*', ' ', s)
    s = re.sub(r'\*\*|\*|_', '', s)
    s = re.sub(r'\[([A-Za-z])\]', lambda m: m.group(1).lower(), s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def cleaner(s):
    """For the 'judgment untouched' test: also drop footnote cruft.

    The note was normalised across two passes and the second (removing the
    "[note: N]" markers) ran after the checkpoint commit, so a raw byte compare
    would flag my own cleanup as if the agent had corrupted the judgment.
    """
    s = re.sub(r'[ \t]*\d*[ \t]*Foot Note \d+[ \t]*×', ' ', s)
    s = re.sub(r'[ \t]*\[note:\s*\d+\]', ' ', s)
    s = re.sub(r'[ \t]{2,}', ' ', s)
    s = re.sub(r'[ \t]+\n', '\n', s)
    return s


def check(path):
    cur = open(path, encoding='utf-8').read()
    head = committed(path)
    print('=' * 78)
    print(path.split('/')[-1])

    # ---- 0. frontmatter integrity ----------------------------------------
    # A note whose frontmatter delimiters are broken silently disappears from
    # every Dataview index (the MOCs, CASE_INDEX, the ratio bank) while still
    # looking perfectly fine in the editor. Seen in the wild: a Markdown
    # round-trip that escaped the opener to `\---` and added two trailing spaces
    # to most lines, to prevent the `---` being read as a setext heading.
    # Nothing below this point notices, so check it first.
    fm_bad, fm_note = [], []
    if re.match(r'^\\+---', cur):
        fm_bad.append('frontmatter opener is escaped (starts with \\---)')
    elif not cur.startswith('---\n'):
        fm_bad.append('does not start with a frontmatter block')
    else:
        close = cur.find('\n---', 3)
        if close < 0:
            fm_bad.append('frontmatter block is never closed')
        elif '## Judgment' in cur:
            # Only judge-note frontmatter, and only INFORMATIONAL. The older
            # casebook stubs legitimately carry neither `## Judgment` nor
            # `importance`, and the MOCs carry no `case_name` — flagging those
            # would make this check cry wolf, which is worse than not having it.
            keys = set(re.findall(r'^([a-z_]+):', cur[3:close], re.M))
            missing = [k for k in ('case_name', 'module', 'week', 'status')
                       if k not in keys]
            if re.search(r'(?m)^module:\s*"?CL1', cur[:close]) and 'importance' not in keys:
                missing.append('importance (CL1)')
            if missing:
                fm_note.append('missing keys: ' + ', '.join(missing))
    n_hard = sum(1 for l in cur.split('\n') if l.endswith('  '))
    if n_hard > 20:
        fm_bad.append('%d lines end in two spaces (hard line breaks?)' % n_hard)
    if fm_bad:
        print('  !!   frontmatter: ' + '; '.join(fm_bad))
        print('        this note will NOT appear in Dataview indexes until fixed')
    else:
        print('  OK   frontmatter intact')
    if fm_note:
        print('  --   frontmatter: ' + '; '.join(fm_note) + '  (informational)')

    # A placeholder note is a designed stub: it records a citation, why the text
    # is unobtainable, and where to read it. There is no judgment to check, so
    # "no ## Judgment heading" here is the correct state, not a failure.
    #
    # `status: casebook` is skipped for the same reason. Those notes cover the
    # English and old casebook authorities which are NOT in the vault as
    # judgments — the note carries the extract or the textbook's treatment with
    # pinpoints into *that* source, so there is no `## Judgment` to compare
    # against and no vault-local paragraph sequence to validate. Running the
    # judgment checks over them reports every blockquote as not-verbatim, which
    # is an artefact of there being no judgment, not drift. (52 such notes exist
    # across CL1 Weeks 1-4 and 9.)
    #
    # Frontmatter is still checked in both cases — that check is applicable.
    fm = cur[:cur.find('\n---', 3)] if cur.startswith('---') else ''
    if re.search(r'^status:\s*(placeholder|casebook)', fm, re.M):
        kind = re.search(r'^status:\s*(\w+)', fm, re.M).group(1)
        print('  --   %s note (no judgment text by design) — skipped' % kind)
        return not fm_bad

    # ---- 1. judgment untouched -------------------------------------------
    if head:
        cj, hj = cur.find('## Judgment'), head.find('## Judgment')
        if cj < 0 or hj < 0:
            print('  !!   no ## Judgment heading')
        elif cleaner(cur[cj:]) == cleaner(head[hj:]):
            print('  OK   ## Judgment unchanged (modulo the footnote-cruft cleanup)')
        else:
            a, b = cleaner(cur[cj:]), cleaner(head[hj:])
            i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), None)
            print(f'  !!   ## Judgment DIFFERS from HEAD at char {i}')
            if i is not None:
                print(f'        HEAD : …{b[max(0,i-70):i+70]!r}')
                print(f'        NOW  : …{a[max(0,i-70):i+70]!r}')
    else:
        print('  --   no committed version to compare')

    body = cur[cur.find('## Judgment'):]
    brief = cur[:cur.find('## Judgment')]
    # Strip the judgment's OWN blockquote markers. Statutes and long extracts
    # are set as "> ..." inside the judgment; without this, every quotation the
    # brief makes of such a passage compares against "> the text" and is falsely
    # reported as drift.
    clean_body = norm(re.sub(r'(?m)^>[ \t]?', '', body))

    # ---- 2. cited paragraph numbers --------------------------------------
    have = {int(m.group(1)) for m in re.finditer(r'\*\*\[(\d+)\]\*\*', body)}
    cited, external = set(), set()
    for m in re.finditer(r'\[(\d{1,3})\](?:\s*[–-]\s*\[?(\d{1,3})\]?)?', brief):
        a = int(m.group(1))
        span = set(range(min(a, int(m.group(2))), max(a, int(m.group(2))) + 1)) if m.group(2) else {a}
        # "AOF at [115]" is a pinpoint into a CITED case, not into this
        # judgment. Flagging those as errors makes the check useless, so
        # classify them separately and report them as informational.
        before = brief[max(0, m.start() - 30):m.start()]
        if re.search(r'\bat\s*$', before) or re.search(r'\bsupra\b', before, re.I):
            external |= {x for x in span if x not in have}
        else:
            cited |= span
    missing = sorted(x for x in cited if x not in have)
    print(f'  {"OK  " if not missing else "!!  "} pinpoints: {len(cited)} cited, '
          f'{len(missing)} not present {missing[:12] if missing else ""}')
    if external:
        print(f'  --   {len(external)} number(s) read as pinpoints into a cited case: '
              f'{sorted(external)[:8]}')

    # ---- 3. verbatim blockquotes -----------------------------------------
    quotes, buf = [], []
    for line in brief.split('\n'):
        if line.startswith('>'):
            buf.append(line.lstrip('> ').strip())
        else:
            if buf:
                quotes.append(' '.join(buf))
                buf = []
    if buf:
        quotes.append(' '.join(buf))

    bad = []
    for q in quotes:
        # Strip the paragraph marker BEFORE the other markdown: removing "**"
        # first turns "**[20]**" into "[20]", which then matches nothing, and
        # every properly-cited quotation is reported as drift.
        q = re.sub(r'\*\*\[\d+\]\*\*', ' ', q)
        q = re.sub(r'\*\*|\*|`|_', '', q).strip()
        q = re.sub(r'^\[\d{1,3}\]\s*', '', q)        # a bare "[20] " prefix
        q = re.sub(r'^(\s*[.…]\s*)+', '', q).strip()  # a leading ellipsis / dots
        # Blockquotes that are the note's OWN commentary, not quotations from
        # the judgment. Matching them against the judgment text always fails.
        # If you add a meta-blockquote convention to the notes, add its opening
        # words here too — otherwise it reports as a fabricated quotation.
        # NOTE the test runs on the markdown-stripped text, so a blockquote that
        # opens with a bold lead-in ("**Textbook.** …") is matched by the words
        # after the asterisks.
        if q.startswith(('⚠', 'Editorial headnote', 'Source', 'Note-up',
                         'Numbering note', 'Citation note', 'Where it sits',
                         'Where this sits', 'Reproduction', 'Reading list',
                         'Status', 'Textbook', 'This judgment carries no',
                         'Pull', '|')):
            continue
        # A quote may legitimately elide material with an ellipsis and resume
        # later. Check each surviving segment on its own; only a segment that
        # appears nowhere in the judgment is real drift.
        segments = [s for s in re.split(r'\s*…\s*|\s*\.\.\.\s*', q) if len(s) >= 60]
        for seg in (segments or ([q] if len(q) >= 60 else [])):
            # A TRAILING pinpoint sits inside the quotation in the older notes —
            # `… would be satisfied. ([43])`. The judgement text of course stops
            # at "satisfied", so the parenthesis must come off or the quote never
            # matches. Both bracketed and round forms, with an optional range.
            seg = re.sub(r'[\s.,;]*\(\s*\[?\d{1,3}(?:\s*[–-]\s*\d{1,3})?\]?\s*\)\s*$', '', seg)
            seg = re.sub(r'[\s.,;]*\[\d{1,3}(?:\s*[–-]\s*\d{1,3})?\]\s*$', '', seg).strip()
            if len(seg) < 60:
                continue
            if norm(seg) not in clean_body:
                bad.append(seg)
    print(f'  {"OK  " if not bad else "!!  "} blockquotes: {len(quotes)} found, '
          f'{len(bad)} not verbatim in the judgment')
    for q in bad[:6]:
        print(f'        NOT FOUND: {q[:110]}')
    return not missing and not bad and not fm_bad


if __name__ == '__main__':
    # evaluate every file — all() over a generator short-circuits on the first
    # failure and silently skips the rest
    results = [check(p) for p in sys.argv[1:]]
    print('=' * 78)
    print(f'{sum(results)}/{len(results)} PASSED'
          if any(results) else 'ALL FAILED' if results else 'nothing to check')
