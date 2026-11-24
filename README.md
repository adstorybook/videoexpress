# VideoExpress

GitHub is the versioned **production brain** for the VideoExpress workflow: story/script versions, storyboard and scene instructions, character bibles, prompts/assets references, corrections, render metadata, QA reports, approvals, publishing records, and analytics insights.

## Start here
- [Production restart and current audit](docs/start-here.md) — current status and next actions
- [Production brain architecture](docs/production-brain.md)
- [Workflow foundation](docs/workflow-foundation.md)
- [Channel publishing, QA and feedback](docs/channel-publishing-and-feedback.md)
- [Project initialization and workflow-state CLI](docs/project-state-cli.md)

## Projects
- [The Clever Little Rabbits](projects/the-clever-little-rabbits/) — source-checked 5-minute draft, 10-scene storyboard and partial generated assets.
- [Mother Magpie](projects/mother-magpie/) — source-checked 5-minute draft, 9-scene storyboard; assets not yet generated.
- [Reusable project template](projects/_template/)

The original scanned storybook was inspected previously, but the source PDF is not currently available in the Library search. Existing scripts remain drafts. A separate expanded workflow document has alternate character names and 14-scene versions; do not mix these versions without reconciliation and user approval.

## Validation

Python 3.12+:

    python -m pip install -r requirements.txt
    python scripts/validate_project.py projects/the-clever-little-rabbits/project.json
    python scripts/validate_project.py projects/mother-magpie/project.json
    python -m unittest discover -s tests -v

GitHub Actions validates manifests and tests on pushes to main and feature branches, and on pull requests to main.

- [Project manifest schema](schemas/project.schema.json)
- [Correction entry schema](schemas/correction.schema.json)
- [QA report schema](schemas/qa-report.schema.json)

## Project initialization and progress tracking

The standard-library CLI initializes new project folders from the template and records scene assets/status plus guarded workflow transitions.

    python scripts/manage_project.py init new-story --title "New Story" --runtime-seconds 300
    python scripts/manage_project.py status projects/new-story
    python scripts/manage_project.py --help

See [CLI commands and safety gates](docs/project-state-cli.md). The CLI records metadata only; generated media stays in VideoExpress or approved external storage.

## Scope and safety

This repository is not yet a working web app or automatic VideoExpress renderer. VideoExpress API availability is unverified. Use the signed-in browser editor unless official API documentation/support confirms a supported integration. Store large media outside Git and reference them with metadata/checksums. Never commit credentials.

The final video must be watched end-to-end and checked before approval. Publishing, visibility, or scheduling require explicit user approval and upload readback verification.
