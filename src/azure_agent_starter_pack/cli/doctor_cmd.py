"""Doctor subcommand: validate prerequisites for init (US5)."""

import shutil

import typer
from rich.console import Console
from rich.table import Table

console = Console(stderr=True)


def _check_command(name: str) -> bool:
    return shutil.which(name) is not None


def run_doctor() -> None:
    table = Table(title="azure-agent-starter-pack doctor")
    table.add_column("Check", style="bold")
    table.add_column("Status")
    table.add_column("Required")

    checks: list[tuple[str, bool, bool]] = [
        ("Python 3.12+", _check_command("python3") or _check_command("python"), True),
        ("uv", _check_command("uv"), True),
        ("Docker", _check_command("docker"), True),
        ("Azure CLI (az)", _check_command("az"), False),
        ("git", _check_command("git"), False),
    ]

    any_required_failed = False
    for label, ok, required in checks:
        status = "[green]OK[/green]" if ok else ("[red]MISSING[/red]" if required else "[yellow]MISSING[/yellow]")
        req_label = "Required" if required else "Optional"
        table.add_row(label, status, req_label)
        if required and not ok:
            any_required_failed = True

    console.print(table)

    if any_required_failed:
        console.print("[red]One or more required checks failed. Fix the issues above before running init.[/red]")
        raise typer.Exit(code=1)
    else:
        console.print("[green]All required checks passed.[/green]")
