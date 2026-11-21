# Production guide and handoff — TheStorybook_ad

## Project status (2026-11-21)
- Two source-based scripts and manifests are ready, each exactly 300 seconds (5 minutes).
- Storyboards contain 10 Rabbit scenes and 9 Magpie scenes.
- Scene-by-scene visual prompt packs are saved beside each project.
- Character sheets are being generated in the connected Runway workspace; see task viewers in ChatGPT.
- Rabbit clips generated and reviewed in VideoExpress: opening reference (6.04s), Scene 2 hug (6.04s), Scene 3 departure (6.04s), and wolf arrival (10.04s), all 1920×1080, 16:9, 24 fps. These are approved partial coverage only; the 30-second scenes remain in progress.
- No final video has been rendered or assembled. No VideoExpress API credential is available in this project. Do not store API keys in Git.
- Keep work on `feat/video-pipeline-foundation`; do not merge to main or publish without explicit approval.

## Final render target
- 1920×1080, 16:9, 30 fps preferred (or project default if VideoExpress cannot set it).
- Separate exports: `the-clever-little-rabbits.mp4` and `mother-magpie.mp4`.
- Total duration exactly 05:00 each; if VideoExpress exports slightly off, trim/pad in editor to the exact narration end.
- Audio: narrator voice warm and clear; subtle sound design; low music bed under narration; no loud/ominous moments; normalize dialog consistently and check peaks.
- Captions: optional but recommended, English subtitles with accurate timing. No AI-generated burned-in text in scene visuals.
- Opening: story starts immediately, avoid long logo intro; closing title/end card 3–5 seconds max (included within scene timing).

## Asset progress (2026-11-21)
- `projects/the-clever-little-rabbits/project.json` records the opening reference, Scene 2 hug, and Scene 3 departure clip IDs and checksums; video files themselves remain outside Git.
- Keep generated media in a user-controlled storage location and reference it by asset ID, filename, and checksum. Do not add large MP4 files to the repository.
- Scene 1 opening reference clip: 6.04 seconds; visual reference/partial coverage.\n- Scene 2 hug clip: 6.04 seconds, 1920×1080, 24 fps; mother and three children hugging at the cottage doorway. Safety instruction and departure still need coverage; Scene 2 remains in progress.\n- Scene 3 departure clip: 6.04 seconds, 1920×1080, 24 fps; mother walks away along the flower-lined path and the three children wave from the cottage doorway. Reviewed as visually consistent and approved for partial coverage; Scene 3 remains in progress.\n- Scene 3 wolf arrival clip: 10.04 seconds, 1920×1080, 24 fps; approved wolf design approaches a woodland cottage. Partial Scene 3 coverage. Cottage design differs somewhat from earlier rabbit cottage shots; check/set location continuity in upcoming clips.

## Efficient generation plan
1. Make/approve character reference sheets. Treat them as visual reference images, not scene outputs.
2. Generate one opening establishing image per story to lock setting, then scene clips from the prompts in `visual-prompts.md`.
3. For continuity, use the approved character references in every applicable generation. Use image-to-video or multi-reference if the platform supports it.
4. Generate short coverage (roughly 5–10 seconds per clip) and select the best takes. Avoid trying to generate a full 5-minute video in one prompt.
5. Assemble clips to the exact scene durations listed in `storyboard.json`, add narration from `script.md`, then music/SFX, captions, and transitions.
6. Export a private/draft MP4. Review full video, audio, character continuity, story accuracy, and safety. Correct defects and rerender.
7. Only after the user approves the final file may upload/publish settings be chosen. User approval must include visibility and schedule.

## Quality-control checklist
- [ ] Story content matches source; no invented return for Mother A in Mother Magpie.
- [ ] Rabbit story shows mother, exactly 3 siblings; wolf blue-violet, brown floppy hat, green clothes; tail gag is non-graphic.
- [ ] Magpie story: two nests at fixed locations, two chicks each initially; exactly four chicks after adoption; eagle is blue with orange beak; no graphic capture.
- [ ] Characters and outfit colors remain stable; no missing/extra characters, broken limbs, distorted faces, flickering, duplicate chicks.
- [ ] Narration is intelligible, paced, and not clipped; no generated gibberish; music stays under speech.
- [ ] Full HD frame, correct 16:9, no watermarks or unwanted text.
- [ ] Runtime and ending are correct; scene transitions clean.
- [ ] Reviewed entire film from beginning to end, not just sample frames.
- [ ] User approval recorded before public upload or scheduling.

## VideoExpress connection
Use the signed-in VideoExpress app for generation if the API/automation connection is not available. If it offers an API key, use the platform's secure credential/settings field only. Do not put secrets into GitHub, project files, prompts, or chat. If it asks for an API endpoint/key but there is no documented API available to this project, stop and verify the official docs/support rather than inventing credentials or endpoints.

## Channel packaging (draft)
Channel: TheStorybook_ad
Suggested title Rabbit: The Clever Little Rabbits 🐰 | 5-Minute Animated Bedtime Story | Safety & Teamwork
Suggested title Magpie: Mother Magpie 🐦 | 5-Minute Animated Story About Kindness & Family
Suggested description: Two gentle animated storybooks for young children, with lessons about staying safe, teamwork, kindness, and welcoming others. Family-friendly narration and colorful 3D storybook animation.
Suggested audience: Made for Kids — confirm YouTube audience setting before upload. Avoid claims about retention or performance guarantees.
