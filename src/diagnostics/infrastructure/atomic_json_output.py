from __future__ import annotations

import json
import os
from pathlib import Path
from uuid import uuid4

from diagnostics.domain.models import InventoryResult


class AtomicJsonOutput:
    def publish(self, result: InventoryResult, output_root: Path) -> Path:
        raw_root = Path(output_root)
        if raw_root.is_symlink():
            raise ValueError("output root cannot be a symbolic link")
        root = raw_root.resolve(strict=False)

        root.mkdir(parents=True, exist_ok=True)
        run_id = str(uuid4())
        staging = root / f".staging-{run_id}"
        destination = root / run_id
        staging.mkdir()
        try:
            temporary_file = staging / "inventory.json"
            with temporary_file.open("w", encoding="utf-8", newline="\n") as file:
                json.dump(result.to_dict(), file, ensure_ascii=False, indent=2, sort_keys=True)
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary_file, staging / "inventory.json")
            os.replace(staging, destination)
        except Exception:
            if staging.exists():
                for child in staging.iterdir():
                    child.unlink()
                staging.rmdir()
            raise
        return destination / "inventory.json"
