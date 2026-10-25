#!/usr/bin/env python3
"""Extract clean text from the two casebook PDFs (Burrows; McKendrick).

These are OCR'd scans, so their text layers carry faults the Academy Publishing
chapters do not. The one that matters for quoting is a **ligature break**: the
`Th`, `th`, `fi`, `fl`, `ffi` and `ffl` ligatures extract with a spurious space
after them, giving "Th is" for "This", "fi rst" for "first", "fl ats" for "flats"
and "faxed th rough to" for "faxed through to". Left alone, a quotation from the
book would read as nonsense.

Counted over both dumps: 241 occurrences in McKendrick, 1 in Burrows. They are
repaired by removing that space, which is safe because `Th`, `fi` and `fl` are
never standalone English words.

Other faults in these scans are *not* repaired, and must not be quoted as written
without a note. Seen in Burrows: `[W)hen` for `[W]hen`, `Cockburn a` for
`Cockburn CJ`, `expre ssed` for `expressed`, `fiat` for `flat`, and running heads
welded to figures (`7 54`, `7 60`). Where a passage is quoted from these books,
say so in the note and copy the passage from a clean source if one exists.

Usage
    casebook_extract.py <pdf> -o out.txt --offset 65
    casebook_extract.py <pdf> --page 824 --offset 65
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile

# ligature + spurious space. Only prefixes that are never words on their own.
LIG_SPACE = re.compile(r'\b(Th|th|fi|fl|ffi|ffl) (?=[a-z])')


def extract(pdf):
    fd, tmp = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    subprocess.run(['pdftotext', '-layout', pdf, tmp], check=True)
    with open(tmp, encoding='utf-8') as fh:
        txt = fh.read()
    os.unlink(tmp)
    return txt


def clean(text):
    text = LIG_SPACE.sub(lambda m: m.group(1), text)
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('-o', '--out')
    ap.add_argument('--offset', type=int, default=0,
                    help='printed page = pdf page - offset')
    ap.add_argument('--page', type=int, help='only this pdf page')
    ap.add_argument('--cat', action='store_true')
    args = ap.parse_args()

    txt = extract(args.pdf)
    pages = txt.split('\f')
    if args.page:
        pages = [pages[args.page - 1]]
        start = args.page
    else:
        start = 1

    chunks = []
    for i, pg in enumerate(pages, start=start):
        label = '<<<PDF PAGE %d' % i
        if args.offset:
            label += ' (book p %d)' % (i - args.offset)
        chunks.append('\n%s>>>\n%s' % (label, clean(pg).strip()))
    text = '\n'.join(chunks)

    if args.cat or not args.out:
        sys.stdout.write(text + '\n')
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as fh:
            fh.write(text)
        n = len(LIG_SPACE.findall(txt))
        print('wrote %s (%d words, %d ligature breaks repaired)'
              % (args.out, len(text.split()), n), file=sys.stderr)


if __name__ == '__main__':
    main()
