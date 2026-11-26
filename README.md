# VideoExpress

GitHub is the versioned **production brain** for the VideoExpress workflow: story/script versions, storyboard and scene instructions, character bibles, prompts/assets references, corrections, render metadata, QA reports, approvals, publishing records, and analytics insights.

## Start here
- [Production restart and current audit](docs/start-here.md) — current status and next actions
- [Production brain architecture](docs/production-brain.md)
- [Workflow foundation](docs/workflow-foundation.md)
- [Channel publishing, QA and feedback](docs/channel-publishing-and-feedback.md)

## Projects
- [The Clever Little Rabbits](projects/the-clever-little-rabbits/) — source-checked 5-minute draft, 10-scene storyboard and partial generated assets.
- [Mother Magpie](projects/mother-magpie/) — source-checked 5-minute draft, 9-scene storyboard; assets not yet generated.
- [Reusable project template](projects/_template/)

## Expanded production packs
- [Expanded story production packs](production-packs/expanded-retellings/) — 14-scene retellings with per-scene still-reference prompts, VideoExpress prompts, narration, optional dialogue, voice direction and audio cues.

**Canon warning:** the expanded packs use alternate character names/designs and remain separate from the source-checked project manifests. Do not replace the canonical project scripts or asset records until the user approves a reconciliation. The original scanned PDF was not re-verified in this update.

## Validation
Python 3.12+:

```bash
python -m pip install -r requirements.txt
python scripts/validate_project.py projects/the-clever-little-rabbits/project.json
python scripts/validate_project.py projects/mother-magpie/project.json
python -m unittest discover -s tests -v
```

GitHub Actions validates manifests and tests on pushes to the development branch and pull requests to `main`.

- [Project manifest schema](schemas/project.schema.json)
- [Correction entry schema](schemas/correction.schema.json)
- [QA report schema](schemas/qa-report.schema.json)

## Scope and safety
This repository is not yet a working web app or automatic VideoExpress renderer. VideoExpress API availability is unverified. Use the signed-in browser editor unless official API documentation/support confirms a supported integration. Store large media outside Git and reference them with metadata/checksums. Never commit credentials.

The final video must be watched end-to-end and checked before approval. Publishing, visibility, or scheduling require explicit user approval and upload readback verification.
