#!/usr/bin/env python3
"""Generate deterministic release commitment and exact all-file manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_PATH = ROOT / "RELEASE.json"
MANIFEST_PATH = ROOT / "PUBLIC_SOURCE_MANIFEST.json"
TOOL_VERSION = "1.0.0"
PRODUCT_DIGEST_EXCLUSIONS = {"PUBLIC_SOURCE_MANIFEST.json", "RELEASE.json"}


def canonical_json(data: object) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def files_except_manifest() -> list[Path]:
    return sorted(
        (
            path
            for path in ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.relative_to(ROOT).parts
            and path.relative_to(ROOT).as_posix() != MANIFEST_PATH.name
        ),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def candidate_product_digest() -> str:
    digest = hashlib.sha256()
    for path in files_except_manifest():
        relative = path.relative_to(ROOT).as_posix()
        if relative in PRODUCT_DIGEST_EXCLUSIONS:
            continue
        payload = path.read_bytes()
        record = f"{relative}\0{len(payload)}\0{digest_bytes(payload)}\n".encode("utf-8")
        digest.update(record)
    return digest.hexdigest()


def expected_documents() -> tuple[bytes, bytes]:
    release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
    release["public_candidate_sha256"] = candidate_product_digest()
    release_bytes = canonical_json(release)

    entries = []
    for path in files_except_manifest():
        relative = path.relative_to(ROOT).as_posix()
        payload = release_bytes if relative == RELEASE_PATH.name else path.read_bytes()
        entries.append(
            {
                "path": relative,
                "sha256": digest_bytes(payload),
                "size_bytes": len(payload),
            }
        )

    manifest = {
        "excluded_category_summary": [
            "credentials and signing material",
            "customer, wallet, payment and transaction data",
            "private repository history and product source",
            "engine logic, prompts and deployment controls",
            "unsupported assets and audit or legal claims",
        ],
        "export_timestamp_utc": release["exported_at_utc"],
        "export_tool_version": TOOL_VERSION,
        "files": entries,
        "included_file_count": len(entries),
        "license_status": release["license_status"],
        "production_alignment": release["production_alignment"],
        "public_release": release["public_release"],
        "release_class": release["release_class"],
        "repository": release["repository"],
        "repository_url": release["repository_url"],
        "repository_creation_status": release["repository_creation_status"],
        "publication_status": release["publication_status"],
        "publication_performed": release["publication_performed"],
        "owner_gate_status": {
            "operator_identity": release["operator_identity_status"],
            "license": release["license_status"],
            "asset_rights": release["asset_rights_status"],
            "security_contact": release["security_contact_status"],
            "open_review_matters": release["publication_blockers"],
        },
        "schema_version": "1.0.0",
        "source_private_commit_sha": release["source_private_commit_sha"],
    }
    return release_bytes, canonical_json(manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail instead of writing")
    args = parser.parse_args()
    release_bytes, manifest_bytes = expected_documents()
    expected = {RELEASE_PATH: release_bytes, MANIFEST_PATH: manifest_bytes}
    failures: list[str] = []
    for path, payload in expected.items():
        if args.check:
            if not path.is_file() or path.read_bytes() != payload:
                failures.append(path.name)
        else:
            path.write_bytes(payload)
    if failures:
        print("METADATA_OUT_OF_DATE: " + ", ".join(sorted(failures)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
