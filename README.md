# LUMA Quant GitHub profile candidate

Status: **PUBLICATION_REVIEW_READY / PUBLIC_REPOSITORY_PENDING**  
Publication performed: **NO**

This repository is the documentation-only candidate for the planned LUMA Quant
GitHub profile at
`https://github.com/wotanIII/lumaquant-github-profile-public`. GitHub repository
creation and URL verification remain `PENDING`; the URL is owner-approved
planning metadata, not a claim that the repository is already public.

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

## Planned public repository targets

`PLANNED_PUBLIC_REPOSITORIES.json` is authoritative for all seven targets. Every
target currently has repository creation `PENDING`, URL verification `PENDING`
and `publication_performed: false`. The current owner namespace is `wotanIII`;
no separate LUMA Quant GitHub organization is asserted.

## Public/private boundary

The candidate contains public-intent documentation and local validation tools.
It excludes product source, private repository history, engine logic, prompts,
customer or wallet data, credentials, deployment controls, signers, payment
logic and production configuration. See `PUBLIC_PRIVATE_BOUNDARY.md`.

## Build and verification

There is no runtime build and no third-party runtime dependency:

```text
python -B scripts/generate_sbom.py --check
python -B scripts/generate_metadata.py --check
python -B scripts/validate_candidate.py
python -B -m unittest discover -s tests -p "test_*.py"
```

Build the deterministic publication-review archive outside the candidate:

```text
python -B scripts/build_archive.py --output-dir ../archives
```

The validation workflow checks exact manifest closure, release and planned-link
metadata, boundary and generated-file rules, local secret patterns, unit tests,
deterministic SBOMs and a pinned Gitleaks scan. CodeQL is prepared for a public
repository but is not claimed as passed before its public-only job runs.

The company website is [www.lumaquant.tech](https://www.lumaquant.tech/).
Repository creation, publication, deployment and release creation are not
performed by this candidate preparation.
