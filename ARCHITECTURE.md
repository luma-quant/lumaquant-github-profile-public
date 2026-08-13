# Architecture

## Rendering path

```text
profile/README.md
        |
        v
future GitHub organization profile renderer
        |
        v
repository index and external product links
```

The rendered document is static. It has no API client, authentication state,
storage, analytics, wallet interaction, payment capability or deployment
automation.

## Evidence path

`RELEASE.json` classifies the artifact and binds a canonical candidate digest.
`PUBLIC_SOURCE_MANIFEST.json` binds every file except the manifest itself.
CycloneDX and SPDX documents record that the package has zero third-party
runtime components. Local validators and pinned CI reproduce these checks.

No architectural statement in this candidate establishes production parity for
any linked product repository.

