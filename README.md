# Cisco Network Operations Skill

Diagnose-first Cisco network operations guidance for AI agents. The skill helps review Cisco changes, troubleshoot operational artifacts, summarize incidents, and review network automation with explicit evidence, validation, and rollback.

The skill is offline/advisory by default. It analyzes artifacts the user provides: configs, diffs, CLI output, parsed telemetry, NMS alerts, topology notes, tickets, and automation code. It does not directly connect to routers, switches, firewalls, or controllers.

## Scope

Primary platforms:

- IOS XE
- NX-OS
- IOS XR

Secondary context:

- ASA/FTD
- ACI
- Catalyst Center
- Meraki
- Cisco SD-WAN

## Install

For local Codex development, point Codex at this repo as a plugin or copy/symlink `skills/cisco-network-ops` into a Codex-discoverable skills directory.

For local Claude Code development, install this repo as a plugin or copy/symlink `skills/cisco-network-ops` into a Claude-discoverable skills directory.

## Try It

Use prompts such as:

- "Use $cisco-network-ops to review this IOS XE trunk change for risk and rollback."
- "Use $cisco-network-ops to troubleshoot this BGP neighbor-down output."
- "Use $cisco-network-ops to review this Netmiko script before production rollout."
- "Use $cisco-network-ops to summarize this NOC incident from logs and show commands."

## Safety Model

- No autonomous production remediation.
- No direct device access in v1.
- Production-impacting advice must include assumptions, risk category, evidence, pre-checks, post-checks, rollback, and escalation notes.
- Config generation is draft text unless the user explicitly asks for it.

## Validate

```bash
python3 scripts/validate_skill.py
```

Smoke prompts live in `tests/smoke-test-prompts.md`.

