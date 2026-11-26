# Expanded story production packs

**Status: alternate expanded retellings — not yet adopted as the repository's canonical scripts.**

These two VideoExpress packs preserve the 14-scene expanded workflow saved in the Library as `videoexpress_story_workflow.md`. They add scene-level still-reference prompts, motion prompts, narration, optional dialogue, voice direction, and sound cues to make each scene independently producible.

## Important canon boundary

The canonical, source-checked project drafts remain:

- `projects/the-clever-little-rabbits/` — 10 scenes, Mother Rabbit and three white rabbits, blue-violet wolf in a brown hat and green outfit.
- `projects/mother-magpie/` — 9 scenes, two neighboring nests, blue eagle, four chicks in the final family.

The expanded packs below use different character names/designs (Mama Hazel/Pip/Clover/Nutmeg/Grizzle; Mama Nell/Mama Tilly/Dot/Dash/Pebble/Button). They are kept separately so they cannot silently overwrite the source-checked drafts. Use them as production-ready alternate treatments only after the user confirms which canon to use. The original scanned PDF was not re-opened for this update; these packs are based on the saved expanded workflow document, not a new source-PDF verification.

## Packs

- [The Three Little Rabbits and the Wolf's Tail](the-three-little-rabbits-and-the-wolfs-tail.md)
- [Mama Nell's Big Heart](mama-nells-big-heart.md)

## Runtime and format

Each pack targets exactly 300 seconds:

- Title card: 5 seconds
- 14 scenes: 290 seconds (scenes 1–10 are 21 seconds each; scenes 11–14 are 20 seconds each)
- End card: 5 seconds

Export target: MP4, 1920×1080, landscape 16:9. Use a consistent narrator, add character dialogue as separate voice clips where practical, keep music below speech, generate captions, and watch the complete export before approval.

## VideoExpress use

1. Create and approve isolated master character references and one location/group reference before scene generation.
2. For each scene, generate the still keyframe from its **Reference image prompt**.
3. Paste the shared style block + relevant character lock + scene **Video prompt** into VideoExpress 3.5. Select the approved references and consistent-character controls where available.
4. Generate short coverage clips (typically 5–10 seconds); do not stretch a short clip to fill a 20–21 second scene. Assemble multiple shots to the target duration.
5. Generate narration and dialogue separately from visuals, using the voice direction in each pack.
6. Add music/SFX, captions, title/end cards, and perform full-film QA.

**Credit and approval gate:** check available credits and clip limits before generation. Do not trigger paid generation, upgrades, or publishing without explicit approval.

## Reference-image status

The prompts in each pack are scene-specific instructions for generating still references. They are not themselves image files, and no scene reference is marked approved until the image is generated, reviewed, and registered in the relevant project manifest. Existing storyboard contact sheets are concept-only and must not be treated as approved character masters.

## Validation

Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_project.py projects/the-clever-little-rabbits/project.json
python scripts/validate_project.py projects/mother-magpie/project.json
```
