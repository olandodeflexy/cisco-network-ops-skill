# ASA/FTD Operations

Use this reference for ASA/FTD policy and NAT triage. Keep v1 guidance advisory; do not model full firewall design or deployment workflows.

## Triage Matrix

| Symptom | First evidence | Next branch |
| --- | --- | --- |
| Flow denied | ACL hit counts, logs, packet-tracer output | rule order, interface/zone, object expansion |
| NAT mismatch | NAT table, xlate entries, packet-tracer phases | manual/auto NAT order, twice NAT, object NAT |
| Route or VPN path issue | route table, crypto/session state, packet-tracer | missing route, asymmetric path, tunnel policy |
| FTD deployment uncertainty | FMC change preview, deployment task, device health | target set, pending changes, policy inheritance |

## Evidence Rules

- Confirm platform path first: ASA CLI, FTD managed by FMC, FDM-managed FTD, or CDO/controller-managed.
- Capture source, destination, protocol, port, ingress interface/zone, egress interface/zone, and VRF/context if applicable.
- Use packet-tracer/simulation output when available, but preserve relevant ACL/NAT/object snippets too.
- Check hit counts before and after changes; a matching rule with zero hits may be the wrong path or direction.

## Safety Rules

- Do not invent ASA, FTD, FMC, or FDM syntax when the deployment path is unclear.
- Treat broad permits, rule reordering, NAT changes, and deploy jobs as state-changing.
- For FTD/FMC, inspect preview and target devices before deployment.
- For ASA, preserve current ACL/NAT snippets and xlate/session evidence before changing policy.

## Escalation Bundle

- Platform and management path.
- Relevant ACL/NAT/object snippets with secrets redacted.
- Packet-tracer or simulation output.
- Hit counts and logs with timestamps.
- Expected business flow and observed failure phase.
