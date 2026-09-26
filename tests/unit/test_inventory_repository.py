from pathlib import Path

from diagnostics.application.inventory_repository import InventoryRepository
from diagnostics.domain.models import EntryKind, InventoryConfig, InventoryEntry, RepositoryInventory, RunStatus


class CompleteSolutionOnlyScanner:
    def scan(self, repository_root: Path, config: InventoryConfig) -> RepositoryInventory:
        return RepositoryInventory("sample", (InventoryEntry("sample.sln", EntryKind.FILE, ".sln"),), (), (), 1, False)


def test_solution_only_inventory_is_unsupported() -> None:
    result = InventoryRepository(CompleteSolutionOnlyScanner()).execute(Path("/repo"), InventoryConfig())

    assert result.status is RunStatus.UNSUPPORTED
    assert result.reason_code == "NO_ELIGIBLE_CSPROJ"
