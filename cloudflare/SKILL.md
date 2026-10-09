---
name: "cloudflare"
description: "Manage Luke's Cloudflare account via the API: deploy Workers, check deploy status. Auth comes from the stored `custom.cloudflare` connector credential via surrogate exchange — never a raw key in chat, flags, env vars, or files. Trigger on: 'deploy the worker', 'cloudflare worker', 'redeploy'."
---

# Cloudflare

## Purpose
Deploy and manage Cloudflare Workers on Luke's account (Absolukie@gmail.com) through the Cloudflare REST API. Used when `wrangler` CLI auth is unavailable on this VM.

## Tooling
- `bin/deploy-worker.py` — bundle a worker with esbuild and upload it via the Script Update API. Reads `wrangler.toml` for the script name, compatibility date, Durable Object bindings, and migrations.
  ```
  bin/deploy-worker.py --dir ~/workspace/liverpool-rummy/worker
  ```
  Options: `--dir` (worker dir containing wrangler.toml and src/), `--account` (account ID; auto-discovered from the first account if omitted), `--esbuild` (path to the esbuild binary).
- `bin/deploy-pages.py` — deploy a static directory to Cloudflare Pages via the Direct Upload API (added 2026-10-07, built for the overnight sprint).
  ```
  bin/deploy-pages.py --dir ~/workspace/builds/buyback --project buyback
  ```
  Flow mirrors wrangler: upload-token → check-missing → base64 asset upload → upsert-hashes → create deployment with multipart manifest → poll → verify 200. Creates the project if missing.
- Raw API calls: `GET /client/v4/accounts` to list accounts, `GET /client/v4/accounts/{id}/workers/scripts` to list workers.

## Pages file-hash gotcha (learned 2026-10-07)
Pages asset hashes are NOT sha256. The recipe (verified byte-for-byte against wrangler's own test vector `2082190357cfd3617ccfe04f340c6247`):
`hex(blake3(base64(file_bytes) + ext_without_dot))[:32]`
Uploading under sha256 hashes "succeeds" but the deployment 500s on every path because the manifest points at nonexistent assets. The `blake3` PyPI package implements it.

## Auth
All requests go through `/opt/hatch/skills/skill-creator/bin/dynamic_credentials.py`:
`dc.add_surrogate_to_request(req, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])`.
A 401/403 means the token is wrong, misplaced, or under-scoped (needs Workers Scripts:Edit). Confirm the request carried the credential before blaming the token.

## Operating Rules
1. Never print, log, or store the raw credential. The surrogate exchange keeps it server-side.
2. Deploying replaces the live worker. Before deploying, confirm the code passed its tests (`npm test` in the worker dir) and `node --check` on edited files.
3. After deploy, verify against the live worker URL: hit a safe read endpoint and confirm the new behavior (e.g. a changed response shape), not just a 200.
4. Migrations are omitted from API deploys: the API rejects re-applying an already-applied sqlite-class migration. Only add a migration when the Durable Object schema actually changed, and then it must be a NEW tag (wrangler handles this; the API script does not auto-bump).
5. The Script Update API only replaces code + metadata settings. Dashboard-only settings (custom domains, triggers) are untouched, but double-check the worker still serves its routes after deploy.

## Hosting rule (Luke's standing decision, 2026-10-05; enforced 2026-10-07)
New shareable web builds go to `projects.lukezhang.si/<site>/` through the lukezhang-si router — NEVER a new Pages project. The account hit the 100-project soft cap; every new Pages project burns a scarce slot. Porting: copy the site's static files into `sites/<name>/` in the `lukezhang-si` repo (index.html required, all asset paths relative), add `<name>` to the `SITES` array in `worker.js`, push via the surgical tree-commit pattern (fetch fresh worker.js from the API, new tree on `base_tree` = head tree, compare-and-swap the ref — never push a stale /tmp copy, never full-tree push over the router). `bin/deploy-pages.py` exists only for legacy Pages projects and one-off prototypes, not for new launches.
