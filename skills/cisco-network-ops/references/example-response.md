# Example Response

Use this as the shape for safety-critical answers. Keep real answers shorter when the user asks a narrow factual question.

## Prompt

```text
Use $cisco-network-ops. IOS XE edge router lost BGP to provider 203.0.113.9.
show ip bgp summary shows Idle for 18 minutes, zero prefixes.
Logs show BGP Notification sent.
```

## Response Pattern

**Assumptions**

- Platform is IOS XE unless later evidence says NX-OS or IOS XR.
- Neighbor `203.0.113.9` is an eBGP provider peer.
- No direct device access is available; all commands are operator-run.
- Missing context: local/remote ASN, update source, VRF, provider interface, recent change window, and notification code/subcode.

**Risk category**

Routing convergence risk and observability gap.

**Evidence**

- `show ip bgp summary`: neighbor `203.0.113.9` is `Idle` for 18 minutes and has zero prefixes.
- Syslog says the local router sent a BGP Notification.
- Inference: local BGP likely detected a protocol condition and reset the session, but the cause is unproven until the notification code/subcode is known.

**Recommendation**

Do not clear the BGP session first. Preserve evidence, find the exact notification reason, then branch by cause.

**Pre-checks**

Read-only checks:

```text
show logging | include 203.0.113.9|BGP-3-NOTIFICATION|BGP-5-ADJCHANGE
show ip bgp neighbors 203.0.113.9
show running-config | section router bgp
show ip route 203.0.113.9
show ip interface brief
show interfaces <provider-facing-interface>
show access-lists
show control-plane host open-ports | include 179
ping 203.0.113.9 source <local-bgp-source>
traceroute 203.0.113.9 source <local-bgp-source>
```

If the peer is in a VRF, use platform-specific VRF-scoped equivalents for every BGP, route, ping, traceroute, and logging check. Example placeholders:

```text
show bgp vrf <vrf> neighbors 203.0.113.9
show ip route vrf <vrf> 203.0.113.9
ping vrf <vrf> 203.0.113.9 source <local-bgp-source>
traceroute vrf <vrf> 203.0.113.9 source <local-bgp-source>
```

Check for maximum-prefix, ASN mismatch, authentication mismatch, update-source/TTL issue, ACL/CoPP block, interface errors, BFD failure, provider maintenance, or malformed update.

**Execution guidance**

If the notification reason is understood and the provider confirms readiness, a controlled BGP clear can be considered during an approved window. Label it state-changing:

```text
clear ip bgp 203.0.113.9
```

For a VRF peer, use the platform-specific VRF-scoped clear for that exact neighbor instead of the global clear. Do not run a global clear for a VRF-scoped incident.

Avoid broad clears such as `clear ip bgp *`.

**Post-checks**

```text
show ip bgp summary
show ip bgp neighbors 203.0.113.9
show ip route bgp
show logging | include 203.0.113.9|BGP
```

Use the same VRF-scoped equivalents in post-checks when the peer belongs to a VRF.

Success means the neighbor reaches `Established`, expected prefixes return, route counts are within expected bounds, and no new notification appears.

**Rollback and abort criteria**

If the clear causes wider route churn, unexpected peer resets, or traffic alarms, stop further actions and restore the prior routing path if one was changed. If no config changed, rollback is evidence preservation plus escalation, not an inverse config.

**Escalation notes**

Send the provider or TAC: timestamp with timezone, local/remote ASN, local/peer IPs, notification code/subcode, interface state/counters, TCP/179 reachability, BFD state if used, and recent local changes.
