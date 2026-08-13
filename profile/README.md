# LUMA Quant

LUMA Quant develops evidence-oriented analytical software, a wallet-oriented
utility portal and an engineering trust layer. The operator is Luma Quant e.U.;
brand LUMA Quant; founder Johann Weitzer; Austria. This identity is
owner-confirmed and not independently registry-verified.

## Public Trust Layer repositories

All seven Trust Layer repositories below are public in the verified owner
namespace `wotanIII`. Their point-in-time HEAD, tree, CI and CodeQL evidence is
recorded in [`PLANNED_PUBLIC_REPOSITORIES.json`](../PLANNED_PUBLIC_REPOSITORIES.json).

| Area | Public repository | Evidence class |
| --- | --- | --- |
| Engine | [luma-engine-evidence-public](https://github.com/wotanIII/luma-engine-evidence-public) | Versioned contracts, commitments and verifier evidence; E4 remains separately governed |
| Quant Lab | [luma-ai-frontend-public](https://github.com/wotanIII/luma-ai-frontend-public) | Sanitized production frontend source |
| Token portal | [luma-token-portal-public](https://github.com/wotanIII/luma-token-portal-public) | Read-only trust surface and source-bound, point-in-time token facts |
| Platform boundary | [luma-platform-api-public](https://github.com/wotanIII/luma-platform-api-public) | Source-bound API contract plus a bounded runnable reference adapter; not the production backend |
| Company | [luma-corporate-site-public](https://github.com/wotanIII/luma-corporate-site-public) | Corporate website and Trust Center source |
| GitHub profile | [lumaquant-github-profile-public](https://github.com/wotanIII/lumaquant-github-profile-public) | Documentation-only profile and navigation source |
| Trust Layer v1.0 | [luma-trust-layer-v1](https://github.com/wotanIII/luma-trust-layer-v1) | Master public source and evidence index |

Private engine, payment, signing, treasury, user-data, administrative and
deployment control planes remain intentionally excluded. The Token Portal
reference boundary keeps `REAL_PAYMENTS_DISABLED` and
`TOKEN_DELIVERY_DISABLED`.

## Live product surfaces

- [LUMA Quant Lab](https://ai.lumaquant.tech/)
- [LUMA Token Portal](https://token.lumaquant.tech/)
- [Corporate website](https://www.lumaquant.tech/)

Public source does not establish production parity. Each repository states its
own alignment and limitations.

## Claim discipline

We distinguish source-backed facts, time-bound on-chain observations,
operator-declared policy and limitations. We do not describe the overall Trust
Layer as independently audited, promise investment returns, call LUMA supply
fixed while mint authority remains active, or describe real payments or token
delivery as enabled when those execution rails are excluded.

The first prospective E4 commitment and reveal remains a separate,
`NOT_YET_COMPLETED` milestone.

## Security and review status

Report security concerns to `security@lumaquant.tech`. The operator confirms
that this mailbox is active, monitored and has passed a reception test.
Independent mailbox verification was not performed and no response-time SLA is
claimed. Legal review and an independent third-party audit remain
`NOT_YET_COMPLETED`.
