# Telemetry and Observability

## Signal Matrix

| Signal | Use | Caution |
| --- | --- | --- |
| Syslog | event timing, adjacency resets, errdisable, HA events | timestamps/time zones may differ |
| SNMP/NMS | interface status, counters, availability | polling delay hides short events |
| Streaming telemetry | high-resolution counters/state | model paths vary by platform/release |
| CLI snapshots | point-in-time truth for device state | manual capture can miss transient events |
| Controller jobs | deployment status and target set | "success" may not prove dataplane health |

## Incident Evidence Pattern

1. Build a timeline with absolute timestamps and time zone.
2. Map alerts to devices, interfaces, VRFs, VLANs, peers, or policies.
3. Separate symptom, suspected cause, confirmed cause, and remediation.
4. Preserve raw logs before summarizing.
5. Identify missing telemetry that blocks confidence.

## Success Signals

| Domain | Success evidence |
| --- | --- |
| Interface | operational up, clean counters trend, expected neighbor/MAC |
| Routing | neighbor stable, expected prefixes present, no unexpected withdrawals |
| Layer 2 | STP stable, no MAC flaps, expected port-channel/vPC state |
| Policy | hit counts match expected flow, no broad deny spike |
| HA | active/standby roles stable, sync healthy, no split-brain indicators |

## Observability Gaps

Flag the gap when no before/after state exists. Recommend the smallest useful evidence capture before remediation.

