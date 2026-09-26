from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from diagnostics.domain.models import (
    DotNetDetection,
    EntryKind,
    InventoryConfig,
    InventoryEntry,
    RepositoryInventory,
    RunStatus,
)


def test_inventory_config_is_immutable() -> None:
    config = InventoryConfig()

    with pytest.raises(FrozenInstanceError):
        config.max_entries = 1  # type: ignore[misc]


def test_inventory_config_rejects_a_non_positive_entry_limit() -> None:
    with pytest.raises(ValueError, match="max_entries"):
        InventoryConfig(max_entries=0)


def test_inventory_serialization_contains_only_relative_paths() -> None:
    inventory = RepositoryInventory(
        repository_name="sample",
        entries=(InventoryEntry("src/App.csproj", EntryKind.FILE, ".csproj"),),
        exclusions=("bin",),
        limitations=(),
        visited_count=1,
        is_partial=False,
    )

    assert inventory.to_dict() == {
        "repository_name": "sample",
        "entries": [
            {"relative_path": "src/App.csproj", "kind": "FILE", "extension": ".csproj"}
        ],
        "exclusions": ["bin"],
        "limitations": [],
        "visited_count": 1,
        "is_partial": False,
    }


def test_run_status_has_only_the_documented_values() -> None:
    assert {status.value for status in RunStatus} == {
        "COMPLETED",
        "PARTIAL",
        "UNSUPPORTED",
        "FAILED",
    }


@pytest.mark.parametrize("path", ["/private/file.csproj", "../outside.csproj", "src/../file.csproj"])
def test_inventory_entry_rejects_absolute_or_parent_relative_paths(path: str) -> None:
    with pytest.raises(ValueError, match="relative_path"):
        InventoryEntry(path, EntryKind.FILE)
