# Media Playback Verification (v6-media)

## What was verified (mechanical, isolated — no desktop GUI used)

| Check | Method | Result |
|---|---|---|
| Video binary inside PPTX | unzip `ppt/media/video1.mp4`, `video2.mp4` present | PASS |
| Poster image inside PPTX | unzip `ppt/media/poster1.jpg`, `poster2.jpg` present | PASS |
| Valid media relationships | `slide6.xml.rels` + `slide15.xml.rels` contain `…/video` and `…/image` targets | PASS |
| Native video markup | `<a:videoFile r:link>` + `<p14:media r:embed>` in slide XML | PASS |
| Content types | `Extension="mp4"` (video/mp4) + `Extension="jpg"` (image/jpeg) | PASS |
| Package integrity | `zipfile.testzip()` == None | PASS |
| 49-slide count preserved | `<p:sldId id=…>` count == 49 | PASS |
| Deck opens in python-pptx | `Presentation()` parses with 0 errors | PASS |
| Clip codec/container | H.264 + AAC MP4, 1280×720, `+faststart` | PASS |
| Render integrity | LibreOffice headless converts to PDF (49 pages) with no error | PASS |

## Playback behavior
- Videos are embedded as native PowerPoint movie objects (`<a:videoFile>` + `p14:media`),
  with poster frames (`blipFill`). No `autoplay` attribute is set — playback is
  teacher-controlled (click to play).
- `p14:media` uses the PowerPoint 2010+ embedded-media extension (`p:ext` in `nvPr` +
  `cNvPr`), matching the repo's Phase 13J embedding convention.

## NOT verified (honest boundary)
- **Live in-application playback** (PowerPoint/Keynote actually playing the clip on
  screen) was **not** performed — this would require opening the visible macOS desktop,
  which is prohibited by the QA-isolation rule. Mechanical embedding integrity is
  verified; a bounded live-playback smoke test remains for a human or an approved
  isolated environment.
- A static thumbnail is NOT treated as proof of playback. This report does not claim
  playback-verified from a thumbnail.
