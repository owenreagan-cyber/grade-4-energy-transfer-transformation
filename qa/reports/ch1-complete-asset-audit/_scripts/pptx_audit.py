#!/usr/bin/env python3
"""Deterministic PPTX forensics: text, notes, fonts, media (dims/type/hash), slide size.
Usage: python3 pptx_audit.py DECK.pptx OUT_DIR [--dump-media]
"""
import sys, zipfile, hashlib, json, re, io
from xml.etree import ElementTree as ET
from pathlib import Path
from collections import Counter


def local(tag):
    return tag.split('}')[-1]


def extract_text(xml_bytes):
    root = ET.fromstring(xml_bytes)
    texts = []
    for t in root.iter():
        if local(t.tag) == 't':
            if t.text:
                texts.append(t.text)
    return texts


def extract_fonts_and_colors(xml_bytes):
    root = ET.fromstring(xml_bytes)
    fonts = Counter()
    solid_colors = Counter()
    for rPr in root.iter():
        if local(rPr.tag) != 'rPr':
            continue
        for latin in rPr:
            if local(latin.tag) in ('latin', 'ea') and latin.get('typeface'):
                fonts[latin.get('typeface')] += 1
        for child in rPr:
            if local(child.tag) == 'solidFill':
                for c in child:
                    if local(c.tag) == 'srgbClr':
                        solid_colors[c.get('val')] += 1
    return dict(fonts), dict(solid_colors)


def image_info(data):
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(data))
        return im.size[0], im.size[1], im.format
    except Exception:
        return None, None, None


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    deck = sys.argv[1]
    out_dir = Path(sys.argv[2])
    dump_media = '--dump-media' in sys.argv
    out_dir.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(deck)
    names = z.namelist()

    pres_xml = z.read('ppt/presentation.xml')
    proot = ET.fromstring(pres_xml)
    sldSz = proot.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldSz')
    size = (sldSz.get('cx'), sldSz.get('cy')) if sldSz is not None else None

    slide_files = sorted(
        [n for n in names if re.match(r'ppt/slides/slide\d+\.xml$', n)],
        key=lambda n: int(re.search(r'(\d+)', n.split('/')[-1]).group(1)),
    )
    media_files = [n for n in names if n.startswith('ppt/media/')]
    media_meta = {}
    for m in media_files:
        data = z.read(m)
        w, h, fmt = image_info(data)
        media_meta[m] = {
            'bytes': len(data), 'w': w, 'h': h, 'format': fmt,
            'sha256': sha(data), 'ext': Path(m).suffix.lower(),
        }

    slides_out = []
    for sf in slide_files:
        num = int(re.search(r'(\d+)', sf.split('/')[-1]).group(1))
        xml = z.read(sf)
        texts = extract_text(xml)
        fonts, colors = extract_fonts_and_colors(xml)
        rels_path = f'ppt/slides/_rels/slide{num}.xml.rels'
        rels = []
        if rels_path in names:
            rroot = ET.fromstring(z.read(rels_path))
            for rel in rroot:
                target = rel.get('Target', '')
                if 'media' in target:
                    rels.append(target)
        notes_text = ''
        notes_path = f'ppt/notesSlides/notesSlide{num}.xml'
        if notes_path in names:
            notes_text = '\n'.join(extract_text(z.read(notes_path)))
        slides_out.append({
            'num': num,
            'text': ''.join(texts),
            'text_blocks': texts,
            'fonts': fonts,
            'colors': colors,
            'media_rels': rels,
            'notes': notes_text,
        })

    result = {
        'deck': Path(deck).name,
        'slide_size_cx_cy': size,
        'slide_size_in': (int(size[0]) / 914400, int(size[1]) / 914400) if size else None,
        'slide_count': len(slide_files),
        'media_count': len(media_files),
        'media': media_meta,
        'slides': slides_out,
    }
    with open(out_dir / 'audit.json', 'w') as f:
        json.dump(result, f, indent=1)

    print(f"DECK: {Path(deck).name}")
    print(f"  slides={len(slide_files)} size_in={result['slide_size_in']} media={len(media_files)}")
    for s in slides_out:
        txt = re.sub(r'\s+', ' ', s['text'].replace('\n', ' ')).strip()[:130]
        media = [Path(m).name for m in s['media_rels']]
        print(f"  S{s['num']:02d} media={media} :: {txt}")
    print("  -- media files --")
    for m, meta in sorted(media_meta.items()):
        print(f"  {Path(m).name}: {meta['w']}x{meta['h']} {meta['format']} {meta['bytes']}B sha={meta['sha256'][:12]}")
    print("  -- fonts --")
    allf = Counter()
    for s in slides_out:
        for f, c in s['fonts'].items():
            allf[f] += c
    for f, c in allf.most_common():
        print(f"  {f}: {c}")
    if dump_media:
        med_dir = out_dir / 'media'
        med_dir.mkdir(exist_ok=True)
        for m in media_files:
            data = z.read(m)
            (med_dir / Path(m).name).write_bytes(data)
        print(f"  dumped {len(media_files)} media files to {med_dir}")


if __name__ == '__main__':
    main()
