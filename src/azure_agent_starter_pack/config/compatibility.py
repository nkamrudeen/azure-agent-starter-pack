"""Compatibility matrix: valid (framework, project_type, pipeline, runtime, iac) combinations."""

from itertools import product

from azure_agent_starter_pack.config.schema import (
    FRAMEWORKS,
    IAC_OPTIONS,
    PIPELINES,
    PROJECT_TYPES,
    RUNTIMES,
)

# Full cartesian product of all supported options is valid.
# If specific combos need to be excluded later, subtract them here.
_VALID_COMBINATIONS: set[tuple[str, str, str, str, str]] = set(
    product(FRAMEWORKS, PROJECT_TYPES, PIPELINES, RUNTIMES, IAC_OPTIONS)
)


class InvalidCombinationError(ValueError):
    """Raised when (framework, project_type, pipeline, runtime, iac) is not supported."""

    def __init__(self, framework: str, project_type: str, pipeline: str, runtime: str, iac: str) -> None:
        self.framework = framework
        self.project_type = project_type
        self.pipeline = pipeline
        self.runtime = runtime
        self.iac = iac
        super().__init__(
            f"Unsupported combination: framework={framework!r}, project_type={project_type!r}, "
            f"pipeline={pipeline!r}, runtime={runtime!r}, iac={iac!r}."
        )


def validate_combination(
    framework: str,
    project_type: str,
    pipeline: str,
    runtime: str,
    iac: str,
) -> None:
    """Validate that the combination is supported. Raises InvalidCombinationError if not (FR-022)."""
    key = (framework, project_type, pipeline, runtime, iac)
    if key not in _VALID_COMBINATIONS:
        raise InvalidCombinationError(framework, project_type, pipeline, runtime, iac)


def is_valid_combination(
    framework: str,
    project_type: str,
    pipeline: str,
    runtime: str,
    iac: str,
) -> bool:
    """Return True if the combination is supported."""
    return (framework, project_type, pipeline, runtime, iac) in _VALID_COMBINATIONS
