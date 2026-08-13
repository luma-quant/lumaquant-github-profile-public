# Known limitations

- The public namespace is the verified GitHub organization `luma-quant`. The
  former personal-namespace URLs under `wotanIII` remain historical facts and
  redirect to the canonical organization URLs.
- The seven repository records are a point-in-time transfer snapshot. A later
  status-only commit does not invalidate the recorded audited pre-rebind HEAD;
  the Master is not cyclically bound to a future status commit.
- Manifested text bytes are canonical LF bytes under `.gitattributes`; this is
  part of the reproducibility boundary.
- This is a documentation reference repository, not a production source mirror.
- Legal review and independent third-party audit are `NOT_YET_COMPLETED`.
- Operator identity, asset rights and mailbox status are owner-confirmed, not
  independently verified.
- The Master index has no CodeQL workflow; its correct status is
  `N/A_NO_CODEQL_ANALYSIS`, while its index-verifier and Gitleaks jobs passed.
- Engine Evidence E4 is separately governed and remains `NOT_YET_COMPLETED`.
- The Token Portal reference boundary disables real payments and token delivery.
- No deployment, DNS change, tag or GitHub Release is claimed by this status
  alignment.
