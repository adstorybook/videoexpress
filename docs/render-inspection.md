# Export inspection and QA report

\`scripts/inspect_render.py\` uses the locally installed \`ffprobe\` binary to inspect a finished MP4 against the project's \`project.json\` targets. It records the measured container, video codec, duration, dimensions, aspect ratio, frame rate, audio-stream presence, and SHA-256 checksum in the repository's \`qa-report.schema.json\` format.

## Requirements

- Python 3.12+
- FFmpeg's \`ffprobe\` executable available on \`PATH\`
- A project manifest that passes \`scripts/validate_project.py\`

No provider API, credentials, network request, or generation credit is used.

## Usage

From the repository root:

~~~bash
python scripts/validate_project.py projects/the-clever-little-rabbits/project.json
python scripts/inspect_render.py \
  projects/the-clever-little-rabbits/project.json \
  /path/to/the-clever-little-rabbits-final.mp4 \
  --output /path/to/rabbits-render-qa.json
~~~

For Mother Magpie:

~~~bash
python scripts/inspect_render.py \
  projects/mother-magpie/project.json \
  /path/to/mother-magpie-final.mp4 \
  --output /path/to/magpie-render-qa.json
~~~

The report is printed to stdout if \`--output\` is omitted. The default runtime tolerance is ±1 second. Use \`--duration-tolerance 2\` only when the edit has a deliberate timing allowance. Audio is required unless \`--allow-missing-audio\` is explicitly supplied.

## Interpretation and safety

- \`overall_status: fail\` means at least one automated technical check failed.
- \`overall_status: incomplete\` means the technical checks passed, but human review is still required.
- The tool always sets \`full_watch_completed: false\` and \`approval.approved: false\`.
- A report is **not** evidence that the film's story, character continuity, audio mix, captions, rights, or visual quality passed.
- A checksum identifies the exact inspected file. If the MP4 changes, run the inspection again.

The tool does not upload, publish, alter project manifests, or overwrite the pre-render baseline reports. Store generated reports outside the canonical project folders until a reviewer has checked the export and deliberately registers the report.
