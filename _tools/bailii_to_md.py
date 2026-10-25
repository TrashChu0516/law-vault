#!/usr/bin/env python3
"""BAILII judgment HTML -> vault case note.

    python3 _tools/bailii_to_md.py <in.html> <out.md> \
        --module CRL --week 7 --jurisdiction UK [--name "..."] [--topic defences]

BAILII serves two quite different markups, and both are in use on this course:

  * modern (1990s+):  paragraphs are <p class="western">, wrapped across source
    lines, one paragraph per element. A Law Lord's speech opens with a
    paragraph whose entire text is a bold all-caps name ("LORD TEMPLEMAN").
  * ICLR reprints (e.g. the 1884 Dudley and Stephens): paragraphs are
    <div class="jdg"> inside <div class="Judgment">, with the speech anchored by
    <a name="LORDCOLERIDGE,CJ">.

Everything outside the judgment — the "[Home] [Databases]" bar, the
"You are here:" breadcrumb, "URL:", "Cite as:", the ICLR buy-links and the
running "- 10 -" page numbers — is chrome and must be dropped, or the note
carries text the judgment never had.
"""
import argparse
import html as H
import re
import sys

# --------------------------------------------------------------------------
TAG = re.compile(r'<[^>]+>')
CHROME = re.compile(
    r'^\s*(\[Home\]|\[New search\]|\[Databases\]|\[Help\]|\[Feedback\]|'
    r'You are here:|URL:|Cite as:|BAILII Citation Number:|Case No:|'
    r'BAILII:|JISCBAILII|\[DONATE\]|\[Buy ICLR report|<a)')
PAGENUM = re.compile(r'^\s*-\s*\d+\s*-\s*$')
# a paragraph that is nothing but a speaker's name ("LORD TEMPLEMAN")
SPEAKER = re.compile(r'^(?:LORD|LADY|SIR|MR|MRS|BARON|VISCOUNT)\s+[A-Z][A-Z ,\.\'\-]+$')


def clean(s):
    s = TAG.sub(' ', s)
    s = H.unescape(s)
    s = s.replace('\xa0', ' ')
    # BAILII hard-wraps the source, so a paragraph arrives full of newlines.
    # Collapse ALL whitespace, not just spaces, or headings render as
    # "LORD" + newline + "TEMPLEMAN".
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


SMALL = {'of', 'the', 'and', 'de', 'van', 'von', 'in', 'on', 'at', 'for'}


def titlecase_name(s):
    """LORD SLYNN OF HADLEY -> Lord Slynn of Hadley (not "... Of Hadley")."""
    words = s.split()
    return ' '.join(w.lower() if (i and w.lower() in SMALL) else w.capitalize()
                    for i, w in enumerate(words))


def blocks(html):
    """Yield (kind, text) in document order.

    kind is 'judgment' for a body paragraph, 'speaker' for a speech heading.
    """
    out = []
    # body elements, in document order
    for m in re.finditer(r'<(p|div)\s+class="(western|jdg)"[^>]*>(.*?)</\1>', html, re.S):
        seg = m.group(3)
        text = clean(seg)
        if not text or PAGENUM.match(text):
            continue
        out.append(('speaker' if SPEAKER.match(text) else 'judgment', text))
    return out


def drop_cover_page(rows):
    """Discard the BAILII / Parliamentary Archives cover page.

    Brown opens with "Die Jovis 11° Martii 1993", "HOUSE OF LORDS",
    "REGINA v.", "BROWN (APPELLANT)" … none of which is the judgment. When the
    judgment has speech headings, the first one is the reliable start. When it
    does not (the ICLR reprints, e.g. Dudley and Stephens), the first
    substantive paragraph is.
    """
    first_speaker = next((i for i, (k, _) in enumerate(rows) if k == 'speaker'), None)
    if first_speaker is not None:
        return rows[first_speaker:]
    first_long = next((i for i, (_, t) in enumerate(rows) if len(t) > 150), 0)
    return rows[first_long:]


def strip_judgment_chrome(body_html):
    """Remove the BAILII furniture that sits above the judgment proper."""
    i = body_html.find('JUDGMENT')
    if i == -1:
        i = body_html.find('Judgment')
    return body_html[i:] if i != -1 else body_html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('out')
    ap.add_argument('--module', default='CRL')
    ap.add_argument('--week', default='7')
    ap.add_argument('--jurisdiction', default='UK')
    ap.add_argument('--name', default='')
    ap.add_argument('--topic', default='')
    ap.add_argument('--tags', default='')
    a = ap.parse_args()

    html = open(a.src, encoding='utf-8', errors='replace').read()

    # ---- header ----------------------------------------------------------
    # "Cite as:" lives inside markup, so read it off the flattened text.
    # Careful: the closing marker flattens to "[ New search ]" (spaces inside
    # the brackets), so a literal "[New search]" never matches and the capture
    # would run to the end of the document.
    flat = clean(html)
    m = re.search(r'Cite as:\s*(.*?)\s*\[\s*New search\s*\]', flat)
    cite_line = m.group(1).strip() if m else ''
    cites = [c.strip() for c in cite_line.split(',') if c.strip()]

    # A neutral citation names the court; a law-report citation names a series.
    # Both can start with a year, so filter on the court code, not the bracket.
    NEUTRAL = re.compile(r'^\[\d{4}\]\s*(?:UKHL|UKSC|UKPC|EWCA|EWHC|SGCA|SGHC|SGDC|SGMC)\b', re.I)
    SERIES = ['AC', 'WLR', 'All ER', 'QBD', 'Cr App R', 'KB', 'QB', 'SLR']
    neutral = next((c for c in cites if NEUTRAL.match(c)), '')
    rest = [c for c in cites if c != neutral]
    reported = ''
    for s in SERIES:
        hit = next((c for c in rest if s in c), None)
        if hit:
            reported = hit
            break
    if not reported and rest:
        reported = rest[0]

    name = a.name
    if not name:
        m = re.search(r'<p class="case">(.*?)</p>', html, re.S)
        if m:
            name = clean(m.group(1))
        else:
            m = re.search(r'Decisions\s*&gt;&gt;\s*(.*?)\s*\(\d', html)
            name = clean(m.group(1)) if m else 'Unknown'
    name = re.sub(r'\s+', ' ', name).rstrip('.')

    crumb = re.search(r'You are here:.*?&gt;&gt;\s*(.*?)\s*(?:\[|$)', html, re.S)
    court = 'United Kingdom'
    if crumb:
        c = clean(crumb.group(1))
        for k in ('House of Lords', "Queen's Bench Division", 'Court of Appeal',
                  'Supreme Court', 'High Court'):
            if k.lower() in c.lower():
                court = ('House of Lords' if 'House of Lords' in c else k)
                break

    date = ''
    m = re.search(r'<title>.*?\((\d{1,2} \w+ \d{4})\)', html, re.S)
    if m:
        date = m.group(1)
    else:
        m = re.search(r'(\d{1,2}\s+\w+\.?\s+\d{4})\.', html)
        if m:
            date = m.group(1)

    # ---- body ------------------------------------------------------------
    body = strip_judgment_chrome(html)
    rows = drop_cover_page(blocks(body))
    if not rows:
        sys.exit('no paragraphs found — is this a BAILII judgment page?')

    lines, speakers = [], 0
    for kind, text in rows:
        if kind == 'speaker':
            lines.append('')
            lines.append(f'### {titlecase_name(text)}')
            lines.append('')
            speakers += 1
        else:
            lines.append(text)
            lines.append('')
    body_md = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()

    topic = f'["{a.topic}"]' if a.topic else '[]'
    tags = '[' + ', '.join(f'"{t.strip()}"' for t in a.tags.split(',')) if a.tags else '[]'
    if a.tags:
        tags += ']'

    note = f'''---
case_name: "{name}"
citation: "{neutral}"
reported: "{reported}"
court: "{court}"
module: "{a.module}"
week: {a.week}
jurisdiction: "{a.jurisdiction}"
decision_date: "{date}"
topic: {topic}
tags: {tags}
source: "BAILII"
type: case
status: fulltext
---

# {name}
> {reported} · {neutral}

**Court:** {court} · **Decision Date:** {date}

> **Source:** BAILII full text ({neutral}) — not an abridged reproduction.

## In this note
- [[#Exam version]] · [[#Case brief]] · [[#Pro Max]] · [[#Judgment]]

## Exam version
<!-- IRAC-ready recap. -->

## Case brief
<!-- Exam-venue version: ratio → facts → holding. -->

## Pro Max
<!-- The deep dive. Reading this ≈ reading the case. -->

## Judgment

{body_md}
'''
    open(a.out, 'w', encoding='utf-8').write(note)
    print(f'{a.out}  ·  {len(body_md.split())} words  ·  {speakers} speeches  ·  {name[:46]}')


if __name__ == '__main__':
    main()
