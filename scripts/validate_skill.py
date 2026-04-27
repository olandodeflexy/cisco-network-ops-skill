#!/usr/bin/env python3
"""Validate the Cisco Network Operations skill package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "cisco-network-ops"
SKILL_MD = SKILL_DIR / "SKILL.md"
REQUIRED_REFS = {
    "quick-reference.md",
    "change-safety.md",
    "platform-matrix.md",
    "routing-troubleshooting.md",
    "switching-troubleshooting.md",
    "security-policy.md",
    "automation-and-apis.md",
    "telemetry-observability.md",
    "testing-and-validation.md",
}


def fail(message: str) -> None:
    print(f"[ERROR] {message}")
    sys.exit(1)


def check_exists() -> None:
    required = [
        SKILL_MD,
        SKILL_DIR / "agents" / "openai.yaml",
        ROOT / ".codex-plugin" / "plugin.json",
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / "tests" / "baseline-scenarios.md",
        ROOT / "tests" / "smoke-test-prompts.md",
    ]
    for path in required:
        if not path.exists():
            fail(f"Missing required file: {path.relative_to(ROOT)}")

    refs_dir = SKILL_DIR / "references"
    missing_refs = sorted(REQUIRED_REFS - {p.name for p in refs_dir.glob("*.md")})
    if missing_refs:
        fail(f"Missing references: {', '.join(missing_refs)}")


def parse_frontmatter(content: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        fail("SKILL.md missing YAML frontmatter")
    frontmatter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip('"')
    return frontmatter


def check_skill_md() -> None:
    content = SKILL_MD.read_text()
    lines = content.splitlines()
    if len(lines) > 300:
        fail(f"SKILL.md has {len(lines)} lines; target is <= 300")

    frontmatter = parse_frontmatter(content)
    if frontmatter.get("name") != "cisco-network-ops":
        fail("SKILL.md frontmatter name must be cisco-network-ops")
    if not frontmatter.get("description", "").startswith("Use when"):
        fail("SKILL.md description must start with 'Use when'")
    if frontmatter.get("license") != "Apache-2.0":
        fail("SKILL.md license must be Apache-2.0")
    if "Response Contract" not in content:
        fail("SKILL.md missing Response Contract")
    if "direct access" not in content and "live device access" not in content:
        fail("SKILL.md must state no assumed direct device access")


def check_links() -> None:
    files = [SKILL_MD, *sorted((SKILL_DIR / "references").glob("*.md"))]
    link_pattern = re.compile(r"\]\((references/[^)#]+\.md)(?:#[^)]+)?\)")
    for path in files:
        content = path.read_text()
        for match in link_pattern.finditer(content):
            target = SKILL_DIR / match.group(1)
            if not target.exists():
                fail(
                    f"Broken reference link in {path.relative_to(ROOT)}: "
                    f"{match.group(1)}"
                )


def check_json() -> None:
    for rel in [
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
    ]:
        path = ROOT / rel
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSON in {rel}: {exc}")
        if rel == ".claude-plugin/marketplace.json" and "version" in data:
            fail("Claude marketplace manifest must not use top-level version")


def check_openai_yaml() -> None:
    content = (SKILL_DIR / "agents" / "openai.yaml").read_text()
    required = [
        "display_name: \"Cisco Network Operations\"",
        "short_description:",
        "default_prompt:",
    ]
    for text in required:
        if text not in content:
            fail(f"agents/openai.yaml missing {text}")


def main() -> int:
    check_exists()
    check_skill_md()
    check_links()
    check_json()
    check_openai_yaml()
    print("[OK] Cisco Network Operations skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
