#!/usr/bin/env python3
"""Parallel additive push (one-shot).

Prefer over gh_push.py for large pushes: parallel blob uploads route around the
VM egress proxy's intermittent hung-HTTPS-POST behavior (2026-10-06).

Same auth pattern as gh_push.py: stored `custom.github` connector credential
via surrogate exchange -- never a raw token. Builds the new tree ON TOP OF
the current HEAD (base_tree), so files not in the stage dir are preserved.
Blobs upload in parallel (12 workers) to route around the VM egress proxy's
intermittent hung-HTTPS-POST behavior; each attempt has a 30s timeout and
exponential backoff. Compare-and-swap on the ref: the ref is re-read right
before PATCH and the push aborts if HEAD moved underneath us.

Usage: push-parallel.py --dir /tmp/push-stage --message "..." [--repo lukezhang-si]
"""
import argparse
import base64
import json
import os
import sys
import threading
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
import dynamic_credentials as dc

CRED = "custom.github"
HOSTS = ["api.github.com"]
API = "https://api.github.com"
WORKERS = 12
TRIES = 4
TIMEOUT = 30

sign_lock = threading.Lock()
prog_lock = threading.Lock()
done = [0]
failed = []


def api(method, path, body=None, timeout=TIMEOUT):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with sign_lock:
        dc.add_surrogate_to_request(req, CRED, allowed_hosts=HOSTS)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status, dc.read_json_response(resp)
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(dc.read_response_body(e).decode())
        except Exception:
            payload = {"message": "HTTP %s" % e.code}
        return e.code, payload


def upload_blob(owner, repo, rel, content):
    body = {"content": base64.b64encode(content).decode(), "encoding": "base64"}
    last = (0, {})
    for attempt in range(TRIES):
        try:
            code, blob = api("POST", "/repos/%s/%s/git/blobs" % (owner, repo), body)
        except Exception as e:
            code, blob = 0, {"message": "%s: %s" % (type(e).__name__, str(e)[:80])}
        if code in (200, 201):
            with prog_lock:
                done[0] += 1
                if done[0] % 50 == 0 or done[0] == total[0]:
                    print("  blobs %d/%d" % (done[0], total[0]), flush=True)
            return rel, blob["sha"]
        last = (code, blob)
        time.sleep(2 ** attempt)
    with prog_lock:
        failed.append((rel, last))
    return rel, None


def api_retry(method, path, body, what, tries=5):
    last = (0, {})
    for attempt in range(tries):
        try:
            code, resp = api(method, path, body)
        except Exception as e:
            code, resp = 0, {"message": "%s: %s" % (type(e).__name__, str(e)[:80])}
        if code in (200, 201):
            return code, resp
        last = (code, resp)
        print("  %s attempt %d: %s %s" % (what, attempt + 1, code, str(resp)[:100]), flush=True)
        time.sleep(2 ** attempt)
    return last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="lukezhang-si")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--message", required=True)
    args = ap.parse_args()

    files = []
    for root, _dirs, filenames in os.walk(args.dir):
        for fn in sorted(filenames):
            if fn.startswith("."):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, args.dir)
            with open(full, "rb") as f:
                files.append((rel, f.read()))
    if not files:
        sys.exit("no files in %s" % args.dir)
    total.append(len(files))
    print("pushing %d files" % len(files), flush=True)

    code, me = api("GET", "/user")
    if code != 200:
        sys.exit("GET /user failed: %s %s" % (code, me))
    owner = me["login"]

    # Current HEAD (for base_tree + CAS check).
    code, ref = api("GET", "/repos/%s/%s/git/ref/heads/main" % (owner, args.repo))
    if code != 200:
        sys.exit("GET ref failed: %s %s" % (code, ref))
    head_sha = ref["object"]["sha"]
    code, commit = api("GET", "/repos/%s/%s/git/commits/%s" % (owner, args.repo, head_sha))
    if code != 200:
        sys.exit("GET commit failed: %s %s" % (code, commit))
    base_tree = commit["tree"]["sha"]
    print("HEAD %s base_tree %s" % (head_sha[:8], base_tree[:8]), flush=True)

    # Reuse blob SHAs from a previous run if the file set is identical.
    sha_cache = "/tmp/push-shas.json"
    shas = {}
    try:
        cached = json.load(open(sha_cache))
        if set(cached.keys()) == set(rel for rel, _ in files):
            shas = cached
            print("reusing %d cached blob SHAs" % len(shas), flush=True)
    except Exception:
        pass

    if not shas:
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            futs = [ex.submit(upload_blob, owner, args.repo, rel, content)
                    for rel, content in files]
            for fut in futs:
                rel, sha = fut.result()
                if sha:
                    shas[rel] = sha
        if failed:
            for rel, (code, blob) in failed[:5]:
                print("FAILED blob %s: %s %s" % (rel, code, str(blob)[:120]))
            sys.exit("aborting: %d blob uploads failed" % len(failed))
        json.dump(shas, open(sha_cache, "w"))
        print("saved blob SHAs", flush=True)

    entries = [{"path": rel, "mode": "100644", "type": "blob", "sha": shas[rel]}
               for rel, _ in files]
    code, tree_resp = api_retry("POST", "/repos/%s/%s/git/trees" % (owner, args.repo),
                                {"base_tree": base_tree, "tree": entries}, "create tree")
    if code not in (200, 201):
        sys.exit("create tree failed: %s %s" % (code, tree_resp))

    code, commit_resp = api_retry("POST", "/repos/%s/%s/git/commits" % (owner, args.repo), {
        "message": args.message, "tree": tree_resp["sha"], "parents": [head_sha]}, "create commit")
    if code not in (200, 201):
        sys.exit("create commit failed: %s %s" % (code, commit_resp))
    new_sha = commit_resp["sha"]

    # Compare-and-swap: re-read the ref; abort if HEAD moved.
    code, ref2 = api("GET", "/repos/%s/%s/git/ref/heads/main" % (owner, args.repo))
    if code != 200 or ref2["object"]["sha"] != head_sha:
        sys.exit("ABORT: HEAD moved during push (was %s, now %s); commit %s orphaned, nothing clobbered"
                 % (head_sha[:8], ref2["object"]["sha"][:8] if code == 200 else "?", new_sha[:8]))
    code, _ = api_retry("PATCH", "/repos/%s/%s/git/refs/heads/main" % (owner, args.repo),
                      {"sha": new_sha}, "update ref")
    if code not in (200, 201):
        sys.exit("update ref failed: %s" % code)
    print("pushed %d files @ %s (was %s)" % (len(entries), new_sha[:8], head_sha[:8]), flush=True)


total = []
if __name__ == "__main__":
    main()
