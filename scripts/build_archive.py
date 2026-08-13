#!/usr/bin/env python3
"""Build a byte-reproducible ZIP and detached SHA-256 commitment."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_check(script: str) -> None:
    subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / script), "--check"]
        if script != "validate_candidate.py"
        else [sys.executable, "-B", str(ROOT / "scripts" / script)],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    run_check("generate_sbom.py")
    run_check("generate_metadata.py")
    run_check("validate_candidate.py")

    release = json.loads((ROOT / "RELEASE.json").read_text(encoding="utf-8"))
    release_name = "v" + release["public_release"]
    archive_name = f"lumaquant-github-profile-public-candidate-{release_name}.zip"
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / archive_name
    timestamp = datetime.fromisoformat(release["exported_at_utc"].replace("Z", "+00:00"))
    zip_time = (timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(
            (
                item
                for item in ROOT.rglob("*")
                if item.is_file() and ".git" not in item.relative_to(ROOT).parts
            ),
            key=lambda item: item.relative_to(ROOT).as_posix(),
        ):
            relative = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(relative, date_time=zip_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_path = archive_path.with_suffix(archive_path.suffix + ".sha256")
    checksum_path.write_text(f"{digest}  {archive_path.name}\n", encoding="ascii", newline="\n")
    print(f"ARCHIVE_SHA256={digest}")
    print(f"ARCHIVE_FILE_COUNT={len(zipfile.ZipFile(archive_path).namelist())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
