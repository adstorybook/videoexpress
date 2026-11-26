# The Clever Little Rabbits — Visual Generation Prompt Pack

**Production target:** 5:00 / 300 seconds; 16:9; 1920×1080 final; narration-led edit. Generate short visual clips for each beat and assemble them to the scene timings in storyboard.json. Use separate narration/audio in the edit rather than relying on generated dialogue.

## Master style and continuity prompt
Family-friendly cinematic 3D storybook animation, soft fluffy fur, expressive eyes, rounded appealing shapes, rich but natural colors, warm cinematic global illumination, gentle depth of field, polished animated-film quality, 16:9 composition. Preserve character designs across shots. No on-screen text, no captions, no logos, no watermark. Suspense is playful and non-threatening; no graphic injury.

## Character lock
- Mother Rabbit: adult white rabbit, gentle face, blue puff-sleeve dress with cream apron, calm warm eyes, upright ears.
- Rabbit 1: smallest white rabbit, red-orange vest, lively and brave.
- Rabbit 2: white rabbit, yellow scarf/outfit, thoughtful.
- Rabbit 3: white rabbit, green overalls, energetic.
- Wolf: large blue-violet furry wolf, brown floppy hat, green outfit, expressive but comically sly; keep his silhouette, hat, clothing, and fur color identical.
- Cottage: cozy small timber cottage, rounded wooden door, meadow flowers; consistent interior and exterior geography.

## Scene prompts (visual clips; narration is in script.md)
1. **Cozy rabbit home (30s):** Establishing wide of flower meadow and cottage, push in through window to mother and three white rabbit siblings sharing carrots, playing gently; show each outfit clearly, sunlight and birds.
2. **Mother goes out (30s):** Build as five short shots using the saved opening image as the character reference: (A) 6s medium shot, Mother Rabbit crouches at the children's eye level and gently reminds them to stay inside and never open the door to a stranger; (B) 6s close shot, all three children listen seriously, their outfit colors and faces unchanged; (C) 6s warm group hug, mother embraces each child; (D) 6s medium-wide from cottage doorway, mother steps outside and walks down the flower path, door closes; (E) 6s inside looking toward the window, three children wave as mother walks away, then turn back indoors. Keep cottage layout, morning light, character sizes and outfits consistent. No new characters, no text, no cut to unrelated locations. Generate each short clip separately, using the saved rabbit-family reference image and consistent-character option where available.
3. **Wolf arrives (30s):** Wide meadow shot; blue-violet wolf in brown floppy hat and green outfit walks in, stomach rumble, notices cottage, mischievous smile; approaches and knocks, exterior angle.
4. **Imitation (35s):** Inside cottage: rabbits exchange cautious looks as muffled knock/voice comes from outside; close-up on ears listening, they whisper and hold the door closed; exterior wolf attempts an exaggerated sweet expression.
5. **Tail test (35s):** Low view of door and narrow gap; rabbits call for proof; wolf confidently pushes his fluffy tail toward gap; suspenseful but humorous, tail visible only through gap.
6. **Door trap (35s):** Rabbits count together, brace, push wooden door closed; quick cartoon impact, wolf startled outside, tail caught; no injury detail; use clear cause-and-effect and comic reaction.
7. **Mother returns (30s):** Mother arrives, sees wolf at door and children safe inside; she takes a small wooden stick and gives a non-graphic cartoon bonk to wolf's head; exaggerated stars/soft comedic reaction, no violence detail.
8. **Wolf escapes (30s):** Wolf pulls away, small cartoon tail-tip left at door, he runs across meadow howling; keep tail gag mild and non-graphic; mother opens door cautiously, gathers children in a hug.
9. **Safe together (30s):** Warm medium and close-ups: mother praises children for staying together and not opening door; three rabbits hug her; she checks each child, closes door securely; golden afternoon light.
10. **Happy ending (15s):** Family cuddled together by cottage window; gentle camera pull-back to flowers and birds; peaceful final composition for moral narration.

## Continuity / editing
Use consistent cottage door direction, interior layout, outfit colors, and wolf tail. Scene 6 must show rabbits inside and wolf outside. Scene 7 mother is outside. Avoid frightening teeth close-ups. Clip lengths may be 5–10 seconds; use multiple coverage shots per scene and assemble to target timing.

## Shot-level generation queue (audited 2026-11-26)

### Reviewed generated coverage
- Scene 1: `rabbit-opening-clip-001` — 6.04s family opening reference; approved as reference/partial coverage, not a finished scene.
- Scene 2: `rabbit-scene2-hug-001` — 6.04s mother/children hug, partial coverage.
- Scene 2: `rabbit-scene2-departure-001` — 6.04s mother leaves and children wave, partial coverage.
- Scene 3: `rabbit-scene3-wolf-arrival-001` — 10.04s wolf approaches the woodland cottage, partial coverage. The cottage differs somewhat from the earlier family shots; reuse a cottage frame as an additional reference if the UI supports it.
- Wolf character reference: `wolf-character-reference-001` — approved visual reference in VideoExpress; original reference image is not separately stored in this repository.

All four clips are 1920x1080, 16:9, 24fps. No full scene is complete yet.

### Next clip — Wolf knocks (10 seconds)
Use the approved wolf reference. If the optional second reference slot is available, use a still from the established rabbit cottage exterior to anchor the door and location.

Cinematic 3D animated children's story. The same blue-violet furry wolf wearing his brown floppy hat and green clothes stands outside the rabbits' cozy wooden cottage. He raises his paw and knocks on the wooden door three times. He pauses, listens carefully, tilts his head, and gives a mischievous smile. He leans toward the door as if preparing to speak. Colorful flowers, warm daylight, soft shadows, expressive cartoon animation, gentle suspense, family-friendly polished storybook movie quality. Medium shot focused on the wolf and cottage door. Preserve the wolf's exact appearance, clothing, colors, and proportions from the reference image. Maintain the cottage exterior and door continuity. No frightening imagery, no text, no subtitles, no extra characters.

### Generation order — do not skip beats
1. Wolf knocks (pending; prompt shared).
2. Rabbits hear the knock (pending; prompt shared).
3. Wolf imitation (pending; prompt shared).
4. Rabbits refuse (pending; prompt shared). Generate and review each in order to preserve cause-and-effect.

## After the knock — Rabbits hear it (10 seconds)
Use the three-rabbit reference. Inside the cozy cottage, the three white rabbit siblings hear three knocks from the closed front door. They stop what they are doing, turn their ears toward the door, exchange surprised and cautious looks, and move close together. The rabbit in red-orange steps slightly forward; yellow looks worried; green raises a paw to signal quiet. Medium interior shot, warm cottage lighting, gentle suspense, family-friendly animation. Preserve the exact three rabbit designs and red-orange, yellow, green outfits. The door stays closed; no wolf visible; no text or subtitles.

## Wolf imitation — exterior (10 seconds)
Use the approved wolf reference and, if possible, the cottage exterior frame. Outside the closed cottage door, the blue-violet wolf in the brown floppy hat and green clothes tries to imitate a sweet motherly voice. He straightens up, clears his throat, puts on an exaggerated gentle smile, and calls toward the door as if he is Mother Rabbit. His fake sweetness slips into a sly impatient expression as he waits. Medium shot; same door and path; playful suspense, not scary. Keep exact character continuity. No text, no subtitles, no other characters visible.

## Rabbit refusal — interior (10 seconds)
Use the three-rabbit reference. The three little white rabbits hear the wolf's rough, growly voice through the closed door. They exchange knowing looks, shake their heads, whisper that it does not sound like their mother, and hold the door shut together. One rabbit points toward the door while another gently signals the others to stay back. Medium interior shot, warm lighting, gentle suspense, teamwork, family-friendly. Keep exact outfits (red-orange, yellow, green), no door opening, no wolf visible, no text/subtitles.

**Assembly reminder:** Each 10-second clip is coverage, not a full scene. Add narration/audio separately in the edit and use cutaways/reaction shots to reach the storyboard timing without stretching or looping visibly.


### Review gate
A clip is not a completed scene. Keep every newly generated 5–10 second shot in pending review until the user uploads it and its metadata/frames are inspected. Mark a scene complete only after approved coverage is assembled to its target duration and reviewed in sequence with narration. As of the 2026-11-26 audit, no uploaded clips are logged for the knock, rabbit-reaction, wolf-imitation, or rabbit-refusal queue. The next user action remains generating the 10-second Wolf-knocking shot.
