# Project initialization and workflow-state CLI

The repository now includes a small standard-library CLI for initializing project folders and recording production progress. It edits only local JSON project records; it does not call VideoExpress, Runway, YouTube, or any paid generation endpoint.

## Requirements

- Python 3.12+
- Run commands from the repository root.
- The default project template is **projects/_template/**.

## Initialize a project

    python scripts/manage_project.py init new-story \
      --title "New Story" \
      --runtime-seconds 300 \
      --source-story-ref "source.pdf pages 1-4"

This creates **projects/new-story/** with:
- **project.json** and a 300-second placeholder scene
- **script.md** and **storyboard.json** draft placeholders
- **corrections.json**
- **qa-report.json**

The command refuses to overwrite an existing project folder. Replace the placeholder scene/script with the source-checked story and approved storyboard before production.

## Inspect progress

    python scripts/manage_project.py status projects/the-clever-little-rabbits
    python scripts/manage_project.py status projects/mother-magpie --json

The status view reports the current workflow stage, target runtime, scene status counts, selected-scene count, and registered asset count.

## Register generated media

Register each output with a stable asset ID and attach it to the scene it covers:

    python scripts/manage_project.py add-asset projects/the-clever-little-rabbits \
      --asset-id rabbit-scene3-knock-001 \
      --type video \
      --provider VideoExpress \
      --model "VideoExpress 3.5" \
      --status approved_partial_scene_coverage \
      --coverage partial \
      --scene-id scene-03 \
      --duration-seconds 10 \
      --resolution 1920x1080 \
      --aspect-ratio 16:9 \
      --rights-note "User-generated; reviewed as partial scene coverage"

The coverage flag defaults to **partial** intentionally. Character references and partial clips must not be mistaken for complete scene coverage. Use **--coverage full** only after the complete scene coverage has been reviewed. Large media files remain in VideoExpress or approved external storage; store a stable storage reference and checksum in the manifest rather than committing video binaries to Git.

To attach an already registered asset to another scene:

    python scripts/manage_project.py attach-asset projects/the-clever-little-rabbits scene-03 rabbit-scene3-knock-001

## Update scene status

    python scripts/manage_project.py scene-status projects/the-clever-little-rabbits \
      scene-03 generated --note "Knock shot received; scene still needs reaction coverage"

    python scripts/manage_project.py scene-status projects/the-clever-little-rabbits \
      scene-03 selected --note "Complete scene coverage reviewed and approved"

A scene cannot become generated without linked image/video coverage. A scene cannot become selected unless it has an approved full-coverage visual asset. Assets marked partial or reference-only do not satisfy that gate.

## Advance workflow stages

    python scripts/manage_project.py set-stage projects/the-clever-little-rabbits \
      assets_ready --note "All storyboard scenes have approved full coverage"

    python scripts/manage_project.py set-stage projects/the-clever-little-rabbits \
      assembly --note "Beginning timeline assembly"

Stages advance one step at a time. The CLI records timestamp, actor, and note in workflow history. It refuses to advance to:
- **assets_ready** or **assembly** while any scene is not selected;
- **review** without a render output reference;
- **approved**, **export_ready**, or **upload_pending_approval** without a passing QA report, a complete end-to-end watch, explicit QA approval, and a render reference;
- **published** without explicit publishing approval metadata and YouTube ID, URL, visibility, and publication timestamp readback.

The CLI never uploads or publishes. Publishing approval must be recorded explicitly, and the actual YouTube upload/readback remains a separate authorized step.

## Record and resume a blocker

    python scripts/manage_project.py set-stage projects/mother-magpie \
      blocked --note "Waiting for approved character references"

    python scripts/manage_project.py resume projects/mother-magpie \
      --note "Character references are now approved"

The resume command returns to the exact stage recorded when the project was blocked.

## Tests

    python -m unittest discover -s tests -v

The tests cover project initialization without overwrite, status reporting, asset registration, partial-coverage protection, scene selection, stage-order enforcement, blocker/resume history, QA approval gates, path traversal protection for QA references, and publishing readback gates.

## Current integration boundary

This CLI is production-state tracking, not a renderer or provider adapter. VideoExpress 3.5 remains operated through its signed-in editor until official API documentation/support confirms a supported integration. The connected Runway workspace currently has no video, speech, music, or sound-effect models enabled, so this run did not submit any generation job or consume credits.
