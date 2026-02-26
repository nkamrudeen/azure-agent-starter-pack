"""Upgrade subcommand: apply template updates to an existing scaffolded project (US2)."""

import json
from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from azure_agent_starter_pack.render.loader import load_templates
from azure_agent_starter_pack.render.renderer import render_tree

console = Console(stderr=True)

_MANIFEST_DIR = ".azure-agent-starter-pack"
_MANIFEST_FILE = "manifest.json"


def _load_manifest(project_root: Path) -> dict[str, Any]:
    manifest_path = project_root / _MANIFEST_DIR / _MANIFEST_FILE
    if not manifest_path.is_file():
        console.print(
            f"[red]Error: No manifest found at {manifest_path}. "
            "Is this a project scaffolded by azure-agent-starter-pack?[/red]"
        )
        raise typer.Exit(code=1)
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def run_upgrade(project_root: str, dry_run: bool) -> None:
    root = Path(project_root).resolve()
    manifest = _load_manifest(root)
    config = manifest.get("config", {})
    old_version = manifest.get("template_version", "unknown")

    try:
        template_root = load_templates(None)
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1) from e

    new_version = "unknown"
    version_file = template_root / "version.txt"
    if version_file.is_file():
        new_version = version_file.read_text(encoding="utf-8").strip()

    if old_version == new_version:
        console.print(f"[green]Already up to date (version {old_version}).[/green]")
        return

    context: dict[str, Any] = {
        "project_name": root.name,
        **config,
    }

    owned_paths = set(manifest.get("owned_paths", []))

    if dry_run:
        console.print(f"[yellow]Dry run: would upgrade from {old_version} → {new_version}[/yellow]")
        console.print(f"  Template-owned paths: {len(owned_paths)}")
        return

    written = render_tree(template_root, context, root)
    updated: list[str] = []
    skipped: list[str] = []
    for p in written:
        ps = str(p)
        if ps in owned_paths or not (root / p).exists():
            updated.append(ps)
        else:
            skipped.append(ps)

    manifest["template_version"] = new_version
    manifest["owned_paths"] = sorted(str(p) for p in written)
    (root / _MANIFEST_DIR / _MANIFEST_FILE).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    console.print(f"[green]Upgraded {old_version} → {new_version}[/green]")
    console.print(f"  Updated: {len(updated)} files")
    if skipped:
        console.print(f"  [yellow]Skipped (user-modified, not template-owned): {len(skipped)} files[/yellow]")
