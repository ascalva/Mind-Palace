"""The CI witness — attest GitLab pipeline verdicts into the chain (owner rule 2026-07-11).

A green pipeline is a claim by an external system; the witness turns it into an
ATTESTED fact: it fetches the pipeline for a commit from the GitLab API and emits
`ci_witness / pipeline_green|pipeline_red` with the commit sha as input and
`pipeline:<id>` as output — chained to the code-sensor's ingest of the same sha, so
"this commit's tests passed remotely" is signed history, not a memory of a web page.

Zone note, stated honestly: this runs UNSEALED at the ops tier and talks to gitlab.com
(stdlib urllib) — the restic/terraform precedent (ops tools reach services from their
own process; the sealed core never does). It is invoked standalone or as a subprocess
of `palace deploy` (whose own process IS sealed; the witness child is not).

Auth: pipeline metadata on this project is public (no token). Playing the manual
semantic-release job needs a token — read from Keychain (`security find-generic-password
-a mind-palace -s gitlab-api -w`), never from config or argv. Absent a token, `release`
degrades to printing the pipeline URL for a by-hand play.
"""

from __future__ import annotations

import json
import subprocess
import urllib.parse
import urllib.request

PROJECT = "ascalva-projects/mind-palace"
API = "https://gitlab.com/api/v4/projects/" + urllib.parse.quote(PROJECT, safe="")

# pipeline states that still have a verdict coming (poll); everything else is terminal
_PENDING = {"created", "waiting_for_resource", "preparing", "pending", "running"}


def _get(path: str, token: str | None = None) -> object:
    req = urllib.request.Request(API + path)
    if token:
        req.add_header("PRIVATE-TOKEN", token)
    with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310 — fixed https host
        return json.load(r)


def _keychain_token() -> str | None:
    r = subprocess.run(["security", "find-generic-password", "-a", "mind-palace",
                        "-s", "gitlab-api", "-w"], capture_output=True, text=True)
    return r.stdout.strip() or None if r.returncode == 0 else None


def pipeline_for(sha: str) -> dict | None:
    """Newest pipeline for the commit, or None if GitLab has none for it."""
    rows = _get(f"/pipelines?sha={sha}&per_page=1")
    return rows[0] if isinstance(rows, list) and rows else None


def verdict(pipe: dict | None) -> str:
    """'green' | 'red' | 'pending' | 'absent' — the witness never guesses."""
    if pipe is None:
        return "absent"
    if pipe["status"] in _PENDING:
        return "pending"
    # 'manual' = all automatic jobs done, only manual gates (semantic-release) remain: green.
    return "green" if pipe["status"] in ("success", "manual") else "red"


def attest_verdict(sha: str, pipe: dict, v: str) -> None:
    from config.loader import get_config
    from core.attestation import build_attestor

    attestor = build_attestor(get_config())
    if attestor is not None:
        attestor.emit(agent_role="ci_witness", action=f"pipeline_{v}",
                      input_hashes=[sha], output_hashes=[f"pipeline:{pipe['id']}"])


def check(sha: str, *, wait_s: float = 600.0) -> int:
    """Poll to a terminal verdict, attest it, rc 0 only on green."""
    import time
    deadline = time.monotonic() + wait_s
    pipe = pipeline_for(sha)
    while verdict(pipe) == "pending" and time.monotonic() < deadline:
        time.sleep(10)
        pipe = pipeline_for(sha)
    v = verdict(pipe)
    if v == "absent":
        print(f"ci-witness: no pipeline for {sha[:12]} — was it pushed? (docs-only pushes "
              "still create a pipeline; a missing one means the sha never reached origin)")
        return 1
    if v == "pending":
        print(f"ci-witness: pipeline {pipe['id']} still {pipe['status']} after {wait_s:.0f}s")
        return 1
    attest_verdict(sha, pipe, v)
    print(f"ci-witness: pipeline {pipe['id']} {v.upper()} for {sha[:12]} — attested")
    return 0 if v == "green" else 1


def release(sha: str) -> int:
    """Play the manual semantic-release job for the sha's pipeline (token required)."""
    pipe = pipeline_for(sha)
    if verdict(pipe) != "green":
        print(f"ci-witness: no green pipeline for {sha[:12]} — nothing to release.")
        return 1
    token = _keychain_token()
    if token is None:
        print("ci-witness: no gitlab-api token in Keychain — play semantic-release by hand:\n"
              f"  {pipe['web_url']}\n"
              "  (one-time setup: security add-generic-password -a mind-palace "
              "-s gitlab-api -w <PAT with api scope>)")
        return 0                                    # degraded, not failed: deploy proceeds
    jobs = _get(f"/pipelines/{pipe['id']}/jobs?scope[]=manual", token)
    rel = [j for j in jobs if j["name"] == "semantic-release"]
    if not rel:
        print("ci-witness: no manual semantic-release job on this pipeline — nothing to play.")
        return 0
    req = urllib.request.Request(API + f"/jobs/{rel[0]['id']}/play", method="POST",
                                 headers={"PRIVATE-TOKEN": token})
    with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310
        played = json.load(r)
    print(f"ci-witness: played semantic-release (job {played['id']}) — release in flight")
    return 0
