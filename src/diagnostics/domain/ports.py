from __future__ import annotations

from pathlib import Path
from typing import Protocol

from diagnostics.domain.models import InventoryConfig, RepositoryInventory


class RepositoryScanner(Protocol):
    def scan(self, repository_root: Path, config: InventoryConfig) -> RepositoryInventory: ...
