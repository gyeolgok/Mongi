# E001 Emotion / Spatial Previz Review

- Episode ID: E001
- Review target: PR #6 `studio/E001-emotion-spatial-previz-v2`
- Decision: **REJECTED**
- Reviewer: Continuity Supervisor (Codex)
- Reviewed at: 2026-09-14T16:31:04.152Z
- Reviewed commit: `1804f166600e0008627ece069f7ea0794aad5610`
- Main / Set Registry baseline: `1e59b4a7790e46cb1e3b2e92477b16d43b3a88ff`
- Asset production: **BLOCKED**

## Summary

Emotion acting, timing, dialogue, Character constraints, Set/Prop references, temporary-phone handling, and mirror prohibition are sufficiently specified. The Previz cannot pass the integrated spatial gate because the Cuts 5–8 Camera Candidate does not define one reproducible camera geometry.

## Findings

| Area | Result | Review |
|---|---|---|
| Script and eight beats | PASS | Five alarm beats, fall, pause, recognition, and final step remain aligned with the approved script. |
| Emotion transition | PASS | Cuts 6–8 retain fatigue and move through gaze, body axis, one ear, tail tip, and weight shift without a sudden victory expression. |
| Character acting | PASS | Bipedal structure, restrained ear intensity, tail behavior, facial limits, and harmless fall constraints follow Character Lock. |
| Bubble/audio intent | PASS | Silent delivery, bubble dwell, silence, and SFX intent are actionable; no audio asset has been created. |
| Set/Prop/TEMP usage | PASS | `SET_HOME_001@1.0`, bed/rug Prop IDs, and `TEMP:E001_PHONE` are correctly scoped. |
| Mirror and Hard anchors | PASS | Mirror/horizontal flip prohibition and bed/central-path Hard anchors are explicitly preserved. |
| `CAM_CANDIDATE_HOME_BED_MEDIUM` | **PASS — E001 ONLY** | Cuts 1–4 retain `CAM_HOME_C` position, facing, and left/right relationship while changing only to a bed-centered medium framing. This approval does not create or register a reusable Camera ID. |
| `CAM_CANDIDATE_HOME_BED_PATH_MEDIUM` | **REJECT** | It uses `CAM_HOME_A/C` as plural anchors and specifies only the bed–path relationship. A single camera position, facing direction, frame bounds/visible directional anchors, and Cut 4→5 screen-direction continuity are not fixed. |

## Blocking issue and required revision

**Location**

- `episodes/E001/emotion-previz.md`
- Spatial scope: `CAM_CANDIDATE_HOME_BED_PATH_MEDIUM`
- Camera cells and required references for Cuts 5–8
- Production note: Camera/space recommendation

**Conflicting rule**

- `continuity/sets/SPATIAL_CONTINUITY.md`: a new camera must have its position and sightline defined on the floorplan before asset generation.
- `governance/WORKFLOW.md`: every repeated-location cut must carry a determinable Camera reference, and Hard Lock directions may not be reinterpreted.
- `SET_HOME_001@1.0`: registered cameras have distinct fixed positions, facing directions, and visibility rules; `CAM_HOME_A/C` is not one registered geometric anchor.

**Required result**

1. Choose exactly one of `CAM_HOME_A` or `CAM_HOME_C` as the sole geometric anchor for `CAM_CANDIDATE_HOME_BED_PATH_MEDIUM`.
2. Define the candidate's E001-only camera position, facing direction, and medium framing bounds relative to the floorplan.
3. State which directional anchors must remain visible and where the bed, central path/rug, Mongi, and phone appear in frame.
4. Preserve the screen direction from Cut 4 into the landing in Cut 5, then keep the same geometry through Cut 8.
5. Keep mirror/horizontal flip prohibited.
6. Keep the name as `CAM_CANDIDATE_*`; do not add it to `SET_REGISTRY.yaml` and do not assign an official reusable Camera ID.

## Non-blocking production cautions

- Keep `TEMP:E001_PHONE` on a consistent bed-edge side through Cuts 1–4 and in the same front paw after the fall.
- In Cut 3, “half-raised” ears must remain visibly below the rare full-ear-up state.
- Cut 4–5 should use the stated simplified silhouette to avoid limb, ear-count, and tail-attachment errors.

## Gate status

The Emotion/Spatial Previz is rejected pending the single spatial correction above. No image, background, action frame, audio, or `edit.json` asset may be generated. After revision, return Previz to `PENDING_REVIEW` and request Continuity review again.

---

## Re-review 1

- Decision: **REJECTED**
- Reviewer: Continuity Supervisor (Codex)
- Reviewed at: 2026-09-14T17:06:18.828Z
- Reviewed commit: `cdcf1cbe32be8a177e7f465594144533418c55d8`
- Main / Set Registry baseline: `1e59b4a7790e46cb1e3b2e92477b16d43b3a88ff`
- Asset production: **BLOCKED**

### Resolution check against the first rejection

| Required revision | Result |
|---|---|
| Choose one geometric anchor | PASS — `CAM_HOME_C` is now explicitly selected. |
| Define camera position, facing, and framing | PASS — position, 15–20° facing relation, crop, and frame bounds are specified. |
| Define visible anchors and subject/prop placement | PASS — bed, central path/rug, Mongi, and phone placement are specified. |
| Preserve Cut 4→5 and Cuts 5–8 screen geometry | PASS — right-bed to center/down-left landing and locked geometry through Cut 8 are specified. |
| Keep mirror/horizontal flip prohibited | PASS |
| Keep Candidate E001-only and unregistered | PASS |

### Remaining blocking inconsistency

The revised spatial scope, baseline view, Camera column, and production note correctly use `CAM_HOME_C` as the sole geometry. However, the cut-level **Required visual reference** cells still contain stale plural references:

- Cut 5 ends with `Home View A/C 및 중앙 통로`.
- Cut 8 ends with `Home View A/C, Soft Organic Bubble`.

Those fields are production inputs. Keeping `A/C` there conflicts with the sole-camera correction and can cause View A and View C to be mixed during image generation.

### Required correction

1. In the Cut 5 required-reference cell, replace the stale `Home View A/C` wording with **Home View C only**.
2. In the Cut 8 required-reference cell, replace the stale `Home View A/C` wording with **Home View C only**.
3. If View A remains in the general Official reference map, label it only as a non-camera structural cross-check; it must not be used as the geometric or generation reference for Cuts 5–8.
4. Do not change `SET_REGISTRY.yaml`, and do not register either Camera Candidate as an official reusable Camera ID.

All emotion, timing, Character, Prop/TEMP, mirror prohibition, and corrected camera-geometry content otherwise pass. After this textual consistency correction, return Previz to `PENDING_REVIEW` for final re-review. No assets may be generated before approval.

