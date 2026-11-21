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
| Image To Video (Old Algorithm) | It accepts a still plus a **Video Action Prompt**, with style choices including **3D**. With the Video Length Booster off, the first rabbit scene completed as a 4-second, 1920×1080 MP4. | Set style to **3D**; the default was Human. The sample 1920×1088 landscape image triggered an aspect-ratio warning, so create/choose exact 1920×1080 or 1080×1920 source frames where possible. A second prompt with the Video Length Booster on is still rendering; do not assume the booster produces a particular duration until the clip is previewed. |
| Timeline assembly | Dragging the completed first rabbit MP4 from **My AI Videos** onto video track 1 worked; the editor showed one clip and a 4-second project duration. | This verifies a single-clip placement only. A full multi-scene story, narration alignment, and export have not been completed. |
| My AI Videos | The gallery shows render progress on the pending boosted scene. The completed test clip is listed as 1920×1080. | Gallery timestamps and thumbnail progress are not clip durations. Open **Play** or preview each completed file to verify its actual length and content. |
| Video Length Booster | A second rabbit scene with the booster checked completed at 8 seconds and 1920×1080. Its preview showed Mother Rabbit and exactly three kits in a warm cottage scene. | The booster-off test was 4 seconds, so the booster doubled this sample to 8 seconds. Even boosted clips are too short to cover a five-minute story on their own. |
| Still-image scene | **Add to Timeline** on a story still placed it as a separate clip on video track 1 at the current playhead. In this test it occupied roughly 20 seconds, longer than the animated sample clips. | The default still duration and a reliable way to change it have not been measured precisely. Preview the timeline before relying on a specific hold length. |
| Text to Speech | **Import Media → Text to Speech** offers English, **Jenny**, an emotion choice such as **Friendly**, and a speed slider accepting 0.7. One 254-character segment at Jenny/Friendly/0.7 rendered as 22 seconds and saved to **My AI Audio**. | Use one narrator and one speed throughout a story. Keep narration segments around 300 characters or less, then verify every actual audio duration stays under 30 seconds. Do not send long narration through Lipsync. |
| Audio placement | Dragging an audio card directly from **My AI Audio** onto track 2 at the chosen position worked. | The audio card's **Add to Timeline** menu placed it on the active video track and appended it after the video clips in this test. Drag it directly to track 2 instead. |
| Generated media | The UI said completed clips appear under **Media Library → My Media**. | A queued job is not a finished project. Confirm it appears and preview the actual clip before using it. |
| Export Video / My Videos | The editor has **Export Video** and **My Videos**. One unrelated travel render preview was 32 seconds. | Do not treat that travel clip as either story. The HD export setting and complete story export are not yet verified. |

## Good workflow for a segmented story

1. Start or open a clearly named project for one story; do not leave it titled with an unrelated example-project name.
2. Set landscape 16:9 and save. Turn off public-gallery sharing.
3. Create/check a landscape character guide and key story frames first. Review character counts, clothing, and continuity before animating; the generated rabbit images looked warm and polished but did not always match every clothing detail in the written prompt.
4. Generate visual clips with **Image To Video (Old Algorithm)**, choosing **3D** and using one focused action per clip. The first booster-off sample was only 4 seconds, so test the booster and preview a sample before planning the number of clips. Check queue completion in **My Media**, then preview each result.
5. Generate narration separately with **Import Media → Text to Speech**. Jenny, Friendly, speed 0.7 produced a 22-second sample at 254 characters; split at sentence boundaries around 300 characters and verify each output is under 30 seconds. Keep voice and pace consistent.
6. Assemble the visual clips in order on video track 1 and drag each narration piece directly to audio track 2 at its intended point. Check alignment, total runtime, transitions, sound levels, captions, opening hook, and closing lesson. Save the project.
7. Export once the full timeline has been previewed. Verify actual duration, 16:9 aspect, Full HD resolution, audio, and visual coverage before calling it upload-ready.

This segmented assembly path has not yet been completed end to end. The rabbit draft now contains a 4-second animation, an 8-second boosted animation, a still-frame clip, and one narration sample on separate tracks. The narration test confirms that 254 characters can fit into a 22-second Jenny/Friendly clip at 0.7 speed. The full 13-part voiceover, Magpie project, and final exports remain pending.

## Managing scenes

The user confirmed that scenes can be added and deleted in the editor. Treat each generated visual clip as an editable beat: add scenes to cover a missing story moment, remove a scene that changes character counts or continuity, and replace it with a focused prompt. Keep every added scene tied to the approved narration and retention outline. The narration drafts already target five minutes, so use scene additions to improve visual coverage and pacing rather than adding filler words. Generated video and stills can be added via **Add to Timeline**; an 8-second clip and a longer still clip were placed sequentially. A narration file must be dragged directly to track 2. Clip trimming, deletion, and transitions still need verification before final assembly.

## Reusable image-to-video action prompt

> Animate this exact 3D storybook frame as a gentle, child-friendly scene. Show one clear action tied to this narration beat. Preserve the same character faces, fur or feather colors, outfits, relative sizes, and number of characters. Use smooth natural motion, soft cinematic lighting, and a gentle camera move. Keep suspense mild and reassuring. No harm, no visible speaking or lip-sync, no on-screen words, captions, or logos. Do not add characters or change the setting.

Add a specific action and setting for each shot; do not reuse the generic prompt unchanged for every segment. The story-specific character anchors and storyboard beats are in each `project-and-youtube-plan.md`.

## Positive points observed

- The media library already contains the Alex/Maya references and several 3D rabbit and magpie guide images, so the story work can reuse those assets.
- Image To Video separates scene animation from narration and accepted the landscape rabbit still without requesting the long-audio upgrade; completed samples were 4 seconds booster-off and 8 seconds booster-on at 1920×1080.
- Still images and separate sub-30-second narration can be added to the same multitrack story project.
- The editor has a multitrack timeline, save control, captions tool, and a visible video export path.

## Negative points and unresolved checks

- Lipsync is easy to confuse with cinematic scene generation; its guidance favors a waist-up talking actor, and the current account blocks speech over 30 seconds.
- Approximate 16:9 dimensions can still trigger the app's ratio warning; prepare exact aspect ratios.
- Generation is asynchronous; a toast only means a job was queued, not that a usable clip was made. The gallery may show percentage progress while rendering.
- The full-length edit, HD export, transition workflow, and sub-30-second segmented final assembly still need a successful end-to-end test. Jenny/Friendly at speed 0.7 was measured at 22 seconds for 254 characters; verify every segment individually.
- A YouTube channel is not connected to the publishing workspace. Connect it and choose privacy only when the reviewed final MP4 exists.

## UI tools not yet tested for these stories

The editor also displayed **Create Video From Prompt** (Image to Video, Lipsync HD, Narrate, Consistent Character), **Text To Video**, **First Frame / Last Frame**, **Smart Edit** (inpainting, object removal, background removal), **Stylize Character**, **Outpainting**, **AI Sound Maker**, **Text Animations**, **Filters**, **Fast Cut**, **Audio Cutter**, and **Automatic Captions** (opens an external captions site). Their controls, prices/quotas, strengths, and limitations have not been verified here. Check before relying on them; do not assume they bypass the 30-second lipsync limit or provide a free HD export.

