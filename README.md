# VideoExpress

GitHub is the versioned **production brain** for the VideoExpress workflow: story/script versions, storyboard and scene instructions, character bibles, prompts/assets references, corrections, render metadata, QA reports, approvals, publishing records, and analytics insights.

## Start here
- [Production restart and current audit](docs/start-here.md) — current status and next actions
- [Production brain architecture](docs/production-brain.md)
- [Workflow foundation](docs/workflow-foundation.md)
- [Channel publishing, QA and feedback](docs/channel-publishing-and-feedback.md)
- [Export inspection and QA report](docs/render-inspection.md) — inspect final MP4 metadata and checksum with ffprobe

## Projects
- [The Clever Little Rabbits](projects/the-clever-little-rabbits/) — source-checked 5-minute draft, 10-scene storyboard and partial generated assets.
- [Mother Magpie](projects/mother-magpie/) — source-checked 5-minute draft, 9-scene storyboard; assets not yet generated.
- [Reusable project template](projects/_template/)

The original scanned storybook was inspected previously, but the source PDF is not currently available in the Library search. Existing scripts remain drafts. A separate expanded workflow document has alternate character names and 14-scene versions; do not mix it with the GitHub source-checked drafts without reconciliation/approval.

## Validation
Python 3.12+:

```bash
python -m pip install -r requirements.txt
python scripts/validate_project.py projects/the-clever-little-rabbits/project.json
python scripts/validate_project.py projects/mother-magpie/project.json
python -m unittest discover -s tests -v
```

GitHub Actions validates manifests and tests on pushes to feature branches and pull requests to `main` or `feat/video-pipeline-foundation`.

- [Project manifest schema](schemas/project.schema.json)
- [Correction entry schema](schemas/correction.schema.json)
- [QA report schema](schemas/qa-report.schema.json)

## Scope and safety
This repository is not yet a working web app or automatic VideoExpress renderer. VideoExpress API availability is unverified. Use the signed-in browser editor unless official API documentation/support confirms a supported integration. Store large media outside Git and reference them with metadata/checksums. Never commit credentials.

The final video must be watched end-to-end and checked before approval. Publishing, visibility, or scheduling require explicit user approval and upload readback verification.
