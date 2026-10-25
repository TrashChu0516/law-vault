#!/usr/bin/env python3
"""Extract clean text from the Academy Publishing (SAL Textbook) chapter PDFs.

Those PDFs carry three things that break a naive extraction, and `pdftotext`
reads all three as ordinary text and interleaves them through the chapter:

    (c) parties come to a mutual agreement
    22 that the contract be brought to an end ("discharge by
    0
    2
    agreement"); and

    contract must be strictly performed. [emphasis *    *
                                                    added]
                                                 y

Quoting that as written would misquote the textbook, which is worse than not
quoting at all.

**The two overlays are identifiable by FONT, and only by font.** Measured with
pdfplumber over Phang ch 16 and ch 19 (SAL Textbook, *The Law of Contract in
Singapore* (2nd Ed, 2022)):

    AAAAAA+Lato-Regular  12.6pt   body text
    CAAAAA+Lato-Bold     12.6pt   inline bold
    CAAAAA+Lato-Bold     15.8pt   headings
    CAAAAA+Lato-Bold     19.7pt   chapter title and contents headings
    CAAAAA+Lato-Bold     >=20pt   **the diagonal watermark.** On every page of
                                  both chapters it is exactly the string
                                  "© 2022 Contributors."
    AAAAAA+Lato-Regular   8.1pt   the paragraph numbers (16.015, 19.043 …)
    BAAAAA+LawNetIcons   10.5pt   **the page mark** — "y**", 3 glyphs (4 on the
                                  cover), same position, every page.

So dropping (a) Lato-Bold at >= 20pt and (b) LawNetIcons removes both overlays and
nothing else. Verified: across all 155 pages of the two chapters, the Lato-Bold
>= 20pt runs concatenate to "© 2022 Contributors." and to nothing else.

Two notes on the thresholds:

* **The 19.7 / 20.0 boundary is load-bearing.** The chapter title is 19.7pt; a
  ">= 19pt" rule deletes the title of the chapter.
* **Do not filter by height instead.** A height rule (>= 22px) catches the body
  of the watermark but leaves the "y**" page mark, which sits at body height. That
  is the bug this tool exists to avoid.

The third breakage is not an overlay: the **`fi` ligature extracts as a null
byte**, so "specified" arrives as "speci\\x00ed" and "sufficient" as
"suf\\x00cien". Every one of the 488 occurrences across both chapters is `fi` in
context (sufficient, difficult, significant, benefit, specified, fulfilment,
Mansfield, first, five, find, affixing, satisfied, qualification, indefinite), so
the tool maps it back. Count the substitutions with `--cat` output or the stderr
note if you ever extract a different chapter.

Usage
    pdf_text_clean.py <pdf> [-o out.txt] [--cat] [--page N] [--flow]
                      [--keep-cover] [--fonts]
"""

import argparse
import re
import sys

import pdfplumber

WATERMARK_FONT = 'Lato-Bold'
WATERMARK_SIZE = 20.0
PAGEMARK_FONT = 'LawNetIcons'
LIGATURES = {'\x00': 'fi'}
# The PDF's ToUnicode CMap maps the **fl ligature to "fi"**, so words with a real
# "fl" come out with "fi": "flat" -> "fiat", "floor" -> "fioor". It is a per-glyph
# fault, not a per-word one, so it cannot be fixed by a blanket substitution — a
# blanket "fi" -> "fl" would destroy *benefit*, *sufficient*, *first*, *specified*,
# *Mansfield*, *Fibrosa* and 100 other correctly-spelled words. The repair is
# therefore a word list, built by listing every distinct word containing "fi" in
# both chapters (131 words) and picking out the ones that are not English. Both
# chapters are checked with this list; re-run it if you extract another chapter.
FL_WORDS = {
    'briefiy': 'briefly',
    'confiation': 'conflation',
    'confiict': 'conflict',
    'confiicting': 'conflicting',
    'fiat': 'flat',
    'fiatly': 'flatly',
    "fiat's": "flat's",
    'fieet': 'fleet',
    'fiights': 'flights',
    'fioor': 'floor',
    'fiowing': 'flowing',
    'fiuctuations': 'fluctuations',
    'infiation': 'inflation',
    'infiuence': 'influence',
    'infiuenced': 'influenced',
    'infiuential': 'influential',
    'refiect': 'reflect',
    'refiected': 'reflected',
    'superfiuous': 'superfluous',
}
FL_RE = __import__('re').compile(
    r'\b(' + '|'.join(__import__('re').escape(k) for k in FL_WORDS) + r')\b',
    __import__('re').IGNORECASE)


def repair_fl(text):
    def sub(m):
        w = m.group(0)
        fixed = FL_WORDS[w.lower()]
        return fixed.capitalize() if w[0].isupper() else fixed
    return FL_RE.sub(sub, text)
Y_TOL = 2.0
# Body lines sit 19-20pt apart; a new paragraph opens at 37pt+. 26 splits them
# cleanly without breaking a normal line.
PARA_GAP = 26.0


def keep(ch):
    fn = ch['fontname'] or ''
    if PAGEMARK_FONT in fn:
        return False
    if WATERMARK_FONT in fn and ch['size'] >= WATERMARK_SIZE:
        return False
    return True


def page_body(chars):
    """Group chars into lines by baseline; blank line on a paragraph-sized gap."""
    rows = {}
    for ch in chars:
        key = None
        for k in rows:
            if abs(k - ch['top']) <= Y_TOL:
                key = k
                break
        if key is None:
            key = ch['top']
            rows[key] = []
        rows[key].append(ch)

    out, prev_top = [], None
    for top in sorted(rows):
        cs = sorted(rows[top], key=lambda c: c['x0'])
        text = ''.join(c['text'] for c in cs)
        for bad, good in LIGATURES.items():
            text = text.replace(bad, good)
        text = repair_fl(text)
        text = re.sub(r'[ \t]{2,}', ' ', text).strip()
        if not text:
            continue
        if prev_top is not None and top - prev_top > PARA_GAP:
            out.append('')
        out.append(text)
        prev_top = top
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('-o', '--out')
    ap.add_argument('--cat', action='store_true')
    ap.add_argument('--page', type=int)
    ap.add_argument('--flow', action='store_true', help='de-hyphenate and reflow')
    ap.add_argument('--keep-cover', action='store_true')
    ap.add_argument('--fonts', action='store_true')
    args = ap.parse_args()

    chunks, ligs = [], 0
    with pdfplumber.open(args.pdf) as pdf:
        if args.fonts:
            import collections
            census = collections.Counter()
            for pg in pdf.pages:
                for ch in pg.chars:
                    census[(ch['fontname'], round(ch['size'], 1))] += 1
            for k, v in census.most_common():
                print('%-30s %-6s %8d' % (k[0], k[1], v))
            return

        pages = pdf.pages
        if args.page:
            pages = [pages[args.page - 1]]
        for i, pg in enumerate(pages, start=(args.page or 1)):
            if i == 1 and not args.keep_cover:
                continue
            ligs += sum(1 for c in pg.chars if c['text'] in LIGATURES)
            body = page_body([c for c in pg.chars if keep(c)])
            if args.page is None:
                chunks.append('\n<<<PDF PAGE %d>>>\n%s' % (i, body))
            else:
                chunks.append(body)

    text = '\n'.join(chunks)
    if args.flow:
        text = re.sub(r'-\n(?=[a-z])', '-', text)
        text = re.sub(r'\n(?!\n)', ' ', text)
        text = re.sub(r'[ \t]{2,}', ' ', text).strip()

    if args.cat or not args.out:
        sys.stdout.write(text + '\n')
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as fh:
            fh.write(text)
        print('wrote %s (%d words, %d ligatures repaired)'
              % (args.out, len(text.split()), ligs), file=sys.stderr)


if __name__ == '__main__':
    main()
