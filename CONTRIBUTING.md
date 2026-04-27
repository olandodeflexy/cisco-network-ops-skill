# Contributing

This repo is executable documentation for AI agents. Optimize for retrieval and safe network operations, not human tutorial prose.

## Development Rules

- Keep `skills/cisco-network-ops/SKILL.md` under 300 lines.
- Put detailed examples in `references/*.md`.
- Use decision tables before long procedures.
- Label read-only vs state-changing commands where relevant.
- Preserve the offline/advisory default.
- Do not imply official Cisco or TAC authority.
- Do not add direct production write automation in v1.

## Validation

Run:

```bash
python3 scripts/validate_skill.py
```

## Review Checklist

- Platform differences are explicit.
- Unsafe changes include pre-checks, post-checks, rollback, and abort criteria.
- Commands are not copied across IOS XE, NX-OS, and IOS XR without qualification.
- Secrets are redacted and not repeated.
- References are retrieval-first and avoid bloated prose.
- Baseline or smoke prompts cover any new behavior.

