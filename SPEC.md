# Cisco Network Operations Skill Specification

## Status

Draft for design review.

## Project Identity

| Field | Value |
| --- | --- |
| Project name | Cisco Network Operations Skill |
| Repository name | `cisco-network-ops-skill` |
| Skill name | `cisco-network-ops` |
| Skill directory | `skills/cisco-network-ops/` |
| Human display name | Cisco Network Operations |
| Default license | Apache-2.0 |
| Initial version | `0.1.0` |

## Problem

AI agents can help network operators reason over Cisco configs, command output, automation code, and incident artifacts, but generic agents often:

- Treat Cisco platforms as interchangeable.
- Generate risky production config without pre-checks, blast-radius controls, or rollback.
- Miss NOC operating constraints such as maintenance windows, peer dependencies, HA state, and change evidence.
- Confuse troubleshooting with remediation and jump to fixes without proof.
- Ignore offline-first reality: most routers and switches are not directly connected to AI agents.

This skill teaches agents to operate like a cautious Cisco network operations assistant: diagnose first, state assumptions, preserve evidence, control blast radius, and produce verifiable plans.

## Goals

- Provide diagnose-first guidance for Cisco network operations, troubleshooting, change review, and automation review.
- Support offline artifact analysis from configs, diffs, logs, CLI output, parsed telemetry, NMS alerts, topology notes, and automation code.
- Produce NOC-ready outputs: change plans, risk reviews, pre-check/post-check lists, rollback plans, incident summaries, and escalation artifacts.
- Keep `SKILL.md` compact and route detailed material to reference files loaded on demand.
- Package the repo so both Claude Code and Codex can use the same skill content.
- Validate behavior with baseline scenarios and real installation/smoke prompts before shipping.

## Non-Goals

- No direct SSH/API connection to production network devices in v1.
- No autonomous remediation or write access to routers, switches, controllers, or firewalls.
- No claim of official Cisco, TAC, or certification authority.
- No exhaustive Cisco API reference dump.
- No certification tutoring or exam prep focus.
- No full deep design coverage for SD-WAN, wireless RF, ACI fabric design, UCS, Intersight, or Webex in v1.
- No recommendation to deploy production config without human review, maintenance-window context, and rollback.

## Primary Users

- NOC engineers reviewing alerts, logs, and show output.
- Network engineers preparing or reviewing Cisco changes.
- SRE/NetOps engineers reviewing Cisco automation.
- Incident responders preparing escalation notes.
- AI coding agents working inside network automation repositories.

## Supported Inputs

| Input | Examples |
| --- | --- |
| Device configs | `running-config`, intended config snippets, Git diffs |
| CLI output | `show version`, `show interface`, `show logging`, `show ip route`, `show bgp summary`, `show spanning-tree`, `show etherchannel summary` |
| Parsed output | pyATS/Genie JSON, TextFSM records, Batfish findings |
| Automation code | Ansible, Nornir, Netmiko, pyATS, NETCONF/RESTCONF, telemetry collectors |
| Operations context | topology notes, device role, maintenance window, affected sites, ticket text |
| Monitoring data | NMS alerts, syslog snippets, SNMP/streaming telemetry summaries |

## Platform Scope

### Primary Platforms

| Platform | v1 Support |
| --- | --- |
| IOS XE | Change review, troubleshooting, command guidance, automation review |
| NX-OS | Change review, troubleshooting, command guidance, automation review |
| IOS XR | Change review, troubleshooting, command guidance, automation review |

### Secondary Platforms

| Platform | v1 Support |
| --- | --- |
| ASA/FTD | Policy/NAT/routing troubleshooting patterns; limited config generation |
| ACI | Context and escalation guidance; no full fabric design |
| Catalyst Center | Context and automation review; no controller API deep reference |
| Meraki | Dashboard/API context; no exhaustive API reference |
| SD-WAN | Context and operational risk guidance; no full vManage design |

When platform or OS version is missing, the skill must state assumptions and avoid platform-specific commands that could be wrong.

## Safety Model

The default operating model is offline and advisory.

- Analyze artifacts provided by the user.
- Ask for missing critical context when a recommendation would be unsafe without it.
- Prefer read-only commands for evidence collection.
- Generate production config only when explicitly asked.
- Pair every state-changing recommendation with pre-checks, post-checks, rollback, and blast-radius controls.
- Treat AI-generated config as draft text requiring human review.
- Avoid instructions that bypass change control, credential controls, or segmentation policy.

## Failure Categories

The skill routes user requests through these categories before generating output:

| Category | Symptoms |
| --- | --- |
| Change blast radius | Large site/fleet impact, unclear target devices, no maintenance window, missing rollback |
| Platform mismatch | IOS XE/NX-OS/IOS XR syntax confusion, wrong feature availability, unsupported commands |
| Config drift / idempotency | Intended state differs from running state, automation repeatedly changes config, non-idempotent CLI pushes |
| Routing convergence risk | BGP/OSPF/EIGRP/IS-IS adjacency changes, route loss, policy changes, redistribution risk |
| Layer 2 risk | STP changes, VLAN pruning, trunk changes, port-channel issues, loop or blackhole risk |
| HA / redundancy risk | HSRP/VRRP/GLBP, VSS/StackWise/vPC, dual-supervisor or route-processor state |
| ACL/NAT/policy shadowing | Rule order problems, broad permits/denies, NAT precedence, object-group mistakes |
| Secret exposure | Passwords, SNMP communities, keys, tokens, logs or configs exposing credentials |
| Observability gaps | Missing before/after evidence, weak telemetry, no alert correlation |
| Validation blind spots | No lab, parser, lint, dry-run, Batfish, pyATS, or post-change verification |

## Response Contract

Every Cisco Network Operations response must include:

1. **Assumptions**: platform, OS version if known, topology role, environment criticality, access path, and what is missing.
2. **Risk category**: one or more diagnosed categories from the routing table.
3. **Evidence**: specific lines, outputs, symptoms, or diffs used to reach the conclusion.
4. **Recommendation**: chosen remediation or next diagnostic step, with tradeoffs.
5. **Pre-checks**: read-only commands, snapshots, backups, neighbor state, interface state, and route/policy evidence.
6. **Execution guidance**: ordered steps or draft config only when appropriate.
7. **Post-checks**: exact verification commands or artifact comparisons.
8. **Rollback**: inverse config, restore path, abort criteria, and evidence to retain.
9. **Escalation notes**: when to involve TAC/vendor, what data to collect, and what not to change further.

For small factual answers, the contract may be compressed, but safety-critical answers must keep the full shape.

## Skill Architecture

```text
skills/
  cisco-network-ops/
    SKILL.md
    agents/
      openai.yaml
    references/
      quick-reference.md
      change-safety.md
      platform-matrix.md
      routing-troubleshooting.md
      switching-troubleshooting.md
      security-policy.md
      automation-and-apis.md
      telemetry-observability.md
      testing-and-validation.md
tests/
  baseline-scenarios.md
  smoke-test-prompts.md
.claude-plugin/
  plugin.json
  marketplace.json
.codex-plugin/
  plugin.json
.github/
  workflows/
    validate.yml
```

### `SKILL.md`

`SKILL.md` is the compact entry point. It must contain:

- Trigger description and scope.
- Response Contract.
- Workflow.
- Diagnose-before-generate routing table.
- Platform scope.
- Quick safety rules.
- Reference-file routing.

Target size: under 300 lines.

### References

Reference files hold detailed playbooks, decision tables, gotchas, and examples. They must be loaded only when relevant.

| File | Purpose |
| --- | --- |
| `quick-reference.md` | Common commands, evidence checklist, platform/version cautions |
| `change-safety.md` | Change planning, blast radius, pre/post checks, rollback templates |
| `platform-matrix.md` | IOS XE vs NX-OS vs IOS XR syntax and operational differences |
| `routing-troubleshooting.md` | BGP, OSPF, EIGRP, IS-IS, route policy, convergence |
| `switching-troubleshooting.md` | VLANs, trunks, STP, EtherChannel, vPC, interface issues |
| `security-policy.md` | ACL, NAT, firewall policy, segmentation, secrets handling |
| `automation-and-apis.md` | Ansible, Nornir, Netmiko, pyATS, NETCONF/RESTCONF, telemetry |
| `telemetry-observability.md` | Syslog, SNMP, streaming telemetry, NMS alert correlation |
| `testing-and-validation.md` | pyATS/Genie, Batfish, lab validation, parser checks, smoke tests |

## Compatibility Requirements

- The core skill content must work for both Claude Code and Codex.
- Use portable `SKILL.md` skill structure.
- Include Claude plugin metadata where practical.
- Include Codex plugin metadata where practical.
- Do not duplicate skill instructions across platform-specific manifests.
- Keep MCP optional and out of the v1 runtime dependency path.

## Validation Strategy

### Static Validation

- Check required files exist.
- Validate `SKILL.md` frontmatter.
- Check internal links to reference files.
- Check `SKILL.md` line count target.
- Run markdown lint if available.

### Baseline Scenarios

Baseline scenarios must cover:

- BGP neighbor down from CLI output.
- Risk review for an IOS XE interface/trunk change.
- NX-OS vPC or port-channel troubleshooting.
- IOS XR route-policy or BGP change review.
- ACL/NAT shadowing review.
- Automation review for a non-idempotent Netmiko or Ansible change.
- Secret exposure in a pasted config.
- Incident summary from logs and show commands.

### Smoke Test

Before shipping, install the skill locally and run realistic prompts against it. Smoke testing must verify:

- The skill is discoverable by Codex.
- The skill is discoverable by Claude Code if available in the environment.
- The response contract appears for safety-critical prompts.
- Platform ambiguity is handled explicitly.
- The agent refuses or gates direct production write behavior.
- Reference routing is useful and not bloated.

## Review Requirements

Each implementation slice must receive adversarial review before merge.

Reviewers must check:

- Does the skill reduce unsafe Cisco/network operations behavior?
- Are platform differences explicit enough?
- Does it avoid pretending to have live network access?
- Does it avoid over-generating production config?
- Are references retrieval-first rather than prose-heavy?
- Are commands marked read-only vs state-changing?
- Are rollback and evidence requirements present for every change workflow?
- Are examples realistic without embedding secrets or dangerous defaults?

Convergence means reviewers stop finding new substantive issues, not merely that validation passes.

## Resolved Decisions

- Include repo-level `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md` in v1.
- Rename the root folder to `cisco-network-ops-skill`.
- Include both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
- Include `agents/openai.yaml` in the first implementation slice.
