# Security Policy

## Reporting a vulnerability

If you believe you've found a security issue in Spwig — the core platform, an
official theme, an official integration, or one of the SDKs — please report it
privately.

**Email:** security@spwig.com

Please do **not** open a public GitHub issue for security reports.

Include enough detail for us to reproduce the issue:

- Affected repo(s) and version(s)
- Reproduction steps or proof-of-concept
- Expected vs. actual behaviour
- Any log excerpts, screenshots, or scripts that help
- Your assessment of the impact
- Whether you'd like credit in the disclosure

If your report involves a live installation on Spwig-hosted infrastructure
(e.g. a merchant on `*.myspwig.com`), please make that clear so we can
coordinate patching there in parallel with the OSS fix.

## What to expect from us

- **Acknowledgement within 48 hours** of your report (typically much faster)
- **Initial triage within 5 business days** — we'll confirm the issue,
  ask any clarifying questions, and give you a rough severity assessment
- **Coordinated disclosure timeline** — we aim to ship a patched release
  within 90 days of confirmation for most issues; critical issues we treat as
  a drop-everything priority. We'll agree the exact timeline with you.
- **Public credit** in the release notes and CVE (if applicable), unless you
  ask to remain anonymous
- **A bounty if the impact warrants it** — we don't run a formal bug bounty
  programme yet, but we may pay a discretionary reward for high-impact
  findings. Contact us for the current policy.

## Scope

**In scope:**
- `Spwig/commerce` — the core Django platform (this repo)
- `Spwig/components` — themes, admin utilities, provider integrations
- `Spwig/theme-sdk`, `Spwig/headless-sdk`, `Spwig/react`, `Spwig/provider-sdks`
- Any Spwig-hosted service reachable at `*.spwig.com` (`geoip.spwig.com`,
  `geocoder.spwig.com`, `updates.spwig.com`, `push.spwig.com`,
  `sso.spwig.com`, and any live subdomain merchants can hit)
- The Spwig-hosted merchant fleet at `*.myspwig.com`

**Out of scope:**
- Denial-of-service attacks against Spwig-hosted infrastructure
- Reports from automated scanners without a working proof-of-concept
- Third-party components we depend on (e.g. Django itself, PostgreSQL, Redis) —
  please report those upstream. If a Spwig-specific misconfiguration
  makes an upstream issue exploitable, that's in scope.
- Merchant-specific configuration issues (e.g. a merchant using weak passwords)

## Safe-harbour

If you make a good-faith effort to comply with this policy, we will not
pursue legal action against you or ask law enforcement to investigate you.
Good faith means:

- You gave us a reasonable window to respond before disclosing publicly
- You only accessed data or systems as much as needed to demonstrate the issue
- You didn't degrade the service or exfiltrate data beyond what's needed to prove impact
- You didn't extort us or a merchant using the finding

## Supported versions

We patch security issues on the current stable release and one release back.
Older releases receive security patches only for critical issues on a
best-effort basis.

## PGP

If you'd like to encrypt your report, ask via email first and we'll share a
current PGP key.
