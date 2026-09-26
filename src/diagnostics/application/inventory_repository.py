from pathlib import Path

from diagnostics.domain.models import InventoryConfig, InventoryResult, RunStatus
from diagnostics.domain.ports import RepositoryScanner
from diagnostics.infrastructure.dotnet_detector import DotNetDetector


class InventoryRepository:
    def __init__(self, scanner: RepositoryScanner, detector: DotNetDetector | None = None) -> None:
        self._scanner = scanner
        self._detector = detector or DotNetDetector()

    def execute(self, repository_root: Path, config: InventoryConfig) -> InventoryResult:
        inventory = self._scanner.scan(repository_root, config)
        detection = self._detector.detect(inventory)
        if inventory.is_partial:
            return InventoryResult(inventory, detection, RunStatus.PARTIAL)
        if not detection.project_files:
            return InventoryResult(inventory, detection, RunStatus.UNSUPPORTED, "NO_ELIGIBLE_CSPROJ")
        return InventoryResult(inventory, detection, RunStatus.COMPLETED)
