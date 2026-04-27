# Switching Troubleshooting

## Switching Triage Matrix

| Symptom | First evidence | Next branch |
| --- | --- | --- |
| Link down/errors | interface status, counters, optics, logs | physical, speed/duplex, errdisable, transceiver |
| VLAN missing | VLAN database, trunk allowed list, interface mode | pruning, native VLAN, VTP/controller source |
| STP instability | root/blocked ports, topology changes, logs | root guard, BPDU guard, loop guard, bad trunk |
| Port-channel down | member state, LACP mode, consistency checks | speed/VLAN mismatch, min-links, vPC/MLAG peer |
| vPC/MLAG issue | peer-link, keepalive, consistency, orphan ports | peer health, VLAN consistency, role priority |

## Layer 2 Change Pre-Checks

- Capture current interface stanza, VLAN membership, trunk allowed list, and port-channel membership.
- Check CDP/LLDP neighbors before changing uplinks or trunks.
- Check STP root and blocked ports before VLAN/trunk changes.
- Check MAC table movement when loops or blackholes are suspected.
- For vPC/MLAG, check peer-link and consistency before member changes.

## HA and Redundancy

| Technology | Evidence |
| --- | --- |
| HSRP/VRRP/GLBP | active/standby state, priority, tracking, preempt, timers |
| vPC | peer adjacency, peer-link, consistency, orphan ports |
| StackWise/VSS | member role, redundancy state, software version, split-brain indicators |
| Dual supervisor/RP | active/standby state, sync, switchover readiness |

## Safety Rules

- Do not remove VLANs from trunks without proving all downstream paths.
- Do not change STP root priority without mapping the L2 domain.
- Treat `shutdown`/`no shutdown`, errdisable recovery, and port-channel member removal as state-changing.
- Prefer one access port or one downstream pair as a canary before broad access-layer changes.

