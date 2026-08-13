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
        "repository_creation_status": "PENDING",
        "public_release": "0.1.0-rc1",
        "live_domain": None,
        "artifact_type": "DOCUMENTATION_PROFILE_CANDIDATE",
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
        "publication_review_status": "PUBLICATION_REVIEW_READY",
        "publication_status": "PUBLIC_REPOSITORY_PENDING",
        "publication_performed": False,
        "visibility_status": "PUBLIC_REPOSITORY_PENDING",
    }
    for key, value in expected_release.items():
        if release.get(key) != value:
            errors.append(f"release field mismatch: {key}")
    if release.get("publication_blockers") != [
        "LEGAL_REVIEW_NOT_YET_COMPLETED",
        "INDEPENDENT_THIRD_PARTY_AUDIT_NOT_YET_COMPLETED",
    ]:
        errors.append("release publication blockers mismatch")

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
            entry.get("repository_creation_status") != "PENDING"
            or entry.get("url_verification_status") != "PENDING"
            or entry.get("publication_performed") is not False
            for entry in planned
        ):
            errors.append("planned public repository status mismatch")
        if owner_status.get("open_review_matters") != release.get("publication_blockers"):
            errors.append("owner open-review status mismatch")
        if asset_inventory.get("asset_count") != 0 or asset_inventory.get("unresolved_asset_count") != 0:
            errors.append("zero-asset inventory mismatch")
    candidate_hash = release.get("public_candidate_sha256")
    if not isinstance(candidate_hash, str) or len(candidate_hash) != 64:
        errors.append("release candidate SHA-256 invalid")

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
