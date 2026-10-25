#!/usr/bin/env python3
"""
elitigation_to_md.py — Faithful converter for Singapore judgments (elitigation.sg) → Obsidian Markdown.

Preserves: case metadata (citation, coram, parties, catchwords), section headings
(3 levels), numbered paragraphs, and block quotes — so the MD is a faithful,
navigable rendering of the authentic judgment.

Usage:
    python3 elitigation_to_md.py <url> <output.md>
    python3 elitigation_to_md.py <saved.html> <output.md>   (if html already downloaded)

The output MD carries YAML frontmatter with citation + source URL for integrity/traceability.
"""
import sys, re, html, urllib.request, os

def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    return urllib.request.urlopen(req, timeout=40).read().decode('utf-8', 'replace')

def strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()

def clean(s):
    s = html.unescape(s)
    s = s.replace('\xa0', ' ')
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

def main():
    src = sys.argv[1]
    out = sys.argv[2]

    if src.startswith('http'):
        raw = fetch(src)
    else:
        raw = open(src, encoding='utf-8', errors='replace').read()

    # ---- metadata ----
    # 1) citation from <title>
    m = re.search(r'<title>(.*?)</title>', raw, re.S)
    citation = clean(strip_tags(m.group(1))) if m else ''

    # 2) case name: <span class="caseTitle"> (legacy) or the <h1> (modern)
    case_name = ''
    mm = re.search(r'<span class="caseTitle"[^>]*>(.*?)</span>', raw, re.S)
    if not mm:
        mm = re.search(r'<h1[^>]*>(.*?)</h1>', raw, re.S)
    if mm:
        case_name = clean(strip_tags(mm.group(1)))

    # 3) metadata — parse the info table row by row. This is exact and works for
    #    BOTH markups. (The old flat-text "Label :" scan over-ran into the
    #    catchwords whenever the heuristic end-marker was absent, so the
    #    Parties field ended up swallowing the whole catchwords list.)
    meta = {}
    mtab = re.search(r'<table id="info-table".*?</table>', raw, re.S)
    if mtab:
        for row in re.finditer(
                r'<td[^>]*class="txt-label"[^>]*>(.*?)</td>.*?'
                r'<td[^>]*class="txt-body"[^>]*>(.*?)</td>', mtab.group(0), re.S):
            label = clean(strip_tags(row.group(1)))
            val = clean(strip_tags(row.group(2)))
            if label and val:
                meta[label] = val
    if not meta:
        # very old pages without info-table: fall back to the flat-text scan
        flat = strip_tags(raw)
        fields = ['Case Number', 'Decision Date', 'Tribunal/Court', 'Coram',
                  'Counsel Name(s)', 'Parties']
        end_marker = re.search(r'V\s*(?:K\s*)?Rajah|Judgment reserved', flat)
        header_end = end_marker.start() if end_marker else len(flat)
        header = flat[:header_end]
        for f in fields:
            m = re.search(re.escape(f) + r'\s*:\s*', header)
            if not m:
                continue
            start = m.end()
            next_pos = header_end
            for g in fields:
                gm = re.search(re.escape(g) + r'\s*:\s*', header[start:])
                if gm:
                    next_pos = min(next_pos, start + gm.start())
            meta[f] = clean(header[start:next_pos])
    if 'Parties' in meta and len(meta['Parties']) > 120:
        meta['Parties'] = meta['Parties'][:120] + '…'

    # ---- body paragraphs, in order ----
    # elitigation uses <p class="Judg-..."> in older judgments and
    # <div class="Judg-..."> in newer ones — match both.
    paras = []
    legacy = False
    for m in re.finditer(r'<(p|div) class="([Jj]udg-[^"]+)"[^>]*>(.*?)</\1>', raw, re.S):
        cls = m.group(2).lower()
        text = clean(strip_tags(m.group(3)))
        if not text:
            continue
        paras.append((cls, text))

    if not paras:
        # ---- LEGACY FALLBACK ----
        # Older judgments (roughly pre-2005) ship as raw HTML inside
        #   <div id="divJudgement"><div class="contentsOfFile"> …
        # with NO Judg-* classes at all. Structure there is:
        #   <table id="info-table"> … </table>      (metadata)
        #   <div class="txt-body"> … </div>          (catchwords, <br><br>-split)
        #   <p>…</p> / <blockquote><i>…</i></blockquote>   (judgment body)
        # Both <p> and <blockquote> must be walked in document order, otherwise
        # quoted passages disappear.
        legacy = True

        # isolate the judgment container, then drop the metadata table
        seg = raw
        for pat in (r'<div id="divJudgement".*?</div>\s*</div>',
                    r'<div class="contentsOfFile">(.*)',
                    r'<div id="divJudgement">(.*)'):
            mm = re.search(pat, raw, re.S)
            if mm:
                seg = mm.group(1) if mm.groups() else mm.group(0)
                break
        seg = re.sub(r'<table id="info-table".*?</table>', '', seg, flags=re.S)

        # 3a) catchwords = the leading <div class="txt-body"> before the body
        mcw = re.match(r'\s*<div class="txt-body">(.*?)</div>', seg, re.S)
        if mcw:
            for blk in re.split(r'<br\s*/?>\s*<br\s*/?>', mcw.group(1)):
                text = clean(strip_tags(blk))
                if text and '–' in text:
                    paras.append(('judg-catchword', text))
            seg = seg[mcw.end():]

        # 3b) judgment body: <p> and <blockquote> in document order
        for m in re.finditer(r'<(p|blockquote)\b[^>]*>(.*?)</\1>', seg, re.S):
            tag, inner = m.group(1).lower(), m.group(2)
            if tag == 'blockquote':
                for sub in re.split(r'<br\s*/?>\s*<br\s*/?>', inner):
                    sub = re.sub(r'</?p\b[^>]*>', ' ', sub)
                    text = clean(strip_tags(sub))
                    if text:
                        paras.append(('judg-quote-1', text))
                continue
            # a single <p> may still hold several paragraphs split by <br><br>
            for sub in re.split(r'<br\s*/?>\s*<br\s*/?>', inner):
                text = clean(strip_tags(sub))
                if not text:
                    continue
                text = text.lstrip(':–—-•· ').strip()
                if not text:
                    continue
                # legacy scans number paragraphs inline as either "39 text"
                # or "39. text" — normalise both to the **[39]** marker.
                m_num = re.match(r'^(\d{1,3})[.)]?\s+(.*)$', text, re.S)
                if m_num and len(text) > 80:
                    paras.append(('judg-1', f'{m_num.group(1)} {m_num.group(2)}'))
                elif (re.match(r"^[A-Z][A-Za-z0-9\s'\-/&,()]{2,70}$", text)
                      and len(text.split()) <= 9):
                    paras.append(('judg-heading-1', text))
                else:
                    paras.append(('judg-2', text))

    # ---- assemble markdown ----
    lines = []
    lines.append('---')
    lines.append(f'citation: "{citation}"')
    if case_name:
        lines.append(f'case_name: "{case_name}"')
    if 'Case Number' in meta:
        lines.append(f'case_number: "{meta["Case Number"]}"')
    if 'Decision Date' in meta:
        lines.append(f'decision_date: "{meta["Decision Date"]}"')
    if 'Coram' in meta:
        lines.append(f'coram: "{meta["Coram"]}"')
    if 'Parties' in meta:
        lines.append(f'parties: "{meta["Parties"]}"')
    lines.append(f'source: "{src}"')
    lines.append('type: case')
    lines.append('---')
    lines.append('')

    # case title line
    lines.append(f'# {case_name or citation}')
    if case_name and case_name != citation:
        lines.append(f'> {citation}')
    if legacy:
        lines.append('')
        lines.append('> ⚠️ **Legacy scan.** This judgment predates eLitigation paragraph '
                     'numbering — the text is complete and unaltered, but it carries no '
                     '`[n]` markers. Cite by page (SLR/SLR(R)) or by heading.')
    lines.append('')

    # metadata block
    if meta:
        for k in ['Case Number', 'Decision Date', 'Tribunal/Court', 'Coram',
                  'Counsel Name(s)', 'Parties']:
            if k in meta:
                lines.append(f'**{k}:** {meta[k]}')
        lines.append('')

    # body
    # A Judg-N div sometimes holds nothing but the paragraph number, because the
    # paragraph's content lives in the following element (usually a quote or a
    # list).  Hold such a number and attach it to the next content line,
    # otherwise it renders as a meaningless bare "5".
    pending = None
    for cls, text in paras:
        if re.match(r'judg-\d+(\s|$)', cls) and re.fullmatch(r'\d{1,3}', text.strip()):
            pending = text.strip()
            continue
        num, pending = pending, None
        num_pfx = f'**[{num}]** ' if num else ''

        if cls == 'judg-author':
            if num:
                lines.append(f'**{num_pfx}{text}**')
            else:
                lines.append('')
                lines.append(f'**{text}**')
                lines.append('')
        elif cls == 'judg-heading-1':
            lines.append(f'## {text}')
        elif cls == 'judg-heading-2':
            lines.append(f'### {text}')
        elif cls.startswith('judg-headg'):
            lines.append(f'#### {text}')
        elif cls == 'judg-catchword':
            lines.append(f'- {num_pfx}{text}')
        elif cls.startswith('judg-quote'):
            lines.append(f'> {num_pfx}{text}')
        elif cls.startswith('judg-list'):
            lines.append(f'- {num_pfx}{text}')
        elif re.match(r'judg-\d+(\s|$)', cls):
            # Numbered body paragraph.
            # NOTE: newer eLitigation markup appends utility classes, e.g.
            #   class="Judg-1 mb-3 text-justify  "   ← must NOT anchor with $
            # The reliable signal for a paragraph number is a leading integer in
            # the text itself; `Judg-2` / `Judg-3` are indented sub-paragraphs
            # which carry no number, so never synthesise one from the class.
            m_num = re.match(r'^(\d+)\s+(.*)$', text, re.S)
            if m_num:
                lines.append(f'**[{m_num.group(1)}]** {m_num.group(2)}')
            elif num:
                lines.append(f'**[{num}]** {text}')
            else:
                lines.append(text)
        else:
            lines.append(f'{num_pfx}{text}')

    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f'OK -> {out}  ({len(paras)} paragraphs)')

if __name__ == '__main__':
    main()
