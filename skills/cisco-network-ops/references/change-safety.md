# Change Safety

## Change Risk Matrix

| Change type | Risk driver | Default control |
| --- | --- | --- |
| Interface access change | Endpoint outage, wrong port, voice/data VLAN mix | Verify CDP/LLDP/MAC, save current stanza, test one port first |
| Trunk/VLAN change | VLAN pruning, STP topology change, blackhole | Check allowed VLANs, STP root, port-channel/vPC state |
| Routing policy change | Route leak/loss, asymmetric path | Snapshot neighbors/routes/policies, apply narrowly, compare prefixes |
| HA/failover change | Active/standby split, dual-active, traffic loss | Confirm peer health and sync state before edits |
| ACL/NAT change | Shadowed rules, unintended permit/deny | Check hit counts, object expansion, order, rollback stanza |
| Automation push | Fleet-wide drift, repeated changes | Limit targets, dry-run/diff, idempotency check, staged rollout |

## Pre-Change Checklist

- Confirm platform, OS version, device role, target scope, and maintenance window.
- Capture current relevant config and command output.
- Identify state-changing commands and who is authorized to run them.
- Define success, abort criteria, and rollback trigger before execution.
- For multi-device changes, choose order: standby before active, edge before core only when safe, one site before fleet.

## Execution Pattern

| Scope | Pattern |
| --- | --- |
| Single low-risk device | Pre-check, apply, post-check, save only after verification |
| HA pair | Verify sync, update standby/passive side first when platform supports it, failover only with explicit plan |
| Many devices | Canary, pause, compare telemetry, continue in batches |
| Routing policy | Apply to narrow peer/VRF/prefix first; avoid broad redistribution changes without lab proof |

## Rollback Patterns

| Platform | Preferred rollback evidence |
| --- | --- |
| IOS XE | saved config stanza, archive/backup if configured, inverse commands |
| NX-OS | checkpoint/rollback where available, saved stanza, inverse commands |
| IOS XR | commit history, rollback target, candidate diff, inverse config |

Rollback text must include the trigger, exact previous state source, and verification after rollback.

