# Provider integration readiness

Status checked: 2026-11-22

## VideoExpress 3.5

The user can operate the VideoExpress 3.5 browser editor. Its Profile screen shows a field labelled "VideoExpress API key", but that field alone does not establish a documented API endpoint, authentication flow, permissions, job lifecycle, rate limits, or supported export methods.

Until official API documentation or vendor support confirms those details:
- Use the browser editor with user-guided steps for production.
- Do not reverse-engineer undocumented endpoints or use browser session cookies as API credentials.
- Do not commit keys, tokens, or account data to this repository.
- If an official API is confirmed, store its key as a server-side secret (e.g. `VIDEOEXPRESS_API_KEY`) and implement an adapter behind the provider-neutral `VideoProvider` interface.

Official product site: https://videoexpress.ai/  
Editor: https://app.videoexpress.ai/

## Runway

Runway can be used as an optional provider through the connected ChatGPT integration when the current workspace exposes video-generation capability. Availability must be checked at runtime; do not assume that the tool schema or a connected account guarantees video access.

The connected integration was checked on 2026-11-22. It authenticated, but its available video-model list was empty, so video generation could not be invoked from this workspace during this check. Image-generation models were available. No generation job was submitted.

## Integration acceptance checklist

Before implementing a production adapter, verify:
- Official API documentation and supported model/task identifiers.
- Authentication and required scopes/permissions.
- Request/response schemas and asynchronous job lifecycle.
- Polling, callbacks, retryable vs. permanent errors, and rate limits.
- Pricing/credits and a user-confirmation gate before paid generation.
- Secure secret storage, redacted logs, and no secrets in client code or manifests.
- Output download/storage, checksums, rights/source metadata, and QA.
- Tests with mocked provider responses plus a small explicitly approved live integration test.

## Current safe fallback

Keep the source-of-truth project manifest, script, storyboard, character bible, corrections, and QA in GitHub. Generate scenes in the VideoExpress UI while the user is logged in, then record the resulting asset metadata and local/external storage reference. This is a manual production path, not yet automated end-to-end.
