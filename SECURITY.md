# Security Policy

## Supported versions

ComponentOS is currently pre-1.0. Security fixes are made against the latest commit on `main`; older releases are not currently supported.

## Reporting a vulnerability

Please do **not** open a public issue for a suspected security vulnerability. Report it privately through [GitHub's private vulnerability reporting](https://github.com/IceCheetah9418/componentOS/security/advisories/new) when available.

If private reporting is unavailable, contact the repository owner through their GitHub profile and include `ComponentOS security report` in the subject. Please include:

- a clear description of the vulnerability and its impact;
- affected files, endpoints, versions, or commits;
- reproducible steps or a proof of concept;
- any suggested mitigation.

Please redact API keys, tokens, device credentials, personal data, and private hardware information before sending a report.

## What to expect

You should receive an acknowledgement within 7 days. We will investigate, keep the reporter informed when practical, and coordinate disclosure after a fix or mitigation is available. Please allow reasonable time for a fix before public disclosure.

## Scope notes

Generated firmware and third-party model providers are part of the deployment chain. Do not send secrets or sensitive device data to a cloud provider. Passing the AST validator does not guarantee that generated code is secure or safe for a physical system; review and test generated code independently.
