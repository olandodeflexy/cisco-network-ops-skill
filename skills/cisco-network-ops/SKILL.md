---
name: cisco-network-ops
description: Use when reviewing Cisco network changes, incidents, configs, logs, or automation for risk, evidence, validation, and rollback.
license: Apache-2.0
metadata:
  author: Cisco Network Operations Skill contributors
  version: 0.1.0
---

# Cisco Network Operations

Diagnose-first guidance for Cisco network operations. Use offline artifacts first: configs, diffs, CLI output, parsed telemetry, NMS alerts, topology notes, tickets, and automation code.

This skill is advisory by default. It does not assume direct access to routers, switches, firewalls, controllers, or production networks.

Reference files live under `references/` relative to this `SKILL.md`; load them from the skill directory, not from the caller's current working directory.

## Response Contract

For safety-critical Cisco network operations responses, include:

1. **Assumptions** - platform, OS version if known, topology role, environment criticality, access path, and missing context.
2. **Risk category** - one or more categories from the diagnose table.
3. **Evidence** - exact config, diff, log, command output, alert, or automation behavior used.
4. **Recommendation** - next diagnostic step or remediation, with tradeoffs.
5. **Pre-checks** - read-only commands, backups, neighbor state, interface state, route/policy evidence.
6. **Execution guidance** - ordered steps or draft config only when appropriate.
7. **Post-checks** - verification commands, parsed checks, telemetry, or before/after comparisons.
8. **Rollback** - inverse config, checkpoint/restore path, abort criteria, and retained evidence.
9. **Escalation notes** - when to involve TAC/vendor/internal escalation and what data to collect.

Small factual answers may compress the contract. Production-impacting advice must keep the full shape.

## Workflow

1. Capture context: platform, OS version, device role, topology, maintenance window, criticality, change intent, and available artifacts.
2. Classify the failure mode using the diagnose table.
3. Load only the reference files matching the category.
4. Separate evidence from inference. State when a conclusion is unproven.
5. Prefer read-only diagnostics before any configuration.
6. For state-changing work, produce pre-checks, execution steps, post-checks, rollback, and abort criteria.
7. Validate with lab, parser, pyATS/Genie, Batfish, lint, or staged post-checks where applicable.
8. Emit the Response Contract. For an end-to-end pattern, see [Example Response](references/example-response.md).

## Diagnose Before You Generate

| Failure category | Symptoms | Primary references |
| --- | --- | --- |
| **Change blast radius** | Large target set, unclear affected devices, no window, no rollback, no pre/post evidence | [Change Safety](references/change-safety.md), [Testing and Validation](references/testing-and-validation.md) |
| **Platform mismatch** | IOS XE/NX-OS/IOS XR syntax mixed, unsupported commands, wrong commit/rollback model | [Platform Matrix](references/platform-matrix.md), [Quick Reference](references/quick-reference.md) |
| **Config drift / idempotency** | Running config differs from intended state, repeated automation changes, unbounded CLI pushes | [Automation and APIs](references/automation-and-apis.md), [Testing and Validation](references/testing-and-validation.md) |
| **Routing convergence risk** | BGP/OSPF/EIGRP/IS-IS adjacency changes, route loss, redistribution, policy edits | [Routing Troubleshooting](references/routing-troubleshooting.md), [Change Safety](references/change-safety.md) |
| **Layer 2 risk** | STP, VLAN, trunk, port-channel, vPC, loop, blackhole, MAC move symptoms | [Switching Troubleshooting](references/switching-troubleshooting.md), [Change Safety](references/change-safety.md) |
| **HA / redundancy risk** | HSRP/VRRP/GLBP, vPC, VSS, StackWise, dual supervisor/RP state, asymmetric failover | [Switching Troubleshooting](references/switching-troubleshooting.md), [Platform Matrix](references/platform-matrix.md) |
| **ACL/NAT/policy shadowing** | Rule order errors, broad permits/denies, NAT precedence, object-group mistakes | [Security Policy](references/security-policy.md), [ASA/FTD Operations](references/asa-ftd.md) |
| **Secret exposure** | Passwords, SNMP communities, keys, tokens, configs or logs exposing credentials | [Security Policy](references/security-policy.md), [Automation and APIs](references/automation-and-apis.md) |
| **Observability gaps** | Missing before/after evidence, weak telemetry, no alert correlation, unclear success signal | [Telemetry and Observability](references/telemetry-observability.md), [Quick Reference](references/quick-reference.md) |
| **Validation blind spots** | No lab, parser, dry-run, pyATS, Batfish, lint, or staged verification | [Testing and Validation](references/testing-and-validation.md) |

## When to Use This Skill

Activate for Cisco network operations tasks: config review, planned change risk analysis, incident triage, routing/switching troubleshooting, ACL/NAT review, HA checks, telemetry interpretation, and Cisco automation review.

Also activate for automation touching Cisco devices through Ansible, Nornir, Netmiko, pyATS/Genie, NETCONF, RESTCONF, controller APIs, or streaming telemetry.

## Do Not Use This Skill For

- General networking definitions that do not involve Cisco operations.
- Certification tutoring or exam-prep drills.
- Official Cisco/TAC authority claims.
- Direct production device access, credential handling, or autonomous remediation.
- Full SD-WAN, ACI, wireless RF, UCS, Intersight, or Webex design.

## Platform Scope

| Platform | v1 behavior |
| --- | --- |
| IOS XE | Primary: change review, troubleshooting, command guidance, automation review |
| NX-OS | Primary: change review, troubleshooting, command guidance, automation review |
| IOS XR | Primary: change review, troubleshooting, command guidance, automation review |
| ASA/FTD | Secondary: ACL/NAT/policy/routing triage; no full firewall design or deployment modeling |
| ACI, Catalyst Center, Meraki, SD-WAN | Secondary: operational context and escalation guidance only |

When platform or version is missing, say so and avoid platform-specific commands that may be wrong.

## Safety Rules

- Treat all production config as draft text until a human reviews it.
- Label commands as read-only or state-changing when giving runbooks.
- Never imply the agent has live device access unless a tool explicitly provides it.
- Prefer `show`/parse/compare evidence before `configure terminal`, commit, write memory, reload, clear, shut/no shut, or failover actions.
- Do not recommend direct production writes without maintenance context, pre-checks, post-checks, rollback, and abort criteria.
- Redact secrets from pasted configs and avoid repeating credentials in responses.
- For ambiguous symptoms, give the next evidence-gathering command before giving a fix.

## Quick Decision Matrix

| User intent | Default output |
| --- | --- |
| "Review this change" | Risk categories, evidence, pre-checks, post-checks, rollback, approval questions |
| "Troubleshoot this output" | Most likely causes, confidence, next read-only commands, escalation data |
| "Generate config" | Ask for missing platform/topology; emit draft config plus validation and rollback |
| "Review automation" | Idempotency, blast radius, secret handling, parser/test strategy |
| "Summarize incident" | Timeline, impact, evidence, current hypothesis, next actions, escalation bundle |
