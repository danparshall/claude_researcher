"""Rebuild a design-tool deck's markdown text mirror from its .pptx.

A deck built in a design tool (Claude Design and the like) has no source
markdown and no builder. This script gives its markdown mirror the one property
it would otherwise lack: reproducibility. Run it after any change to the deck;
do not hand-edit the mirror. Paired asset of design_deck_reconciliation_skill.md.

Layout-aware, because the deck's chrome defeats naive extraction:
  - title   = largest type in the header band (a title placeholder is not set)
  - eyebrow = a line sitting wholly above the title; any other text, however
    high on the slide, is body - a split list's first row, level with the band,
    is a list item, not header text
  - persistent nav rails (top strip, right half) are dropped by
    geometry, not by frequency - frequency also catches real callout numerals
  - big-number callouts (and short figures set larger than their caption) are
    joined to the caption beneath them, and label/value rows to the text just
    past the label's right edge, as `**label** - value`; each shape is emitted
    once, and shapes within 50000 EMU of a row's top are read as one row
  - pictures repeating on 4+ slides, or covering the slide, are template chrome
  - highlighted runs (a:highlight in the run properties, any color) are wrapped
    as ==text==, adjacent highlighted runs merged into one pair of markers
  - no text shape is dropped silently: the only text left out is the nav rail
    and bare bullet glyphs; anything else reaches the title, eyebrow or a body line

Usage:  python3 extract_design_deck_mirror.py <deck.pptx> [-o out.md] [--visuals DIR]

Starter-package edition, mirrored from kit v6.11 (2026-10-10); record your own changes here.

Writes the mirror alongside the deck as <deck-stem>_text.md unless -o says otherwise.
--visuals points at a folder of PNGs; any picture in the deck byte-identical to one of
them is named in the mirror instead of being marked as a bare [image].
"""
from pptx import Presentation
from pptx.oxml.ns import qn
import hashlib, os, collections

import argparse, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
ap.add_argument('deck',
                help='the .pptx to mirror')
ap.add_argument('-o', '--out', default=None,
                help='output path (default: <deck-stem>_text.md beside the deck)')
ap.add_argument('--visuals', default=None,
                help='folder of PNGs to name matched pictures from '
                     '(default: <repo>/workspace/visuals if it exists)')
ARGS = ap.parse_args()

DECK = os.path.abspath(ARGS.deck)
if not os.path.exists(DECK):
    sys.exit(f"deck not found: {DECK}")
DECK_DIR = os.path.dirname(DECK)
OUT = os.path.abspath(ARGS.out) if ARGS.out else os.path.join(
    DECK_DIR, os.path.splitext(os.path.basename(DECK))[0] + '_text.md')

if ARGS.visuals:
    VISUALS = os.path.abspath(ARGS.visuals)
else:
    guess = os.path.abspath(os.path.join(DECK_DIR, '..', '..', '..', 'workspace', 'visuals'))
    VISUALS = guess if os.path.isdir(guess) else None

P = Presentation(DECK)
SW, SH = P.slide_width, P.slide_height

ours = {}
if VISUALS and os.path.isdir(VISUALS):
    for f in os.listdir(VISUALS):
        if f.endswith('.png'):
            ours[hashlib.sha1(open(os.path.join(VISUALS, f), 'rb').read()).hexdigest()] = f

def pt(sh):
    """Largest font size in the shape, in points."""
    best = 0
    for para in sh.text_frame.paragraphs:
        sz = para.font.size
        for r in para.runs:
            if r.font.size: sz = max(sz or r.font.size, r.font.size)
        if sz: best = max(best, sz.pt)
    return best

def raw(tf):
    """Plain text of a text frame, whitespace-normalized (used for the layout tests)."""
    return " ".join(tf.text.split())

def txt(tf):
    """Text of a text frame as the mirror shows it: highlighted runs wrapped as ==text==.

    The author marks decisions with highlight in the design tool; plain text would lose them.
    Whitespace between two highlighted runs belongs to the phrase, so a highlighted phrase
    split over several runs gets one pair of markers.
    """
    paras = []
    for p in tf.paragraphs:
        segs = []  # (text, highlighted), in reading order: runs, fields, line breaks
        for el in p._p:
            if el.tag in (qn('a:r'), qn('a:fld')):
                t_el, rpr = el.find(qn('a:t')), el.find(qn('a:rPr'))
                segs.append(((t_el.text or '') if t_el is not None else '',
                             rpr is not None and rpr.find(qn('a:highlight')) is not None))
            elif el.tag == qn('a:br'):
                segs.append((' ', False))
        hl = [h and bool(t.strip()) for t, h in segs]
        for k, (t, _) in enumerate(segs):
            if not t.strip():
                before = [hl[m] for m in range(k) if segs[m][0].strip()]
                after = [hl[m] for m in range(k + 1, len(segs)) if segs[m][0].strip()]
                hl[k] = bool(before and after and before[-1] and after[0])
        out, k = [], 0
        while k < len(segs):
            m = k
            while m < len(segs) and hl[m] == hl[k]:
                m += 1
            chunk = "".join(t for t, _ in segs[k:m])
            if hl[k]:
                chunk = ((" " if chunk[:1].isspace() else "") + "==" + " ".join(chunk.split())
                         + "==" + (" " if chunk[-1:].isspace() else ""))
            out.append(chunk)
            k = m
        paras.append("".join(out))
    return " ".join(" ".join(paras).split())

# --- pass 1: collect text shapes, find repeated chrome -----------------
slides = []
freq = collections.Counter()
for s in P.slides:
    items = []
    for sh in s.shapes:
        if sh.has_text_frame and raw(sh.text_frame):
            items.append(dict(t=txt(sh.text_frame), raw=raw(sh.text_frame),
                              top=sh.top or 0, left=sh.left or 0,
                              w=sh.width or 0, h=sh.height or 0, pt=pt(sh), kind='text'))
        elif sh.has_table:
            rows = [[txt(c.text_frame) for c in r.cells] for r in sh.table.rows]
            items.append(dict(t='', rows=rows, top=sh.top or 0, left=sh.left or 0, kind='table'))
        elif sh.__class__.__name__ == 'Picture':
            items.append(dict(t='', sha=sh.image.sha1, top=sh.top or 0, left=sh.left or 0,
                              w=sh.width or 0, h=sh.height or 0, kind='pic'))
    for it in items:
        if it['kind'] == 'text':
            freq[it['raw']] += 1
    slides.append(items)

CHROME = set()  # nav rail is removed geometrically below, not by frequency

pic_freq = collections.Counter()
for items in slides:
    for it in items:
        if it['kind'] == 'pic': pic_freq[it['sha']] += 1
PIC_CHROME = {h for h, c in pic_freq.items() if c >= 4}

# --- pass 2: structure each slide -------------------------------------
out = []
for n, items in enumerate(slides, 1):
    texts = [i for i in items if i['kind'] == 'text' and i['raw'] not in CHROME
             and i['raw'] not in ('▪', '•', '-')]
    # nav rail zone: top strip, right half
    texts = [i for i in texts if not (i['top'] < 600000 and i['left'] > 6900000)]

    head = [i for i in texts if i['top'] < 1300000] or texts
    eyebrow = title = None
    if head:
        title_it = max(head, key=lambda i: (i['pt'], -i['top']))
        title = title_it['t']
        # The eyebrow is a line wholly above the title (bottom edge at or above the title's
        # top); the one nearest the title wins. Everything else stays body. A fixed band
        # took a split list's first row, level with the band, for header text: its numeral
        # became the eyebrow and its text was dropped.
        above = [i for i in head if i is not title_it
                 and i['top'] + i['h'] <= title_it['top'] + 100000]
        eyebrow_it = max(above, key=lambda i: i['top']) if above else None
        eyebrow = eyebrow_it['t'] if eyebrow_it else None
        texts = [i for i in texts if i is not title_it and i is not eyebrow_it]

    # Reading order: rows top to bottom, each row left to right. Shapes whose tops differ by
    # less than ROW_TOL from the row's first shape are one row: a value box set a few EMU
    # above its label must not be read before it.
    ROW_TOL = 50000
    body_items, row = [], []
    for i in sorted([i for i in items if i['kind'] != 'text' or i in texts],
                    key=lambda i: (i['top'], i['left'])):
        if row and i['top'] - row[0]['top'] >= ROW_TOL:
            body_items += sorted(row, key=lambda i: i['left']); row = []
        row.append(i)
    body_items += sorted(row, key=lambda i: i['left'])

    used = set()  # indices already on a line, on their own or as a join partner
    lines = []
    for idx, it in enumerate(body_items):
        if idx in used: continue
        used.add(idx)
        if it['kind'] == 'pic':
            if it['sha'] in PIC_CHROME or it['w'] * it['h'] >= 0.9 * SW * SH: continue
            nm = ours.get(it['sha'])
            lines.append(f"- [image: {nm}]" if nm else "- [image]")
            continue
        if it['kind'] == 'table':
            r = it['rows']
            lines += ["", "| " + " | ".join(r[0]) + " |", "|" + "---|" * len(r[0])] \
                     + ["| " + " | ".join(x) + " |" for x in r[1:]] + [""]
            continue
        # callout: a figure with its caption directly beneath, same left. A figure is a big
        # number (28pt+), or a short text with a digit in larger type than the caption: a row
        # of stat boxes (40% / Cost, 40% / Reach) pairs each figure with its own caption,
        # not with the next figure along the row. A join never takes a shape already on a
        # line (`used`) or a twin with the same text.
        if it['pt'] >= 28 or (len(it['raw']) <= 12 and any(c.isdigit() for c in it['raw'])):
            cap = next((j for j, o in enumerate(body_items)
                        if j not in used and o['kind'] == 'text' and o['raw'] != it['raw']
                        and abs(o['left'] - it['left']) < 60000
                        and 300000 < o['top'] - it['top'] < 600000
                        and (it['pt'] >= 28 or o['pt'] < it['pt'])), None)
            if cap is not None:
                lines.append(f"- **{it['t']}** — {body_items[cap]['t']}")
                used.add(cap); continue
            if it['pt'] >= 28:
                lines.append(f"- **{it['t']}**"); continue
        # label / value row: short left label, text at same top starting just past its right
        # edge. A shape further along the row (past 200000 EMU of gap) is a sibling - the
        # next chip in a row of chips, or the next column - not this label's value.
        if it['w'] < 1800000 and len(it['raw']) < 40:
            for j, o in enumerate(body_items):
                if j in used or o['kind'] != 'text' or o['raw'] == it['raw']: continue
                if (abs(o['top'] - it['top']) < 40000
                        and it['left'] + it['w'] - 100000 < o['left'] < it['left'] + it['w'] + 200000):
                    lines.append(f"- **{it['t']}** — {o['t']}")
                    used.add(j); break
            else:
                lines.append(f"- {it['t']}")
            continue
        lines.append(f"- {it['t']}")

    # Safety net: every text item left after the title and eyebrow must be on a line of its
    # own (`- t`, `- **t**`, `- **t** - x`) or joined as a partner (`... - t`). One that is
    # not (a later rule consuming it by mistake) is emitted as a body line rather than lost.
    def on_a_line(t):
        return any(ln == f"- {t}" or ln.startswith(f"- **{t}**") or ln.endswith(f"\u2014 {t}")
                   for ln in lines)
    lines += [f"- {i['t']}" for i in texts if not on_a_line(i['t'])]

    notes = ""
    s = P.slides[n - 1]
    if s.has_notes_slide and s.notes_slide.notes_text_frame is not None:
        notes = " ".join(s.notes_slide.notes_text_frame.text.split())

    out.append(dict(n=n, eyebrow=eyebrow, title=title, lines=lines, notes=notes))

DECK_STEM = os.path.splitext(os.path.basename(DECK))[0]
HEADER = f"""# {DECK_STEM} — text mirror

Plain-text content of every slide of `{os.path.basename(DECK)}`, per the
markdown-mirror convention in `skills/design_deck_reconciliation_skill.md`.

**Not script-generated from a source; extracted from the deck.** The deck was
built in a design tool, so there is no source to regenerate the `.pptx` from.
This mirror, however, *is* reproducible: run `extract_design_deck_mirror.py`
against the deck, which reads the `.pptx` and rebuilds this file. Re-run it
when the deck changes; do not hand-edit.

Extraction is layout-aware: the slide title is the largest type in the header
band, the eyebrow a line wholly above it (any other text, however high, is a
body line), persistent nav rails are
dropped by geometry, big-number callouts are joined to their captions
(`**87%** — caption`), and label/value rows are joined the same way. Pictures
are marked `[image]`; where one is byte-identical to a visual in the
`--visuals` folder, it is named.

Text highlighted in the deck (the author's marks) is wrapped as `==text==`; a
highlighted phrase gets one pair of markers. The markers are the mirror's; they
are not characters on the slide.

---
"""

lines_out = [HEADER.rstrip() + "\n"]
for s_ in out:
    head = f"## Slide {s_['n']} — "
    head += (s_['eyebrow'] + " — " if s_['eyebrow'] and s_['eyebrow'] != s_['title'] else "")
    head += s_['title'] or "(no title)"
    lines_out.append(head + "\n")
    if s_['lines']:
        lines_out.append("\n".join(s_['lines']) + "\n")
    if s_['notes']:
        lines_out.append(f"**Notes:** {s_['notes']}\n")

# The whole mirror is built before the file is opened, and written as UTF-8 whatever the
# locale: a design deck carries glyphs outside cp1252, and a crash mid-write would leave a
# truncated mirror that the never-hand-edit rule makes a later session trust.
text = "\n".join(lines_out)
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(text)
print(f"wrote {OUT} ({len(out)} slides"
      + (f", {len(ours)} visuals indexed)" if ours else ", no visuals folder)"))
