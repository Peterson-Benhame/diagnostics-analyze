from __future__ import annotations

import os
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from diagnostics.domain.models import (
    EntryKind,
    InventoryConfig,
    InventoryEntry,
    Limitation,
    RepositoryInventory,
)


@dataclass(slots=True)
class _ScanState:
    visited_count: int = 0
    stopped: bool = False


class LocalRepositoryScanner:
    """Inventories filesystem metadata without opening repository files."""

    def scan(self, repository_root: Path, config: InventoryConfig) -> RepositoryInventory:
        root_input = Path(repository_root)
        try:
            root_status = root_input.lstat()
        except OSError as error:
            raise ValueError("repository root is not readable") from error

        if self._is_redirect(root_status):
            raise ValueError("repository root cannot be a symbolic link or redirect")
        if not stat.S_ISDIR(root_status.st_mode):
            raise ValueError("repository root must be a directory")

        root = root_input.resolve(strict=True)
        entries: list[InventoryEntry] = []
        limitations: list[Limitation] = []
        state = _ScanState()
        self._scan_directory(root, root, config, entries, limitations, state)
        return RepositoryInventory(
            repository_name=root.name,
            entries=tuple(entries),
            exclusions=tuple(config.exclude_patterns),
            limitations=tuple(limitations),
            visited_count=state.visited_count,
            is_partial=bool(limitations),
        )

    def _scan_directory(
        self,
        root: Path,
        directory: Path,
        config: InventoryConfig,
        entries: list[InventoryEntry],
        limitations: list[Limitation],
        state: _ScanState,
    ) -> None:
        try:
            children = directory.iterdir()
        except OSError as error:
            limitations.append(
                Limitation("DIRECTORY_UNREADABLE", "Directory metadata could not be read.")
            )
            return

        for child in children:
            if state.stopped:
                return
            relative_path = self._relative_path(root, child)
            state.visited_count += 1
            if state.visited_count > config.max_entries:
                limitations.append(
                    Limitation(
                        "ENTRY_LIMIT_REACHED",
                        f"Repository inventory exceeded {config.max_entries} entries.",
                    )
                )
                state.stopped = True
                return
            try:
                child_status = child.lstat()
            except OSError:
                limitations.append(Limitation("ENTRY_UNREADABLE", "Entry metadata could not be read.", relative_path))
                continue

            if self._is_redirect(child_status):
                limitations.append(
                    Limitation("SYMLINK_SKIPPED", "Symbolic links are not followed.", relative_path)
                )
                continue

            if stat.S_ISDIR(child_status.st_mode):
                if child.name in config.ignore_directory_names:
                    continue
                if self._is_excluded(relative_path, config.exclude_patterns):
                    continue
                entries.append(InventoryEntry(relative_path, EntryKind.DIRECTORY))
                self._scan_directory(root, child, config, entries, limitations, state)
                continue

            if stat.S_ISREG(child_status.st_mode):
                if self._is_excluded(relative_path, config.exclude_patterns):
                    continue
                entries.append(InventoryEntry(relative_path, EntryKind.FILE, child.suffix.lower() or None))
                continue

            entries.append(InventoryEntry(relative_path, EntryKind.OTHER))

    @staticmethod
    def _relative_path(root: Path, path: Path) -> str:
        relative = path.relative_to(root)
        normalized = PurePosixPath(*relative.parts)
        if normalized.is_absolute() or ".." in normalized.parts:
            raise ValueError("path escapes repository root")
        return normalized.as_posix()

    @staticmethod
    def _is_excluded(relative_path: str, patterns: tuple[str, ...]) -> bool:
        candidate = PurePosixPath(relative_path)
        for pattern in patterns:
            if candidate.match(pattern):
                return True
            if pattern.endswith("/**") and candidate == PurePosixPath(pattern[:-3]):
                return True
        return False

    @staticmethod
    def _is_redirect(file_status: os.stat_result) -> bool:
        reparse_point = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        attributes = getattr(file_status, "st_file_attributes", 0)
        return stat.S_ISLNK(file_status.st_mode) or bool(attributes & reparse_point)
