# Video assembly milestone — 2026-11-28

## Repository state checked

- Development foundation remains on feat/video-pipeline-foundation and is diverged from main (95 commits ahead, 2 behind at audit time). No merge or main-branch update was made.
- Render-inspection work remains on feat/render-qa-inspector, nine commits ahead of the foundation branch, with draft PR #2 open.
- Rabbit production remains at four partial clips plus the approved Wolf reference; no knock/reaction/imitation/refusal clips are registered.
- Mother Magpie remains at script/storyboard draft with no generated assets registered.

## Increment delivered

Added a provider-neutral local FFmpeg draft assembly utility. It reads a JSON assembly plan, resolves source paths relative to that plan, probes clip durations, trims and normalises clips to the project's resolution/frame rate, concatenates them in order, and mixes explicit narration/music tracks. A short or silent preview requires an explicit CLI flag. Existing outputs are never overwritten.

Files:
- scripts/assemble_render.py
- schemas/assembly-plan.schema.json
- tests/test_assemble_render.py
- docs/video-assembly.md
- examples/assembly-plan.example.json
- README.md
- .github/workflows/validate-manifests.yml

## Verification

- Eight local unit/integration tests passed.
- A real FFmpeg smoke test generated two test clips and separate voice/music WAV tracks, assembled them into a 4-second 1920×1080 MP4, and verified the resulting video dimensions, audio stream, and duration with ffprobe.
- No production media was generated or changed; no VideoExpress or Runway credits were spent.
- GitHub Actions must be read back for the pushed branch/PR before claiming CI success.

## Limitations / next work

- This is a local linear assembly utility, not a nonlinear editor. Transitions, captions, per-scene audio edits and visual effects remain in VideoExpress or another editor.
- VideoExpress official API access is still unverified; use the signed-in editor for generation.
- The next production action remains the 10-second Rabbit Wolf-knocking shot. Once approved clip exports and narration/music files are available locally, create a real assembly plan and build a preview.
- Mother Magpie still needs approved master character/location references before generating Scene 1.
- No merge, deployment, upload or publishing was performed.
