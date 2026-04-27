# Quick Reference

## Evidence Checklist

| Need | Collect |
| --- | --- |
| Platform/version | `show version`, image name, license/feature state |
| Current state | relevant running config section, interface/routing/policy outputs |
| Intended state | change ticket, config diff, automation code, expected paths |
| Blast radius | device role, site, peers, VRF/VLAN/interface list, affected services |
| Baseline | pre-change routes, neighbors, counters, logs, NMS alerts |
| Rollback | saved config, checkpoint, archive, previous automation commit |

## Read-Only Command Defaults

| Platform | Useful read-only commands |
| --- | --- |
| IOS XE | `show version`, `show running-config`, `show ip interface brief`, `show interfaces`, `show logging`, `show ip route`, `show ip bgp summary` |
| NX-OS | `show version`, `show running-config`, `show interface status`, `show port-channel summary`, `show vpc brief`, `show logging last 200`, `show ip route`, `show bgp summary` |
| IOS XR | `show version`, `show running-config`, `show interfaces brief`, `show route`, `show bgp summary`, `show logging`, `show configuration commit list` |

Use platform help (`?`) or local runbooks when command spelling differs by release, feature set, or device family.

## State-Changing Command Triggers

Treat these as gated actions: `configure terminal`, `commit`, `copy running-config startup-config`, `write memory`, `reload`, `clear`, `shutdown`, `no shutdown`, `default interface`, `rollback`, `install`, `failover`, and controller-driven deploys.

## Missing Context Prompts

Ask for missing context when the answer would change based on:

- Platform family or OS version.
- L2 vs L3 device role.
- HA pair or multi-chassis role.
- Maintenance window and rollback authority.
- Exact interface, VRF, VLAN, prefix, neighbor, policy, or object-group.
- Whether the output is pre-change, post-change, or during incident.

