# Start here — VideoExpress production reset and audit

**Audited:** 2026-11-25  
**Active development branch:** `feat/video-pipeline-foundation`  
**Repository:** https://github.com/adstorybook/videoexpress  
**Channel:** TheStorybook_ad

This is the current source of truth for restarting the production workflow from the beginning. Keep production records on the development branch; do not merge into `main`, publish, or change upload visibility without explicit approval.

## 0. Project audit

- The foundation branch contains story manifests, scripts, storyboards, scene prompts, schemas, validation, tests, workflow documentation, and GitHub Actions.
- The validator and regression suite were extended on 2026-11-25. The connected GitHub tools do not expose a confirmed push-run result for the current branch head; do not infer CI success from the workflow configuration.
- **Branch safety:** the development branch is now diverged from `main` (2 commits behind as checked 2026-11-25; 75 commits ahead; the development branch remains ahead and diverged). The two main-only commits add separate Hare-and-Tortoise workflow notes and a future five-story series handler; these are not part of the current two-film scope. Do not merge or cherry-pick without explicit approval.
- VideoExpress 3.5 is available through the signed-in browser editor. A field labelled API key is not proof of a documented API; the API integration remains unverified.
- The original scanned story PDF is not currently available in the Library search. Existing GitHub scripts were previously source-checked; if exact source re-verification is needed, re-upload the PDF.
- A separate user workflow document contains expanded 14-scene retellings and character names (e.g. Mama Hazel/Pip/Clover/Nutmeg/Grizzle and Mama Nell/Tilly/Dot/Dash/Pebble/Button). It differs from the GitHub drafts' scene counts and some character descriptions. **Do not silently mix these versions.** The GitHub source-checked drafts remain the working canon until the user approves a reconciliation.

## 1. Locked output targets

For each story:
- Separate 5-minute film (300 seconds)
- Landscape 16:9
- 1920×1080 Full HD
- Pixar-inspired 3D storybook look (descriptive style only)
- English narration, consistent voice, music under narration, checked captions
- Short title/end cards within the runtime
- MP4 export, full-film review before approval

## 2. Story 1 — The Clever Little Rabbits

**Status:** Assets generating; no finished scene or film yet.

Reviewed partial assets in VideoExpress:
1. `rabbit-opening-clip-001` — 6.04 sec family opening/reference
2. `rabbit-scene2-hug-001` — 6.04 sec mother and children hug; partial Scene 2
3. `rabbit-scene2-departure-001` — 6.04 sec mother leaves and children wave; partial Scene 2
4. `rabbit-scene3-wolf-arrival-001` — 10.04 sec wolf approaches cottage; partial Scene 3
5. `wolf-character-reference-001` — approved Wolf reference stored in VideoExpress; original file/checksum unavailable

**Next shot to generate (sequence order):** (1) 10-second Wolf knocks at the cottage door; (2) rabbits hear/react to the knock; (3) Wolf imitates Mother Rabbit's voice; (4) rabbits refuse and recognize the voice. Prompts have been shared for all four, but **no uploaded clips are logged for these shots as of 2026-11-24**. Scene 2 also still needs a clear visual safety-instruction shot. Use the approved Wolf reference for Wolf shots; rabbit group reference for interior reaction shots; if available, add a cottage frame to anchor exterior location. Do not skip the knock/reaction beats.

The four video clips are partial coverage only. Do not stretch them to fill long scenes or claim any scene is complete.

## 3. Story 2 — Mother Magpie

**Status:** Script/storyboard draft; no generated assets logged.

The visual prompt pack now contains copy-ready reference prompts for both mothers, both chick pairs, the blue eagle, and the tree with two nests. Start with:
1. Generate and approve the character reference sheets and location reference.
2. A wide establishing clip showing the same large tree and exactly two nests (two chicks in each nest).
3. Lock nest geography and chick markings before scene generation.

Maintain source-story constraints: Mother A is carried away and does not return; the neighbor mother adopts the two chicks; the final family has four chicks; eagle sequence is non-graphic.

## 4. Production sequence

1. **Canon check:** confirm title, script, scene count, character descriptions, and source accuracy; reconcile the separate expanded workflow document before adopting it.
2. **Character references:** create and approve one master image per character plus a group/location reference.
3. **Scene coverage:** generate short 5–10 second clips; track prompt, reference IDs, duration, resolution, frame rate, asset ID, and review status. Longer scenes require multiple coverage shots.
4. **Narration:** use one consistent narrator; record/produce narration separately from visual clips if generated speech is unreliable.
5. **Assembly:** arrange coverage to storyboard timings; add narration, music, SFX, transitions, captions, and title/end cards.
6. **Preview export:** private/draft MP4, 1080p; inspect full runtime and audio/video quality.
7. **QA and corrections:** watch the complete video; record scene/timecode defects and correction outcomes in GitHub.
8. **Final export:** recheck exact runtime, Full HD, 16:9, sound, captions, continuity, and story accuracy.
9. **Publishing:** only after explicit user approval; confirm Made for Kids setting, title/description/tags/thumbnail, visibility and schedule. Verify upload readback.

## 5. API and automation

Until VideoExpress provides official API documentation and support confirms the endpoint/authentication/job/export capabilities, use the browser editor with user-guided steps. Never reverse-engineer undocumented endpoints, use session cookies as credentials, or commit API keys. No paid generation should be triggered without the user's clear approval of the action/credits.

## 6. Current handoff

- **Rabbit:** generate the 10-second Wolf-knocking shot next; continue in strict sequence with rabbit reaction, wolf imitation, and refusal. The prompts have been shared, but those clips are not yet received.
- **Magpie:** begin character references and establishing-tree shot once the character design/canon is reconciled.
- **Repository:** record every generated/reviewed asset in the manifest and production log; run validation after edits.
- **Validation:** the manifest validator now checks character reference asset IDs against the asset registry. CI push-run status is not readable through the connected GitHub workflow-run action, so do not assume it passed.
