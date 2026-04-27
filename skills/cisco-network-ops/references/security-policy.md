# Security Policy

## ACL/NAT Review Matrix

| Risk | Evidence | Review action |
| --- | --- | --- |
| Shadowed rule | ACL order, object expansion, hit counts | Identify earlier match that makes later rule unreachable |
| Overbroad permit | source/destination/service too wide | Narrow object, prefix, port, or direction |
| Unintended deny | implicit deny, missing return path, wrong interface | Trace packet direction and policy attachment |
| NAT precedence issue | NAT order, route, interface zones | Compare specific vs broad NAT rules |
| Stale object | unused object-group or zero-hit rule | Confirm with owner before removal |

## Secrets Handling

- Redact passwords, keys, SNMP communities, RADIUS/TACACS keys, tokens, and private addresses when needed.
- Do not repeat pasted secrets back to the user.
- Flag weak constructs such as type 7 passwords, plaintext communities, broad management ACLs, and shared local accounts.
- In automation, keep secrets in vault/secret managers and mark logs as sensitive.

## Policy Change Safety

- Confirm traffic direction, interface/zone attachment, VRF/context, and NAT order.
- Capture hit counts before and after the change.
- For deny rules, provide a business-impact question before recommending deployment.
- For firewall/controller platforms, avoid CLI assumptions until platform and deployment path are known.

## Escalation Bundle

For unresolved policy issues, collect:

- Source, destination, protocol, port, VRF/context, ingress and egress interface.
- Relevant ACL/NAT/object-group snippets with secrets redacted.
- Packet-tracer/simulation output when available.
- Hit counts and timestamps before/after attempted change.

