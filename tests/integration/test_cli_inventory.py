from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import json

import pytest


def test_analyze_requires_repo_argument() -> None:
    repository_root = Path(__file__).parents[2]
    environment = os.environ | {
        "PYTHONPATH": str(repository_root / "src")
        + os.pathsep
        + os.environ.get("PYTHONPATH", "")
    }
    result = subprocess.run(
        [sys.executable, "-m", "diagnostics.cli", "analyze"],
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )

    assert result.returncode == 2
    assert "--repo" in result.stderr


def test_analyze_publishes_inventory_for_a_dotnet_project(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    output = tmp_path / "output"
    repository.mkdir()
    (repository / "App.csproj").write_text("not read", encoding="utf-8")

    result = _run_cli("analyze", "--repo", str(repository), "--output", str(output))

    run_files = list(output.glob("*/inventory.json"))
    assert result.returncode == 0, result.stderr
    assert len(run_files) == 1
    assert json.loads(run_files[0].read_text(encoding="utf-8"))["inventory"]["repository_name"] == "repository"
    assert all(
        not entry["relative_path"].startswith("/")
        for entry in json.loads(run_files[0].read_text(encoding="utf-8"))["inventory"]["entries"]
    )


def test_analyze_rejects_output_inside_repository(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()

    result = _run_cli("analyze", "--repo", str(repository), "--output", str(repository / "results"))

    assert result.returncode == 2
    assert not (repository / "results").exists()


def test_analyze_publishes_unsupported_solution_only_result(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    output = tmp_path / "output"
    repository.mkdir()
    (repository / "App.sln").write_text("not read", encoding="utf-8")

    result = _run_cli("analyze", "--repo", str(repository), "--output", str(output))

    [run_file] = output.glob("*/inventory.json")
    assert result.returncode == 3
    assert json.loads(run_file.read_text(encoding="utf-8"))["status"] == "UNSUPPORTED"


def test_analyze_rejects_symbolic_link_inputs_before_resolution(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    (repository / "App.csproj").write_text("not read", encoding="utf-8")
    repository_link = tmp_path / "repository-link"
    output_link = tmp_path / "output-link"
    try:
        repository_link.symlink_to(repository, target_is_directory=True)
        output_link.symlink_to(tmp_path / "published", target_is_directory=True)
    except OSError as error:
        pytest.skip(f"symlinks are unavailable: {error}")

    assert _run_cli("analyze", "--repo", str(repository_link), "--output", str(tmp_path / "output")).returncode == 2
    assert _run_cli("analyze", "--repo", str(repository), "--output", str(output_link)).returncode == 2


def _run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    repository_root = Path(__file__).parents[2]
    environment = os.environ | {
        "PYTHONPATH": str(repository_root / "src")
        + os.pathsep
        + os.environ.get("PYTHONPATH", "")
    }
    return subprocess.run(
        [sys.executable, "-m", "diagnostics.cli", *arguments],
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )
