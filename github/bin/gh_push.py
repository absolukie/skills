#!/usr/bin/env python3
"""Push a local directory to a GitHub repo, creating the repo if needed.

Uses the GitHub REST API only (no git binary): blobs -> tree -> commit -> ref.
Auth comes from the stored `custom.github` connector credential via surrogate
exchange -- never a raw key in chat, flags, env vars, or files.

Usage:
  gh_push.py --repo NAME --dir PATH [--description TEXT] [--private]
             [--branch main] [--message "msg"]
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
import dynamic_credentials as dc

CRED = "custom.github"
HOSTS = ["api.github.com"]
API = "https://api.github.com"


def api(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    dc.add_surrogate_to_request(req, CRED, allowed_hosts=HOSTS)
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, dc.read_json_response(resp)
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(dc.read_response_body(e).decode())
        except Exception:
            payload = {"message": "HTTP %s" % e.code}
        return e.code, payload


def create_blob(blob_url, rel, content, tries=4):
    """POST a base64 blob with retry on transient 400s/timeouts."""
    body = {
        "content": base64.b64encode(content).decode(),
        "encoding": "base64",
    }
    last = (0, {})
    for attempt in range(tries):
        try:
            code, blob = api("POST", blob_url, body)
        except Exception as e:  # timeouts etc.
            code, blob = 0, {"message": "timeout: %s" % e}
        if code in (200, 201):
            return code, blob
        last = (code, blob)
        time.sleep(2 ** attempt)
    return last


def push_via_contents(owner, repo, branch, files, message):
    """File-by-file push for a completely empty repo (the git-database blob
    API 409s there). One commit per file."""
    import urllib.parse
    for i, (rel, content) in enumerate(files):
        msg = message if i == 0 else "Add %s" % rel
        code, resp = api("PUT", "/repos/%s/%s/contents/%s"
                         % (owner, repo, urllib.parse.quote(rel)), {
            "message": msg,
            "content": base64.b64encode(content).decode(),
            "branch": branch,
        })
        if code not in (200, 201):
            sys.exit("contents %s failed: %s %s" % (rel, code, resp))
    print("pushed %d files to https://github.com/%s/%s/tree/%s"
          % (len(files), owner, repo, branch))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="Repository name (created if missing)")
    ap.add_argument("--dir", required=True, help="Local directory whose files become the repo content")
    ap.add_argument("--description", default="")
    ap.add_argument("--private", action="store_true")
    ap.add_argument("--branch", default=None,
                    help="Target branch. Defaults to the repo's default branch. "
                         "If the branch does not exist yet, it is created.")
    ap.add_argument("--message", default="Initial commit")
    args = ap.parse_args()

    if not os.path.isdir(args.dir):
        sys.exit("not a directory: %s" % args.dir)

    code, me = api("GET", "/user")
    if code != 200:
        sys.exit("GET /user failed: %s %s" % (code, me))
    owner = me["login"]

    code, repo = api("GET", "/repos/%s/%s" % (owner, args.repo))
    if code == 404:
        code, repo = api("POST", "/user/repos", {
            "name": args.repo,
            "description": args.description,
            "private": args.private,
            "auto_init": False,
        })
        if code not in (200, 201):
            sys.exit("create repo failed: %s %s" % (code, repo))
        print("created repo %s" % repo["full_name"])
    elif code != 200:
        sys.exit("GET repo failed: %s %s" % (code, repo))
    # An explicit --branch always wins; otherwise use the repo default.
    # (Previously this line ignored --branch on existing repos and always
    # pushed to the default branch, which once overwrote main by accident.)
    default_branch = args.branch or repo.get("default_branch") or "main"

    local_files = []
    for root, _dirs, filenames in os.walk(args.dir):
        for fn in sorted(filenames):
            if fn.startswith("."):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, args.dir)
            with open(full, "rb") as f:
                local_files.append((rel, f.read()))
    if not local_files:
        sys.exit("no files found in %s" % args.dir)

    # Probe blob creation: GitHub 409s the git-database API on a completely
    # empty repo ("Git Repository is empty"), so fall back to the contents API.
    blob_url = "/repos/%s/%s/git/blobs" % (owner, args.repo)
    probe_rel, probe_content = local_files[0]
    code, blob = create_blob(blob_url, probe_rel, probe_content)
    if code == 409 and "empty" in str(blob.get("message", "")).lower():
        push_via_contents(owner, args.repo, default_branch, local_files, args.message)
        return
    if code not in (200, 201):
        sys.exit("blob %s failed: %s %s" % (probe_rel, code, blob))

    entries = [{"path": probe_rel, "mode": "100644", "type": "blob", "sha": blob["sha"]}]
    for rel, content in local_files[1:]:
        code, blob = create_blob(blob_url, rel, content)
        if code not in (200, 201):
            sys.exit("blob %s failed: %s %s" % (rel, code, blob))
        entries.append({"path": rel, "mode": "100644", "type": "blob", "sha": blob["sha"]})

    parents = []
    base_tree = None
    code, ref = api("GET", "/repos/%s/%s/git/ref/heads/%s" % (owner, args.repo, default_branch))
    if code == 200:
        head_sha = ref["object"]["sha"]
        parents = [head_sha]
        code, commit = api("GET", "/repos/%s/%s/git/commits/%s" % (owner, args.repo, head_sha))
        if code == 200:
            base_tree = commit["tree"]["sha"]

    tree_body = {"tree": entries}
    if base_tree:
        tree_body["base_tree"] = base_tree
    code, tree_resp = api("POST", "/repos/%s/%s/git/trees" % (owner, args.repo), tree_body)
    if code not in (200, 201):
        sys.exit("create tree failed: %s %s" % (code, tree_resp))

    code, commit_resp = api("POST", "/repos/%s/%s/git/commits" % (owner, args.repo), {
        "message": args.message,
        "tree": tree_resp["sha"],
        "parents": parents,
    })
    if code not in (200, 201):
        sys.exit("create commit failed: %s %s" % (code, commit_resp))

    new_sha = commit_resp["sha"]
    if parents:
        code, _ = api("PATCH", "/repos/%s/%s/git/refs/heads/%s" % (owner, args.repo, default_branch),
                      {"sha": new_sha})
    else:
        code, _ = api("POST", "/repos/%s/%s/git/refs" % (owner, args.repo),
                      {"ref": "refs/heads/%s" % default_branch, "sha": new_sha})
    if code not in (200, 201):
        sys.exit("update ref failed: %s" % code)

    print("pushed %d files to https://github.com/%s/%s/tree/%s @ %s"
          % (len(entries), owner, args.repo, default_branch, new_sha[:7]))


if __name__ == "__main__":
    main()
