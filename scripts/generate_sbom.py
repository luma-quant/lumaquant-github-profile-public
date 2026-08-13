#!/usr/bin/env python3
"""Generate deterministic zero-third-party-component SBOM documents."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_PATH = ROOT / "RELEASE.json"
CYCLONEDX_PATH = ROOT / "SBOM.cdx.json"
SPDX_PATH = ROOT / "SBOM.spdx.json"
TOOL_NAME = "luma-profile-sbom-generator"
TOOL_VERSION = "1.0.0"


def canonical_json(data: object) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def documents() -> dict[Path, bytes]:
    release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
    repository = release["repository"]
    repository_url = release["repository_url"]
    version = release["public_release"]
    timestamp = release["exported_at_utc"]
    identity = f"{repository}@{version}"
    serial = uuid.uuid5(uuid.NAMESPACE_URL, identity)

    cyclonedx = {
        "bomFormat": "CycloneDX",
        "components": [],
        "dependencies": [],
        "metadata": {
            "component": {
                "copyright": "Copyright 2026 Luma Quant e.U. All rights reserved.",
                "licenses": [{"license": {"id": "LicenseRef-LumaQuant-Proprietary"}}],
                "name": "lumaquant-github-profile",
                "externalReferences": [{"type": "vcs", "url": repository_url}],
                "properties": [
                    {"name": "luma:artifact_type", "value": release["artifact_type"]},
                    {"name": "luma:third_party_runtime_component_count", "value": "0"},
                ],
                "type": "application",
                "version": version,
            },
            "timestamp": timestamp,
            "tools": {
                "components": [
                    {"name": TOOL_NAME, "type": "application", "version": TOOL_VERSION}
                ]
            },
        },
        "serialNumber": f"urn:uuid:{serial}",
        "specVersion": "1.6",
        "version": 1,
    }

    package_spdx_id = "SPDXRef-Package-lumaquant-github-profile"
    spdx = {
        "SPDXID": "SPDXRef-DOCUMENT",
        "creationInfo": {
            "created": timestamp,
            "creators": [f"Tool: {TOOL_NAME}-{TOOL_VERSION}"],
        },
        "dataLicense": "CC0-1.0",
        "documentNamespace": f"urn:uuid:{serial}",
        "name": f"lumaquant-github-profile-{version}",
        "packages": [
            {
                "SPDXID": package_spdx_id,
                "copyrightText": "Copyright 2026 Luma Quant e.U. All rights reserved.",
                "downloadLocation": repository_url,
                "filesAnalyzed": False,
                "licenseConcluded": "LicenseRef-LumaQuant-Proprietary",
                "licenseDeclared": "LicenseRef-LumaQuant-Proprietary",
                "name": "lumaquant-github-profile",
                "primaryPackagePurpose": "APPLICATION",
                "supplier": "Organization: Luma Quant e.U.",
                "versionInfo": version,
            }
        ],
        "relationships": [
            {
                "relatedSpdxElement": package_spdx_id,
                "relationshipType": "DESCRIBES",
                "spdxElementId": "SPDXRef-DOCUMENT",
            }
        ],
        "spdxVersion": "SPDX-2.3",
    }
    return {
        CYCLONEDX_PATH: canonical_json(cyclonedx),
        SPDX_PATH: canonical_json(spdx),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail instead of writing")
    args = parser.parse_args()
    failures: list[str] = []
    for path, expected in documents().items():
        if args.check:
            if not path.is_file() or path.read_bytes() != expected:
                failures.append(path.name)
        else:
            path.write_bytes(expected)
    if failures:
        print("SBOM_OUT_OF_DATE: " + ", ".join(sorted(failures)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
