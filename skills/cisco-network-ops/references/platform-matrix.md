# Platform Matrix

## Platform Differences

| Topic | IOS XE | NX-OS | IOS XR |
| --- | --- | --- | --- |
| Config model | Immediate running-config changes | Immediate running-config changes with feature-centric behavior | Candidate config committed to running config |
| Save model | `copy running-config startup-config` or `write memory` | `copy running-config startup-config` | Commit persists changes in running config; startup model differs by platform |
| Rollback style | Archive/config replace when configured; inverse commands otherwise | Checkpoint/rollback often available | Commit rollback model is core behavior |
| Interface names | `GigabitEthernet`, `TenGigabitEthernet`, `Port-channel` | `Ethernet`, `port-channel` | `GigabitEthernet`, `Bundle-Ether` |
| Feature enablement | Often implicit by config/license | Many features require `feature ...` | Package/feature support varies by image and release |
| VRF syntax | IOS-style `vrf definition`/address-family on many releases | `vrf context` | VRF under XR routing/address-family model |

Do not translate config across platforms without checking syntax and feature support.

## Command Safety Classes

| Class | Examples | Handling |
| --- | --- | --- |
| Read-only | `show ...`, parsed telemetry, config display | Safe to request first |
| Candidate/diff | IOS XR candidate diff, automation dry-run, Batfish/pyATS checks | Use before writes |
| State-changing | config mode, commit, write, rollback, clear, reload, shut/no shut | Require gates and rollback |

## Ambiguity Rules

- If the prompt says "Cisco router" but not platform, ask for `show version` or infer only with low confidence.
- If config syntax looks mixed, flag platform mismatch before generating fixes.
- If a command exists on one platform but not another, provide a platform-specific table instead of one command.
- If the user gives controller context only, avoid device CLI assumptions until the deployment path is clear.

