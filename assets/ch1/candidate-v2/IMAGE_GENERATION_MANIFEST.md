# Chapter 1 Visual Candidate — Image Generation Manifest

Generated: 2026-10-09  
Mode: built-in OpenAI image generation tool (not fallback CLI)  
Use case: scientific-educational classroom slide visuals  
Provenance: **CUSTOM** raster artwork, conceptually **ADAPTED** from the authoritative Chapter 1 science content. No authoritative source files were modified.

## Shared prompt constraints

All prompts requested a premium editorial science-textbook look for Grade 4, realistic physical objects and lighting, 16:9 or crop-safe composition, no people identifiable as real individuals, no logos, no watermark, no baked-in labels, no fantasy glow, no visible “energy,” and no scientifically misleading effects. The generated images serve as observation evidence; the editable slide layer supplies all instructional text.

## Accepted prompt set

| Asset | Slide use | Generation prompt |
|---|---|---|
| `slide-01-opener.png` | 1 | Cinematic but realistic elementary science classroom still life at dusk: desk lamp switched on over an open notebook, yellow pencil, small orange ball, books and globe in the background; warm pool of light against a deep navy room; spacious left side for title; premium museum-education photography. |
| `slide-04-dark-bright.png` | 4–5 | Exact matched classroom corner shown before and after a desk lamp turns on; split composition, same camera and objects, left side dim and right side clearly brighter; change must come only from the lamp; realistic exposure and no magical glow. |
| `slide-09-pencil-before-after.png` | 6, 9, 11, 28, 36–37 | Exact matched tabletop before/after comparison with the same yellow pencil and black electric sharpener; before pencil is dull and longer, after pencil is shorter and sharply pointed with ordinary shavings visible; same camera, scale, background, and lighting. |
| `slide-10-energy.png` | 10 | Close classroom demonstration: a child-safe hand pushes a small red toy car toward a wooden block on a clean tabletop; realistic motion cue without blur tricks or glowing energy; uncluttered background and crop-safe framing. |
| `slide-14-seashore.png` | 14 | Calm rocky seashore with small waves reaching wet sand; observable movement and sand shift, overcast natural light, realistic elementary science field-observation photograph, ample dark-water/sky area for slide overlay. |
| `slide-17-five-forms.png` | 17, 19 | Five coordinated realistic panels in one horizontal image: rolling orange ball, ringing handbell, lit desk lamp, steaming warm mug, electric fan operating; consistent classroom/lab setting, each example visually distinct, no text or icons. |
| `slide-22-stored-energy.png` | 22, 38–39 | Two hands safely hold a stretched rubber band still over a classroom tabletop; tension is clear from shape and posture but nothing is moving yet; centered, uncluttered, realistic science demonstration. |
| `slide-25-stored-examples.png` | 25, 44 | Three coordinated realistic tabletop scenes: battery beside an open flashlight, stretched rubber band held still, and apple held above a low stool; consistent neutral classroom background, no labels, no unsafe action. |
| `slide-28-evidence.png` | 28 | Three coordinated before/after evidence scenes: lamp turns a dark work area bright, pencil becomes shorter and sharper with shavings, orange ball crosses a floor marker; realistic matched evidence, no text, no visible energy. |
| `slide-33-reflection.png` | 33 | Soft, subdued classroom science still life with notebook, pencil, desk lamp, ball, and flashlight; warm cream and navy palette, shallow depth of field, generous clean central area for reflection writing. |
| `slide-45-close.png` | 45 | Dark premium chapter-closing still life: lamp, notebook, yellow pencil, orange ball, battery and flashlight arranged on a classroom desk; subtle warm light, deep navy shadows, clean composition with space for closing message. |

## Excluded generation

`slide-06-pencil-before.png` was an early standalone close-up. It was rejected because it did not provide the same-object matched comparison needed for strong evidence. Slides 6 and 9 instead use crops from `slide-09-pencil-before-after.png`.

