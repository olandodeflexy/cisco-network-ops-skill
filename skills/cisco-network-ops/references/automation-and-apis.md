# Automation and APIs

## Automation Risk Matrix

| Tool/path | Main risk | Default guard |
| --- | --- | --- |
| Ansible network modules | platform mismatch, weak diff/check support | pin collection, use network_cli/httpapi/netconf intentionally, run check/diff where supported |
| Netmiko/Scrapli CLI | non-idempotent command pushes | compare intended vs current config before send_config |
| Nornir | broad inventory blast radius | filter inventory explicitly and batch changes |
| pyATS/Genie | parser assumptions | preserve raw output and parser version |
| NETCONF/RESTCONF | model/version mismatch | validate YANG path, candidate/confirmed commit if supported |
| NX-API | endpoint/payload mismatch, CLI-over-API ambiguity | confirm NX-OS version, transport mode, payload type, and rollback path |
| Controller API | hidden deployment blast radius | inspect preview/diff and controller job target set |

## Idempotency Rules

- Do not push a config line just because it is desired; first prove it is absent or different.
- Scope inventory by device, role, site, platform, and maintenance window.
- Capture before/after parsed state for each changed object.
- Fail closed on unknown platform or parser errors.
- Keep generated config separate from execution code.

## Review Checklist

- Credentials are externalized and not logged.
- Target inventory cannot accidentally include production/fleet-wide devices.
- Diff/check mode or equivalent preview exists before execution.
- Rollback path is code-reviewed and tested.
- Parser failures do not become "success".
- State-changing operations require explicit approval.

## API Guidance

Prefer model-driven interfaces for structured state when platform support is proven. Prefer CLI show output for triage when API coverage is incomplete or during incidents.

Do not invent endpoint paths, YANG models, or controller API fields. Ask for docs, schema, or captured responses when exact API shape matters.

For NX-OS NX-API, distinguish CLI passthrough, JSON-RPC, and REST-style calls before reviewing automation. Require captured request/response samples, NX-OS version, feature enablement state, auth path, and whether the operation is read-only or state-changing.
