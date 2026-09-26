from __future__ import annotations

from pathlib import Path

import pytest

from diagnostics.domain.models import InventoryConfig
from diagnostics.infrastructure.local_repository_reader import LocalRepositoryScanner


def test_scan_returns_sorted_metadata_and_skips_ignored_directories(tmp_path: Path) -> None:
    project = tmp_path / "src" / "App"
    (project / "bin").mkdir(parents=True)
    (project / "App.csproj").write_text("not read", encoding="utf-8")
    (project / "bin" / "out.dll").write_bytes(b"not read")

    inventory = LocalRepositoryScanner().scan(tmp_path, InventoryConfig())

    assert [entry.relative_path for entry in inventory.entries] == [
        "src",
        "src/App",
        "src/App/App.csproj",
    ]
    assert inventory.is_partial is False


def test_scan_skips_a_symlink_without_reading_its_target(tmp_path: Path) -> None:
    external = tmp_path.parent / "external.csproj"
    external.write_text("external", encoding="utf-8")
    link = tmp_path / "linked.csproj"
    try:
        link.symlink_to(external)
    except OSError as error:
        pytest.skip(f"symlinks are unavailable: {error}")

    inventory = LocalRepositoryScanner().scan(tmp_path, InventoryConfig())

    assert inventory.entries == ()
    assert [limitation.code for limitation in inventory.limitations] == ["SYMLINK_SKIPPED"]
    assert inventory.limitations[0].relative_path == "linked.csproj"


def test_scan_rejects_a_symlink_as_repository_root(tmp_path: Path) -> None:
    root_link = tmp_path.parent / "root-link"
    try:
        root_link.symlink_to(tmp_path, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"symlinks are unavailable: {error}")

    with pytest.raises(ValueError, match="symbolic link"):
        LocalRepositoryScanner().scan(root_link, InventoryConfig())


def test_scan_stops_once_the_entry_limit_is_reached(tmp_path: Path) -> None:
    # The production default is 50,000 entries; this small limit makes the boundary observable.
    for name in ("a.csproj", "b.csproj", "c.csproj"):
        (tmp_path / name).write_text("not read", encoding="utf-8")

    inventory = LocalRepositoryScanner().scan(tmp_path, InventoryConfig(max_entries=2))

    assert [entry.relative_path for entry in inventory.entries] == ["a.csproj", "b.csproj"]
    assert inventory.is_partial is True
    assert [limitation.code for limitation in inventory.limitations] == ["ENTRY_LIMIT_REACHED"]


def test_scan_omits_custom_excluded_directories(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "examples").mkdir()
    (tmp_path / "src" / "Keep.csproj").write_text("not read", encoding="utf-8")
    (tmp_path / "examples" / "Skip.csproj").write_text("not read", encoding="utf-8")

    inventory = LocalRepositoryScanner().scan(
        tmp_path,
        InventoryConfig(exclude_patterns=("examples/**",)),
    )

    assert [entry.relative_path for entry in inventory.entries] == ["src", "src/Keep.csproj"]
    assert inventory.exclusions == ("examples/**",)
