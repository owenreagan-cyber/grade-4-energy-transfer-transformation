# Chapter 3 Debug Tool Disposition

Every untracked `tools/ch3_*.py` script is classified here. None may seal
certification evidence. They are left in place (not deleted blindly) pending
the F-4/F-8-adjacent decision to retire or track them.

Rules applied:
- `DEBUG_ONLY` — read-only/inspection probes; cannot write certifying evidence.
- `RETIRE` — historically produced or laundered Chapter 3 evidence; must not be
  on the certification path and is superseded by tracked `tools/chapter_qa/*`.

| path | purpose | historically wrote | certification dependency | disposition | maySealEvidence |
|---|---|---|---|---|---|
| `tools/ch3_emit_chapter_spec.py` | emit CHAPTER_SPEC evidence | yes | none (superseded by `mandatory_producers.emit_chapter_spec`) | RETIRE | NO |
| `tools/ch3_emit_source.py` | emit source evidence | yes | none (superseded by `source_audit`) | RETIRE | NO |
| `tools/ch3_emit_structure.py` | emit structure evidence | yes | none | RETIRE | NO |
| `tools/ch3_seal_remaining.py` | seal remaining gates | yes | none | RETIRE | NO |
| `tools/ch3_reseal_attack.py` | reseal after detector changes | yes | none | RETIRE | NO |
| `tools/ch3_reseal_dependents.py` | reseal invalidated dependents | yes | none | RETIRE | NO |
| `tools/ch3_reseal_loop2.py` | reseal visual/render/PDF | yes | none | RETIRE | NO |
| `tools/ch3_reseal_region.py` | reseal playbook region | yes | none | RETIRE | NO |
| `tools/ch3_hook_reasons.py` | print invalidation/judge reasons | no | none | DEBUG_ONLY | NO |
| `tools/ch3_judge.py` | run judge + hook for build | no | none | DEBUG_ONLY | NO |
| `tools/ch3_cause_probe.py` | image pixel probe | no | none | DEBUG_ONLY | NO |
| `tools/ch3_classify_probe.py` | classify title/content pages | no | none | DEBUG_ONLY | NO |
| `tools/ch3_find_escape.py` | find mutation escapes | no | none | DEBUG_ONLY | NO |
| `tools/ch3_margin_probe.py` | margin ink probe | no | none | DEBUG_ONLY | NO |
| `tools/ch3_n2_probe.py` | N2 anchor probe | no | none | DEBUG_ONLY | NO |
| `tools/ch3_observe_sync.py` | sync observation probe | no | none | DEBUG_ONLY | NO |
| `tools/ch3_overlap_debug.py` | text overlap debug | no | none | DEBUG_ONLY | NO |
| `tools/ch3_render_debug.py` | render debug | no | none | DEBUG_ONLY | NO |
| `tools/ch3_slide6_pairs.py` | slide 6 text pairs | no | none | DEBUG_ONLY | NO |
| `tools/ch3_slide_margin.py` | slide margin bands | no | none | DEBUG_ONLY | NO |
| `tools/ch3_text_probe.py` | text extraction probe | no | none | DEBUG_ONLY | NO |
| `tools/ch3_title_ink.py` | title ink probe | no | none | DEBUG_ONLY | NO |
| `tools/ch3_visual_summary.py` | visual map summary | no | none | DEBUG_ONLY | NO |

All scripts: **maySealEvidence = NO**. Untracked code may never produce
release-certifying evidence (F-4). The tracked `tools/chapter_qa/*` producers
are the only certification path.
