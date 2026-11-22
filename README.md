# VideoExpress

GitHub is the versioned **production brain** for the VideoExpress workflow: story/script versions, storyboard and scene instructions, character bibles, prompts/assets references, corrections, render metadata, QA reports, approvals, publishing records, and analytics insights.

## Start here
- [Production brain architecture](docs/production-brain.md)
- [Workflow foundation](docs/workflow-foundation.md)
- [Channel publishing, QA and feedback](docs/channel-publishing-and-feedback.md)

## Project folders
- [The Clever Little Rabbits](projects/the-clever-little-rabbits/) — source-checked 5-minute script draft, 10-scene storyboard and manifest.
- [Mother Magpie](projects/mother-magpie/) — source-checked 5-minute script draft, 9-scene storyboard and manifest.

The user's scanned storybook (5 pages) has been inspected. The source PDF is not committed to this repository; projects cite the source page ranges. Both scripts remain drafts awaiting user approval.
- [Reusable project template](projects/_template/)

## Validation contracts

Validate a project manifest locally (Python 3.12+):

```bash
python -m pip install -r requirements.txt
python scripts/validate_project.py projects/the-clever-little-rabbits/project.json
python scripts/validate_project.py projects/mother-magpie/project.json
python -m unittest discover -s tests -v
```

The validator also checks duplicate scene/character/asset IDs and catches broken character or scene references to assets. GitHub Actions runs the tests and validates both seed projects on pushes to `main` or `feat/**`, pull requests to `main`, and manual runs.

- [Project manifest schema](schemas/project.schema.json)
- [Correction entry schema](schemas/correction.schema.json)
- [QA report schema](schemas/qa-report.schema.json)

## Current scope
This branch contains workflow documentation, schemas, templates, and initial project plans. It is not yet a working web app or automatic VideoExpress renderer. VideoExpress API availability is unverified; production integrations should only use documented/authorized APIs. Media files should be stored outside Git and referenced with metadata/checksums.

## Safety and approval
Never commit credentials. The final video must be watched end-to-end and checked before approval. Publishing, visibility, or scheduling require explicit user approval and upload readback verification.
