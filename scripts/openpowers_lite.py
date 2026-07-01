#!/usr/bin/env python3
"""OpenPowers Lite repository checks and upstream audit tooling."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = Path(".openpowers/upstreams.json")
DEFAULT_LOCK = Path(".openpowers/upstreams.lock.json")
DEFAULT_REPORT = Path(".openpowers/upgrade-report.md")
DEFAULT_CHANGELOG = Path(".openpowers/UPGRADE_CHANGELOG.md")


@dataclass(frozen=True)
class CheckResult:
    status: str
    message: str


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_command(args: list[str], cwd: Path | None = None) -> str:
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"Command not found: {args[0]}") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip()
        raise RuntimeError(f"{' '.join(args)} failed: {detail}") from exc
    return completed.stdout.strip()


def resolve_git_ref(url: str, ref: str) -> str:
    output = run_command(["git", "ls-remote", url, ref])
    if not output:
        raise RuntimeError(f"No git ref matched {ref!r} at {url}")
    first_line = output.splitlines()[0]
    sha = first_line.split()[0]
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise RuntimeError(f"Unexpected git ls-remote output for {url}: {first_line}")
    return sha


def resolve_npm_version(package: str, registry: str | None) -> str:
    url_package = urllib.request.quote(package, safe="@")
    url = f"{(registry or 'https://registry.npmjs.org').rstrip('/')}/{url_package}/latest"
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"npm metadata request failed for {package}: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"npm metadata request failed for {package}: {exc.reason}") from exc
    version = payload.get("version") if isinstance(payload, dict) else None
    if not isinstance(version, str) or not version:
        raise RuntimeError(f"npm metadata for {package} did not include a version")
    return version


def resolve_upstreams(config: dict[str, Any], registry_override: str | None) -> dict[str, Any]:
    upstreams = config.get("upstreams")
    if not isinstance(upstreams, list):
        raise SystemExit("upstreams.json field `upstreams` must be an array")

    resolved: list[dict[str, Any]] = []
    errors: list[str] = []
    for upstream in upstreams:
        if not isinstance(upstream, dict):
            errors.append("upstream entries must be objects")
            continue
        name = upstream.get("name")
        kind = upstream.get("type")
        if not isinstance(name, str) or not name:
            errors.append("upstream entry is missing non-empty `name`")
            continue
        try:
            if kind == "git":
                url = require_str(upstream, "url", name)
                ref = require_str(upstream, "ref", name)
                resolved_value = resolve_git_ref(url, ref)
            elif kind == "npm":
                package = require_str(upstream, "package", name)
                registry = registry_override or upstream.get("registry")
                if registry is not None and not isinstance(registry, str):
                    raise RuntimeError(f"{name}.registry must be a string when present")
                resolved_value = resolve_npm_version(package, registry)
            else:
                raise RuntimeError(f"{name}.type must be `git` or `npm`")
        except RuntimeError as exc:
            errors.append(str(exc))
            continue

        resolved.append(
            {
                "name": name,
                "type": kind,
                "source": upstream,
                "resolved": resolved_value,
            }
        )

    if errors:
        raise SystemExit("Unable to resolve upstreams:\n- " + "\n- ".join(errors))

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "upstreams": resolved,
    }


def require_str(payload: dict[str, Any], key: str, name: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"{name}.{key} must be a non-empty string")
    return value


def index_lock(lock_payload: dict[str, Any]) -> dict[str, str]:
    indexed: dict[str, str] = {}
    upstreams = lock_payload.get("upstreams", [])
    if isinstance(upstreams, list):
        for upstream in upstreams:
            if isinstance(upstream, dict):
                name = upstream.get("name")
                resolved = upstream.get("resolved")
                if isinstance(name, str) and isinstance(resolved, str):
                    indexed[name] = resolved
    return indexed


def build_upgrade_report(
    config_path: Path,
    previous_lock: dict[str, Any] | None,
    current_lock: dict[str, Any],
) -> str:
    previous = index_lock(previous_lock or {})
    rows: list[str] = []
    changed = False
    for upstream in current_lock["upstreams"]:
        name = upstream["name"]
        current = upstream["resolved"]
        old = previous.get(name)
        if old is None:
            status = "new"
            changed = True
        elif old == current:
            status = "unchanged"
        else:
            status = "changed"
            changed = True
        rows.append(f"| {name} | {status} | `{old or '-'}` | `{current}` |")

    return "\n".join(
        [
            "# OpenPowers Upstream Upgrade Report",
            "",
            f"- Generated: `{current_lock['generated_at']}`",
            f"- Config: `{config_path}`",
            f"- Workflow rules changed automatically: `no`",
            f"- Upstream changes detected: `{'yes' if changed else 'no'}`",
            "",
            "| Upstream | Status | Previous | Current |",
            "| --- | --- | --- | --- |",
            *rows,
            "",
            "## Review checklist",
            "",
            "- Run the OpenSpec upstream updater in the target project only after reviewing this report.",
            "- Keep OpenSpec as the single product specification source.",
            "- Do not copy Superpowers product specs or large prompt bodies into this repository.",
            "- If local workflow rules change, commit the diff and explain it in `CHANGELOG.md`.",
            "- Open a PR for any lock, script, skill, or AGENTS.md change before installing it broadly.",
            "",
        ]
    )


def build_upgrade_changelog(previous_lock: dict[str, Any] | None, current_lock: dict[str, Any]) -> str:
    previous = index_lock(previous_lock or {})
    lines = [
        "# OpenPowers Upgrade Changelog",
        "",
        f"## {current_lock['generated_at']}",
        "",
    ]
    for upstream in current_lock["upstreams"]:
        name = upstream["name"]
        current = upstream["resolved"]
        old = previous.get(name)
        if old is None:
            lines.append(f"- Track `{name}` at `{current}`.")
        elif old == current:
            lines.append(f"- `{name}` unchanged at `{current}`.")
        else:
            lines.append(f"- `{name}` changed from `{old}` to `{current}`.")
    lines.extend(
        [
            "",
            "No local workflow rules were changed by this command.",
            "",
        ]
    )
    return "\n".join(lines)


def check_path_exists(root: Path, relative: str, label: str) -> CheckResult:
    path = root / relative
    if path.exists():
        return CheckResult("ok", f"{label}: {relative}")
    return CheckResult("fail", f"{label} missing: {relative}")


def verify_repo(root: Path) -> list[CheckResult]:
    checks: list[CheckResult] = [
        check_path_exists(root, "README.md", "README"),
        check_path_exists(root, "AGENTS.md", "repository agent rules"),
        check_path_exists(root, "templates/AGENTS.openpowers.md", "consumer AGENTS template"),
        check_path_exists(root, "plugins/openpowers/.codex-plugin/plugin.json", "plugin manifest"),
        check_path_exists(root, "plugins/openpowers/skills/openpowers-lite/SKILL.md", "skill"),
        check_path_exists(root, ".agents/plugins/marketplace.json", "marketplace"),
        check_path_exists(root, ".openpowers/upstreams.json", "upstream config"),
        check_path_exists(root, ".openpowers/upstreams.lock.json", "upstream lock"),
    ]

    checks.extend(verify_plugin_manifest(root))
    checks.extend(verify_skill_contract(root))
    checks.extend(verify_no_duplicate_product_specs(root))
    checks.extend(verify_no_todo_markers(root))
    return checks


def verify_plugin_manifest(root: Path) -> list[CheckResult]:
    manifest_path = root / "plugins/openpowers/.codex-plugin/plugin.json"
    marketplace_path = root / ".agents/plugins/marketplace.json"
    results: list[CheckResult] = []
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        if manifest.get("name") == "openpowers":
            results.append(CheckResult("ok", "plugin manifest name is openpowers"))
        else:
            results.append(CheckResult("fail", "plugin manifest name must be openpowers"))
        if manifest.get("skills") == "./skills/":
            results.append(CheckResult("ok", "plugin exposes skills directory"))
        else:
            results.append(CheckResult("fail", "plugin manifest must expose ./skills/"))
    if marketplace_path.exists():
        marketplace = load_json(marketplace_path)
        entries = marketplace.get("plugins", [])
        matching = [entry for entry in entries if isinstance(entry, dict) and entry.get("name") == "openpowers"]
        if matching and matching[0].get("source", {}).get("path") == "./plugins/openpowers":
            results.append(CheckResult("ok", "marketplace points at ./plugins/openpowers"))
        else:
            results.append(CheckResult("fail", "marketplace must include openpowers at ./plugins/openpowers"))
    return results


def verify_skill_contract(root: Path) -> list[CheckResult]:
    skill_path = root / "plugins/openpowers/skills/openpowers-lite/SKILL.md"
    if not skill_path.exists():
        return []
    text = skill_path.read_text(encoding="utf-8")
    required_phrases = [
        "OpenSpec owns WHAT",
        "Superpowers Lite guards HOW",
        "AGENTS.md decides WHEN",
        "Do not create product specifications outside OpenSpec",
    ]
    results = []
    for phrase in required_phrases:
        if phrase in text:
            results.append(CheckResult("ok", f"skill states invariant: {phrase}"))
        else:
            results.append(CheckResult("fail", f"skill missing invariant: {phrase}"))
    return results


def verify_no_duplicate_product_specs(root: Path) -> list[CheckResult]:
    forbidden = [
        ".openpowers/specs",
        "superpowers/specs",
        ".superpowers/specs",
        "plugins/openpowers/specs",
    ]
    found = [relative for relative in forbidden if (root / relative).exists()]
    if found:
        return [CheckResult("fail", "duplicate product spec locations found: " + ", ".join(found))]
    return [CheckResult("ok", "no OpenPowers/Superpowers product spec directories found")]


def verify_no_todo_markers(root: Path) -> list[CheckResult]:
    candidates = [
        root / "README.md",
        root / "AGENTS.md",
        root / "plugins/openpowers/.codex-plugin/plugin.json",
        root / "plugins/openpowers/skills/openpowers-lite/SKILL.md",
    ]
    offenders: list[str] = []
    for path in candidates:
        if path.exists() and "[TODO:" in path.read_text(encoding="utf-8"):
            offenders.append(str(path.relative_to(root)))
    if offenders:
        return [CheckResult("fail", "TODO placeholders remain: " + ", ".join(offenders))]
    return [CheckResult("ok", "no scaffold TODO placeholders in primary files")]


def cmd_verify(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    results = verify_repo(root)
    for result in results:
        prefix = "OK" if result.status == "ok" else "FAIL"
        print(f"[{prefix}] {result.message}")
    return 1 if any(result.status == "fail" for result in results) else 0


def cmd_upgrade_check(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    config_path = root / args.config
    lock_path = root / args.lock
    report_path = root / args.report
    changelog_path = root / args.changelog

    if args.branch:
        run_command(["git", "checkout", "-b", args.branch], cwd=root)

    config = load_json(config_path)
    previous_lock = load_json(lock_path) if lock_path.exists() else None
    current_lock = resolve_upstreams(config, args.npm_registry)

    report = build_upgrade_report(config_path.relative_to(root), previous_lock, current_lock)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    if args.write_lock:
        write_json(lock_path, current_lock)
        changelog_path.write_text(build_upgrade_changelog(previous_lock, current_lock), encoding="utf-8")

    print(f"Wrote report: {report_path}")
    if args.write_lock:
        print(f"Wrote lock: {lock_path}")
        print(f"Wrote changelog: {changelog_path}")
        print("Review with: git diff -- .openpowers")
    else:
        print("Lock unchanged. Re-run with --write-lock to create a reviewable diff.")

    if args.commit:
        if not args.write_lock:
            raise SystemExit("--commit requires --write-lock")
        run_command(["git", "add", str(lock_path), str(report_path), str(changelog_path)], cwd=root)
        run_command(["git", "commit", "-m", args.commit], cwd=root)
        print(f"Created commit: {args.commit}")

    if args.pr:
        if not args.commit:
            raise SystemExit("--pr requires --commit")
        run_command(["gh", "pr", "create", "--fill"], cwd=root)
        print("Created GitHub pull request with gh.")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="OpenPowers Lite repository verification and upstream audit tooling."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify = subparsers.add_parser("verify", help="Check repository/plugin invariants")
    verify.add_argument("--root", default=".", help="Repository root to check")
    verify.set_defaults(func=cmd_verify)

    upgrade = subparsers.add_parser("upgrade-check", help="Resolve upstream refs and write an audit report")
    upgrade.add_argument("--root", default=".", help="Repository root")
    upgrade.add_argument("--config", default=str(DEFAULT_CONFIG), help="Upstream config path")
    upgrade.add_argument("--lock", default=str(DEFAULT_LOCK), help="Upstream lock path")
    upgrade.add_argument("--report", default=str(DEFAULT_REPORT), help="Markdown report path")
    upgrade.add_argument("--changelog", default=str(DEFAULT_CHANGELOG), help="Generated changelog path")
    upgrade.add_argument("--npm-registry", help="Override npm registry for npm upstream checks")
    upgrade.add_argument("--write-lock", action="store_true", help="Update lock and changelog files")
    upgrade.add_argument("--branch", help="Create and switch to a review branch before writing files")
    upgrade.add_argument("--commit", help="Commit generated upgrade files with this message")
    upgrade.add_argument("--pr", action="store_true", help="Create a GitHub PR with gh after committing")
    upgrade.set_defaults(func=cmd_upgrade_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
