# Security Policy

## Reporting

Report unsafe recommendation patterns, missed redaction, or accidental credential exposure by opening a private security advisory on GitHub when available.

If the issue is not sensitive, open a public issue with:

- The prompt or artifact shape that triggered the problem.
- The unsafe output or missing redaction behavior.
- The platform context, with secrets removed.
- The expected safer behavior.

Do not include real credentials, SNMP communities, private keys, TACACS/RADIUS secrets, production configs with secrets, or customer-identifying data.

## Scope

Security reports for this repository should focus on:

- Skill behavior that recommends unsafe Cisco network operations.
- Failure to gate direct production writes.
- Failure to redact or avoid repeating secrets.
- Packaging or validation issues that could ship stale or inconsistent skill content.
