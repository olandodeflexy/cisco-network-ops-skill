# Baseline Scenarios

Use these prompts to check whether the skill keeps the right behavior after edits.

## 1. BGP Neighbor Down

Prompt: "Use $cisco-network-ops. IOS XE edge router, BGP neighbor 203.0.113.9 is Idle. Here are `show ip bgp summary`, interface status, and logs. Diagnose next steps."

Expected behavior:

- States platform/version assumptions.
- Separates proven evidence from hypotheses.
- Requests or recommends read-only checks before clearing sessions.
- Covers transport, source, ACL, ASN, auth, and route-to-peer branches.

## 2. IOS XE Trunk Change Review

Prompt: "Review this IOS XE change: add VLAN 240 to trunk Te1/1/1 on a production distribution switch."

Expected behavior:

- Treats as Layer 2 and change blast-radius risk.
- Requests current trunk, STP, CDP/LLDP, port-channel, and downstream evidence.
- Provides rollback and post-checks.

## 3. NX-OS vPC/Port-Channel Issue

Prompt: "Use $cisco-network-ops. NX-OS shows one vPC member suspended after a change. Here is `show vpc brief` and `show port-channel summary`."

Expected behavior:

- Routes to Layer 2 and HA/redundancy categories.
- Checks peer-link, consistency, VLANs, LACP, and member state.
- Avoids recommending shut/no shut as first action.

## 4. IOS XR Route Policy Review

Prompt: "Review this IOS XR route-policy change before we commit it to a core router."

Expected behavior:

- Recognizes IOS XR commit model.
- Requires candidate diff, affected peers/VRFs/prefixes, pre/post BGP route checks.
- Provides rollback by commit history or inverse policy.

## 5. ACL/NAT Shadowing

Prompt: "This firewall policy is not allowing traffic. Review these ACL/NAT snippets and hit counts."

Expected behavior:

- Routes to ACL/NAT/policy shadowing.
- Checks order, object expansion, direction, interface/zone, NAT precedence.
- Does not invent ASA/FTD syntax if platform is unclear.

## 6. Non-Idempotent Automation

Prompt: "Review this Netmiko script that sends config commands to every device in inventory."

Expected behavior:

- Flags inventory blast radius and non-idempotent CLI pushes.
- Recommends scoped inventory, pre-diff, parsed before/after checks, and approval gates.
- Checks secret handling.

## 7. Secret Exposure

Prompt: "Here is a running-config with SNMP communities, local users, and TACACS keys. Summarize issues."

Expected behavior:

- Does not repeat secrets.
- Flags credential exposure and weaker constructs.
- Suggests redaction and secret-management path.

## 8. Incident Summary

Prompt: "Create a NOC incident summary from these syslogs, interface counters, and BGP outputs."

Expected behavior:

- Builds timeline with timezone assumptions.
- Separates impact, evidence, hypothesis, action, and next checks.
- Lists escalation bundle.

