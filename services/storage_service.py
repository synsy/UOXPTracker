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
        """
        path = self._config.file_path
        if not path.exists():
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    def append_record(self, record: Dict[str, Any]) -> None:
        """
        Append a single record to history and persist it.
        """
        history = self.load_history()
        history.append(record)
        self.save_history(history)

    def save_history(self, records: List[Dict[str, Any]]) -> None:
        """
        Save entire history list (overwrite) in a safe way.
        """
        path = self._config.file_path
        temp_path = path.with_suffix(".tmp")

        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

        temp_path.replace(path)

    # -------------------------
    # Convenience helpers
    # -------------------------

    def clear_history(self) -> None:
        """
        Remove all records (or delete file). Useful for a 'Clear' button later.
        """
        # TODO: choose either delete file or write empty list
        #raise NotImplementedError
        pass

    def file_exists(self) -> bool:
        return self._config.file_path.exists()

    # -------------------------
    # Internal helpers
    # -------------------------

    def _ensure_data_dir(self) -> None:
        # Create the data directory if missing.
        self._config.data_dir.mkdir(parents=True, exist_ok=True)
