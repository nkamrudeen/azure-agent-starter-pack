"""Typer app entrypoint: azure-agent-starter-pack."""

import typer

from azure_agent_starter_pack.cli.doctor_cmd import run_doctor
from azure_agent_starter_pack.cli.init_cmd import run_init
from azure_agent_starter_pack.cli.upgrade_cmd import run_upgrade

app = typer.Typer(
    name="azure-agent-starter-pack",
    help="Scaffold Azure AI Agent projects with configurable options.",
)


@app.command()
def init(
    target_dir: str = typer.Argument(
        ".",
        help="Target directory for the new project.",
    ),
    framework: str = typer.Option(None, "--framework", "-f", help="Agent framework"),
    project_type: str = typer.Option(None, "--project-type", "-p", help="Project type"),
    pipeline: str = typer.Option(None, "--pipeline", help="CI/CD pipeline"),
    runtime: str = typer.Option(None, "--runtime", "-r", help="Runtime environment"),
    iac: str = typer.Option(None, "--iac", help="Infrastructure as Code"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Allow non-empty directory"),
    non_interactive: bool = typer.Option(
        False, "--non-interactive", help="Fail if option missing; no prompts"
    ),
    template_version: str = typer.Option(
        None, "--template-version", help="Template version (semver or tag)"
    ),
) -> None:
    """Scaffold a new Azure AI Agent project."""
    run_init(
        target_dir=target_dir,
        framework=framework,
        project_type=project_type,
        pipeline=pipeline,
        runtime=runtime,
        iac=iac,
        overwrite=overwrite,
        non_interactive=non_interactive,
        template_version=template_version,
    )


@app.command()
def upgrade(
    project_root: str = typer.Argument(
        ".",
        help="Project root of scaffolded project.",
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Report changes only"),
) -> None:
    """Update a scaffolded project to a newer template version."""
    run_upgrade(project_root=project_root, dry_run=dry_run)


@app.command()
def doctor() -> None:
    """Validate environment and configuration for init."""
    run_doctor()


if __name__ == "__main__":
    app()
