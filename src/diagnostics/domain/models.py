from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import PurePosixPath


DEFAULT_IGNORED_DIRECTORY_NAMES = frozenset(
    {
        ".git",
        ".idea",
        ".venv",
        ".vs",
        "__pycache__",
        "bin",
        "build",
        "dist",
        "node_modules",
        "obj",
        "vendor",
        "venv",
    }
)


class EntryKind(str, Enum):
    FILE = "FILE"
    DIRECTORY = "DIRECTORY"
    SYMLINK = "SYMLINK"
    OTHER = "OTHER"


class RunStatus(str, Enum):
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    UNSUPPORTED = "UNSUPPORTED"
    FAILED = "FAILED"


def _relative_path(value: str, field_name: str = "relative_path") -> str:
    if not isinstance(value, str) or not value.strip() or "\\" in value:
        raise ValueError(f"{field_name} must be a non-empty POSIX relative path")

    path = PurePosixPath(value)
    if path.is_absolute() or value == "." or ".." in path.parts:
        raise ValueError(f"{field_name} must be relative and cannot contain '..'")
    return path.as_posix()


@dataclass(frozen=True, slots=True)
class InventoryConfig:
    ignore_directory_names: frozenset[str] = DEFAULT_IGNORED_DIRECTORY_NAMES
    exclude_patterns: tuple[str, ...] = ()
    max_entries: int = 50_000
    max_manifest_bytes: int = 2 * 1024 * 1024

    def __post_init__(self) -> None:
        if self.max_entries <= 0:
            raise ValueError("max_entries must be positive")
        if self.max_manifest_bytes <= 0:
            raise ValueError("max_manifest_bytes must be positive")
        object.__setattr__(self, "ignore_directory_names", frozenset(self.ignore_directory_names))
        object.__setattr__(self, "exclude_patterns", tuple(self.exclude_patterns))


@dataclass(frozen=True, slots=True)
class InventoryEntry:
    relative_path: str
    kind: EntryKind
    extension: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "relative_path", _relative_path(self.relative_path))
        if self.extension is not None and not self.extension.startswith("."):
            raise ValueError("extension must start with '.'")


@dataclass(frozen=True, slots=True)
class Limitation:
    code: str
    message: str
    relative_path: str | None = None

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise ValueError("code must not be blank")
        if not self.message.strip():
            raise ValueError("message must not be blank")
        if self.relative_path is not None:
            object.__setattr__(self, "relative_path", _relative_path(self.relative_path))


@dataclass(frozen=True, slots=True)
class RepositoryInventory:
    repository_name: str
    entries: tuple[InventoryEntry, ...]
    exclusions: tuple[str, ...]
    limitations: tuple[Limitation, ...]
    visited_count: int
    is_partial: bool

    def __post_init__(self) -> None:
        if not self.repository_name.strip():
            raise ValueError("repository_name must not be blank")
        if self.visited_count < 0:
            raise ValueError("visited_count cannot be negative")
        object.__setattr__(self, "entries", tuple(self.entries))
        object.__setattr__(self, "exclusions", tuple(self.exclusions))
        object.__setattr__(self, "limitations", tuple(self.limitations))

    def to_dict(self) -> dict[str, object]:
        return {
            "repository_name": self.repository_name,
            "entries": [
                {
                    "relative_path": entry.relative_path,
                    "kind": entry.kind.value,
                    "extension": entry.extension,
                }
                for entry in self.entries
            ],
            "exclusions": list(self.exclusions),
            "limitations": [
                {
                    "code": limitation.code,
                    "message": limitation.message,
                    "relative_path": limitation.relative_path,
                }
                for limitation in self.limitations
            ],
            "visited_count": self.visited_count,
            "is_partial": self.is_partial,
        }


@dataclass(frozen=True, slots=True)
class DotNetDetection:
    stack_signals: tuple[str, ...] = ()
    project_files: tuple[str, ...] = ()
    solution_files: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "stack_signals", tuple(self.stack_signals))
        object.__setattr__(self, "project_files", tuple(_relative_path(path) for path in self.project_files))
        object.__setattr__(self, "solution_files", tuple(_relative_path(path) for path in self.solution_files))


@dataclass(frozen=True, slots=True)
class InventoryResult:
    inventory: RepositoryInventory
    detection: DotNetDetection
    status: RunStatus
    reason_code: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "inventory": self.inventory.to_dict(),
            "detection": {
                "stack_signals": list(self.detection.stack_signals),
                "project_files": list(self.detection.project_files),
                "solution_files": list(self.detection.solution_files),
            },
            "status": self.status.value,
            "reason_code": self.reason_code,
        }
