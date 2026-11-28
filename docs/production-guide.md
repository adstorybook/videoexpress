# Production guide and handoff — TheStorybook_ad

**Last audited:** 2026-11-27  
**Active branch:** `feat/video-pipeline-foundation`  
**Branch relationship:** diverged from `main`; the 2026-11-27 pre-update comparison showed 89 commits ahead and 2 behind. This audit adds further commits, so refresh the live comparison before any integration. No merge or cherry-pick was performed. Do not merge without approval. Main-only commits reviewed and are outside this two-film scope.

See [Start here](start-here.md) for the complete reset audit and next-shot handoff.

## Current project status

### The Clever Little Rabbits
- Script/storyboard: source-checked draft; 10 scenes, target 300 seconds.
- Workflow: `assets_generating`.
- Four reviewed video clips are logged as partial coverage only:
  - `rabbit-opening-clip-001` — 6.04 seconds, family opening/reference.
  - `rabbit-scene2-hug-001` — 6.04 seconds, mother/children hug.
  - `rabbit-scene2-departure-001` — 6.04 seconds, mother leaves and children wave; **Scene 2**.
  - `rabbit-scene3-wolf-arrival-001` — 10.04 seconds, wolf approaches cottage; **Scene 3**.
- `wolf-character-reference-001` — approved reference in VideoExpress; source image is not separately available in Git.
- Next shot in order: 10-second Wolf knock at the cottage door, using Wolf reference and (if available) cottage frame. Rabbit reaction, Wolf imitation, and refusal prompts are queued, but no uploaded clips are logged for these shots as of 2026-11-24. Scene 2 also still needs a clear visual safety-instruction shot.
- No scene is complete; no final video is assembled or rendered.

### Mother Magpie
- Script/storyboard: source-checked draft; 9 scenes, target 300 seconds.
- Workflow: `script_draft`.
- No generated assets are logged yet. The visual prompt pack now includes isolated reference prompts for both mothers, both chick pairs, the eagle, and the two-nest tree layout.
- Next: approve the character/location references, then generate the establishing shot of the large tree with two neighboring nests and exactly two chicks in each.

## Render target
- 1920×1080, 16:9, 24 fps where supported; confirm actual export metadata.
- Separate MP4s: `the-clever-little-rabbits.mp4` and `mother-magpie.mp4`.
- Runtime target: exactly 05:00 each. Trim/assemble to narration end if needed.
- Warm, clear, consistent narrator; subtle sound design; music below narration; captions timed and spell-checked.
- No AI-generated text in scene visuals; title/end cards are added during editing and kept within runtime.

## Continuity constraints

### Rabbits
- Mother and exactly three siblings; preserve approved character/outfit references.
- Wolf design: blue-violet fur, brown floppy hat, green outfit; non-frightening.
- Tail-trap gag non-graphic. Preserve cottage continuity.
- Scene 2 includes the mother’s safety instruction and departure; the departure clip is partial coverage.

### Magpie
- Two nests on fixed neighboring branches; two chicks in each nest initially.
- Blue eagle with orange beak/feet; capture sequence non-graphic.
- Neighbor mother adopts the two orphaned chicks; final family has exactly four chicks.
- Mother A does not return in this story.

## Production process
1. Lock script, scene beats, and character designs.
2. Generate approved character/location reference images.
3. Generate 5–10 second coverage shots per beat, maintaining reference IDs.
4. Record prompt, asset ID, provider/model, duration, resolution, frame rate, checksum (if file available), and review status.
5. Assemble clips to storyboard timing with narration, music, SFX, transitions, and captions.
6. Export a private/draft MP4 and review the complete film.
7. Correct defects, rerender, and repeat QA.
8. Obtain explicit approval before any upload/publication or visibility/schedule change.

## QA checklist
- [ ] Story accuracy and continuity
- [ ] No missing/extra characters or distorted/flickering imagery
- [ ] Character designs, colors, outfits, and location remain consistent
- [ ] Narration is clear, correctly paced, and not clipped
- [ ] Music and SFX do not overpower speech
- [ ] Captions accurate, readable, and safe-area aligned
- [ ] Full HD, 16:9, no unwanted text or watermarks
- [ ] Exact runtime and clean ending
- [ ] Entire export watched end-to-end
- [ ] User approval recorded before upload

## VideoExpress integration
Use the signed-in browser editor while API support remains unverified. Do not use undocumented endpoints, browser cookies, or credentials in Git. Paid generation should be explicitly confirmed; record credits/costs where shown.


## Validation update (2026-11-25)
- Manifest validator now checks that every character `reference_asset_ids` entry resolves to a declared asset, in addition to scene asset references.
- Regression tests cover missing character references and reject a video asset used as a character reference; character references must resolve to declared image assets.
- The branch's push workflow is configured to run on development-branch updates; the connector cannot read push-triggered run status, so CI completion is not claimed in this audit.


## Pre-render QA baseline (2026-11-26)
- Added `projects/the-clever-little-rabbits/qa-report.json` and `projects/mother-magpie/qa-report.json`; both are explicitly `incomplete`, have no render/export, and carry no approval.
- Linked each baseline from its project manifest via `qa_report_ref`.
- Rabbit baseline records four partial video clips plus the approved Wolf reference; the cottage-location mismatch remains a warning. The next required clip is still the 10-second Wolf knock.
- Magpie baseline records a valid 300-second/9-scene plan but no generated image/video assets; create and approve character/location references before Scene 1 footage.
- These are pre-render tracking reports, not a claim that a final video has passed QA.


## 2026-11-27 audit — next-shot gate and CI readback
- Re-read both manifests, both QA baselines, both prompt packs, the project validator, unit tests, schemas, and branch workflow.
- Live branch comparison before today's writes: `feat/video-pipeline-foundation` is **89 commits ahead and 2 behind `main`** (diverged). No integration was attempted.
- Rabbit inventory is unchanged: four partial video clips and one approved Wolf character reference. No new Wolf-knock, rabbit-reaction, imitation, or refusal clip was received in this audit.
- Added an execution card and objective acceptance gate for the 10-second Wolf-knock shot: reference image, cottage reference if available, three visible knocks, closed door, continuity checks, and actual-file metadata inspection. Approval remains partial Scene 3 coverage.
- Rabbit QA baseline now explicitly tracks the next-shot gate as a warning; overall QA remains incomplete and no render or approval is claimed.
- Verified the latest pre-update GitHub Actions push run for head `455cbff86d6e808130b8ce2a45454b6c7f91103b` completed successfully on 2026-11-26 (run [45785349081](https://github.com/adstorybook/videoexpress/actions/runs/45785349081)). Today's documentation/manifest commits will trigger a new run; its result must be checked separately.
- Mother Magpie remains at script/storyboard draft with nine scenes and no generated assets. Next task is approved character/location reference images, then the two-nest establishing shot.
- No VideoExpress generation, credits, final render, merge, deployment, or publication occurred.


## 2026-11-28 audit — asset integrity and regression coverage
- Reconciled the stale Rabbit history note so Mother Rabbit's departure is consistently recorded as Scene 2, not Scene 3.
- Added regression tests for the approved opening clip's 6-second / 1920×1080 / 16:9 partial-reference contract and for the Scene 2 departure / Scene 3 Wolf-arrival mapping.
- Added an explicit Scene 2 safety-instruction pickup prompt. It remains required before final assembly; the active next-generation sequence remains Wolf knock → rabbit reaction → Wolf imitation → rabbit refusal.
- Refreshed both QA baseline timestamps. Rabbit QA remains incomplete with no render/export/approval; Magpie QA remains incomplete with no generated references or footage.
- Verified the previous branch-head Actions run 45964657962 for commit 6fbcf00 succeeded before this update. The current commit's push validation must be read back separately.
