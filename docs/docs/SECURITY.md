# Security Policy

## Reporting Vulnerabilities
If you discover a security vulnerability, please do **not** open a public issue. Email us directly at `security@cognisync.ai`. We will respond within 48 hours.

## Security Controls
- **API Keys:** Never hardcode secrets. All contributions are scanned for leaked secrets using `gitleaks` in our CI pipeline.
- **Data Privacy:** PRs must NOT introduce logging of document content or PII (Personally Identifiable Information).
- **Dependency Audits:** We run `npm audit` and `safety` (Python) on every deployment.
- **RBAC:** Any changes to the authorization layer require a specific "Security Review" flag from a core maintainer.