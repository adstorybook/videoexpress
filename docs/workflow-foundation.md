# VideoExpress workflow foundation

This repository now contains the workflow documentation, project/schema templates, two story project manifests, a manifest validator, unit tests, and GitHub Actions validation. It is still a foundation—not a working web app or automatic VideoExpress renderer. This document describes the provider-neutral MVP and remaining implementation work.

## Goal

Turn a brief or script into a reviewed, rendered video with traceable assets and reproducible project settings.

## MVP pipeline

1. **Brief** — capture topic, audience, tone, duration, aspect ratio, language, platform, and any brand constraints.
2. **Script** — draft narration and scene beats; allow human approval/editing before generation.
3. **Storyboard** — convert approved script into scenes with visual prompts, narration, duration, and transition notes.
4. **Assets** — generate or source images/video, voiceover, and music; record provider, model, prompt, license/source, and asset location for each.
5. **Assembly** — compose scene assets, narration, captions, music, and transitions into a timeline.
6. **Render** — produce a preview and final export (MVP target: MP4/H.264, 1080p, with configurable aspect ratio).
7. **Review** — provide preview, validation checks (duration, missing media, audio clipping, caption alignment), and an approval gate.
8. **Export** — save final video plus project manifest and captions.

## Implemented foundation\n\nThe current Python validator checks JSON Schema compliance, scene order and runtime totals, unique scene/character/asset IDs, character IDs used by scenes, and asset IDs referenced by scenes or character reference sheets. Unit tests cover the two seed projects and invalid-reference cases. GitHub Actions runs these checks on feature/main pushes and pull requests.\n\n## Suggested interfaces

Keep provider implementations behind adapters so a provider can be changed without redesigning the workflow:

- `TextProvider.generateScript(brief)` and `TextProvider.createStoryboard(script)`
- `VideoProvider.generateClip(scene, options)`
- `ImageProvider.generateImage(prompt, options)`
- `VoiceProvider.synthesize(text, voice, options)`
- `MusicProvider.generateOrSelect(options)`
- `Renderer.assemble(project, options)`

Provider calls should return structured results containing status, asset URL/path, provider/model metadata, and errors. Long-running generation should use job IDs, poll or callback for completion, and retry transient failures with bounded exponential backoff.

## Data model (initial)

- **Project**: id, brief, status, settings, timestamps
- **Scene**: id, order, narration, visual prompt, duration, asset references
- **Asset**: id, type, provider/model, source/license metadata, storage reference, checksum
- **Job**: id, stage, status, attempts, timestamps, error summary
- **Render**: output reference, settings, duration, validation report

Store secrets only in environment variables or a secrets manager; never in source, client bundles, logs, or manifests. Validate provider inputs and file types, limit upload size, and keep generated assets in private storage until approved.

## Runway integration

Use Runway as one optional video/image generation adapter, not as a hard dependency for the whole pipeline. Confirm the currently available API capabilities, model names, request schema, and usage costs before implementing. Credentials should be server-side only (e.g. `RUNWAY_API_KEY`). Keep a mock adapter for local tests, but the production path must call the real provider.

## Recommended implementation sequence

1. Choose the application stack and deployment/storage target; add project scaffold and CI.
2. Implement typed project/scene/job schemas and a basic workflow API.
3. Add script/storyboard generation adapter with provider configuration.
4. Add real Runway adapter with job lifecycle, polling, error handling, and tests.
5. Add voice, captions, and media assembly using a renderer such as FFmpeg.
6. Build a minimal UI for project creation, scene review, progress, preview, and export.
7. Add integration tests, observability, rate limits, and cost controls.

## Acceptance criteria

- A user can create a project from a brief and approve a script/storyboard.
- Each scene has an asset and generation metadata, or a clearly surfaced failure requiring action.
- Jobs can resume after transient errors without losing completed assets.
- A render has a preview, captions, and a validation report.
- The final MP4 and project manifest are exportable.
- No credentials are exposed and no external generation/rendering is triggered without user intent.
