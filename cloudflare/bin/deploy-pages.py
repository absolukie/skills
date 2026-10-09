#!/usr/bin/env python3
"""Deploy a static site to Cloudflare Pages via the Direct Upload API.

Flow mirrors wrangler's pages deployment:
  1. GET  /accounts/{id}/pages/projects/{name}/upload-token      -> {jwt}
  2. POST /pages/assets/check-missing  {hashes}                  -> missing[]
  3. POST /pages/assets/upload  [{key,value,metadata,base64}]    -> ok
  4. POST /pages/assets/upsert-hashes {hashes}                   -> ok
  5. POST /accounts/{id}/pages/projects/{name}/deployments (multipart manifest)
  6. Poll deployment until it leaves queued/initializing.

Usage: deploy-pages.py --dir ~/workspace/builds/buyback --project buyback [--account ID]

Auth comes from the stored `custom.cloudflare` connector credential via
surrogate exchange -- never a raw key in chat, flags, env vars, or files.
"""
import argparse
import base64
import hashlib
import json
import mimetypes
import os
import sys
import time
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
import dynamic_credentials as dc

CRED = "custom.cloudflare"
HOSTS = ["api.cloudflare.com"]
API = "https://api.cloudflare.com/client/v4"


def api(method, path, body=None, ctype="application/json", bearer=None):
    data = body.encode() if isinstance(body, str) else body
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Accept", "application/json")
    if ctype:
        req.add_header("Content-Type", ctype)
    if bearer:
        req.add_header("Authorization", "Bearer " + bearer)
    else:
        dc.add_surrogate_to_request(req, CRED, allowed_hosts=HOSTS)
    try:
        resp = urllib.request.urlopen(req, timeout=180)
        raw = resp.read()
        return resp.status, json.loads(raw.decode()) if raw else {}
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


def ext_without_dot(filename):
    """Node path.extname semantics: extension without the leading dot."""
    base = os.path.basename(filename)
    i = base.rfind(".")
    if i <= 0:
        return ""
    return base[i + 1:]


def pages_hash(blob, filename):
    """Cloudflare Pages file hash (from wrangler source):
    hex(blake3(base64(content) + extWithoutDot))[:32]."""
    from blake3 import blake3
    return blake3((base64.b64encode(blob).decode() + ext_without_dot(filename)).encode()).hexdigest()[:32]


def collect_files(root):
    out = []
    for dirpath, _, filenames in os.walk(root):
        for fn in sorted(filenames):
            if fn.startswith("."):
                continue
            full = os.path.join(dirpath, fn)
            rel = "/" + os.path.relpath(full, root).replace(os.sep, "/")
            with open(full, "rb") as f:
                blob = f.read()
            h = pages_hash(blob, fn)
            ctype = mimetypes.guess_type(fn)[0] or "application/octet-stream"
            if fn.endswith(".js"):
                ctype = "application/javascript"
            out.append({"path": rel, "hash": h, "blob": blob, "ctype": ctype})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--account", default=None)
    args = ap.parse_args()

    files = collect_files(os.path.abspath(os.path.expanduser(args.dir)))
    if not files:
        sys.exit("no files found")
    print("files: %d" % len(files), flush=True)
    account = get_account_id(args.account)

    # ensure project exists
    code, data = api("GET", "/accounts/%s/pages/projects/%s" % (account, args.project))
    if code == 404 or not data.get("success"):
        code, data = api("POST", "/accounts/%s/pages/projects" % account,
                         json.dumps({"name": args.project, "production_branch": "main"}))
        if code not in (200, 201) or not data.get("success"):
            sys.exit("project create failed: %s" % json.dumps(data)[:400])
        print("created project " + args.project, flush=True)

    # 1. upload token
    code, data = api("GET", "/accounts/%s/pages/projects/%s/upload-token" % (account, args.project))
    if code != 200 or not data.get("success"):
        sys.exit("upload-token failed: %s" % json.dumps(data)[:400])
    jwt = data["result"]["jwt"]

    # 2. check missing
    hashes = [f["hash"] for f in files]
    code, data = api("POST", "/pages/assets/check-missing", json.dumps({"hashes": hashes}), bearer=jwt)
    if code != 200 or not data.get("success"):
        sys.exit("check-missing failed: %s" % json.dumps(data)[:400])
    missing = set(data["result"] if isinstance(data["result"], list) else data["result"].get("missing", []))
    print("missing blobs: %d" % len(missing), flush=True)

    # 3. upload missing
    payload = [{"key": f["hash"], "value": base64.b64encode(f["blob"]).decode(),
                "metadata": {"contentType": f["ctype"]}, "base64": True}
               for f in files if f["hash"] in missing]
    if payload:
        code, data = api("POST", "/pages/assets/upload", json.dumps(payload), bearer=jwt)
        if code != 200 or not data.get("success"):
            sys.exit("assets upload failed: %s" % json.dumps(data)[:500])
        print("uploaded %d blobs" % len(payload), flush=True)

    # 4. upsert hashes
    code, data = api("POST", "/pages/assets/upsert-hashes", json.dumps({"hashes": hashes}), bearer=jwt)
    if code != 200:
        print("warning: upsert-hashes -> %s" % json.dumps(data)[:200], flush=True)

    # 5. create deployment with manifest
    manifest = {f["path"]: f["hash"] for f in files}
    boundary = "----pagesdeploy%d" % os.getpid()
    mjson = json.dumps(manifest)
    body = ("--%s\r\nContent-Disposition: form-data; name=\"manifest\"\r\n\r\n%s\r\n--%s--\r\n"
            % (boundary, mjson, boundary)).encode()
    code, data = api("POST", "/accounts/%s/pages/projects/%s/deployments" % (account, args.project),
                     body, ctype="multipart/form-data; boundary=" + boundary)
    if code not in (200, 201) or not data.get("success"):
        sys.exit("deployment create failed: %s" % json.dumps(data)[:500])
    dep = data["result"]
    dep_id, url = dep["id"], dep.get("url", "")
    print("deployment %s" % dep_id[:8], flush=True)

    # 6. poll
    for _ in range(30):
        time.sleep(4)
        code, data = api("GET", "/accounts/%s/pages/projects/%s/deployments/%s" % (account, args.project, dep_id))
        if code == 200 and data.get("success"):
            stage = (data["result"].get("latest_stage") or {}).get("name")
            status = (data["result"].get("latest_stage") or {}).get("status")
            if stage not in ("queued", "initialize") or status in ("success", "failure", "idle"):
                url = data["result"].get("url", url)
                break
    # verify live
    live = False
    for _ in range(12):
        time.sleep(5)
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=20)
            if r.status == 200 and b"Buyback" in r.read()[:20000]:
                live = True
                break
        except Exception:
            pass
    print("LIVE: " + url + (" (verified 200)" if live else " (NOT verified - check manually)"), flush=True)


if __name__ == "__main__":
    main()
