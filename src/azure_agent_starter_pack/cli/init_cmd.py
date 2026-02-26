"""Init subcommand: scaffold a new Azure AI Agent project."""

import json
import os
import sys
from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from azure_agent_starter_pack.adapters.registry import (
    get_framework_adapter,
    get_pipeline_generator,
    get_project_type_generator,
    get_runtime_adapter,
)
from azure_agent_starter_pack.config.compatibility import (
    InvalidCombinationError,
    validate_combination,
)
from azure_agent_starter_pack.config.schema import (
    FRAMEWORKS,
    IAC_OPTIONS,
    PIPELINES,
    PROJECT_TYPES,
    RUNTIMES,
    ProjectConfig,
)
from azure_agent_starter_pack.render.loader import load_templates
from azure_agent_starter_pack.render.renderer import render_tree

console = Console(stderr=True)

_MANIFEST_DIR = ".azure-agent-starter-pack"
_MANIFEST_FILE = "manifest.json"


def _is_interactive() -> bool:
    return sys.stdin.isatty()


def _prompt_choice(label: str, choices: tuple[str, ...]) -> str:
    """Prompt user to pick from choices (interactive only)."""
    console.print(f"\n[bold]{label}[/bold]")
    for i, c in enumerate(choices, 1):
        console.print(f"  {i}) {c}")
    while True:
        raw = input(f"Enter number (1-{len(choices)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            return choices[int(raw) - 1]
        console.print("[red]Invalid choice, try again.[/red]")


def _resolve_option(
    value: str | None,
    env_key: str,
    label: str,
    choices: tuple[str, ...],
    non_interactive: bool,
) -> str:
    """Resolve an option from flag, env, or interactive prompt."""
    if value is not None:
        return value
    env_val = os.environ.get(env_key)
    if env_val is not None:
        return env_val
    if non_interactive or not _is_interactive():
        console.print(f"[red]Error: --{label.lower().replace(' ', '-')} is required in non-interactive mode.[/red]")
        raise typer.Exit(code=1)
    return _prompt_choice(label, choices)


def _validate_target_dir(target: Path, overwrite: bool) -> None:
    """FR-021: require empty directory or --overwrite."""
    target.mkdir(parents=True, exist_ok=True)
    if any(target.iterdir()) and not overwrite:
        console.print(
            f"[red]Error: Target directory '{target}' is not empty. "
            "Use --overwrite to allow writing into a non-empty directory.[/red]"
        )
        raise typer.Exit(code=1)


def _write_manifest(output_root: Path, config: ProjectConfig, written: list[Path]) -> None:
    """Write manifest.json for upgrade command."""
    manifest_dir = output_root / _MANIFEST_DIR
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "schema_version": "1",
        "cli_tool": "azure-agent-starter-pack",
        "cli_version": "0.1.0",
        "template_version": config.template_version or "1.0.0",
        "config": {
            "framework": config.framework,
            "project_type": config.project_type,
            "pipeline": config.pipeline,
            "runtime": config.runtime,
            "iac": config.iac,
        },
        "owned_paths": sorted(str(p) for p in written),
    }
    (manifest_dir / _MANIFEST_FILE).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def run_init(
    target_dir: str,
    framework: str | None,
    project_type: str | None,
    pipeline: str | None,
    runtime: str | None,
    iac: str | None,
    overwrite: bool,
    non_interactive: bool,
    template_version: str | None = None,
) -> None:
    """Core init logic, separated from Typer for testability."""
    is_ni = non_interactive or not _is_interactive()

    fw = _resolve_option(framework, "AASP_FRAMEWORK", "Framework", FRAMEWORKS, is_ni)
    pt = _resolve_option(project_type, "AASP_PROJECT_TYPE", "Project type", PROJECT_TYPES, is_ni)
    pl = _resolve_option(pipeline, "AASP_PIPELINE", "Pipeline", PIPELINES, is_ni)
    rt = _resolve_option(runtime, "AASP_RUNTIME", "Runtime", RUNTIMES, is_ni)
    ic = _resolve_option(iac, "AASP_IAC", "IaC", IAC_OPTIONS, is_ni)

    try:
        validate_combination(fw, pt, pl, rt, ic)
    except InvalidCombinationError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1) from e

    target = Path(target_dir).resolve()
    _validate_target_dir(target, overwrite)

    config = ProjectConfig(
        framework=fw,
        project_type=pt,
        pipeline=pl,
        runtime=rt,
        iac=ic,
        target_dir=target,
        template_version=template_version,
        overwrite=overwrite,
        non_interactive=is_ni,
    )

    templates_root = load_templates(config.template_version)

    # Resolve adapters and merge context
    context: dict[str, Any] = {
        "framework": config.framework,
        "project_type": config.project_type,
        "pipeline": config.pipeline,
        "runtime": config.runtime,
        "iac": config.iac,
        "project_name": target.name or "azure-ai-agent",
    }
    try:
        fw_adapter = get_framework_adapter(config.framework)
        context.update(fw_adapter.get_context())
    except KeyError:
        pass
    try:
        pt_gen = get_project_type_generator(config.project_type)
        context.update(pt_gen.get_context())
    except KeyError:
        pass
    try:
        rt_adapter = get_runtime_adapter(config.runtime)
        context.update(rt_adapter.get_context())
    except KeyError:
        pass
    try:
        pl_gen = get_pipeline_generator(config.pipeline)
        context.update(pl_gen.get_context())
    except KeyError:
        pass

    written: list[Path] = []

    # 1) Render shared _common/ templates (config, identity, observability, pyproject, run.py)
    common_root = templates_root / "_common"
    if common_root.is_dir():
        written.extend(render_tree(common_root, context, target))

    # 2) Render self-contained framework/project_type templates
    combo_root = templates_root / config.framework / config.project_type
    if combo_root.is_dir():
        written.extend(render_tree(combo_root, context, target))
    else:
        console.print(
            f"[red]Error: No template found for {config.framework}/{config.project_type}[/red]"
        )
        raise typer.Exit(code=1)

    # 3) Layer IaC overlay
    iac_overlay = templates_root / "iac" / config.iac
    if iac_overlay.is_dir():
        written.extend(render_tree(iac_overlay, context, target))

    # 4) Layer runtime overlay
    rt_overlay = templates_root / "runtimes" / config.runtime
    if rt_overlay.is_dir():
        written.extend(render_tree(rt_overlay, context, target))

    # 5) Layer pipeline overlay
    pl_overlay = templates_root / "pipelines" / config.pipeline
    if pl_overlay.is_dir():
        written.extend(render_tree(pl_overlay, context, target))

    # Deduplicate written paths (overlays may overwrite default files)
    seen: set[str] = set()
    unique_written: list[Path] = []
    for p in written:
        ps = str(p)
        if ps not in seen:
            seen.add(ps)
            unique_written.append(p)
    written = unique_written

    _write_manifest(target, config, written)

    console.print(f"[green]Project scaffolded at {target}[/green]")
    console.print(f"  Framework:    {config.framework}")
    console.print(f"  Project type: {config.project_type}")
    console.print(f"  Pipeline:     {config.pipeline}")
    console.print(f"  Runtime:      {config.runtime}")
    console.print(f"  IaC:          {config.iac}")
    console.print(f"  Files written: {len(written) + 1}")  # +1 for manifest
