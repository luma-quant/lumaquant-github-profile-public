# Public/private boundary

## Included by explicit allowlist

- organization-profile copy,
- repository-purpose and evidence-class descriptions,
- public product-domain links,
- claim-discipline and disclosure guidance,
- release and publication-gate metadata,
- deterministic manifests and zero-dependency SBOMs,
- local validators, tests and pinned CI definitions.

## Intentionally excluded

- private repository content or history,
- product runtime source,
- engine algorithms, prompts or scoring logic,
- customer, user, wallet, payment or transaction data,
- keys, tokens, credentials, signers or seed phrases,
- internal endpoints and production configuration,
- administration, treasury, antifraud and deployment controls,
- unsupported asset, audit, legal or investment claims.

The export must fail if a symlink, denied generated file, local absolute path or
unmanifested file is introduced.

The candidate contains zero binary/media assets. Its fail-closed inventory has
zero unresolved entries. Operator identity, license and security contact are
owner-confirmed; legal review and independent third-party audit remain open.
