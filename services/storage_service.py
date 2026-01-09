# services/storage_service.py
#
# Skeleton storage service for a small desktop tool.
# Responsibilities:
# - Know where the JSON file lives
# - Read existing history
# - Append a new record
# - Write back safely
#

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class StorageConfig:
    """
    Centralize where/how data is stored so you don't scatter paths everywhere.
    """
    data_dir: Path
    filename: str = "history.json"

    @property
    def file_path(self) -> Path:
        return self.data_dir / self.filename


class StorageService:
    """
    JSON storage for a simple append-only history log.

    Design notes:
    - Keep the schema simple: a list of dict records.
    - The controller decides *what* the record contains.
    - This service decides *how* it gets persisted.
    """

    def __init__(self, config: StorageConfig):
        self._config = config
        self._ensure_data_dir()

    # -------------------------
    # Public API (controller uses these)
    # -------------------------

    def load_history(self) -> List[Dict[str, Any]]:
        """
        Load and return all saved records.

        Returns:
            A list of record dicts (may be empty).
        """
        # TODO:
        # 1) If file doesn't exist, return []
        # 2) Read JSON
        # 3) Validate basic shape (list)
        # 4) Return list
        raise NotImplementedError

    def append_record(self, record: Dict[str, Any]) -> None:
        """
        Append a single record to history and persist it.

        Args:
            record: dict representing one entry (controller/model provides this)
        """
        # TODO:
        # 1) Load existing history
        # 2) Append record
        # 3) Save updated history
        raise NotImplementedError

    def save_history(self, records: List[Dict[str, Any]]) -> None:
        """
        Save entire history list (overwrite) in a safe way.

        Args:
            records: list of record dicts
        """
        # TODO:
        # 1) Write to a temp file
        # 2) fsync (optional)
        # 3) Atomic replace
        raise NotImplementedError

    # -------------------------
    # Optional convenience helpers
    # -------------------------

    def clear_history(self) -> None:
        """
        Remove all records (or delete file). Useful for a 'Clear' button later.
        """
        # TODO: choose either delete file or write empty list
        raise NotImplementedError

    def file_exists(self) -> bool:
        return self._config.file_path.exists()

    # -------------------------
    # Internal helpers
    # -------------------------

    def _ensure_data_dir(self) -> None:
        """
        Create the data directory if missing.
        """
        # TODO: mkdir(parents=True, exist_ok=True)
        raise NotImplementedError

    def _read_json(self) -> Any:
        """
        Low-level JSON read. Keep it private so you can change format later.
        """
        # TODO: open file_path, json.load
        raise NotImplementedError

    def _write_json_atomic(self, data: Any) -> None:
        """
        Write JSON safely:
        - Write to temp file in same directory
        - Replace the target file
        """
        # TODO:
        # 1) temp_path = file_path.with_suffix(".tmp")
        # 2) json.dump(data, temp file)
        # 3) temp_path.replace(file_path)
        raise NotImplementedError
