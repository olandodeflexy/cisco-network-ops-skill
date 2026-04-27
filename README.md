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

### Codex

Add this repository as a Codex plugin marketplace:

```bash
codex plugin marketplace add olandodeflexy/cisco-network-ops-skill
```

For local development from a checkout, symlink the skill directly:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/cisco-network-ops" ~/.codex/skills/cisco-network-ops
```

### Claude Code

Add this repository as a Claude Code marketplace, then install the plugin:

```bash
claude plugin marketplace add olandodeflexy/cisco-network-ops-skill
claude plugin install cisco-network-ops-skill@cisco-network-ops-skill
```

For one-off local testing from a checkout:

```bash
claude -p --plugin-dir "$(pwd)" 'Use $cisco-network-ops to review this Cisco change for risk and rollback.'
```

## Metadata Notes

The Codex manifest includes `skills` and rich `interface` metadata because Codex reads those fields for plugin discovery and UI presentation.

The Claude plugin manifest stays minimal because Claude Code discovers skills from the plugin `skills/` directory convention and validates the current manifest without a Codex-style `interface` block.

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
