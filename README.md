# LUMA Quant GitHub profile

Status: **PUBLIC_REPOSITORY_VERIFIED**
Publication performed: **YES**

This documentation-only repository is public at
[wotanIII/lumaquant-github-profile-public](https://github.com/wotanIII/lumaquant-github-profile-public).
The initial public root `624ea78912e67ebc536d0e270446a9ec77563f31`,
its public CI and its CodeQL analysis were verified on 13 August 2026. The
repository lives in the owner account `wotanIII`; no separate LUMA Quant GitHub
organization is asserted.

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
repositories. It records their exact verified URLs, audited public HEADs and
trees, successful CI runs and CodeQL evidence. The Master index correctly uses
`N/A_NO_CODEQL_ANALYSIS`: it contains an index verifier and Gitleaks, but no
CodeQL workflow.

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
