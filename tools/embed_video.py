#!/usr/bin/env python3
"""
Embed a video (mp4) into a PPTX deck as a native, portable media relationship.

Mirrors the Phase 13J embedding convention:
  - registers video/mp4 + image/jpeg content types
  - adds a new slide whose .rels links rId2 -> poster image, rId3 -> video
  - the slide <p:pic> carries <a:videoFile r:link> + <p14:media r:embed>
  - the new slide is inserted into <p:sldIdLst> at a chosen position

Usage:
  python embed_video.py \
      --pptx production/slides/03-ch3-energy-speed-slides.pptx \
      --mp4 assets/supplemental/media/chapter-03/speed-and-energy-ramp-it-up-classroom-cut.mp4 \
      --poster /tmp/ml13/speed_poster.jpg \
      --after 16 \
      --title "WATCH — Ramp It Up in Action" \
      --subtitle "Optional video · 2:29 · Week 2 · Ramp It Up 2.0" \
      --prompt "THINK: Which variable changed, and which stayed the same?" \
      --badge "17"
"""

import argparse
import re
import shutil
import zipfile

NS = {
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}
CT_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def read_zip(zf: zipfile.ZipFile, name: str) -> str:
    return zf.read(name).decode("utf-8")


def build_slide_xml(title, subtitle, prompt, badge):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/><p:sp><p:nvSpPr><p:cNvPr id="2" name="Title Bar"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="12191695" cy="1417320"/></a:xfrm><a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="1F3A5F"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:style><a:lnRef idx="1"><a:schemeClr val="accent1"/></a:lnRef><a:fillRef idx="3"><a:schemeClr val="accent1"/></a:fillRef><a:effectRef idx="2"><a:schemeClr val="accent1"/></a:effectRef><a:fontRef idx="minor"><a:schemeClr val="lt1"/></a:fontRef></p:style><p:txBody><a:bodyPr rtlCol="0" anchor="ctr" wrap="square"/><a:lstStyle/><a:p><a:pPr algn="ctr"/></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="3" name="Title"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="457200" y="109728"/><a:ext cx="9855190" cy="868680"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" anchor="ctr"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="l"/><a:r><a:rPr sz="3200" b="1"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>{esc(title)}</a:t></a:r></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="4" name="Subtitle"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="457200" y="1024128"/><a:ext cx="9855190" cy="329184"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" anchor="ctr"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="l"/><a:r><a:rPr sz="1500" b="0"><a:solidFill><a:srgbClr val="C9D2E8"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>{esc(subtitle)}</a:t></a:r></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="5" name="Watch Badge"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="10820400" y="256032"/><a:ext cx="1203960" cy="420624"/></a:xfrm><a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="C05014"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:style><a:lnRef idx="1"><a:schemeClr val="accent1"/></a:lnRef><a:fillRef idx="3"><a:schemeClr val="accent1"/></a:fillRef><a:effectRef idx="2"><a:schemeClr val="accent1"/></a:effectRef><a:fontRef idx="minor"><a:schemeClr val="lt1"/></a:fontRef></p:style><p:txBody><a:bodyPr rtlCol="0" anchor="ctr" wrap="none"/><a:lstStyle/><a:p><a:pPr algn="ctr"/><a:r><a:rPr sz="1100" b="1"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>WATCH</a:t></a:r></a:p></p:txBody></p:sp><p:pic><p:nvPicPr><p:cNvPr id="6" name="Video 1"><a:extLst><a:ext uri="{{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230}}"><p14:media xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" r:embed="rId3"/></a:ext></a:extLst></p:cNvPr><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr><a:videoFile r:link="rId3"/><p:extLst><p:ext uri="{{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230}}"><p14:media xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" r:embed="rId3"/></p:ext></p:extLst></p:nvPr></p:nvPicPr><p:blipFill><a:blip r:embed="rId2"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="1895847" y="1720000"/><a:ext cx="8400000" cy="4725000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic><p:sp><p:nvSpPr><p:cNvPr id="7" name="Prompt"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="457200" y="6500000"/><a:ext cx="11277295" cy="300000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" anchor="ctr"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="ctr"/><a:r><a:rPr sz="1800" b="1"><a:solidFill><a:srgbClr val="1F3A5F"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>{esc(prompt)}</a:t></a:r></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:cNvPr id="8" name="Slide Number"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="11338560" y="6446520"/><a:ext cx="731520" cy="365760"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" anchor="t"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="r"/><a:r><a:rPr sz="1200" b="0"><a:solidFill><a:srgbClr val="555555"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>{esc(badge)}</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''


def build_slide_rels():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout7.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/POSTER_NAME"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/video" Target="../media/VIDEO_NAME"/></Relationships>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pptx", required=True)
    ap.add_argument("--mp4", required=True)
    ap.add_argument("--poster", required=True)
    ap.add_argument("--after", type=int, required=True, help="0-based index of slide to insert AFTER")
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--badge", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    # Read source package fully.
    zin = zipfile.ZipFile(args.pptx, "r")
    names = zin.namelist()
    # Determine media naming + next slide index.
    media_entries = [n for n in names if n.startswith("ppt/media/")]
    media_idx = 1
    while f"ppt/media/video{media_idx}.mp4" in media_entries or f"ppt/media/poster{media_idx}.jpg" in media_entries:
        media_idx += 1
    poster_name = f"poster{media_idx}.jpg"
    video_name = f"video{media_idx}.mp4"

    slide_files = [n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
    slide_idx = max(int(re.search(r"slide(\d+)\.xml", n).group(1)) for n in slide_files) + 1
    slide_file = f"ppt/slides/slide{slide_idx}.xml"
    slide_rels_file = f"ppt/slides/_rels/slide{slide_idx}.xml.rels"

    # Next presentation relationship id.
    pres_rels = read_zip(zin, "ppt/_rels/presentation.xml.rels")
    rid_nums = [int(m) for m in re.findall(r'Id="rId(\d+)"', pres_rels)]
    next_rid = max(rid_nums) + 1
    new_slide_rid = f"rId{next_rid}"

    # Build files.
    slide_xml = build_slide_xml(args.title, args.subtitle, args.prompt, args.badge)
    slide_rels = build_slide_rels().replace("POSTER_NAME", poster_name).replace("VIDEO_NAME", video_name)

    # Read poster bytes.
    with open(args.poster, "rb") as f:
        poster_bytes = f.read()
    with open(args.mp4, "rb") as f:
        video_bytes = f.read()

    # Content types: ensure mp4 + jpg defaults.
    ct = read_zip(zin, "[Content_Types].xml")
    if 'Extension="mp4"' not in ct:
        ct = ct.replace(
            "</Types>",
            '<Default Extension="mp4" ContentType="video/mp4"/></Types>',
        )
    if 'Extension="jpg"' not in ct:
        ct = ct.replace(
            "</Types>",
            '<Default Extension="jpg" ContentType="image/jpeg"/></Types>',
        )
    ct = ct.replace(
        "</Types>",
        f'<Override PartName="/{slide_file}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>',
    )

    # presentation.xml: insert sldId in order.
    pres = read_zip(zin, "ppt/presentation.xml")
    sld_lst = re.search(r"<p:sldIdLst>(.*?)</p:sldIdLst>", pres, re.S).group(1)
    sld_ids = re.findall(r'<p:sldId\b[^>]*/>', sld_lst)
    if args.after + 1 > len(sld_ids):
        raise SystemExit(f"--after {args.after} out of range (deck has {len(sld_ids)} slides)")
    new_sld_id = f'<p:sldId id="{256 + slide_idx - 1}" r:id="{new_slide_rid}"/>'
    sld_ids.insert(args.after + 1, new_sld_id)
    new_sld_lst = "".join(sld_ids)
    start = pres.find("<p:sldIdLst>") + len("<p:sldIdLst>")
    end = pres.find("</p:sldIdLst>")
    pres = pres[:start] + new_sld_lst + pres[end:]

    # presentation.xml.rels: append new slide relationship.
    pres_rels = pres_rels.replace(
        "</Relationships>",
        f'<Relationship Id="{new_slide_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/{slide_file.split(chr(47))[-1]}"/></Relationships>',
    )

    # Write output package.
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            if n in ("[Content_Types].xml", "ppt/presentation.xml", "ppt/_rels/presentation.xml.rels"):
                continue
            zout.writestr(n, zin.read(n))
        zout.writestr("[Content_Types].xml", ct)
        zout.writestr("ppt/presentation.xml", pres)
        zout.writestr("ppt/_rels/presentation.xml.rels", pres_rels)
        zout.writestr(slide_file, slide_xml)
        zout.writestr(slide_rels_file, slide_rels)
        zout.writestr(f"ppt/media/{poster_name}", poster_bytes)
        zout.writestr(f"ppt/media/{video_name}", video_bytes)
    zin.close()
    print(f"OK: wrote {args.out} (slide {slide_file}, video {video_name}, poster {poster_name}, {new_slide_rid})")


if __name__ == "__main__":
    main()
