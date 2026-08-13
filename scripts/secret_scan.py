#!/usr/bin/env python3
"""Run a conservative high-confidence secret and local-path scan."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".json", ".md", ".py", ".toml", ".txt", ".yml", ".yaml"}


def rules() -> dict[str, re.Pattern[str]]:
    private_header = "BEGIN " + "PRIVATE KEY"
    stripe_live = "sk" + "_live_"
    github_pat = "gh" + "p_"
    aws_access = "AK" + "IA"
    return {
        "private-key-header": re.compile(re.escape(private_header)),
        "stripe-live-secret": re.compile(re.escape(stripe_live) + r"[A-Za-z0-9]{16,}"),
        "github-personal-token": re.compile(re.escape(github_pat) + r"[A-Za-z0-9]{20,}"),
        "aws-access-key": re.compile(re.escape(aws_access) + r"[A-Z0-9]{16}"),
        "assigned-secret": re.compile(
            r"(?i)(?:api[_-]?key|client[_-]?secret|private[_-]?key|password)\s*[:=]\s*[\"'][^\"']{12,}[\"']"
        ),
    }


def local_path_rules() -> dict[str, re.Pattern[str]]:
    slash = "\\"
    drive_prefix = "[A-Za-z]" + ":" + re.escape(slash)
    unix_user_root = "/" + "Users" + "/|/" + "home" + "/"
    return {
        "windows-absolute-path": re.compile(drive_prefix),
        "user-home-absolute-path": re.compile(unix_user_root),
    }


def scan() -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    scanners = {**rules(), **local_path_rules()}
    for path in sorted(ROOT.rglob("*")):
        if (
            not path.is_file()
            or ".git" in path.relative_to(ROOT).parts
            or path.suffix.lower() not in TEXT_SUFFIXES
        ):
            continue
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for rule_id, pattern in scanners.items():
            if pattern.search(text):
                findings.append((rule_id, relative))
    return findings


def main() -> int:
    findings = scan()
    if findings:
        for rule_id, path in findings:
            print(f"{rule_id}: {path}", file=sys.stderr)
        return 1
    print("SECRET_AND_LOCAL_PATH_SCAN_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
