#!/usr/bin/env python3
"""Validate Trust-v1 metadata, exact closure and publication boundaries."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "PUBLIC_SOURCE_MANIFEST.json"
RELEASE_PATH = ROOT / "RELEASE.json"
DENIED_DIRECTORIES = {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__", "node_modules"}
DENIED_SUFFIXES = {".key", ".map", ".p12", ".pem", ".pfx", ".pyc", ".pyo"}
REQUIRED_FILES = {
    ".gitattributes",
    ".github/workflows/codeql.yml",
    ".github/workflows/validate-profile.yml",
    "ARCHITECTURE.md",
    "ASSET_RIGHTS_INVENTORY.json",
    "CHANGELOG.md",
    "KNOWN_LIMITATIONS.md",
    "LICENSE.md",
    "NOTICE.md",
    "OWNER_GATE_STATUS.json",
    "PLANNED_PUBLIC_REPOSITORIES.json",
    "PUBLICATION_STATUS.md",
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "PUBLIC_SOURCE_MANIFEST.json",
    "README.md",
    "RELEASE.json",
    "SBOM.cdx.json",
    "SBOM.spdx.json",
    "SECURITY.md",
    "profile/README.md",
}

EXPECTED_REPOSITORY_EVIDENCE = {
    "engine-evidence": {
        "head": "03516148a5a2345c0bf967598c65194e5c5ea401",
        "tree": "993d88ee3dbb164a513c8bd392dd3d085b886239",
        "ci_runs": [31703977937, 31703977901, 31703977831, 31703977872],
        "codeql_analysis_id": 1613639143,
    },
    "ai-frontend": {
        "head": "f9192d49d11701c5b1e92efcd7b614922a4dc595",
        "tree": "54ab7014a3511443e890cfd3e066f7a6aa9605eb",
        "ci_runs": [31704278130, 31704278127],
        "codeql_analysis_id": 1613660523,
    },
    "token-portal": {
        "head": "b26bb211ec1c063e7fa2cdd36d0f085f01f3301a",
        "tree": "50f27eb376c7ab47469d7c0e1f8e9ad6bc0bf04e",
        "ci_runs": [31704480279],
        "codeql_analysis_id": 1613670899,
    },
    "platform-api": {
        "head": "44b9b15d1dbd2e70e3c4db8764f10bbae14c608c",
        "tree": "187e4b8416e048a505bb59290d9e05b5c610e1bb",
        "ci_runs": [31705801892],
        "codeql_analysis_id": 1613761037,
    },
    "corporate-site": {
        "head": "49ed20aae24b1832081a89f37eeb1007b1c72816",
        "tree": "64c7423ea2156948c31d64daa4b50cdd348de7b4",
        "ci_runs": [31706078911, 31706078886],
        "codeql_analysis_id": 1613778562,
    },
    "github-profile": {
        "head": "624ea78912e67ebc536d0e270446a9ec77563f31",
        "tree": "ead9651a5c956b0dc02333218dc9ffe3da8889d3",
        "ci_runs": [31692227539, 31692227634],
        "codeql_analysis_id": 1612947444,
    },
    "trust-layer-master": {
        "head": "dee8a0466f446602c5de0923eb3700f20c6ca19f",
        "tree": "95f212beab546ba945bc8d79451b1edf71587088",
        "ci_runs": [31699097582],
        "codeql_analysis_id": None,
    },
}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def actual_files() -> dict[str, Path]:
    return {
        path.relative_to(ROOT).as_posix(): path
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(ROOT).parts
    }


def validate() -> list[str]:
    errors: list[str] = []
    files = actual_files()
    missing_required = REQUIRED_FILES - files.keys()
    if missing_required:
        errors.append("missing required files: " + ", ".join(sorted(missing_required)))
    attributes = files.get(".gitattributes")
    if attributes is not None and attributes.read_bytes() != b"* text=auto eol=lf\n":
        errors.append("canonical LF .gitattributes policy mismatch")
    for relative, path in files.items():
        if b"\r\n" in path.read_bytes():
            errors.append(f"CRLF bytes violate canonical LF policy: {relative}")

    for current, directory_names, file_names in os.walk(ROOT, followlinks=False):
        current_path = Path(current)
        directory_names[:] = [name for name in directory_names if name != ".git"]
        for name in directory_names:
            path = current_path / name
            if path.is_symlink():
                errors.append(f"symlink directory denied: {path.relative_to(ROOT).as_posix()}")
            if name in DENIED_DIRECTORIES:
                errors.append(f"denied directory: {path.relative_to(ROOT).as_posix()}")
        for name in file_names:
            path = current_path / name
            relative = path.relative_to(ROOT).as_posix()
            if path.is_symlink():
                errors.append(f"symlink file denied: {relative}")
            if path.suffix.lower() in DENIED_SUFFIXES:
                errors.append(f"denied file suffix: {relative}")

    try:
        release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return errors + [f"metadata unreadable: {type(exc).__name__}"]

    expected_release = {
        "repository": "wotanIII/lumaquant-github-profile-public",
        "repository_url": "https://github.com/wotanIII/lumaquant-github-profile-public",
        "repository_creation_status": "COMPLETED",
        "public_release": "0.1.0-rc1",
        "live_domain": None,
        "artifact_type": "DOCUMENTATION_PROFILE_PUBLIC_STATUS",
        "release_class": "REFERENCE_IMPLEMENTATION",
        "source_private_commit_sha": None,
        "production_alignment": "REFERENCE_ONLY",
        "independent_audit": "NOT_YET_COMPLETED",
        "legal_review": "NOT_YET_COMPLETED",
        "license_status": "PROPRIETARY_SOURCE_AVAILABLE_ALL_RIGHTS_RESERVED",
        "operator_identity_status": "COMPLETED_OWNER_CONFIRMED",
        "security_contact": "security@lumaquant.tech",
        "security_contact_status": "COMPLETED_OWNER_CONFIRMED",
        "deployment_status": "NOT_DEPLOYED",
        "publication_review_status": "INDEPENDENT_PUBLICATION_REVIEW_PASSED",
        "publication_status": "PUBLIC_REPOSITORY_VERIFIED",
        "publication_performed": True,
        "visibility_status": "PUBLIC",
    }
    for key, value in expected_release.items():
        if release.get(key) != value:
            errors.append(f"release field mismatch: {key}")
    if release.get("open_review_matters") != [
        "LEGAL_REVIEW_NOT_YET_COMPLETED",
        "INDEPENDENT_THIRD_PARTY_AUDIT_NOT_YET_COMPLETED",
    ]:
        errors.append("release open review matters mismatch")

    try:
        repositories = json.loads((ROOT / "PLANNED_PUBLIC_REPOSITORIES.json").read_text(encoding="utf-8"))
        owner_status = json.loads((ROOT / "OWNER_GATE_STATUS.json").read_text(encoding="utf-8"))
        asset_inventory = json.loads((ROOT / "ASSET_RIGHTS_INVENTORY.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(f"owner metadata unreadable: {type(exc).__name__}")
    else:
        planned = repositories.get("repositories")
        expected_urls = [
            "https://github.com/wotanIII/luma-engine-evidence-public",
            "https://github.com/wotanIII/luma-ai-frontend-public",
            "https://github.com/wotanIII/luma-token-portal-public",
            "https://github.com/wotanIII/luma-platform-api-public",
            "https://github.com/wotanIII/luma-corporate-site-public",
            "https://github.com/wotanIII/lumaquant-github-profile-public",
            "https://github.com/wotanIII/luma-trust-layer-v1",
        ]
        if not isinstance(planned, list) or [entry.get("url") for entry in planned] != expected_urls:
            errors.append("planned public repository URLs mismatch")
        elif any(
            entry.get("repository_creation_status") != "COMPLETED"
            or entry.get("url_verification_status") != "VERIFIED"
            or entry.get("publication_performed") is not True
            or entry.get("visibility") != "PUBLIC"
            or entry.get("default_branch") != "main"
            or entry.get("ci", {}).get("status") != "PASS_AT_VERIFIED_PUBLIC_HEAD"
            for entry in planned
        ):
            errors.append("verified public repository status mismatch")
        if isinstance(planned, list):
            for entry in planned:
                expected = EXPECTED_REPOSITORY_EVIDENCE.get(entry.get("candidate"))
                if expected is None:
                    errors.append(f"unexpected repository evidence record: {entry.get('candidate')}")
                    continue
                if entry.get("verified_public_head") != expected["head"]:
                    errors.append(f"verified public HEAD mismatch: {entry.get('candidate')}")
                if entry.get("verified_public_tree") != expected["tree"]:
                    errors.append(f"verified public tree mismatch: {entry.get('candidate')}")
                run_ids = [run.get("id") for run in entry.get("ci", {}).get("runs", [])]
                if run_ids != expected["ci_runs"] or any(
                    run.get("conclusion") != "success" for run in entry.get("ci", {}).get("runs", [])
                ):
                    errors.append(f"verified public CI evidence mismatch: {entry.get('candidate')}")
                codeql = entry.get("codeql", {})
                if expected["codeql_analysis_id"] is None:
                    if codeql.get("status") != "N/A_NO_CODEQL_ANALYSIS" or "analysis_id" in codeql:
                        errors.append(f"CodeQL applicability mismatch: {entry.get('candidate')}")
                elif (
                    codeql.get("analysis_id") != expected["codeql_analysis_id"]
                    or codeql.get("status") != "PASS_ZERO_RESULTS_ZERO_OPEN_ALERTS"
                    or codeql.get("results_count") != 0
                    or codeql.get("open_alert_count") != 0
                ):
                    errors.append(f"verified CodeQL evidence mismatch: {entry.get('candidate')}")
        if repositories.get("open_review_matters") != release.get("open_review_matters"):
            errors.append("repository registry open-review status mismatch")
        if owner_status.get("open_review_matters") != release.get("open_review_matters"):
            errors.append("owner open-review status mismatch")
        master = planned[-1] if isinstance(planned, list) and planned else {}
        if master.get("verified_public_head") != "dee8a0466f446602c5de0923eb3700f20c6ca19f":
            errors.append("master public HEAD mismatch")
        if master.get("codeql", {}).get("status") != "N/A_NO_CODEQL_ANALYSIS":
            errors.append("master CodeQL applicability mismatch")
        if asset_inventory.get("asset_count") != 0 or asset_inventory.get("unresolved_asset_count") != 0:
            errors.append("zero-asset inventory mismatch")
    candidate_hash = release.get("public_candidate_sha256")
    if not isinstance(candidate_hash, str) or len(candidate_hash) != 64:
        errors.append("release candidate SHA-256 invalid")
    if release.get("public_commit_sha") != "624ea78912e67ebc536d0e270446a9ec77563f31":
        errors.append("verified profile public commit mismatch")
    if release.get("public_commit_tree_sha") != "ead9651a5c956b0dc02333218dc9ffe3da8889d3":
        errors.append("verified profile public tree mismatch")
    if release.get("ci_run_id") != 31692227539 or release.get("codeql_analysis_id") != 1612947444:
        errors.append("verified profile CI/CodeQL evidence mismatch")
    if release.get("codeql_results_count") != 0 or release.get("codeql_open_alert_count") != 0:
        errors.append("profile CodeQL zero evidence mismatch")
    if release.get("first_prospective_e4", {}).get("included_in_this_publication") is not False:
        errors.append("E4 must remain separate from this publication")
    runtime = release.get("runtime_scope", {})
    if any(runtime.get(key) is not False for key in (
        "real_payments_enabled", "token_delivery_enabled", "automatic_token_delivery_enabled",
        "refund_automation_enabled", "deployment_in_scope",
    )):
        errors.append("runtime scope must remain disabled")

    manifest_entries = manifest.get("files")
    if not isinstance(manifest_entries, list):
        errors.append("manifest files must be a list")
        manifest_entries = []
    listed_paths = [entry.get("path") for entry in manifest_entries if isinstance(entry, dict)]
    if listed_paths != sorted(listed_paths):
        errors.append("manifest paths are not canonical sorted paths")
    if len(listed_paths) != len(set(listed_paths)):
        errors.append("manifest contains duplicate paths")
    expected_paths = set(files) - {MANIFEST_PATH.name}
    if set(listed_paths) != expected_paths:
        errors.append("manifest closure does not equal candidate file set minus manifest")
    if manifest.get("included_file_count") != len(expected_paths):
        errors.append("manifest included-file count mismatch")
    for entry in manifest_entries:
        if not isinstance(entry, dict) or entry.get("path") not in files:
            continue
        payload = files[entry["path"]].read_bytes()
        if entry.get("size_bytes") != len(payload):
            errors.append(f"manifest size mismatch: {entry['path']}")
        if entry.get("sha256") != sha256(payload):
            errors.append(f"manifest SHA-256 mismatch: {entry['path']}")

    subprocess_result = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "secret_scan.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if subprocess_result.returncode != 0:
        errors.append("secret/local-path scan failed")

    workflow_text = "\n".join(
        (ROOT / relative).read_text(encoding="utf-8")
        for relative in (
            ".github/workflows/validate-profile.yml",
            ".github/workflows/codeql.yml",
        )
    )
    action_pattern = r"(?m)^\s*-?\s*uses" + ":" + r"\s*([^\s#]+)"
    action_uses = re.findall(action_pattern, workflow_text)
    if len(action_uses) != 5 or any(
        "@" not in action or not re.fullmatch(r"[0-9a-f]{40}", action.rsplit("@", 1)[1])
        for action in action_uses
    ):
        errors.append("CI actions must be exactly five full-SHA references")
    if "persist-credentials: false" not in workflow_text or "secrets." in workflow_text:
        errors.append("CI credential boundary mismatch")
    if "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb" not in workflow_text:
        errors.append("pinned Gitleaks archive checksum missing")

    forbidden_markers = (
        "private" + "-review",
        "private" + " review",
        "private" + " staging",
        "private" + "_staging",
        "ready_for_external_review_" + "private",
        "draft" + "_pr",
        "draft pull" + " request",
        "public_security_contact_" + "required",
        "license_review_" + "required",
        "owner_publication_approval_" + "required",
    )
    for relative, path in files.items():
        try:
            text = path.read_text(encoding="utf-8").casefold()
        except (OSError, UnicodeDecodeError):
            continue
        for marker in forbidden_markers:
            if marker.casefold() in text:
                errors.append(f"obsolete publication label: {relative}:{marker}")
        old_repository = "wotaniii/lumaquant-github-" + "profile(?!-public)"
        if re.search(old_repository, text):
            errors.append(f"obsolete repository target: {relative}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("CANDIDATE_VALIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
