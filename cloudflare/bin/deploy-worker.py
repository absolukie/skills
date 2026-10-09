#!/usr/bin/env python3
"""Deploy a Cloudflare Worker via the Script Update API.

Bundles the entry point with esbuild, reads wrangler.toml for the script
name / compatibility date / Durable Object bindings / migrations, and
uploads everything as multipart/form-data.

Auth comes from the stored `custom.cloudflare` connector credential via
surrogate exchange -- never a raw key in chat, flags, env vars, or files.

Usage:
  deploy-worker.py --dir ~/workspace/liverpool-rummy/worker [--account ID]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
import dynamic_credentials as dc

CRED = "custom.cloudflare"
HOSTS = ["api.cloudflare.com"]
API = "https://api.cloudflare.com/client/v4"


def api(method, path, body=None, content_type=None):
    req = urllib.request.Request(API + path, data=body, method=method)
    req.add_header("Accept", "application/json")
    if content_type:
        req.add_header("Content-Type", content_type)
    elif body is not None:
        req.add_header("Content-Type", "application/json")
    dc.add_surrogate_to_request(req, CRED, allowed_hosts=HOSTS)
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode())
        except Exception:
            payload = {"errors": [{"message": "HTTP %s" % e.code}]}
        return e.code, payload


def get_account_id(hint=None):
    code, data = api("GET", "/accounts")
    if code != 200 or not data.get("success"):
        sys.exit("accounts lookup failed: %s" % json.dumps(data)[:300])
    accounts = data["result"]
    if hint:
        for a in accounts:
            if a["id"] == hint or a["name"] == hint:
                return a["id"]
        sys.exit("no account matching %r" % hint)
    if not accounts:
        sys.exit("no Cloudflare accounts found")
    return accounts[0]["id"]


def build_metadata(cfg):
    meta = {"main_module": "worker.js"}
    if cfg.get("compatibility_date"):
        meta["compatibility_date"] = cfg["compatibility_date"]
    bindings = []
    for b in cfg.get("durable_objects", {}).get("bindings", []):
        bindings.append({
            "type": "durable_object_namespace",
            "name": b["name"],
            "class_name": b["class_name"],
        })
    # D1 databases: [[d1_databases]] with database_id + binding.
    # CRITICAL (learned 2026-10-09): the Script Update API REPLACES all
    # bindings with what this metadata declares. Anything the worker needs
    # (D1, R2, KV) MUST be declared here, or a deploy silently unwires it
    # (env.DB becomes undefined) while dashboard-only settings survive.
    # wrangler.toml is the source of truth; never rely on dashboard-only
    # bindings with this script.
    for db in cfg.get("d1_databases", []):
        bindings.append({
            "type": "d1",
            "name": db["binding"],
            "id": db["database_id"],
        })
    for b in cfg.get("r2_buckets", []):
        bindings.append({
            "type": "r2_bucket",
            "name": b["binding"],
            "bucket_name": b["bucket_name"],
        })
    if bindings:
        meta["bindings"] = bindings
    # Plain (non-secret) vars. Same replacement semantics: declare every
    # var the worker reads, or it vanishes on deploy. Secrets are managed
    # separately and are NOT affected by this call.
    if cfg.get("vars"):
        meta["vars"] = dict(cfg["vars"])
    # Migrations are intentionally omitted: the API rejects re-applying an
    # already-applied sqlite-class migration, and this deploy changes only
    # worker code, not the Durable Object schema. Omit the key and the
    # existing DO configuration is left untouched.
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="worker dir with wrangler.toml")
    ap.add_argument("--account", default=None, help="account ID or name")
    ap.add_argument("--esbuild", default=None, help="path to esbuild binary")
    args = ap.parse_args()

    with open(os.path.join(args.dir, "wrangler.toml"), "rb") as f:
        cfg = tomllib.load(f)
    name = cfg.get("name")
    entry = os.path.join(args.dir, cfg.get("main", "src/index.js"))
    if not name:
        sys.exit("wrangler.toml has no name")

    esbuild = args.esbuild or shutil.which("esbuild") or os.path.expanduser(
        "~/workspace/liverpool-rummy/worker/node_modules/.bin/esbuild")
    if not (esbuild and os.path.exists(esbuild)):
        sys.exit("esbuild not found; pass --esbuild")

    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "worker.js")
        r = subprocess.run(
            [esbuild, entry, "--bundle", "--format=esm",
             "--target=es2022", "--outfile=" + out],
            capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("esbuild failed:\n" + r.stderr[-2000:])
        with open(out, "rb") as f:
            bundle = f.read()
    print("bundled %d bytes" % len(bundle), file=sys.stderr)

    metadata = build_metadata(cfg)
    boundary = "----cfdeploy" + os.urandom(8).hex()
    body = b"".join([
        ("--" + boundary + "\r\n").encode(),
        b'Content-Disposition: form-data; name="metadata"\r\n',
        b"Content-Type: application/json\r\n\r\n",
        json.dumps(metadata).encode(), b"\r\n",
        ("--" + boundary + "\r\n").encode(),
        b'Content-Disposition: form-data; name="worker.js"; filename="worker.js"\r\n',
        b"Content-Type: application/javascript+module\r\n\r\n",
        bundle, b"\r\n",
        ("--" + boundary + "--\r\n").encode(),
    ])

    account_id = get_account_id(args.account)
    code, data = api(
        "PUT", "/accounts/%s/workers/scripts/%s" % (account_id, name),
        body=body,
        content_type="multipart/form-data; boundary=" + boundary)
    if code != 200 or not data.get("success"):
        sys.exit("deploy failed (HTTP %s): %s" % (code, json.dumps(data)[:1000]))
    print(json.dumps({
        "script": data["result"].get("id"),
        "etag": data["result"].get("etag"),
        "modified_on": data["result"].get("modified_on"),
    }, indent=2))


if __name__ == "__main__":
    main()
