# Testing and Validation

## Validation Matrix

| Task | Validation |
| --- | --- |
| Config review | syntax/platform check, peer review, pre/post command list |
| Routing policy | lab or Batfish where available, prefix diff, peer-specific advertised/received route checks |
| Switching change | lab/canary, STP/vPC/port-channel checks, MAC/neighbor comparison |
| Automation change | lint, dry-run/diff, limited inventory, parsed before/after state |
| Incident diagnosis | raw evidence preservation, timeline, next read-only command, escalation bundle |

## pyATS/Genie Pattern

- Preserve raw command output with parsed JSON.
- Record parser and platform versions.
- Compare specific keys, not only command success.
- Treat parser exceptions as validation failure unless explicitly waived.

## Batfish Pattern

Use Batfish for reachability, routing policy, ACL, and differential checks when configs are available and platform support fits. Keep CLI/device evidence as source of truth for live incidents.

## Smoke-Test Criteria

A useful skill smoke test must prove:

- Platform ambiguity is called out.
- Direct write access is not assumed.
- State-changing recommendations include rollback.
- Read-only diagnostics come before fixes.
- Secrets are redacted or not repeated.
- Automation review catches idempotency and inventory blast radius.

