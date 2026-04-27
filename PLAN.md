# Cisco Network Operations Skill Implementation Plan

## Stage Gate

This plan follows the approved `SPEC.md`. Do not implement behavior outside that scope without updating the spec first.

## Slice 1: Repository Skeleton and Core Skill

Create the portable skill structure:

- `skills/cisco-network-ops/SKILL.md`
- `skills/cisco-network-ops/references/*.md`
- `skills/cisco-network-ops/agents/openai.yaml`
- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`
- `.github/workflows/validate.yml`
- `tests/baseline-scenarios.md`
- `tests/smoke-test-prompts.md`

Acceptance criteria:

- `SKILL.md` is under 300 lines.
- Frontmatter is valid and starts the description with `Use when`.
- All reference links resolve.
- Skill clearly states offline/advisory default and no direct device access.
- Response Contract appears in core file.

Review focus:

- Over-broad Cisco claims.
- Unsafe change-generation behavior.
- Missing platform assumptions.
- Reference bloat in `SKILL.md`.

## Slice 2: Reference Content

Fill initial references with retrieval-first guidance:

- Change safety and rollback.
- Platform matrix for IOS XE, NX-OS, IOS XR.
- Routing troubleshooting.
- Switching troubleshooting.
- Security policy and secrets.
- Automation/API review.
- Telemetry and observability.
- Testing and validation.

Acceptance criteria:

- Each reference opens sections with decision tables where multiple approaches exist.
- Commands are labeled read-only or state-changing where relevant.
- Examples are realistic and avoid secrets.
- Every state-changing workflow includes pre-checks, post-checks, and rollback.

Review focus:

- IOS XE/NX-OS/IOS XR syntax confusion.
- Dangerous commands without gates.
- Human tutorial prose instead of LLM retrieval structure.
- Missing escalation/evidence guidance.

## Slice 3: Tests and Validation

Add validation and scenario coverage:

- Baseline scenario prompts for major categories.
- Smoke-test prompts for real installation checks.
- Validation script or CI checks for frontmatter, link integrity, and line count.

Acceptance criteria:

- Local validation passes.
- Baseline scenarios cover at least the eight cases from `SPEC.md`.
- Smoke prompts include ambiguity, change safety, direct-write refusal/gating, and automation review.

Review focus:

- Scenarios too shallow to catch unsafe behavior.
- Test prompts leaking expected answers.
- CI checking formatting only and missing skill-specific constraints.

## Slice 4: Adversarial Review and Convergence

Run review loops until no new substantive issues remain:

- Self-review against `SPEC.md`.
- Adversarial review pass focused on operational safety.
- Adversarial review pass focused on skill retrieval quality.
- Fix issues and repeat review if new substantive issues are found.

Acceptance criteria:

- No unresolved high/medium review findings.
- Any accepted risks are documented in the final handoff.
- Changes remain within the approved scope.

## Slice 5: Real Installation and Smoke Test

Install and exercise the skill locally.

Codex smoke:

- Install or symlink the repo into a Codex-discoverable skill/plugin location.
- Run realistic prompts from `tests/smoke-test-prompts.md`.
- Confirm the skill invokes and emits the Response Contract for safety-critical prompts.

Claude smoke, if available:

- Install or symlink the repo into a Claude-discoverable plugin/skill location.
- Run the same class of prompts.
- Confirm compatibility or document the blocker.

Acceptance criteria:

- At least one real Codex skill/plugin discovery path is tested.
- Prompts use realistic Cisco artifacts, not toy examples.
- Smoke results are recorded in the final handoff.

## Non-Negotiables

- Do not add direct network-device write automation in v1.
- Do not imply official Cisco/TAC authority.
- Do not recommend production deployment without human review and rollback.
- Do not duplicate long guidance between `SKILL.md` and references.
- Do not hide uncertainty when platform, version, topology, or change window is missing.
