# Production guide and handoff — TheStorybook_ad

## Project status (2026-11-22)
- Two source-based scripts and manifests are prepared, each targeting exactly 300 seconds (5 minutes).
- Storyboards: 10 Rabbit scenes and 9 Magpie scenes.
- Prompt packs and production-brain tracking are maintained on `feat/video-pipeline-foundation`.
- Rabbit family reference is being reused from the generated clips; the Wolf character reference was generated in VideoExpress and visually approved by the user. The original Wolf reference image remains in VideoExpress (not separately uploaded as a file to Git).
- Four Rabbit video clips have been generated/reviewed: opening family reference, Scene 2 hug, Scene 2 departure, and Scene 3 wolf arrival. All are partial coverage; no scene is complete.
- No final video has been assembled or rendered. No VideoExpress API credential is recorded. Do not store API keys in Git.
- Development branch is ahead of `main` and has no divergence behind it at the latest check. Do not merge, publish, deploy, or change `main` without explicit approval.

## Final render target
- 1920×1080, 16:9, 24 fps (verified clip rate; project default) unless VideoExpress exposes another agreed setting.
- Separate exports: `the-clever-little-rabbits.mp4` and `mother-magpie.mp4`.
- Total duration exactly 05:00 each; trim/pad to narration end in editor if needed.
- Audio: warm clear narrator; subtle sound design; low music under speech; normalize dialogue consistently and check peaks.
- Captions: English subtitles with accurate timing; no generated burned-in text in scene visuals.
- Start story immediately; closing card 3–5 seconds maximum and included within scene timing.

## Asset progress (2026-11-22)
- Asset IDs, prompts, checksums (for video files when available), and review notes are in each project's `project.json`. Large media remain outside Git.
- **Scene 1 — opening family reference:** `rabbit-opening-clip-001`, 6.04s, 1920×1080, 16:9, 24fps. Approved as visual reference/partial coverage, not final scene.
- **Scene 2 — hug:** `rabbit-scene2-hug-001`, 6.04s, 1920×1080, 16:9, 24fps. Partial coverage. The safety instruction is not confirmed visually; retain it in narration and create an appropriate shot if needed.
- **Scene 2 — departure:** `rabbit-scene2-departure-001`, 6.04s, 1920×1080, 16:9, 24fps. Mother walks away; children wave. Corrected scene association in manifest.
- **Scene 3 — wolf arrival:** `rabbit-scene3-wolf-arrival-001`, 10.04s, 1920×1080, 16:9, 24fps. Approved partial coverage. Wolf design matches approved reference. Cottage visual differs somewhat from earlier family shots; reuse a cottage reference frame in upcoming generations if available.
- **Wolf character reference:** `wolf-character-reference-001`, approved and visible in VideoExpress's consistent-character reference slot. The original image is not separately in the repository; only screenshot evidence was provided.
- **Pending next shots:** wolf knocking; rabbits hear knocks; wolf imitates Mother; rabbits reject the voice. No new clips for these shots have been uploaded/reviewed yet.

## Efficient generation plan
1. Use approved character references consistently. For location continuity, add a cottage frame as a second reference if the app allows it.
2. Generate 5–10 second coverage clips for each beat. Do not attempt one full five-minute generation.
3. Track each uploaded clip with an asset ID, actual duration/resolution/frame rate, checksum when the file is available, review notes, and its scene association.
4. Assemble clips to storyboard durations, add narration, music/SFX, captions and transitions.
5. Export a private/draft MP4; review the full video, audio, character continuity, story accuracy, safety, and exact runtime.
6. Only after explicit user approval may upload/publishing visibility or schedule be set.

## Quality-control checklist
- [ ] Story content matches source; Mother A does not return in Mother Magpie.
- [ ] Rabbit story has mother and exactly 3 siblings; wolf blue-violet, brown floppy hat, green clothes; tail gag non-graphic.
- [ ] Magpie story: two nests at fixed locations, two chicks each initially; exactly four after adoption; eagle blue with orange beak; no graphic capture.
- [ ] Characters/outfit colors stay stable; no extra/missing characters, distorted faces, flicker or artifacts.
- [ ] Narration intelligible and not clipped; no gibberish; music under speech.
- [ ] Full HD, 16:9, no unwanted text/watermarks.
- [ ] Full runtime and ending correct; transitions clean.
- [ ] Full video watched, not just samples.
- [ ] User approval recorded before public upload or scheduling.

## VideoExpress connection
Use the signed-in VideoExpress app when direct API/automation is unavailable. If it asks for a credential, use only the platform's secure credential/settings field. Do not put secrets in Git, project files, prompts, or chat. Verify official docs/support before relying on an undocumented API.

## Channel packaging (draft)
Channel: TheStorybook_ad
- Rabbit title: The Clever Little Rabbits 🐰 | 5-Minute Animated Bedtime Story | Safety & Teamwork
- Magpie title: Mother Magpie 🐦 | 5-Minute Animated Story About Kindness & Family
- Suggested description: Two gentle animated storybooks for young children, with lessons about staying safe, teamwork, kindness, and welcoming others. Family-friendly narration and colorful 3D storybook animation.
- Suggested audience: Made for Kids — confirm audience setting before upload. Performance/retention targets are aspirational, not guarantees.
