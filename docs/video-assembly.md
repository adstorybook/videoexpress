# Local video assembly (draft MP4)

The assemble_render.py utility combines an ordered list of generated clips and optional narration/music tracks into a local MP4 using FFmpeg. It is provider-neutral: VideoExpress exports, Runway exports, or other supported local video files can be used as inputs.

## Requirements

- Python 3.12+
- FFmpeg (ffmpeg and ffprobe) on PATH
- Repository dependencies installed with python -m pip install -r requirements.txt
- A valid project manifest and an assembly plan (see examples/assembly-plan.example.json)

No provider API, browser session, credential, network request, generation credit, upload, or publishing action is used.

## Plan format

Paths in the plan are resolved relative to the plan file. A relative --output override is resolved from the current working directory. The project manifest supplies target runtime, resolution, aspect ratio, and frame rate. Clips are concatenated in the order listed. Each clip can optionally specify start_seconds and duration_seconds to trim coverage. Audio tracks are mixed in the order listed; gain is linear (0–2), start_seconds offsets the track, and loop=true repeats a music bed to cover the assembled video.

Example:

    {
      "project_manifest": "../projects/the-clever-little-rabbits/project.json",
      "output": "../renders/rabbits-preview.mp4",
      "clips": [
        {"path": "../media/scene-01.mp4"},
        {"path": "../media/scene-02.mp4", "start_seconds": 0.5, "duration_seconds": 18}
      ],
      "audio_tracks": [
        {"path": "../audio/narration.wav", "gain": 1.0},
        {"path": "../audio/music.wav", "gain": 0.12, "loop": true}
      ]
    }

## Validate and assemble

    python scripts/validate_project.py projects/the-clever-little-rabbits/project.json
    python scripts/assemble_render.py /path/to/rabbits-assembly-plan.json --dry-run
    python scripts/assemble_render.py /path/to/rabbits-assembly-plan.json
    python scripts/inspect_render.py projects/the-clever-little-rabbits/project.json /path/to/rabbits-preview.mp4 --output /path/to/rabbits-qa.json

The checked-in example contains placeholder media paths; copy it and replace them with real exported clip/audio files before running it. A complete assembly must match the project's target runtime within ±1 second by default. For a shorter rough cut, explicitly use --allow-partial-preview. For a silent visual-only rough cut, explicitly use --allow-silent-preview. These flags are for previews, not final delivery. The output must be a new .mp4 path; existing files and source media are never overwritten. The -n flag is also passed to FFmpeg as a second overwrite safeguard.

## Technical behaviour and limitations

- Video is scaled to fit the manifest resolution, letterboxed with black padding if needed, converted to the manifest frame rate, and normalised to square pixels/yuv420p before concatenation.
- Source clip audio is not carried through. Add narration and music as explicit audio_tracks so the mix is intentional.
- Audio tracks are volume-adjusted, optionally delayed/looped, padded, trimmed to the assembled duration, and mixed. Keep music gain low enough for narration to remain intelligible.
- This is a linear assembly utility, not a nonlinear editor: no transitions, per-scene crossfades, captions, or visual effects are added. Add those in VideoExpress or a dedicated editor before final export.
- The tool only creates a local draft MP4. Run scripts/inspect_render.py afterwards, then watch the entire movie and record human QA/approval separately. Automated metadata checks never approve a film.
- Generated media should remain outside Git; store only manifests, prompts, metadata, and checksums in the repository.

No final render, approval, or publishing is implied by a successful assembly command.
