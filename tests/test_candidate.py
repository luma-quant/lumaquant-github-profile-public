from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProfileCandidateTests(unittest.TestCase):
    def test_release_is_publication_review_ready_without_publish_claim(self) -> None:
        release = json.loads((ROOT / "RELEASE.json").read_text(encoding="utf-8"))
        self.assertEqual("0.1.0-rc1", release["public_release"])
        self.assertEqual("REFERENCE_IMPLEMENTATION", release["release_class"])
        self.assertEqual("REFERENCE_ONLY", release["production_alignment"])
        self.assertEqual("PUBLIC_REPOSITORY_PENDING", release["visibility_status"])
        self.assertEqual("PENDING", release["repository_creation_status"])
        self.assertFalse(release["publication_performed"])
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
            release["publication_blockers"],
        )

    def test_all_seven_repository_targets_are_pending_and_not_published(self) -> None:
        plan = json.loads((ROOT / "PLANNED_PUBLIC_REPOSITORIES.json").read_text(encoding="utf-8"))
        self.assertEqual("wotanIII", plan["account_owner"])
        self.assertEqual("NO_SEPARATE_GITHUB_ORGANIZATION_CONFIRMED", plan["organization_status"])
        self.assertEqual(7, len(plan["repositories"]))
        for entry in plan["repositories"]:
            self.assertTrue(entry["url"].startswith("https://github.com/wotanIII/"))
            self.assertEqual("PENDING", entry["repository_creation_status"])
            self.assertEqual("PENDING", entry["url_verification_status"])
            self.assertFalse(entry["publication_performed"])

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
