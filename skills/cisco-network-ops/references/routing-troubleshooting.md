# Routing Troubleshooting

## Routing Triage Matrix

| Symptom | First evidence | Next branch |
| --- | --- | --- |
| BGP neighbor down | neighbor summary, logs, interface/route to peer | transport, TTL, auth, ASN, update-source, ACL |
| Routes missing | RIB/FIB, protocol database, policy counters | origination, filtering, next-hop, redistribution |
| Route leak | advertised/received routes, policy diff, VRF context | prefix-list/route-map/RPL, communities, redistribution |
| Flapping | logs, timers, interface counters, control-plane drops | physical, BFD, CPU, keepalive/hold timers |
| Asymmetric path | traceroute, route table per VRF, policy/PBR | route preference, ECMP, NAT/firewall path |

## BGP Evidence

Collect platform-appropriate equivalents for:

- Neighbor summary and specific neighbor detail.
- TCP reachability to peer source/destination.
- Local/remote ASN, update-source, ebgp-multihop/TTL, authentication.
- Received and advertised route samples.
- Route policy/prefix-list/RPL hit behavior.
- Recent logs for resets and notification codes.

## OSPF/EIGRP/IS-IS Evidence

| Protocol | Check |
| --- | --- |
| OSPF | neighbor state, area, network type, MTU, authentication, passive interface |
| EIGRP | neighbor state, K-values, stub, authentication, topology entry |
| IS-IS | adjacency state, level-1/level-2 role, NET/system ID, MTU, circuit type, LSP/database evidence |

For IS-IS, collect platform-appropriate equivalents for neighbor/CLNS adjacency state, level-1 vs level-2 participation, interface circuit type, area/NET, LSP database health, overload bit, metric changes, authentication, and MTU. On IOS XR, also capture commit history or candidate diff if the symptom follows a routing-policy or interface change.

## Change Safety Rules

- Treat redistribution and default-route changes as high blast-radius unless constrained.
- Confirm VRF/address-family before interpreting any route output.
- Compare pre/post routes for specific prefixes and aggregate counts.
- Avoid clearing routing sessions as a first step; it is state-changing and can hide root cause.
