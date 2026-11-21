# VideoExpress

GitHub is the versioned **production brain** for the VideoExpress workflow: story/script versions, storyboard and scene instructions, character bibles, prompts/assets references, corrections, render metadata, QA reports, approvals, publishing records, and analytics insights.

## Start here
- [Production brain architecture](docs/production-brain.md)
- [Workflow foundation](docs/workflow-foundation.md)
- [Channel publishing, QA and feedback](docs/channel-publishing-and-feedback.md)

## Project folders
- [The Clever Little Rabbits](projects/the-clever-little-rabbits/) — 5-minute outline and project manifest; original story must be verified before script approval.
- [Mother Magpie](projects/mother-magpie/) — 5-minute outline and project manifest; original story must be verified before script approval.
- [Reusable project template](projects/_template/)

## Validation contracts
- [Project manifest schema](schemas/project.schema.json)
- [Correction entry schema](schemas/correction.schema.json)
- [QA report schema](schemas/qa-report.schema.json)

## Current scope
This branch contains workflow documentation, schemas, templates, and initial project plans. It is not yet a working web app or automatic VideoExpress renderer. VideoExpress API availability is unverified; production integrations should only use documented/authorized APIs. Media files should be stored outside Git and referenced with metadata/checksums.

## Safety and approval
Never commit credentials. The final video must be watched end-to-end and checked before approval. Publishing, visibility, or scheduling require explicit user approval and upload readback verification.
