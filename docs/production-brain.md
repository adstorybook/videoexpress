# VideoExpress production brain

GitHub is the durable, versioned source of truth for production knowledge. It does not generate/render videos by itself: VideoExpress (or a future approved provider adapter) performs media generation, and this repository records instructions, outcomes, and reusable corrections.

## Principles
- **Project memory is explicit and versioned:** never rely on chat history alone.
- **Apply approved corrections:** only corrections explicitly approved by the user become global/channel defaults. Project-only corrections remain scoped.
- **Character continuity:** store character bible entries and reference images/asset IDs; scene prompts reference stable character IDs and canonical descriptions.
- **Reproducibility:** save prompt text, provider/model/version, settings, seed where available, source/license, timestamps, and output asset IDs.
- **Human approval gates:** approve script/storyboard before generation when requested; review complete final export before publishing. Publishing and visibility/scheduling always require explicit approval.
- **No secrets:** API keys, OAuth tokens, passwords, and private credentials must never be committed. Use server-side secret storage/environment variables.
- **Fail safely:** mark failed or unverified stages; do not silently skip them or claim success.

## Repository layout (target)
```
projects/
  <project-slug>/
    project.json             # brief, settings, workflow status, approved script/storyboard refs
    script.md
    storyboard.json
    characters.json
    assets/                  # manifests/refs; large media stored separately
    corrections.json         # project-scoped feedback
    qa-report.json
    exports/                 # metadata/links only; avoid large binaries in Git
schemas/
  project.schema.json
  correction.schema.json
  qa-report.schema.json
defaults/
  channel-profile.json       # reusable channel defaults; approval metadata
  correction-rules.json      # only user-approved reusable rules
docs/
  ...
```

Large generated media should live in VideoExpress or a storage provider, not Git history. Store safe URLs/IDs, hashes, and rights metadata in asset manifests. A Git LFS/storage strategy can be decided later.

## Production memory loop
1. Load channel profile + reusable approved rules.
2. Load project manifest, story/script, characters, storyboard, and project corrections.
3. Apply rules when generating scripts, prompts, narration, editing and QA.
4. Record each new correction with scope (project/channel), status (proposed/approved/rejected), what changed, and evidence (scene/timecode).
5. Only promote a correction to reusable channel defaults after user approval; retain its provenance.
6. At final review, store QA report, render version, approval and export reference.
7. After publishing approval and verified upload, record video URL/ID and analytics checkpoints/insights; use those insights as proposals, not automatic global rules.

## Workflow status
`idea → script_draft → script_approved → storyboard_draft → storyboard_approved → assets_generating → assets_ready → assembly → render_preview → review → approved → export_ready → upload_pending_approval → published → analytics`

Status changes must include timestamp, actor/source, and notes. A failed stage can move to `blocked` with error and retry notes.

## Video quality profile (initial channel default, pending approval)
- Style: Pixar-inspired 3D animated family/storybook film (descriptive style, not a claim of affiliation).
- Default canvas: 1920×1080, 16:9, Full HD; confirm provider/export actually supports it.
- Target runtime: per-project brief; short story projects default to 300 seconds only when specified.
- Voice: clear, expressive, consistent across scenes; pronunciation guide retained.
- Captions: timed, readable, safe-area placement, verified.
- Retention: ambitious 80%+ retention target, not a guarantee. Evaluate actual analytics by video length and audience/source.
- Final review: watch the entire exported file; check story, continuity, visuals, sound, captions, encoding and rights.

## Adapter/API boundaries
Use provider-neutral interfaces (script/storyboard, image/video, voice, music, renderer, storage, publishing, analytics). Each call must return a job ID/status and persisted result metadata. Keep provider keys server-side. VideoExpress API availability is not verified; do not pretend an API exists. If no supported API is available, use user-guided/manual operation or another provider with a documented integration, and keep the project records provider-neutral.

## Next implementation steps
1. Add schemas and sample/template project records (this commit).
2. Implement validator and tests for project/correction/QA JSON.
3. Add a CLI or API for initializing projects, validating manifests, and applying approved rules.
4. Build UI for script/storyboard approval, scene tracking, correction capture, QA and export.
5. Connect a verified provider adapter only after docs/credentials and capability checks.
6. Add YouTube/vidIQ analytics/publishing adapter, with approval gate and readback verification.
