# Media Storage Recommendation — Phase 2

> How the ~2.0 GB standalone video library (75 MP4 files) is preserved OUTSIDE ordinary Git.

## Principle
Video binaries must NOT enter ordinary Git (`.gitignore` already excludes
`assets/supplemental/`; `source-intake/*/media/` and candidate `media/` dirs are
new and must stay out too). They are preserved by (a) an exact SHA-256 manifest in
this repo, and (b) a verified copy in external storage. **The manifest exists now;
the external copy is NOT yet verified.**

## What is covered
- `assets/supplemental/media/` — 47 files (Chapter 1–7 + Unit 2 explainer library).
- `source-intake/2026-10-09-chapter-1/media/` — 18 files (Chapter 1 intake originals).
- `production/candidates/*/…/media/` — 6 derivative clips + 4 full-source fallbacks
  (duplicates of `assets/supplemental/media` content; see duplicate list).
- **Exact manifest:** `work/ch2-media-storage/MEDIA_SHA256_MANIFEST.json`
  (75 files, SHA-256 + size each). 2.00 GB total.

## Duplicate note (dedup before upload)
Several media files are byte-identical across locations (e.g.
`How_Scientists_Spot_Invisible_Energy.mp4`, `Stored_Energy.mp4`,
`Why_Still_Objects_Secretly_Have_Energy.mp4`, `Marble_Collisions…`,
`Ch_2__Motion_Energy_in_Action`, `Things_on_the_Move`). Upload one canonical copy
per unique SHA-256, not per path. `inventory/byte_identical_duplicates.txt` holds
the full dedup map.

## Recommended destination: school Google Drive (mirror = NOT verified)
- **Account:** `owen.reagan@thalesacademy.org` (school) — primary; `oreagan81@gmail.com` (personal) — backup.
- **Folder:** `Core Knowledge Curriculum/Unit 1 - Energy Transfer and Transformation/media-archive/`
- **Storage IDs:** the Google Doc/Slides IDs are already recorded in
  `docs/provenance/SOURCE_PROVENANCE.md`; media files have no Drive IDs yet — they
  must be assigned at upload time and recorded back into the manifest.
- **Versioning:** Drive version history + dated folder `media-archive-2026-10-10/`.
- **Redundancy:** two accounts (school + personal) AND local disk (current location).
- **Classroom playback:** media is also embedded inside the candidate PPTX (teacher-controlled),
  so the standalone files are a fallback only.

## Restore procedure (when verified)
1. Upload each unique SHA-256 file to the Drive archive folder.
2. Re-download to a scratch dir and recompute SHA-256; compare to
   `MEDIA_SHA256_MANIFEST.json` (must match exactly).
3. Record the Drive file ID per path into the manifest (`drive_id` field).
4. Update this file from "NOT verified" to "VERIFIED".

## Current status
- **NOT VERIFIED** — Google Drive account access and uploaded-byte check have not
  been performed. Local disk is currently the ONLY copy. **This media is not yet
  backed up off-site.**

## Git LFS
Not adopted. LFS would be an alternative if the owner prefers Git-hosted media
(requires GitHub LFS enablement + bandwidth); current recommendation is Drive +
manifest, consistent with `docs/technical/BINARY_ASSET_POLICY.md`.
