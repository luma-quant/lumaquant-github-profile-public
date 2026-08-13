# LUMA Quant GitHub profile

Status: **PUBLIC_REPOSITORY_VERIFIED**
Publication performed: **YES**

This documentation-only repository is public at
[luma-quant/lumaquant-github-profile-public](https://github.com/luma-quant/lumaquant-github-profile-public).
The registry now binds the final current organization-rebound public heads for
Engine, AI, Token, API and Corporate. For this self-describing Profile, it
records the last completed predecessor
`b9f649dc8d7b2c594815c31ea646b96aefbab1a2` and tree
`c23ff252b5413a82a75ea96240285715cb2bf0b7`, together with its successful CI
and zero-result CodeQL analysis. That record is observed predecessor evidence,
not a self-referential claim about the current commit. All seven Trust Layer
repositories are in the verified `luma-quant` GitHub organization. Their former
`wotanIII` URLs redirect to the canonical organization URLs; the transfer
itself changed neither content nor history.

## Scope and evidence class

- **Operator:** Luma Quant e.U.; brand LUMA Quant; founder Johann Weitzer;
  Austria. Owner-confirmed, not independently registry-verified.
- **Product represented:** GitHub landing-page copy and a repository index; no
  product runtime.
- **Release class:** `REFERENCE_IMPLEMENTATION` / `REFERENCE_ONLY`.
- **Deployment:** `NOT_DEPLOYED`; this package has no associated live domain.
- **License:** `PROPRIETARY_SOURCE_AVAILABLE_ALL_RIGHTS_RESERVED`.
- **Assets:** zero included binary/media assets; unresolved assets excluded.
- **Security contact:** `security@lumaquant.tech`, owner-confirmed active,
  monitored and test-received; independent mailbox verification not performed;
  no response-time SLA.
- **Open review matters:** only legal review and independent third-party audit.

## Verified public repository index

[`PLANNED_PUBLIC_REPOSITORIES.json`](PLANNED_PUBLIC_REPOSITORIES.json) is the
authoritative point-in-time registry for all seven public Trust Layer
repositories. It records exact verified URLs, the five final current component
HEADs and trees, successful CI runs and CodeQL evidence. The Profile entry is
explicitly the last completed predecessor observed before this status commit,
not a current self-binding. The Master index correctly uses
`N/A_NO_CODEQL_ANALYSIS`: it contains an index verifier and Gitleaks, but no
CodeQL workflow. The Master remains deliberately bound to transferred
pre-rebind HEAD `a8b2cbe1c9e32d5ebdff8cfcba435d7ca9304e1b` until its separately governed
rebuild.

The first prospective E4 commitment and reveal remains separate and
`NOT_YET_COMPLETED`. This publication does not enable real payments, token
delivery, refund automation or deployment.

## Public/private boundary

This repository contains public documentation and local validation tools. It
excludes product source, private history, engine logic, prompts, customer or
wallet data, credentials, deployment controls, signers, payment logic and
production configuration. See [PUBLIC_PRIVATE_BOUNDARY.md](PUBLIC_PRIVATE_BOUNDARY.md).

## Build and verification

There is no runtime build and no third-party runtime dependency:

```text
python -B scripts/generate_sbom.py --check
python -B scripts/generate_metadata.py --check
python -B scripts/validate_candidate.py
python -B -m unittest discover -s tests -p "test_*.py"
```

The workflow checks exact manifest closure, status metadata, generated-file
rules, public-boundary conditions, deterministic SBOMs, pinned action
references, Gitleaks and CodeQL. Source availability remains governed by
[LICENSE.md](LICENSE.md); public visibility grants no general reuse right.

The company website is [www.lumaquant.tech](https://www.lumaquant.tech/).
Legal review and an independent third-party audit remain
`NOT_YET_COMPLETED`; neither is claimed complete.
