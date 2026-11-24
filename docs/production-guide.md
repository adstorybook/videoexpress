# Production guide and handoff — TheStorybook_ad

**Last audited:** 2026-11-24  
**Active branch:** `feat/video-pipeline-foundation`  
**Branch relationship:** diverged from `main`; 63 ahead, 2 behind (checked 2026-11-24). Do not merge without approval. Main-only commits reviewed and are outside this two-film scope.

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


## Validation update (2026-11-24)
- Manifest validator now checks that every character `reference_asset_ids` entry resolves to a declared asset, in addition to scene asset references.
- A regression test covers missing character reference assets.
- The branch's push workflow is configured to run on development-branch updates; the connector cannot read push-triggered run status, so CI completion is not claimed in this audit.
