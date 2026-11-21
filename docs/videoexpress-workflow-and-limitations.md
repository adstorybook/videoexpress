# VideoExpress workflow notes for children's story videos

**Observed:** 2026-11-21, in the current VideoExpress account and browser session. These are practical notes, not permanent product guarantees; confirm limits and options in the UI on the next run.

## Target configuration

- Two separate projects, one story per project.
- YouTube landscape, 16:9; aim for Full HD (1920×1080) only after confirming that option in the export dialog.
- Gentle 3D storybook look. Keep Alex and Maya as recurring storybook hosts in the opening and closing frames; keep the rabbit or magpie cast as each fable's protagonists.
- Use the generated character guides from **My AI Images** and turn off public-gallery sharing.
- Keep narration on an audio track and generate visual story clips separately. This avoids the current long-audio limit in the lipsync tool.

## Tested facts and limits

| Tool or area | What worked / what the UI showed | Caution |
|---|---|---|
| Media Library | Folders include **My AI Audio**, **My AI Images**, **My AI Videos**, and **Videos**. Generated images can be selected from **My AI Images** for Image To Video. | The app says project files are hosted for up to 50 days; download final outputs promptly. |
| Text to Speech | A 553-character sample with Emotion Jenny, Friendly, speed 0.7 generated 42 seconds of audio and saved to **My AI Audio**. The text box limit shown was 600 characters. | The generated duration depends on wording and voice speed. Measure each chunk; for sub-30-second lipsync audio, use a safe margin (roughly 300–350 characters at this voice setting, then verify). |
| Lipsync Video (Old Algorithm) | It accepts a generated image plus speech and offers consistent-character controls. The UI says it works best with a centered waist-up actor and a 16:9 or 9:16 image. | This is a talking-presenter/lip-sync tool, not a story montage tool. A 42-second audio sample was rejected: the current account showed a 30-second maximum and an upgrade prompt for audio up to 300 seconds. Do not upgrade or top up without explicit approval. |
| Image To Video (Old Algorithm) | It accepts a still plus a **Video Action Prompt**, with style choices including **3D**. A rabbit-family still was accepted and a short scene entered the background queue. | Set style to **3D**; the default was Human. The sample 1920×1088 landscape image triggered an aspect-ratio warning, so create/choose exact 1920×1080 or 1080×1920 source frames where possible. The queued sample still needs review. |
| Generated media | The UI said completed clips appear under **Media Library → My Media**. | A queued job is not a finished project. Confirm it appears and preview the actual clip before using it. |
| Export Video / My Videos | The editor has **Export Video** and **My Videos**. One unrelated travel render preview was 32 seconds. | Do not treat that travel clip as either story. The HD export setting and complete story export are not yet verified. |

## Good workflow for a segmented story

1. Start or open a clearly named project for one story; do not leave it titled with an unrelated example-project name.
2. Set landscape 16:9 and save. Turn off public-gallery sharing.
3. Create/check a landscape character guide and key story frames first. Review character counts, clothing, and continuity before animating; the generated rabbit images looked warm and polished but did not always match every clothing detail in the written prompt.
4. Generate visual clips with **Image To Video (Old Algorithm)**, choosing **3D** and using one focused action per clip. Keep each visual beat short and relevant to the narration. Check queue completion in **My Media**, then preview it.
5. Create or import narration separately. Split TTS text at sentence boundaries under 600 characters; verify the resulting duration and avoid clips longer than 30 seconds if sending them through Lipsync.
6. Assemble the visual clips in order on the video track and narration pieces in order on the audio track. Check total runtime, transitions, sound levels, captions, opening hook, and closing lesson. Save the project.
7. Export once the full timeline has been previewed. Verify actual duration, 16:9 aspect, Full HD resolution, audio, and visual coverage before calling it upload-ready.

This segmented assembly path has not yet been completed end to end. The first rabbit Image To Video sample is the current test; the Magpie project and final exports remain pending.

## Managing scenes

The user confirmed that scenes can be added and deleted in the editor. Treat each generated visual clip as an editable beat: add scenes to cover a missing story moment, remove a scene that changes character counts or continuity, and replace it with a focused prompt. Keep every added scene tied to the approved narration and retention outline. The narration drafts already target five minutes, so use scene additions to improve visual coverage and pacing rather than adding filler words. Before bulk editing, verify how the current editor places a new clip on the timeline and how deletion affects neighboring clips.

## Reusable image-to-video action prompt

> Animate this exact 3D storybook frame as a gentle, child-friendly scene. Show one clear action tied to this narration beat. Preserve the same character faces, fur or feather colors, outfits, relative sizes, and number of characters. Use smooth natural motion, soft cinematic lighting, and a gentle camera move. Keep suspense mild and reassuring. No harm, no visible speaking or lip-sync, no on-screen words, captions, or logos. Do not add characters or change the setting.

Add a specific action and setting for each shot; do not reuse the generic prompt unchanged for every segment. The story-specific character anchors and storyboard beats are in each `project-and-youtube-plan.md`.

## Positive points observed

- The media library already contains the Alex/Maya references and several 3D rabbit and magpie guide images, so the story work can reuse those assets.
- Image To Video separates scene animation from narration and accepted the landscape rabbit still without requesting the long-audio upgrade.
- The editor has a multitrack timeline, save control, captions tool, and a visible video export path.

## Negative points and unresolved checks

- Lipsync is easy to confuse with cinematic scene generation; its guidance favors a waist-up talking actor, and the current account blocks speech over 30 seconds.
- Approximate 16:9 dimensions can still trigger the app's ratio warning; prepare exact aspect ratios.
- Generation is asynchronous; a toast only means a job was queued, not that a usable clip was made.
- The full-length edit, HD export, transition workflow, and sub-30-second segmented final assembly still need a successful end-to-end test.
- A YouTube channel is not connected to the publishing workspace. Connect it and choose privacy only when the reviewed final MP4 exists.

## UI tools not yet tested for these stories

The editor also displayed **Create Video From Prompt** (Image to Video, Lipsync HD, Narrate, Consistent Character), **Text To Video**, **First Frame / Last Frame**, **Smart Edit** (inpainting, object removal, background removal), **Stylize Character**, **Outpainting**, **AI Sound Maker**, **Text Animations**, **Filters**, **Fast Cut**, **Audio Cutter**, and **Automatic Captions** (opens an external captions site). Their controls, prices/quotas, strengths, and limitations have not been verified here. Check before relying on them; do not assume they bypass the 30-second lipsync limit or provide a free HD export.

