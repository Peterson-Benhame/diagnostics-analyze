from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from diagnostics.application.inventory_repository import InventoryRepository
from diagnostics.domain.models import InventoryConfig, RunStatus
from diagnostics.infrastructure.atomic_json_output import AtomicJsonOutput
from diagnostics.infrastructure.local_repository_reader import LocalRepositoryScanner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="diagnostics")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("--repo", required=True)
    analyze.add_argument("--output", required=True)
    analyze.add_argument("--exclude", action="append", default=[])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)
    repository = Path(arguments.repo)
    output = Path(arguments.output)
    if repository.is_symlink() or output.is_symlink():
        parser.error("--repo and --output cannot be symbolic links")
    repository_resolved = repository.resolve(strict=False)
    output_resolved = output.resolve(strict=False)
    if output_resolved == repository_resolved or repository_resolved in output_resolved.parents:
        parser.error("--output must be outside --repo")
    try:
        result = InventoryRepository(LocalRepositoryScanner()).execute(
            repository,
            InventoryConfig(exclude_patterns=tuple(arguments.exclude)),
        )
        report_path = AtomicJsonOutput().publish(result, output)
    except ValueError as error:
        parser.error(str(error))
    except OSError as error:
        print(f"operational error: {error}", file=__import__("sys").stderr)
        return 1
    print(report_path)
    return 0 if result.status is RunStatus.COMPLETED else 3


if __name__ == "__main__":
    raise SystemExit(main())
