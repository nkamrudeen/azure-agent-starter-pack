"""Jinja2 renderer: deterministic output, sorted file order (NFR-001)."""

import shutil
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_tree(template_root: Path, context: dict[str, Any], output_root: Path) -> list[Path]:
    """
    Render template tree under template_root into output_root with context.
    .j2 files are rendered and written without the .j2 suffix.
    All other files are copied as-is.
    Returns list of written file paths (relative to output_root).
    """
    env = Environment(
        loader=FileSystemLoader(str(template_root)),
        autoescape=select_autoescape(),
        keep_trailing_newline=True,
    )
    written: list[Path] = []
    for path in sorted(template_root.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(template_root)
        if rel.suffix == ".j2":
            out_rel = rel.with_suffix("")
            template_name = str(rel.as_posix())
            try:
                tmpl = env.get_template(template_name)
                content = tmpl.render(**context)
            except Exception:
                continue
            out_path = output_root / out_rel
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(content, encoding="utf-8")
            written.append(out_rel)
        else:
            out_path = output_root / rel
            out_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, out_path)
            written.append(rel)
    return written
