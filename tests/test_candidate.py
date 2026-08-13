from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProfileCandidateTests(unittest.TestCase):
    def test_release_records_verified_publication_without_runtime_claims(self) -> None:
        release = json.loads((ROOT / "RELEASE.json").read_text(encoding="utf-8"))
        self.assertEqual("0.1.0-rc1", release["public_release"])
        self.assertEqual("REFERENCE_IMPLEMENTATION", release["release_class"])
        self.assertEqual("REFERENCE_ONLY", release["production_alignment"])
        self.assertEqual("PUBLIC", release["visibility_status"])
        self.assertEqual("COMPLETED", release["repository_creation_status"])
        self.assertTrue(release["publication_performed"])
        self.assertEqual("PUBLIC_REPOSITORY_VERIFIED", release["publication_status"])
        self.assertEqual("817c6a65eb1ebee78acacf4c3a516aa2fd25c6d6", release["public_commit_sha"])
        self.assertEqual(31707575973, release["ci_run_id"])
        self.assertEqual(1613882333, release["codeql_analysis_id"])
        self.assertEqual("luma-quant", release["github_namespace"]["canonical_owner"])
        self.assertFalse(release["github_namespace"]["content_changed_by_transfer"])
        self.assertEqual(
            "624ea78912e67ebc536d0e270446a9ec77563f31",
            release["initial_publication_root"]["head"],
        )
        self.assertEqual(0, release["codeql_results_count"])
        self.assertEqual(0, release["codeql_open_alert_count"])
        self.assertEqual("COMPLETED_OWNER_CONFIRMED", release["operator_identity_status"])
        self.assertEqual("Luma Quant e.U.", release["operator_identity"]["legal_operator"])
        self.assertEqual(
            "PROPRIETARY_SOURCE_AVAILABLE_ALL_RIGHTS_RESERVED",
            release["license_status"],
        )
        self.assertEqual("security@lumaquant.tech", release["security_contact"])
        self.assertEqual(
            [
                "LEGAL_REVIEW_NOT_YET_COMPLETED",
                "INDEPENDENT_THIRD_PARTY_AUDIT_NOT_YET_COMPLETED",
            ],
            release["open_review_matters"],
        )

    def test_all_seven_repository_targets_are_public_and_verified(self) -> None:
        plan = json.loads((ROOT / "PLANNED_PUBLIC_REPOSITORIES.json").read_text(encoding="utf-8"))
        self.assertEqual("luma-quant", plan["account_owner"])
        self.assertEqual("ORGANIZATION", plan["account_type"])
        self.assertEqual(316678262, plan["organization_id"])
        self.assertEqual("VERIFIED_CREATED_AND_TRANSFER_COMPLETE", plan["organization_status"])
        self.assertEqual("wotanIII", plan["namespace_transfer"]["former_owner"])
        self.assertFalse(plan["namespace_transfer"]["content_changed_by_transfer"])
        self.assertEqual(7, len(plan["repositories"]))
        for entry in plan["repositories"]:
            self.assertTrue(entry["url"].startswith("https://github.com/luma-quant/"))
            self.assertEqual("COMPLETED", entry["repository_creation_status"])
            self.assertEqual("VERIFIED", entry["url_verification_status"])
            self.assertTrue(entry["publication_performed"])
            self.assertEqual("PUBLIC", entry["visibility"])
            self.assertEqual("main", entry["default_branch"])
            self.assertEqual("PASS_AT_VERIFIED_PUBLIC_HEAD", entry["ci"]["status"])
        self.assertEqual(
            "a8b2cbe1c9e32d5ebdff8cfcba435d7ca9304e1b",
            plan["repositories"][-1]["verified_public_head"],
        )
        self.assertEqual("N/A_NO_CODEQL_ANALYSIS", plan["repositories"][-1]["codeql"]["status"])

    def test_current_public_heads_and_evidence_are_exact(self) -> None:
        plan = json.loads((ROOT / "PLANNED_PUBLIC_REPOSITORIES.json").read_text(encoding="utf-8"))
        expected = {
            "engine-evidence": ("03516148a5a2345c0bf967598c65194e5c5ea401", 31703977937, 1613639143),
            "ai-frontend": ("f9192d49d11701c5b1e92efcd7b614922a4dc595", 31704278130, 1613660523),
            "token-portal": ("b26bb211ec1c063e7fa2cdd36d0f085f01f3301a", 31704480279, 1613670899),
            "platform-api": ("44b9b15d1dbd2e70e3c4db8764f10bbae14c608c", 31705801892, 1613761037),
            "corporate-site": ("49ed20aae24b1832081a89f37eeb1007b1c72816", 31706078911, 1613778562),
            "github-profile": ("817c6a65eb1ebee78acacf4c3a516aa2fd25c6d6", 31707575973, 1613882333),
            "trust-layer-master": ("a8b2cbe1c9e32d5ebdff8cfcba435d7ca9304e1b", 31710806734, None),
        }
        for entry in plan["repositories"]:
            head, first_ci, analysis = expected[entry["candidate"]]
            self.assertEqual(head, entry["verified_public_head"])
            self.assertEqual(first_ci, entry["ci"]["runs"][0]["id"])
            if analysis is None:
                self.assertEqual("N/A_NO_CODEQL_ANALYSIS", entry["codeql"]["status"])
            else:
                self.assertEqual(analysis, entry["codeql"]["analysis_id"])
                self.assertEqual(0, entry["codeql"]["results_count"])
                self.assertEqual(0, entry["codeql"]["open_alert_count"])

    def test_manifested_files_use_canonical_lf_bytes(self) -> None:
        self.assertEqual(b"* text=auto eol=lf\n", (ROOT / ".gitattributes").read_bytes())
        for path in ROOT.rglob("*"):
            if path.is_file() and ".git" not in path.relative_to(ROOT).parts:
                self.assertNotIn(b"\r\n", path.read_bytes(), path.relative_to(ROOT).as_posix())

    def test_profile_claims_are_bounded_and_security_contact_is_owner_confirmed(self) -> None:
        profile = (ROOT / "profile" / "README.md").read_text(encoding="utf-8")
        self.assertIn("Source-bound API contract", profile)
        self.assertIn("bounded runnable reference adapter", profile)
        self.assertIn("not the production backend", profile)
        self.assertIn("security@lumaquant.tech", profile)
        self.assertIn("Independent mailbox verification was not performed", profile)
        self.assertIn("REAL_PAYMENTS_DISABLED", profile)
        self.assertIn("TOKEN_DELIVERY_DISABLED", profile)

    def test_candidate_has_zero_assets_and_no_unresolved_rights(self) -> None:
        inventory = json.loads((ROOT / "ASSET_RIGHTS_INVENTORY.json").read_text(encoding="utf-8"))
        self.assertEqual(0, inventory["asset_count"])
        self.assertEqual(0, inventory["unresolved_asset_count"])
        self.assertEqual([], inventory["assets"])

    def test_sboms_bind_the_canonical_organization_repository(self) -> None:
        cyclonedx = json.loads((ROOT / "SBOM.cdx.json").read_text(encoding="utf-8"))
        spdx = json.loads((ROOT / "SBOM.spdx.json").read_text(encoding="utf-8"))
        expected_url = "https://github.com/luma-quant/lumaquant-github-profile-public"
        self.assertEqual(
            expected_url,
            cyclonedx["metadata"]["component"]["externalReferences"][0]["url"],
        )
        self.assertEqual(expected_url, spdx["packages"][0]["downloadLocation"])

    def test_candidate_validator(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "validate_candidate.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
